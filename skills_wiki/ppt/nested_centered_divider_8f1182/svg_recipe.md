# SVG Recipe — Nested Centered Divider

## Visual mechanism
A calm full-slide field is interrupted by a stack of perfectly centered, nested rectangles that act like a ceremonial frame for a short headline. Subtle gradients, soft shadows, inner strokes, and tiny corner accents make the divider feel premium while preserving a minimal corporate tone.

## SVG primitives needed
- 1× `<rect>` for the full-slide background
- 2× `<ellipse>` for soft ambient light halos behind the centered structure
- 4× `<rect>` for the nested centered rectangle system: outer glass frame, middle panel, inner card, and headline plate
- 4× `<path>` for decorative corner bracket accents
- 2× `<line>` for the small centered divider rule above and below the subhead
- 3× `<text>` for section label, headline, and optional subhead
- 3× `<linearGradient>` for background, card surface, and accent strokes
- 1× `<radialGradient>` for ambient glow
- 2× `<filter>` using blur/shadow effects applied to rectangles, ellipses, and text

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGradient" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#07111F"/>
      <stop offset="48%" stop-color="#0C1B2E"/>
      <stop offset="100%" stop-color="#111827"/>
    </linearGradient>

    <radialGradient id="haloGradient" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#6DA8FF" stop-opacity="0.34"/>
      <stop offset="55%" stop-color="#3D6CA8" stop-opacity="0.10"/>
      <stop offset="100%" stop-color="#07111F" stop-opacity="0"/>
    </radialGradient>

    <linearGradient id="glassStroke" x1="240" y1="130" x2="1040" y2="590" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.65"/>
      <stop offset="42%" stop-color="#8DA7C7" stop-opacity="0.18"/>
      <stop offset="100%" stop-color="#F4C96B" stop-opacity="0.55"/>
    </linearGradient>

    <linearGradient id="cardSurface" x1="330" y1="205" x2="950" y2="515" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#F8FAFC"/>
      <stop offset="52%" stop-color="#EEF3F8"/>
      <stop offset="100%" stop-color="#DCE6F2"/>
    </linearGradient>

    <linearGradient id="goldAccent" x1="380" y1="270" x2="900" y2="450" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#F7D98C"/>
      <stop offset="50%" stop-color="#CFA24A"/>
      <stop offset="100%" stop-color="#FFF0BA"/>
    </linearGradient>

    <filter id="softShadow" x="-20%" y="-25%" width="140%" height="150%">
      <feOffset dx="0" dy="18" in="SourceAlpha" result="off"/>
      <feGaussianBlur in="off" stdDeviation="18" result="blur"/>
      <feColorMatrix in="blur" type="matrix"
        values="0 0 0 0 0.01  0 0 0 0 0.03  0 0 0 0 0.08  0 0 0 0.40 0" result="shadow"/>
      <feMerge>
        <feMergeNode in="shadow"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="ambientBlur" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="30"/>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGradient)"/>

  <ellipse cx="640" cy="360" rx="420" ry="210" fill="url(#haloGradient)" filter="url(#ambientBlur)" opacity="0.95"/>
  <ellipse cx="900" cy="190" rx="220" ry="120" fill="#D6AA55" opacity="0.10" filter="url(#ambientBlur)"/>

  <rect x="235" y="125" width="810" height="470" rx="38"
        fill="#FFFFFF" opacity="0.045"
        stroke="url(#glassStroke)" stroke-width="1.6"/>

  <rect x="280" y="170" width="720" height="380" rx="30"
        fill="#0E2237" opacity="0.86"
        stroke="#FFFFFF" stroke-opacity="0.12" stroke-width="1.2"
        filter="url(#softShadow)"/>

  <rect x="330" y="220" width="620" height="280" rx="24"
        fill="url(#cardSurface)"
        stroke="#FFFFFF" stroke-width="2"/>

  <rect x="375" y="270" width="530" height="180" rx="18"
        fill="#FFFFFF" opacity="0.74"
        stroke="url(#goldAccent)" stroke-width="2.2"/>

  <path d="M315 205 L315 180 L340 180" fill="none" stroke="#F5D381" stroke-width="3" stroke-linecap="round"/>
  <path d="M965 180 L990 180 L990 205" fill="none" stroke="#F5D381" stroke-width="3" stroke-linecap="round"/>
  <path d="M315 515 L315 540 L340 540" fill="none" stroke="#F5D381" stroke-width="3" stroke-linecap="round"/>
  <path d="M965 540 L990 540 L990 515" fill="none" stroke="#F5D381" stroke-width="3" stroke-linecap="round"/>

  <line x1="565" y1="318" x2="715" y2="318" stroke="url(#goldAccent)" stroke-width="2"/>
  <line x1="565" y1="410" x2="715" y2="410" stroke="url(#goldAccent)" stroke-width="2"/>

  <text x="640" y="292" width="420" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="13" font-weight="700" letter-spacing="3.5"
        fill="#8A6A2D">
    SECTION 03
  </text>

  <text x="640" y="375" width="560" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="52" font-weight="800"
        fill="#0B1B2B">
    MARKET RESET
  </text>

  <text x="640" y="443" width="520" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="19" font-weight="400"
        fill="#4B5B6C">
    A focused transition into the next strategic chapter
  </text>
</svg>
```

## Avoid in this skill
- ❌ Overloading the center with long paragraphs; the nested frame works best with a short headline and one restrained subhead.
- ❌ Using `<mask>` to create inner cutouts or vignette effects; use translucent rectangles, gradients, and blur filters instead.
- ❌ Applying `filter` to `<line>` elements for glowing rules; use clean strokes or place a blurred rectangle/ellipse behind them if glow is needed.
- ❌ Skewed or matrix-transformed frames; keep the rectangles centered and orthogonal so PowerPoint preserves the crisp divider geometry.
- ❌ Repeating the nested rectangles through `<use>`; duplicate the actual shapes directly if variations are needed.

## Composition notes
- Keep the headline plate centered both vertically and horizontally; the whole slide should feel symmetrical and ceremonial.
- Use generous negative space around the outer frame, typically 15–20% of slide width on each side.
- Let the brightest value sit in the central card while the background stays dark or muted, creating a strong focal pull.
- Accent color should appear sparingly on the thin border, divider rules, and corner brackets to avoid turning the layout into a decorative frame.