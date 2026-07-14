# SVG Recipe — Minimal Two-Panel Comparison

## Visual mechanism
A calm split-screen composition uses two oversized rounded panels with strongly differentiated color treatments to frame a binary choice. Each panel gets a matching icon badge, headline, short explanation, and two compact evidence points so the viewer can compare options at a glance.

## SVG primitives needed
- 1× `<rect>` for the slide background
- 2× large `<rect>` for the left and right comparison panels
- 2× `<linearGradient>` for distinct panel personalities
- 1× `<filter id="panelShadow">` applied to both panels for soft depth
- 2× `<circle>` for icon badges inside the panels
- 4× `<path>` for simple editable line-style icons and decorative corner geometry
- 2× `<line>` for the vertical center seam and small divider rules
- 10× `<text>` with explicit `width` attributes for headings, body copy, labels, and metric callouts
- 4× small `<rect>` for pill labels and metric cards
- 6× translucent `<circle>` / `<ellipse>` accents for minimal executive-keynote polish

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="leftPanel" x1="48" y1="64" x2="616" y2="656" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#102A43"/>
      <stop offset="0.56" stop-color="#174A6A"/>
      <stop offset="1" stop-color="#1E6B84"/>
    </linearGradient>
    <linearGradient id="rightPanel" x1="664" y1="64" x2="1232" y2="656" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#FFF6E6"/>
      <stop offset="0.58" stop-color="#FFE2B8"/>
      <stop offset="1" stop-color="#F8B46A"/>
    </linearGradient>
    <linearGradient id="leftGlow" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#63D6FF" stop-opacity="0.55"/>
      <stop offset="1" stop-color="#63D6FF" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="rightGlow" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#FFFFFF" stop-opacity="0.72"/>
      <stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/>
    </linearGradient>
    <filter id="panelShadow" x="-10%" y="-10%" width="120%" height="125%">
      <feOffset dx="0" dy="14"/>
      <feGaussianBlur stdDeviation="18"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="softGlow" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="14"/>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#F4F6F8"/>

  <rect x="48" y="64" width="568" height="592" rx="36" fill="url(#leftPanel)" filter="url(#panelShadow)"/>
  <rect x="664" y="64" width="568" height="592" rx="36" fill="url(#rightPanel)" filter="url(#panelShadow)"/>

  <line x1="640" y1="112" x2="640" y2="608" stroke="#D8DEE6" stroke-width="2" stroke-dasharray="7 12"/>

  <circle cx="548" cy="132" r="118" fill="url(#leftGlow)" opacity="0.35" filter="url(#softGlow)"/>
  <circle cx="1098" cy="594" r="148" fill="url(#rightGlow)" opacity="0.48" filter="url(#softGlow)"/>
  <ellipse cx="120" cy="594" rx="108" ry="42" fill="#FFFFFF" opacity="0.06"/>
  <ellipse cx="1170" cy="142" rx="96" ry="34" fill="#A65F13" opacity="0.08"/>

  <path d="M488 104 C544 84 584 96 606 132 C566 126 530 143 500 184 C505 150 501 124 488 104 Z"
        fill="#FFFFFF" opacity="0.10"/>
  <path d="M726 594 C758 534 819 502 884 510 C824 544 792 590 789 649 C770 624 749 606 726 594 Z"
        fill="#9E5B10" opacity="0.08"/>

  <rect x="96" y="106" width="136" height="34" rx="17" fill="#FFFFFF" opacity="0.14"/>
  <text x="116" y="129" width="100" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="14" font-weight="700" letter-spacing="1.4" fill="#BDEFFF">OPTION A</text>

  <rect x="712" y="106" width="136" height="34" rx="17" fill="#7B3E00" opacity="0.10"/>
  <text x="732" y="129" width="100" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="14" font-weight="700" letter-spacing="1.4" fill="#7B3E00">OPTION B</text>

  <circle cx="126" cy="206" r="38" fill="#FFFFFF" opacity="0.16"/>
  <path d="M108 210 L122 224 L148 190" fill="none" stroke="#FFFFFF" stroke-width="7"
        stroke-linecap="round" stroke-linejoin="round"/>

  <circle cx="742" cy="206" r="38" fill="#8B4A08" opacity="0.12"/>
  <path d="M724 190 L760 226 M760 190 L724 226" fill="none" stroke="#8B4A08" stroke-width="7"
        stroke-linecap="round" stroke-linejoin="round"/>

  <text x="96" y="286" width="424" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="44" font-weight="750" fill="#FFFFFF">
    Platform-led growth
  </text>
  <text x="96" y="336" width="430" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="20" fill="#D8F4FF">
    <tspan x="96" dy="0">Consolidate core workflows into one shared operating</tspan>
    <tspan x="96" dy="30">model, prioritizing reuse, governance, and visibility.</tspan>
  </text>

  <text x="712" y="286" width="424" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="44" font-weight="750" fill="#2E1A05">
    Point-solution speed
  </text>
  <text x="712" y="336" width="430" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="20" fill="#6D430F">
    <tspan x="712" dy="0">Deploy targeted tools quickly for individual teams,</tspan>
    <tspan x="712" dy="30">maximizing autonomy and near-term delivery pace.</tspan>
  </text>

  <line x1="96" y1="430" x2="520" y2="430" stroke="#FFFFFF" stroke-width="1.5" opacity="0.20"/>
  <line x1="712" y1="430" x2="1136" y2="430" stroke="#7B3E00" stroke-width="1.5" opacity="0.18"/>

  <rect x="96" y="468" width="198" height="98" rx="22" fill="#FFFFFF" opacity="0.13"/>
  <text x="120" y="505" width="150" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="28" font-weight="750" fill="#FFFFFF">+32%</text>
  <text x="120" y="535" width="150" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="15" fill="#CDEFFF">reuse across teams</text>

  <rect x="322" y="468" width="198" height="98" rx="22" fill="#FFFFFF" opacity="0.13"/>
  <text x="346" y="505" width="150" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="28" font-weight="750" fill="#FFFFFF">6 mo.</text>
  <text x="346" y="535" width="150" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="15" fill="#CDEFFF">payback horizon</text>

  <rect x="712" y="468" width="198" height="98" rx="22" fill="#7B3E00" opacity="0.09"/>
  <text x="736" y="505" width="150" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="28" font-weight="750" fill="#2E1A05">3 wks</text>
  <text x="736" y="535" width="150" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="15" fill="#6D430F">launch window</text>

  <rect x="938" y="468" width="198" height="98" rx="22" fill="#7B3E00" opacity="0.09"/>
  <text x="962" y="505" width="150" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="28" font-weight="750" fill="#2E1A05">Low</text>
  <text x="962" y="535" width="150" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="15" fill="#6D430F">central dependency</text>
</svg>
```

## Avoid in this skill
- ❌ Do not add many small comparison rows; this shell depends on two dominant panels, not a feature matrix.
- ❌ Do not use a plain vertical split with no padding or rounded panels; it will look like a basic dashboard instead of a keynote comparison.
- ❌ Do not apply `clip-path` to decorative shapes or text; clipping is only reliable for `<image>` elements.
- ❌ Do not use `marker-end` for arrows between panels; if needed, draw directional cues with plain editable `<line>` and separate triangular `<path>` shapes.
- ❌ Avoid low-contrast text on the colored panels; each side needs its own text color system.

## Composition notes
- Keep the two panels equal in width with a narrow neutral gutter; the comparison should feel balanced and non-hierarchical.
- Place each panel’s title in the upper-middle third, then use short body text and compact metric cards below.
- Use mirrored structure but asymmetric color: dark/cool on one side, warm/light on the other for instant separation.
- Preserve generous internal margins, especially around the top chips and bottom metric cards, so the slide stays minimal rather than table-like.