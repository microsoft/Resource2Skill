# SVG Recipe — Centered Accent Divider

## Visual mechanism
A low-density section divider built from a centered stack of nested rectangles, with a short headline locked to the middle and a crisp accent bar acting as the visual hinge. Subtle gradients, shadows, and faint geometric background marks make the layout feel premium while preserving a disciplined corporate structure.

## SVG primitives needed
- 1× `<rect>` for the full-slide gradient background
- 3× large decorative `<circle>` / `<ellipse>` shapes for soft background atmosphere
- 4× `<path>` for faint architectural corner-line decorations
- 1× `<rect>` for the outer centered frame
- 1× `<rect>` for the main elevated title panel
- 2× `<rect>` for nested inner borders
- 5× small `<rect>` elements for the centered accent divider bar and end caps
- 2× `<text>` elements for headline and optional subtitle, each with explicit `width=`
- 2× `<linearGradient>` definitions for background and accent fills
- 1× `<radialGradient>` for soft ambient glow
- 2× `<filter>` definitions for card shadow and accent glow

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1280" y2="720">
      <stop offset="0%" stop-color="#07111F"/>
      <stop offset="52%" stop-color="#101A2B"/>
      <stop offset="100%" stop-color="#061526"/>
    </linearGradient>

    <linearGradient id="panelGrad" x1="325" y1="248" x2="955" y2="472">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="100%" stop-color="#EEF3F8"/>
    </linearGradient>

    <linearGradient id="accentGrad" x1="440" y1="0" x2="840" y2="0">
      <stop offset="0%" stop-color="#2DD4BF"/>
      <stop offset="48%" stop-color="#F7C948"/>
      <stop offset="100%" stop-color="#FF7A59"/>
    </linearGradient>

    <radialGradient id="ambientGlow" cx="50%" cy="45%" r="55%">
      <stop offset="0%" stop-color="#2DD4BF" stop-opacity="0.22"/>
      <stop offset="70%" stop-color="#2DD4BF" stop-opacity="0.04"/>
      <stop offset="100%" stop-color="#2DD4BF" stop-opacity="0"/>
    </radialGradient>

    <filter id="cardShadow" x="-20%" y="-30%" width="140%" height="160%">
      <feOffset dx="0" dy="18"/>
      <feGaussianBlur stdDeviation="18"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="accentGlow" x="-40%" y="-80%" width="180%" height="260%">
      <feGaussianBlur stdDeviation="8"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>
  <ellipse cx="640" cy="358" rx="470" ry="260" fill="url(#ambientGlow)"/>
  <circle cx="1080" cy="96" r="190" fill="#284766" opacity="0.16"/>
  <circle cx="138" cy="650" r="230" fill="#153B52" opacity="0.18"/>

  <path d="M92 116 H294 M92 116 V250" fill="none" stroke="#FFFFFF" stroke-width="2" opacity="0.12"/>
  <path d="M1188 116 H986 M1188 116 V250" fill="none" stroke="#FFFFFF" stroke-width="2" opacity="0.12"/>
  <path d="M92 604 H294 M92 604 V470" fill="none" stroke="#FFFFFF" stroke-width="2" opacity="0.10"/>
  <path d="M1188 604 H986 M1188 604 V470" fill="none" stroke="#FFFFFF" stroke-width="2" opacity="0.10"/>

  <rect x="266" y="200" width="748" height="320" rx="10" fill="none" stroke="#FFFFFF" stroke-width="1.5" opacity="0.22"/>
  <rect x="292" y="224" width="696" height="272" rx="8" fill="none" stroke="#69E0D0" stroke-width="1" opacity="0.20"/>

  <rect x="325" y="258" width="630" height="204" rx="14" fill="url(#panelGrad)" filter="url(#cardShadow)"/>
  <rect x="353" y="286" width="574" height="148" rx="8" fill="none" stroke="#0E1A2B" stroke-width="1.2" opacity="0.18"/>
  <rect x="373" y="306" width="534" height="108" rx="4" fill="none" stroke="#0E1A2B" stroke-width="1" opacity="0.08"/>

  <rect x="438" y="357" width="404" height="6" rx="3" fill="#D8E1EA"/>
  <rect x="490" y="355" width="300" height="10" rx="5" fill="url(#accentGrad)" filter="url(#accentGlow)"/>
  <rect x="428" y="354" width="16" height="12" rx="2" fill="#2DD4BF"/>
  <rect x="836" y="354" width="16" height="12" rx="2" fill="#FF7A59"/>
  <rect x="620" y="348" width="40" height="24" rx="4" fill="#0E1A2B"/>

  <text x="640" y="340" width="520" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="18" font-weight="700" letter-spacing="4"
        fill="#526070">
    Q4 EXECUTIVE BRIEFING
  </text>

  <text x="640" y="404" width="560" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="42" font-weight="700" letter-spacing="1"
        fill="#101A2B">
    STRATEGIC RESET
  </text>

  <text x="640" y="440" width="500" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="15" font-weight="400"
        fill="#657386">
    Priorities, operating rhythm, and investment focus
  </text>
</svg>
```

## Avoid in this skill
- ❌ Using only one flat rectangle and centered text; the technique depends on visible nesting and a strong accent divider.
- ❌ Overcrowding the center panel with bullets, charts, or long paragraphs; this is a section divider, not a content slide.
- ❌ Applying `filter` to `<line>` elements for glow or shadow; use thin `<rect>` elements for glowing divider bars.
- ❌ Using `<mask>` or clipping on non-image shapes for the frame effect; nested editable rectangles translate more reliably.
- ❌ Placing the accent bar too close to the headline baseline; keep it as a deliberate separator, not an underline collision.

## Composition notes
- Keep the visual mass centered: roughly 50–60% slide width for the main panel and generous negative space around it.
- Use a dark background with a pale center panel for maximum keynote-style contrast.
- The accent divider should be short, saturated, and horizontally centered; it is the focal mechanism.
- Decorative corner lines and ambient glows should stay low-opacity so they support the frame without competing with the title.