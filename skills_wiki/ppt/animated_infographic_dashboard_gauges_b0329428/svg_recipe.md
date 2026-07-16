# SVG Recipe — Animated Infographic Dashboard Gauges

## Visual mechanism
A premium dashboard slide built from three semi-circular, segmented speedometer gauges, each using progressive monochrome arc colors and a rotated triangular needle to show a KPI percentage. Since SVG animation is not PowerPoint-editable, the SVG should encode the final needle angle and preserve a transparent counterweight shape so PowerPoint can later apply a true spin animation around the pivot.

## SVG primitives needed
- 1× `<rect>` for the full-slide dark technical background
- 3× `<rect>` for glass-like KPI cards behind each gauge
- 15× `<path>` for five thick arc segments per gauge
- 6× `<path>` for visible needle triangles plus transparent counterweight triangles
- 3× `<circle>` for needle pivot hubs
- 6× `<line>` for minimal 0% / 100% gauge tick accents
- 13× `<text>` for title, subtitle, KPI values, KPI labels, and min/max labels
- 3× `<linearGradient>` for background and card surface styling
- 1× `<radialGradient>` for the central dashboard glow
- 2× `<filter>` definitions: one soft card shadow and one glow/needle shadow applied only to shapes/text

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <radialGradient id="bgGlow" cx="50%" cy="38%" r="72%">
      <stop offset="0%" stop-color="#203B5C"/>
      <stop offset="48%" stop-color="#111C2B"/>
      <stop offset="100%" stop-color="#07101B"/>
    </radialGradient>

    <linearGradient id="cardGlass" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.16"/>
      <stop offset="55%" stop-color="#FFFFFF" stop-opacity="0.07"/>
      <stop offset="100%" stop-color="#FFFFFF" stop-opacity="0.03"/>
    </linearGradient>

    <linearGradient id="topRule" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#5ED7FF" stop-opacity="0"/>
      <stop offset="50%" stop-color="#5ED7FF" stop-opacity="0.75"/>
      <stop offset="100%" stop-color="#5ED7FF" stop-opacity="0"/>
    </linearGradient>

    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="14" result="off"/>
      <feGaussianBlur in="off" stdDeviation="16" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="needleGlow" x="-30%" y="-30%" width="160%" height="160%">
      <feOffset dx="0" dy="4" result="off"/>
      <feGaussianBlur in="off" stdDeviation="5" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGlow)"/>
  <circle cx="640" cy="390" r="430" fill="#5ED7FF" opacity="0.05"/>
  <rect x="280" y="128" width="720" height="2" rx="1" fill="url(#topRule)"/>

  <text x="640" y="78" width="780" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="42" font-weight="700" fill="#F4F8FF" letter-spacing="6">EFFICIENCY DASHBOARD</text>
  <text x="640" y="115" width="760" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#9FB3C8" letter-spacing="2">LIVE KPI GAUGES · FINAL STATE PRESERVED AS EDITABLE SHAPES</text>

  <rect x="105" y="175" width="310" height="390" rx="34" fill="url(#cardGlass)" stroke="#FFFFFF" stroke-opacity="0.16" filter="url(#softShadow)"/>
  <rect x="485" y="175" width="310" height="390" rx="34" fill="url(#cardGlass)" stroke="#FFFFFF" stroke-opacity="0.16" filter="url(#softShadow)"/>
  <rect x="865" y="175" width="310" height="390" rx="34" fill="url(#cardGlass)" stroke="#FFFFFF" stroke-opacity="0.16" filter="url(#softShadow)"/>

  <!-- Gauge 1: Reach, 82% -->
  <path d="M135 405 A125 125 0 0 1 158.9 331.5" fill="none" stroke="#ADD8E6" stroke-width="28" stroke-linecap="butt"/>
  <path d="M158.9 331.5 A125 125 0 0 1 221.4 286.1" fill="none" stroke="#96C8DD" stroke-width="28" stroke-linecap="butt"/>
  <path d="M221.4 286.1 A125 125 0 0 1 298.6 286.1" fill="none" stroke="#7FB6D1" stroke-width="28" stroke-linecap="butt"/>
  <path d="M298.6 286.1 A125 125 0 0 1 361.1 331.5" fill="none" stroke="#649DC0" stroke-width="28" stroke-linecap="butt"/>
  <path d="M361.1 331.5 A125 125 0 0 1 385 405" fill="none" stroke="#4682B4" stroke-width="28" stroke-linecap="butt"/>
  <line x1="130" y1="405" x2="158" y2="405" stroke="#7EAECF" stroke-width="3" opacity="0.6"/>
  <line x1="362" y1="405" x2="390" y2="405" stroke="#7EAECF" stroke-width="3" opacity="0.6"/>
  <g transform="rotate(147.6 260 405)">
    <path d="M148 405 L260 392 L260 418 Z" fill="#1E3759" filter="url(#needleGlow)"/>
    <path d="M372 405 L260 392 L260 418 Z" fill="#1E3759" fill-opacity="0"/>
    <circle cx="260" cy="405" r="23" fill="#1E3759" filter="url(#needleGlow)"/>
  </g>
  <circle cx="260" cy="405" r="9" fill="#CFEFFF"/>
  <text x="150" y="438" width="70" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#8BA9C7">0</text>
  <text x="370" y="438" width="70" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#8BA9C7">100</text>
  <text x="260" y="506" width="230" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="48" font-weight="700" fill="#E9F8FF" filter="url(#needleGlow)">82%</text>
  <text x="260" y="542" width="230" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#7EC8EE" letter-spacing="3">REACH</text>

  <!-- Gauge 2: Engagement, 64% -->
  <path d="M515 405 A125 125 0 0 1 538.9 331.5" fill="none" stroke="#FBD5B5" stroke-width="28" stroke-linecap="butt"/>
  <path d="M538.9 331.5 A125 125 0 0 1 601.4 286.1" fill="none" stroke="#F8C499" stroke-width="28" stroke-linecap="butt"/>
  <path d="M601.4 286.1 A125 125 0 0 1 678.6 286.1" fill="none" stroke="#F4B17E" stroke-width="28" stroke-linecap="butt"/>
  <path d="M678.6 286.1 A125 125 0 0 1 741.1 331.5" fill="none" stroke="#F09E63" stroke-width="28" stroke-linecap="butt"/>
  <path d="M741.1 331.5 A125 125 0 0 1 765 405" fill="none" stroke="#EE8E48" stroke-width="28" stroke-linecap="butt"/>
  <line x1="510" y1="405" x2="538" y2="405" stroke="#F1A56C" stroke-width="3" opacity="0.6"/>
  <line x1="742" y1="405" x2="770" y2="405" stroke="#F1A56C" stroke-width="3" opacity="0.6"/>
  <g transform="rotate(115.2 640 405)">
    <path d="M528 405 L640 392 L640 418 Z" fill="#B05517" filter="url(#needleGlow)"/>
    <path d="M752 405 L640 392 L640 418 Z" fill="#B05517" fill-opacity="0"/>
    <circle cx="640" cy="405" r="23" fill="#B05517" filter="url(#needleGlow)"/>
  </g>
  <circle cx="640" cy="405" r="9" fill="#FFE6D2"/>
  <text x="530" y="438" width="70" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#D8A27D">0</text>
  <text x="750" y="438" width="70" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#D8A27D">100</text>
  <text x="640" y="506" width="230" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="48" font-weight="700" fill="#FFF0E4" filter="url(#needleGlow)">64%</text>
  <text x="640" y="542" width="230" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#F2A66A" letter-spacing="3">ENGAGEMENT</text>

  <!-- Gauge 3: Quality, 91% -->
  <path d="M895 405 A125 125 0 0 1 918.9 331.5" fill="none" stroke="#C5E0B4" stroke-width="28" stroke-linecap="butt"/>
  <path d="M918.9 331.5 A125 125 0 0 1 981.4 286.1" fill="none" stroke="#AED39A" stroke-width="28" stroke-linecap="butt"/>
  <path d="M981.4 286.1 A125 125 0 0 1 1058.6 286.1" fill="none" stroke="#95C47E" stroke-width="28" stroke-linecap="butt"/>
  <path d="M1058.6 286.1 A125 125 0 0 1 1121.1 331.5" fill="none" stroke="#7DB563" stroke-width="28" stroke-linecap="butt"/>
  <path d="M1121.1 331.5 A125 125 0 0 1 1145 405" fill="none" stroke="#70AD47" stroke-width="28" stroke-linecap="butt"/>
  <line x1="890" y1="405" x2="918" y2="405" stroke="#95C57B" stroke-width="3" opacity="0.6"/>
  <line x1="1122" y1="405" x2="1150" y2="405" stroke="#95C57B" stroke-width="3" opacity="0.6"/>
  <g transform="rotate(163.8 1020 405)">
    <path d="M908 405 L1020 392 L1020 418 Z" fill="#2F5316" filter="url(#needleGlow)"/>
    <path d="M1132 405 L1020 392 L1020 418 Z" fill="#2F5316" fill-opacity="0"/>
    <circle cx="1020" cy="405" r="23" fill="#2F5316" filter="url(#needleGlow)"/>
  </g>
  <circle cx="1020" cy="405" r="9" fill="#E3F6D8"/>
  <text x="910" y="438" width="70" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#A8C99A">0</text>
  <text x="1130" y="438" width="70" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#A8C99A">100</text>
  <text x="1020" y="506" width="230" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="48" font-weight="700" fill="#EFFFEA" filter="url(#needleGlow)">91%</text>
  <text x="1020" y="542" width="230" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#9CD47A" letter-spacing="3">QUALITY</text>
</svg>
```

## Avoid in this skill
- ❌ Do not use SVG `<animate>` or `<animateTransform>` for the needle; PowerPoint will not preserve it as an editable animation.
- ❌ Do not rasterize the whole gauge as an `<image>` unless absolutely necessary; editable arc paths and needle paths are the point of this technique.
- ❌ Do not rely on `marker-end` arrowheads for the needle; build the pointer as a filled triangular `<path>`.
- ❌ Do not apply filters to `<line>` tick marks; filter support on lines is dropped.
- ❌ Do not use masks to hide half of a donut chart; construct the visible semi-circle directly with arc paths.

## Composition notes
- Keep gauges in a clean horizontal row with equal card widths; the card spacing is as important as the gauge detail.
- Put the gauge pivot around the lower third of each card, leaving room below for the large KPI number and compact label.
- Use one monochrome ramp per metric so the dashboard feels coordinated but each KPI remains instantly distinguishable.
- For PowerPoint animation, group each visible needle with its transparent counterweight, then apply a spin rotation of `percentage × 1.8°` around the pivot.