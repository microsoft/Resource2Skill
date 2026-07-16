# SVG Recipe — Automated Hierarchical Organization Chart (SmartArt Emulation)

## Visual mechanism
A nested hierarchy is rendered as a top-down tree where each parent node is centered above the midpoint of its children, with clean orthogonal connector paths showing reporting relationships. Depth-based color gradients, soft shadows, and a contained “SmartArt canvas” make the automated layout feel polished and executive-ready.

## SVG primitives needed
- 1× `<rect>` for the full-slide gradient background
- 1× `<rect>` for the rounded chart canvas / frosted panel
- 10× `<rect>` for rounded organization nodes, filled by hierarchy-level gradients
- 10× `<circle>` for small role/status dots inside nodes
- 9× `<path>` for orthogonal elbow connectors between parents and children
- 2× decorative `<path>` blobs for premium background atmosphere
- 14× `<text>` elements for title, subtitle, legend labels, and node labels; every `<text>` has explicit `width`
- 5× `<linearGradient>` definitions for background, panel, and node levels
- 1× `<radialGradient>` for the background glow
- 1× `<filter id="nodeShadow">` using `feOffset + feGaussianBlur + feMerge`, applied to node rectangles only
- 1× `<filter id="softGlow">` using `feGaussianBlur`, applied to decorative blob paths only

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#07162F"/>
      <stop offset="55%" stop-color="#0D2448"/>
      <stop offset="100%" stop-color="#122D5C"/>
    </linearGradient>

    <radialGradient id="blueGlow" cx="50%" cy="38%" r="65%">
      <stop offset="0%" stop-color="#3E7BFF" stop-opacity="0.34"/>
      <stop offset="62%" stop-color="#1A4FB9" stop-opacity="0.10"/>
      <stop offset="100%" stop-color="#07162F" stop-opacity="0"/>
    </radialGradient>

    <linearGradient id="panelGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.13"/>
      <stop offset="100%" stop-color="#FFFFFF" stop-opacity="0.04"/>
    </linearGradient>

    <linearGradient id="level0" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#233F78"/>
      <stop offset="100%" stop-color="#102653"/>
    </linearGradient>
    <linearGradient id="level1" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#3E73C6"/>
      <stop offset="100%" stop-color="#244F9B"/>
    </linearGradient>
    <linearGradient id="level2" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#5D8FE3"/>
      <stop offset="100%" stop-color="#3A69BC"/>
    </linearGradient>

    <filter id="nodeShadow" x="-20%" y="-25%" width="140%" height="160%">
      <feOffset dx="0" dy="6" in="SourceAlpha" result="off"/>
      <feGaussianBlur in="off" stdDeviation="7" result="blur"/>
      <feColorMatrix in="blur" type="matrix"
        values="0 0 0 0 0  0 0 0 0 0.04  0 0 0 0 0.12  0 0 0 .28 0" result="shadow"/>
      <feMerge>
        <feMergeNode in="shadow"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="softGlow" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="18"/>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>
  <rect x="0" y="0" width="1280" height="720" fill="url(#blueGlow)"/>

  <path d="M1000,64 C1105,18 1210,62 1244,148 C1284,248 1170,294 1082,244 C1000,198 922,110 1000,64 Z"
        fill="#4D8BFF" opacity="0.16" filter="url(#softGlow)"/>
  <path d="M42,600 C130,540 248,560 286,646 C316,714 202,748 106,716 C32,692 -34,650 42,600 Z"
        fill="#7BD3FF" opacity="0.12" filter="url(#softGlow)"/>

  <text x="72" y="62" width="620" font-family="Segoe UI, Microsoft YaHei" font-size="32" font-weight="700" fill="#FFFFFF">
    Corporate Organization Structure
  </text>
  <text x="74" y="94" width="650" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#BFD0F2">
    SmartArt-style hierarchy generated from nested source data — parents centered above their child subtrees.
  </text>

  <rect x="62" y="116" width="1156" height="552" rx="28" fill="url(#panelGrad)" stroke="#FFFFFF" stroke-opacity="0.18"/>

  <text x="86" y="150" width="300" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#DCE7FF">
    DEPTH-BASED COLOR LOGIC
  </text>
  <circle cx="92" cy="174" r="5" fill="#233F78"/>
  <text x="106" y="179" width="92" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#BFD0F2">Executive</text>
  <circle cx="206" cy="174" r="5" fill="#3E73C6"/>
  <text x="220" y="179" width="92" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#BFD0F2">VP Level</text>
  <circle cx="318" cy="174" r="5" fill="#5D8FE3"/>
  <text x="332" y="179" width="110" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#BFD0F2">Managers</text>

  <!-- CEO -->
  <rect x="546" y="132" width="170" height="58" rx="16" fill="url(#level0)" stroke="#9AB6FF" stroke-opacity="0.55" filter="url(#nodeShadow)"/>
  <circle cx="570" cy="161" r="7" fill="#9AB6FF"/>
  <text x="631" y="157" width="130" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#FFFFFF">
    CEO
  </text>
  <text x="631" y="174" width="130" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="10" fill="#D8E4FF">
    Executive Office
  </text>

  <!-- Root connectors -->
  <path d="M631 190 V228 H214 V270" fill="none" stroke="#9AA5B8" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M631 190 V228 H631 V270" fill="none" stroke="#9AA5B8" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M631 190 V228 H1049 V270" fill="none" stroke="#9AA5B8" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>

  <!-- VP row -->
  <rect x="129" y="270" width="170" height="58" rx="15" fill="url(#level1)" stroke="#B7CBFF" stroke-opacity="0.45" filter="url(#nodeShadow)"/>
  <circle cx="153" cy="299" r="6" fill="#CFE0FF"/>
  <text x="214" y="298" width="130" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#FFFFFF">VP Operations</text>
  <text x="214" y="314" width="130" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="9.5" fill="#E4ECFF">Supply Chain</text>

  <rect x="546" y="270" width="170" height="58" rx="15" fill="url(#level1)" stroke="#B7CBFF" stroke-opacity="0.45" filter="url(#nodeShadow)"/>
  <circle cx="570" cy="299" r="6" fill="#CFE0FF"/>
  <text x="631" y="298" width="130" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#FFFFFF">VP Marketing</text>
  <text x="631" y="314" width="130" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="9.5" fill="#E4ECFF">Growth Engine</text>

  <rect x="964" y="270" width="170" height="58" rx="15" fill="url(#level1)" stroke="#B7CBFF" stroke-opacity="0.45" filter="url(#nodeShadow)"/>
  <circle cx="988" cy="299" r="6" fill="#CFE0FF"/>
  <text x="1049" y="298" width="130" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#FFFFFF">VP Engineering</text>
  <text x="1049" y="314" width="130" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="9.5" fill="#E4ECFF">Product Platform</text>

  <!-- VP connectors -->
  <path d="M214 328 V370 H130 V430" fill="none" stroke="#9AA5B8" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M214 328 V370 H297 V430" fill="none" stroke="#9AA5B8" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M631 328 V370 H464 V430" fill="none" stroke="#9AA5B8" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M631 328 V370 H631 V430" fill="none" stroke="#9AA5B8" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M631 328 V370 H798 V430" fill="none" stroke="#9AA5B8" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M1049 328 V370 H965 V430" fill="none" stroke="#9AA5B8" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M1049 328 V370 H1132 V430" fill="none" stroke="#9AA5B8" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>

  <!-- Manager row -->
  <rect x="55" y="430" width="150" height="54" rx="14" fill="url(#level2)" stroke="#D2DFFF" stroke-opacity="0.35" filter="url(#nodeShadow)"/>
  <text x="130" y="456" width="128" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="11" font-weight="700" fill="#FFFFFF">Director of</text>
  <text x="130" y="471" width="128" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="11" font-weight="700" fill="#FFFFFF">Logistics</text>

  <rect x="222" y="430" width="150" height="54" rx="14" fill="url(#level2)" stroke="#D2DFFF" stroke-opacity="0.35" filter="url(#nodeShadow)"/>
  <text x="297" y="456" width="128" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="11" font-weight="700" fill="#FFFFFF">Director of</text>
  <text x="297" y="471" width="128" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="11" font-weight="700" fill="#FFFFFF">Production</text>

  <rect x="389" y="430" width="150" height="54" rx="14" fill="url(#level2)" stroke="#D2DFFF" stroke-opacity="0.35" filter="url(#nodeShadow)"/>
  <text x="464" y="462" width="128" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="11" font-weight="700" fill="#FFFFFF">SEO Manager</text>

  <rect x="556" y="430" width="150" height="54" rx="14" fill="url(#level2)" stroke="#D2DFFF" stroke-opacity="0.35" filter="url(#nodeShadow)"/>
  <text x="631" y="462" width="128" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="11" font-weight="700" fill="#FFFFFF">Email Manager</text>

  <rect x="723" y="430" width="150" height="54" rx="14" fill="url(#level2)" stroke="#D2DFFF" stroke-opacity="0.35" filter="url(#nodeShadow)"/>
  <text x="798" y="462" width="128" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="11" font-weight="700" fill="#FFFFFF">Webmaster</text>

  <rect x="890" y="430" width="150" height="54" rx="14" fill="url(#level2)" stroke="#D2DFFF" stroke-opacity="0.35" filter="url(#nodeShadow)"/>
  <text x="965" y="462" width="128" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="11" font-weight="700" fill="#FFFFFF">Frontend Lead</text>

  <rect x="1057" y="430" width="150" height="54" rx="14" fill="url(#level2)" stroke="#D2DFFF" stroke-opacity="0.35" filter="url(#nodeShadow)"/>
  <text x="1132" y="462" width="128" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="11" font-weight="700" fill="#FFFFFF">Backend Lead</text>

  <text x="84" y="626" width="520" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#9FB2D8">
    Layout rule: compute leaf positions first, then center each parent over the average x-position of its children.
  </text>
</svg>
```

## Avoid in this skill
- ❌ Do not use `<use>` or `<symbol>` to duplicate node components; repeated org-chart boxes should be explicit editable shapes.
- ❌ Do not use `marker-end` for connector arrows; organization charts usually need plain orthogonal connectors, and path markers will not translate reliably.
- ❌ Do not apply filters to `<line>` connectors; if shadow is needed, keep it on node rectangles only.
- ❌ Do not use `<foreignObject>` for wrapped HTML text; use native `<text>` / `<tspan>` and give every `<text>` an explicit `width`.
- ❌ Do not rely on PowerPoint SmartArt objects; emulate the SmartArt look with native editable SVG shapes.

## Composition notes
- Keep the top 15–20% of the slide for title, subtitle, and legend; place the chart inside a large rounded panel below.
- Use generous vertical spacing between levels so elbow connectors have room to breathe and do not collide with node shadows.
- Parent nodes should sit exactly above the center of their child group, not merely above the first child; this is the key SmartArt-emulation behavior.
- Use darker, more saturated fills for senior levels and lighter fills for deeper levels so hierarchy is readable before the audience reads the labels.