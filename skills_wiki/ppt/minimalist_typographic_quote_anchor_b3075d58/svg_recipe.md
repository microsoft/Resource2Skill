# SVG Recipe — Minimalist Typographic Quote Anchor

## Visual mechanism
A huge outlined quotation mark becomes the slide’s architectural anchor, sitting like a quiet typographic sculpture on the left while the actual quote is set in bold, high-contrast text on the right. The mark has no fill and a low-opacity stroke, so it signals “quote” instantly without competing with the message.

## SVG primitives needed
- 1× `<rect>` for the off-white slide background
- 1× `<linearGradient>` for a very subtle editorial paper wash
- 1× `<filter id="softShadow">` for the faint floating quote content panel
- 1× `<rect>` for a soft white quote panel behind the main text
- 1× oversized `<text>` for the outlined quotation mark anchor
- 1× `<text>` for the small eyebrow label
- 1× `<rect>` for the short accent divider bar
- 1× `<text>` with nested `<tspan>` rows for the main quote
- 1× `<text>` for the author name
- 1× `<text>` for the author role / citation
- 2× decorative `<circle>` elements for restrained background rhythm
- 1× decorative `<path>` for a subtle abstract corner accent

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="paperWash" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="58%" stop-color="#F8F9FA"/>
      <stop offset="100%" stop-color="#EEF2F6"/>
    </linearGradient>

    <linearGradient id="slateFade" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#2D3748" stop-opacity="0.20"/>
      <stop offset="100%" stop-color="#2D3748" stop-opacity="0.04"/>
    </linearGradient>

    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feOffset dx="0" dy="18"/>
      <feGaussianBlur stdDeviation="22"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <!-- Background -->
  <rect x="0" y="0" width="1280" height="720" fill="url(#paperWash)"/>

  <!-- Quiet decorative atmosphere -->
  <circle cx="105" cy="620" r="118" fill="#2D3748" opacity="0.035"/>
  <circle cx="1180" cy="95" r="170" fill="#3B82F6" opacity="0.045"/>
  <path d="M1120,720 C1175,635 1228,590 1280,570 L1280,720 Z"
        fill="url(#slateFade)" opacity="0.45"/>

  <!-- Massive typographic quote anchor -->
  <text x="382" y="548"
        width="380"
        font-family="Georgia, serif"
        font-size="570"
        font-weight="700"
        text-anchor="end"
        fill="none"
        stroke="#2D3748"
        stroke-width="5"
        opacity="0.22">“</text>

  <!-- Right-side editorial panel -->
  <rect x="505" y="126" width="650" height="468" rx="28"
        fill="#FFFFFF" opacity="0.84" filter="url(#softShadow)"/>

  <!-- Eyebrow -->
  <text x="560" y="184"
        width="500"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="15"
        font-weight="700"
        letter-spacing="3"
        fill="#64748B">CLIENT TESTIMONIAL</text>

  <!-- Accent divider -->
  <rect x="560" y="212" width="74" height="6" rx="3" fill="#2D3748"/>

  <!-- Main quote -->
  <text x="560" y="286"
        width="535"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="43"
        font-weight="750"
        line-height="1.18"
        fill="#111827">
    <tspan x="560" dy="0">Design is not just</tspan>
    <tspan x="560" dy="54">what it looks like</tspan>
    <tspan x="560" dy="54">and feels like.</tspan>
    <tspan x="560" dy="54">Design is how it</tspan>
    <tspan x="560" dy="54">works.</tspan>
  </text>

  <!-- Author lockup -->
  <text x="560" y="535"
        width="440"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="22"
        font-weight="700"
        fill="#2D3748">Steve Jobs</text>

  <text x="560" y="566"
        width="460"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="15"
        font-weight="500"
        letter-spacing="0.4"
        fill="#64748B">Co-founder, Apple</text>
</svg>
```

## Avoid in this skill
- ❌ Don’t fill the giant quotation mark with a solid color; it becomes too heavy and competes with the quote text.
- ❌ Don’t center everything. The technique relies on asymmetric left-anchor / right-content tension.
- ❌ Don’t use `<textPath>` to curve the quote or author line; it will not translate reliably.
- ❌ Don’t use masks for the outlined mark. Use stroked text or a hand-drawn `<path>` outline instead.
- ❌ Don’t place the main quote directly over the large mark unless the mark is extremely faint.

## Composition notes
- Keep the oversized quote mark in the left 30–35% of the slide; let it slightly crop or press against the invisible center divide.
- Place the readable quote in the right 55–60% with generous margins and strong line breaks.
- Use one dark neutral as both the quote-mark stroke and the main type color for a premium editorial feel.
- The author block should be visually secondary: smaller, lower, and separated by a short divider or whitespace.