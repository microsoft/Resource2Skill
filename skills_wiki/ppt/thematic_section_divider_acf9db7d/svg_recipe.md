# SVG Recipe — Thematic Section Divider

## Visual mechanism
A polished section divider splits the slide into a symbolic “chapter card” on the left and a mini-agenda timeline on the right. The title banner, framed thematic icon, numbered agenda nodes, and connector lines work together as a navigational signpost between major presentation chapters.

## SVG primitives needed
- 1× `<rect>` for the white slide background
- 2× `<path>` for soft decorative background sweeps that add keynote-style depth without clutter
- 1× `<rect>` for the left title banner
- 1× `<text>` for the section title inside the banner
- 1× `<rect>` for the framed icon container
- 8–12× `<path>` for the custom thematic icon, such as a funnel, product card, spark, or idea-screening motif
- 6× `<circle>` for agenda number badges
- 6× `<text>` for agenda numbers inside the badges
- 6× `<text>` for agenda item labels
- 1× `<line>` for the vertical agenda spine
- 6× `<line>` for horizontal connector ticks from the spine to each agenda item
- 2× `<linearGradient>` for premium banner/card surface fills
- 1× `<filter id="softShadow">` applied to the left icon card and active agenda node
- 1× `<filter id="pinkGlow">` applied to the active agenda badge or accent icon detail

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bannerGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#F17B81"/>
      <stop offset="100%" stop-color="#D94F5E"/>
    </linearGradient>

    <linearGradient id="cardGrad" x1="0" y1="110" x2="0" y2="520" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="100%" stop-color="#F7F9FC"/>
    </linearGradient>

    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feOffset dx="0" dy="10" result="off"/>
      <feGaussianBlur in="off" stdDeviation="12" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="pinkGlow" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="6" result="glow"/>
      <feMerge>
        <feMergeNode in="glow"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <!-- Background -->
  <rect x="0" y="0" width="1280" height="720" fill="#FFFFFF"/>
  <path d="M-80,600 C170,520 210,690 470,610 C690,545 780,640 1040,555 C1160,515 1260,520 1360,570 L1360,760 L-80,760 Z"
        fill="#FCEDEE" opacity="0.75"/>
  <path d="M920,-80 C1110,10 1125,165 1310,210 L1310,-80 Z"
        fill="#EEF3FA" opacity="0.95"/>

  <!-- Left chapter card -->
  <g transform="translate(86 112)">
    <rect x="0" y="0" width="455" height="72" rx="4" fill="url(#bannerGrad)"/>
    <text x="26" y="46" width="405"
          font-family="Segoe UI, Microsoft YaHei, sans-serif"
          font-size="28" font-weight="700" fill="#FFFFFF">
      Product Idea Screening
    </text>

    <rect x="0" y="72" width="455" height="400" rx="0"
          fill="url(#cardGrad)" stroke="#1E3250" stroke-width="2.2"
          filter="url(#softShadow)"/>

    <!-- Small label -->
    <text x="34" y="118" width="190"
          font-family="Segoe UI, Microsoft YaHei, sans-serif"
          font-size="13" font-weight="700" letter-spacing="2"
          fill="#E76C72">
      SECTION 02
    </text>

    <!-- Thematic icon: idea funnel + screened product card -->
    <g transform="translate(94 128)">
      <circle cx="132" cy="118" r="118" fill="#F4F7FB" stroke="#D9E1EC" stroke-width="2"/>

      <!-- funnel body -->
      <path d="M50,55 L214,55 C220,55 223,62 219,67 L155,151 L155,205 C155,211 151,216 145,219 L115,234 C107,238 98,232 98,223 L98,151 L45,67 C41,62 44,55 50,55 Z"
            fill="#1E3250"/>
      <path d="M70,72 L194,72 L141,141 L141,195 L113,209 L113,141 Z"
            fill="#FFFFFF" opacity="0.16"/>

      <!-- screened dots inside funnel -->
      <circle cx="92" cy="93" r="8" fill="#E76C72" filter="url(#pinkGlow)"/>
      <circle cx="132" cy="93" r="8" fill="#FFFFFF" opacity="0.9"/>
      <circle cx="172" cy="93" r="8" fill="#FFFFFF" opacity="0.9"/>

      <!-- product card emerging -->
      <path d="M165,166 L239,146 C249,143 259,149 262,159 L280,226 C283,237 277,247 266,250 L192,270 C182,273 172,267 169,257 L151,190 C148,180 154,169 165,166 Z"
            fill="#FFFFFF" stroke="#1E3250" stroke-width="5"/>
      <path d="M178,185 L239,169" stroke="#E76C72" stroke-width="6" stroke-linecap="round" fill="none"/>
      <path d="M184,211 L247,194" stroke="#1E3250" stroke-width="5" stroke-linecap="round" fill="none" opacity="0.75"/>
      <path d="M191,236 L232,225" stroke="#1E3250" stroke-width="5" stroke-linecap="round" fill="none" opacity="0.35"/>

      <!-- spark -->
      <path d="M236,55 L246,78 L269,88 L246,98 L236,121 L226,98 L203,88 L226,78 Z"
            fill="#E76C72"/>
      <path d="M40,198 C55,186 72,186 86,199" stroke="#E76C72" stroke-width="6" stroke-linecap="round" fill="none"/>
      <circle cx="41" cy="198" r="5" fill="#E76C72"/>
      <circle cx="86" cy="199" r="5" fill="#E76C72"/>
    </g>

    <text x="46" y="426" width="360"
          font-family="Segoe UI, Microsoft YaHei, sans-serif"
          font-size="15" fill="#5F7088">
      Prioritize high-potential concepts before investing in detailed development.
    </text>
  </g>

  <!-- Right mini-agenda -->
  <g transform="translate(650 128)">
    <text x="0" y="0" width="420"
          font-family="Segoe UI, Microsoft YaHei, sans-serif"
          font-size="16" font-weight="700" letter-spacing="2"
          fill="#E76C72">
      CHAPTER AGENDA
    </text>

    <text x="0" y="44" width="440"
          font-family="Segoe UI, Microsoft YaHei, sans-serif"
          font-size="32" font-weight="700"
          fill="#1E3250">
      What we will cover
    </text>

    <line x1="28" y1="104" x2="28" y2="492" stroke="#C9D3E0" stroke-width="2"/>

    <!-- Item 01 active -->
    <line x1="28" y1="122" x2="86" y2="122" stroke="#E76C72" stroke-width="2.5"/>
    <circle cx="28" cy="122" r="24" fill="#E76C72" filter="url(#softShadow)"/>
    <text x="13" y="130" width="30"
          font-family="Segoe UI, Microsoft YaHei, sans-serif"
          font-size="13" font-weight="700" fill="#FFFFFF">01</text>
    <text x="104" y="130" width="430"
          font-family="Segoe UI, Microsoft YaHei, sans-serif"
          font-size="22" font-weight="700" fill="#1E3250">
      New Product Introduction
    </text>

    <!-- Item 02 -->
    <line x1="28" y1="196" x2="86" y2="196" stroke="#C9D3E0" stroke-width="2"/>
    <circle cx="28" cy="196" r="21" fill="#1E3250"/>
    <text x="13" y="204" width="30"
          font-family="Segoe UI, Microsoft YaHei, sans-serif"
          font-size="13" font-weight="700" fill="#FFFFFF">02</text>
    <text x="104" y="204" width="430"
          font-family="Segoe UI, Microsoft YaHei, sans-serif"
          font-size="21" fill="#1E3250">
      New Product Detailed Overview
    </text>

    <!-- Item 03 -->
    <line x1="28" y1="270" x2="86" y2="270" stroke="#C9D3E0" stroke-width="2"/>
    <circle cx="28" cy="270" r="21" fill="#1E3250"/>
    <text x="13" y="278" width="30"
          font-family="Segoe UI, Microsoft YaHei, sans-serif"
          font-size="13" font-weight="700" fill="#FFFFFF">03</text>
    <text x="104" y="278" width="430"
          font-family="Segoe UI, Microsoft YaHei, sans-serif"
          font-size="21" fill="#1E3250">
      Understanding Customer Needs
    </text>

    <!-- Item 04 -->
    <line x1="28" y1="344" x2="86" y2="344" stroke="#C9D3E0" stroke-width="2"/>
    <circle cx="28" cy="344" r="21" fill="#1E3250"/>
    <text x="13" y="352" width="30"
          font-family="Segoe UI, Microsoft YaHei, sans-serif"
          font-size="13" font-weight="700" fill="#FFFFFF">04</text>
    <text x="104" y="352" width="430"
          font-family="Segoe UI, Microsoft YaHei, sans-serif"
          font-size="21" fill="#1E3250">
      External Sources of Ideas
    </text>

    <!-- Item 05 -->
    <line x1="28" y1="418" x2="86" y2="418" stroke="#C9D3E0" stroke-width="2"/>
    <circle cx="28" cy="418" r="21" fill="#1E3250"/>
    <text x="13" y="426" width="30"
          font-family="Segoe UI, Microsoft YaHei, sans-serif"
          font-size="13" font-weight="700" fill="#FFFFFF">05</text>
    <text x="104" y="426" width="430"
          font-family="Segoe UI, Microsoft YaHei, sans-serif"
          font-size="21" fill="#1E3250">
      Internal Sources of Ideas
    </text>

    <!-- Item 06 -->
    <line x1="28" y1="492" x2="86" y2="492" stroke="#C9D3E0" stroke-width="2"/>
    <circle cx="28" cy="492" r="21" fill="#1E3250"/>
    <text x="13" y="500" width="30"
          font-family="Segoe UI, Microsoft YaHei, sans-serif"
          font-size="13" font-weight="700" fill="#FFFFFF">06</text>
    <text x="104" y="500" width="430"
          font-family="Segoe UI, Microsoft YaHei, sans-serif"
          font-size="21" fill="#1E3250">
      Product Roadmap
    </text>
  </g>

  <!-- Footer progress cue -->
  <line x1="88" y1="662" x2="1192" y2="662" stroke="#E7ECF3" stroke-width="2"/>
  <circle cx="315" cy="662" r="6" fill="#E76C72"/>
  <circle cx="475" cy="662" r="4" fill="#CBD5E1"/>
  <circle cx="635" cy="662" r="4" fill="#CBD5E1"/>
  <circle cx="795" cy="662" r="4" fill="#CBD5E1"/>
  <text x="88" y="692" width="240"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="12" font-weight="700" letter-spacing="1.5"
        fill="#8A98AA">
    STRATEGY PRESENTATION
  </text>
</svg>
```

## Avoid in this skill
- ❌ Do not use `<marker>` arrowheads for the agenda connector; simple `<line>` ticks are safer and translate cleanly.
- ❌ Do not rely on auto-sized text. Every `<text>` element needs an explicit `width` so agenda labels do not reflow unpredictably in PowerPoint.
- ❌ Do not use `<clipPath>` on normal shapes for the icon container; clipping is only reliable for `<image>` elements.
- ❌ Do not overfill the right side with long agenda sentences. This technique works best with short chapter labels.
- ❌ Do not use `<use>` for repeated agenda nodes; duplicate the editable circle/text/line elements directly.

## Composition notes
- Keep the left chapter card to roughly 38–42% of the canvas width; it should feel like a strong visual anchor, not a sidebar.
- The agenda column should start around x=630–680, leaving a clear gutter between the icon card and the list.
- Use one accent color for the title banner and the current agenda item; keep all other nodes dark blue to preserve hierarchy.
- Let the background remain mostly white. Decorative sweeps should be pale and peripheral so the divider feels premium, calm, and easy to scan.