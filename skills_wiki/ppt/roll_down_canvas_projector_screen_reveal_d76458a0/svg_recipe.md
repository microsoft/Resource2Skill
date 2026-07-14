# SVG Recipe — Roll-Down Projector Screen Reveal

## Visual mechanism
A quote or mission statement is framed as a physical roll-down projector screen: a flat fabric canvas sits between glossy cylindrical bars, with a string and pull-ring suggesting the screen has just been revealed. The dimensional bars, shadows, overhangs, and tactile handle make the text feel staged and important.

## SVG primitives needed
- 1× `<rect>` for the full-slide background
- 1× `<rect>` for a subtle left-side presentation panel / context area
- 1× `<rect>` for the fabric screen canvas
- 2× `<rect>` for the top and bottom metallic cylindrical bars
- 2× `<ellipse>` for soft bar end-cap highlights
- 4× `<line>` for side cords, pull string, and bar highlight seams
- 2× `<circle>` for the pull-ring outer and inner hole
- 2× `<path>` for decorative hand-outline strokes below the ring
- 3× `<text>` blocks for heading, label, and editable quote content
- 1× `<linearGradient id="metalCylinder">` for the 3D bar finish
- 1× `<linearGradient id="canvasFill">` for subtle fabric depth
- 1× `<linearGradient id="darkPanel">` for the contrast panel
- 1× `<filter id="softShadow">` applied to the canvas and bars
- 1× `<filter id="textGlow">` applied to the key title text

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="pageBg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#f7f8fb"/>
      <stop offset="100%" stop-color="#e8ebf0"/>
    </linearGradient>

    <linearGradient id="darkPanel" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#122033"/>
      <stop offset="100%" stop-color="#223951"/>
    </linearGradient>

    <linearGradient id="canvasFill" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#fbfbfd"/>
      <stop offset="45%" stop-color="#eceef2"/>
      <stop offset="100%" stop-color="#d8dbe1"/>
    </linearGradient>

    <linearGradient id="metalCylinder" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#34363b"/>
      <stop offset="20%" stop-color="#777b82"/>
      <stop offset="43%" stop-color="#e7e8eb"/>
      <stop offset="58%" stop-color="#9b9da2"/>
      <stop offset="100%" stop-color="#2d2f34"/>
    </linearGradient>

    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="160%">
      <feOffset dx="0" dy="8"/>
      <feGaussianBlur stdDeviation="7"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="textGlow" x="-10%" y="-10%" width="120%" height="130%">
      <feGaussianBlur stdDeviation="1.8"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#pageBg)"/>
  <rect x="0" y="0" width="410" height="720" fill="url(#darkPanel)"/>

  <text x="44" y="86" width="320" font-family="Segoe UI, Microsoft YaHei" font-size="42" fill="#ffffff" letter-spacing="0.5">
    <tspan x="44" dy="0">Hero quote as</tspan>
    <tspan x="44" dy="62" font-size="70" font-weight="700" fill="#ffc400">Roll-Down</tspan>
    <tspan x="44" dy="76" font-size="70" font-weight="700" fill="#ffc400">Screen</tspan>
  </text>

  <text x="48" y="604" width="300" font-family="Segoe UI, Microsoft YaHei" font-size="24" fill="#d7e4f3">
    <tspan x="48" dy="0">Editable PPT shapes</tspan>
    <tspan x="48" dy="34" fill="#8fb3d9">canvas · bars · pull ring</tspan>
  </text>

  <!-- screen group, fully revealed state -->
  <rect x="513" y="170" width="620" height="250" fill="url(#canvasFill)" stroke="#c9ccd3" stroke-width="1.5" filter="url(#softShadow)"/>
  <line x1="533" y1="178" x2="533" y2="418" stroke="#b7bac1" stroke-width="2"/>
  <line x1="1113" y1="178" x2="1113" y2="418" stroke="#b7bac1" stroke-width="2"/>

  <rect x="488" y="146" width="670" height="34" rx="2" fill="url(#metalCylinder)" filter="url(#softShadow)"/>
  <ellipse cx="500" cy="163" rx="13" ry="16" fill="#42444a" opacity="0.65"/>
  <ellipse cx="1146" cy="163" rx="13" ry="16" fill="#24262a" opacity="0.65"/>
  <line x1="504" y1="154" x2="1140" y2="154" stroke="#f3f4f6" stroke-width="1.2" opacity="0.65"/>

  <rect x="488" y="409" width="670" height="34" rx="2" fill="url(#metalCylinder)" filter="url(#softShadow)"/>
  <ellipse cx="500" cy="426" rx="13" ry="16" fill="#42444a" opacity="0.65"/>
  <ellipse cx="1146" cy="426" rx="13" ry="16" fill="#24262a" opacity="0.65"/>
  <line x1="504" y1="417" x2="1140" y2="417" stroke="#f3f4f6" stroke-width="1.2" opacity="0.65"/>

  <text x="575" y="265" width="500" font-family="Segoe UI, Microsoft YaHei" font-size="28" fill="#2b2d31" text-anchor="middle">
    <tspan x="823" dy="0" font-size="30" font-style="italic">“Great strategy is not a document.</tspan>
    <tspan x="823" dy="42" font-size="30" font-style="italic">It is the shared picture of where</tspan>
    <tspan x="823" dy="42" font-size="30" font-style="italic">the organization is going next.”</tspan>
    <tspan x="823" dy="54" font-size="18" font-weight="700" fill="#6b7078">— EXECUTIVE OFFSITE PRINCIPLE</tspan>
  </text>

  <line x1="823" y1="443" x2="823" y2="494" stroke="#2c2f34" stroke-width="6" stroke-linecap="round"/>
  <circle cx="823" cy="524" r="35" fill="#2c2f34"/>
  <circle cx="823" cy="524" r="22" fill="#f0f2f6"/>
  <circle cx="814" cy="512" r="5" fill="#ffffff" opacity="0.45"/>

  <!-- optional illustrative hand outline, editable path strokes -->
  <path d="M755 581 C775 594 800 599 825 596 C846 594 861 585 870 568
           C879 549 873 535 859 529 C844 522 830 531 821 544
           C811 531 799 520 787 517 C774 514 766 521 768 536
           C748 527 735 530 731 541 C727 552 739 565 755 581 Z"
        fill="none" stroke="#111318" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M797 596 C790 618 790 640 805 660
           M847 586 C862 610 872 630 887 650
           M768 536 C782 553 801 564 823 569
           M821 544 C837 553 852 558 868 568"
        fill="none" stroke="#111318" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>

  <text x="560" y="90" width="560" font-family="Segoe UI, Microsoft YaHei" font-size="21" font-weight="700" fill="#6e7480" letter-spacing="2">
    PROJECTOR SCREEN REVEAL COMPONENT
  </text>
</svg>
```

## Avoid in this skill
- ❌ Do not use SVG `<animate>` to simulate the roll-down; build the final open state and add PowerPoint wipe / motion-path animation natively afterward.
- ❌ Do not use `<mask>` for the hollow pull ring; use two circles or an editable donut-like path instead.
- ❌ Do not apply filters to `<line>` elements such as cords or strings; use filters only on rectangles, paths, circles, ellipses, or text.
- ❌ Do not rely on `marker-end` for pull cords or arrows; if needed, draw arrowheads manually with paths or use plain lines.
- ❌ Do not place quote text without an explicit `width` attribute; otherwise PowerPoint text wrapping will not match the SVG layout.

## Composition notes
- Keep the screen centered or slightly right of center, occupying about 55–65% of slide width; the bars should overhang the canvas by 20–35 px on each side.
- The quote area needs generous interior padding, usually 60–80 px from the canvas edges, so the text feels intentionally staged rather than squeezed.
- Use metallic gradients on the top and bottom bars to create the physical projector-screen metaphor; the canvas itself should stay quiet and matte.
- Place the pull ring directly on the screen’s vertical centerline; it is the visual cue that makes the component feel mechanical and animation-ready.