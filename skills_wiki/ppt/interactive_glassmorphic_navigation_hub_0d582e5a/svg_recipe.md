# SVG Recipe — Interactive Glassmorphic Navigation Hub

## Visual mechanism
A vibrant mesh-gradient background is overlaid with semi-transparent frosted-glass navigation cards, each acting as a clickable topic tile. The visual suggests interactive zoom navigation by using central cards, subtle glows, transparent hit areas, and a persistent “hub” composition that can be duplicated across linked section slides.

## SVG primitives needed
- 1× full-slide `<rect>` for the base gradient background
- 5× large blurred `<circle>` / `<ellipse>` color orbs for the mesh-gradient depth
- 1× `<filter id="orbBlur">` using `feGaussianBlur` for soft background color diffusion
- 1× `<filter id="glassShadow">` using `feOffset + feGaussianBlur + feMerge` for card elevation
- 1× `<filter id="softGlow">` using `feGaussianBlur` for the active/hover-like glow ring
- 1× large rounded `<rect>` for the central glass stage
- 5× rounded `<rect>` navigation cards with translucent fills and gradient strokes
- 5× transparent rounded `<rect>` hit zones, intended to receive PowerPoint hyperlinks after SVG conversion
- Multiple `<path>`, `<circle>`, `<line>`, and `<rect>` primitives for editable monochrome topic icons
- 1× compact `<path>` home icon motif for demonstrating return-navigation styling
- Multiple `<text>` elements with explicit `width` attributes for title, labels, and microcopy
- 3× `<linearGradient>` definitions for background, glass fill, and card accents
- 1× `<radialGradient>` definition for glowing accent highlights

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgMesh" x1="0" y1="0" x2="1280" y2="720">
      <stop offset="0%" stop-color="#2B5876"/>
      <stop offset="38%" stop-color="#036F71"/>
      <stop offset="68%" stop-color="#4E1D44"/>
      <stop offset="100%" stop-color="#AA4B35"/>
    </linearGradient>

    <linearGradient id="glassFill" x1="120" y1="95" x2="1160" y2="635">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.34"/>
      <stop offset="45%" stop-color="#FFFFFF" stop-opacity="0.16"/>
      <stop offset="100%" stop-color="#FFFFFF" stop-opacity="0.08"/>
    </linearGradient>

    <linearGradient id="cardStroke" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.78"/>
      <stop offset="55%" stop-color="#FFFFFF" stop-opacity="0.20"/>
      <stop offset="100%" stop-color="#FFFFFF" stop-opacity="0.46"/>
    </linearGradient>

    <radialGradient id="accentGlow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.68"/>
      <stop offset="42%" stop-color="#78F5E4" stop-opacity="0.22"/>
      <stop offset="100%" stop-color="#78F5E4" stop-opacity="0"/>
    </radialGradient>

    <filter id="orbBlur" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="55"/>
    </filter>

    <filter id="glassShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="18" in="SourceAlpha" result="off"/>
      <feGaussianBlur stdDeviation="22" in="off" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="softGlow" x="-60%" y="-60%" width="220%" height="220%">
      <feGaussianBlur stdDeviation="16"/>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgMesh)"/>

  <circle cx="210" cy="145" r="210" fill="#1DB9C3" opacity="0.42" filter="url(#orbBlur)"/>
  <ellipse cx="1090" cy="120" rx="260" ry="190" fill="#A33C89" opacity="0.48" filter="url(#orbBlur)"/>
  <ellipse cx="1080" cy="610" rx="280" ry="180" fill="#FF8A55" opacity="0.42" filter="url(#orbBlur)"/>
  <circle cx="365" cy="640" r="245" fill="#036F71" opacity="0.50" filter="url(#orbBlur)"/>
  <ellipse cx="660" cy="355" rx="320" ry="150" fill="#43256D" opacity="0.30" filter="url(#orbBlur)"/>

  <rect x="88" y="78" width="1104" height="564" rx="44" fill="url(#glassFill)" stroke="#FFFFFF" stroke-opacity="0.28" stroke-width="1.5" filter="url(#glassShadow)"/>
  <rect x="112" y="102" width="1056" height="516" rx="34" fill="none" stroke="#FFFFFF" stroke-opacity="0.16" stroke-width="1"/>

  <text x="870" y="56" width="340" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="700" letter-spacing="2.5" fill="#FFFFFF" opacity="0.84" text-anchor="end">HOW TO ADD HYPERLINK TO A SLIDE</text>
  <text x="132" y="156" width="650" font-family="Segoe UI, Microsoft YaHei" font-size="46" font-weight="800" fill="#FFFFFF">Choose your path</text>
  <text x="136" y="196" width="560" font-family="Segoe UI, Microsoft YaHei" font-size="18" fill="#FFFFFF" opacity="0.72">A glassmorphic hub for non-linear executive storytelling.</text>

  <circle cx="1058" cy="155" r="56" fill="url(#accentGlow)" filter="url(#softGlow)"/>
  <rect x="1010" y="118" width="96" height="74" rx="24" fill="#FFFFFF" opacity="0.12" stroke="#FFFFFF" stroke-opacity="0.34"/>
  <path d="M1033 153 L1058 132 L1083 153 L1083 181 L1067 181 L1067 162 L1049 162 L1049 181 L1033 181 Z" fill="none" stroke="#FFFFFF" stroke-width="4" stroke-linejoin="round"/>
  <text x="995" y="214" width="126" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#FFFFFF" opacity="0.72" text-anchor="middle">RETURN HOME</text>

  <g id="nav-card-introduction">
    <rect x="150" y="290" width="180" height="190" rx="30" fill="#FFFFFF" opacity="0.18" stroke="url(#cardStroke)" stroke-width="1.6" filter="url(#glassShadow)"/>
    <circle cx="240" cy="354" r="38" fill="#FFFFFF" opacity="0.12"/>
    <path d="M222 350 C222 337 232 328 246 328 C260 328 270 337 270 350 C270 360 264 367 254 371 L254 380 L236 380 L236 367 C227 364 222 358 222 350 Z" fill="none" stroke="#FFFFFF" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>
    <line x1="236" y1="395" x2="254" y2="395" stroke="#FFFFFF" stroke-width="5" stroke-linecap="round"/>
    <text x="170" y="438" width="140" font-family="Segoe UI, Microsoft YaHei" font-size="19" font-weight="800" fill="#FFFFFF" text-anchor="middle">Introduction</text>
    <rect id="hit-introduction" x="150" y="290" width="180" height="190" rx="30" fill="#FFFFFF" opacity="0.001"/>
  </g>

  <g id="nav-card-goals">
    <rect x="350" y="290" width="180" height="190" rx="30" fill="#FFFFFF" opacity="0.18" stroke="url(#cardStroke)" stroke-width="1.6" filter="url(#glassShadow)"/>
    <circle cx="440" cy="354" r="38" fill="#FFFFFF" opacity="0.12"/>
    <circle cx="440" cy="354" r="30" fill="none" stroke="#FFFFFF" stroke-width="5"/>
    <circle cx="440" cy="354" r="14" fill="none" stroke="#FFFFFF" stroke-width="5"/>
    <line x1="440" y1="354" x2="466" y2="331" stroke="#FFFFFF" stroke-width="5" stroke-linecap="round"/>
    <text x="370" y="438" width="140" font-family="Segoe UI, Microsoft YaHei" font-size="19" font-weight="800" fill="#FFFFFF" text-anchor="middle">Goals</text>
    <rect id="hit-goals" x="350" y="290" width="180" height="190" rx="30" fill="#FFFFFF" opacity="0.001"/>
  </g>

  <g id="nav-card-topic">
    <rect x="550" y="290" width="180" height="190" rx="30" fill="#FFFFFF" opacity="0.22" stroke="url(#cardStroke)" stroke-width="1.8" filter="url(#glassShadow)"/>
    <circle cx="640" cy="354" r="46" fill="url(#accentGlow)" filter="url(#softGlow)"/>
    <rect x="608" y="322" width="64" height="64" rx="16" fill="none" stroke="#FFFFFF" stroke-width="5"/>
    <line x1="624" y1="342" x2="656" y2="342" stroke="#FFFFFF" stroke-width="5" stroke-linecap="round"/>
    <line x1="624" y1="357" x2="656" y2="357" stroke="#FFFFFF" stroke-width="5" stroke-linecap="round"/>
    <line x1="624" y1="372" x2="646" y2="372" stroke="#FFFFFF" stroke-width="5" stroke-linecap="round"/>
    <text x="570" y="438" width="140" font-family="Segoe UI, Microsoft YaHei" font-size="19" font-weight="800" fill="#FFFFFF" text-anchor="middle">Topic</text>
    <rect id="hit-topic" x="550" y="290" width="180" height="190" rx="30" fill="#FFFFFF" opacity="0.001"/>
  </g>

  <g id="nav-card-examples">
    <rect x="750" y="290" width="180" height="190" rx="30" fill="#FFFFFF" opacity="0.18" stroke="url(#cardStroke)" stroke-width="1.6" filter="url(#glassShadow)"/>
    <circle cx="840" cy="354" r="38" fill="#FFFFFF" opacity="0.12"/>
    <path d="M811 346 L830 327 L847 344 L862 329 L879 346 L879 379 L811 379 Z" fill="none" stroke="#FFFFFF" stroke-width="5" stroke-linejoin="round"/>
    <circle cx="829" cy="344" r="5" fill="#FFFFFF"/>
    <text x="770" y="438" width="140" font-family="Segoe UI, Microsoft YaHei" font-size="19" font-weight="800" fill="#FFFFFF" text-anchor="middle">Examples</text>
    <rect id="hit-examples" x="750" y="290" width="180" height="190" rx="30" fill="#FFFFFF" opacity="0.001"/>
  </g>

  <g id="nav-card-analysis">
    <rect x="950" y="290" width="180" height="190" rx="30" fill="#FFFFFF" opacity="0.18" stroke="url(#cardStroke)" stroke-width="1.6" filter="url(#glassShadow)"/>
    <circle cx="1040" cy="354" r="38" fill="#FFFFFF" opacity="0.12"/>
    <line x1="1012" y1="380" x2="1068" y2="380" stroke="#FFFFFF" stroke-width="5" stroke-linecap="round"/>
    <rect x="1018" y="352" width="10" height="28" rx="5" fill="#FFFFFF"/>
    <rect x="1035" y="334" width="10" height="46" rx="5" fill="#FFFFFF"/>
    <rect x="1052" y="318" width="10" height="62" rx="5" fill="#FFFFFF"/>
    <text x="970" y="438" width="140" font-family="Segoe UI, Microsoft YaHei" font-size="19" font-weight="800" fill="#FFFFFF" text-anchor="middle">Analysis</text>
    <rect id="hit-analysis" x="950" y="290" width="180" height="190" rx="30" fill="#FFFFFF" opacity="0.001"/>
  </g>

  <text x="150" y="565" width="780" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#FFFFFF" opacity="0.62">After conversion, assign each transparent hit rectangle a PowerPoint hyperlink to its matching section slide; add a Zoom transition between hub and content slides.</text>
  <line x1="150" y1="590" x2="1130" y2="590" stroke="#FFFFFF" stroke-opacity="0.18" stroke-width="1"/>
  <text x="150" y="622" width="320" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#FFFFFF" opacity="0.68">01  HUB</text>
  <text x="995" y="622" width="140" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#FFFFFF" opacity="0.68" text-anchor="end">CLICKABLE MENU</text>
</svg>
```

## Avoid in this skill
- ❌ Real SVG animation such as `<animate>` or `<animateTransform>`; create the zoom feeling with PowerPoint slide transitions after conversion.
- ❌ `<foreignObject>` buttons or HTML UI elements; build all cards, labels, and icons from native SVG shapes and text.
- ❌ `clip-path` on glass panels or cards; clipping only reliably applies to `<image>`, so use rounded `<rect>` geometry directly for panels.
- ❌ `filter` on `<line>` icon strokes; keep icon lines unfiltered and apply shadows/glows to surrounding rects, circles, or paths instead.
- ❌ SVG `<mask>` for frosted glass; simulate glass with translucent fills, gradient strokes, shadows, and blurred background orbs.

## Composition notes
- Keep the hub cards in a centered horizontal band occupying roughly 70–80% of slide width; this makes the slide feel like an interactive control surface.
- Reserve the upper-left area for the main navigation prompt and the upper-right for compact deck context or a home motif.
- Use a continuous mesh-gradient background on every linked slide so the hub and section slides feel spatially connected.
- For section slides, reuse the same background and place one large glass panel over the left or center two-thirds, with a small home button linked back to the hub.