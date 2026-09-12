#!/usr/bin/env python3
"""transcribe.py — word-level transcript + SRT from the committed wav (Scribe v2).

Vendored/adapted from https://github.com/elevenlabs/skills (MIT,
Copyright (c) 2024 ElevenLabs), speech-to-text skill +
references/transcription-options.md. Adaptations for this repo: batch
scribe_v2 with word timestamps and keyterms from voice_pin.json, SRT
chunking on phrase boundaries (punctuation / breath points, max line
length), and a summary JSON for the build log. MIT carries no change-
note obligation; notes kept anyway.

Transport: REST v1 directly (stable API; the request-id header is the
audit data the SDK swallows).

The transcript is the timing backbone for visual beat sync:
scene specs cite cue timestamps from words.json; the captions skill
consumes captions.srt (standing decision: soft SRT from the committed
wav, VIDEO_CONCEPT §11).

Usage (from repo root):
  python3 videos/pipeline/tts/transcribe.py --video-dir videos/<slug>
      [--wav audio/voiceover.wav]

Key: ELEVENLABS_API_KEY in the environment, else
~/.config/elevenlabs/api_key (file, 0600). Never in the repo.

Outputs under <video-dir>/audio/timing/:
  words.json          full word-level transcript (verbatim, start/end per word)
  captions.srt        chunked caption timings (soft captions)
  transcribe-summary.json  build-log record (model, keyterms, request-id, checksums)
"""
import argparse
import hashlib
import json
import os
import sys
from pathlib import Path

MIN_GAP_S = 0.45    # pause this long (or longer) forces a new caption chunk
MAX_CHUNK_WORDS = 8  # max words per caption line before forced split
SRT_LEAD_S = 0.02   # start caption slightly before the first phoneme
SRT_TAIL_S = 0.20   # hold after the last phoneme


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


def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def srt_ts(t):
    ms = int(round(t * 1000))
    h, ms = divmod(ms, 3600000)
    m, ms = divmod(ms, 60000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def chunk_words(words):
    """Group word entries into caption lines.

    Split on: punctuation-ending words (natural phrase boundaries),
    pauses >= MIN_GAP_S, or MAX_CHUNK_WORDS reached.
    """
    chunks, cur = [], []
    prev_end = None
    for w in words:
        if cur:
            gap = w["start"] - prev_end
            end_punct = cur[-1]["text"].rstrip()[-1:] in ".!?…"
            if gap >= MIN_GAP_S or end_punct or len(cur) >= MAX_CHUNK_WORDS:
                chunks.append(cur)
                cur = []
        cur.append(w)
        prev_end = w["end"]
    if cur:
        chunks.append(cur)
    return chunks


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--video-dir", required=True)
    ap.add_argument("--wav", default="audio/voiceover.wav",
                    help="wav path relative to the video dir")
    args = ap.parse_args()

    _requests()
    import requests
    key = _load_key()

    pin = json.loads((Path(__file__).resolve().parent / "voice_pin.json").read_text())
    stt = pin["stt"]
    video_dir = Path(args.video_dir)
    wav = video_dir / args.wav
    if not wav.exists():
        sys.exit(f"error: {wav} not found")
    timing = video_dir / "audio" / "timing"
    timing.mkdir(parents=True, exist_ok=True)

    payload = {
        "model_id": stt["model_id"],
        "language_code": stt["language_code"],
        "timestamps_granularity": stt["timestamps_granularity"],
        "keyterms": pin["keyterms"],
    }
    with open(wav, "rb") as f:
        r = requests.post(
            "https://api.elevenlabs.io/v1/speech-to-text",
            headers={"xi-api-key": key},
            data=payload,
            files={"file": ("voiceover.wav", f, "audio/wav")},
            timeout=600,
        )
    if r.status_code != 200:
        sys.exit(f"error: STT HTTP {r.status_code}: {r.text[:300]}")
    data = r.json()

    # Verbatim word-level record (only real words — drop spacing entries)
    words = [{"text": w["text"], "start": w["start"], "end": w["end"]}
             for w in (data.get("words") or []) if w.get("type") == "word"]
    words_json = {
        "wav": args.wav,
        "wav_sha256": sha256(wav),
        "model_id": stt["model_id"],
        "transcription_id": data.get("transcription_id"),
        "language_code": data.get("language_code"),
        "audio_duration_secs": data.get("audio_duration_secs"),
        "words": words,
    }
    words_path = timing / "words.json"
    words_path.write_text(json.dumps(words_json, indent=2) + "\n")

    # SRT from phrase chunks
    lines = []
    for i, ch in enumerate(chunk_words(words), 1):
        start = max(0.0, ch[0]["start"] - SRT_LEAD_S)
        end = ch[-1]["end"] + SRT_TAIL_S
        text = " ".join(w["text"] for w in ch)
        lines.append(f"{i}\n{srt_ts(start)} --> {srt_ts(end)}\n{text}\n")
    srt_path = timing / "captions.srt"
    srt_path.write_text("\n".join(lines))

    lock_path = Path(__file__).resolve().parent / "requirements.lock.txt"
    summary = {
        "tool": "transcribe.py",
        "transport": f"REST v1 via requests {requests.__version__}",
        "requirements_lock_sha256": sha256(lock_path),
        "model_id": stt["model_id"],
        "keyterms": pin["keyterms"],
        "request_id": r.headers.get("request-id"),
        "transcription_id": data.get("transcription_id"),
        "language_code": data.get("language_code"),
        "language_probability": data.get("language_probability"),
        "audio_duration_secs": data.get("audio_duration_secs"),
        "word_count": len(words),
        "caption_count": len(lines),
        "wav_sha256": words_json["wav_sha256"],
        "outputs": {"words": "audio/timing/words.json",
                    "srt": "audio/timing/captions.srt"},
    }
    (timing / "transcribe-summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps({
        "words_json": str(words_path), "srt": str(srt_path),
        "words": len(words), "captions": len(lines),
        "duration_s": data.get("audio_duration_secs"),
        "request_id": r.headers.get("request-id"),
    }, indent=2))


if __name__ == "__main__":
    main()
