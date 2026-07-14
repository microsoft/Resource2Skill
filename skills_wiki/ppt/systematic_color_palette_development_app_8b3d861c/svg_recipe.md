# SVG Recipe — Systematic Color Palette Development & Application

## Visual mechanism
A limited, logo-derived accent palette is applied consistently across a chart slide: neutrals carry structure and readability, while one accent color highlights the key data point, title underline, KPI, and palette legend. The slide teaches the palette system visually by showing the color tokens and their use in the chart at the same time.

## SVG primitives needed
- 1× `<rect>` for the clean neutral slide background
- 2× `<path>` for soft decorative background ribbons using low-opacity accent color
- 3× `<rect>` for premium white content cards with subtle shadows
- 6× `<rect>` for palette swatches showing accent, tint, dark text, mid gray, light gray, and white
- 4× `<rect>` for chart bars, with one accent-highlighted bar and remaining neutral/tint bars
- 5× `<line>` for chart gridlines and axis baseline
- 1× `<linearGradient id="accentGrad">` for the primary highlighted chart bar
- 1× `<linearGradient id="softBg">` for a barely tinted presentation background
- 1× `<filter id="cardShadow">` applied to cards
- 1× `<filter id="accentGlow">` applied to the key accent bar
- Multiple `<text>` elements with explicit `width` attributes for title, labels, swatch names, values, and explanatory notes

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="softBg" x1="0" y1="0" x2="1280" y2="720" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#FFFFFF"/>
      <stop offset="0.55" stop-color="#FAFAFA"/>
      <stop offset="1" stop-color="#FFF3EA"/>
    </linearGradient>
    <linearGradient id="accentGrad" x1="0" y1="520" x2="0" y2="250" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#FF6A00"/>
      <stop offset="1" stop-color="#FFB066"/>
    </linearGradient>
    <linearGradient id="neutralBar" x1="0" y1="520" x2="0" y2="280" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#D9D9D9"/>
      <stop offset="1" stop-color="#F2F2F2"/>
    </linearGradient>
    <filter id="cardShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feOffset dx="0" dy="10" in="SourceAlpha" result="off"/>
      <feGaussianBlur in="off" stdDeviation="12" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="accentGlow" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="7" result="glow"/>
      <feMerge>
        <feMergeNode in="glow"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#softBg)"/>
  <path d="M918,-42 C1088,4 1212,112 1305,252 L1305,0 L918,0 Z" fill="#FF6A00" opacity="0.08"/>
  <path d="M-70,598 C150,552 245,650 424,705 L-70,740 Z" fill="#FF6A00" opacity="0.07"/>

  <text x="70" y="74" width="700" font-family="Segoe UI, Microsoft YaHei" font-size="36" font-weight="700" fill="#282828">
    Systematic Color Palette
  </text>
  <text x="72" y="110" width="720" font-family="Segoe UI, Microsoft YaHei" font-size="18" fill="#666666">
    One accent, disciplined neutrals, repeated with intent
  </text>
  <rect x="70" y="128" width="245" height="8" rx="4" fill="#FF6A00"/>

  <rect x="70" y="170" width="365" height="132" rx="24" fill="#FFFFFF" filter="url(#cardShadow)"/>
  <text x="100" y="207" width="260" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#282828">
    LOGO-DERIVED PALETTE
  </text>
  <rect x="100" y="226" width="46" height="46" rx="12" fill="#FF6A00"/>
  <rect x="157" y="226" width="46" height="46" rx="12" fill="#FFE5D1"/>
  <rect x="214" y="226" width="46" height="46" rx="12" fill="#282828"/>
  <rect x="271" y="226" width="46" height="46" rx="12" fill="#8A8A8A"/>
  <rect x="328" y="226" width="46" height="46" rx="12" fill="#F2F2F2" stroke="#DDDDDD"/>
  <text x="100" y="291" width="310" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#666666">
    Accent is reserved for meaning: key data, action, and brand memory.
  </text>

  <rect x="470" y="170" width="740" height="448" rx="28" fill="#FFFFFF" filter="url(#cardShadow)"/>
  <text x="510" y="214" width="410" font-family="Segoe UI, Microsoft YaHei" font-size="22" font-weight="700" fill="#282828">
    Regional Revenue Performance
  </text>
  <text x="510" y="240" width="510" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#777777">
    Neutral bars provide context; accent bar directs attention to the business story.
  </text>

  <line x1="540" y1="520" x2="1135" y2="520" stroke="#282828" stroke-width="1.5"/>
  <line x1="540" y1="456" x2="1135" y2="456" stroke="#EEEEEE" stroke-width="1"/>
  <line x1="540" y1="392" x2="1135" y2="392" stroke="#EEEEEE" stroke-width="1"/>
  <line x1="540" y1="328" x2="1135" y2="328" stroke="#EEEEEE" stroke-width="1"/>
  <line x1="540" y1="264" x2="1135" y2="264" stroke="#EEEEEE" stroke-width="1"/>

  <rect x="590" y="364" width="82" height="156" rx="14" fill="url(#neutralBar)"/>
  <rect x="735" y="320" width="82" height="200" rx="14" fill="#FFE5D1"/>
  <rect x="880" y="272" width="82" height="248" rx="14" fill="url(#accentGrad)" filter="url(#accentGlow)"/>
  <rect x="1025" y="400" width="82" height="120" rx="14" fill="url(#neutralBar)"/>

  <text x="595" y="348" width="78" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" text-anchor="middle" fill="#555555">
    19.2
  </text>
  <text x="740" y="304" width="78" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" text-anchor="middle" fill="#555555">
    21.4
  </text>
  <text x="885" y="256" width="78" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="800" text-anchor="middle" fill="#FF6A00">
    26.8
  </text>
  <text x="1030" y="384" width="78" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" text-anchor="middle" fill="#555555">
    16.7
  </text>

  <text x="590" y="554" width="82" font-family="Segoe UI, Microsoft YaHei" font-size="13" text-anchor="middle" fill="#666666">East</text>
  <text x="735" y="554" width="82" font-family="Segoe UI, Microsoft YaHei" font-size="13" text-anchor="middle" fill="#666666">West</text>
  <text x="880" y="554" width="82" font-family="Segoe UI, Microsoft YaHei" font-size="13" text-anchor="middle" fill="#282828" font-weight="700">North</text>
  <text x="1025" y="554" width="82" font-family="Segoe UI, Microsoft YaHei" font-size="13" text-anchor="middle" fill="#666666">Midwest</text>

  <rect x="70" y="332" width="365" height="286" rx="24" fill="#FFFFFF" filter="url(#cardShadow)"/>
  <text x="100" y="375" width="270" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="700" fill="#282828">
    Application rules
  </text>
  <circle cx="113" cy="414" r="6" fill="#FF6A00"/>
  <text x="132" y="421" width="250" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#555555">
    Use accent for the single most important message.
  </text>
  <circle cx="113" cy="462" r="6" fill="#8A8A8A"/>
  <text x="132" y="469" width="250" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#555555">
    Use dark gray for titles and high-readability labels.
  </text>
  <circle cx="113" cy="510" r="6" fill="#F2F2F2" stroke="#CCCCCC"/>
  <text x="132" y="517" width="250" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#555555">
    Use light gray for grids, dividers, and quiet structure.
  </text>
  <rect x="100" y="552" width="270" height="38" rx="19" fill="#FF6A00"/>
  <text x="124" y="577" width="220" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#FFFFFF">
    Palette discipline = instant polish
  </text>

  <rect x="930" y="205" width="210" height="48" rx="24" fill="#FFF3EA" stroke="#FFB066"/>
  <text x="958" y="235" width="160" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#FF6A00">
    Highlighted by palette
  </text>
</svg>
```

## Avoid in this skill
- ❌ Random rainbow palettes for chart categories; they weaken hierarchy and make the slide look unbranded.
- ❌ Equal saturation for every element; the accent color should be rare enough to feel meaningful.
- ❌ Pure black body text on pure white for all typography; use near-black and gray neutrals for a more premium tone.
- ❌ Applying gradients, glows, or shadows to every bar; reserve visual effects for the highlighted datapoint.
- ❌ Using low-contrast accent text on tinted backgrounds; verify every label remains readable.

## Composition notes
- Keep the palette explanation compact on the left and the applied chart large on the right so the viewer sees both the rule and the result.
- Use white or very light warm-gray negative space as the dominant color; the accent should occupy a small but memorable percentage of the slide.
- Repeat the accent in three places only: title underline, key data bar, and call-to-action chip.
- Let gridlines, secondary bars, and supporting notes recede into light neutrals to make the highlighted data point feel intentional.