#!/usr/bin/env python3
"""voiceover.py — per-beat narration TTS (ElevenLabs).

Vendored/adapted from https://github.com/elevenlabs/skills (MIT,
Copyright (c) 2024 ElevenLabs). Adaptations for this repo: per-beat
synthesis of a markdown narration script, pinned voice/model from
voice_pin.json, 44.1 kHz mono WAV outputs, deterministic concatenation
with a pinned inter-beat gap, and a beat-map for visual sync. MIT
carries no change-note obligation; notes kept anyway.

Transport: REST v1 directly (stable API; request headers give the
audit data — request-id, character count — the SDK swallows).

The committed master wav is the timing source of truth (VIDEO_CONCEPT
§7). Re-generating a voiceover is a deliberate, logged act: the summary
JSON below is the build-log record.

Usage (from repo root):
  python3 videos/pipeline/tts/voiceover.py \
      --script videos/<slug>/narration.md \
      --video-dir videos/<slug> \
      [--voice-id ID] [--model-id ID] [--gap 0.75] \
      [--summary audio/timing/voiceover-summary.json]

Key: ELEVENLABS_API_KEY in the environment, else
~/.config/elevenlabs/api_key (file, 0600; the repo convention —
~/.bashrc early-returns for non-interactive shells, so the env var is
not visible to tool invocations). The key never lands in the repo.

Outputs under <video-dir>/audio/:
  beats/beat-NN.wav             per-beat narration (44.1 kHz mono)
  voiceover.wav                 concatenated master (pinned gap between beats)
  timing/beat-map.json          exact per-beat start/end (ffprobe-derived)
  timing/voiceover-summary.json build-log record (voice/model/settings,
                                chars, request-ids, sha256, durations)
"""
import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path


def _load_key():
    k = os.environ.get("ELEVENLABS_API_KEY")
    if k:
        return k.strip()
    p = Path.home() / ".config" / "elevenlabs" / "api_key"
    if p.exists():
        return p.read_text().strip()
    sys.exit("error: no API key — set ELEVENLABS_API_KEY or write ~/.config/elevenlabs/api_key (0600)")


def _requests():
    try:
        import requests  # noqa: F401
        return
    except ImportError:
        venv = Path(__file__).resolve().parent / ".venv"
        for pydir in sorted((venv / "lib").glob("python*")):
            sp = pydir / "site-packages"
            if sp.exists():
                sys.path.insert(0, str(sp))
        import requests  # noqa: F401
        return
    sys.exit("error: requests not available (rebuild tts/.venv: see requirements.lock.txt)")


def tts_call(key, voice_id, model_id, settings, out_format, text):
    import requests
    r = requests.post(
        f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}?output_format={out_format}",
        headers={"xi-api-key": key},
        json={"text": text, "model_id": model_id, "voice_settings": settings},
        timeout=300,
    )
    if r.status_code != 200:
        sys.exit(f"error: TTS HTTP {r.status_code}: {r.text[:300]}")
    return r.content, dict(r.headers)


def parse_script(text):
    """Parse '## beat-NN' headed markdown into beats.

    Returns [{'id': 'beat-01', 'text': '...'}, ...] in file order.
    Everything from a '## beat' heading to the next '##' heading is the
    beat's text (blank lines dropped, lines joined).
    """
    beats, cur = [], None
    for line in text.splitlines():
        m = re.match(r"^##\s+beat[-_ ]?(\d+)\b", line, re.IGNORECASE)
        if m:
            cur = {"id": f"beat-{int(m.group(1)):02d}", "lines": []}
            beats.append(cur)
            continue
        if re.match(r"^##\s", line):
            cur = None  # a non-beat H2 ends beat collection
            continue
        if cur is not None:
            cur["lines"].append(line)
    for b in beats:
        b["text"] = " ".join(l.strip() for l in b["lines"] if l.strip()).strip()
    return beats


