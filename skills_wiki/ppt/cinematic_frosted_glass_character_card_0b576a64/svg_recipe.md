# SVG Recipe — Cinematic Frosted Glass Character Card

## Visual mechanism
A full-bleed cinematic background is duplicated inside a large rounded card as a pre-blurred image, then darkened with translucent overlays to create a frosted glass pane. A sharp transparent character cutout overlaps the glass edge, while large metallic-gold typography sits on the readable glass zone.

## SVG primitives needed
- 1× `<image>` for the full-slide atmospheric background photo.
- 1× `<image>` for the same background pre-blurred, clipped to the glass card.
- 1× `<clipPath>` with rounded `<rect>` for the frosted glass crop.
- 1× `<image>` for the transparent PNG character/person cutout.
- 4× `<rect>` for vignette, panel shadow base, glass tint, and glass border/highlight.
- 2× `<path>` for cinematic glow behind the subject and decorative gold accent marks.
- 2× `<linearGradient>` for background vignette and metallic-gold text/accent fills.
- 1× `<filter id="panelShadow">` applied to the glass shadow rectangle.
- 1× `<filter id="softGlow">` applied to the glow path behind the character.
- 6× `<text>` blocks with explicit `width` attributes for role label, name, quote, stats, and metadata.

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="vignette" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#020407" stop-opacity="0.88"/>
      <stop offset="45%" stop-color="#111827" stop-opacity="0.18"/>
      <stop offset="100%" stop-color="#000000" stop-opacity="0.72"/>
    </linearGradient>

    <linearGradient id="goldText" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#fff2b8"/>
      <stop offset="28%" stop-color="#d8aa38"/>
      <stop offset="55%" stop-color="#f8d978"/>
      <stop offset="78%" stop-color="#9e6d1f"/>
      <stop offset="100%" stop-color="#ffe69a"/>
    </linearGradient>

    <linearGradient id="glassEdge" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#ffffff" stop-opacity="0.58"/>
      <stop offset="42%" stop-color="#ffffff" stop-opacity="0.12"/>
      <stop offset="100%" stop-color="#d8aa38" stop-opacity="0.28"/>
    </linearGradient>

    <filter id="panelShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feOffset dx="0" dy="18"/>
      <feGaussianBlur stdDeviation="22"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="softGlow" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="28"/>
    </filter>

    <clipPath id="glassClip">
      <rect x="64" y="72" width="705" height="576" rx="34" ry="34"/>
    </clipPath>
  </defs>

  <image x="0" y="0" width="1280" height="720"
         href="https://images.example.com/cinematic-night-boardroom-wide-background.jpg"/>

  <rect x="0" y="0" width="1280" height="720" fill="url(#vignette)"/>

  <path d="M730,98 C885,38 1072,76 1164,204 C1248,321 1220,514 1090,625 C976,722 770,681 690,552 C604,414 596,151 730,98 Z"
        fill="#d8aa38" opacity="0.18" filter="url(#softGlow)"/>

  <rect x="64" y="72" width="705" height="576" rx="34" ry="34"
        fill="#02060c" opacity="0.62" filter="url(#panelShadow)"/>

  <image x="0" y="0" width="1280" height="720"
         clip-path="url(#glassClip)"
         href="https://images.example.com/cinematic-night-boardroom-wide-background-preblurred.jpg"/>

  <rect x="64" y="72" width="705" height="576" rx="34" ry="34"
        fill="#07111d" opacity="0.66"/>

  <rect x="82" y="92" width="669" height="536" rx="26" ry="26"
        fill="none" stroke="url(#glassEdge)" stroke-width="1.6" opacity="0.92"/>

  <path d="M112,144 L222,144" stroke="#d8aa38" stroke-width="3" stroke-linecap="round" opacity="0.95"/>
  <path d="M112,152 L174,152" stroke="#ffffff" stroke-width="1" stroke-linecap="round" opacity="0.34"/>

  <text x="112" y="130" width="540"
        font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="600"
        letter-spacing="4" fill="#ffffff" opacity="0.78">
    CHARACTER DOSSIER
  </text>

  <text x="112" y="224" width="560"
        font-family="Segoe UI, Microsoft YaHei" font-size="78" font-weight="800"
        letter-spacing="1" fill="url(#goldText)">
    <tspan x="112" dy="0">MAYA</tspan>
    <tspan x="112" dy="82">RHEE</tspan>
  </text>

  <text x="116" y="336" width="500"
        font-family="Segoe UI, Microsoft YaHei" font-size="21" font-weight="600"
        fill="#ffffff" opacity="0.92">
    Chief Negotiator · Strategic Operations
  </text>

  <text x="116" y="390" width="548"
        font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="400"
        fill="#dce6f2" opacity="0.86">
    <tspan x="116" dy="0">A calm center in high-pressure rooms, turning</tspan>
    <tspan x="116" dy="31">incomplete signals into decisive moves before</tspan>
    <tspan x="116" dy="31">the rest of the table sees the pattern.</tspan>
  </text>

  <rect x="116" y="506" width="150" height="72" rx="18" ry="18" fill="#ffffff" opacity="0.08"/>
  <rect x="292" y="506" width="150" height="72" rx="18" ry="18" fill="#ffffff" opacity="0.08"/>
  <rect x="468" y="506" width="150" height="72" rx="18" ry="18" fill="#ffffff" opacity="0.08"/>

  <text x="136" y="536" width="112"
        font-family="Segoe UI, Microsoft YaHei" font-size="24" font-weight="800" fill="url(#goldText)">14</text>
  <text x="136" y="562" width="112"
        font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="600" letter-spacing="1.5"
        fill="#ffffff" opacity="0.62">MISSIONS</text>

  <text x="312" y="536" width="112"
        font-family="Segoe UI, Microsoft YaHei" font-size="24" font-weight="800" fill="url(#goldText)">98%</text>
  <text x="312" y="562" width="112"
        font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="600" letter-spacing="1.5"
        fill="#ffffff" opacity="0.62">CLOSE RATE</text>

  <text x="488" y="536" width="112"
        font-family="Segoe UI, Microsoft YaHei" font-size="24" font-weight="800" fill="url(#goldText)">A1</text>
  <text x="488" y="562" width="112"
        font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="600" letter-spacing="1.5"
        fill="#ffffff" opacity="0.62">CLEARANCE</text>

  <image x="625" y="42" width="505" height="665"
         href="https://images.example.com/transparent-png-cutout-confident-executive-woman.png"/>

  <text x="928" y="650" width="240"
        font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="600"
        letter-spacing="2.4" fill="#ffffff" opacity="0.58">
    SEASON 04 · EPISODE 07
  </text>
</svg>
```

## Avoid in this skill
- ❌ Applying `clip-path` to the glass tint `<rect>`; only the blurred `<image>` needs the clip, while rounded rectangles should use `rx`/`ry`.
- ❌ Using SVG `<mask>` for the portrait cutout; provide a real transparent PNG subject image instead.
- ❌ Relying on live SVG blur filters on the background photo; use a pre-blurred duplicate image for reliable PPT translation.
- ❌ Placing the character fully outside the card; the depth illusion depends on the subject overlapping the frosted glass boundary.
- ❌ Putting small text directly on the raw photo background; keep all critical copy inside the darkened glass pane.

## Composition notes
- Keep the frosted card on the left 55–60% of the slide, leaving the right side for the portrait and atmospheric background.
- Let the subject overlap the glass edge by roughly 80–140 px so the slide has a foreground/midground/background depth stack.
- Use dark blue-black tints for the glass and warm gold only for hierarchy: name, accent lines, and key numbers.
- Preserve generous negative space above and below the name; the card should feel cinematic, not like a dense profile form.