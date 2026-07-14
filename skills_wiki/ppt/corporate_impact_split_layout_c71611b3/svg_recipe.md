# SVG Recipe — Corporate Impact Split-Layout

## Visual mechanism
A corporate identity slide built from bold cobalt top/bottom panels interrupted by a clean white horizontal band and a diagonal white split, creating a “presentation opener” frame. The center band carries the brand message, logo mark, and executive photo crop, while the blue fields provide high-contrast structure without competing with the content.

## SVG primitives needed
- 1× `<rect>` for the white slide background.
- 4× `<path>` for the cobalt blue top-left, top-right, bottom-left, and bottom-right geometric panels.
- 1× `<rect>` for the central white content band.
- 4× `<line>` for subtle horizontal and diagonal divider rules.
- 1× `<clipPath>` with `<rect>` for cropping the executive/team photo into the white band.
- 1× `<image>` for the right-side corporate people photo.
- 6× `<path>` for the editable circular-arrow logo illustration.
- 3× `<text>` elements for company name, tagline, and website.
- 1× `<linearGradient>` for premium blue panel depth.
- 1× `<filter id="softLogoShadow">` applied to the logo paths for slight dimensionality.

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="panelBlue" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#123cff"/>
      <stop offset="58%" stop-color="#0032f0"/>
      <stop offset="100%" stop-color="#0029ca"/>
    </linearGradient>

    <filter id="softLogoShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feOffset dx="0" dy="3"/>
      <feGaussianBlur stdDeviation="3"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <clipPath id="peopleCrop">
      <rect x="748" y="274" width="380" height="204" rx="0"/>
    </clipPath>
  </defs>

  <!-- Base canvas -->
  <rect x="0" y="0" width="1280" height="720" fill="#ffffff"/>

  <!-- Blue split panels -->
  <path d="M0 0 H586 L550 263 H0 Z" fill="url(#panelBlue)"/>
  <path d="M748 0 H1280 V263 H710 Z" fill="url(#panelBlue)"/>
  <path d="M0 477 H520 L485 720 H0 Z" fill="url(#panelBlue)"/>
  <path d="M678 477 H1280 V720 H645 Z" fill="url(#panelBlue)"/>

  <!-- White corporate information band -->
  <rect x="0" y="263" width="1280" height="214" fill="#ffffff"/>

  <!-- Subtle structural divider lines -->
  <line x1="0" y1="263" x2="1280" y2="263" stroke="#cfcfcf" stroke-width="1.2"/>
  <line x1="0" y1="477" x2="1280" y2="477" stroke="#cfcfcf" stroke-width="1.2"/>
  <line x1="586" y1="0" x2="550" y2="263" stroke="#002299" stroke-width="1.4"/>
  <line x1="748" y1="0" x2="710" y2="263" stroke="#002299" stroke-width="1.4"/>
  <line x1="520" y1="477" x2="485" y2="720" stroke="#002299" stroke-width="1.4"/>
  <line x1="678" y1="477" x2="645" y2="720" stroke="#002299" stroke-width="1.4"/>

  <!-- Left-side brand copy -->
  <text x="140" y="362" width="390" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="31" fill="#0030a8" font-weight="400">
    Decisions Plus Strategic
  </text>
  <text x="142" y="389" width="360" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="17" fill="#0030a8" font-style="italic">
    "we serve businesses who serve the world"
  </text>
  <text x="183" y="430" width="300" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="17" fill="#0030a8" font-style="italic">
    www.decisionsplusstrategic.com
  </text>

  <!-- Editable circular-arrows logo approximation -->
  <g filter="url(#softLogoShadow)">
    <path d="M619 286
             C566 286 529 316 529 357
             C529 386 548 411 580 422
             L570 443 L642 436 L604 373 L594 395
             C570 388 555 374 555 354
             C555 327 579 309 617 309 Z"
          fill="#1267b2"/>
    <path d="M641 434
             C694 434 731 404 731 363
             C731 334 712 309 680 298
             L690 277 L618 284 L656 347 L666 325
             C690 332 705 346 705 366
             C705 393 681 411 643 411 Z"
          fill="#2c9b45"/>
    <path d="M612 326 L664 326 L664 309 L707 349 L664 389 L664 370 L612 370 Z"
          fill="#ffffff"/>
    <path d="M649 394 L597 394 L597 411 L554 371 L597 331 L597 350 L649 350 Z"
          fill="#ffffff"/>
    <path d="M586 323 L623 323 L623 309 L670 349 L623 389 L623 373 L586 373 Z"
          fill="#2c9b45"/>
    <path d="M674 397 L637 397 L637 411 L590 371 L637 331 L637 347 L674 347 Z"
          fill="#1267b2"/>
  </g>

  <!-- Right-side executive/team image, cropped to the central band -->
  <image x="748" y="274" width="380" height="204"
         href="https://images.example.com/corporate-team-two-executives-transparent-background.png"
         clip-path="url(#peopleCrop)" preserveAspectRatio="xMidYMid meet"/>

  <!-- Small photo grounding shadow inside the white band -->
  <ellipse cx="943" cy="466" rx="170" ry="10" fill="#000000" opacity="0.08"/>
</svg>
```

## Avoid in this skill
- ❌ Do not use `<mask>` to fade or blur the people image; use a clean source photo and crop with `<clipPath>` only.
- ❌ Do not rely on `<pattern>` fills for the blue panels; use solid fills or editable gradients.
- ❌ Do not use `skewX`, `skewY`, or matrix transforms for the diagonal split; draw the angled panels directly as `<path>` polygons.
- ❌ Do not place arrowheads with `marker-end` on logo paths; create arrowheads as explicit editable `<path>` shapes.
- ❌ Do not omit `width` on text elements, or PowerPoint text wrapping will be unpredictable.

## Composition notes
- Keep the white horizontal band about 30% of slide height; it should feel like a calm corporate identity strip cutting through energetic blue panels.
- Place brand copy in the left third, the logo near center, and the people/photo crop in the right third for a balanced left-to-right read.
- The diagonal white split should continue visually through both blue regions, giving the slide motion without disturbing the central content band.
- Use one dominant corporate blue, with small green/blue logo accents to add brand specificity and prevent the slide from feeling monochrome.