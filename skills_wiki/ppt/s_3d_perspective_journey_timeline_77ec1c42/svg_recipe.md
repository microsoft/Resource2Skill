# SVG Recipe — 3D Perspective Journey Timeline

## Visual mechanism
A tapered “road” recedes toward a vanishing point while milestone anchors shrink with distance, creating a forced-perspective journey. Each milestone uses flattened floor rings plus a vertical translucent light beam to fake 3D pins rising from the path into editable text callouts.

## SVG primitives needed
- 1× `<rect>` for the white slide background
- 2× `<path>` for the tapered perspective road and subtle road-edge highlight
- 1× `<path>` with `stroke-dasharray` for the receding center guide line
- 5× flattened `<ellipse>` pairs for milestone floor rings and colored anchor pads
- 5× narrow `<line>` elements for vertical pin stems
- 5× translucent gradient `<rect>` elements for vertical pin glow / glass-beam effects
- 5× small `<circle>` elements for pin heads
- 5× rounded `<rect>` cards behind text / thumbnails
- 3× `<image>` elements clipped into rounded thumbnail cards
- 3× `<clipPath>` definitions using rounded `<rect>` for editable image crops
- 5× `<linearGradient>` definitions for colored pin glows
- 2× `<linearGradient>` definitions for the road surface and card fills
- 1× `<filter id="softShadow">` using `feOffset + feGaussianBlur + feMerge` applied to cards, rings, and road
- Multiple `<text>` elements with explicit `width` attributes for title, years, labels, and descriptions

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="roadFill" x1="230" y1="245" x2="900" y2="720" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#f3f4f6"/>
      <stop offset="0.62" stop-color="#dedede"/>
      <stop offset="1" stop-color="#cfcfcf"/>
    </linearGradient>
    <linearGradient id="cardFill" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#ffffff"/>
      <stop offset="1" stop-color="#f7f8fb"/>
    </linearGradient>
    <linearGradient id="glowGreen" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#92D050" stop-opacity="0"/><stop offset="1" stop-color="#92D050" stop-opacity="0.6"/></linearGradient>
    <linearGradient id="glowYellow" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFC000" stop-opacity="0"/><stop offset="1" stop-color="#FFC000" stop-opacity="0.62"/></linearGradient>
    <linearGradient id="glowBlue" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0070C0" stop-opacity="0"/><stop offset="1" stop-color="#0070C0" stop-opacity="0.58"/></linearGradient>
    <linearGradient id="glowCyan" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#00B0F0" stop-opacity="0"/><stop offset="1" stop-color="#00B0F0" stop-opacity="0.58"/></linearGradient>
    <linearGradient id="glowPurple" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#7030A0" stop-opacity="0"/><stop offset="1" stop-color="#7030A0" stop-opacity="0.56"/></linearGradient>
    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="8"/>
      <feGaussianBlur stdDeviation="10"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <clipPath id="clipThumb1"><rect x="774" y="91" width="142" height="80" rx="14"/></clipPath>
    <clipPath id="clipThumb2"><rect x="154" y="338" width="156" height="88" rx="16"/></clipPath>
    <clipPath id="clipThumb3"><rect x="858" y="499" width="178" height="100" rx="18"/></clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#ffffff"/>
  <text x="64" y="70" width="480" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="700" fill="#3b3f45">Corporate Journey</text>
  <text x="66" y="103" width="520" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#89909a">A forced-perspective roadmap that turns milestones into a dimensional path.</text>

  <path d="M230 235 C302 278 430 335 610 415 C776 489 979 590 1190 720 L585 720 C489 612 382 486 270 332 C246 298 232 265 230 235 Z"
        fill="url(#roadFill)" filter="url(#softShadow)"/>
  <path d="M260 256 C355 315 500 384 673 461 C825 529 994 611 1152 704"
        fill="none" stroke="#ffffff" stroke-width="5" stroke-opacity="0.55"/>
  <path d="M286 291 C398 356 533 420 682 489 C816 551 966 626 1112 704"
        fill="none" stroke="#aeb4bd" stroke-width="3" stroke-opacity="0.5" stroke-dasharray="12 16"/>

  <rect x="612" y="91" width="322" height="118" rx="22" fill="url(#cardFill)" filter="url(#softShadow)"/>
  <image href="https://images.example.com/rounded-thumbnail-global-market-expansion.jpg" x="774" y="91" width="142" height="80" clip-path="url(#clipThumb1)"/>
  <text x="634" y="123" width="130" font-family="Segoe UI, Microsoft YaHei" font-size="26" font-weight="700" fill="#92D050">2018</text>
  <text x="634" y="151" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#44484f">MARKET EXPANSION</text>
  <text x="634" y="174" width="260" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#8b929c">Launched regional hubs and opened the first international channel.</text>

  <rect x="252" y="131" width="34" height="126" rx="17" fill="url(#glowGreen)"/>
  <line x1="269" y1="134" x2="269" y2="259" stroke="#92D050" stroke-width="2.5"/>
  <ellipse cx="269" cy="259" rx="62" ry="18" fill="#92D050" fill-opacity="0.16" filter="url(#softShadow)"/>
  <ellipse cx="269" cy="259" rx="44" ry="12" fill="#92D050"/>
  <ellipse cx="269" cy="259" rx="68" ry="20" fill="none" stroke="#92D050" stroke-width="2" stroke-opacity="0.6"/>
  <circle cx="269" cy="134" r="5" fill="#92D050"/>

  <rect x="120" y="306" width="224" height="138" rx="24" fill="url(#cardFill)" filter="url(#softShadow)"/>
  <image href="https://images.example.com/rounded-thumbnail-strategic-partnerships.jpg" x="154" y="338" width="156" height="88" clip-path="url(#clipThumb2)"/>
  <text x="145" y="334" width="160" font-family="Segoe UI, Microsoft YaHei" font-size="28" font-weight="700" fill="#FFC000">2019</text>
  <text x="145" y="456" width="180" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#44484f">NEW PARTNERSHIPS</text>
  <text x="145" y="478" width="170" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#8b929c">Built a partner ecosystem to accelerate delivery.</text>

  <rect x="407" y="174" width="42" height="174" rx="21" fill="url(#glowYellow)"/>
  <line x1="428" y1="177" x2="428" y2="350" stroke="#FFC000" stroke-width="3"/>
  <ellipse cx="428" cy="350" rx="82" ry="24" fill="#FFC000" fill-opacity="0.18" filter="url(#softShadow)"/>
  <ellipse cx="428" cy="350" rx="56" ry="16" fill="#FFC000"/>
  <ellipse cx="428" cy="350" rx="90" ry="27" fill="none" stroke="#FFC000" stroke-width="2.5" stroke-opacity="0.62"/>
  <circle cx="428" cy="177" r="6" fill="#FFC000"/>

  <rect x="752" y="257" width="276" height="116" rx="22" fill="url(#cardFill)" filter="url(#softShadow)"/>
  <text x="778" y="301" width="160" font-family="Segoe UI, Microsoft YaHei" font-size="31" font-weight="700" fill="#0070C0">2021</text>
  <text x="778" y="331" width="210" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#44484f">PLATFORM MODERNIZATION</text>
  <text x="778" y="354" width="220" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#8b929c">Rebuilt the core product into a scalable cloud architecture.</text>

  <rect x="588" y="230" width="50" height="212" rx="25" fill="url(#glowBlue)"/>
  <line x1="613" y1="232" x2="613" y2="444" stroke="#0070C0" stroke-width="3.5"/>
  <ellipse cx="613" cy="444" rx="102" ry="30" fill="#0070C0" fill-opacity="0.17" filter="url(#softShadow)"/>
  <ellipse cx="613" cy="444" rx="70" ry="20" fill="#0070C0"/>
  <ellipse cx="613" cy="444" rx="112" ry="33" fill="none" stroke="#0070C0" stroke-width="3" stroke-opacity="0.58"/>
  <circle cx="613" cy="232" r="7" fill="#0070C0"/>

  <rect x="250" y="506" width="302" height="122" rx="24" fill="url(#cardFill)" filter="url(#softShadow)"/>
  <text x="280" y="548" width="160" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="700" fill="#00B0F0">2023</text>
  <text x="280" y="580" width="210" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#44484f">CUSTOMER SUCCESS ENGINE</text>
  <text x="280" y="606" width="230" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#8b929c">Introduced high-touch onboarding and predictive support workflows.</text>

  <rect x="795" y="323" width="60" height="256" rx="30" fill="url(#glowCyan)"/>
  <line x1="825" y1="326" x2="825" y2="581" stroke="#00B0F0" stroke-width="4"/>
  <ellipse cx="825" cy="581" rx="125" ry="37" fill="#00B0F0" fill-opacity="0.18" filter="url(#softShadow)"/>
  <ellipse cx="825" cy="581" rx="86" ry="25" fill="#00B0F0"/>
  <ellipse cx="825" cy="581" rx="138" ry="41" fill="none" stroke="#00B0F0" stroke-width="3" stroke-opacity="0.58"/>
  <circle cx="825" cy="326" r="8" fill="#00B0F0"/>

  <rect x="830" y="473" width="250" height="146" rx="26" fill="url(#cardFill)" filter="url(#softShadow)"/>
  <image href="https://images.example.com/rounded-thumbnail-ai-product-roadmap.jpg" x="858" y="499" width="178" height="100" clip-path="url(#clipThumb3)"/>
  <text x="1038" y="520" width="90" font-family="Segoe UI, Microsoft YaHei" font-size="32" font-weight="700" fill="#7030A0">2025</text>
  <text x="1038" y="551" width="120" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#44484f">AI ROADMAP</text>
  <text x="1038" y="574" width="120" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#8b929c">Next wave of intelligent automation.</text>

  <rect x="1045" y="365" width="68" height="300" rx="34" fill="url(#glowPurple)"/>
  <line x1="1079" y1="368" x2="1079" y2="668" stroke="#7030A0" stroke-width="4.5"/>
  <ellipse cx="1079" cy="668" rx="150" ry="44" fill="#7030A0" fill-opacity="0.16" filter="url(#softShadow)"/>
  <ellipse cx="1079" cy="668" rx="100" ry="29" fill="#7030A0"/>
  <ellipse cx="1079" cy="668" rx="165" ry="49" fill="none" stroke="#7030A0" stroke-width="3.5" stroke-opacity="0.56"/>
  <circle cx="1079" cy="368" r="9" fill="#7030A0"/>
</svg>
```

## Avoid in this skill
- ❌ True 3D transforms, skew, or matrix transforms; fake perspective with manually tapered paths, flattened ellipses, and size scaling.
- ❌ `marker-end` on path-based road lines; arrowheads may disappear, and this design does not need explicit arrows.
- ❌ Applying `clip-path` to cards, rings, or beams; use clipping only on `<image>` thumbnails.
- ❌ Overcrowding all labels on the road surface; keep text lifted into callout cards so the path remains readable.
- ❌ Using identical milestone sizes; the illusion depends on distant anchors being smaller and near anchors being larger.

## Composition notes
- Place the road from upper-left/mid-left toward the lower-right foreground; the lower-right anchor should be the largest and most visually dominant.
- Alternate callout cards left and right of the path to create rhythm and avoid vertical pin collisions.
- Use flattened ellipses at every anchor point; their width-to-height ratio should be roughly 3:1 to suggest a horizontal floor plane.
- Keep the background mostly white or very pale so the colored pins, glow beams, and road perspective carry the visual energy.