# SVG Recipe — Masked Handwriting Reveal

## Visual mechanism
A handwriting-style wordmark sits behind a same-color “stencil cover” that hides the unrevealed portion; in PowerPoint, animate the cover or the text with a left-to-right wipe to create the illusion that the letters are being written. Add a pen tip and soft wipe edge to make the reveal feel intentional, artisanal, and tactile.

## SVG primitives needed
- 1× `<rect>` for the warm full-slide background.
- 1× `<rect>` for a soft paper card surface behind the handwriting.
- 1× `<rect>` for the active stencil/reveal cover that matches the background/card color and hides the unrevealed text.
- 1× `<rect>` with gradient fill for the soft leading edge of the wipe.
- 2× `<text>` for the handwriting title and small supporting caption; all text includes explicit `width`.
- 5× `<path>` for loose ink underlines, paper-corner decoration, pencil/pen nib shape, and small hand-drawn accent marks.
- 3× `<line>` for pencil body details and small drafting marks.
- 2× `<circle>` for tiny ink dots / handmade texture.
- 2× `<linearGradient>` for paper warmth and wipe-edge transparency.
- 2× `<filter>` with blur/offset for paper shadow and subtle ink softness.

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="paperGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#F9D0A9"/>
      <stop offset="55%" stop-color="#F2B482"/>
      <stop offset="100%" stop-color="#EFA56F"/>
    </linearGradient>

    <linearGradient id="wipeEdge" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#F2B482" stop-opacity="0"/>
      <stop offset="42%" stop-color="#F2B482" stop-opacity="0.82"/>
      <stop offset="100%" stop-color="#F2B482" stop-opacity="1"/>
    </linearGradient>

    <filter id="paperShadow" x="-10%" y="-20%" width="120%" height="150%">
      <feOffset dx="0" dy="14"/>
      <feGaussianBlur stdDeviation="16"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="inkSoftness" x="-5%" y="-20%" width="110%" height="150%">
      <feGaussianBlur stdDeviation="0.45"/>
    </filter>
  </defs>

  <!-- background -->
  <rect x="0" y="0" width="1280" height="720" fill="#F2B482"/>

  <!-- premium paper field -->
  <rect x="120" y="112" width="1040" height="496" rx="34" fill="url(#paperGrad)" filter="url(#paperShadow)"/>

  <!-- subtle handmade texture and decorative edges -->
  <circle cx="195" cy="180" r="3.5" fill="#C06F48" opacity="0.22"/>
  <circle cx="1058" cy="533" r="4.5" fill="#9F5739" opacity="0.16"/>
  <path d="M154 151 C189 137, 228 142, 260 126" fill="none" stroke="#8D4E36" stroke-width="2" opacity="0.22" stroke-linecap="round"/>
  <path d="M1018 578 C1058 592, 1091 575, 1124 591" fill="none" stroke="#8D4E36" stroke-width="2" opacity="0.18" stroke-linecap="round"/>
  <line x1="178" y1="544" x2="274" y2="544" stroke="#6D3C2D" stroke-width="2" opacity="0.16" stroke-dasharray="8 9"/>
  <line x1="1004" y1="181" x2="1104" y2="181" stroke="#6D3C2D" stroke-width="2" opacity="0.14" stroke-dasharray="6 8"/>

  <!-- content layer: the handwriting that will be revealed -->
  <text x="640" y="366"
        width="920"
        text-anchor="middle"
        font-family="'Patrick Hand','Segoe UI','Microsoft YaHei',cursive"
        font-size="112"
        font-weight="400"
        fill="#15120F"
        filter="url(#inkSoftness)">
    Smooth Handwriting
  </text>

  <!-- organic ink underline already revealed on the left side -->
  <path d="M310 410 C384 430, 493 423, 566 418 C613 415, 658 418, 699 428"
        fill="none"
        stroke="#15120F"
        stroke-width="5"
        stroke-linecap="round"
        opacity="0.92"/>

  <!-- top stencil/reveal cover: animate this rectangle off to the right, or apply a left-to-right wipe -->
  <rect x="694" y="230" width="426" height="232" fill="#F2B482"/>

  <!-- soft leading edge so the reveal does not feel mechanically sharp -->
  <rect x="644" y="230" width="78" height="232" fill="url(#wipeEdge)"/>

  <!-- pen tip placed at current reveal boundary -->
  <g transform="translate(694 401) rotate(-14)">
    <path d="M0 0 L86 -24 L106 -7 L20 19 Z"
          fill="#2A2521"
          stroke="#15120F"
          stroke-width="2"/>
    <path d="M86 -24 L126 -34 L106 -7 Z"
          fill="#F7D36B"
          stroke="#15120F"
          stroke-width="2"/>
    <path d="M126 -34 L148 -42 L137 -19 Z"
          fill="#FCE6A0"
          stroke="#15120F"
          stroke-width="2"/>
    <line x1="24" y1="11" x2="90" y2="-8" stroke="#F6EFE8" stroke-width="3" opacity="0.55"/>
  </g>

  <!-- small live-ink mark at the boundary -->
  <path d="M669 407 C682 398, 694 402, 705 410"
        fill="none"
        stroke="#15120F"
        stroke-width="4"
        stroke-linecap="round"/>

  <!-- supporting caption -->
  <text x="640" y="505"
        width="680"
        text-anchor="middle"
        font-family="'Segoe UI','Microsoft YaHei',sans-serif"
        font-size="22"
        letter-spacing="1.4"
        fill="#5E3428"
        opacity="0.72">
    MASKED WIPE REVEAL · HAND-LETTERED TITLE MOMENT
  </text>

  <!-- tiny accent strokes to reinforce the handwritten theme -->
  <path d="M362 258 C373 244, 389 240, 401 248" fill="none" stroke="#15120F" stroke-width="3" opacity="0.28" stroke-linecap="round"/>
  <path d="M908 463 C924 475, 944 475, 958 461" fill="none" stroke="#15120F" stroke-width="3" opacity="0.22" stroke-linecap="round"/>
</svg>
```

## Avoid in this skill
- ❌ Do not use SVG `<mask>` on text or shapes; PPT-Master will not translate it reliably.
- ❌ Do not use `<animate>` or `<animateTransform>` for the reveal; create the visual state in SVG, then apply PowerPoint wipe animation after import.
- ❌ Do not rely on `<textPath>` to make the lettering follow a stroke; it will be dropped.
- ❌ Do not put `clip-path` on `<text>` or `<rect>`; clipping is only safe for `<image>` crops.
- ❌ Do not use `marker-end` for pen or arrow details; draw pen tips and arrows manually with paths/lines.

## Composition notes
- Keep the handwriting large and central; this effect works best when the title occupies 55–75% of the slide width.
- The stencil/reveal cover must exactly match the surface color behind it, otherwise the hidden portion will look like a block instead of a clean mask.
- Use a warm monochrome palette with black ink for a scrapbook/artisanal tone; for blueprint themes, switch the background to navy and the ink to white or pale cyan.
- Add only a few tactile details — pen nib, underline, tiny ink marks — so the reveal remains the visual focus.