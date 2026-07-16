# SVG Recipe — Split-Panel Feature Layout (Staging for Simultaneous Animations)

## Visual mechanism
A high-contrast split stage pairs oversized headline typography on a clean white angled panel with an isolated subject on a colored/photo side. The layout deliberately separates the copy group and subject group so they can be animated simultaneously in PowerPoint without visual collision.

## SVG primitives needed
- 1× `<rect>` for the full white slide background
- 2× `<path>` for the angled split-panel geometry: right color/photo stage and left white foreground plane
- 1× `<image>` for the right-side subject/photo, clipped to the right panel
- 1× `<clipPath>` with `<path>` for the angled right-side image crop
- 5× `<text>` for the stacked headline and small staging labels
- 1× `<circle>` for the lower-left app/icon badge
- 4× `<rect>` for the PowerPoint-style icon card and layered tile shadow
- 2× `<circle>` / `<path>` shapes for the pie-chart motif inside the icon
- 2× `<filter>` definitions: soft panel shadow and icon drop shadow
- 2× `<linearGradient>` definitions for the right panel tint and icon color depth

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="rightBlue" x1="680" y1="0" x2="1280" y2="720" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#c7d8f4"/>
      <stop offset="0.52" stop-color="#9fb8dc"/>
      <stop offset="1" stop-color="#6f88b2"/>
    </linearGradient>

    <linearGradient id="pptOrange" x1="70" y1="500" x2="230" y2="650" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#ff8b6f"/>
      <stop offset="1" stop-color="#d74328"/>
    </linearGradient>

    <filter id="panelShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feOffset dx="10" dy="0"/>
      <feGaussianBlur stdDeviation="18"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="iconShadow" x="-40%" y="-40%" width="180%" height="180%">
      <feOffset dx="0" dy="12"/>
      <feGaussianBlur stdDeviation="16"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <clipPath id="rightStageClip">
      <path d="M770 0 L1280 0 L1280 720 L610 720 Z"/>
    </clipPath>
  </defs>

  <!-- Background -->
  <rect x="0" y="0" width="1280" height="720" fill="#ffffff"/>

  <!-- Right image/color stage: keep as its own group for a simultaneous subject animation -->
  <g id="subject-stage">
    <path d="M770 0 L1280 0 L1280 720 L610 720 Z" fill="url(#rightBlue)"/>
    <image
      href="https://images.example.com/transparent-product-cutout-on-soft-blue-background.png"
      x="610" y="0" width="720" height="720"
      preserveAspectRatio="xMidYMid slice"
      clip-path="url(#rightStageClip)"/>
    <path d="M790 0 L1280 0 L1280 720 L635 720 Z" fill="#7fa1d0" opacity="0.18"/>
  </g>

  <!-- Left copy panel: angled edge gives the split more energy than a vertical rectangle -->
  <path
    d="M0 0 L785 0 L625 720 L0 720 Z"
    fill="#ffffff"
    filter="url(#panelShadow)"/>

  <!-- Copy group: animate this independently from the subject-stage group -->
  <g id="copy-stage">
    <text x="30" y="103" width="690"
      font-family="Segoe UI, Microsoft YaHei, sans-serif"
      font-size="92" font-weight="800" fill="#000000">Make Two</text>

    <text x="28" y="204" width="735"
      font-family="Segoe UI, Microsoft YaHei, sans-serif"
      font-size="92" font-weight="800" fill="#000000">Animations At</text>

    <text x="27" y="305" width="735"
      font-family="Segoe UI, Microsoft YaHei, sans-serif"
      font-size="92" font-weight="800" fill="#000000">The Same Time</text>

    <text x="34" y="372" width="520"
      font-family="Segoe UI, Microsoft YaHei, sans-serif"
      font-size="22" font-weight="600" fill="#7a7a7a" letter-spacing="1.5">
      COPY GROUP + SUBJECT GROUP
    </text>

    <text x="34" y="405" width="500"
      font-family="Segoe UI, Microsoft YaHei, sans-serif"
      font-size="19" fill="#999999">
      built as separate animation stages
    </text>
  </g>

  <!-- Decorative lower-left PowerPoint-style badge -->
  <g id="icon-badge" filter="url(#iconShadow)">
    <circle cx="145" cy="580" r="107" fill="#ffffff"/>
    <circle cx="160" cy="580" r="74" fill="url(#pptOrange)"/>
    <path d="M160 506 A74 74 0 0 1 234 580 L160 580 Z" fill="#ff876d"/>
    <path d="M160 580 L234 580 A74 74 0 0 1 87 580 Z" fill="#d9492f"/>
    <rect x="62" y="540" width="91" height="82" rx="5" fill="#a53225" opacity="0.28"/>
    <rect x="56" y="536" width="88" height="84" rx="5" fill="#c53a26"/>
    <rect x="62" y="542" width="76" height="72" rx="4" fill="#db472d"/>
    <text x="78" y="604" width="58"
      font-family="Segoe UI, Microsoft YaHei, sans-serif"
      font-size="70" font-weight="800" fill="#ffffff">P</text>
  </g>

  <!-- Subtle staging guide accents; can be hidden before export if undesired -->
  <path d="M690 70 L646 265" stroke="#000000" stroke-width="2" opacity="0.06" fill="none"/>
  <path d="M655 420 L610 620" stroke="#000000" stroke-width="2" opacity="0.06" fill="none"/>
</svg>
```

## Avoid in this skill
- ❌ Do not use actual SVG animation tags; stage the groups visually, then add animations in PowerPoint.
- ❌ Do not use `clip-path` on the left white panel shape; use a direct `<path>` instead so it remains editable.
- ❌ Do not put a filter on a `<line>` for motion guides; use faint `<path>` strokes or omit guides.
- ❌ Do not merge headline text and subject image into one bitmap, or the two animation stages become impossible to edit independently.
- ❌ Do not use a rectangular photo crop if the design calls for a dynamic split; the angled edge is the key premium layout cue.

## Composition notes
- Keep the left copy panel around 55–60% of the canvas, with the angled edge cutting into the right side for motion and depth.
- Treat the headline, icon badge, and right subject as three separate animation-ready groups.
- Use very large, heavy typography with tight stacking; this layout works best when the copy feels poster-like.
- The right side should have fewer details and more atmospheric color, allowing the isolated subject to read cleanly against the split.