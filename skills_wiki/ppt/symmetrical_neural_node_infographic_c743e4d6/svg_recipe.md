# SVG Recipe — Symmetrical Hub & Spoke Diagram

## Visual mechanism
A central hub anchors ten equally weighted spokes that radiate symmetrically into colored node pills, creating a neural-network or circuit-board feel. Matching side text blocks use the same color coding, so the viewer can scan from the core concept outward to each supporting point.

## SVG primitives needed
- 1× `<rect>` for the clean white slide background
- 10× `<path>` for thick angled ribbon spokes that connect the hub to each node
- 10× `<rect>` for rounded colored endpoint node pills
- 10× `<circle>` for small white node badges / connector dots
- 1× `<circle>` for the central hub
- 2× `<circle>` for subtle central hub rings
- 10× `<path>` for small white line-art symbols inside the node badges
- 21× `<text>` for title, central label, node numbers, and left/right description blocks; every text element includes `width`
- 1× `<radialGradient>` for the dimensional central hub
- 1× `<filter id="softShadow">` applied to hub and node pills
- 1× `<filter id="spokeGlow">` applied to colored spokes for a premium luminous edge

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <radialGradient id="hubGrad" cx="38%" cy="30%" r="75%">
      <stop offset="0%" stop-color="#607D8B"/>
      <stop offset="55%" stop-color="#263238"/>
      <stop offset="100%" stop-color="#11191D"/>
    </radialGradient>
    <filter id="softShadow" x="-25%" y="-25%" width="150%" height="150%">
      <feOffset dx="0" dy="8"/>
      <feGaussianBlur stdDeviation="10"/>
      <feColorMatrix type="matrix" values="0 0 0 0 0.05 0 0 0 0 0.08 0 0 0 0 0.10 0 0 0 .22 0"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="spokeGlow" x="-20%" y="-40%" width="140%" height="180%">
      <feGaussianBlur stdDeviation="3" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#FFFFFF"/>

  <text x="640" y="50" width="520" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="28" font-weight="700" fill="#263238" letter-spacing="2">BUSINESS INFOGRAPHIC</text>
  <text x="640" y="78" width="620" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#90A4AE">Ten balanced priorities connected to one strategic core</text>

  <!-- left spokes -->
  <path d="M594 334 L532 112 L490 112 L490 138 L532 138 L598 374 Z" fill="#9C27B0" opacity="0.96" filter="url(#spokeGlow)"/>
  <path d="M590 342 L530 230 L490 230 L490 256 L530 256 L596 372 Z" fill="#3F51B5" opacity="0.96" filter="url(#spokeGlow)"/>
  <path d="M586 348 L530 347 L490 347 L490 373 L530 373 L586 372 Z" fill="#00BCD4" opacity="0.96" filter="url(#spokeGlow)"/>
  <path d="M596 348 L530 464 L490 464 L490 490 L530 490 L590 378 Z" fill="#4CAF50" opacity="0.96" filter="url(#spokeGlow)"/>
  <path d="M598 346 L532 582 L490 582 L490 608 L532 608 L594 386 Z" fill="#8BC34A" opacity="0.96" filter="url(#spokeGlow)"/>

  <!-- right spokes -->
  <path d="M686 334 L748 112 L790 112 L790 138 L748 138 L682 374 Z" fill="#E91E63" opacity="0.96" filter="url(#spokeGlow)"/>
  <path d="M690 342 L750 230 L790 230 L790 256 L750 256 L684 372 Z" fill="#F44336" opacity="0.96" filter="url(#spokeGlow)"/>
  <path d="M694 348 L750 347 L790 347 L790 373 L750 373 L694 372 Z" fill="#FF9800" opacity="0.96" filter="url(#spokeGlow)"/>
  <path d="M684 348 L750 464 L790 464 L790 490 L750 490 L690 378 Z" fill="#FFC107" opacity="0.96" filter="url(#spokeGlow)"/>
  <path d="M682 346 L748 582 L790 582 L790 608 L748 608 L686 386 Z" fill="#FFEB3B" opacity="0.96" filter="url(#spokeGlow)"/>

  <!-- node pills -->
  <rect x="370" y="96" width="126" height="58" rx="29" fill="#9C27B0" filter="url(#softShadow)"/>
  <rect x="370" y="214" width="126" height="58" rx="29" fill="#3F51B5" filter="url(#softShadow)"/>
  <rect x="370" y="331" width="126" height="58" rx="29" fill="#00BCD4" filter="url(#softShadow)"/>
  <rect x="370" y="448" width="126" height="58" rx="29" fill="#4CAF50" filter="url(#softShadow)"/>
  <rect x="370" y="566" width="126" height="58" rx="29" fill="#8BC34A" filter="url(#softShadow)"/>

  <rect x="784" y="96" width="126" height="58" rx="29" fill="#E91E63" filter="url(#softShadow)"/>
  <rect x="784" y="214" width="126" height="58" rx="29" fill="#F44336" filter="url(#softShadow)"/>
  <rect x="784" y="331" width="126" height="58" rx="29" fill="#FF9800" filter="url(#softShadow)"/>
  <rect x="784" y="448" width="126" height="58" rx="29" fill="#FFC107" filter="url(#softShadow)"/>
  <rect x="784" y="566" width="126" height="58" rx="29" fill="#FFEB3B" filter="url(#softShadow)"/>

  <!-- central hub -->
  <circle cx="640" cy="360" r="90" fill="none" stroke="#ECEFF1" stroke-width="2"/>
  <circle cx="640" cy="360" r="72" fill="none" stroke="#CFD8DC" stroke-width="5" opacity="0.65"/>
  <circle cx="640" cy="360" r="58" fill="url(#hubGrad)" filter="url(#softShadow)"/>
  <text x="640" y="352" width="110" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#FFFFFF" letter-spacing="1.5">STRATEGIC</text>
  <text x="640" y="374" width="110" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="800" fill="#FFFFFF">CORE</text>

  <!-- node badges and numbers -->
  <circle cx="400" cy="125" r="20" fill="#FFFFFF" opacity="0.24"/><text x="400" y="133" width="40" text-anchor="middle" font-family="Segoe UI" font-size="18" font-weight="800" fill="#FFFFFF">01</text>
  <circle cx="400" cy="243" r="20" fill="#FFFFFF" opacity="0.24"/><text x="400" y="251" width="40" text-anchor="middle" font-family="Segoe UI" font-size="18" font-weight="800" fill="#FFFFFF">02</text>
  <circle cx="400" cy="360" r="20" fill="#FFFFFF" opacity="0.24"/><text x="400" y="368" width="40" text-anchor="middle" font-family="Segoe UI" font-size="18" font-weight="800" fill="#FFFFFF">03</text>
  <circle cx="400" cy="477" r="20" fill="#FFFFFF" opacity="0.24"/><text x="400" y="485" width="40" text-anchor="middle" font-family="Segoe UI" font-size="18" font-weight="800" fill="#FFFFFF">04</text>
  <circle cx="400" cy="595" r="20" fill="#FFFFFF" opacity="0.24"/><text x="400" y="603" width="40" text-anchor="middle" font-family="Segoe UI" font-size="18" font-weight="800" fill="#FFFFFF">05</text>

  <circle cx="880" cy="125" r="20" fill="#FFFFFF" opacity="0.26"/><text x="880" y="133" width="40" text-anchor="middle" font-family="Segoe UI" font-size="18" font-weight="800" fill="#FFFFFF">06</text>
  <circle cx="880" cy="243" r="20" fill="#FFFFFF" opacity="0.26"/><text x="880" y="251" width="40" text-anchor="middle" font-family="Segoe UI" font-size="18" font-weight="800" fill="#FFFFFF">07</text>
  <circle cx="880" cy="360" r="20" fill="#FFFFFF" opacity="0.26"/><text x="880" y="368" width="40" text-anchor="middle" font-family="Segoe UI" font-size="18" font-weight="800" fill="#FFFFFF">08</text>
  <circle cx="880" cy="477" r="20" fill="#FFFFFF" opacity="0.26"/><text x="880" y="485" width="40" text-anchor="middle" font-family="Segoe UI" font-size="18" font-weight="800" fill="#263238">09</text>
  <circle cx="880" cy="595" r="20" fill="#FFFFFF" opacity="0.30"/><text x="880" y="603" width="40" text-anchor="middle" font-family="Segoe UI" font-size="18" font-weight="800" fill="#263238">10</text>

  <!-- small line-art details inside pills -->
  <path d="M438 117 L458 117 M438 125 L472 125 M438 133 L464 133" stroke="#FFFFFF" stroke-width="4" stroke-linecap="round"/>
  <path d="M438 235 L470 235 M438 243 L458 243 M438 251 L474 251" stroke="#FFFFFF" stroke-width="4" stroke-linecap="round"/>
  <path d="M438 352 L466 352 M438 360 L476 360 M438 368 L458 368" stroke="#FFFFFF" stroke-width="4" stroke-linecap="round"/>
  <path d="M438 469 L468 469 M438 477 L456 477 M438 485 L474 485" stroke="#FFFFFF" stroke-width="4" stroke-linecap="round"/>
  <path d="M438 587 L462 587 M438 595 L476 595 M438 603 L456 603" stroke="#FFFFFF" stroke-width="4" stroke-linecap="round"/>
  <path d="M806 117 L826 117 M806 125 L840 125 M806 133 L832 133" stroke="#FFFFFF" stroke-width="4" stroke-linecap="round"/>
  <path d="M806 235 L838 235 M806 243 L826 243 M806 251 L842 251" stroke="#FFFFFF" stroke-width="4" stroke-linecap="round"/>
  <path d="M806 352 L834 352 M806 360 L844 360 M806 368 L826 368" stroke="#FFFFFF" stroke-width="4" stroke-linecap="round"/>
  <path d="M806 469 L836 469 M806 477 L824 477 M806 485 L842 485" stroke="#FFFFFF" stroke-width="4" stroke-linecap="round"/>
  <path d="M806 587 L830 587 M806 595 L844 595 M806 603 L824 603" stroke="#263238" stroke-width="4" stroke-linecap="round" opacity="0.75"/>

  <!-- left text blocks -->
  <text x="335" y="116" width="250" text-anchor="end" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#546E7A"><tspan font-weight="800" fill="#9C27B0">01 </tspan><tspan font-weight="800" fill="#263238">Customer Trust</tspan><tspan x="335" dy="21" font-size="12" fill="#78909C">Build credibility with clear proof points.</tspan></text>
  <text x="335" y="234" width="250" text-anchor="end" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#546E7A"><tspan font-weight="800" fill="#3F51B5">02 </tspan><tspan font-weight="800" fill="#263238">Market Focus</tspan><tspan x="335" dy="21" font-size="12" fill="#78909C">Prioritize segments where momentum is strongest.</tspan></text>
  <text x="335" y="351" width="250" text-anchor="end" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#546E7A"><tspan font-weight="800" fill="#00BCD4">03 </tspan><tspan font-weight="800" fill="#263238">Digital Flow</tspan><tspan x="335" dy="21" font-size="12" fill="#78909C">Connect data, teams, and decisions seamlessly.</tspan></text>
  <text x="335" y="468" width="250" text-anchor="end" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#546E7A"><tspan font-weight="800" fill="#4CAF50">04 </tspan><tspan font-weight="800" fill="#263238">Operational Fit</tspan><tspan x="335" dy="21" font-size="12" fill="#78909C">Scale repeatable processes without friction.</tspan></text>
  <text x="335" y="586" width="250" text-anchor="end" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#546E7A"><tspan font-weight="800" fill="#8BC34A">05 </tspan><tspan font-weight="800" fill="#263238">Sustainability</tspan><tspan x="335" dy="21" font-size="12" fill="#78909C">Make growth resilient, responsible, and durable.</tspan></text>

  <!-- right text blocks -->
  <text x="945" y="116" width="250" text-anchor="start" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#546E7A"><tspan font-weight="800" fill="#E91E63">06 </tspan><tspan font-weight="800" fill="#263238">Brand Energy</tspan><tspan x="945" dy="21" font-size="12" fill="#78909C">Create memorable moments in every channel.</tspan></text>
  <text x="945" y="234" width="250" text-anchor="start" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#546E7A"><tspan font-weight="800" fill="#F44336">07 </tspan><tspan font-weight="800" fill="#263238">Fast Execution</tspan><tspan x="945" dy="21" font-size="12" fill="#78909C">Shorten cycles from insight to measurable action.</tspan></text>
  <text x="945" y="351" width="250" text-anchor="start" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#546E7A"><tspan font-weight="800" fill="#FF9800">08 </tspan><tspan font-weight="800" fill="#263238">Revenue Lift</tspan><tspan x="945" dy="21" font-size="12" fill="#78909C">Turn priority initiatives into commercial upside.</tspan></text>
  <text x="945" y="468" width="250" text-anchor="start" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#546E7A"><tspan font-weight="800" fill="#FFC107">09 </tspan><tspan font-weight="800" fill="#263238">Partner Reach</tspan><tspan x="945" dy="21" font-size="12" fill="#78909C">Extend capability through a stronger ecosystem.</tspan></text>
  <text x="945" y="586" width="250" text-anchor="start" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#546E7A"><tspan font-weight="800" fill="#FBC02D">10 </tspan><tspan font-weight="800" fill="#263238">Future Options</tspan><tspan x="945" dy="21" font-size="12" fill="#78909C">Keep strategic flexibility as conditions evolve.</tspan></text>
</svg>
```

## Avoid in this skill
- ❌ Using plain thin lines for spokes; the technique depends on thick filled ribbon paths that feel integrated with the node pills.
- ❌ Using arrow markers on paths; if direction is needed, use color sequencing or separate editable line arrows instead.
- ❌ Placing all labels inside the central diagram; it destroys the clean bilateral symmetry and makes the hub area crowded.
- ❌ Applying `clip-path` to spoke paths or node rectangles; clipping is only reliable for images in this workflow.
- ❌ Overusing shadows on every connector; keep the glow subtle so the diagram stays crisp in PowerPoint.

## Composition notes
- Keep the central hub exactly on the slide midpoint and mirror all node y-positions left/right for a balanced executive-infographic look.
- Reserve the outer 25% of each side for explanatory text; keep the middle 50% for the graphic structure.
- Use a cool-to-green palette on the left and warm-to-yellow palette on the right to make the ten items distinct while preserving rhythm.
- Let spokes sit behind the hub and node pills; this overlap makes the geometry feel like a single continuous neural circuit.