# SVG Recipe — Prismatic Green Geometric Layout

## Visual mechanism
A full-slide low-poly mesh of overlapping green facets creates depth and analytical energy while remaining flat, editable, and clean. High-contrast white title typography and crisp hexagonal content nodes sit above the facets to give the layout a structured corporate keynote feel.

## SVG primitives needed
- 15× `<path>` for angular low-poly background facets and diagonal shard overlays
- 3× `<path>` for white hexagonal numbered content nodes
- 3× `<rect>` for semi-transparent rounded content cards on the right
- 6× `<line>` for subtle geometric connector accents and diagonal construction lines
- 5× `<circle>` for small precision-dot accents
- 7× `<text>` for title, subtitle, node numbers, and body copy
- 3× `<linearGradient>` for green depth fields and a soft glass-card fill
- 1× `<radialGradient>` for the bright central highlight glow
- 1× `<filter id="softShadow">` applied to cards and hexagons
- 1× `<filter id="titleGlow">` applied to the main title text

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="greenBase" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#B5EFC8"/>
      <stop offset="45%" stop-color="#74C98F"/>
      <stop offset="100%" stop-color="#3A9B67"/>
    </linearGradient>
    <linearGradient id="deepFacet" x1="1" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#48B777"/>
      <stop offset="100%" stop-color="#237F59"/>
    </linearGradient>
    <linearGradient id="glassCard" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.96"/>
      <stop offset="100%" stop-color="#E9FFF0" stop-opacity="0.78"/>
    </linearGradient>
    <radialGradient id="centerGlow" cx="42%" cy="28%" r="70%">
      <stop offset="0%" stop-color="#D9FFE2" stop-opacity="0.85"/>
      <stop offset="58%" stop-color="#8ADAA2" stop-opacity="0.38"/>
      <stop offset="100%" stop-color="#2C8E5F" stop-opacity="0"/>
    </radialGradient>
    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="10"/>
      <feGaussianBlur stdDeviation="12"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="titleGlow" x="-10%" y="-20%" width="120%" height="150%">
      <feGaussianBlur stdDeviation="3"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#greenBase)"/>
  <rect x="0" y="0" width="1280" height="720" fill="url(#centerGlow)"/>

  <path d="M0 0 L575 0 L410 265 L0 392 Z" fill="#9CE0B1"/>
  <path d="M575 0 L890 0 L710 218 L410 265 Z" fill="#C4F4CF"/>
  <path d="M890 0 L1280 0 L1280 260 L1010 184 Z" fill="#8BD9A2"/>
  <path d="M710 218 L1010 184 L1280 260 L1280 458 L960 398 Z" fill="#58BA7E"/>
  <path d="M410 265 L710 218 L960 398 L628 512 Z" fill="#76CB91"/>
  <path d="M0 392 L410 265 L628 512 L308 720 L0 720 Z" fill="#4FAF78"/>
  <path d="M628 512 L960 398 L1280 458 L1280 720 L810 720 Z" fill="#2F9462"/>
  <path d="M308 720 L628 512 L810 720 Z" fill="#6BC58A"/>
  <path d="M0 0 L210 0 L0 138 Z" fill="#D2F9D9" opacity="0.45"/>
  <path d="M1040 0 L1280 0 L1280 112 Z" fill="#B8EFC5" opacity="0.5"/>
  <path d="M0 585 L180 510 L335 720 L0 720 Z" fill="#287F58" opacity="0.38"/>
  <path d="M1048 487 L1280 400 L1280 720 L945 720 Z" fill="#1F714F" opacity="0.35"/>
  <path d="M245 118 L410 265 L250 326 L112 252 Z" fill="#A7E7B8" opacity="0.54"/>
  <path d="M790 92 L1010 184 L892 270 L710 218 Z" fill="#D5FADB" opacity="0.38"/>
  <path d="M520 360 L628 512 L438 588 L355 458 Z" fill="#3E9C68" opacity="0.36"/>

  <line x1="88" y1="92" x2="592" y2="520" stroke="#FFFFFF" stroke-opacity="0.24" stroke-width="1.5"/>
  <line x1="288" y1="58" x2="1110" y2="602" stroke="#FFFFFF" stroke-opacity="0.16" stroke-width="1"/>
  <line x1="760" y1="38" x2="1178" y2="366" stroke="#FFFFFF" stroke-opacity="0.22" stroke-width="1.2"/>
  <line x1="78" y1="610" x2="540" y2="238" stroke="#FFFFFF" stroke-opacity="0.18" stroke-width="1"/>
  <line x1="842" y1="188" x2="842" y2="548" stroke="#FFFFFF" stroke-opacity="0.45" stroke-width="2" stroke-dasharray="8 10"/>
  <line x1="780" y1="356" x2="1168" y2="356" stroke="#FFFFFF" stroke-opacity="0.22" stroke-width="1.5"/>

  <circle cx="88" cy="92" r="5" fill="#FFFFFF" opacity="0.62"/>
  <circle cx="288" cy="58" r="4" fill="#FFFFFF" opacity="0.48"/>
  <circle cx="760" cy="38" r="5" fill="#FFFFFF" opacity="0.44"/>
  <circle cx="1178" cy="366" r="4" fill="#FFFFFF" opacity="0.5"/>
  <circle cx="540" cy="238" r="4" fill="#FFFFFF" opacity="0.5"/>

  <text x="84" y="296" width="650" font-family="Segoe UI, Microsoft YaHei" font-size="74" font-weight="800" letter-spacing="2" fill="#FFFFFF" filter="url(#titleGlow)">POWERPOINT</text>
  <text x="90" y="344" width="620" font-family="Microsoft YaHei, Segoe UI" font-size="22" font-weight="400" fill="#FFFFFF" opacity="0.96">工作计划 / 汇报总结 / 年中总结 / 述职报告</text>
  <text x="92" y="390" width="520" font-family="Segoe UI, Microsoft YaHei" font-size="16" fill="#ECFFF1" opacity="0.82">Strategic planning template with a prismatic green geometric background.</text>

  <rect x="828" y="154" width="352" height="94" rx="24" fill="url(#glassCard)" filter="url(#softShadow)"/>
  <rect x="828" y="314" width="352" height="94" rx="24" fill="url(#glassCard)" filter="url(#softShadow)"/>
  <rect x="828" y="474" width="352" height="94" rx="24" fill="url(#glassCard)" filter="url(#softShadow)"/>

  <path d="M776 154 L818 178 L818 226 L776 250 L734 226 L734 178 Z" fill="#FFFFFF" filter="url(#softShadow)"/>
  <path d="M776 314 L818 338 L818 386 L776 410 L734 386 L734 338 Z" fill="#FFFFFF" filter="url(#softShadow)"/>
  <path d="M776 474 L818 498 L818 546 L776 570 L734 546 L734 498 Z" fill="#FFFFFF" filter="url(#softShadow)"/>

  <text x="756" y="214" width="42" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="800" fill="#39A66D">01</text>
  <text x="756" y="374" width="42" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="800" fill="#39A66D">02</text>
  <text x="756" y="534" width="42" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="800" fill="#39A66D">03</text>

  <text x="858" y="187" width="286" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#274739">Corporate Profile<tspan x="858" dy="26" font-size="13" font-weight="400" fill="#436858">Build a precise, modern brand story.</tspan></text>
  <text x="858" y="347" width="286" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#274739">Data Reporting<tspan x="858" dy="26" font-size="13" font-weight="400" fill="#436858">Express complexity through clean structure.</tspan></text>
  <text x="858" y="507" width="286" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#274739">Strategy Planning<tspan x="858" dy="26" font-size="13" font-weight="400" fill="#436858">Connect insights, milestones, and action.</tspan></text>
</svg>
```

## Avoid in this skill
- ❌ Using a single flat green rectangle; the design depends on many angular facets with slight value shifts.
- ❌ Applying heavy photographic textures or noise overlays; they reduce the clean, corporate low-poly effect.
- ❌ Putting text directly over the brightest mint facets without a darkened area or card behind it.
- ❌ Using `<pattern>` fills for the polygon mesh; draw each facet as an editable `<path>` instead.
- ❌ Using `<mask>` or clipping non-image elements to create shards; keep facets as direct paths for reliable PowerPoint editing.

## Composition notes
- Keep the left 55–60% as the hero title zone; use large white typography over medium-to-dark green facets.
- Place structured content on the right third using white or near-white geometric cards to counterbalance the busy background.
- Let the facets radiate from a brighter upper-center area toward darker lower/right corners for depth.
- Use small circles, dashed lines, and thin white strokes sparingly as “precision” accents, not as a full grid.