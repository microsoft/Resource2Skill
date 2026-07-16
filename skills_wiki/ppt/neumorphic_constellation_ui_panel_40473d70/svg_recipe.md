# SVG Recipe — Neumorphic Constellation UI Panel

## Visual mechanism
A same-color foreground panel floats above a dark navy canvas using an oversized soft shadow, while thin constellation lines and a partial structural arc sit behind it to imply a futuristic data network. Bright white italic headline typography, small neon diamonds, and a pill CTA create a premium motion-graphics UI composition.

## SVG primitives needed
- 2× `<rect>` for the full-slide dark background and main neumorphic content panel
- 1× `<rect>` with gradient fill for the rounded blue CTA button
- 1× `<rect>` outline for a subtle bevel/highlight on the panel edge
- 2× `<path>` for large background U-arc structures
- 3× `<path>` for white triangular “play” chevrons between panel and CTA
- 17× `<line>` for the constellation network edges
- 12× `<circle>` for constellation nodes
- 5× `<circle>` for floating white decorative dots
- 5× rotated `<rect>` for floating diamond accents
- 4× `<text>` blocks for headline, subhead, button label, and bottom tagline
- 1× `<linearGradient>` for the blue CTA button
- 1× `<radialGradient>` for the soft background halo
- 1× `<filter id="softShadow">` applied to the main panel and CTA button
- 1× `<filter id="textLift">` applied to headline text for subtle dark depth

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <radialGradient id="bgHalo" cx="46%" cy="28%" r="58%">
      <stop offset="0%" stop-color="#24304d"/>
      <stop offset="55%" stop-color="#1c2237"/>
      <stop offset="100%" stop-color="#192035"/>
    </radialGradient>

    <linearGradient id="buttonBlue" x1="872" y1="333" x2="1182" y2="387" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#2563eb"/>
      <stop offset="52%" stop-color="#3b82f6"/>
      <stop offset="100%" stop-color="#2563eb"/>
    </linearGradient>

    <filter id="softShadow" x="-30%" y="-30%" width="170%" height="180%">
      <feOffset in="SourceAlpha" dx="34" dy="24" result="offset"/>
      <feGaussianBlur in="offset" stdDeviation="26" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="textLift" x="-10%" y="-10%" width="130%" height="140%">
      <feOffset in="SourceAlpha" dx="3" dy="4" result="txtOffset"/>
      <feGaussianBlur in="txtOffset" stdDeviation="2" result="txtBlur"/>
      <feMerge>
        <feMergeNode in="txtBlur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgHalo)"/>

  <!-- Deep structural U-arcs behind the panel -->
  <path d="M328 410 A270 270 0 1 1 828 410" fill="none" stroke="#111a2d" stroke-width="60" opacity="0.82"/>
  <path d="M388 388 A205 205 0 1 1 768 388" fill="none" stroke="#30405d" stroke-width="3" opacity="0.6"/>

  <!-- Constellation network -->
  <line x1="423" y1="88" x2="536" y2="63" stroke="#8c96aa" stroke-width="1.4" opacity="0.78"/>
  <line x1="536" y1="63" x2="596" y2="17" stroke="#8c96aa" stroke-width="1.4" opacity="0.78"/>
  <line x1="596" y1="17" x2="663" y2="61" stroke="#8c96aa" stroke-width="1.4" opacity="0.78"/>
  <line x1="536" y1="63" x2="560" y2="102" stroke="#8c96aa" stroke-width="1.4" opacity="0.78"/>
  <line x1="423" y1="88" x2="498" y2="126" stroke="#8c96aa" stroke-width="1.4" opacity="0.78"/>
  <line x1="423" y1="88" x2="431" y2="205" stroke="#8c96aa" stroke-width="1.4" opacity="0.78"/>
  <line x1="498" y1="126" x2="560" y2="102" stroke="#8c96aa" stroke-width="1.4" opacity="0.78"/>
  <line x1="560" y1="102" x2="596" y2="17" stroke="#8c96aa" stroke-width="1.4" opacity="0.78"/>
  <line x1="560" y1="102" x2="596" y2="123" stroke="#8c96aa" stroke-width="1.4" opacity="0.78"/>
  <line x1="596" y1="123" x2="663" y2="61" stroke="#8c96aa" stroke-width="1.4" opacity="0.78"/>
  <line x1="596" y1="123" x2="642" y2="198" stroke="#8c96aa" stroke-width="1.4" opacity="0.78"/>
  <line x1="663" y1="61" x2="672" y2="151" stroke="#8c96aa" stroke-width="1.4" opacity="0.78"/>
  <line x1="672" y1="151" x2="750" y2="180" stroke="#8c96aa" stroke-width="1.4" opacity="0.78"/>
  <line x1="642" y1="198" x2="750" y2="180" stroke="#8c96aa" stroke-width="1.4" opacity="0.78"/>
  <line x1="498" y1="126" x2="556" y2="212" stroke="#8c96aa" stroke-width="1.4" opacity="0.78"/>
  <line x1="556" y1="212" x2="642" y2="198" stroke="#8c96aa" stroke-width="1.4" opacity="0.78"/>
  <line x1="431" y1="205" x2="556" y2="212" stroke="#8c96aa" stroke-width="1.4" opacity="0.78"/>

  <circle cx="596" cy="17" r="6" fill="#9aa4b8"/>
  <circle cx="536" cy="63" r="6" fill="#9aa4b8"/>
  <circle cx="663" cy="61" r="6" fill="#9aa4b8"/>
  <circle cx="423" cy="88" r="6" fill="#9aa4b8"/>
  <circle cx="560" cy="102" r="6" fill="#9aa4b8"/>
  <circle cx="498" cy="126" r="6" fill="#9aa4b8"/>
  <circle cx="596" cy="123" r="6" fill="#9aa4b8"/>
  <circle cx="672" cy="151" r="6" fill="#9aa4b8"/>
  <circle cx="750" cy="180" r="6" fill="#9aa4b8"/>
  <circle cx="431" cy="205" r="6" fill="#9aa4b8"/>
  <circle cx="556" cy="212" r="6" fill="#9aa4b8"/>
  <circle cx="642" cy="198" r="6" fill="#9aa4b8"/>

  <!-- Floating neumorphic panel -->
  <rect x="230" y="152" width="425" height="386" fill="#1c2237" filter="url(#softShadow)"/>
  <rect x="231" y="153" width="423" height="384" fill="none" stroke="#26324d" stroke-width="1.2" opacity="0.55"/>

  <text x="278" y="286" width="340" fill="#ffffff" font-family="Segoe UI Black, Segoe UI, Microsoft YaHei, sans-serif" font-size="64" font-style="italic" font-weight="900" letter-spacing="2" filter="url(#textLift)">EASY UI</text>
  <text x="258" y="377" width="390" fill="#ffffff" font-family="Segoe UI Black, Segoe UI, Microsoft YaHei, sans-serif" font-size="64" font-style="italic" font-weight="900" letter-spacing="1.5" filter="url(#textLift)">ANIMATION</text>
  <text x="250" y="448" width="315" fill="#ffffff" font-family="Segoe UI Black, Segoe UI, Microsoft YaHei, sans-serif" font-size="42" font-style="italic" font-weight="900" letter-spacing="1.5" filter="url(#textLift)">POWERPOINT</text>

  <!-- White play chevrons -->
  <path d="M680 344 L704 361 L680 378 Z" fill="#ffffff"/>
  <path d="M740 344 L764 361 L740 378 Z" fill="#ffffff"/>
  <path d="M800 344 L824 361 L800 378 Z" fill="#ffffff"/>

  <!-- CTA button -->
  <rect x="872" y="333" width="310" height="55" rx="27.5" fill="url(#buttonBlue)" filter="url(#softShadow)"/>
  <text x="938" y="378" width="190" fill="#ffffff" font-family="Segoe UI Black, Segoe UI, Microsoft YaHei, sans-serif" font-size="48" font-style="italic" font-weight="900" letter-spacing="1">FOLLOW</text>

  <!-- Decorative dots and diamonds -->
  <circle cx="99" cy="383" r="9" fill="#ffffff"/>
  <circle cx="778" cy="535" r="9" fill="#ffffff"/>
  <circle cx="795" cy="49" r="9" fill="#ffffff"/>
  <circle cx="1140" cy="620" r="9" fill="#ffffff"/>
  <circle cx="63" cy="100" r="10" fill="#ffffff"/>

  <rect x="50" y="86" width="27" height="27" rx="3" fill="#ffffff" transform="rotate(45 63.5 99.5)"/>
  <rect x="217" y="196" width="13" height="13" rx="2" fill="#e11d48" transform="rotate(45 223.5 202.5)"/>
  <rect x="1081" y="162" width="13" height="13" rx="2" fill="#e11d48" transform="rotate(45 1087.5 168.5)"/>
  <rect x="1081" y="510" width="13" height="13" rx="2" fill="#e11d48" transform="rotate(45 1087.5 516.5)"/>
  <rect x="137" y="642" width="13" height="13" rx="2" fill="#ffffff" transform="rotate(45 143.5 648.5)"/>

  <text x="174" y="668" width="460" fill="#a7b0c4" font-family="Segoe UI Black, Segoe UI, Microsoft YaHei, sans-serif" font-size="52" font-style="italic" font-weight="900" letter-spacing="1.5" opacity="0.9">MOTION GRAPHIC</text>
  <rect x="650" y="643" width="13" height="13" rx="2" fill="#ffffff" transform="rotate(45 656.5 649.5)"/>
</svg>
```

## Avoid in this skill
- ❌ Using `<mask>` to create the partial donut/U-arc; draw the visible arc directly with a thick stroked `<path>` instead.
- ❌ Applying `filter` to constellation `<line>` elements; filters on lines are dropped, so keep lines flat and use opacity/color for depth.
- ❌ Building arrowheads with `marker-end`; use small filled triangular `<path>` shapes for the play chevrons.
- ❌ Omitting `width` on `<text>`; every text object needs an explicit width for clean PowerPoint text box rendering.
- ❌ Over-bright constellation strokes; the network should sit behind the card, not compete with the headline.

## Composition notes
- Keep the main card left-of-center, occupying roughly the middle 35% of slide width; its fill should match the background exactly so the shadow creates the separation.
- Place the constellation and U-arc behind the panel, with parts hidden naturally by the foreground rectangle to create depth.
- Use white text and dots sparingly, then repeat small red diamonds as the only hot accent to avoid breaking the monochrome neumorphic mood.
- Reserve the right third for breathing room and the CTA button; the constellation should feel technical but airy, not like a dense chart.