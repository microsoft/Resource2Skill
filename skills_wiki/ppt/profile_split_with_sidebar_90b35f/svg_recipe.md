# SVG Recipe — Profile Split with Sidebar

## Visual mechanism
A bold editorial profile cover built from three vertical zones: a dark role sidebar, oversized staggered name typography in the center, and a tall clipped portrait card on the right. The technique relies on strong column tension, restrained accent color, and a premium photo crop to make a personal brand slide feel keynote-ready.

## SVG primitives needed
- 4× `<rect>` for full-slide background, left sidebar, central content backing, and portrait frame/shadow planes
- 1× `<image>` clipped to a rounded vertical card for the 9:16 profile photo
- 1× `<clipPath>` with rounded `<rect>` for the portrait crop
- 4× `<path>` for decorative editorial shapes: oversized soft blob, angled accent ribbon, sidebar notch, and subtle background contour
- 2× `<linearGradient>` for background depth and sidebar sheen
- 1× `<radialGradient>` for a warm glow behind the name/photo seam
- 2× `<filter>` definitions: one drop shadow for cards and one soft blur glow for decorative shapes
- 5× `<line>` for sidebar separators and small typographic rules
- 12× `<text>` elements for name, role stack, bio, labels, and rotated sidebar wordmark

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1280" y2="720">
      <stop offset="0" stop-color="#F7F2EA"/>
      <stop offset="0.55" stop-color="#EFE6D8"/>
      <stop offset="1" stop-color="#E3D4C0"/>
    </linearGradient>

    <linearGradient id="sidebarGrad" x1="0" y1="0" x2="260" y2="720">
      <stop offset="0" stop-color="#111827"/>
      <stop offset="0.55" stop-color="#172033"/>
      <stop offset="1" stop-color="#0B1020"/>
    </linearGradient>

    <radialGradient id="warmGlow" cx="50%" cy="48%" r="60%">
      <stop offset="0" stop-color="#DFA35D" stop-opacity="0.45"/>
      <stop offset="0.55" stop-color="#DFA35D" stop-opacity="0.12"/>
      <stop offset="1" stop-color="#DFA35D" stop-opacity="0"/>
    </radialGradient>

    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feOffset dx="0" dy="18"/>
      <feGaussianBlur stdDeviation="18"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="blurGlow" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="28"/>
    </filter>

    <clipPath id="portraitClip">
      <rect x="876" y="72" width="292" height="576" rx="34" ry="34"/>
    </clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>
  <path d="M648,40 C760,62 810,154 795,258 C778,374 869,452 828,560 C782,681 582,692 497,604 C421,526 451,395 392,318 C323,229 424,72 648,40 Z"
        fill="url(#warmGlow)" filter="url(#blurGlow)"/>

  <rect x="0" y="0" width="246" height="720" fill="url(#sidebarGrad)"/>
  <path d="M246,0 L304,0 C272,92 272,184 304,276 C333,360 320,455 276,551 C256,594 248,651 246,720 Z"
        fill="#111827" opacity="0.92"/>
  <path d="M0,468 C68,440 137,452 246,398 L246,720 L0,720 Z"
        fill="#DFA35D" opacity="0.11"/>

  <line x1="62" y1="116" x2="184" y2="116" stroke="#DFA35D" stroke-width="3"/>
  <line x1="62" y1="584" x2="184" y2="584" stroke="#DFA35D" stroke-width="3"/>
  <text x="64" y="78" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" letter-spacing="3" fill="#DFA35D">PROFILE</text>
  <text x="76" y="548" width="230" transform="rotate(-90 76 548)"
        font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="800" letter-spacing="5" fill="#F7F2EA">EXECUTIVE BIO</text>

  <text x="62" y="170" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#F7F2EA">PRIMARY ROLE</text>
  <text x="62" y="204" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="22" font-weight="800" fill="#FFFFFF">Chief Strategy Officer</text>
  <line x1="62" y1="246" x2="162" y2="246" stroke="#FFFFFF" stroke-opacity="0.25" stroke-width="1"/>

  <text x="62" y="290" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" letter-spacing="1.5" fill="#DFA35D">ALSO KNOWN FOR</text>
  <text x="62" y="326" width="155" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#D7DCE8">Board advisor</text>
  <text x="62" y="354" width="155" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#D7DCE8">Growth architect</text>
  <text x="62" y="382" width="155" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#D7DCE8">M&A operator</text>
  <text x="62" y="410" width="155" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#D7DCE8">AI transformation lead</text>

  <rect x="302" y="86" width="520" height="548" rx="42" fill="#F9F5ED" opacity="0.55"/>
  <path d="M312,128 C423,97 514,109 585,157 C666,212 687,291 753,334 C805,369 821,445 778,500 C724,569 621,542 546,588 C456,644 338,608 314,512 C292,424 353,359 326,292 C304,235 248,166 312,128 Z"
        fill="#FFFFFF" opacity="0.28"/>

  <text x="328" y="184" width="500" font-family="Segoe UI, Microsoft YaHei" font-size="104" font-weight="800" letter-spacing="-5" fill="#151A24">Maya</text>
  <text x="392" y="292" width="510" font-family="Segoe UI, Microsoft YaHei" font-size="112" font-weight="800" letter-spacing="-6" fill="#151A24">Chen</text>
  <line x1="330" y1="328" x2="448" y2="328" stroke="#DFA35D" stroke-width="5"/>
  <line x1="466" y1="328" x2="538" y2="328" stroke="#151A24" stroke-opacity="0.18" stroke-width="5"/>

  <text x="330" y="384" width="430" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" letter-spacing="2" fill="#9A6B2E">LEADERSHIP PROFILE</text>
  <text x="330" y="428" width="445" font-family="Segoe UI, Microsoft YaHei" font-size="24" font-weight="650" fill="#222936">
    Builds category-defining businesses at the intersection of strategy, capital, and product.
  </text>
  <text x="330" y="502" width="430" font-family="Segoe UI, Microsoft YaHei" font-size="17" fill="#5E6470">
    Known for translating ambiguous markets into investable narratives, aligning executive teams, and scaling operating systems from first traction to global expansion.
  </text>

  <path d="M802,104 L904,72 L904,648 L802,616 Z" fill="#DFA35D" opacity="0.22"/>
  <rect x="858" y="92" width="328" height="576" rx="38" fill="#111827" opacity="0.18" filter="url(#softShadow)"/>
  <rect x="876" y="72" width="292" height="576" rx="34" fill="#FFFFFF" filter="url(#softShadow)"/>
  <image x="876" y="72" width="292" height="576" clip-path="url(#portraitClip)" preserveAspectRatio="xMidYMid slice"
         href="https://images.example.com/editorial-portrait-confident-executive-woman-warm-studio-lighting.jpg"/>
  <rect x="876" y="72" width="292" height="576" rx="34" fill="none" stroke="#FFFFFF" stroke-width="8"/>
  <path d="M876,482 C940,454 1024,472 1168,414 L1168,648 L876,648 Z" fill="#0B1020" opacity="0.26"/>

  <text x="914" y="610" width="210" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="800" letter-spacing="2" fill="#FFFFFF">GLOBAL GROWTH · AI · CAPITAL</text>
</svg>
```

## Avoid in this skill
- ❌ Do not use `<mask>` to fade or darken the portrait; use a clipped `<image>` plus editable translucent `<rect>` or `<path>` overlays instead.
- ❌ Do not use `<textPath>` for the vertical sidebar label; rotate a normal `<text>` element so it remains editable.
- ❌ Do not apply filters to `<line>` separators; filter support on lines is dropped, so keep rules crisp and unfiltered.
- ❌ Do not build the portrait from repeated rectangles or placeholder silhouettes; this layout depends on a real editorial photo crop.
- ❌ Do not center all typography in a grid; the name should be staggered and slightly offset to create magazine-cover energy.

## Composition notes
- Keep the sidebar around 18–22% of slide width, the name/bio column around 40–45%, and the portrait card around 23–28%.
- The visual focus should jump from the oversized name to the portrait; sidebar content is supporting metadata.
- Use one warm accent color repeatedly in thin rules, labels, and translucent shapes to unify the dark sidebar with the light editorial center.
- Preserve generous negative space around the bio; the profile should feel premium, not like a résumé page.