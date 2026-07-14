# SVG Recipe — Sequential Chevron Tabs (Accordion Process Layout)

## Visual mechanism
A row of tall overlapping chevron panels creates a left-to-right sequence, with each tab casting a soft rightward shadow onto the next tab to imply stacked paper depth. Large translucent step letters and compact text blocks sit inside each panel, turning the entire slide into a process diagram rather than a chart.

## SVG primitives needed
- 1× `<rect>` for the dark slide background
- 5× `<path>` for the full-height chevron tab panels, drawn right-to-left so the leftmost tab sits on top
- 5× `<linearGradient>` for subtle vertical/diagonal color variation inside each tab
- 1× `<filter id="tabShadow">` using `feOffset + feGaussianBlur + feMerge`, applied to each chevron path
- 5× `<path>` for semi-transparent edge highlights on each chevron point
- 5× `<circle>` for small icon badges
- 5× decorative `<path>` icons inside the badges
- 15× `<text>` elements for large step letters, tab titles, and multiline body copy
- 1× `<text>` slide eyebrow label for optional context

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#11384F"/>
      <stop offset="0.55" stop-color="#082B42"/>
      <stop offset="1" stop-color="#061A2A"/>
    </linearGradient>

    <linearGradient id="tab1" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#8BEAF6"/>
      <stop offset="1" stop-color="#51CFE4"/>
    </linearGradient>
    <linearGradient id="tab2" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#58D0EE"/>
      <stop offset="1" stop-color="#22A9D3"/>
    </linearGradient>
    <linearGradient id="tab3" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#22B1D8"/>
      <stop offset="1" stop-color="#1186BD"/>
    </linearGradient>
    <linearGradient id="tab4" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#137FB9"/>
      <stop offset="1" stop-color="#0E5F91"/>
    </linearGradient>
    <linearGradient id="tab5" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#0C5D86"/>
      <stop offset="1" stop-color="#083C62"/>
    </linearGradient>

    <filter id="tabShadow" x="-5%" y="-5%" width="125%" height="110%">
      <feOffset in="SourceAlpha" dx="14" dy="0" result="offset"/>
      <feGaussianBlur in="offset" stdDeviation="9" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bg)"/>

  <!-- Back-to-front chevron stack: rightmost first, leftmost last -->
  <path d="M1024 0 L1280 0 L1348 360 L1280 720 L1024 720 Z" fill="url(#tab5)" filter="url(#tabShadow)"/>
  <path d="M768 0 L1024 0 L1092 360 L1024 720 L768 720 Z" fill="url(#tab4)" filter="url(#tabShadow)"/>
  <path d="M512 0 L768 0 L836 360 L768 720 L512 720 Z" fill="url(#tab3)" filter="url(#tabShadow)"/>
  <path d="M256 0 L512 0 L580 360 L512 720 L256 720 Z" fill="url(#tab2)" filter="url(#tabShadow)"/>
  <path d="M0 0 L256 0 L324 360 L256 720 L0 720 Z" fill="url(#tab1)" filter="url(#tabShadow)"/>

  <!-- Chevron point highlights -->
  <path d="M256 0 L324 360 L256 720 L236 720 L304 360 L236 0 Z" fill="#FFFFFF" opacity="0.14"/>
  <path d="M512 0 L580 360 L512 720 L492 720 L560 360 L492 0 Z" fill="#FFFFFF" opacity="0.10"/>
  <path d="M768 0 L836 360 L768 720 L748 720 L816 360 L748 0 Z" fill="#FFFFFF" opacity="0.08"/>
  <path d="M1024 0 L1092 360 L1024 720 L1004 720 L1072 360 L1004 0 Z" fill="#FFFFFF" opacity="0.07"/>
  <path d="M1280 0 L1348 360 L1280 720 L1260 720 L1328 360 L1260 0 Z" fill="#FFFFFF" opacity="0.06"/>

  <text x="40" y="46" width="420" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="18" font-weight="700" letter-spacing="3" fill="#DFFBFF" opacity="0.75">OPERATING MODEL ROADMAP</text>

  <!-- Step A -->
  <text x="38" y="154" width="160" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="112" font-weight="800" fill="#FFFFFF" opacity="0.38">A</text>
  <circle cx="82" cy="236" r="28" fill="#FFFFFF" opacity="0.22"/>
  <path d="M70 236 L80 246 L96 226" fill="none" stroke="#FFFFFF" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/>
  <text x="38" y="320" width="170" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="26" font-weight="800" fill="#FFFFFF" letter-spacing="1">DISCOVER</text>
  <text x="38" y="370" width="180" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="17" fill="#EAFDFF">
    <tspan x="38" dy="0">Clarify the ambition,</tspan>
    <tspan x="38" dy="26">audience needs, and</tspan>
    <tspan x="38" dy="26">success criteria.</tspan>
  </text>

  <!-- Step B -->
  <text x="330" y="154" width="140" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="112" font-weight="800" fill="#FFFFFF" opacity="0.32">B</text>
  <circle cx="374" cy="236" r="28" fill="#FFFFFF" opacity="0.20"/>
  <path d="M362 236 L386 236 M374 224 L374 248" fill="none" stroke="#FFFFFF" stroke-width="7" stroke-linecap="round"/>
  <text x="330" y="320" width="150" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="26" font-weight="800" fill="#FFFFFF" letter-spacing="1">MAP</text>
  <text x="330" y="370" width="158" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="17" fill="#EAFDFF">
    <tspan x="330" dy="0">Sequence the core</tspan>
    <tspan x="330" dy="26">journey, handoffs,</tspan>
    <tspan x="330" dy="26">and decision gates.</tspan>
  </text>

  <!-- Step C -->
  <text x="586" y="154" width="140" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="112" font-weight="800" fill="#FFFFFF" opacity="0.28">C</text>
  <circle cx="630" cy="236" r="28" fill="#FFFFFF" opacity="0.18"/>
  <path d="M618 247 L630 221 L642 247 Z" fill="none" stroke="#FFFFFF" stroke-width="7" stroke-linejoin="round"/>
  <text x="586" y="320" width="150" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="26" font-weight="800" fill="#FFFFFF" letter-spacing="1">BUILD</text>
  <text x="586" y="370" width="158" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="17" fill="#EAFDFF">
    <tspan x="586" dy="0">Prototype the offers,</tspan>
    <tspan x="586" dy="26">tools, rituals, and</tspan>
    <tspan x="586" dy="26">operating cadence.</tspan>
  </text>

  <!-- Step D -->
  <text x="842" y="154" width="140" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="112" font-weight="800" fill="#FFFFFF" opacity="0.24">D</text>
  <circle cx="886" cy="236" r="28" fill="#FFFFFF" opacity="0.17"/>
  <path d="M874 246 C884 220, 896 220, 898 246 M874 246 L898 246" fill="none" stroke="#FFFFFF" stroke-width="7" stroke-linecap="round"/>
  <text x="842" y="320" width="150" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="26" font-weight="800" fill="#FFFFFF" letter-spacing="1">LAUNCH</text>
  <text x="842" y="370" width="158" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="17" fill="#EAFDFF">
    <tspan x="842" dy="0">Activate the field</tspan>
    <tspan x="842" dy="26">with a focused pilot</tspan>
    <tspan x="842" dy="26">and feedback loop.</tspan>
  </text>

  <!-- Step E -->
  <text x="1098" y="154" width="140" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="112" font-weight="800" fill="#FFFFFF" opacity="0.22">E</text>
  <circle cx="1142" cy="236" r="28" fill="#FFFFFF" opacity="0.16"/>
  <path d="M1130 246 L1130 230 L1142 238 L1154 220 L1154 246 Z" fill="none" stroke="#FFFFFF" stroke-width="7" stroke-linejoin="round"/>
  <text x="1098" y="320" width="150" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="26" font-weight="800" fill="#FFFFFF" letter-spacing="1">SCALE</text>
  <text x="1098" y="370" width="158" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="17" fill="#EAFDFF">
    <tspan x="1098" dy="0">Codify repeatable</tspan>
    <tspan x="1098" dy="26">plays and expand</tspan>
    <tspan x="1098" dy="26">across the system.</tspan>
  </text>
</svg>
```

## Avoid in this skill
- ❌ Drawing the tabs left-to-right; that places the right tabs on top and destroys the stacked accordion illusion.
- ❌ Using `marker-end` arrows to imply flow; the chevron geometry itself should create direction.
- ❌ Applying `filter` to `<line>` elements for shadows; use shadowed `<path>` panels instead.
- ❌ Reusing a chevron with `<use>`; duplicate the path coordinates so the PPTX remains reliable and editable.
- ❌ Omitting explicit `width` on text; every `<text>` needs a width for clean PowerPoint rendering.

## Composition notes
- Keep the chevron point around 20–30% of a tab’s rectangular width; too small feels like a bevel, too large steals text space.
- Draw the darkest tab at the back/right and the lightest at the front/left for a natural depth gradient.
- Place body copy away from the chevron tips; titles and icons should live in the flatter rectangular zone of each tab.
- Use large semi-transparent letters as texture, not primary content; they add hierarchy without competing with the step titles.