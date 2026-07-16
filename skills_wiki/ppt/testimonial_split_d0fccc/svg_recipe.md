# SVG Recipe — Testimonial Split

## Visual mechanism
A warm editorial split layout: the top half is a full-bleed hero image with a dark gradient overlay and title, while the bottom half is a soft testimonial panel that rises into the image with an organic curve. The quote is treated as the primary content, supported by a circular author portrait and compact attribution.

## SVG primitives needed
- 1× `<image>` for the full-width hero photo header
- 1× `<image>` for the circular author portrait
- 2× `<clipPath>` definitions for rounded hero cropping and circular avatar cropping
- 2× `<linearGradient>` definitions for image readability overlay and warm panel shading
- 1× `<radialGradient>` for a subtle ambient glow in the testimonial panel
- 1× `<filter id="softShadow">` applied to the lower quote panel
- 1× `<rect>` for the slide background
- 1× `<path>` for the curved lower testimonial panel
- 2× `<rect>` overlays for darkening the hero image and creating a small kicker pill
- 2× `<circle>` shapes for avatar ring and decorative quote accent
- 1× `<path>` for a large decorative quotation-mark flourish
- 1× `<line>` for a small author divider rule
- Multiple `<text>` elements with explicit `width` attributes for kicker, headline, quote, author name, and author title

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <clipPath id="heroClip">
      <rect x="0" y="0" width="1280" height="470" rx="0" ry="0"/>
    </clipPath>

    <clipPath id="avatarClip">
      <circle cx="214" cy="548" r="54"/>
    </clipPath>

    <linearGradient id="heroFade" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#111827" stop-opacity="0.30"/>
      <stop offset="48%" stop-color="#111827" stop-opacity="0.18"/>
      <stop offset="100%" stop-color="#111827" stop-opacity="0.72"/>
    </linearGradient>

    <linearGradient id="panelWarmth" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#FFF7ED"/>
      <stop offset="58%" stop-color="#FFFDF9"/>
      <stop offset="100%" stop-color="#F5E7D8"/>
    </linearGradient>

    <radialGradient id="quoteGlow" cx="0.35" cy="0.25" r="0.85">
      <stop offset="0%" stop-color="#FBBF77" stop-opacity="0.34"/>
      <stop offset="55%" stop-color="#FBBF77" stop-opacity="0.08"/>
      <stop offset="100%" stop-color="#FBBF77" stop-opacity="0"/>
    </radialGradient>

    <filter id="softShadow" x="-10%" y="-20%" width="120%" height="150%">
      <feOffset dx="0" dy="-8"/>
      <feGaussianBlur stdDeviation="18"/>
      <feColorMatrix type="matrix" values="0 0 0 0 0.28  0 0 0 0 0.18  0 0 0 0 0.10  0 0 0 0.18 0"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#14110F"/>

  <image
    href="https://images.example.com/testimonial-hero-warm-studio-team-meeting.jpg"
    x="0" y="0" width="1280" height="470"
    preserveAspectRatio="xMidYMid slice"
    clip-path="url(#heroClip)"/>

  <rect x="0" y="0" width="1280" height="470" fill="url(#heroFade)"/>

  <rect x="78" y="70" width="176" height="34" rx="17" fill="#FFFFFF" opacity="0.18"/>
  <text x="102" y="93" width="220"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="13" font-weight="700" letter-spacing="2.2"
        fill="#FFFFFF">CLIENT STORY</text>

  <text x="78" y="176" width="720"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="58" font-weight="750"
        fill="#FFFFFF">
    <tspan x="78" dy="0">A calmer way to</tspan>
    <tspan x="78" dy="66">scale customer care</tspan>
  </text>

  <text x="82" y="327" width="520"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="18" font-weight="400"
        fill="#FDEBD8" opacity="0.95">
    How Brightline reduced response times without losing their human voice.
  </text>

  <path d="M0,398
           C190,356 344,430 538,392
           C739,352 915,358 1280,404
           L1280,720 L0,720 Z"
        fill="url(#panelWarmth)"
        filter="url(#softShadow)"/>

  <path d="M0,398
           C190,356 344,430 538,392
           C739,352 915,358 1280,404
           L1280,720 L0,720 Z"
        fill="url(#quoteGlow)" opacity="0.85"/>

  <circle cx="214" cy="548" r="61" fill="#FFFFFF"/>
  <circle cx="214" cy="548" r="59" fill="#E8C7AA"/>
  <image
    href="https://images.example.com/author-portrait-woman-founder-square.jpg"
    x="160" y="494" width="108" height="108"
    preserveAspectRatio="xMidYMid slice"
    clip-path="url(#avatarClip)"/>

  <line x1="154" y1="638" x2="274" y2="638" stroke="#D7B799" stroke-width="2"/>

  <text x="120" y="658" width="190"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="21" font-weight="750"
        text-anchor="middle"
        fill="#2C211A">Maya Chen</text>

  <text x="120" y="684" width="190"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="14" font-weight="500"
        text-anchor="middle"
        fill="#8A6B55">COO, Brightline</text>

  <circle cx="420" cy="500" r="38" fill="#F5C38E" opacity="0.26"/>

  <path d="M405,520
           C390,520 380,508 380,491
           C380,467 397,451 424,443
           L429,455
           C414,461 406,470 406,481
           C418,482 426,491 426,503
           C426,513 418,520 405,520
           Z
           M462,520
           C447,520 437,508 437,491
           C437,467 454,451 481,443
           L486,455
           C471,461 463,470 463,481
           C475,482 483,491 483,503
           C483,513 475,520 462,520
           Z"
        fill="#B77948" opacity="0.18"/>

  <text x="430" y="500" width="720"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="34" font-weight="550"
        fill="#2B211B">
    <tspan x="430" dy="0">“The team gave us a system that feels</tspan>
    <tspan x="430" dy="44">personal at every touchpoint — even as</tspan>
    <tspan x="430" dy="44">our volume doubled in one quarter.”</tspan>
  </text>

  <text x="432" y="660" width="510"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="15" font-weight="650"
        letter-spacing="1.4"
        fill="#A76B3C">CUSTOMER EXPERIENCE TRANSFORMATION</text>

  <rect x="1012" y="624" width="118" height="6" rx="3" fill="#D7A36B"/>
  <rect x="1142" y="624" width="56" height="6" rx="3" fill="#EAD2BC"/>
</svg>
```

## Avoid in this skill
- ❌ Do not use a `<mask>` to fade the hero image; use an editable gradient `<rect>` overlay instead.
- ❌ Do not clip the curved lower panel with `clip-path`; draw it directly as a `<path>`.
- ❌ Do not place the author image inside a `<g>` with clipping; apply `clip-path` directly to the `<image>`.
- ❌ Do not rely on `<textPath>` for curved quote styling; keep quote text in normal editable `<text>` blocks.
- ❌ Do not use `<filter>` on separator lines; shadows should be reserved for the panel or large filled shapes.

## Composition notes
- Keep the hero image in the upper 55–65% of the slide, with headline text anchored top-left and enough dark overlay for legibility.
- Let the lower testimonial panel overlap the image with a curved edge; this creates a premium editorial transition instead of a rigid horizontal split.
- Place author identity in a compact left column and the quote in a wider right column; the quote should occupy the visual center of the lower panel.
- Use warm neutrals, soft browns, and restrained accent bars to support a human testimonial mood without competing with the hero image.