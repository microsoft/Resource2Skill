# SVG Recipe — Dynamic Morph Continuity Sequence

## Visual mechanism
Create a cinematic “Morph / Magic Move” frame where persistent objects feel like they have transformed into their new positions: huge gradient typography sits behind a foreground subject silhouette, while small icon anchors and app-card elements remain available to match across adjacent slides. The continuity comes from exporting two neighboring slides with the same editable SVG objects, then applying PowerPoint Morph and naming matched objects consistently.

## SVG primitives needed
- 1× `<image>` for a dark cinematic studio / tutorial background photo
- 2× full-slide `<rect>` overlays for darkening and radial color atmosphere
- 1× large `<text>` object for the morphing hero phrase
- 1× foreground `<path>` silhouette for the presenter/body occluding the hero type
- 2× `<path>` shapes for cap brim / shoulder detailing
- 1× rounded `<rect>` app icon base with gradient fill and shadow
- Several small `<rect>`, `<circle>`, `<line>`, and `<path>` objects for the Keynote-style app glyph
- 6× top-row icon groups built from editable `<path>`, `<circle>`, `<rect>`, and `<line>` primitives
- 1× soft teal light streak using `<rect>` plus `feGaussianBlur`
- 1× `<filter id="softShadow">` applied to large foreground objects
- 1× `<filter id="cyanGlow">` applied to the light streak
- 2× `<linearGradient>` fills for coral hero typography and blue app icon
- 1× `<radialGradient>` background wash for cinematic depth

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="coralText" x1="40" y1="260" x2="1240" y2="460" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#ff7a55"/>
      <stop offset="0.48" stop-color="#ff334e"/>
      <stop offset="1" stop-color="#d71857"/>
    </linearGradient>
    <linearGradient id="appBlue" x1="70" y1="535" x2="210" y2="675" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#16c9ff"/>
      <stop offset="0.55" stop-color="#0088ff"/>
      <stop offset="1" stop-color="#0757e8"/>
    </linearGradient>
    <radialGradient id="stageWash" cx="50%" cy="43%" r="68%">
      <stop offset="0" stop-color="#123a36" stop-opacity="0.56"/>
      <stop offset="0.46" stop-color="#071a1d" stop-opacity="0.45"/>
      <stop offset="1" stop-color="#020407" stop-opacity="0.92"/>
    </radialGradient>
    <filter id="softShadow" x="-30%" y="-30%" width="160%" height="170%">
      <feOffset dx="0" dy="18"/>
      <feGaussianBlur stdDeviation="18"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="cyanGlow" x="-50%" y="-300%" width="200%" height="700%">
      <feGaussianBlur stdDeviation="8"/>
    </filter>
  </defs>

  <image id="morph_background_photo" href="https://images.example.com/cinematic-dark-studio-tutorial-background-no-visible-face.jpg" x="0" y="0" width="1280" height="720" preserveAspectRatio="xMidYMid slice"/>
  <rect id="morph_background_dim" x="0" y="0" width="1280" height="720" fill="#05070b" opacity="0.42"/>
  <rect id="morph_background_wash" x="0" y="0" width="1280" height="720" fill="url(#stageWash)"/>

  <rect id="morph_teal_light_streak" x="70" y="221" width="230" height="9" rx="5" fill="#00e5d4" opacity="0.92" filter="url(#cyanGlow)"/>
  <rect id="morph_warm_bokeh" x="1010" y="324" width="112" height="62" rx="31" fill="#ffb13d" opacity="0.62" filter="url(#cyanGlow)"/>

  <g id="morph_top_icons" fill="#8f3f43" stroke="#8f3f43" stroke-width="4" stroke-linecap="round" stroke-linejoin="round" opacity="0.78">
    <g id="morph_icon_crown" transform="translate(64 70)">
      <path d="M5 74 L16 20 L43 55 L61 0 L82 55 L110 20 L122 74 Z"/>
      <circle cx="5" cy="16" r="4"/><circle cx="61" cy="0" r="4"/><circle cx="122" cy="16" r="4"/>
    </g>
    <g id="morph_icon_diamond" transform="translate(220 74)" fill="none">
      <path d="M0 20 L20 0 H78 L98 20 L49 92 Z"/>
      <path d="M0 20 H98 M20 0 L49 92 M78 0 L49 92 M20 0 L36 20 M78 0 L62 20"/>
    </g>
    <g id="morph_icon_case" transform="translate(378 70)" fill="#8f3f43">
      <rect x="0" y="12" width="96" height="66" rx="8" stroke="none"/>
      <path d="M33 13 V4 H63 V13" fill="none"/>
      <rect x="20" y="12" width="10" height="66" stroke="none" fill="#081012" opacity="0.55"/>
      <rect x="66" y="12" width="10" height="66" stroke="none" fill="#081012" opacity="0.55"/>
    </g>
    <g id="morph_icon_clock" transform="translate(850 76)" fill="none">
      <circle cx="38" cy="38" r="36"/>
      <line x1="38" y1="38" x2="38" y2="16"/>
      <line x1="38" y1="38" x2="18" y2="24"/>
      <line x1="38" y1="7" x2="38" y2="12"/>
      <line x1="38" y1="64" x2="38" y2="69"/>
      <line x1="7" y1="38" x2="12" y2="38"/>
      <line x1="64" y1="38" x2="69" y2="38"/>
    </g>
    <g id="morph_icon_clapper" transform="translate(995 70)">
      <rect x="0" y="28" width="76" height="46" rx="5" fill="#8f3f43" stroke="none"/>
      <path d="M0 15 L72 0 L76 12 L4 27 Z" fill="#8f3f43"/>
      <path d="M13 12 L27 24 M36 7 L50 19 M59 2 L72 14" fill="none" stroke="#081012"/>
      <line x1="12" y1="42" x2="63" y2="42" stroke="#081012"/>
      <line x1="12" y1="56" x2="52" y2="56" stroke="#081012"/>
    </g>
    <g id="morph_icon_brain" transform="translate(1135 82)" fill="none">
      <path d="M35 55 C20 56 10 45 14 32 C3 24 9 7 25 9 C32 -4 52 -2 58 11 C72 8 86 18 82 33 C94 40 85 57 68 55 C62 69 43 68 35 55 Z"/>
      <path d="M33 14 C28 24 34 31 45 30 M58 12 C55 24 62 30 74 29 M27 40 C39 36 46 43 43 55 M61 40 C70 41 73 48 68 55"/>
    </g>
  </g>

  <text id="morph_hero_word" x="56" y="464" width="1180" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="188" font-weight="900" letter-spacing="-9" fill="url(#coralText)">MAGIC MOVE</text>

  <g id="morph_presenter_silhouette" filter="url(#softShadow)">
    <path id="morph_body" d="M331 720 C352 590 382 505 448 470 C504 440 522 362 540 248 C552 125 609 4 698 0 C777 1 819 66 817 148 C815 255 748 405 814 470 C899 519 942 611 963 720 Z" fill="#071116"/>
    <path id="morph_jacket_left" d="M385 720 C405 596 448 527 520 491 C548 570 590 651 638 720 Z" fill="#0b1b20" opacity="0.95"/>
    <path id="morph_jacket_right" d="M682 720 C731 646 771 565 801 491 C875 529 921 600 942 720 Z" fill="#0d2228" opacity="0.95"/>
    <path id="morph_cap" d="M553 136 C579 42 641 -7 717 7 C779 19 816 74 821 134 C747 111 636 113 553 136 Z" fill="#10242c"/>
    <path id="morph_cap_bright_rim" d="M551 145 C613 87 740 78 819 123 C818 134 814 145 807 153 C738 118 625 119 557 167 Z" fill="#d9e0dc" opacity="0.62"/>
    <ellipse id="morph_head_shadow" cx="683" cy="285" rx="108" ry="146" fill="#0a1113"/>
  </g>

  <g id="morph_keynote_app" transform="translate(66 535)" filter="url(#softShadow)">
    <rect x="0" y="0" width="143" height="143" rx="28" fill="url(#appBlue)"/>
    <rect x="31" y="21" width="76" height="44" rx="6" fill="#f4f7fb"/>
    <path d="M35 59 H103 L96 69 H42 Z" fill="#c7d6e8"/>
    <line x1="72" y1="70" x2="72" y2="116" stroke="#f6f8fb" stroke-width="6"/>
    <rect x="49" y="116" width="46" height="7" rx="3.5" fill="#d9e6f2"/>
    <circle cx="72" cy="43" r="14" fill="#ffffff"/>
    <path d="M72 29 A14 14 0 0 1 86 43 H72 Z" fill="#ff4b4b"/>
    <path d="M86 43 A14 14 0 0 1 72 57 V43 Z" fill="#42c86b"/>
    <path d="M72 57 A14 14 0 0 1 58 43 H72 Z" fill="#ffd33d"/>
    <path d="M58 43 A14 14 0 0 1 72 29 V43 Z" fill="#3a83ff"/>
  </g>

  <text id="morph_subtitle" x="286" y="642" width="760" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="78" font-weight="800" letter-spacing="-2" fill="#ffffff">Keynote Tutorial</text>
  <text id="morph_micro_label" x="950" y="686" width="250" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="18" font-weight="600" fill="#b8c6c9" opacity="0.62">Morph objects by name</text>
</svg>
```

## Avoid in this skill
- ❌ Do not rasterize the hero word or icons; Morph works best when text and shapes remain editable PowerPoint objects.
- ❌ Do not change object identity between slides. Keep the same SVG IDs / PowerPoint names, then rename matched shapes with the same `!!role_name` convention after import if your workflow supports it.
- ❌ Do not rely on SVG animation tags; the motion must be created by PowerPoint Morph between adjacent slides.
- ❌ Do not use masks or clip paths on regular shapes for the presenter occlusion; use editable paths layered above the text instead.
- ❌ Do not build the sequence as unrelated slide screenshots, because that destroys object permanence and forces a fade instead of a true morph.

## Composition notes
- Keep the hero typography enormous and partially hidden behind the foreground subject; this makes the transition feel spatial, not decorative.
- Use stable anchor objects: the app icon, top icon row, hero word, and silhouette should persist across slides with the same names.
- Slide A can start with the hero word smaller or off-center; Slide B expands it to full width while the foreground silhouette scales up into focus.
- Maintain a dark background with coral/red typography and cyan highlights so moving objects remain visually trackable during Morph.