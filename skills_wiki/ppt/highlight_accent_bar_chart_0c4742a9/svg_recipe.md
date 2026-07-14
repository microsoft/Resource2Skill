# SVG Recipe — Accent Bar Chart

## Visual mechanism
A single vivid bar is isolated against a field of muted neutral bars, using color contrast, a soft glow, and a compact annotation to make the key data point impossible to miss. Minimal gridlines, restrained typography, and generous whitespace keep the chart executive-clean while still providing enough scale context.

## SVG primitives needed
- 1× `<rect>` for the full-slide gradient background
- 1× `<rect>` for a subtle chart card backdrop
- 1× `<rect>` for the translucent vertical accent band behind the highlighted bar
- 6× `<line>` for horizontal value gridlines
- 1× dashed `<line>` for the target/reference threshold
- 6× `<path>` for rounded-top vertical bars
- 1× `<ellipse>` for the soft accent glow behind the highlighted value
- 1× `<rect>` for the annotation pill
- 1× `<line>` for the annotation leader
- 1× `<path>` for the custom arrowhead triangle
- Multiple `<text>` elements for title, subtitle, axis labels, value labels, target label, annotation, and source note
- 3× `<linearGradient>` for background, neutral bars, and accent bar
- 1× `<radialGradient>` for the highlighted bar’s halo
- 2× `<filter>` definitions: one soft shadow for the card/callout, one glow for the accent halo/bar

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#F8FAFC"/>
      <stop offset="100%" stop-color="#EEF3F8"/>
    </linearGradient>

    <linearGradient id="cardGrad" x1="0" y1="130" x2="0" y2="640" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="100%" stop-color="#F7F9FC"/>
    </linearGradient>

    <linearGradient id="barBase" x1="0" y1="205" x2="0" y2="545" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#C7D7EA"/>
      <stop offset="100%" stop-color="#AFC2DC"/>
    </linearGradient>

    <linearGradient id="barAccent" x1="0" y1="252" x2="0" y2="545" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#FFB27C"/>
      <stop offset="100%" stop-color="#F36F45"/>
    </linearGradient>

    <linearGradient id="accentBand" x1="0" y1="160" x2="0" y2="570" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#FFF1E8" stop-opacity="0.85"/>
      <stop offset="100%" stop-color="#FFF1E8" stop-opacity="0"/>
    </linearGradient>

    <radialGradient id="halo" cx="50%" cy="45%" r="60%">
      <stop offset="0%" stop-color="#FF9D66" stop-opacity="0.42"/>
      <stop offset="100%" stop-color="#FF9D66" stop-opacity="0"/>
    </radialGradient>

    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="10"/>
      <feGaussianBlur stdDeviation="14"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="accentGlow" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="12"/>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>

  <text x="70" y="70" width="760" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="700" fill="#243447">
    Market Share by Platform
  </text>
  <text x="72" y="106" width="690" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#6B7785">
    Percentage of active enterprise accounts, Q4 2026
  </text>

  <rect x="64" y="140" width="1152" height="505" rx="28" fill="url(#cardGrad)" filter="url(#softShadow)"/>

  <text x="92" y="182" width="280" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="600" fill="#7A8795">
    SHARE OF ACCOUNTS
  </text>

  <rect x="628" y="188" width="156" height="382" rx="24" fill="url(#accentBand)"/>
  <ellipse cx="706" cy="276" rx="94" ry="64" fill="url(#halo)" filter="url(#accentGlow)"/>

  <line x1="130" y1="205" x2="1130" y2="205" stroke="#DDE4EC" stroke-width="1"/>
  <line x1="130" y1="273" x2="1130" y2="273" stroke="#E3E9F0" stroke-width="1"/>
  <line x1="130" y1="341" x2="1130" y2="341" stroke="#E3E9F0" stroke-width="1"/>
  <line x1="130" y1="409" x2="1130" y2="409" stroke="#E3E9F0" stroke-width="1"/>
  <line x1="130" y1="477" x2="1130" y2="477" stroke="#E3E9F0" stroke-width="1"/>
  <line x1="130" y1="545" x2="1130" y2="545" stroke="#CDD6E0" stroke-width="1.3"/>

  <line x1="130" y1="273" x2="1130" y2="273" stroke="#F36F45" stroke-width="1.6" stroke-dasharray="7 7" opacity="0.72"/>
  <text x="1038" y="263" width="100" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="600" fill="#D85F3B">
    40% target
  </text>

  <text x="94" y="209" width="42" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#84909C" text-anchor="end">50%</text>
  <text x="94" y="277" width="42" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#84909C" text-anchor="end">40%</text>
  <text x="94" y="345" width="42" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#84909C" text-anchor="end">30%</text>
  <text x="94" y="413" width="42" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#84909C" text-anchor="end">20%</text>
  <text x="94" y="481" width="42" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#84909C" text-anchor="end">10%</text>
  <text x="94" y="549" width="42" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#84909C" text-anchor="end">0%</text>

  <path d="M180 545 L180 396 Q180 382 194 382 L258 382 Q272 382 272 396 L272 545 Z" fill="url(#barBase)"/>
  <path d="M340 545 L340 349 Q340 335 354 335 L418 335 Q432 335 432 349 L432 545 Z" fill="url(#barBase)"/>
  <path d="M500 545 L500 369 Q500 355 514 355 L578 355 Q592 355 592 369 L592 545 Z" fill="url(#barBase)"/>
  <path d="M660 545 L660 267 Q660 253 674 253 L738 253 Q752 253 752 267 L752 545 Z" fill="url(#barAccent)" filter="url(#softShadow)"/>
  <path d="M820 545 L820 430 Q820 416 834 416 L898 416 Q912 416 912 430 L912 545 Z" fill="url(#barBase)"/>
  <path d="M980 545 L980 321 Q980 307 994 307 L1058 307 Q1072 307 1072 321 L1072 545 Z" fill="url(#barBase)"/>

  <text x="226" y="371" width="80" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="600" fill="#596675" text-anchor="middle">24%</text>
  <text x="386" y="324" width="80" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="600" fill="#596675" text-anchor="middle">31%</text>
  <text x="546" y="344" width="80" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="600" fill="#596675" text-anchor="middle">28%</text>
  <text x="706" y="238" width="90" font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="800" fill="#E75F38" text-anchor="middle">43%</text>
  <text x="866" y="405" width="80" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="600" fill="#596675" text-anchor="middle">19%</text>
  <text x="1026" y="296" width="80" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="600" fill="#596675" text-anchor="middle">35%</text>

  <text x="226" y="586" width="100" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#596675" text-anchor="middle">Nova</text>
  <text x="386" y="586" width="100" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#596675" text-anchor="middle">Atlas</text>
  <text x="546" y="586" width="100" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#596675" text-anchor="middle">Zenith</text>
  <text x="706" y="586" width="100" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="800" fill="#E75F38" text-anchor="middle">Acme</text>
  <text x="866" y="586" width="100" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#596675" text-anchor="middle">Orion</text>
  <text x="1026" y="586" width="100" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#596675" text-anchor="middle">Pulse</text>

  <rect x="814" y="214" width="230" height="74" rx="18" fill="#FFFFFF" filter="url(#softShadow)"/>
  <text x="836" y="244" width="188" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#243447">
    Acme leads the field
  </text>
  <text x="836" y="267" width="190" font-family="Segoe UI, Microsoft YaHei" font-size="12.5" fill="#6B7785">
    8 pts above nearest competitor
  </text>
  <line x1="814" y1="268" x2="755" y2="276" stroke="#F36F45" stroke-width="2"/>
  <path d="M752 276 L765 269 L765 283 Z" fill="#F36F45"/>

  <text x="970" y="680" width="240" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#98A3AF">
    Source: Enterprise account survey
  </text>
</svg>
```

## Avoid in this skill
- ❌ Using a different bright color for every bar; it destroys the isolation effect.
- ❌ Heavy chart borders, legends, or axis lines; the emphasis should come from the accent bar, not chart furniture.
- ❌ `marker-end` on paths for annotation arrows; use a `<line>` plus a small triangular `<path>` arrowhead.
- ❌ Applying filters to grid `<line>` elements; shadows/glows should be reserved for the highlighted bar, card, or annotation.
- ❌ Clipping or masking non-image elements to create bars; use editable `<rect>` or `<path>` bar shapes instead.

## Composition notes
- Keep the title and subtitle in the upper-left, then let the chart occupy the central 70–80% of the slide width.
- Use muted bars for the baseline series and reserve the warm accent color for exactly one data point.
- Place value labels just above bars; enlarge or embolden only the highlighted value label.
- Add a small annotation near the highlighted bar, but keep it secondary to the bar itself.