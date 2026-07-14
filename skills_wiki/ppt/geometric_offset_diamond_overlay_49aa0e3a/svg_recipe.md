# SVG Recipe — Geometric Offset Diamond Overlay

## Visual mechanism
A square hero image is clipped into a crisp diamond, then paired with a thick hollow diamond outline that is intentionally shifted up and to the right. The offset creates editorial tension and a layered, faux-3D feel while keeping the layout geometrically disciplined.

## SVG primitives needed
- 1× `<rect>` for the full-slide background
- 1× `<linearGradient>` for a subtle premium white-to-blush background wash
- 1× `<clipPath>` with a diamond `<path>` to crop the hero image
- 1× `<image>` for the clipped hero photo
- 1× `<path>` for the soft diamond shadow behind the clipped image
- 1× `<filter id="softShadow">` applied to the shadow diamond
- 1× `<path>` for the offset hollow accent diamond frame
- 3× `<line>` for thin accent dividers and data-rule details
- 4× `<path>` for small decorative diamond motifs
- Multiple `<text>` elements with explicit `width` attributes for kicker, headline, body copy, and metric callouts

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgWash" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="62%" stop-color="#FBFBFC"/>
      <stop offset="100%" stop-color="#FFF0F4"/>
    </linearGradient>

    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feOffset dx="0" dy="18" result="off"/>
      <feGaussianBlur in="off" stdDeviation="18" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <clipPath id="diamondCrop" clipPathUnits="userSpaceOnUse">
      <path d="M925 105 L1165 345 L925 585 L685 345 Z"/>
    </clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgWash)"/>

  <!-- Left editorial text block -->
  <text x="96" y="96" width="360" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="14" font-weight="700" letter-spacing="2.8" fill="#A9ADB5">
    STRATEGIC PORTFOLIO
  </text>

  <line x1="96" y1="126" x2="224" y2="126" stroke="#D52B52" stroke-width="5" stroke-linecap="round"/>

  <text x="94" y="210" width="470" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="60" font-weight="800" letter-spacing="-1.2" fill="#1E1E1E">
    <tspan x="94" dy="0">PROJECT</tspan>
    <tspan x="94" dy="66">DESCRIPTION</tspan>
  </text>

  <text x="98" y="362" width="420" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="17" font-weight="400" fill="#6E737C">
    <tspan x="98" dy="0">A focused visual system for turning standard</tspan>
    <tspan x="98" dy="25">business imagery into a sharp, high-contrast</tspan>
    <tspan x="98" dy="25">executive narrative with geometric momentum.</tspan>
  </text>

  <line x1="98" y1="462" x2="468" y2="462" stroke="#D9DCE2" stroke-width="1.5"/>

  <text x="98" y="512" width="140" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="42" font-weight="800" fill="#D52B52">42%</text>
  <text x="98" y="544" width="180" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="13" font-weight="700" letter-spacing="1.6" fill="#767B84">GROWTH INDEX</text>

  <text x="286" y="512" width="140" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="42" font-weight="800" fill="#1E1E1E">18M</text>
  <text x="286" y="544" width="180" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="13" font-weight="700" letter-spacing="1.6" fill="#767B84">ACTIVE REACH</text>

  <line x1="98" y1="585" x2="174" y2="585" stroke="#D52B52" stroke-width="3"/>
  <line x1="190" y1="585" x2="468" y2="585" stroke="#D9DCE2" stroke-width="3"/>

  <!-- Decorative micro diamonds echo the main geometry -->
  <path d="M564 142 L582 160 L564 178 L546 160 Z" fill="none" stroke="#E7A2B4" stroke-width="2"/>
  <path d="M612 598 L626 612 L612 626 L598 612 Z" fill="#D52B52" opacity="0.22"/>
  <path d="M1218 626 L1235 643 L1218 660 L1201 643 Z" fill="none" stroke="#D52B52" stroke-width="3"/>
  <path d="M632 84 L640 92 L632 100 L624 92 Z" fill="#1E1E1E" opacity="0.16"/>

  <!-- Shadow diamond placed behind the clipped image -->
  <path d="M925 105 L1165 345 L925 585 L685 345 Z"
        fill="#1E1E1E" opacity="0.13" filter="url(#softShadow)"/>

  <!-- Diamond-clipped hero image -->
  <image x="685" y="105" width="480" height="480"
         href="https://images.unsplash.com/photo-1556761175-5973dc0f32d7?auto=format&amp;fit=crop&amp;w=1200&amp;q=85"
         preserveAspectRatio="xMidYMid slice"
         clip-path="url(#diamondCrop)"/>

  <!-- Offset hollow diamond frame: deliberately misaligned upward and rightward -->
  <path d="M986 58 L1238 310 L986 562 L734 310 Z"
        fill="none" stroke="#D52B52" stroke-width="10" stroke-linejoin="miter"/>

  <!-- Small label attached to the diamond composition -->
  <rect x="920" y="618" width="212" height="46" rx="23" fill="#FFFFFF" stroke="#ECEEF2" stroke-width="1.5"/>
  <text x="950" y="647" width="160" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="14" font-weight="800" letter-spacing="1.8" fill="#D52B52">
    OFFSET OVERLAY
  </text>
</svg>
```

## Avoid in this skill
- ❌ Do not rotate a normal rectangular image and leave it uncropped; the technique depends on a true diamond crop using `clipPath` applied directly to the `<image>`.
- ❌ Do not use `clip-path` on the accent frame or shadow path; clipping non-image elements is ignored by the translator.
- ❌ Do not use `<mask>` to create the diamond image; use a `<clipPath>` with a path or polygon instead.
- ❌ Do not center-align the whole layout; the effect works best with strict left typography and an oversized right-side geometric image.
- ❌ Do not make the frame perfectly aligned with the image unless you want a simple border; the visual signature is the deliberate offset.

## Composition notes
- Keep the text block in the left 35–42% of the slide with generous white space; the right-side diamond should dominate the visual weight.
- Offset the hollow frame by roughly 40–80 px horizontally and 25–60 px vertically from the clipped image for visible tension.
- Use one strong accent color for the frame, divider, and small data highlights so the geometry feels integrated with the slide system.
- Let the diamond approach or slightly exceed the safe margins; large scale makes the layout feel like an editorial keynote rather than a standard image placeholder.