def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def probe_duration_s(p):
    out = subprocess.check_output(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=nw=1:nk=1", str(p)])
    return float(out.strip())


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--script", required=True, help="narration markdown with '## beat-NN' headings")
    ap.add_argument("--video-dir", required=True, help="video dir; audio lands in <video-dir>/audio/")
    ap.add_argument("--voice-id", help="override pinned voice (auditions)")
    ap.add_argument("--model-id", help="override pinned model")
    ap.add_argument("--gap", type=float, help="seconds of silence between beats (default: pin's gap_s)")
    ap.add_argument("--summary", default="timing/voiceover-summary.json",
                    help="summary JSON path, relative to <video-dir>/audio/")
    args = ap.parse_args()

    _requests()
    import requests
    key = _load_key()

    pin_path = Path(__file__).resolve().parent / "voice_pin.json"
    pin = json.loads(pin_path.read_text())
    voice_id = args.voice_id or pin.get("voice_id")
    if not voice_id:
        sys.exit("error: no voice pinned (voice_pin.json voice_id is null) — pass --voice-id")
    model_id = args.model_id or pin["model_id"]
    settings = pin["voice_settings"]
    gap = args.gap if args.gap is not None else pin["gap_s"]
    out_format = pin["output_format"]

    script = Path(args.script)
    beats = parse_script(script.read_text())
    if not beats:
        sys.exit(f"error: no '## beat-NN' headings found in {script}")
    for b in beats:
        if not b["text"]:
            sys.exit(f"error: {b['id']} has no text")

    audio_dir = Path(args.video_dir) / "audio"
    beats_dir = audio_dir / "beats"
    timing_dir = audio_dir / "timing"
    beats_dir.mkdir(parents=True, exist_ok=True)
    timing_dir.mkdir(parents=True, exist_ok=True)

    # Inter-beat silence (same format as normalized beats: 44.1 kHz mono s16)
    gap_wav = beats_dir / ".gap.wav"
    subprocess.check_call(
        ["ffmpeg", "-y", "-v", "error", "-f", "lavfi",
         "-i", "anullsrc=r=44100:cl=mono", "-t", f"{gap}",
         "-c:a", "pcm_s16le", str(gap_wav)],
        stdout=subprocess.DEVNULL)

    summary_beats = []
    list_lines = []
    for i, b in enumerate(beats):
        data, headers = tts_call(key, voice_id, model_id, settings, out_format, b["text"])
        norm = beats_dir / f"{b['id']}.wav"
        raw = beats_dir / f"{b['id']}.raw.bin"
        raw.write_bytes(data)
        if out_format.startswith("pcm_"):
            # Raw little-endian s16 mono (e.g. pcm_24000) — wrap, then normalize.
            sr = pin.get("pcm_sample_rate", int(out_format.split("_")[1]))
            wrapped = beats_dir / f"{b['id']}.wrapped.wav"
            subprocess.check_call(
                ["ffmpeg", "-y", "-v", "error", "-f", "s16le", "-ar", str(sr), "-ac", "1",
                 "-i", str(raw), "-c:a", "pcm_s16le", str(wrapped)],
                stdout=subprocess.DEVNULL)
            raw.unlink()
            src = wrapped
        else:
            src = raw
        subprocess.check_call(
            ["ffmpeg", "-y", "-v", "error", "-i", str(src),
             "-ar", "44100", "-ac", "1", "-c:a", "pcm_s16le", str(norm)],
            stdout=subprocess.DEVNULL)
        src.unlink()
        dur = probe_duration_s(norm)
        summary_beats.append({
            "id": b["id"],
            "chars": len(b["text"]),
            "request_id": headers.get("request-id"),
            "character_count": headers.get("x-character-count"),
            "duration_s": round(dur, 3),
        })
        list_lines.append(f"file '{norm}'")
        if i < len(beats) - 1:
            list_lines.append(f"file '{gap_wav}'")
        print(f"  {b['id']}: {len(b['text'])} chars, {dur:.2f}s, "
              f"req={headers.get('request-id')}", file=sys.stderr)

    list_path = audio_dir / ".concat.txt"
    list_path.write_text("\n".join(list_lines) + "\n")
    master = audio_dir / "voiceover.wav"
    subprocess.check_call(
        ["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0",
         "-i", str(list_path), "-c", "copy", str(master)],
        stdout=subprocess.DEVNULL)
    list_path.unlink()
    gap_wav.unlink()
    master_dur = probe_duration_s(master)

    # Beat map: exact global start/end per beat (deterministic from probes + gap)
    beat_map = []
    t = 0.0
    for i, sb in enumerate(summary_beats):
        beat_map.append({
            "id": sb["id"],
            "start_s": round(t, 3),
            "end_s": round(t + sb["duration_s"], 3),
            "duration_s": sb["duration_s"],
            "gap_after_s": gap if i < len(summary_beats) - 1 else None,
        })
        t += sb["duration_s"] + (gap if i < len(summary_beats) - 1 else 0.0)
    (timing_dir / "beat-map.json").write_text(json.dumps(
        {"master": "audio/voiceover.wav", "master_sha256": sha256(master),
         "master_duration_s": round(master_dur, 3), "gap_s": gap, "beats": beat_map},
        indent=2) + "\n")

    lock_path = Path(__file__).resolve().parent / "requirements.lock.txt"
    summary = {
        "tool": "voiceover.py",
        "transport": f"REST v1 via requests {requests.__version__}",
        "requirements_lock_sha256": sha256(lock_path),
        "voice_id": voice_id,
        "voice_name": pin.get("voice_name"),
        "model_id": model_id,
        "voice_settings": settings,
        "output_format": out_format,
        "gap_s": gap,
        "script_path": str(script),
        "script_sha256": sha256(script),
        "beats": summary_beats,
        "master": {"path": "audio/voiceover.wav",
                   "sha256": sha256(master), "duration_s": round(master_dur, 3)},
    }
    summary_path = audio_dir / args.summary
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    summary_path.write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps({"master": str(master), "duration_s": round(master_dur, 3),
                      "sha256": summary["master"]["sha256"],
                      "summary": str(summary_path)}, indent=2))


if __name__ == "__main__":
    main()
