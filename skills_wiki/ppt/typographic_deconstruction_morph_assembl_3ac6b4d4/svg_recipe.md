# SVG Recipe — Typographic Deconstruction & Morph Assembly

## Visual mechanism
Break the title into independently addressable character blocks and synthetic stroke fragments, scatter them on slide 1, then use PowerPoint Morph to snap the same IDs into a precise centered wordmark on slide 2. The static SVG keyframe should look like a premium tech title: deep gradient field, cyan assembly dust, glowing fragments, and bold editable typography.

## SVG primitives needed
- 1× `<rect>` for the full-slide gradient background
- 10–14× `<line>` for faint technical grid lines and assembly vectors
- 9× `<text>` for individually morphable headline characters
- 1× `<text>` for the supporting subtitle with nested `<tspan>` styling
- 18–24× `<rect>` for cyan stroke chips, data bars, and small square particles
- 10–16× `<path>` for angular typography shards, orbit arcs, and decorative tech strokes
- 1× `<radialGradient>` for the deep navy background energy bloom
- 2× `<linearGradient>` for metallic-white type and cyan fragment fills
- 2× `<filter>` using blur/offset for editable glow and soft shadow effects
- Optional 2-slide Morph setup: duplicate this SVG as the final assembled slide; create a first slide with the same element IDs but scattered `transform` values

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <radialGradient id="bgDeepTech" cx="50%" cy="45%" r="72%">
      <stop offset="0%" stop-color="#102D70"/>
      <stop offset="48%" stop-color="#071B4A"/>
      <stop offset="100%" stop-color="#030814"/>
    </radialGradient>

    <linearGradient id="typeWhite" x1="250" y1="300" x2="1030" y2="390">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="55%" stop-color="#DCEBFF"/>
      <stop offset="100%" stop-color="#FFFFFF"/>
    </linearGradient>

    <linearGradient id="cyanShard" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#00F0FF"/>
      <stop offset="55%" stop-color="#00B7FF"/>
      <stop offset="100%" stop-color="#5B7CFF"/>
    </linearGradient>

    <filter id="softShadow" x="-30%" y="-30%" width="160%" height="160%">
      <feOffset dx="0" dy="10" result="off"/>
      <feGaussianBlur in="off" stdDeviation="12" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="cyanGlow" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="5" result="glow"/>
      <feMerge>
        <feMergeNode in="glow"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect id="background" x="0" y="0" width="1280" height="720" fill="url(#bgDeepTech)"/>

  <!-- faint technical grid; keep as simple lines so it stays editable -->
  <line x1="120" y1="0" x2="120" y2="720" stroke="#00DCFF" stroke-width="1" opacity="0.08"/>
  <line x1="280" y1="0" x2="280" y2="720" stroke="#00DCFF" stroke-width="1" opacity="0.06"/>
  <line x1="500" y1="0" x2="500" y2="720" stroke="#00DCFF" stroke-width="1" opacity="0.07"/>
  <line x1="780" y1="0" x2="780" y2="720" stroke="#00DCFF" stroke-width="1" opacity="0.07"/>
  <line x1="1040" y1="0" x2="1040" y2="720" stroke="#00DCFF" stroke-width="1" opacity="0.06"/>
  <line x1="0" y1="150" x2="1280" y2="150" stroke="#00DCFF" stroke-width="1" opacity="0.06"/>
  <line x1="0" y1="360" x2="1280" y2="360" stroke="#00DCFF" stroke-width="1" opacity="0.08"/>
  <line x1="0" y1="570" x2="1280" y2="570" stroke="#00DCFF" stroke-width="1" opacity="0.06"/>

  <!-- assembly orbit arcs and digital field marks -->
  <path id="orbit-01" d="M238 352 C326 245, 452 204, 618 214" fill="none" stroke="#00DCFF" stroke-width="2" opacity="0.28" stroke-dasharray="10 16"/>
  <path id="orbit-02" d="M1040 365 C948 475, 805 514, 638 504" fill="none" stroke="#00DCFF" stroke-width="2" opacity="0.23" stroke-dasharray="8 14"/>
  <path id="orbit-03" d="M340 480 C474 565, 758 566, 930 456" fill="none" stroke="#5B7CFF" stroke-width="1.5" opacity="0.18" stroke-dasharray="4 18"/>

  <!-- final assembled character targets; duplicate these IDs on the scattered slide -->
  <text id="char-00" x="316" y="365" width="76" text-anchor="middle" font-family="Microsoft YaHei, Segoe UI, sans-serif" font-size="66" font-weight="800" fill="url(#typeWhite)" filter="url(#softShadow)">创</text>
  <text id="char-01" x="394" y="365" width="76" text-anchor="middle" font-family="Microsoft YaHei, Segoe UI, sans-serif" font-size="66" font-weight="800" fill="url(#typeWhite)" filter="url(#softShadow)">新</text>
  <text id="char-02" x="472" y="365" width="76" text-anchor="middle" font-family="Microsoft YaHei, Segoe UI, sans-serif" font-size="66" font-weight="800" fill="url(#typeWhite)" filter="url(#softShadow)">不</text>
  <text id="char-03" x="550" y="365" width="76" text-anchor="middle" font-family="Microsoft YaHei, Segoe UI, sans-serif" font-size="66" font-weight="800" fill="url(#typeWhite)" filter="url(#softShadow)">止</text>
  <text id="char-04" x="628" y="365" width="50" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="58" font-weight="700" fill="#00DCFF" filter="url(#cyanGlow)">·</text>
  <text id="char-05" x="706" y="365" width="76" text-anchor="middle" font-family="Microsoft YaHei, Segoe UI, sans-serif" font-size="66" font-weight="800" fill="url(#typeWhite)" filter="url(#softShadow)">未</text>
  <text id="char-06" x="784" y="365" width="76" text-anchor="middle" font-family="Microsoft YaHei, Segoe UI, sans-serif" font-size="66" font-weight="800" fill="url(#typeWhite)" filter="url(#softShadow)">来</text>
  <text id="char-07" x="862" y="365" width="76" text-anchor="middle" font-family="Microsoft YaHei, Segoe UI, sans-serif" font-size="66" font-weight="800" fill="url(#typeWhite)" filter="url(#softShadow)">可</text>
  <text id="char-08" x="940" y="365" width="76" text-anchor="middle" font-family="Microsoft YaHei, Segoe UI, sans-serif" font-size="66" font-weight="800" fill="url(#typeWhite)" filter="url(#softShadow)">期</text>

  <!-- synthetic stroke fragments that feel like detached glyph pieces -->
  <rect id="frag-01" x="300" y="392" width="54" height="5" rx="2.5" fill="url(#cyanShard)" opacity="0.9" filter="url(#cyanGlow)"/>
  <rect id="frag-02" x="386" y="284" width="44" height="4" rx="2" fill="#00DCFF" opacity="0.72" transform="rotate(-16 408 286)"/>
  <rect id="frag-03" x="470" y="414" width="72" height="6" rx="3" fill="#00B7FF" opacity="0.7" transform="rotate(9 506 417)"/>
  <rect id="frag-04" x="555" y="266" width="36" height="5" rx="2.5" fill="url(#cyanShard)" opacity="0.85" transform="rotate(28 573 268)"/>
  <rect id="frag-05" x="672" y="400" width="48" height="5" rx="2.5" fill="#00F0FF" opacity="0.75" transform="rotate(-10 696 402)"/>
  <rect id="frag-06" x="782" y="276" width="62" height="6" rx="3" fill="url(#cyanShard)" opacity="0.82" transform="rotate(12 813 279)"/>
  <rect id="frag-07" x="892" y="400" width="58" height="5" rx="2.5" fill="#00DCFF" opacity="0.75" transform="rotate(-6 921 402)"/>
  <rect id="frag-08" x="346" y="458" width="16" height="16" rx="3" fill="#00DCFF" opacity="0.5"/>
  <rect id="frag-09" x="918" y="241" width="13" height="13" rx="2" fill="#00DCFF" opacity="0.46"/>

  <path id="shard-01" d="M248 314 L286 294 L276 333 Z" fill="url(#cyanShard)" opacity="0.38" filter="url(#cyanGlow)"/>
  <path id="shard-02" d="M424 226 L465 240 L438 255 Z" fill="#00DCFF" opacity="0.32" filter="url(#cyanGlow)"/>
  <path id="shard-03" d="M593 435 L646 424 L626 454 Z" fill="url(#cyanShard)" opacity="0.42" filter="url(#cyanGlow)"/>
  <path id="shard-04" d="M748 250 L790 230 L781 270 Z" fill="#5B7CFF" opacity="0.34" filter="url(#cyanGlow)"/>
  <path id="shard-05" d="M1000 390 L1042 378 L1024 414 Z" fill="url(#cyanShard)" opacity="0.36" filter="url(#cyanGlow)"/>
  <path id="shard-06" d="M1028 288 L1062 305 L1034 323 Z" fill="#00DCFF" opacity="0.24"/>

  <!-- subtle incoming vectors: use plain lines, no marker-end on paths -->
  <line id="vector-01" x1="174" y1="188" x2="286" y2="302" stroke="#00DCFF" stroke-width="1.5" opacity="0.22"/>
  <line id="vector-02" x1="1120" y1="174" x2="946" y2="332" stroke="#00DCFF" stroke-width="1.5" opacity="0.18"/>
  <line id="vector-03" x1="228" y1="610" x2="468" y2="388" stroke="#5B7CFF" stroke-width="1.2" opacity="0.18"/>
  <line id="vector-04" x1="1110" y1="560" x2="822" y2="388" stroke="#5B7CFF" stroke-width="1.2" opacity="0.18"/>

  <text id="subtitle" x="360" y="452" width="560" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="17" letter-spacing="3" fill="#A9DFFF" opacity="0.84">
    <tspan fill="#00DCFF" font-weight="700">MORPH ASSEMBLY</tspan>
    <tspan fill="#A9DFFF"> / FROM CHAOS TO CLARITY</tspan>
  </text>

  <rect id="underline-core" x="405" y="392" width="470" height="2" rx="1" fill="#FFFFFF" opacity="0.18"/>
  <rect id="underline-cyan" x="515" y="392" width="250" height="3" rx="1.5" fill="#00DCFF" opacity="0.7" filter="url(#cyanGlow)"/>
</svg>
```

## Avoid in this skill
- ❌ Do not use `<animate>` or `<animateTransform>`; create two separate slides and let PowerPoint Morph perform the movement.
- ❌ Do not use `<mask>` or clip non-image elements to imitate sliced letters; PowerPoint translation will ignore or fail those cases.
- ❌ Do not rely on a single whole-title `<text>` if you want convincing assembly; each character or fragment needs its own stable ID.
- ❌ Do not use `<textPath>` for orbiting typography; keep all text as standard editable `<text>` with explicit `width`.
- ❌ Do not place `marker-end` on `<path>` assembly vectors; use simple `<line>` elements if arrows or motion guides are needed.

## Composition notes
- Build the effect as a Morph pair: slide 1 uses scattered transforms around the canvas edges; slide 2 uses the clean centered coordinates shown above.
- Keep the central 55–65% of the canvas reserved for the final title so the assembly resolves into a strong executive-keynote lockup.
- Use cyan fragments sparingly around the wordmark; they should feel like digital strokes being magnetized into place, not random confetti.
- Maintain a dark, low-noise background with faint grid lines so the white type and electric-blue fragments carry the visual energy.