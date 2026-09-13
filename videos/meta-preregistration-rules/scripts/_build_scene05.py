#!/usr/bin/env python3
"""Build helper for scene-05 — deterministic SHA injection.

Per the spec (scene-specs/scene-05.md, Inputs): the seal SHA is "read from
the file at build time, never computed and never typed into markup"
(composition reads data/spec-sha.txt). This script IS that read: it checks
the committed data input's checksum, then injects its 40 hex chars into
the template's two span chains (the typed command + the amber SHA).
Same input file → byte-identical composition/scene-05.html.

Usage: python3 scripts/_build_scene05.py   (from the video dir)
"""
import hashlib
import re
import sys

SHA_FILE = "data/spec-sha.txt"
FILE_SHA = "225809172e884309cab78e4fb11be46bece0dc67856d7a3cdf9dc003acf4f29d"
TEMPLATE = "scripts/_scene-05.tmpl.html"
OUT = "composition/scene-05.html"

raw = open(SHA_FILE, "rb").read()
digest = hashlib.sha256(raw).hexdigest()
if digest != FILE_SHA:
    sys.exit(f"REFUSED: data/spec-sha.txt sha256 {digest} != committed {FILE_SHA}")
sha = raw.decode().strip()
assert re.fullmatch(r"[0-9a-f]{40}", sha), f"bad sha content: {sha!r}"

html = open(TEMPLATE).read()
chars = "".join(f'<span class="ch">{c}</span>' for c in sha)
out = html.replace("<!--CMD-SHA-CHARS-->", chars).replace("<!--SSHA-CHARS-->", chars)
for marker in ("<!--CMD-SHA-CHARS-->", "<!--SSHA-CHARS-->"):
    assert marker not in out, f"unreplaced marker {marker}"
# the two span chains must spell exactly: "git commit  " + sha (command)
# and sha (the amber line). Parse the spans (class "sp" = a double space,
# class "ch" = one char) rather than string-munging stripped tags.
import html as _html
def chain_text(block):
    parts = []
    for cls, txt in re.findall(r'<span class="(sp|ch)">([^<]*)</span>', block):
        parts.append("\xa0" if cls == "sp" else _html.unescape(txt))
    return "".join(parts)
cmd = re.search(r'<div class="cmd"[^>]*>(.*?)</div>', out).group(1)
ssha = re.search(r'<div class="seal-sha[^"]*" id="ssha">(.*?)</div>', out).group(1)
cmd_text = chain_text(cmd).replace('\xa0', ' ')
ssha_text = chain_text(ssha)
assert cmd_text == "git commit " + sha, repr(cmd_text)
assert ssha_text == sha, repr(ssha_text)
open(OUT, "w").write(out)
print(f"wrote {OUT} ({len(out)} bytes), sha {sha}")
