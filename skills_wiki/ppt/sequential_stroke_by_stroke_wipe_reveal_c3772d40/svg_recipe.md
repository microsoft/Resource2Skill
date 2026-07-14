# SVG Recipe — Sequential Stroke-by-Stroke Wipe Reveal

## Visual mechanism
Build the headline as separate filled vector “strokes” rather than live text, then sequence those shapes in natural writing order so each can receive an individual PowerPoint Wipe entrance. The static SVG should make every stroke an independent editable shape, with subtle numbering/direction cues that can be removed after animation is assigned.

## SVG primitives needed
- 1× `<rect>` full-canvas background with radial/linear gradient mood lighting.
- 13× filled stroke shapes for the constructed word: `<rect>` for vertical/horizontal strokes and `<path>` for diagonal/curved strokes.
- 1× `<filter id="neonGlow">` applied to the main stroke shapes for a premium luminous reveal look.
- 1× `<filter id="softShadow">` applied to instructional cards and title text.
- 10× `<circle>` timing badges showing stroke sequence numbers.
- 10× `<line>` plus 10× small `<path>` arrowheads indicating wipe direction; use lines and separate triangle paths, not path markers.
- 4× `<text>` blocks with explicit `width` attributes for title, subtitle, labels, and timing guidance.

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <radialGradient id="bgGlow" cx="50%" cy="42%" r="72%">
      <stop offset="0%" stop-color="#22324A"/>
      <stop offset="48%" stop-color="#101827"/>
      <stop offset="100%" stop-color="#070A12"/>
    </radialGradient>
    <linearGradient id="strokeGrad" x1="200" y1="180" x2="1050" y2="520" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#26E6FF"/>
      <stop offset="48%" stop-color="#5B8CFF"/>
      <stop offset="100%" stop-color="#B45CFF"/>
    </linearGradient>
    <linearGradient id="edgeGrad" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.95"/>
      <stop offset="100%" stop-color="#FFFFFF" stop-opacity="0"/>
    </linearGradient>
    <filter id="neonGlow" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="8" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feOffset dx="0" dy="8" result="off"/>
      <feGaussianBlur in="off" stdDeviation="12" result="shadow"/>
      <feMerge>
        <feMergeNode in="shadow"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGlow)"/>
  <circle cx="1060" cy="120" r="150" fill="#2E5BFF" opacity="0.10"/>
  <circle cx="165" cy="590" r="190" fill="#00D7FF" opacity="0.08"/>

  <text x="88" y="84" width="720" font-family="Segoe UI, Microsoft YaHei" font-size="26" fill="#EAF3FF" font-weight="700" filter="url(#softShadow)">Sequential stroke-by-stroke wipe reveal</text>
  <text x="88" y="118" width="660" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#9FB3C8">Each colored shape below is a separate editable PowerPoint stroke. Apply Wipe entrances in badge order.</text>

  <g id="word-WIPE" filter="url(#neonGlow)" fill="url(#strokeGrad)">
    <!-- W: four diagonal strokes -->
    <path id="stroke-01-W-down-left" d="M218 214 L254 214 L305 484 L269 484 Z"/>
    <path id="stroke-02-W-up-inner" d="M300 484 L336 484 L395 214 L359 214 Z"/>
    <path id="stroke-03-W-down-inner" d="M386 214 L422 214 L481 484 L445 484 Z"/>
    <path id="stroke-04-W-up-right" d="M475 484 L511 484 L562 214 L526 214 Z"/>

    <!-- I: top bar, stem, bottom bar -->
    <rect id="stroke-05-I-top" x="600" y="214" width="126" height="38" rx="19"/>
    <rect id="stroke-06-I-stem" x="644" y="252" width="38" height="194" rx="19"/>
    <rect id="stroke-07-I-bottom" x="600" y="446" width="126" height="38" rx="19"/>

    <!-- P: vertical stem, top bar, curved bowl, mid bar -->
    <rect id="stroke-08-P-stem" x="772" y="214" width="40" height="270" rx="20"/>
    <rect id="stroke-09-P-top" x="812" y="214" width="118" height="38" rx="19"/>
    <path id="stroke-10-P-bowl" d="M910 214 C990 214 1028 252 1028 318 C1028 383 990 416 910 416 L858 416 L858 378 L910 378 C963 378 986 358 986 318 C986 276 963 252 910 252 L858 252 L858 214 Z"/>
    <rect id="stroke-11-P-mid" x="812" y="378" width="118" height="38" rx="19"/>

    <!-- E: vertical spine and three crossbars -->
    <rect id="stroke-12-E-spine" x="1062" y="214" width="40" height="270" rx="20"/>
    <rect id="stroke-13-E-top" x="1102" y="214" width="116" height="38" rx="19"/>
    <rect id="stroke-14-E-mid" x="1102" y="331" width="96" height="38" rx="19"/>
    <rect id="stroke-15-E-bottom" x="1102" y="446" width="116" height="38" rx="19"/>
  </g>

  <!-- reveal leading-edge accents: show where wipe fronts would pass during animation -->
  <rect x="218" y="214" width="20" height="270" fill="url(#edgeGrad)" opacity="0.45"/>
  <rect x="600" y="214" width="62" height="38" rx="19" fill="url(#edgeGrad)" opacity="0.42"/>
  <rect x="772" y="214" width="20" height="270" fill="url(#edgeGrad)" opacity="0.36"/>
  <rect x="1062" y="214" width="20" height="270" fill="url(#edgeGrad)" opacity="0.36"/>

  <!-- sequence badges and wipe-direction hints -->
  <g id="sequence-badges" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700">
    <circle cx="210" cy="195" r="15" fill="#FFFFFF"/><text x="205" y="200" width="18" fill="#0A1220">1</text>
    <line x1="225" y1="202" x2="246" y2="315" stroke="#FFFFFF" stroke-width="2"/><path d="M247 319 L239 307 L256 310 Z" fill="#FFFFFF"/>

    <circle cx="346" cy="503" r="15" fill="#FFFFFF"/><text x="341" y="508" width="18" fill="#0A1220">2</text>
    <line x1="350" y1="489" x2="374" y2="372" stroke="#FFFFFF" stroke-width="2"/><path d="M375 368 L380 382 L363 379 Z" fill="#FFFFFF"/>

    <circle cx="620" cy="195" r="15" fill="#FFFFFF"/><text x="615" y="200" width="18" fill="#0A1220">5</text>
    <line x1="637" y1="233" x2="695" y2="233" stroke="#FFFFFF" stroke-width="2"/><path d="M700 233 L688 226 L688 240 Z" fill="#FFFFFF"/>

    <circle cx="746" cy="214" r="15" fill="#FFFFFF"/><text x="741" y="219" width="18" fill="#0A1220">8</text>
    <line x1="792" y1="225" x2="792" y2="338" stroke="#FFFFFF" stroke-width="2"/><path d="M792 343 L784 330 L800 330 Z" fill="#FFFFFF"/>

    <circle cx="914" cy="195" r="15" fill="#FFFFFF"/><text x="905" y="200" width="24" fill="#0A1220">10</text>
    <line x1="930" y1="232" x2="990" y2="292" stroke="#FFFFFF" stroke-width="2"/><path d="M994 296 L980 292 L992 280 Z" fill="#FFFFFF"/>

    <circle cx="1040" cy="214" r="15" fill="#FFFFFF"/><text x="1031" y="219" width="24" fill="#0A1220">12</text>
    <line x1="1082" y1="225" x2="1082" y2="338" stroke="#FFFFFF" stroke-width="2"/><path d="M1082 343 L1074 330 L1090 330 Z" fill="#FFFFFF"/>
  </g>

  <g id="timing-card" filter="url(#softShadow)">
    <rect x="88" y="586" width="1104" height="74" rx="24" fill="#0D1627" opacity="0.92"/>
    <rect x="110" y="609" width="126" height="28" rx="14" fill="#26E6FF" opacity="0.18"/>
    <text x="128" y="629" width="120" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#78F0FF" font-weight="700">Animation map</text>
    <text x="260" y="629" width="840" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#DCEBFF">
      Wipe each stroke individually: diagonals follow their writing angle, vertical stems wipe top→bottom, crossbars wipe left→right, curved bowl wipes clockwise/rightward.
    </text>
  </g>
</svg>
```

## Avoid in this skill
- ❌ Do not use live `<text>` as the main headline if the goal is stroke-by-stroke reveal; text will animate as one object, not as individual strokes.
- ❌ Do not merge all strokes into one compound `<path>`; PowerPoint needs separate editable shapes so each stroke can receive its own Wipe timing.
- ❌ Do not use SVG `<animate>` or `<animateTransform>` to simulate the reveal; they hard-fail and do not become PowerPoint animations.
- ❌ Do not use `<mask>` or clip-paths on the stroke shapes to fake wipes; masks/clips on non-image elements are not reliably translated.
- ❌ Do not put arrowheads on `<path marker-end="...">`; if direction cues are needed, use `<line>` plus separate triangle `<path>` arrowheads.

## Composition notes
- Keep the constructed word centered and large, occupying roughly the middle 40–50% of the slide; the animation needs surrounding negative space to feel intentional.
- Use high-contrast strokes against a dark or very light background; gradients and glow make the final reveal feel premium without changing the animation logic.
- DOM/layer order should match intended animation order: first stroke first, last stroke last. This makes PowerPoint animation assignment easier after translation.
- Remove or hide the sequence badges/arrows in the final keynote version; they are authoring guides, not part of the polished reveal unless presenting the method itself.