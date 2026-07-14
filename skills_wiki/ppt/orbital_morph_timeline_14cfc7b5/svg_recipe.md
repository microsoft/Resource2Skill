# SVG Recipe — Orbital Morph Timeline

## Visual mechanism
A giant off-screen planet acts as the rotational pivot for a radial timeline: milestone cards sit on invisible orbital rings and appear to sweep through space as the slide sequence morph-rotates the whole orbital system. The composition feels cinematic because only one milestone is dominant in the readable center-left zone while the planet, orbit arcs, stars, and dimmed nodes maintain global high-tech context.

## SVG primitives needed
- 1× `<rect>` for the full-slide deep-space gradient background
- 2× blurred `<circle>` elements for nebula glows behind the timeline and planet
- 25–40× small `<circle>` elements for stars and star clusters
- 1× `<image>` clipped by a circular `<clipPath>` for the planetary texture
- 2–3× translucent `<circle>` elements over the planet for atmosphere, rim light, and dark-side shading
- 3× dashed `<path>` elements for large orbital arcs centered on the planet pivot
- 5× timeline node groups made from `<rect>`, `<circle>`, `<line>`, and `<text>`
- 1× highlighted active node card using a brighter gradient fill, thicker connector, and glow filter
- Several `<linearGradient>` and `<radialGradient>` definitions for background, planet lighting, cards, and accents
- 2× `<filter>` definitions: one soft glow for orbit/active elements, one shadow for cards and planet depth
- Multiple `<text>` elements with explicit `width` attributes for title, subtitle, years, milestone titles, and descriptions

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="spaceBg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#0D111C"/>
      <stop offset="55%" stop-color="#071A3B"/>
      <stop offset="100%" stop-color="#020713"/>
    </linearGradient>

    <radialGradient id="nebulaBlue" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#2B76FF" stop-opacity="0.38"/>
      <stop offset="55%" stop-color="#0C3E88" stop-opacity="0.14"/>
      <stop offset="100%" stop-color="#071A3B" stop-opacity="0"/>
    </radialGradient>

    <radialGradient id="planetShade" cx="34%" cy="28%" r="72%">
      <stop offset="0%" stop-color="#74D5FF" stop-opacity="0.34"/>
      <stop offset="42%" stop-color="#1459B5" stop-opacity="0.16"/>
      <stop offset="78%" stop-color="#020713" stop-opacity="0.36"/>
      <stop offset="100%" stop-color="#000000" stop-opacity="0.72"/>
    </radialGradient>

    <linearGradient id="activeCard" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#183A66" stop-opacity="0.96"/>
      <stop offset="100%" stop-color="#061323" stop-opacity="0.94"/>
    </linearGradient>

    <linearGradient id="dimCard" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#172033" stop-opacity="0.72"/>
      <stop offset="100%" stop-color="#07101E" stop-opacity="0.62"/>
    </linearGradient>

    <filter id="softGlow" x="-80%" y="-80%" width="260%" height="260%">
      <feGaussianBlur stdDeviation="8" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="cardShadow" x="-40%" y="-40%" width="180%" height="180%">
      <feOffset dx="0" dy="12" result="off"/>
      <feGaussianBlur in="off" stdDeviation="18" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <clipPath id="planetClip">
      <circle cx="1010" cy="610" r="430"/>
    </clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#spaceBg)"/>
  <circle cx="560" cy="260" r="360" fill="url(#nebulaBlue)" filter="url(#softGlow)" opacity="0.8"/>
  <circle cx="1010" cy="610" r="520" fill="#0B4C94" opacity="0.16" filter="url(#softGlow)"/>

  <circle cx="84" cy="72" r="1.4" fill="#FFFFFF" opacity="0.9"/>
  <circle cx="168" cy="132" r="1.1" fill="#9AD9FF" opacity="0.7"/>
  <circle cx="252" cy="58" r="1.8" fill="#FFFFFF" opacity="0.8"/>
  <circle cx="418" cy="104" r="1.2" fill="#F4D48A" opacity="0.75"/>
  <circle cx="612" cy="74" r="1.5" fill="#FFFFFF" opacity="0.85"/>
  <circle cx="748" cy="146" r="1.1" fill="#9AD9FF" opacity="0.7"/>
  <circle cx="934" cy="82" r="1.7" fill="#FFFFFF" opacity="0.8"/>
  <circle cx="1148" cy="128" r="1.3" fill="#FFFFFF" opacity="0.72"/>
  <circle cx="104" cy="314" r="1.3" fill="#FFFFFF" opacity="0.65"/>
  <circle cx="302" cy="248" r="2.1" fill="#9AD9FF" opacity="0.85"/>
  <circle cx="500" cy="350" r="1.2" fill="#FFFFFF" opacity="0.7"/>
  <circle cx="820" cy="302" r="1.5" fill="#F4D48A" opacity="0.78"/>
  <circle cx="1164" cy="342" r="1.1" fill="#FFFFFF" opacity="0.65"/>
  <circle cx="192" cy="586" r="1.4" fill="#FFFFFF" opacity="0.72"/>
  <circle cx="392" cy="656" r="1.2" fill="#9AD9FF" opacity="0.6"/>
  <circle cx="690" cy="610" r="1.8" fill="#FFFFFF" opacity="0.78"/>

  <text x="72" y="82" width="560" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="700" fill="#FFFFFF" letter-spacing="0.5">
    GoTech 发展历程
  </text>
  <text x="74" y="116" width="520" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#9FB7D8" letter-spacing="2.2">
    ORBITAL ROADMAP · GLOBAL TECHNOLOGY EVOLUTION
  </text>

  <path d="M 392 608 A 620 620 0 0 1 870 18" fill="none" stroke="#2E8CFF" stroke-width="1.4" stroke-opacity="0.42" stroke-dasharray="8 12" filter="url(#softGlow)"/>
  <path d="M 305 535 A 720 720 0 0 1 1018 -110" fill="none" stroke="#FFFFFF" stroke-width="0.9" stroke-opacity="0.18" stroke-dasharray="2 14"/>
  <path d="M 470 690 A 520 520 0 0 1 870 120" fill="none" stroke="#F2C056" stroke-width="1.2" stroke-opacity="0.42" stroke-dasharray="16 18"/>

  <image href="https://images.example.com/blue-earth-night-lights-clouds-high-resolution.jpg"
         x="580" y="180" width="860" height="860" preserveAspectRatio="xMidYMid slice"
         clip-path="url(#planetClip)"/>
  <circle cx="1010" cy="610" r="430" fill="url(#planetShade)"/>
  <circle cx="1010" cy="610" r="430" fill="none" stroke="#69D8FF" stroke-width="3" stroke-opacity="0.48" filter="url(#softGlow)"/>
  <circle cx="892" cy="438" r="120" fill="#B8F4FF" opacity="0.12" filter="url(#softGlow)"/>

  <g transform="rotate(-12 540 395)">
    <line x1="540" y1="395" x2="944" y2="590" stroke="#F2C056" stroke-width="2.2" stroke-opacity="0.72"/>
    <circle cx="540" cy="395" r="9" fill="#F2C056" filter="url(#softGlow)"/>
    <rect x="248" y="322" width="300" height="118" rx="18" fill="url(#activeCard)" stroke="#F2C056" stroke-width="1.6" filter="url(#cardShadow)"/>
    <text x="272" y="360" width="250" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="800" fill="#F2C056">2026</text>
    <text x="272" y="388" width="250" font-family="Segoe UI, Microsoft YaHei" font-size="21" font-weight="650" fill="#FFFFFF">Global AI Platform</text>
    <text x="272" y="416" width="250" font-family="Segoe UI, Microsoft YaHei" font-size="13.5" fill="#C9D5E6">Unified cloud intelligence deployed across 36 markets.</text>
  </g>

  <g transform="rotate(-28 705 252)">
    <line x1="705" y1="252" x2="965" y2="560" stroke="#6BB7FF" stroke-width="1.3" stroke-opacity="0.38"/>
    <circle cx="705" cy="252" r="6" fill="#6BB7FF" opacity="0.8"/>
    <rect x="536" y="198" width="230" height="86" rx="15" fill="url(#dimCard)" stroke="#6BB7FF" stroke-width="0.9" opacity="0.86"/>
    <text x="556" y="230" width="190" font-family="Segoe UI, Microsoft YaHei" font-size="24" font-weight="750" fill="#BBDFFF">2024</text>
    <text x="556" y="258" width="190" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="600" fill="#FFFFFF">Edge Network</text>
  </g>

  <g transform="rotate(-42 842 136)">
    <line x1="842" y1="136" x2="986" y2="548" stroke="#6BB7FF" stroke-width="1.1" stroke-opacity="0.28"/>
    <circle cx="842" cy="136" r="5" fill="#6BB7FF" opacity="0.6"/>
    <rect x="702" y="94" width="205" height="72" rx="14" fill="url(#dimCard)" stroke="#6BB7FF" stroke-width="0.8" opacity="0.62"/>
    <text x="720" y="123" width="170" font-family="Segoe UI, Microsoft YaHei" font-size="21" font-weight="750" fill="#A6CFFF">2022</text>
    <text x="720" y="148" width="170" font-family="Segoe UI, Microsoft YaHei" font-size="13.5" fill="#D9E7F7">First overseas hub</text>
  </g>

  <g transform="rotate(10 474 553)">
    <line x1="474" y1="553" x2="930" y2="618" stroke="#FFFFFF" stroke-width="1.1" stroke-opacity="0.22"/>
    <circle cx="474" cy="553" r="5.5" fill="#FFFFFF" opacity="0.52"/>
    <rect x="248" y="512" width="218" height="76" rx="14" fill="url(#dimCard)" stroke="#FFFFFF" stroke-width="0.7" opacity="0.58"/>
    <text x="266" y="540" width="176" font-family="Segoe UI, Microsoft YaHei" font-size="21" font-weight="750" fill="#E6EDF7">2020</text>
    <text x="266" y="565" width="176" font-family="Segoe UI, Microsoft YaHei" font-size="13.5" fill="#BFC9D8">Cloud-native launch</text>
  </g>

  <g transform="rotate(24 392 682)">
    <line x1="392" y1="682" x2="906" y2="646" stroke="#FFFFFF" stroke-width="1" stroke-opacity="0.14"/>
    <circle cx="392" cy="682" r="5" fill="#FFFFFF" opacity="0.35"/>
    <rect x="170" y="642" width="210" height="70" rx="14" fill="url(#dimCard)" stroke="#FFFFFF" stroke-width="0.7" opacity="0.38"/>
    <text x="188" y="670" width="170" font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="750" fill="#D6DEEA">2018</text>
    <text x="188" y="694" width="170" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#AAB5C5">Founded in Shenzhen</text>
  </g>

  <text x="928" y="676" width="230" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#8EA9C8" letter-spacing="1.4">
    PIVOT: duplicate slides and rotate this orbital system around the planet center
  </text>
