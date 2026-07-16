# SVG Recipe — Metric Dashboard Split

## Visual mechanism
A cool corporate split-screen layout: dense metric storytelling in a left column, balanced by a large rounded hero image on the right. The dashboard feel comes from layered metric cards, accent progress bars, small status chips, and subtle technical linework that points attention toward the image.

## SVG primitives needed
- 1× `<rect>` for the dark slide background
- 2× `<linearGradient>` for background depth and metric progress fills
- 1× `<radialGradient>` for a cool glow behind the hero image
- 1× `<filter id="softShadow">` applied to cards and the image frame
- 1× `<filter id="glow">` applied to decorative accent paths/circles
- 1× `<clipPath>` with rounded `<rect>` for the hero image crop
- 1× `<image>` for the right-side hero photo
- 8× `<rect>` for cards, progress tracks, progress fills, chips, and image frame
- 4× `<circle>` for KPI dots, progress endpoints, and decorative glow nodes
- 5× `<path>` for decorative technical curves, dividers, and small icon marks
- 1× `<line>` for the vertical split rule
- Multiple `<text>` elements with explicit `width` for headline, metric labels, values, and annotations

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1280" y2="720">
      <stop offset="0%" stop-color="#07111F"/>
      <stop offset="55%" stop-color="#0B1726"/>
      <stop offset="100%" stop-color="#101D31"/>
    </linearGradient>

    <linearGradient id="cyanGrad" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#35D8FF"/>
      <stop offset="52%" stop-color="#4D7CFF"/>
      <stop offset="100%" stop-color="#8B5CFF"/>
    </linearGradient>

    <linearGradient id="limeGrad" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#8DFFB3"/>
      <stop offset="100%" stop-color="#28D7C4"/>
    </linearGradient>

    <radialGradient id="heroGlow" cx="50%" cy="50%" r="60%">
      <stop offset="0%" stop-color="#2AD4FF" stop-opacity="0.34"/>
      <stop offset="100%" stop-color="#2AD4FF" stop-opacity="0"/>
    </radialGradient>

    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feOffset dx="0" dy="18"/>
      <feGaussianBlur stdDeviation="18"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="glow" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="5"/>
    </filter>

    <clipPath id="heroClip">
      <rect x="704" y="92" width="480" height="536" rx="34"/>
    </clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>
  <circle cx="912" cy="360" r="360" fill="url(#heroGlow)"/>

  <path d="M70 585 C210 520 310 620 455 548 S660 490 742 565" fill="none" stroke="#183655" stroke-width="2" opacity="0.65"/>
  <path d="M632 104 C673 152 673 229 632 278" fill="none" stroke="#2AD4FF" stroke-width="2" opacity="0.35" stroke-dasharray="8 10"/>
  <line x1="636" y1="86" x2="636" y2="636" stroke="#264158" stroke-width="1.4" opacity="0.7"/>

  <text x="78" y="88" width="160" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" letter-spacing="2.8" fill="#5BD9FF">Q4 OPERATING VIEW</text>
  <text x="78" y="152" width="500" font-family="Segoe UI, Microsoft YaHei" font-size="47" font-weight="750" fill="#F4F8FF">
    <tspan x="78" dy="0">Growth signal</tspan>
    <tspan x="78" dy="54">is compounding</tspan>
  </text>
  <text x="80" y="276" width="462" font-family="Segoe UI, Microsoft YaHei" font-size="18" fill="#AAB7C8">
    Two leading indicators moved ahead of forecast, while activation efficiency held above the threshold for scaled investment.
  </text>

  <rect x="78" y="342" width="496" height="116" rx="24" fill="#0F2235" stroke="#203A53" stroke-width="1.2" filter="url(#softShadow)"/>
  <rect x="102" y="366" width="62" height="28" rx="14" fill="#123A4F"/>
  <circle cx="119" cy="380" r="5" fill="#35D8FF" filter="url(#glow)"/>
  <text x="135" y="385" width="120" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#8AEAFF">PIPELINE</text>
  <text x="104" y="428" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="40" font-weight="760" fill="#FFFFFF">+28%</text>
  <text x="252" y="397" width="270" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="650" fill="#DCE8F6">Enterprise qualified demand</text>
  <text x="252" y="423" width="260" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#8FA2B9">Ahead of quarterly plan by 6.4 pts</text>
  <rect x="252" y="440" width="276" height="8" rx="4" fill="#1B3347"/>
  <rect x="252" y="440" width="214" height="8" rx="4" fill="url(#cyanGrad)"/>
  <circle cx="466" cy="444" r="7" fill="#35D8FF"/>

  <rect x="78" y="486" width="496" height="116" rx="24" fill="#0E2030" stroke="#203A53" stroke-width="1.2" filter="url(#softShadow)"/>
  <rect x="102" y="510" width="72" height="28" rx="14" fill="#173C35"/>
  <circle cx="119" cy="524" r="5" fill="#8DFFB3" filter="url(#glow)"/>
  <text x="135" y="529" width="130" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#B9FFD0">ADOPTION</text>
  <text x="104" y="572" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="40" font-weight="760" fill="#FFFFFF">74%</text>
  <text x="252" y="541" width="270" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="650" fill="#DCE8F6">Weekly active accounts</text>
  <text x="252" y="567" width="270" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#8FA2B9">Retention corridor remains stable</text>
  <rect x="252" y="584" width="276" height="8" rx="4" fill="#1B3347"/>
  <rect x="252" y="584" width="188" height="8" rx="4" fill="url(#limeGrad)"/>
  <circle cx="440" cy="588" r="7" fill="#8DFFB3"/>

  <rect x="694" y="82" width="500" height="556" rx="42" fill="#0B1523" stroke="#2B4763" stroke-width="1.3" filter="url(#softShadow)"/>
  <image x="704" y="92" width="480" height="536" preserveAspectRatio="xMidYMid slice" clip-path="url(#heroClip)" href="https://images.example.com/hero-photo-data-operations-team-in-blue-control-room.jpg"/>
  <rect x="704" y="92" width="480" height="536" rx="34" fill="#07111F" opacity="0.18"/>
  <rect x="734" y="548" width="244" height="54" rx="18" fill="#081523" opacity="0.84" stroke="#33516B"/>
  <text x="758" y="581" width="210" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#FFFFFF">Live ops cockpit</text>
  <text x="758" y="598" width="210" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#9DB0C4">North America · 14 markets</text>

  <path d="M1043 126 L1086 126 L1108 148 L1150 148" fill="none" stroke="#35D8FF" stroke-width="2.2" opacity="0.75"/>
  <path d="M1043 126 L1031 138 L1043 150" fill="none" stroke="#35D8FF" stroke-width="2.2" opacity="0.75"/>
  <circle cx="1150" cy="148" r="5" fill="#35D8FF"/>
  <path d="M716 150 C760 118 836 116 884 148" fill="none" stroke="#FFFFFF" stroke-width="1.5" opacity="0.28" stroke-dasharray="5 8"/>
</svg>
```

## Avoid in this skill
- ❌ Do not build the hero side from many small rectangles; use a real clipped `<image>` so the slide feels premium.
- ❌ Do not apply `clip-path` to overlay rectangles or decorative shapes; only clip the `<image>`.
- ❌ Do not rely on `<foreignObject>` for metric cards or rich text blocks; use native `<text>` and `<tspan>`.
- ❌ Do not use marker arrows on paths for callouts; if arrows are needed, use native `<line>` with marker attributes directly on the line, or draw arrowheads as small paths.
- ❌ Avoid flat white dashboard cards on a dark split layout; use translucent dark cards, thin strokes, gradients, and glow accents for depth.

## Composition notes
- Keep the left column to roughly 45% of the slide width: headline on top, two metric cards stacked below.
- Reserve the right 40–42% for the rounded hero image; it should be taller than the metric stack and act as the visual anchor.
- Use one bright accent family for the first metric and a secondary accent for the second metric to create clear KPI hierarchy.
- Maintain generous negative space between the headline and cards so the slide reads as an executive summary, not a dense analytics screen.