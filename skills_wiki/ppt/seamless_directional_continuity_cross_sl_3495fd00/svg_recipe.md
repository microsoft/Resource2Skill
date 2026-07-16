# SVG Recipe — Seamless Directional Continuity (Cross-Slide Flow)

## Visual mechanism
Create the illusion that each slide is a cropped viewport on one long horizontal world: persistent skyline, matching horizon height, and off-canvas elements that bleed across slide edges. When paired with a PowerPoint push transition, the viewer reads the deck as a smooth camera pan rather than separate slides.

## SVG primitives needed
- 1× `<rect>` for the main slide background color.
- 2× edge-bleed `<rect>` shapes for hints of the previous/next slide colors.
- 15–25× `<rect>` for a continuous white skyline silhouette and matching window cutouts.
- 3–5× `<circle>` / `<ellipse>` for persistent decorative anchors that slide across frames.
- 1× `<line>` plus 1× `<path>` arrowhead for the horizontal “camera direction” rail.
- 2× floating `<rect>` cards for transition/animation UI callouts.
- 6–10× `<text>` blocks with explicit `width` attributes for title, bullets, step labels, and UI labels.
- 2× `<filter>` definitions: one soft shadow for floating panels and one glow for white continuity elements.
- Optional `<linearGradient>` for a premium but still flat-feeling background wash.

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" font-family="Segoe UI, Microsoft YaHei, sans-serif">
  <defs>
    <linearGradient id="roseWash" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#E69AA0"/>
      <stop offset="62%" stop-color="#DD8F94"/>
      <stop offset="100%" stop-color="#C97782"/>
    </linearGradient>
    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="14"/>
      <feGaussianBlur stdDeviation="14"/>
      <feColorMatrix type="matrix" values="0 0 0 0 0.06 0 0 0 0 0.05 0 0 0 0 0.10 0 0 0 0.28 0"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="whiteGlow" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="8"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <!-- current viewport background; adjacent colors peek in to imply the deck continues horizontally -->
  <rect x="0" y="0" width="1280" height="720" fill="url(#roseWash)"/>
  <rect x="-90" y="0" width="160" height="720" fill="#5B8EEB" opacity="0.95"/>
  <rect x="1210" y="0" width="160" height="720" fill="#8C7BE8" opacity="0.82"/>

  <!-- cross-slide camera rail -->
  <line x1="250" y1="92" x2="1060" y2="92" stroke="#FFFFFF" stroke-width="5" stroke-linecap="round" opacity="0.72"/>
  <path d="M1060 92 L1038 78 L1038 106 Z" fill="#FFFFFF" opacity="0.72"/>
  <circle cx="320" cy="92" r="13" fill="#FFFFFF"/>
  <circle cx="640" cy="92" r="16" fill="#FFFFFF"/>
  <circle cx="960" cy="92" r="13" fill="#FFFFFF" opacity="0.72"/>
  <text x="284" y="132" width="80" font-size="18" font-weight="700" fill="#FFFFFF" text-anchor="middle">SLIDE 1</text>
  <text x="600" y="136" width="90" font-size="20" font-weight="800" fill="#FFFFFF" text-anchor="middle">SLIDE 2</text>
  <text x="922" y="132" width="80" font-size="18" font-weight="700" fill="#FFFFFF" text-anchor="middle" opacity="0.78">SLIDE 3</text>

  <!-- slide content: large, flat, persistent geometry -->
  <circle cx="92" cy="190" r="36" fill="#FFFFFF" filter="url(#whiteGlow)"/>
  <ellipse cx="1182" cy="244" rx="74" ry="74" fill="#FFFFFF" opacity="0.18"/>
  <circle cx="1252" cy="244" r="34" fill="#FFFFFF" opacity="0.55"/>

  <text x="92" y="210" width="390" font-size="64" font-weight="900" letter-spacing="2" fill="#FFFFFF">SLIDE 2</text>
  <text x="154" y="276" width="560" font-size="28" font-weight="600" fill="#FFFFFF">• This is my first point</text>
  <text x="154" y="320" width="560" font-size="28" font-weight="600" fill="#FFFFFF">• This is my second point</text>
  <text x="154" y="364" width="560" font-size="28" font-weight="600" fill="#FFFFFF" opacity="0.72">• This is my third point</text>

  <!-- floating transition UI cards, reinforcing directional continuity -->
  <rect x="720" y="150" width="380" height="168" rx="18" fill="#FFFFFF" filter="url(#softShadow)" transform="rotate(-3 910 234)"/>
  <text x="760" y="204" width="280" font-size="23" font-weight="700" fill="#111111" transform="rotate(-3 910 234)">Slide Transition</text>
  <rect x="762" y="232" width="34" height="26" rx="4" fill="#EEF1F4" stroke="#4E5660" stroke-width="3" transform="rotate(-3 910 234)"/>
  <text x="820" y="254" width="210" font-size="22" font-weight="600" fill="#111111" transform="rotate(-3 910 234)">Push from right</text>
  <path d="M1048 242 L1064 252 L1048 262 Z" fill="#111111" transform="rotate(-3 910 234)"/>

  <rect x="770" y="324" width="410" height="146" rx="16" fill="#FFFFFF" filter="url(#softShadow)" transform="rotate(-5 975 397)"/>
  <text x="812" y="372" width="250" font-size="22" font-weight="700" fill="#111111" transform="rotate(-5 975 397)">Object Animations</text>
  <text x="812" y="414" width="250" font-size="20" font-weight="500" fill="#111111" transform="rotate(-5 975 397)">Fly in from left</text>
  <line x1="812" y1="444" x2="1100" y2="444" stroke="#E7A800" stroke-width="5" stroke-linecap="round" transform="rotate(-5 975 397)"/>
  <circle cx="1010" cy="444" r="14" fill="#FFC400" transform="rotate(-5 975 397)"/>

  <!-- persistent white skyline anchored to the same y-position on every slide in the sequence -->
  <rect x="0" y="646" width="1280" height="74" fill="#FFFFFF"/>
  <rect x="-8" y="536" width="86" height="184" fill="#FFFFFF"/>
  <rect x="96" y="582" width="74" height="138" fill="#FFFFFF"/>
  <rect x="194" y="500" width="112" height="220" fill="#FFFFFF"/>
  <rect x="330" y="552" width="82" height="168" fill="#FFFFFF"/>
  <rect x="438" y="470" width="128" height="250" fill="#FFFFFF"/>
  <rect x="590" y="578" width="74" height="142" fill="#FFFFFF"/>
  <rect x="690" y="528" width="104" height="192" fill="#FFFFFF"/>
  <rect x="820" y="604" width="84" height="116" fill="#FFFFFF"/>
  <rect x="930" y="486" width="130" height="234" fill="#FFFFFF"/>
  <rect x="1080" y="560" width="82" height="160" fill="#FFFFFF"/>
  <rect x="1190" y="512" width="102" height="208" fill="#FFFFFF"/>

  <!-- window cutouts use the local slide color; duplicate their positions across slides -->
  <rect x="226" y="540" width="18" height="24" rx="3" fill="#DD8F94"/>
  <rect x="258" y="540" width="18" height="24" rx="3" fill="#DD8F94"/>
  <rect x="470" y="512" width="20" height="28" rx="3" fill="#DD8F94"/>
  <rect x="512" y="512" width="20" height="28" rx="3" fill="#DD8F94"/>
  <rect x="724" y="568" width="18" height="24" rx="3" fill="#DD8F94"/>
  <rect x="758" y="568" width="18" height="24" rx="3" fill="#DD8F94"/>
  <rect x="974" y="528" width="20" height="28" rx="3" fill="#DD8F94"/>
  <rect x="1016" y="528" width="20" height="28" rx="3" fill="#DD8F94"/>

  <!-- edge labels remind the slide author what must align between neighboring slides -->
  <text x="18" y="700" width="220" font-size="16" font-weight="800" fill="#5B8EEB">previous slide continues here</text>
  <text x="1025" y="700" width="230" font-size="16" font-weight="800" fill="#8C7BE8" text-anchor="end">next slide begins here</text>
</svg>
```

## Avoid in this skill
- ❌ Do not fake continuity with unrelated backgrounds per slide; the skyline/horizon must align exactly across the sequence.
- ❌ Do not use SVG `<animate>` or `<animateTransform>` for the slide motion; use PowerPoint’s native Push transition after translation.
- ❌ Do not use `<marker>` arrowheads on paths; draw arrowheads as simple editable `<path>` triangles.
- ❌ Do not rely on masks or clipping on vector shapes for the panorama crop; keep the slide itself as the crop/viewport.
- ❌ Do not change horizon height, building positions, or decorative anchor positions between slides unless they are intentionally moving through the “world.”

## Composition notes
- Treat each slide as a 1280×720 viewport on a wider imaginary canvas; repeat the same bottom skyline at the same `y` coordinate on every slide.
- Keep 20–30% of the bottom as the persistent city/floor layer, with the main text living in the upper-left or center for clear motion readability.
- Add edge-bleed shapes that partially enter/exit the canvas so the push transition has objects to carry across the seam.
- In PowerPoint, apply a slide-level Push transition from right/left consistently; the SVG supplies the visual continuity, while the transition supplies the camera-pan illusion.