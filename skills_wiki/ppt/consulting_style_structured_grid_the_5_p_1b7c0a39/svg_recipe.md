# SVG Recipe — Consulting-Style Structured Grid (The 5-Principle Layout)

## Visual mechanism
A premium consulting grid is built from generous whitespace, strict alignment, clear hierarchy, tight proximity within content groups, and balanced column widths. This recipe frames a clean three-column business slide as the central artifact, then adds executive-keynote annotations that call out “Space,” “Alignment,” and “Proximity.”

## SVG primitives needed
- 2× `<rect>` for the dark backdrop and white consulting slide card
- 1× `<rect>` for the thin header divider inside the card
- 3× `<rect>` for faint column zones that reveal the invisible grid
- 4× `<line>` for vertical alignment guides and small icon strokes
- 3× `<circle>` / `<ellipse>` for numbered accent badges and a red proximity callout
- 12× `<path>` for hand-drawn red arrows, arrowheads, icon illustrations, and subtle decorative accents
- 18× `<text>` with explicit `width` for the annotation labels, slide title, column headers, body copy, captions, and footer
- 1× `<linearGradient>` for the dark executive-stage background
- 1× `<filter id="softShadow">` applied to the central card
- 1× `<filter id="redGlow">` applied to red annotation strokes for presenter-style emphasis

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="navyBg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#031126"/>
      <stop offset="48%" stop-color="#05284c"/>
      <stop offset="100%" stop-color="#00101f"/>
    </linearGradient>
    <linearGradient id="tealFade" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#00A0B0" stop-opacity="0.95"/>
      <stop offset="100%" stop-color="#2DB7C4" stop-opacity="0.25"/>
    </linearGradient>
    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="12" in="SourceAlpha" result="off"/>
      <feGaussianBlur in="off" stdDeviation="14" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="redGlow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="2.2" result="glow"/>
      <feMerge>
        <feMergeNode in="glow"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#navyBg)"/>
  <ellipse cx="910" cy="355" rx="370" ry="245" fill="#0A4F83" opacity="0.16"/>
  <ellipse cx="1080" cy="225" rx="260" ry="190" fill="#0E6FA8" opacity="0.10"/>

  <text x="218" y="114" width="310" font-family="Georgia, 'Times New Roman', serif" font-size="66" font-weight="700" fill="#FFFFFF" letter-spacing="1">SPACE</text>
  <text x="560" y="134" width="500" font-family="Georgia, 'Times New Roman', serif" font-size="60" font-weight="700" fill="#FFFFFF" letter-spacing="1">ALIGNMENT</text>
  <text x="338" y="656" width="460" font-family="Georgia, 'Times New Roman', serif" font-size="62" font-weight="700" fill="#FFFFFF" letter-spacing="1">PROXIMITY</text>

  <rect x="74" y="181" width="690" height="389" rx="2" fill="#FFFFFF" filter="url(#softShadow)"/>
  <rect x="108" y="262" width="622" height="1.5" fill="#DCE2E8"/>

  <text x="108" y="230" width="600" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="20" font-weight="700" fill="#2C7FD0">
    Consumption of digital services remains strong
  </text>
  <text x="503" y="230" width="210" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="18" fill="#172033">
    more than a year
  </text>
  <text x="108" y="254" width="610" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="18" fill="#172033">
    after the pandemic started — a trend that will likely continue
  </text>

  <text x="304" y="298" width="210" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="11" font-weight="700" fill="#2C7FD0">
    Top 3 drivers
  </text>
  <text x="379" y="298" width="270" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="11" fill="#5A646E">
    of digital service consumption
  </text>

  <rect x="124" y="318" width="158" height="170" rx="8" fill="#F7FAFC" opacity="0.35"/>
  <rect x="364" y="318" width="158" height="170" rx="8" fill="#F7FAFC" opacity="0.35"/>
  <rect x="604" y="318" width="126" height="170" rx="8" fill="#F7FAFC" opacity="0.35"/>

  <circle cx="202" cy="357" r="15" fill="url(#tealFade)" opacity="0.75"/>
  <path d="M184 362 C192 354,198 347,205 339 C213 349,220 356,228 351 C235 347,239 340,244 334" fill="none" stroke="#2C7FD0" stroke-width="2"/>
  <path d="M240 334 L247 333 L245 340" fill="none" stroke="#2C7FD0" stroke-width="2"/>
  <text x="141" y="409" width="130" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" font-weight="700" text-anchor="middle" fill="#202A35">Continued adoption</text>
  <text x="132" y="452" width="145" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="12" text-anchor="middle" fill="#69737D">The internet economy continues to attract new consumers even a year after the pandemic began</text>

  <path d="M397 363 L455 363 L455 325 L397 325 Z" fill="none" stroke="#2C7FD0" stroke-width="2"/>
  <path d="M389 369 L464 369" fill="none" stroke="#2C7FD0" stroke-width="2"/>
  <circle cx="438" cy="325" r="2.5" fill="#FFC83D"/>
  <path d="M421 360 C421 348,431 347,433 358 C437 344,449 344,449 357 C456 352,465 356,462 365 C458 377,444 378,435 373 C429 381,420 376,421 360 Z" fill="#FFFFFF" stroke="#2C7FD0" stroke-width="2"/>
  <text x="373" y="409" width="140" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" font-weight="700" text-anchor="middle" fill="#202A35">Deeper usage</text>
  <text x="352" y="452" width="170" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="12" text-anchor="middle" fill="#69737D">The internet economy has seen increased spend and frequency of use amongst existing consumers</text>

  <circle cx="632" cy="357" r="15" fill="url(#tealFade)" opacity="0.75"/>
  <path d="M632 340 L632 374 M615 357 L649 357" stroke="#2C7FD0" stroke-width="2" fill="none"/>
  <path d="M650 326 L655 333 L663 336 L655 340 L651 348 L647 340 L639 336 L647 332 Z" fill="none" stroke="#2C7FD0" stroke-width="1.8"/>
  <path d="M667 350 L671 354 L676 356 L671 359 L669 364 L665 359 L660 357 L665 354 Z" fill="none" stroke="#2C7FD0" stroke-width="1.5"/>
  <text x="577" y="409" width="125" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" font-weight="700" text-anchor="middle" fill="#202A35">New way of life</text>
  <text x="575" y="452" width="128" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="12" text-anchor="middle" fill="#69737D">New consumer behaviour is not a one-off phenomenon — users are highly satisfied and intend to continue</text>

  <text x="108" y="540" width="430" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="6.8" fill="#6B7580">
    Source: illustrative research summary. Note: small footer kept close to source line to demonstrate proximity and grouping.
  </text>
  <text x="570" y="542" width="160" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="7" fill="#7A838D">GOOGLE    TEMASEK    BAIN & COMPANY</text>

  <ellipse cx="205" cy="292" rx="72" ry="43" fill="none" stroke="#E60012" stroke-width="4"/>
  <path d="M302 128 C252 158,224 196,214 244" fill="none" stroke="#FF2030" stroke-width="6" stroke-linecap="round" filter="url(#redGlow)"/>
  <path d="M211 244 L198 204 M211 244 L236 218" fill="none" stroke="#FF2030" stroke-width="6" stroke-linecap="round"/>
  <path d="M765 158 C742 208,700 251,652 276" fill="none" stroke="#FF2030" stroke-width="6" stroke-linecap="round" filter="url(#redGlow)"/>
  <path d="M652 276 L681 233 M652 276 L701 270" fill="none" stroke="#FF2030" stroke-width="6" stroke-linecap="round"/>
  <line x1="629" y1="259" x2="629" y2="530" stroke="#E60012" stroke-width="7" stroke-dasharray="12 8"/>
  <path d="M327 633 C266 621,206 590,193 558" fill="none" stroke="#FF2030" stroke-width="6" stroke-linecap="round" filter="url(#redGlow)"/>
  <path d="M193 558 L222 581 M193 558 L190 596" fill="none" stroke="#FF2030" stroke-width="6" stroke-linecap="round"/>
</svg>
```

## Avoid in this skill
- ❌ Free-floating content blocks that are not snapped to a shared column grid; the layout loses its consulting-grade trust signal.
- ❌ Overdecorated cards, heavy gradients, or too many accent colors; this technique depends on restraint.
- ❌ Center-aligning body copy inside each column unless the whole design is intentionally poster-like; left alignment is usually more executive and readable.
- ❌ Using tiny text without explicit `width`; in PowerPoint translation it can clip or fail to communicate hierarchy.
- ❌ Applying filters to `<line>` elements; use filtered `<path>` strokes for glowing annotation arrows instead.

## Composition notes
- Keep a large top header zone, a single clean divider, then a three-column content grid with equal widths and generous gutters.
- Use proximity inside each column: icon close to heading, heading close to body, but columns separated by noticeably larger whitespace.
- Use navy, gray, white, and one vibrant accent color; the restrained palette makes the structure feel premium.
- If showing the design principles pedagogically, add red hand-drawn arrows and dashed guides above the finished slide, but keep the underlying grid clean and readable.