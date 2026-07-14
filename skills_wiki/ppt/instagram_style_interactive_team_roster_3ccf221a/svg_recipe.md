# SVG Recipe — Instagram-Style Interactive Team Roster

## Visual mechanism
A corporate team roster is styled like an Instagram interface: circular “Story” avatars across the top act as interactive selectors, while the active teammate expands into a shadowed feed-style profile card with a large portrait and bold bio typography. A vibrant orange–pink–purple gradient ring marks the selected person, creating familiar social-media navigation and immediate visual focus.

## SVG primitives needed
- 1× `<rect>` for the light gray app-canvas background
- 1× `<linearGradient>` for Instagram-style active story rings
- 1× `<linearGradient>` for a subtle blue/cyan backdrop accent
- 1× `<filter id="softShadow">` for the main white card depth
- 1× `<filter id="avatarShadow">` for the enlarged active avatar bubble
- 6× `<clipPath>` with circles/rounded rects for editable circular avatar crops and portrait crop
- 5× `<image>` for circular teammate avatars
- 1× `<image>` for the selected teammate portrait inside the card
- 5× gradient/gray stroked `<circle>` elements for story rings
- Multiple `<rect>` elements for white cards, sidebar rail, feed header, text panels, and highlight pills
- Multiple `<path>` elements for simple Instagram-like navigation icons and a cursor pointer
- Multiple `<text>` elements with explicit `width` attributes for title, usernames, name, role, stats, and bio copy

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgWash" x1="0" y1="720" x2="1280" y2="0">
      <stop offset="0%" stop-color="#12D8D8"/>
      <stop offset="38%" stop-color="#F2F2F2"/>
      <stop offset="100%" stop-color="#F2F2F2"/>
    </linearGradient>
    <linearGradient id="instaRing" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#F58529"/>
      <stop offset="48%" stop-color="#DD2A7B"/>
      <stop offset="100%" stop-color="#8134AF"/>
    </linearGradient>
    <filter id="softShadow" x="-30%" y="-30%" width="160%" height="170%">
      <feOffset dx="0" dy="18"/>
      <feGaussianBlur stdDeviation="22"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="avatarShadow" x="-40%" y="-40%" width="180%" height="180%">
      <feOffset dx="0" dy="12"/>
      <feGaussianBlur stdDeviation="16"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <clipPath id="avatarAurora" clipPathUnits="userSpaceOnUse"><circle cx="278" cy="184" r="31"/></clipPath>
    <clipPath id="avatarDraven" clipPathUnits="userSpaceOnUse"><circle cx="402" cy="184" r="31"/></clipPath>
    <clipPath id="avatarMax" clipPathUnits="userSpaceOnUse"><circle cx="526" cy="184" r="31"/></clipPath>
    <clipPath id="avatarZoe" clipPathUnits="userSpaceOnUse"><circle cx="650" cy="184" r="31"/></clipPath>
    <clipPath id="avatarNoor" clipPathUnits="userSpaceOnUse"><circle cx="774" cy="184" r="31"/></clipPath>
    <clipPath id="portraitCrop" clipPathUnits="userSpaceOnUse"><rect x="210" y="325" width="295" height="318" rx="22"/></clipPath>
    <clipPath id="heroBubbleCrop" clipPathUnits="userSpaceOnUse"><circle cx="860" cy="405" r="88"/></clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgWash)"/>
  <text x="164" y="128" width="980" font-family="Segoe UI" font-size="118" font-weight="900" letter-spacing="8" fill="#FFFFFF" filter="url(#softShadow)">CREATIVE</text>
  <text x="72" y="246" width="1120" font-family="Segoe UI" font-size="82" font-weight="900" letter-spacing="9" fill="#FF514B" filter="url(#softShadow)">TEAM SLIDES</text>

  <g transform="rotate(-3 630 465)">
    <rect x="48" y="260" width="790" height="455" rx="0" fill="#FFFFFF" filter="url(#softShadow)"/>
    <rect x="48" y="260" width="108" height="455" fill="#FFFFFF"/>
    <text x="70" y="324" width="90" font-family="Segoe UI" font-size="28" font-weight="800" fill="#111111">Our Team</text>

    <path d="M82 379 L92 369 L102 379 L102 393 L86 393 L86 382 L82 382 Z" fill="none" stroke="#222" stroke-width="2.2" stroke-linejoin="round"/>
    <circle cx="92" cy="430" r="8" fill="none" stroke="#222" stroke-width="2.2"/><line x1="98" y1="436" x2="106" y2="444" stroke="#222" stroke-width="2.2"/>
    <circle cx="92" cy="474" r="8" fill="none" stroke="#222" stroke-width="2.2"/><path d="M89 476 L96 470" fill="none" stroke="#222" stroke-width="2.2"/>
    <rect x="84" y="506" width="16" height="16" rx="4" fill="none" stroke="#222" stroke-width="2.2"/><path d="M87 509 L97 519 M97 509 L87 519" stroke="#222" stroke-width="1.8"/>
    <path d="M84 557 C86 548 98 548 101 556 C104 566 92 572 92 572 C92 572 80 566 84 557 Z" fill="none" stroke="#222" stroke-width="2.2"/>
    <circle cx="105" cy="552" r="3.5" fill="#FF4B55"/>
    <rect x="84" y="613" width="17" height="17" rx="4" fill="none" stroke="#222" stroke-width="2.2"/><line x1="92.5" y1="617" x2="92.5" y2="626" stroke="#222" stroke-width="1.8"/><line x1="88" y1="621.5" x2="97" y2="621.5" stroke="#222" stroke-width="1.8"/>

    <circle cx="278" cy="184" r="39" fill="none" stroke="#C8C8C8" stroke-width="4"/>
    <image href="https://images.example.com/team/aurora-curly-hair-avatar.jpg" x="247" y="153" width="62" height="62" clip-path="url(#avatarAurora)"/>
    <text x="240" y="236" width="80" font-family="Segoe UI" font-size="13" text-anchor="middle" fill="#111">Aurora</text>

    <circle cx="402" cy="184" r="41" fill="none" stroke="url(#instaRing)" stroke-width="5"/>
    <image href="https://images.example.com/team/draven-soft-portrait-avatar.jpg" x="371" y="153" width="62" height="62" clip-path="url(#avatarDraven)"/>
    <text x="364" y="236" width="80" font-family="Segoe UI" font-size="13" text-anchor="middle" fill="#111">Draven</text>

    <circle cx="526" cy="184" r="39" fill="none" stroke="#BDBDBD" stroke-width="4"/>
    <image href="https://images.example.com/team/max-dark-jacket-avatar.jpg" x="495" y="153" width="62" height="62" clip-path="url(#avatarMax)"/>
    <text x="488" y="236" width="80" font-family="Segoe UI" font-size="13" text-anchor="middle" fill="#111">Max</text>

    <circle cx="650" cy="184" r="39" fill="none" stroke="#C8C8C8" stroke-width="4"/>
    <image href="https://images.example.com/team/zoe-bob-hair-avatar.jpg" x="619" y="153" width="62" height="62" clip-path="url(#avatarZoe)"/>
    <text x="612" y="236" width="80" font-family="Segoe UI" font-size="13" text-anchor="middle" fill="#111">Zoe</text>

    <circle cx="774" cy="184" r="39" fill="none" stroke="#C8C8C8" stroke-width="4"/>
    <image href="https://images.example.com/team/noor-profile-avatar.jpg" x="743" y="153" width="62" height="62" clip-path="url(#avatarNoor)"/>
    <text x="736" y="236" width="80" font-family="Segoe UI" font-size="13" text-anchor="middle" fill="#111">Noor</text>

    <rect x="190" y="282" width="330" height="385" rx="3" fill="#FFFFFF" filter="url(#softShadow)"/>
    <circle cx="230" cy="310" r="13" fill="none" stroke="url(#instaRing)" stroke-width="3"/>
    <image href="https://images.example.com/team/draven-soft-portrait-avatar.jpg" x="217" y="297" width="26" height="26" clip-path="url(#avatarDraven)"/>
    <text x="260" y="316" width="160" font-family="Segoe UI" font-size="15" font-weight="700" fill="#111">dravenswift</text>
    <image href="https://images.example.com/team/draven-vertical-editorial-portrait.jpg" x="210" y="325" width="295" height="318" clip-path="url(#portraitCrop)"/>

    <rect x="548" y="330" width="242" height="245" rx="18" fill="#FFFFFF"/>
    <text x="558" y="389" width="250" font-family="Segoe UI" font-size="34" font-weight="900" fill="#111111">Draven Swift</text>
    <text x="560" y="424" width="245" font-family="Segoe UI" font-size="23" font-weight="800" fill="#222222">25, Technical Lead</text>
    <rect x="560" y="445" width="66" height="24" rx="12" fill="#FCE7F1"/>
    <text x="575" y="463" width="80" font-family="Segoe UI" font-size="12" font-weight="700" fill="#DD2A7B">ACTIVE</text>
    <text x="560" y="497" width="245" font-family="Segoe UI" font-size="15" fill="#222222">Turns complex product ideas into elegant launch systems. Known for rapid prototyping, calm leadership, and pixel-level polish across every client handoff.</text>
    <text x="560" y="552" width="230" font-family="Segoe UI" font-size="12" font-weight="700" fill="#777">24 POSTS   18 PROJECTS   6 AWARDS</text>
  </g>

  <g filter="url(#avatarShadow)">
    <circle cx="860" cy="405" r="112" fill="#FFFFFF"/>
    <circle cx="860" cy="405" r="92" fill="none" stroke="url(#instaRing)" stroke-width="7"/>
    <image href="https://images.example.com/team/draven-soft-portrait-avatar.jpg" x="772" y="317" width="176" height="176" clip-path="url(#heroBubbleCrop)"/>
    <text x="790" y="542" width="150" font-family="Segoe UI" font-size="32" font-weight="800" text-anchor="middle" fill="#111">Draven</text>
  </g>
  <path d="M915 455 L963 506 L932 500 L920 535 L900 528 L912 494 L884 512 Z" fill="#FFFFFF" stroke="#000000" stroke-width="5" stroke-linejoin="round"/>

  <circle cx="1084" cy="392" r="140" fill="#FF5B36" filter="url(#avatarShadow)"/>
  <path d="M960 318 L1066 342 C1080 345 1090 358 1088 373 L1072 494 C1070 509 1056 519 1041 515 L938 491 C923 488 913 474 916 459 L932 338 C934 324 946 315 960 318 Z" fill="#D9300A"/>
  <path d="M975 349 L1045 365 C1055 367 1062 376 1060 386 L1048 472 C1046 482 1037 488 1027 486 L957 470 C947 468 940 459 942 449 L954 363 C956 353 965 347 975 349 Z" fill="#F04A1F"/>
  <text x="980" y="438" width="90" font-family="Segoe UI" font-size="78" font-weight="900" fill="#FFFFFF">P</text>
</svg>
```

## Avoid in this skill
- ❌ Do not use `<mask>` to create avatar crops; use `<clipPath>` applied directly to each `<image>`.
- ❌ Do not apply `clip-path` to groups, circles, or card rectangles; PPT-Master only preserves clipping reliably on images.
- ❌ Do not use `<foreignObject>` for social-media UI panels or HTML-like layouts; build the interface from native SVG shapes and text.
- ❌ Do not rely on `marker-end` for cursor arrows or UI pointers; draw cursor/pointer shapes with editable `<path>` geometry.
- ❌ Do not omit `width` on text labels; story names and bio blocks need explicit widths for stable PowerPoint rendering.

## Composition notes
- Keep the top 20–25% for story navigation; use one saturated gradient ring for the active teammate and muted gray rings for inactive teammates.
- Place the main card slightly off-axis or rotated by 2–4 degrees to make the static slide feel like a captured app interaction.
- Reserve the left rail for small monochrome navigation icons; this makes the roster immediately read as a social app without cluttering the profile content.
- Use color sparingly: mostly white, black, and light gray, with Instagram gradient accents only on active states, badges, and avatar focus.