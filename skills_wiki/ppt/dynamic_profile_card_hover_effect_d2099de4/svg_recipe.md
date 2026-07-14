# SVG Recipe — Dynamic Profile Card Hover Effect

## Visual mechanism
A clean team-card grid becomes engaging by showing one “hovered” profile in an expanded state: a rotated color panel blooms behind the white card, the photo lifts visually, and extra role/contact details appear. In PowerPoint, reproduce the motion by exporting separate SVG states as slides and applying Morph between them, keeping persistent objects in matching positions/IDs.

## SVG primitives needed
- 1× full-slide `<rect>` for the warm off-white presentation background.
- 2× decorative `<path>` blobs for soft editorial depth in the corners.
- 3× rotated rounded `<rect>` accent panels behind profile cards; inactive cards use low opacity, active card uses saturated color.
- 3× rounded white `<rect>` foreground cards with a soft shadow filter.
- 3× `<clipPath>` definitions with `<circle>` shapes for circular avatar crops.
- 3× `<image>` elements clipped to avatar circles.
- 3× `<circle>` avatar rings to create a premium framed portrait effect.
- 10× `<text>` elements for title, names, roles, and revealed micro-details; every text element includes explicit `width`.
- 1× `<filter id="cardShadow">` using `feOffset`, `feGaussianBlur`, and `feMerge` for card depth.
- 1× `<filter id="softGlow">` using `feGaussianBlur` for the active accent halo.
- 3× `<linearGradient>` fills for the colored hover panels.

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="greenPanel" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#B8EC6A"/>
      <stop offset="100%" stop-color="#77C843"/>
    </linearGradient>
    <linearGradient id="bluePanel" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#72A7EA"/>
      <stop offset="100%" stop-color="#3F72B8"/>
    </linearGradient>
    <linearGradient id="tealPanel" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#26D9C2"/>
      <stop offset="100%" stop-color="#009E8C"/>
    </linearGradient>

    <filter id="cardShadow" x="-30%" y="-30%" width="160%" height="170%">
      <feOffset dx="0" dy="18" result="off"/>
      <feGaussianBlur in="off" stdDeviation="18" result="blur"/>
      <feColorMatrix in="blur" type="matrix"
        values="0 0 0 0 0.05  0 0 0 0 0.07  0 0 0 0 0.10  0 0 0 0.22 0" result="shadow"/>
      <feMerge>
        <feMergeNode in="shadow"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="softGlow" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="14"/>
    </filter>

    <clipPath id="avatarMarcus">
      <circle cx="250" cy="280" r="68"/>
    </clipPath>
    <clipPath id="avatarDavid">
      <circle cx="640" cy="250" r="76"/>
    </clipPath>
    <clipPath id="avatarJason">
      <circle cx="1030" cy="280" r="68"/>
    </clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#F7F4EE"/>

  <path d="M-70,122 C70,10 207,28 263,139 C322,254 188,343 50,311 C-76,282 -172,209 -70,122 Z"
        fill="#EAF7D7" opacity="0.62"/>
  <path d="M1108,526 C1234,432 1356,501 1340,638 C1328,751 1167,789 1059,705 C964,631 1005,603 1108,526 Z"
        fill="#DDF5F0" opacity="0.72"/>

  <text x="0" y="76" width="1280" text-anchor="middle"
        font-family="Segoe Script, Segoe UI, Microsoft YaHei" font-size="48" font-weight="700" fill="#242424">
    Meet Our Team
  </text>
  <text x="360" y="116" width="560" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#707070">
    A progressive profile reveal layout for speaker introductions and leadership slides
  </text>

  <!-- Inactive profile card: Marcus -->
  <rect x="132" y="198" width="236" height="304" rx="34" fill="url(#greenPanel)"
        opacity="0.34" transform="rotate(-10 250 350)"/>
  <rect x="145" y="205" width="210" height="292" rx="30" fill="#FFFFFF" filter="url(#cardShadow)"/>
  <image href="https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?q=80&amp;w=400&amp;h=400&amp;fit=crop"
         x="182" y="212" width="136" height="136" preserveAspectRatio="xMidYMid slice"
         clip-path="url(#avatarMarcus)"/>
  <circle cx="250" cy="280" r="70" fill="none" stroke="#FFFFFF" stroke-width="7"/>
  <circle cx="250" cy="280" r="72" fill="none" stroke="#A3DA5C" stroke-width="3" opacity="0.75"/>
  <text x="165" y="396" width="170" text-anchor="middle"
        font-family="Segoe Script, Segoe UI, Microsoft YaHei" font-size="29" font-weight="700" fill="#262626">
    Marcus Lee
  </text>
  <text x="165" y="428" width="170" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#777777">
    Visual Storyteller
  </text>

  <!-- Active / hovered profile card: David -->
  <rect x="501" y="148" width="278" height="374" rx="42" fill="url(#bluePanel)"
        opacity="0.34" filter="url(#softGlow)" transform="rotate(-13 640 335)"/>
  <rect x="501" y="148" width="278" height="374" rx="42" fill="url(#bluePanel)"
        transform="rotate(-13 640 335)"/>
  <rect x="515" y="162" width="250" height="350" rx="34" fill="#FFFFFF" filter="url(#cardShadow)"/>
  <image href="https://images.unsplash.com/photo-1583864697784-a0efc8379f70?q=80&amp;w=400&amp;h=400&amp;fit=crop"
         x="564" y="174" width="152" height="152" preserveAspectRatio="xMidYMid slice"
         clip-path="url(#avatarDavid)"/>
  <circle cx="640" cy="250" r="79" fill="none" stroke="#FFFFFF" stroke-width="8"/>
  <circle cx="640" cy="250" r="82" fill="none" stroke="#4F81BD" stroke-width="4"/>
  <text x="535" y="373" width="210" text-anchor="middle"
        font-family="Segoe Script, Segoe UI, Microsoft YaHei" font-size="34" font-weight="700" fill="#202020">
    David Ryan
  </text>
  <text x="545" y="408" width="190" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#4F81BD">
    Creative Director
  </text>
  <text x="547" y="439" width="186" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#606060">
    Photographer · Videographer · Journalist
  </text>
  <line x1="575" y1="461" x2="705" y2="461" stroke="#D8DFEA" stroke-width="2"/>
  <text x="550" y="490" width="180" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#858585">
    Leads brand films, keynote visuals, and executive profile shoots
  </text>

  <!-- Inactive profile card: Jason -->
  <rect x="912" y="198" width="236" height="304" rx="34" fill="url(#tealPanel)"
        opacity="0.34" transform="rotate(10 1030 350)"/>
  <rect x="925" y="205" width="210" height="292" rx="30" fill="#FFFFFF" filter="url(#cardShadow)"/>
  <image href="https://images.unsplash.com/photo-1542327897-4141b355e20e?q=80&amp;w=400&amp;h=400&amp;fit=crop"
         x="962" y="212" width="136" height="136" preserveAspectRatio="xMidYMid slice"
         clip-path="url(#avatarJason)"/>
  <circle cx="1030" cy="280" r="70" fill="none" stroke="#FFFFFF" stroke-width="7"/>
  <circle cx="1030" cy="280" r="72" fill="none" stroke="#00B096" stroke-width="3" opacity="0.75"/>
  <text x="945" y="396" width="170" text-anchor="middle"
        font-family="Segoe Script, Segoe UI, Microsoft YaHei" font-size="29" font-weight="700" fill="#262626">
    Jason Cole
  </text>
  <text x="945" y="428" width="170" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#777777">
    Field Producer
  </text>
</svg>
```

## Avoid in this skill
- ❌ Do not use SVG `<animate>` or `<animateTransform>` for the hover; create separate slide states and use PowerPoint Morph.
- ❌ Do not clip the whole card group; only apply `clip-path` to the `<image>` avatar.
- ❌ Do not use `<mask>` for circular photos; use `<clipPath>` with a `<circle>`.
- ❌ Do not use `<use>` or `<symbol>` to duplicate cards; repeat the editable shapes directly so PowerPoint keeps them independent.
- ❌ Do not apply filters to `<line>` separators; shadows/glows should be on rectangles, paths, circles, ellipses, or text only.

## Composition notes
- Keep the title and subtitle in the top 15–18% of the slide; the card row should occupy the middle band with generous side margins.
- The hovered card should be 10–18% larger or taller than inactive cards, with the rotated color panel visible beyond the white card edges.
- For Morph, build one slide per hover state: same card/photo/name objects remain, while detail text and saturated accent panels appear on the active profile.
- Use a restrained palette: white cards, dark typography, and one vivid accent color per person so the reveal feels intentional rather than noisy.