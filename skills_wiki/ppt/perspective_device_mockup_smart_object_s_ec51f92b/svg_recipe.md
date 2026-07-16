# SVG Recipe — Perspective Device Mockup (Smart Object Simulation)

## Visual mechanism
Place a product screenshot inside an angled laptop screen by clipping the image to a four-corner screen polygon, then reinforce the “smart object” illusion with perspective-aligned bezel, keyboard base, screen glare, shadows, and vector UI overlays. The device occupies the left two-thirds of the slide while crisp executive messaging sits in the negative space on the right.

## SVG primitives needed
- 2× `<rect>` for full-slide background and desk plane
- 8–12× `<path>` for laptop lid, bezel, screen well, base, keyboard tray, hinge, trackpad, glare, and perspective UI panels
- 1× `<image>` clipped to the angled screen polygon for the inserted product screenshot
- 1× `<clipPath>` with a screen-shaped `<path>` applied only to the screenshot image
- 10–16× small `<path>` elements for keyboard keys and UI cards following the same perspective angle
- 2× `<circle>` or `<ellipse>` for ambient accent glows and soft floor shadow
- 1× `<linearGradient>` for the background, 1× for the desk, 1× for metallic device surfaces, and 1× for the screen/UI accent
- 2× `<filter>` definitions: one soft shadow for device depth, one blur glow for ambient color
- 5–7× `<text>` elements with explicit `width` attributes for title, body, label, and callout metrics

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#F8FAFD"/>
      <stop offset="55%" stop-color="#EEF3F8"/>
      <stop offset="100%" stop-color="#D9E0EA"/>
    </linearGradient>

    <linearGradient id="deskGrad" x1="0" y1="390" x2="0" y2="720" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#EEF2F6"/>
      <stop offset="100%" stop-color="#B8C0CC"/>
    </linearGradient>

    <linearGradient id="metalGrad" x1="180" y1="580" x2="1040" y2="720" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#DDE3EA"/>
      <stop offset="45%" stop-color="#BFC7D1"/>
      <stop offset="100%" stop-color="#EEF2F6"/>
    </linearGradient>

    <linearGradient id="screenGrad" x1="170" y1="145" x2="790" y2="650" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#14213D"/>
      <stop offset="55%" stop-color="#08111F"/>
      <stop offset="100%" stop-color="#03070D"/>
    </linearGradient>

    <radialGradient id="cyanGlow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#00BFFF" stop-opacity="0.42"/>
      <stop offset="100%" stop-color="#00BFFF" stop-opacity="0"/>
    </radialGradient>

    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="18"/>
      <feGaussianBlur stdDeviation="18"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="glowBlur" x="-60%" y="-60%" width="220%" height="220%">
      <feGaussianBlur stdDeviation="28"/>
    </filter>

    <clipPath id="screenClip">
      <path d="M174 146 L781 198 L783 579 L173 648 Z"/>
    </clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>
  <circle cx="735" cy="205" r="190" fill="url(#cyanGlow)" filter="url(#glowBlur)" opacity="0.55"/>
  <rect x="0" y="405" width="1280" height="315" fill="url(#deskGrad)"/>

  <ellipse cx="585" cy="668" rx="480" ry="52" fill="#6D7787" opacity="0.22" filter="url(#softShadow)"/>

  <!-- Laptop lid and bezel -->
  <path d="M132 106 L814 166 C829 167 838 179 838 194 L835 588 C835 604 824 615 808 617 L154 690 C138 692 126 681 126 665 L125 127 C125 114 119 107 132 106 Z"
        fill="#25282D" filter="url(#softShadow)"/>
  <path d="M149 120 L805 178 L806 598 L151 675 Z"
        fill="#34383E" stroke="#B8C0CA" stroke-width="3"/>
  <path d="M166 137 L790 193 L792 586 L166 657 Z"
        fill="#080B10"/>

  <!-- Inserted screenshot: clipped to screen polygon to simulate smart-object replacement -->
  <image href="https://images.example.com/mockups/analytics-dashboard-screenshot-wide.jpg"
         x="150" y="125" width="660" height="540"
         preserveAspectRatio="xMidYMid slice"
         clip-path="url(#screenClip)"
         opacity="0.92"/>

  <!-- Perspective vector UI overlay, aligned to the same screen edges -->
  <path d="M174 146 L781 198 L781 245 L174 192 Z" fill="#071528" opacity="0.94"/>
  <path d="M205 222 L410 240 L410 372 L205 392 Z" fill="#FFFFFF" opacity="0.11"/>
  <path d="M432 243 L746 270 L746 384 L432 370 Z" fill="#00BFFF" opacity="0.16"/>
  <path d="M205 417 L365 403 L365 535 L205 553 Z" fill="#FFFFFF" opacity="0.10"/>
  <path d="M388 401 L548 386 L548 516 L388 534 Z" fill="#FFFFFF" opacity="0.09"/>
  <path d="M572 385 L747 368 L747 503 L572 522 Z" fill="#FFFFFF" opacity="0.10"/>
  <path d="M225 267 C270 238 325 248 352 288 C382 332 344 369 292 362 C242 356 203 314 225 267 Z"
        fill="none" stroke="#35D0FF" stroke-width="9" opacity="0.72"/>
  <path d="M452 309 L512 295 L574 326 L636 285 L718 315"
        fill="none" stroke="#7CF5C7" stroke-width="7" opacity="0.75"/>
  <path d="M225 458 L340 447" stroke="#FFFFFF" stroke-width="8" opacity="0.32"/>
  <path d="M225 490 L326 478" stroke="#00BFFF" stroke-width="6" opacity="0.62"/>
  <path d="M408 442 L525 430" stroke="#FFFFFF" stroke-width="8" opacity="0.30"/>
  <path d="M592 426 L720 412" stroke="#FFFFFF" stroke-width="8" opacity="0.30"/>

  <!-- Glass reflection -->
  <path d="M470 172 L780 199 L780 306 C715 298 641 260 575 219 C532 192 499 181 470 172 Z"
        fill="#FFFFFF" opacity="0.17"/>
  <path d="M174 146 L781 198 L783 579 L173 648 Z"
        fill="none" stroke="#1E2630" stroke-width="4"/>

  <!-- Hinge and laptop base -->
  <path d="M150 665 L807 589 L1084 681 L254 762 L130 704 Z"
        fill="url(#metalGrad)" stroke="#AEB7C2" stroke-width="2"/>
  <path d="M214 674 L758 612 L958 656 L328 732 Z"
        fill="#6D7680" opacity="0.88"/>
  <path d="M462 687 L670 665 L755 687 L536 716 Z"
        fill="#AAB3BE" opacity="0.78"/>
  <path d="M154 650 L807 576 L807 603 L154 679 Z"
        fill="#15181C"/>

  <!-- Perspective keyboard keys -->
  <path d="M253 684 L304 678 L324 684 L272 691 Z" fill="#DCE2E8" opacity="0.48"/>
  <path d="M325 676 L376 670 L398 676 L345 683 Z" fill="#DCE2E8" opacity="0.48"/>
  <path d="M399 668 L454 662 L477 668 L420 675 Z" fill="#DCE2E8" opacity="0.48"/>
  <path d="M479 660 L538 653 L562 660 L501 668 Z" fill="#DCE2E8" opacity="0.48"/>
  <path d="M562 651 L625 644 L651 651 L586 659 Z" fill="#DCE2E8" opacity="0.48"/>
  <path d="M648 642 L713 635 L742 642 L674 651 Z" fill="#DCE2E8" opacity="0.48"/>
  <path d="M302 704 L369 696 L393 703 L324 712 Z" fill="#DCE2E8" opacity="0.38"/>
  <path d="M395 693 L468 684 L494 692 L419 702 Z" fill="#DCE2E8" opacity="0.38"/>
  <path d="M498 681 L584 671 L612 679 L524 690 Z" fill="#DCE2E8" opacity="0.38"/>
  <path d="M618 667 L704 657 L736 666 L646 678 Z" fill="#DCE2E8" opacity="0.38"/>

  <!-- Right-side editorial content -->
  <text x="900" y="132" width="270" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="14" font-weight="700" letter-spacing="2.5" fill="#00A7D9">PRODUCT EXPERIENCE</text>

  <text x="898" y="205" width="320" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="48" font-weight="750" fill="#172033">
    <tspan x="898" dy="0">Digital</tspan>
    <tspan x="898" dy="58" fill="#00A7D9">Ecosystem</tspan>
  </text>

  <text x="902" y="333" width="300" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="19" fill="#5A6472">
    Seamlessly deploy responsive analytics, workflows, and customer experiences across every platform.
  </text>

  <path d="M902 400 L1178 400" stroke="#B9C3D0" stroke-width="2" stroke-dasharray="7 9"/>
  <circle cx="924" cy="458" r="23" fill="#00BFFF" opacity="0.16"/>
  <text x="956" y="466" width="235" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="18" font-weight="650" fill="#202B3A">Perspective-ready mockup</text>

  <circle cx="924" cy="520" r="23" fill="#7CF5C7" opacity="0.18"/>
  <text x="956" y="528" width="235" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="18" font-weight="650" fill="#202B3A">Editable vector device frame</text>

  <path d="M900 592 C900 578 911 567 925 567 L1144 567 C1158 567 1169 578 1169 592 L1169 634 C1169 648 1158 659 1144 659 L925 659 C911 659 900 648 900 634 Z"
        fill="#172033"/>
  <text x="929" y="624" width="220" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="17" font-weight="700" fill="#FFFFFF">Launch demo preview</text>
</svg>
```

## Avoid in this skill
- ❌ `transform="skewX(...)"`, `skewY(...)`, or `matrix(...)` for the screen image; these are not reliably preserved.
- ❌ Applying `clip-path` to a `<g>`, `<rect>`, or `<path>` to crop UI elements; clipping is only safe on `<image>`.
- ❌ Expecting the clipped screenshot to be mathematically perspective-warped. For true homography, pre-render the screenshot as a perspective raster, then place it inside the screen clip.
- ❌ Using `<mask>` for screen reflections or rounded crops; use translucent `<path>` overlays and image clipPaths instead.
- ❌ Putting shadows on `<line>` elements; use `<path>` strokes or filled shapes if the element needs a filter.

## Composition notes
- Keep the laptop large, usually spanning x≈120–850, with its base bleeding slightly below the slide for a premium cropped-product feel.
- Use the right 30% of the slide for title and value proposition; avoid crowding the device with text.
- Make every visible edge of the screen, UI cards, keyboard, and base share the same perspective rhythm so the flat screenshot feels embedded.
- Add a subtle glass glare and ambient cyan glow sparingly; the effect should read as polished hardware, not sci-fi neon.