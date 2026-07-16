# SVG Recipe — Dynamic Masonry Team Morph

## Visual mechanism
A split-screen “meet the team” layout pairs restrained editorial typography on the left with a floating masonry portrait collage on the right. The dynamic effect comes from making a second slide with the same portrait objects and IDs, but swapped sizes/positions, so PowerPoint Morph animates the hierarchy shift from one featured person to another.

## SVG primitives needed
- 1× `<rect>` for the white slide background
- 1× oversized outlined `<text>` for the low-contrast “OUR TEAM” background typography
- 4× foreground `<text>` blocks for eyebrow, headline, description, and selected member metadata
- 2× decorative `<path>` blobs behind the masonry cluster for depth and motion energy
- 6× shadow `<rect>` cards behind portraits, each with rounded corners and a soft filter
- 6× `<clipPath>` definitions using rounded `<rect>` shapes for editable rounded image crops
- 6× `<image>` portraits clipped into masonry cards
- 6× small label `<rect>` overlays for member initials / role tags
- 6× small `<text>` overlays for initials or short labels
- 1× `<linearGradient>` for subtle text/label accents
- 1× `<radialGradient>` for ambient color glow behind the image cluster
- 1× `<filter id="cardShadow">` applied to portrait backing rectangles
- 1× `<filter id="softGlow">` applied to decorative blobs

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="inkGrad" x1="80" y1="0" x2="480" y2="0" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#111827"/>
      <stop offset="1" stop-color="#3B3F51"/>
    </linearGradient>

    <radialGradient id="clusterGlow" cx="50%" cy="50%" r="65%">
      <stop offset="0" stop-color="#F5B7D2" stop-opacity="0.38"/>
      <stop offset="0.55" stop-color="#B8D7FF" stop-opacity="0.18"/>
      <stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/>
    </radialGradient>

    <filter id="cardShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="18"/>
      <feGaussianBlur stdDeviation="18"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="softGlow" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="24"/>
    </filter>

    <clipPath id="clip-member-sophia"><rect x="610" y="134" width="350" height="438" rx="34"/></clipPath>
    <clipPath id="clip-member-eva"><rect x="980" y="82" width="176" height="198" rx="24"/></clipPath>
    <clipPath id="clip-member-ethan"><rect x="984" y="314" width="212" height="220" rx="26"/></clipPath>
    <clipPath id="clip-member-jackson"><rect x="1188" y="188" width="132" height="178" rx="22"/></clipPath>
    <clipPath id="clip-member-caleb"><rect x="502" y="72" width="132" height="132" rx="24"/></clipPath>
    <clipPath id="clip-member-emily"><rect x="518" y="574" width="198" height="116" rx="26"/></clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#FFFFFF"/>

  <text x="54" y="246" width="520" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="104" font-weight="800" letter-spacing="-4"
        fill="none" stroke="#E2E4EA" stroke-width="2.2">OUR</text>
  <text x="54" y="350" width="560" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="104" font-weight="800" letter-spacing="-4"
        fill="none" stroke="#E2E4EA" stroke-width="2.2">TEAM</text>

  <text x="88" y="118" width="360" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="15" font-weight="700" letter-spacing="4" fill="#E4568A">MEET THE MAKERS</text>

  <text x="86" y="214" width="410" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="62" letter-spacing="-2" fill="url(#inkGrad)">
    <tspan font-weight="300">Sophia</tspan>
    <tspan x="86" dy="68" font-weight="800">White</tspan>
  </text>

  <text x="90" y="356" width="370" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="20" line-height="1.35" fill="#5E6472">
    <tspan x="90">Brand strategist shaping the visual</tspan>
    <tspan x="90" dy="30">language behind our most memorable</tspan>
    <tspan x="90" dy="30">campaign launches.</tspan>
  </text>

  <rect x="88" y="482" width="220" height="44" rx="22" fill="#111827"/>
  <text x="112" y="511" width="180" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="15" font-weight="700" fill="#FFFFFF">ACTIVE PROFILE</text>

  <text x="90" y="586" width="320" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="15" fill="#8A91A2">
    <tspan font-weight="700" fill="#111827">Morph cue:</tspan>
    <tspan> duplicate this slide, keep the same image IDs, then swap portrait slots.</tspan>
  </text>

  <ellipse cx="850" cy="354" rx="390" ry="286" fill="url(#clusterGlow)"/>
  <path d="M780,70 C908,22 1056,72 1084,178 C1114,292 988,338 876,306 C746,268 668,112 780,70 Z"
        fill="#FCE6F0" opacity="0.6" filter="url(#softGlow)"/>
  <path d="M645,536 C754,492 880,566 862,646 C846,720 680,716 594,670 C524,632 552,574 645,536 Z"
        fill="#DCF2E8" opacity="0.65" filter="url(#softGlow)"/>

  <rect id="card-shadow-sophia" x="610" y="134" width="350" height="438" rx="34" fill="#FFFFFF" filter="url(#cardShadow)"/>
  <image id="member-sophia" x="610" y="134" width="350" height="438"
         href="https://images.example.com/team/sophia-white-teal-studio-portrait.jpg"
         clip-path="url(#clip-member-sophia)" preserveAspectRatio="xMidYMid slice"/>
  <rect x="638" y="498" width="220" height="48" rx="24" fill="#FFFFFF" opacity="0.92"/>
  <text x="662" y="529" width="180" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="16" font-weight="800" fill="#111827">SW · Brand Strategy</text>

  <rect id="card-shadow-eva" x="980" y="82" width="176" height="198" rx="24" fill="#FFFFFF" filter="url(#cardShadow)"/>
  <image id="member-eva" x="980" y="82" width="176" height="198"
         href="https://images.example.com/team/eva-rodriguez-pink-portrait.jpg"
         clip-path="url(#clip-member-eva)" preserveAspectRatio="xMidYMid slice"/>
  <rect x="998" y="232" width="70" height="32" rx="16" fill="#EB578E"/>
  <text x="1016" y="254" width="44" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="14" font-weight="800" fill="#FFFFFF">ER</text>

  <rect id="card-shadow-ethan" x="984" y="314" width="212" height="220" rx="26" fill="#FFFFFF" filter="url(#cardShadow)"/>
  <image id="member-ethan" x="984" y="314" width="212" height="220"
         href="https://images.example.com/team/ethan-turner-yellow-portrait.jpg"
         clip-path="url(#clip-member-ethan)" preserveAspectRatio="xMidYMid slice"/>
  <rect x="1006" y="486" width="70" height="32" rx="16" fill="#FDCB58"/>
  <text x="1024" y="508" width="44" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="14" font-weight="800" fill="#111827">ET</text>

  <rect id="card-shadow-jackson" x="1188" y="188" width="132" height="178" rx="22" fill="#FFFFFF" filter="url(#cardShadow)"/>
  <image id="member-jackson" x="1188" y="188" width="132" height="178"
         href="https://images.example.com/team/jackson-smith-purple-portrait.jpg"
         clip-path="url(#clip-member-jackson)" preserveAspectRatio="xMidYMid slice"/>
  <rect x="1202" y="324" width="58" height="30" rx="15" fill="#9266CC"/>
  <text x="1218" y="345" width="34" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="13" font-weight="800" fill="#FFFFFF">JS</text>

  <rect id="card-shadow-caleb" x="502" y="72" width="132" height="132" rx="24" fill="#FFFFFF" filter="url(#cardShadow)"/>
  <image id="member-caleb" x="502" y="72" width="132" height="132"
         href="https://images.example.com/team/caleb-davis-orange-portrait.jpg"
         clip-path="url(#clip-member-caleb)" preserveAspectRatio="xMidYMid slice"/>
  <rect x="518" y="158" width="58" height="30" rx="15" fill="#FF8C00"/>
  <text x="534" y="179" width="34" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="13" font-weight="800" fill="#FFFFFF">CD</text>

  <rect id="card-shadow-emily" x="518" y="574" width="198" height="116" rx="26" fill="#FFFFFF" filter="url(#cardShadow)"/>
  <image id="member-emily" x="518" y="574" width="198" height="116"
         href="https://images.example.com/team/emily-lewis-green-wide-portrait.jpg"
         clip-path="url(#clip-member-emily)" preserveAspectRatio="xMidYMid slice"/>
  <rect x="538" y="640" width="60" height="30" rx="15" fill="#43B581"/>
  <text x="554" y="661" width="36" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="13" font-weight="800" fill="#FFFFFF">EL</text>
</svg>
```

## Avoid in this skill
- ❌ Do not use `<animate>` or `<animateTransform>` for the motion; create two separate slides and let PowerPoint Morph interpolate object positions.
- ❌ Do not change portrait IDs between morph states; the same member image should keep the same `id` on every slide.
- ❌ Do not use `<mask>` for rounded portraits; use `<clipPath>` applied directly to each `<image>`.
- ❌ Do not apply `clip-path` to grouped cards or backing rectangles; only clipped images are reliable.
- ❌ Do not build the collage as one flattened screenshot; individual image objects must remain editable and morphable.
- ❌ Do not use `<use>` or `<symbol>` to repeat card structures; duplicate the native shapes explicitly.

## Composition notes
- Keep the left 38–42% of the slide quiet and typographic; the masonry cluster should own the right side.
- Make the hero portrait roughly 3× the area of secondary portraits so the morph has a clear focus target.
- Use consistent rounded corners and soft card shadows to make the collage feel like floating physical tiles.
- For the second morph state, move another member into the large hero slot and shrink the previous hero into one of the smaller slots while preserving IDs and image sources.