# SVG Recipe — Centered Metric Panel

## Visual mechanism
A single oversized metric sits inside a centered, elevated panel with soft glow, subtle gradients, and restrained executive-style ornamentation. The surrounding slide is intentionally quiet so the viewer’s eye lands immediately on the number.

## SVG primitives needed
- 1× `<rect>` for the full-slide gradient background
- 3× blurred `<path>` blobs for atmospheric depth behind the panel
- 1× large rounded `<rect>` for the main metric panel
- 2× rounded `<rect>` overlays for glass highlight and inner border
- 2× `<ellipse>` halos behind the metric to create a premium spotlight effect
- 1× `<path>` decorative top accent arc inside the card
- 4× `<line>` elements for fine divider and corner accents
- 4× `<text>` elements for eyebrow, metric, unit/context, and caption; every text element includes explicit `width`
- 3× `<linearGradient>` definitions for background, card, and accent stroke
- 2× `<radialGradient>` definitions for glow fields
- 3× `<filter>` definitions for shadow, blur glow, and metric glow

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1280" y2="720" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#07111F"/>
      <stop offset="0.48" stop-color="#0B1730"/>
      <stop offset="1" stop-color="#111827"/>
    </linearGradient>

    <linearGradient id="cardGrad" x1="410" y1="182" x2="870" y2="548" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#182744"/>
      <stop offset="0.52" stop-color="#101C32"/>
      <stop offset="1" stop-color="#0B1324"/>
    </linearGradient>

    <linearGradient id="accentGrad" x1="420" y1="220" x2="860" y2="220" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#38BDF8" stop-opacity="0"/>
      <stop offset="0.5" stop-color="#67E8F9" stop-opacity="1"/>
      <stop offset="1" stop-color="#A78BFA" stop-opacity="0"/>
    </linearGradient>

    <radialGradient id="cyanGlow" cx="50%" cy="50%" r="50%">
      <stop offset="0" stop-color="#22D3EE" stop-opacity="0.55"/>
      <stop offset="0.58" stop-color="#2563EB" stop-opacity="0.18"/>
      <stop offset="1" stop-color="#0F172A" stop-opacity="0"/>
    </radialGradient>

    <radialGradient id="violetGlow" cx="50%" cy="50%" r="50%">
      <stop offset="0" stop-color="#A78BFA" stop-opacity="0.36"/>
      <stop offset="0.64" stop-color="#7C3AED" stop-opacity="0.14"/>
      <stop offset="1" stop-color="#0F172A" stop-opacity="0"/>
    </radialGradient>

    <filter id="softBlur" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="34"/>
    </filter>

    <filter id="panelShadow" x="-25%" y="-25%" width="150%" height="160%">
      <feOffset dx="0" dy="22"/>
      <feGaussianBlur stdDeviation="24"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="metricGlow" x="-30%" y="-40%" width="160%" height="180%">
      <feGaussianBlur stdDeviation="3" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>

  <path d="M118 100 C252 28 375 67 437 176 C498 282 418 382 283 384 C146 386 28 292 43 196 C50 151 78 122 118 100 Z"
        fill="url(#cyanGlow)" filter="url(#softBlur)" opacity="0.75"/>
  <path d="M948 76 C1087 15 1226 80 1244 205 C1263 334 1132 421 1012 374 C900 331 836 217 887 133 C902 108 922 90 948 76 Z"
        fill="url(#violetGlow)" filter="url(#softBlur)" opacity="0.85"/>
  <path d="M498 590 C611 520 758 535 826 622 C888 702 764 754 613 735 C478 717 387 658 498 590 Z"
        fill="url(#cyanGlow)" filter="url(#softBlur)" opacity="0.38"/>

  <ellipse cx="640" cy="365" rx="275" ry="155" fill="url(#cyanGlow)" opacity="0.24"/>
  <ellipse cx="640" cy="365" rx="205" ry="102" fill="url(#violetGlow)" opacity="0.22"/>

  <rect x="400" y="174" width="480" height="372" rx="34"
        fill="url(#cardGrad)" stroke="#243B63" stroke-width="1.5" filter="url(#panelShadow)"/>
  <rect x="415" y="189" width="450" height="342" rx="26"
        fill="none" stroke="#FFFFFF" stroke-opacity="0.11" stroke-width="1"/>
  <rect x="428" y="201" width="424" height="86" rx="22"
        fill="#FFFFFF" opacity="0.035"/>

  <path d="M454 228 C518 202 596 199 640 216 C690 235 760 230 826 202"
        fill="none" stroke="url(#accentGrad)" stroke-width="3" stroke-linecap="round"/>
  <line x1="452" y1="302" x2="828" y2="302" stroke="#8AB4F8" stroke-opacity="0.18" stroke-width="1"/>
  <line x1="452" y1="486" x2="828" y2="486" stroke="#8AB4F8" stroke-opacity="0.18" stroke-width="1"/>

  <line x1="424" y1="214" x2="466" y2="214" stroke="#67E8F9" stroke-opacity="0.9" stroke-width="2" stroke-linecap="round"/>
  <line x1="814" y1="506" x2="856" y2="506" stroke="#A78BFA" stroke-opacity="0.9" stroke-width="2" stroke-linecap="round"/>

  <text x="640" y="263" width="360" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="17" font-weight="700"
        letter-spacing="3" fill="#9DDCFB">
    GO-LIVE READINESS
  </text>

  <text x="640" y="411" width="430" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="118" font-weight="800"
        fill="#F8FAFC" filter="url(#metricGlow)">
    92%
  </text>

  <text x="640" y="455" width="340" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="22" font-weight="600"
        fill="#B7C7E6">
    launch confidence index
  </text>

  <text x="640" y="514" width="390" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="14"
        fill="#7E8DA8">
    Updated after final integration checkpoint
  </text>
</svg>
```

## Avoid in this skill
- ❌ Adding multiple competing charts or KPI cards; the technique works because one number owns the slide.
- ❌ Using `<filter>` on `<line>` for glowing dividers; line filters are dropped, so use gradient strokes or nearby blurred shapes instead.
- ❌ Cropping decorative glows with `clip-path` on non-image elements; clipping only translates reliably for `<image>`.
- ❌ Using huge text without an explicit `width` attribute; PowerPoint may render the metric differently without it.
- ❌ Heavy dashed borders around the central card; they make the metric feel like a dashboard widget instead of an executive focal point.

## Composition notes
- Keep the card centered and occupy roughly 35–45% of slide width; the surrounding negative space is part of the premium effect.
- Place the metric on the optical center, slightly below the card midpoint, with a small eyebrow above and a short caption below.
- Use saturated cyan/violet accents sparingly; most of the slide should remain dark, muted, and calm.
- Background blobs should sit behind the card and remain soft enough to create atmosphere without becoming separate visual subjects.