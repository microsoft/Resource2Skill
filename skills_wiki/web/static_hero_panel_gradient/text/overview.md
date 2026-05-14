# Hero Panel with Gradient

Full-bleed hero section with a left-aligned headline, subhead, and CTA button on top of a 135-degree linear-gradient background. Uses CSS Grid to align headline column (60%) and decorative image column (40%) on screens ≥ 768px and stacks them on smaller viewports.

## Markup
- `<section class="hero">` — outer container
- `<div class="hero__content">` — text column (h1, p, a.cta)
- `<div class="hero__visual">` — decorative column (svg / img)

## Theming knobs
- `--hero-gradient-from`, `--hero-gradient-to` (CSS custom properties)
- `--cta-bg`, `--cta-fg` for the button colour pair
- `--max-width` for the container

## Suggested use
Use as the first viewport on a marketing landing page. Pair with the bento card grid below for a complete above-fold layout.