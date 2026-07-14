# SVG Recipe — Rotating Wheel Bullet List

## Visual mechanism
A large mechanical wheel sits on the left as an ambient “rotating” motif, built from concentric rings, dashed arcs, spokes, and tangential labels to imply motion without actual SVG animation. The right side balances it with a crisp CTA banner, arrow-shaped subhead banner, and a four-item executive bullet list.

## SVG primitives needed
- 1× `<rect>` for the full-slide background
- 2× `<linearGradient>` for the background wash and CTA banner fill
- 2× `<radialGradient>` for the wheel face and hub glow
- 2× `<filter>` using blur/offset/merge for soft card shadows and glow
- 4× `<circle>` for wheel rings, dashed orbit strokes, center hub, and inner dial
- 8× `<line>` for spokes and accent ticks
- 6× `<path>` for curved motion arcs, the arrow subhead banner, decorative chevrons, and small bullet icons
- 8× `<rect>` for CTA banner, bullet cards, small accent pills, and highlight strips
- 12× `<text>` for CTA, headline, subhead, circular wheel labels, bullet titles, and bullet descriptions
- Optional `<tspan>` inside headline text for inline emphasis

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#071A2F"/>
      <stop offset="55%" stop-color="#102E4A"/>
      <stop offset="100%" stop-color="#06101F"/>
    </linearGradient>
    <linearGradient id="ctaGrad" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#00C2FF"/>
      <stop offset="100%" stop-color="#7C3AED"/>
    </linearGradient>
    <radialGradient id="wheelGrad" cx="50%" cy="46%" r="58%">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.95"/>
      <stop offset="45%" stop-color="#BFE9FF" stop-opacity="0.35"/>
      <stop offset="100%" stop-color="#00A3FF" stop-opacity="0.08"/>
    </radialGradient>
    <radialGradient id="hubGrad" cx="50%" cy="45%" r="55%">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="70%" stop-color="#46D5FF"/>
      <stop offset="100%" stop-color="#1769FF"/>
    </radialGradient>
    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="12" result="off"/>
      <feGaussianBlur in="off" stdDeviation="16" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="cyanGlow" x="-35%" y="-35%" width="170%" height="170%">
      <feGaussianBlur stdDeviation="8" result="glow"/>
      <feMerge>
        <feMergeNode in="glow"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>
  <path d="M-40 655 C160 585 260 690 430 620 C575 560 640 605 760 535 C900 455 1050 500 1320 390"
        fill="none" stroke="#2ED3FF" stroke-opacity="0.12" stroke-width="52"/>

  <circle cx="310" cy="385" r="222" fill="url(#wheelGrad)" stroke="#BFEFFF" stroke-opacity="0.35" stroke-width="2" filter="url(#cyanGlow)"/>
  <circle cx="310" cy="385" r="196" fill="none" stroke="#56D7FF" stroke-width="8" stroke-dasharray="34 18" transform="rotate(-18 310 385)"/>
  <circle cx="310" cy="385" r="154" fill="none" stroke="#FFFFFF" stroke-opacity="0.45" stroke-width="2" stroke-dasharray="8 12"/>
  <circle cx="310" cy="385" r="92" fill="#06182D" stroke="#65E4FF" stroke-width="4"/>
  <circle cx="310" cy="385" r="46" fill="url(#hubGrad)" stroke="#FFFFFF" stroke-opacity="0.75" stroke-width="3" filter="url(#cyanGlow)"/>

  <line x1="310" y1="210" x2="310" y2="305" stroke="#C8F6FF" stroke-opacity="0.65" stroke-width="4"/>
  <line x1="310" y1="465" x2="310" y2="560" stroke="#C8F6FF" stroke-opacity="0.65" stroke-width="4"/>
  <line x1="135" y1="385" x2="230" y2="385" stroke="#C8F6FF" stroke-opacity="0.65" stroke-width="4"/>
  <line x1="390" y1="385" x2="485" y2="385" stroke="#C8F6FF" stroke-opacity="0.65" stroke-width="4"/>
  <line x1="186" y1="261" x2="252" y2="327" stroke="#C8F6FF" stroke-opacity="0.42" stroke-width="3"/>
  <line x1="368" y1="443" x2="434" y2="509" stroke="#C8F6FF" stroke-opacity="0.42" stroke-width="3"/>
  <line x1="434" y1="261" x2="368" y2="327" stroke="#C8F6FF" stroke-opacity="0.42" stroke-width="3"/>
  <line x1="252" y1="443" x2="186" y2="509" stroke="#C8F6FF" stroke-opacity="0.42" stroke-width="3"/>

  <path d="M95 384 C96 270 180 180 292 164" fill="none" stroke="#9B5CFF" stroke-width="10" stroke-linecap="round" stroke-dasharray="52 30"/>
  <path d="M522 384 C520 493 438 585 326 604" fill="none" stroke="#00E0FF" stroke-width="10" stroke-linecap="round" stroke-dasharray="52 30"/>
  <path d="M111 268 L136 244 L144 276 Z" fill="#9B5CFF"/>
  <path d="M507 501 L482 526 L474 494 Z" fill="#00E0FF"/>

  <text x="258" y="183" width="110" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#FFFFFF" letter-spacing="2" transform="rotate(-8 310 183)">DISCOVER</text>
  <text x="423" y="373" width="90" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#FFFFFF" letter-spacing="2" transform="rotate(82 468 373)">ALIGN</text>
  <text x="253" y="596" width="100" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#FFFFFF" letter-spacing="2" transform="rotate(174 303 596)">SCALE</text>
  <text x="106" y="394" width="90" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#FFFFFF" letter-spacing="2" transform="rotate(-98 151 394)">BUILD</text>

  <rect x="650" y="70" width="350" height="46" rx="23" fill="url(#ctaGrad)" filter="url(#softShadow)"/>
  <text x="682" y="100" width="292" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#FFFFFF" letter-spacing="1.4">LAUNCH THE NEXT CYCLE</text>

  <text x="650" y="180" width="520" font-family="Segoe UI, Microsoft YaHei" font-size="56" font-weight="800" fill="#FFFFFF">
    Rotating <tspan fill="#54DFFF">Wheel</tspan> Bullet List
  </text>
  <text x="653" y="224" width="470" font-family="Segoe UI, Microsoft YaHei" font-size="18" fill="#A9C6DB">Use the dial as a visual anchor for momentum, iteration, and continuous improvement.</text>

  <path d="M650 266 H1042 L1082 304 L1042 342 H650 Z" fill="#FFFFFF" fill-opacity="0.10" stroke="#4FDCFF" stroke-opacity="0.55" stroke-width="2" filter="url(#softShadow)"/>
  <rect x="670" y="286" width="8" height="36" rx="4" fill="#00E0FF"/>
  <text x="696" y="313" width="330" font-family="Segoe UI, Microsoft YaHei" font-size="22" font-weight="700" fill="#FFFFFF">Four moves that keep the program in motion</text>

  <rect x="650" y="386" width="500" height="58" rx="18" fill="#FFFFFF" fill-opacity="0.09" stroke="#FFFFFF" stroke-opacity="0.12"/>
  <path d="M678 414 m-13 0 a13 13 0 1 0 26 0 a13 13 0 1 0 -26 0 M672 414 l5 6 l10 -13" fill="none" stroke="#42F0C8" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
  <text x="710" y="410" width="390" font-family="Segoe UI, Microsoft YaHei" font-size="19" font-weight="700" fill="#FFFFFF">Diagnose the current state</text>
  <text x="710" y="432" width="390" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#A9C6DB">Map friction points before prescribing solutions.</text>

  <rect x="650" y="462" width="500" height="58" rx="18" fill="#FFFFFF" fill-opacity="0.075" stroke="#FFFFFF" stroke-opacity="0.10"/>
  <path d="M678 490 m-13 0 a13 13 0 1 0 26 0 a13 13 0 1 0 -26 0 M672 490 l5 6 l10 -13" fill="none" stroke="#42F0C8" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
  <text x="710" y="486" width="390" font-family="Segoe UI, Microsoft YaHei" font-size="19" font-weight="700" fill="#FFFFFF">Align owners around the dial</text>
  <text x="710" y="508" width="390" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#A9C6DB">Give each phase a visible sponsor and decision path.</text>

  <rect x="650" y="538" width="500" height="58" rx="18" fill="#FFFFFF" fill-opacity="0.06" stroke="#FFFFFF" stroke-opacity="0.09"/>
  <path d="M678 566 m-13 0 a13 13 0 1 0 26 0 a13 13 0 1 0 -26 0 M672 566 l5 6 l10 -13" fill="none" stroke="#42F0C8" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
  <text x="710" y="562" width="390" font-family="Segoe UI, Microsoft YaHei" font-size="19" font-weight="700" fill="#FFFFFF">Prototype visible wins</text>
  <text x="710" y="584" width="390" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#A9C6DB">Turn the next spoke into a tangible proof point.</text>

  <rect x="650" y="614" width="500" height="58" rx="18" fill="#FFFFFF" fill-opacity="0.045" stroke="#FFFFFF" stroke-opacity="0.08"/>
  <path d="M678 642 m-13 0 a13 13 0 1 0 26 0 a13 13 0 1 0 -26 0 M672 642 l5 6 l10 -13" fill="none" stroke="#42F0C8" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
  <text x="710" y="638" width="390" font-family="Segoe UI, Microsoft YaHei" font-size="19" font-weight="700" fill="#FFFFFF">Scale the operating rhythm</text>
  <text x="710" y="660" width="390" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#A9C6DB">Repeat the cycle with sharper metrics each turn.</text>
</svg>
```

## Avoid in this skill
- ❌ SVG `<animateTransform>` or `<animate>` for the wheel spin; PPT-Master will not translate animation tags, so imply motion with dashed arcs, rotated labels, and arrowheads instead.
- ❌ `<textPath>` for circular wheel labels; place short text blocks manually around the ring using `transform="rotate(... cx cy)"`.
- ❌ `marker-end` arrowheads on curved paths; create arrowheads as small filled `<path>` triangles.
- ❌ Applying filters to `<line>` spokes; shadows/glows on lines are dropped, so keep spokes clean and put glow on circles or paths.
- ❌ Clipping or masking non-image wheel elements; use explicit paths, circles, and strokes instead of masks.

## Composition notes
- Keep the wheel large enough to crop emotionally into the slide’s left half; a 420–460 px diameter gives the motif keynote-scale presence.
- Reserve the right 50% for text, with the CTA at top, headline below, arrow banner as a bridge, and bullets stacked in a calm vertical rhythm.
- Use cool neon accents sparingly: cyan for motion and validation, violet for secondary rotation cues, white for the main content.
- The slide works best when the wheel feels slightly more luminous than the cards, while the bullet area remains high-contrast and easy to edit.