# SVG Recipe — Translucent Vellum Quote Overlay (Vintage Craft Aesthetic)

## Visual mechanism
A busy vintage floral background is softened by a centered semi-transparent “vellum sticker” panel with a diffused shadow, rounded corners, and nested antique borders. Mixed typography sits on the vellum while paper-craft rosettes and botanical accents overlap the panel corners to make the slide feel tactile and handmade.

## SVG primitives needed
- 1× `<image>` for the full-bleed vintage floral / craft-paper background
- 2× `<rect>` for warm color washes over the background and the translucent vellum base
- 2× `<rect>` for nested rounded antique-gold borders inside the vellum
- 2× `<filter>`: one diffused drop shadow for vellum and rosettes, one soft blur/glow for atmospheric background tint
- 3× `<linearGradient>` for background warming, vellum sheen, and paper rosette fills
- 2× `<radialGradient>` for floral rosette centers and soft vignette accents
- 8–12× `<path>` for rosette petals, leaves, corner flourishes, and decorative botanical shapes
- 6–8× `<circle>` / `<ellipse>` for rosette centers, pearl dots, and small craft embellishments
- 5× `<text>` with explicit `width` attributes for editable quote typography, author label, and small decorative labels
- Optional `<line>` elements for short divider rules; do not use markers or arrowheads

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="warmWash" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#f6d5cf" stop-opacity="0.34"/>
      <stop offset="52%" stop-color="#fff4df" stop-opacity="0.16"/>
      <stop offset="100%" stop-color="#9fb99b" stop-opacity="0.28"/>
    </linearGradient>

    <linearGradient id="vellumSheen" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#ffffff" stop-opacity="0.92"/>
      <stop offset="48%" stop-color="#fffaf1" stop-opacity="0.84"/>
      <stop offset="100%" stop-color="#ffffff" stop-opacity="0.78"/>
    </linearGradient>

    <linearGradient id="pinkPaper" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#f1a7b4"/>
      <stop offset="100%" stop-color="#c96f82"/>
    </linearGradient>

    <radialGradient id="goldCenter" cx="50%" cy="45%" r="60%">
      <stop offset="0%" stop-color="#fff1bb"/>
      <stop offset="100%" stop-color="#b9944f"/>
    </radialGradient>

    <radialGradient id="softVignette" cx="50%" cy="50%" r="65%">
      <stop offset="0%" stop-color="#ffffff" stop-opacity="0"/>
      <stop offset="100%" stop-color="#3b2a28" stop-opacity="0.24"/>
    </radialGradient>

    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feOffset dx="0" dy="12" result="off"/>
      <feGaussianBlur in="off" stdDeviation="16" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="blurGlow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="22"/>
    </filter>
  </defs>

  <image href="https://images.example.com/vintage-floral-wallpaper-soft-pink-sage-craft-paper.jpg"
         x="0" y="0" width="1280" height="720" preserveAspectRatio="xMidYMid slice"/>
  <rect x="0" y="0" width="1280" height="720" fill="url(#warmWash)"/>
  <rect x="0" y="0" width="1280" height="720" fill="url(#softVignette)"/>

  <ellipse cx="176" cy="112" rx="170" ry="80" fill="#f2c7bd" opacity="0.22" filter="url(#blurGlow)"/>
  <ellipse cx="1110" cy="610" rx="210" ry="96" fill="#b8cba7" opacity="0.24" filter="url(#blurGlow)"/>

  <rect x="315" y="142" width="650" height="438" rx="34" fill="url(#vellumSheen)" opacity="0.88" filter="url(#softShadow)"/>
  <rect x="344" y="170" width="592" height="382" rx="25" fill="none" stroke="#bfa064" stroke-width="4"/>
  <rect x="358" y="184" width="564" height="354" rx="20" fill="none" stroke="#bfa064" stroke-width="1.4" opacity="0.58"/>

  <path d="M392 218 C415 198, 449 200, 466 228 C438 222, 418 232, 402 252 C400 240, 396 228, 392 218 Z"
        fill="#9fb99b" opacity="0.72"/>
  <path d="M888 500 C863 528, 828 526, 812 496 C842 504, 864 492, 878 470 C880 483, 884 493, 888 500 Z"
        fill="#9fb99b" opacity="0.72"/>

  <g transform="translate(292 131) rotate(-18)" filter="url(#softShadow)">
    <path d="M0,-56 L14,-24 L48,-36 L32,-6 L62,12 L27,17 L34,52 L6,30 L-19,57 L-18,21 L-55,18 L-25,-3 L-45,-35 L-10,-23 Z"
          fill="url(#pinkPaper)"/>
    <circle cx="0" cy="0" r="27" fill="#f7d8df" stroke="#ffffff" stroke-width="3" opacity="0.96"/>
    <circle cx="0" cy="0" r="13" fill="url(#goldCenter)"/>
    <ellipse cx="-38" cy="36" rx="18" ry="8" fill="#8cae87" transform="rotate(-26 -38 36)"/>
    <ellipse cx="41" cy="-32" rx="20" ry="8" fill="#9fb99b" transform="rotate(-34 41 -32)"/>
  </g>

  <g transform="translate(970 568) rotate(15)" filter="url(#softShadow)">
    <path d="M0,-64 L16,-28 L54,-42 L36,-8 L70,13 L30,20 L40,58 L7,34 L-22,64 L-22,24 L-64,21 L-29,-4 L-51,-40 L-12,-26 Z"
          fill="#d98ba0"/>
    <circle cx="0" cy="0" r="31" fill="#f3c0cb" stroke="#fff6ee" stroke-width="4"/>
    <circle cx="0" cy="0" r="14" fill="url(#goldCenter)"/>
    <ellipse cx="-45" cy="-22" rx="22" ry="9" fill="#91ad86" transform="rotate(22 -45 -22)"/>
    <ellipse cx="50" cy="32" rx="24" ry="9" fill="#a9bf9e" transform="rotate(18 50 32)"/>
  </g>

  <circle cx="372" cy="535" r="5" fill="#bfa064" opacity="0.8"/>
  <circle cx="394" cy="535" r="3.5" fill="#d98ba0" opacity="0.72"/>
  <circle cx="416" cy="535" r="5" fill="#bfa064" opacity="0.8"/>
  <circle cx="864" cy="187" r="4" fill="#d98ba0" opacity="0.72"/>
  <circle cx="886" cy="187" r="5" fill="#bfa064" opacity="0.8"/>
  <circle cx="908" cy="187" r="4" fill="#d98ba0" opacity="0.72"/>

  <text x="390" y="240" width="500" font-family="Segoe UI, Microsoft YaHei" font-size="15"
        letter-spacing="4" fill="#9a7b46" text-anchor="middle">
    <tspan x="640">A GENTLE REMINDER</tspan>
  </text>

  <line x1="488" y1="265" x2="792" y2="265" stroke="#bfa064" stroke-width="1.2" opacity="0.62"/>

  <text x="390" y="330" width="500" font-family="Georgia, Segoe UI, Microsoft YaHei" font-size="46"
        font-weight="700" letter-spacing="1.5" fill="#333333" text-anchor="middle">
    <tspan x="640">THERE IS NO TIME</tspan>
  </text>

  <text x="390" y="398" width="500" font-family="Georgia, Segoe UI, Microsoft YaHei" font-size="44"
        font-style="italic" fill="#d27c91" text-anchor="middle">
    <tspan x="640">like the present</tspan>
  </text>

  <text x="430" y="456" width="420" font-family="Segoe UI, Microsoft YaHei" font-size="17"
        fill="#4a4a4a" text-anchor="middle">
    <tspan x="640">Begin where you are, with what you have,</tspan>
    <tspan x="640" dy="25">and let the day become something beautiful.</tspan>
  </text>

  <line x1="530" y1="508" x2="750" y2="508" stroke="#bfa064" stroke-width="1.2" opacity="0.55"/>

  <text x="490" y="534" width="300" font-family="Segoe UI, Microsoft YaHei" font-size="13"
        letter-spacing="3" fill="#7c765f" text-anchor="middle">
    <tspan x="640">VINTAGE CRAFT NOTES</tspan>
  </text>
</svg>
```

## Avoid in this skill
- ❌ Do not use `backdrop-filter` or SVG masks to blur the background behind the vellum; PowerPoint translation will not preserve that effect. Simulate vellum with translucent white/cream fills plus soft shadow.
- ❌ Do not use `<pattern>` fills for paper grain or floral wallpaper. Use a full-bleed `<image>` or hand-placed decorative paths/circles instead.
- ❌ Do not apply `clip-path` to the vellum rectangle or decorative paths; clipping is only reliable on `<image>` elements.
- ❌ Do not build rosettes with `<use>` or `<symbol>` duplication. Duplicate the editable paths directly.
- ❌ Do not put filters on `<line>` dividers; apply blur/shadow only to rects, circles, ellipses, paths, or text.

## Composition notes
- Keep the vellum panel centered and sized to roughly 50–55% of slide width and 55–65% of slide height, leaving enough floral background visible around all sides.
- Use a warm, low-contrast palette: antique gold borders, dusty pink accents, sage leaves, charcoal text, and creamy whites.
- Let the rosettes overlap opposite vellum corners so the panel feels physically layered rather than digitally boxed.
- Text should sit in a calm vertical stack: small tracked label, bold serif headline, italic/script-like accent line, then a smaller supporting quote.