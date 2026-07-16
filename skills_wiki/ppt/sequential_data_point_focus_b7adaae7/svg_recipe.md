# SVG Recipe — Sequential Data Point Focus

## Visual mechanism
Build the chart as editable SVG shapes, then dim every non-story data point to a quiet gray while one selected bar receives a saturated fill, glow/shadow, and a short annotation. Duplicate the slide for each focus step, changing only the active bar, label, and callout, then use a Fade transition in PowerPoint.

## SVG primitives needed
- 2× `<rect>` for the slide background and main chart card
- 5× `<rect>` for vertical bars, with inactive bars in muted gray and one active bar in accent color
- 1× extra `<rect>` behind the active bar for a soft focus glow
- 4× `<line>` for subtle horizontal gridlines
- 1× `<line>` for the annotation connector
- 1× `<path>` for the connector arrowhead triangle
- 5× `<circle>` for sequence-progress dots showing which data point is currently active
- Multiple `<text>` elements for title, subtitle, axis labels, category labels, data labels, callout copy, and sequence label
- 1× `<linearGradient id="activeBar">` for the highlighted data point
- 1× `<filter id="cardShadow">` for the chart card shadow
- 1× `<filter id="activeGlow">` for the highlighted bar glow
- 1× `<filter id="labelShadow">` for the annotation pill shadow

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="activeBar" x1="0" y1="565" x2="0" y2="370" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#2F528F"/>
      <stop offset="100%" stop-color="#4EACA0"/>
    </linearGradient>

    <filter id="cardShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feOffset dx="0" dy="14"/>
      <feGaussianBlur stdDeviation="18"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="activeGlow" x="-80%" y="-40%" width="260%" height="200%">
      <feGaussianBlur stdDeviation="18"/>
    </filter>

    <filter id="labelShadow" x="-30%" y="-40%" width="160%" height="180%">
      <feOffset dx="0" dy="8"/>
      <feGaussianBlur stdDeviation="10"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#F4F7FB"/>
  <circle cx="1085" cy="120" r="180" fill="#E7F3F1" opacity="0.65"/>
  <circle cx="160" cy="650" r="150" fill="#E9EEF8" opacity="0.75"/>

  <rect x="76" y="58" width="1128" height="604" rx="34" fill="#FFFFFF" filter="url(#cardShadow)"/>

  <text x="116" y="118" width="650" font-family="Segoe UI, Microsoft YaHei" font-size="31" font-weight="700" fill="#172033">
    App Downloads 2020
  </text>
  <text x="116" y="150" width="720" font-family="Segoe UI, Microsoft YaHei" font-size="16" fill="#667085">
    Sequential focus state: spotlight the current data point, mute the rest
  </text>

  <rect x="933" y="92" width="158" height="34" rx="17" fill="#EFF6F5"/>
  <text x="958" y="115" width="115" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#2F8278">
    Focus 5 of 5
  </text>
  <circle cx="1118" cy="109" r="5" fill="#CBD5E1"/>
  <circle cx="1135" cy="109" r="5" fill="#CBD5E1"/>
  <circle cx="1152" cy="109" r="5" fill="#CBD5E1"/>
  <circle cx="1169" cy="109" r="5" fill="#CBD5E1"/>
  <circle cx="1186" cy="109" r="6" fill="#4EACA0"/>

  <line x1="150" y1="485" x2="1095" y2="485" stroke="#E6EAF0" stroke-width="1.2" stroke-dasharray="5 7"/>
  <line x1="150" y1="405" x2="1095" y2="405" stroke="#E6EAF0" stroke-width="1.2" stroke-dasharray="5 7"/>
  <line x1="150" y1="325" x2="1095" y2="325" stroke="#E6EAF0" stroke-width="1.2" stroke-dasharray="5 7"/>
  <line x1="150" y1="245" x2="1095" y2="245" stroke="#E6EAF0" stroke-width="1.2" stroke-dasharray="5 7"/>

  <text x="108" y="489" width="35" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#98A2B3">200</text>
  <text x="108" y="409" width="35" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#98A2B3">400</text>
  <text x="108" y="329" width="35" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#98A2B3">600</text>
  <text x="108" y="249" width="35" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#98A2B3">800</text>

  <rect x="196" y="225" width="104" height="340" rx="12" fill="#D3D8E0"/>
  <rect x="376" y="325" width="104" height="240" rx="12" fill="#D3D8E0"/>
  <rect x="556" y="349" width="104" height="216" rx="12" fill="#D3D8E0"/>
  <rect x="736" y="364" width="104" height="201" rx="12" fill="#D3D8E0"/>

  <rect x="901" y="342" width="134" height="236" rx="24" fill="#4EACA0" opacity="0.30" filter="url(#activeGlow)"/>
  <rect x="916" y="374" width="104" height="191" rx="12" fill="url(#activeBar)"/>

  <text x="202" y="211" width="92" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" text-anchor="middle" fill="#98A2B3">850M</text>
  <text x="382" y="311" width="92" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" text-anchor="middle" fill="#98A2B3">600M</text>
  <text x="562" y="335" width="92" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" text-anchor="middle" fill="#98A2B3">540M</text>
  <text x="742" y="350" width="92" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" text-anchor="middle" fill="#98A2B3">503M</text>
  <text x="922" y="358" width="92" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="800" text-anchor="middle" fill="#2F528F">477M</text>

  <text x="196" y="604" width="104" font-family="Segoe UI, Microsoft YaHei" font-size="15" text-anchor="middle" fill="#667085">TikTok</text>
  <text x="366" y="604" width="124" font-family="Segoe UI, Microsoft YaHei" font-size="15" text-anchor="middle" fill="#667085">WhatsApp</text>
  <text x="546" y="604" width="124" font-family="Segoe UI, Microsoft YaHei" font-size="15" text-anchor="middle" fill="#667085">Facebook</text>
  <text x="726" y="604" width="124" font-family="Segoe UI, Microsoft YaHei" font-size="15" text-anchor="middle" fill="#667085">Instagram</text>
  <text x="916" y="604" width="104" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="800" text-anchor="middle" fill="#172033">Zoom</text>

  <rect x="835" y="206" width="302" height="92" rx="18" fill="#172033" filter="url(#labelShadow)"/>
  <text x="858" y="235" width="254" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="800" fill="#FFFFFF">
    Spotlight insight
  </text>
  <text x="858" y="263" width="254" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#BFE7E1">
    Zoom enters the top five
  </text>
  <text x="858" y="286" width="254" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#D7DEE8">
    A late-year surge becomes the closing focus point.
  </text>

  <line x1="965" y1="298" x2="965" y2="366" stroke="#172033" stroke-width="2"/>
  <path d="M965 374 L957 360 L973 360 Z" fill="#172033"/>

  <text x="150" y="642" width="945" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#98A2B3">
    Tip: duplicate this slide, move the accent fill and callout to the next bar, and apply Fade between slides.
  </text>
</svg>
```

## Avoid in this skill
- ❌ Do not use a live embedded chart if you need fully editable individual data-point states; draw the bars as SVG `<rect>` elements instead.
- ❌ Do not animate the highlight inside SVG with `<animate>` or `<animateTransform>`; create one static SVG state per slide and use PowerPoint transitions.
- ❌ Do not keep all bars saturated; the technique depends on strong contrast between muted context and one active point.
- ❌ Do not use `marker-end` on a `<path>` for callout arrows; draw the connector as a `<line>` plus a small triangular `<path>` arrowhead.
- ❌ Do not overload the chart with heavy axes, legends, and gridlines; this weakens the sequential focus effect.

## Composition notes
- Keep the chart as the hero element, occupying roughly the central 70–80% of the slide, with generous margins and a clean title band.
- Use low-contrast gridlines and muted labels so the active bar, value label, and callout dominate immediately.
- Place the callout near the highlighted point, not in a detached legend area; the audience should not have to search for the insight.
- For a sequence, preserve identical bar positions across slides and change only the highlighted bar, progress indicator, and annotation copy.