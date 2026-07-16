# SVG Recipe — Animated Comic Diorama (Morph Scene)

## Visual mechanism
Build a layered 2.5D comic scene like a tiny theatrical stage: muted full-bleed environment in back, a colorful mid-ground prop, and foreground characters with bold outlines. For the Morph effect, create two slides from the same SVG structure: Slide 1 places character groups off-canvas, Slide 2 moves/rotates them into the scene while keeping all other objects identical.

## SVG primitives needed
- 8× `<rect>` for the full-bleed background, train body, train stripe, windows, awning stripes, counter panels, and signage
- 8× `<line>` for subway tile seams, platform rails, and prop construction lines
- 10× `<circle>` for heads, hands, lights, halftone accents, and comic dots
- 7× `<ellipse>` for floor shadows, face details, and stage spotlight pools
- 18× `<path>` for perspective platform planes, train doors, awning scallops, character hair, torsos, limbs, speech bubble, steam puffs, and decorative comic motion strokes
- 5× `<text>` with explicit `width` for the station sign, kiosk label, speech bubble, and slide annotation
- 2× `<linearGradient>` for subway depth and train metal
- 1× `<radialGradient>` for the stage spotlight glow
- 1× `<filter id="softShadow">` using `feOffset + feGaussianBlur + feMerge`, applied to props and characters
- 1× `<filter id="comicGlow">` using `feGaussianBlur`, applied to the speech bubble and spotlight accents

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="wallDepth" x1="0" y1="0" x2="0" y2="720">
      <stop offset="0" stop-color="#EEF1F4"/>
      <stop offset="0.48" stop-color="#C9D0D7"/>
      <stop offset="1" stop-color="#8F99A6"/>
    </linearGradient>
    <linearGradient id="trainMetal" x1="100" y1="110" x2="1180" y2="450">
      <stop offset="0" stop-color="#F9FAFC"/>
      <stop offset="0.55" stop-color="#D8DEE6"/>
      <stop offset="1" stop-color="#B7C0CB"/>
    </linearGradient>
    <radialGradient id="spotlight" cx="50%" cy="56%" r="55%">
      <stop offset="0" stop-color="#FFF5B8" stop-opacity="0.65"/>
      <stop offset="1" stop-color="#FFF5B8" stop-opacity="0"/>
    </radialGradient>
    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="10" in="SourceAlpha" result="off"/>
      <feGaussianBlur in="off" stdDeviation="8" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="comicGlow" x="-25%" y="-25%" width="150%" height="150%">
      <feGaussianBlur stdDeviation="7"/>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#wallDepth)"/>
  <rect x="0" y="145" width="1280" height="235" fill="#252D3A"/>
  <ellipse cx="640" cy="505" rx="560" ry="210" fill="url(#spotlight)" filter="url(#comicGlow)"/>

  <rect x="94" y="96" width="1092" height="358" rx="24" fill="url(#trainMetal)" stroke="#263447" stroke-width="6" filter="url(#softShadow)"/>
  <rect x="100" y="374" width="1080" height="34" fill="#0969C8"/>
  <path d="M350 112 L350 452 M640 112 L640 452 M930 112 L930 452" stroke="#6E7885" stroke-width="5" fill="none"/>
  <rect x="150" y="190" width="124" height="120" rx="10" fill="#18212B" stroke="#EFF5FF" stroke-width="5"/>
  <rect x="425" y="190" width="124" height="120" rx="10" fill="#18212B" stroke="#EFF5FF" stroke-width="5"/>
  <rect x="700" y="190" width="124" height="120" rx="10" fill="#18212B" stroke="#EFF5FF" stroke-width="5"/>
  <rect x="975" y="190" width="124" height="120" rx="10" fill="#18212B" stroke="#EFF5FF" stroke-width="5"/>

  <rect x="58" y="44" width="332" height="62" rx="12" fill="#122239" stroke="#FFFFFF" stroke-width="4"/>
  <circle cx="96" cy="75" r="18" fill="#FFCA3A"/>
  <text x="128" y="84" width="235" font-family="Segoe UI, Microsoft YaHei" font-size="28" font-weight="700" fill="#FFFFFF">MORPH STREET</text>

  <path d="M0 572 C260 540 470 538 640 560 C820 584 1020 580 1280 540 L1280 720 L0 720 Z" fill="#5F6874"/>
  <line x1="0" y1="615" x2="1280" y2="585" stroke="#BBC3CB" stroke-width="4"/>
  <line x1="0" y1="670" x2="1280" y2="636" stroke="#3C444E" stroke-width="5"/>
  <line x1="220" y1="562" x2="170" y2="720" stroke="#7C8793" stroke-width="3"/>
  <line x1="505" y1="558" x2="490" y2="720" stroke="#7C8793" stroke-width="3"/>
  <line x1="790" y1="564" x2="815" y2="720" stroke="#7C8793" stroke-width="3"/>
  <line x1="1060" y1="555" x2="1125" y2="720" stroke="#7C8793" stroke-width="3"/>

  <g id="kiosk" transform="translate(410 270)">
    <ellipse cx="230" cy="385" rx="285" ry="36" fill="#1A1D25" opacity="0.28"/>
    <rect x="52" y="126" width="32" height="290" rx="10" fill="#858C96" stroke="#2F3742" stroke-width="5"/>
    <rect x="392" y="126" width="32" height="290" rx="10" fill="#858C96" stroke="#2F3742" stroke-width="5"/>
    <path d="M18 108 L458 108 L492 205 L-16 205 Z" fill="#FFFFFF" stroke="#2F3742" stroke-width="7" filter="url(#softShadow)"/>
    <rect x="18" y="108" width="70" height="97" fill="#E23232"/>
    <rect x="158" y="108" width="70" height="97" fill="#E23232"/>
    <rect x="298" y="108" width="70" height="97" fill="#E23232"/>
    <path d="M-16 205 C4 236 38 236 58 205 C78 236 112 236 132 205 C152 236 186 236 206 205 C226 236 260 236 280 205 C300 236 334 236 354 205 C374 236 408 236 428 205 C448 236 482 236 492 205 Z" fill="#FFF4E6" stroke="#2F3742" stroke-width="6"/>
    <rect x="20" y="245" width="456" height="158" rx="12" fill="#B47445" stroke="#2F3742" stroke-width="7"/>
    <rect x="54" y="275" width="388" height="92" rx="10" fill="#8E5736"/>
    <text x="108" y="334" width="280" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="800" fill="#FFE7A8">BAD NEWS TACOS</text>
  </g>

  <path d="M820 118 C900 75 1010 90 1032 156 C1056 228 956 250 895 224 L845 255 L858 211 C800 190 778 151 820 118 Z" fill="#FFFFFF" stroke="#202938" stroke-width="6" filter="url(#softShadow)"/>
  <text x="846" y="158" width="160" font-family="Segoe UI, Microsoft YaHei" font-size="24" font-weight="800" fill="#202938">Revenue dipped...</text>
  <text x="858" y="190" width="145" font-family="Segoe UI, Microsoft YaHei" font-size="21" fill="#E23232">but the story lands.</text>

  <g id="character_left_final" transform="translate(252 276) rotate(-3 92 190)">
    <ellipse cx="92" cy="397" rx="74" ry="18" fill="#111722" opacity="0.24"/>
    <path d="M66 154 C28 184 26 270 42 328 L75 328 C64 262 66 215 96 184 Z" fill="#FFD8B8" stroke="#202938" stroke-width="6"/>
    <path d="M118 152 C160 178 168 250 154 320 L122 318 C134 252 130 212 100 184 Z" fill="#FFD8B8" stroke="#202938" stroke-width="6"/>
    <path d="M48 134 Q92 92 136 134 L153 292 Q92 330 31 292 Z" fill="#00A896" stroke="#202938" stroke-width="7"/>
    <rect x="58" y="288" width="28" height="104" rx="10" fill="#293241" stroke="#202938" stroke-width="6"/>
    <rect x="103" y="288" width="28" height="104" rx="10" fill="#293241" stroke="#202938" stroke-width="6"/>
    <circle cx="92" cy="74" r="48" fill="#FFD8B8" stroke="#202938" stroke-width="7"/>
    <path d="M46 70 C55 18 115 8 142 48 C114 42 91 57 76 86 C65 78 56 73 46 70 Z" fill="#2B1B16" stroke="#202938" stroke-width="5"/>
    <ellipse cx="74" cy="78" rx="5" ry="7" fill="#202938"/>
    <ellipse cx="108" cy="78" rx="5" ry="7" fill="#202938"/>
    <path d="M76 102 Q92 116 111 102" fill="none" stroke="#202938" stroke-width="5"/>
  </g>

  <g id="character_right_final" transform="translate(845 288) rotate(4 92 190)">
    <ellipse cx="92" cy="385" rx="70" ry="17" fill="#111722" opacity="0.24"/>
    <path d="M52 152 C28 195 34 242 67 270" fill="none" stroke="#FFD8B8" stroke-width="24" stroke-linecap="round"/>
    <path d="M132 150 C170 182 174 230 145 268" fill="none" stroke="#FFD8B8" stroke-width="24" stroke-linecap="round"/>
    <path d="M44 130 Q92 98 142 130 L158 280 Q92 315 28 280 Z" fill="#FF9F1C" stroke="#202938" stroke-width="7"/>
    <rect x="58" y="275" width="29" height="108" rx="10" fill="#202938" stroke="#202938" stroke-width="6"/>
    <rect x="104" y="275" width="29" height="108" rx="10" fill="#202938" stroke="#202938" stroke-width="6"/>
    <circle cx="92" cy="70" r="47" fill="#FFD8B8" stroke="#202938" stroke-width="7"/>
    <path d="M48 58 C58 18 111 5 138 39 C130 72 91 78 48 58 Z" fill="#56351E" stroke="#202938" stroke-width="5"/>
    <ellipse cx="75" cy="75" rx="5" ry="7" fill="#202938"/>
    <ellipse cx="109" cy="75" rx="5" ry="7" fill="#202938"/>
    <path d="M76 101 Q92 91 110 101" fill="none" stroke="#202938" stroke-width="5"/>
  </g>

  <path d="M220 360 C190 350 166 332 150 305" fill="none" stroke="#FFFFFF" stroke-width="8" stroke-linecap="round"/>
  <path d="M1020 362 C1050 348 1075 326 1090 296" fill="none" stroke="#FFFFFF" stroke-width="8" stroke-linecap="round"/>
  <circle cx="1120" cy="150" r="8" fill="#FFCA3A"/>
  <circle cx="1148" cy="176" r="5" fill="#FFCA3A"/>
  <circle cx="1110" cy="198" r="4" fill="#FFCA3A"/>
  <text x="56" y="690" width="520" font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="600" fill="#FFFFFF" opacity="0.82">Morph setup: duplicate this slide; move character groups off-canvas on slide 1, keep ids and layering unchanged.</text>
</svg>
```

## Avoid in this skill
- ❌ SVG `<animate>` or `<animateTransform>` for the walking entrance; use PowerPoint Morph between two static SVG-derived slides instead.
- ❌ Replacing the whole scene with one flattened PNG; it kills editability and prevents clean Morph matching.
- ❌ `marker-end` arrows for motion cues; use curved `<path>` strokes or small comic burst shapes instead.
- ❌ Applying filters to `<line>` elements for motion streaks; use plain strokes or convert streaks to `<path>`.
- ❌ Changing object count or grouping between the two Morph states; Morph works best when characters keep the same editable parts and only transform position/rotation/scale.

## Composition notes
- Treat the slide like a stage: environment fills the canvas, the kiosk anchors the bottom-center, and characters occupy the foreground left/right thirds.
- Keep the background muted blue-gray so the red-white awning and bright shirts become the narrative focal points.
- For Morph, Slide 1 should place `character_left_final` at about `translate(-220 276)` and `character_right_final` at about `translate(1320 288)`; Slide 2 uses the final positions shown.
- Add tiny speech bubbles, speed arcs, and halftone dots sparingly so the scene feels comic-like without obscuring the main prop.