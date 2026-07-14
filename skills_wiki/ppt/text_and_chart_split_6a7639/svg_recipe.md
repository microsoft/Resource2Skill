# SVG Recipe — Text and Chart Split

## Visual mechanism
A disciplined executive split layout: a centered topic header anchors the slide, while the lower canvas divides into an editorial narrative column on the left and a structured chart card on the right. The separation is reinforced with negative space, a slim accent divider, and a premium chart container with subtle depth.

## SVG primitives needed
- 3× `<linearGradient>` for background wash, chart card sheen, and accent fills
- 1× `<radialGradient>` for soft ambient highlight behind the chart
- 2× `<filter>` definitions: one drop shadow for cards, one glow for accents
- 1× full-slide `<rect>` for the background
- 2× decorative `<path>` blobs for subtle executive-keynote polish
- 1× centered header text group using `<text>` and nested `<tspan>`
- 1× left narrative card `<rect>` plus multiple `<text>` elements for kicker, title, body, and metrics
- 1× vertical `<rect>` divider to separate text and chart zones
- 1× right chart card `<rect>` with shadow
- Multiple `<line>` elements for chart gridlines and axis ticks
- Multiple `<rect>` elements for editable bar-chart columns
- 1× `<path>` for an editable trend line over the bars
- Multiple `<circle>` elements for trend-line data points
- Multiple `<text>` elements for chart labels, legends, and callouts

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgWash" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#F7FAFF"/>
      <stop offset="58%" stop-color="#EEF3FA"/>
      <stop offset="100%" stop-color="#E7EEF8"/>
    </linearGradient>
    <linearGradient id="accentGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#2F80ED"/>
      <stop offset="100%" stop-color="#24C6DC"/>
    </linearGradient>
    <linearGradient id="cardSheen" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="100%" stop-color="#F8FBFF"/>
    </linearGradient>
    <radialGradient id="chartHalo" cx="70%" cy="54%" r="45%">
      <stop offset="0%" stop-color="#7AC7FF" stop-opacity="0.28"/>
      <stop offset="100%" stop-color="#7AC7FF" stop-opacity="0"/>
    </radialGradient>
    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="14"/>
      <feGaussianBlur stdDeviation="18"/>
      <feColorMatrix type="matrix" values="0 0 0 0 0.04  0 0 0 0 0.10  0 0 0 0 0.20  0 0 0 0.18 0"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="accentGlow" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="8"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgWash)"/>
  <rect x="0" y="0" width="1280" height="720" fill="url(#chartHalo)"/>

  <path d="M-70,92 C70,18 196,38 248,132 C304,232 224,328 98,310 C-26,292 -116,180 -70,92 Z"
        fill="#DCEBFF" opacity="0.65"/>
  <path d="M1084,24 C1210,-24 1324,58 1302,174 C1282,278 1152,300 1070,222 C992,148 996,58 1084,24 Z"
        fill="url(#accentGrad)" opacity="0.13" filter="url(#accentGlow)"/>

  <text x="640" y="70" width="820" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="17" font-weight="700"
        letter-spacing="2.8" fill="#2F80ED">QUARTERLY PERFORMANCE BRIEF</text>
  <text x="640" y="122" width="900" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="43" font-weight="700"
        fill="#172033">Text and Chart Split</text>
  <text x="640" y="154" width="760" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="18"
        fill="#667085">A concise narrative paired with a right-side data proof point.</text>

  <rect x="82" y="206" width="458" height="392" rx="28" fill="#FFFFFF" opacity="0.78"/>
  <rect x="100" y="224" width="6" height="112" rx="3" fill="url(#accentGrad)"/>
  <text x="126" y="254" width="350"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="14" font-weight="700"
        letter-spacing="1.5" fill="#2F80ED">INSIGHT SUMMARY</text>
  <text x="126" y="301" width="360"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="30" font-weight="700"
        fill="#172033">Efficiency improved while acquisition costs normalized</text>
  <text x="126" y="360" width="350"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="17"
        fill="#536173">
    <tspan x="126" dy="0">The current operating model shows a stronger conversion profile,</tspan>
    <tspan x="126" dy="27">with growth increasingly driven by retained customers and higher</tspan>
    <tspan x="126" dy="27">repeat purchase frequency. The chart highlights the shift from</tspan>
    <tspan x="126" dy="27">volume-led gains to margin-accretive performance.</tspan>
  </text>

  <rect x="126" y="494" width="118" height="68" rx="18" fill="#F2F7FF"/>
  <text x="146" y="520" width="80"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" fill="#667085">Revenue</text>
  <text x="146" y="548" width="90"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="25" font-weight="700" fill="#172033">+18%</text>

  <rect x="264" y="494" width="118" height="68" rx="18" fill="#F1FBF8"/>
  <text x="284" y="520" width="80"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" fill="#667085">Margin</text>
  <text x="284" y="548" width="90"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="25" font-weight="700" fill="#12805C">+6.4pt</text>

  <rect x="562" y="220" width="3" height="360" rx="1.5" fill="#C9D6E8"/>
  <circle cx="563.5" cy="206" r="6" fill="#2F80ED"/>
  <circle cx="563.5" cy="594" r="6" fill="#24C6DC"/>

  <rect x="604" y="198" width="584" height="424" rx="32" fill="url(#cardSheen)" filter="url(#softShadow)"/>
  <text x="642" y="246" width="340"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="22" font-weight="700"
        fill="#172033">Pipeline conversion by quarter</text>
  <text x="642" y="275" width="360"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="14"
        fill="#667085">Bars show qualified pipeline; line shows win-rate trend.</text>

  <rect x="1006" y="228" width="14" height="14" rx="3" fill="#2F80ED"/>
  <text x="1028" y="240" width="90"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" fill="#667085">Pipeline</text>
  <circle cx="1122" cy="235" r="6" fill="#24C6DC"/>
  <text x="1136" y="240" width="70"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" fill="#667085">Win rate</text>

  <line x1="664" y1="530" x2="1128" y2="530" stroke="#D8E2F0" stroke-width="1"/>
  <line x1="664" y1="480" x2="1128" y2="480" stroke="#E5ECF5" stroke-width="1"/>
  <line x1="664" y1="430" x2="1128" y2="430" stroke="#E5ECF5" stroke-width="1"/>
  <line x1="664" y1="380" x2="1128" y2="380" stroke="#E5ECF5" stroke-width="1"/>
  <line x1="664" y1="330" x2="1128" y2="330" stroke="#E5ECF5" stroke-width="1"/>

  <text x="626" y="535" width="36" text-anchor="end"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="12" fill="#98A2B3">0</text>
  <text x="626" y="435" width="36" text-anchor="end"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="12" fill="#98A2B3">50</text>
  <text x="626" y="335" width="36" text-anchor="end"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="12" fill="#98A2B3">100</text>

  <rect x="700" y="424" width="42" height="106" rx="10" fill="#CFE1FF"/>
  <rect x="770" y="392" width="42" height="138" rx="10" fill="#AFCBFF"/>
  <rect x="840" y="356" width="42" height="174" rx="10" fill="#82AFFF"/>
  <rect x="910" y="374" width="42" height="156" rx="10" fill="#5B95F5"/>
  <rect x="980" y="322" width="42" height="208" rx="10" fill="#2F80ED"/>
  <rect x="1050" y="300" width="42" height="230" rx="10" fill="#1769D8"/>

  <path d="M721,410 C768,398 780,370 791,365 C836,342 850,330 861,326 C910,308 930,346 931,344 C982,302 1002,292 1001,292 C1046,272 1067,258 1071,254"
        fill="none" stroke="#24C6DC" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>
  <circle cx="721" cy="410" r="7" fill="#24C6DC" stroke="#FFFFFF" stroke-width="3"/>
  <circle cx="791" cy="365" r="7" fill="#24C6DC" stroke="#FFFFFF" stroke-width="3"/>
  <circle cx="861" cy="326" r="7" fill="#24C6DC" stroke="#FFFFFF" stroke-width="3"/>
  <circle cx="931" cy="344" r="7" fill="#24C6DC" stroke="#FFFFFF" stroke-width="3"/>
  <circle cx="1001" cy="292" r="7" fill="#24C6DC" stroke="#FFFFFF" stroke-width="3"/>
  <circle cx="1071" cy="254" r="7" fill="#24C6DC" stroke="#FFFFFF" stroke-width="3"/>

  <text x="721" y="565" width="46" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" fill="#667085">Q1</text>
  <text x="791" y="565" width="46" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" fill="#667085">Q2</text>
  <text x="861" y="565" width="46" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" fill="#667085">Q3</text>
  <text x="931" y="565" width="46" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" fill="#667085">Q4</text>
  <text x="1001" y="565" width="46" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" fill="#667085">Q5</text>
  <text x="1071" y="565" width="46" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" fill="#667085">Q6</text>

  <rect x="896" y="286" width="122" height="42" rx="21" fill="#172033"/>
  <text x="957" y="313" width="104" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="14" font-weight="700" fill="#FFFFFF">Peak: 47%</text>
</svg>
```

## Avoid in this skill
- ❌ Using a real PowerPoint chart embedded as an image or `<foreignObject>`; instead, build the chart from editable SVG bars, lines, circles, and labels.
- ❌ Applying `filter` to `<line>` gridlines; shadows/glows should go on cards, paths, text, rects, or circles only.
- ❌ Letting the chart and narrative compete equally; the split should be obvious, with the header centered above both zones.
- ❌ Overfilling the left text column; this layout works best with one strong insight, a short paragraph, and 1–2 metric chips.

## Composition notes
- Keep the header centered in the top 20–25% of the slide; it acts as the common topic for both left text and right chart.
- Allocate roughly 40% width to the narrative column and 50% width to the chart card, leaving a slim divider and breathing room between them.
- Use muted neutrals for body text and gridlines, then repeat one accent gradient in the divider, chart line, and key labels for cohesion.
- The chart card should feel lighter and more dimensional than the left text panel, making the data visualization the primary focal area.