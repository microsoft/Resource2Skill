# SVG Recipe — Analytical Chart Showcase Layout

## Visual mechanism
A clean educational slide pairs a strong concept title and short definition with a large, centered statistical chart rendered as native SVG shapes. The chart is intentionally minimalist: light axes, sparse gridlines, translucent data marks, and one accent relationship line so the audience focuses on the data relationship rather than exact values.

## SVG primitives needed
- 2× `<rect>` for the off-white background and elevated chart card
- 1× `<rect>` for a small category tag pill
- 8× `<line>` for axes, gridlines, and tick marks
- 1× `<path>` for the soft confidence/relationship band behind the data
- 1× `<line>` for the main trend line
- 30+× `<circle>` for scatterplot points with semi-transparent fill
- 1× `<linearGradient>` for the subtle page background
- 1× `<linearGradient>` for the translucent confidence band
- 1× `<radialGradient>` for dimensional data point styling
- 1× `<filter id="cardShadow">` applied to the chart card
- 1× `<filter id="pointGlow">` applied to selected/highlighted points
- Multiple `<text>` elements with explicit `width` for category, title, subtitle, axis labels, tick labels, legend, and explanatory annotation

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="pageBg" x1="0" y1="0" x2="0" y2="720" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#ffffff"/>
      <stop offset="1" stop-color="#fafafa"/>
    </linearGradient>

    <linearGradient id="bandFill" x1="260" y1="300" x2="1020" y2="560" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#00BFFF" stop-opacity="0.10"/>
      <stop offset="0.55" stop-color="#00BFFF" stop-opacity="0.18"/>
      <stop offset="1" stop-color="#DB4437" stop-opacity="0.10"/>
    </linearGradient>

    <radialGradient id="pointFill" cx="35%" cy="30%" r="70%">
      <stop offset="0" stop-color="#A9ECFF" stop-opacity="0.95"/>
      <stop offset="0.55" stop-color="#00BFFF" stop-opacity="0.72"/>
      <stop offset="1" stop-color="#009ACD" stop-opacity="0.62"/>
    </radialGradient>

    <filter id="cardShadow" x="-10%" y="-15%" width="120%" height="135%">
      <feOffset dx="0" dy="10" result="off"/>
      <feGaussianBlur in="off" stdDeviation="14" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="pointGlow" x="-80%" y="-80%" width="260%" height="260%">
      <feGaussianBlur stdDeviation="3"/>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#pageBg)"/>

  <rect x="58" y="34" width="176" height="34" rx="17" fill="#F1F3F4"/>
  <text x="78" y="57" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" letter-spacing="1.6" fill="#6A6A6A">RELATIONSHIPS</text>

  <text x="0" y="126" width="1280" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="44" font-weight="800" letter-spacing="2.5" fill="#DB4437">SCATTERPLOT</text>
  <text x="210" y="172" width="860" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="22" font-style="italic" fill="#4F4F4F">“Scatterplots reveal the relationship between two variables by showing paired observations.”</text>

  <rect x="150" y="232" width="980" height="410" rx="28" fill="#FFFFFF" filter="url(#cardShadow)"/>
  <rect x="184" y="262" width="912" height="344" rx="18" fill="#FFFFFF"/>

  <text x="210" y="294" width="360" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="700" fill="#333333">Positive association example</text>
  <text x="210" y="318" width="430" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#777777">Each dot is one observation; the slope summarizes the relationship.</text>

  <line x1="250" y1="560" x2="1030" y2="560" stroke="#BDBDBD" stroke-width="2"/>
  <line x1="250" y1="300" x2="250" y2="560" stroke="#BDBDBD" stroke-width="2"/>

  <line x1="250" y1="508" x2="1030" y2="508" stroke="#E8E8E8" stroke-width="1"/>
  <line x1="250" y1="456" x2="1030" y2="456" stroke="#E8E8E8" stroke-width="1"/>
  <line x1="250" y1="404" x2="1030" y2="404" stroke="#E8E8E8" stroke-width="1"/>
  <line x1="250" y1="352" x2="1030" y2="352" stroke="#E8E8E8" stroke-width="1"/>
  <line x1="406" y1="300" x2="406" y2="560" stroke="#F0F0F0" stroke-width="1"/>
  <line x1="562" y1="300" x2="562" y2="560" stroke="#F0F0F0" stroke-width="1"/>
  <line x1="718" y1="300" x2="718" y2="560" stroke="#F0F0F0" stroke-width="1"/>
  <line x1="874" y1="300" x2="874" y2="560" stroke="#F0F0F0" stroke-width="1"/>

  <path d="M265 548 C410 512, 540 482, 690 430 C820 386, 930 344, 1015 303 L1015 358 C925 390, 810 432, 690 472 C540 522, 400 552, 265 584 Z" fill="url(#bandFill)"/>
  <line x1="265" y1="548" x2="1015" y2="330" stroke="#DB4437" stroke-width="4" stroke-linecap="round"/>

  <circle cx="295" cy="536" r="9" fill="url(#pointFill)" stroke="#FFFFFF" stroke-width="2"/>
  <circle cx="322" cy="511" r="8" fill="url(#pointFill)" stroke="#FFFFFF" stroke-width="2"/>
  <circle cx="350" cy="526" r="10" fill="url(#pointFill)" stroke="#FFFFFF" stroke-width="2"/>
  <circle cx="384" cy="494" r="8" fill="url(#pointFill)" stroke="#FFFFFF" stroke-width="2"/>
  <circle cx="418" cy="470" r="9" fill="url(#pointFill)" stroke="#FFFFFF" stroke-width="2"/>
  <circle cx="452" cy="501" r="8" fill="url(#pointFill)" stroke="#FFFFFF" stroke-width="2"/>
  <circle cx="486" cy="465" r="10" fill="url(#pointFill)" stroke="#FFFFFF" stroke-width="2"/>
  <circle cx="520" cy="447" r="8" fill="url(#pointFill)" stroke="#FFFFFF" stroke-width="2"/>
  <circle cx="556" cy="471" r="9" fill="url(#pointFill)" stroke="#FFFFFF" stroke-width="2"/>
  <circle cx="590" cy="433" r="10" fill="url(#pointFill)" stroke="#FFFFFF" stroke-width="2"/>
  <circle cx="626" cy="438" r="8" fill="url(#pointFill)" stroke="#FFFFFF" stroke-width="2"/>
  <circle cx="660" cy="408" r="9" fill="url(#pointFill)" stroke="#FFFFFF" stroke-width="2"/>
  <circle cx="694" cy="421" r="8" fill="url(#pointFill)" stroke="#FFFFFF" stroke-width="2"/>
  <circle cx="728" cy="388" r="11" fill="url(#pointFill)" stroke="#FFFFFF" stroke-width="2" filter="url(#pointGlow)"/>
  <circle cx="762" cy="402" r="8" fill="url(#pointFill)" stroke="#FFFFFF" stroke-width="2"/>
  <circle cx="796" cy="371" r="9" fill="url(#pointFill)" stroke="#FFFFFF" stroke-width="2"/>
  <circle cx="830" cy="384" r="8" fill="url(#pointFill)" stroke="#FFFFFF" stroke-width="2"/>
  <circle cx="864" cy="354" r="10" fill="url(#pointFill)" stroke="#FFFFFF" stroke-width="2"/>
  <circle cx="898" cy="365" r="9" fill="url(#pointFill)" stroke="#FFFFFF" stroke-width="2"/>
  <circle cx="932" cy="335" r="8" fill="url(#pointFill)" stroke="#FFFFFF" stroke-width="2"/>
  <circle cx="966" cy="348" r="10" fill="url(#pointFill)" stroke="#FFFFFF" stroke-width="2"/>
  <circle cx="1000" cy="318" r="9" fill="url(#pointFill)" stroke="#FFFFFF" stroke-width="2"/>

  <text x="230" y="588" width="820" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#666666">Variable X</text>
  <text x="112" y="430" width="120" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#666666" transform="rotate(-90 172 430)">Variable Y</text>

  <text x="238" y="566" width="42" text-anchor="end" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#888888">0</text>
  <text x="238" y="512" width="42" text-anchor="end" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#888888">25</text>
  <text x="238" y="460" width="42" text-anchor="end" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#888888">50</text>
  <text x="238" y="408" width="42" text-anchor="end" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#888888">75</text>
  <text x="238" y="356" width="42" text-anchor="end" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#888888">100</text>

  <rect x="835" y="276" width="220" height="58" rx="16" fill="#FFF5F3" stroke="#F3C6BE" stroke-width="1"/>
  <circle cx="862" cy="306" r="8" fill="url(#pointFill)" stroke="#FFFFFF" stroke-width="2"/>
  <line x1="890" y1="306" x2="940" y2="306" stroke="#DB4437" stroke-width="4" stroke-linecap="round"/>
  <text x="956" y="311" width="84" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#DB4437">trend line</text>
</svg>
```

## Avoid in this skill
- ❌ Embedding the chart as a screenshot when the relationship can be drawn with editable SVG circles, lines, and paths
- ❌ Heavy chart decoration: 3D bars, dense gridlines, thick borders, or saturated backgrounds that compete with the concept title
- ❌ Tiny numeric labels on every point; this layout teaches pattern recognition, not exact-value lookup
- ❌ Applying filters to `<line>` elements for axis shadows or glow; use clean flat lines instead
- ❌ Using `<foreignObject>` for rich text or HTML chart labels; keep all typography as native `<text>` with explicit `width`

## Composition notes
- Keep the top 20–25% of the slide for the category tag, concept title, and one-sentence definition.
- Center the chart card in the lower 70–75% with wide side margins so it reads like a textbook figure.
- Use one strong accent color for the title and trend line; use translucent cool colors for the data marks.
- Preserve whitespace inside the chart: sparse gridlines, light axes, and only one or two explanatory annotations.