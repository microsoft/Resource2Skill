# SVG Recipe — Overlapping Circles Grid

## Visual mechanism
Three large translucent circles form a horizontal feature grid, with the middle circle drawn last so it visually floats above the side circles. Each circle acts as a soft container for one feature, using gradients, shadows, and simple line-art icons to keep the layout minimal but premium.

## SVG primitives needed
- 1× `<rect>` for the full-slide background
- 3× large `<circle>` for the overlapping feature containers
- 3× small `<circle>` for numbered badges inside the feature circles
- 6× decorative `<circle>` for ambient dots and soft depth
- 1× `<line>` for a subtle dashed horizontal alignment guide behind the circles
- 6× `<path>` for simple editable feature icons and decorative spark accents
- 1× `<linearGradient>` for the background wash
- 3× `<radialGradient>` for dimensional circle fills
- 1× `<filter id="softShadow">` for circle card shadows
- 1× `<filter id="glow">` for the top circle’s luminous edge
- Multiple `<text>` elements with explicit `width` attributes for headline, subtitle, labels, and body copy

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgWash" x1="0" y1="0" x2="1280" y2="720">
      <stop offset="0%" stop-color="#F7FAFF"/>
      <stop offset="48%" stop-color="#EEF4FF"/>
      <stop offset="100%" stop-color="#F8FBFF"/>
    </linearGradient>

    <radialGradient id="circleBlue" cx="38%" cy="28%" r="72%">
      <stop offset="0%" stop-color="#7EC8FF"/>
      <stop offset="58%" stop-color="#4F8DF7"/>
      <stop offset="100%" stop-color="#3567D6"/>
    </radialGradient>

    <radialGradient id="circleMint" cx="42%" cy="24%" r="76%">
      <stop offset="0%" stop-color="#B7FFE8"/>
      <stop offset="54%" stop-color="#43D6B2"/>
      <stop offset="100%" stop-color="#16A489"/>
    </radialGradient>

    <radialGradient id="circleViolet" cx="38%" cy="24%" r="78%">
      <stop offset="0%" stop-color="#D7C6FF"/>
      <stop offset="54%" stop-color="#8A6BFF"/>
      <stop offset="100%" stop-color="#5C42D6"/>
    </radialGradient>

    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="18"/>
      <feGaussianBlur stdDeviation="18"/>
      <feColorMatrix type="matrix" values="0 0 0 0 0.13  0 0 0 0 0.18  0 0 0 0 0.28  0 0 0 0.22 0"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="glow" x="-25%" y="-25%" width="150%" height="150%">
      <feGaussianBlur stdDeviation="10" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgWash)"/>

  <circle cx="156" cy="158" r="5" fill="#80A7FF" opacity="0.35"/>
  <circle cx="1098" cy="138" r="7" fill="#41D4B1" opacity="0.38"/>
  <circle cx="1132" cy="594" r="4" fill="#8A6BFF" opacity="0.32"/>
  <circle cx="118" cy="604" r="6" fill="#4F8DF7" opacity="0.25"/>
  <circle cx="1010" cy="248" r="3" fill="#15233D" opacity="0.16"/>
  <circle cx="268" cy="246" r="3" fill="#15233D" opacity="0.14"/>

  <text x="640" y="78" width="760" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="42" font-weight="700" fill="#172033">
    Three forces, one operating model
  </text>
  <text x="640" y="116" width="680" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="17" fill="#5A6578">
    Use overlapping circles when separate initiatives must read as connected parts of the same system.
  </text>

  <line x1="265" y1="385" x2="1015" y2="385" stroke="#AEBBE0" stroke-width="2" stroke-dasharray="8 14" opacity="0.55"/>

  <!-- Draw side circles first so their overlap tucks underneath the center circle -->
  <circle cx="430" cy="390" r="188" fill="url(#circleBlue)" fill-opacity="0.88" filter="url(#softShadow)"/>
  <circle cx="850" cy="390" r="188" fill="url(#circleViolet)" fill-opacity="0.88" filter="url(#softShadow)"/>

  <path d="M398 287 L462 287 L484 316 L430 357 L376 316 Z" fill="none" stroke="#FFFFFF" stroke-width="8" stroke-linejoin="round" opacity="0.86"/>
  <path d="M397 318 C410 332 418 339 430 347 C443 337 452 329 463 318" fill="none" stroke="#FFFFFF" stroke-width="7" stroke-linecap="round" opacity="0.62"/>

  <path d="M810 292 C833 274 867 275 890 295 C913 316 917 350 900 375 C884 399 852 407 826 394 L795 404 L806 373 C790 348 790 314 810 292 Z" fill="none" stroke="#FFFFFF" stroke-width="8" stroke-linejoin="round" opacity="0.86"/>
  <path d="M835 330 L875 330 M835 356 L862 356" fill="none" stroke="#FFFFFF" stroke-width="7" stroke-linecap="round" opacity="0.68"/>

  <circle cx="640" cy="390" r="206" fill="url(#circleMint)" fill-opacity="0.94" filter="url(#glow)"/>
  <circle cx="640" cy="390" r="206" fill="none" stroke="#FFFFFF" stroke-width="3" opacity="0.5"/>

  <path d="M640 282 C674 282 701 309 701 343 C701 377 674 404 640 404 C606 404 579 377 579 343 C579 309 606 282 640 282 Z" fill="none" stroke="#FFFFFF" stroke-width="8" opacity="0.9"/>
  <path d="M611 344 L632 365 L674 322" fill="none" stroke="#FFFFFF" stroke-width="10" stroke-linecap="round" stroke-linejoin="round" opacity="0.9"/>

  <circle cx="356" cy="252" r="28" fill="#FFFFFF" opacity="0.94"/>
  <text x="356" y="262" width="52" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="24" font-weight="700" fill="#3567D6">1</text>

  <circle cx="640" cy="220" r="30" fill="#FFFFFF" opacity="0.96"/>
  <text x="640" y="231" width="56" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="25" font-weight="700" fill="#16A489">2</text>

  <circle cx="924" cy="252" r="28" fill="#FFFFFF" opacity="0.94"/>
  <text x="924" y="262" width="52" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="24" font-weight="700" fill="#5C42D6">3</text>

  <text x="430" y="445" width="230" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="28" font-weight="700" fill="#FFFFFF">Discover</text>
  <text x="430" y="482" width="245" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" fill="#EAF3FF">
    Map signals, customer pain points, and opportunity spaces before scaling decisions.
  </text>

  <text x="640" y="458" width="250" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="31" font-weight="700" fill="#FFFFFF">Design</text>
  <text x="640" y="497" width="270" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="16" fill="#EEFFF9">
    Convert insight into a shared operating model with clear ownership and momentum.
  </text>

  <text x="850" y="445" width="230" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="28" font-weight="700" fill="#FFFFFF">Deliver</text>
  <text x="850" y="482" width="245" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" fill="#F1EDFF">
    Launch priority moves, track value, and keep teams aligned through execution.
  </text>

  <path d="M272 213 L282 236 L306 246 L282 256 L272 279 L262 256 L238 246 L262 236 Z" fill="#FFFFFF" opacity="0.55"/>
  <path d="M1008 452 L1018 474 L1041 484 L1018 494 L1008 516 L998 494 L975 484 L998 474 Z" fill="#FFFFFF" opacity="0.44"/>
</svg>
```

## Avoid in this skill
- ❌ Drawing the center circle before the side circles; the overlap hierarchy becomes unclear and the grid loses its focal point.
- ❌ Using `<mask>` or blend-mode-dependent effects to create intersections; rely on opacity, gradients, and draw order instead.
- ❌ Placing long bullet lists inside the circles; curved containers need short labels and one concise supporting sentence.
- ❌ Applying filters to dashed connector `<line>` elements; shadows and glows should be applied to circles or paths only.

## Composition notes
- Keep the headline and subtitle in the top 15–18% of the slide; the circle cluster should dominate the middle and lower middle.
- Use three circles with 25–35% horizontal overlap; the side circles should feel partially tucked under the center.
- Put the most important item in the center circle and make it slightly larger, brighter, or more saturated.
- Maintain high-contrast white text inside the circles and use the background only for calm negative space.