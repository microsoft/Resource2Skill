# SVG Recipe — Newspaper Article 3-Column

## Visual mechanism
A formal editorial page uses a large newspaper-style headline above three narrow text columns, with fine hairline rules and an embedded photo interrupting the center column. Dense body copy, restrained monochrome typography, and small captions create the feeling of a premium report or feature article.

## SVG primitives needed
- 2× `<rect>` for the warm page background and subtle paper sheet panel
- 8× `<line>` for masthead rules, headline divider, column separators, and caption rule
- 1× `<image>` for the embedded editorial photo in the center column
- 1× `<clipPath>` with rounded `<rect>` applied to the image crop
- 1× `<filter id="paperShadow">` applied to the paper panel
- 1× `<linearGradient>` for the slight off-white paper tone
- 1× `<radialGradient>` for a soft spotlight behind the headline area
- Multiple `<text>` elements with nested `<tspan>` for kicker, headline, byline, body columns, drop cap, caption, and footer metadata

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="paperTone" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#fbfaf5"/>
      <stop offset="100%" stop-color="#f0eee6"/>
    </linearGradient>
    <radialGradient id="headlineGlow" cx="50%" cy="18%" r="62%">
      <stop offset="0%" stop-color="#ffffff" stop-opacity="0.92"/>
      <stop offset="100%" stop-color="#f4f1e8" stop-opacity="0"/>
    </radialGradient>
    <filter id="paperShadow" x="-10%" y="-10%" width="120%" height="120%">
      <feOffset dx="0" dy="10" result="offset"/>
      <feGaussianBlur in="offset" stdDeviation="16" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <clipPath id="photoCrop">
      <rect x="466" y="286" width="348" height="196" rx="3" ry="3"/>
    </clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#d9d3c6"/>
  <rect x="42" y="28" width="1196" height="664" rx="8" fill="url(#paperTone)" filter="url(#paperShadow)"/>
  <rect x="42" y="28" width="1196" height="220" rx="8" fill="url(#headlineGlow)"/>

  <line x1="70" y1="60" x2="1210" y2="60" stroke="#1d1d1b" stroke-width="1.2"/>
  <line x1="70" y1="86" x2="1210" y2="86" stroke="#1d1d1b" stroke-width="0.7"/>
  <line x1="70" y1="198" x2="1210" y2="198" stroke="#1d1d1b" stroke-width="2"/>
  <line x1="70" y1="204" x2="1210" y2="204" stroke="#1d1d1b" stroke-width="0.6"/>

  <text x="70" y="78" width="350" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="12" font-weight="700" letter-spacing="2.2" fill="#20201e">
    GLOBAL BUSINESS REVIEW
  </text>
  <text x="930" y="78" width="280" text-anchor="end" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="11" letter-spacing="1.2" fill="#55524a">
    MONDAY EDITION · STRATEGY REPORT
  </text>

  <text x="70" y="132" width="1010" font-family="Georgia, 'Times New Roman', serif" font-size="54" font-weight="700" fill="#11110f">
    <tspan x="70" dy="0">Boards Rewrite the Rules for</tspan>
    <tspan x="70" dy="56">Growth in a Higher-Rate Era</tspan>
  </text>

  <text x="70" y="226" width="520" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="12" letter-spacing="1.1" fill="#56524a">
    BY ELENA MORRIS · SENIOR MARKETS CORRESPONDENT
  </text>
  <text x="835" y="226" width="375" text-anchor="end" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="12" fill="#56524a">
    Analysis based on 142 executive interviews
  </text>

  <line x1="426" y1="244" x2="426" y2="650" stroke="#b9b2a4" stroke-width="0.8"/>
  <line x1="854" y1="244" x2="854" y2="650" stroke="#b9b2a4" stroke-width="0.8"/>

  <text x="70" y="286" width="58" font-family="Georgia, 'Times New Roman', serif" font-size="74" font-weight="700" fill="#151512">
    T
  </text>
  <text x="126" y="260" width="270" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" fill="#22221f">
    <tspan x="126" dy="0">he latest operating plans from global</tspan>
    <tspan x="126" dy="22">leaders suggest that efficiency is no</tspan>
    <tspan x="126" dy="22">longer a defensive theme. It has become</tspan>
    <tspan x="126" dy="22">the primary source of strategic optionality.</tspan>
  </text>
  <text x="70" y="360" width="330" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" fill="#22221f">
    <tspan x="70" dy="0">Across industries, management teams are</tspan>
    <tspan x="70" dy="22">rebalancing capital away from broad, multi-</tspan>
    <tspan x="70" dy="22">year transformation programs and toward</tspan>
    <tspan x="70" dy="22">smaller bets with faster proof points.</tspan>
    <tspan x="70" dy="28">The result is a sharper editorial narrative:</tspan>
    <tspan x="70" dy="22">growth is still possible, but the bar for</tspan>
    <tspan x="70" dy="22">funding it has moved substantially higher.</tspan>
    <tspan x="70" dy="28">Executives describe a market in which speed,</tspan>
    <tspan x="70" dy="22">pricing discipline, and operational data now</tspan>
    <tspan x="70" dy="22">carry more weight than headline expansion.</tspan>
  </text>

  <text x="466" y="260" width="348" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" fill="#22221f">
    <tspan x="466" dy="0">A quieter but more consequential shift is</tspan>
    <tspan x="466" dy="22">happening inside the annual planning cycle.</tspan>
  </text>
  <image x="466" y="286" width="348" height="196" preserveAspectRatio="xMidYMid slice" clip-path="url(#photoCrop)"
         href="https://images.example.com/editorial-boardroom-city-skyline-16x9.jpg"/>
  <line x1="466" y1="500" x2="814" y2="500" stroke="#1d1d1b" stroke-width="0.8"/>
  <text x="466" y="520" width="348" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="11" fill="#615d53">
    <tspan x="466" dy="0">Above: finance and strategy leaders increasingly use</tspan>
    <tspan x="466" dy="16">short-cycle reviews to redirect capital before year end.</tspan>
  </text>
  <text x="466" y="568" width="348" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" fill="#22221f">
    <tspan x="466" dy="0">The most advanced organizations are creating</tspan>
    <tspan x="466" dy="22">rolling investment forums, replacing fixed</tspan>
    <tspan x="466" dy="22">budget rituals with evidence-led reviews.</tspan>
    <tspan x="466" dy="22">That makes the operating model feel less like</tspan>
    <tspan x="466" dy="22">an annual contract and more like a newsroom.</tspan>
  </text>

  <text x="894" y="260" width="316" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" fill="#22221f">
    <tspan x="894" dy="0">Three signals stand out. First, teams are</tspan>
    <tspan x="894" dy="22">compressing decision windows from quarters</tspan>
    <tspan x="894" dy="22">to weeks. Second, they are separating durable</tspan>
    <tspan x="894" dy="22">platform investments from discretionary</tspan>
    <tspan x="894" dy="22">growth experiments. Third, they are asking</tspan>
    <tspan x="894" dy="22">leaders to explain not only upside, but also</tspan>
    <tspan x="894" dy="22">the trigger that would stop an initiative.</tspan>
    <tspan x="894" dy="30">This approach favors clarity over theater.</tspan>
    <tspan x="894" dy="22">It gives boards a consistent way to compare</tspan>
    <tspan x="894" dy="22">AI programs, geographic expansion, pricing</tspan>
    <tspan x="894" dy="22">moves, and cost redesign on the same page.</tspan>
    <tspan x="894" dy="30">For report decks, the format works because</tspan>
    <tspan x="894" dy="22">it makes dense material feel intentional:</tspan>
    <tspan x="894" dy="22">a strong headline, disciplined columns, and</tspan>
    <tspan x="894" dy="22">one visual proof point anchoring the story.</tspan>
  </text>

  <line x1="70" y1="664" x2="1210" y2="664" stroke="#1d1d1b" stroke-width="0.8"/>
  <text x="70" y="684" width="360" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="10" letter-spacing="1" fill="#6a665d">
    THE EXECUTIVE LEDGER
  </text>
  <text x="1210" y="684" width="360" text-anchor="end" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="10" letter-spacing="1" fill="#6a665d">
    PAGE 04 · STRATEGY & CAPITAL ALLOCATION
  </text>
</svg>
```

## Avoid in this skill
- ❌ Relying on automatic text wrapping; use explicit `<tspan>` line breaks and set `width=` on every `<text>` element.
- ❌ Applying `clip-path` to text or decorative shapes; only clip the embedded `<image>`.
- ❌ Using `<pattern>` for paper grain or halftone texture; simulate editorial texture with subtle gradients, rules, and typography instead.
- ❌ Overusing color blocks or card grids, which breaks the newspaper illusion; keep the palette mostly ink, ivory, and muted gray.

## Composition notes
- Keep the headline in the upper third with generous leading; it should dominate before the reader enters the columns.
- Use three equal-width columns with narrow gutters and vertical hairlines to create editorial density without looking messy.
- Place the image in the center column so it interrupts the rhythm like a real article feature photo; keep the caption small and ruled.
- Maintain a restrained color rhythm: warm paper, near-black ink, gray metadata, and only subtle shading for depth.