# SVG Recipe — Isometric 3D Target Infographic

## Visual mechanism
Create each “3D target” as a shallow cylinder: a dark front half-wall plus stacked concentric ellipses on top, viewed from an isometric angle. Add a slanted composite arrow piercing the bullseye, with soft ground shadows and aligned text/icon blocks above each target.

## SVG primitives needed
- 1× `<rect>` for the clean slide background.
- 1× large subtle `<path>` for a pale decorative background sweep.
- 3× target groups, each using:
  - 1× blurred `<ellipse>` for the ground shadow.
  - 1× `<path>` for the visible cylindrical side wall.
  - 5× concentric `<ellipse>` shapes for alternating target rings.
  - 1× translucent highlight `<ellipse>` for the glossy top surface.
- 3× arrow groups, each using:
  - 1× blurred `<ellipse>` for the arrow cast shadow.
  - 1× `<path>` for the metallic shaft.
  - 1× `<path>` for the arrowhead.
  - 2× `<path>` shapes for colored fletching feathers.
- 3× simple monochrome icon groups made from `<path>`, `<circle>`, and `<line>`.
- 6× `<text>` blocks with explicit `width` attributes for titles and body copy.
- 2× `<linearGradient>` definitions for metallic shafts and background tint.
- 1× `<radialGradient>` for subtle top-surface highlights.
- 1× `<filter id="softShadow">` applied directly to ellipses/paths for editable soft shadows.

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgWash" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#F7FAFF"/>
      <stop offset="1" stop-color="#EEF3FB"/>
    </linearGradient>
    <linearGradient id="steel" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#B7C0CC"/>
      <stop offset="0.45" stop-color="#F7FAFC"/>
      <stop offset="0.72" stop-color="#8E9AAA"/>
      <stop offset="1" stop-color="#D8DEE6"/>
    </linearGradient>
    <radialGradient id="topGlow" cx="38%" cy="24%" r="70%">
      <stop offset="0" stop-color="#FFFFFF" stop-opacity="0.55"/>
      <stop offset="0.55" stop-color="#FFFFFF" stop-opacity="0.16"/>
      <stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/>
    </radialGradient>
    <filter id="softShadow" x="-40%" y="-60%" width="180%" height="240%">
      <feOffset dx="0" dy="10"/>
      <feGaussianBlur stdDeviation="14"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#FFFFFF"/>
  <path d="M0,570 C210,492 350,610 520,548 C760,462 873,318 1280,392 L1280,720 L0,720 Z" fill="url(#bgWash)"/>

  <g transform="translate(222 96)" fill="none" stroke="#2F5597" stroke-width="5" stroke-linecap="round">
    <circle cx="0" cy="0" r="23"/>
    <line x1="-34" y1="0" x2="-18" y2="0"/>
    <line x1="18" y1="0" x2="34" y2="0"/>
    <line x1="0" y1="-34" x2="0" y2="-18"/>
    <line x1="0" y1="18" x2="0" y2="34"/>
  </g>
  <text x="107" y="157" width="230" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="25" font-weight="700" fill="#2F5597">TARGET 01</text>
  <text x="107" y="192" width="230" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#6B7280">
    <tspan x="222">Expand into priority</tspan><tspan x="222" dy="20">segments with sharper</tspan><tspan x="222" dy="20">commercial focus.</tspan>
  </text>

  <g transform="translate(640 96)" fill="none" stroke="#FF0000" stroke-width="5" stroke-linecap="round" stroke-linejoin="round">
    <path d="M-25,25 L-8,-20 L8,8 L25,-25"/>
    <circle cx="-25" cy="25" r="5" fill="#FF0000" stroke="none"/>
    <circle cx="25" cy="-25" r="5" fill="#FF0000" stroke="none"/>
  </g>
  <text x="525" y="157" width="230" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="25" font-weight="700" fill="#FF0000">TARGET 02</text>
  <text x="525" y="192" width="230" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#6B7280">
    <tspan x="640">Accelerate revenue</tspan><tspan x="640" dy="20">conversion through</tspan><tspan x="640" dy="20">precision execution.</tspan>
  </text>

  <g transform="translate(1058 96)" fill="none" stroke="#00B050" stroke-width="5" stroke-linecap="round" stroke-linejoin="round">
    <path d="M-28,18 C-8,-18 14,-20 30,-32"/>
    <path d="M-28,18 C-9,14 6,18 20,30"/>
    <circle cx="-28" cy="18" r="5" fill="#00B050" stroke="none"/>
  </g>
  <text x="943" y="157" width="230" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="25" font-weight="700" fill="#00B050">TARGET 03</text>
  <text x="943" y="192" width="230" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#6B7280">
    <tspan x="1058">Lock in measurable</tspan><tspan x="1058" dy="20">milestones and scale</tspan><tspan x="1058" dy="20">what works fastest.</tspan>
  </text>

  <g transform="translate(222 440)">
    <ellipse cx="8" cy="65" rx="140" ry="32" fill="#000000" opacity="0.16" filter="url(#softShadow)"/>
    <path d="M-120,0 A120,48 0 0 0 120,0 L120,34 A120,48 0 0 1 -120,34 Z" fill="#1E3D73"/>
    <ellipse cx="0" cy="0" rx="120" ry="48" fill="#2F5597" stroke="#17365D" stroke-width="2"/>
    <ellipse cx="0" cy="0" rx="92" ry="36" fill="#FFFFFF"/>
    <ellipse cx="0" cy="0" rx="66" ry="26" fill="#2F5597"/>
    <ellipse cx="0" cy="0" rx="38" ry="15" fill="#FFFFFF"/>
    <ellipse cx="0" cy="0" rx="15" ry="6" fill="#2F5597"/>
    <ellipse cx="-28" cy="-14" rx="70" ry="20" fill="url(#topGlow)"/>
    <ellipse cx="88" cy="-55" rx="95" ry="12" fill="#000000" opacity="0.13" transform="rotate(-27)" filter="url(#softShadow)"/>
    <g transform="translate(7 -6) rotate(-28)">
      <path d="M0,-5 L158,-5 L158,5 L0,5 Z" fill="url(#steel)" stroke="#778391" stroke-width="1"/>
      <path d="M-27,0 L4,-16 L4,16 Z" fill="#AEB7C2" stroke="#6D7785" stroke-width="1"/>
      <path d="M152,-6 L186,-28 L176,-2 Z" fill="#2F5597"/>
      <path d="M152,6 L186,28 L176,2 Z" fill="#25477F"/>
    </g>
  </g>

  <g transform="translate(640 440)">
    <ellipse cx="8" cy="65" rx="140" ry="32" fill="#000000" opacity="0.16" filter="url(#softShadow)"/>
    <path d="M-120,0 A120,48 0 0 0 120,0 L120,34 A120,48 0 0 1 -120,34 Z" fill="#B50000"/>
    <ellipse cx="0" cy="0" rx="120" ry="48" fill="#FF0000" stroke="#9D0000" stroke-width="2"/>
    <ellipse cx="0" cy="0" rx="92" ry="36" fill="#FFFFFF"/>
    <ellipse cx="0" cy="0" rx="66" ry="26" fill="#FF0000"/>
    <ellipse cx="0" cy="0" rx="38" ry="15" fill="#FFFFFF"/>
    <ellipse cx="0" cy="0" rx="15" ry="6" fill="#FF0000"/>
    <ellipse cx="-28" cy="-14" rx="70" ry="20" fill="url(#topGlow)"/>
    <ellipse cx="88" cy="-55" rx="95" ry="12" fill="#000000" opacity="0.13" transform="rotate(-27)" filter="url(#softShadow)"/>
    <g transform="translate(7 -6) rotate(-28)">
      <path d="M0,-5 L158,-5 L158,5 L0,5 Z" fill="url(#steel)" stroke="#778391" stroke-width="1"/>
      <path d="M-27,0 L4,-16 L4,16 Z" fill="#AEB7C2" stroke="#6D7785" stroke-width="1"/>
      <path d="M152,-6 L186,-28 L176,-2 Z" fill="#FF0000"/>
      <path d="M152,6 L186,28 L176,2 Z" fill="#BE0000"/>
    </g>
  </g>

  <g transform="translate(1058 440)">
    <ellipse cx="8" cy="65" rx="140" ry="32" fill="#000000" opacity="0.16" filter="url(#softShadow)"/>
    <path d="M-120,0 A120,48 0 0 0 120,0 L120,34 A120,48 0 0 1 -120,34 Z" fill="#00813B"/>
    <ellipse cx="0" cy="0" rx="120" ry="48" fill="#00B050" stroke="#007A38" stroke-width="2"/>
    <ellipse cx="0" cy="0" rx="92" ry="36" fill="#FFFFFF"/>
    <ellipse cx="0" cy="0" rx="66" ry="26" fill="#00B050"/>
    <ellipse cx="0" cy="0" rx="38" ry="15" fill="#FFFFFF"/>
    <ellipse cx="0" cy="0" rx="15" ry="6" fill="#00B050"/>
    <ellipse cx="-28" cy="-14" rx="70" ry="20" fill="url(#topGlow)"/>
    <ellipse cx="88" cy="-55" rx="95" ry="12" fill="#000000" opacity="0.13" transform="rotate(-27)" filter="url(#softShadow)"/>
    <g transform="translate(7 -6) rotate(-28)">
      <path d="M0,-5 L158,-5 L158,5 L0,5 Z" fill="url(#steel)" stroke="#778391" stroke-width="1"/>
      <path d="M-27,0 L4,-16 L4,16 Z" fill="#AEB7C2" stroke="#6D7785" stroke-width="1"/>
      <path d="M152,-6 L186,-28 L176,-2 Z" fill="#00B050"/>
      <path d="M152,6 L186,28 L176,2 Z" fill="#007A38"/>
    </g>
  </g>
</svg>
```

## Avoid in this skill
- ❌ Do not rely on PowerPoint-only 3D extrusion settings; approximate the target with editable SVG ellipses and side-wall paths instead.
- ❌ Do not use `<mask>` or clip paths on non-image elements to create rings; simple stacked ellipses translate more reliably.
- ❌ Do not use `marker-end` on arrow paths; build arrows from editable shaft, head, and fletching shapes.
- ❌ Do not apply filters to `<line>` elements; use filtered ellipses or paths for shadows.
- ❌ Do not use skew or matrix transforms for isometric perspective; use flattened ellipses and simple `rotate(...)` transforms.

## Composition notes
- Keep targets in the lower half of the slide, evenly spaced across three columns; the top half is reserved for icons, titles, and concise explanatory copy.
- The target top should feel compressed vertically: use wide ellipses, not circles, to create the isometric tabletop view.
- Match each title, icon, bullseye color, and arrow fletching color for strong column association.
- Use soft gray shadows beneath both the targets and arrows so the infographic feels physical without becoming heavy.