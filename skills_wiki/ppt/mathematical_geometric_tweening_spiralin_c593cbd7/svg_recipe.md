# SVG Recipe — Mathematical Geometric Tweening (Spiraling Wireframes & Depth Interpolation)

## Visual mechanism
Generate a tunnel-like field by interpolating rounded rectangles from a small bright “start state” to an oversized muted “end state,” changing size, position, rotation, stroke color, and opacity step by step. The repeated wireframes create pseudo-3D depth and leading lines that pull attention toward the title.

## SVG primitives needed
- 1× `<rect>` for the dark full-slide background
- 1× `<rect>` with radial/linear gradient fill for atmospheric color wash
- 28–45× `<rect>` with `fill="none"`, `rx`, interpolated `stroke`, and `transform="rotate(...)"` for the spiraling tweened wireframe tunnel
- 1× `<ellipse>` with blur filter for the inner cyan energy glow
- 1× `<path>` for a soft diagonal depth haze / light beam
- 1× `<filter id="softGlow">` using `feGaussianBlur` for the focal glow
- 1× `<filter id="textShadow">` using `feOffset + feGaussianBlur + feMerge` for premium title depth
- 3× `<text>` blocks with explicit `width` attributes for title, subtitle, and small metadata label
- 2× `<line>` elements for thin editorial accent rules

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <radialGradient id="bgRadial" cx="36%" cy="50%" r="70%">
      <stop offset="0%" stop-color="#12304C"/>
      <stop offset="38%" stop-color="#091A2F"/>
      <stop offset="100%" stop-color="#070B18"/>
    </radialGradient>
    <linearGradient id="hazeGrad" x1="180" y1="80" x2="1160" y2="660" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#00FFD8" stop-opacity="0.18"/>
      <stop offset="45%" stop-color="#2A7BFF" stop-opacity="0.08"/>
      <stop offset="100%" stop-color="#071024" stop-opacity="0"/>
    </linearGradient>
    <filter id="softGlow" x="-80%" y="-80%" width="260%" height="260%">
      <feGaussianBlur stdDeviation="18"/>
    </filter>
    <filter id="textShadow" x="-20%" y="-20%" width="150%" height="150%">
      <feOffset dx="0" dy="8"/>
      <feGaussianBlur stdDeviation="8"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#070B18"/>
  <rect x="0" y="0" width="1280" height="720" fill="url(#bgRadial)"/>
  <path d="M70,590 C260,410 430,265 610,230 C820,190 990,270 1240,70 L1280,720 L0,720 Z" fill="url(#hazeGrad)" opacity="0.85"/>
  <ellipse cx="455" cy="360" rx="120" ry="92" fill="#00FFD8" opacity="0.18" filter="url(#softGlow)"/>

  <rect x="424" y="329" width="62" height="62" rx="14" fill="none" stroke="#00FFD8" stroke-width="2.2" opacity="1.00" transform="rotate(0 455 360)"/>
  <rect x="414" y="319" width="82" height="82" rx="18" fill="none" stroke="#00F4D5" stroke-width="2.1" opacity="0.98" transform="rotate(5 455 360)"/>
  <rect x="401" y="306" width="108" height="108" rx="22" fill="none" stroke="#00E9D1" stroke-width="2.0" opacity="0.96" transform="rotate(10 455 360)"/>
  <rect x="386" y="291" width="138" height="138" rx="27" fill="none" stroke="#00DDCC" stroke-width="1.9" opacity="0.94" transform="rotate(16 455 360)"/>
  <rect x="368" y="273" width="174" height="174" rx="33" fill="none" stroke="#00D1C6" stroke-width="1.8" opacity="0.92" transform="rotate(22 455 360)"/>
  <rect x="347" y="252" width="216" height="216" rx="39" fill="none" stroke="#00C4BF" stroke-width="1.75" opacity="0.90" transform="rotate(28 455 360)"/>
  <rect x="323" y="229" width="264" height="264" rx="45" fill="none" stroke="#00B8B8" stroke-width="1.7" opacity="0.88" transform="rotate(34 455 360)"/>
  <rect x="294" y="203" width="320" height="320" rx="52" fill="none" stroke="#05ABB0" stroke-width="1.65" opacity="0.86" transform="rotate(40 454 363)"/>
  <rect x="260" y="174" width="386" height="386" rx="60" fill="none" stroke="#0A9EAA" stroke-width="1.6" opacity="0.84" transform="rotate(47 453 367)"/>
  <rect x="221" y="141" width="462" height="462" rx="69" fill="none" stroke="#0F92A4" stroke-width="1.55" opacity="0.82" transform="rotate(54 452 372)"/>
  <rect x="176" y="103" width="550" height="550" rx="78" fill="none" stroke="#14869E" stroke-width="1.5" opacity="0.79" transform="rotate(61 451 378)"/>
  <rect x="125" y="61" width="650" height="650" rx="88" fill="none" stroke="#187A98" stroke-width="1.45" opacity="0.76" transform="rotate(68 450 386)"/>
  <rect x="67" y="14" width="764" height="764" rx="99" fill="none" stroke="#1B6F93" stroke-width="1.4" opacity="0.73" transform="rotate(75 449 396)"/>
  <rect x="3" y="-39" width="894" height="894" rx="112" fill="none" stroke="#1E648C" stroke-width="1.35" opacity="0.70" transform="rotate(82 450 408)"/>
  <rect x="-67" y="-100" width="1040" height="1040" rx="126" fill="none" stroke="#205B87" stroke-width="1.3" opacity="0.66" transform="rotate(89 453 420)"/>
  <rect x="-142" y="-168" width="1206" height="1206" rx="142" fill="none" stroke="#225281" stroke-width="1.25" opacity="0.62" transform="rotate(96 461 435)"/>
  <rect x="-223" y="-242" width="1392" height="1392" rx="158" fill="none" stroke="#244A7B" stroke-width="1.2" opacity="0.58" transform="rotate(103 473 454)"/>
  <rect x="-309" y="-323" width="1598" height="1598" rx="176" fill="none" stroke="#254474" stroke-width="1.15" opacity="0.54" transform="rotate(110 490 476)"/>
  <rect x="-400" y="-411" width="1824" height="1824" rx="194" fill="none" stroke="#253D6E" stroke-width="1.1" opacity="0.50" transform="rotate(117 512 501)"/>
  <rect x="-494" y="-505" width="2070" height="2070" rx="214" fill="none" stroke="#243766" stroke-width="1.05" opacity="0.46" transform="rotate(124 541 530)"/>
  <rect x="-592" y="-606" width="2336" height="2336" rx="236" fill="none" stroke="#23315F" stroke-width="1.0" opacity="0.42" transform="rotate(131 576 562)"/>
  <rect x="-688" y="-710" width="2620" height="2620" rx="258" fill="none" stroke="#212C57" stroke-width="0.95" opacity="0.38" transform="rotate(138 622 600)"/>

  <rect x="72" y="224" width="520" height="252" rx="28" fill="#070B18" opacity="0.54"/>
  <line x1="92" y1="246" x2="210" y2="246" stroke="#00FFD8" stroke-width="3"/>
  <line x1="92" y1="484" x2="360" y2="484" stroke="#2A7BFF" stroke-width="1.5" opacity="0.65"/>

  <text x="92" y="322" width="500" font-family="Segoe UI, Microsoft YaHei" font-size="48" font-weight="700" fill="#F5FBFF" letter-spacing="3" filter="url(#textShadow)">
    多 元 化 创 新 发 展
  </text>
  <text x="96" y="374" width="470" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="600" fill="#00FFD8" letter-spacing="4">
    GEOMETRIC TWEENING SYSTEM
  </text>
  <text x="96" y="423" width="430" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#A9BCD6" opacity="0.86">
    Interpolated size, rotation, position, and color create a native vector tunnel with cinematic depth.
  </text>
</svg>
```

## Avoid in this skill
- ❌ Using `<animate>` or `<animateTransform>` to create the spiral; build the static tweened frames as separate editable shapes instead
- ❌ Applying `marker-end` to paths for arrows inside the vortex; use plain wireframe rectangles and separate `<line>` arrows only if needed
- ❌ Using `<pattern>` fills for the tunnel texture; repeated native rectangles are more reliable and editable
- ❌ Applying `clip-path` to the wireframe rectangles; clipping non-image elements will not translate reliably
- ❌ Using `transform="matrix(...)"` or skew transforms to fake perspective; use rotation, scale-like size changes, and position interpolation only

## Composition notes
- Place the smallest, brightest rectangle near the intended focal point; it becomes the “vanishing core” that guides the eye.
- Let the largest rectangles extend well beyond the slide edges so the tunnel feels immersive rather than contained.
- Keep text on a calmer dark patch or translucent plaque; avoid placing fine typography over the densest wireframe region.
- Use color rhythm from bright cyan at the core to muted navy-blue at the perimeter to imply depth and atmospheric fade.