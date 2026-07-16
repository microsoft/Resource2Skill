# SVG Recipe — Typographic Hierarchy & Contrast

## Visual mechanism
Create a premium text-led slide by making one typographic voice dominant through scale, weight, and font personality, then supporting it with smaller, cleaner sans-serif copy. A dark textured field, a rigid vertical accent, and generous negative space make the hierarchy feel intentional rather than merely large.

## SVG primitives needed
- 1× `<image>` for a dark abstract/photo texture background
- 2× full-slide `<rect>` overlays for darkening, color wash, and vignette control
- 3× `<linearGradient>` / `<radialGradient>` definitions for background depth, accent glow, and headline emphasis
- 1× `<filter id="softShadow">` applied to the headline text and accent card for depth
- 2× blurred `<ellipse>` / `<path>` shapes for atmospheric color glows behind the typography
- 1× narrow `<rect>` for the strong vertical typographic anchor
- 1× translucent rounded `<rect>` for the body-copy reading panel
- 5× `<text>` elements for eyebrow, headline, subtitle, body copy, and small footer note
- Multiple `<tspan>` elements inside text for controlled line breaks and inline emphasis

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="darkWash" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#070A13" stop-opacity="0.96"/>
      <stop offset="45%" stop-color="#12182B" stop-opacity="0.90"/>
      <stop offset="100%" stop-color="#05060B" stop-opacity="0.98"/>
    </linearGradient>

    <radialGradient id="vignette" cx="62%" cy="45%" r="75%">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0"/>
      <stop offset="58%" stop-color="#050814" stop-opacity="0.24"/>
      <stop offset="100%" stop-color="#000000" stop-opacity="0.72"/>
    </radialGradient>

    <linearGradient id="accentGold" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#FFF1B8"/>
      <stop offset="48%" stop-color="#D7A84C"/>
      <stop offset="100%" stop-color="#7C5520"/>
    </linearGradient>

    <linearGradient id="bodyPanel" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.13"/>
      <stop offset="100%" stop-color="#FFFFFF" stop-opacity="0.04"/>
    </linearGradient>

    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="10" in="SourceAlpha" result="off"/>
      <feGaussianBlur in="off" stdDeviation="14" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="atmosphereBlur" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="34"/>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#070A13"/>

  <image
    href="https://images.unsplash.com/photo-1519608487953-e999c86e7455?auto=format&amp;fit=crop&amp;w=1280&amp;h=720"
    x="0" y="0" width="1280" height="720" preserveAspectRatio="xMidYMid slice" opacity="0.42"/>

  <rect x="0" y="0" width="1280" height="720" fill="url(#darkWash)"/>
  <rect x="0" y="0" width="1280" height="720" fill="url(#vignette)"/>

  <ellipse cx="1070" cy="105" rx="310" ry="150" fill="#2647FF" opacity="0.22" filter="url(#atmosphereBlur)"/>
  <path d="M925,520 C1015,440 1144,448 1212,530 C1262,590 1216,674 1125,684 C1018,696 884,625 925,520 Z"
        fill="#C8913C" opacity="0.18" filter="url(#atmosphereBlur)"/>

  <rect x="120" y="150" width="10" height="330" rx="5" fill="url(#accentGold)" filter="url(#softShadow)"/>
  <rect x="152" y="486" width="520" height="118" rx="26" fill="url(#bodyPanel)" stroke="#FFFFFF" stroke-opacity="0.16"/>

  <text x="154" y="145" width="580"
        font-family="Mulish, Segoe UI, Microsoft YaHei, sans-serif"
        font-size="15" font-weight="700" letter-spacing="4"
        fill="#D7A84C">
    EXECUTIVE DESIGN SYSTEM
  </text>

  <text x="152" y="252" width="860"
        font-family="Roboto Slab, Georgia, Segoe UI, Microsoft YaHei, serif"
        font-size="88" font-weight="800"
        fill="#FFFFFF" filter="url(#softShadow)">
    <tspan x="152" dy="0">TYPE BUILDS</tspan>
    <tspan x="152" dy="92">CLARITY.</tspan>
  </text>

  <text x="156" y="410" width="720"
        font-family="Mulish, Segoe UI, Microsoft YaHei, sans-serif"
        font-size="28" font-weight="800"
        fill="#F3F5FF">
    <tspan>Use contrast to tell the room what matters first.</tspan>
  </text>

  <text x="180" y="526" width="462"
        font-family="Mulish, Segoe UI, Microsoft YaHei, sans-serif"
        font-size="17" font-weight="400"
        fill="#DDE3F4">
    <tspan x="180" dy="0">Pair a high-impact headline with a quiet, readable</tspan>
    <tspan x="180" dy="26">supporting face. Scale, weight, spacing, and rhythm</tspan>
    <tspan x="180" dy="26">create hierarchy before the audience reads a word.</tspan>
  </text>

  <text x="905" y="575" width="250"
        font-family="Mulish, Segoe UI, Microsoft YaHei, sans-serif"
        font-size="13" font-weight="700" letter-spacing="2.4"
        fill="#FFFFFF" opacity="0.62">
    SLAB HEADLINE + SANS BODY
  </text>

  <line x1="905" y1="592" x2="1155" y2="592" stroke="#D7A84C" stroke-width="2" stroke-dasharray="10 8"/>
</svg>
```

## Avoid in this skill
- ❌ Using one font size with only bold/regular changes; hierarchy should come from scale, weight, spacing, and position together.
- ❌ Centering every text box by default; typographic contrast usually looks stronger with one clear alignment edge.
- ❌ Long all-caps body copy; reserve uppercase and letter spacing for short eyebrow labels or metadata.
- ❌ Applying decorative effects to every text level; keep the headline expressive and the body copy calm.
- ❌ Relying on unsupported text features such as `<textPath>` or clipping text with masks.

## Composition notes
- Keep the dominant headline on one side of the slide, occupying roughly 40–55% of the canvas width and 25–35% of the height.
- Use a single hard alignment edge: the vertical accent, eyebrow, headline, subtitle, and body panel should all lock to the same left margin.
- Protect negative space around the headline; do not let body text crowd the main typographic gesture.
- Use color sparingly: white for hierarchy, muted blue/charcoal for atmosphere, and one warm accent for structure and premium contrast.