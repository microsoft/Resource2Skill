# SVG Recipe — Faded Image Overlay (Semi-Transparent Picture Blend)

## Visual mechanism
A full-bleed background photo establishes atmosphere, while a second thematic photo is placed on top at reduced opacity so it reads as a soft ghosted layer rather than a dominant image. Text sits in a high-legibility zone, often protected by a translucent gradient scrim, while the faded picture blends into the background on the opposite side.

## SVG primitives needed
- 1× `<image>` for the full-slide environmental background photograph
- 1× `<image>` for the semi-transparent foreground photograph, using `opacity="0.45"` to create the faded overlay
- 1× `<clipPath>` with rounded `<rect>` for cropping the foreground image into a refined soft-corner card
- 2× `<linearGradient>` for left-side readability scrim and bottom atmospheric tint
- 1× `<radialGradient>` for a subtle glow behind the faded image
- 1× `<filter>` with `feOffset + feGaussianBlur + feMerge` for a premium soft shadow behind the foreground image
- 3× `<rect>` for full-canvas tints, glass text panel, and faded photo shadow/card base
- 4× `<circle>` for decorative bullet markers and small environmental accent dots
- 1× `<path>` for an organic green accent shape that visually ties the copy to the imagery
- 5× `<text>` blocks with explicit `width` attributes for title, subtitle, paragraph, and bullet labels

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="leftScrim" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#F7FAF1" stop-opacity="0.96"/>
      <stop offset="54%" stop-color="#F7FAF1" stop-opacity="0.82"/>
      <stop offset="82%" stop-color="#F7FAF1" stop-opacity="0.24"/>
      <stop offset="100%" stop-color="#F7FAF1" stop-opacity="0"/>
    </linearGradient>

    <linearGradient id="bottomMist" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0"/>
      <stop offset="100%" stop-color="#DDECCF" stop-opacity="0.55"/>
    </linearGradient>

    <radialGradient id="photoGlow" cx="50%" cy="48%" r="58%">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.58"/>
      <stop offset="72%" stop-color="#E8F3DD" stop-opacity="0.20"/>
      <stop offset="100%" stop-color="#E8F3DD" stop-opacity="0"/>
    </radialGradient>

    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="145%">
      <feOffset dx="0" dy="18" in="SourceAlpha" result="off"/>
      <feGaussianBlur in="off" stdDeviation="22" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <clipPath id="roundedPhotoCrop">
      <rect x="676" y="126" width="520" height="428" rx="34" ry="34"/>
    </clipPath>
  </defs>

  <!-- Full-bleed atmospheric background -->
  <image
    href="https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?auto=format&amp;fit=crop&amp;w=1920&amp;h=1080"
    x="0" y="0" width="1280" height="720" preserveAspectRatio="xMidYMid slice"/>

  <!-- Global brightening and readability treatments -->
  <rect x="0" y="0" width="1280" height="720" fill="#EEF6E8" opacity="0.20"/>
  <rect x="0" y="0" width="900" height="720" fill="url(#leftScrim)"/>
  <rect x="0" y="440" width="1280" height="280" fill="url(#bottomMist)"/>

  <!-- Organic accent wash behind text -->
  <path d="M-60,590 C120,520 202,625 348,578 C504,528 552,620 692,570 C650,706 420,750 196,724 C42,706 -38,676 -60,590 Z"
        fill="#8FCB54" opacity="0.16"/>

  <!-- Soft glow and shadow base for faded overlay image -->
  <ellipse cx="936" cy="346" rx="340" ry="260" fill="url(#photoGlow)"/>
  <rect x="676" y="126" width="520" height="428" rx="34" ry="34"
        fill="#FFFFFF" opacity="0.32" filter="url(#softShadow)"/>

  <!-- The semi-transparent picture blend: foreground image intentionally ghosted -->
  <image
    href="https://images.unsplash.com/photo-1524594152303-9fd13543fe6e?auto=format&amp;fit=crop&amp;w=1000&amp;h=820"
    x="676" y="126" width="520" height="428"
    preserveAspectRatio="xMidYMid slice"
    clip-path="url(#roundedPhotoCrop)"
    opacity="0.46"/>

  <!-- Optional pale overlay to make the faded image feel integrated, not pasted -->
  <rect x="676" y="126" width="520" height="428" rx="34" ry="34"
        fill="#F4FAED" opacity="0.18"/>

  <!-- Text panel content -->
  <text x="86" y="112" width="470"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="18" font-weight="700" letter-spacing="2.8"
        fill="#6FAF2B">SUSTAINABILITY OUTLOOK</text>

  <text x="84" y="184" width="520"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="48" font-weight="800"
        fill="#2F342F">
    <tspan x="84" dy="0">Faded imagery</tspan>
    <tspan x="84" dy="58">keeps the data calm</tspan>
  </text>

  <text x="88" y="288" width="500"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="22" font-weight="400"
        fill="#3C433B">
    <tspan x="88" dy="0">Use a semi-transparent picture when the image</tspan>
    <tspan x="88" dy="34">should provide emotional context without fighting</tspan>
    <tspan x="88" dy="34">for attention against the message.</tspan>
  </text>

  <!-- Bullet 1 -->
  <circle cx="102" cy="420" r="8" fill="#73B829"/>
  <text x="126" y="428" width="470"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="21" font-weight="700"
        fill="#303630">Reduce photo opacity to 40–55%</text>

  <!-- Bullet 2 -->
  <circle cx="102" cy="478" r="8" fill="#73B829"/>
  <text x="126" y="486" width="470"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="21" font-weight="700"
        fill="#303630">Protect text with a light gradient scrim</text>

  <!-- Bullet 3 -->
  <circle cx="102" cy="536" r="8" fill="#73B829"/>
  <text x="126" y="544" width="470"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="21" font-weight="700"
        fill="#303630">Use matching accent colors for cohesion</text>

  <!-- Small decorative environmental dots -->
  <circle cx="1130" cy="104" r="6" fill="#FFFFFF" opacity="0.48"/>
  <circle cx="1190" cy="586" r="10" fill="#73B829" opacity="0.28"/>
</svg>
```

## Avoid in this skill
- ❌ Do not simulate transparency with a white rectangle only; the actual foreground `<image>` should carry reduced `opacity` so it genuinely blends with the background.
- ❌ Do not apply `clip-path` to groups, rectangles, or text; only apply the rounded crop to the `<image>`.
- ❌ Do not use `<mask>` for fading the picture edges; masks are not safe for this workflow.
- ❌ Do not place high-contrast text directly over the faded photo unless a scrim or panel preserves readability.
- ❌ Do not use `filter` on `<line>` elements; if adding arrows or callouts, keep shadows on rectangles, paths, or text only.

## Composition notes
- Keep the text block on one side, usually the left 40–48% of the slide, and reserve the opposite side for the faded photo overlay.
- Use 40–55% foreground image opacity for a true ghosted effect; below 35% the image may disappear, above 65% it becomes too dominant.
- Add a soft light gradient behind copy so the slide still reads like a clean executive page rather than text pasted over a photograph.
- Pull accent colors from the photo theme, such as greens for nature imagery, to make bullets and labels feel integrated.