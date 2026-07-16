# SVG Recipe — 3D Isometric Progression Cylinders

## Visual mechanism
A diagonal sequence of stacked isometric cylinders grows from lower-left to upper-right, with each cylinder height increasing to communicate progression. Floating colored halo ellipses, soft shadows, and top icons create the illusion of premium 3D PowerPoint geometry while staying fully editable as SVG shapes.

## SVG primitives needed
- 1× `<rect>` for the soft blue slide background.
- 6× subtle decorative `<path>` / `<line>` elements for diagonal isometric guide accents and movement rhythm.
- 5× blurred `<ellipse>` shadows beneath the cylinders.
- 5× white/blue-gradient `<path>` bodies for the cylinder side walls.
- 5× darker front-lip `<path>` curves to make the extrusion read as cylindrical.
- 5× top `<ellipse>` shapes for the visible top faces.
- 5× colored halo `<ellipse>` rings floating above each cylinder.
- 5× small colored `<circle>` icon plates placed on top of the cylinders.
- 5× simple icon/number `<text>` labels centered on the top plates.
- 5× milestone caption `<text>` blocks with explicit `width`.
- 3× `<linearGradient>` definitions for background and cylinder shading.
- 1× `<filter id="softShadow">` using `feOffset + feGaussianBlur + feMerge` for cylinder shadows.
- 1× `<filter id="haloGlow">` using `feGaussianBlur` for glowing colored rings.

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#eef6ff"/>
      <stop offset="58%" stop-color="#dfeaf6"/>
      <stop offset="100%" stop-color="#cfddea"/>
    </linearGradient>
    <linearGradient id="bodyGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#ffffff"/>
      <stop offset="55%" stop-color="#f4f8fc"/>
      <stop offset="100%" stop-color="#d5e1ec"/>
    </linearGradient>
    <linearGradient id="topGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#ffffff"/>
      <stop offset="100%" stop-color="#edf4fb"/>
    </linearGradient>
    <filter id="softShadow" x="-30%" y="-30%" width="160%" height="170%">
      <feOffset dx="0" dy="12"/>
      <feGaussianBlur stdDeviation="12"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="haloGlow" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="5"/>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>

  <path d="M60 620 L1120 190" fill="none" stroke="#ffffff" stroke-width="2" opacity="0.55" stroke-dasharray="10 18"/>
  <path d="M170 660 L1230 230" fill="none" stroke="#b9c9d9" stroke-width="1.5" opacity="0.35" stroke-dasharray="6 14"/>
  <line x1="118" y1="552" x2="1030" y2="182" stroke="#ffffff" stroke-width="5" opacity="0.22"/>
  <path d="M920 85 C1030 105 1115 150 1180 220" fill="none" stroke="#ffffff" stroke-width="18" opacity="0.25"/>
  <path d="M965 92 C1070 122 1142 175 1198 252" fill="none" stroke="#c3d1df" stroke-width="2" opacity="0.35"/>
  <circle cx="1145" cy="134" r="58" fill="#ffffff" opacity="0.22"/>

  <text x="78" y="86" width="520" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="46" font-weight="700" fill="#243447">Growth Progression</text>
  <text x="82" y="126" width="500" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="17" fill="#5f7184">Five rising isometric cylinders turn a simple sequence into a premium executive milestone model.</text>

  <line x1="236" y1="532" x2="423" y2="455" stroke="#8fa1b2" stroke-width="2" opacity="0.45" stroke-dasharray="7 9"/>
  <line x1="434" y1="453" x2="621" y2="376" stroke="#8fa1b2" stroke-width="2" opacity="0.45" stroke-dasharray="7 9"/>
  <line x1="632" y1="374" x2="819" y2="297" stroke="#8fa1b2" stroke-width="2" opacity="0.45" stroke-dasharray="7 9"/>
  <line x1="830" y1="295" x2="1017" y2="218" stroke="#8fa1b2" stroke-width="2" opacity="0.45" stroke-dasharray="7 9"/>

  <!-- Step 1 -->
  <ellipse cx="196" cy="600" rx="86" ry="28" fill="#74869a" opacity="0.22" filter="url(#softShadow)"/>
  <path d="M126 515 C126 489 266 489 266 515 L266 558 C266 584 126 584 126 558 Z" fill="url(#bodyGrad)" stroke="#c9d6e3" stroke-width="1"/>
  <path d="M126 558 C126 584 266 584 266 558" fill="none" stroke="#bac9d8" stroke-width="3" opacity="0.75"/>
  <ellipse cx="196" cy="515" rx="70" ry="26" fill="url(#topGrad)" stroke="#ffffff" stroke-width="3"/>
  <ellipse cx="196" cy="486" rx="87" ry="31" fill="none" stroke="#ff5050" stroke-width="7" opacity="0.36" filter="url(#haloGlow)"/>
  <ellipse cx="196" cy="486" rx="87" ry="31" fill="none" stroke="#ff5050" stroke-width="3"/>
  <circle cx="196" cy="511" r="25" fill="#ff5050"/>
  <text x="181" y="522" width="30" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="26" font-weight="700" fill="#ffffff">1</text>
  <text x="126" y="644" width="150" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="18" font-weight="700" fill="#2b3b4d">Launch</text>

  <!-- Step 2 -->
  <ellipse cx="394" cy="527" rx="88" ry="29" fill="#74869a" opacity="0.22" filter="url(#softShadow)"/>
  <path d="M324 420 C324 394 464 394 464 420 L464 492 C464 518 324 518 324 492 Z" fill="url(#bodyGrad)" stroke="#c9d6e3" stroke-width="1"/>
  <path d="M324 492 C324 518 464 518 464 492" fill="none" stroke="#bac9d8" stroke-width="3" opacity="0.75"/>
  <ellipse cx="394" cy="420" rx="70" ry="26" fill="url(#topGrad)" stroke="#ffffff" stroke-width="3"/>
  <ellipse cx="394" cy="391" rx="87" ry="31" fill="none" stroke="#ffaa00" stroke-width="7" opacity="0.34" filter="url(#haloGlow)"/>
  <ellipse cx="394" cy="391" rx="87" ry="31" fill="none" stroke="#ffaa00" stroke-width="3"/>
  <circle cx="394" cy="416" r="25" fill="#ffaa00"/>
  <text x="379" y="427" width="30" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="26" font-weight="700" fill="#ffffff">2</text>
  <text x="324" y="563" width="150" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="18" font-weight="700" fill="#2b3b4d">Adoption</text>

  <!-- Step 3 -->
  <ellipse cx="592" cy="455" rx="90" ry="30" fill="#74869a" opacity="0.22" filter="url(#softShadow)"/>
  <path d="M522 328 C522 302 662 302 662 328 L662 420 C662 446 522 446 522 420 Z" fill="url(#bodyGrad)" stroke="#c9d6e3" stroke-width="1"/>
  <path d="M522 420 C522 446 662 446 662 420" fill="none" stroke="#bac9d8" stroke-width="3" opacity="0.75"/>
  <ellipse cx="592" cy="328" rx="70" ry="26" fill="url(#topGrad)" stroke="#ffffff" stroke-width="3"/>
  <ellipse cx="592" cy="299" rx="87" ry="31" fill="none" stroke="#1ec896" stroke-width="7" opacity="0.34" filter="url(#haloGlow)"/>
  <ellipse cx="592" cy="299" rx="87" ry="31" fill="none" stroke="#1ec896" stroke-width="3"/>
  <circle cx="592" cy="324" r="25" fill="#1ec896"/>
  <text x="577" y="335" width="30" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="26" font-weight="700" fill="#ffffff">3</text>
  <text x="522" y="490" width="150" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="18" font-weight="700" fill="#2b3b4d">Scale</text>

  <!-- Step 4 -->
  <ellipse cx="790" cy="382" rx="92" ry="31" fill="#74869a" opacity="0.22" filter="url(#softShadow)"/>
  <path d="M720 229 C720 203 860 203 860 229 L860 347 C860 373 720 373 720 347 Z" fill="url(#bodyGrad)" stroke="#c9d6e3" stroke-width="1"/>
  <path d="M720 347 C720 373 860 373 860 347" fill="none" stroke="#bac9d8" stroke-width="3" opacity="0.75"/>
  <ellipse cx="790" cy="229" rx="70" ry="26" fill="url(#topGrad)" stroke="#ffffff" stroke-width="3"/>
  <ellipse cx="790" cy="200" rx="87" ry="31" fill="none" stroke="#3296ff" stroke-width="7" opacity="0.34" filter="url(#haloGlow)"/>
  <ellipse cx="790" cy="200" rx="87" ry="31" fill="none" stroke="#3296ff" stroke-width="3"/>
  <circle cx="790" cy="225" r="25" fill="#3296ff"/>
  <text x="775" y="236" width="30" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="26" font-weight="700" fill="#ffffff">4</text>
  <text x="720" y="417" width="150" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="18" font-weight="700" fill="#2b3b4d">Optimize</text>

  <!-- Step 5 -->
  <ellipse cx="988" cy="310" rx="94" ry="32" fill="#74869a" opacity="0.22" filter="url(#softShadow)"/>
  <path d="M918 128 C918 102 1058 102 1058 128 L1058 275 C1058 301 918 301 918 275 Z" fill="url(#bodyGrad)" stroke="#c9d6e3" stroke-width="1"/>
  <path d="M918 275 C918 301 1058 301 1058 275" fill="none" stroke="#bac9d8" stroke-width="3" opacity="0.75"/>
  <ellipse cx="988" cy="128" rx="70" ry="26" fill="url(#topGrad)" stroke="#ffffff" stroke-width="3"/>
  <ellipse cx="988" cy="99" rx="87" ry="31" fill="none" stroke="#9650ff" stroke-width="7" opacity="0.34" filter="url(#haloGlow)"/>
  <ellipse cx="988" cy="99" rx="87" ry="31" fill="none" stroke="#9650ff" stroke-width="3"/>
  <circle cx="988" cy="124" r="25" fill="#9650ff"/>
  <text x="973" y="135" width="30" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="26" font-weight="700" fill="#ffffff">5</text>
  <text x="918" y="344" width="150" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="18" font-weight="700" fill="#2b3b4d">Leadership</text>

  <text x="864" y="616" width="330" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" fill="#66798b">Use cylinder height as the value cue, color as the step identity, and the diagonal path as the progression axis.</text>
</svg>
```

## Avoid in this skill
- ❌ Real PowerPoint 3D XML assumptions inside SVG; approximate the extrusion with editable ellipse/path geometry instead.
- ❌ `<use>` symbols for repeated cylinders; duplicate the actual editable shapes so PPT-Master can translate every part.
- ❌ `marker-end` arrows on paths; use simple lines, dashed connectors, or custom triangle paths if arrowheads are needed.
- ❌ Filters on `<line>` connectors; apply glow/shadow only to ellipses, paths, rectangles, or text.
- ❌ Skew or matrix transforms to fake isometric projection; draw the ellipse/path coordinates directly.

## Composition notes
- Keep the title and explanatory copy in the upper-left; the cylinder sequence should own the diagonal from lower-left to upper-right.
- Increase cylinder height by a consistent visual increment so the growth story is instantly readable.
- Use white cylinder bodies against a cool blue background, then reserve saturated accent colors for halo rings and top icons.
- Leave generous negative space around the tallest cylinder so the final milestone feels aspirational rather than crowded.