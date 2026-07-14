# SVG Recipe — Straddling Profile Tooltips

## Visual mechanism
Circular profile photos sit exactly on the boundary between a saturated dark header and a pale content panel, creating a high-contrast “straddle” focal line. Each avatar is anchored by a glossy tooltip ribbon with a small pointer, shadow, and editable name text, followed by short bio copy underneath.

## SVG primitives needed
- 2× `<rect>` for the white canvas/pale lower panel and dark upper header band
- 1× `<linearGradient id="headerGrad">` for the royal-purple header background
- 1× `<linearGradient id="ribbonGrad">` for glossy purple tooltip ribbons
- 2× `<filter>` for soft shadows on avatars and tooltip ribbons
- 3× `<clipPath>` with `<circle>` for circular avatar image crops
- 3× `<image>` for editable circular-cropped profile photos
- 6× `<circle>` per avatar group for avatar shadow, white ring, purple accent ring, and decorative dots
- 3× `<path>` for custom tooltip ribbon shapes with a centered downward pointer
- 2× `<line>` plus 2× small `<circle>` for the title divider ornament
- Multiple `<text>` elements with explicit `width` for title, names, and bios

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="headerGrad" x1="0" y1="78" x2="0" y2="328" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#5C0A8D"/>
      <stop offset="0.55" stop-color="#31045F"/>
      <stop offset="1" stop-color="#130041"/>
    </linearGradient>

    <linearGradient id="ribbonGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#7022B7"/>
      <stop offset="0.48" stop-color="#4D078A"/>
      <stop offset="1" stop-color="#1F004E"/>
    </linearGradient>

    <filter id="avatarShadow" x="-25%" y="-25%" width="150%" height="150%">
      <feOffset dx="6" dy="8" in="SourceAlpha" result="off"/>
      <feGaussianBlur in="off" stdDeviation="5" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="ribbonShadow" x="-25%" y="-35%" width="150%" height="180%">
      <feOffset dx="4" dy="8" in="SourceAlpha" result="off"/>
      <feGaussianBlur in="off" stdDeviation="5" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <clipPath id="clipA"><circle cx="296" cy="326" r="82"/></clipPath>
    <clipPath id="clipB"><circle cx="640" cy="326" r="82"/></clipPath>
    <clipPath id="clipC"><circle cx="984" cy="326" r="82"/></clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#FFFFFF"/>
  <rect x="118" y="55" width="1044" height="603" fill="#EDEDED"/>
  <rect x="0" y="78" width="1280" height="249" fill="url(#headerGrad)"/>

  <line x1="0" y1="163" x2="410" y2="161" stroke="#FFFFFF" stroke-width="1.2" opacity="0.85"/>
  <circle cx="410" cy="161" r="4.5" fill="#FFFFFF"/>
  <line x1="870" y1="161" x2="1280" y2="163" stroke="#FFFFFF" stroke-width="1.2" opacity="0.85"/>
  <circle cx="870" cy="161" r="4.5" fill="#FFFFFF"/>

  <text x="490" y="178" width="300" font-family="Georgia, 'Times New Roman', serif" font-size="56" font-weight="700" fill="#FFFFFF" text-anchor="middle">
    <tspan x="640">Our Team</tspan>
  </text>

  <!-- Profile 1 avatar -->
  <circle cx="296" cy="326" r="101" fill="#000000" opacity="0.35" filter="url(#avatarShadow)"/>
  <circle cx="296" cy="326" r="101" fill="#FFFFFF"/>
  <circle cx="296" cy="326" r="92" fill="none" stroke="#4B0785" stroke-width="7"/>
  <image href="https://images.example.com/team/member-1-professional-portrait.jpg" x="214" y="244" width="164" height="164" clip-path="url(#clipA)" preserveAspectRatio="xMidYMid slice"/>
  <circle cx="296" cy="326" r="82" fill="none" stroke="#FFFFFF" stroke-width="3"/>

  <path d="M214 411 L378 411 Q393 411 393 427 Q393 445 376 445 L326 445 Q309 445 301 462 L296 481 L291 462 Q283 445 266 445 L216 445 Q197 445 197 427 Q197 411 214 411 Z"
        fill="url(#ribbonGrad)" filter="url(#ribbonShadow)"/>
  <path d="M217 412 L375 412 Q390 412 392 425 L199 425 Q202 412 217 412 Z" fill="#8D46CE" opacity="0.38"/>
  <text x="197" y="431" width="196" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="16" font-weight="700" fill="#FFFFFF" text-anchor="middle">
    <tspan x="295">NAME HERE</tspan>
  </text>
  <text x="187" y="527" width="220" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="16" font-weight="700" fill="#111111">
    <tspan x="187">Lorem ipsum dolor sit amet</tspan>
  </text>
  <text x="190" y="550" width="215" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="16" fill="#111111">
    <tspan x="190">Lorem ipsum dolor sit amet</tspan>
  </text>
  <circle cx="278" cy="589" r="5" fill="none" stroke="#3B006D" stroke-width="2"/>
  <circle cx="296" cy="589" r="5" fill="none" stroke="#3B006D" stroke-width="2"/>
  <circle cx="314" cy="589" r="5" fill="none" stroke="#3B006D" stroke-width="2"/>

  <!-- Profile 2 avatar -->
  <circle cx="640" cy="326" r="101" fill="#000000" opacity="0.35" filter="url(#avatarShadow)"/>
  <circle cx="640" cy="326" r="101" fill="#FFFFFF"/>
  <circle cx="640" cy="326" r="92" fill="none" stroke="#4B0785" stroke-width="7"/>
  <image href="https://images.example.com/team/member-2-professional-portrait.jpg" x="558" y="244" width="164" height="164" clip-path="url(#clipB)" preserveAspectRatio="xMidYMid slice"/>
  <circle cx="640" cy="326" r="82" fill="none" stroke="#FFFFFF" stroke-width="3"/>

  <path d="M558 411 L722 411 Q737 411 737 427 Q737 445 720 445 L670 445 Q653 445 645 462 L640 481 L635 462 Q627 445 610 445 L560 445 Q541 445 541 427 Q541 411 558 411 Z"
        fill="url(#ribbonGrad)" filter="url(#ribbonShadow)"/>
  <path d="M561 412 L719 412 Q734 412 736 425 L543 425 Q546 412 561 412 Z" fill="#8D46CE" opacity="0.38"/>
  <text x="541" y="431" width="196" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="16" font-weight="700" fill="#FFFFFF" text-anchor="middle">
    <tspan x="639">NAME HERE</tspan>
  </text>
  <text x="532" y="527" width="220" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="16" font-weight="700" fill="#111111">
    <tspan x="532">Lorem ipsum dolor sit amet</tspan>
  </text>
  <text x="536" y="550" width="215" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="16" fill="#111111">
    <tspan x="536">Lorem ipsum dolor sit amet</tspan>
  </text>
  <circle cx="623" cy="589" r="5" fill="none" stroke="#3B006D" stroke-width="2"/>
  <circle cx="641" cy="589" r="5" fill="none" stroke="#3B006D" stroke-width="2"/>
  <circle cx="659" cy="589" r="5" fill="none" stroke="#3B006D" stroke-width="2"/>

  <!-- Profile 3 avatar -->
  <circle cx="984" cy="326" r="101" fill="#000000" opacity="0.35" filter="url(#avatarShadow)"/>
  <circle cx="984" cy="326" r="101" fill="#FFFFFF"/>
  <circle cx="984" cy="326" r="92" fill="none" stroke="#4B0785" stroke-width="7"/>
  <image href="https://images.example.com/team/member-3-professional-portrait.jpg" x="902" y="244" width="164" height="164" clip-path="url(#clipC)" preserveAspectRatio="xMidYMid slice"/>
  <circle cx="984" cy="326" r="82" fill="none" stroke="#FFFFFF" stroke-width="3"/>

  <path d="M902 411 L1066 411 Q1081 411 1081 427 Q1081 445 1064 445 L1014 445 Q997 445 989 462 L984 481 L979 462 Q971 445 954 445 L904 445 Q885 445 885 427 Q885 411 902 411 Z"
        fill="url(#ribbonGrad)" filter="url(#ribbonShadow)"/>
  <path d="M905 412 L1063 412 Q1078 412 1080 425 L887 425 Q890 412 905 412 Z" fill="#8D46CE" opacity="0.38"/>
  <text x="885" y="431" width="196" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="16" font-weight="700" fill="#FFFFFF" text-anchor="middle">
    <tspan x="983">NAME HERE</tspan>
  </text>
  <text x="878" y="527" width="220" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="16" font-weight="700" fill="#111111">
    <tspan x="878">Lorem ipsum dolor sit amet</tspan>
  </text>
  <text x="882" y="550" width="215" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="16" fill="#111111">
    <tspan x="882">Lorem ipsum dolor sit amet</tspan>
  </text>
  <circle cx="968" cy="589" r="5" fill="none" stroke="#3B006D" stroke-width="2"/>
  <circle cx="986" cy="589" r="5" fill="none" stroke="#3B006D" stroke-width="2"/>
  <circle cx="1004" cy="589" r="5" fill="none" stroke="#3B006D" stroke-width="2"/>
</svg>
```

## Avoid in this skill
- ❌ Applying `clip-path` to grouped avatar shapes; only clip the `<image>` and build rings/shadows as separate editable circles.
- ❌ Using `<mask>` to create circular photos or tooltip notches; masks are fragile in PPT translation.
- ❌ Putting the avatar fully inside either the header or lower panel; the visual effect depends on the circles straddling the color boundary.
- ❌ Overloading bios with long paragraphs; the tooltip/avatar stack needs generous negative space below.

## Composition notes
- Keep the dark header around 35–40% of slide height, with the avatar centers placed directly on the header/lower-panel boundary.
- Use three or four equal columns; center-align each avatar, ribbon, bio block, and dot ornament on the same vertical axis.
- Maintain strong contrast: white title/rings on purple, dark body text on pale gray, and purple ribbons as the bridge between zones.
- Shadows should be soft and offset downward/right to make the avatars and ribbons feel like layered UI cards.