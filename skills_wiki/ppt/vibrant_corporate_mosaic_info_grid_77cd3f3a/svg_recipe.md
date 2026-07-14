# SVG Recipe — Vibrant Corporate Mosaic Info Grid

## Visual mechanism
A disciplined 2×4 mosaic of equal-sized, high-saturation corporate cards turns a list of project or product categories into a scannable executive grid. Each tile uses a bold color, white vector icon, compact title, and two-line explanation, with subtle shadows and oversized translucent geometric accents to keep the flat layout premium rather than plain.

## SVG primitives needed
- 1× `<rect>` for the full-slide background
- 1× `<linearGradient>` for a very subtle background wash
- 1× `<filter id="cardShadow">` using `feOffset + feGaussianBlur + feMerge`, applied to card rectangles
- 8× `<rect>` for the colored mosaic cards
- 8× translucent `<circle>` / `<ellipse>` accents inside cards for visual depth
- 18–24× `<path>` primitives for crisp white editable icons
- 30+× `<text>` elements for header, subtitle, card titles, and short body copy
- Optional 1× `<path>` or `<rect>` accent rule under the header to connect title and grid

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgWash" x1="0" y1="0" x2="1280" y2="720" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#FFFFFF"/>
      <stop offset="1" stop-color="#F2F5F8"/>
    </linearGradient>
    <filter id="cardShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="7" in="SourceAlpha" result="off"/>
      <feGaussianBlur in="off" stdDeviation="7" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgWash)"/>
  <text x="64" y="64" width="720" font-family="Segoe UI, Microsoft YaHei" font-size="38" font-weight="700" fill="#323A45">Product Overview</text>
  <text x="66" y="101" width="760" font-family="Segoe UI, Microsoft YaHei" font-size="17" fill="#7A8491">Eight focus areas organized as a vibrant corporate decision grid</text>
  <rect x="64" y="126" width="210" height="5" rx="2.5" fill="#2DA8D8"/>
  <text x="1010" y="76" width="200" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#6C7580" text-anchor="end">2026 STRATEGY SNAPSHOT</text>

  <g transform="translate(65 160)">
    <rect x="0" y="0" width="280" height="235" rx="10" fill="#2DA8D8" filter="url(#cardShadow)"/>
    <circle cx="244" cy="28" r="62" fill="#FFFFFF" opacity="0.13"/>
    <path d="M138 27 L111 78 L135 76 L123 117 L172 55 L147 58 Z" fill="#FFFFFF"/>
    <text x="140" y="133" width="230" font-family="Segoe UI, Microsoft YaHei" font-size="19" font-weight="700" fill="#FFFFFF" text-anchor="middle">Problem Statement</text>
    <text x="140" y="164" width="230" font-family="Segoe UI, Microsoft YaHei" font-size="13.5" fill="#FFFFFF" opacity="0.92" text-anchor="middle">Define the business reason</text>
    <text x="140" y="184" width="230" font-family="Segoe UI, Microsoft YaHei" font-size="13.5" fill="#FFFFFF" opacity="0.92" text-anchor="middle">and the issue to solve.</text>
  </g>

  <g transform="translate(355 160)">
    <rect x="0" y="0" width="280" height="235" rx="10" fill="#247BA0" filter="url(#cardShadow)"/>
    <ellipse cx="238" cy="190" rx="72" ry="46" fill="#FFFFFF" opacity="0.12"/>
    <path d="M112 35 H158 L176 53 V112 H112 Z" fill="none" stroke="#FFFFFF" stroke-width="8" stroke-linejoin="round"/>
    <path d="M158 35 V56 H176" fill="none" stroke="#FFFFFF" stroke-width="8" stroke-linejoin="round"/>
    <path d="M126 69 H162 M126 87 H160" fill="none" stroke="#FFFFFF" stroke-width="6" stroke-linecap="round"/>
    <text x="140" y="133" width="230" font-family="Segoe UI, Microsoft YaHei" font-size="19" font-weight="700" fill="#FFFFFF" text-anchor="middle">Project Description</text>
    <text x="140" y="164" width="230" font-family="Segoe UI, Microsoft YaHei" font-size="13.5" fill="#FFFFFF" opacity="0.92" text-anchor="middle">Summarize the approach</text>
    <text x="140" y="184" width="230" font-family="Segoe UI, Microsoft YaHei" font-size="13.5" fill="#FFFFFF" opacity="0.92" text-anchor="middle">and operating model.</text>
  </g>

  <g transform="translate(645 160)">
    <rect x="0" y="0" width="280" height="235" rx="10" fill="#75C043" filter="url(#cardShadow)"/>
    <circle cx="30" cy="38" r="68" fill="#FFFFFF" opacity="0.12"/>
    <circle cx="140" cy="74" r="43" fill="none" stroke="#FFFFFF" stroke-width="7"/>
    <circle cx="140" cy="74" r="25" fill="none" stroke="#FFFFFF" stroke-width="7"/>
    <circle cx="140" cy="74" r="7" fill="#FFFFFF"/>
    <path d="M174 40 L193 21 M193 21 H174 M193 21 V40" fill="none" stroke="#FFFFFF" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>
    <text x="140" y="133" width="230" font-family="Segoe UI, Microsoft YaHei" font-size="19" font-weight="700" fill="#FFFFFF" text-anchor="middle">Goals &amp; Objectives</text>
    <text x="140" y="164" width="230" font-family="Segoe UI, Microsoft YaHei" font-size="13.5" fill="#FFFFFF" opacity="0.92" text-anchor="middle">Translate strategy into</text>
    <text x="140" y="184" width="230" font-family="Segoe UI, Microsoft YaHei" font-size="13.5" fill="#FFFFFF" opacity="0.92" text-anchor="middle">measurable outcomes.</text>
  </g>

  <g transform="translate(935 160)">
    <rect x="0" y="0" width="280" height="235" rx="10" fill="#F6AE2D" filter="url(#cardShadow)"/>
    <ellipse cx="250" cy="40" rx="82" ry="54" fill="#FFFFFF" opacity="0.15"/>
    <path d="M140 29 L153 59 L186 62 L161 83 L169 116 L140 98 L111 116 L119 83 L94 62 L127 59 Z" fill="#FFFFFF"/>
    <text x="140" y="133" width="230" font-family="Segoe UI, Microsoft YaHei" font-size="19" font-weight="700" fill="#FFFFFF" text-anchor="middle">Assumptions</text>
    <text x="140" y="164" width="230" font-family="Segoe UI, Microsoft YaHei" font-size="13.5" fill="#FFFFFF" opacity="0.94" text-anchor="middle">Capture known constraints</text>
    <text x="140" y="184" width="230" font-family="Segoe UI, Microsoft YaHei" font-size="13.5" fill="#FFFFFF" opacity="0.94" text-anchor="middle">and planning dependencies.</text>
  </g>

  <g transform="translate(65 405)">
    <rect x="0" y="0" width="280" height="235" rx="10" fill="#F26419" filter="url(#cardShadow)"/>
    <circle cx="252" cy="198" r="75" fill="#FFFFFF" opacity="0.13"/>
    <path d="M95 72 C95 47 115 27 140 27 C165 27 185 47 185 72 C185 97 165 117 140 117 C115 117 95 97 95 72 Z" fill="none" stroke="#FFFFFF" stroke-width="8"/>
    <path d="M119 72 H161 M140 51 V93" fill="none" stroke="#FFFFFF" stroke-width="7" stroke-linecap="round"/>
    <text x="140" y="133" width="230" font-family="Segoe UI, Microsoft YaHei" font-size="19" font-weight="700" fill="#FFFFFF" text-anchor="middle">Project Scope</text>
    <text x="140" y="164" width="230" font-family="Segoe UI, Microsoft YaHei" font-size="13.5" fill="#FFFFFF" opacity="0.92" text-anchor="middle">Define boundaries, owners</text>
    <text x="140" y="184" width="230" font-family="Segoe UI, Microsoft YaHei" font-size="13.5" fill="#FFFFFF" opacity="0.92" text-anchor="middle">and delivery limits.</text>
  </g>

  <g transform="translate(355 405)">
    <rect x="0" y="0" width="280" height="235" rx="10" fill="#D93F4C" filter="url(#cardShadow)"/>
    <ellipse cx="38" cy="202" rx="78" ry="50" fill="#FFFFFF" opacity="0.12"/>
    <path d="M140 32 V112 M100 72 H180" fill="none" stroke="#FFFFFF" stroke-width="15" stroke-linecap="round"/>
    <text x="140" y="133" width="230" font-family="Segoe UI, Microsoft YaHei" font-size="19" font-weight="700" fill="#FFFFFF" text-anchor="middle">Project Inclusions</text>
    <text x="140" y="164" width="230" font-family="Segoe UI, Microsoft YaHei" font-size="13.5" fill="#FFFFFF" opacity="0.92" text-anchor="middle">List committed activities,</text>
    <text x="140" y="184" width="230" font-family="Segoe UI, Microsoft YaHei" font-size="13.5" fill="#FFFFFF" opacity="0.92" text-anchor="middle">features and deliverables.</text>
  </g>

  <g transform="translate(645 405)">
    <rect x="0" y="0" width="280" height="235" rx="10" fill="#8E44AD" filter="url(#cardShadow)"/>
    <circle cx="247" cy="38" r="66" fill="#FFFFFF" opacity="0.13"/>
    <path d="M99 72 H181" fill="none" stroke="#FFFFFF" stroke-width="16" stroke-linecap="round"/>
    <path d="M102 35 L178 111" fill="none" stroke="#FFFFFF" stroke-width="8" stroke-linecap="round" opacity="0.85"/>
    <text x="140" y="133" width="230" font-family="Segoe UI, Microsoft YaHei" font-size="19" font-weight="700" fill="#FFFFFF" text-anchor="middle">Project Exclusions</text>
    <text x="140" y="164" width="230" font-family="Segoe UI, Microsoft YaHei" font-size="13.5" fill="#FFFFFF" opacity="0.92" text-anchor="middle">Clarify what is outside</text>
    <text x="140" y="184" width="230" font-family="Segoe UI, Microsoft YaHei" font-size="13.5" fill="#FFFFFF" opacity="0.92" text-anchor="middle">the current mandate.</text>
  </g>

  <g transform="translate(935 405)">
    <rect x="0" y="0" width="280" height="235" rx="10" fill="#2BACB8" filter="url(#cardShadow)"/>
    <ellipse cx="37" cy="35" rx="74" ry="54" fill="#FFFFFF" opacity="0.12"/>
    <path d="M94 48 L140 25 L186 48 V78 C186 104 163 119 140 124 C117 119 94 104 94 78 Z" fill="none" stroke="#FFFFFF" stroke-width="8" stroke-linejoin="round"/>
    <path d="M118 73 L135 90 L164 58" fill="none" stroke="#FFFFFF" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/>
    <text x="140" y="133" width="230" font-family="Segoe UI, Microsoft YaHei" font-size="19" font-weight="700" fill="#FFFFFF" text-anchor="middle">Critical Success</text>
    <text x="140" y="164" width="230" font-family="Segoe UI, Microsoft YaHei" font-size="13.5" fill="#FFFFFF" opacity="0.92" text-anchor="middle">Identify conditions that</text>
    <text x="140" y="184" width="230" font-family="Segoe UI, Microsoft YaHei" font-size="13.5" fill="#FFFFFF" opacity="0.92" text-anchor="middle">make execution viable.</text>
  </g>
</svg>
```

## Avoid in this skill
- ❌ Using `<symbol>` / `<use>` for repeated icons; duplicate the icon paths directly so PowerPoint receives editable shapes.
- ❌ Applying `clip-path` to the colored card rectangles to crop decorative accents; clipping only translates reliably on `<image>`.
- ❌ Long paragraphs inside cards; PowerPoint text boxes will be editable but dense copy destroys the grid’s scanability.
- ❌ Low-contrast pastel fills with gray text; this technique depends on saturated fills and white typography.
- ❌ Filters on `<line>` icons; use `<path>` strokes for icon strokes if a shape may need visual effects.

## Composition notes
- Keep the header in the top 18–20% of the slide; the mosaic should dominate the lower three-quarters.
- Use equal card dimensions and consistent gutters to preserve the “corporate system” feel.
- Place icons in the upper half of each card, titles just below, and body copy in two short centered lines.
- Rotate hues across the grid so adjacent cards contrast strongly; avoid grouping similar blues or reds side by side.