# SVG Recipe — 3D Radial Hub & Spoke Infographic

## Visual mechanism
A segmented radial hub sits behind a glossy central sphere, with color-matched rounded “spokes” extending outward to eight labeled points. Small 3D spheres cap each spoke-to-hub joint, hiding geometry seams and creating a polished dimensional infographic.

## SVG primitives needed
- 8× `<path>` for colored radial pie-slice hub segments behind the center sphere
- 8× `<rect>` for outward rounded pill spokes
- 8× smaller `<rect>` overlays for glossy highlights on the pill spokes
- 9× `<circle>` for one large central sphere and eight small junction spheres
- 9× small highlight `<ellipse>` / `<circle>` overlays to strengthen the 3D sphere illusion
- 17× `<text>` for title, central hub label, spoke labels, and numeric sphere labels
- 1× `<linearGradient>` for the slide background
- 1× `<radialGradient>` for the large central 3D sphere
- 1× `<radialGradient>` for the small junction spheres
- 1× `<linearGradient>` for pill gloss overlays
- 2× `<filter>` definitions for soft drop shadows on pills and spheres

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#FAFBFD"/>
      <stop offset="100%" stop-color="#ECEFF4"/>
    </linearGradient>

    <radialGradient id="sphereLarge" cx="38%" cy="30%" r="72%" fx="25%" fy="18%">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="42%" stop-color="#F2F4F7"/>
      <stop offset="78%" stop-color="#D9DDE3"/>
      <stop offset="100%" stop-color="#B8BEC8"/>
    </radialGradient>

    <radialGradient id="sphereSmall" cx="35%" cy="28%" r="74%" fx="24%" fy="18%">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="48%" stop-color="#F1F3F6"/>
      <stop offset="82%" stop-color="#D4D8DF"/>
      <stop offset="100%" stop-color="#AEB5C0"/>
    </radialGradient>

    <linearGradient id="pillGloss" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.38"/>
      <stop offset="100%" stop-color="#FFFFFF" stop-opacity="0"/>
    </linearGradient>

    <filter id="softShadow" x="-25%" y="-35%" width="150%" height="180%">
      <feOffset dx="0" dy="8"/>
      <feGaussianBlur stdDeviation="9"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="sphereShadow" x="-35%" y="-35%" width="170%" height="180%">
      <feOffset dx="0" dy="12"/>
      <feGaussianBlur stdDeviation="13"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bg)"/>
  <text x="640" y="58" width="720" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="700" fill="#293241">8 Step Business Infographic</text>
  <text x="640" y="91" width="640" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#7B8492">A radial hub-and-spoke map for strategy, capabilities, or process architecture</text>

  <!-- segmented radial hub, intentionally hidden in the middle by the large sphere -->
  <path d="M640 360 L646 170 A190 190 0 0 1 770 219 Z" fill="#34568B" stroke="#F7F8FA" stroke-width="4"/>
  <path d="M640 360 L779 230 A190 190 0 0 1 830 353 Z" fill="#6B5B95" stroke="#F7F8FA" stroke-width="4"/>
  <path d="M640 360 L830 367 A190 190 0 0 1 779 490 Z" fill="#0072B5" stroke="#F7F8FA" stroke-width="4"/>
  <path d="M640 360 L770 501 A190 190 0 0 1 647 550 Z" fill="#00A170" stroke="#F7F8FA" stroke-width="4"/>
  <path d="M640 360 L633 550 A190 190 0 0 1 510 490 Z" fill="#92A8D1" stroke="#F7F8FA" stroke-width="4"/>
  <path d="M640 360 L501 490 A190 190 0 0 1 450 367 Z" fill="#88B04B" stroke="#F7F8FA" stroke-width="4"/>
  <path d="M640 360 L450 353 A190 190 0 0 1 501 230 Z" fill="#EFC050" stroke="#F7F8FA" stroke-width="4"/>
  <path d="M640 360 L510 221 A190 190 0 0 1 633 170 Z" fill="#E15D44" stroke="#F7F8FA" stroke-width="4"/>

  <!-- left spokes -->
  <rect x="130" y="140" width="380" height="62" rx="31" fill="#E15D44" filter="url(#softShadow)"/>
  <rect x="130" y="140" width="380" height="24" rx="12" fill="url(#pillGloss)" opacity="0.85"/>
  <rect x="130" y="228" width="340" height="62" rx="31" fill="#EFC050" filter="url(#softShadow)"/>
  <rect x="130" y="228" width="340" height="24" rx="12" fill="url(#pillGloss)" opacity="0.8"/>
  <rect x="130" y="430" width="340" height="62" rx="31" fill="#88B04B" filter="url(#softShadow)"/>
  <rect x="130" y="430" width="340" height="24" rx="12" fill="url(#pillGloss)" opacity="0.8"/>
  <rect x="130" y="518" width="380" height="62" rx="31" fill="#92A8D1" filter="url(#softShadow)"/>
  <rect x="130" y="518" width="380" height="24" rx="12" fill="url(#pillGloss)" opacity="0.8"/>

  <!-- right spokes -->
  <rect x="770" y="140" width="380" height="62" rx="31" fill="#6B5B95" filter="url(#softShadow)"/>
  <rect x="770" y="140" width="380" height="24" rx="12" fill="url(#pillGloss)" opacity="0.82"/>
  <rect x="810" y="228" width="340" height="62" rx="31" fill="#34568B" filter="url(#softShadow)"/>
  <rect x="810" y="228" width="340" height="24" rx="12" fill="url(#pillGloss)" opacity="0.8"/>
  <rect x="810" y="430" width="340" height="62" rx="31" fill="#0072B5" filter="url(#softShadow)"/>
  <rect x="810" y="430" width="340" height="24" rx="12" fill="url(#pillGloss)" opacity="0.8"/>
  <rect x="770" y="518" width="380" height="62" rx="31" fill="#00A170" filter="url(#softShadow)"/>
  <rect x="770" y="518" width="380" height="24" rx="12" fill="url(#pillGloss)" opacity="0.8"/>

  <!-- spoke labels -->
  <text x="430" y="178" width="260" text-anchor="end" font-family="Segoe UI, Microsoft YaHei" font-size="19" font-weight="700" fill="#FFFFFF">Market Insight</text>
  <text x="391" y="266" width="240" text-anchor="end" font-family="Segoe UI, Microsoft YaHei" font-size="19" font-weight="700" fill="#FFFFFF">Customer Fit</text>
  <text x="391" y="468" width="240" text-anchor="end" font-family="Segoe UI, Microsoft YaHei" font-size="19" font-weight="700" fill="#FFFFFF">Operations</text>
  <text x="430" y="556" width="260" text-anchor="end" font-family="Segoe UI, Microsoft YaHei" font-size="19" font-weight="700" fill="#FFFFFF">Governance</text>
  <text x="850" y="178" width="260" font-family="Segoe UI, Microsoft YaHei" font-size="19" font-weight="700" fill="#FFFFFF">Brand System</text>
  <text x="890" y="266" width="240" font-family="Segoe UI, Microsoft YaHei" font-size="19" font-weight="700" fill="#FFFFFF">Data Platform</text>
  <text x="890" y="468" width="240" font-family="Segoe UI, Microsoft YaHei" font-size="19" font-weight="700" fill="#FFFFFF">Growth Engine</text>
  <text x="850" y="556" width="260" font-family="Segoe UI, Microsoft YaHei" font-size="19" font-weight="700" fill="#FFFFFF">Partner Network</text>

  <!-- large central 3D sphere -->
  <circle cx="640" cy="360" r="118" fill="url(#sphereLarge)" filter="url(#sphereShadow)"/>
  <ellipse cx="600" cy="310" rx="38" ry="24" fill="#FFFFFF" opacity="0.72"/>
  <text x="640" y="348" width="190" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="21" font-weight="700" fill="#333A45">CORE</text>
  <text x="640" y="382" width="210" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="27" font-weight="800" fill="#202734">STRATEGY</text>

  <!-- junction spheres with numbers -->
  <circle cx="500" cy="171" r="37" fill="url(#sphereSmall)" filter="url(#sphereShadow)"/>
  <circle cx="460" cy="259" r="37" fill="url(#sphereSmall)" filter="url(#sphereShadow)"/>
  <circle cx="460" cy="461" r="37" fill="url(#sphereSmall)" filter="url(#sphereShadow)"/>
  <circle cx="500" cy="549" r="37" fill="url(#sphereSmall)" filter="url(#sphereShadow)"/>
  <circle cx="780" cy="171" r="37" fill="url(#sphereSmall)" filter="url(#sphereShadow)"/>
  <circle cx="820" cy="259" r="37" fill="url(#sphereSmall)" filter="url(#sphereShadow)"/>
  <circle cx="820" cy="461" r="37" fill="url(#sphereSmall)" filter="url(#sphereShadow)"/>
  <circle cx="780" cy="549" r="37" fill="url(#sphereSmall)" filter="url(#sphereShadow)"/>

  <text x="500" y="179" width="60" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="19" font-weight="800" fill="#5D6570">01</text>
  <text x="460" y="267" width="60" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="19" font-weight="800" fill="#5D6570">02</text>
  <text x="460" y="469" width="60" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="19" font-weight="800" fill="#5D6570">03</text>
  <text x="500" y="557" width="60" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="19" font-weight="800" fill="#5D6570">04</text>
  <text x="780" y="179" width="60" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="19" font-weight="800" fill="#5D6570">05</text>
  <text x="820" y="267" width="60" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="19" font-weight="800" fill="#5D6570">06</text>
  <text x="820" y="469" width="60" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="19" font-weight="800" fill="#5D6570">07</text>
  <text x="780" y="557" width="60" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="19" font-weight="800" fill="#5D6570">08</text>
</svg>
```

## Avoid in this skill
- ❌ Do not use `<mask>` to hide the inner hub; simply place the large central sphere above the radial paths.
- ❌ Do not build the spokes with rotated groups or skew transforms; horizontal rounded rectangles are cleaner and translate more reliably.
- ❌ Do not use `<marker-end>` for spoke connectors; this design does not need arrowheads, and markers may disappear.
- ❌ Do not apply filters to `<line>` elements; use filtered `<rect>`, `<circle>`, or `<path>` shapes for shadows.
- ❌ Do not omit `width` on text labels; every `<text>` needs an explicit width for predictable PowerPoint rendering.

## Composition notes
- Keep the visual center around `(640, 360)` with the large sphere covering the inner pie-slice joints; this is what makes the geometry look seamless.
- Use four spokes on each side, vertically staggered so the top and bottom spokes are slightly longer than the middle spokes.
- Match each spoke color to its nearest hub segment so the viewer reads the layout as one continuous radial system.
- Leave generous top space for the slide title and keep the outer left/right edges clear so labels feel premium rather than cramped.