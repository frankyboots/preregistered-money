# Theme Tokens Reference

Use this when a user requests brand cleanup, color consistency, or replacement of off-palette accents.

## Tokenize First

Prefer named tokens:

```css
:root {
  --color-bg: #f7f3ec;
  --color-ink: #111111;
  --color-muted: rgba(17, 17, 17, 0.62);
  --color-accent: #ef6f22;
  --glass-fill: rgba(255, 255, 255, 0.52);
  --glass-border: rgba(255, 255, 255, 0.72);
}
```

In this repo the token values come from the versioned style spec (`videos/pipeline/style/style-spec.md`), not from this file — this reference is about the discipline, not the values.

## Search Targets

- CSS variables.
- Raw hex colors.
- RGB/RGBA values.
- SVG `fill` and `stroke`.
- Canvas/WebGL constants.
- Inline HTML styles.
- Duplicated start/carryover frames.

`videos/pipeline/tools/scan_theme_colors.py` automates this scan against an allow-list of the style-spec palette.

## Exclusions

Do not recolor unless explicitly requested:

- Logo artwork.
- User-provided reference images.
- Screenshot imagery of real tools (commit views, terminals, scoreboards).

## Proof

Check at least one proof frame per affected scene and one proof frame from the next scene if it carries over the same visual.
