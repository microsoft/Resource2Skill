# SVG Recipe — Editorial Data Journalism Style (The Economist Method)

## Visual mechanism
A spare, print-editorial chart uses only horizontal gridlines, charcoal typography, and direct series labels; one high-saturation red line carries the argument while all comparison data recedes into grey. A thick red top rule and a conclusion-style headline make the slide feel like an authoritative data-journalism exhibit rather than a generic chart.

## SVG primitives needed
- 1× `<rect>` for the white slide background
- 2× `<rect>` for the signature red editorial masthead block and thin red underline
- 6× `<line>` for horizontal gridlines and one subtle baseline
- 3× `<path>` for the editable data series lines: one red highlight, two grey context series
- 3× `<circle>` for endpoint emphasis on the line series
- 1× `<path>` for a small red annotation leader bracket
- 20+× `<text>` for headline, subtitle, axis labels, direct series labels, annotation, and source note
- 1× `<filter id="softGlow">` with `feGaussianBlur` for a restrained glow behind the red endpoint
- 1× `<linearGradient id="fadeRed">` for a subtle editorial callout fill

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <filter id="softGlow" x="-80%" y="-80%" width="260%" height="260%">
      <feGaussianBlur stdDeviation="6"/>
    </filter>
    <linearGradient id="fadeRed" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#E3120B" stop-opacity="0.16"/>
      <stop offset="100%" stop-color="#E3120B" stop-opacity="0"/>
    </linearGradient>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#FFFFFF"/>

  <!-- Economist-like top anchor -->
  <rect x="104" y="48" width="184" height="12" fill="#E3120B"/>
  <rect x="104" y="64" width="1052" height="3" fill="#E3120B"/>
  <text x="104" y="106" width="840" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="34" font-weight="700" fill="#262626">
    Taiwan’s local identity has become the clear majority
  </text>
  <text x="104" y="138" width="780" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="18" fill="#555555">
    Taiwan, % of respondents identifying as:
  </text>

  <!-- Small editorial kicker -->
  <text x="104" y="184" width="610" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" fill="#777777">
    The highlighted series states the argument; grey lines provide context without competing for attention.
  </text>

  <!-- Chart frame coordinates: x=104..1014, y=246..586 -->
  <rect x="104" y="246" width="910" height="340" fill="url(#fadeRed)" opacity="0.55"/>

  <!-- Horizontal grid only -->
  <line x1="104" y1="586" x2="1014" y2="586" stroke="#CFCFCF" stroke-width="1"/>
  <line x1="104" y1="501" x2="1014" y2="501" stroke="#DFDFDF" stroke-width="1"/>
  <line x1="104" y1="416" x2="1014" y2="416" stroke="#DFDFDF" stroke-width="1"/>
  <line x1="104" y1="331" x2="1014" y2="331" stroke="#DFDFDF" stroke-width="1"/>
  <line x1="104" y1="246" x2="1014" y2="246" stroke="#DFDFDF" stroke-width="1"/>
  <line x1="104" y1="586" x2="1014" y2="586" stroke="#262626" stroke-width="1.4"/>

  <!-- Y-axis labels floated on the right; no axis line -->
  <text x="1038" y="591" width="42" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" font-weight="700" fill="#333333">0</text>
  <text x="1038" y="506" width="42" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" font-weight="700" fill="#333333">20</text>
  <text x="1038" y="421" width="42" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" font-weight="700" fill="#333333">40</text>
  <text x="1038" y="336" width="42" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" font-weight="700" fill="#333333">60</text>
  <text x="1038" y="251" width="42" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" font-weight="700" fill="#333333">80</text>
  <text x="1018" y="225" width="96" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" font-weight="700" fill="#555555">%</text>

  <!-- X-axis labels: sparse and editorial -->
  <text x="94" y="626" width="56" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" fill="#333333">1992</text>
  <text x="207" y="626" width="40" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" fill="#333333">95</text>
  <text x="346" y="626" width="56" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" fill="#333333">2000</text>
  <text x="491" y="626" width="40" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" fill="#333333">05</text>
  <text x="635" y="626" width="40" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" fill="#333333">10</text>
  <text x="779" y="626" width="40" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" fill="#333333">15</text>
  <text x="923" y="626" width="56" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" fill="#333333">2020</text>

  <!-- Context data: muted, direct-labelled, no legend box -->
  <path d="M104 399 C160 391 214 405 260 410 C330 420 390 416 450 428 C526 441 592 438 658 447 C728 457 790 449 854 462 C914 472 966 464 1014 456"
        fill="none" stroke="#A0A0A0" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M104 459 C164 466 220 454 276 470 C344 486 404 482 466 493 C538 505 604 500 668 511 C742 522 806 515 872 525 C930 535 972 529 1014 519"
        fill="none" stroke="#C4C4C4" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>

  <!-- Highlight data -->
  <path d="M104 505 C160 494 216 482 272 472 C338 459 398 451 462 431 C536 408 596 389 660 372 C734 351 796 340 860 325 C920 313 970 304 1014 292"
        fill="none" stroke="#E3120B" stroke-width="4.5" stroke-linecap="round" stroke-linejoin="round"/>

  <!-- Endpoint emphasis -->
  <circle cx="1014" cy="292" r="15" fill="#E3120B" opacity="0.22" filter="url(#softGlow)"/>
  <circle cx="1014" cy="292" r="5.5" fill="#E3120B"/>
  <circle cx="1014" cy="456" r="4.5" fill="#A0A0A0"/>
  <circle cx="1014" cy="519" r="4.5" fill="#C4C4C4"/>

  <!-- Direct labels -->
  <text x="1036" y="298" width="170" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="17" font-weight="700" fill="#E3120B">
    Taiwanese
  </text>
  <text x="1036" y="462" width="190" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" font-weight="700" fill="#777777">
    Taiwanese and Chinese
  </text>
  <text x="1036" y="525" width="120" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" font-weight="700" fill="#999999">
    Chinese
  </text>

  <!-- Minimal annotation, placed near the evidence -->
  <path d="M724 356 C760 332 802 314 852 306" fill="none" stroke="#E3120B" stroke-width="1.6" stroke-linecap="round"/>
  <text x="558" y="342" width="210" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="14" font-weight="700" fill="#E3120B">
    steady rise after 2010
  </text>

  <!-- Footer rule and source -->
  <line x1="104" y1="666" x2="1156" y2="666" stroke="#E5E5E5" stroke-width="1"/>
  <text x="104" y="692" width="620" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="12" fill="#777777">
    Source: Election Study Centre; The Economist-style illustrative reconstruction
  </text>
</svg>
```

## Avoid in this skill
- ❌ Default chart furniture: surrounding plot boxes, vertical gridlines, tick marks, heavy axes, or a separate legend panel
- ❌ Rainbow categorical palettes; this method works by using one aggressive red highlight against restrained greys
- ❌ Centered titles or decorative display fonts; use left-aligned editorial hierarchy with sober sans-serif typography
- ❌ Over-annotating every inflection point; use one or two direct labels and one concise annotation at most
- ❌ Blurry screenshot charts; build the chart from native `<line>`, `<path>`, `<circle>`, and `<text>` so it remains editable

## Composition notes
- Keep a strong left margin and align the red masthead, title, subtitle, plot area, and source to the same vertical column.
- Reserve the right side of the chart for floated y-axis values and direct series labels; this eliminates the need for a legend.
- Let the red line be the only saturated element below the title area; everything else should be charcoal, light grey, or white.
- Use generous whitespace above and below the chart so the slide feels like a magazine graphic, not a dense dashboard.