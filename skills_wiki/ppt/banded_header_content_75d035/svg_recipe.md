# SVG Recipe — Banded Header Content

## Visual mechanism
A strong horizontal header band anchors the slide near the top: a thick, centered title banner is visually extended by thin flanking rules. The body content sits below in a calm executive panel, preserving negative space while the band establishes hierarchy and section-divider polish.

## SVG primitives needed
- 12× `<rect>` for the background, flanking header rules, banner highlight strip, content panel, accent rail, metric cards, and card top bars
- 4× `<path>` for soft decorative background geometry, the notched central header banner, and a small chevron underline accent
- 5× `<circle>` for banner rivets and body bullet markers
- 10× `<text>` for eyebrow label, headline, body copy, bullets, and metric-card labels
- 4× `<linearGradient>` for the background, central band, pale panel, and accent fills
- 1× `<radialGradient>` for a subtle top-right atmosphere glow
- 2× `<filter>` definitions for editable soft shadow and glow applied to rect/path/circle/text shapes

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#F7FAFD"/>
      <stop offset="55%" stop-color="#EEF4F9"/>
      <stop offset="100%" stop-color="#E4ECF4"/>
    </linearGradient>
    <radialGradient id="atmosphere" cx="82%" cy="8%" r="70%">
      <stop offset="0%" stop-color="#BBD7F2" stop-opacity="0.65"/>
      <stop offset="55%" stop-color="#BBD7F2" stop-opacity="0.14"/>
      <stop offset="100%" stop-color="#BBD7F2" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="bandGrad" x1="304" y1="72" x2="976" y2="136" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#102B46"/>
      <stop offset="48%" stop-color="#1F5C88"/>
      <stop offset="100%" stop-color="#0E2A45"/>
    </linearGradient>
    <linearGradient id="panelGrad" x1="154" y1="206" x2="1126" y2="584" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="100%" stop-color="#F4F8FB"/>
    </linearGradient>
    <linearGradient id="accentGrad" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#5BD2FF"/>
      <stop offset="100%" stop-color="#2A6F9E"/>
    </linearGradient>
    <filter id="softShadow" x="-20%" y="-30%" width="140%" height="170%">
      <feOffset dx="0" dy="10"/>
      <feGaussianBlur stdDeviation="14"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="coolGlow" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="8"/>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>
  <rect x="0" y="0" width="1280" height="720" fill="url(#atmosphere)"/>

  <path d="M-60 104 C148 24 250 10 386 64 C260 104 142 146 -12 228 Z" fill="#D6E8F7" opacity="0.48"/>
  <path d="M846 -40 C1042 10 1188 96 1350 218 L1350 0 L846 0 Z" fill="#C9DCEC" opacity="0.38"/>
  <path d="M1014 610 C1088 556 1168 544 1292 570 L1292 720 L948 720 C960 672 978 636 1014 610 Z" fill="#DCE8F2" opacity="0.55"/>

  <rect x="78" y="102" width="246" height="4" rx="2" fill="#315F82" opacity="0.72"/>
  <rect x="956" y="102" width="246" height="4" rx="2" fill="#315F82" opacity="0.72"/>
  <path d="M338 72 H942 L976 104 L942 136 H338 L304 104 Z" fill="url(#bandGrad)" filter="url(#softShadow)"/>
  <rect x="354" y="81" width="572" height="7" rx="3.5" fill="#8FDFFF" opacity="0.24"/>
  <circle cx="326" cy="104" r="7" fill="#7DE2FF" opacity="0.95" filter="url(#coolGlow)"/>
  <circle cx="954" cy="104" r="7" fill="#7DE2FF" opacity="0.95" filter="url(#coolGlow)"/>

  <text x="640" y="58" width="520" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" letter-spacing="3" fill="#4D6C82">
    EXECUTIVE OPERATING BRIEF
  </text>
  <text x="640" y="114" width="610" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="30" font-weight="700" fill="#FFFFFF">
    Banded Header Content
  </text>

  <rect x="154" y="206" width="972" height="378" rx="24" fill="url(#panelGrad)" filter="url(#softShadow)"/>
  <rect x="184" y="238" width="6" height="258" rx="3" fill="url(#accentGrad)"/>
  <path d="M214 236 H428 L410 252 H214 Z" fill="#2A6F9E" opacity="0.14"/>

  <text x="214" y="258" width="820" font-family="Segoe UI, Microsoft YaHei" font-size="30" font-weight="700" fill="#18324A">
    Why this model works
  </text>
  <text x="214" y="304" width="850" font-family="Segoe UI, Microsoft YaHei" font-size="18" fill="#536879">
    <tspan x="214" dy="0">The band creates an immediate reading order: first the topic, then the supporting narrative.</tspan>
    <tspan x="214" dy="28">Use it when a slide needs to feel structured, formal, and presentation-ready without becoming dense.</tspan>
  </text>

  <circle cx="224" cy="363" r="5" fill="#2A6F9E"/>
  <text x="244" y="370" width="770" font-family="Segoe UI, Microsoft YaHei" font-size="17" fill="#334B5F">
    Strong top anchor prevents the page from feeling empty on low-density content slides.
  </text>
  <circle cx="224" cy="403" r="5" fill="#2A6F9E"/>
  <text x="244" y="410" width="770" font-family="Segoe UI, Microsoft YaHei" font-size="17" fill="#334B5F">
    Thin side rules extend the header visually while preserving a refined, minimal footprint.
  </text>
  <circle cx="224" cy="443" r="5" fill="#2A6F9E"/>
  <text x="244" y="450" width="770" font-family="Segoe UI, Microsoft YaHei" font-size="17" fill="#334B5F">
    The content panel below can hold a short narrative, recommendation, or section introduction.
  </text>

  <rect x="214" y="494" width="258" height="58" rx="14" fill="#FFFFFF" stroke="#D8E4EE"/>
  <rect x="214" y="494" width="258" height="5" rx="2.5" fill="#5BD2FF"/>
  <text x="236" y="530" width="214" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#19364F">
    Best for section dividers
  </text>

  <rect x="510" y="494" width="258" height="58" rx="14" fill="#FFFFFF" stroke="#D8E4EE"/>
  <rect x="510" y="494" width="258" height="5" rx="2.5" fill="#2A6F9E"/>
  <text x="532" y="530" width="214" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#19364F">
    Low-density narrative pages
  </text>

  <rect x="806" y="494" width="258" height="58" rx="14" fill="#FFFFFF" stroke="#D8E4EE"/>
  <rect x="806" y="494" width="258" height="5" rx="2.5" fill="#163B5A"/>
  <text x="828" y="530" width="214" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#19364F">
    Corporate keynote rhythm
  </text>
</svg>
```

## Avoid in this skill
- ❌ Do not replace the flanking rules with arrowed paths; `marker-end` on paths may disappear, and arrows weaken the quiet executive tone.
- ❌ Do not apply `filter` to `<line>` elements for the side rules; use thin rounded `<rect>` rules instead.
- ❌ Do not put the headline in an unconstrained `<text>` box; every text element needs an explicit `width` so PowerPoint keeps the intended wrapping.
- ❌ Do not overcrowd the body area with dense grids; the banded header depends on generous negative space and a clear top-to-bottom hierarchy.

## Composition notes
- Keep the band in the upper 15–20% of the slide; it should feel like an architectural header, not a mid-slide label.
- The center banner should carry the primary headline, while the flanking rules extend the visual width without adding visual weight.
- Place body content in a single calm block beneath the band, ideally starting around y=220 with ample margins.
- Use cool corporate blues, pale gray-blue backgrounds, and one bright cyan accent to create rhythm without distracting from the title.