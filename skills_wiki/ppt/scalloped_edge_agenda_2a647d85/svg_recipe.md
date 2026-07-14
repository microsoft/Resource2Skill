# SVG Recipe — Scalloped Edge Agenda

## Visual mechanism
A split agenda slide becomes distinctive by replacing the hard image/content boundary with white circular “scallops” that overlap the photo edge. The circles visually cut into the image while also holding the agenda numbers, tying the list structure directly to the visual anchor.

## SVG primitives needed
- 1× `<image>` for the large left-side hero photo
- 1× `<clipPath>` with `<rect rx>` applied to the image for a premium cropped photo card edge
- 2× `<rect>` for the white slide background and right content panel
- 1× `<rect>` with gradient fill over the photo for readability and mood
- 5× `<circle>` for the scalloped cutouts along the vertical seam
- 5× `<text>` for centered agenda numbers inside the scallops
- 5× `<text>` for agenda item titles
- 5× `<text>` for smaller agenda descriptions
- 1× `<text>` for the main title
- 1× `<text>` for the small eyebrow label
- 1× `<linearGradient>` for the photo overlay
- 1× `<filter id="softShadow">` applied to the scallop circles and content accents
- 1× `<filter id="panelShadow">` applied to the right panel edge for subtle depth

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="photoWash" x1="0" y1="126" x2="588" y2="720" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#172033" stop-opacity="0.12"/>
      <stop offset="0.55" stop-color="#172033" stop-opacity="0.25"/>
      <stop offset="1" stop-color="#172033" stop-opacity="0.58"/>
    </linearGradient>

    <linearGradient id="titleAccent" x1="52" y1="104" x2="230" y2="104" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#FFB000"/>
      <stop offset="1" stop-color="#FF5C35"/>
    </linearGradient>

    <filter id="softShadow" x="-25%" y="-25%" width="150%" height="150%">
      <feOffset dx="0" dy="8"/>
      <feGaussianBlur stdDeviation="10"/>
      <feColorMatrix type="matrix" values="0 0 0 0 0.04  0 0 0 0 0.05  0 0 0 0 0.08  0 0 0 0.20 0"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="panelShadow" x="-15%" y="-5%" width="130%" height="110%">
      <feOffset dx="-10" dy="0"/>
      <feGaussianBlur stdDeviation="14"/>
      <feColorMatrix type="matrix" values="0 0 0 0 0.03  0 0 0 0 0.04  0 0 0 0 0.07  0 0 0 0.16 0"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <clipPath id="photoClip">
      <rect x="0" y="126" width="600" height="594" rx="0" ry="0"/>
    </clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#FFFFFF"/>

  <image
    x="0" y="126" width="600" height="594"
    href="https://images.example.com/hero-photo-modern-business-workshop-with-people-and-glass-walls.jpg"
    preserveAspectRatio="xMidYMid slice"
    clip-path="url(#photoClip)"/>

  <rect x="0" y="126" width="600" height="594" fill="url(#photoWash)"/>

  <rect x="588" y="0" width="692" height="720" fill="#FFFFFF" filter="url(#panelShadow)"/>

  <text x="52" y="50" width="220" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" font-weight="700" letter-spacing="2.2" fill="#FF6A2A">
    STRATEGIC SESSION
  </text>
  <text x="52" y="92" width="650" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="38" font-weight="800" fill="#101828">
    Agenda Slide Design
  </text>
  <rect x="52" y="108" width="178" height="5" rx="2.5" fill="url(#titleAccent)"/>

  <text x="54" y="646" width="360" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" font-weight="600" fill="#FFFFFF">
    Transformation workshop
  </text>
  <text x="54" y="674" width="430" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="12" fill="#DDE5F2">
    Aligning leadership, operating model, and execution rhythm
  </text>

  <circle cx="588" cy="186" r="46" fill="#FFFFFF" filter="url(#softShadow)"/>
  <circle cx="588" cy="296" r="46" fill="#FFFFFF" filter="url(#softShadow)"/>
  <circle cx="588" cy="406" r="46" fill="#FFFFFF" filter="url(#softShadow)"/>
  <circle cx="588" cy="516" r="46" fill="#FFFFFF" filter="url(#softShadow)"/>
  <circle cx="588" cy="626" r="46" fill="#FFFFFF" filter="url(#softShadow)"/>

  <circle cx="588" cy="186" r="31" fill="#F7F8FA"/>
  <circle cx="588" cy="296" r="31" fill="#F7F8FA"/>
  <circle cx="588" cy="406" r="31" fill="#F7F8FA"/>
  <circle cx="588" cy="516" r="31" fill="#F7F8FA"/>
  <circle cx="588" cy="626" r="31" fill="#F7F8FA"/>

  <text x="563" y="198" width="50" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="28" font-weight="800" fill="#1D2939">01</text>
  <text x="563" y="308" width="50" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="28" font-weight="800" fill="#1D2939">02</text>
  <text x="563" y="418" width="50" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="28" font-weight="800" fill="#1D2939">03</text>
  <text x="563" y="528" width="50" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="28" font-weight="800" fill="#1D2939">04</text>
  <text x="563" y="638" width="50" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="28" font-weight="800" fill="#1D2939">05</text>

  <text x="675" y="177" width="470" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="24" font-weight="750" fill="#101828">
    Introductions &amp; outcomes
  </text>
  <text x="675" y="207" width="470" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" fill="#667085">
    Set the ambition, frame the decisions, and align on the working rhythm.
  </text>

  <text x="675" y="287" width="470" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="24" font-weight="750" fill="#101828">
    Why transformation now?
  </text>
  <text x="675" y="317" width="470" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" fill="#667085">
    Review market pressure, customer shifts, and internal performance gaps.
  </text>

  <text x="675" y="397" width="470" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="24" font-weight="750" fill="#101828">
    What must change?
  </text>
  <text x="675" y="427" width="470" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" fill="#667085">
    Identify capabilities, processes, and behaviors that require redesign.
  </text>

  <text x="675" y="507" width="470" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="24" font-weight="750" fill="#101828">
    How we will execute
  </text>
  <text x="675" y="537" width="470" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" fill="#667085">
    Define workstreams, governance, milestones, and decision checkpoints.
  </text>

  <text x="675" y="617" width="470" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="24" font-weight="750" fill="#101828">
    Owners and next steps
  </text>
  <text x="675" y="647" width="470" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" fill="#667085">
    Confirm sponsors, accountable leads, and the first 30-day action plan.
  </text>
</svg>
```

## Avoid in this skill
- ❌ Do not use SVG masks to “subtract” circles from the image; PowerPoint translation may fail or ignore the mask. Use white circles layered over the seam instead.
- ❌ Do not apply `clip-path` to the scallop circles or content panel; clipping is only reliable on `<image>` for this workflow.
- ❌ Do not make the image and content areas exactly 50/50 if the agenda text is long; the right panel needs more breathing room.
- ❌ Do not place the numbers far inside the content area; the numbers should sit directly on the scalloped boundary to preserve the illusion.
- ❌ Do not use thin outlines around the white scallops; the effect depends on clean negative space, not bordered badges.

## Composition notes
- Keep the title in a shallow top band, then let the photo begin below it so the agenda system has a clear vertical stage.
- Place the scallop centers exactly on the photo/content seam; half of each circle should overlap the image and half should sit in the white panel.
- Use generous right-side whitespace: item titles should start 80–100 px to the right of the seam, leaving the scallop numbers visually isolated.
- Use a darker photo overlay so the white scallops pop strongly against the image side while the right panel remains calm and readable.