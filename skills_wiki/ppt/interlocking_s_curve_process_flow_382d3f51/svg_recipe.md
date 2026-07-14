# SVG Recipe — Interlocking S-Curve Process Flow

## Visual mechanism
A vertical process becomes a flowing S-shaped ribbon by stacking overlapping bi-color donut nodes, each made from alternating solid and translucent semicircles. Text blocks alternate left and right of the spine, turning a linear list into a dynamic, connected infographic.

## SVG primitives needed
- 1× `<rect>` for the soft full-slide background
- 1× `<linearGradient>` for subtle background depth
- 1× `<filter id="softShadow">` applied to node halves and inner circles for premium depth
- 10× `<path>` for the solid/translucent semicircle halves of the five donut nodes
- 5× `<circle>` for white inner donut centers
- 5× `<text>` for large step numbers inside the nodes
- 5× `<line>` for short connector rules from node to text block
- 10× `<text>` for alternating step titles and descriptions
- 2× `<path>` for faint decorative background curves that echo the S-flow

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#F4F5FF"/>
      <stop offset="58%" stop-color="#E8EAF6"/>
      <stop offset="100%" stop-color="#DEE3F5"/>
    </linearGradient>

    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feOffset dx="0" dy="8"/>
      <feGaussianBlur stdDeviation="10"/>
      <feColorMatrix type="matrix" values="0 0 0 0 0.13  0 0 0 0 0.16  0 0 0 0 0.24  0 0 0 .22 0"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bg)"/>

  <path d="M520 95 C770 150 475 255 710 325 C910 385 580 500 760 622"
        fill="none" stroke="#FFFFFF" stroke-width="38" stroke-linecap="round" opacity="0.38"/>
  <path d="M575 108 C760 168 515 252 690 325 C860 398 620 505 720 610"
        fill="none" stroke="#C7CEE9" stroke-width="3" stroke-dasharray="8 13" opacity="0.75"/>

  <text x="70" y="66" width="520" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="800"
        letter-spacing="2" fill="#343746">FIVE STEPS TO DESIGN</text>
  <text x="72" y="98" width="430" font-family="Segoe UI, Microsoft YaHei" font-size="15"
        fill="#6E7284">A connected process flow for research, ideation, and launch readiness.</text>

  <!-- Step 5: draw bottom nodes first so upper translucent halves interlock above them -->
  <path d="M640 504 A66 66 0 0 1 640 636 L640 570 Z" fill="#EC407A" filter="url(#softShadow)"/>
  <path d="M640 504 A66 66 0 0 0 640 636 L640 570 Z" fill="#EC407A" opacity="0.30"/>
  <circle cx="640" cy="570" r="38" fill="#FFFFFF" filter="url(#softShadow)"/>

  <!-- Step 4 -->
  <path d="M640 404 A66 66 0 0 0 640 536 L640 470 Z" fill="#F79646" filter="url(#softShadow)"/>
  <path d="M640 404 A66 66 0 0 1 640 536 L640 470 Z" fill="#F79646" opacity="0.30"/>
  <circle cx="640" cy="470" r="38" fill="#FFFFFF" filter="url(#softShadow)"/>

  <!-- Step 3 -->
  <path d="M640 304 A66 66 0 0 1 640 436 L640 370 Z" fill="#00B294" filter="url(#softShadow)"/>
  <path d="M640 304 A66 66 0 0 0 640 436 L640 370 Z" fill="#00B294" opacity="0.30"/>
  <circle cx="640" cy="370" r="38" fill="#FFFFFF" filter="url(#softShadow)"/>

  <!-- Step 2 -->
  <path d="M640 204 A66 66 0 0 0 640 336 L640 270 Z" fill="#0096C6" filter="url(#softShadow)"/>
  <path d="M640 204 A66 66 0 0 1 640 336 L640 270 Z" fill="#0096C6" opacity="0.30"/>
  <circle cx="640" cy="270" r="38" fill="#FFFFFF" filter="url(#softShadow)"/>

  <!-- Step 1 -->
  <path d="M640 104 A66 66 0 0 1 640 236 L640 170 Z" fill="#673AB7" filter="url(#softShadow)"/>
  <path d="M640 104 A66 66 0 0 0 640 236 L640 170 Z" fill="#673AB7" opacity="0.30"/>
  <circle cx="640" cy="170" r="38" fill="#FFFFFF" filter="url(#softShadow)"/>

  <text x="610" y="181" width="60" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei"
        font-size="29" font-weight="800" fill="#673AB7">01</text>
  <text x="610" y="281" width="60" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei"
        font-size="29" font-weight="800" fill="#0096C6">02</text>
  <text x="610" y="381" width="60" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei"
        font-size="29" font-weight="800" fill="#00B294">03</text>
  <text x="610" y="481" width="60" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei"
        font-size="29" font-weight="800" fill="#F79646">04</text>
  <text x="610" y="581" width="60" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei"
        font-size="29" font-weight="800" fill="#EC407A">05</text>

  <line x1="705" y1="170" x2="770" y2="170" stroke="#673AB7" stroke-width="3"/>
  <text x="790" y="154" width="310" font-family="Segoe UI, Microsoft YaHei" font-size="18"
        font-weight="800" letter-spacing="1.1" fill="#404040">DO YOUR RESEARCH</text>
  <text x="790" y="181" width="330" font-family="Segoe UI, Microsoft YaHei" font-size="14"
        fill="#5D6070">Map audience needs, constraints, competitors, and decision triggers before designing.</text>

  <line x1="575" y1="270" x2="510" y2="270" stroke="#0096C6" stroke-width="3"/>
  <text x="220" y="254" width="270" text-anchor="end" font-family="Segoe UI, Microsoft YaHei"
        font-size="18" font-weight="800" letter-spacing="1.1" fill="#404040">DEFINE THE PROBLEM</text>
  <text x="160" y="281" width="330" text-anchor="end" font-family="Segoe UI, Microsoft YaHei"
        font-size="14" fill="#5D6070">Turn raw findings into a clear opportunity statement and success metric.</text>

  <line x1="705" y1="370" x2="770" y2="370" stroke="#00B294" stroke-width="3"/>
  <text x="790" y="354" width="310" font-family="Segoe UI, Microsoft YaHei" font-size="18"
        font-weight="800" letter-spacing="1.1" fill="#404040">CREATE CONCEPTS</text>
  <text x="790" y="381" width="335" font-family="Segoe UI, Microsoft YaHei" font-size="14"
        fill="#5D6070">Explore several visual directions, then select the concept with the strongest story.</text>

  <line x1="575" y1="470" x2="510" y2="470" stroke="#F79646" stroke-width="3"/>
  <text x="220" y="454" width="270" text-anchor="end" font-family="Segoe UI, Microsoft YaHei"
        font-size="18" font-weight="800" letter-spacing="1.1" fill="#404040">PROTOTYPE FAST</text>
  <text x="160" y="481" width="330" text-anchor="end" font-family="Segoe UI, Microsoft YaHei"
        font-size="14" fill="#5D6070">Build lightweight mockups to test hierarchy, flow, and executive readability.</text>

  <line x1="705" y1="570" x2="770" y2="570" stroke="#EC407A" stroke-width="3"/>
  <text x="790" y="554" width="310" font-family="Segoe UI, Microsoft YaHei" font-size="18"
        font-weight="800" letter-spacing="1.1" fill="#404040">LAUNCH & ITERATE</text>
  <text x="790" y="581" width="335" font-family="Segoe UI, Microsoft YaHei" font-size="14"
        fill="#5D6070">Publish the final experience, capture feedback, and refine the next release cycle.</text>
</svg>
```

## Avoid in this skill
- ❌ Do not use `<mask>` to punch the donut holes; use white inner `<circle>` elements instead.
- ❌ Do not use `<clipPath>` on the semicircle node shapes; build each semicircle directly with editable `<path>` arcs.
- ❌ Do not put `marker-end` on connector paths; if arrows are needed, use simple `<line>` elements or draw arrowheads manually.
- ❌ Do not use `<use>` or `<symbol>` to repeat the nodes; duplicate the editable paths so PowerPoint can preserve every node as a native shape.
- ❌ Do not apply filters to `<line>` connector rules, because line filters are not reliably preserved.

## Composition notes
- Keep the S-curve centered, with roughly 30% vertical overlap between adjacent nodes to create the interlocking illusion.
- Alternate text blocks left and right; align each block to the nearest connector line and leave generous negative space around the spine.
- Use vivid step colors for the nodes, but keep the background pale and text dark gray so the process flow remains the visual focus.
- Draw lower nodes first and upper nodes last so the translucent halves appear to weave over the next step.