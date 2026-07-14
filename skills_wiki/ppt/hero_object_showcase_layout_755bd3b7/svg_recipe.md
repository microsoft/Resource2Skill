# SVG Recipe — Hero Object Showcase Layout

## Visual mechanism
A high-impact poster slide: oversized condensed typography dominates one half while a single hero object/logo sits large and centered on the other half. The composition uses extreme simplicity, high contrast, saturated accent color, and generous negative space so the audience reads the concept instantly.

## SVG primitives needed
- 7× `<rect>` for the canvas base, split-color panels, and rainbow edge frame
- 4× `<rect>` for the layered hero-card body and manual depth offsets
- 3× `<text>` for the stacked title words, each with explicit `width`
- 1× `<text>` for the white “P” mark on the hero object
- 1× `<circle>` for the hero-object shadow/backing disk
- 4× `<path>` for editable PowerPoint-style circular quadrant segments
- 7× `<path>` for the dark tactile background texture on the hero side
- 5× `<linearGradient>` for mint panel, rainbow borders, and glossy orange card fill
- 1× `<filter id="softShadow">` applied to hero logo shapes for dimensional depth

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="mintPanel" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#b7ffbd"/>
      <stop offset="55%" stop-color="#72eb95"/>
      <stop offset="100%" stop-color="#50d77a"/>
    </linearGradient>

    <linearGradient id="borderTop" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#11aee8"/>
      <stop offset="24%" stop-color="#4752d9"/>
      <stop offset="45%" stop-color="#e51c85"/>
      <stop offset="66%" stop-color="#ffef25"/>
      <stop offset="84%" stop-color="#18b65d"/>
      <stop offset="100%" stop-color="#007d55"/>
    </linearGradient>

    <linearGradient id="borderBottom" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#10b9ee"/>
      <stop offset="30%" stop-color="#6748d7"/>
      <stop offset="50%" stop-color="#e61e91"/>
      <stop offset="70%" stop-color="#ffdb2a"/>
      <stop offset="100%" stop-color="#00875d"/>
    </linearGradient>

    <linearGradient id="borderSide" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#10addf"/>
      <stop offset="45%" stop-color="#0aa9e8"/>
      <stop offset="100%" stop-color="#15b9ec"/>
    </linearGradient>

    <linearGradient id="cardOrange" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#f04a18"/>
      <stop offset="52%" stop-color="#db3513"/>
      <stop offset="100%" stop-color="#b72c12"/>
    </linearGradient>

    <filter id="softShadow" x="-25%" y="-25%" width="150%" height="150%">
      <feOffset dx="12" dy="12" in="SourceAlpha" result="offset"/>
      <feGaussianBlur in="offset" stdDeviation="10" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#ffffff"/>
  <rect x="0" y="0" width="1280" height="20" fill="url(#borderTop)"/>
  <rect x="0" y="700" width="1280" height="20" fill="url(#borderBottom)"/>
  <rect x="0" y="0" width="16" height="720" fill="url(#borderSide)"/>
  <rect x="1264" y="0" width="16" height="720" fill="#008457"/>

  <rect x="16" y="20" width="696" height="680" fill="url(#mintPanel)"/>
  <rect x="712" y="20" width="552" height="680" fill="#050606"/>

  <g opacity="0.24" fill="none" stroke="#222829" stroke-width="5" stroke-linecap="round">
    <path d="M738 52 c8 -13 28 -13 36 0 M784 52 c8 -13 28 -13 36 0 M830 52 c8 -13 28 -13 36 0 M876 52 c8 -13 28 -13 36 0 M922 52 c8 -13 28 -13 36 0 M968 52 c8 -13 28 -13 36 0 M1014 52 c8 -13 28 -13 36 0 M1060 52 c8 -13 28 -13 36 0 M1106 52 c8 -13 28 -13 36 0 M1152 52 c8 -13 28 -13 36 0 M1198 52 c8 -13 28 -13 36 0"/>
    <path d="M760 94 c8 -13 28 -13 36 0 M806 94 c8 -13 28 -13 36 0 M852 94 c8 -13 28 -13 36 0 M898 94 c8 -13 28 -13 36 0 M944 94 c8 -13 28 -13 36 0 M990 94 c8 -13 28 -13 36 0 M1036 94 c8 -13 28 -13 36 0 M1082 94 c8 -13 28 -13 36 0 M1128 94 c8 -13 28 -13 36 0 M1174 94 c8 -13 28 -13 36 0 M1220 94 c8 -13 28 -13 36 0"/>
    <path d="M738 136 c8 -13 28 -13 36 0 M784 136 c8 -13 28 -13 36 0 M830 136 c8 -13 28 -13 36 0 M876 136 c8 -13 28 -13 36 0 M922 136 c8 -13 28 -13 36 0 M968 136 c8 -13 28 -13 36 0 M1014 136 c8 -13 28 -13 36 0 M1060 136 c8 -13 28 -13 36 0 M1106 136 c8 -13 28 -13 36 0 M1152 136 c8 -13 28 -13 36 0 M1198 136 c8 -13 28 -13 36 0"/>
    <path d="M760 178 c8 -13 28 -13 36 0 M806 178 c8 -13 28 -13 36 0 M852 178 c8 -13 28 -13 36 0 M898 178 c8 -13 28 -13 36 0 M944 178 c8 -13 28 -13 36 0 M990 178 c8 -13 28 -13 36 0 M1036 178 c8 -13 28 -13 36 0 M1082 178 c8 -13 28 -13 36 0 M1128 178 c8 -13 28 -13 36 0 M1174 178 c8 -13 28 -13 36 0 M1220 178 c8 -13 28 -13 36 0"/>
    <path d="M738 612 c8 -13 28 -13 36 0 M784 612 c8 -13 28 -13 36 0 M830 612 c8 -13 28 -13 36 0 M876 612 c8 -13 28 -13 36 0 M922 612 c8 -13 28 -13 36 0 M968 612 c8 -13 28 -13 36 0 M1014 612 c8 -13 28 -13 36 0 M1060 612 c8 -13 28 -13 36 0 M1106 612 c8 -13 28 -13 36 0 M1152 612 c8 -13 28 -13 36 0 M1198 612 c8 -13 28 -13 36 0"/>
    <path d="M760 654 c8 -13 28 -13 36 0 M806 654 c8 -13 28 -13 36 0 M852 654 c8 -13 28 -13 36 0 M898 654 c8 -13 28 -13 36 0 M944 654 c8 -13 28 -13 36 0 M990 654 c8 -13 28 -13 36 0 M1036 654 c8 -13 28 -13 36 0 M1082 654 c8 -13 28 -13 36 0 M1128 654 c8 -13 28 -13 36 0 M1174 654 c8 -13 28 -13 36 0 M1220 654 c8 -13 28 -13 36 0"/>
    <path d="M734 224 c9 -14 29 -14 38 0 M790 266 c9 -14 29 -14 38 0 M1180 304 c9 -14 29 -14 38 0 M1148 430 c9 -14 29 -14 38 0 M776 526 c9 -14 29 -14 38 0 M1202 544 c9 -14 29 -14 38 0"/>
  </g>

  <text x="354" y="248" width="660" text-anchor="middle"
        font-family="Impact, Arial Black, Segoe UI, Microsoft YaHei" font-size="174"
        font-weight="900" letter-spacing="2" fill="#000000">HOW TO</text>

  <text x="354" y="456" width="650" text-anchor="middle"
        font-family="Impact, Arial Black, Segoe UI, Microsoft YaHei" font-size="176"
        font-weight="900" letter-spacing="1" fill="#0908f6">ADD</text>

  <text x="354" y="626" width="675" text-anchor="middle"
        font-family="Impact, Arial Black, Segoe UI, Microsoft YaHei" font-size="126"
        font-weight="900" letter-spacing="1" fill="#0908f6">ANIMATION</text>

  <circle cx="1000" cy="360" r="226" fill="#2b120c" opacity="0.45" filter="url(#softShadow)"/>
  <path d="M1000 134 A226 226 0 0 0 774 360 L1000 360 Z" fill="#f4663d"/>
  <path d="M1000 134 A226 226 0 0 1 1226 360 L1000 360 Z" fill="#ff8d67"/>
  <path d="M1226 360 A226 226 0 0 1 1000 586 L1000 360 Z" fill="#dc4b25"/>
  <path d="M774 360 A226 226 0 0 0 1000 586 L1000 360 Z" fill="#c64220"/>

  <rect x="804" y="282" width="226" height="226" rx="22" fill="#541b0d" opacity="0.34"/>
  <rect x="790" y="268" width="226" height="226" rx="22" fill="#6b210e" opacity="0.30"/>
  <rect x="776" y="254" width="226" height="226" rx="22" fill="#7f260f" opacity="0.26"/>
  <rect x="744" y="238" width="250" height="248" rx="20" fill="url(#cardOrange)" filter="url(#softShadow)"/>

  <text x="865" y="427" width="155" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, Arial" font-size="142"
        font-weight="700" fill="#ffffff">P</text>
</svg>
```

## Avoid in this skill
- ❌ SVG `<pattern>` fills for the dark texture; use editable repeated paths instead.
- ❌ Clipping or masking the hero logo quadrants; draw editable circle segments with `<path>`.
- ❌ Overcrowding the slide with subtitles, bullets, badges, or explanatory copy.
- ❌ Thin or lightweight title fonts; this layout depends on poster-scale heavy typography.
- ❌ Applying filters to `<line>` elements; use shadows only on rects, circles, paths, or text.

## Composition notes
- Keep the hero object at roughly 35–45% of slide width; it should feel iconic, not like a small illustration.
- Reserve one side for huge stacked typography and the other side for the hero object; avoid mixing text into the object zone.
- Use a restrained background split: bright clean panel for text, dark or neutral panel behind the hero to amplify contrast.
- Saturated accent color should repeat in only one or two places, such as title keywords and the hero object.