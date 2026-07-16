# SVG Recipe — Hemisphere Rotational Transition

## Visual mechanism
A single oversized square with a hard two-color vertical split sits behind all content and rotates 180° between two consecutive slides using PowerPoint Morph. Because the square is larger than the slide diagonal, its edges never appear, so the viewer perceives the whole background “hemisphere” flipping from bottom to top.

## SVG primitives needed
- 1× full-slide `<rect>` for a safe white base layer
- 1× oversized `<rect>` for the Morph rotator, filled by a hard-stop `<linearGradient>`
- 1× `<linearGradient>` for the two-tone hemisphere split
- 1× `<filter id="softShadow">` applied to foreground cards/device shapes
- 1× `<filter id="ambientGlow">` applied to soft accent orbs
- 2× `<circle>` for subtle decorative glow fields
- 3× `<rect>` for a static laptop/device frame, screen, and base
- 1× `<clipPath>` with rounded `<rect>` for clipping the screenshot image into the laptop screen
- 1× `<image>` for the static foreground screenshot/content window
- 4× `<path>` for device highlight, base shadow, decorative orbit arcs, and small icon geometry
- Multiple `<text>` elements with explicit `width` for section title, subtitle, and instructional labels
- Several thin `<line>` elements for decorative UI ticks and separators

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <!-- Hard split: white top, coral bottom. Rotate this oversized rect 180° on the next slide. -->
    <linearGradient id="hemisphereSplit" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="49.85%" stop-color="#FFFFFF"/>
      <stop offset="50.15%" stop-color="#FF7F50"/>
      <stop offset="100%" stop-color="#FF7F50"/>
    </linearGradient>

    <linearGradient id="deviceMetal" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#242734"/>
      <stop offset="55%" stop-color="#11131B"/>
      <stop offset="100%" stop-color="#05060A"/>
    </linearGradient>

    <linearGradient id="screenWash" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.96"/>
      <stop offset="100%" stop-color="#F5F7FB" stop-opacity="0.96"/>
    </linearGradient>

    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="18"/>
      <feGaussianBlur stdDeviation="18"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="ambientGlow" x="-80%" y="-80%" width="260%" height="260%">
      <feGaussianBlur stdDeviation="34"/>
    </filter>

    <clipPath id="screenClip">
      <rect x="359" y="189" width="562" height="316" rx="18"/>
    </clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#FFFFFF"/>

  <!-- Morph target: keep identical on both slides except transform rotation.
       In PowerPoint, name this shape/group !!Rotator on both slides. -->
  <rect id="morph_rotator"
        x="-95" y="-455" width="1470" height="1470"
        fill="url(#hemisphereSplit)"
        transform="rotate(0 640 360)"/>

  <!-- Subtle atmospheric depth; these are static foreground/background accents, not Morph targets. -->
  <circle cx="1020" cy="610" r="150" fill="#FFFFFF" opacity="0.24" filter="url(#ambientGlow)"/>
  <circle cx="245" cy="565" r="105" fill="#FFB39A" opacity="0.24" filter="url(#ambientGlow)"/>

  <path d="M104 559 C210 501, 316 506, 410 569"
        fill="none" stroke="#FFFFFF" stroke-width="2.5" stroke-opacity="0.42"
        stroke-dasharray="10 12"/>
  <path d="M880 118 C998 65, 1126 88, 1195 184"
        fill="none" stroke="#FF7F50" stroke-width="2.5" stroke-opacity="0.18"
        stroke-dasharray="8 14"/>

  <!-- Static title layer. It does not rotate; only the large split square changes between slides. -->
  <text x="82" y="104" width="410"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="18" font-weight="700" letter-spacing="3"
        fill="#FF7F50">STRATEGIC SHIFT</text>

  <text x="78" y="174" width="470"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="64" font-weight="800"
        fill="#101218">PART 01</text>

  <text x="84" y="220" width="430"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="19" fill="#3E4351">
    <tspan x="84" dy="0">Foundation phase: align the operating model</tspan>
    <tspan x="84" dy="27">before the next hemisphere rotates in.</tspan>
  </text>

  <!-- Laptop mockup remains visually stable while the background flips. -->
  <rect x="324" y="155" width="632" height="392" rx="32"
        fill="url(#deviceMetal)" filter="url(#softShadow)"/>
  <rect x="349" y="179" width="582" height="340" rx="24"
        fill="#0B0D13"/>
  <rect x="359" y="189" width="562" height="316" rx="18"
        fill="url(#screenWash)"/>

  <image x="359" y="189" width="562" height="316"
         href="https://images.example.com/product-dashboard-clean-light-ui.png"
         clip-path="url(#screenClip)"
         preserveAspectRatio="xMidYMid slice"/>

  <!-- Editable overlay UI details, so the mockup still looks good if the image is unavailable. -->
  <rect x="392" y="224" width="176" height="20" rx="10" fill="#111827" opacity="0.88"/>
  <rect x="392" y="262" width="118" height="11" rx="5.5" fill="#FF7F50" opacity="0.92"/>
  <rect x="392" y="292" width="420" height="10" rx="5" fill="#D8DEE9"/>
  <rect x="392" y="318" width="365" height="10" rx="5" fill="#E3E7EF"/>
  <rect x="392" y="344" width="438" height="10" rx="5" fill="#E3E7EF"/>

  <path d="M647 437 C690 369, 742 386, 770 326 C800 260, 846 259, 884 216"
        fill="none" stroke="#FF7F50" stroke-width="7" stroke-linecap="round" opacity="0.86"/>
  <circle cx="647" cy="437" r="8" fill="#FF7F50"/>
  <circle cx="884" cy="216" r="8" fill="#FF7F50"/>

  <path d="M282 548 L998 548 C974 579, 916 594, 826 594 L454 594 C364 594, 306 579, 282 548 Z"
        fill="#171A23" filter="url(#softShadow)"/>
  <rect x="526" y="548" width="228" height="9" rx="4.5" fill="#2E3340"/>
  <path d="M324 548 C396 568, 884 568, 956 548"
        fill="none" stroke="#FFFFFF" stroke-width="2" stroke-opacity="0.12"/>

  <!-- Transition cue / presenter note rendered as editable text. -->
  <rect x="914" y="604" width="258" height="46" rx="23"
        fill="#FFFFFF" opacity="0.82"/>
  <text x="940" y="633" width="215"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="15" font-weight="700"
        fill="#1A1D26">Next slide: rotate 180°</text>

  <line x1="84" y1="642" x2="244" y2="642" stroke="#FFFFFF" stroke-width="3" stroke-opacity="0.65"/>
  <line x1="84" y1="660" x2="180" y2="660" stroke="#FFFFFF" stroke-width="3" stroke-opacity="0.42"/>
  <text x="84" y="628" width="245"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="13" font-weight="600" letter-spacing="1.8"
        fill="#FFFFFF" opacity="0.82">MORPH-READY BACKDROP</text>
</svg>
```

## Avoid in this skill
- ❌ Do not use SVG `<animate>` or `<animateTransform>`; create two static slides and let PowerPoint Morph perform the rotation.
- ❌ Do not build the flip from two separate half-slide rectangles; Morph will not read it as one rotating object and the seam may drift.
- ❌ Do not let the oversized square be too small. Its side should be at least the slide diagonal, preferably 1450–1500 units on a 1280×720 canvas.
- ❌ Do not apply `clip-path` to the rotator or foreground shapes; use clipping only on `<image>` elements.
- ❌ Do not use `transform="matrix(...)"` or skew transforms for the rotator; use plain `rotate(angle 640 360)`.

## Composition notes
- Duplicate the slide, keep the same oversized rotator in the same position, and change only its transform from `rotate(0 640 360)` to `rotate(180 640 360)`; then apply PowerPoint’s Morph transition to the second slide.
- In PowerPoint, name the corresponding rotator object `!!Rotator` on both slides if your workflow exposes object names; this makes Morph matching more reliable.
- Keep the main text and device mockup static above the rotator so the audience has a stable visual anchor while the background flips.
- Use one strong accent color plus white; the premium effect comes from the clean hard split, oversized geometry, and controlled negative space.