# SVG Recipe — Swiss International Typographic Layout

## Visual mechanism
A strict modular grid, massive left-aligned typography, and one primary-color anchor bar create an asymmetrical but highly disciplined editorial poster. The message is treated as the main graphic object, with sparse data labels and micro-rules reinforcing precision.

## SVG primitives needed
- 1× `<rect>` for the off-white slide background using a very subtle linear gradient
- 1× `<linearGradient>` for barely perceptible paper-like tonal variation
- 12× `<line>` for the visible Swiss grid, baseline guides, and separator rules
- 1× `<rect>` for the vertical red anchor bar
- 8× `<rect>` for compact data bars, small accent blocks, and proportional information strips
- 1× `<path>` for a small geometric Swiss-style plus/isotype accent
- 15× `<text>` for overline, headline, highlighted inline word, body copy, data labels, numeric emphasis, footer, and rotated metadata
- Nested `<tspan>` inside headline text for inline red emphasis

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="paper" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#FBFBF8"/>
      <stop offset="100%" stop-color="#F4F4EF"/>
    </linearGradient>
  </defs>

  <!-- background -->
  <rect x="0" y="0" width="1280" height="720" fill="url(#paper)"/>

  <!-- modular grid: visible but quiet -->
  <line x1="96" y1="72" x2="96" y2="648" stroke="#DCDCD6" stroke-width="1"/>
  <line x1="224" y1="72" x2="224" y2="648" stroke="#E7E7E1" stroke-width="1"/>
  <line x1="352" y1="72" x2="352" y2="648" stroke="#E7E7E1" stroke-width="1"/>
  <line x1="480" y1="72" x2="480" y2="648" stroke="#E7E7E1" stroke-width="1"/>
  <line x1="608" y1="72" x2="608" y2="648" stroke="#E7E7E1" stroke-width="1"/>
  <line x1="736" y1="72" x2="736" y2="648" stroke="#E7E7E1" stroke-width="1"/>
  <line x1="864" y1="72" x2="864" y2="648" stroke="#DCDCD6" stroke-width="1"/>
  <line x1="96" y1="72" x2="1184" y2="72" stroke="#DCDCD6" stroke-width="1"/>
  <line x1="96" y1="116" x2="1184" y2="116" stroke="#E7E7E1" stroke-width="1"/>
  <line x1="96" y1="318" x2="1184" y2="318" stroke="#E7E7E1" stroke-width="1"/>
  <line x1="96" y1="484" x2="1184" y2="484" stroke="#E7E7E1" stroke-width="1"/>
  <line x1="96" y1="648" x2="1184" y2="648" stroke="#DCDCD6" stroke-width="1"/>

  <!-- primary Swiss red anchor -->
  <rect x="96" y="116" width="10" height="478" fill="#DC2626"/>

  <!-- overline -->
  <text x="132" y="104" width="620" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="14" font-weight="700" letter-spacing="3" fill="#5F5F5A">
    PRODUCT PHILOSOPHY
  </text>

  <!-- massive typographic statement -->
  <text x="132" y="190" width="780" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="72" font-weight="800" letter-spacing="-2.5" fill="#141414">
    Every tool has
  </text>
  <text x="132" y="266" width="780" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="72" font-weight="800" letter-spacing="-2.5" fill="#141414">
    an opinion about
  </text>
  <text x="132" y="342" width="780" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="72" font-weight="800" letter-spacing="-2.5" fill="#141414">
    how you should
  </text>
  <text x="132" y="418" width="780" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="72" font-weight="800" letter-spacing="-2.5" fill="#141414">
    work.
  </text>
  <text x="132" y="494" width="820" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="72" font-weight="800" letter-spacing="-2.5">
    <tspan fill="#141414">This one </tspan><tspan fill="#DC2626">doesn't.</tspan>
  </text>

  <!-- body copy -->
  <text x="132" y="568" width="700" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="24" font-weight="500" letter-spacing="-0.2" fill="#2E2E2A">
    A workspace that adapts to you — not the other way around.
  </text>

  <!-- right-side information module -->
  <text x="880" y="132" width="260" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="12" font-weight="700" letter-spacing="2.5" fill="#5F5F5A">
    SYSTEM INDEX
  </text>
  <text x="880" y="266" width="260" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="152" font-weight="800" letter-spacing="-8" fill="#141414">
    01
  </text>
  <text x="1036" y="246" width="120" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="16" font-weight="700" letter-spacing="1.5" fill="#DC2626">
    NO
  </text>
  <text x="1036" y="268" width="120" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="16" font-weight="700" letter-spacing="1.5" fill="#DC2626">
    DEFAULTS
  </text>

  <!-- geometric plus/isotype -->
  <path d="M1114 82 L1134 82 L1134 102 L1154 102 L1154 122 L1134 122 L1134 142 L1114 142 L1114 122 L1094 122 L1094 102 L1114 102 Z"
        fill="#DC2626"/>

  <!-- compact data bars in Swiss style -->
  <text x="880" y="374" width="260" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="13" font-weight="700" letter-spacing="1.6" fill="#141414">
    ADAPTABILITY
  </text>
  <rect x="880" y="388" width="246" height="4" fill="#DADAD3"/>
  <rect x="880" y="388" width="226" height="4" fill="#141414"/>
  <text x="1138" y="394" width="50" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="14" font-weight="700" fill="#141414">
    92
  </text>

  <text x="880" y="434" width="260" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="13" font-weight="700" letter-spacing="1.6" fill="#141414">
    FRICTION
  </text>
  <rect x="880" y="448" width="246" height="4" fill="#DADAD3"/>
  <rect x="880" y="448" width="48" height="4" fill="#DC2626"/>
  <text x="1138" y="454" width="50" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="14" font-weight="700" fill="#DC2626">
    19
  </text>

  <text x="880" y="494" width="260" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="13" font-weight="700" letter-spacing="1.6" fill="#141414">
    CONTROL
  </text>
  <rect x="880" y="508" width="246" height="4" fill="#DADAD3"/>
  <rect x="880" y="508" width="238" height="4" fill="#141414"/>
  <text x="1138" y="514" width="50" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="14" font-weight="700" fill="#141414">
    97
  </text>

  <!-- footer and rotated metadata -->
  <line x1="132" y1="616" x2="736" y2="616" stroke="#141414" stroke-width="2"/>
  <rect x="132" y="632" width="16" height="16" fill="#DC2626"/>
  <text x="164" y="646" width="360" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="14" font-weight="700" letter-spacing="2" fill="#141414">
    CHARMIQ — 2026
  </text>
  <text x="1184" y="636" width="320" transform="rotate(-90 1184 636)"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="11" font-weight="700" letter-spacing="2.2" fill="#777770">
    INTERNATIONAL TYPOGRAPHIC SYSTEM / GRID 12
  </text>
</svg>
```

## Avoid in this skill
- ❌ Decorative shadows, glows, bevels, or glassmorphism; they undermine the Swiss objective clarity.
- ❌ Centered headline blocks; the style depends on strong left alignment and asymmetric negative space.
- ❌ Random spacing or manually “eyeballed” placement; align all elements to a visible or implied grid.
- ❌ Too many accent colors; use black/charcoal, off-white, gray, and one decisive red.
- ❌ Auto-wrapped text without explicit line breaks; Swiss typography needs deliberate line endings and tight leading.

## Composition notes
- Keep the main text block in the left 60–65% of the slide, anchored by a narrow red vertical bar.
- Preserve a generous right-side negative-space field; use it only for metadata, one large number, or compact data bars.
- Use very large, heavy sans-serif type with tight letter spacing and deliberate line breaks.
- Let the red accent appear in only a few places: anchor bar, highlighted word, small isotype, and one data cue.