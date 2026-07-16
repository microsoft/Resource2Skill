# SVG Recipe — High-Contrast Minimalist Metric Reveal (Keynote Style)

## Visual mechanism
A cinematic dark gradient stage isolates one oversized metric and one ultra-minimal progress ring, making the data feel like a premium product reveal rather than a chart. The composition uses high contrast, generous negative space, and a single electric accent color to pull attention instantly to the key number.

## SVG primitives needed
- 1× `<rect>` for the full-slide dark gradient background
- 2× `<ellipse>` for soft atmospheric accent glows behind the chart and text
- 3× `<circle>` for the donut track, the active metric arc, and the subtle inner glass disc
- 1× `<path>` for a minimal accent underline / energy stroke near the headline
- 1× `<rect>` for a small contextual benchmark pill
- 5× `<text>` for the central metric, right-side headline, subtitle, micro-label, and benchmark text
- 1× `<linearGradient>` for the OLED-style background
- 2× `<radialGradient>` for cyan and violet ambient glows
- 1× `<filter id="cyanGlow">` applied to the active metric arc and small accent path
- 1× `<filter id="softBlur">` applied to atmospheric ellipses

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGradient" x1="0" y1="0" x2="0" y2="720">
      <stop offset="0%" stop-color="#1A1B22"/>
      <stop offset="52%" stop-color="#0D0E13"/>
      <stop offset="100%" stop-color="#000000"/>
    </linearGradient>

    <radialGradient id="cyanHalo" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#00BFFF" stop-opacity="0.55"/>
      <stop offset="42%" stop-color="#00BFFF" stop-opacity="0.18"/>
      <stop offset="100%" stop-color="#00BFFF" stop-opacity="0"/>
    </radialGradient>

    <radialGradient id="violetHalo" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#7B61FF" stop-opacity="0.35"/>
      <stop offset="55%" stop-color="#7B61FF" stop-opacity="0.10"/>
      <stop offset="100%" stop-color="#7B61FF" stop-opacity="0"/>
    </radialGradient>

    <filter id="softBlur" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="42"/>
    </filter>

    <filter id="cyanGlow" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="8" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGradient)"/>

  <ellipse cx="350" cy="360" rx="250" ry="250" fill="url(#cyanHalo)" filter="url(#softBlur)" opacity="0.85"/>
  <ellipse cx="1040" cy="165" rx="280" ry="190" fill="url(#violetHalo)" filter="url(#softBlur)" opacity="0.55"/>

  <circle cx="380" cy="360" r="172"
          fill="none"
          stroke="#30323A"
          stroke-width="28"
          opacity="0.95"/>

  <circle cx="380" cy="360" r="172"
          fill="none"
          stroke="#00BFFF"
          stroke-width="28"
          stroke-linecap="round"
          stroke-dasharray="1016 1081"
          transform="rotate(-90 380 360)"
          filter="url(#cyanGlow)"/>

  <circle cx="380" cy="360" r="125"
          fill="#FFFFFF"
          opacity="0.035"
          stroke="#FFFFFF"
          stroke-width="1.5"
          stroke-opacity="0.10"/>

  <text x="380" y="360"
        width="300"
        text-anchor="middle"
        dominant-baseline="central"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="96"
        font-weight="800"
        fill="#FFFFFF"
        letter-spacing="-5">94%</text>

  <text x="380" y="493"
        width="300"
        text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="17"
        font-weight="600"
        fill="#8D93A1"
        letter-spacing="2.5">WEEKLY REACH</text>

  <path d="M704 292 C760 272, 827 272, 884 292"
        fill="none"
        stroke="#00BFFF"
        stroke-width="5"
        stroke-linecap="round"
        opacity="0.9"
        filter="url(#cyanGlow)"/>

  <text x="700" y="252"
        width="470"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="52"
        font-weight="750"
        fill="#FFFFFF"
        letter-spacing="-1.5">
    <tspan x="700" dy="0">觀看 YouTube</tspan>
    <tspan x="700" dy="62">已成為每週習慣</tspan>
  </text>

  <text x="704" y="405"
        width="430"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="24"
        font-weight="400"
        fill="#B7BBC6"
        line-height="1.25">
    <tspan x="704" dy="0">18–44 歲的網路使用者</tspan>
    <tspan x="704" dy="34">每週至少觀看一次影片內容</tspan>
  </text>

  <rect x="704" y="504" width="304" height="46" rx="23"
        fill="#FFFFFF"
        opacity="0.075"
        stroke="#FFFFFF"
        stroke-opacity="0.14"
        stroke-width="1"/>

  <text x="728" y="534"
        width="260"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="16"
        font-weight="650"
        fill="#E9F8FF"
        letter-spacing="0.3">
    <tspan fill="#00BFFF">▲ +12 pts</tspan>
    <tspan fill="#AEB4C2"> vs. prior quarter</tspan>
  </text>

  <text x="704" y="620"
        width="430"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="13"
        font-weight="500"
        fill="#626977"
        letter-spacing="1.6">SOURCE: INTERNAL AUDIENCE STUDY · 2026</text>
</svg>
```

## Avoid in this skill
- ❌ Dense gridlines, axes, legends, and labels; they weaken the keynote-style “single takeaway” reveal
- ❌ Multicolor chart palettes; use one accent color plus dark neutral track colors
- ❌ Paragraph-length explanations; the slide should support the speaker, not replace them
- ❌ `<marker-end>` arrows or decorative callout arrows; they make the composition feel analytical instead of cinematic
- ❌ Applying blur filters to `<line>` elements; use filtered `<path>`, `<circle>`, or `<ellipse>` for glows instead

## Composition notes
- Keep the progress ring on the left third to create asymmetrical balance; center the main number inside the ring.
- Place the headline and context text on the right with generous line spacing and no more than two short lines per tier.
- Use the electric accent sparingly: active ring, small underline, and one benchmark highlight are enough.
- Preserve large dark negative space around the metric so the slide feels confident, premium, and uncluttered.