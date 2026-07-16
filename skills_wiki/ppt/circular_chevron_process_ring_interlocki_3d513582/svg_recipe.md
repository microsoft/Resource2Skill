# SVG Recipe — Circular Chevron Process Ring (Interlocking Flow)

## Visual mechanism
A complete circular process ring is built from equal curved chevron segments: each arc has a pointed leading edge and a notched trailing edge, making the phases look physically interlocked and implying continuous clockwise motion. The center remains open for a unifying label, while concise phase notes radiate around the outside.

## SVG primitives needed
- 6× `<path>` for the interlocking curved chevron segments
- 6× `<linearGradient>` for jewel-tone segment fills with subtle dimensional highlights
- 1× `<ellipse>` for a soft shared shadow under the ring
- 1× `<circle>` for the central void / label container
- 6× `<circle>` for small numeric badges on top of each segment
- 1× `<filter id="softShadow">` using `feOffset + feGaussianBlur + feMerge` applied to the shadow ellipse
- 6× `<line>` for subtle radial callout connectors
- 19× `<text>` for center title, segment numbers, and outside labels; every text element includes an explicit `width` attribute

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="gPurple" x1="520" y1="120" x2="720" y2="280" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#7F4BC0"/><stop offset="1" stop-color="#592C82"/>
    </linearGradient>
    <linearGradient id="gCrimson" x1="780" y1="200" x2="900" y2="430" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#DD386E"/><stop offset="1" stop-color="#BA144C"/>
    </linearGradient>
    <linearGradient id="gOrange" x1="760" y1="420" x2="650" y2="610" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#FFAA45"/><stop offset="1" stop-color="#EB7E1F"/>
    </linearGradient>
    <linearGradient id="gMustard" x1="620" y1="590" x2="430" y2="470" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#FFD84B"/><stop offset="1" stop-color="#F9BB0E"/>
    </linearGradient>
    <linearGradient id="gSlate" x1="430" y1="470" x2="440" y2="230" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#5B8DD1"/><stop offset="1" stop-color="#426EA9"/>
    </linearGradient>
    <linearGradient id="gNavy" x1="450" y1="220" x2="620" y2="120" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#3D4B9D"/><stop offset="1" stop-color="#2D3470"/>
    </linearGradient>
    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feOffset dx="0" dy="12" in="SourceAlpha" result="off"/>
      <feGaussianBlur in="off" stdDeviation="16" result="blur"/>
      <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#F7F8FB"/>
  <ellipse cx="640" cy="382" rx="260" ry="245" fill="#000000" opacity="0.13" filter="url(#softShadow)"/>

  <path d="M 640 135 A 225 225 0 0 1 834.9 247.5 L 768.9 243.9 L 745.7 299 A 122 122 0 0 0 640 238 L 603.9 190.3 Z" fill="url(#gPurple)" stroke="#FFFFFF" stroke-width="5"/>
  <path d="M 834.9 247.5 A 225 225 0 0 1 834.9 472.5 L 805 413.6 L 745.7 421 A 122 122 0 0 0 745.7 299 L 768.9 243.9 Z" fill="url(#gCrimson)" stroke="#FFFFFF" stroke-width="5"/>
  <path d="M 834.9 472.5 A 225 225 0 0 1 640 585 L 676.1 529.7 L 640 482 A 122 122 0 0 0 745.7 421 L 805 413.6 Z" fill="url(#gOrange)" stroke="#FFFFFF" stroke-width="5"/>
  <path d="M 640 585 A 225 225 0 0 1 445.1 472.5 L 511.1 476.1 L 534.3 421 A 122 122 0 0 0 640 482 L 676.1 529.7 Z" fill="url(#gMustard)" stroke="#FFFFFF" stroke-width="5"/>
  <path d="M 445.1 472.5 A 225 225 0 0 1 445.1 247.5 L 475 306.4 L 534.3 299 A 122 122 0 0 0 534.3 421 L 511.1 476.1 Z" fill="url(#gSlate)" stroke="#FFFFFF" stroke-width="5"/>
  <path d="M 445.1 247.5 A 225 225 0 0 1 640 135 L 603.9 190.3 L 640 238 A 122 122 0 0 0 534.3 299 L 475 306.4 Z" fill="url(#gNavy)" stroke="#FFFFFF" stroke-width="5"/>

  <circle cx="640" cy="360" r="105" fill="#F7F8FB" stroke="#FFFFFF" stroke-width="8"/>
  <text x="565" y="335" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#252A3A" text-anchor="middle">CONTINUOUS</text>
  <text x="548" y="363" width="184" font-family="Segoe UI, Microsoft YaHei" font-size="26" font-weight="800" fill="#252A3A" text-anchor="middle">IMPROVEMENT</text>
  <text x="580" y="392" width="120" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="700" fill="#6B7280" text-anchor="middle">LOOP</text>

  <circle cx="640" cy="178" r="25" fill="#FFFFFF" opacity="0.95"/><text x="625" y="188" width="30" font-family="Segoe UI" font-size="24" font-weight="800" fill="#592C82" text-anchor="middle">1</text>
  <circle cx="797" cy="269" r="25" fill="#FFFFFF" opacity="0.95"/><text x="782" y="279" width="30" font-family="Segoe UI" font-size="24" font-weight="800" fill="#BA144C" text-anchor="middle">2</text>
  <circle cx="797" cy="451" r="25" fill="#FFFFFF" opacity="0.95"/><text x="782" y="461" width="30" font-family="Segoe UI" font-size="24" font-weight="800" fill="#EB7E1F" text-anchor="middle">3</text>
  <circle cx="640" cy="542" r="25" fill="#FFFFFF" opacity="0.95"/><text x="625" y="552" width="30" font-family="Segoe UI" font-size="24" font-weight="800" fill="#B88700" text-anchor="middle">4</text>
  <circle cx="483" cy="451" r="25" fill="#FFFFFF" opacity="0.95"/><text x="468" y="461" width="30" font-family="Segoe UI" font-size="24" font-weight="800" fill="#426EA9" text-anchor="middle">5</text>
  <circle cx="483" cy="269" r="25" fill="#FFFFFF" opacity="0.95"/><text x="468" y="279" width="30" font-family="Segoe UI" font-size="24" font-weight="800" fill="#2D3470" text-anchor="middle">6</text>

  <line x1="640" y1="120" x2="640" y2="70" stroke="#BCC3D1" stroke-width="2" stroke-dasharray="5 7"/>
  <line x1="855" y1="235" x2="1030" y2="160" stroke="#BCC3D1" stroke-width="2" stroke-dasharray="5 7"/>
  <line x1="855" y1="485" x2="1030" y2="560" stroke="#BCC3D1" stroke-width="2" stroke-dasharray="5 7"/>
  <line x1="640" y1="600" x2="640" y2="665" stroke="#BCC3D1" stroke-width="2" stroke-dasharray="5 7"/>
  <line x1="425" y1="485" x2="250" y2="560" stroke="#BCC3D1" stroke-width="2" stroke-dasharray="5 7"/>
  <line x1="425" y1="235" x2="250" y2="160" stroke="#BCC3D1" stroke-width="2" stroke-dasharray="5 7"/>

  <text x="540" y="52" width="200" font-family="Segoe UI, Microsoft YaHei" font-size="21" font-weight="800" fill="#252A3A" text-anchor="middle">Discover</text>
  <text x="505" y="82" width="270" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#6B7280" text-anchor="middle">Capture signals and define the opportunity.</text>

  <text x="1035" y="150" width="190" font-family="Segoe UI, Microsoft YaHei" font-size="21" font-weight="800" fill="#252A3A">Design</text>
  <text x="1035" y="180" width="205" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#6B7280">Convert insight into a practical operating plan.</text>

  <text x="1035" y="548" width="190" font-family="Segoe UI, Microsoft YaHei" font-size="21" font-weight="800" fill="#252A3A">Deliver</text>
  <text x="1035" y="578" width="205" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#6B7280">Launch the workstream and coordinate execution.</text>

  <text x="540" y="690" width="200" font-family="Segoe UI, Microsoft YaHei" font-size="21" font-weight="800" fill="#252A3A" text-anchor="middle">Measure</text>
  <text x="505" y="714" width="270" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#6B7280" text-anchor="middle">Track outcomes and surface improvement levers.</text>

  <text x="55" y="548" width="190" font-family="Segoe UI, Microsoft YaHei" font-size="21" font-weight="800" fill="#252A3A" text-anchor="end">Optimize</text>
  <text x="40" y="578" width="210" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#6B7280" text-anchor="end">Tune the model before the next operating cycle.</text>

  <text x="55" y="150" width="190" font-family="Segoe UI, Microsoft YaHei" font-size="21" font-weight="800" fill="#252A3A" text-anchor="end">Scale</text>
  <text x="40" y="180" width="210" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#6B7280" text-anchor="end">Embed the new practice across teams and markets.</text>
</svg>
```

## Avoid in this skill
- ❌ Building the ring from ordinary pie slices only; it loses the interlocking flow effect.
- ❌ Using `<marker-end>` arrowheads on curved paths; arrowheads may disappear, and the chevron geometry already implies direction.
- ❌ Applying `clip-path` or `mask` to the colored segment paths; the technique should be native editable paths, not masked artwork.
- ❌ Overcrowding the ring interior with long labels; keep the central void clean and use the outer perimeter for detail.
- ❌ Using very thin gaps between segments; PowerPoint rendering can make hairline seams look inconsistent, so use clear white strokes.

## Composition notes
- Keep the ring centered and large, roughly 60–70% of slide height, with a clean central void for the concept label.
- Use short radial callouts outside the ring; place detailed text in the surrounding negative space rather than inside each segment.
- Maintain clockwise color rhythm with strong contrast between neighboring segments; jewel tones work especially well.
- Add a single soft shared shadow beneath the ring rather than heavy shadows on every segment, so the diagram feels cohesive instead of fragmented.