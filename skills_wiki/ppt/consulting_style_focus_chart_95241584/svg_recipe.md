# SVG Recipe — Consulting-Style Focus Chart

## Visual mechanism
A minimalist column chart uses neutral gray for all context data and one saturated accent color for the single point the audience should notice. Data labels replace the Y-axis, while a subtle focus band and annotation quantify the takeaway without adding chart clutter.

## SVG primitives needed
- 1× `<rect>` for the white slide background
- 1× `<rect>` for a pale vertical focus band behind the highlighted bar
- 7× `<rect>` for the column bars, with the final bar using an accent gradient
- 1× `<line>` for the understated X-axis baseline
- 2× `<line>` for a clean growth annotation connector
- 1× `<path>` for a custom arrowhead triangle
- 1× `<rect>` for the annotation pill
- 23× `<text>` for action title, subtitle, data labels, category labels, and annotation copy
- 1× `<linearGradient>` for the highlighted column fill
- 1× `<filter id="softShadow">` applied only to the highlighted bar and annotation pill

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="accentBlue" x1="0" y1="568" x2="0" y2="214" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#274A86"/>
      <stop offset="100%" stop-color="#3E6AB6"/>
    </linearGradient>

    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="6" in="SourceAlpha" result="offset"/>
      <feGaussianBlur stdDeviation="7" in="offset" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <!-- slide canvas -->
  <rect x="0" y="0" width="1280" height="720" fill="#FFFFFF"/>

  <!-- action title -->
  <text x="64" y="62" width="1050" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="30" font-weight="700" fill="#333333">
    Net sales grew <tspan fill="#2F528F">+400%</tspan> from 2015 to 2021
  </text>
  <text x="66" y="102" width="760" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="15" fill="#777777">
    Indexed revenue performance; values shown directly on columns to remove the need for a Y-axis
  </text>

  <!-- quiet section rule -->
  <line x1="64" y1="126" x2="1216" y2="126" stroke="#E6E6E6" stroke-width="1"/>

  <!-- chart focus band -->
  <rect x="956" y="158" width="158" height="438" rx="22" fill="#F2F6FC"/>

  <!-- annotation pill -->
  <rect x="826" y="168" width="230" height="54" rx="27" fill="#FFFFFF" filter="url(#softShadow)"/>
  <text x="852" y="201" width="180" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="20" font-weight="700" fill="#2F528F">+400% growth</text>

  <!-- annotation connector: use lines and a path arrowhead instead of marker-end -->
  <line x1="248" y1="455" x2="820" y2="222" stroke="#2F528F" stroke-width="2"/>
  <line x1="820" y1="222" x2="846" y2="222" stroke="#2F528F" stroke-width="2"/>
  <path d="M248 455 L263 450 L257 464 Z" fill="#2F528F"/>

  <!-- baseline -->
  <line x1="118" y1="568" x2="1120" y2="568" stroke="#BFBFBF" stroke-width="1.2"/>

  <!-- columns -->
  <rect x="148" y="499" width="74" height="69" rx="3" fill="#D9D9D9"/>
  <rect x="288" y="453" width="74" height="115" rx="3" fill="#D9D9D9"/>
  <rect x="428" y="361" width="74" height="207" rx="3" fill="#D9D9D9"/>
  <rect x="568" y="292" width="74" height="276" rx="3" fill="#D9D9D9"/>
  <rect x="708" y="384" width="74" height="184" rx="3" fill="#D9D9D9"/>
  <rect x="848" y="269" width="74" height="299" rx="3" fill="#D9D9D9"/>
  <rect x="988" y="223" width="74" height="345" rx="3" fill="url(#accentBlue)" filter="url(#softShadow)"/>

  <!-- value labels -->
  <text x="147" y="486" width="76" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="16" font-weight="600" fill="#595959">3</text>
  <text x="287" y="440" width="76" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="16" font-weight="600" fill="#595959">5</text>
  <text x="427" y="348" width="76" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="16" font-weight="600" fill="#595959">9</text>
  <text x="567" y="279" width="76" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="16" font-weight="600" fill="#595959">12</text>
  <text x="707" y="371" width="76" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="16" font-weight="600" fill="#595959">8</text>
  <text x="847" y="256" width="76" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="16" font-weight="600" fill="#595959">13</text>
  <text x="987" y="207" width="76" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="20" font-weight="700" fill="#2F528F">15</text>

  <!-- category labels -->
  <text x="147" y="602" width="76" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="14" fill="#595959">2015</text>
  <text x="287" y="602" width="76" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="14" fill="#595959">2016</text>
  <text x="427" y="602" width="76" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="14" fill="#595959">2017</text>
  <text x="567" y="602" width="76" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="14" fill="#595959">2018</text>
  <text x="707" y="602" width="76" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="14" fill="#595959">2019</text>
  <text x="847" y="602" width="76" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="14" fill="#595959">2020</text>
  <text x="987" y="602" width="76" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="15" font-weight="700" fill="#2F528F">2021</text>

  <!-- small source note -->
  <text x="66" y="668" width="560" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="12" fill="#9A9A9A">
    Source: Company analysis. Bars shown in USD millions.
  </text>
</svg>
```

## Avoid in this skill
- ❌ Heavy Y-axes, gridlines, borders, legends, or tick marks that compete with the highlighted point
- ❌ Rainbow coloring every bar; this destroys the intentional pre-attentive focus
- ❌ Relying on chart objects or embedded screenshots when editable SVG columns and labels are sufficient
- ❌ `marker-end` on `<path>` for annotation arrows; build the arrowhead with a small editable `<path>`
- ❌ Missing `width` attributes on `<text>` elements, which causes PowerPoint text rendering issues

## Composition notes
- Keep the title in the upper-left as an “action title” that states the conclusion, not merely the metric name.
- Reserve 70–80% of the slide width for the chart; leave generous white space around the plot to preserve a consulting-style feel.
- Use gray for context bars and labels, then repeat the same accent color in the highlighted bar, value label, title emphasis, and annotation.
- Remove the Y-axis entirely when values are labeled above each column; one thin X-axis baseline is enough visual structure.