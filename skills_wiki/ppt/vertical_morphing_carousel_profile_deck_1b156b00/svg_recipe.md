# SVG Recipe — Vertical Morphing Carousel (Profile Deck)

## Visual mechanism
A tall, right-anchored column of profile photos behaves like a continuous vertical filmstrip; each slide is a different keyframe where the same image group is shifted up or down so one profile locks to the center. The active profile receives the large text treatment and highlighted role pill, while adjacent items remain visible as peripheral context.

## SVG primitives needed
- 1× full-canvas `<rect>` for the muted presentation backdrop
- 1× large rounded `<rect>` for the main white profile card
- 1× clipped `<image>` for the active hero portrait on the right side
- 4× smaller clipped `<image>` elements for the vertical carousel previews above and below the active portrait
- 5× `<clipPath>` definitions using rounded `<rect>` crops for editable rounded photo cards
- 1× `<linearGradient>` for the teal-to-cyan active designation pill
- 1× `<linearGradient>` for the right-side photo fade wash
- 1× `<filter id="cardShadow">` for the main card shadow
- 1× `<filter id="photoShadow">` for lifted photo tiles
- 1× `<filter id="softGlow">` for accent highlight depth
- Multiple `<text>` elements with explicit `width` for title, name, surname, role list, bio, and keyframe notes
- 2× decorative `<path>` shapes for subtle vertical motion arrows and carousel track accents
- 1× dashed `<line>` for the center alignment axis

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#91A7BC"/>
      <stop offset="100%" stop-color="#6F879F"/>
    </linearGradient>

    <linearGradient id="pillGrad" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#087F7E"/>
      <stop offset="100%" stop-color="#10B8C7"/>
    </linearGradient>

    <linearGradient id="photoWash" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.42"/>
      <stop offset="45%" stop-color="#FFFFFF" stop-opacity="0"/>
      <stop offset="100%" stop-color="#111827" stop-opacity="0.18"/>
    </linearGradient>

    <filter id="cardShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="14"/>
      <feGaussianBlur stdDeviation="13"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="photoShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="10"/>
      <feGaussianBlur stdDeviation="9"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="softGlow" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="5"/>
    </filter>

    <clipPath id="heroClip">
      <rect x="785" y="80" width="350" height="560" rx="0" ry="0"/>
    </clipPath>
    <clipPath id="thumbTop2">
      <rect x="1090" y="-120" width="150" height="190" rx="28" ry="28"/>
    </clipPath>
    <clipPath id="thumbTop1">
      <rect x="1088" y="86" width="154" height="194" rx="30" ry="30"/>
    </clipPath>
    <clipPath id="thumbBottom1">
      <rect x="1088" y="440" width="154" height="194" rx="30" ry="30"/>
    </clipPath>
    <clipPath id="thumbBottom2">
      <rect x="1090" y="650" width="150" height="190" rx="28" ry="28"/>
    </clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>

  <text x="28" y="52" width="580" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="38" font-weight="900" fill="#FFC928" stroke="#1E293B" stroke-width="7" paint-order="stroke fill">TEAM INTRO ANIMATION</text>

  <rect x="142" y="80" width="995" height="560" rx="30" ry="30" fill="#FFFFFF" filter="url(#cardShadow)"/>
  <rect x="142" y="80" width="995" height="560" rx="30" ry="30" fill="none" stroke="#FFFFFF" stroke-width="2" opacity="0.75"/>

  <rect x="142" y="164" width="238" height="58" rx="29" ry="29" fill="url(#pillGrad)" filter="url(#softGlow)"/>
  <text x="160" y="203" width="210" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="27" font-weight="800" fill="#FFFFFF">DESIGNATION 1</text>

  <text x="160" y="264" width="210" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="14" font-weight="800" fill="#111111">DESIGNATION 2</text>
  <text x="160" y="331" width="210" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="14" font-weight="800" fill="#111111">DESIGNATION 3</text>
  <text x="160" y="398" width="210" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="14" font-weight="800" fill="#111111">DESIGNATION 4</text>
  <text x="160" y="466" width="210" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="14" font-weight="800" fill="#111111">DESIGNATION 5</text>
  <text x="160" y="532" width="210" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="14" font-weight="800" fill="#111111">DESIGNATION 6</text>

  <line x1="784" y1="80" x2="784" y2="640" stroke="#E5E7EB" stroke-width="1"/>
  <line x1="1010" y1="360" x2="1235" y2="360" stroke="#0E8F91" stroke-width="2" stroke-dasharray="8 10" opacity="0.5"/>

  <g id="carouselTrack_keyframe_1">
    <image x="1090" y="-120" width="150" height="190" clip-path="url(#thumbTop2)" href="https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=300&amp;h=380&amp;fit=crop" opacity="0.45"/>
    <rect x="1090" y="-120" width="150" height="190" rx="28" fill="#FFFFFF" opacity="0.18"/>

    <image x="1088" y="86" width="154" height="194" clip-path="url(#thumbTop1)" href="https://images.unsplash.com/photo-1544005313-94ddf0286df2?w=308&amp;h=388&amp;fit=crop" opacity="0.72"/>
    <rect x="1088" y="86" width="154" height="194" rx="30" fill="#FFFFFF" opacity="0.12"/>

    <image x="785" y="80" width="350" height="560" clip-path="url(#heroClip)" href="https://images.unsplash.com/photo-1560250097-0b93528c311a?w=700&amp;h=1120&amp;fit=crop" filter="url(#photoShadow)"/>
    <rect x="785" y="80" width="350" height="560" fill="url(#photoWash)"/>

    <image x="1088" y="440" width="154" height="194" clip-path="url(#thumbBottom1)" href="https://images.unsplash.com/photo-1551836022-d5d88e9218df?w=308&amp;h=388&amp;fit=crop" opacity="0.72"/>
    <rect x="1088" y="440" width="154" height="194" rx="30" fill="#111827" opacity="0.08"/>

    <image x="1090" y="650" width="150" height="190" clip-path="url(#thumbBottom2)" href="https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=300&amp;h=380&amp;fit=crop" opacity="0.45"/>
    <rect x="1090" y="650" width="150" height="190" rx="28" fill="#111827" opacity="0.08"/>
  </g>

  <rect x="448" y="220" width="295" height="120" fill="#FFFFFF" opacity="0.96"/>
  <text x="448" y="263" width="310" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="44" font-weight="900" fill="#000000" letter-spacing="1">NAME</text>
  <text x="522" y="318" width="260" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="44" font-weight="800" fill="#000000" letter-spacing="1">SURNAME 1</text>

  <text x="482" y="369" width="255" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="14" fill="#222222">
    <tspan x="482" dy="0">Some text goes here. Some text goes here.</tspan>
    <tspan x="482" dy="20">The active profile stays locked to the</tspan>
    <tspan x="482" dy="20">center line while the photo strip morphs</tspan>
    <tspan x="482" dy="20">vertically between slides. Keep object</tspan>
    <tspan x="482" dy="20">names and sizes identical for smooth</tspan>
    <tspan x="482" dy="20">PowerPoint Morph interpolation.</tspan>
  </text>

  <path d="M1194 288 C1218 310 1220 410 1194 432" fill="none" stroke="#FFFFFF" stroke-width="6" stroke-linecap="round" opacity="0.75"/>
  <path d="M1194 288 L1210 305 L1186 307 Z" fill="#FFFFFF" opacity="0.75"/>
  <path d="M1194 432 L1210 415 L1186 413 Z" fill="#FFFFFF" opacity="0.75"/>

  <rect x="948" y="622" width="268" height="54" rx="27" ry="27" fill="#12BDE3"/>
  <rect x="1082" y="622" width="134" height="54" rx="27" ry="27" fill="#1976F3" opacity="0.92"/>
  <path d="M1095 617 L1144 617 L1122 681 L1074 681 Z" fill="#F30845"/>
  <text x="982" y="638" width="120" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="10" font-weight="700" fill="#064E5A">WITH</text>
  <text x="982" y="668" width="170" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="28" font-weight="900" fill="#111827">VOICE OVER</text>

  <circle cx="72" cy="654" r="36" fill="#E95B35" opacity="0.9" filter="url(#cardShadow)"/>
  <rect x="30" y="632" width="50" height="42" rx="4" fill="#D94A2E"/>
  <text x="40" y="663" width="40" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="28" font-weight="800" fill="#FFFFFF">P</text>

  <text x="944" y="138" width="180" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="12" font-weight="700" fill="#0E8F91" opacity="0.8">ACTIVE FRAME</text>
</svg>
```

## Avoid in this skill
- ❌ Do not use SVG animation tags; create multiple slides and rely on PowerPoint Morph between static keyframes.
- ❌ Do not crop photos with masks on rectangles; use `clipPath` directly on each `<image>`.
- ❌ Do not change photo dimensions between keyframes; Morph looks best when only the carousel group’s Y-position changes.
- ❌ Do not use `<use>` or `<symbol>` for repeated profile cards; duplicate the editable shapes directly.
- ❌ Do not put arrowheads on paths with `marker-end`; use simple paths or lines for motion accents.

## Composition notes
- Keep the profile text block in the middle-left 45–50% of the slide and reserve the right 25–30% for the moving photo track.
- The active portrait should align to a fixed horizontal center axis; on the next slide, shift the entire photo group vertically so the next portrait occupies the same slot.
- Use one high-saturation accent, usually teal or cyan, for the active designation pill and tiny alignment cues.
- Leave generous white space around the name and surname; the carousel motion supplies energy, so the typography should remain clean and executive.