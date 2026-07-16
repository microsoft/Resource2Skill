# SVG Recipe — Composite Layered Cover (图片+色块+线框叠层封面法)

## Visual mechanism
A full-bleed photographic background is quieted by a semi-transparent dark color block, then sharpened with a thin neon line frame and centered executive typography. The signature look comes from four stacked layers: image texture, glass-like reading pane, precise glowing frame, and high-contrast title/ribbon text.

## SVG primitives needed
- 1× `<image>` for the full-bleed architectural/technology background photo
- 2× full-slide `<rect>` overlays for darkening and cool gradient tinting the background
- 2× `<ellipse>` for soft cyan/violet background light blooms
- 5× decorative `<path>` strokes for angular “tech cover” linework behind the panel
- 2× large `<rect>` for the translucent navy reading panel and its soft shadow
- 2× `<rect>` for the inner neon line frame, one blurred/glowing duplicate and one crisp foreground frame
- 8× small `<rect>` for corner brackets and micro-square tech accents
- 2× `<rect>` for the subtitle ribbon and its shadow/accent underlay
- 5× `<text>` blocks for eyebrow, main title, subtitle, date, and footer metadata
- 2× `<filter>` definitions: one panel shadow, one neon glow
- 3× gradient definitions for background tint, panel fill, and ribbon fill

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="coolTint" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#05111f" stop-opacity="0.82"/>
      <stop offset="45%" stop-color="#07182d" stop-opacity="0.45"/>
      <stop offset="100%" stop-color="#01040a" stop-opacity="0.88"/>
    </linearGradient>

    <linearGradient id="panelGlass" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#061322" stop-opacity="0.88"/>
      <stop offset="55%" stop-color="#0a1020" stop-opacity="0.78"/>
      <stop offset="100%" stop-color="#020713" stop-opacity="0.90"/>
    </linearGradient>

    <linearGradient id="ribbonCyan" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#00d7ff"/>
      <stop offset="60%" stop-color="#39f2ff"/>
      <stop offset="100%" stop-color="#8af7ff"/>
    </linearGradient>

    <filter id="panelShadow" x="-10%" y="-20%" width="120%" height="140%">
      <feOffset dx="0" dy="16"/>
      <feGaussianBlur stdDeviation="18"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="neonGlow" x="-20%" y="-30%" width="140%" height="160%">
      <feGaussianBlur stdDeviation="5"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <image x="0" y="0" width="1280" height="720" preserveAspectRatio="xMidYMid slice"
         href="https://images.example.com/full-bleed-night-city-glass-tower-data-center.jpg"/>

  <rect x="0" y="0" width="1280" height="720" fill="#020711" opacity="0.32"/>
  <rect x="0" y="0" width="1280" height="720" fill="url(#coolTint)"/>

  <ellipse cx="1010" cy="160" rx="280" ry="150" fill="#00d7ff" opacity="0.12"/>
  <ellipse cx="215" cy="620" rx="360" ry="170" fill="#7e3cff" opacity="0.14"/>

  <path d="M80 134 L300 134 L365 198 L560 198" fill="none" stroke="#00d7ff" stroke-width="1.4" opacity="0.34"/>
  <path d="M880 118 L1035 118 L1098 178 L1210 178" fill="none" stroke="#8af7ff" stroke-width="1.2" opacity="0.28"/>
  <path d="M72 584 L250 584 L315 528 L450 528" fill="none" stroke="#ffffff" stroke-width="1" opacity="0.22"/>
  <path d="M842 574 L1015 574 L1085 510 L1210 510" fill="none" stroke="#00d7ff" stroke-width="1.2" opacity="0.30"/>
  <path d="M1110 258 L1168 258 L1192 282 L1192 340" fill="none" stroke="#ffffff" stroke-width="1" opacity="0.24" stroke-dasharray="7 7"/>

  <rect x="86" y="188" width="1108" height="344" rx="6" fill="#000814" opacity="0.38" filter="url(#panelShadow)"/>
  <rect x="86" y="188" width="1108" height="344" rx="6" fill="url(#panelGlass)" stroke="#ffffff" stroke-width="1" stroke-opacity="0.08"/>

  <rect x="116" y="218" width="1048" height="284" rx="2" fill="none" stroke="#00d7ff" stroke-width="2.4" opacity="0.75" filter="url(#neonGlow)"/>
  <rect x="116" y="218" width="1048" height="284" rx="2" fill="none" stroke="#7ff3ff" stroke-width="1.5" opacity="0.96"/>

  <rect x="116" y="218" width="16" height="16" fill="#00d7ff"/>
  <rect x="1148" y="218" width="16" height="16" fill="#00d7ff"/>
  <rect x="116" y="486" width="16" height="16" fill="#00d7ff"/>
  <rect x="1148" y="486" width="16" height="16" fill="#00d7ff"/>

  <rect x="154" y="250" width="46" height="3" fill="#8af7ff" opacity="0.9"/>
  <rect x="1080" y="250" width="46" height="3" fill="#8af7ff" opacity="0.9"/>
  <rect x="154" y="468" width="46" height="3" fill="#8af7ff" opacity="0.9"/>
  <rect x="1080" y="468" width="46" height="3" fill="#8af7ff" opacity="0.9"/>

  <text x="640" y="280" width="760" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="600"
        letter-spacing="5" fill="#8af7ff">EXECUTIVE INTELLIGENCE BRIEF</text>

  <text x="640" y="360" width="1000" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei" font-size="62" font-weight="800"
        letter-spacing="1.5" fill="#f4fbff">GLOBAL MARKET &amp; TECH</text>

  <text x="640" y="410" width="900" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei" font-size="24" font-weight="300"
        letter-spacing="7" fill="#d9f8ff" opacity="0.88">STRATEGIC TREND OUTLOOK</text>

  <rect x="421" y="438" width="438" height="42" rx="2" fill="#00101b" opacity="0.75"/>
  <rect x="410" y="430" width="460" height="42" rx="2" fill="url(#ribbonCyan)"/>

  <text x="640" y="459" width="430" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="800"
        letter-spacing="2.8" fill="#04101b">TREND ANALYSIS REPORT 2024</text>

  <text x="640" y="548" width="620" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="400"
        letter-spacing="2" fill="#ffffff" opacity="0.58">INSIGHT GROUP · PRODUCT STRATEGY · CONFIDENTIAL</text>
</svg>
```

## Avoid in this skill
- ❌ Do not put title text directly on the photo without the translucent panel; the cover loses the “图片+色块+线框” layered mechanism.
- ❌ Do not use `<mask>` for the glass panel; use semi-transparent `<rect>` fills instead.
- ❌ Do not apply `filter` to `<line>` elements for glowing frame effects; use stroked `<rect>` or `<path>` duplicates with a blur filter.
- ❌ Do not use `<textPath>` or warped text for the headline; premium cover typography should remain crisp and editable.
- ❌ Do not overfill the panel with many small UI widgets; the method relies on a calm central reading pane.

## Composition notes
- Keep the photo full-bleed, but darken it enough that the central panel is dominant and all text remains readable.
- The translucent color block should occupy roughly the middle half of the slide height and most of the slide width, leaving a slim photo border visible.
- Inset the neon frame by 25–35 px from the panel edge; this creates the refined “designed boundary” rather than a heavy box.
- Use one vivid accent color, usually cyan, electric blue, or magenta, and repeat it in the frame, corner ticks, eyebrow text, and subtitle ribbon.