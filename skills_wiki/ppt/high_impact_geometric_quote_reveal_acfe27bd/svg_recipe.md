# SVG Recipe — High-Impact Geometric Quote Reveal

## Visual mechanism
A dark, premium stage pairs an oversized monochrome portrait clipped into a bold geometric accent shape with a large, high-contrast quote block. The accent color is repeated in selected quote keywords and small graphic shards, making the portrait container and message feel like one unified reveal.

## SVG primitives needed
- 2× `<rect>` for the full-bleed dark background and subtle left text-panel grounding
- 1× `<radialGradient>` for the moody background bloom
- 1× `<linearGradient>` for a faint glassy text-side overlay
- 1× `<circle>` for the vibrant geometric portrait container
- 1× `<image>` for the grayscale executive portrait, clipped into a circular crop
- 1× `<clipPath>` with `<circle>` to crop the portrait image
- 5× `<path>` for angled geometric shards, highlight wedges, and decorative motion accents
- 1× `<line>` for the attribution rule
- 4× `<text>` blocks for the watermark quote mark, main quote, author, and role/context label
- 1× `<filter id="softShadow">` using `feOffset + feGaussianBlur + feMerge` for premium depth on the accent circle
- 1× `<filter id="quietGlow">` using `feGaussianBlur` for a soft accent glow behind the portrait

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <radialGradient id="bgBloom" cx="78%" cy="43%" r="70%">
      <stop offset="0%" stop-color="#2b3038"/>
      <stop offset="42%" stop-color="#181a1f"/>
      <stop offset="100%" stop-color="#0d0f13"/>
    </radialGradient>

    <linearGradient id="leftVeil" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#101318" stop-opacity="0.95"/>
      <stop offset="68%" stop-color="#101318" stop-opacity="0.52"/>
      <stop offset="100%" stop-color="#101318" stop-opacity="0"/>
    </linearGradient>

    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="18" result="off"/>
      <feGaussianBlur in="off" stdDeviation="18" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="quietGlow" x="-35%" y="-35%" width="170%" height="170%">
      <feGaussianBlur stdDeviation="26"/>
    </filter>

    <clipPath id="portraitCircle">
      <circle cx="925" cy="356" r="216"/>
    </clipPath>
  </defs>

  <!-- Dark cinematic background -->
  <rect x="0" y="0" width="1280" height="720" fill="url(#bgBloom)"/>
  <rect x="0" y="0" width="780" height="720" fill="url(#leftVeil)"/>

  <!-- Oversized watermark quotation mark -->
  <text x="72" y="272" width="310"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="285" font-weight="900"
        fill="#2f343d" opacity="0.72">“</text>

  <!-- Accent glow and circle container -->
  <circle cx="925" cy="356" r="238" fill="#ffcc00" opacity="0.25" filter="url(#quietGlow)"/>
  <circle cx="925" cy="356" r="226" fill="#ffcc00" filter="url(#softShadow)"/>

  <!-- Geometric shards that imply a reveal motion -->
  <path d="M1078 124 L1168 124 L1124 198 L1036 198 Z" fill="#ffcc00" opacity="0.92"/>
  <path d="M1115 520 L1192 520 L1150 592 L1073 592 Z" fill="#ffcc00" opacity="0.34"/>
  <path d="M760 112 L826 112 L792 170 L728 170 Z" fill="#ffffff" opacity="0.08"/>
  <path d="M704 562 L780 562 L742 626 L666 626 Z" fill="#ffffff" opacity="0.06"/>
  <path d="M835 111 C878 86 946 76 1003 94 C955 100 902 119 859 152 Z"
        fill="#ffffff" opacity="0.10"/>

  <!-- Grayscale portrait asset; use an already black-and-white image for reliable PPT output -->
  <image x="709" y="140" width="432" height="432"
         href="https://images.example.com/grayscale-executive-portrait-square.png"
         preserveAspectRatio="xMidYMid slice"
         clip-path="url(#portraitCircle)"/>

  <!-- Subtle dark crescent overlay for contrast on portrait edge -->
  <path d="M746 472 C824 584 1002 610 1116 500 C1068 596 951 650 835 620 C785 607 746 584 714 548 Z"
        fill="#0d0f13" opacity="0.22"/>

  <!-- Main quote block -->
  <text x="96" y="245" width="620"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="52" font-weight="800"
        letter-spacing="-1.2"
        fill="#f5f7fb">
    <tspan x="96" dy="0">BE THE </tspan>
    <tspan fill="#ffcc00">CHANGE</tspan>
    <tspan> THAT</tspan>
    <tspan x="96" dy="66">YOU WISH TO SEE</tspan>
    <tspan x="96" dy="66">IN THE </tspan>
    <tspan fill="#ffcc00">WORLD.</tspan>
  </text>

  <!-- Attribution -->
  <line x1="98" y1="492" x2="176" y2="492" stroke="#ffcc00" stroke-width="6"/>
  <text x="196" y="503" width="360"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="25" font-weight="700"
        fill="#ffffff">Mahatma Gandhi</text>

  <text x="196" y="536" width="410"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="17" font-weight="500"
        letter-spacing="2.6"
        fill="#9fa6b2">LEADERSHIP PRINCIPLE</text>

  <!-- Small footer accent to balance the composition -->
  <path d="M96 642 L226 642 L210 658 L96 658 Z" fill="#ffcc00"/>
  <path d="M238 642 L310 642 L294 658 L222 658 Z" fill="#ffffff" opacity="0.16"/>
</svg>
```

## Avoid in this skill
- ❌ Do not rely on SVG grayscale filters such as `feColorMatrix`; use a preprocessed black-and-white portrait image instead.
- ❌ Do not use `mask` to crop the portrait; use `clipPath` on the `<image>` only.
- ❌ Do not apply `clip-path` to decorative circles or paths; the translator only preserves clipping reliably on images.
- ❌ Do not use `skewX`, `skewY`, or `matrix()` for the angled geometry; draw parallelograms directly as `<path>` shapes.
- ❌ Do not make the quote too long; this design depends on large type and strong negative space.

## Composition notes
- Keep the quote on the left 50–60% of the slide, with generous line spacing and only one or two highlighted keywords.
- Place the portrait circle on the right third, slightly oversized, so it feels poster-like rather than like a profile photo.
- Repeat the accent color in the container, highlighted words, attribution rule, and small shards for visual rhythm.
- Let the oversized watermark quote mark sit behind the text at low contrast; it should add texture, not compete with the quote.