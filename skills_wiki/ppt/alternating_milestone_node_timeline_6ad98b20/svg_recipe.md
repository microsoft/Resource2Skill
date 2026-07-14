# SVG Recipe — Alternating Milestone Node Timeline

## Visual mechanism
A central horizontal time axis anchors a sequence of milestones, with stems alternating above and below the line to prevent text collisions. Each milestone is emphasized by a colored circular node, soft editable shadow, and date pill on the axis, creating a premium roadmap rhythm.

## SVG primitives needed
- 1× `<rect>` for the full-slide soft background
- 2× decorative `<path>` blobs for subtle executive-slide depth
- 1× `<rect>` for the rounded central timeline axis
- 5× `<line>` for vertical milestone stems
- 5× small `<circle>` tick points on the axis
- 5× shadowed `<circle>` milestone nodes
- 5× smaller highlight `<circle>` overlays inside the nodes
- 5× rounded `<rect>` date pills placed over the axis
- 5× `<text>` node numbers
- 5× `<text>` date labels
- 5× `<text>` milestone titles
- 5× multiline `<text>` milestone descriptions using `<tspan>`
- 2× header `<text>` elements for slide title and subtitle
- 5× `<linearGradient>` fills for color-rich node surfaces
- 1× `<filter id="softShadow">` using `feOffset`, `feGaussianBlur`, and `feMerge` for node/pill depth
- 1× `<filter id="subtleGlow">` using `feGaussianBlur` for faint background accents

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#F8FAFC"/>
      <stop offset="100%" stop-color="#EEF2FF"/>
    </linearGradient>

    <linearGradient id="blueGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#60A5FA"/>
      <stop offset="100%" stop-color="#2563EB"/>
    </linearGradient>
    <linearGradient id="emeraldGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#34D399"/>
      <stop offset="100%" stop-color="#059669"/>
    </linearGradient>
    <linearGradient id="amberGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#FBBF24"/>
      <stop offset="100%" stop-color="#D97706"/>
    </linearGradient>
    <linearGradient id="roseGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#FB7185"/>
      <stop offset="100%" stop-color="#DC2626"/>
    </linearGradient>
    <linearGradient id="purpleGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#A78BFA"/>
      <stop offset="100%" stop-color="#7C3AED"/>
    </linearGradient>

    <filter id="softShadow" x="-40%" y="-40%" width="180%" height="180%">
      <feOffset dx="0" dy="8" in="SourceAlpha" result="offset"/>
      <feGaussianBlur stdDeviation="8" in="offset" result="blur"/>
      <feColorMatrix in="blur" type="matrix" values="0 0 0 0 0.05 0 0 0 0 0.08 0 0 0 0 0.15 0 0 0 0.22 0" result="shadow"/>
      <feMerge>
        <feMergeNode in="shadow"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="subtleGlow" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="18"/>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>

  <path d="M-80,120 C120,40 220,110 320,30 C410,-40 520,0 600,80 C460,145 310,150 180,205 C60,255 -20,230 -80,120 Z"
        fill="#DBEAFE" opacity="0.55" filter="url(#subtleGlow)"/>
  <path d="M990,650 C1070,560 1210,570 1340,450 L1340,760 L930,760 C915,715 940,690 990,650 Z"
        fill="#EDE9FE" opacity="0.72" filter="url(#subtleGlow)"/>

  <text x="78" y="70" width="760" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="700" fill="#0F172A">
    Product Launch Roadmap
  </text>
  <text x="80" y="104" width="820" font-family="Segoe UI, Microsoft YaHei" font-size="17" fill="#475569">
    Strategic timeline and core milestones for go-to-market execution.
  </text>

  <rect x="145" y="389" width="990" height="7" rx="3.5" fill="#CBD5E1"/>

  <line x1="180" y1="392" x2="180" y2="268" stroke="#CBD5E1" stroke-width="3"/>
  <line x1="410" y1="392" x2="410" y2="502" stroke="#CBD5E1" stroke-width="3"/>
  <line x1="640" y1="392" x2="640" y2="268" stroke="#CBD5E1" stroke-width="3"/>
  <line x1="870" y1="392" x2="870" y2="502" stroke="#CBD5E1" stroke-width="3"/>
  <line x1="1100" y1="392" x2="1100" y2="268" stroke="#CBD5E1" stroke-width="3"/>

  <circle cx="180" cy="392" r="7" fill="#FFFFFF" stroke="#3B82F6" stroke-width="3"/>
  <circle cx="410" cy="392" r="7" fill="#FFFFFF" stroke="#10B981" stroke-width="3"/>
  <circle cx="640" cy="392" r="7" fill="#FFFFFF" stroke="#F59E0B" stroke-width="3"/>
  <circle cx="870" cy="392" r="7" fill="#FFFFFF" stroke="#EF4444" stroke-width="3"/>
  <circle cx="1100" cy="392" r="7" fill="#FFFFFF" stroke="#8B5CF6" stroke-width="3"/>

  <rect x="139" y="363" width="82" height="30" rx="15" fill="#3B82F6" filter="url(#softShadow)"/>
  <rect x="369" y="391" width="82" height="30" rx="15" fill="#10B981" filter="url(#softShadow)"/>
  <rect x="599" y="363" width="82" height="30" rx="15" fill="#F59E0B" filter="url(#softShadow)"/>
  <rect x="829" y="391" width="82" height="30" rx="15" fill="#EF4444" filter="url(#softShadow)"/>
  <rect x="1059" y="363" width="82" height="30" rx="15" fill="#8B5CF6" filter="url(#softShadow)"/>

  <text x="180" y="383" width="82" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#FFFFFF">Q1 2024</text>
  <text x="410" y="411" width="82" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#FFFFFF">Q2 2024</text>
  <text x="640" y="383" width="82" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#FFFFFF">Q3 2024</text>
  <text x="870" y="411" width="82" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#FFFFFF">Q4 2024</text>
  <text x="1100" y="383" width="82" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#FFFFFF">Q1 2025</text>

  <circle cx="180" cy="248" r="38" fill="url(#blueGrad)" filter="url(#softShadow)"/>
  <circle cx="192" cy="235" r="10" fill="#FFFFFF" opacity="0.30"/>
  <text x="180" y="257" width="76" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="19" font-weight="800" fill="#FFFFFF">01</text>

  <circle cx="410" cy="522" r="38" fill="url(#emeraldGrad)" filter="url(#softShadow)"/>
  <circle cx="422" cy="509" r="10" fill="#FFFFFF" opacity="0.30"/>
  <text x="410" y="531" width="76" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="19" font-weight="800" fill="#FFFFFF">02</text>

  <circle cx="640" cy="248" r="38" fill="url(#amberGrad)" filter="url(#softShadow)"/>
  <circle cx="652" cy="235" r="10" fill="#FFFFFF" opacity="0.30"/>
  <text x="640" y="257" width="76" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="19" font-weight="800" fill="#FFFFFF">03</text>

  <circle cx="870" cy="522" r="38" fill="url(#roseGrad)" filter="url(#softShadow)"/>
  <circle cx="882" cy="509" r="10" fill="#FFFFFF" opacity="0.30"/>
  <text x="870" y="531" width="76" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="19" font-weight="800" fill="#FFFFFF">04</text>

  <circle cx="1100" cy="248" r="38" fill="url(#purpleGrad)" filter="url(#softShadow)"/>
  <circle cx="1112" cy="235" r="10" fill="#FFFFFF" opacity="0.30"/>
  <text x="1100" y="257" width="76" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="19" font-weight="800" fill="#FFFFFF">05</text>

  <text x="70" y="172" width="220" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="700" fill="#2563EB">Concept &amp; Strategy</text>
  <text x="70" y="202" width="220" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#475569">
    <tspan x="70" dy="0">Market research, competitive</tspan>
    <tspan x="70" dy="18">analysis, and core product</tspan>
    <tspan x="70" dy="18">ideation phase.</tspan>
  </text>

  <text x="300" y="610" width="220" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="700" fill="#059669">Prototyping</text>
  <text x="300" y="640" width="220" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#475569">
    <tspan x="300" dy="0">Develop wireframes, UX flows,</tspan>
    <tspan x="300" dy="18">and scalable architecture for</tspan>
    <tspan x="300" dy="18">the first working build.</tspan>
  </text>

  <text x="530" y="172" width="220" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="700" fill="#D97706">Beta Release</text>
  <text x="530" y="202" width="220" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#475569">
    <tspan x="530" dy="0">Closed beta testing with key</tspan>
    <tspan x="530" dy="18">stakeholders to gather critical</tspan>
    <tspan x="530" dy="18">feedback and refine fit.</tspan>
  </text>

  <text x="760" y="610" width="220" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="700" fill="#DC2626">Launch Prep</text>
  <text x="760" y="640" width="220" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#475569">
    <tspan x="760" dy="0">Finalize marketing materials,</tspan>
    <tspan x="760" dy="18">sales enablement, QA testing,</tspan>
    <tspan x="760" dy="18">and release readiness.</tspan>
  </text>

  <text x="990" y="172" width="220" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="700" fill="#7C3AED">Public Launch</text>
  <text x="990" y="202" width="220" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#475569">
    <tspan x="990" dy="0">Global product rollout, PR</tspan>
    <tspan x="990" dy="18">campaign, and initial user</tspan>
    <tspan x="990" dy="18">acquisition motion.</tspan>
  </text>
</svg>
```

## Avoid in this skill
- ❌ Do not use `marker-end` arrows for the timeline; this layout should read as a clean progression line, and SVG arrow markers may not translate reliably.
- ❌ Do not apply filters to `<line>` stems or the axis; use shadows only on circles, pills, or decorative paths.
- ❌ Do not use `<use>` to duplicate milestone groups; repeat the editable shapes explicitly so each node remains independent in PowerPoint.
- ❌ Do not rely on automatic text wrapping; every `<text>` needs a `width` attribute, and multiline descriptions should use explicit `<tspan>` rows.
- ❌ Do not place text too close to the central axis; alternating layouts need breathing room around each stem and node.

## Composition notes
- Keep the axis slightly below center, around `y=390`, leaving strong title/subtitle space at the top and room for lower milestones.
- Use equal horizontal spacing between milestone nodes; five nodes work well from roughly `x=180` to `x=1100`.
- Alternate text blocks above and below the axis in sync with the nodes to avoid overlap and create a clear visual cadence.
- Use one accent color per milestone, repeating it on the node, date pill, tick stroke, and title for fast phase recognition.