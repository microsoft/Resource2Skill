# SVG Recipe — Dynamic Content Callouts & CTA Buttons

## Visual mechanism
Create tactile “pressable” UI widgets by stacking rounded rectangles: a soft drop shadow, a darker lower rim, a saturated gradient face, and a narrow highlight band. Pair the raised CTA with a beveled content callout panel so the slide clearly distinguishes “read this” from “act now.”

## SVG primitives needed
- 1× `<rect>` for the full-slide background
- 2× decorative `<path>` blobs for premium ambient depth behind the widgets
- 8× `<rect>` for CTA shadow, rim, face, highlight, inset gloss, and small button details
- 5× `<rect>` for the testimonial/callout panel shadow, rim, face, highlight, and bottom bevel
- 2× `<circle>` for quote-badge and CTA icon accents
- 1× `<path>` for a simple arrow/chevron inside the CTA button
- 6× `<text>` elements with explicit `width=` for headline, CTA label, helper copy, quote mark, body copy, and attribution
- 6× `<linearGradient>` definitions for background, button face, button rim, WordArt-style text, callout face, and glossy highlights
- 3× `<filter>` definitions using blur/offset/merge for editable shadows and glows applied to rectangles, paths, and text

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#fffdf7"/>
      <stop offset="55%" stop-color="#fff7e6"/>
      <stop offset="100%" stop-color="#f5ecff"/>
    </linearGradient>

    <linearGradient id="accentBlob" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#ffcf33" stop-opacity="0.55"/>
      <stop offset="100%" stop-color="#9b2bff" stop-opacity="0.22"/>
    </linearGradient>

    <linearGradient id="buttonRim" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#fff9a8"/>
      <stop offset="48%" stop-color="#f6c900"/>
      <stop offset="100%" stop-color="#a46d00"/>
    </linearGradient>

    <linearGradient id="buttonFace" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#fff879"/>
      <stop offset="38%" stop-color="#ffe600"/>
      <stop offset="100%" stop-color="#ffc400"/>
    </linearGradient>

    <linearGradient id="buttonTextGrad" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#8c140f"/>
      <stop offset="52%" stop-color="#c01838"/>
      <stop offset="100%" stop-color="#4c0099"/>
    </linearGradient>

    <linearGradient id="panelFace" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#ff3b2f"/>
      <stop offset="48%" stop-color="#c1121f"/>
      <stop offset="100%" stop-color="#7a0013"/>
    </linearGradient>

    <linearGradient id="gloss" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#ffffff" stop-opacity="0.62"/>
      <stop offset="100%" stop-color="#ffffff" stop-opacity="0"/>
    </linearGradient>

    <filter id="shadow" x="-20%" y="-25%" width="140%" height="160%">
      <feOffset dx="0" dy="14" in="SourceAlpha" result="off"/>
      <feGaussianBlur in="off" stdDeviation="14" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="tightShadow" x="-15%" y="-20%" width="130%" height="150%">
      <feOffset dx="0" dy="5" in="SourceAlpha" result="off"/>
      <feGaussianBlur in="off" stdDeviation="5" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="textGlow" x="-10%" y="-20%" width="120%" height="140%">
      <feGaussianBlur stdDeviation="2.2" result="glow"/>
      <feMerge>
        <feMergeNode in="glow"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>

  <path d="M918 28 C1066 -28 1244 54 1288 171 C1336 300 1196 392 1062 342 C939 296 783 277 780 173 C778 92 830 61 918 28 Z"
        fill="url(#accentBlob)" filter="url(#shadow)"/>
  <path d="M-42 558 C65 471 188 488 244 578 C302 670 214 756 78 740 C-65 724 -139 636 -42 558 Z"
        fill="#ffdf59" opacity="0.28" filter="url(#shadow)"/>

  <text x="92" y="76" width="760" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="700" fill="#241331">
    Turn attention into action
  </text>
  <text x="94" y="112" width="670" font-family="Segoe UI, Microsoft YaHei" font-size="17" fill="#6a5a72">
    Use raised callouts for proof, then anchor the close with a tactile CTA button.
  </text>

  <g transform="translate(92 162)">
    <rect x="0" y="18" width="488" height="310" rx="34" fill="#56000d" opacity="0.34" filter="url(#shadow)"/>
    <rect x="0" y="0" width="488" height="310" rx="34" fill="#70000f"/>
    <rect x="8" y="7" width="472" height="292" rx="28" fill="url(#panelFace)" stroke="#ffd1d1" stroke-opacity="0.34" stroke-width="2"/>
    <rect x="24" y="20" width="440" height="72" rx="22" fill="url(#gloss)" opacity="0.75"/>
    <rect x="26" y="268" width="436" height="18" rx="9" fill="#49000b" opacity="0.42"/>

    <circle cx="62" cy="72" r="31" fill="#ffffff" opacity="0.96" filter="url(#tightShadow)"/>
    <text x="49" y="84" width="40" font-family="Georgia, serif" font-size="46" font-weight="700" fill="#b00018">“</text>

    <text x="108" y="68" width="330" font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="700" fill="#ffffff">
      The final nudge matters.
    </text>
    <text x="50" y="128" width="390" font-family="Segoe UI, Microsoft YaHei" font-size="21" fill="#fff5f5">
      <tspan x="50" dy="0">A strong close does more than summarize.</tspan>
      <tspan x="50" dy="32">It isolates the next step, removes doubt,</tspan>
      <tspan x="50" dy="32">and makes the decision feel immediate.</tspan>
      <tspan x="50" dy="32">That is why the callout and button need</tspan>
      <tspan x="50" dy="32">their own visual gravity.</tspan>
    </text>
    <text x="50" y="274" width="380" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#ffd9d9">
      — Closing slide design principle
    </text>
  </g>

  <g transform="translate(614 304)">
    <rect x="14" y="30" width="566" height="144" rx="45" fill="#6e4a00" opacity="0.32" filter="url(#shadow)"/>
    <rect x="0" y="0" width="566" height="144" rx="45" fill="url(#buttonRim)" stroke="#595959" stroke-width="3"/>
    <rect x="9" y="8" width="548" height="118" rx="38" fill="url(#buttonFace)"/>
    <rect x="27" y="18" width="512" height="40" rx="20" fill="url(#gloss)" opacity="0.88"/>
    <rect x="34" y="112" width="498" height="13" rx="7" fill="#a66e00" opacity="0.42"/>

    <circle cx="76" cy="72" r="28" fill="#ffffff" opacity="0.76" filter="url(#tightShadow)"/>
    <path d="M68 57 L88 72 L68 87 Z" fill="#7b0b34"/>

    <text x="118" y="86" width="390" font-family="Segoe UI, Microsoft YaHei" font-size="41" font-weight="800"
          fill="url(#buttonTextGrad)" stroke="#ffffff" stroke-width="1.2" filter="url(#textGlow)">
      GET INSTANT ACCESS
    </text>
  </g>

  <g transform="translate(668 482)">
    <rect x="0" y="0" width="460" height="82" rx="24" fill="#ffffff" opacity="0.76" filter="url(#tightShadow)"/>
    <rect x="14" y="13" width="54" height="54" rx="17" fill="#efe3ff"/>
    <circle cx="41" cy="40" r="10" fill="#7b2cff"/>
    <text x="86" y="34" width="330" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="700" fill="#2f1b3d">
      Make the close unmistakable
    </text>
    <text x="86" y="58" width="330" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#6a5a72">
      One proof block, one action, one visual destination.
    </text>
  </g>
</svg>
```

## Avoid in this skill
- ❌ Relying on PowerPoint 3D bevel XML equivalents; simulate bevels with stacked SVG rectangles, gradients, highlights, and lower rims instead.
- ❌ Applying `filter` to `<line>` elements for shadows; use shadowed `<rect>`, `<path>`, `<circle>`, or `<text>` only.
- ❌ Using `clip-path` on callout shapes for gloss bands; translator only preserves clipping reliably on `<image>`, so use rounded rectangles as visible highlight layers.
- ❌ Building the CTA as one flat yellow rectangle; the tactile effect needs at least shadow, rim, face, highlight, and darker bottom edge.
- ❌ Omitting `width=` on text; every editable PowerPoint text object must include an explicit width.

## Composition notes
- Keep the proof/callout panel on the left or upper-left, then place the CTA lower-right to create a natural reading path toward action.
- Use saturated warm colors for the CTA and deeper thematic colors for the callout; the CTA should be the brightest object on the slide.
- Reserve generous negative space around the button so its shadow and bevel read as intentional, not crowded.
- For premium polish, repeat the same highlight language on both widgets, but make the CTA larger, brighter, and more centered in the closing area.