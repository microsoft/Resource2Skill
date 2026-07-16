# SVG Recipe — Cinematic Narrative Staging & Morph Choreography

## Visual mechanism
Create a “camera viewport into a larger world”: a sweeping diagonal landscape with actors staged partly off-canvas, ghosted future positions, and a visible travel path. For PowerPoint motion, duplicate the slide as sequential keyframes, keep object identities/order consistent, and change only actor coordinates/rotations so Morph choreographs the journey.

## SVG primitives needed
- 1× `<rect>` for the full-slide cinematic sky background
- 3× `<radialGradient>/<linearGradient>` for sky, sun, terrain, and actor depth
- 2× `<filter>` for soft object shadows and sun glow
- 1× `<circle>` for the glowing sun
- 4× `<ellipse>` for layered clouds and atmospheric staging
- 4× `<path>` for rolling hills, foreground terrain, ridge highlights, and decorative grass
- 1× `<path>` with `stroke-dasharray` for the visible motion trajectory
- 5× `<path>` arrowhead/impact accent shapes, drawn manually instead of using markers
- 6× `<rect>` for actor bodies, pail, storyboard keyframe cards, and title plate
- 4× `<circle>` for actor heads / simplified character details
- 5× `<line>` for pail handle, actor limbs, and cinematic guide ticks
- 6× `<text>` with explicit `width` for title, scene labels, and keyframe captions
- Several grouped shapes with `transform="translate(...) rotate(...)"` to show staged motion positions

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="skyGrad" x1="0" y1="0" x2="0" y2="720">
      <stop offset="0%" stop-color="#7fd7ff"/>
      <stop offset="58%" stop-color="#b8ecff"/>
      <stop offset="100%" stop-color="#f6fbff"/>
    </linearGradient>
    <radialGradient id="sunGrad" cx="50%" cy="50%" r="60%">
      <stop offset="0%" stop-color="#fff8a8"/>
      <stop offset="55%" stop-color="#ffd700"/>
      <stop offset="100%" stop-color="#ff9f1c"/>
    </radialGradient>
    <linearGradient id="hillGrad" x1="0" y1="260" x2="1280" y2="720">
      <stop offset="0%" stop-color="#2fb344"/>
      <stop offset="48%" stop-color="#188038"/>
      <stop offset="100%" stop-color="#0b5d2a"/>
    </linearGradient>
    <linearGradient id="frontHillGrad" x1="0" y1="500" x2="1280" y2="720">
      <stop offset="0%" stop-color="#17692f"/>
      <stop offset="100%" stop-color="#073d1c"/>
    </linearGradient>
    <linearGradient id="navyActor" x1="0" y1="0" x2="0" y2="120">
      <stop offset="0%" stop-color="#2737d8"/>
      <stop offset="100%" stop-color="#000080"/>
    </linearGradient>
    <linearGradient id="magentaActor" x1="0" y1="0" x2="0" y2="120">
      <stop offset="0%" stop-color="#ff68bd"/>
      <stop offset="100%" stop-color="#ff1493"/>
    </linearGradient>
    <filter id="softShadow" x="-30%" y="-30%" width="160%" height="180%">
      <feOffset dx="0" dy="10"/>
      <feGaussianBlur stdDeviation="10"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="sunGlow" x="-80%" y="-80%" width="260%" height="260%">
      <feGaussianBlur stdDeviation="18"/>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#skyGrad)"/>

  <circle cx="1075" cy="110" r="82" fill="#ffd700" opacity="0.28" filter="url(#sunGlow)"/>
  <circle cx="1075" cy="110" r="56" fill="url(#sunGrad)"/>

  <ellipse cx="168" cy="118" rx="86" ry="24" fill="#ffffff" opacity="0.72"/>
  <ellipse cx="225" cy="105" rx="60" ry="20" fill="#ffffff" opacity="0.58"/>
  <ellipse cx="850" cy="170" rx="105" ry="28" fill="#ffffff" opacity="0.48"/>
  <ellipse cx="925" cy="154" rx="70" ry="20" fill="#ffffff" opacity="0.38"/>

  <rect x="56" y="54" width="470" height="110" rx="28" fill="#06224a" opacity="0.84" filter="url(#softShadow)"/>
  <text x="88" y="98" width="410" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="700" fill="#ffffff">
    Cinematic journey
  </text>
  <text x="90" y="133" width="420" font-family="Segoe UI, Microsoft YaHei" font-size="17" fill="#b8ecff">
    Stage actors off-screen, then Morph them along the hill.
  </text>

  <path d="M-160,530 C120,485 275,500 430,445 C610,380 720,268 885,250 C1040,232 1145,322 1440,286 L1440,760 L-160,760 Z"
        fill="url(#hillGrad)" filter="url(#softShadow)"/>
  <path d="M-140,612 C120,568 330,604 520,552 C720,496 900,540 1080,482 C1190,445 1295,455 1440,430 L1440,760 L-140,760 Z"
        fill="url(#frontHillGrad)" opacity="0.92"/>
  <path d="M-50,528 C164,500 312,498 468,430 C638,356 732,274 888,250 C1038,228 1142,318 1320,285"
        fill="none" stroke="#a7f36b" stroke-width="9" stroke-linecap="round" opacity="0.72"/>

  <path d="M-100,512 C150,500 322,485 478,422 C640,357 742,284 884,264 C1018,246 1137,308 1320,292"
        fill="none" stroke="#fff7a8" stroke-width="4" stroke-dasharray="14 16" stroke-linecap="round" opacity="0.92"/>
  <path d="M1155,294 L1190,282 L1164,320 Z" fill="#fff7a8" opacity="0.95"/>

  <g transform="translate(-70 446) rotate(-8)" opacity="0.38">
    <circle cx="24" cy="-32" r="20" fill="#0b155f"/>
    <rect x="0" y="-16" width="50" height="86" rx="16" fill="url(#navyActor)"/>
    <line x1="8" y1="70" x2="-10" y2="108" stroke="#0b155f" stroke-width="8" stroke-linecap="round"/>
    <line x1="42" y1="70" x2="70" y2="104" stroke="#0b155f" stroke-width="8" stroke-linecap="round"/>
  </g>

  <g transform="translate(320 422) rotate(4)" filter="url(#softShadow)">
    <circle cx="24" cy="-32" r="20" fill="#09155f"/>
    <rect x="0" y="-16" width="50" height="86" rx="16" fill="url(#navyActor)"/>
    <line x1="8" y1="70" x2="-6" y2="110" stroke="#09155f" stroke-width="8" stroke-linecap="round"/>
    <line x1="42" y1="70" x2="66" y2="108" stroke="#09155f" stroke-width="8" stroke-linecap="round"/>
  </g>

  <g transform="translate(520 366) rotate(-10)" opacity="0.68">
    <circle cx="24" cy="-32" r="20" fill="#9b075d"/>
    <rect x="0" y="-16" width="50" height="86" rx="16" fill="url(#magentaActor)"/>
    <line x1="8" y1="70" x2="-12" y2="106" stroke="#9b075d" stroke-width="8" stroke-linecap="round"/>
    <line x1="42" y1="70" x2="68" y2="104" stroke="#9b075d" stroke-width="8" stroke-linecap="round"/>
  </g>

  <g transform="translate(790 240) rotate(16)" filter="url(#softShadow)">
    <circle cx="24" cy="-32" r="20" fill="#9b075d"/>
    <rect x="0" y="-16" width="50" height="86" rx="16" fill="url(#magentaActor)"/>
    <line x1="8" y1="70" x2="-14" y2="103" stroke="#9b075d" stroke-width="8" stroke-linecap="round"/>
    <line x1="42" y1="70" x2="70" y2="102" stroke="#9b075d" stroke-width="8" stroke-linecap="round"/>
  </g>

  <g transform="translate(855 178)" filter="url(#softShadow)">
    <rect x="0" y="38" width="78" height="70" rx="14" fill="#c9d1d9" stroke="#697386" stroke-width="3"/>
    <path d="M10,46 C18,5 60,5 68,46" fill="none" stroke="#697386" stroke-width="6" stroke-linecap="round"/>
    <rect x="14" y="55" width="50" height="16" rx="8" fill="#8bd3ff" opacity="0.85"/>
    <text x="-18" y="137" width="120" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#06224a" text-anchor="middle">goal</text>
  </g>

  <path d="M890,355 C930,395 970,430 1030,468" fill="none" stroke="#ffffff" stroke-width="3" stroke-dasharray="5 12" opacity="0.62"/>
  <path d="M1030,468 L1006,462 L1022,445 Z" fill="#ffffff" opacity="0.62"/>

  <g transform="translate(72 638)">
    <rect x="0" y="0" width="118" height="44" rx="14" fill="#ffffff" opacity="0.82"/>
    <text x="18" y="28" width="90" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#06224a">01 stage</text>
  </g>
  <g transform="translate(206 638)">
    <rect x="0" y="0" width="118" height="44" rx="14" fill="#ffffff" opacity="0.82"/>
    <text x="18" y="28" width="90" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#06224a">02 climb</text>
  </g>
  <g transform="translate(340 638)">
    <rect x="0" y="0" width="118" height="44" rx="14" fill="#ffffff" opacity="0.82"/>
    <text x="18" y="28" width="90" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#06224a">03 crest</text>
  </g>
  <g transform="translate(474 638)">
    <rect x="0" y="0" width="118" height="44" rx="14" fill="#ffffff" opacity="0.82"/>
    <text x="18" y="28" width="90" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#06224a">04 fall</text>
  </g>

  <text x="1015" y="650" width="210" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="600" fill="#ffffff" opacity="0.9">
    Duplicate as keyframes → Morph by object
  </text>
</svg>
```

## Avoid in this skill
- ❌ SVG `<animate>` or `<animateTransform>`; PowerPoint Morph should create the motion between separate slides instead.
- ❌ `<path marker-end="...">` for arrows; draw arrowheads manually as small triangle paths, or use `marker-end` only on individual `<line>` elements if absolutely needed.
- ❌ Changing object order, IDs, shape type, or group structure between keyframe slides; Morph needs stable matching.
- ❌ Masking or clipping non-image shapes to fake camera reveals; use off-canvas placement and slide-to-slide Morph staging instead.
- ❌ Overloading the slide with text; the narrative should be carried by motion, landscape, and actor state changes.

## Composition notes
- Treat the 1280×720 slide as a camera viewport inside a wider world; allow actors and terrain to extend beyond the left/right edges for dramatic entrances and exits.
- Use a strong diagonal hill from lower-left to upper-right as the primary eye path; place goals, obstacles, or reveals near the crest.
- Keep text minimal: a title plate in the opening keyframe, then small keyframe labels or no text at all in later slides.
- For Morph slides, preserve the environment exactly and move/rotate only the actors, props, and emphasis marks to create cinematic continuity.