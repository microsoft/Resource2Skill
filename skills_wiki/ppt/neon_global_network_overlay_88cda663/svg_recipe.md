# SVG Recipe — Neon Global Network Overlay

## Visual mechanism
A dark, cinematic Earth map is treated as the substrate for bright neon infrastructure paths: layered glowing curves, angular route segments, and white hub nodes create the illusion of global data cables across oceans. The strongest effect comes from stacking blurred colored strokes beneath crisp colored cores, then anchoring every convergence point with small luminous nodes.

## SVG primitives needed
- 1× `<rect>` for the deep space / dark ocean background
- 35–60× tiny `<circle>` for sparse starfield particles
- 1× `<clipPath>` with `<circle>` for cropping a satellite Earth/map image into a globe edge
- 1× `<image>` for the photorealistic Earth or high-contrast regional satellite map
- 1× large `<circle>` for atmospheric cyan rim glow around the globe
- 1× large `<circle>` with radial gradient for dark vignette shading over the globe
- 18–30× `<path>` for neon network routes, using cubic or polyline-like path commands
- 18–30× duplicate `<path>` for soft under-glow strokes beneath the crisp route lines
- 12–20× `<circle>` for bright hub nodes at landing stations
- 1× `<filter id="softGlow">` using `feGaussianBlur` for atmospheric and route glow
- 1× `<filter id="nodeGlow">` using `feGaussianBlur` + `feMerge` for glowing node dots
- 2–4× `<text>` with explicit `width` attributes for optional executive title/caption overlay

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <radialGradient id="spaceVignette" cx="54%" cy="42%" r="78%">
      <stop offset="0%" stop-color="#18324A"/>
      <stop offset="58%" stop-color="#07111F"/>
      <stop offset="100%" stop-color="#02050B"/>
    </radialGradient>

    <radialGradient id="globeShade" cx="44%" cy="34%" r="72%">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0"/>
      <stop offset="55%" stop-color="#00162C" stop-opacity="0.10"/>
      <stop offset="100%" stop-color="#00040A" stop-opacity="0.52"/>
    </radialGradient>

    <linearGradient id="horizonGlow" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#BFFFFF" stop-opacity="0.95"/>
      <stop offset="42%" stop-color="#00D8FF" stop-opacity="0.42"/>
      <stop offset="100%" stop-color="#005A88" stop-opacity="0"/>
    </linearGradient>

    <filter id="softGlow" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="5"/>
    </filter>

    <filter id="nodeGlow" x="-250%" y="-250%" width="600%" height="600%">
      <feGaussianBlur in="SourceGraphic" stdDeviation="5" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="titleShadow" x="-20%" y="-20%" width="150%" height="150%">
      <feOffset dx="0" dy="4" result="off"/>
      <feGaussianBlur in="off" stdDeviation="6" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <clipPath id="globeClip">
      <circle cx="462" cy="365" r="575"/>
    </clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#spaceVignette)"/>

  <circle cx="42" cy="68" r="1.3" fill="#FFFFFF" opacity="0.55"/>
  <circle cx="95" cy="119" r="0.9" fill="#B8F7FF" opacity="0.45"/>
  <circle cx="168" cy="38" r="1.1" fill="#FFFFFF" opacity="0.38"/>
  <circle cx="244" cy="91" r="1.6" fill="#FFFFFF" opacity="0.50"/>
  <circle cx="336" cy="28" r="0.9" fill="#99EFFF" opacity="0.35"/>
  <circle cx="1134" cy="47" r="1.2" fill="#FFFFFF" opacity="0.38"/>
  <circle cx="1208" cy="98" r="1.6" fill="#D8FFFF" opacity="0.44"/>
  <circle cx="1167" cy="174" r="0.8" fill="#FFFFFF" opacity="0.32"/>
  <circle cx="80" cy="620" r="1.1" fill="#FFFFFF" opacity="0.28"/>
  <circle cx="1185" cy="632" r="1.2" fill="#FFFFFF" opacity="0.30"/>
  <circle cx="1237" cy="514" r="0.9" fill="#B8F7FF" opacity="0.32"/>

  <circle cx="462" cy="365" r="592" fill="none" stroke="url(#horizonGlow)" stroke-width="22" opacity="0.75" filter="url(#softGlow)"/>
  <circle cx="462" cy="365" r="577" fill="#061A2B"/>

  <image
    href="https://images.example.com/satellite-earth-east-asia-pacific-dark-ocean.jpg"
    x="-95" y="-235" width="1230" height="1230"
    preserveAspectRatio="xMidYMid slice"
    clip-path="url(#globeClip)"
    opacity="0.94"/>

  <circle cx="462" cy="365" r="575" fill="url(#globeShade)"/>
  <path d="M18 464 C78 314 158 174 284 76 C354 22 431 -6 530 -22" fill="none" stroke="#D6FFFF" stroke-width="3.2" opacity="0.78" filter="url(#softGlow)"/>

  <g fill="none" stroke-linecap="round" stroke-linejoin="round" opacity="0.72" filter="url(#softGlow)">
    <path d="M343 520 C470 420 566 330 725 218 C840 137 982 124 1132 100" stroke="#00FFFF" stroke-width="7"/>
    <path d="M482 574 C574 472 662 403 822 361 C948 327 1044 236 1178 162" stroke="#FF00FF" stroke-width="7"/>
    <path d="M356 412 C493 447 604 467 742 438 C892 405 1016 414 1228 375" stroke="#F9FF46" stroke-width="6"/>
    <path d="M513 494 C620 414 699 357 836 288 C941 236 1078 222 1210 196" stroke="#31FF53" stroke-width="7"/>
    <path d="M438 326 C542 344 628 371 731 405 C849 443 995 536 1192 661" stroke="#FF4B3E" stroke-width="7"/>
    <path d="M606 266 C684 315 750 362 824 421 L963 618 L1214 646" stroke="#35B9FF" stroke-width="6"/>
    <path d="M726 218 L798 282 L909 256 L1007 325 L1162 313 L1248 384" stroke="#F4DE38" stroke-width="5"/>
    <path d="M611 486 L710 530 L834 505 L965 421 L1106 438 L1244 503" stroke="#00FF7A" stroke-width="5"/>
    <path d="M410 610 L536 541 L626 565 L742 496 L865 530 L1020 518" stroke="#58E8FF" stroke-width="5"/>
    <path d="M878 692 L963 618 L1046 539 L1162 552 L1263 610" stroke="#864BFF" stroke-width="6"/>
  </g>

  <g fill="none" stroke-linecap="round" stroke-linejoin="round">
    <path d="M343 520 C470 420 566 330 725 218 C840 137 982 124 1132 100" stroke="#BFFFFF" stroke-width="1.9"/>
    <path d="M482 574 C574 472 662 403 822 361 C948 327 1044 236 1178 162" stroke="#FF65FF" stroke-width="1.8"/>
    <path d="M356 412 C493 447 604 467 742 438 C892 405 1016 414 1228 375" stroke="#FFFF6A" stroke-width="1.8"/>
    <path d="M513 494 C620 414 699 357 836 288 C941 236 1078 222 1210 196" stroke="#62FF72" stroke-width="1.9"/>
    <path d="M438 326 C542 344 628 371 731 405 C849 443 995 536 1192 661" stroke="#FF786B" stroke-width="1.9"/>
    <path d="M606 266 C684 315 750 362 824 421 L963 618 L1214 646" stroke="#7AEAFF" stroke-width="1.6"/>
    <path d="M726 218 L798 282 L909 256 L1007 325 L1162 313 L1248 384" stroke="#FFF36A" stroke-width="1.5"/>
    <path d="M611 486 L710 530 L834 505 L965 421 L1106 438 L1244 503" stroke="#41FF99" stroke-width="1.5"/>
    <path d="M410 610 L536 541 L626 565 L742 496 L865 530 L1020 518" stroke="#A5F6FF" stroke-width="1.4"/>
    <path d="M878 692 L963 618 L1046 539 L1162 552 L1263 610" stroke="#A87BFF" stroke-width="1.6"/>
  </g>

  <g filter="url(#nodeGlow)">
    <circle cx="343" cy="520" r="5.2" fill="#FFFFFF"/>
    <circle cx="482" cy="574" r="5.4" fill="#FFFFFF"/>
    <circle cx="356" cy="412" r="4.8" fill="#FFFFFF"/>
    <circle cx="438" cy="326" r="4.9" fill="#FFFFFF"/>
    <circle cx="513" cy="494" r="5.4" fill="#FFFFFF"/>
    <circle cx="606" cy="266" r="4.6" fill="#FFFFFF"/>
    <circle cx="725" cy="218" r="5.1" fill="#FFFFFF"/>
    <circle cx="822" cy="361" r="4.8" fill="#FFFFFF"/>
    <circle cx="963" cy="618" r="5.6" fill="#FFFFFF"/>
    <circle cx="1007" cy="325" r="4.8" fill="#FFFFFF"/>
    <circle cx="1132" cy="100" r="5.6" fill="#FFFFFF"/>
    <circle cx="1178" cy="162" r="5.0" fill="#FFFFFF"/>
  </g>

  <text x="58" y="82" width="420" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="19" font-weight="700" fill="#8EEBFF" letter-spacing="2" opacity="0.95" filter="url(#titleShadow)">GLOBAL BACKBONE MAP</text>
  <text x="58" y="134" width="500" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="44" font-weight="800" fill="#FFFFFF" letter-spacing="-1.5" filter="url(#titleShadow)">
    <tspan x="58" dy="0">NEON NETWORK</tspan>
    <tspan x="58" dy="48" fill="#CFFFFF">OVERLAY</tspan>
  </text>
  <text x="62" y="232" width="380" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="16" font-weight="500" fill="#B7C7D8" opacity="0.82">
    Live routes, cable corridors, and regional landing hubs visualized as luminous infrastructure paths.
  </text>
</svg>
```

## Avoid in this skill
- ❌ Do not use `<mask>` to fade the globe edge; use gradients, large circles, and image clipping instead.
- ❌ Do not apply `clip-path` to route paths or shading shapes; clipping is reliable here only on the `<image>`.
- ❌ Do not rely on `marker-end` for route arrows; this technique is about glowing cable paths, not arrowheads.
- ❌ Do not make all paths straight horizontal lines; mix sweeping Bezier arcs with angular route segments for a cable-map feel.
- ❌ Do not over-label the geography; too many labels destroy the cinematic infrastructure aesthetic.

## Composition notes
- Keep the globe/map dominant: 70–85% of the canvas should feel like dark Earth, ocean, or space, with the planet edge partially cropped for scale.
- Place text in a low-detail dark area, usually upper-left or lower-left, and keep it short so the network overlay remains the hero.
- Use each neon color more than once, but let cyan and white be the visual “key light”; magenta, lime, yellow, and red are accents.
- Build every important cable as two strokes: a thick blurred glow underneath and a thin crisp stroke above, with white glowing nodes at convergence points.