# SVG Recipe — Interactive Morphing Profile Carousel

## Visual mechanism
A row of portrait cards preserves spatial continuity while one selected card morphs into a large centered hero card and the surrounding cards shrink toward the margins. The slide reads like an app carousel: stable card IDs across slides enable PowerPoint Morph, while shadows, clipped photography, a pointer hand, and a subtle PowerPoint cue signal interactivity.

## SVG primitives needed
- 1× `<rect>` for the soft off-white slide background
- 5× `<rect>` shadow plates behind the portrait cards
- 5× `<image>` clipped into rounded portrait cards for profile imagery
- 5× `<clipPath>` with rounded `<rect>` crops for the portrait images
- 2× `<text>` elements for the active profile name and role, each with explicit `width`
- 1× `<path>` cluster for a large hand/click cursor overlay
- 5× `<line>` or `<path>` click rays around the fingertip
- 3× `<rect>` plus 1× `<circle>`/`<ellipse>` accent group for the PowerPoint-style interaction badge
- 2× `<filter>` definitions for card shadow and cursor shadow
- 3× `<linearGradient>` definitions for background glow, card tint overlays, and orange badge depth

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <filter id="cardShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="18"/>
      <feGaussianBlur stdDeviation="18"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="cursorShadow" x="-25%" y="-25%" width="160%" height="160%">
      <feOffset dx="0" dy="10"/>
      <feGaussianBlur stdDeviation="10"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <linearGradient id="bgGlow" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#ffffff"/>
      <stop offset="0.55" stop-color="#f2f3f4"/>
      <stop offset="1" stop-color="#e7e8ea"/>
    </linearGradient>
    <linearGradient id="pptOrange" x1="1015" y1="520" x2="1230" y2="710" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#ff6a2a"/>
      <stop offset="1" stop-color="#f1431f"/>
    </linearGradient>
    <linearGradient id="pptCircle" x1="1060" y1="430" x2="1230" y2="610" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#ff914a"/>
      <stop offset="1" stop-color="#ff6a2a"/>
    </linearGradient>

    <clipPath id="clip-card-0"><rect x="48" y="219" width="167" height="249" rx="10" ry="10"/></clipPath>
    <clipPath id="clip-card-1"><rect x="253" y="193" width="203" height="302" rx="10" ry="10"/></clipPath>
    <clipPath id="clip-card-2"><rect x="478" y="83" width="352" height="519" rx="20" ry="20"/></clipPath>
    <clipPath id="clip-card-3"><rect x="852" y="193" width="203" height="302" rx="10" ry="10"/></clipPath>
    <clipPath id="clip-card-4"><rect x="1090" y="220" width="168" height="246" rx="10" ry="10"/></clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGlow)"/>

  <rect id="card-0-shadow" x="48" y="219" width="167" height="249" rx="10" fill="#ffffff" filter="url(#cardShadow)" opacity="0.55"/>
  <image id="card-0" x="48" y="219" width="167" height="249" href="https://images.example.com/profile-yellow-fashion-portrait.jpg" preserveAspectRatio="xMidYMid slice" clip-path="url(#clip-card-0)"/>

  <rect id="card-1-shadow" x="253" y="193" width="203" height="302" rx="10" fill="#ffffff" filter="url(#cardShadow)" opacity="0.62"/>
  <image id="card-1" x="253" y="193" width="203" height="302" href="https://images.example.com/profile-red-jacket-portrait.jpg" preserveAspectRatio="xMidYMid slice" clip-path="url(#clip-card-1)"/>

  <rect id="card-2-shadow" x="478" y="83" width="352" height="519" rx="20" fill="#ffffff" filter="url(#cardShadow)" opacity="0.75"/>
  <image id="card-2-active" x="478" y="83" width="352" height="519" href="https://images.example.com/profile-purple-studio-portrait.jpg" preserveAspectRatio="xMidYMid slice" clip-path="url(#clip-card-2)"/>

  <rect id="card-3-shadow" x="852" y="193" width="203" height="302" rx="10" fill="#ffffff" filter="url(#cardShadow)" opacity="0.62"/>
  <image id="card-3" x="852" y="193" width="203" height="302" href="https://images.example.com/profile-blue-studio-portrait.jpg" preserveAspectRatio="xMidYMid slice" clip-path="url(#clip-card-3)"/>

  <rect id="card-4-shadow" x="1090" y="220" width="168" height="246" rx="10" fill="#ffffff" filter="url(#cardShadow)" opacity="0.55"/>
  <image id="card-4" x="1090" y="220" width="168" height="246" href="https://images.example.com/profile-green-chair-portrait.jpg" preserveAspectRatio="xMidYMid slice" clip-path="url(#clip-card-4)"/>

  <text x="487" y="646" width="340" font-family="Segoe UI, Microsoft YaHei" font-size="32" font-weight="700" fill="#323232" text-anchor="middle">Angela Chen</text>
  <text x="487" y="678" width="340" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="400" fill="#787878" text-anchor="middle">Project Manager · Click any card to explore</text>

  <g id="click-rays" stroke="#202020" stroke-width="10" stroke-linecap="round" opacity="0.95">
    <line x1="659" y1="444" x2="647" y2="401"/>
    <line x1="632" y1="476" x2="590" y2="459"/>
    <line x1="655" y1="502" x2="610" y2="513"/>
    <line x1="692" y1="462" x2="709" y2="424"/>
    <line x1="728" y1="481" x2="766" y2="458"/>
  </g>

  <path id="cursor-hand" filter="url(#cursorShadow)" fill="#ffffff" stroke="#202020" stroke-width="11" stroke-linejoin="round" stroke-linecap="round"
        d="M704 490
           C688 497 677 515 681 532
           L714 651
           L724 651
           L707 618
           C698 600 704 585 719 581
           C733 577 744 587 753 604
           L762 622
           L762 508
           C762 491 774 482 787 487
           C797 491 802 500 802 514
           L802 613
           L817 613
           L817 553
           C817 537 828 528 842 532
           C854 536 859 545 859 560
           L859 613
           L874 613
           L874 558
           C874 544 885 535 898 539
           C909 542 914 552 914 567
           L914 613
           L929 613
           L929 566
           C929 552 939 543 952 547
           C963 551 968 560 968 576
           L968 682
           C968 710 945 734 917 734
           L793 734
           C760 734 733 718 716 689
           L691 646
           L673 611
           L704 490 Z"/>

  <ellipse cx="1176" cy="527" rx="121" ry="95" fill="url(#pptCircle)" opacity="0.82"/>
  <rect x="1142" y="619" width="138" height="99" rx="6" fill="#c9321a" opacity="0.85"/>
  <rect x="1017" y="517" width="206" height="203" rx="16" fill="url(#pptOrange)" filter="url(#cardShadow)"/>
  <text x="1070" y="676" width="120" font-family="Segoe UI, Microsoft YaHei" font-size="118" font-weight="800" fill="#ffffff">P</text>
</svg>
```

## Avoid in this skill
- ❌ SVG `<animate>` or `<animateTransform>` for the morph; create separate slides/states and let PowerPoint Morph interpolate identical element IDs.
- ❌ `<use>` / `<symbol>` for repeated cards or icons; duplicate real shapes so each card remains independently editable and morph-trackable.
- ❌ Applying `clip-path` to card shadow rectangles; clip only the `<image>` and draw separate rounded rectangles for shadows/plates.
- ❌ `marker-end` arrowheads for click cues; use explicit `<line>` rays or hand paths instead.
- ❌ Mask-based photo crops or blur masks; use `clipPath` with rounded rects on images.

## Composition notes
- Keep the active card centered and 2–2.5× larger than the side cards; side cards should retain left-to-right order to make the morph feel spatially logical.
- Reserve a clean lower band for the active person’s name/role, but allow the oversized cursor to overlap the hero card for an app-like interaction moment.
- Use saturated portrait backgrounds against a quiet white/gray canvas; color rhythm should progress warm → red → violet hero → cyan → green.
- For actual Morph slides, duplicate the same five card elements on every slide, changing only x/y/width/height/rx and opacity/text reveal state.