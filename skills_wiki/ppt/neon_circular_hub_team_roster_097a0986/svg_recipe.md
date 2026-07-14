# SVG Recipe — Neon Circular Hub Team Roster

## Visual mechanism
A dark “solar system” team roster places glowing central typography at the hub while circular headshots orbit along neon tracking rings. The slide feels interactive because each avatar is positioned as a future Morph target that can expand into a detailed profile view.

## SVG primitives needed
- 1× `<rect>` for the black-to-green radial background wash
- 2× `<path>` for oversized ambient neon blobs / energy arcs in the corners
- 10× `<line>` for faint dashed hub-and-spoke connectors and micro grid accents
- 6× `<circle>` for orbital guide rings, central glow, and radar-style neon rings
- 8× `<clipPath>` with `<circle>` for circular avatar crops
- 8× `<image>` clipped into circular headshots
- 8× `<circle>` for editable neon avatar halos behind the clipped images
- 1× `<text>` with nested `<tspan>` for the stacked central title
- 10× `<text>` elements for subtitle, member names, and small interface labels
- 2× `<linearGradient>` / `<radialGradient>` for background depth and avatar halo highlights
- 2× `<filter>` using `feGaussianBlur` / `feOffset` for neon glow and soft shadows applied only to editable shapes/text

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <radialGradient id="bgPulse" cx="50%" cy="50%" r="70%">
      <stop offset="0%" stop-color="#06351f"/>
      <stop offset="36%" stop-color="#020906"/>
      <stop offset="100%" stop-color="#000000"/>
    </radialGradient>

    <linearGradient id="neonStroke" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#00ff7f"/>
      <stop offset="55%" stop-color="#0affd6"/>
      <stop offset="100%" stop-color="#00ff7f"/>
    </linearGradient>

    <radialGradient id="centerGlow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#00ff7f" stop-opacity="0.42"/>
      <stop offset="68%" stop-color="#00ff7f" stop-opacity="0.08"/>
      <stop offset="100%" stop-color="#00ff7f" stop-opacity="0"/>
    </radialGradient>

    <filter id="glow">
      <feGaussianBlur stdDeviation="7" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="softShadow">
      <feOffset dx="0" dy="10" result="off"/>
      <feGaussianBlur in="off" stdDeviation="14" result="shadow"/>
      <feMerge>
        <feMergeNode in="shadow"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <clipPath id="avatarA" clipPathUnits="userSpaceOnUse"><circle cx="640" cy="92" r="52"/></clipPath>
    <clipPath id="avatarB" clipPathUnits="userSpaceOnUse"><circle cx="832" cy="168" r="52"/></clipPath>
    <clipPath id="avatarC" clipPathUnits="userSpaceOnUse"><circle cx="910" cy="360" r="52"/></clipPath>
    <clipPath id="avatarD" clipPathUnits="userSpaceOnUse"><circle cx="832" cy="552" r="52"/></clipPath>
    <clipPath id="avatarE" clipPathUnits="userSpaceOnUse"><circle cx="640" cy="628" r="52"/></clipPath>
    <clipPath id="avatarF" clipPathUnits="userSpaceOnUse"><circle cx="448" cy="552" r="52"/></clipPath>
    <clipPath id="avatarG" clipPathUnits="userSpaceOnUse"><circle cx="370" cy="360" r="52"/></clipPath>
    <clipPath id="avatarH" clipPathUnits="userSpaceOnUse"><circle cx="448" cy="168" r="52"/></clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgPulse)"/>

  <path d="M1030 -60 C1190 20 1245 155 1308 300 C1182 238 1056 237 960 285 C1002 170 960 48 1030 -60 Z"
        fill="#00ff7f" opacity="0.08" filter="url(#glow)"/>
  <path d="M-70 590 C80 500 185 520 300 646 C170 640 72 694 -20 780 C-50 702 -92 646 -70 590 Z"
        fill="#00ffd0" opacity="0.06" filter="url(#glow)"/>

  <line x1="160" y1="120" x2="1120" y2="120" stroke="#00ff7f" stroke-opacity="0.12" stroke-width="1" stroke-dasharray="2 14"/>
  <line x1="160" y1="600" x2="1120" y2="600" stroke="#00ff7f" stroke-opacity="0.12" stroke-width="1" stroke-dasharray="2 14"/>

  <circle cx="640" cy="360" r="286" fill="none" stroke="#00ff7f" stroke-opacity="0.28" stroke-width="2" stroke-dasharray="7 14"/>
  <circle cx="640" cy="360" r="238" fill="none" stroke="#0affd6" stroke-opacity="0.13" stroke-width="1"/>
  <circle cx="640" cy="360" r="166" fill="none" stroke="#00ff7f" stroke-opacity="0.16" stroke-width="1" stroke-dasharray="2 10"/>
  <circle cx="640" cy="360" r="144" fill="url(#centerGlow)" filter="url(#glow)"/>

  <line x1="640" y1="360" x2="640" y2="92" stroke="#00ff7f" stroke-opacity="0.18" stroke-width="1"/>
  <line x1="640" y1="360" x2="832" y2="168" stroke="#00ff7f" stroke-opacity="0.18" stroke-width="1"/>
  <line x1="640" y1="360" x2="910" y2="360" stroke="#00ff7f" stroke-opacity="0.18" stroke-width="1"/>
  <line x1="640" y1="360" x2="832" y2="552" stroke="#00ff7f" stroke-opacity="0.18" stroke-width="1"/>
  <line x1="640" y1="360" x2="640" y2="628" stroke="#00ff7f" stroke-opacity="0.18" stroke-width="1"/>
  <line x1="640" y1="360" x2="448" y2="552" stroke="#00ff7f" stroke-opacity="0.18" stroke-width="1"/>
  <line x1="640" y1="360" x2="370" y2="360" stroke="#00ff7f" stroke-opacity="0.18" stroke-width="1"/>
  <line x1="640" y1="360" x2="448" y2="168" stroke="#00ff7f" stroke-opacity="0.18" stroke-width="1"/>

  <circle cx="640" cy="92" r="61" fill="none" stroke="url(#neonStroke)" stroke-width="3" filter="url(#glow)"/>
  <image href="https://images.example.com/team/founder-portrait-confident-woman.jpg" x="588" y="40" width="104" height="104" clip-path="url(#avatarA)"/>

  <circle cx="832" cy="168" r="61" fill="none" stroke="url(#neonStroke)" stroke-width="3" filter="url(#glow)"/>
  <image href="https://images.example.com/team/product-lead-portrait-studio.jpg" x="780" y="116" width="104" height="104" clip-path="url(#avatarB)"/>

  <circle cx="910" cy="360" r="61" fill="none" stroke="url(#neonStroke)" stroke-width="3" filter="url(#glow)"/>
  <image href="https://images.example.com/team/design-director-portrait-neon.jpg" x="858" y="308" width="104" height="104" clip-path="url(#avatarC)"/>

  <circle cx="832" cy="552" r="61" fill="none" stroke="url(#neonStroke)" stroke-width="3" filter="url(#glow)"/>
  <image href="https://images.example.com/team/growth-strategist-portrait.jpg" x="780" y="500" width="104" height="104" clip-path="url(#avatarD)"/>

  <circle cx="640" cy="628" r="61" fill="none" stroke="url(#neonStroke)" stroke-width="3" filter="url(#glow)"/>
  <image href="https://images.example.com/team/engineering-lead-portrait.jpg" x="588" y="576" width="104" height="104" clip-path="url(#avatarE)"/>

  <circle cx="448" cy="552" r="61" fill="none" stroke="url(#neonStroke)" stroke-width="3" filter="url(#glow)"/>
  <image href="https://images.example.com/team/research-lead-portrait.jpg" x="396" y="500" width="104" height="104" clip-path="url(#avatarF)"/>

  <circle cx="370" cy="360" r="61" fill="none" stroke="url(#neonStroke)" stroke-width="3" filter="url(#glow)"/>
  <image href="https://images.example.com/team/operations-lead-portrait.jpg" x="318" y="308" width="104" height="104" clip-path="url(#avatarG)"/>

  <circle cx="448" cy="168" r="61" fill="none" stroke="url(#neonStroke)" stroke-width="3" filter="url(#glow)"/>
  <image href="https://images.example.com/team/brand-lead-portrait.jpg" x="396" y="116" width="104" height="104" clip-path="url(#avatarH)"/>

  <text x="640" y="310" width="390" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="78" font-weight="900" letter-spacing="-3" fill="#00ff7f" filter="url(#glow)">
    <tspan x="640" dy="0">OUR</tspan>
    <tspan x="640" dy="78">TEAM</tspan>
  </text>
  <text x="640" y="444" width="360" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="600" letter-spacing="4" fill="#eafff4" opacity="0.86">
    PRODUCT STUDIO • 2026
  </text>

  <text x="640" y="172" width="150" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#ffffff">Maya Chen</text>
  <text x="870" y="160" width="150" text-anchor="start" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#ffffff">Noah Patel</text>
  <text x="986" y="366" width="150" text-anchor="start" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#ffffff">Ava Rivera</text>
  <text x="870" y="570" width="150" text-anchor="start" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#ffffff">Leo Morgan</text>
  <text x="640" y="705" width="150" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#ffffff">Iris Kim</text>
  <text x="410" y="570" width="150" text-anchor="end" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#ffffff">Owen Stone</text>
  <text x="294" y="366" width="150" text-anchor="end" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#ffffff">Zara Ali</text>
  <text x="410" y="160" width="150" text-anchor="end" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#ffffff">Kai Brooks</text>

  <text x="64" y="64" width="230" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" letter-spacing="3" fill="#00ff7f" opacity="0.86">LIVE ROSTER HUB</text>
  <text x="1030" y="664" width="190" text-anchor="end" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="600" letter-spacing="2" fill="#8affc2" opacity="0.65">CLICK AVATAR → MORPH</text>
</svg>
```

## Avoid in this skill
- ❌ Do not use `<mask>` to make circular portraits; use `<clipPath>` on each `<image>` instead.
- ❌ Do not put `clip-path` on circles or groups; only apply it directly to the avatar `<image>`.
- ❌ Do not use `marker-end` for spoke arrows; this design works better with clean radial `<line>` connectors.
- ❌ Do not apply filters to `<line>` elements; use glowing circles, paths, or text for the neon effect.
- ❌ Do not build the roster as a rectangular grid; the identity of this skill is the radial hub orbit.

## Composition notes
- Keep the central title in the middle 20–25% of the slide; it should feel like a glowing navigation core, not a normal heading.
- Place avatars on one invisible circle with equal radius from center so every person gets equal visual weight.
- Use bright neon green sparingly: rings, title, and small UI labels. Let portraits and white names provide contrast.
- For a Morph detail slide, duplicate the SVG layout, enlarge one avatar to the right side, add 2–3 large concentric rings behind it, and move that person’s name/role/bio into a left-side text block.