# SVG Recipe — Minimal Bullet List

## Visual mechanism
A low-density editorial slide: one clean title, a narrow accent spine, and a spacious vertical list where each bullet is treated like a calm typographic line rather than a heavy card. Subtle background gradients and tiny status dots create hierarchy without clutter.

## SVG primitives needed
- 1× `<rect>` for the full-slide warm off-white background
- 1× `<rect>` with gradient fill for a slim vertical accent spine
- 1× `<path>` for a soft decorative ambient color field in the upper-right
- 1× `<filter id="softBlur">` applied to the ambient path for a premium glow
- 1× `<filter id="cardShadow">` applied to the active bullet row highlight
- 1× `<rect>` for a very subtle active bullet highlight strip
- 5× `<circle>` for bullet dots, with the active item emphasized
- 5× `<text>` groups for bullet copy
- 1× `<text>` for the slide title
- 1× `<text>` for the short contextual eyebrow/subtitle
- 4× `<line>` for delicate separators between bullet rows

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgWash" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#FAFAF7"/>
      <stop offset="55%" stop-color="#F7F5F0"/>
      <stop offset="100%" stop-color="#EEF4F7"/>
    </linearGradient>

    <linearGradient id="accentSpine" x1="0" y1="120" x2="0" y2="600" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#2F80ED"/>
      <stop offset="52%" stop-color="#15B8A6"/>
      <stop offset="100%" stop-color="#B6E3D4"/>
    </linearGradient>

    <radialGradient id="auraFill" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#4DA3FF" stop-opacity="0.28"/>
      <stop offset="58%" stop-color="#6DE0C5" stop-opacity="0.14"/>
      <stop offset="100%" stop-color="#FFFFFF" stop-opacity="0"/>
    </radialGradient>

    <filter id="softBlur" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="36"/>
    </filter>

    <filter id="cardShadow" x="-20%" y="-50%" width="140%" height="220%">
      <feOffset dx="0" dy="10"/>
      <feGaussianBlur stdDeviation="18"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgWash)"/>

  <path d="M875 28 C1000 -20 1165 20 1236 116 C1309 214 1236 330 1102 356 C956 384 825 314 800 210 C780 126 802 61 875 28 Z"
        fill="url(#auraFill)" filter="url(#softBlur)"/>

  <rect x="96" y="118" width="6" height="484" rx="3" fill="url(#accentSpine)"/>

  <text x="138" y="142" width="780" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="18" font-weight="600" letter-spacing="2.5" fill="#5B6773">
    PRODUCT OPERATING PRINCIPLES
  </text>

  <text x="136" y="206" width="840" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="46" font-weight="700" fill="#172033">
    Keep the system simple
  </text>

  <text x="138" y="246" width="760" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="18" font-weight="400" fill="#667085">
    Five rules for turning complex work into clear executive decisions.
  </text>

  <rect x="132" y="304" width="850" height="76" rx="22" fill="#FFFFFF" opacity="0.78" filter="url(#cardShadow)"/>
  <circle cx="166" cy="342" r="7" fill="#2F80ED"/>
  <text x="194" y="335" width="700" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="24" font-weight="650" fill="#172033">
    Lead with the outcome
    <tspan x="194" dy="26" font-size="15" font-weight="400" fill="#788392">
      State the decision first, then reveal only the evidence that changes it.
    </tspan>
  </text>

  <line x1="194" y1="414" x2="938" y2="414" stroke="#D9DEE7" stroke-width="1"/>
  <circle cx="166" cy="454" r="5" fill="#15B8A6"/>
  <text x="194" y="462" width="720" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="23" font-weight="500" fill="#2D3748">
    Use one metric as the anchor for the conversation
  </text>

  <line x1="194" y1="492" x2="938" y2="492" stroke="#D9DEE7" stroke-width="1"/>
  <circle cx="166" cy="532" r="5" fill="#15B8A6" opacity="0.78"/>
  <text x="194" y="540" width="720" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="23" font-weight="500" fill="#2D3748">
    Remove anything that does not affect the next action
  </text>

  <line x1="194" y1="570" x2="938" y2="570" stroke="#D9DEE7" stroke-width="1"/>
  <circle cx="166" cy="610" r="5" fill="#15B8A6" opacity="0.56"/>
  <text x="194" y="618" width="720" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="23" font-weight="500" fill="#2D3748">
    Let whitespace signal confidence, not missing content
  </text>

  <line x1="194" y1="648" x2="938" y2="648" stroke="#D9DEE7" stroke-width="1"/>
  <circle cx="166" cy="688" r="5" fill="#15B8A6" opacity="0.38"/>
  <text x="194" y="696" width="720" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="23" font-weight="500" fill="#2D3748">
    End with a crisp owner, date, and trade-off
  </text>
</svg>
```

## Avoid in this skill
- ❌ Dense bullet paragraphs; this style depends on short, scannable lines.
- ❌ Heavy boxes around every bullet; use only one active-row highlight or no card at all.
- ❌ Decorative icons for every item; they compete with the minimal typographic rhythm.
- ❌ Centered bullet text; left alignment is essential for executive readability.
- ❌ Applying filters to `<line>` separators; shadows and blur should stay on rects, paths, circles, or text.

## Composition notes
- Keep the list in the left two-thirds of the slide; leave the right side mostly open for negative space and ambient color.
- Use 4–6 bullets maximum, with generous vertical spacing and one optional highlighted “current” bullet.
- Treat color as a rhythm: one strong accent dot, then progressively quieter dots or separators.
- Title and bullets should share the same left edge; the accent spine creates structure without adding visual noise.