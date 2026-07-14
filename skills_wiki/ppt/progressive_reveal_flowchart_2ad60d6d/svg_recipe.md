# SVG Recipe — Progressive Reveal Flowchart

## Visual mechanism
Show the complete process in a muted “forest view,” then create detail slides where a translucent veil dims the whole diagram while the current stage is redrawn on top in accent color with a nearby annotation card. The audience always sees context, but attention is controlled by the focused node, connector, and explanation panel.

## SVG primitives needed
- 12× `<rect>` for neutral rounded flowchart nodes
- 1× `<rect>` for the semi-transparent white focus veil
- 2× `<rect>` for highlighted focus nodes redrawn above the veil
- 1× `<rect>` for the annotation card
- 1× `<rect>` for the small stage badge
- 13× `<line>` for straight flow connectors with arrowheads; put `marker-end` on each line directly
- 2× `<path>` for soft decorative background ribbons / emphasis glow shapes
- 1× `<linearGradient>` for the warm focus-node fill
- 1× `<linearGradient>` for the annotation card accent strip
- 1× `<filter id="softShadow">` applied to nodes and annotation card
- 1× `<filter id="glow">` applied to the focus halo path
- Multiple `<text>` elements with explicit `width` attributes for node labels, title, and annotation copy

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="focusFill" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#FFF7D6"/>
      <stop offset="100%" stop-color="#FFD88A"/>
    </linearGradient>
    <linearGradient id="cardStrip" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#F59E0B"/>
      <stop offset="100%" stop-color="#F97316"/>
    </linearGradient>
    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="8"/>
      <feGaussianBlur stdDeviation="10"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="glow" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="14"/>
    </filter>
    <marker id="arrowGray" markerWidth="10" markerHeight="10" refX="8" refY="5" orient="auto">
      <path d="M0,0 L10,5 L0,10 Z" fill="#A8AFBA"/>
    </marker>
    <marker id="arrowOrange" markerWidth="10" markerHeight="10" refX="8" refY="5" orient="auto">
      <path d="M0,0 L10,5 L0,10 Z" fill="#D97706"/>
    </marker>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#FBFCFE"/>
  <path d="M-80,110 C180,20 320,120 520,70 C780,5 1010,55 1360,-40 L1360,0 L-80,0 Z" fill="#EEF3FA"/>
  <path d="M930,620 C1040,560 1170,590 1320,510 L1320,720 L900,720 Z" fill="#FFF4DE"/>

  <text x="56" y="56" width="720" font-family="Segoe UI, Microsoft YaHei" font-size="28" font-weight="700" fill="#172033">Diagnostic Decision Flow</text>
  <text x="56" y="86" width="760" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#667085">Progressive reveal slide: entire algorithm remains visible while the current decision point receives narrative focus.</text>

  <line x1="180" y1="350" x2="282" y2="210" stroke="#A8AFBA" stroke-width="2.5" marker-end="url(#arrowGray)"/>
  <line x1="180" y1="350" x2="282" y2="350" stroke="#A8AFBA" stroke-width="2.5" marker-end="url(#arrowGray)"/>
  <line x1="180" y1="350" x2="282" y2="490" stroke="#A8AFBA" stroke-width="2.5" marker-end="url(#arrowGray)"/>
  <line x1="470" y1="210" x2="562" y2="205" stroke="#A8AFBA" stroke-width="2.5" marker-end="url(#arrowGray)"/>
  <line x1="470" y1="350" x2="562" y2="350" stroke="#A8AFBA" stroke-width="2.5" marker-end="url(#arrowGray)"/>
  <line x1="470" y1="490" x2="562" y2="505" stroke="#A8AFBA" stroke-width="2.5" marker-end="url(#arrowGray)"/>
  <line x1="730" y1="205" x2="818" y2="170" stroke="#A8AFBA" stroke-width="2.5" marker-end="url(#arrowGray)"/>
  <line x1="730" y1="505" x2="818" y2="462" stroke="#A8AFBA" stroke-width="2.5" marker-end="url(#arrowGray)"/>
  <line x1="730" y1="505" x2="818" y2="585" stroke="#A8AFBA" stroke-width="2.5" marker-end="url(#arrowGray)"/>
  <line x1="1000" y1="170" x2="1085" y2="170" stroke="#A8AFBA" stroke-width="2.5" marker-end="url(#arrowGray)"/>
  <line x1="1000" y1="462" x2="1085" y2="462" stroke="#A8AFBA" stroke-width="2.5" marker-end="url(#arrowGray)"/>
  <line x1="1000" y1="585" x2="1085" y2="585" stroke="#A8AFBA" stroke-width="2.5" marker-end="url(#arrowGray)"/>

  <rect x="60" y="300" width="120" height="100" rx="18" fill="#F2F4F7" stroke="#CBD2DC" stroke-width="1.5"/>
  <text x="82" y="333" width="82" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#344054">Initial suspicion</text>
  <text x="82" y="365" width="82" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#667085">Symptoms + history</text>

  <rect x="282" y="158" width="188" height="104" rx="18" fill="#F2F4F7" stroke="#CBD2DC" stroke-width="1.5"/>
  <text x="306" y="190" width="140" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#344054">Screening panel A</text>
  <text x="306" y="218" width="142" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#667085">Low function · low marker</text>

  <rect x="282" y="298" width="188" height="104" rx="18" fill="#F2F4F7" stroke="#CBD2DC" stroke-width="1.5"/>
  <text x="306" y="330" width="140" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#344054">Screening panel B</text>
  <text x="306" y="358" width="142" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#667085">Low function · normal level</text>

  <rect x="282" y="438" width="188" height="104" rx="18" fill="#F2F4F7" stroke="#CBD2DC" stroke-width="1.5"/>
  <text x="306" y="470" width="140" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#344054">Screening panel C</text>
  <text x="306" y="498" width="142" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#667085">Normal baseline results</text>

  <rect x="562" y="166" width="168" height="78" rx="16" fill="#F2F4F7" stroke="#CBD2DC" stroke-width="1.5"/>
  <text x="586" y="197" width="124" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#344054">Confirm type I</text>
  <text x="586" y="220" width="126" font-family="Segoe UI, Microsoft YaHei" font-size="10.5" fill="#667085">Repeat blood test</text>

  <rect x="562" y="311" width="168" height="78" rx="16" fill="#F2F4F7" stroke="#CBD2DC" stroke-width="1.5"/>
  <text x="586" y="342" width="124" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#344054">Confirm type II</text>
  <text x="586" y="365" width="126" font-family="Segoe UI, Microsoft YaHei" font-size="10.5" fill="#667085">Repeat blood test</text>

  <rect x="562" y="466" width="168" height="78" rx="16" fill="#F2F4F7" stroke="#CBD2DC" stroke-width="1.5"/>
  <text x="586" y="497" width="124" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#344054">Retest during event</text>
  <text x="586" y="520" width="126" font-family="Segoe UI, Microsoft YaHei" font-size="10.5" fill="#667085">Capture active episode</text>

  <rect x="818" y="128" width="182" height="84" rx="16" fill="#F2F4F7" stroke="#CBD2DC" stroke-width="1.5"/>
  <text x="842" y="159" width="136" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#344054">Family history?</text>
  <text x="842" y="183" width="138" font-family="Segoe UI, Microsoft YaHei" font-size="10.5" fill="#667085">Late onset triggers exclusion</text>

  <rect x="818" y="424" width="182" height="76" rx="16" fill="#F2F4F7" stroke="#CBD2DC" stroke-width="1.5"/>
  <text x="842" y="455" width="136" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#344054">Abnormal retest</text>
  <text x="842" y="478" width="138" font-family="Segoe UI, Microsoft YaHei" font-size="10.5" fill="#667085">Route back to panel B</text>

  <rect x="818" y="548" width="182" height="76" rx="16" fill="#F2F4F7" stroke="#CBD2DC" stroke-width="1.5"/>
  <text x="842" y="579" width="136" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#344054">Normal retest</text>
  <text x="842" y="602" width="138" font-family="Segoe UI, Microsoft YaHei" font-size="10.5" fill="#667085">Proceed to genetics</text>

  <rect x="1085" y="142" width="128" height="56" rx="14" fill="#F2F4F7" stroke="#CBD2DC" stroke-width="1.5"/>
  <text x="1107" y="176" width="84" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#344054">Exclude AAE</text>
  <rect x="1085" y="434" width="128" height="56" rx="14" fill="#F2F4F7" stroke="#CBD2DC" stroke-width="1.5"/>
  <text x="1107" y="468" width="84" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#344054">Loop back</text>
  <rect x="1085" y="557" width="128" height="56" rx="14" fill="#F2F4F7" stroke="#CBD2DC" stroke-width="1.5"/>
  <text x="1107" y="591" width="84" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#344054">Final classify</text>

  <rect x="0" y="0" width="1280" height="720" fill="#FFFFFF" opacity="0.68"/>

  <path d="M520,278 C600,225 720,230 790,292 C864,358 842,464 752,518 C652,580 512,548 456,458 C414,390 440,325 520,278 Z" fill="#F59E0B" opacity="0.18" filter="url(#glow)"/>
  <line x1="470" y1="350" x2="562" y2="350" stroke="#D97706" stroke-width="4" marker-end="url(#arrowOrange)"/>
  <line x1="562" y1="350" x2="470" y2="350" stroke="#D97706" stroke-width="0"/>

  <rect x="282" y="298" width="188" height="104" rx="20" fill="url(#focusFill)" stroke="#F59E0B" stroke-width="3" filter="url(#softShadow)"/>
  <text x="306" y="330" width="140" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="800" fill="#92400E">Screening panel B</text>
  <text x="306" y="359" width="145" font-family="Segoe UI, Microsoft YaHei" font-size="11.5" fill="#A16207">Low function with normal or elevated level</text>

  <rect x="562" y="311" width="168" height="78" rx="18" fill="#FFF7ED" stroke="#D97706" stroke-width="2.5" filter="url(#softShadow)"/>
  <text x="586" y="342" width="124" font-family="Segoe UI, Microsoft YaHei" font-size="13.5" font-weight="800" fill="#92400E">Confirm type II</text>
  <text x="586" y="365" width="126" font-family="Segoe UI, Microsoft YaHei" font-size="10.5" fill="#A16207">Repeat test before label</text>

  <rect x="802" y="250" width="390" height="250" rx="28" fill="#FFFFFF" stroke="#E6EAF0" stroke-width="1.5" filter="url(#softShadow)"/>
  <rect x="802" y="250" width="390" height="8" rx="4" fill="url(#cardStrip)"/>
  <rect x="832" y="284" width="92" height="28" rx="14" fill="#FEF3C7"/>
  <text x="850" y="304" width="58" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#B45309">REVEAL 02</text>
  <text x="832" y="348" width="310" font-family="Segoe UI, Microsoft YaHei" font-size="27" font-weight="800" fill="#172033">Interpret the ambiguous result</text>
  <text x="832" y="389" width="318" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#475467">This branch keeps the full algorithm visible but isolates the second screening outcome. The presenter explains why the follow-up confirmation step is required before moving forward.</text>
  <text x="832" y="455" width="310" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#D97706">Presenter cue: advance next slide to move the spotlight to retesting.</text>
</svg>
```

## Avoid in this skill
- ❌ Do not use `<mask>` to create the spotlight; instead place a semi-transparent white `<rect>` over the full chart and redraw the highlighted nodes above it.
- ❌ Do not put `marker-end` on a `<path>` connector or on a parent `<g>`; use individual `<line>` elements with `marker-end` applied directly.
- ❌ Do not apply shadows or blur filters to `<line>` connectors; filters on lines are dropped by the translator.
- ❌ Do not rely on PowerPoint animation inside the SVG; build separate slides for overview, reveal 01, reveal 02, etc., and optionally apply Morph in PowerPoint.
- ❌ Do not use text without explicit `width`; every node label and annotation block needs a fixed width for clean PPTX rendering.

## Composition notes
- Keep the full flowchart across the central 70% of the slide so the audience retains system context even when dimmed.
- Reserve a right-side annotation panel for the narrative explanation; avoid placing dense body copy directly inside the flowchart.
- Use neutral gray for overview elements, then one warm accent family for the focused step, highlighted connector, badge, and card strip.
- For a multi-slide sequence, keep all base-node coordinates identical; only move the highlight redraw and annotation copy from slide to slide.