# SVG Recipe — Hyperlinked Table of Contents

## Visual mechanism
A navigation hub slide uses two clean columns of individually clickable section rows, each styled like a premium app menu item with numbering, subtle cards, link affordances, and progress/section metadata. The hyperlink behavior is represented by one editable text/group per item so PPT-Master or downstream code can attach each row to its target slide.

## SVG primitives needed
- 1× `<rect>` for the full-slide background
- 2× `<linearGradient>` for premium background and clickable-row fills
- 1× `<radialGradient>` for a soft spotlight behind the title area
- 2× `<filter>` definitions for card shadows and soft glow
- 3× decorative `<path>` shapes for abstract corner waves and motion accents
- 2× large rounded `<rect>` column panels for the ToC list areas
- 12× rounded `<rect>` row buttons for individual navigable entries
- 12× small rounded `<rect>` number badges
- 12× `<text>` number labels
- 12× `<text>` section titles, each with explicit `width`
- 12× `<text>` slide/page labels, each with explicit `width`
- 12× `<line>` underline/link affordance strokes
- 12× small `<path>` arrow/link icons
- 1× right-side rounded `<rect>` summary card
- 6× `<circle>` nodes and 5× `<line>` connectors for a miniature deck-map preview
- 1× `<text>` title and several supporting metadata labels, all with explicit `width`

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#F7FAFF"/>
      <stop offset="55%" stop-color="#EEF4FF"/>
      <stop offset="100%" stop-color="#EAF7F6"/>
    </linearGradient>
    <linearGradient id="rowGrad" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="100%" stop-color="#F5F9FF"/>
    </linearGradient>
    <linearGradient id="accentGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#1B66FF"/>
      <stop offset="100%" stop-color="#00A6A6"/>
    </linearGradient>
    <radialGradient id="spotlight" cx="30%" cy="12%" r="55%">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.95"/>
      <stop offset="100%" stop-color="#FFFFFF" stop-opacity="0"/>
    </radialGradient>
    <filter id="cardShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="10"/>
      <feGaussianBlur stdDeviation="14"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="softGlow" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="10"/>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>
  <rect x="0" y="0" width="1280" height="260" fill="url(#spotlight)"/>
  <path d="M1008,-40 C1135,20 1188,100 1328,62 L1328,0 L1008,0 Z" fill="#D9E8FF" opacity="0.65"/>
  <path d="M-70,612 C80,560 168,652 294,604 C374,574 430,516 520,544 L520,760 L-70,760 Z" fill="#D8F3EF" opacity="0.75"/>
  <path d="M1040,642 C1112,604 1194,618 1270,570" fill="none" stroke="#1B66FF" stroke-width="3" stroke-dasharray="8 12" opacity="0.35"/>

  <text x="70" y="86" width="650" font-family="Segoe UI, Microsoft YaHei" font-size="44" font-weight="700" fill="#12213A">Table of Contents</text>
  <text x="72" y="124" width="720" font-family="Segoe UI, Microsoft YaHei" font-size="16" fill="#63708A">Select any section to jump directly to that part of the deck.</text>
  <rect x="70" y="150" width="142" height="32" rx="16" fill="#E7F0FF"/>
  <text x="92" y="172" width="120" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="600" fill="#1B66FF">12 linked sections</text>

  <rect x="70" y="210" width="500" height="430" rx="26" fill="#FFFFFF" opacity="0.88" filter="url(#cardShadow)"/>
  <rect x="610" y="210" width="500" height="430" rx="26" fill="#FFFFFF" opacity="0.88" filter="url(#cardShadow)"/>
  <text x="100" y="250" width="260" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" letter-spacing="1.8" fill="#8792A8">FOUNDATION</text>
  <text x="640" y="250" width="260" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" letter-spacing="1.8" fill="#8792A8">EXECUTION</text>

  <g id="toc-item-01" data-target-slide="slide-03">
    <rect x="98" y="272" width="444" height="48" rx="14" fill="url(#rowGrad)" stroke="#E5ECF8"/>
    <rect x="116" y="284" width="36" height="24" rx="12" fill="url(#accentGrad)"/>
    <text x="126" y="302" width="24" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#FFFFFF">01</text>
    <text x="168" y="302" width="260" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="600" fill="#14233F">Executive summary</text>
    <text x="440" y="302" width="54" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#7B879A">p. 03</text>
    <line x1="168" y1="309" x2="306" y2="309" stroke="#1B66FF" stroke-width="1.4" opacity="0.55"/>
    <path d="M514 291 L524 296 L514 301 M505 296 L523 296" fill="none" stroke="#1B66FF" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
  </g>

  <g id="toc-item-02" data-target-slide="slide-05">
    <rect x="98" y="332" width="444" height="48" rx="14" fill="url(#rowGrad)" stroke="#E5ECF8"/>
    <rect x="116" y="344" width="36" height="24" rx="12" fill="#EAF1FF"/>
    <text x="126" y="362" width="24" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#1B66FF">02</text>
    <text x="168" y="362" width="270" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="600" fill="#14233F">Market landscape</text>
    <text x="440" y="362" width="54" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#7B879A">p. 05</text>
    <line x1="168" y1="369" x2="293" y2="369" stroke="#1B66FF" stroke-width="1.4" opacity="0.45"/>
    <path d="M514 351 L524 356 L514 361 M505 356 L523 356" fill="none" stroke="#1B66FF" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
  </g>

  <g id="toc-item-03" data-target-slide="slide-08">
    <rect x="98" y="392" width="444" height="48" rx="14" fill="url(#rowGrad)" stroke="#E5ECF8"/>
    <rect x="116" y="404" width="36" height="24" rx="12" fill="#EAF1FF"/>
    <text x="126" y="422" width="24" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#1B66FF">03</text>
    <text x="168" y="422" width="280" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="600" fill="#14233F">Customer insights</text>
    <text x="440" y="422" width="54" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#7B879A">p. 08</text>
    <line x1="168" y1="429" x2="302" y2="429" stroke="#1B66FF" stroke-width="1.4" opacity="0.45"/>
    <path d="M514 411 L524 416 L514 421 M505 416 L523 416" fill="none" stroke="#1B66FF" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
  </g>

  <g id="toc-item-04" data-target-slide="slide-11">
    <rect x="98" y="452" width="444" height="48" rx="14" fill="url(#rowGrad)" stroke="#E5ECF8"/>
    <rect x="116" y="464" width="36" height="24" rx="12" fill="#EAF1FF"/>
    <text x="126" y="482" width="24" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#1B66FF">04</text>
    <text x="168" y="482" width="290" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="600" fill="#14233F">Product strategy</text>
    <text x="440" y="482" width="54" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#7B879A">p. 11</text>
    <line x1="168" y1="489" x2="290" y2="489" stroke="#1B66FF" stroke-width="1.4" opacity="0.45"/>
    <path d="M514 471 L524 476 L514 481 M505 476 L523 476" fill="none" stroke="#1B66FF" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
  </g>

  <g id="toc-item-05" data-target-slide="slide-14">
    <rect x="98" y="512" width="444" height="48" rx="14" fill="url(#rowGrad)" stroke="#E5ECF8"/>
    <rect x="116" y="524" width="36" height="24" rx="12" fill="#EAF1FF"/>
    <text x="126" y="542" width="24" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#1B66FF">05</text>
    <text x="168" y="542" width="292" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="600" fill="#14233F">Experience principles</text>
    <text x="440" y="542" width="54" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#7B879A">p. 14</text>
    <line x1="168" y1="549" x2="330" y2="549" stroke="#1B66FF" stroke-width="1.4" opacity="0.45"/>
    <path d="M514 531 L524 536 L514 541 M505 536 L523 536" fill="none" stroke="#1B66FF" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
  </g>

  <g id="toc-item-06" data-target-slide="slide-17">
    <rect x="98" y="572" width="444" height="48" rx="14" fill="url(#rowGrad)" stroke="#E5ECF8"/>
    <rect x="116" y="584" width="36" height="24" rx="12" fill="#EAF1FF"/>
    <text x="126" y="602" width="24" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#1B66FF">06</text>
    <text x="168" y="602" width="292" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="600" fill="#14233F">Solution architecture</text>
    <text x="440" y="602" width="54" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#7B879A">p. 17</text>
    <line x1="168" y1="609" x2="326" y2="609" stroke="#1B66FF" stroke-width="1.4" opacity="0.45"/>
    <path d="M514 591 L524 596 L514 601 M505 596 L523 596" fill="none" stroke="#1B66FF" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
  </g>

  <g id="toc-item-07" data-target-slide="slide-20">
    <rect x="638" y="272" width="444" height="48" rx="14" fill="url(#rowGrad)" stroke="#E5ECF8"/>
    <rect x="656" y="284" width="36" height="24" rx="12" fill="url(#accentGrad)"/>
    <text x="666" y="302" width="24" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#FFFFFF">07</text>
    <text x="708" y="302" width="272" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="600" fill="#14233F">Implementation roadmap</text>
    <text x="980" y="302" width="54" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#7B879A">p. 20</text>
    <line x1="708" y1="309" x2="890" y2="309" stroke="#1B66FF" stroke-width="1.4" opacity="0.55"/>
    <path d="M1054 291 L1064 296 L1054 301 M1045 296 L1063 296" fill="none" stroke="#1B66FF" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
  </g>

  <g id="toc-item-08" data-target-slide="slide-23">
    <rect x="638" y="332" width="444" height="48" rx="14" fill="url(#rowGrad)" stroke="#E5ECF8"/>
    <rect x="656" y="344" width="36" height="24" rx="12" fill="#EAF1FF"/>
    <text x="666" y="362" width="24" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#1B66FF">08</text>
    <text x="708" y="362" width="272" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="600" fill="#14233F">Operating model</text>
    <text x="980" y="362" width="54" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#7B879A">p. 23</text>
    <line x1="708" y1="369" x2="826" y2="369" stroke="#1B66FF" stroke-width="1.4" opacity="0.45"/>
    <path d="M1054 351 L1064 356 L1054 361 M1045 356 L1063 356" fill="none" stroke="#1B66FF" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
  </g>

  <g id="toc-item-09" data-target-slide="slide-26">
    <rect x="638" y="392" width="444" height="48" rx="14" fill="url(#rowGrad)" stroke="#E5ECF8"/>
    <rect x="656" y="404" width="36" height="24" rx="12" fill="#EAF1FF"/>
    <text x="666" y="422" width="24" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#1B66FF">09</text>
    <text x="708" y="422" width="272" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="600" fill="#14233F">Financial outlook</text>
    <text x="980" y="422" width="54" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#7B879A">p. 26</text>
    <line x1="708" y1="429" x2="830" y2="429" stroke="#1B66FF" stroke-width="1.4" opacity="0.45"/>
    <path d="M1054 411 L1064 416 L1054 421 M1045 416 L1063 416" fill="none" stroke="#1B66FF" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
  </g>

  <g id="toc-item-10" data-target-slide="slide-29">
    <rect x="638" y="452" width="444" height="48" rx="14" fill="url(#rowGrad)" stroke="#E5ECF8"/>
    <rect x="656" y="464" width="36" height="24" rx="12" fill="#EAF1FF"/>
    <text x="666" y="482" width="24" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#1B66FF">10</text>
    <text x="708" y="482" width="272" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="600" fill="#14233F">Risk register</text>
    <text x="980" y="482" width="54" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#7B879A">p. 29</text>
    <line x1="708" y1="489" x2="804" y2="489" stroke="#1B66FF" stroke-width="1.4" opacity="0.45"/>
    <path d="M1054 471 L1064 476 L1054 481 M1045 476 L1063 476" fill="none" stroke="#1B66FF" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
  </g>

  <g id="toc-item-11" data-target-slide="slide-32">
    <rect x="638" y="512" width="444" height="48" rx="14" fill="url(#rowGrad)" stroke="#E5ECF8"/>
    <rect x="656" y="524" width="36" height="24" rx="12" fill="#EAF1FF"/>
    <text x="666" y="542" width="24" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#1B66FF">11</text>
    <text x="708" y="542" width="272" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="600" fill="#14233F">Decision requirements</text>
    <text x="980" y="542" width="54" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#7B879A">p. 32</text>
    <line x1="708" y1="549" x2="872" y2="549" stroke="#1B66FF" stroke-width="1.4" opacity="0.45"/>
    <path d="M1054 531 L1064 536 L1054 541 M1045 536 L1063 536" fill="none" stroke="#1B66FF" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
  </g>

  <g id="toc-item-12" data-target-slide="slide-35">
    <rect x="638" y="572" width="444" height="48" rx="14" fill="url(#rowGrad)" stroke="#E5ECF8"/>
    <rect x="656" y="584" width="36" height="24" rx="12" fill="#EAF1FF"/>
    <text x="666" y="602" width="24" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#1B66FF">12</text>
    <text x="708" y="602" width="272" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="600" fill="#14233F">Appendix and references</text>
    <text x="980" y="602" width="54" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#7B879A">p. 35</text>
    <line x1="708" y1="609" x2="880" y2="609" stroke="#1B66FF" stroke-width="1.4" opacity="0.45"/>
    <path d="M1054 591 L1064 596 L1054 601 M1045 596 L1063 596" fill="none" stroke="#1B66FF" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
  </g>

  <rect x="1130" y="210" width="92" height="430" rx="24" fill="#10213D" opacity="0.96" filter="url(#cardShadow)"/>
  <text x="1154" y="252" width="54" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#AFC7FF">MAP</text>
  <line x1="1176" y1="304" x2="1176" y2="568" stroke="#5D7196" stroke-width="2"/>
  <circle cx="1176" cy="304" r="10" fill="#1B66FF" filter="url(#softGlow)"/>
  <circle cx="1176" cy="356" r="7" fill="#8FB2FF"/>
  <circle cx="1176" cy="408" r="7" fill="#8FB2FF"/>
  <circle cx="1176" cy="460" r="7" fill="#8FB2FF"/>
  <circle cx="1176" cy="512" r="7" fill="#8FB2FF"/>
  <circle cx="1176" cy="568" r="10" fill="#00A6A6"/>
  <text x="1148" y="614" width="60" font-family="Segoe UI, Microsoft YaHei" font-size="11" font-weight="600" fill="#DDE8FF">click to jump</text>
</svg>
```

## Avoid in this skill
- ❌ Do not make the ToC one giant text box if hyperlinks must target different slides; use one row/group/text element per navigable entry.
- ❌ Do not rely only on default blue underlined text; add row cards, number badges, arrows, and metadata so the slide feels intentional rather than auto-generated.
- ❌ Do not use SVG `<a>` wrappers as the only hyperlink mechanism unless your PPT-Master pipeline explicitly maps them to PowerPoint hyperlinks; prefer attaching slide links to each generated row/text shape after conversion.
- ❌ Do not use `marker-end` for row arrows; draw arrowheads as small editable `<path>` shapes.
- ❌ Do not overcrowd with every slide in a long deck; link to section-divider slides or create paginated ToC slides for very large decks.

## Composition notes
- Keep the title and navigation instruction in the upper-left 20% of the slide; this establishes the slide as an interactive menu before the viewer scans the entries.
- Use two balanced columns for 8–16 entries; for more entries, reduce vertical padding slightly or split into “Part 1 / Part 2” ToC slides.
- Make each ToC item a distinct visual hit target: 44–56 px row height, clear left number badge, title, page label, and small arrow on the right.
- Use hyperlink blue sparingly as an affordance, while the main typography remains dark slate for executive polish.