# SVG Recipe — Corporate Geometric Arc Framing

## Visual mechanism
Oversized circles are positioned partially off-canvas so only sweeping arcs remain visible, creating a soft geometric frame around a circular hero photo. The left side carries layered gold/white/photo circles, while the right side stays open for large corporate title typography and a small badge.

## SVG primitives needed
- 1× `<rect>` for the warm cream slide background
- 5× oversized `<circle>` / `<ellipse>` for off-canvas gold, white, and pale decorative arcs
- 1× `<clipPath>` with `<circle>` for the circular hero photo crop
- 1× `<image>` clipped to the circular photo frame
- 1× `<filter id="softShadow">` applied to the photo rim for depth
- 1× `<linearGradient>` for subtle gold dimensionality
- 1× rounded `<rect>` for the navy subtitle pill
- Multiple `<text>` elements with explicit `width` for title, subtitle, and logo lettering
- 3× `<circle>` plus 3× small `<path>` icons for the simple corporate team logo

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="goldGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#f6c956"/>
      <stop offset="58%" stop-color="#e8b93b"/>
      <stop offset="100%" stop-color="#d79f25"/>
    </linearGradient>

    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feOffset dx="4" dy="6" result="off"/>
      <feGaussianBlur in="off" stdDeviation="5" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <clipPath id="photoCircle">
      <circle cx="306" cy="390" r="229"/>
    </clipPath>
  </defs>

  <!-- warm corporate background -->
  <rect x="0" y="0" width="1280" height="720" fill="#f2efe9"/>

  <!-- pale balancing arcs on the right side -->
  <circle cx="1228" cy="704" r="402" fill="#e6e1d7" opacity="0.72"/>
  <circle cx="1218" cy="704" r="273" fill="#f2efe9"/>
  <circle cx="1252" cy="726" r="488" fill="none" stroke="#e6e1d7" stroke-width="2.5" opacity="0.95"/>

  <!-- left off-canvas gold circle creates the dominant sweeping arc -->
  <circle cx="-72" cy="-108" r="615" fill="url(#goldGrad)"/>

  <!-- quiet cream crescent between the gold arc and the content -->
  <circle cx="10" cy="-70" r="642" fill="none" stroke="#ded9cd" stroke-width="118" opacity="0.58"/>

  <!-- photo framing stack: gold offset rim, white rim, clipped image -->
  <circle cx="332" cy="402" r="248" fill="#e8b93b" opacity="0.98"/>
  <circle cx="306" cy="390" r="252" fill="#ffffff" filter="url(#softShadow)"/>
  <circle cx="306" cy="390" r="232" fill="#e8b93b"/>

  <image
    href="https://images.example.com/corporate-team-meeting-around-table-square.jpg"
    x="72" y="156" width="468" height="468"
    preserveAspectRatio="xMidYMid slice"
    clip-path="url(#photoCircle)"/>

  <!-- subtle translucent overlay to make stock photography feel presentation-ready -->
  <circle cx="306" cy="390" r="229" fill="#1f2937" opacity="0.08"/>

  <!-- small top-right team logo -->
  <g transform="translate(984 38)">
    <circle cx="18" cy="23" r="16" fill="#2aa7df"/>
    <circle cx="52" cy="17" r="18" fill="#2aa7df"/>
    <circle cx="86" cy="23" r="16" fill="#2aa7df"/>

    <path d="M2 71 C3 48 12 38 27 38 C36 38 43 42 47 50 C39 52 34 60 34 76 L2 76 Z" fill="#2aa7df"/>
    <path d="M30 77 C31 49 40 35 52 35 C65 35 74 49 75 77 Z" fill="#2aa7df"/>
    <path d="M57 76 C57 60 63 52 72 50 C76 42 83 38 92 38 C107 38 116 48 118 71 L118 76 Z" fill="#2aa7df"/>

    <path d="M50 43 L45 66 L52 76 L59 66 L54 43 Z" fill="#ffffff" opacity="0.95"/>
    <path d="M17 47 L14 63 L18 70 L22 63 L20 47 Z" fill="#ffffff" opacity="0.9"/>
    <path d="M84 47 L81 63 L86 70 L90 63 L88 47 Z" fill="#ffffff" opacity="0.9"/>

    <text x="132" y="33" width="120" font-family="Segoe UI, Microsoft YaHei, sans-serif"
          font-size="30" font-weight="700" fill="#2aa7df">Slide</text>
    <text x="132" y="76" width="120" font-family="Segoe UI, Microsoft YaHei, sans-serif"
          font-size="30" font-weight="800" fill="#111827">Team</text>
  </g>

  <!-- main title block -->
  <text x="604" y="321" width="650"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="96" font-weight="300" letter-spacing="1"
        fill="#050505">Performance</text>

  <text x="965" y="443" width="280"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="82" font-weight="800"
        fill="#050505">Team</text>

  <!-- subtitle pill -->
  <rect x="850" y="486" width="384" height="44" rx="22" fill="#2b5773"/>
  <text x="910" y="516" width="275"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="16" font-weight="400"
        fill="#ffffff">Collection of 10+ PowerPoint Templates</text>

  <!-- faint bottom hairline for deck-template polish -->
  <line x1="0" y1="666" x2="1280" y2="666" stroke="#ffffff" stroke-width="1" opacity="0.65"/>
</svg>
```

## Avoid in this skill
- ❌ Using `<mask>` to crop the photo; use `<clipPath>` on the `<image>` instead.
- ❌ Applying `clip-path` to grouped circles or decorative shapes; clipping is only reliable here on the hero `<image>`.
- ❌ Replacing the off-canvas circles with hand-drawn arc paths unless you need a non-circular custom contour.
- ❌ Putting shadows on `<line>` elements; apply filters to circles, ellipses, paths, or text only.
- ❌ Overfilling the right side with extra graphics; the technique depends on generous negative space around the headline.

## Composition notes
- Keep the hero image circle large, roughly 450–500 px wide, and let it overlap the left edge arc system.
- The title should sit in the open right half, with the lighter word above and the bold word offset down/right for hierarchy.
- Use one saturated accent color, usually gold, and repeat it only in the left framing system to avoid visual noise.
- Balance the heavy left photo with pale oversized arcs in the bottom-right corner, kept low contrast so they do not compete with the text.