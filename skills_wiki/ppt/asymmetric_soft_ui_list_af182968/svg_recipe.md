# SVG Recipe — Asymmetric Soft-UI List

## Visual mechanism
A large layered circular title medallion anchors the left side, while a vertically stacked set of rounded agenda cards floats on the right. Soft shadows, offset accent layers, and pill-shaped white surfaces create a tactile “modern app UI” feeling without losing executive-slide clarity.

## SVG primitives needed
- 1× `<rect>` for the full-slide blue background
- 2× decorative `<circle>` elements for subtle background glow accents
- 2× large `<circle>` elements for the asymmetric left title medallion: yellow rear disk and white front disk
- 4× yellow `<rect rx>` elements for offset accent backplates behind agenda items
- 4× white `<rect rx>` elements for foreground agenda item cards
- 4× small `<circle>` elements for numbered/lettered item badges
- 4× small `<path>` elements for minimalist icon marks inside the badges
- 1× decorative `<path>` curve behind the title area for extra premium depth
- Multiple `<text>` elements with explicit `width` for title, item numbers, item headings, and microcopy
- 2× `<linearGradient>` fills for background and white cards
- 2× `<radialGradient>` fills for the yellow medallion and badges
- 2× `<filter>` effects: one broad soft shadow for floating cards/circles, one subtle glow for the decorative background circles

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgBlue" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#345d9d"/>
      <stop offset="55%" stop-color="#2f5496"/>
      <stop offset="100%" stop-color="#243f78"/>
    </linearGradient>

    <linearGradient id="cardWhite" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#ffffff"/>
      <stop offset="100%" stop-color="#f2f5fb"/>
    </linearGradient>

    <radialGradient id="accentGold" cx="35%" cy="28%" r="70%">
      <stop offset="0%" stop-color="#ffd85a"/>
      <stop offset="68%" stop-color="#ffc000"/>
      <stop offset="100%" stop-color="#e2a500"/>
    </radialGradient>

    <radialGradient id="softGlow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#ffffff" stop-opacity="0.24"/>
      <stop offset="100%" stop-color="#ffffff" stop-opacity="0"/>
    </radialGradient>

    <filter id="softShadow" x="-25%" y="-25%" width="150%" height="150%">
      <feOffset dx="7" dy="10" in="SourceAlpha" result="offset"/>
      <feGaussianBlur stdDeviation="10" in="offset" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="ambientGlow" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="22"/>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgBlue)"/>

  <circle cx="1070" cy="120" r="170" fill="url(#softGlow)" filter="url(#ambientGlow)"/>
  <circle cx="110" cy="645" r="150" fill="url(#softGlow)" filter="url(#ambientGlow)"/>

  <path d="M42 430 C150 360, 184 228, 303 180 C407 138, 513 161, 588 96"
        fill="none" stroke="#ffffff" stroke-opacity="0.12" stroke-width="18" stroke-linecap="round"/>

  <circle cx="245" cy="360" r="180" fill="url(#accentGold)" filter="url(#softShadow)"/>
  <circle cx="280" cy="350" r="170" fill="url(#cardWhite)" filter="url(#softShadow)"/>

  <text x="280" y="304" width="250" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="31" font-weight="800"
        letter-spacing="2.5" fill="#303846">
    <tspan x="280" dy="0">TABLE OF</tspan>
    <tspan x="280" dy="42">CONTENTS</tspan>
  </text>
  <text x="280" y="398" width="210" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" font-weight="600"
        letter-spacing="1.4" fill="#748093">STRATEGY REVIEW</text>

  <rect x="540" y="112" width="610" height="94" rx="47" fill="url(#accentGold)" filter="url(#softShadow)"/>
  <rect x="514" y="96" width="610" height="94" rx="47" fill="url(#cardWhite)" filter="url(#softShadow)"/>
  <circle cx="574" cy="143" r="36" fill="url(#accentGold)"/>
  <path d="M562 143 L571 152 L589 132" fill="none" stroke="#2f5496" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>
  <text x="635" y="134" width="360" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="25" font-weight="750" fill="#303846">Market Context</text>
  <text x="636" y="163" width="390" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="14" font-weight="500" fill="#7b8492">Signals, shifts, and customer demand patterns</text>
  <text x="1055" y="152" width="42" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="18" font-weight="800" fill="#9aa3b2">01</text>

  <rect x="590" y="246" width="610" height="94" rx="47" fill="url(#accentGold)" filter="url(#softShadow)"/>
  <rect x="564" y="230" width="610" height="94" rx="47" fill="url(#cardWhite)" filter="url(#softShadow)"/>
  <circle cx="624" cy="277" r="36" fill="url(#accentGold)"/>
  <path d="M610 278 C617 264, 633 264, 640 278 C633 292, 617 292, 610 278 Z" fill="none" stroke="#2f5496" stroke-width="6" stroke-linejoin="round"/>
  <circle cx="625" cy="278" r="5" fill="#2f5496"/>
  <text x="685" y="268" width="360" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="25" font-weight="750" fill="#303846">Strategic Choices</text>
  <text x="686" y="297" width="400" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="14" font-weight="500" fill="#7b8492">Where we will play and how we will win</text>
  <text x="1105" y="286" width="42" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="18" font-weight="800" fill="#9aa3b2">02</text>

  <rect x="540" y="380" width="610" height="94" rx="47" fill="url(#accentGold)" filter="url(#softShadow)"/>
  <rect x="514" y="364" width="610" height="94" rx="47" fill="url(#cardWhite)" filter="url(#softShadow)"/>
  <circle cx="574" cy="411" r="36" fill="url(#accentGold)"/>
  <path d="M559 423 L559 401 L574 392 L589 401 L589 423 Z" fill="none" stroke="#2f5496" stroke-width="6" stroke-linejoin="round"/>
  <path d="M574 392 L574 423" fill="none" stroke="#2f5496" stroke-width="5" stroke-linecap="round"/>
  <text x="635" y="402" width="360" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="25" font-weight="750" fill="#303846">Operating Model</text>
  <text x="636" y="431" width="405" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="14" font-weight="500" fill="#7b8492">Capabilities, governance, and execution cadence</text>
  <text x="1055" y="420" width="42" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="18" font-weight="800" fill="#9aa3b2">03</text>

  <rect x="590" y="514" width="610" height="94" rx="47" fill="url(#accentGold)" filter="url(#softShadow)"/>
  <rect x="564" y="498" width="610" height="94" rx="47" fill="url(#cardWhite)" filter="url(#softShadow)"/>
  <circle cx="624" cy="545" r="36" fill="url(#accentGold)"/>
  <path d="M610 557 L638 557 M614 548 L624 536 L634 548" fill="none" stroke="#2f5496" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/>
  <text x="685" y="536" width="380" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="25" font-weight="750" fill="#303846">Investment Roadmap</text>
  <text x="686" y="565" width="405" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="14" font-weight="500" fill="#7b8492">Prioritized initiatives, owners, and milestones</text>
  <text x="1105" y="554" width="42" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="18" font-weight="800" fill="#9aa3b2">04</text>
</svg>
```

## Avoid in this skill
- ❌ Perfectly centered two-column symmetry; the design depends on the left title anchor and staggered right-side cards.
- ❌ Hard black shadows or thin outline-only cards; use broad, low-opacity shadows and filled surfaces to preserve the soft-UI effect.
- ❌ Applying `filter` to `<line>` elements; if connectors are added, keep them unfiltered or use `<path>` curves instead.
- ❌ Using `<mask>`, `<foreignObject>`, `<textPath>`, or `<pattern>` fills; these will not translate reliably into editable PowerPoint shapes.
- ❌ Forgetting explicit `width` on `<text>` elements; PowerPoint rendering will otherwise be unpredictable.

## Composition notes
- Keep the title medallion around 35–40% of slide width, vertically centered, with the yellow disk offset slightly left/down behind the white disk.
- The agenda cards should occupy the right 55% of the canvas, with alternating x-offsets to reinforce asymmetry.
- Use generous vertical gaps between cards; the soft shadows need breathing room to read as depth rather than clutter.
- Maintain a simple color rhythm: blue background, yellow accents, white foreground cards, and dark gray text.