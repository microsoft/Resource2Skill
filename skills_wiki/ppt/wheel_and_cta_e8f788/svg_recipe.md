# SVG Recipe — Wheel and CTA

## Visual mechanism
A playful segmented wheel acts as the closing-slide “engagement engine,” with each colorful slice implying an action or community touchpoint. A large, high-contrast CTA button anchors the composition and makes the desired next step unmistakable.

## SVG primitives needed
- 1× `<rect>` for the full-slide gradient background
- 2× `<path>` for soft abstract background blobs
- 8× `<path>` for exploded donut-wheel segments
- 1× `<circle>` for the wheel hub
- 4× `<circle>` for small decorative orbit dots
- 1× `<path>` for a play/arrow icon inside the wheel hub
- 2× `<rect>` for the CTA button base and highlight strip
- 1× `<path>` for the CTA button play icon
- 1× `<circle>` plus 2× `<path>` for the bell/notification icon
- Multiple `<text>` elements with explicit `width` for headline, segment labels, CTA copy, and footer line
- 8× `<linearGradient>` for premium segment fills
- 1× `<radialGradient>` for the background glow
- 2× `<filter>` definitions: one soft shadow and one colored glow

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <radialGradient id="bg" cx="48%" cy="38%" r="72%">
      <stop offset="0%" stop-color="#263B80"/>
      <stop offset="52%" stop-color="#101A3F"/>
      <stop offset="100%" stop-color="#070B1E"/>
    </radialGradient>
    <linearGradient id="seg1" x1="560" y1="130" x2="720" y2="470"><stop offset="0%" stop-color="#7C5CFF"/><stop offset="100%" stop-color="#4C2DCC"/></linearGradient>
    <linearGradient id="seg2" x1="600" y1="130" x2="820" y2="350"><stop offset="0%" stop-color="#00D3FF"/><stop offset="100%" stop-color="#0077FF"/></linearGradient>
    <linearGradient id="seg3" x1="790" y1="210" x2="710" y2="440"><stop offset="0%" stop-color="#31E6A5"/><stop offset="100%" stop-color="#00A86B"/></linearGradient>
    <linearGradient id="seg4" x1="800" y1="360" x2="580" y2="490"><stop offset="0%" stop-color="#FFE15A"/><stop offset="100%" stop-color="#FF9F1C"/></linearGradient>
    <linearGradient id="seg5" x1="680" y1="480" x2="470" y2="350"><stop offset="0%" stop-color="#FF7A59"/><stop offset="100%" stop-color="#F94144"/></linearGradient>
    <linearGradient id="seg6" x1="520" y1="455" x2="440" y2="220"><stop offset="0%" stop-color="#FF4FD8"/><stop offset="100%" stop-color="#B5179E"/></linearGradient>
    <linearGradient id="seg7" x1="470" y1="350" x2="600" y2="120"><stop offset="0%" stop-color="#A3F7BF"/><stop offset="100%" stop-color="#38B000"/></linearGradient>
    <linearGradient id="seg8" x1="500" y1="200" x2="720" y2="120"><stop offset="0%" stop-color="#B8C0FF"/><stop offset="100%" stop-color="#5E60CE"/></linearGradient>
    <linearGradient id="cta" x1="710" y1="488" x2="1050" y2="600"><stop offset="0%" stop-color="#FF2E63"/><stop offset="100%" stop-color="#FF7A00"/></linearGradient>
    <filter id="shadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="14"/>
      <feGaussianBlur stdDeviation="16"/>
      <feMerge><feMergeNode/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <filter id="glow" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="10"/>
      <feMerge><feMergeNode/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bg)"/>
  <path d="M70,110 C160,35 275,80 300,185 C328,305 205,355 105,315 C20,280 -15,185 70,110 Z" fill="#4157FF" opacity="0.16"/>
  <path d="M1035,50 C1170,20 1275,105 1287,235 C1298,360 1170,410 1058,350 C955,295 910,85 1035,50 Z" fill="#00D3FF" opacity="0.12"/>

  <text x="88" y="88" width="520" font-family="Segoe UI, Microsoft YaHei" font-size="25" font-weight="700" fill="#8EE8FF" letter-spacing="3">THANK YOU FOR WATCHING</text>
  <text x="86" y="145" width="560" font-family="Segoe UI, Microsoft YaHei" font-size="58" font-weight="800" fill="#FFFFFF">Stay in the loop</text>
  <text x="90" y="190" width="500" font-family="Segoe UI, Microsoft YaHei" font-size="22" fill="#B9C7FF">Pick your next step — subscribe, share, or follow for the next update.</text>

  <g filter="url(#shadow)">
    <path d="M596,136 A170,170 0 0 1 712,146 L682,209 A100,100 0 0 0 614,203 Z" fill="url(#seg1)" transform="translate(-10,-18)"/>
    <path d="M725,153 A170,170 0 0 1 800,242 L734,266 A100,100 0 0 0 690,213 Z" fill="url(#seg2)" transform="translate(14,-12)"/>
    <path d="M804,256 A170,170 0 0 1 794,372 L731,342 A100,100 0 0 0 737,274 Z" fill="url(#seg3)" transform="translate(20,4)"/>
    <path d="M787,385 A170,170 0 0 1 698,460 L674,394 A100,100 0 0 0 727,350 Z" fill="url(#seg4)" transform="translate(12,18)"/>
    <path d="M684,464 A170,170 0 0 1 568,454 L598,391 A100,100 0 0 0 666,397 Z" fill="url(#seg5)" transform="translate(-6,22)"/>
    <path d="M555,447 A170,170 0 0 1 480,358 L546,334 A100,100 0 0 0 590,387 Z" fill="url(#seg6)" transform="translate(-20,10)"/>
    <path d="M476,344 A170,170 0 0 1 486,228 L549,258 A100,100 0 0 0 543,326 Z" fill="url(#seg7)" transform="translate(-22,-6)"/>
    <path d="M493,215 A170,170 0 0 1 582,140 L606,206 A100,100 0 0 0 553,250 Z" fill="url(#seg8)" transform="translate(-12,-18)"/>
  </g>

  <circle cx="640" cy="300" r="88" fill="#FFFFFF" opacity="0.98" filter="url(#shadow)"/>
  <circle cx="640" cy="300" r="62" fill="#111B46"/>
  <path d="M625,263 L684,300 L625,337 Z" fill="#FFFFFF"/>
  <circle cx="420" cy="170" r="8" fill="#00D3FF" opacity="0.85"/>
  <circle cx="858" cy="185" r="6" fill="#FFE15A" opacity="0.9"/>
  <circle cx="427" cy="450" r="7" fill="#FF4FD8" opacity="0.85"/>
  <circle cx="838" cy="465" r="9" fill="#31E6A5" opacity="0.85"/>

  <text x="528" y="104" width="120" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#DDE6FF" text-anchor="middle">LIKE</text>
  <text x="808" y="214" width="140" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#DDE6FF" text-anchor="middle">SHARE</text>
  <text x="788" y="486" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#DDE6FF" text-anchor="middle">FOLLOW</text>
  <text x="492" y="485" width="160" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#DDE6FF" text-anchor="middle">COMMENT</text>

  <rect x="716" y="505" width="390" height="88" rx="44" fill="url(#cta)" filter="url(#shadow)"/>
  <rect x="740" y="517" width="342" height="20" rx="10" fill="#FFFFFF" opacity="0.18"/>
  <path d="M773,535 L773,563 L798,549 Z" fill="#FFFFFF"/>
  <text x="825" y="562" width="230" font-family="Segoe UI, Microsoft YaHei" font-size="30" font-weight="900" fill="#FFFFFF" letter-spacing="1">SUBSCRIBE</text>

  <circle cx="1128" cy="549" r="36" fill="#FFFFFF" filter="url(#glow)"/>
  <path d="M1114,548 C1114,535 1121,526 1128,526 C1136,526 1142,535 1142,548 L1148,562 L1108,562 Z" fill="#111B46"/>
  <path d="M1120,567 C1123,573 1134,573 1137,567" fill="none" stroke="#111B46" stroke-width="5" stroke-linecap="round"/>

  <text x="90" y="650" width="720" font-family="Segoe UI, Microsoft YaHei" font-size="19" fill="#93A4D8">Scan the wheel, choose one action, and keep the conversation going.</text>
</svg>
```

## Avoid in this skill
- ❌ Do not create the wheel with `<mask>` or masked shapes; masks are not reliable for editable PowerPoint output.
- ❌ Do not use `<textPath>` to curve labels around the wheel; place short straight labels near the segments instead.
- ❌ Do not use `<use>` or `<symbol>` to duplicate segment icons; draw each simple icon/shape directly.
- ❌ Do not rely on `marker-end` for arrows pointing to the CTA; if arrows are needed, use `<line>` with explicit marker placement or draw arrowheads as paths.
- ❌ Do not apply filters to `<line>` elements; shadows/glows should be on paths, circles, rects, or text.

## Composition notes
- Keep the segmented wheel slightly left of center so it feels like an active visual object, with the CTA button occupying the lower-right action zone.
- Use a dark, cinematic background so the colorful wheel segments and warm CTA button pop.
- Reserve the top-left quadrant for the closing headline and a short explanatory sentence; avoid crowding the wheel with long copy.
- Make the CTA button the largest single horizontal object on the slide, with a glow or shadow strong enough to read as the final click target.