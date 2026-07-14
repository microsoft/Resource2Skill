# SVG Recipe — Layered Arc Layout

## Visual mechanism
A large dark color field is carved into the slide with a sweeping curved edge, while thinner cyan and orange arc bands peek out from behind it to create depth, motion, and a premium branded partition. The content sits in the calm negative space opposite the arcs, letting the curve act as both divider and visual guide.

## SVG primitives needed
- 1× `<rect>` for the full-slide soft gradient background
- 3× `<rect>` for small content pills / labels
- 5× `<path>` for the layered arc system: orange band, cyan band, main navy field, and subtle curved highlight strokes
- 2× `<path>` for decorative abstract background swooshes
- 5× `<circle>` for logo dots, bullet points, and accent nodes
- 2× `<ellipse>` for soft decorative halos inside the navy field
- 8× `<text>` for title, subtitle, section labels, and bullet copy
- 3× `<linearGradient>` for background, navy field, and accent bands
- 1× `<radialGradient>` for soft halo lighting
- 1× `<filter id="softShadow">` applied to the main navy arc field
- 1× `<filter id="arcGlow">` applied to the cyan/orange accent arcs

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="58%" stop-color="#F5F7FA"/>
      <stop offset="100%" stop-color="#E9EEF5"/>
    </linearGradient>

    <linearGradient id="navyGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#052E64"/>
      <stop offset="55%" stop-color="#011F54"/>
      <stop offset="100%" stop-color="#001637"/>
    </linearGradient>

    <linearGradient id="cyanGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#35D7FF"/>
      <stop offset="100%" stop-color="#0096D6"/>
    </linearGradient>

    <linearGradient id="orangeGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#F2A35A"/>
      <stop offset="100%" stop-color="#C97230"/>
    </linearGradient>

    <radialGradient id="haloGrad" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.34"/>
      <stop offset="100%" stop-color="#FFFFFF" stop-opacity="0"/>
    </radialGradient>

    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feOffset dx="-8" dy="10" result="offset"/>
      <feGaussianBlur in="offset" stdDeviation="14" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="arcGlow" x="-25%" y="-25%" width="150%" height="150%">
      <feGaussianBlur stdDeviation="5" result="glow"/>
      <feMerge>
        <feMergeNode in="glow"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>

  <path d="M-60 610 C150 560 255 670 430 620 C530 592 610 606 700 690 L-60 760 Z"
        fill="#DDE6F2" opacity="0.48"/>
  <path d="M-40 84 C150 118 260 34 440 64 C535 80 612 120 684 178"
        fill="none" stroke="#D7E0EC" stroke-width="3" opacity="0.8"/>

  <path d="M612 -46 C805 116 780 266 700 394 C626 513 650 612 805 770 L704 770
           C560 624 544 509 618 383 C694 254 714 128 520 -46 Z"
        fill="url(#orangeGrad)" opacity="0.96" filter="url(#arcGlow)"/>

  <path d="M566 -46 C754 110 742 260 656 398 C584 514 610 624 765 770 L686 770
           C525 620 502 506 584 374 C660 252 668 130 488 -46 Z"
        fill="url(#cyanGrad)" opacity="0.96" filter="url(#arcGlow)"/>

  <path d="M665 -42 C840 112 812 268 732 398 C654 524 680 620 842 762
           L1308 762 L1308 -42 Z"
        fill="url(#navyGrad)" filter="url(#softShadow)"/>

  <ellipse cx="1024" cy="176" rx="245" ry="150" fill="url(#haloGrad)" opacity="0.9"/>
  <ellipse cx="1120" cy="548" rx="210" ry="118" fill="url(#haloGrad)" opacity="0.55"/>

  <path d="M724 118 C866 210 890 330 824 454 C790 516 800 584 882 660"
        fill="none" stroke="#FFFFFF" stroke-width="2.5" opacity="0.18"/>
  <path d="M788 40 C966 150 1000 304 928 444 C878 542 918 620 1056 702"
        fill="none" stroke="#30C9F4" stroke-width="3" opacity="0.32"/>

  <circle cx="1110" cy="132" r="6" fill="#35D7FF" opacity="0.9"/>
  <circle cx="1168" cy="188" r="3.5" fill="#F2A35A" opacity="0.95"/>
  <circle cx="1012" cy="616" r="5" fill="#FFFFFF" opacity="0.56"/>

  <circle cx="96" cy="86" r="22" fill="#012357"/>
  <circle cx="96" cy="86" r="9" fill="#35D7FF"/>
  <text x="132" y="93" width="240" font-family="Segoe UI, Microsoft YaHei" font-size="22" font-weight="700" fill="#012357" letter-spacing="2">
    ARC STUDIO
  </text>

  <text x="88" y="190" width="520" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="700" fill="#0096D6" letter-spacing="3">
    EXECUTIVE STRATEGY DIVIDER
  </text>

  <text x="86" y="276" width="560" font-family="Segoe UI, Microsoft YaHei" font-size="58" font-weight="800" fill="#10213D">
    <tspan x="86" dy="0">Layered Arc</tspan>
    <tspan x="86" dy="68">Growth Narrative</tspan>
  </text>

  <text x="90" y="412" width="500" font-family="Segoe UI, Microsoft YaHei" font-size="21" fill="#516174">
    A modern section opener using sweeping branded arcs to separate message, context, and visual momentum.
  </text>

  <rect x="90" y="492" width="176" height="42" rx="21" fill="#012357"/>
  <text x="119" y="520" width="130" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#FFFFFF" letter-spacing="1">
    Q3 UPDATE
  </text>

  <rect x="286" y="492" width="198" height="42" rx="21" fill="#FFFFFF" stroke="#D8E0EA" stroke-width="1.4"/>
  <text x="315" y="520" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#012357" letter-spacing="1">
    BOARD REVIEW
  </text>

  <text x="850" y="216" width="300" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#35D7FF" letter-spacing="3">
    SECTION 02
  </text>

  <text x="846" y="286" width="330" font-family="Segoe UI, Microsoft YaHei" font-size="42" font-weight="800" fill="#FFFFFF">
    Momentum by Design
  </text>

  <text x="850" y="356" width="300" font-family="Segoe UI, Microsoft YaHei" font-size="18" fill="#D7E7F6">
    The arc edge creates a natural reading path while keeping the right-side field bold and brand-owned.
  </text>

  <circle cx="862" cy="446" r="5" fill="#F2A35A"/>
  <text x="882" y="452" width="250" font-family="Segoe UI, Microsoft YaHei" font-size="16" fill="#FFFFFF">
    Use dark field for short claims
  </text>

  <circle cx="862" cy="492" r="5" fill="#35D7FF"/>
  <text x="882" y="498" width="250" font-family="Segoe UI, Microsoft YaHei" font-size="16" fill="#FFFFFF">
    Keep primary title in open space
  </text>

  <rect x="850" y="558" width="238" height="46" rx="23" fill="#FFFFFF" opacity="0.12"/>
  <text x="878" y="588" width="190" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#FFFFFF" letter-spacing="1.5">
    BRAND MOTION SYSTEM
  </text>
</svg>
```

## Avoid in this skill
- ❌ Do not rasterize the arcs as PNGs unless absolutely necessary; closed `<path>` bands remain editable in PowerPoint.
- ❌ Do not use `<mask>` or clip a non-image shape to “cut” the arcs; draw each arc as its own filled path instead.
- ❌ Do not build the layout from only giant stroked ellipses that rely on slide-edge cropping; use deliberate closed arc paths for predictable PPT editing.
- ❌ Do not apply filters to `<line>` elements; use shadows/glows on filled `<path>`, `<rect>`, `<circle>`, or `<text>` only.
- ❌ Do not use `skewX`, `skewY`, or `matrix()` transforms for dynamic arc angles; author the curve directly with Bézier path coordinates.

## Composition notes
- Reserve 45–55% of the slide as quiet negative space for the headline; the arc partition should energize the slide without crowding the title.
- Layer accent arcs behind the main dark field: orange slightly wider/farther out, cyan closer to the primary edge, then navy on top.
- Keep high-contrast text on the navy field short: section numbers, short claims, or 2–3 bullet points.
- Use restrained accent repetition: small cyan/orange dots or pills echo the arcs and make the whole slide feel intentionally branded.