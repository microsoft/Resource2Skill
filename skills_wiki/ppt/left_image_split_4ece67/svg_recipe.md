# SVG Recipe — Left Image Split

## Visual mechanism
A large editorial photo anchors the left half of the slide while the right half carries structured narrative copy, creating a clean “show + explain” executive layout. Premium polish comes from a rounded clipped image card, soft shadow, restrained gradients, and small accent geometry that ties the two halves together.

## SVG primitives needed
- 3× `<rect>` for full-slide background, image shadow card, and right-side content surface
- 1× `<image>` for the left hero photo, clipped to a rounded rectangle
- 1× `<clipPath>` with rounded `<rect>` for the photo crop
- 4× `<linearGradient>` for background wash, image overlay, accent ribbon, and pill fill
- 2× `<filter>` for card shadow and soft accent glow
- 5× `<path>` for decorative editorial arcs, split accent ribbon, and subtle background shapes
- 5× `<circle>` for bullet icons and small highlight dots
- 1× `<line>` for a vertical divider/accent rule
- 8× `<text>` blocks with explicit `width` attributes for headline, eyebrow, body copy, metric labels, and bullets
- Nested `<tspan>` for multi-line and inline-styled text

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgWash" x1="0" y1="0" x2="1280" y2="720" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#F6F8FB"/>
      <stop offset="0.55" stop-color="#FFFFFF"/>
      <stop offset="1" stop-color="#EEF3F8"/>
    </linearGradient>

    <linearGradient id="imageOverlay" x1="70" y1="150" x2="615" y2="580" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#071E34" stop-opacity="0.40"/>
      <stop offset="0.55" stop-color="#071E34" stop-opacity="0.08"/>
      <stop offset="1" stop-color="#071E34" stop-opacity="0"/>
    </linearGradient>

    <linearGradient id="accentGrad" x1="560" y1="140" x2="710" y2="580" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#2FD6C5"/>
      <stop offset="0.52" stop-color="#2B7BFF"/>
      <stop offset="1" stop-color="#6B5BFF"/>
    </linearGradient>

    <linearGradient id="pillGrad" x1="700" y1="155" x2="890" y2="155" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#E8F7F5"/>
      <stop offset="1" stop-color="#EEF3FF"/>
    </linearGradient>

    <filter id="cardShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="18"/>
      <feGaussianBlur stdDeviation="18"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="softGlow" x="-80%" y="-80%" width="260%" height="260%">
      <feGaussianBlur stdDeviation="18"/>
    </filter>

    <clipPath id="photoClip">
      <rect x="70" y="150" width="545" height="430" rx="28" ry="28"/>
    </clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgWash)"/>

  <path d="M-40,610 C160,520 270,660 430,560 C550,485 610,530 700,470"
        fill="none" stroke="#DDE7F2" stroke-width="34" stroke-linecap="round" opacity="0.55"/>
  <path d="M1030,-60 C1135,30 1235,48 1320,24 L1320,210 C1210,190 1100,145 1014,78 Z"
        fill="#EAF1FA" opacity="0.75"/>
  <circle cx="1166" cy="116" r="46" fill="#DDEBFF" opacity="0.55" filter="url(#softGlow)"/>

  <text x="70" y="80" width="820"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="38" font-weight="700" fill="#102033">
    From operational insight to strategic action
  </text>
  <text x="72" y="112" width="610"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="15" font-weight="500" fill="#6D7D90" letter-spacing="0.8">
    LEFT IMAGE SPLIT · EDITORIAL EXECUTIVE LAYOUT
  </text>

  <rect x="70" y="150" width="545" height="430" rx="28" ry="28"
        fill="#FFFFFF" filter="url(#cardShadow)" opacity="0.95"/>
  <image x="70" y="150" width="545" height="430"
         href="https://images.example.com/hero-photo-modern-team-reviewing-strategy-wall.jpg"
         preserveAspectRatio="xMidYMid slice"
         clip-path="url(#photoClip)"/>
  <rect x="70" y="150" width="545" height="430" rx="28" ry="28"
        fill="url(#imageOverlay)" opacity="0.95"/>

  <path d="M575,150 C628,224 627,506 575,580 L628,580 C676,500 676,232 628,150 Z"
        fill="url(#accentGrad)" opacity="0.96"/>
  <path d="M606,198 C636,278 636,452 606,532"
        fill="none" stroke="#FFFFFF" stroke-width="2" stroke-linecap="round" opacity="0.38"/>

  <rect x="96" y="505" width="258" height="52" rx="16" ry="16"
        fill="#071E34" opacity="0.78"/>
  <text x="116" y="529" width="220"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="13" font-weight="600" fill="#FFFFFF" letter-spacing="0.5">
    MARKET SIGNAL
  </text>
  <text x="116" y="550" width="230"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="15" font-weight="400" fill="#D9F7FF">
    Teams align faster when context is visible.
  </text>

  <rect x="690" y="146" width="505" height="454" rx="30" ry="30"
        fill="#FFFFFF" opacity="0.82"/>
  <rect x="710" y="165" width="178" height="34" rx="17" ry="17"
        fill="url(#pillGrad)"/>
  <circle cx="732" cy="182" r="5" fill="#2FD6C5"/>
  <text x="748" y="187" width="130"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="12" font-weight="700" fill="#2B5877" letter-spacing="0.7">
    EXECUTIVE BRIEF
  </text>

  <text x="710" y="250" width="430"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="30" font-weight="700" fill="#102033">
    A split composition for balancing evidence and explanation
  </text>

  <line x1="710" y1="288" x2="710" y2="442"
        stroke="#2B7BFF" stroke-width="3" stroke-linecap="round"/>

  <text x="735" y="314" width="410"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="18" font-weight="400" fill="#435266">
    Use the left panel for the proof point: a customer moment, product detail,
    field image, or operational scene. Keep the right panel concise, with one
    clear argument and two to three supporting takeaways.
  </text>

  <circle cx="724" cy="480" r="8" fill="#2FD6C5"/>
  <text x="744" y="486" width="390"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="17" font-weight="600" fill="#17293C">
    Lead with the image; let the copy interpret its business meaning.
  </text>

  <circle cx="724" cy="522" r="8" fill="#2B7BFF"/>
  <text x="744" y="528" width="390"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="17" font-weight="600" fill="#17293C">
    Reserve the top band for a strong headline, not extra navigation.
  </text>

  <circle cx="724" cy="564" r="8" fill="#6B5BFF"/>
  <text x="744" y="570" width="390"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="17" font-weight="600" fill="#17293C">
    Add a slim accent bridge to visually connect both halves.
  </text>

  <path d="M1050,624 C1090,606 1138,612 1174,636"
        fill="none" stroke="#B9C9DD" stroke-width="2" stroke-dasharray="6 8" opacity="0.8"/>
  <text x="1012" y="652" width="178"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="12" font-weight="600" fill="#7B8A9D" text-anchor="end">
    Recommended for medium-density narrative slides
  </text>
</svg>
```

## Avoid in this skill
- ❌ Do not use a plain left rectangle and right text block with no visual bridge; the split will feel generic and under-designed.
- ❌ Do not apply `clip-path` to groups or overlay shapes; only clip the `<image>` and use matching rounded rectangles for overlays.
- ❌ Avoid placing body text over the photo unless the image has a strong dark overlay and the text is short.
- ❌ Do not make both halves equally busy; one side should be visual evidence, the other side structured interpretation.
- ❌ Avoid extremely wide body lines on the right; keep text width around 380–460 px for readable executive copy.

## Composition notes
- Keep the hero photo at roughly 42–45% of slide width, starting below the title band, with generous margins on the left and bottom.
- Use the right half for a hierarchy: small eyebrow, bold explanatory heading, short paragraph, then 2–3 emphasized bullets.
- Add a narrow gradient ribbon or curved accent between the image and text to soften the split and make the layout feel intentional.
- Preserve negative space in the upper-right and lower-right corners so the slide reads as editorial, not like a dense report page.