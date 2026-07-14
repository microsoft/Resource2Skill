# SVG Recipe — Centered Ring Divider

## Visual mechanism
A single oversized ring sits perfectly centered on a vertical divider line, acting like a bold “portal” for the section title. The layout is intentionally sparse: strong geometry, high contrast, and centered typography create a premium section-break moment.

## SVG primitives needed
- 1× `<rect>` for the full-slide background wash
- 1× `<line>` for the vertical center divider running through the slide
- 6× `<circle>` for the main ring, inner clearing disc, thin secondary rings, and small orbital dots
- 4× `<path>` for short curved accent arcs around the ring
- 3× `<text>` elements for section label, headline, and subtitle
- 2× `<linearGradient>` for background and ring stroke coloration
- 1× `<radialGradient>` for subtle center glow
- 2× `<filter>` definitions: soft shadow/glow applied only to circles and text, not lines

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgWash" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#FFF7EC"/>
      <stop offset="52%" stop-color="#FFFDF8"/>
      <stop offset="100%" stop-color="#F3F6FF"/>
    </linearGradient>

    <linearGradient id="ringHot" x1="420" y1="180" x2="860" y2="540" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#FF6A3D"/>
      <stop offset="45%" stop-color="#E8356D"/>
      <stop offset="100%" stop-color="#6C4DFF"/>
    </linearGradient>

    <radialGradient id="centerGlow" cx="50%" cy="46%" r="62%">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="1"/>
      <stop offset="65%" stop-color="#FFF4E6" stop-opacity="0.82"/>
      <stop offset="100%" stop-color="#FFFFFF" stop-opacity="0"/>
    </radialGradient>

    <filter id="softShadow" x="-30%" y="-30%" width="160%" height="160%">
      <feOffset dx="0" dy="16"/>
      <feGaussianBlur stdDeviation="18"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="softGlow" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="8"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgWash)"/>

  <circle cx="640" cy="360" r="315" fill="none" stroke="#F2C9A8" stroke-width="1.5" opacity="0.36"/>
  <circle cx="640" cy="360" r="246" fill="none" stroke="#DCE2F4" stroke-width="1.5" opacity="0.55"/>
  <circle cx="640" cy="360" r="188" fill="url(#centerGlow)" opacity="0.9"/>

  <line x1="640" y1="72" x2="640" y2="648" stroke="#1C2742" stroke-width="2.2" opacity="0.22"/>

  <circle cx="640" cy="360" r="174" fill="#FFFDF8" opacity="0.96" filter="url(#softShadow)"/>
  <circle cx="640" cy="360" r="176" fill="none" stroke="url(#ringHot)" stroke-width="28" filter="url(#softGlow)"/>
  <circle cx="640" cy="360" r="214" fill="none" stroke="#151A2D" stroke-width="2" stroke-dasharray="7 15" opacity="0.48"/>

  <path d="M 451 297 C 468 240, 518 199, 579 187" fill="none" stroke="#FFB340" stroke-width="8" stroke-linecap="round" opacity="0.95"/>
  <path d="M 705 184 C 765 199, 814 242, 831 301" fill="none" stroke="#755CFF" stroke-width="8" stroke-linecap="round" opacity="0.9"/>
  <path d="M 829 419 C 811 478, 762 519, 704 535" fill="none" stroke="#E8356D" stroke-width="8" stroke-linecap="round" opacity="0.9"/>
  <path d="M 577 533 C 518 520, 468 477, 451 420" fill="none" stroke="#1F9D8A" stroke-width="8" stroke-linecap="round" opacity="0.82"/>

  <circle cx="440" cy="360" r="9" fill="#151A2D"/>
  <circle cx="840" cy="360" r="9" fill="#151A2D"/>
  <circle cx="640" cy="148" r="6" fill="#FF6A3D"/>
  <circle cx="640" cy="572" r="6" fill="#6C4DFF"/>

  <text x="640" y="302" width="360" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="18" font-weight="700" letter-spacing="4"
        fill="#E8356D">
    SECTION 03
  </text>

  <text x="640" y="368" width="470" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="56" font-weight="800"
        fill="#151A2D">
    Momentum
  </text>

  <text x="640" y="412" width="430" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="22" font-weight="400"
        fill="#5E6477">
    where strategy turns into motion
  </text>
</svg>
```

## Avoid in this skill
- ❌ Do not build the donut by masking one circle out of another; use stroked circles instead so the ring stays editable.
- ❌ Do not apply a filter to the vertical `<line>`; line filters are dropped, so keep shadows/glows on circles or paths.
- ❌ Do not overcrowd the center with long copy; this divider works best with one short headline and a small subtitle.
- ❌ Do not use `<use>` to duplicate orbital dots or arcs; repeat the editable primitives directly.

## Composition notes
- Keep the ring exactly centered at `(640, 360)`; the precision is what makes the divider feel intentional and keynote-like.
- Let the vertical line extend well beyond the ring, but place it behind the center disc so the title remains clean and readable.
- Use a warm-to-cool gradient on the ring and tiny accent arcs to add energy without losing the minimalist feel.
- Reserve generous negative space on both sides; this layout should feel like a pause between presentation chapters, not an information slide.