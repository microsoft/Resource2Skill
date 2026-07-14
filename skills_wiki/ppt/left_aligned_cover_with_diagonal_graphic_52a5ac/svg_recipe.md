# SVG Recipe — Left Aligned Cover with Diagonal Graphic

## Visual mechanism
A calm, text-heavy left column is contrasted with a high-energy diagonal graphic field on the right. The diagonal edge creates motion and a premium keynote feel while keeping the headline area clean and highly readable.

## SVG primitives needed
- 1× `<rect>` for the full-slide background
- 2× `<rect>` for subtle left-side text anchoring accents
- 5× `<path>` for the main diagonal color block, darker diagonal wedge, translucent ribbons, and angular highlights
- 5× `<circle>` / `<ellipse>` for floating decorative orbs inside the diagonal field
- 4× `<text>` for eyebrow label, headline, subtitle, and small footer metadata
- 3× `<linearGradient>` for background wash, main diagonal fill, and accent strokes
- 1× `<radialGradient>` for soft orb fills
- 2× `<filter>` definitions: one shadow for the diagonal block and one glow for decorative shapes

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgWash" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#F7FAFC"/>
      <stop offset="62%" stop-color="#EEF3F8"/>
      <stop offset="100%" stop-color="#E8EEF5"/>
    </linearGradient>

    <linearGradient id="diagonalMain" x1="0.1" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#1D4ED8"/>
      <stop offset="45%" stop-color="#6D28D9"/>
      <stop offset="100%" stop-color="#EC4899"/>
    </linearGradient>

    <linearGradient id="diagonalDeep" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#102A7A"/>
      <stop offset="100%" stop-color="#4C1D95"/>
    </linearGradient>

    <linearGradient id="accentGold" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#FDE68A"/>
      <stop offset="100%" stop-color="#F59E0B"/>
    </linearGradient>

    <radialGradient id="orbFill" cx="35%" cy="30%" r="70%">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.85"/>
      <stop offset="45%" stop-color="#93C5FD" stop-opacity="0.42"/>
      <stop offset="100%" stop-color="#7C3AED" stop-opacity="0.08"/>
    </radialGradient>

    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feOffset dx="-18" dy="20" result="off"/>
      <feGaussianBlur in="off" stdDeviation="24" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="ambientGlow" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="14" result="glow"/>
      <feMerge>
        <feMergeNode in="glow"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgWash)"/>

  <!-- Main diagonal graphic field -->
  <path d="M716 0 H1280 V720 H540 Z"
        fill="url(#diagonalMain)"
        filter="url(#softShadow)"/>

  <!-- Deep right-side diagonal plane -->
  <path d="M978 0 H1280 V720 H835 Z"
        fill="url(#diagonalDeep)"
        opacity="0.72"/>

  <!-- Angular translucent ribbons -->
  <path d="M762 70 L1280 0 L1280 88 L816 162 Z"
        fill="#FFFFFF"
        opacity="0.16"/>
  <path d="M690 515 L1280 322 L1280 392 L650 610 Z"
        fill="#FFFFFF"
        opacity="0.14"/>
  <path d="M905 172 L1280 72 L1280 125 L930 238 Z"
        fill="url(#accentGold)"
        opacity="0.82"/>

  <!-- Thin geometric highlight facets -->
  <path d="M850 0 L930 0 L617 720 L548 720 Z"
        fill="#FFFFFF"
        opacity="0.08"/>
  <path d="M1126 0 L1188 0 L893 720 L830 720 Z"
        fill="#000000"
        opacity="0.12"/>

  <!-- Floating decorative orbs -->
  <circle cx="1048" cy="168" r="76"
          fill="url(#orbFill)"
          opacity="0.65"
          filter="url(#ambientGlow)"/>
  <circle cx="1194" cy="514" r="112"
          fill="url(#orbFill)"
          opacity="0.45"
          filter="url(#ambientGlow)"/>
  <ellipse cx="894" cy="450" rx="54" ry="54"
           fill="#FFFFFF"
           opacity="0.18"/>
  <circle cx="777" cy="246" r="24"
          fill="#FDE68A"
          opacity="0.84"/>
  <ellipse cx="1132" cy="290" rx="18" ry="18"
           fill="#FFFFFF"
           opacity="0.36"/>

  <!-- Left text anchor accents -->
  <rect x="86" y="156" width="72" height="6" rx="3"
        fill="url(#accentGold)"/>
  <rect x="86" y="618" width="170" height="2" rx="1"
        fill="#CBD5E1"/>

  <!-- Eyebrow -->
  <text x="86" y="132"
        width="430"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="15"
        font-weight="700"
        letter-spacing="3"
        fill="#2563EB">
    STRATEGY BRIEFING
  </text>

  <!-- Main headline -->
  <text x="84" y="246"
        width="520"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="64"
        font-weight="800"
        fill="#0F172A">
    <tspan x="84" dy="0">Designing</tspan>
    <tspan x="84" dy="76">Momentum</tspan>
    <tspan x="84" dy="76">for Growth</tspan>
  </text>

  <!-- Subtitle -->
  <text x="88" y="500"
        width="468"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="22"
        font-weight="400"
        fill="#475569">
    A bold operating narrative for product expansion, market focus, and executive alignment.
  </text>

  <!-- Footer metadata -->
  <text x="88" y="652"
        width="500"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="14"
        font-weight="600"
        fill="#64748B">
    Q4 Executive Session  ·  Confidential
  </text>
</svg>
```

## Avoid in this skill
- ❌ `transform="skewX(...)"` or matrix transforms for the diagonal edge; draw the diagonal as explicit `<path>` coordinates instead.
- ❌ Putting text over the diagonal field unless it is very short and white; the strength of this layout is a clean left reading zone.
- ❌ Using `<clipPath>` on the diagonal shapes; clipping is unnecessary here and may be ignored on non-image elements.
- ❌ Adding shadows to `<line>` elements; use filled `<rect>` or `<path>` accents if a shadowed detail is needed.
- ❌ Overloading the right side with too many small shapes; keep the diagonal graphic bold and legible from a distance.

## Composition notes
- Reserve roughly the left 45% of the slide for text, with generous negative space and no busy decoration behind the headline.
- Let the diagonal begin around x=540–720 so it feels like it is cutting into the slide without crowding the title.
- Use one dominant gradient on the diagonal field, then repeat its colors in small accents such as the eyebrow text or gold highlight strip.
- Keep decorative circles and ribbons inside the right-side diagonal zone to reinforce motion while preserving the cover’s executive clarity.