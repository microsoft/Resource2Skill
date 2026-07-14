# SVG Recipe — Four Column Split Feature

## Visual mechanism
A premium editorial slide divided into four full-height vertical zones: an introduction column, a full-bleed photographic column, and two contrasting feature columns. The power comes from strong column color blocking, a cropped image wedge, oversized numbering, and restrained icon/details inside each feature panel.

## SVG primitives needed
- 4× full-height `<rect>` panels for the four vertical columns and alternating backgrounds
- 1× `<image>` clipped into a tall editorial column crop
- 1× `<clipPath>` with a custom `<path>` for the slanted image crop
- 2× `<linearGradient>` fills for premium feature-column color depth
- 1× `<filter id="softShadow">` applied to floating label cards / icon tiles
- 2× `<rect>` icon tiles with rounded corners
- 4× `<path>` elements for simple editable line icons and decorative overlays
- 4× `<line>` elements for subtle vertical separators and accent rules
- Multiple `<text>` elements with explicit `width` attributes for title, intro, feature numbers, labels, headings, body copy, and bullets

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="introWash" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#F7F2EA"/>
      <stop offset="100%" stop-color="#EDE6DA"/>
    </linearGradient>
    <linearGradient id="navyPanel" x1="620" y1="0" x2="950" y2="720" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#17364A"/>
      <stop offset="62%" stop-color="#0E2432"/>
      <stop offset="100%" stop-color="#081820"/>
    </linearGradient>
    <linearGradient id="copperPanel" x1="950" y1="0" x2="1280" y2="720" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#E3B36D"/>
      <stop offset="52%" stop-color="#CF874A"/>
      <stop offset="100%" stop-color="#A85C39"/>
    </linearGradient>
    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="12" in="SourceAlpha" result="off"/>
      <feGaussianBlur in="off" stdDeviation="16" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <clipPath id="photoColumnClip">
      <path d="M330 0 H642 L610 720 H330 Z"/>
    </clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#F4EFE7"/>
  <rect x="0" y="0" width="330" height="720" fill="url(#introWash)"/>
  <rect x="620" y="0" width="330" height="720" fill="url(#navyPanel)"/>
  <rect x="950" y="0" width="330" height="720" fill="url(#copperPanel)"/>

  <image x="300" y="0" width="370" height="720" preserveAspectRatio="xMidYMid slice"
         clip-path="url(#photoColumnClip)"
         href="https://images.example.com/editorial-photo-of-architectural-glass-facade-and-people.jpg"/>

  <path d="M330 0 H642 L610 720 H330 Z" fill="#0B1820" opacity="0.16"/>
  <line x1="329" y1="0" x2="329" y2="720" stroke="#D9CFC0" stroke-width="1"/>
  <line x1="620" y1="0" x2="620" y2="720" stroke="#FFFFFF" stroke-width="1" opacity="0.24"/>
  <line x1="950" y1="0" x2="950" y2="720" stroke="#FFFFFF" stroke-width="1" opacity="0.22"/>
  <line x1="1220" y1="78" x2="1260" y2="78" stroke="#F7E2BF" stroke-width="3"/>

  <text x="48" y="78" width="230" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700"
        letter-spacing="2.5" fill="#9A6B3D">STRATEGIC SPLIT</text>
  <text x="48" y="158" width="240" font-family="Segoe UI, Microsoft YaHei" font-size="48" font-weight="700"
        fill="#17212A">
    <tspan x="48" dy="0">Four ways</tspan>
    <tspan x="48" dy="54">to frame</tspan>
    <tspan x="48" dy="54">one story</tspan>
  </text>
  <rect x="48" y="342" width="52" height="4" fill="#C97A45"/>
  <text x="48" y="390" width="235" font-family="Segoe UI, Microsoft YaHei" font-size="17"
        fill="#4B4A45">
    <tspan x="48" dy="0">Use this shell when a</tspan>
    <tspan x="48" dy="25">short executive setup must</tspan>
    <tspan x="48" dy="25">sit beside a bold image and</tspan>
    <tspan x="48" dy="25">two high-contrast feature</tspan>
    <tspan x="48" dy="25">pillars.</tspan>
  </text>
  <text x="48" y="660" width="210" font-family="Segoe UI, Microsoft YaHei" font-size="12"
        letter-spacing="1.8" fill="#8B8277">EDITORIAL / FEATURE GRID</text>

  <rect x="675" y="78" width="86" height="86" rx="22" fill="#FFFFFF" opacity="0.08" filter="url(#softShadow)"/>
  <path d="M704 125 C704 110 716 98 731 98 C746 98 758 110 758 125 C758 140 746 152 731 152 C716 152 704 140 704 125 Z"
        fill="none" stroke="#9ED8E6" stroke-width="4"/>
  <path d="M715 126 L727 138 L750 112" fill="none" stroke="#F7E2BF" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>

  <text x="675" y="236" width="210" font-family="Segoe UI, Microsoft YaHei" font-size="92"
        font-weight="700" fill="#FFFFFF" opacity="0.12">01</text>
  <text x="675" y="288" width="205" font-family="Segoe UI, Microsoft YaHei" font-size="28"
        font-weight="700" fill="#FFFFFF">
    <tspan x="675" dy="0">Clarify the</tspan>
    <tspan x="675" dy="34">decision lens</tspan>
  </text>
  <text x="675" y="370" width="214" font-family="Segoe UI, Microsoft YaHei" font-size="16"
        fill="#C7D6DC">
    <tspan x="675" dy="0">Anchor the audience with</tspan>
    <tspan x="675" dy="24">criteria, constraints, and</tspan>
    <tspan x="675" dy="24">the tradeoffs that matter.</tspan>
  </text>
  <circle cx="684" cy="486" r="4" fill="#9ED8E6"/>
  <text x="700" y="492" width="185" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#EAF4F6">Sharper executive alignment</text>
  <circle cx="684" cy="526" r="4" fill="#9ED8E6"/>
  <text x="700" y="532" width="185" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#EAF4F6">Faster path to action</text>

  <rect x="1005" y="78" width="86" height="86" rx="22" fill="#FFF7EA" opacity="0.92" filter="url(#softShadow)"/>
  <path d="M1026 132 C1042 102 1070 102 1086 132" fill="none" stroke="#A85C39" stroke-width="5" stroke-linecap="round"/>
  <path d="M1031 134 H1081 M1040 148 H1072" fill="none" stroke="#17364A" stroke-width="5" stroke-linecap="round"/>
  <path d="M1174 292 C1210 252 1252 268 1276 318 L1276 720 H1122 C1122 610 1127 382 1174 292 Z"
        fill="#FFFFFF" opacity="0.10"/>

  <text x="1005" y="236" width="210" font-family="Segoe UI, Microsoft YaHei" font-size="92"
        font-weight="700" fill="#3B1F18" opacity="0.18">02</text>
  <text x="1005" y="288" width="218" font-family="Segoe UI, Microsoft YaHei" font-size="28"
        font-weight="700" fill="#FFFFFF">
    <tspan x="1005" dy="0">Package the</tspan>
    <tspan x="1005" dy="34">proof points</tspan>
  </text>
  <text x="1005" y="370" width="220" font-family="Segoe UI, Microsoft YaHei" font-size="16"
        fill="#FFF0DA">
    <tspan x="1005" dy="0">Use the right column for</tspan>
    <tspan x="1005" dy="24">evidence, customer signal,</tspan>
    <tspan x="1005" dy="24">or measurable business lift.</tspan>
  </text>
  <circle cx="1014" cy="486" r="4" fill="#FFF7EA"/>
  <text x="1030" y="492" width="185" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#FFF8ED">Memorable proof hierarchy</text>
  <circle cx="1014" cy="526" r="4" fill="#FFF7EA"/>
  <text x="1030" y="532" width="185" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#FFF8ED">Clear next-step narrative</text>
</svg>
```

## Avoid in this skill
- ❌ Four identical white cards in a plain grid; the technique depends on full-height editorial columns and alternating visual weight.
- ❌ Applying `clip-path` to rectangles or paths for decorative crops; only clip the `<image>` so the PPTX translator preserves the crop reliably.
- ❌ Using `<pattern>` or `<mask>` for the photo treatment; use an image clipPath plus translucent overlay paths instead.
- ❌ Long paragraphs in the feature columns; keep each feature to a heading, 2–3 body lines, and two compact bullets.

## Composition notes
- Keep the first column text-heavy but airy: title and intro should occupy the upper/middle left, with generous negative space below.
- The image column should feel full-bleed and editorial; a slanted crop adds movement without disrupting the four-column logic.
- Feature columns should alternate dark and warm backgrounds, with large low-opacity numerals to create hierarchy.
- Align feature content vertically across columns so the slide reads as a comparison, while icons and color accents give each pillar its own identity.