</svg>
```

## Avoid in this skill
- ❌ Do not use SVG `<animate>` or `<animateTransform>` for the orbiting motion; create several PPT slides and use PowerPoint Morph between rotated states.
- ❌ Do not use `<mask>` to crop the planet; use `<clipPath>` only on the `<image>` element.
- ❌ Do not put `filter` on `<line>` connectors; if glow is needed, use a glowing `<path>` or glowing `<circle>` near the node.
- ❌ Do not use `<textPath>` for orbital labels; rotate regular `<text>` or whole node groups instead.
- ❌ Do not rely on `marker-end` for arrows on orbital paths; timeline motion should be implied by dashed arcs, node placement, and Morph rotation.

## Composition notes
- Keep the planet center around `(1000, 610)` with a radius of roughly `420–460`, so the sphere bleeds off the bottom-right and feels macro-scale.
- Place the active milestone in the center-left reading zone, around `x=240–560`, `y=300–440`; dim earlier/later milestones as they rotate toward edges.
- Use a dark navy background with cyan orbit lines and one warm gold accent for the active year to create a premium technology keynote mood.
- For a real Morph sequence, duplicate the slide 4–6 times and rotate the entire timeline-node/orbit system around the planet center by about `-25°` to `-35°` per slide while keeping object structure consistent.