# SVG Recipe — 3D Hinged Paper Cut-out Typography

## Visual mechanism
A dark, full-width base letter creates the “cut hole,” while a white duplicate letter is pinned to the same left edge and horizontally compressed to look like a paper flap folded outward. A blurred, offset duplicate between the two layers supplies the inner depth shadow, making the word feel physically sliced from the slide surface.

## SVG primitives needed
- 1× `<rect>` for the warm paper-sheet background
- 6× `<text>` for the dark full-size void letters
- 6× `<text>` for the blurred inner shadow cast by each folded flap
- 6× `<text>` for the compressed white flap letters
- 6× `<line>` for subtle vertical hinge creases at each letter’s left edge
- 4× `<path>` for decorative paper-cut slivers and soft surface highlights
- 1× `<linearGradient id="paperBg">` for the background paper tone
- 1× `<linearGradient id="voidGrad">` for the purple cut-out depth
- 1× `<filter id="innerShadow">` applied to the shadow text duplicates
- 1× `<filter id="softGlow">` applied to the white flap text for a faint paper lift

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="paperBg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#f8f8f6"/>
      <stop offset="55%" stop-color="#eeeeeb"/>
      <stop offset="100%" stop-color="#e3e1dd"/>
    </linearGradient>

    <linearGradient id="voidGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#26113d"/>
      <stop offset="48%" stop-color="#4b007f"/>
      <stop offset="100%" stop-color="#170b24"/>
    </linearGradient>

    <filter id="innerShadow" x="-25%" y="-25%" width="160%" height="160%">
      <feOffset dx="18" dy="14" in="SourceAlpha" result="off"/>
      <feGaussianBlur stdDeviation="10" in="off" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="softGlow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="1.2"/>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#paperBg)"/>

  <path d="M77 96 C186 58 292 64 412 88" fill="none" stroke="#ffffff" stroke-width="4" opacity="0.45"/>
  <path d="M882 617 C1008 660 1125 647 1218 591" fill="none" stroke="#cbc7bf" stroke-width="3" opacity="0.5"/>
  <path d="M1060 98 L1132 78 L1110 151 Z" fill="#ffffff" opacity="0.38"/>
  <path d="M173 594 L236 626 L153 653 Z" fill="#d8d4cc" opacity="0.36"/>

  <!-- Layer 1: full-width colored cut-out voids -->
  <text x="135" y="452" width="160" font-family="Segoe UI Black, Segoe UI, Microsoft YaHei, sans-serif" font-size="230" font-weight="900" fill="url(#voidGrad)">E</text>
  <text x="300" y="452" width="160" font-family="Segoe UI Black, Segoe UI, Microsoft YaHei, sans-serif" font-size="230" font-weight="900" fill="url(#voidGrad)">F</text>
  <text x="465" y="452" width="160" font-family="Segoe UI Black, Segoe UI, Microsoft YaHei, sans-serif" font-size="230" font-weight="900" fill="url(#voidGrad)">F</text>
  <text x="630" y="452" width="160" font-family="Segoe UI Black, Segoe UI, Microsoft YaHei, sans-serif" font-size="230" font-weight="900" fill="url(#voidGrad)">E</text>
  <text x="795" y="452" width="170" font-family="Segoe UI Black, Segoe UI, Microsoft YaHei, sans-serif" font-size="230" font-weight="900" fill="url(#voidGrad)">C</text>
  <text x="970" y="452" width="160" font-family="Segoe UI Black, Segoe UI, Microsoft YaHei, sans-serif" font-size="230" font-weight="900" fill="url(#voidGrad)">T</text>

  <!-- Layer 2: offset soft shadow, compressed from the same hinge edge -->
  <text transform="translate(157 14) scale(0.72 1)" x="0" y="452" width="160" font-family="Segoe UI Black, Segoe UI, Microsoft YaHei, sans-serif" font-size="230" font-weight="900" fill="#1b0a2b" opacity="0.55" filter="url(#innerShadow)">E</text>
  <text transform="translate(322 14) scale(0.72 1)" x="0" y="452" width="160" font-family="Segoe UI Black, Segoe UI, Microsoft YaHei, sans-serif" font-size="230" font-weight="900" fill="#1b0a2b" opacity="0.55" filter="url(#innerShadow)">F</text>
  <text transform="translate(487 14) scale(0.72 1)" x="0" y="452" width="160" font-family="Segoe UI Black, Segoe UI, Microsoft YaHei, sans-serif" font-size="230" font-weight="900" fill="#1b0a2b" opacity="0.55" filter="url(#innerShadow)">F</text>
  <text transform="translate(652 14) scale(0.72 1)" x="0" y="452" width="160" font-family="Segoe UI Black, Segoe UI, Microsoft YaHei, sans-serif" font-size="230" font-weight="900" fill="#1b0a2b" opacity="0.55" filter="url(#innerShadow)">E</text>
  <text transform="translate(817 14) scale(0.72 1)" x="0" y="452" width="170" font-family="Segoe UI Black, Segoe UI, Microsoft YaHei, sans-serif" font-size="230" font-weight="900" fill="#1b0a2b" opacity="0.55" filter="url(#innerShadow)">C</text>
  <text transform="translate(992 14) scale(0.72 1)" x="0" y="452" width="160" font-family="Segoe UI Black, Segoe UI, Microsoft YaHei, sans-serif" font-size="230" font-weight="900" fill="#1b0a2b" opacity="0.55" filter="url(#innerShadow)">T</text>

  <!-- Layer 3: white folded paper flaps, left edge pinned -->
  <text transform="translate(135 0) scale(0.72 1)" x="0" y="452" width="160" font-family="Segoe UI Black, Segoe UI, Microsoft YaHei, sans-serif" font-size="230" font-weight="900" fill="#ffffff" filter="url(#softGlow)">E</text>
  <text transform="translate(300 0) scale(0.72 1)" x="0" y="452" width="160" font-family="Segoe UI Black, Segoe UI, Microsoft YaHei, sans-serif" font-size="230" font-weight="900" fill="#ffffff" filter="url(#softGlow)">F</text>
  <text transform="translate(465 0) scale(0.72 1)" x="0" y="452" width="160" font-family="Segoe UI Black, Segoe UI, Microsoft YaHei, sans-serif" font-size="230" font-weight="900" fill="#ffffff" filter="url(#softGlow)">F</text>
  <text transform="translate(630 0) scale(0.72 1)" x="0" y="452" width="160" font-family="Segoe UI Black, Segoe UI, Microsoft YaHei, sans-serif" font-size="230" font-weight="900" fill="#ffffff" filter="url(#softGlow)">E</text>
  <text transform="translate(795 0) scale(0.72 1)" x="0" y="452" width="170" font-family="Segoe UI Black, Segoe UI, Microsoft YaHei, sans-serif" font-size="230" font-weight="900" fill="#ffffff" filter="url(#softGlow)">C</text>
  <text transform="translate(970 0) scale(0.72 1)" x="0" y="452" width="160" font-family="Segoe UI Black, Segoe UI, Microsoft YaHei, sans-serif" font-size="230" font-weight="900" fill="#ffffff" filter="url(#softGlow)">T</text>

  <!-- Hinge creases: place on top so the fold reads as a physical seam -->
  <line x1="135" y1="276" x2="135" y2="456" stroke="#d7d4ce" stroke-width="3" opacity="0.85"/>
  <line x1="300" y1="276" x2="300" y2="456" stroke="#d7d4ce" stroke-width="3" opacity="0.85"/>
  <line x1="465" y1="276" x2="465" y2="456" stroke="#d7d4ce" stroke-width="3" opacity="0.85"/>
  <line x1="630" y1="276" x2="630" y2="456" stroke="#d7d4ce" stroke-width="3" opacity="0.85"/>
  <line x1="795" y1="276" x2="795" y2="456" stroke="#d7d4ce" stroke-width="3" opacity="0.85"/>
  <line x1="970" y1="276" x2="970" y2="456" stroke="#d7d4ce" stroke-width="3" opacity="0.85"/>

  <text x="132" y="548" width="1020" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="22" font-weight="600" letter-spacing="5" fill="#6f6878" opacity="0.72">HINGED PAPER TYPOGRAPHY / EDITABLE SVG SHAPES</text>
</svg>
```

## Avoid in this skill
- ❌ `skewX`, `skewY`, or `matrix(...)` transforms to fake perspective; they are not reliably preserved.
- ❌ `<mask>` or clip paths on text to create cut-out interiors; clipping is only safe on `<image>`.
- ❌ Converting the whole word into a single flat screenshot; the effect should remain editable as native text and shapes.
- ❌ Tight letter spacing; the compressed white flaps need breathing room or they visually collide.
- ❌ Shadows on `<line>` hinge marks; line filters are dropped, so keep hinge lines simple and unfiltered.

## Composition notes
- Keep the word large and centered, occupying roughly 65–75% of slide width; this effect works best as the hero object.
- Use a light neutral paper background so the white folded flaps are visible through shadow, crease lines, and subtle contrast.
- Give each letter independent spacing; the left edge of every flap must align with its dark base letter to read as a hinge.
- Reserve the bottom 15–20% for a small subtitle or metadata line; do not compete with the typographic illusion.