# SVG Recipe — Thematic Q&A Reveal Card (Space Aesthetic)

## Visual mechanism
A dark starfield slide is split into a left-side knowledge-check card and a right-side thematic space illustration. The answer sits inside a gold-bordered reveal container so it can be animated independently in PowerPoint while the moon, orbit arcs, and stars create a gamified trivia atmosphere.

## SVG primitives needed
- 2× `<rect>` for the full-slide space background and the answer reveal card
- 1× `<rect>` for the purple question-number tile
- 30–50× `<circle>` for deterministic editable stars of varied size and opacity
- 1× `<circle>` for the main moon body
- 5× `<ellipse>` for editable moon craters
- 3× `<path>` for soft nebula clouds behind the content
- 2× `<path>` for dashed orbital arcs around the moon
- 2× `<path>` for small decorative spacecraft / shooting-star accents
- 5× `<text>` for eyebrow label, sequence number, question prompt, answer label, and answer text
- 3× gradient definitions for background glow, answer-card depth, and moon shading
- 2× `<filter>` definitions: one soft shadow for cards/moon and one blur glow for nebula shapes

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <radialGradient id="spaceGlow" cx="72%" cy="43%" r="72%">
      <stop offset="0%" stop-color="#2A174E"/>
      <stop offset="42%" stop-color="#12172B"/>
      <stop offset="100%" stop-color="#0C0E16"/>
    </radialGradient>

    <linearGradient id="answerFill" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#24242A"/>
      <stop offset="100%" stop-color="#15151B"/>
    </linearGradient>

    <radialGradient id="moonFill" cx="34%" cy="28%" r="72%">
      <stop offset="0%" stop-color="#F0F0F0"/>
      <stop offset="55%" stop-color="#D7D7D7"/>
      <stop offset="100%" stop-color="#AFAFAF"/>
    </radialGradient>

    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="12" result="off"/>
      <feGaussianBlur in="off" stdDeviation="12" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="purpleGlow" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="18"/>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#0C0E16"/>
  <rect x="0" y="0" width="1280" height="720" fill="url(#spaceGlow)"/>

  <path d="M760 95 C850 40 1015 55 1085 150 C1145 230 1050 300 930 292 C800 284 690 200 760 95 Z"
        fill="#5A2C8D" opacity="0.22" filter="url(#purpleGlow)"/>
  <path d="M45 520 C140 450 310 470 360 560 C410 650 210 690 90 642 C15 612 -20 570 45 520 Z"
        fill="#1E6CA8" opacity="0.14" filter="url(#purpleGlow)"/>
  <path d="M930 520 C1045 460 1200 500 1245 610 C1285 710 1080 740 980 682 C910 642 865 565 930 520 Z"
        fill="#6D3AC8" opacity="0.16" filter="url(#purpleGlow)"/>

  <circle cx="54" cy="62" r="1.7" fill="#FFFFFF" opacity="0.78"/>
  <circle cx="120" cy="126" r="1.1" fill="#D8D8E8" opacity="0.62"/>
  <circle cx="215" cy="54" r="2.2" fill="#FFFFFF" opacity="0.86"/>
  <circle cx="310" cy="105" r="1.2" fill="#BFC4D8" opacity="0.60"/>
  <circle cx="422" cy="48" r="1.8" fill="#FFFFFF" opacity="0.70"/>
  <circle cx="552" cy="92" r="1.0" fill="#D8D8E8" opacity="0.55"/>
  <circle cx="650" cy="42" r="2.4" fill="#FFFFFF" opacity="0.90"/>
  <circle cx="770" cy="74" r="1.3" fill="#BFC4D8" opacity="0.66"/>
  <circle cx="910" cy="35" r="1.6" fill="#FFFFFF" opacity="0.76"/>
  <circle cx="1128" cy="82" r="2.0" fill="#FFFFFF" opacity="0.82"/>
  <circle cx="1216" cy="142" r="1.0" fill="#D8D8E8" opacity="0.58"/>
  <circle cx="98" cy="250" r="1.4" fill="#FFFFFF" opacity="0.72"/>
  <circle cx="348" cy="220" r="1.0" fill="#BFC4D8" opacity="0.50"/>
  <circle cx="522" cy="278" r="1.6" fill="#FFFFFF" opacity="0.68"/>
  <circle cx="710" cy="246" r="1.1" fill="#D8D8E8" opacity="0.54"/>
  <circle cx="829" cy="330" r="2.0" fill="#FFFFFF" opacity="0.84"/>
  <circle cx="1185" cy="286" r="1.4" fill="#BFC4D8" opacity="0.62"/>
  <circle cx="56" cy="420" r="2.1" fill="#FFFFFF" opacity="0.80"/>
  <circle cx="190" cy="512" r="1.2" fill="#D8D8E8" opacity="0.58"/>
  <circle cx="386" cy="400" r="1.5" fill="#FFFFFF" opacity="0.70"/>
  <circle cx="612" cy="458" r="1.1" fill="#BFC4D8" opacity="0.52"/>
  <circle cx="760" cy="585" r="2.3" fill="#FFFFFF" opacity="0.88"/>
  <circle cx="878" cy="650" r="1.4" fill="#D8D8E8" opacity="0.62"/>
  <circle cx="1024" cy="438" r="1.0" fill="#FFFFFF" opacity="0.56"/>
  <circle cx="1160" cy="598" r="2.0" fill="#FFFFFF" opacity="0.78"/>
  <circle cx="1240" cy="675" r="1.3" fill="#BFC4D8" opacity="0.60"/>

  <path d="M780 390 C870 205 1090 150 1195 250" fill="none" stroke="#D6B35A" stroke-width="2.5" stroke-opacity="0.65" stroke-dasharray="10 12"/>
  <path d="M820 475 C940 585 1125 570 1228 430" fill="none" stroke="#FFFFFF" stroke-width="1.4" stroke-opacity="0.34" stroke-dasharray="5 10"/>

  <circle cx="1012" cy="330" r="170" fill="url(#moonFill)" filter="url(#softShadow)"/>
  <ellipse cx="935" cy="265" rx="38" ry="34" fill="#B7B7B7" opacity="0.84"/>
  <ellipse cx="1060" cy="338" rx="54" ry="43" fill="#B2B2B2" opacity="0.86"/>
  <ellipse cx="1113" cy="250" rx="28" ry="26" fill="#BCBCBC" opacity="0.78"/>
  <ellipse cx="966" cy="422" rx="46" ry="35" fill="#B0B0B0" opacity="0.82"/>
  <ellipse cx="1102" cy="450" rx="32" ry="27" fill="#BBBBBB" opacity="0.78"/>
  <path d="M870 325 C890 215 970 155 1075 175 C980 192 910 250 885 360 Z" fill="#FFFFFF" opacity="0.18"/>

  <path d="M1138 210 l34 10 l-27 17 l-10 34 l-17 -28 l-34 -9 l28 -17 z"
        fill="#F4C95D" opacity="0.92"/>
  <path d="M715 155 C750 138 790 128 832 126" fill="none" stroke="#F4C95D" stroke-width="3" stroke-linecap="round" opacity="0.85"/>

  <rect x="96" y="214" width="112" height="148" rx="0" fill="#5A3C82" filter="url(#softShadow)"/>
  <rect x="240" y="430" width="540" height="136" rx="10" fill="url(#answerFill)" stroke="#DAA520" stroke-width="3" filter="url(#softShadow)"/>
  <rect x="240" y="410" width="92" height="4" rx="2" fill="#DAA520"/>

  <text x="96" y="164" width="520" fill="#B9B8D6"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="18" font-weight="700" letter-spacing="3">
    KNOWLEDGE CHECK
  </text>

  <text x="152" y="312" width="112" text-anchor="middle" fill="#FFFFFF"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="74" font-weight="800">
    1
  </text>

  <text x="240" y="250" width="560" fill="#FFFFFF"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="42" font-weight="800">
    <tspan x="240" dy="0">Who was the first</tspan>
    <tspan x="240" dy="54">person to walk on</tspan>
    <tspan x="240" dy="54">the moon?</tspan>
  </text>

  <text x="272" y="478" width="480" fill="#9A9AA4"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="18" font-weight="700" letter-spacing="2">
    REVEAL ANSWER
  </text>

  <text x="272" y="526" width="480" fill="#FFFFFF"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="34" font-weight="700">
    <tspan fill="#DAA520">Answer: </tspan><tspan>Neil Armstrong</tspan>
  </text>
</svg>
```

## Avoid in this skill
- ❌ Generating the starfield as a single bitmap unless you specifically need photographic noise; editable `<circle>` stars are safer and remain theme-editable in PowerPoint.
- ❌ Using `<mask>` or clipping tricks to make the moon crescent; use a simple editable highlight `<path>` overlay instead.
- ❌ Putting the answer and question into one text object if you plan to animate the answer reveal separately.
- ❌ Applying filters to `<line>` elements for orbit trails; use `<path>` strokes for dashed arcs and glow-free motion lines.
- ❌ Overcrowding the left text panel with stars behind the question; keep the reading zone darker and cleaner than the illustration zone.

## Composition notes
- Keep the left 60% of the slide reserved for the question hierarchy: eyebrow, number tile, prompt, and answer box.
- Place the moon in the right 40%, large enough to feel thematic but not so bright that it competes with the answer reveal.
- Use gold sparingly as the “interactive” color: answer border, small accent bar, and optional orbital highlights.
- For PowerPoint animation, animate the answer text or the entire answer-card group with Fade, Wipe, or letter-by-letter reveal while keeping the background static.