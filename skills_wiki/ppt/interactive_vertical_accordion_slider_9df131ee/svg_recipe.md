# SVG Recipe — Interactive Vertical Accordion Slider

## Visual mechanism
A single expanded portrait card dominates the row while peer items remain visible as narrow vertical photo slices. The contrast between full-width active content and compressed inactive strips creates an app-like accordion state that can be duplicated across slides and animated with PowerPoint Morph.

## SVG primitives needed
- 1× `<rect>` full-slide background with a soft vertical gradient.
- 2× large blurred `<ellipse>` shapes for premium ambient color glow.
- 7× shadow `<rect>` shapes behind the accordion cards.
- 7× `<clipPath>` definitions using rounded `<rect>` crops, applied only to `<image>` elements.
- 7× `<image>` elements for team portraits: 1 active wide crop and 6 inactive vertical strip crops.
- 1× active-card gradient overlay `<rect>` for white text readability.
- 6× inactive-card translucent dark overlay `<rect>` shapes to unify narrow strips.
- Multiple `<text>` elements with explicit `width` attributes: slide title, subtitle, active name/role/bio, and rotated inactive labels.
- 1× accent `<line>` beside the active biography.
- 1× small accent `<circle>` and several small `<rect>` UI chips to suggest current accordion state.
- 1× `<filter id="softShadow">` using offset/blur/merge for card shadows.
- 1× `<filter id="glowBlur">` using Gaussian blur for background glow ellipses.
- 3× `<linearGradient>` definitions for background, active overlay, and subtle strip overlay.

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="0" y2="720">
      <stop offset="0%" stop-color="#F7FAFD"/>
      <stop offset="55%" stop-color="#EEF3F8"/>
      <stop offset="100%" stop-color="#DDE5EE"/>
    </linearGradient>

    <linearGradient id="activeOverlay" x1="0" y1="250" x2="0" y2="610" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#000000" stop-opacity="0"/>
      <stop offset="55%" stop-color="#000000" stop-opacity="0.25"/>
      <stop offset="100%" stop-color="#000000" stop-opacity="0.78"/>
    </linearGradient>

    <linearGradient id="stripOverlay" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#101820" stop-opacity="0.05"/>
      <stop offset="100%" stop-color="#101820" stop-opacity="0.62"/>
    </linearGradient>

    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="18"/>
      <feGaussianBlur stdDeviation="18"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="glowBlur" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="36"/>
    </filter>

    <clipPath id="clipEva"><rect x="78" y="150" width="82" height="448" rx="28"/></clipPath>
    <clipPath id="clipJacob"><rect x="182" y="150" width="82" height="448" rx="28"/></clipPath>
    <clipPath id="clipEmily"><rect x="286" y="150" width="82" height="448" rx="28"/></clipPath>
    <clipPath id="clipSarah"><rect x="392" y="96" width="430" height="556" rx="36"/></clipPath>
    <clipPath id="clipLauren"><rect x="846" y="150" width="82" height="448" rx="28"/></clipPath>
    <clipPath id="clipMike"><rect x="950" y="150" width="82" height="448" rx="28"/></clipPath>
    <clipPath id="clipAngie"><rect x="1054" y="150" width="82" height="448" rx="28"/></clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>
  <ellipse cx="1090" cy="88" rx="210" ry="92" fill="#FFD76A" opacity="0.20" filter="url(#glowBlur)"/>
  <ellipse cx="166" cy="652" rx="260" ry="96" fill="#7AB8FF" opacity="0.18" filter="url(#glowBlur)"/>

  <text x="76" y="62" width="430" font-family="Segoe UI, Microsoft YaHei" font-size="42" font-weight="800" fill="#202834">Our Team</text>
  <text x="78" y="96" width="520" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="500" fill="#687384" letter-spacing="1.8">
    CLICK THROUGH EACH LEADER WITH A MORPH ACCORDION STATE
  </text>

  <rect x="78" y="150" width="82" height="448" rx="28" fill="#263241" opacity="0.20" filter="url(#softShadow)"/>
  <image x="38" y="150" width="162" height="448" href="https://picsum.photos/seed/eva-team-portrait/500/900" clip-path="url(#clipEva)" preserveAspectRatio="xMidYMid slice"/>
  <rect x="78" y="150" width="82" height="448" rx="28" fill="url(#stripOverlay)"/>
  <text x="118" y="552" width="230" transform="rotate(-90 118 552)" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="800" fill="#FFFFFF" letter-spacing="3">EVA · FINANCE</text>

  <rect x="182" y="150" width="82" height="448" rx="28" fill="#263241" opacity="0.20" filter="url(#softShadow)"/>
  <image x="142" y="150" width="162" height="448" href="https://picsum.photos/seed/jacob-team-portrait/500/900" clip-path="url(#clipJacob)" preserveAspectRatio="xMidYMid slice"/>
  <rect x="182" y="150" width="82" height="448" rx="28" fill="url(#stripOverlay)"/>
  <text x="222" y="552" width="230" transform="rotate(-90 222 552)" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="800" fill="#FFFFFF" letter-spacing="3">JACOB · ADMIN</text>

  <rect x="286" y="150" width="82" height="448" rx="28" fill="#263241" opacity="0.20" filter="url(#softShadow)"/>
  <image x="246" y="150" width="162" height="448" href="https://picsum.photos/seed/emily-team-portrait/500/900" clip-path="url(#clipEmily)" preserveAspectRatio="xMidYMid slice"/>
  <rect x="286" y="150" width="82" height="448" rx="28" fill="url(#stripOverlay)"/>
  <text x="326" y="552" width="260" transform="rotate(-90 326 552)" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="800" fill="#FFFFFF" letter-spacing="3">EMILY · OPS</text>

  <rect x="392" y="96" width="430" height="556" rx="36" fill="#263241" opacity="0.22" filter="url(#softShadow)"/>
  <image x="392" y="96" width="430" height="556" href="https://picsum.photos/seed/sarah-manager-portrait/900/1100" clip-path="url(#clipSarah)" preserveAspectRatio="xMidYMid slice"/>
  <rect x="392" y="96" width="430" height="556" rx="36" fill="url(#activeOverlay)"/>
  <circle cx="432" cy="134" r="8" fill="#FFD45A"/>
  <text x="432" y="484" width="330" font-family="Segoe UI, Microsoft YaHei" font-size="58" font-weight="900" fill="#FFFFFF">Sarah</text>
  <text x="436" y="522" width="260" font-family="Segoe UI, Microsoft YaHei" font-size="19" font-weight="700" fill="#FFD45A" letter-spacing="2">GENERAL MANAGER</text>
  <line x1="438" y1="548" x2="438" y2="614" stroke="#FFD45A" stroke-width="4"/>
  <text x="458" y="562" width="310" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="500" fill="#FFFFFF" opacity="0.92">
    Leads cross-functional delivery with a calm operating rhythm and a bias for fast decisions.
  </text>

  <rect x="846" y="150" width="82" height="448" rx="28" fill="#263241" opacity="0.20" filter="url(#softShadow)"/>
  <image x="806" y="150" width="162" height="448" href="https://picsum.photos/seed/lauren-team-portrait/500/900" clip-path="url(#clipLauren)" preserveAspectRatio="xMidYMid slice"/>
  <rect x="846" y="150" width="82" height="448" rx="28" fill="url(#stripOverlay)"/>
  <text x="886" y="552" width="250" transform="rotate(-90 886 552)" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="800" fill="#FFFFFF" letter-spacing="3">LAUREN · DESIGN</text>

  <rect x="950" y="150" width="82" height="448" rx="28" fill="#263241" opacity="0.20" filter="url(#softShadow)"/>
  <image x="910" y="150" width="162" height="448" href="https://picsum.photos/seed/mike-team-portrait/500/900" clip-path="url(#clipMike)" preserveAspectRatio="xMidYMid slice"/>
  <rect x="950" y="150" width="82" height="448" rx="28" fill="url(#stripOverlay)"/>
  <text x="990" y="552" width="260" transform="rotate(-90 990 552)" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="800" fill="#FFFFFF" letter-spacing="3">MIKE · DEV</text>

  <rect x="1054" y="150" width="82" height="448" rx="28" fill="#263241" opacity="0.20" filter="url(#softShadow)"/>
  <image x="1014" y="150" width="162" height="448" href="https://picsum.photos/seed/angie-team-portrait/500/900" clip-path="url(#clipAngie)" preserveAspectRatio="xMidYMid slice"/>
  <rect x="1054" y="150" width="82" height="448" rx="28" fill="url(#stripOverlay)"/>
  <text x="1094" y="552" width="230" transform="rotate(-90 1094 552)" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="800" fill="#FFFFFF" letter-spacing="3">ANGIE · HR</text>

  <rect x="1154" y="244" width="6" height="38" rx="3" fill="#CBD5E1"/>
  <rect x="1154" y="292" width="6" height="38" rx="3" fill="#CBD5E1"/>
  <rect x="1154" y="340" width="6" height="72" rx="3" fill="#FFD45A"/>
  <rect x="1154" y="422" width="6" height="38" rx="3" fill="#CBD5E1"/>
</svg>
```

## Avoid in this skill
- ❌ Do not use SVG `<animate>` or `<animateTransform>` for the accordion movement; create separate slide states and let PowerPoint Morph interpolate them.
- ❌ Do not apply `clip-path` to overlay rectangles or text; only the portrait `<image>` elements should receive clipping.
- ❌ Do not use `<foreignObject>` for vertical labels; rotate native `<text>` elements instead.
- ❌ Do not use `<use>` or `<symbol>` to duplicate the inactive strips; repeat the shapes explicitly so PowerPoint keeps everything editable.
- ❌ Do not put filters on `<line>` elements; use shadow rectangles behind cards instead.

## Composition notes
- Keep the accordion row horizontally centered and give all cards a shared vertical centerline; the active card may be taller, but it should still feel locked to the same carousel rail.
- The active panel should consume roughly 40–45% of the visual row width; inactive strips should remain narrow enough to read as context rather than equal competitors.
- Put the active name and role inside the lower third of the expanded image with a dark gradient overlay for contrast.
- To build the interactive sequence, duplicate the slide, move the wide clip/image/text treatment to a different person, compress the previous active card into a strip, and apply PowerPoint Morph between slides.