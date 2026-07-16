# SVG Recipe — Contextual Data Storytelling Panel

## Visual mechanism
A semi-transparent rounded narrative panel floats above a full-slide data visualization, letting the audience see the evidence while the foreground copy explains the “so what.” The panel creates a controlled reading zone with strong hierarchy, while the chart remains visible as contextual proof.

## SVG primitives needed
- 1× `<rect>` full-slide background with subtle gradient
- 8–12× `<line>` for chart gridlines and axes
- 8–12× `<text>` for chart labels, axis labels, panel headline, and bullet narrative
- 1× `<path>` for filled chart area
- 1× `<path>` for main trend line
- 1× `<path>` for secondary comparison line
- 5–8× `<circle>` for emphasized data points and anomaly markers
- 1× `<rect>` translucent rounded storytelling panel
- 1× `<rect>` thin top accent strip inside the panel
- 1× `<filter id="panelShadow">` applied to the rounded panel
- 1× `<filter id="softGlow">` applied to the key data-point circle
- 2–3× `<linearGradient>` for background, chart fill, and panel accent

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#F8FAFC"/>
      <stop offset="55%" stop-color="#EEF6FA"/>
      <stop offset="100%" stop-color="#F7F2FF"/>
    </linearGradient>

    <linearGradient id="areaGrad" x1="0" y1="130" x2="0" y2="610">
      <stop offset="0%" stop-color="#2F80ED" stop-opacity="0.32"/>
      <stop offset="100%" stop-color="#2F80ED" stop-opacity="0.03"/>
    </linearGradient>

    <linearGradient id="accentGrad" x1="64" y1="0" x2="564" y2="0">
      <stop offset="0%" stop-color="#2F80ED"/>
      <stop offset="55%" stop-color="#00A6A6"/>
      <stop offset="100%" stop-color="#8E5CF7"/>
    </linearGradient>

    <filter id="panelShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feOffset dx="0" dy="14"/>
      <feGaussianBlur stdDeviation="18"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="softGlow" x="-80%" y="-80%" width="260%" height="260%">
      <feGaussianBlur stdDeviation="10"/>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>

  <text x="650" y="62" width="500" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="600" fill="#5B6575">
    Quarterly net revenue, indexed
  </text>

  <line x1="590" y1="610" x2="1180" y2="610" stroke="#D8DEE8" stroke-width="1"/>
  <line x1="590" y1="510" x2="1180" y2="510" stroke="#E5EAF2" stroke-width="1"/>
  <line x1="590" y1="410" x2="1180" y2="410" stroke="#E5EAF2" stroke-width="1"/>
  <line x1="590" y1="310" x2="1180" y2="310" stroke="#E5EAF2" stroke-width="1"/>
  <line x1="590" y1="210" x2="1180" y2="210" stroke="#E5EAF2" stroke-width="1"/>
  <line x1="590" y1="110" x2="1180" y2="110" stroke="#E5EAF2" stroke-width="1"/>

  <line x1="590" y1="110" x2="590" y2="610" stroke="#CBD5E1" stroke-width="1.3"/>
  <line x1="590" y1="610" x2="1180" y2="610" stroke="#CBD5E1" stroke-width="1.3"/>

  <text x="548" y="616" width="34" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#718096">80</text>
  <text x="540" y="516" width="42" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#718096">100</text>
  <text x="540" y="416" width="42" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#718096">120</text>
  <text x="540" y="316" width="42" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#718096">140</text>
  <text x="540" y="216" width="42" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#718096">160</text>

  <text x="600" y="642" width="56" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#718096">Q1</text>
  <text x="728" y="642" width="56" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#718096">Q2</text>
  <text x="856" y="642" width="56" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#718096">Q3</text>
  <text x="984" y="642" width="56" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#718096">Q4</text>
  <text x="1110" y="642" width="64" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#718096">Q1 ’25</text>

  <path d="M590 560 C635 548, 670 535, 715 525 C765 512, 805 498, 850 462 C895 424, 925 352, 970 282 C1016 210, 1064 236, 1112 198 C1140 176, 1160 150, 1180 132 L1180 610 L590 610 Z"
        fill="url(#areaGrad)"/>

  <path d="M590 560 C635 548, 670 535, 715 525 C765 512, 805 498, 850 462 C895 424, 925 352, 970 282 C1016 210, 1064 236, 1112 198 C1140 176, 1160 150, 1180 132"
        fill="none" stroke="#1F7AE0" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>

  <path d="M590 570 C655 558, 720 552, 785 538 C850 522, 905 498, 970 470 C1030 444, 1085 430, 1180 405"
        fill="none" stroke="#94A3B8" stroke-width="3" stroke-dasharray="9 8" stroke-linecap="round"/>

  <circle cx="850" cy="462" r="6" fill="#1F7AE0"/>
  <circle cx="970" cy="282" r="8" fill="#1F7AE0"/>
  <circle cx="1112" cy="198" r="7" fill="#1F7AE0"/>
  <circle cx="1180" cy="132" r="9" fill="#0F766E"/>
  <circle cx="970" cy="282" r="26" fill="#2F80ED" opacity="0.16" filter="url(#softGlow)"/>

  <text x="986" y="272" width="180" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#174EA6">
    Q3 acceleration
  </text>
  <text x="986" y="294" width="190" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#526173">
    conversion gains compound
  </text>

  <rect x="64" y="70" width="500" height="580" rx="34" fill="#F8FAFC" fill-opacity="0.90" filter="url(#panelShadow)"/>
  <rect x="92" y="102" width="170" height="7" rx="3.5" fill="url(#accentGrad)"/>

  <text x="92" y="156" width="420" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="700" letter-spacing="1.2" fill="#2F80ED">
    KEY TAKEAWAY
  </text>

  <text x="92" y="214" width="410" font-family="Segoe UI, Microsoft YaHei" font-size="36" font-weight="700" fill="#202833">
    Revenue growth is being pulled forward by retention, not volume.
  </text>

  <text x="92" y="300" width="408" font-family="Segoe UI, Microsoft YaHei" font-size="19" fill="#4B5563">
    The chart shows a sharp Q3 inflection, but the driver is less about new traffic and more about repeat buyers converting faster.
  </text>

  <circle cx="106" cy="370" r="5" fill="#2F80ED"/>
  <text x="126" y="377" width="370" font-family="Segoe UI, Microsoft YaHei" font-size="18" fill="#394150">
    Repeat-customer revenue rose 31% after the loyalty refresh.
  </text>

  <circle cx="106" cy="430" r="5" fill="#00A6A6"/>
  <text x="126" y="437" width="370" font-family="Segoe UI, Microsoft YaHei" font-size="18" fill="#394150">
    New-customer acquisition stayed flat, confirming this is quality growth.
  </text>

  <circle cx="106" cy="490" r="5" fill="#8E5CF7"/>
  <text x="126" y="497" width="370" font-family="Segoe UI, Microsoft YaHei" font-size="18" fill="#394150">
    Next step: segment the retention lift by product tier and market.
  </text>

  <rect x="92" y="560" width="390" height="58" rx="18" fill="#EAF4FF"/>
  <text x="116" y="596" width="340" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#174EA6">
    Decision: fund loyalty expansion before paid acquisition.
  </text>
</svg>
```

## Avoid in this skill
- ❌ Using an opaque panel that completely hides the chart; the point is to preserve evidence behind the story.
- ❌ Placing long paragraphs in the overlay; the panel should contain a headline, a short explanation, and 2–3 supporting points.
- ❌ Applying blur or filters to chart gridlines; filters on `<line>` are not reliably preserved.
- ❌ Using `clip-path` on the panel itself; if a cropped photo is needed, apply clipping only to an `<image>`.
- ❌ Building the chart as a flat screenshot when editable SVG lines, paths, circles, and labels can preserve PowerPoint editability.

## Composition notes
- Keep the storytelling panel on the left or right third, occupying roughly 35–45% of slide width; let the data visual breathe behind it.
- Use a translucent near-white panel with a soft shadow so the foreground reads cleanly without feeling pasted on.
- Reserve the strongest accent color for the key chart inflection and repeat that color in the panel’s label or bullets.
- Keep chart labels subdued; the narrative panel should be the dominant reading path, while the chart supplies context and credibility.