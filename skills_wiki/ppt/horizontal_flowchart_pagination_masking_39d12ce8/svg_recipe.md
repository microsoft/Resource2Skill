# SVG Recipe — Horizontal Flowchart Pagination & Masking

## Visual mechanism
A complete left-to-right decision tree is drawn in pale neutral tones, then a translucent white mask is placed over the whole chart to fade inactive branches. The active pathway is redrawn above the mask in a vibrant accent color, creating progressive disclosure while preserving the audience’s mental map of the full process.

## SVG primitives needed
- 1× `<rect>` for the slide background
- 5× pale `<rect>` flowchart nodes for the full underlying decision tree
- 5× duplicate active `<rect>` nodes redrawn above the mask
- 4× pale `<path>` elbow connectors for the full underlying tree
- 2× duplicate active `<path>` elbow connectors redrawn above the mask
- 6× small triangular `<path>` arrowheads for connector direction
- 1× full-slide translucent white `<rect>` as the pagination mask
- 1× large white `<rect>` annotation panel with accent border
- 1× small accent `<rect>` label tab on the annotation panel
- 1× `<linearGradient>` for the subtle page background
- 1× `<filter id="cardShadow">` applied to the annotation panel and active nodes
- 1× `<filter id="softShadow">` applied to base nodes for slight depth
- Multiple `<text>` elements with explicit `width` attributes for titles, node labels, annotation copy, and pagination metadata

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#F7F8FA"/>
      <stop offset="55%" stop-color="#FFFFFF"/>
      <stop offset="100%" stop-color="#F1F3F6"/>
    </linearGradient>
    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feOffset dx="0" dy="2"/>
      <feGaussianBlur stdDeviation="4"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="cardShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feOffset dx="0" dy="10"/>
      <feGaussianBlur stdDeviation="14"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>
  <text x="70" y="62" width="620" font-family="Segoe UI, Microsoft YaHei" font-size="28" font-weight="700" fill="#2C2C2C">Diagnostic Guideline — Focused Path</text>
  <text x="70" y="94" width="760" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#7A7A7A">Pagination state: inactive branches are masked; active clinical pathway is redrawn above the overlay.</text>
  <rect x="1032" y="46" width="150" height="34" rx="17" fill="#FFF0E7" stroke="#ED7D31" stroke-width="1.5"/>
  <text x="1054" y="69" width="110" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#ED7D31">PAGE 2 / 5</text>

  <!-- full underlying horizontal flowchart -->
  <path d="M250 344 L318 344 L318 188 L390 188" fill="none" stroke="#D9D9D9" stroke-width="3"/>
  <path d="M250 344 L390 344" fill="none" stroke="#D9D9D9" stroke-width="3"/>
  <path d="M250 344 L318 344 L318 500 L390 500" fill="none" stroke="#D9D9D9" stroke-width="3"/>
  <path d="M610 188 L720 188" fill="none" stroke="#D9D9D9" stroke-width="3"/>
  <path d="M382 181 L398 188 L382 195 Z" fill="#D9D9D9"/>
  <path d="M382 337 L398 344 L382 351 Z" fill="#D9D9D9"/>
  <path d="M382 493 L398 500 L382 507 Z" fill="#D9D9D9"/>
  <path d="M712 181 L728 188 L712 195 Z" fill="#D9D9D9"/>

  <rect x="70" y="292" width="180" height="104" rx="18" fill="#F2F2F2" stroke="#D9D9D9" stroke-width="2" filter="url(#softShadow)"/>
  <text x="94" y="330" width="132" font-family="Segoe UI, Microsoft YaHei" font-size="21" font-weight="700" fill="#404040" text-anchor="middle">
    <tspan x="160" dy="0">Suspicion</tspan><tspan x="160" dy="29">of HAE</tspan>
  </text>

  <rect x="390" y="128" width="220" height="120" rx="18" fill="#F2F2F2" stroke="#D9D9D9" stroke-width="2" filter="url(#softShadow)"/>
  <text x="420" y="161" width="160" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="700" fill="#404040" text-anchor="middle">
    <tspan x="500" dy="0">Type I Pattern</tspan><tspan x="500" dy="25">C1-INH Func. ↓</tspan><tspan x="500" dy="24">C4 level ↓</tspan>
  </text>

  <rect x="390" y="284" width="220" height="120" rx="18" fill="#F2F2F2" stroke="#D9D9D9" stroke-width="2" filter="url(#softShadow)"/>
  <text x="420" y="317" width="160" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="700" fill="#404040" text-anchor="middle">
    <tspan x="500" dy="0">Type II Pattern</tspan><tspan x="500" dy="25">Function ↓</tspan><tspan x="500" dy="24">Level Normal</tspan>
  </text>

  <rect x="390" y="440" width="220" height="120" rx="18" fill="#F2F2F2" stroke="#D9D9D9" stroke-width="2" filter="url(#softShadow)"/>
  <text x="420" y="473" width="160" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="700" fill="#404040" text-anchor="middle">
    <tspan x="500" dy="0">Normal Result</tspan><tspan x="500" dy="25">C1-INH Normal</tspan><tspan x="500" dy="24">C4 Normal</tspan>
  </text>

  <rect x="720" y="128" width="240" height="120" rx="18" fill="#F2F2F2" stroke="#D9D9D9" stroke-width="2" filter="url(#softShadow)"/>
  <text x="754" y="161" width="172" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="700" fill="#404040" text-anchor="middle">
    <tspan x="840" dy="0">HAE-I</tspan><tspan x="840" dy="25">Confirm by repeating</tspan><tspan x="840" dy="24">blood test</tspan>
  </text>

  <!-- pagination mask: fade everything already drawn -->
  <rect x="0" y="0" width="1280" height="720" fill="#FFFFFF" fill-opacity="0.82"/>

  <!-- large annotation box placed in negative space created by the mask -->
  <rect x="706" y="326" width="486" height="244" rx="26" fill="#FFFFFF" stroke="#ED7D31" stroke-width="4" filter="url(#cardShadow)"/>
  <rect x="744" y="304" width="182" height="46" rx="23" fill="#ED7D31"/>
  <text x="773" y="334" width="130" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#FFFFFF">ACTIVE NOTE</text>
  <text x="746" y="392" width="388" font-family="Segoe UI, Microsoft YaHei" font-size="30" font-weight="800" fill="#2C2C2C">Repeat testing confirms diagnosis</text>
  <text x="748" y="440" width="380" font-family="Segoe UI, Microsoft YaHei" font-size="19" fill="#565656">
    <tspan x="748" dy="0">Focus the audience only on the Type I branch.</tspan>
    <tspan x="748" dy="31">The rest of the algorithm remains visible,</tspan>
    <tspan x="748" dy="31">but deliberately low-contrast for context.</tspan>
  </text>
  <line x1="748" y1="522" x2="1125" y2="522" stroke="#FFE0CF" stroke-width="3"/>
  <text x="748" y="550" width="356" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="700" fill="#ED7D31">Presenter cue: explain one path, then paginate to the next branch.</text>

  <!-- active pathway redrawn above mask -->
  <path d="M250 344 L318 344 L318 188 L390 188" fill="none" stroke="#ED7D31" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M610 188 L720 188" fill="none" stroke="#ED7D31" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M382 178 L404 188 L382 198 Z" fill="#ED7D31"/>
  <path d="M712 178 L734 188 L712 198 Z" fill="#ED7D31"/>

  <rect x="70" y="292" width="180" height="104" rx="18" fill="#ED7D31" stroke="#C75D17" stroke-width="2" filter="url(#cardShadow)"/>
  <text x="94" y="330" width="132" font-family="Segoe UI, Microsoft YaHei" font-size="21" font-weight="800" fill="#FFFFFF" text-anchor="middle">
    <tspan x="160" dy="0">Suspicion</tspan><tspan x="160" dy="29">of HAE</tspan>
  </text>

  <rect x="390" y="128" width="220" height="120" rx="18" fill="#ED7D31" stroke="#C75D17" stroke-width="2" filter="url(#cardShadow)"/>
  <text x="420" y="161" width="160" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="800" fill="#FFFFFF" text-anchor="middle">
    <tspan x="500" dy="0">Type I Pattern</tspan><tspan x="500" dy="25">C1-INH Func. ↓</tspan><tspan x="500" dy="24">C4 level ↓</tspan>
  </text>

  <rect x="720" y="128" width="240" height="120" rx="18" fill="#ED7D31" stroke="#C75D17" stroke-width="2" filter="url(#cardShadow)"/>
  <text x="754" y="161" width="172" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="800" fill="#FFFFFF" text-anchor="middle">
    <tspan x="840" dy="0">HAE-I</tspan><tspan x="840" dy="25">Confirm by repeating</tspan><tspan x="840" dy="24">blood test</tspan>
  </text>
</svg>
```

## Avoid in this skill
- ❌ Do not use SVG `<mask>` to create the fade layer; use a semi-transparent white `<rect>` overlay instead.
- ❌ Do not rely on clipping or masking non-image shapes to reveal the active path; redraw active nodes and connectors above the overlay.
- ❌ Do not use `marker-end` on `<path>` connectors for arrowheads; use small triangular `<path>` arrowheads as editable shapes.
- ❌ Do not put all flowchart elements inside one flattened image; the value of this technique is that every node, connector, and label remains editable in PowerPoint.
- ❌ Do not make the mask fully opaque; keep inactive branches faintly visible so the audience retains context.

## Composition notes
- Reserve the upper-left and mid-left of the slide for the horizontal flowchart; keep the active branch visually continuous from left to right.
- Place the annotation box in the largest area of negative space created by the fade, commonly the lower-right quadrant.
- Use one strong accent color only for the active pathway, arrowheads, label tab, and annotation border.
- The mask should fade inactive content to roughly 15–25% perceived intensity while the active nodes are redrawn at full contrast above it.