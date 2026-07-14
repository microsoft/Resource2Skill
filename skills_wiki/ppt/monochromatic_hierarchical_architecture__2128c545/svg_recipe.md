# SVG Recipe — Monochromatic Architecture Diagram

## Visual mechanism
A complex architecture is clarified by nesting rounded containers and nodes in progressively darker tints of one hue. Visual hierarchy comes from tonal weight, border style, spacing, and curved flow lines rather than many competing colors.

## SVG primitives needed
- 1× `<rect>` for the slide background
- 3× large rounded `<rect>` elements for hierarchical architecture containers
- 10× medium rounded `<rect>` elements for services, domains, and infrastructure blocks
- 12× small rounded `<rect>` elements for submodules inside service domains
- 8× `<path>` elements for smooth architecture connectors and decorative background contour lines
- 1× `<linearGradient>` for the soft monochrome slide background
- 3× `<linearGradient>` definitions for dark, medium, and light teal fills
- 1× `<radialGradient>` for a subtle architectural glow behind the system
- 2× `<filter>` definitions: one soft shadow for cards, one glow for highlighted connectors
- Multiple `<text>` elements with explicit `width` attributes for titles, labels, node names, and annotations

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgWash" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#F7FBFB"/>
      <stop offset="55%" stop-color="#EEF6F6"/>
      <stop offset="100%" stop-color="#E3F0F0"/>
    </linearGradient>
    <radialGradient id="systemGlow" cx="50%" cy="42%" r="58%">
      <stop offset="0%" stop-color="#7EB9BA" stop-opacity="0.34"/>
      <stop offset="62%" stop-color="#7EB9BA" stop-opacity="0.10"/>
      <stop offset="100%" stop-color="#7EB9BA" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="darkTeal" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#1F5557"/>
      <stop offset="100%" stop-color="#2C6668"/>
    </linearGradient>
    <linearGradient id="medTeal" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#4F8F91"/>
      <stop offset="100%" stop-color="#6EA8AA"/>
    </linearGradient>
    <linearGradient id="lightTeal" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#C9DFE0"/>
      <stop offset="100%" stop-color="#A8CBCC"/>
    </linearGradient>
    <filter id="cardShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="8" result="off"/>
      <feGaussianBlur in="off" stdDeviation="10" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="connectorGlow" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="3"/>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgWash)"/>
  <circle cx="650" cy="356" r="430" fill="url(#systemGlow)"/>

  <path d="M56 166 C160 92, 278 92, 390 150 C505 210, 640 210, 775 146 C912 82, 1052 98, 1190 170" fill="none" stroke="#2C6668" stroke-opacity="0.08" stroke-width="2"/>
  <path d="M64 545 C206 470, 346 488, 468 552 C590 616, 728 616, 850 548 C980 476, 1115 478, 1218 540" fill="none" stroke="#2C6668" stroke-opacity="0.08" stroke-width="2"/>
  <path d="M102 242 C250 197, 360 214, 490 272 C612 326, 774 326, 912 264 C1034 209, 1136 204, 1210 232" fill="none" stroke="#2C6668" stroke-opacity="0.06" stroke-width="1.5"/>

  <text x="72" y="64" width="760" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="700" fill="#214F51">Monochromatic Platform Architecture</text>
  <text x="74" y="96" width="620" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#527678">One hue, four tonal levels: environment → domains → services → capabilities</text>

  <rect x="1010" y="50" width="178" height="94" rx="22" fill="#FFFFFF" stroke="#B8D2D3" stroke-width="1.5" filter="url(#cardShadow)"/>
  <text x="1030" y="82" width="140" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#2C6668">TONAL KEY</text>
  <rect x="1030" y="96" width="24" height="12" rx="6" fill="#2C6668"/>
  <text x="1062" y="107" width="100" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#496B6C">Core layer</text>
  <rect x="1030" y="118" width="24" height="12" rx="6" fill="#6EA8AA"/>
  <text x="1062" y="129" width="100" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#496B6C">Service layer</text>

  <rect x="160" y="120" width="960" height="86" rx="30" fill="url(#darkTeal)" filter="url(#cardShadow)"/>
  <text x="640" y="155" width="660" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="24" font-weight="700" fill="#FFFFFF">Customer Experience Gateway</text>
  <text x="640" y="182" width="700" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#DCEEEE">Web, mobile, partner API, identity entry points</text>

  <rect x="94" y="245" width="1092" height="220" rx="28" fill="#EDF6F6" stroke="#2C6668" stroke-width="2"/>
  <text x="122" y="282" width="280" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="700" fill="#2C6668">Application & Domain Services</text>
  <text x="910" y="282" width="230" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#5A7A7B">Level 2: grouped by business capability</text>

  <rect x="142" y="310" width="290" height="116" rx="22" fill="url(#medTeal)" filter="url(#cardShadow)"/>
  <text x="287" y="342" width="220" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="700" fill="#FFFFFF">Commerce Domain</text>
  <rect x="166" y="362" width="74" height="34" rx="14" fill="url(#lightTeal)"/>
  <rect x="250" y="362" width="74" height="34" rx="14" fill="url(#lightTeal)"/>
  <rect x="334" y="362" width="74" height="34" rx="14" fill="url(#lightTeal)"/>
  <text x="203" y="384" width="60" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="11" font-weight="700" fill="#244D4F">Catalog</text>
  <text x="287" y="384" width="60" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="11" font-weight="700" fill="#244D4F">Orders</text>
  <text x="371" y="384" width="60" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="11" font-weight="700" fill="#244D4F">Pricing</text>

  <rect x="495" y="310" width="290" height="116" rx="22" fill="url(#medTeal)" filter="url(#cardShadow)"/>
  <text x="640" y="342" width="230" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="700" fill="#FFFFFF">Intelligence Domain</text>
  <rect x="519" y="362" width="74" height="34" rx="14" fill="url(#lightTeal)"/>
  <rect x="603" y="362" width="74" height="34" rx="14" fill="url(#lightTeal)"/>
  <rect x="687" y="362" width="74" height="34" rx="14" fill="url(#lightTeal)"/>
  <text x="556" y="384" width="60" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="11" font-weight="700" fill="#244D4F">Models</text>
  <text x="640" y="384" width="60" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="11" font-weight="700" fill="#244D4F">Rules</text>
  <text x="724" y="384" width="60" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="11" font-weight="700" fill="#244D4F">Insights</text>

  <rect x="848" y="310" width="290" height="116" rx="22" fill="url(#medTeal)" filter="url(#cardShadow)"/>
  <text x="993" y="342" width="220" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="700" fill="#FFFFFF">Integration Domain</text>
  <rect x="872" y="362" width="74" height="34" rx="14" fill="url(#lightTeal)"/>
  <rect x="956" y="362" width="74" height="34" rx="14" fill="url(#lightTeal)"/>
  <rect x="1040" y="362" width="74" height="34" rx="14" fill="url(#lightTeal)"/>
  <text x="909" y="384" width="60" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="11" font-weight="700" fill="#244D4F">Events</text>
  <text x="993" y="384" width="60" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="11" font-weight="700" fill="#244D4F">APIs</text>
  <text x="1077" y="384" width="60" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="11" font-weight="700" fill="#244D4F">Queues</text>

  <path d="M640 206 C640 232, 287 235, 287 310" fill="none" stroke="#2C6668" stroke-width="3" stroke-linecap="round" stroke-opacity="0.45"/>
  <path d="M640 206 C640 236, 640 252, 640 310" fill="none" stroke="#2C6668" stroke-width="4" stroke-linecap="round" stroke-opacity="0.55" filter="url(#connectorGlow)"/>
  <path d="M640 206 C640 232, 993 235, 993 310" fill="none" stroke="#2C6668" stroke-width="3" stroke-linecap="round" stroke-opacity="0.45"/>

  <rect x="94" y="505" width="1092" height="142" rx="28" fill="#F5FAFA" stroke="#2C6668" stroke-width="2" stroke-dasharray="9 8"/>
  <text x="122" y="542" width="280" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="700" fill="#2C6668">Shared Data & Cloud Foundation</text>

  <rect x="152" y="570" width="220" height="46" rx="18" fill="#DDEDEE" stroke="#A8CBCC" stroke-width="1"/>
  <rect x="407" y="570" width="220" height="46" rx="18" fill="#DDEDEE" stroke="#A8CBCC" stroke-width="1"/>
  <rect x="662" y="570" width="220" height="46" rx="18" fill="#DDEDEE" stroke="#A8CBCC" stroke-width="1"/>
  <rect x="917" y="570" width="220" height="46" rx="18" fill="#DDEDEE" stroke="#A8CBCC" stroke-width="1"/>
  <text x="262" y="599" width="170" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#2C6668">Operational Data Store</text>
  <text x="517" y="599" width="160" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#2C6668">Lakehouse & BI</text>
  <text x="772" y="599" width="160" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#2C6668">Kubernetes Platform</text>
  <text x="1027" y="599" width="160" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#2C6668">Security & Observability</text>

  <path d="M287 426 C287 470, 262 500, 262 570" fill="none" stroke="#2C6668" stroke-width="2.5" stroke-linecap="round" stroke-opacity="0.36"/>
  <path d="M640 426 C640 470, 517 500, 517 570" fill="none" stroke="#2C6668" stroke-width="2.5" stroke-linecap="round" stroke-opacity="0.36"/>
  <path d="M640 426 C640 470, 772 500, 772 570" fill="none" stroke="#2C6668" stroke-width="2.5" stroke-linecap="round" stroke-opacity="0.36"/>
  <path d="M993 426 C993 470, 1027 500, 1027 570" fill="none" stroke="#2C6668" stroke-width="2.5" stroke-linecap="round" stroke-opacity="0.36"/>

  <text x="74" y="686" width="900" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#6D8586">Design rule: darker solid shapes carry executive-level meaning; pale outlined containers show scope without adding visual noise.</text>
</svg>
```

## Avoid in this skill
- ❌ Random category colors for every system box; it destroys the monochromatic hierarchy.
- ❌ Dense orthogonal connector mazes; use whitespace and a few smooth curved paths instead.
- ❌ Applying `clip-path` to rectangles or paths; only use clipping on images if a photo or logo is required.
- ❌ Tiny text inside every node; reserve labels for the minimum set of architecture decisions.
- ❌ Heavy black strokes; use the base hue at low opacity or dashed outlines for containers.

## Composition notes
- Keep the top-level capability as the darkest, most visually dominant pill near the upper center.
- Use 80–90% slide-width containers for major layers, with generous inner padding so hierarchy is readable.
- Place service domains in a symmetrical row; align submodules inside them to create rhythm without grid clutter.
- Let the monochrome palette do the grouping: dark core, medium domains, light modules, pale container background.