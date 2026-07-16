# SVG Recipe — Morphing Folder Tab Accordion

## Visual mechanism
A set of overlapping horizontal “folder” panels compress and expand like an accordion, with one active panel widened to reveal content while the others remain visible as narrow navigational tabs. Create multiple slides with the same tab objects but different widths/x-positions, then apply PowerPoint Morph to animate the folder expansion.

## SVG primitives needed
- 1× `<rect>` for the dark violet slide background
- 1× `<radialGradient>` for a subtle ambient glow behind the folders
- 4× `<linearGradient>` fills for the layered folder panels
- 4× `<path>` for custom folder-tab bodies with protruding right-side lips
- 1× `<filter id="tabShadow">` using `feOffset + feGaussianBlur + feMerge`, applied to each folder path
- 1× `<ellipse>` for soft background illumination
- 6× `<rect>` for active-content pills, progress ticks, and small accent bars
- 1× `<line>` for an internal content divider
- Multiple `<text>` elements with explicit `width` attributes for compressed labels, active title/body, watermark number, and persistent chapter title

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <radialGradient id="bgGlow" cx="45%" cy="45%" r="70%">
      <stop offset="0%" stop-color="#7F3FC2" stop-opacity="0.34"/>
      <stop offset="48%" stop-color="#4A1F79" stop-opacity="0.18"/>
      <stop offset="100%" stop-color="#2D124B" stop-opacity="0"/>
    </radialGradient>

    <linearGradient id="tabOne" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#F1E2FF"/>
      <stop offset="100%" stop-color="#D5A9FA"/>
    </linearGradient>
    <linearGradient id="tabTwo" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#D6A1F4"/>
      <stop offset="100%" stop-color="#B76BE9"/>
    </linearGradient>
    <linearGradient id="tabThree" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#A95BDB"/>
      <stop offset="100%" stop-color="#7A2EAD"/>
    </linearGradient>
    <linearGradient id="tabFour" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#6B2399"/>
      <stop offset="100%" stop-color="#3E145F"/>
    </linearGradient>

    <filter id="tabShadow" x="-10%" y="-10%" width="130%" height="130%">
      <feGaussianBlur in="SourceAlpha" stdDeviation="7" result="blur"/>
      <feOffset in="blur" dx="10" dy="0" result="offsetBlur"/>
      <feMerge>
        <feMergeNode in="offsetBlur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#2D124B"/>
  <ellipse cx="520" cy="360" rx="560" ry="360" fill="url(#bgGlow)"/>

  <!-- Back-most collapsed folder -->
  <path filter="url(#tabShadow)" fill="url(#tabFour)"
        d="M870 86 H1010 Q1026 86 1026 102 V164
           C1026 174 1037 181 1050 182 L1074 185
           C1088 187 1096 197 1096 210 V292
           C1096 305 1088 315 1074 317 L1050 320
           C1037 321 1026 328 1026 338 V618
           Q1026 634 1010 634 H886 Q870 634 870 618 V102 Q870 86 886 86 Z"/>
  <text x="928" y="560" width="240" transform="rotate(-90 928 560)"
        font-family="Segoe UI, Microsoft YaHei" font-size="22" font-weight="700"
        letter-spacing="3" fill="#EBD8FF" opacity="0.72">04 SCALE</text>

  <!-- Third collapsed folder -->
  <path filter="url(#tabShadow)" fill="url(#tabThree)"
        d="M750 86 H890 Q906 86 906 102 V246
           C906 256 917 263 930 264 L954 267
           C968 269 976 279 976 292 V374
           C976 387 968 397 954 399 L930 402
           C917 403 906 410 906 420 V618
           Q906 634 890 634 H766 Q750 634 750 618 V102 Q750 86 766 86 Z"/>
  <text x="808" y="560" width="260" transform="rotate(-90 808 560)"
        font-family="Segoe UI, Microsoft YaHei" font-size="22" font-weight="700"
        letter-spacing="3" fill="#F4E8FF" opacity="0.78">03 DESIGN</text>

  <!-- Active expanded folder -->
  <path filter="url(#tabShadow)" fill="url(#tabTwo)"
        d="M120 86 H760 Q778 86 778 104 V142
           C778 153 790 160 804 162 L834 166
           C850 168 860 180 860 196 V292
           C860 308 850 320 834 322 L804 326
           C790 328 778 335 778 346 V616
           Q778 634 760 634 H138 Q120 634 120 616 V104 Q120 86 138 86 Z"/>

  <text x="460" y="548" width="310"
        font-family="Segoe UI, Microsoft YaHei" font-size="230" font-weight="800"
        fill="#FFFFFF" opacity="0.16">02</text>

  <rect x="182" y="148" width="74" height="8" rx="4" fill="#FFD34D"/>
  <text x="182" y="190" width="460"
        font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700"
        letter-spacing="4" fill="#4A145F" opacity="0.78">CHAPTER 02</text>
  <text x="182" y="252" width="520"
        font-family="Segoe UI, Microsoft YaHei" font-size="46" font-weight="800"
        fill="#FFFFFF">Market Signals</text>
  <line x1="182" y1="286" x2="662" y2="286" stroke="#FFFFFF" stroke-width="2" opacity="0.36"/>
  <text x="182" y="328" width="500"
        font-family="Segoe UI, Microsoft YaHei" font-size="22" fill="#FFFFFF" opacity="0.86">
    Decode customer momentum, competitor shifts, and early indicators before they become obvious.
  </text>

  <rect x="182" y="458" width="118" height="34" rx="17" fill="#FFFFFF" opacity="0.22"/>
  <text x="205" y="481" width="90"
        font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#FFFFFF">INSIGHT</text>
  <rect x="316" y="458" width="132" height="34" rx="17" fill="#FFFFFF" opacity="0.14"/>
  <text x="340" y="481" width="100"
        font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#FFFFFF">PRIORITY</text>
  <rect x="464" y="458" width="128" height="34" rx="17" fill="#FFFFFF" opacity="0.14"/>
  <text x="489" y="481" width="90"
        font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#FFFFFF">ACTION</text>

  <!-- Front collapsed folder -->
  <path filter="url(#tabShadow)" fill="url(#tabOne)"
        d="M0 86 H140 Q156 86 156 102 V82
           C156 92 167 99 180 100 L204 103
           C218 105 226 115 226 128 V210
           C226 223 218 233 204 235 L180 238
           C167 239 156 246 156 256 V618
           Q156 634 140 634 H0 Z"/>
  <text x="72" y="558" width="230" transform="rotate(-90 72 558)"
        font-family="Segoe UI, Microsoft YaHei" font-size="22" font-weight="800"
        letter-spacing="3" fill="#4A145F">01 CONTEXT</text>

  <!-- Persistent right-side chapter title -->
  <text x="1092" y="314" width="150"
        font-family="Segoe UI, Microsoft YaHei" font-size="36" font-style="italic"
        font-weight="800" text-anchor="middle" fill="#FFD34D">chapter</text>
  <text x="1092" y="364" width="170"
        font-family="Segoe UI, Microsoft YaHei" font-size="42" font-weight="800"
        text-anchor="middle" fill="#FFFFFF">SLIDES</text>
  <rect x="1050" y="404" width="84" height="5" rx="2.5" fill="#FFD34D"/>
  <text x="1040" y="468" width="120"
        font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700"
        text-anchor="middle" letter-spacing="2" fill="#FFFFFF" opacity="0.58">MORPH READY</text>
</svg>
```

## Avoid in this skill
- ❌ SVG `<animate>` or `<animateTransform>`; use separate Morph keyframe slides instead.
- ❌ `<use href="#id">` for duplicated tabs; draw each tab path explicitly so PowerPoint keeps editable shapes.
- ❌ `clip-path` on folder paths; clipping is only reliable on `<image>` elements.
- ❌ `marker-end` on paths for navigation arrows; this technique does not need arrows, and path markers may disappear.
- ❌ Filters on `<line>` elements; keep shadows only on the folder `<path>` shapes.

## Composition notes
- Keep the accordion working area on the left 80% of the slide; reserve the far-right column for a persistent chapter/navigation label.
- The active tab should occupy roughly 60–70% of the folder width, while collapsed tabs remain narrow but readable.
- Draw back folders first and front folders last so shadows and overlaps create a physical paper-stack illusion.
- For Morph, duplicate the slide and adjust the same four tab paths/text positions so a different tab becomes expanded on each slide.