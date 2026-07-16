# SVG Recipe — Dynamic Subject-Harmonized Portrait Presentation

## Visual mechanism
A transparent cutout portrait is placed over a background whose base and accent colors are harmonized to the subject’s clothing, making the person and slide feel like one branded composition. Large diagonal color planes create editorial motion, while crisp right-side typography and small data details provide executive profile structure.

## SVG primitives needed
- 1× `<rect>` for the full-slide harmonized background
- 4× `<path>` for oversized diagonal accent panels and editorial color slices
- 1× `<ellipse>` for a soft grounding shadow beneath the portrait
- 1× `<image>` for the transparent-background cutout portrait
- 5× `<line>` for fine editorial dividers and micro-layout guides
- 9× `<circle>` for decorative bullets, metric dots, and small hierarchy anchors
- 6× `<rect>` for translucent metric/data cards and small value bars
- 8× `<text>` elements with explicit `width` for name, role, quote, data labels, and profile details
- 1× `<linearGradient>` for a subtle background sheen
- 1× `<linearGradient>` for diagonal accent depth
- 1× `<filter id="softShadow">` applied to ellipse/path/rect elements for depth

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgSheen" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#F0C2CE"/>
      <stop offset="55%" stop-color="#E2A9B8"/>
      <stop offset="100%" stop-color="#D494A6"/>
    </linearGradient>
    <linearGradient id="accentDepth" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#D48FA1"/>
      <stop offset="60%" stop-color="#CD8999"/>
      <stop offset="100%" stop-color="#B96F82"/>
    </linearGradient>
    <filter id="softShadow" x="-30%" y="-30%" width="160%" height="160%">
      <feOffset dx="0" dy="18"/>
      <feGaussianBlur stdDeviation="18"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgSheen)"/>

  <path d="M420 -90 L650 -90 L415 810 L185 810 Z" fill="#D18A9B" opacity="0.52"/>
  <path d="M655 -80 L850 -80 L615 800 L420 800 Z" fill="url(#accentDepth)" opacity="0.82" filter="url(#softShadow)"/>
  <path d="M920 -120 L1055 -120 L820 780 L685 780 Z" fill="#C87B8E" opacity="0.38"/>
  <path d="M1085 -80 L1170 -80 L945 800 L860 800 Z" fill="#F7D3DC" opacity="0.32"/>

  <ellipse cx="322" cy="668" rx="210" ry="34" fill="#8B4254" opacity="0.26" filter="url(#softShadow)"/>

  <image
    href="https://images.example.com/cutout-portrait-woman-mauve-blazer-transparent-background.png"
    x="42" y="72" width="515" height="648"
    preserveAspectRatio="xMidYMax meet"/>

  <line x1="720" y1="128" x2="1135" y2="128" stroke="#FFFFFF" stroke-width="2" opacity="0.72"/>
  <circle cx="700" cy="128" r="5" fill="#FFFFFF"/>
  <text x="720" y="106" width="430" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="600" letter-spacing="5" fill="#FFFFFF">
    EXECUTIVE PROFILE
  </text>

  <text x="690" y="210" width="500" font-family="Segoe UI, Microsoft YaHei" font-size="68" font-weight="800" fill="#323232">
    Jenny Davis
  </text>
  <text x="694" y="258" width="460" font-family="Segoe UI, Microsoft YaHei" font-size="22" font-weight="700" letter-spacing="4" fill="#FFFFFF">
    CREATIVE DIRECTOR
  </text>

  <path d="M690 292 L1118 292" stroke="#323232" stroke-width="2" opacity="0.35"/>
  <text x="694" y="332" width="440" font-family="Segoe UI, Microsoft YaHei" font-size="21" fill="#323232">
    Harmonizes brand systems, campaign storytelling, and visual strategy for high-growth consumer teams.
  </text>

  <rect x="690" y="390" width="150" height="104" rx="24" fill="#FFFFFF" opacity="0.22" filter="url(#softShadow)"/>
  <rect x="865" y="390" width="150" height="104" rx="24" fill="#FFFFFF" opacity="0.22" filter="url(#softShadow)"/>
  <rect x="1040" y="390" width="150" height="104" rx="24" fill="#FFFFFF" opacity="0.22" filter="url(#softShadow)"/>

  <text x="714" y="430" width="105" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="800" fill="#323232">
    38%
  </text>
  <text x="714" y="465" width="110" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="600" letter-spacing="1.5" fill="#FFFFFF">
    BRAND LIFT
  </text>

  <text x="889" y="430" width="105" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="800" fill="#323232">
    24
  </text>
  <text x="889" y="465" width="110" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="600" letter-spacing="1.5" fill="#FFFFFF">
    MARKETS
  </text>

  <text x="1064" y="430" width="105" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="800" fill="#323232">
    12Y
  </text>
  <text x="1064" y="465" width="110" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="600" letter-spacing="1.5" fill="#FFFFFF">
    EXPERIENCE
  </text>

  <line x1="695" y1="545" x2="1136" y2="545" stroke="#FFFFFF" stroke-width="1.5" opacity="0.55"/>
  <circle cx="704" cy="585" r="5" fill="#323232"/>
  <text x="724" y="592" width="360" font-family="Segoe UI, Microsoft YaHei" font-size="17" fill="#323232">
    Leads integrated creative teams across product, retail, and digital launches.
  </text>

  <circle cx="704" cy="632" r="5" fill="#323232"/>
  <text x="724" y="639" width="360" font-family="Segoe UI, Microsoft YaHei" font-size="17" fill="#323232">
    Known for warm minimalism, narrative systems, and premium visual language.
  </text>

  <line x1="1110" y1="570" x2="1168" y2="570" stroke="#323232" stroke-width="5" opacity="0.25"/>
  <line x1="1110" y1="594" x2="1190" y2="594" stroke="#FFFFFF" stroke-width="5" opacity="0.55"/>
  <line x1="1110" y1="618" x2="1152" y2="618" stroke="#323232" stroke-width="5" opacity="0.25"/>

  <circle cx="1168" cy="570" r="7" fill="#323232" opacity="0.55"/>
  <circle cx="1190" cy="594" r="7" fill="#FFFFFF" opacity="0.9"/>
  <circle cx="1152" cy="618" r="7" fill="#323232" opacity="0.55"/>

  <rect x="52" y="618" width="185" height="42" rx="21" fill="#FFFFFF" opacity="0.25"/>
  <circle cx="80" cy="639" r="6" fill="#FFFFFF"/>
  <text x="98" y="645" width="125" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" letter-spacing="1.2" fill="#FFFFFF">
    COLOR-MATCHED
  </text>
</svg>
```

## Avoid in this skill
- ❌ Using a rectangular portrait photo with its original background; the technique depends on a transparent cutout subject overlapping the geometry.
- ❌ Applying `clip-path` or `mask` to text/paths to fake cutouts; keep clipping only for images if needed.
- ❌ Flat, unrelated background colors; the base and accent palette should be sampled from the subject’s clothing or brand styling.
- ❌ Centered, symmetrical ID-card layouts; the premium editorial effect comes from asymmetry and diagonal tension.
- ❌ Overloading the right side with dense paragraphs; use short profile copy plus a few high-contrast data points.

## Composition notes
- Keep the subject on the left 40–45% of the slide, anchored to the bottom edge, with the body overlapping at least one diagonal accent plane.
- Reserve the right 50% for hierarchy: small label, large name, role line, concise description, then metric/detail rows.
- Use the extracted clothing color as the base background, then make diagonal panels darker or more saturated variants of the same hue.
- Maintain generous negative space around the face and name; the diagonals should create motion, not compete with the portrait or typography.