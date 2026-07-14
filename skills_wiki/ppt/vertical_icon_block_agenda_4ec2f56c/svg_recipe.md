# SVG Recipe — Vertical Icon-Block Agenda

## Visual mechanism
A full-height contextual image anchors the slide on the left, while the right side becomes a vertical “menu” of large rounded icon blocks. Each block behaves like a premium agenda button: monochrome icon, bold label, soft shadow, and generous spacing for fast scanning.

## SVG primitives needed
- 1× `<image>` for the large contextual hero/photo area on the left
- 1× `<clipPath>` with a custom `<path>` to crop the image with a softened organic right edge
- 1× `<rect>` for the slide background
- 1× `<rect>` for a translucent photo wash over the image
- 1× `<rect>` for the right-side clean content panel
- 5× `<rect>` for rounded agenda blocks
- 5× small `<rect>` accent tabs on the left edge of each block
- Multiple `<circle>`, `<ellipse>`, `<line>`, `<rect>`, and `<path>` elements for editable flat-vector icons
- 7× `<text>` elements for title, subtitle, block labels, and small section numbers
- 2× `<linearGradient>` definitions for soft background/photo treatments
- 1× `<filter id="cardShadow">` applied to agenda block rectangles for soft depth
- 1× `<filter id="photoGlow">` applied to a decorative blurred ellipse over the photo area

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="pageBg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#F8F8F6"/>
      <stop offset="100%" stop-color="#ECEDEA"/>
    </linearGradient>

    <linearGradient id="photoVeil" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.08"/>
      <stop offset="70%" stop-color="#FFFFFF" stop-opacity="0.18"/>
      <stop offset="100%" stop-color="#FFFFFF" stop-opacity="0.80"/>
    </linearGradient>

    <linearGradient id="blockFill" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#F2F2F0"/>
      <stop offset="100%" stop-color="#E3E4E1"/>
    </linearGradient>

    <filter id="cardShadow" x="-20%" y="-30%" width="140%" height="170%">
      <feOffset dx="0" dy="10" result="off"/>
      <feGaussianBlur in="off" stdDeviation="10" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="photoGlow" x="-60%" y="-60%" width="220%" height="220%">
      <feGaussianBlur stdDeviation="30"/>
    </filter>

    <clipPath id="photoClip">
      <path d="M0,0 L650,0 C610,135 696,245 620,360 C560,450 645,590 604,720 L0,720 Z"/>
    </clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#pageBg)"/>

  <image x="0" y="0" width="690" height="720" preserveAspectRatio="xMidYMid slice"
         href="https://images.example.com/hero-photo-premium-smartphone-retail-display.jpg"
         clip-path="url(#photoClip)"/>
  <rect x="0" y="0" width="720" height="720" fill="url(#photoVeil)"/>
  <ellipse cx="225" cy="600" rx="230" ry="70" fill="#FFFFFF" opacity="0.30" filter="url(#photoGlow)"/>

  <text x="68" y="92" width="500" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="600"
        letter-spacing="3" fill="#FFFFFF" opacity="0.86">EXECUTIVE AGENDA</text>
  <text x="68" y="142" width="520" font-family="Segoe UI, Microsoft YaHei" font-size="44" font-weight="700"
        fill="#FFFFFF">India growth review</text>
  <text x="70" y="184" width="440" font-family="Segoe UI, Microsoft YaHei" font-size="17"
        fill="#FFFFFF" opacity="0.82">Five discussion blocks for market context, products, channels, performance, and roadmap.</text>

  <rect x="665" y="0" width="615" height="720" fill="#F7F7F5" opacity="0.96"/>

  <text x="735" y="82" width="420" font-family="Segoe UI, Microsoft YaHei" font-size="30" font-weight="700"
        fill="#363636">Sales of Apple Products in India</text>
  <text x="737" y="113" width="410" font-family="Segoe UI, Microsoft YaHei" font-size="15"
        fill="#737373">Structured agenda for the leadership review</text>

  <!-- Block 01 -->
  <rect x="720" y="150" width="470" height="82" rx="22" fill="url(#blockFill)" filter="url(#cardShadow)"/>
  <rect x="720" y="171" width="7" height="40" rx="3.5" fill="#505050"/>
  <text x="750" y="183" width="38" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700"
        fill="#8A8A8A">01</text>
  <circle cx="817" cy="191" r="26" fill="none" stroke="#3E3E3E" stroke-width="5"/>
  <ellipse cx="817" cy="191" rx="11" ry="26" fill="none" stroke="#3E3E3E" stroke-width="4"/>
  <line x1="792" y1="191" x2="842" y2="191" stroke="#3E3E3E" stroke-width="5" stroke-linecap="round"/>
  <text x="870" y="201" width="270" font-family="Segoe UI, Microsoft YaHei" font-size="24" font-weight="700"
        fill="#3C3C3C">Market Landscape</text>

  <!-- Block 02 -->
  <rect x="720" y="255" width="470" height="82" rx="22" fill="url(#blockFill)" filter="url(#cardShadow)"/>
  <rect x="720" y="276" width="7" height="40" rx="3.5" fill="#505050"/>
  <text x="750" y="288" width="38" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700"
        fill="#8A8A8A">02</text>
  <rect x="795" y="265" width="44" height="62" rx="9" fill="none" stroke="#3E3E3E" stroke-width="5"/>
  <circle cx="817" cy="316" r="3.5" fill="#3E3E3E"/>
  <line x1="809" y1="275" x2="825" y2="275" stroke="#3E3E3E" stroke-width="4" stroke-linecap="round"/>
  <text x="870" y="306" width="285" font-family="Segoe UI, Microsoft YaHei" font-size="24" font-weight="700"
        fill="#3C3C3C">Product Portfolio</text>

  <!-- Block 03 -->
  <rect x="720" y="360" width="470" height="82" rx="22" fill="url(#blockFill)" filter="url(#cardShadow)"/>
  <rect x="720" y="381" width="7" height="40" rx="3.5" fill="#505050"/>
  <text x="750" y="393" width="38" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700"
        fill="#8A8A8A">03</text>
  <circle cx="806" cy="386" r="13" fill="none" stroke="#3E3E3E" stroke-width="5"/>
  <circle cx="831" cy="389" r="10" fill="none" stroke="#3E3E3E" stroke-width="4"/>
  <path d="M782,426 C786,408 825,406 830,426" fill="none" stroke="#3E3E3E" stroke-width="5" stroke-linecap="round"/>
  <path d="M819,425 C824,412 851,414 855,426" fill="none" stroke="#3E3E3E" stroke-width="4" stroke-linecap="round"/>
  <text x="870" y="411" width="285" font-family="Segoe UI, Microsoft YaHei" font-size="24" font-weight="700"
        fill="#3C3C3C">Customer Channels</text>

  <!-- Block 04 -->
  <rect x="720" y="465" width="470" height="82" rx="22" fill="url(#blockFill)" filter="url(#cardShadow)"/>
  <rect x="720" y="486" width="7" height="40" rx="3.5" fill="#505050"/>
  <text x="750" y="498" width="38" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700"
        fill="#8A8A8A">04</text>
  <line x1="793" y1="521" x2="846" y2="521" stroke="#3E3E3E" stroke-width="5" stroke-linecap="round"/>
  <line x1="793" y1="521" x2="793" y2="477" stroke="#3E3E3E" stroke-width="5" stroke-linecap="round"/>
  <rect x="803" y="501" width="9" height="20" fill="#3E3E3E"/>
  <rect x="820" y="488" width="9" height="33" fill="#3E3E3E"/>
  <rect x="837" y="474" width="9" height="47" fill="#3E3E3E"/>
  <text x="870" y="516" width="300" font-family="Segoe UI, Microsoft YaHei" font-size="24" font-weight="700"
        fill="#3C3C3C">Sales Performance</text>

  <!-- Block 05 -->
  <rect x="720" y="570" width="470" height="82" rx="22" fill="url(#blockFill)" filter="url(#cardShadow)"/>
  <rect x="720" y="591" width="7" height="40" rx="3.5" fill="#505050"/>
  <text x="750" y="603" width="38" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700"
        fill="#8A8A8A">05</text>
  <path d="M793,618 C810,590 828,633 846,596" fill="none" stroke="#3E3E3E" stroke-width="5" stroke-linecap="round"/>
  <circle cx="793" cy="618" r="5" fill="#3E3E3E"/>
  <circle cx="846" cy="596" r="5" fill="#3E3E3E"/>
  <path d="M833,594 L847,596 L840,608" fill="none" stroke="#3E3E3E" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
  <text x="870" y="621" width="270" font-family="Segoe UI, Microsoft YaHei" font-size="24" font-weight="700"
        fill="#3C3C3C">Growth Roadmap</text>
</svg>
```

## Avoid in this skill
- ❌ Tiny bullet lists inside the blocks; the pattern works best when each block has one strong label.
- ❌ Highly saturated mixed icon colors; use one charcoal tone so the blocks feel like a coherent menu.
- ❌ Equal 50/50 split with no overlap or breathing room; the image should feel offset and contextual, not like a separate column in a table.
- ❌ Applying `clip-path` to the agenda block rectangles; keep clipping only on the hero image for reliable PowerPoint translation.
- ❌ Using `marker-end` arrows for roadmap icons; draw arrowheads manually with short editable paths.

## Composition notes
- Keep the photo/image on the left 50–55% of the slide and push the functional agenda stack into the right 40%.
- Use large rounded blocks with 20–30 px vertical gaps; the gaps are what make the items read as premium navigation tiles rather than a list.
- Place icons consistently around 90–105 px from the block’s left edge, with labels starting on the same x-coordinate across all blocks.
- Maintain a restrained palette: warm off-white background, pale grey agenda blocks, charcoal typography, and one subtle accent tab per block.