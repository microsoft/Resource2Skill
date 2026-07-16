# SVG Recipe — Layered Flat Design Scenery

## Visual mechanism
A handcrafted flat landscape is built by stacking simple vector silhouettes from back to front: sky details, distant hills, house and trees, foreground hills, then water. Depth comes from z-order, scale, and muted color shifts rather than realistic shading.

## SVG primitives needed
- 1× `<rect>` for the solid dark teal sky background
- 3× translucent `<path>` trapezoids for angled light beams
- 1× `<circle>` with a soft blur `<filter>` for a subtle sun/glow accent
- 9× `<circle>` / `<ellipse>` for flat cloud clusters and chimney smoke
- 5× large curved `<path>` shapes for layered semicircle-style hills and island landforms
- 6× `<path>` leaf/teardrop forms for stylized tree canopies
- 4× `<rect>` for tree trunks, house body, door, and windows
- 1× `<path>` for the house roof
- 2× rounded `<rect>` shapes for foreground water bands
- 5× `<line>` elements for water ripples
- 2× `<text>` blocks with explicit `width` for title-slide usage
- 1× `<filter id="softGlow">` applied to the sun only

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <filter id="softGlow" x="-80%" y="-80%" width="260%" height="260%">
      <feGaussianBlur stdDeviation="18"/>
    </filter>
  </defs>

  <!-- Background sky -->
  <rect x="0" y="0" width="1280" height="720" fill="#004D40"/>

  <!-- Quiet sun glow and angled flat light beams -->
  <circle cx="1018" cy="132" r="62" fill="#FFF8E1" opacity="0.24" filter="url(#softGlow)"/>
  <circle cx="1018" cy="132" r="24" fill="#FFF3C4" opacity="0.55"/>
  <path d="M760 0 L860 0 L620 520 L545 520 Z" fill="#FFFFFF" opacity="0.09"/>
  <path d="M905 0 L990 0 L810 520 L735 520 Z" fill="#FFFFFF" opacity="0.075"/>
  <path d="M1080 0 L1160 0 L1045 520 L970 520 Z" fill="#FFFFFF" opacity="0.06"/>

  <!-- Clouds, kept very flat and geometric -->
  <g opacity="0.94">
    <ellipse cx="185" cy="118" rx="58" ry="24" fill="#FFFFFF"/>
    <circle cx="145" cy="113" r="25" fill="#FFFFFF"/>
    <circle cx="205" cy="97" r="34" fill="#FFFFFF"/>
    <circle cx="247" cy="118" r="22" fill="#FFFFFF"/>

    <ellipse cx="1090" cy="248" rx="64" ry="25" fill="#FFFFFF" opacity="0.86"/>
    <circle cx="1048" cy="243" r="23" fill="#FFFFFF" opacity="0.86"/>
    <circle cx="1115" cy="225" r="34" fill="#FFFFFF" opacity="0.86"/>
    <circle cx="1162" cy="249" r="20" fill="#FFFFFF" opacity="0.86"/>
  </g>

  <!-- Title text area, balanced against the illustration -->
  <text x="92" y="284" width="455" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="54" font-weight="700" fill="#E8F5E9">
    Layered Flat
    <tspan x="92" dy="62" fill="#B9E4A8">Design Scenery</tspan>
  </text>
  <text x="96" y="407" width="420" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="22" fill="#B2DFDB" opacity="0.92">
    Build a memorable keynote landscape from editable PowerPoint vector shapes.
  </text>

  <!-- Distant land mass -->
  <path d="M455 555 A240 178 0 0 1 935 555 L935 628 L455 628 Z" fill="#558B2F"/>
  <path d="M272 575 A310 206 0 0 1 892 575 L892 640 L272 640 Z" fill="#9CCC65"/>
  <path d="M604 580 A250 162 0 0 1 1104 580 L1104 646 L604 646 Z" fill="#B9E4A8"/>

  <!-- House -->
  <rect x="715" y="390" width="86" height="76" rx="3" fill="#FFCCBC"/>
  <path d="M700 394 L758 341 L816 394 Z" fill="#BF360C"/>
  <rect x="746" y="422" width="24" height="44" rx="2" fill="#6D4C41"/>
  <rect x="721" y="408" width="20" height="18" rx="2" fill="#FFF3E0"/>
  <rect x="779" y="408" width="18" height="18" rx="2" fill="#FFF3E0"/>

  <!-- Chimney smoke -->
  <ellipse cx="802" cy="339" rx="12" ry="8" fill="#FFFFFF" opacity="0.65"/>
  <ellipse cx="820" cy="315" rx="17" ry="11" fill="#FFFFFF" opacity="0.48"/>
  <ellipse cx="845" cy="286" rx="22" ry="13" fill="#FFFFFF" opacity="0.34"/>

  <!-- Trees: trunks plus split teardrop canopies -->
  <rect x="405" y="430" width="20" height="92" rx="4" fill="#558B2F"/>
  <path d="M416 444 C362 409 370 335 425 303 C454 359 453 416 416 444 Z" fill="#B9E4A8"/>
  <path d="M416 444 C470 409 462 335 407 303 C378 359 379 416 416 444 Z" fill="#9CCC65"/>

  <rect x="930" y="430" width="18" height="84" rx="4" fill="#558B2F"/>
  <path d="M939 442 C892 411 900 350 948 322 C975 370 973 414 939 442 Z" fill="#B9E4A8"/>
  <path d="M939 442 C986 411 978 350 930 322 C903 370 905 414 939 442 Z" fill="#9CCC65"/>

  <rect x="560" y="462" width="14" height="58" rx="3" fill="#558B2F"/>
  <path d="M567 472 C530 446 537 400 575 382 C594 421 594 451 567 472 Z" fill="#B9E4A8"/>
  <path d="M567 472 C604 446 597 400 559 382 C540 421 540 451 567 472 Z" fill="#9CCC65"/>

  <!-- Foreground island cap and water -->
  <path d="M335 604 C420 520 560 493 680 535 C775 568 886 535 965 585 C1012 615 981 652 867 655 L425 655 C315 650 279 631 335 604 Z" fill="#B9E4A8"/>
  <rect x="0" y="612" width="1280" height="108" fill="#4FC3F7"/>
  <rect x="138" y="626" width="1004" height="62" rx="31" fill="#81D4FA" opacity="0.96"/>

  <!-- Water ripples -->
  <line x1="207" y1="657" x2="342" y2="657" stroke="#E1F5FE" stroke-width="7" stroke-linecap="round" opacity="0.72"/>
  <line x1="420" y1="682" x2="514" y2="682" stroke="#E1F5FE" stroke-width="6" stroke-linecap="round" opacity="0.58"/>
  <line x1="610" y1="649" x2="760" y2="649" stroke="#E1F5FE" stroke-width="7" stroke-linecap="round" opacity="0.62"/>
  <line x1="854" y1="674" x2="980" y2="674" stroke="#E1F5FE" stroke-width="6" stroke-linecap="round" opacity="0.55"/>
  <line x1="1045" y1="644" x2="1130" y2="644" stroke="#E1F5FE" stroke-width="5" stroke-linecap="round" opacity="0.45"/>
</svg>
```

## Avoid in this skill
- ❌ Using `<mask>` to hide the lower halves of hills; instead, draw the hill as a closed semicircle-like `<path>` or cover its base with foreground water.
- ❌ Applying `clip-path` to hills, clouds, or other non-image shapes; the translator only preserves clipping reliably on `<image>`.
- ❌ Overusing gradients and shadows; this style depends on flat color layers and clean silhouettes.
- ❌ Using `<use>` for repeated trees or clouds; duplicate the editable shapes directly so PowerPoint receives separate native objects.
- ❌ Using `marker-end` arrows or complex SVG symbols for decorative birds/ripples; keep accents as simple editable paths or lines.

## Composition notes
- Keep the landscape in the lower half to lower third of the slide; reserve the upper sky for title text, clouds, and light beams.
- Layer from darkest/farthest to lightest/nearest: dark back hill, medium hill, house/trees, light foreground island, then water.
- Use a limited analogous palette: dark teal background, three greens for terrain, light blue water, and one warm accent for the house roof.
- Leave generous negative space around the title; the illustration should feel like a handcrafted scene supporting the message, not a dense infographic.