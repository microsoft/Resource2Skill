# SVG Recipe — Kinetic Brutalist Typography

## Visual mechanism
Oversized ultra-bold typography is packed into interlocking blocks, with magenta slabs, white outline frames, and rotated side labels creating the feeling of paused motion-graphics typography. The slide works like a poster: text is not merely read, it becomes the primary graphic structure.

## SVG primitives needed
- 1× `<rect>` for the full dark indigo background
- 8× `<rect>` for hot-pink brutalist text bars and hero boxes
- 2× `<rect>` with transparent fill and white stroke for offset structural frames
- 13× `<text>` for oversized headline words, compact label bars, rotated side text, and punctuation
- 5× `<path>` for kinetic diagonal shards and motion-accent fragments
- 1× `<linearGradient>` for a subtle background depth wash
- 1× `<filter id="hardShadow">` applied to large text and slabs for crisp poster depth
- 1× `<filter id="pinkGlow">` applied sparingly to accent blocks for energetic magenta bloom

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgWash" x1="0" y1="0" x2="1280" y2="720" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#20163D"/>
      <stop offset="0.55" stop-color="#1D1733"/>
      <stop offset="1" stop-color="#17112A"/>
    </linearGradient>

    <filter id="hardShadow" x="-10%" y="-10%" width="120%" height="130%">
      <feOffset dx="5" dy="6" result="off"/>
      <feGaussianBlur in="off" stdDeviation="0.8" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="pinkGlow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="5" result="glow"/>
      <feMerge>
        <feMergeNode in="glow"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgWash)"/>

  <!-- kinetic accent shards -->
  <path d="M1018 86 L1067 86 L1045 101 L995 101 Z" fill="#F33664" opacity="0.95"/>
  <path d="M640 119 L666 119 L654 138 L628 138 Z" fill="#FFFFFF" opacity="0.9"/>
  <path d="M553 558 L589 558 L573 580 L536 580 Z" fill="#F33664" opacity="0.9"/>
  <path d="M1128 257 L1172 257 L1156 274 L1112 274 Z" fill="#FFFFFF" opacity="0.86"/>
  <path d="M330 610 L372 610 L352 629 L310 629 Z" fill="#F33664" opacity="0.75"/>

  <!-- top-left IF block -->
  <rect x="84" y="136" width="180" height="178" fill="none" stroke="#FFFFFF" stroke-width="5"/>
  <rect x="100" y="151" width="149" height="149" fill="#F33664" filter="url(#pinkGlow)"/>
  <text x="174" y="282" width="150" text-anchor="middle"
        font-family="Segoe UI Black, Segoe UI, Microsoft YaHei, sans-serif"
        font-size="126" font-weight="900" fill="#FFFFFF" letter-spacing="-6" filter="url(#hardShadow)">IF</text>

  <rect x="290" y="134" width="230" height="42" fill="#F33664"/>
  <text x="405" y="166" width="230" text-anchor="middle"
        font-family="Segoe UI Black, Segoe UI, Microsoft YaHei, sans-serif"
        font-size="31" font-weight="900" fill="#FFFFFF" letter-spacing="1">YOU WANNA</text>

  <text x="289" y="247" width="250"
        font-family="Segoe UI Black, Segoe UI, Microsoft YaHei, sans-serif"
        font-size="62" font-weight="900" fill="#FFFFFF" letter-spacing="1.5" filter="url(#hardShadow)">CREATE</text>

  <rect x="290" y="274" width="230" height="42" fill="#F33664"/>
  <text x="405" y="306" width="230" text-anchor="middle"
        font-family="Segoe UI Black, Segoe UI, Microsoft YaHei, sans-serif"
        font-size="29" font-weight="900" fill="#FFFFFF" letter-spacing="0.5">THE KINETIC</text>

  <!-- top-right title lockup -->
  <text x="653" y="166" width="420"
        font-family="Segoe UI Black, Segoe UI, Microsoft YaHei, sans-serif"
        font-size="39" font-weight="900" fill="#FFFFFF" letter-spacing="4">USING POWERPOINT</text>

  <text x="619" y="233" width="525"
        font-family="Segoe UI Black, Segoe UI, Microsoft YaHei, sans-serif"
        font-size="92" font-weight="900" fill="#FFFFFF" letter-spacing="-2" filter="url(#hardShadow)">typography</text>

  <text x="773" y="306" width="46"
        font-family="Segoe UI Black, Segoe UI, Microsoft YaHei, sans-serif"
        font-size="56" font-weight="900" fill="#FFFFFF" text-anchor="middle">&amp;</text>

  <rect x="828" y="266" width="388" height="48" fill="#F33664"/>
  <text x="1022" y="303" width="388" text-anchor="middle"
        font-family="Segoe UI Black, Segoe UI, Microsoft YaHei, sans-serif"
        font-size="35" font-weight="900" fill="#FFFFFF" letter-spacing="1">TEXT ANIMATIONS</text>

  <!-- lower-left BECOME cluster -->
  <rect x="69" y="470" width="164" height="119" fill="#F33664" filter="url(#pinkGlow)"/>
  <text x="151" y="579" width="164" text-anchor="middle"
        font-family="Segoe UI Black, Segoe UI, Microsoft YaHei, sans-serif"
        font-size="126" font-weight="900" fill="#FFFFFF" letter-spacing="-8" filter="url(#hardShadow)">BE</text>

  <rect x="248" y="470" width="253" height="38" fill="#F33664"/>
  <text x="374" y="500" width="253" text-anchor="middle"
        font-family="Segoe UI Black, Segoe UI, Microsoft YaHei, sans-serif"
        font-size="29" font-weight="900" fill="#FFFFFF" letter-spacing="0.2">YOUR OWN BOSS</text>

  <text x="247" y="589" width="264"
        font-family="Segoe UI Black, Segoe UI, Microsoft YaHei, sans-serif"
        font-size="88" font-weight="900" fill="#FFFFFF" letter-spacing="-3" filter="url(#hardShadow)">COME</text>

  <text x="525" y="589" width="122" transform="rotate(-90 525 589)"
        font-family="Segoe UI Black, Segoe UI, Microsoft YaHei, sans-serif"
        font-size="17" font-weight="900" fill="#FFFFFF" letter-spacing="1.4">INDEPENDENT</text>

  <!-- lower-right surprise cluster -->
  <text x="662" y="553" width="82"
        font-family="Segoe UI Black, Segoe UI, Microsoft YaHei, sans-serif"
        font-size="96" font-weight="900" fill="#F33664" filter="url(#hardShadow)">&amp;</text>

  <text x="762" y="549" width="390"
        font-family="Segoe UI Black, Segoe UI, Microsoft YaHei, sans-serif"
        font-size="86" font-weight="900" fill="#FFFFFF" letter-spacing="2" filter="url(#hardShadow)">surprise</text>

  <rect x="953" y="566" width="141" height="41" fill="#F33664"/>
  <text x="1023" y="597" width="141" text-anchor="middle"
        font-family="Segoe UI Black, Segoe UI, Microsoft YaHei, sans-serif"
        font-size="30" font-weight="900" fill="#FFFFFF" letter-spacing="0.5">OTHERS</text>

  <!-- offset structure behind bottom motion field -->
  <rect x="642" y="465" width="470" height="124" fill="none" stroke="#FFFFFF" stroke-width="3" opacity="0.18"/>
</svg>
```

## Avoid in this skill
- ❌ Thin, light, or rounded typography; the effect depends on heavy condensed visual mass.
- ❌ Centered paragraph layouts or generous line spacing; keep text blocks tightly locked together.
- ❌ `<textPath>` for curved kinetic text — it will not translate reliably; use rotated `<text>` instead.
- ❌ `skewX`, `skewY`, or matrix transforms for fake motion perspective; use rotated text, diagonal `<path>` shards, and offset frames.
- ❌ Applying clip paths or masks to text/shapes; keep all text and blocks as native editable SVG primitives.

## Composition notes
- Keep the main typographic weight in the left and upper-center zones, with one secondary statement on the lower-right to balance the poster.
- Use magenta as a structural rhythm: hero block, label bars, punctuation, and small shards should repeat across the slide.
- Let the dark background breathe; brutalist clusters need surrounding negative space so the typography feels intentional rather than crowded.
- Offset outline rectangles should sit slightly behind the dominant blocks, implying motion and construction without reducing readability.