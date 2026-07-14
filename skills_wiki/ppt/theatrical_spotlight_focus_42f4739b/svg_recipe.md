# SVG Recipe — Theatrical Spotlight Focus

## Visual mechanism
Create a dark stage environment where semi-transparent white light beams descend from visible overhead fixtures and overlap on a bright elliptical stage pool. The brightest center area holds the hero content, making the person, product, or announcement feel like a live reveal.

## SVG primitives needed
- 2× `<rect>` for the dark background and top truss bar
- 6× `<line>` for truss cross-bracing and hanging rig details
- 8× `<path>` for wide and narrow spotlight beam polygons
- 4× grouped fixture assemblies using `<rect>`, `<circle>`, and `<ellipse>` for lamps and lenses
- 2× `<ellipse>` for the glowing stage pool and its bright core
- 1× `<image>` clipped by a circular `<clipPath>` for the featured portrait or product image
- 2× `<circle>` for avatar border and subtle halo
- 5× `<text>` elements for title, name, role, and small stage-label copy
- 2× `<linearGradient>` for moody background and light beams
- 2× `<radialGradient>` for vignette and stage glow
- 2× `<filter>` definitions: one soft glow for light/stage, one shadow for the portrait card

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgPurple" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#16051f"/>
      <stop offset="48%" stop-color="#4b0f69"/>
      <stop offset="100%" stop-color="#0b0615"/>
    </linearGradient>

    <radialGradient id="vignette" cx="50%" cy="48%" r="70%">
      <stop offset="0%" stop-color="#7d2aa1" stop-opacity="0"/>
      <stop offset="68%" stop-color="#1a0629" stop-opacity="0.28"/>
      <stop offset="100%" stop-color="#000000" stop-opacity="0.66"/>
    </radialGradient>

    <linearGradient id="beamWhite" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#ffffff" stop-opacity="0.08"/>
      <stop offset="42%" stop-color="#ffffff" stop-opacity="0.28"/>
      <stop offset="100%" stop-color="#ffffff" stop-opacity="0.42"/>
    </linearGradient>

    <linearGradient id="beamGold" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#fff4bf" stop-opacity="0.05"/>
      <stop offset="55%" stop-color="#ffffff" stop-opacity="0.22"/>
      <stop offset="100%" stop-color="#fff8d9" stop-opacity="0.38"/>
    </linearGradient>

    <radialGradient id="stageGlow" cx="50%" cy="50%" r="58%">
      <stop offset="0%" stop-color="#ffffff" stop-opacity="1"/>
      <stop offset="42%" stop-color="#fff6d6" stop-opacity="0.82"/>
      <stop offset="74%" stop-color="#d8b7ff" stop-opacity="0.30"/>
      <stop offset="100%" stop-color="#ffffff" stop-opacity="0"/>
    </radialGradient>

    <filter id="softGlow" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="14" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="portraitShadow" x="-35%" y="-35%" width="170%" height="170%">
      <feOffset dx="0" dy="16" result="off"/>
      <feGaussianBlur in="off" stdDeviation="18" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <clipPath id="avatarClip">
      <circle cx="640" cy="310" r="112"/>
    </clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgPurple)"/>
  <rect x="0" y="0" width="1280" height="720" fill="url(#vignette)"/>

  <!-- Wide overlapping theatrical beams -->
  <path d="M185 92 L305 92 L605 622 L338 622 Z" fill="url(#beamWhite)" opacity="0.42" filter="url(#softGlow)"/>
  <path d="M397 92 L507 92 L685 622 L468 622 Z" fill="url(#beamGold)" opacity="0.36" filter="url(#softGlow)"/>
  <path d="M773 92 L883 92 L812 622 L595 622 Z" fill="url(#beamGold)" opacity="0.36" filter="url(#softGlow)"/>
  <path d="M975 92 L1095 92 L942 622 L675 622 Z" fill="url(#beamWhite)" opacity="0.42" filter="url(#softGlow)"/>

  <!-- Narrow bright cores increase the additive overlap at center -->
  <path d="M224 110 L260 110 L572 610 L505 610 Z" fill="#ffffff" opacity="0.13"/>
  <path d="M435 110 L470 110 L650 610 L588 610 Z" fill="#ffffff" opacity="0.16"/>
  <path d="M810 110 L845 110 L692 610 L630 610 Z" fill="#ffffff" opacity="0.16"/>
  <path d="M1020 110 L1056 110 L775 610 L708 610 Z" fill="#ffffff" opacity="0.13"/>

  <!-- Stage light pool -->
  <ellipse cx="640" cy="625" rx="390" ry="72" fill="url(#stageGlow)" opacity="0.95" filter="url(#softGlow)"/>
  <ellipse cx="640" cy="628" rx="250" ry="42" fill="#ffffff" opacity="0.42"/>

  <!-- Overhead truss -->
  <rect x="0" y="0" width="1280" height="64" fill="#050407"/>
  <line x1="70" y1="16" x2="1210" y2="16" stroke="#15121a" stroke-width="10"/>
  <line x1="70" y1="48" x2="1210" y2="48" stroke="#15121a" stroke-width="10"/>
  <line x1="120" y1="16" x2="190" y2="48" stroke="#25202b" stroke-width="5"/>
  <line x1="360" y1="48" x2="430" y2="16" stroke="#25202b" stroke-width="5"/>
  <line x1="850" y1="16" x2="920" y2="48" stroke="#25202b" stroke-width="5"/>
  <line x1="1090" y1="48" x2="1160" y2="16" stroke="#25202b" stroke-width="5"/>

  <!-- Stage fixtures -->
  <g transform="translate(245 70) rotate(18)">
    <rect x="-38" y="-18" width="76" height="36" rx="8" fill="#09080b"/>
    <circle cx="-44" cy="0" r="13" fill="#020203"/>
    <ellipse cx="45" cy="0" rx="22" ry="15" fill="#111018"/>
    <ellipse cx="49" cy="0" rx="13" ry="9" fill="#fff2bc" opacity="0.72"/>
  </g>
  <g transform="translate(455 70) rotate(9)">
    <rect x="-38" y="-18" width="76" height="36" rx="8" fill="#09080b"/>
    <circle cx="-44" cy="0" r="13" fill="#020203"/>
    <ellipse cx="45" cy="0" rx="22" ry="15" fill="#111018"/>
    <ellipse cx="49" cy="0" rx="13" ry="9" fill="#fff2bc" opacity="0.72"/>
  </g>
  <g transform="translate(825 70) rotate(-9)">
    <rect x="-38" y="-18" width="76" height="36" rx="8" fill="#09080b"/>
    <circle cx="44" cy="0" r="13" fill="#020203"/>
    <ellipse cx="-45" cy="0" rx="22" ry="15" fill="#111018"/>
    <ellipse cx="-49" cy="0" rx="13" ry="9" fill="#fff2bc" opacity="0.72"/>
  </g>
  <g transform="translate(1035 70) rotate(-18)">
    <rect x="-38" y="-18" width="76" height="36" rx="8" fill="#09080b"/>
    <circle cx="44" cy="0" r="13" fill="#020203"/>
    <ellipse cx="-45" cy="0" rx="22" ry="15" fill="#111018"/>
    <ellipse cx="-49" cy="0" rx="13" ry="9" fill="#fff2bc" opacity="0.72"/>
  </g>

  <!-- Spotlighted content -->
  <circle cx="640" cy="310" r="132" fill="#ffffff" opacity="0.18" filter="url(#softGlow)"/>
  <image href="https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=900&amp;q=80"
         x="528" y="198" width="224" height="224" preserveAspectRatio="xMidYMid slice"
         clip-path="url(#avatarClip)" filter="url(#portraitShadow)"/>
  <circle cx="640" cy="310" r="116" fill="none" stroke="#ffffff" stroke-width="9"/>
  <circle cx="640" cy="310" r="126" fill="none" stroke="#fff2bc" stroke-width="2" opacity="0.75"/>

  <text x="640" y="470" width="760" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="30" font-weight="700"
        letter-spacing="6" fill="#fff2bc">EMPLOYEE SPOTLIGHT</text>

  <text x="640" y="524" width="760" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="58" font-weight="800"
        fill="#ffffff">Jane Doe</text>

  <text x="640" y="562" width="760" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="24" font-weight="500"
        fill="#e9d9ff">Lead Designer · Experience Systems</text>

  <text x="640" y="652" width="520" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="16" font-weight="700"
        letter-spacing="3" fill="#5b2d75" opacity="0.78">CENTER STAGE RECOGNITION</text>

  <text x="1160" y="690" width="180" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13"
        fill="#cdb7df" opacity="0.5">Q4 ALL-HANDS</text>
</svg>
```

## Avoid in this skill
- ❌ Using `<mask>` for spotlight falloff; use semi-transparent paths, gradients, and glow filters instead.
- ❌ Applying `filter` to truss `<line>` elements; line filters may be dropped, so keep truss lines crisp.
- ❌ Clipping the light beams or stage ellipses; clip paths should only be used on the portrait/product `<image>`.
- ❌ Flat, opaque white beam polygons; the effect depends on translucent overlap and additive brightness.
- ❌ Too many competing bright objects outside the beam convergence area, which weakens the theatrical focus.

## Composition notes
- Keep the top 10–15% reserved for black truss and physical light fixtures; this makes the beams feel sourced, not decorative.
- Put the hero image or product exactly where beams overlap, slightly above vertical center, with the strongest text below it.
- Use a dark jewel-tone background and mostly white/gold light so the slide reads as dramatic rather than corporate-dashboard.
- The stage ellipse should occupy the lower 15–20% of the slide and act as a visual anchor for names, roles, or reveal copy.