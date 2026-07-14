# SVG Recipe — Minimalist High-Key Profile with Geometric Accent

## Visual mechanism
A pure white, high-key profile layout pairs a large studio-style portrait on the right with sharp left-aligned typography on the left. A small faceted geometric mark provides the only strong color, acting as a premium brand anchor without disturbing the minimalist field.

## SVG primitives needed
- 1× `<rect>` for the full-slide high-key background
- 1× `<radialGradient>` for a barely visible studio-cove glow behind the portrait
- 1× `<ellipse>` for a soft floor shadow under the portrait
- 1× `<filter id="softBlur">` applied to the portrait floor shadow
- 1× `<clipPath>` with rounded `<rect>` for cropping the portrait image cleanly
- 1× `<image>` for the high-key business portrait
- 8× `<path>` for the faceted geometric “L” accent mark
- 2× `<line>` for minimal brand-rule typography accents
- 3× `<text>` blocks for name, role/company, and small descriptor label
- 1× `<linearGradient>` for a subtle blue highlight sliver in the geometric accent

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <radialGradient id="coveGlow" cx="72%" cy="47%" r="48%">
      <stop offset="0%" stop-color="#F7F9FF"/>
      <stop offset="58%" stop-color="#FFFFFF"/>
      <stop offset="100%" stop-color="#FFFFFF"/>
    </radialGradient>

    <linearGradient id="blueFacet" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#54A0FF"/>
      <stop offset="100%" stop-color="#1D65D8"/>
    </linearGradient>

    <filter id="softBlur" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="18"/>
    </filter>

    <clipPath id="portraitClip">
      <rect x="742" y="70" width="420" height="590" rx="18" ry="18"/>
    </clipPath>
  </defs>

  <!-- high-key white studio field -->
  <rect x="0" y="0" width="1280" height="720" fill="#FFFFFF"/>
  <rect x="0" y="0" width="1280" height="720" fill="url(#coveGlow)"/>

  <!-- almost invisible studio floor shadow -->
  <ellipse cx="950" cy="638" rx="235" ry="34" fill="#D8DDE8" opacity="0.34" filter="url(#softBlur)"/>

  <!-- portrait crop: use a high-key photo with white or light gray background -->
  <image
    href="https://images.unsplash.com/photo-1500648767791-00dcc994a43e?auto=format&amp;fit=crop&amp;w=900&amp;q=90"
    x="716" y="52" width="500" height="640"
    preserveAspectRatio="xMidYMid slice"
    clip-path="url(#portraitClip)"/>

  <!-- right-edge white fade panel to keep the portrait airy and integrated -->
  <rect x="1118" y="0" width="162" height="720" fill="#FFFFFF" opacity="0.82"/>

  <!-- geometric faceted accent mark -->
  <g transform="translate(96 86)">
    <path d="M0 0 L50 0 L0 76 Z" fill="#BAC4EE"/>
    <path d="M50 0 L50 76 L0 76 Z" fill="url(#blueFacet)"/>
    <path d="M0 76 L50 76 L0 152 Z" fill="#2C82F0"/>
    <path d="M50 76 L50 152 L0 152 Z" fill="#123466"/>
    <path d="M50 108 L108 108 L50 152 Z" fill="#2C82F0"/>
    <path d="M108 108 L108 152 L50 152 Z" fill="#BAC4EE"/>
    <path d="M108 108 L160 130 L108 152 Z" fill="#2C82F0"/>
    <path d="M160 130 L178 152 L108 152 Z" fill="#123466" opacity="0.94"/>
  </g>

  <!-- small typographic eyebrow -->
  <line x1="98" y1="276" x2="158" y2="276" stroke="#2C82F0" stroke-width="3"/>
  <text x="174" y="282" width="330"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="14" font-weight="700" letter-spacing="2.4"
        fill="#7A7A7A">
    EXECUTIVE PROFILE
  </text>

  <!-- main name -->
  <text x="96" y="374" width="540"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="58" font-weight="800"
        fill="#1E1E1E">
    Marcus Brotz
  </text>

  <!-- role and company -->
  <text x="100" y="426" width="470"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="24" font-weight="400"
        fill="#787878">
    <tspan x="100" dy="0">Director of Business Development</tspan>
    <tspan x="100" dy="34">Legion Enterprises</tspan>
  </text>

  <!-- restrained supporting statement -->
  <line x1="100" y1="514" x2="238" y2="514" stroke="#E2E6F0" stroke-width="2"/>
  <text x="100" y="558" width="500"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="18" font-weight="400"
        fill="#9A9A9A">
    Building strategic partnerships across emerging markets with a focus on clarity, trust, and measurable growth.
  </text>
</svg>
```

## Avoid in this skill
- ❌ Busy backgrounds, texture fields, or decorative grids; the design depends on open white space.
- ❌ Heavy photo frames or dark containers around the portrait; use cropping and subtle shadow only.
- ❌ Applying `clip-path` to non-image shapes; keep clipping only on the portrait `<image>`.
- ❌ Overbuilding the geometric accent into a large illustration; it should remain a small brand anchor.
- ❌ Centered typography; this layout works best with a strict left-aligned reading axis.

## Composition notes
- Keep the left 45% reserved for the logo, name, role, and short descriptor; avoid filling all vertical space.
- Let the portrait occupy the right 40–45%, ideally cropped tall with generous white margins.
- Use color sparingly: charcoal and gray for text, with blue/violet/navy reserved for the geometric mark.
- Maintain a wide central gutter so the portrait and typography feel balanced rather than crowded.