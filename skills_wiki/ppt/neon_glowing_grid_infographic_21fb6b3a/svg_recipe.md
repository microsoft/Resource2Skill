# SVG Recipe — Neon Glowing Grid Infographic

## Visual mechanism
A dark-mode hero metric pairs oversized neon typography with a 10×10 dot matrix, where each dot represents 1% and active dots glow in lime. Soft blurred atmospheric orbs and a subtle device-like panel create depth, making the percentage feel like a premium tech keynote visual rather than a flat chart.

## SVG primitives needed
- 1× `<rect>` for the near-black full-slide background
- 3× `<ellipse>` for blurred neon atmospheric glow orbs behind the content
- 3× `<rect>` for a tilted dark display panel, inner screen, and small accent underline
- 100× `<circle>` for the 10×10 percentage matrix dots
- 75× active `<circle>` dots filled neon lime with glow filter
- 25× inactive `<circle>` dots filled muted green with neon outline
- 3× `<text>` elements for the subtitle, main number, and outlined percent sign
- 1× `<linearGradient>` for the display panel surface
- 2× `<radialGradient>` definitions for background glow color fields
- 3× `<filter>` definitions for soft background blur, dot glow, and panel shadow

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="screenGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#172500"/>
      <stop offset="55%" stop-color="#101A05"/>
      <stop offset="100%" stop-color="#071004"/>
    </linearGradient>

    <radialGradient id="limeOrb" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#BCFF01" stop-opacity="0.8"/>
      <stop offset="55%" stop-color="#78B500" stop-opacity="0.28"/>
      <stop offset="100%" stop-color="#BCFF01" stop-opacity="0"/>
    </radialGradient>

    <radialGradient id="cyanOrb" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#00FFD1" stop-opacity="0.6"/>
      <stop offset="70%" stop-color="#00FFD1" stop-opacity="0.15"/>
      <stop offset="100%" stop-color="#00FFD1" stop-opacity="0"/>
    </radialGradient>

    <filter id="softBlur" x="-80%" y="-80%" width="260%" height="260%">
      <feGaussianBlur stdDeviation="34"/>
    </filter>

    <filter id="panelShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="20"/>
      <feGaussianBlur stdDeviation="22"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="dotGlow" x="-80%" y="-80%" width="260%" height="260%">
      <feGaussianBlur stdDeviation="4" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="textGlow" x="-15%" y="-20%" width="140%" height="150%">
      <feGaussianBlur stdDeviation="5" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#111B07"/>

  <ellipse cx="135" cy="600" rx="310" ry="160" fill="url(#limeOrb)" filter="url(#softBlur)" opacity="0.9"/>
  <ellipse cx="44" cy="55" rx="190" ry="310" fill="url(#cyanOrb)" filter="url(#softBlur)" opacity="0.55"/>
  <ellipse cx="1210" cy="115" rx="230" ry="310" fill="#FF9B00" filter="url(#softBlur)" opacity="0.18"/>

  <g transform="rotate(-5 640 360)">
    <rect x="54" y="72" width="870" height="548" rx="30" fill="#030807" filter="url(#panelShadow)"/>
    <rect x="78" y="98" width="822" height="495" rx="18" fill="url(#screenGrad)" stroke="#34433A" stroke-width="3"/>
    <rect x="83" y="103" width="812" height="485" rx="14" fill="none" stroke="#6F8A92" stroke-width="1" opacity="0.35"/>

    <text x="118" y="206" width="320" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="22" font-weight="800" letter-spacing="1.2" fill="#BCFF01">
      GROWTH RATE
    </text>
    <rect x="118" y="225" width="292" height="3" fill="#BCFF01" opacity="0.75"/>

    <text x="115" y="445" width="270" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="152" font-weight="900" fill="#BCFF01" filter="url(#textGlow)">
      75
    </text>
    <text x="360" y="405" width="145" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="132" font-weight="900" fill="#132000" stroke="#BCFF01" stroke-width="5" paint-order="stroke fill">
      %
    </text>

    <circle cx="514" cy="133" r="16" fill="#385000" stroke="#BCFF01" stroke-width="1.6" opacity="0.72"/><circle cx="550" cy="133" r="16" fill="#385000" stroke="#BCFF01" stroke-width="1.6" opacity="0.72"/><circle cx="586" cy="133" r="16" fill="#385000" stroke="#BCFF01" stroke-width="1.6" opacity="0.72"/><circle cx="622" cy="133" r="16" fill="#385000" stroke="#BCFF01" stroke-width="1.6" opacity="0.72"/><circle cx="658" cy="133" r="16" fill="#385000" stroke="#BCFF01" stroke-width="1.6" opacity="0.72"/><circle cx="694" cy="133" r="16" fill="#385000" stroke="#BCFF01" stroke-width="1.6" opacity="0.72"/><circle cx="730" cy="133" r="16" fill="#385000" stroke="#BCFF01" stroke-width="1.6" opacity="0.72"/><circle cx="766" cy="133" r="16" fill="#385000" stroke="#BCFF01" stroke-width="1.6" opacity="0.72"/><circle cx="802" cy="133" r="16" fill="#385000" stroke="#BCFF01" stroke-width="1.6" opacity="0.72"/><circle cx="838" cy="133" r="16" fill="#385000" stroke="#BCFF01" stroke-width="1.6" opacity="0.72"/>
    <circle cx="514" cy="169" r="16" fill="#385000" stroke="#BCFF01" stroke-width="1.6" opacity="0.72"/><circle cx="550" cy="169" r="16" fill="#385000" stroke="#BCFF01" stroke-width="1.6" opacity="0.72"/><circle cx="586" cy="169" r="16" fill="#385000" stroke="#BCFF01" stroke-width="1.6" opacity="0.72"/><circle cx="622" cy="169" r="16" fill="#385000" stroke="#BCFF01" stroke-width="1.6" opacity="0.72"/><circle cx="658" cy="169" r="16" fill="#385000" stroke="#BCFF01" stroke-width="1.6" opacity="0.72"/><circle cx="694" cy="169" r="16" fill="#385000" stroke="#BCFF01" stroke-width="1.6" opacity="0.72"/><circle cx="730" cy="169" r="16" fill="#385000" stroke="#BCFF01" stroke-width="1.6" opacity="0.72"/><circle cx="766" cy="169" r="16" fill="#385000" stroke="#BCFF01" stroke-width="1.6" opacity="0.72"/><circle cx="802" cy="169" r="16" fill="#385000" stroke="#BCFF01" stroke-width="1.6" opacity="0.72"/><circle cx="838" cy="169" r="16" fill="#385000" stroke="#BCFF01" stroke-width="1.6" opacity="0.72"/>
    <circle cx="514" cy="205" r="16" fill="#BCFF01" filter="url(#dotGlow)"/><circle cx="550" cy="205" r="16" fill="#BCFF01" filter="url(#dotGlow)"/><circle cx="586" cy="205" r="16" fill="#BCFF01" filter="url(#dotGlow)"/><circle cx="622" cy="205" r="16" fill="#BCFF01" filter="url(#dotGlow)"/><circle cx="658" cy="205" r="16" fill="#BCFF01" filter="url(#dotGlow)"/><circle cx="694" cy="205" r="16" fill="#385000" stroke="#BCFF01" stroke-width="1.6" opacity="0.72"/><circle cx="730" cy="205" r="16" fill="#385000" stroke="#BCFF01" stroke-width="1.6" opacity="0.72"/><circle cx="766" cy="205" r="16" fill="#385000" stroke="#BCFF01" stroke-width="1.6" opacity="0.72"/><circle cx="802" cy="205" r="16" fill="#385000" stroke="#BCFF01" stroke-width="1.6" opacity="0.72"/><circle cx="838" cy="205" r="16" fill="#385000" stroke="#BCFF01" stroke-width="1.6" opacity="0.72"/>
    <circle cx="514" cy="241" r="16" fill="#BCFF01" filter="url(#dotGlow)"/><circle cx="550" cy="241" r="16" fill="#BCFF01" filter="url(#dotGlow)"/><circle cx="586" cy="241" r="16" fill="#BCFF01" filter="url(#dotGlow)"/><circle cx="622" cy="241" r="16" fill="#BCFF01" filter="url(#dotGlow)"/><circle cx="658" cy="241" r="16" fill="#BCFF01" filter="url(#dotGlow)"/><circle cx="694" cy="241" r="16" fill="#BCFF01" filter="url(#dotGlow)"/><circle cx="730" cy="241" r="16" fill="#BCFF01" filter="url(#dotGlow)"/><circle cx="766" cy="241" r="16" fill="#BCFF01" filter="url(#dotGlow)"/><circle cx="802" cy="241" r="16" fill="#BCFF01" filter="url(#dotGlow)"/><circle cx="838" cy="241" r="16" fill="#BCFF01" filter="url(#dotGlow)"/>
    <circle cx="514" cy="277" r="16" fill="#BCFF01" filter="url(#dotGlow)"/><circle cx="550" cy="277" r="16" fill="#BCFF01" filter="url(#dotGlow)"/><circle cx="586" cy="277" r="16" fill="#BCFF01" filter="url(#dotGlow)"/><circle cx="622" cy="277" r="16" fill="#BCFF01" filter="url(#dotGlow)"/><circle cx="658" cy="277" r="16" fill="#BCFF01" filter="url(#dotGlow)"/><circle cx="694" cy="277" r="16" fill="#BCFF01" filter="url(#dotGlow)"/><circle cx="730" cy="277" r="16" fill="#BCFF01" filter="url(#dotGlow)"/><circle cx="766" cy="277" r="16" fill="#BCFF01" filter="url(#dotGlow)"/><circle cx="802" cy="277" r="16" fill="#BCFF01" filter="url(#dotGlow)"/><circle cx="838" cy="277" r="16" fill="#BCFF01" filter="url(#dotGlow)"/>
    <circle cx="514" cy="313" r="16" fill="#BCFF01" filter="url(#dotGlow)"/><circle cx="550" cy="313" r="16" fill="#BCFF01" filter="url(#dotGlow)"/><circle cx="586" cy="313" r="16" fill="#BCFF01" filter="url(#dotGlow)"/><circle cx="622" cy="313" r="16" fill="#BCFF01" filter="url(#dotGlow)"/><circle cx="658" cy="313" r="16" fill="#BCFF01" filter="url(#dotGlow)"/><circle cx="694" cy="313" r="16" fill="#BCFF01" filter="url(#dotGlow)"/><circle cx="730" cy="313" r="16" fill="#BCFF01" filter="url(#dotGlow)"/><circle cx="766" cy="313" r="16" fill="#BCFF01" filter="url(#dotGlow)"/><circle cx="802" cy="313" r="16" fill="#BCFF01" filter="url(#dotGlow)"/><circle cx="838" cy="313" r="16" fill="#BCFF01" filter="url(#dotGlow)"/>
    <circle cx="514" cy="349" r="16" fill="#BCFF01" filter="url(#dotGlow)"/><circle cx="550" cy="349" r="16" fill="#BCFF01" filter="url(#dotGlow)"/><circle cx="586" cy="349" r="16" fill="#BCFF01" filter="url(#dotGlow)"/><circle cx="622" cy="349" r="16" fill="#BCFF01" filter="url(#dotGlow)"/><circle cx="658" cy="349" r="16" fill="#BCFF01" filter="url(#dotGlow)"/><circle cx="694" cy="349" r="16" fill="#BCFF01" filter="url(#dotGlow)"/><circle cx="730" cy="349" r="16" fill="#BCFF01" filter="url(#dotGlow)"/><circle cx="766" cy="349" r="16" fill="#BCFF01" filter="url(#dotGlow)"/><circle cx="802" cy="349" r="16" fill="#BCFF01" filter="url(#dotGlow)"/><circle cx="838" cy="349" r="16" fill="#BCFF01" filter="url(#dotGlow)"/>
    <circle cx="514" cy="385" r="16" fill="#BCFF01" filter="url(#dotGlow)"/><circle cx="550" cy="385" r="16" fill="#BCFF01" filter="url(#dotGlow)"/><circle cx="586" cy="385" r="16" fill="#BCFF01" filter="url(#dotGlow)"/><circle cx="622" cy="385" r="16" fill="#BCFF01" filter="url(#dotGlow)"/><circle cx="658" cy="385" r="16" fill="#BCFF01" filter="url(#dotGlow)"/><circle cx="694" cy="385" r="16" fill="#BCFF01" filter="url(#dotGlow)"/><circle cx="730" cy="385" r="16" fill="#BCFF01" filter="url(#dotGlow)"/><circle cx="766" cy="385" r="16" fill="#BCFF01" filter="url(#dotGlow)"/><circle cx="802" cy="385" r="16" fill="#BCFF01" filter="url(#dotGlow)"/><circle cx="838" cy="385" r="16" fill="#BCFF01" filter="url(#dotGlow)"/>
    <circle cx="514" cy="421" r="16" fill="#BCFF01" filter="url(#dotGlow)"/><circle cx="550" cy="421" r="16" fill="#BCFF01" filter="url(#dotGlow)"/><circle cx="586" cy="421" r="16" fill="#BCFF01" filter="url(#dotGlow)"/><circle cx="622" cy="421" r="16" fill="#BCFF01" filter="url(#dotGlow)"/><circle cx="658" cy="421" r="16" fill="#BCFF01" filter="url(#dotGlow)"/><circle cx="694" cy="421" r="16" fill="#BCFF01" filter="url(#dotGlow)"/><circle cx="730" cy="421" r="16" fill="#BCFF01" filter="url(#dotGlow)"/><circle cx="766" cy="421" r="16" fill="#BCFF01" filter="url(#dotGlow)"/><circle cx="802" cy="421" r="16" fill="#BCFF01" filter="url(#dotGlow)"/><circle cx="838" cy="421" r="16" fill="#BCFF01" filter="url(#dotGlow)"/>
    <circle cx="514" cy="457" r="16" fill="#BCFF01" filter="url(#dotGlow)"/><circle cx="550" cy="457" r="16" fill="#BCFF01" filter="url(#dotGlow)"/><circle cx="586" cy="457" r="16" fill="#BCFF01" filter="url(#dotGlow)"/><circle cx="622" cy="457" r="16" fill="#BCFF01" filter="url(#dotGlow)"/><circle cx="658" cy="457" r="16" fill="#BCFF01" filter="url(#dotGlow)"/><circle cx="694" cy="457" r="16" fill="#BCFF01" filter="url(#dotGlow)"/><circle cx="730" cy="457" r="16" fill="#BCFF01" filter="url(#dotGlow)"/><circle cx="766" cy="457" r="16" fill="#BCFF01" filter="url(#dotGlow)"/><circle cx="802" cy="457" r="16" fill="#BCFF01" filter="url(#dotGlow)"/><circle cx="838" cy="457" r="16" fill="#BCFF01" filter="url(#dotGlow)"/>
  </g>

  <rect x="950" y="92" width="144" height="144" rx="20" fill="#E92820" opacity="0.96" filter="url(#panelShadow)"/>
  <text x="994" y="197" width="80" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="105" font-weight="900" fill="#FFFFFF" stroke="#C7C7C7" stroke-width="2">
    P
  </text>
</svg>
```

## Avoid in this skill
- ❌ Using `<use>` or `<symbol>` to repeat the 100 dots; duplicate native `<circle>` elements instead so PowerPoint keeps every dot editable.
- ❌ Applying `filter` to a parent `<g>` for the dot matrix; put glow filters directly on the active circles.
- ❌ Relying on `<pattern>` fills for the grid; pattern fills will not translate into editable PowerPoint shapes.
- ❌ Using `skewX`, `skewY`, or `matrix()` to fake perspective on the display panel; use a simple `rotate()` transform and layered rounded rectangles.
- ❌ Putting the underline in a `<line>` with a filter; use a thin `<rect>` accent bar instead.

## Composition notes
- Keep the hero number on the left 35–40% of the panel, with the 10×10 dot grid occupying the right 45–50%.
- Use a near-black olive background so the lime `#BCFF01` feels electric without becoming visually harsh.
- Place blurred glow orbs behind, not over, the data elements; they should create atmosphere while preserving chart readability.
- For different percentages, fill dots from bottom-left upward, leaving the remaining dots as dark muted circles with neon outlines.