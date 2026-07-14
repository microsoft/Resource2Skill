# SVG Recipe — Animated Architecture Flow

## Visual mechanism
A dark-mode architecture diagram is overlaid with a glowing “tracer” and fading ghost positions along a routed connector, creating the impression of motion without relying on SVG animation. The flow path is visually narrated by subtle rails, bright active segments, arrowheads, and a comet-like pulse trail.

## SVG primitives needed
- 1× `<rect>` for the full-slide dark background
- 8× `<line>` for subtle background grid accents
- 6× `<rect>` for architecture component cards
- 6× `<path>` for simple editable service icons inside cards
- 3× `<path>` for static routed connector rails
- 2× `<path>` for highlighted active flow segments
- 5× `<path>` for manual arrowheads at connector endpoints
- 9× `<circle>` for ghost tracer positions and the current glowing tracer
- 1× `<filter id="softShadow">` applied to component cards
- 1× `<filter id="orangeGlow">` applied to highlighted paths and tracer dots
- 3× `<linearGradient>` for background, cards, and active flow strokes
- Multiple `<text>` elements with explicit `width` for title, labels, badges, and annotations

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1280" y2="720">
      <stop offset="0%" stop-color="#070812"/>
      <stop offset="58%" stop-color="#0B1024"/>
      <stop offset="100%" stop-color="#111827"/>
    </linearGradient>
    <linearGradient id="cardGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#172033"/>
      <stop offset="100%" stop-color="#0E1628"/>
    </linearGradient>
    <linearGradient id="flowGrad" x1="100" y1="285" x2="1120" y2="530">
      <stop offset="0%" stop-color="#FFD166"/>
      <stop offset="45%" stop-color="#FF8A00"/>
      <stop offset="100%" stop-color="#FF4D6D"/>
    </linearGradient>
    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="12"/>
      <feGaussianBlur stdDeviation="14"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="orangeGlow" x="-80%" y="-80%" width="260%" height="260%">
      <feGaussianBlur stdDeviation="7" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>

  <line x1="70" y1="150" x2="1210" y2="150" stroke="#26324A" stroke-width="1" opacity="0.35"/>
  <line x1="70" y1="390" x2="1210" y2="390" stroke="#26324A" stroke-width="1" opacity="0.25"/>
  <line x1="70" y1="630" x2="1210" y2="630" stroke="#26324A" stroke-width="1" opacity="0.18"/>
  <line x1="180" y1="120" x2="180" y2="650" stroke="#26324A" stroke-width="1" opacity="0.18"/>
  <line x1="430" y1="120" x2="430" y2="650" stroke="#26324A" stroke-width="1" opacity="0.18"/>
  <line x1="680" y1="120" x2="680" y2="650" stroke="#26324A" stroke-width="1" opacity="0.18"/>
  <line x1="930" y1="120" x2="930" y2="650" stroke="#26324A" stroke-width="1" opacity="0.18"/>
  <line x1="1180" y1="120" x2="1180" y2="650" stroke="#26324A" stroke-width="1" opacity="0.18"/>

  <text x="70" y="68" width="720" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="700" fill="#F8FAFC">Webhook-to-Cloud Delivery Flow</text>
  <text x="72" y="102" width="620" font-family="Segoe UI, Microsoft YaHei" font-size="16" fill="#94A3B8">Static architecture diagram with an editable motion-trail overlay that implies a looping tracer animation.</text>
  <text x="1005" y="72" width="180" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#FFB454">LIVE FLOW PATH</text>
  <rect x="998" y="82" width="142" height="6" rx="3" fill="#334155"/>
  <rect x="998" y="82" width="92" height="6" rx="3" fill="url(#flowGrad)" filter="url(#orangeGlow)"/>

  <path d="M300 285 L370 285 L580 285 L650 285 L860 285 L930 285 L1045 285" fill="none" stroke="#38445C" stroke-width="3" stroke-linecap="round"/>
  <path d="M1045 350 L1045 465" fill="none" stroke="#38445C" stroke-width="3" stroke-linecap="round"/>
  <path d="M860 528 L930 528" fill="none" stroke="#38445C" stroke-width="3" stroke-linecap="round"/>
  <path d="M300 285 L370 285 L580 285 L650 285 L860 285 L930 285 L1045 285" fill="none" stroke="#59667E" stroke-width="1.4" stroke-dasharray="7 8" opacity="0.65"/>
  <path d="M1045 285 L1045 465 L860 528 L930 528" fill="none" stroke="#59667E" stroke-width="1.4" stroke-dasharray="7 8" opacity="0.65"/>

  <path d="M300 285 L370 285 L580 285 L650 285 L860 285 L930 285 L1045 285" fill="none" stroke="url(#flowGrad)" stroke-width="5" stroke-linecap="round" opacity="0.75" filter="url(#orangeGlow)"/>
  <path d="M1045 285 L1045 465 L860 528 L930 528" fill="none" stroke="url(#flowGrad)" stroke-width="5" stroke-linecap="round" opacity="0.55" filter="url(#orangeGlow)"/>

  <path d="M1045 285 L1029 277 L1029 293 Z" fill="#FFB454"/>
  <path d="M1045 465 L1037 449 L1053 449 Z" fill="#FF8A00"/>
  <path d="M930 528 L914 520 L914 536 Z" fill="#FF4D6D"/>

  <circle cx="430" cy="285" r="5" fill="#FFB454" opacity="0.20" filter="url(#orangeGlow)"/>
  <circle cx="555" cy="285" r="6" fill="#FFB454" opacity="0.30" filter="url(#orangeGlow)"/>
  <circle cx="690" cy="285" r="6" fill="#FF9F1C" opacity="0.42" filter="url(#orangeGlow)"/>
  <circle cx="825" cy="285" r="7" fill="#FF8A00" opacity="0.55" filter="url(#orangeGlow)"/>
  <circle cx="970" cy="285" r="8" fill="#FF7A18" opacity="0.72" filter="url(#orangeGlow)"/>
  <circle cx="1045" cy="335" r="9" fill="#FF6B2C" opacity="0.82" filter="url(#orangeGlow)"/>
  <circle cx="1045" cy="398" r="11" fill="#FF8A00" opacity="0.95" filter="url(#orangeGlow)"/>
  <circle cx="1045" cy="398" r="20" fill="#FF8A00" opacity="0.18" filter="url(#orangeGlow)"/>
  <circle cx="1045" cy="398" r="5" fill="#FFF7ED"/>

  <rect x="90" y="220" width="210" height="130" rx="24" fill="url(#cardGrad)" stroke="#334155" stroke-width="1.5" filter="url(#softShadow)"/>
  <path d="M145 266 C145 251 157 239 172 239 C187 239 199 251 199 266 C199 279 190 290 178 293 L178 311 L166 311 L166 293 C154 290 145 279 145 266 Z" fill="none" stroke="#7DD3FC" stroke-width="4"/>
  <path d="M166 310 L155 325 M178 310 L189 325" fill="none" stroke="#7DD3FC" stroke-width="4" stroke-linecap="round"/>
  <text x="125" y="270" width="130" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#E2E8F0">Git Repository</text>
  <text x="125" y="300" width="145" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#94A3B8">Commit + webhook event</text>

  <rect x="370" y="220" width="210" height="130" rx="24" fill="url(#cardGrad)" stroke="#334155" stroke-width="1.5" filter="url(#softShadow)"/>
  <path d="M425 245 L500 245 L520 265 L520 315 L425 315 Z" fill="none" stroke="#A78BFA" stroke-width="4"/>
  <path d="M500 245 L500 265 L520 265" fill="none" stroke="#A78BFA" stroke-width="4"/>
  <path d="M445 282 L472 282 M445 300 L494 300" fill="none" stroke="#A78BFA" stroke-width="4" stroke-linecap="round"/>
  <text x="405" y="270" width="145" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#E2E8F0">Build + Test</text>
  <text x="405" y="300" width="145" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#94A3B8">Package, scan, validate</text>

  <rect x="650" y="220" width="210" height="130" rx="24" fill="url(#cardGrad)" stroke="#334155" stroke-width="1.5" filter="url(#softShadow)"/>
  <path d="M735 242 L790 262 L790 309 C790 326 764 335 762 336 C760 335 735 326 735 309 Z" fill="none" stroke="#34D399" stroke-width="4"/>
  <path d="M748 287 L759 299 L779 273" fill="none" stroke="#34D399" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>
  <text x="685" y="270" width="145" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#E2E8F0">Policy Gate</text>
  <text x="685" y="300" width="145" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#94A3B8">Approve secure release</text>

  <rect x="930" y="220" width="230" height="130" rx="24" fill="url(#cardGrad)" stroke="#FF8A00" stroke-width="2" filter="url(#softShadow)"/>
  <path d="M1000 256 C1018 238 1056 238 1074 256 C1092 274 1092 306 1074 324 C1056 342 1018 342 1000 324 C982 306 982 274 1000 256 Z" fill="none" stroke="#FFB454" stroke-width="4"/>
  <path d="M1037 248 L1037 332 M996 290 L1080 290" fill="none" stroke="#FFB454" stroke-width="4" stroke-linecap="round"/>
  <text x="965" y="270" width="160" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#FFF7ED">Serverless Runtime</text>
  <text x="965" y="300" width="165" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#FDBA74">Deploy function bundle</text>

  <rect x="650" y="465" width="210" height="125" rx="24" fill="url(#cardGrad)" stroke="#334155" stroke-width="1.5" filter="url(#softShadow)"/>
  <path d="M710 494 C710 482 792 482 792 494 L792 548 C792 560 710 560 710 548 Z" fill="none" stroke="#60A5FA" stroke-width="4"/>
  <path d="M710 494 C710 506 792 506 792 494 M710 521 C710 533 792 533 792 521" fill="none" stroke="#60A5FA" stroke-width="4"/>
  <text x="685" y="515" width="145" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#E2E8F0">Object Store</text>
  <text x="685" y="545" width="145" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#94A3B8">Artifacts and metadata</text>

  <rect x="930" y="465" width="230" height="125" rx="24" fill="url(#cardGrad)" stroke="#334155" stroke-width="1.5" filter="url(#softShadow)"/>
  <path d="M995 540 L1015 515 L1038 528 L1064 494 L1095 548" fill="none" stroke="#F472B6" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M990 552 L1105 552" fill="none" stroke="#F472B6" stroke-width="4" stroke-linecap="round"/>
  <text x="965" y="515" width="160" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#E2E8F0">Observability</text>
  <text x="965" y="545" width="165" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#94A3B8">Logs, traces, metrics</text>

  <rect x="76" y="610" width="360" height="54" rx="18" fill="#0F172A" stroke="#334155" stroke-width="1"/>
  <text x="100" y="635" width="310" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#CBD5E1">Design trick: each faded dot is a different animation frame, stacked into one editable static slide.</text>
</svg>
```

## Avoid in this skill
- ❌ Do not use `<animate>` or `<animateTransform>` for the moving tracer; these hard-fail translation.
- ❌ Do not use `marker-end` on `<path>` connectors; draw arrowheads manually with small editable `<path>` triangles.
- ❌ Do not apply filters to `<line>` elements; use filters on `<path>` highlights or `<circle>` tracers instead.
- ❌ Do not use `<textPath>` to label routes; place ordinary `<text width="...">` near the path.
- ❌ Do not rely on true looping playback inside the SVG; create a motion illusion with ghosted tracer positions, or export a separate GIF if true animation is required.

## Composition notes
- Keep the architecture cards arranged in a clear left-to-right process flow, with any secondary destination cards placed below the main route.
- Reserve the highest-contrast color only for the active route and tracer dots; all other rails should be low-contrast blue-gray.
- Use a dark, spacious background so glows and dashed guide paths feel premium rather than cluttered.
- The “current” tracer should sit near the most important system handoff, with progressively faded dots behind it to imply direction and speed.