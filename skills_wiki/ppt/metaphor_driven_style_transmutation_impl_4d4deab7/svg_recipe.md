# SVG Recipe — Premium Glassmorphism Keynote Style

## Visual mechanism
A deep navy, gradient-lit stage is layered with translucent rounded “glass” panels, soft glow fields, hairline borders, and precise high-contrast typography. The illusion comes from stacked opacity, blurred ambient color behind cards, and crisp UI-like alignment rather than heavy decoration.

## SVG primitives needed
- 1× `<rect>` for the full-slide dark gradient background
- 4× `<ellipse>` for blurred cyan/violet ambient glow fields behind the glass
- 6× `<rect>` for frosted-glass cards, micro-panels, and translucent UI surfaces
- 5× `<path>` for decorative network curves, sparklines, and premium data-visual strokes
- 11× `<circle>` for status dots, metric icons, chart nodes, and connection points
- 4× `<line>` for thin UI dividers and subtle architecture connectors
- 15× `<text>` elements with explicit `width=` for editable title, labels, metrics, and body copy
- 3× `<linearGradient>` for background, glass surface, and accent strokes
- 2× `<radialGradient>` for soft luminous color pools
- 2× `<filter>` definitions: one shadow filter for glass cards, one blur/glow filter for ambient light and accent strokes

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgDeep" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#070B16"/>
      <stop offset="45%" stop-color="#0D111C"/>
      <stop offset="100%" stop-color="#111827"/>
    </linearGradient>

    <radialGradient id="cyanPool" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#00BFFF" stop-opacity="0.65"/>
      <stop offset="70%" stop-color="#00BFFF" stop-opacity="0.12"/>
      <stop offset="100%" stop-color="#00BFFF" stop-opacity="0"/>
    </radialGradient>

    <radialGradient id="violetPool" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#7C3AED" stop-opacity="0.55"/>
      <stop offset="72%" stop-color="#7C3AED" stop-opacity="0.11"/>
      <stop offset="100%" stop-color="#7C3AED" stop-opacity="0"/>
    </radialGradient>

    <linearGradient id="glassFill" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.20"/>
      <stop offset="48%" stop-color="#FFFFFF" stop-opacity="0.075"/>
      <stop offset="100%" stop-color="#FFFFFF" stop-opacity="0.035"/>
    </linearGradient>

    <linearGradient id="edgeLine" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.62"/>
      <stop offset="45%" stop-color="#7DD3FC" stop-opacity="0.24"/>
      <stop offset="100%" stop-color="#FFFFFF" stop-opacity="0.12"/>
    </linearGradient>

    <filter id="glassShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="18" in="SourceAlpha" result="off"/>
      <feGaussianBlur in="off" stdDeviation="18" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="softGlow" x="-60%" y="-60%" width="220%" height="220%">
      <feGaussianBlur stdDeviation="26"/>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgDeep)"/>

  <ellipse cx="220" cy="120" rx="260" ry="150" fill="url(#cyanPool)" filter="url(#softGlow)"/>
  <ellipse cx="1060" cy="155" rx="300" ry="170" fill="url(#violetPool)" filter="url(#softGlow)"/>
  <ellipse cx="970" cy="640" rx="360" ry="125" fill="url(#cyanPool)" opacity="0.55" filter="url(#softGlow)"/>
  <ellipse cx="430" cy="600" rx="260" ry="110" fill="url(#violetPool)" opacity="0.42" filter="url(#softGlow)"/>

  <path d="M84 210 C230 132, 352 264, 514 182 S840 90, 1046 230 S1190 310, 1238 250"
        fill="none" stroke="#38BDF8" stroke-width="1.3" stroke-opacity="0.24" stroke-dasharray="8 14"/>
  <path d="M96 560 C272 490, 350 622, 542 548 S826 432, 1040 516 S1190 620, 1246 558"
        fill="none" stroke="#A78BFA" stroke-width="1.1" stroke-opacity="0.22" stroke-dasharray="5 12"/>

  <rect x="70" y="62" width="1140" height="178" rx="34" fill="url(#glassFill)" stroke="url(#edgeLine)" stroke-width="1.5" filter="url(#glassShadow)"/>
  <text x="116" y="118" width="720" font-family="Segoe UI, Microsoft YaHei" font-size="18" fill="#7DD3FC" letter-spacing="3">PRODUCT INTELLIGENCE CLOUD</text>
  <text x="112" y="174" width="760" font-family="Segoe UI, Microsoft YaHei" font-size="54" font-weight="700" fill="#FFFFFF">Glass UI for executive clarity</text>
  <text x="116" y="216" width="760" font-family="Segoe UI, Microsoft YaHei" font-size="21" fill="#CBD5E1">Turn dense SaaS metrics into a premium keynote interface with spatial hierarchy, calm depth, and luminous focus.</text>

  <rect x="920" y="94" width="238" height="104" rx="24" fill="#FFFFFF" fill-opacity="0.08" stroke="#FFFFFF" stroke-opacity="0.24"/>
  <circle cx="962" cy="145" r="18" fill="#00BFFF" fill-opacity="0.22" stroke="#67E8F9" stroke-width="1.2"/>
  <circle cx="962" cy="145" r="6" fill="#67E8F9"/>
  <text x="994" y="133" width="140" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#94A3B8">Live signal</text>
  <text x="994" y="166" width="140" font-family="Segoe UI, Microsoft YaHei" font-size="32" font-weight="700" fill="#FFFFFF">98.7%</text>

  <rect x="70" y="286" width="350" height="300" rx="32" fill="url(#glassFill)" stroke="url(#edgeLine)" stroke-width="1.3" filter="url(#glassShadow)"/>
  <text x="108" y="342" width="270" font-family="Segoe UI, Microsoft YaHei" font-size="18" fill="#94A3B8">Adoption velocity</text>
  <text x="108" y="404" width="270" font-family="Segoe UI, Microsoft YaHei" font-size="62" font-weight="700" fill="#FFFFFF">+42%</text>
  <text x="112" y="440" width="260" font-family="Segoe UI, Microsoft YaHei" font-size="18" fill="#67E8F9">Quarter over quarter</text>
  <path d="M112 520 C150 486, 178 506, 216 468 S292 442, 344 392"
        fill="none" stroke="#22D3EE" stroke-width="5" stroke-linecap="round" filter="url(#softGlow)"/>
  <path d="M112 520 C150 486, 178 506, 216 468 S292 442, 344 392"
        fill="none" stroke="#A5F3FC" stroke-width="2.2" stroke-linecap="round"/>
  <circle cx="344" cy="392" r="6.5" fill="#FFFFFF" stroke="#22D3EE" stroke-width="3"/>

  <rect x="465" y="286" width="350" height="300" rx="32" fill="url(#glassFill)" stroke="url(#edgeLine)" stroke-width="1.3" filter="url(#glassShadow)"/>
  <text x="505" y="342" width="260" font-family="Segoe UI, Microsoft YaHei" font-size="18" fill="#94A3B8">Architecture map</text>
  <text x="505" y="386" width="260" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="700" fill="#FFFFFF">Secure data plane</text>
  <line x1="562" y1="470" x2="718" y2="470" stroke="#67E8F9" stroke-width="1.6" stroke-opacity="0.58"/>
  <line x1="640" y1="424" x2="640" y2="524" stroke="#67E8F9" stroke-width="1.6" stroke-opacity="0.40"/>
  <circle cx="562" cy="470" r="30" fill="#FFFFFF" fill-opacity="0.09" stroke="#FFFFFF" stroke-opacity="0.32"/>
  <circle cx="640" cy="424" r="30" fill="#FFFFFF" fill-opacity="0.09" stroke="#FFFFFF" stroke-opacity="0.32"/>
  <circle cx="718" cy="470" r="30" fill="#FFFFFF" fill-opacity="0.09" stroke="#FFFFFF" stroke-opacity="0.32"/>
  <circle cx="640" cy="524" r="30" fill="#00BFFF" fill-opacity="0.18" stroke="#67E8F9" stroke-opacity="0.8"/>
  <text x="535" y="575" width="210" font-family="Segoe UI, Microsoft YaHei" font-size="16" fill="#CBD5E1">Encrypted ingestion, routing, and inference orchestration.</text>

  <rect x="860" y="286" width="350" height="300" rx="32" fill="url(#glassFill)" stroke="url(#edgeLine)" stroke-width="1.3" filter="url(#glassShadow)"/>
  <text x="900" y="342" width="260" font-family="Segoe UI, Microsoft YaHei" font-size="18" fill="#94A3B8">Operating leverage</text>
  <text x="900" y="402" width="260" font-family="Segoe UI, Microsoft YaHei" font-size="58" font-weight="700" fill="#FFFFFF">3.8×</text>
  <text x="900" y="438" width="260" font-family="Segoe UI, Microsoft YaHei" font-size="18" fill="#67E8F9">Automation impact</text>
  <rect x="902" y="488" width="48" height="56" rx="10" fill="#22D3EE" fill-opacity="0.35"/>
  <rect x="966" y="456" width="48" height="88" rx="10" fill="#22D3EE" fill-opacity="0.50"/>
  <rect x="1030" y="420" width="48" height="124" rx="10" fill="#22D3EE" fill-opacity="0.68"/>
  <rect x="1094" y="382" width="48" height="162" rx="10" fill="#FFFFFF" fill-opacity="0.20" stroke="#67E8F9" stroke-opacity="0.58"/>

  <rect x="210" y="624" width="860" height="46" rx="23" fill="#FFFFFF" fill-opacity="0.07" stroke="#FFFFFF" stroke-opacity="0.16"/>
  <circle cx="246" cy="647" r="6" fill="#22C55E"/>
  <text x="268" y="654" width="270" font-family="Segoe UI, Microsoft YaHei" font-size="16" fill="#CBD5E1">Board-ready narrative</text>
  <circle cx="558" cy="647" r="6" fill="#38BDF8"/>
  <text x="580" y="654" width="270" font-family="Segoe UI, Microsoft YaHei" font-size="16" fill="#CBD5E1">Editable native PPT shapes</text>
  <circle cx="890" cy="647" r="6" fill="#A78BFA"/>
  <text x="912" y="654" width="130" font-family="Segoe UI, Microsoft YaHei" font-size="16" fill="#CBD5E1">Premium depth</text>
</svg>
```

## Avoid in this skill
- ❌ Using actual SVG `backdrop-filter` or masks to blur content behind cards; PowerPoint translation will not preserve that behavior.
- ❌ Applying `filter` to `<line>` connectors; use filters only on rects, circles, ellipses, paths, or text.
- ❌ Opaque white cards; they destroy the glass effect. Keep fills around 4–20% opacity with a brighter 15–60% opacity stroke.
- ❌ Dense grids, thick borders, or saturated backgrounds; glassmorphism needs restraint and negative space.
- ❌ Text without explicit `width=`; PowerPoint will not size editable text reliably.

## Composition notes
- Keep the slide background dark and immersive; place large blurred cyan/violet glow fields behind the cards to imply depth.
- Use one dominant hero glass panel in the upper third, then 3 aligned metric cards below for an executive dashboard rhythm.
- Reserve pure white for headline numbers and titles; use cyan for signals, trends, and “live” emphasis.
- Cards should breathe: generous padding, rounded corners around 24–36 px, and thin luminous borders create the premium keynote feel.