# SVG Recipe — 3D Pop-Out Layer Effect

## Visual mechanism
Create depth by splitting one photo into two aligned layers: a trapezoid-clipped “stage” made from the original image, and a transparent cutout PNG of the subject placed above it so the figure breaks out of the frame. Add perspective shadows, a bottom color wash, and crisp text hierarchy to make the pop-out feel intentional rather than like a simple pasted image.

## SVG primitives needed
- 1× `<rect>` for the white slide background
- 1× `<rect>` with `<linearGradient>` for the bottom grounding band
- 2× `<path>` for soft organic background accents
- 1× `<path>` for the trapezoid drop shadow under the image stage
- 1× `<path>` for the darker extruded underside of the trapezoid stage
- 1× `<image>` clipped by a trapezoid `<clipPath>` for the original photo “ground plane”
- 1× `<image>` for the transparent PNG subject cutout layered above the stage
- 2× `<path>` for thin stage highlight and perspective edge strokes
- 1× `<ellipse>` with blur filter for the subject contact shadow
- 1× `<filter id="softShadow">` for stage shadows
- 1× `<filter id="glow">` for subtle accent glows
- 3× `<text>` blocks with explicit `width` attributes for title, subtitle, and caption

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bottomGreen" x1="0" y1="720" x2="0" y2="500" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#129447"/>
      <stop offset="0.52" stop-color="#54C778"/>
      <stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/>
    </linearGradient>

    <linearGradient id="stageEdge" x1="360" y1="394" x2="940" y2="626" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#DDF9E4"/>
      <stop offset="0.5" stop-color="#35A85A"/>
      <stop offset="1" stop-color="#0B5D2B"/>
    </linearGradient>

    <radialGradient id="accentGlow" cx="50%" cy="50%" r="50%">
      <stop offset="0" stop-color="#54C778" stop-opacity="0.38"/>
      <stop offset="1" stop-color="#54C778" stop-opacity="0"/>
    </radialGradient>

    <filter id="softShadow" x="-20%" y="-30%" width="140%" height="170%">
      <feOffset dx="0" dy="18"/>
      <feGaussianBlur stdDeviation="18"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="glow" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="22"/>
    </filter>

    <clipPath id="trapezoidStage">
      <path d="M374 392 L906 392 L1010 626 L270 626 Z"/>
    </clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#FFFFFF"/>

  <rect x="0" y="500" width="1280" height="220" fill="url(#bottomGreen)"/>

  <path d="M-90 632 C130 565 204 640 392 582 C520 543 615 565 718 646 C540 734 205 744 -90 718 Z"
        fill="#1FA35A" opacity="0.14" filter="url(#glow)"/>
  <path d="M1004 114 C1124 70 1224 118 1308 226 L1308 0 L1036 0 C978 30 958 78 1004 114 Z"
        fill="url(#accentGlow)" filter="url(#glow)"/>

  <text x="95" y="92" width="700"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="46" font-weight="800" fill="#127231">
    Nature Walk, Reimagined
  </text>

  <text x="98" y="138" width="650"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="18" font-weight="400" fill="#4B5B50">
    A cutout subject rises beyond the cropped stage, turning a flat event photo into a dimensional hero moment.
  </text>

  <path d="M344 418 L936 418 L1046 646 L238 646 Z"
        fill="#052F17" opacity="0.22" filter="url(#softShadow)"/>

  <path d="M270 626 L1010 626 L948 674 L330 674 Z"
        fill="#0A6B32" opacity="0.88"/>

  <image x="300" y="188" width="680" height="510"
         href="https://images.example.com/forest-community-walk-original-photo.jpg"
         clip-path="url(#trapezoidStage)"
         preserveAspectRatio="xMidYMid slice"/>

  <path d="M374 392 L906 392 L1010 626 L270 626 Z"
        fill="none" stroke="url(#stageEdge)" stroke-width="8" stroke-linejoin="round"/>

  <path d="M374 392 L906 392"
        fill="none" stroke="#FFFFFF" stroke-width="4" stroke-linecap="round" opacity="0.85"/>

  <ellipse cx="640" cy="602" rx="170" ry="28"
           fill="#062A14" opacity="0.28" filter="url(#glow)"/>

  <image x="390" y="116" width="500" height="505"
         href="https://images.example.com/forest-community-walk-subject-cutout-transparent.png"
         preserveAspectRatio="xMidYMid meet"/>

  <path d="M298 645 C382 676 880 678 982 645"
        fill="none" stroke="#BFF3CC" stroke-width="3" stroke-linecap="round" opacity="0.7"/>

  <text x="96" y="625" width="330"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="15" font-weight="600" fill="#FFFFFF" opacity="0.92">
   公益活动 · 城市踏青 · COMMUNITY HEALTH
  </text>

  <text x="824" y="96" width="340"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="20" font-weight="700" fill="#127231">
    Break the frame
    <tspan x="824" dy="30" font-size="16" font-weight="400" fill="#55645B">
      Align the subject cutout exactly over the same person in the stage photo.
    </tspan>
  </text>
</svg>
```

## Avoid in this skill
- ❌ Do not use `<mask>` to create the trapezoid crop; use `<clipPath>` directly on the `<image>`.
- ❌ Do not apply `clip-path` to regular shapes for this effect; the translator only preserves image clipping reliably.
- ❌ Do not rely on SVG blend modes or CSS `mix-blend-mode`; create depth using stacked editable paths, gradients, and shadows.
- ❌ Do not use `<use>` to duplicate stage edges or decorative accents; draw each path explicitly.
- ❌ Do not place the cutout subject in a rectangular photo container, or the “breaking the frame” illusion disappears.

## Composition notes
- Keep the pop-out subject centered and tall, occupying roughly 65–75% of slide height; the head or key object should rise well above the trapezoid stage.
- The trapezoid should sit in the lower middle third, with its top edge narrower than its base to imply perspective.
- Leave clean negative space in the upper left or upper right for title copy; avoid placing text behind the cutout subject.
- Use a simple bottom gradient or color wash to ground the stage, then repeat that accent color in title text and stage edge highlights.