# SVG Recipe — The Single-Message KPI Knockout (Hero Metric + Funnel Breakdown)

## Visual mechanism
A massive, high-contrast hero metric dominates the slide, while a restrained funnel breakdown explains the drivers without competing for attention. The layout uses executive-keynote hierarchy: one memorable number first, then progressively narrowing funnel stages as the proof layer.

## SVG primitives needed
- 1× `<rect>` for the full-slide background
- 2× `<radialGradient>` / `<linearGradient>` for premium blue depth and gold funnel fills
- 1× `<filter id="softShadow">` applied to funnel blocks and KPI badge elements
- 1× `<filter id="glow">` applied to the hero metric aura
- 3× `<circle>` / `<ellipse>` for subtle spotlight and KPI glow accents
- 4× `<path>` for descending trapezoid funnel stages
- 1× `<line>` for the vertical funnel center spine
- 12× `<text>` elements for hero metric, labels, funnel values, and step descriptions
- 3× `<rect>` for small annotation pills and separator accents

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgBlue" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#0B2545"/>
      <stop offset="55%" stop-color="#0D3B66"/>
      <stop offset="100%" stop-color="#1F8CCC"/>
    </linearGradient>

    <radialGradient id="heroGlow" cx="38%" cy="47%" r="42%">
      <stop offset="0%" stop-color="#FFC000" stop-opacity="0.38"/>
      <stop offset="55%" stop-color="#FFC000" stop-opacity="0.08"/>
      <stop offset="100%" stop-color="#FFC000" stop-opacity="0"/>
    </radialGradient>

    <linearGradient id="goldFunnel" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#FFE08A"/>
      <stop offset="48%" stop-color="#FFC000"/>
      <stop offset="100%" stop-color="#C98200"/>
    </linearGradient>

    <linearGradient id="blueGlass" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.18"/>
      <stop offset="100%" stop-color="#FFFFFF" stop-opacity="0.04"/>
    </linearGradient>

    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="160%">
      <feOffset dx="0" dy="12"/>
      <feGaussianBlur stdDeviation="14"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="glow" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="18"/>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgBlue)"/>
  <ellipse cx="460" cy="345" rx="420" ry="300" fill="url(#heroGlow)" filter="url(#glow)"/>
  <circle cx="1080" cy="110" r="190" fill="#FFFFFF" opacity="0.05"/>
  <circle cx="1190" cy="650" r="280" fill="#000000" opacity="0.10"/>

  <text x="80" y="86" width="520" font-family="Segoe UI, Microsoft YaHei" font-size="22" font-weight="600" fill="#FFFFFF" opacity="0.82" letter-spacing="2">
    Q4 GROWTH SNAPSHOT
  </text>

  <rect x="80" y="112" width="84" height="5" rx="2.5" fill="#FFC000"/>
  <text x="80" y="202" width="610" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="300" fill="#FFFFFF" opacity="0.94">
    One message the board should remember
  </text>

  <text x="76" y="370" width="660" font-family="Segoe UI, Microsoft YaHei" font-size="126" font-weight="800" fill="#FFC000">
    $1.1M
  </text>
  <text x="92" y="430" width="500" font-family="Segoe UI, Microsoft YaHei" font-size="42" font-weight="300" fill="#FFFFFF">
    weekly sales
  </text>

  <rect x="88" y="474" width="330" height="48" rx="24" fill="url(#blueGlass)" stroke="#FFFFFF" stroke-opacity="0.22"/>
  <text x="116" y="506" width="290" font-family="Segoe UI, Microsoft YaHei" font-size="19" font-weight="600" fill="#FFFFFF">
    +38% vs. prior quarter
  </text>

  <text x="82" y="610" width="560" font-family="Segoe UI, Microsoft YaHei" font-size="24" font-weight="300" fill="#DDEEFF" opacity="0.92">
    Start with the outcome. Then reveal the conversion path that produced it.
  </text>

  <rect x="714" y="78" width="470" height="564" rx="34" fill="#FFFFFF" opacity="0.08" stroke="#FFFFFF" stroke-opacity="0.18"/>
  <text x="754" y="138" width="390" font-family="Segoe UI, Microsoft YaHei" font-size="30" font-weight="700" fill="#FFFFFF">
    Drivers behind the number
  </text>
  <text x="754" y="172" width="360" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="400" fill="#DDEEFF" opacity="0.86">
    Funnel proof, sequenced from attention to revenue.
  </text>

  <line x1="950" y1="225" x2="950" y2="560" stroke="#FFFFFF" stroke-opacity="0.22" stroke-width="2" stroke-dasharray="8 10"/>

  <path d="M770 220 L1130 220 L1095 292 L805 292 Z" fill="url(#goldFunnel)" filter="url(#softShadow)"/>
  <text x="812" y="260" width="170" font-family="Segoe UI, Microsoft YaHei" font-size="28" font-weight="800" fill="#0B2545">
    330K
  </text>
  <text x="960" y="260" width="155" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="600" fill="#0B2545">
    social engagements
  </text>

  <path d="M815 318 L1085 318 L1052 390 L848 390 Z" fill="#FFFFFF" opacity="0.92" filter="url(#softShadow)"/>
  <text x="858" y="358" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="28" font-weight="800" fill="#0D3B66">
    44K
  </text>
  <text x="980" y="358" width="105" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="600" fill="#0D3B66">
    new visitors
  </text>

  <path d="M858 416 L1042 416 L1014 488 L886 488 Z" fill="#DDEEFF" opacity="0.96" filter="url(#softShadow)"/>
  <text x="892" y="456" width="120" font-family="Segoe UI, Microsoft YaHei" font-size="28" font-weight="800" fill="#0D3B66">
    323%
  </text>
  <text x="980" y="456" width="76" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="600" fill="#0D3B66">
    lead lift
  </text>

  <path d="M895 514 L1005 514 L982 572 L918 572 Z" fill="#FFC000" opacity="0.98" filter="url(#softShadow)"/>
  <text x="912" y="550" width="85" font-family="Segoe UI, Microsoft YaHei" font-size="24" font-weight="800" fill="#0B2545">
    $1.1M
  </text>

  <rect x="744" y="602" width="196" height="32" rx="16" fill="#FFFFFF" opacity="0.14"/>
  <text x="762" y="624" width="160" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="600" fill="#FFFFFF" opacity="0.86">
    funnel narrows by intent
  </text>
</svg>
```

## Avoid in this skill
- ❌ Dense KPI grids that dilute the “single-message” hierarchy
- ❌ Equal-sized funnel bars; the visual point is sequential narrowing
- ❌ Low-contrast metric colors against the background
- ❌ Placing long paragraphs near the hero number
- ❌ Using `marker-end` arrows on paths; use simple lines or native shapes instead
- ❌ Clipping or masking non-image funnel shapes; use editable `<path>` trapezoids

## Composition notes
- Keep the hero metric on the left or center with extreme scale; it should be readable from the back of a room.
- Reserve the right side for the funnel proof layer, using descending widths and a shared center axis.
- Use one accent color for the hero number and the top/bottom funnel stages to create a clear narrative thread.
- Maintain generous negative space around the hero metric; the funnel should support the story, not become a dashboard.