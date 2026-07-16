# SVG Recipe — Simple Bullet List

## Visual mechanism
A clean title-and-list slide with each bullet rendered as its own editable row: soft card bands, numbered circular markers, and a subtle vertical progress spine make a basic list feel structured and presentation-ready. The layout preserves sequential disclosure because every bullet label is a separate `<text>` object.

## SVG primitives needed
- 1× `<rect>` for the full-slide background
- 2× `<path>` for abstract decorative gradient shapes in the corners
- 1× `<rect>` for the main content panel
- 6× `<rect>` for individual bullet row cards
- 1× `<line>` for the vertical bullet spine
- 6× `<circle>` for numbered bullet markers
- 6× `<path>` for small check accents inside the markers
- 9× `<text>` for eyebrow, headline, subtitle, and separate bullet text boxes
- 2× `<linearGradient>` for premium background/accent fills
- 1× `<radialGradient>` for ambient glow
- 1× `<filter id="cardShadow">` for soft editable shadows on panel and rows
- 1× `<filter id="softGlow">` for background accent glow

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1280" y2="720" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#081A2F"/>
      <stop offset="0.55" stop-color="#0E2A46"/>
      <stop offset="1" stop-color="#07111F"/>
    </linearGradient>

    <linearGradient id="accentGrad" x1="0" y1="0" x2="360" y2="360" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#39D5FF"/>
      <stop offset="0.55" stop-color="#6C63FF"/>
      <stop offset="1" stop-color="#FF7AC8"/>
    </linearGradient>

    <radialGradient id="ambientGlow" cx="50%" cy="50%" r="50%">
      <stop offset="0" stop-color="#39D5FF" stop-opacity="0.36"/>
      <stop offset="1" stop-color="#39D5FF" stop-opacity="0"/>
    </radialGradient>

    <filter id="cardShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="12"/>
      <feGaussianBlur stdDeviation="18"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="softGlow" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="28"/>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>

  <circle cx="1080" cy="100" r="210" fill="url(#ambientGlow)" filter="url(#softGlow)" opacity="0.85"/>
  <path d="M1015 0 C1135 24 1240 94 1280 188 L1280 0 Z" fill="url(#accentGrad)" opacity="0.42"/>
  <path d="M0 600 C95 548 198 552 278 617 C338 666 420 698 520 720 L0 720 Z" fill="url(#accentGrad)" opacity="0.18"/>

  <rect x="86" y="72" width="1108" height="576" rx="34" fill="#FFFFFF" opacity="0.96" filter="url(#cardShadow)"/>
  <rect x="86" y="72" width="10" height="576" rx="5" fill="url(#accentGrad)"/>

  <text x="132" y="126" width="320" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="14" font-weight="700" letter-spacing="2.5" fill="#5B6B7F">
    EXECUTION AGENDA
  </text>

  <text x="132" y="178" width="720" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="42" font-weight="750" fill="#10243A">
    Q3 Launch Priorities
  </text>

  <text x="134" y="214" width="780" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="18" fill="#607086">
    Six focus areas for aligning product, marketing, revenue, and customer success.
  </text>

  <line x1="178" y1="273" x2="178" y2="576" stroke="#D8E2EE" stroke-width="3" stroke-linecap="round"/>

  <rect x="132" y="246" width="1012" height="58" rx="18" fill="#F7FAFD"/>
  <circle cx="178" cy="275" r="20" fill="#10243A"/>
  <path d="M168 274 L176 282 L190 266" fill="none" stroke="#FFFFFF" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
  <text x="220" y="282" width="850" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="21" font-weight="650" fill="#162B42">
    Lock final positioning and message hierarchy for the launch narrative
  </text>

  <rect x="132" y="310" width="1012" height="58" rx="18" fill="#FFFFFF"/>
  <circle cx="178" cy="339" r="20" fill="#2E7CF6"/>
  <path d="M168 338 L176 346 L190 330" fill="none" stroke="#FFFFFF" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
  <text x="220" y="346" width="850" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="21" font-weight="650" fill="#162B42">
    Finalize pricing, packaging, and approval paths for enterprise deals
  </text>

  <rect x="132" y="374" width="1012" height="58" rx="18" fill="#F7FAFD"/>
  <circle cx="178" cy="403" r="20" fill="#6558F5"/>
  <path d="M168 402 L176 410 L190 394" fill="none" stroke="#FFFFFF" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
  <text x="220" y="410" width="850" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="21" font-weight="650" fill="#162B42">
    Build the sales enablement kit with competitive proof points
  </text>

  <rect x="132" y="438" width="1012" height="58" rx="18" fill="#FFFFFF"/>
  <circle cx="178" cy="467" r="20" fill="#00A6B4"/>
  <path d="M168 466 L176 474 L190 458" fill="none" stroke="#FFFFFF" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
  <text x="220" y="474" width="850" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="21" font-weight="650" fill="#162B42">
    Confirm launch analytics, success metrics, and executive dashboard inputs
  </text>

  <rect x="132" y="502" width="1012" height="58" rx="18" fill="#F7FAFD"/>
  <circle cx="178" cy="531" r="20" fill="#F26BAA"/>
  <path d="M168 530 L176 538 L190 522" fill="none" stroke="#FFFFFF" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
  <text x="220" y="538" width="850" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="21" font-weight="650" fill="#162B42">
    Schedule customer proof sessions and partner amplification moments
  </text>

  <rect x="132" y="566" width="1012" height="58" rx="18" fill="#FFFFFF"/>
  <circle cx="178" cy="595" r="20" fill="#FF9F1C"/>
  <path d="M168 594 L176 602 L190 586" fill="none" stroke="#FFFFFF" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
  <text x="220" y="602" width="850" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="21" font-weight="650" fill="#162B42">
    Run the final readiness review with owners, dates, and decision gates
  </text>
</svg>
```

## Avoid in this skill
- ❌ A single multi-line `<text>` object for all bullets; it prevents clean sequential reveal and makes individual bullet editing harder.
- ❌ Native SVG bullet characters only, such as “•”, without separate marker shapes; they look flat and offer less control over alignment.
- ❌ Filters on `<line>` for the vertical spine; line filters are dropped, so keep the spine simple.
- ❌ Overcrowding the list with more than 7 bullets; this shell is designed for low-density executive summaries.
- ❌ Using `<foreignObject>` for rich text wrapping; it hard-fails translation.

## Composition notes
- Keep the title block in the upper-left 25–30% of the slide; the list should begin below it with generous breathing room.
- Treat each bullet row as its own editable unit: row card, marker, icon/check, and text.
- Use alternating soft row fills to guide the eye without making the slide feel like a table.
- Reserve color intensity for the bullet markers and accent edge; the main panel should remain calm and highly legible.