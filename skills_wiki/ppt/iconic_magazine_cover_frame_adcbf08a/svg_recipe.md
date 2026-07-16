# SVG Recipe — Iconic Magazine Cover Frame

## Visual mechanism
A full-bleed cinematic photograph is disciplined by a thick inset yellow rectangular frame, creating an instantly recognizable editorial “cover” structure. Large legacy serif masthead typography sits at the top while article headlines are anchored at the bottom over subtle black gradients for readability.

## SVG primitives needed
- 1× `<image>` for the full-bleed 16:9 hero photograph.
- 2× `<rect>` with vertical `<linearGradient>` fills for top and bottom readability fades.
- 1× `<rect>` with `<radialGradient>` fill for a subtle edge vignette over the photo.
- 1× `<rect>` with no fill and a thick yellow stroke for the iconic inset cover frame.
- 1× `<filter id="softTextShadow">` applied to headline text for legibility over complex imagery.
- 1× `<filter id="frameGlow">` applied to the yellow frame for a premium printed-light edge.
- Multiple `<text>` elements with explicit `width` attributes for metadata, masthead, cover line, headline, subtitle, and footer details.
- Several short `<line>` elements for small editorial divider rules and issue-detail accents.

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="topFade" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#000000" stop-opacity="0.72"/>
      <stop offset="58%" stop-color="#000000" stop-opacity="0.30"/>
      <stop offset="100%" stop-color="#000000" stop-opacity="0"/>
    </linearGradient>

    <linearGradient id="bottomFade" x1="0" y1="1" x2="0" y2="0">
      <stop offset="0%" stop-color="#000000" stop-opacity="0.82"/>
      <stop offset="58%" stop-color="#000000" stop-opacity="0.38"/>
      <stop offset="100%" stop-color="#000000" stop-opacity="0"/>
    </linearGradient>

    <radialGradient id="edgeVignette" cx="50%" cy="46%" r="72%">
      <stop offset="54%" stop-color="#000000" stop-opacity="0"/>
      <stop offset="86%" stop-color="#000000" stop-opacity="0.22"/>
      <stop offset="100%" stop-color="#000000" stop-opacity="0.48"/>
    </radialGradient>

    <filter id="softTextShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="4" result="off"/>
      <feGaussianBlur in="off" stdDeviation="4" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="frameGlow" x="-10%" y="-10%" width="120%" height="120%">
      <feGaussianBlur stdDeviation="2.2" result="glow"/>
      <feMerge>
        <feMergeNode in="glow"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <image
    href="https://images.unsplash.com/photo-1540573133985-87b6da6d54a9?q=80&amp;w=1920&amp;auto=format&amp;fit=crop"
    x="0" y="0" width="1280" height="720"
    preserveAspectRatio="xMidYMid slice"/>

  <rect x="0" y="0" width="1280" height="250" fill="url(#topFade)"/>
  <rect x="0" y="390" width="1280" height="330" fill="url(#bottomFade)"/>
  <rect x="0" y="0" width="1280" height="720" fill="url(#edgeVignette)"/>

  <rect
    x="54" y="52" width="1172" height="616"
    fill="none"
    stroke="#FFCC00"
    stroke-width="14"
    filter="url(#frameGlow)"/>

  <text
    x="640" y="84" width="720"
    text-anchor="middle"
    font-family="Segoe UI, Microsoft YaHei, sans-serif"
    font-size="13"
    font-weight="700"
    letter-spacing="4"
    fill="#FFFFFF"
    opacity="0.92">
    ISSUE 07  ·  WILDLIFE FRONTIERS  ·  2026
  </text>

  <line x1="440" y1="105" x2="532" y2="105" stroke="#FFCC00" stroke-width="3"/>
  <line x1="748" y1="105" x2="840" y2="105" stroke="#FFCC00" stroke-width="3"/>

  <text
    x="640" y="166" width="980"
    text-anchor="middle"
    font-family="Times New Roman, Georgia, serif"
    font-size="76"
    font-weight="700"
    letter-spacing="3"
    fill="#FFFFFF"
    filter="url(#softTextShadow)">
    FIELD ATLAS
  </text>

  <text
    x="640" y="204" width="660"
    text-anchor="middle"
    font-family="Segoe UI, Microsoft YaHei, sans-serif"
    font-size="15"
    font-weight="600"
    letter-spacing="5"
    fill="#FFCC00">
    REPORTS FROM THE EDGE OF THE KNOWN WORLD
  </text>

  <text
    x="92" y="108" width="160"
    font-family="Segoe UI, Microsoft YaHei, sans-serif"
    font-size="12"
    font-weight="700"
    letter-spacing="2"
    fill="#FFFFFF"
    opacity="0.9">
    VOL. 114
  </text>

  <text
    x="1098" y="108" width="120"
    text-anchor="end"
    font-family="Segoe UI, Microsoft YaHei, sans-serif"
    font-size="12"
    font-weight="700"
    letter-spacing="2"
    fill="#FFFFFF"
    opacity="0.9">
    $12.00
  </text>

  <text
    x="640" y="508" width="900"
    text-anchor="middle"
    font-family="Times New Roman, Georgia, serif"
    font-size="54"
    font-weight="700"
    fill="#FFFFFF"
    filter="url(#softTextShadow)">
    INTO THE UNKNOWN
  </text>

  <text
    x="640" y="552" width="760"
    text-anchor="middle"
    font-family="Times New Roman, Georgia, serif"
    font-size="26"
    font-style="italic"
    fill="#FFFFFF"
    opacity="0.96"
    filter="url(#softTextShadow)">
    Discovering the hidden habitats that still resist the map
  </text>

  <line x1="510" y1="583" x2="770" y2="583" stroke="#FFCC00" stroke-width="4"/>

  <text
    x="640" y="620" width="760"
    text-anchor="middle"
    font-family="Segoe UI, Microsoft YaHei, sans-serif"
    font-size="16"
    font-weight="700"
    letter-spacing="2"
    fill="#FFCC00">
    CLIMATE  ·  MIGRATION  ·  SURVIVAL  ·  THE NEW EXPEDITION ERA
  </text>

  <text
    x="96" y="642" width="280"
    font-family="Segoe UI, Microsoft YaHei, sans-serif"
    font-size="12"
    font-weight="600"
    fill="#FFFFFF"
    opacity="0.82">
    SPECIAL DOCUMENTARY EDITION
  </text>

  <text
    x="1184" y="642" width="280"
    text-anchor="end"
    font-family="Segoe UI, Microsoft YaHei, sans-serif"
    font-size="12"
    font-weight="600"
    fill="#FFFFFF"
    opacity="0.82">
    PHOTOGRAPHY BY A. RIVERA
  </text>
</svg>
```

## Avoid in this skill
- ❌ Do not create the yellow frame as a filled rectangle with a “hole”; masks and non-image clipping will not translate reliably. Use a stroked `<rect>` instead.
- ❌ Do not rely on photo brightness for text legibility; always add top and bottom gradient overlays behind the typography.
- ❌ Do not use actual magazine trademarks unless the client owns the rights; create a fictional masthead with the same editorial hierarchy.
- ❌ Do not place text directly on the frame stroke; keep all typography inside the inset border with comfortable padding.
- ❌ Do not use `<textPath>`, `<pattern>`, or SVG masks for decorative magazine effects.

## Composition notes
- Keep the frame inset around 4% of slide width, with a stroke thick enough to read as an iconic editorial device rather than a thin outline.
- The photograph should have one strong central subject; avoid busy images where the masthead or headline competes with faces or bright sky.
- Reserve the top 25–30% for masthead and issue metadata, and the bottom 28–35% for the cover headline stack.
- Use yellow sparingly: frame, divider, and one supporting line of text. White remains the dominant typography color.