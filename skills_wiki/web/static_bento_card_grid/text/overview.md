# Bento Card Grid (3x3)

Nine-card responsive grid using CSS `grid-template-columns: repeat(3, 1fr)` on desktop and a single column on mobile. Each card has rounded corners, a subtle shadow, and a hover lift transform. Cards include an icon slot, headline, body copy, and an optional CTA link.

## Markup
- `<ul class="bento">` — outer grid
- `<li class="bento__card">` — repeating card with `<svg class="bento__icon">`, `<h3>`, `<p>`, `<a>`

## Layout knobs
- `--bento-gap` (default 1.25rem)
- `--bento-radius` (default 1rem)
- `--bento-shadow` (default `0 1px 2px rgba(0,0,0,.04), 0 4px 16px rgba(0,0,0,.08)`)

## Suggested use
Use below the hero panel to break up a long-scroll feature list into a glanceable grid.