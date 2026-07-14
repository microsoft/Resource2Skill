# SVG Recipe — Angled Split Corporate Layout

## Visual mechanism
A bold brand panel cuts diagonally across the left side while a dark angled header locks the top-right content area into the same slant, creating a kinetic corporate split. The remaining white space becomes a crisp information zone with right-aligned text, geometric icon bullets, and thin accent rules.

## SVG primitives needed
- 1× `<rect>` for the white canvas base.
- 2× `<linearGradient>` for subtle premium depth on the red brand block and black header block.
- 1× `<filter id="softShadow">` applied to the dark angled header and contact icon containers.
- 1× large red `<path>` for the left angled brand panel.
- 1× narrow white `<path>` for the angled separator gap between red and black zones.
- 1× black `<path>` for the top-right angled header.
- 2× small accent `<path>` shapes for diagonal red/gray rhythm in the white content area.
- 2× `<circle>` plus 1× monogram `<path>` for the logo mark.
- 3× hexagon `<path>` shapes for contact icon containers.
- 6× small stroked `<path>` shapes for phone, email, and location pictograms.
- 3× `<line>` elements for contact row separators and content structure.
- Multiple `<text width="...">` elements for brand name, section title, person name, role, and contact details.

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="redPanel" x1="0" y1="0" x2="520" y2="720" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#E31B3F"/>
      <stop offset="0.58" stop-color="#C8102E"/>
      <stop offset="1" stop-color="#9F0D26"/>
    </linearGradient>
    <linearGradient id="blackPanel" x1="460" y1="0" x2="1280" y2="260" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#242424"/>
      <stop offset="1" stop-color="#000000"/>
    </linearGradient>
    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="160%">
      <feOffset dx="0" dy="10" result="off"/>
      <feGaussianBlur in="off" stdDeviation="12" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="redGlow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="8"/>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#FFFFFF"/>

  <!-- Primary angled split -->
  <path d="M0 0 L405 0 L558 720 L0 720 Z" fill="url(#redPanel)"/>
  <path d="M405 0 L432 0 L586 720 L558 720 Z" fill="#FFFFFF"/>
  <path d="M438 0 L1280 0 L1280 248 L489 248 Z" fill="url(#blackPanel)" filter="url(#softShadow)"/>

  <!-- Secondary diagonal accents -->
  <path d="M511 270 L1280 270 L1280 292 L516 292 Z" fill="#C8102E"/>
  <path d="M980 600 L1280 600 L1280 626 L986 626 Z" fill="#F1F2F4"/>
  <path d="M1074 646 L1280 646 L1280 662 L1077 662 Z" fill="#F7D9DF"/>
  <path d="M1038 97 L1280 97 L1280 104 L1040 104 Z" fill="#3B3B3B" opacity="0.65"/>

  <!-- Left logo mark -->
  <circle cx="214" cy="158" r="74" fill="#FFFFFF"/>
  <circle cx="214" cy="158" r="58" fill="none" stroke="#C8102E" stroke-width="5"/>
  <path d="M180 189 L180 126 L199 126 L214 158 L229 126 L248 126 L248 189 L231 189 L231 154 L220 178 L208 178 L197 154 L197 189 Z"
        fill="#C8102E"/>

  <!-- Brand text -->
  <text x="214" y="333" width="360" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="48" font-weight="800" fill="#FFFFFF" letter-spacing="1">
    <tspan x="214" dy="0">MY</tspan>
    <tspan x="214" dy="56">BUSINESS</tspan>
  </text>
  <line x1="103" y1="432" x2="325" y2="432" stroke="#FFFFFF" stroke-width="3" opacity="0.75"/>
  <text x="214" y="474" width="330" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="18" font-weight="600" fill="#FFFFFF" letter-spacing="3">
    CORPORATE IDENTITY
  </text>
  <text x="214" y="508" width="330" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="14" fill="#FFE9ED" letter-spacing="1">
    Strategy • Operations • Growth
  </text>

  <!-- Top-right header copy -->
  <text x="1188" y="84" width="620" text-anchor="end" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="52" font-weight="800" fill="#FFFFFF" letter-spacing="1">
    JOHN DOE
  </text>
  <text x="1188" y="124" width="620" text-anchor="end" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="22" font-weight="600" fill="#C8102E" letter-spacing="1.5">
    BUSINESS OWNER
  </text>
  <text x="1188" y="172" width="590" text-anchor="end" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="15" fill="#D7D7D7">
    Building high-performance teams, scalable operations, and memorable client experiences.
  </text>

  <!-- Contact section heading -->
  <text x="1188" y="350" width="520" text-anchor="end" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="20" font-weight="800" fill="#111111" letter-spacing="2">
    CONTACT DETAILS
  </text>
  <line x1="735" y1="368" x2="1188" y2="368" stroke="#D9DDE2" stroke-width="2"/>

  <!-- Phone row -->
  <path d="M754 409 L772 378 L808 378 L826 409 L808 440 L772 440 Z" fill="#C8102E" filter="url(#softShadow)"/>
  <path d="M785 394 C782 397 782 406 788 413 C795 422 806 425 810 421 L815 416 L807 407 L802 412 C798 410 793 405 791 400 L796 395 L788 388 Z"
        fill="none" stroke="#FFFFFF" stroke-width="4" stroke-linejoin="round" stroke-linecap="round"/>
  <text x="1188" y="397" width="410" text-anchor="end" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="13" font-weight="700" fill="#C8102E" letter-spacing="1.5">
    PHONE
  </text>
  <text x="1188" y="426" width="410" text-anchor="end" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="27" font-weight="700" fill="#111111">
    +1 234 567 8900
  </text>

  <!-- Email row -->
  <line x1="735" y1="469" x2="1188" y2="469" stroke="#ECEFF3" stroke-width="2"/>
  <path d="M754 519 L772 488 L808 488 L826 519 L808 550 L772 550 Z" fill="#111111" filter="url(#softShadow)"/>
  <path d="M775 505 L813 505 L813 533 L775 533 Z" fill="none" stroke="#FFFFFF" stroke-width="4" stroke-linejoin="round"/>
  <path d="M776 506 L794 522 L812 506" fill="none" stroke="#FFFFFF" stroke-width="4" stroke-linejoin="round" stroke-linecap="round"/>
  <text x="1188" y="507" width="410" text-anchor="end" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="13" font-weight="700" fill="#C8102E" letter-spacing="1.5">
    EMAIL
  </text>
  <text x="1188" y="536" width="410" text-anchor="end" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="26" font-weight="700" fill="#111111">
    john@mybusiness.com
  </text>

  <!-- Location row -->
  <line x1="735" y1="579" x2="1188" y2="579" stroke="#ECEFF3" stroke-width="2"/>
  <path d="M754 629 L772 598 L808 598 L826 629 L808 660 L772 660 Z" fill="#C8102E" filter="url(#softShadow)"/>
  <path d="M790 613 C780 613 773 620 773 630 C773 643 790 654 790 654 C790 654 807 643 807 630 C807 620 800 613 790 613 Z"
        fill="none" stroke="#FFFFFF" stroke-width="4" stroke-linejoin="round"/>
  <circle cx="790" cy="630" r="5" fill="#FFFFFF"/>
  <text x="1188" y="617" width="410" text-anchor="end" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="13" font-weight="700" fill="#C8102E" letter-spacing="1.5">
    OFFICE
  </text>
  <text x="1188" y="646" width="410" text-anchor="end" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="25" font-weight="700" fill="#111111">
    1200 Market Street, New York
  </text>
</svg>
```

## Avoid in this skill
- ❌ Using ordinary vertical rectangles for the split; the diagonal polygon edges are the whole identity of the layout.
- ❌ Applying `clip-path` to the red or black vector panels; use direct `<path>` geometry instead.
- ❌ Letting the white separator gap be inconsistent with the main diagonal angle; the edges should feel parallel and engineered.
- ❌ Center-aligning the right-side contact information; the layout works best when the content is anchored firmly to the right edge.
- ❌ Adding too many colors; keep the palette restrained to brand red, black, white, and very light grays.

## Composition notes
- Keep the red brand block around 38–45% of the slide width, with its bottom edge extending farther right than its top edge.
- Reserve the upper-right dark block for the strongest identity text: name, title, headline, or section label.
- Use the lower-right white area for detailed information, with generous spacing and right-aligned copy.
- Repeat the diagonal angle in small accent strips so the whole slide feels intentional rather than like two unrelated panels.