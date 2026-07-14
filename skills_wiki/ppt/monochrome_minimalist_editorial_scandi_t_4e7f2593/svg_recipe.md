# SVG Recipe — Monochrome Minimalist Editorial (Scandi-Tech Aesthetic)

## Visual mechanism
A stark white editorial canvas uses a bottom-anchored black-and-white image fade, thin geometric framing, large disciplined typography, and tiny rotated perimeter labels. A single muted coral accent appears only in micro data marks and one structural detail, making the slide feel premium, restrained, and intentional.

## SVG primitives needed
- 1× `<rect>` full-slide white background
- 1× `<clipPath>` with `<rect>` to crop the bottom editorial photo
- 1× `<image>` for the black-and-white atmospheric photo layer
- 1× `<linearGradient>` for the white fade overlay above the photo
- 1× `<rect>` using the fade gradient to dissolve the photo into negative space
- 1× `<rect>` outline-only editorial frame around the title area
- 6× `<line>` for hairline grid rules, chart axis, and minimalist perimeter structure
- 4× `<rect>` for sparse monochrome/coral data bars
- 3× `<circle>` for minimalist data points/accent dots
- 1× `<path>` for a thin organic contour/mountain trace over the photo
- 10× `<text>` blocks for title, subtitle, captions, metadata, rotated micro-typography, and data labels

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <clipPath id="photoCrop">
      <rect x="0" y="380" width="1280" height="340" rx="0"/>
    </clipPath>

    <linearGradient id="photoFadeToWhite" x1="0" y1="380" x2="0" y2="590" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#FFFFFF" stop-opacity="1"/>
      <stop offset="0.36" stop-color="#FFFFFF" stop-opacity="0.92"/>
      <stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/>
    </linearGradient>

    <linearGradient id="quietBar" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#1E1E1E"/>
      <stop offset="1" stop-color="#6E6E6E"/>
    </linearGradient>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#FFFFFF"/>

  <image
    x="0" y="360" width="1280" height="380"
    preserveAspectRatio="xMidYMid slice"
    clip-path="url(#photoCrop)"
    href="https://images.example.com/monochrome-high-contrast-snow-mountain-editorial.jpg"/>

  <rect x="0" y="360" width="1280" height="250" fill="url(#photoFadeToWhite)"/>

  <path d="M92 604 C190 568, 255 596, 336 548 C420 496, 494 570, 578 525 C658 482, 744 534, 832 500 C928 462, 1014 520, 1186 474"
        fill="none" stroke="#FFFFFF" stroke-width="1.4" opacity="0.72"/>

  <line x1="96" y1="88" x2="1184" y2="88" stroke="#1E1E1E" stroke-width="1"/>
  <line x1="96" y1="632" x2="1184" y2="632" stroke="#1E1E1E" stroke-width="1" opacity="0.65"/>
  <line x1="96" y1="88" x2="96" y2="632" stroke="#1E1E1E" stroke-width="1" opacity="0.45"/>
  <line x1="1184" y1="88" x2="1184" y2="632" stroke="#1E1E1E" stroke-width="1" opacity="0.45"/>

  <rect x="418" y="176" width="444" height="214" fill="none" stroke="#1E1E1E" stroke-width="2"/>

  <text x="132" y="112" width="260" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="11" font-weight="700" letter-spacing="4" fill="#1E1E1E">
    SYSTEM INDEX / 2026
  </text>

  <text x="456" y="252" width="390" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="62" font-weight="800" letter-spacing="-2" fill="#1E1E1E">
    NORDIC
  </text>

  <text x="456" y="314" width="390" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="62" font-weight="800" letter-spacing="-2" fill="#1E1E1E">
    SYSTEMS
  </text>

  <text x="456" y="354" width="338" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="12" font-weight="600" letter-spacing="3" fill="#777777">
    M O N O C H R O M E   D A T A   B R I E F
  </text>

  <text x="882" y="198" width="170" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="10" font-weight="600" letter-spacing="2" fill="#DC695F">
    / SIGNAL CLARITY
  </text>

  <text x="882" y="226" width="220" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="12" fill="#555555">
    Reduced interface noise across four product surfaces, indexed to Q1 baseline.
  </text>

  <text x="54" y="548" width="360" transform="rotate(-90 54 548)"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="9" font-weight="700" letter-spacing="4" fill="#1E1E1E">
    S C A N D I  -  T E C H   E D I T O R I A L
  </text>

  <text x="1226" y="174" width="300" transform="rotate(90 1226 174)"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="9" font-weight="700" letter-spacing="4" fill="#777777">
    C O N S T R A I N E D   C O L O U R   S Y S T E M
  </text>

  <line x1="900" y1="514" x2="1104" y2="514" stroke="#1E1E1E" stroke-width="1"/>
  <line x1="900" y1="456" x2="900" y2="514" stroke="#1E1E1E" stroke-width="1"/>

  <rect x="924" y="486" width="18" height="28" fill="url(#quietBar)"/>
  <rect x="966" y="470" width="18" height="44" fill="url(#quietBar)"/>
  <rect x="1008" y="442" width="18" height="72" fill="#DC695F"/>
  <rect x="1050" y="462" width="18" height="52" fill="url(#quietBar)"/>

  <circle cx="933" cy="486" r="3.5" fill="#1E1E1E"/>
  <circle cx="1017" cy="442" r="4.5" fill="#DC695F"/>
  <circle cx="1059" cy="462" r="3.5" fill="#1E1E1E"/>

  <text x="900" y="542" width="220" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="9" font-weight="700" letter-spacing="3" fill="#1E1E1E">
    NOISE INDEX / 4 SURFACES
  </text>

  <text x="132" y="604" width="310" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="12" fill="#FFFFFF" opacity="0.88">
    High-contrast imagery remains secondary: it anchors the page while the white field carries the message.
  </text>
</svg>
```

## Avoid in this skill
- ❌ Do not use colorful chart palettes; the effect depends on near-total monochrome with one muted coral accent.
- ❌ Do not fill the slide with dense grids, labels, or dashboard elements; data should appear as sparse editorial evidence.
- ❌ Do not use masks for the image fade; use a white gradient overlay rectangle instead.
- ❌ Do not apply clip paths to text, rectangles, or chart marks; only clip the `<image>` layer.
- ❌ Do not add heavy shadows, glossy effects, or 3D styling; they break the Scandi editorial restraint.

## Composition notes
- Keep 55–70% of the slide visually empty; the whitespace is the luxury signal, not unused space.
- Anchor visual weight asymmetrically: title/frame near center-left, sparse data at right, atmospheric photo along the bottom edge.
- Use hairline rules and rotated micro-type to create a perimeter “editorial frame.”
- Limit the coral accent to one data bar, one tiny label, or one dot so it feels curated rather than decorative.