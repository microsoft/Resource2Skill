# SVG Recipe — Intentional Data Highlight (Consulting Chart Refactoring)

## Visual mechanism
Strip the chart down to only category labels, horizontal bars, and outside-end value labels; make all context bars neutral grey and reserve one saturated accent color for the target category. Pair two clean bar-chart panels under a sentence-style takeaway title so the audience reads the conclusion first and then sees the evidence.

## SVG primitives needed
- 1× `<rect>` for the off-white slide background.
- 2× `<rect>` for subtle white chart panels/cards.
- 2× `<rect>` for small accent tabs beside each chart subtitle.
- 11× `<rect>` for horizontal data bars, with only the target category filled by the accent gradient.
- 1× `<rect>` for the “Focus: WhatsApp” pill.
- 2× `<path>` for thin accent brackets around the highlighted bar rows.
- 1× `<line>` for the title separator rule.
- Multiple `<text>` elements for the title, chart subtitles, category labels, value labels, and focus pill; every `<text>` has an explicit `width`.
- 1× `<linearGradient id="accentGrad">` for the highlighted bars.
- 1× `<filter id="softShadow">` applied only to the chart panel `<rect>` elements for a very subtle keynote-style lift.

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="accentGrad" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#E14444"/>
      <stop offset="100%" stop-color="#B91E2E"/>
    </linearGradient>
    <filter id="softShadow" x="-10%" y="-10%" width="120%" height="130%">
      <feOffset dx="0" dy="6"/>
      <feGaussianBlur stdDeviation="8"/>
      <feColorMatrix type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 .10 0"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#F7F8FA"/>

  <text x="56" y="58" width="1040" font-family="Segoe UI, Microsoft YaHei" font-size="30" font-weight="700" fill="#282828">
    WhatsApp’s expansive reach and daily usage make it the strongest channel for customer conversations
  </text>
  <rect x="1084" y="35" width="140" height="34" rx="17" fill="#F2E7E8"/>
  <text x="1102" y="58" width="108" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#B91E2E">
    Focus: WhatsApp
  </text>
  <line x1="56" y1="118" x2="1224" y2="118" stroke="#D5D7DA" stroke-width="1.2"/>

  <rect x="52" y="148" width="548" height="512" rx="18" fill="#FFFFFF" filter="url(#softShadow)"/>
  <rect x="680" y="148" width="548" height="512" rx="18" fill="#FFFFFF" filter="url(#softShadow)"/>

  <rect x="82" y="178" width="5" height="44" rx="2.5" fill="url(#accentGrad)"/>
  <text x="102" y="194" width="430" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#282828">
    Global messenger reach
  </text>
  <text x="102" y="218" width="430" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#787878">
    Monthly active users, millions
  </text>

  <rect x="710" y="178" width="5" height="44" rx="2.5" fill="url(#accentGrad)"/>
  <text x="730" y="194" width="430" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#282828">
    Engagement intensity
  </text>
  <text x="730" y="218" width="430" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#787878">
    Share of users opening the app daily, %
  </text>

  <!-- Left chart: reach -->
  <text x="92" y="266" width="160" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#B91E2E">WhatsApp</text>
  <rect x="262" y="244" width="270" height="28" rx="5" fill="url(#accentGrad)"/>
  <text x="546" y="266" width="45" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#B91E2E">2,000</text>
  <path d="M538 238 L562 238 L562 278 L538 278" fill="none" stroke="#B91E2E" stroke-width="2"/>

  <text x="92" y="320" width="160" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#282828">WeChat</text>
  <rect x="262" y="298" width="177" height="28" rx="5" fill="#D4D4D4"/>
  <text x="453" y="320" width="45" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#737373">1,313</text>

  <text x="92" y="374" width="160" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#282828">Messenger</text>
  <rect x="262" y="352" width="126" height="28" rx="5" fill="#D4D4D4"/>
  <text x="402" y="374" width="45" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#737373">931</text>

  <text x="92" y="428" width="160" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#282828">Telegram</text>
  <rect x="262" y="406" width="108" height="28" rx="5" fill="#D4D4D4"/>
  <text x="384" y="428" width="45" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#737373">800</text>

  <text x="92" y="482" width="160" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#282828">Snapchat</text>
  <rect x="262" y="460" width="101" height="28" rx="5" fill="#D4D4D4"/>
  <text x="377" y="482" width="45" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#737373">750</text>

  <text x="92" y="536" width="160" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#282828">Signal</text>
  <rect x="262" y="514" width="24" height="28" rx="5" fill="#D4D4D4"/>
  <text x="300" y="536" width="45" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#737373">40</text>

  <!-- Right chart: engagement -->
  <text x="720" y="266" width="160" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#B91E2E">WhatsApp</text>
  <rect x="890" y="244" width="249" height="28" rx="5" fill="url(#accentGrad)"/>
  <text x="1153" y="266" width="45" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#B91E2E">83%</text>
  <path d="M1145 238 L1169 238 L1169 278 L1145 278" fill="none" stroke="#B91E2E" stroke-width="2"/>

  <text x="720" y="320" width="160" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#282828">Messenger</text>
  <rect x="890" y="298" width="186" height="28" rx="5" fill="#D4D4D4"/>
  <text x="1090" y="320" width="45" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#737373">62%</text>

  <text x="720" y="374" width="160" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#282828">Telegram</text>
  <rect x="890" y="352" width="165" height="28" rx="5" fill="#D4D4D4"/>
  <text x="1069" y="374" width="45" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#737373">55%</text>

  <text x="720" y="428" width="160" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#282828">iMessage</text>
  <rect x="890" y="406" width="141" height="28" rx="5" fill="#D4D4D4"/>
  <text x="1045" y="428" width="45" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#737373">47%</text>

  <text x="720" y="482" width="160" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#282828">Signal</text>
  <rect x="890" y="460" width="66" height="28" rx="5" fill="#D4D4D4"/>
  <text x="970" y="482" width="45" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#737373">22%</text>

  <text x="82" y="620" width="490" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#8A8A8A">
    Note: axes and gridlines intentionally removed; values are encoded by bar length and labeled directly.
  </text>
  <text x="710" y="620" width="490" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#8A8A8A">
    Source: illustrative market benchmark; replace values while preserving highlight logic.
  </text>
</svg>
```

## Avoid in this skill
- ❌ Full chart axes, tick marks, gridlines, plot borders, or legends; they weaken the “consulting refactor” effect.
- ❌ Random categorical colors for each bar; only the strategic target should receive the accent color.
- ❌ Value labels inside short bars, where they become cramped or illegible; place labels just outside the bar end.
- ❌ Vertical bar charts when category names are long; horizontal bars preserve readability.
- ❌ SVG `<marker>` arrowheads or parent-inherited markers for annotations; use simple lines/paths or text callouts instead.

## Composition notes
- Reserve the top 15–20% of the slide for a complete sentence takeaway, then separate it from the evidence with a thin rule.
- Use two equal-width chart panels with a generous center gutter; each panel needs its own concise subtitle and metric descriptor.
- Keep category labels left-aligned, bars aligned to a common origin, and value labels placed consistently outside the bar ends.
- Use neutral greys for context, charcoal for readable text, and one saturated accent color repeated only on the target category, subtitle tab, and optional focus pill.