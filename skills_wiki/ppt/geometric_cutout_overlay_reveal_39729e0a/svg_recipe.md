# SVG Recipe — Geometric Cutout Overlay Reveal

## Visual mechanism
A full-bleed photographic background is covered by an off-white “paper” layer whose large geometric windows reveal the image underneath. Blurred dark strokes placed under the overlay but aligned to the cutout edges create the illusion of an inner shadow, making the overlay feel physically cut from thick stock.

## SVG primitives needed
- 1× `<image>` for the full-bleed photographic background.
- 1× `<rect>` for a subtle dark vignette over the photo to improve contrast.
- 1× `<linearGradient>` for the vignette wash.
- 1× compound `<path fill-rule="evenodd">` for the off-white overlay with geometric cutout holes.
- 2× `<path>` for blurred inner-shadow strokes around each geometric cutout.
- 2× `<path>` for thin highlight strokes along the cutout edges.
- 1× `<filter id="innerCutShadow">` using `feGaussianBlur` for soft cutout depth.
- 1× `<filter id="softPaperShadow">` using `feOffset`, `feGaussianBlur`, and `feMerge` for subtle paper lift.
- 5× `<text>` blocks with explicit `width` attributes for title, subtitle, body, and photo-side annotation.
- 2× `<line>` elements for editorial rules and separators.

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="photoVignette" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#07140d" stop-opacity="0.12"/>
      <stop offset="55%" stop-color="#07140d" stop-opacity="0.02"/>
      <stop offset="100%" stop-color="#07140d" stop-opacity="0.48"/>
    </linearGradient>

    <filter id="innerCutShadow" x="-15%" y="-15%" width="130%" height="130%">
      <feGaussianBlur stdDeviation="13"/>
    </filter>

    <filter id="softPaperShadow" x="-10%" y="-10%" width="120%" height="120%">
      <feOffset dx="0" dy="10"/>
      <feGaussianBlur stdDeviation="18"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <!-- Full-bleed image -->
  <image
    href="https://images.example.com/hero/foggy-pine-forest-wide-1280x720.jpg"
    x="0" y="0" width="1280" height="720"
    preserveAspectRatio="xMidYMid slice"/>

  <!-- Image contrast wash -->
  <rect x="0" y="0" width="1280" height="720" fill="url(#photoVignette)"/>

  <!-- Large cutout shadow, drawn before the paper overlay so the overlay hides the outer half -->
  <path
    d="M 760 150
       C 785 125 825 125 850 150
       L 1140 440
       C 1165 465 1165 505 1140 530
       L 850 820
       C 825 845 785 845 760 820
       L 470 530
       C 445 505 445 465 470 440
       Z"
    fill="none"
    stroke="#000000"
    stroke-opacity="0.36"
    stroke-width="38"
    filter="url(#innerCutShadow)"/>

  <!-- Secondary overlapping cutout shadow -->
  <path
    d="M 1040 -80
       C 1062 -102 1098 -102 1120 -80
       L 1295 95
       C 1317 117 1317 153 1295 175
       L 1120 350
       C 1098 372 1062 372 1040 350
       L 865 175
       C 843 153 843 117 865 95
       Z"
    fill="none"
    stroke="#000000"
    stroke-opacity="0.30"
    stroke-width="34"
    filter="url(#innerCutShadow)"/>

  <!-- Off-white overlay with compound cutout holes -->
  <path
    fill="#FAFAF5"
    fill-rule="evenodd"
    filter="url(#softPaperShadow)"
    d="M 0 0 H 1280 V 720 H 0 Z

       M 760 150
       C 785 125 825 125 850 150
       L 1140 440
       C 1165 465 1165 505 1140 530
       L 850 820
       C 825 845 785 845 760 820
       L 470 530
       C 445 505 445 465 470 440
       Z

       M 1040 -80
       C 1062 -102 1098 -102 1120 -80
       L 1295 95
       C 1317 117 1317 153 1295 175
       L 1120 350
       C 1098 372 1062 372 1040 350
       L 865 175
       C 843 153 843 117 865 95
       Z"/>

  <!-- Subtle cut-edge highlights, also half-covered by the overlay -->
  <path
    d="M 760 150
       C 785 125 825 125 850 150
       L 1140 440
       C 1165 465 1165 505 1140 530
       L 850 820
       C 825 845 785 845 760 820
       L 470 530
       C 445 505 445 465 470 440
       Z"
    fill="none"
    stroke="#FFFFFF"
    stroke-opacity="0.38"
    stroke-width="3"/>

  <path
    d="M 1040 -80
       C 1062 -102 1098 -102 1120 -80
       L 1295 95
       C 1317 117 1317 153 1295 175
       L 1120 350
       C 1098 372 1062 372 1040 350
       L 865 175
       C 843 153 843 117 865 95
       Z"
    fill="none"
    stroke="#FFFFFF"
    stroke-opacity="0.28"
    stroke-width="3"/>

  <!-- Overlay-side editorial typography -->
  <line x1="92" y1="112" x2="220" y2="112" stroke="#2D5A3C" stroke-width="3"/>
  <text x="92" y="96" width="360" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" letter-spacing="3" fill="#2D5A3C">
    FIELD REPORT
  </text>

  <text x="88" y="222" width="430" font-family="Segoe UI, Microsoft YaHei" font-size="74" font-weight="300" letter-spacing="8" fill="#2D5A3C">
    NATURE
  </text>

  <text x="94" y="278" width="390" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="600" letter-spacing="2" fill="#6F8C78">
    GEOMETRIC REVEAL SYSTEM
  </text>

  <line x1="94" y1="314" x2="392" y2="314" stroke="#B7C5B9" stroke-width="1.5"/>

  <text x="94" y="358" width="420" font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="400" fill="#315E42">
    <tspan x="94" dy="0">A layered cutout frame creates a</tspan>
    <tspan x="94" dy="30">premium editorial reveal while</tspan>
    <tspan x="94" dy="30">preserving high-contrast space</tspan>
    <tspan x="94" dy="30">for narrative and key data.</tspan>
  </text>

  <!-- Photo-side annotation -->
  <text x="842" y="560" width="320" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="600" letter-spacing="2" fill="#FFFFFF">
    FOREST INDEX
  </text>

  <text x="842" y="632" width="330" font-family="Segoe UI, Microsoft YaHei" font-size="72" font-weight="300" fill="#FFFFFF">
    68<tspan font-size="34" baseline-shift="super">%</tspan>
  </text>

  <text x="846" y="672" width="300" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="400" fill="#E7F0E8">
    canopy density increase
  </text>
</svg>
```

## Avoid in this skill
- ❌ Do not use SVG `<mask>` to punch the photo window; use a compound `<path fill-rule="evenodd">` for the overlay cutout.
- ❌ Do not apply `clip-path` to the overlay or shadow paths; clipping is only reliable on `<image>` elements.
- ❌ Do not rely on `<pattern>` fills for paper texture; use flat off-white fills or subtle gradients instead.
- ❌ Do not put `filter` on `<line>` elements; use filtered `<path>` strokes for blurred cutout shadows.
- ❌ Do not use `skewX`, `skewY`, or matrix transforms to fake the angled geometry; draw the diagonal path coordinates directly.

## Composition notes
- Keep the off-white overlay to roughly 40–50% of the slide so the title has calm negative space and the image remains emotionally dominant.
- Place the biggest cutout off-center, usually toward the lower-right, so the diagonal geometry creates motion across the canvas.
- Use dark green or charcoal typography on the paper layer, then white typography only where it sits over the exposed image.
- Let the cutout shadow cross the photo edge visibly; this shadow is the main cue that the image is being revealed through a physical layer.