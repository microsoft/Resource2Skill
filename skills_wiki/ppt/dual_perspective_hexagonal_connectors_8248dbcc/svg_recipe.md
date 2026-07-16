# SVG Recipe — Dual-Perspective Hexagonal Connectors

## Visual mechanism
A mirrored comparison infographic uses two elongated, hollow hexagonal “arms” that converge toward the center, each ending in a bold filled hexagonal cap. Contrasting color palettes, face icons, and checklist symbols turn a plain pros/cons list into a balanced executive-style visual.

## SVG primitives needed
- 1× `<rect>` for the soft slide background
- 2× `<path>` for the hollow elongated hexagonal connector outlines
- 2× `<path>` for the solid central hexagonal caps
- 1× `<path>` for the small center diamond connector
- 7× `<circle>` for icon faces, eyes, and list-item bullets
- 8× `<path>` for smile/sad mouths, checkmarks, and cross marks
- 1× `<line>` for the subtle vertical center axis
- Multiple `<text>` elements with explicit `width` for title, labels, and list items
- 2× `<linearGradient>` for rich cap fills
- 1× `<radialGradient>` for the center hub glow
- 1× `<filter id="softShadow">` applied to the filled caps and center diamond
- 1× `<filter id="textGlow">` applied to the center “VS” label

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgWash" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#F8FAFC"/>
      <stop offset="58%" stop-color="#FFFFFF"/>
      <stop offset="100%" stop-color="#F2F5F8"/>
    </linearGradient>

    <linearGradient id="greenCap" x1="465" y1="235" x2="635" y2="385" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#42CF62"/>
      <stop offset="100%" stop-color="#1D9B35"/>
    </linearGradient>

    <linearGradient id="redCap" x1="645" y1="235" x2="815" y2="385" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#E24848"/>
      <stop offset="100%" stop-color="#B40000"/>
    </linearGradient>

    <radialGradient id="hubGlow" cx="50%" cy="50%" r="60%">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="70%" stop-color="#EEF2F7"/>
      <stop offset="100%" stop-color="#D9E1EA"/>
    </radialGradient>

    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="12"/>
      <feGaussianBlur stdDeviation="10"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="textGlow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="2"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgWash)"/>

  <text x="90" y="86" width="1100" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="800" fill="#1F2937" letter-spacing="0.5">
    Strategic Decision Snapshot
  </text>
  <text x="92" y="120" width="820" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#667085">
    Two opposing perspectives are framed as connected hexagonal branches, making trade-offs easy to scan.
  </text>

  <line x1="640" y1="185" x2="640" y2="500" stroke="#D8DEE8" stroke-width="2" stroke-dasharray="7 10"/>

  <path d="M 535 245 L 185 245 L 120 310 L 185 375 L 535 375"
        fill="none" stroke="#9BD5A2" stroke-width="8" stroke-linejoin="round" stroke-linecap="round"/>
  <path d="M 745 245 L 1095 245 L 1160 310 L 1095 375 L 745 375"
        fill="none" stroke="#D96A6B" stroke-width="8" stroke-linejoin="round" stroke-linecap="round"/>

  <path d="M 510 235 L 590 235 L 635 310 L 590 385 L 510 385 L 465 310 Z"
        fill="url(#greenCap)" filter="url(#softShadow)"/>
  <path d="M 770 235 L 690 235 L 645 310 L 690 385 L 770 385 L 815 310 Z"
        fill="url(#redCap)" filter="url(#softShadow)"/>

  <path d="M 640 260 L 690 310 L 640 360 L 590 310 Z"
        fill="url(#hubGlow)" stroke="#CBD5E1" stroke-width="2" filter="url(#softShadow)"/>
  <text x="610" y="321" width="60" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="900" fill="#475467" filter="url(#textGlow)">
    VS
  </text>

  <circle cx="550" cy="286" r="28" fill="none" stroke="#FFFFFF" stroke-width="5"/>
  <circle cx="540" cy="279" r="4" fill="#FFFFFF"/>
  <circle cx="560" cy="279" r="4" fill="#FFFFFF"/>
  <path d="M 535 298 Q 550 312 565 298" fill="none" stroke="#FFFFFF" stroke-width="5" stroke-linecap="round"/>

  <circle cx="730" cy="286" r="28" fill="none" stroke="#FFFFFF" stroke-width="5"/>
  <circle cx="720" cy="279" r="4" fill="#FFFFFF"/>
  <circle cx="740" cy="279" r="4" fill="#FFFFFF"/>
  <path d="M 715 305 Q 730 291 745 305" fill="none" stroke="#FFFFFF" stroke-width="5" stroke-linecap="round"/>

  <text x="492" y="346" width="116" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="900" fill="#FFFFFF" letter-spacing="1.2">
    POSITIVES
  </text>
  <text x="672" y="346" width="116" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="900" fill="#FFFFFF" letter-spacing="1.2">
    NEGATIVES
  </text>

  <text x="155" y="214" width="300" font-family="Segoe UI, Microsoft YaHei" font-size="22" font-weight="900" fill="#2EAC3C" letter-spacing="1.4">
    ADVANTAGES
  </text>
  <text x="825" y="214" width="300" text-anchor="start" font-family="Segoe UI, Microsoft YaHei" font-size="22" font-weight="900" fill="#C00000" letter-spacing="1.4">
    RISKS
  </text>

  <circle cx="168" cy="282" r="13" fill="#2EAC3C"/>
  <path d="M 161 282 L 166 287 L 176 276" fill="none" stroke="#FFFFFF" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
  <text x="195" y="288" width="285" font-family="Segoe UI, Microsoft YaHei" font-size="18" fill="#595959">
    Faster adoption across customer teams
  </text>

  <circle cx="168" cy="322" r="13" fill="#2EAC3C"/>
  <path d="M 161 322 L 166 327 L 176 316" fill="none" stroke="#FFFFFF" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
  <text x="195" y="328" width="290" font-family="Segoe UI, Microsoft YaHei" font-size="18" fill="#595959">
    Higher perceived value and loyalty
  </text>

  <circle cx="168" cy="362" r="13" fill="#2EAC3C"/>
  <path d="M 161 362 L 166 367 L 176 356" fill="none" stroke="#FFFFFF" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
  <text x="195" y="368" width="295" font-family="Segoe UI, Microsoft YaHei" font-size="18" fill="#595959">
    Clearer story for executive buyers
  </text>

  <circle cx="1112" cy="282" r="13" fill="#C00000"/>
  <path d="M 1106 276 L 1118 288 M 1118 276 L 1106 288" fill="none" stroke="#FFFFFF" stroke-width="4" stroke-linecap="round"/>
  <text x="810" y="288" width="275" font-family="Segoe UI, Microsoft YaHei" font-size="18" fill="#595959">
    Requires stronger launch discipline
  </text>

  <circle cx="1112" cy="322" r="13" fill="#C00000"/>
  <path d="M 1106 316 L 1118 328 M 1118 316 L 1106 328" fill="none" stroke="#FFFFFF" stroke-width="4" stroke-linecap="round"/>
  <text x="810" y="328" width="275" font-family="Segoe UI, Microsoft YaHei" font-size="18" fill="#595959">
    Short-term cost pressure increases
  </text>

  <circle cx="1112" cy="362" r="13" fill="#C00000"/>
  <path d="M 1106 356 L 1118 368 M 1118 356 L 1106 368" fill="none" stroke="#FFFFFF" stroke-width="4" stroke-linecap="round"/>
  <text x="810" y="368" width="275" font-family="Segoe UI, Microsoft YaHei" font-size="18" fill="#595959">
    More dependencies across partners
  </text>

  <text x="450" y="505" width="380" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#667085">
    Use color, symmetry, and mirrored geometry to make comparison instantly readable.
  </text>
</svg>
```

## Avoid in this skill
- ❌ Do not use `<polygon>` if your translator workflow favors editable custom paths; use explicit `<path d="...">` for each hexagonal connector.
- ❌ Do not put `marker-end` on connector paths; if arrows are needed, draw them manually with short `<line>` or `<path>` segments.
- ❌ Do not apply filters to `<line>` elements; shadows should be applied only to the filled hex cap paths or center diamond.
- ❌ Do not use masks or clipping on non-image objects to cut the hollow connector; create the hollow look with stroked open paths instead.
- ❌ Do not rely on Unicode emoji faces for the cap icons; draw simple editable circles and paths for consistent PowerPoint rendering.

## Composition notes
- Keep the filled hexagonal caps near the center so the two perspectives feel connected, while the long hollow outlines carry the list content outward.
- Reserve generous white space above and below the infographic; the connector should occupy the middle 45–55% of the slide height.
- Use matched saturation but different hues: green for positives, red for negatives, with lighter outline tints to create hierarchy.
- Place list text inside the hollow arms, aligned away from the center, so the audience reads each side as an independent argument stream.