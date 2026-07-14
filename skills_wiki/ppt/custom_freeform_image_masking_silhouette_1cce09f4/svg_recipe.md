# SVG Recipe — Custom Freeform Image Masking (Silhouette Crop)

## Visual mechanism
Crop a rectangular photo into a hand-drawn silhouette or irregular freeform path so the image reads as a standalone cutout rather than a boxed picture. Pair the clipped image with bold editorial typography and a shadow that follows the same custom edge to emphasize the bespoke crop.

## SVG primitives needed
- 1× `<rect>` for the full-slide dark navy background
- 4× `<rect>` for stacked headline label blocks and the rounded PowerPoint callout pill
- 1× `<linearGradient>` for the teal headline block
- 2× `<filter>` definitions: one soft edge shadow for the custom silhouette, one cyan glow for tutorial text
- 1× `<clipPath>` containing a custom `<path>` silhouette used to crop the photo
- 1× `<image>` clipped by the freeform silhouette path
- 2× duplicated `<path>` shapes for silhouette shadow and optional contour emphasis
- 2× `<path>` shapes for the curved tutorial arrow and its arrowhead
- 5× small `<rect>` shapes for the editable PowerPoint icon
- Multiple `<text>` elements with explicit `width` for bold title, glowing subtitle, and callout text

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#020B22"/>
      <stop offset="58%" stop-color="#031B3A"/>
      <stop offset="100%" stop-color="#000615"/>
    </linearGradient>

    <linearGradient id="tealGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#05B8CE"/>
      <stop offset="100%" stop-color="#008BA5"/>
    </linearGradient>

    <filter id="edgeShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="18" in="SourceAlpha" result="off"/>
      <feGaussianBlur in="off" stdDeviation="18" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="cyanGlow" x="-20%" y="-40%" width="140%" height="180%">
      <feGaussianBlur in="SourceGraphic" stdDeviation="4" result="blur1"/>
      <feGaussianBlur in="SourceGraphic" stdDeviation="11" result="blur2"/>
      <feMerge>
        <feMergeNode in="blur2"/>
        <feMergeNode in="blur1"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <clipPath id="hoodieSilhouetteClip" clipPathUnits="userSpaceOnUse">
      <path d="M940 0
               C982 8 1018 38 1026 92
               C1077 106 1105 146 1112 205
               C1119 265 1091 306 1062 326
               C1125 340 1174 379 1210 438
               C1255 513 1268 609 1260 720
               L650 720
               C646 607 662 513 704 446
               C742 387 797 354 854 334
               C819 304 797 260 804 202
               C812 144 850 108 893 94
               C895 52 908 18 940 0 Z"/>
    </clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>
  <ellipse cx="735" cy="430" rx="420" ry="250" fill="#0078D4" opacity="0.10"/>

  <!-- Shadow uses the same freeform outline as the image crop. Do not use <use>. -->
  <path filter="url(#edgeShadow)" opacity="0.55" fill="#000000"
        d="M940 0
           C982 8 1018 38 1026 92
           C1077 106 1105 146 1112 205
           C1119 265 1091 306 1062 326
           C1125 340 1174 379 1210 438
           C1255 513 1268 609 1260 720
           L650 720
           C646 607 662 513 704 446
           C742 387 797 354 854 334
           C819 304 797 260 804 202
           C812 144 850 108 893 94
           C895 52 908 18 940 0 Z"/>

  <image x="610" y="-28" width="710" height="770"
         href="https://images.example.com/premium-photo-person-in-white-fleece-hoodie-on-dark-background.jpg"
         preserveAspectRatio="xMidYMid slice"
         clip-path="url(#hoodieSilhouetteClip)"/>

  <path opacity="0.22" fill="none" stroke="#52E7FF" stroke-width="3"
        d="M940 0
           C982 8 1018 38 1026 92
           C1077 106 1105 146 1112 205
           C1119 265 1091 306 1062 326
           C1125 340 1174 379 1210 438
           C1255 513 1268 609 1260 720
           L650 720"/>

  <rect x="74" y="52" width="484" height="94" fill="#FFFFFF"/>
  <rect x="74" y="144" width="390" height="68" fill="#FFFFFF"/>
  <text x="88" y="122" width="455" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="65" font-weight="900" fill="#04112B" letter-spacing="2">MASK IMAGE</text>
  <text x="88" y="190" width="360" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="65" font-weight="900" fill="#04112B" letter-spacing="2">WITH ANY</text>

  <path d="M72 218 L440 218 L440 323 L370 323 L370 398 L72 398 Z"
        fill="url(#tealGrad)"/>
  <text x="86" y="293" width="335" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="67" font-weight="900" fill="#FFFFFF" letter-spacing="1">CUSTOM</text>
  <text x="86" y="370" width="285" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="67" font-weight="900" fill="#FFFFFF" letter-spacing="1">SHAPE</text>

  <text x="96" y="486" width="500" filter="url(#cyanGlow)"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="60" font-weight="800" fill="#A8F7FF" letter-spacing="5">FULL TUTORIAL</text>

  <rect x="64" y="508" width="520" height="156" rx="64" fill="#FFFFFF"/>
  <rect x="124" y="534" width="91" height="104" fill="#E04A22"/>
  <rect x="124" y="534" width="91" height="28" fill="#FF6B35" opacity="0.85"/>
  <rect x="124" y="589" width="91" height="49" fill="#C9391C" opacity="0.85"/>
  <rect x="100" y="558" width="58" height="57" rx="3" fill="#B93226"/>
  <text x="116" y="599" width="38" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="36" font-weight="800" fill="#FFFFFF">P</text>
  <text x="248" y="604" width="300" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="54" font-weight="400" fill="#050505">PowerPoint</text>

  <path d="M588 586 C640 583 652 524 615 469" fill="none"
        stroke="#FFFFFF" stroke-width="9" stroke-linecap="round"/>
  <path d="M617 462 L640 460 L622 476 L610 516 L586 469 Z" fill="#FFFFFF"/>
</svg>
```

## Avoid in this skill
- ❌ `mask="url(#...)"` on the image or shape; use `<clipPath>` applied directly to `<image>` instead.
- ❌ Applying `clip-path` to a `<rect>` or `<path>` expecting a boolean intersection; the translator only preserves clipping reliably on `<image>`.
- ❌ `<use href="#silhouette">` to reuse the crop outline; duplicate the path data for shadow/outline layers.
- ❌ Rectangular image shadows; place a duplicate freeform path behind the image and apply the shadow filter to that path so the shadow follows the custom edge.
- ❌ Overly jagged polygon masks unless that is intentional; smooth Bézier paths create a more premium silhouette crop.

## Composition notes
- Keep the clipped image large and anchored to one side so the custom edge becomes the visual hero, not a small decorative crop.
- Use high-contrast headline blocks on the opposite side; the image silhouette should carve out negative space around the typography.
- Repeat one accent color, such as cyan/teal, in the label block, glow text, and subtle image contour for a cohesive branded rhythm.
- Let the photo bleed beyond the canvas before clipping; this prevents the original rectangular photo boundary from appearing inside the custom silhouette.