# SVG Recipe — Geometric Profile Showcase

## Visual mechanism
A desaturated full-bleed background photo is energized by large translucent diagonal polygons in magenta, orange, and deep violet. A framed profile portrait anchors the left side while bold white typography, line icons, and gradient skill bars occupy the right side, creating a modern expert-introduction slide.

## SVG primitives needed
- 2× `<image>` for the full-slide background city/photo texture and the expert portrait
- 1× `<clipPath>` with rounded `<rect>` for the editable rounded portrait crop
- 1× `<rect>` for the darkening overlay over the background photo
- 4× `<path>` for large semi-transparent angular polygon overlays
- 1× `<linearGradient>` for the magenta-to-orange skill bar fills
- 1× `<linearGradient>` for a subtle violet background wash
- 1× `<filter id="softShadow">` applied to the portrait frame and cards
- 3× `<rect>` for portrait frame, shadow card, and translucent info panel
- 8× `<rect>` for skill bar tracks and filled progress bars
- 8× `<path>` for simple white line-art icons and geometric accent strokes
- Multiple `<text>` elements with explicit `width` for title, name, bio, labels, and values

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="violetWash" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#100B22" stop-opacity="0.20"/>
      <stop offset="100%" stop-color="#2E2153" stop-opacity="0.65"/>
    </linearGradient>
    <linearGradient id="hotGrad" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#E33383"/>
      <stop offset="55%" stop-color="#EF6D66"/>
      <stop offset="100%" stop-color="#F6A15F"/>
    </linearGradient>
    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feOffset dx="0" dy="14" result="off"/>
      <feGaussianBlur in="off" stdDeviation="14" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <clipPath id="portraitClip">
      <rect x="86" y="170" width="330" height="330" rx="18" ry="18"/>
    </clipPath>
  </defs>

  <image x="0" y="0" width="1280" height="720" preserveAspectRatio="xMidYMid slice"
         href="https://images.unsplash.com/photo-1605979854205-399564177716?q=80&amp;w=1600&amp;auto=format&amp;fit=crop"/>
  <rect x="0" y="0" width="1280" height="720" fill="#15121C" opacity="0.62"/>
  <rect x="0" y="0" width="1280" height="720" fill="url(#violetWash)"/>

  <path d="M0,330 L1280,438 L1280,720 L0,720 Z" fill="#2E2153" opacity="0.74"/>
  <path d="M0,0 L825,0 L444,720 L0,720 Z" fill="#DB2777" opacity="0.58"/>
  <path d="M520,0 L1280,0 L1280,436 L965,368 Z" fill="#EF7153" opacity="0.68"/>
  <path d="M1005,192 L1280,250 L1280,720 L1082,720 Z" fill="#15112B" opacity="0.40"/>

  <path d="M730,86 L970,34 L936,92 L1240,40" fill="none" stroke="#FFFFFF" stroke-width="2" opacity="0.25"/>
  <path d="M40,612 L315,548 L286,610 L565,548" fill="none" stroke="#FFFFFF" stroke-width="2" opacity="0.18"/>

  <rect x="66" y="150" width="370" height="370" rx="24" fill="#100A1E" opacity="0.45" filter="url(#softShadow)"/>
  <rect x="76" y="160" width="350" height="350" rx="22" fill="#FFFFFF" opacity="0.96"/>
  <image x="86" y="170" width="330" height="330" preserveAspectRatio="xMidYMid slice" clip-path="url(#portraitClip)"
         href="https://images.unsplash.com/photo-1594744803329-e58b31de8bf5?q=80&amp;w=900&amp;auto=format&amp;fit=crop"/>

  <text x="72" y="92" width="480" font-family="Segoe UI, Microsoft YaHei" font-size="28" font-weight="700"
        letter-spacing="4" fill="#FFFFFF">ABOUT OUR EXPERT</text>
  <text x="76" y="565" width="420" font-family="Segoe UI, Microsoft YaHei" font-size="42" font-weight="800"
        letter-spacing="2" fill="#FFFFFF">ANGELA SMITH</text>
  <text x="80" y="604" width="430" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="500"
        letter-spacing="1.2" fill="#FFFFFF" opacity="0.92">WEB DESIGNER • DEVELOPER • CREATIVE</text>

  <rect x="520" y="126" width="650" height="470" rx="28" fill="#140F26" opacity="0.28" filter="url(#softShadow)"/>
  <text x="560" y="174" width="560" font-family="Segoe UI, Microsoft YaHei" font-size="24" font-weight="800"
        letter-spacing="3" fill="#FFFFFF">PROFILE SNAPSHOT</text>
  <text x="560" y="222" width="560" font-family="Segoe UI, Microsoft YaHei" font-size="17" fill="#FFFFFF" opacity="0.88">
    <tspan font-weight="700">Angela</tspan><tspan> leads product experiences for fast-moving technology teams. Her work blends brand systems, interface design, and front-end craft to turn complex ideas into memorable digital products.</tspan>
  </text>

  <path d="M562,278 h58 m-29,-29 v58" stroke="#FFFFFF" stroke-width="5" stroke-linecap="round" opacity="0.92" fill="none"/>
  <path d="M678,256 c26,0 48,17 56,40 c-12,23 -33,40 -56,40 c-25,0 -47,-17 -58,-40 c11,-23 33,-40 58,-40 z M678,281 c9,0 16,7 16,15 c0,9 -7,16 -16,16 c-9,0 -16,-7 -16,-16 c0,-8 7,-15 16,-15 z" fill="none" stroke="#FFFFFF" stroke-width="4" opacity="0.9"/>
  <path d="M804,252 l44,22 v42 l-44,22 l-44,-22 v-42 z M782,275 l22,12 l22,-12 M804,287 v31" fill="none" stroke="#FFFFFF" stroke-width="4" stroke-linejoin="round" opacity="0.9"/>
  <path d="M924,252 c28,0 50,22 50,50 c0,28 -22,50 -50,50 c-28,0 -50,-22 -50,-50 c0,-28 22,-50 50,-50 z M900,302 h48 M924,278 v48" fill="none" stroke="#FFFFFF" stroke-width="4" stroke-linecap="round" opacity="0.9"/>

  <text x="560" y="392" width="180" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="700" fill="#FFFFFF">UX STRATEGY</text>
  <text x="1030" y="392" width="80" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="700" fill="#FFFFFF" text-anchor="end">92%</text>
  <rect x="560" y="410" width="550" height="12" rx="6" fill="#FFFFFF" opacity="0.22"/>
  <rect x="560" y="410" width="506" height="12" rx="6" fill="url(#hotGrad)"/>

  <text x="560" y="458" width="180" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="700" fill="#FFFFFF">VISUAL DESIGN</text>
  <text x="1030" y="458" width="80" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="700" fill="#FFFFFF" text-anchor="end">88%</text>
  <rect x="560" y="476" width="550" height="12" rx="6" fill="#FFFFFF" opacity="0.22"/>
  <rect x="560" y="476" width="484" height="12" rx="6" fill="url(#hotGrad)"/>

  <text x="560" y="524" width="180" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="700" fill="#FFFFFF">FRONT-END</text>
  <text x="1030" y="524" width="80" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="700" fill="#FFFFFF" text-anchor="end">81%</text>
  <rect x="560" y="542" width="550" height="12" rx="6" fill="#FFFFFF" opacity="0.22"/>
  <rect x="560" y="542" width="446" height="12" rx="6" fill="url(#hotGrad)"/>

  <text x="560" y="636" width="260" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700"
        letter-spacing="2" fill="#FFFFFF" opacity="0.72">AVAILABLE FOR KEYNOTES</text>
  <path d="M1035,624 L1108,624 L1088,604 M1108,624 L1088,644" fill="none" stroke="#FFFFFF" stroke-width="4" stroke-linecap="round" stroke-linejoin="round" opacity="0.78"/>
</svg>
```

## Avoid in this skill
- ❌ Do not use SVG `<mask>` or blend modes to desaturate the background; use a pre-desaturated image or dark translucent overlays instead.
- ❌ Do not clip polygons, text, or groups; only apply `clip-path` to the portrait `<image>`.
- ❌ Do not use `marker-end` for decorative arrows; draw arrowheads as explicit `<path>` geometry.
- ❌ Do not build the diagonal backdrop as a flat raster image if editability matters; use individual translucent `<path>` polygons.
- ❌ Do not omit `width` on text blocks, especially paragraph text and labels, or PowerPoint text layout will be unpredictable.

## Composition notes
- Keep the portrait and name in the left third; this creates a stable identity anchor against the energetic diagonal geometry.
- Use the right two-thirds for the bio, icons, and skill bars, aligning everything to one strong vertical axis.
- Let the largest polygons extend beyond the slide edges so the composition feels cropped, cinematic, and less like a diagram.
- Maintain high contrast: white typography over deep violet shadows, with magenta/orange gradients reserved for emphasis and progress indicators.