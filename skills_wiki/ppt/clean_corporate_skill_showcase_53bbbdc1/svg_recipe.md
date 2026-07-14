# SVG Recipe — Clean Corporate Skill Showcase

## Visual mechanism
A premium corporate metrics slide turns a skills list into a calm, executive data display: left-aligned skill names, right-aligned percentages, and proportional rounded progress bars with a dark-blue-to-cyan gradient. The final SVG represents the completed state; in PowerPoint, the fill bars can be given sequential left-to-right wipe animations for the intended reveal.

## SVG primitives needed
- 1× `<rect>` for the full-slide lavender-gray background
- 1× large rounded `<rect>` for the central white content card with soft shadow
- 1× small rounded `<rect>` for the section eyebrow pill
- 7× light gray rounded `<rect>` for progress bar tracks
- 7× gradient rounded `<rect>` for progress bar fills
- 7× small `<circle>` elements for status dots beside skill labels
- 3× decorative blurred `<circle>` elements for ambient cyan/blue glow
- 2× decorative `<path>` elements for subtle corporate background swooshes
- Multiple `<text>` elements with explicit `width` for title, subtitle, skill labels, and percentages
- 2× `<linearGradient>` definitions for background polish and progress bars
- 1× `<radialGradient>` definition for glow accents
- 2× `<filter>` definitions: one soft card shadow and one ambient blur/glow

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgWash" x1="0" y1="0" x2="1280" y2="720" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#F2F2F7"/>
      <stop offset="0.58" stop-color="#EDEDF2"/>
      <stop offset="1" stop-color="#E4E9F2"/>
    </linearGradient>

    <linearGradient id="barGrad" x1="420" y1="0" x2="1020" y2="0" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#2F334A"/>
      <stop offset="0.62" stop-color="#317EA4"/>
      <stop offset="1" stop-color="#33C2DB"/>
    </linearGradient>

    <radialGradient id="cyanGlow" cx="50%" cy="50%" r="50%">
      <stop offset="0" stop-color="#33C2DB" stop-opacity="0.45"/>
      <stop offset="1" stop-color="#33C2DB" stop-opacity="0"/>
    </radialGradient>

    <filter id="cardShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="18"/>
      <feGaussianBlur stdDeviation="18"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="softGlow" x="-80%" y="-80%" width="260%" height="260%">
      <feGaussianBlur stdDeviation="24"/>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgWash)"/>

  <circle cx="1110" cy="110" r="150" fill="url(#cyanGlow)" filter="url(#softGlow)"/>
  <circle cx="185" cy="625" r="115" fill="#2F334A" opacity="0.08" filter="url(#softGlow)"/>
  <circle cx="1010" cy="610" r="72" fill="#33C2DB" opacity="0.14" filter="url(#softGlow)"/>

  <path d="M-20,198 C150,126 256,138 386,198 C532,266 676,248 806,178 C900,128 1000,101 1130,125 C1203,139 1260,166 1305,196"
        fill="none" stroke="#FFFFFF" stroke-width="2" opacity="0.62"/>
  <path d="M932,46 C1028,72 1089,140 1112,223 C1141,326 1209,379 1320,392"
        fill="none" stroke="#33C2DB" stroke-width="4" stroke-linecap="round" opacity="0.22"/>

  <rect x="122" y="86" width="1036" height="552" rx="34" fill="#FFFFFF" opacity="0.96" filter="url(#cardShadow)"/>
  <rect x="122" y="86" width="1036" height="552" rx="34" fill="none" stroke="#FFFFFF" stroke-width="2" opacity="0.75"/>

  <rect x="178" y="132" width="142" height="34" rx="17" fill="#E7F7FA"/>
  <text x="197" y="154" width="108" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="14" font-weight="700" letter-spacing="1.7" fill="#2F334A">CAPABILITY</text>

  <text x="178" y="214" width="340" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="48" font-weight="800" letter-spacing="2.5" fill="#2F334A">OUR SKILLS</text>
  <text x="178" y="248" width="420" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="17" fill="#8B8FA0">
    Quantified expertise across delivery, growth, and digital product disciplines.
  </text>

  <line x1="585" y1="134" x2="585" y2="590" stroke="#E6E7ED" stroke-width="1"/>
  <text x="620" y="154" width="210" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" font-weight="700" letter-spacing="1.4" fill="#9A9AA5">DISCIPLINE</text>
  <text x="1012" y="154" width="74" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" font-weight="700" letter-spacing="1.4" fill="#9A9AA5" text-anchor="end">SCORE</text>

  <g transform="translate(620 196)">
    <circle cx="0" cy="8" r="5" fill="#33C2DB"/>
    <text x="20" y="14" width="220" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="20" fill="#2F334A">Web Development</text>
    <text x="466" y="14" width="70" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="20" fill="#9E9E9E" text-anchor="end">90%</text>
    <rect x="20" y="34" width="516" height="12" rx="6" fill="#DCDCE2"/>
    <rect x="20" y="34" width="464" height="12" rx="6" fill="url(#barGrad)"/>
  </g>

  <g transform="translate(620 252)">
    <circle cx="0" cy="8" r="5" fill="#33C2DB"/>
    <text x="20" y="14" width="220" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="20" fill="#2F334A">Mobile App</text>
    <text x="466" y="14" width="70" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="20" fill="#9E9E9E" text-anchor="end">100%</text>
    <rect x="20" y="34" width="516" height="12" rx="6" fill="#DCDCE2"/>
    <rect x="20" y="34" width="516" height="12" rx="6" fill="url(#barGrad)"/>
  </g>

  <g transform="translate(620 308)">
    <circle cx="0" cy="8" r="5" fill="#33C2DB"/>
    <text x="20" y="14" width="220" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="20" fill="#2F334A">Social Media</text>
    <text x="466" y="14" width="70" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="20" fill="#9E9E9E" text-anchor="end">95%</text>
    <rect x="20" y="34" width="516" height="12" rx="6" fill="#DCDCE2"/>
    <rect x="20" y="34" width="490" height="12" rx="6" fill="url(#barGrad)"/>
  </g>

  <g transform="translate(620 364)">
    <circle cx="0" cy="8" r="5" fill="#33C2DB"/>
    <text x="20" y="14" width="220" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="20" fill="#2F334A">Photography</text>
    <text x="466" y="14" width="70" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="20" fill="#9E9E9E" text-anchor="end">100%</text>
    <rect x="20" y="34" width="516" height="12" rx="6" fill="#DCDCE2"/>
    <rect x="20" y="34" width="516" height="12" rx="6" fill="url(#barGrad)"/>
  </g>

  <g transform="translate(620 420)">
    <circle cx="0" cy="8" r="5" fill="#33C2DB"/>
    <text x="20" y="14" width="220" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="20" fill="#2F334A">SEO</text>
    <text x="466" y="14" width="70" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="20" fill="#9E9E9E" text-anchor="end">100%</text>
    <rect x="20" y="34" width="516" height="12" rx="6" fill="#DCDCE2"/>
    <rect x="20" y="34" width="516" height="12" rx="6" fill="url(#barGrad)"/>
  </g>

  <g transform="translate(620 476)">
    <circle cx="0" cy="8" r="5" fill="#33C2DB"/>
    <text x="20" y="14" width="220" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="20" fill="#2F334A">Marketing</text>
    <text x="466" y="14" width="70" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="20" fill="#9E9E9E" text-anchor="end">95%</text>
    <rect x="20" y="34" width="516" height="12" rx="6" fill="#DCDCE2"/>
    <rect x="20" y="34" width="490" height="12" rx="6" fill="url(#barGrad)"/>
  </g>

  <g transform="translate(620 532)">
    <circle cx="0" cy="8" r="5" fill="#33C2DB"/>
    <text x="20" y="14" width="220" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="20" fill="#2F334A">UI Design</text>
    <text x="466" y="14" width="70" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="20" fill="#9E9E9E" text-anchor="end">85%</text>
    <rect x="20" y="34" width="516" height="12" rx="6" fill="#DCDCE2"/>
    <rect x="20" y="34" width="439" height="12" rx="6" fill="url(#barGrad)"/>
  </g>
</svg>
```

## Avoid in this skill
- ❌ SVG `<animate>` or `<animateTransform>` for the wipe effect; create the completed SVG state, then apply PowerPoint wipe/fly/fade animations after translation.
- ❌ `clip-path` on progress bar rectangles; it will be ignored for non-image elements, so use actual bar widths for each percentage.
- ❌ `marker-end` arrowheads for callouts; this technique does not need arrows, and SVG marker behavior is unreliable in translation.
- ❌ Overly dense gridlines or chart furniture; the premium look depends on generous whitespace and a restrained data table.
- ❌ Filters on `<line>` elements; use filters only on rectangles, circles, paths, or text.

## Composition notes
- Keep the title block on the left third and the metrics table on the right two-thirds; this creates a polished editorial layout instead of a plain list.
- Use a soft white card over a lavender-gray background to make the content feel elevated and presentation-ready.
- Maintain consistent vertical rhythm: each skill row should have a label, percentage, track, and fill bar aligned to the same baseline.
- For animation in PowerPoint, sequence each row as: skill label fly-in from left, gradient bar wipe from left, percentage fade-in.