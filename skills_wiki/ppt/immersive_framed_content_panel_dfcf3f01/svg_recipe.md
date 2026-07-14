# SVG Recipe — Immersive Framed Content Panel

## Visual mechanism
A cinematic, dark, high-energy background fills the entire slide while a pristine white content card floats above it with a soft shadow. The visible border of the background creates an immersive “stage,” and the opaque panel preserves executive-level readability for dense chart, agenda, or pitch content.

## SVG primitives needed
- 1× `<image>` for the full-bleed immersive stage / technology background.
- 2× `<rect>` for dark overlay tint and central white content panel.
- 1× `<linearGradient>` for the background color wash.
- 1× `<radialGradient>` for blue spotlight glow behind the card.
- 1× `<filter id="cardShadow">` using offset + blur + merge for panel elevation.
- 1× `<filter id="blueGlow">` using Gaussian blur for luminous background accents.
- 10–20× `<line>` for network / stage-beam geometry in the background.
- 20–40× `<circle>` for glowing nodes, LED dots, and audience silhouettes.
- 4–6× `<path>` for decorative brand/event motifs and a small rocket badge.
- Multiple `<text>` elements with explicit `width` for title, section labels, bullets, and metadata.

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="nightWash" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#080B15"/>
      <stop offset="45%" stop-color="#101A33"/>
      <stop offset="100%" stop-color="#24113B"/>
    </linearGradient>

    <radialGradient id="cyanHalo" cx="72%" cy="42%" r="58%">
      <stop offset="0%" stop-color="#19D8FF" stop-opacity="0.55"/>
      <stop offset="38%" stop-color="#005BFF" stop-opacity="0.28"/>
      <stop offset="100%" stop-color="#050713" stop-opacity="0"/>
    </radialGradient>

    <filter id="cardShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="16" in="SourceAlpha" result="off"/>
      <feGaussianBlur in="off" stdDeviation="18" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="blueGlow" x="-80%" y="-80%" width="260%" height="260%">
      <feGaussianBlur stdDeviation="8"/>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#nightWash)"/>
  <image href="https://images.example.com/dark-conference-stage-blue-network-screen.jpg"
         x="0" y="0" width="1280" height="720" preserveAspectRatio="xMidYMid slice" opacity="0.42"/>
  <rect x="0" y="0" width="1280" height="720" fill="#02040B" opacity="0.42"/>
  <rect x="0" y="0" width="1280" height="720" fill="url(#cyanHalo)"/>

  <!-- immersive stage beams and digital-network background -->
  <line x1="0" y1="525" x2="1280" y2="290" stroke="#00B7FF" stroke-opacity="0.28" stroke-width="2"/>
  <line x1="0" y1="610" x2="1130" y2="170" stroke="#006BFF" stroke-opacity="0.24" stroke-width="2"/>
  <line x1="110" y1="720" x2="760" y2="60" stroke="#19D8FF" stroke-opacity="0.20" stroke-width="2"/>
  <line x1="345" y1="720" x2="1020" y2="120" stroke="#00B7FF" stroke-opacity="0.24" stroke-width="2"/>
  <line x1="1280" y1="585" x2="360" y2="210" stroke="#31E7FF" stroke-opacity="0.22" stroke-width="2"/>
  <line x1="1280" y1="690" x2="690" y2="215" stroke="#006BFF" stroke-opacity="0.30" stroke-width="2"/>
  <path d="M720 145 C830 105 930 108 1035 165 S1190 258 1265 218" fill="none" stroke="#1CD7FF" stroke-opacity="0.30" stroke-width="3"/>
  <path d="M650 425 C760 330 885 318 1028 362 S1195 418 1280 360" fill="none" stroke="#005DFF" stroke-opacity="0.36" stroke-width="4" filter="url(#blueGlow)"/>

  <circle cx="158" cy="534" r="9" fill="#4BEAFF" opacity="0.75" filter="url(#blueGlow)"/>
  <circle cx="330" cy="468" r="6" fill="#69F7FF" opacity="0.70"/>
  <circle cx="534" cy="394" r="8" fill="#4BEAFF" opacity="0.72"/>
  <circle cx="760" cy="302" r="7" fill="#8CFBFF" opacity="0.78"/>
  <circle cx="970" cy="248" r="10" fill="#2EDBFF" opacity="0.70" filter="url(#blueGlow)"/>
  <circle cx="1138" cy="328" r="8" fill="#7DF5FF" opacity="0.68"/>
  <circle cx="1220" cy="462" r="11" fill="#43DFFF" opacity="0.60" filter="url(#blueGlow)"/>

  <!-- bottom audience / stage silhouettes -->
  <ellipse cx="85" cy="692" rx="64" ry="35" fill="#02030A" opacity="0.72"/>
  <ellipse cx="250" cy="700" rx="92" ry="38" fill="#02030A" opacity="0.76"/>
  <ellipse cx="455" cy="698" rx="110" ry="36" fill="#02030A" opacity="0.72"/>
  <ellipse cx="720" cy="702" rx="140" ry="42" fill="#02030A" opacity="0.70"/>
  <ellipse cx="1002" cy="694" rx="118" ry="38" fill="#02030A" opacity="0.74"/>
  <ellipse cx="1195" cy="700" rx="98" ry="36" fill="#02030A" opacity="0.72"/>

  <!-- floating content panel -->
  <rect x="160" y="82" width="960" height="556" rx="10" fill="#FFFFFF" filter="url(#cardShadow)"/>
  <rect x="160" y="82" width="960" height="8" rx="4" fill="#FFD21F"/>

  <text x="214" y="144" width="730" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="20" font-weight="700" fill="#FFB800" letter-spacing="2">STARTUP PITCH MASTERCLASS</text>

  <text x="214" y="218" width="760" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="50" font-weight="800" fill="#070707">
    <tspan x="214" dy="0">How to Perfectly Pitch</tspan>
    <tspan x="214" dy="58">Your Startup</tspan>
  </text>

  <text x="214" y="300" width="765" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="22" fill="#4F5561">
    A clean content panel lets the audience read the framework while the event-stage background keeps the slide cinematic and premium.
  </text>

  <line x1="214" y1="342" x2="1048" y2="342" stroke="#E5E8EF" stroke-width="2"/>

  <text x="214" y="386" width="330" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="22" font-weight="800" fill="#111827">Common pitch elements</text>
  <text x="214" y="430" width="360" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="21" fill="#3F4652">
    <tspan x="214" dy="0">• What do you do?</tspan>
    <tspan x="214" dy="36">• Team and founder insight</tspan>
    <tspan x="214" dy="36">• Traction and customer proof</tspan>
    <tspan x="214" dy="36">• Market size and urgency</tspan>
  </text>

  <text x="640" y="386" width="330" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="22" font-weight="800" fill="#111827">Investor-ready narrative</text>
  <text x="640" y="430" width="360" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="21" fill="#3F4652">
    <tspan x="640" dy="0">• Unique insight</tspan>
    <tspan x="640" dy="36">• Why now?</tspan>
    <tspan x="640" dy="36">• Defensible advantage</tspan>
    <tspan x="640" dy="36">• Clear ask and next step</tspan>
  </text>

  <!-- small branded rocket badge -->
  <circle cx="1010" cy="545" r="50" fill="#0B1020"/>
  <path d="M1010 505 C1030 524 1036 552 1010 582 C984 552 990 524 1010 505 Z" fill="#FFFFFF"/>
  <path d="M996 560 C984 565 977 577 974 590 C989 588 1001 581 1007 568 Z" fill="#FFD21F"/>
  <path d="M1024 560 C1036 565 1043 577 1046 590 C1031 588 1019 581 1013 568 Z" fill="#FFD21F"/>
  <circle cx="1010" cy="536" r="8" fill="#17C9FF"/>
  <text x="900" y="624" width="220" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="15" font-weight="700" fill="#6B7280" text-anchor="middle">YC-style pitch workshop</text>
</svg>
```

## Avoid in this skill
- ❌ Transparent text directly on the complex background for primary content; readability collapses quickly.
- ❌ Using `<mask>` to fade the background image; use a semi-transparent `<rect>` overlay or gradients instead.
- ❌ Applying `clip-path` to the white content panel; PowerPoint translation only preserves clipping reliably on `<image>`.
- ❌ Overcrowding the frame border with foreground elements that compete with the content card.
- ❌ Filter effects on `<line>` elements; use glows on nearby circles or paths instead.

## Composition notes
- Keep the central panel around 75–80% of slide width and height, leaving a continuous cinematic border.
- Use the background for atmosphere only: darken it with overlays so it frames rather than fights the content.
- Inside the card, maintain generous padding, strong black title typography, and softer gray body text.
- Add one small brand/icon motif inside the panel or near a corner to connect the clean card back to the immersive stage.