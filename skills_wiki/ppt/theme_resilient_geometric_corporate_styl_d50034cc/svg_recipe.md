# SVG Recipe — Theme-Resilient Geometric Corporate Style

## Visual mechanism
A strong corporate slide frame is built from edge-anchored geometric primitives: vertical accent stripes, partially cropped circles, and oversized concentric rings. The center remains a disciplined content safe zone with explicit text widths and consistent margins so the slide survives theme swaps, edits, and chart/data substitutions.

## SVG primitives needed
- 1× `<rect>` for the full-slide theme background
- 3× `<rect>` for right-edge vertical accent stripes
- 1× `<circle>` for the cropped bottom-right anchor disk
- 4× `<circle>` for oversized left-side concentric outline rings
- 1× `<rect>` for the central editable data/chart panel
- 4× `<rect>` for KPI tiles inside the panel
- 5× `<rect>` for editable vertical bar-chart bars
- 5× `<circle>` for bar-chart data markers
- 2× `<line>` for clean chart axes/rules
- 1× `<path>` for a small angular corporate logo mark
- Multiple `<text>` elements with explicit `width` attributes for title, subtitle, labels, metrics, and chart annotations
- 1× `<linearGradient id="bgGradient">` for a theme-like dimensional background
- 1× `<linearGradient id="panelGradient">` for a premium translucent panel treatment
- 1× `<filter id="softShadow">` applied to the central panel and KPI tiles
- 1× `<filter id="accentGlow">` applied to the bottom-right circle for subtle depth

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGradient" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#2436D6"/>
      <stop offset="62%" stop-color="#1E2DB7"/>
      <stop offset="100%" stop-color="#172282"/>
    </linearGradient>

    <linearGradient id="panelGradient" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.18"/>
      <stop offset="100%" stop-color="#FFFFFF" stop-opacity="0.08"/>
    </linearGradient>

    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="14"/>
      <feGaussianBlur stdDeviation="16"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="accentGlow" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="10"/>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGradient)"/>

  <!-- Left oversized concentric rings: decorative, edge-anchored, non-content -->
  <circle cx="-100" cy="360" r="255" fill="none" stroke="#FFFFFF" stroke-opacity="0.18" stroke-width="2"/>
  <circle cx="-100" cy="360" r="315" fill="none" stroke="#FFFFFF" stroke-opacity="0.14" stroke-width="2"/>
  <circle cx="-100" cy="360" r="375" fill="none" stroke="#FFFFFF" stroke-opacity="0.10" stroke-width="2"/>
  <circle cx="-100" cy="360" r="435" fill="none" stroke="#FFFFFF" stroke-opacity="0.07" stroke-width="2"/>

  <!-- Right-edge vertical accent stripes -->
  <rect x="1148" y="0" width="18" height="430" fill="#EB3440"/>
  <rect x="1192" y="0" width="18" height="430" fill="#EB3440"/>
  <rect x="1236" y="0" width="18" height="430" fill="#EB3440"/>

  <!-- Cropped bottom-right anchor circle -->
  <circle cx="1240" cy="705" r="145" fill="#EB3440" filter="url(#accentGlow)" opacity="0.95"/>
  <circle cx="1240" cy="705" r="145" fill="#EB3440"/>

  <!-- Top-left logo/title lockup -->
  <path d="M72 72 L91 53 L110 72 L91 91 Z M91 59 L104 72 L91 85 L78 72 Z" fill="#EB3440"/>
  <text x="126" y="79" width="260" font-family="Segoe UI, Microsoft YaHei, Arial, sans-serif" font-size="18" font-weight="700" fill="#FFFFFF" letter-spacing="1.2">
    APEX STRATEGY
  </text>

  <!-- Main headline zone with explicit widths -->
  <text x="86" y="180" width="480" font-family="Segoe UI, Microsoft YaHei, Arial, sans-serif" font-size="58" font-weight="800" fill="#FFFFFF">
    Theme-Ready
  </text>
  <text x="86" y="244" width="520" font-family="Segoe UI, Microsoft YaHei, Arial, sans-serif" font-size="58" font-weight="800" fill="#FFFFFF">
    Data Narrative
  </text>
  <text x="90" y="306" width="500" font-family="Segoe UI, Microsoft YaHei, Arial, sans-serif" font-size="20" fill="#FFFFFF" opacity="0.82">
    A geometric corporate layout that stays editable, aligned, and robust across brand color changes.
  </text>

  <!-- Central data panel -->
  <rect x="610" y="126" width="484" height="462" rx="28" fill="url(#panelGradient)" stroke="#FFFFFF" stroke-opacity="0.30" stroke-width="1.5" filter="url(#softShadow)"/>
  <text x="650" y="176" width="300" font-family="Segoe UI, Microsoft YaHei, Arial, sans-serif" font-size="19" font-weight="700" fill="#FFFFFF">
    Quarterly Performance
  </text>
  <text x="650" y="205" width="360" font-family="Segoe UI, Microsoft YaHei, Arial, sans-serif" font-size="13" fill="#FFFFFF" opacity="0.72">
    Replace metrics and bars while preserving the geometric frame.
  </text>

  <!-- KPI tiles -->
  <rect x="650" y="238" width="92" height="82" rx="16" fill="#FFFFFF" opacity="0.14" filter="url(#softShadow)"/>
  <rect x="762" y="238" width="92" height="82" rx="16" fill="#FFFFFF" opacity="0.14" filter="url(#softShadow)"/>
  <rect x="874" y="238" width="92" height="82" rx="16" fill="#FFFFFF" opacity="0.14" filter="url(#softShadow)"/>
  <rect x="986" y="238" width="68" height="82" rx="16" fill="#EB3440" opacity="0.95" filter="url(#softShadow)"/>

  <text x="668" y="269" width="60" font-family="Segoe UI, Microsoft YaHei, Arial, sans-serif" font-size="25" font-weight="800" fill="#FFFFFF">42%</text>
  <text x="668" y="296" width="58" font-family="Segoe UI, Microsoft YaHei, Arial, sans-serif" font-size="11" fill="#FFFFFF" opacity="0.70">Growth</text>
  <text x="780" y="269" width="60" font-family="Segoe UI, Microsoft YaHei, Arial, sans-serif" font-size="25" font-weight="800" fill="#FFFFFF">18</text>
  <text x="780" y="296" width="58" font-family="Segoe UI, Microsoft YaHei, Arial, sans-serif" font-size="11" fill="#FFFFFF" opacity="0.70">Markets</text>
  <text x="892" y="269" width="60" font-family="Segoe UI, Microsoft YaHei, Arial, sans-serif" font-size="25" font-weight="800" fill="#FFFFFF">9.6</text>
  <text x="892" y="296" width="58" font-family="Segoe UI, Microsoft YaHei, Arial, sans-serif" font-size="11" fill="#FFFFFF" opacity="0.70">NPS</text>
  <text x="1001" y="269" width="42" font-family="Segoe UI, Microsoft YaHei, Arial, sans-serif" font-size="24" font-weight="800" fill="#FFFFFF">A</text>
  <text x="996" y="296" width="48" font-family="Segoe UI, Microsoft YaHei, Arial, sans-serif" font-size="11" fill="#FFFFFF" opacity="0.82">Rating</text>

  <!-- Chart axes and bars -->
  <line x1="670" y1="508" x2="1038" y2="508" stroke="#FFFFFF" stroke-opacity="0.34" stroke-width="1.5"/>
  <line x1="670" y1="372" x2="670" y2="508" stroke="#FFFFFF" stroke-opacity="0.34" stroke-width="1.5"/>

  <rect x="710" y="444" width="34" height="64" rx="8" fill="#FFFFFF" opacity="0.72"/>
  <rect x="783" y="414" width="34" height="94" rx="8" fill="#FFFFFF" opacity="0.78"/>
  <rect x="856" y="386" width="34" height="122" rx="8" fill="#FFFFFF" opacity="0.86"/>
  <rect x="929" y="405" width="34" height="103" rx="8" fill="#FFFFFF" opacity="0.80"/>
  <rect x="1002" y="358" width="34" height="150" rx="8" fill="#EB3440"/>

  <circle cx="727" cy="432" r="6" fill="#EB3440"/>
  <circle cx="800" cy="402" r="6" fill="#EB3440"/>
  <circle cx="873" cy="374" r="6" fill="#EB3440"/>
  <circle cx="946" cy="393" r="6" fill="#EB3440"/>
  <circle cx="1019" cy="346" r="6" fill="#FFFFFF"/>

  <text x="704" y="536" width="54" font-family="Segoe UI, Microsoft YaHei, Arial, sans-serif" font-size="12" fill="#FFFFFF" opacity="0.70">Q1</text>
  <text x="777" y="536" width="54" font-family="Segoe UI, Microsoft YaHei, Arial, sans-serif" font-size="12" fill="#FFFFFF" opacity="0.70">Q2</text>
  <text x="850" y="536" width="54" font-family="Segoe UI, Microsoft YaHei, Arial, sans-serif" font-size="12" fill="#FFFFFF" opacity="0.70">Q3</text>
  <text x="923" y="536" width="54" font-family="Segoe UI, Microsoft YaHei, Arial, sans-serif" font-size="12" fill="#FFFFFF" opacity="0.70">Q4</text>
  <text x="994" y="536" width="62" font-family="Segoe UI, Microsoft YaHei, Arial, sans-serif" font-size="12" font-weight="700" fill="#FFFFFF">FY</text>

  <!-- Footer rule and robust editable footer text -->
  <rect x="86" y="624" width="72" height="6" rx="3" fill="#EB3440"/>
  <text x="176" y="633" width="560" font-family="Segoe UI, Microsoft YaHei, Arial, sans-serif" font-size="14" fill="#FFFFFF" opacity="0.72">
    Built with editable SVG geometry: no rasterized frame, no fragile masks, no layout-dependent autofit.
  </text>
</svg>
```

## Avoid in this skill
- ❌ Hardcoding text boxes without `width`; this style depends on predictable no-autofit text geometry in PowerPoint.
- ❌ Centering the rings or stripes in the content area; the premium look comes from pushing decoration to the canvas edges.
- ❌ Using masks or clipping on regular shapes to create half-circles; simply place circles partially outside the viewBox.
- ❌ Overusing tiny decorative elements; the style should feel like a robust corporate template, not an infographic collage.
- ❌ Applying filters to `<line>` elements for chart axes; keep axis lines simple and editable.

## Composition notes
- Keep the left 40–45% as the headline safe zone, with generous negative space and all text left-aligned.
- Anchor geometric accents to the canvas edges: rings should bleed off the left, stripes should touch the top/right, and the large accent circle should crop off the bottom-right.
- Use a strict color rhythm: one dominant background color, one accent color, and white text/data elements.
- For data slides, place charts in a single clean panel on the right or center-right so the decorative geometry frames the content rather than competing with it.