# scene-specs/

One spec per scene (scene-01 … scene-09). A scene spec is the contract the
Phase C build is checked against: fixed window from `audio/timing/beat-map.json`,
cue rows pinned to word timestamps from `audio/timing/words.json`, element
list, data inputs, motion verbs (style spec §5.2 only), continuity, QA.

Rules enforced here (style spec v1.1.0 §5.1):
- reveal on the word that names the element;
- no element fully visible >2s before its cue;
- ≥1 state change per 10s of continuous speech (change floor);
- stillness only after the last word (earned final hold).

Status flow: SPEC → built (Phase C) → draft render + proof frames → REVIEW →
final. Scene 05 reads its SHA from `data/spec-sha.txt` (pinned, checksummed);
no number is computed in a composition.
