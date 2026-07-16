# SVG Recipe — Professional Title Slide with Translucent Graphic

## Visual mechanism
Layer a semi-transparent professional portrait over a corporate-blue field, then add a tonal “data bar” texture behind it so the slide feels both human and analytical. Keep the typography crisp and high-contrast, using white for authority and one bright accent color for brand energy.

## SVG primitives needed
- 1× `<rect>` for the solid corporate-blue canvas
- 1× `<linearGradient>` for a subtle left-to-right blue depth wash
- 1× `<radialGradient>` for a soft atmospheric glow behind the portrait
- 14× `<rect>` for translucent vertical bar-chart texture
- 5× `<line>` for faint analytical grid ticks
- 2× `<path>` for abstract translucent data ribbons / curved graphic overlays
- 1× `<clipPath>` with `<path>` to crop the portrait into a right-side organic panel
- 1× `<image>` for the translucent professional portrait
- 1× `<filter id="softShadow">` for understated text/card depth
- 1× `<filter id="textGlow">` for slight title glow
- 6× `<text>` elements for logo, title, accent word, section label, main message, and metadata

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="blueDepth" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#1f5f98"/>
      <stop offset="58%" stop-color="#2569a3"/>
      <stop offset="100%" stop-color="#174d7b"/>
    </linearGradient>

    <radialGradient id="portraitGlow" cx="70%" cy="48%" r="44%">
      <stop offset="0%" stop-color="#79b6df" stop-opacity="0.34"/>
      <stop offset="62%" stop-color="#3e8bc1" stop-opacity="0.16"/>
      <stop offset="100%" stop-color="#2569a3" stop-opacity="0"/>
    </radialGradient>

    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="8"/>
      <feGaussianBlur stdDeviation="10"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="textGlow" x="-10%" y="-20%" width="120%" height="150%">
      <feGaussianBlur stdDeviation="2"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <clipPath id="portraitPanel">
      <path d="M760,0 C840,90 820,190 890,270 C970,365 955,475 895,570 C860,628 855,680 895,720 L1280,720 L1280,0 Z"/>
    </clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#blueDepth)"/>
  <ellipse cx="930" cy="345" rx="430" ry="350" fill="url(#portraitGlow)"/>

  <rect x="80" y="488" width="54" height="232" fill="#5994c3" opacity="0.20"/>
  <rect x="160" y="420" width="54" height="300" fill="#5994c3" opacity="0.17"/>
  <rect x="240" y="520" width="54" height="200" fill="#5994c3" opacity="0.18"/>
  <rect x="320" y="366" width="54" height="354" fill="#5994c3" opacity="0.16"/>
  <rect x="400" y="460" width="54" height="260" fill="#5994c3" opacity="0.18"/>
  <rect x="480" y="305" width="54" height="415" fill="#5994c3" opacity="0.15"/>
  <rect x="560" y="392" width="54" height="328" fill="#5994c3" opacity="0.16"/>
  <rect x="640" y="252" width="54" height="468" fill="#5994c3" opacity="0.14"/>
  <rect x="720" y="330" width="54" height="390" fill="#5994c3" opacity="0.13"/>
  <rect x="800" y="210" width="54" height="510" fill="#5994c3" opacity="0.12"/>
  <rect x="880" y="285" width="54" height="435" fill="#5994c3" opacity="0.12"/>
  <rect x="960" y="185" width="54" height="535" fill="#5994c3" opacity="0.11"/>
  <rect x="1040" y="250" width="54" height="470" fill="#5994c3" opacity="0.10"/>
  <rect x="1120" y="135" width="54" height="585" fill="#5994c3" opacity="0.10"/>

  <line x1="70" y1="560" x2="1210" y2="560" stroke="#8fc3e6" stroke-width="1" opacity="0.18" stroke-dasharray="8 12"/>
  <line x1="70" y1="440" x2="1210" y2="440" stroke="#8fc3e6" stroke-width="1" opacity="0.13" stroke-dasharray="8 12"/>
  <line x1="70" y1="320" x2="1210" y2="320" stroke="#8fc3e6" stroke-width="1" opacity="0.10" stroke-dasharray="8 12"/>
  <line x1="70" y1="200" x2="1210" y2="200" stroke="#8fc3e6" stroke-width="1" opacity="0.08" stroke-dasharray="8 12"/>
  <line x1="70" y1="80" x2="1210" y2="80" stroke="#8fc3e6" stroke-width="1" opacity="0.06" stroke-dasharray="8 12"/>

  <path d="M-40,580 C130,500 240,540 390,450 C530,365 640,390 780,300 C905,220 1010,225 1325,120"
        fill="none" stroke="#bada55" stroke-width="5" opacity="0.36" stroke-linecap="round"/>
  <path d="M-80,645 C160,560 300,612 480,510 C640,420 760,470 930,370 C1060,295 1160,310 1360,235 L1360,720 L-80,720 Z"
        fill="#0d3f68" opacity="0.16"/>

  <image href="https://images.example.com/transparent-professional-speaker-portrait-facing-left.png"
         x="735" y="40" width="520" height="690" opacity="0.34" clip-path="url(#portraitPanel)"/>

  <rect x="72" y="68" width="162" height="42" rx="21" fill="#174d7b" opacity="0.35" filter="url(#softShadow)"/>
  <text x="98" y="96" width="130" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="19" font-weight="700" letter-spacing="2.5" fill="#ffffff" opacity="0.92">INSIGHT LAB</text>

  <text x="82" y="222" width="500" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="92" font-weight="800" letter-spacing="4" fill="#ffffff" filter="url(#textGlow)">MOXIE</text>
  <text x="405" y="232" width="180" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="48" font-weight="600" font-style="italic" fill="#bada55">talk</text>

  <text x="84" y="342" width="560" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="28" font-weight="600" letter-spacing="3" fill="#d9ecf8" opacity="0.88">EXECUTIVE COMMUNICATION SERIES</text>

  <rect x="82" y="566" width="96" height="6" rx="3" fill="#bada55"/>
  <text x="82" y="628" width="250" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="54" font-weight="800" fill="#ffffff">TIP 1:</text>
  <text x="280" y="628" width="620" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="54" font-weight="800" fill="#ffffff" letter-spacing="1">PREPARE</text>

  <text x="935" y="82" width="260" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="18" font-weight="600" fill="#ffffff" opacity="0.78" text-anchor="end">Q3 LEADERSHIP BRIEFING</text>
</svg>
```

## Avoid in this skill
- ❌ Using `<mask>` to fade the portrait edge; masks on shapes/images are not reliable for this pipeline.
- ❌ Applying `clip-path` to rectangles or paths for decorative overlays; clipping should be reserved for the `<image>` only.
- ❌ Using `mix-blend-mode`, CSS filters, or color-matrix filters to tint the portrait; instead, use a transparent PNG portrait with low opacity over the blue background.
- ❌ Making the data bars too opaque or colorful; they should read as background texture, not as the main chart.
- ❌ Placing white text directly over the brightest part of the portrait; keep the headline mostly on the clean left-side blue field.

## Composition notes
- Keep the left 55–60% of the slide reserved for text hierarchy: small brand mark, large title, subtitle, and bottom message.
- Let the portrait occupy the right third to right half of the canvas, with opacity around 0.25–0.40 so it adds presence without competing with the title.
- Use the translucent bars across the full width, but reduce their opacity as they approach the portrait so the human figure remains legible.
- The color rhythm should be restrained: corporate blue base, white typography, pale blue texture, and one vivid green accent.