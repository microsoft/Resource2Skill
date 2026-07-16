# SVG Recipe — High-Contrast "Dark Anthracite & Vibrant Yellow" Corporate Profile

## Visual mechanism
A deep anthracite canvas is paired with darkened grayscale corporate imagery and a single luminous yellow accent used only for the title, active data bars, metric highlights, and section markers. Data is visualized as bespoke horizontal “signal lines”: thin muted-gray baselines overlaid with thicker yellow progress strokes, creating a premium executive-dashboard feel without using standard charts.

## SVG primitives needed
- 2× `<rect>` for full-slide anthracite background and translucent black image wash
- 1× `<image>` for a dark grayscale architectural / corporate background photo
- 1× `<clipPath>` with rounded `<rect>` for the executive photo card crop
- 1× `<image>` clipped into the rounded photo card
- 1× `<linearGradient>` for subtle anthracite background depth
- 1× `<radialGradient>` for a restrained yellow glow behind the profile metrics
- 1× `<filter id="shadow">` with `feOffset`, `feGaussianBlur`, and `feMerge` applied to cards and the title block
- 1× `<filter id="yellowGlow">` with `feGaussianBlur` applied to yellow emphasis shapes
- 4× `<path>` for angular yellow/charcoal decorative corporate shards
- 8× `<line>` for paired custom horizontal data bars
- 5× `<rect>` for metric cards, yellow pill label, and chart containers
- Multiple `<text>` elements with explicit `width` for headline, labels, numeric metrics, and chart annotations

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="anthraciteDepth" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#181A1D"/>
      <stop offset="58%" stop-color="#212327"/>
      <stop offset="100%" stop-color="#2A2D32"/>
    </linearGradient>

    <radialGradient id="yellowHaze" cx="50%" cy="50%" r="60%">
      <stop offset="0%" stop-color="#FECB0E" stop-opacity="0.34"/>
      <stop offset="55%" stop-color="#FECB0E" stop-opacity="0.10"/>
      <stop offset="100%" stop-color="#FECB0E" stop-opacity="0"/>
    </radialGradient>

    <filter id="shadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="14"/>
      <feGaussianBlur stdDeviation="16"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="yellowGlow" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="10"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <clipPath id="photoCardClip">
      <rect x="884" y="88" width="292" height="424" rx="30" ry="30"/>
    </clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#anthraciteDepth)"/>

  <image href="https://images.example.com/grayscale-corporate-architecture-glass-towers-dark.jpg"
         x="0" y="0" width="1280" height="720" preserveAspectRatio="xMidYMid slice" opacity="0.34"/>
  <rect x="0" y="0" width="1280" height="720" fill="#000000" opacity="0.58"/>

  <circle cx="250" cy="300" r="220" fill="url(#yellowHaze)" opacity="0.75"/>
  <path d="M0 625 L230 570 L290 720 L0 720 Z" fill="#FECB0E" opacity="0.10"/>
  <path d="M1052 0 L1280 0 L1280 170 L1128 132 Z" fill="#FECB0E" opacity="0.16"/>
  <path d="M1010 625 L1280 568 L1280 720 L950 720 Z" fill="#111214" opacity="0.82"/>
  <path d="M756 114 L823 94 L795 154 Z" fill="#FECB0E" opacity="0.95" filter="url(#yellowGlow)"/>

  <text x="74" y="76" width="320" fill="#FECB0E" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="700" letter-spacing="3">
    CORPORATE PROFILE
  </text>

  <text x="72" y="151" width="680" fill="#FFFFFF" font-family="Segoe UI, Microsoft YaHei" font-size="56" font-weight="800" letter-spacing="-1" filter="url(#shadow)">
    STRATEGIC
  </text>
  <text x="72" y="210" width="680" fill="#FFFFFF" font-family="Segoe UI, Microsoft YaHei" font-size="56" font-weight="800" letter-spacing="-1" filter="url(#shadow)">
    OPERATING SNAPSHOT
  </text>

  <rect x="76" y="238" width="282" height="38" rx="19" fill="#FECB0E" filter="url(#yellowGlow)"/>
  <text x="104" y="263" width="230" fill="#000000" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="800" letter-spacing="1.4">
    FY2026 BOARD BRIEF
  </text>

  <text x="76" y="318" width="540" fill="#C8CCD2" font-family="Segoe UI, Microsoft YaHei" font-size="19" font-weight="400">
    Anthracite surfaces, monochrome imagery, and high-voltage yellow highlights focus attention on the indicators that matter.
  </text>

  <rect x="72" y="374" width="170" height="122" rx="22" fill="#2A2D32" opacity="0.94" filter="url(#shadow)"/>
  <rect x="91" y="394" width="38" height="7" rx="3.5" fill="#FECB0E"/>
  <text x="91" y="436" width="130" fill="#FFFFFF" font-family="Segoe UI, Microsoft YaHei" font-size="38" font-weight="800">
    18.7%
  </text>
  <text x="91" y="470" width="126" fill="#AEB4BC" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="600">
    REVENUE CAGR
  </text>

  <rect x="264" y="374" width="170" height="122" rx="22" fill="#2A2D32" opacity="0.94" filter="url(#shadow)"/>
  <rect x="283" y="394" width="38" height="7" rx="3.5" fill="#FECB0E"/>
  <text x="283" y="436" width="130" fill="#FFFFFF" font-family="Segoe UI, Microsoft YaHei" font-size="38" font-weight="800">
    42
  </text>
  <text x="283" y="470" width="126" fill="#AEB4BC" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="600">
    GLOBAL MARKETS
  </text>

  <rect x="456" y="374" width="170" height="122" rx="22" fill="#2A2D32" opacity="0.94" filter="url(#shadow)"/>
  <rect x="475" y="394" width="38" height="7" rx="3.5" fill="#FECB0E"/>
  <text x="475" y="436" width="130" fill="#FFFFFF" font-family="Segoe UI, Microsoft YaHei" font-size="38" font-weight="800">
    $9.4B
  </text>
  <text x="475" y="470" width="126" fill="#AEB4BC" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="600">
    ENTERPRISE VALUE
  </text>

  <rect x="678" y="364" width="470" height="226" rx="28" fill="#1B1D20" opacity="0.92" filter="url(#shadow)"/>
  <text x="714" y="410" width="300" fill="#FFFFFF" font-family="Segoe UI, Microsoft YaHei" font-size="24" font-weight="800">
    PERFORMANCE INDEX
  </text>
  <text x="714" y="435" width="320" fill="#8F969F" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="600" letter-spacing="1.2">
    CUSTOM LINE-BAR DATA VISUALIZATION
  </text>

  <text x="714" y="478" width="120" fill="#DDE1E6" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700">Digital</text>
  <line x1="842" y1="472" x2="1090" y2="472" stroke="#50545A" stroke-width="5" stroke-linecap="round"/>
  <line x1="842" y1="472" x2="1048" y2="472" stroke="#FECB0E" stroke-width="11" stroke-linecap="round"/>
  <text x="1110" y="478" width="44" fill="#FECB0E" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="800">83</text>

  <text x="714" y="517" width="120" fill="#DDE1E6" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700">Margin</text>
  <line x1="842" y1="511" x2="1090" y2="511" stroke="#50545A" stroke-width="5" stroke-linecap="round"/>
  <line x1="842" y1="511" x2="1014" y2="511" stroke="#FECB0E" stroke-width="11" stroke-linecap="round"/>
  <text x="1110" y="517" width="44" fill="#FECB0E" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="800">69</text>

  <text x="714" y="556" width="120" fill="#DDE1E6" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700">Retention</text>
  <line x1="842" y1="550" x2="1090" y2="550" stroke="#50545A" stroke-width="5" stroke-linecap="round"/>
  <line x1="842" y1="550" x2="1070" y2="550" stroke="#FECB0E" stroke-width="11" stroke-linecap="round"/>
  <text x="1110" y="556" width="44" fill="#FECB0E" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="800">92</text>

  <image href="https://images.example.com/grayscale-executive-portrait-in-modern-office.jpg"
         x="884" y="88" width="292" height="424" preserveAspectRatio="xMidYMid slice" clip-path="url(#photoCardClip)" opacity="0.86"/>
  <rect x="884" y="88" width="292" height="424" rx="30" fill="#000000" opacity="0.34"/>
  <rect x="908" y="464" width="196" height="44" rx="22" fill="#FECB0E"/>
  <text x="930" y="493" width="156" fill="#000000" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="900" letter-spacing="1.1">
    CEO MESSAGE
  </text>

  <line x1="72" y1="636" x2="1182" y2="636" stroke="#3B3F45" stroke-width="1"/>
  <text x="74" y="668" width="450" fill="#8F969F" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="600" letter-spacing="1.4">
    CONFIDENTIAL STRATEGY REVIEW  ·  ANTHRACITE / YELLOW SYSTEM
  </text>
  <text x="1032" y="668" width="150" fill="#FECB0E" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="800" text-anchor="end">
    01 / 12
  </text>
</svg>
```

## Avoid in this skill
- ❌ Applying `filter` to `<line>` data bars; the translator drops line filters, so use clean thick yellow strokes instead.
- ❌ Using SVG image filters such as `feColorMatrix` to grayscale the photo; supply an already grayscale/darkened image or overlay it with a translucent black `<rect>`.
- ❌ Using `<mask>` for the cinematic wash; use a normal semi-transparent black rectangle over the image.
- ❌ Using `<pattern>` fills for texture; use real photographic images plus dark overlays for the premium corporate surface.
- ❌ Putting `clip-path` on decorative shapes or cards; clipping is reliable here only for `<image>` crops.

## Composition notes
- Keep the title and primary metrics on the left two-thirds; reserve the right side for a clipped grayscale photo card or executive portrait.
- Use yellow sparingly: section eyebrow, pill label, short metric rules, active data bars, and one or two angular accents.
- Make the background feel cinematic but quiet: dark photo opacity around 25–40%, then add a black overlay around 55–70%.
- Custom chart bars should be simple paired lines: muted gray baseline at 100%, thicker yellow overlay for the actual value.