# SVG Recipe — Origami Folded Ribbon Agenda

## Visual mechanism
A stacked agenda is transformed into a set of interlocking folded tags: each row combines a neutral gray chevron “fold” behind a saturated left-pointing color tip and a long banner body. The 3D/origami illusion comes from precise polygon adjacency, darker fold facets, and slight tonal gradients rather than true 3D effects.

## SVG primitives needed
- 1× `<rect>` for the clean slide background
- 1× `<line>` for the left-column editorial divider
- 4× neutral `<path>` chevrons for the gray folded anchor tabs
- 4× darker `<path>` fold facets to imply overlap/shadow inside the chevrons
- 4× colored `<path>` triangles for the left arrow tips
- 4× colored `<path>` banner bodies with squared left edge and rounded right corners
- 4× `<circle>` number medallions for visual hierarchy inside each banner
- 13× `<text>` elements for eyebrow label, title, subtitle, row numbers, row titles, and descriptions
- 5× `<linearGradient>` definitions for subtle depth on gray fold and colored banners
- 1× `<filter id="softShadow">` applied to banner/fold paths for premium separation from the white background

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="foldGrad" x1="380" y1="0" x2="500" y2="0" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#ECEEF3"/>
      <stop offset="0.55" stop-color="#D2D2D7"/>
      <stop offset="1" stop-color="#BFC1C8"/>
    </linearGradient>
    <linearGradient id="blueGrad" x1="470" y1="0" x2="1165" y2="0" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#4969AF"/>
      <stop offset="1" stop-color="#2F497E"/>
    </linearGradient>
    <linearGradient id="maroonGrad" x1="470" y1="0" x2="1165" y2="0" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#BD3349"/>
      <stop offset="1" stop-color="#861C2E"/>
    </linearGradient>
    <linearGradient id="greenGrad" x1="470" y1="0" x2="1165" y2="0" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#3FA36E"/>
      <stop offset="1" stop-color="#236D43"/>
    </linearGradient>
    <linearGradient id="purpleGrad" x1="470" y1="0" x2="1165" y2="0" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#7D49B6"/>
      <stop offset="1" stop-color="#4E257F"/>
    </linearGradient>
    <filter id="softShadow" x="-10%" y="-20%" width="130%" height="150%">
      <feOffset dx="0" dy="6" in="SourceAlpha" result="off"/>
      <feGaussianBlur stdDeviation="7" in="off" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#FCFCFE"/>

  <line x1="355" y1="146" x2="355" y2="574" stroke="#DADDE5" stroke-width="2"/>
  <text x="72" y="172" width="250" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" letter-spacing="3" fill="#87909C">EXECUTIVE BRIEF</text>
  <text x="70" y="260" width="290" font-family="Segoe UI, Microsoft YaHei" font-size="52" font-weight="800" fill="#263445">AGENDA</text>
  <text x="72" y="304" width="270" font-family="Segoe UI, Microsoft YaHei" font-size="52" font-weight="800" fill="#263445">SLIDE</text>
  <text x="74" y="370" width="260" font-family="Segoe UI, Microsoft YaHei" font-size="18" fill="#7C8792">
    <tspan x="74" dy="0">Four focused sections</tspan>
    <tspan x="74" dy="28">for a concise strategic</tspan>
    <tspan x="74" dy="28">conversation.</tspan>
  </text>

  <!-- Row 01 -->
  <path d="M382 102 L474 102 L432 145 L474 188 L382 188 L424 145 Z" fill="url(#foldGrad)" filter="url(#softShadow)"/>
  <path d="M424 145 L474 102 L458 145 L474 188 Z" fill="#AEB1BB" opacity="0.55"/>
  <path d="M470 102 L470 188 L430 145 Z" fill="#3B5998"/>
  <path d="M470 102 H1128 Q1162 102 1162 136 V154 Q1162 188 1128 188 H470 Z" fill="url(#blueGrad)" filter="url(#softShadow)"/>
  <circle cx="528" cy="145" r="30" fill="#FFFFFF" opacity="0.18"/>
  <text x="505" y="158" width="52" font-family="Segoe UI, Microsoft YaHei" font-size="31" font-weight="800" fill="#FFFFFF">01</text>
  <text x="588" y="135" width="490" font-family="Segoe UI, Microsoft YaHei" font-size="24" font-weight="700" fill="#FFFFFF">Align on the decision context</text>
  <text x="590" y="166" width="500" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#E7ECF8">Frame objectives, constraints, and the choices this meeting must resolve.</text>

  <!-- Row 02 -->
  <path d="M382 232 L474 232 L432 275 L474 318 L382 318 L424 275 Z" fill="url(#foldGrad)" filter="url(#softShadow)"/>
  <path d="M424 275 L474 232 L458 275 L474 318 Z" fill="#AEB1BB" opacity="0.55"/>
  <path d="M470 232 L470 318 L430 275 Z" fill="#A62639"/>
  <path d="M470 232 H1128 Q1162 232 1162 266 V284 Q1162 318 1128 318 H470 Z" fill="url(#maroonGrad)" filter="url(#softShadow)"/>
  <circle cx="528" cy="275" r="30" fill="#FFFFFF" opacity="0.18"/>
  <text x="505" y="288" width="52" font-family="Segoe UI, Microsoft YaHei" font-size="31" font-weight="800" fill="#FFFFFF">02</text>
  <text x="588" y="265" width="490" font-family="Segoe UI, Microsoft YaHei" font-size="24" font-weight="700" fill="#FFFFFF">Review the evidence base</text>
  <text x="590" y="296" width="500" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#F7E5E8">Highlight the data, market signals, and operating facts that matter most.</text>

  <!-- Row 03 -->
  <path d="M382 362 L474 362 L432 405 L474 448 L382 448 L424 405 Z" fill="url(#foldGrad)" filter="url(#softShadow)"/>
  <path d="M424 405 L474 362 L458 405 L474 448 Z" fill="#AEB1BB" opacity="0.55"/>
  <path d="M470 362 L470 448 L430 405 Z" fill="#2E8B57"/>
  <path d="M470 362 H1128 Q1162 362 1162 396 V414 Q1162 448 1128 448 H470 Z" fill="url(#greenGrad)" filter="url(#softShadow)"/>
  <circle cx="528" cy="405" r="30" fill="#FFFFFF" opacity="0.18"/>
  <text x="505" y="418" width="52" font-family="Segoe UI, Microsoft YaHei" font-size="31" font-weight="800" fill="#FFFFFF">03</text>
  <text x="588" y="395" width="490" font-family="Segoe UI, Microsoft YaHei" font-size="24" font-weight="700" fill="#FFFFFF">Explore strategic options</text>
  <text x="590" y="426" width="500" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#E4F4EB">Compare viable paths, trade-offs, risks, and execution implications.</text>

  <!-- Row 04 -->
  <path d="M382 492 L474 492 L432 535 L474 578 L382 578 L424 535 Z" fill="url(#foldGrad)" filter="url(#softShadow)"/>
  <path d="M424 535 L474 492 L458 535 L474 578 Z" fill="#AEB1BB" opacity="0.55"/>
  <path d="M470 492 L470 578 L430 535 Z" fill="#663399"/>
  <path d="M470 492 H1128 Q1162 492 1162 526 V544 Q1162 578 1128 578 H470 Z" fill="url(#purpleGrad)" filter="url(#softShadow)"/>
  <circle cx="528" cy="535" r="30" fill="#FFFFFF" opacity="0.18"/>
  <text x="505" y="548" width="52" font-family="Segoe UI, Microsoft YaHei" font-size="31" font-weight="800" fill="#FFFFFF">04</text>
  <text x="588" y="525" width="490" font-family="Segoe UI, Microsoft YaHei" font-size="24" font-weight="700" fill="#FFFFFF">Confirm actions and owners</text>
  <text x="590" y="556" width="500" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#EFE6FA">Translate decisions into next steps, accountability, and operating cadence.</text>
</svg>
```

## Avoid in this skill
- ❌ Using a single rounded rectangle for the whole row; it loses the folded-ribbon illusion and creates gaps where the triangle should attach.
- ❌ Applying `clip-path` to the chevron or banner shapes; clipping is only reliably preserved for images, so build the folds directly with `<path>`.
- ❌ Overusing heavy shadows or bevel-like effects; the technique should read as crisp editorial origami, not glossy 3D.
- ❌ Letting the colored triangle and banner body overlap inconsistently; align their shared vertical edge exactly to avoid hairline seams in PowerPoint.

## Composition notes
- Keep the left 30% of the slide mostly open for title, subtitle, or section context; the right 70% carries the stacked agenda.
- Use equal row heights and equal vertical gaps so the folded geometry feels engineered and intentional.
- The gray chevron should be neutral and consistent across rows; let the row colors carry semantic meaning.
- Place numbers near the fold/arrow junction to make each ribbon scan like a premium agenda tab.