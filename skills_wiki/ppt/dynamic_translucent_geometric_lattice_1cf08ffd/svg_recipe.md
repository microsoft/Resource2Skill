# SVG Recipe — Dynamic Translucent Geometric Lattice

## Visual mechanism
Large, oversized rectangular bars rotate at exactly 45° and -45°, bleeding beyond the slide edges and overlapping with semi-transparent warm fills. The intersections automatically create richer tones, forming a faceted geometric lattice that adds motion and depth while leaving clean negative space for sparse executive content.

## SVG primitives needed
- 1× `<rect>` for the full-slide light background
- 14× oversized `<rect>` for translucent diagonal lattice bars, rotated 45° and -45°
- 4× thin `<rect>` for sharper accent slashes embedded in the lattice
- 1× translucent rounded `<rect>` for a foreground content panel
- 3× small rounded `<rect>` for metric chips / data callouts
- 1× `<line>` for the title accent rule
- 7× `<text>` elements with explicit `width` attributes for kicker, title, subtitle, and metrics
- 3× `<linearGradient>` definitions for the background and warm translucent bar fills
- 1× `<filter id="softShadow">` applied to the content panel
- 1× `<filter id="warmGlow">` applied to selected accent bars

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgWash" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#ffffff"/>
      <stop offset="58%" stop-color="#fbf7f3"/>
      <stop offset="100%" stop-color="#f5eee8"/>
    </linearGradient>

    <linearGradient id="peachBar" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#ffe2c8"/>
      <stop offset="100%" stop-color="#f7b37a"/>
    </linearGradient>

    <linearGradient id="terracottaBar" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#f49a53"/>
      <stop offset="55%" stop-color="#e9733f"/>
      <stop offset="100%" stop-color="#c84f35"/>
    </linearGradient>

    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feOffset dx="0" dy="10" in="SourceAlpha" result="off"/>
      <feGaussianBlur in="off" stdDeviation="16" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="warmGlow" x="-25%" y="-25%" width="150%" height="150%">
      <feGaussianBlur stdDeviation="8"/>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgWash)"/>

  <!-- Pale structural lattice, bleeding far beyond canvas -->
  <rect x="720" y="-260" width="980" height="155" rx="8" fill="url(#peachBar)" opacity="0.32" transform="rotate(45 1210 -120)"/>
  <rect x="660" y="-90" width="1030" height="112" rx="8" fill="#f6c19a" opacity="0.30" transform="rotate(45 1175 10)"/>
  <rect x="740" y="90" width="920" height="76" rx="6" fill="#eda46f" opacity="0.28" transform="rotate(45 1200 128)"/>
  <rect x="870" y="260" width="850" height="96" rx="6" fill="#f7d0b0" opacity="0.36" transform="rotate(45 1295 308)"/>
  <rect x="780" y="440" width="980" height="128" rx="8" fill="#f1a263" opacity="0.25" transform="rotate(45 1270 504)"/>

  <!-- Perpendicular bars create the lattice intersections -->
  <rect x="610" y="80" width="1030" height="132" rx="8" fill="#f8caa8" opacity="0.38" transform="rotate(-45 1125 146)"/>
  <rect x="710" y="235" width="910" height="82" rx="6" fill="#ed8c50" opacity="0.31" transform="rotate(-45 1165 276)"/>
  <rect x="820" y="392" width="860" height="110" rx="8" fill="url(#terracottaBar)" opacity="0.22" transform="rotate(-45 1250 447)"/>
  <rect x="930" y="535" width="730" height="72" rx="6" fill="#cf6040" opacity="0.25" transform="rotate(-45 1295 571)"/>

  <!-- Stronger foreground slashes for dynamic hierarchy -->
  <rect x="915" y="-40" width="820" height="46" rx="4" fill="url(#terracottaBar)" opacity="0.54" transform="rotate(45 1325 -17)" filter="url(#warmGlow)"/>
  <rect x="1025" y="116" width="710" height="34" rx="3" fill="#dd6b3c" opacity="0.62" transform="rotate(45 1380 133)"/>
  <rect x="1010" y="350" width="650" height="38" rx="3" fill="#f18943" opacity="0.48" transform="rotate(-45 1335 369)" filter="url(#warmGlow)"/>
  <rect x="890" y="620" width="710" height="30" rx="3" fill="#bf4937" opacity="0.42" transform="rotate(-45 1245 635)"/>

  <!-- Bottom-right echo lattice -->
  <rect x="470" y="620" width="520" height="54" rx="5" fill="#ffd3b5" opacity="0.45" transform="rotate(45 730 647)"/>
  <rect x="610" y="675" width="600" height="42" rx="5" fill="#e96f3d" opacity="0.30" transform="rotate(-45 910 696)"/>

  <!-- Content block in the negative-space zone -->
  <rect x="82" y="92" width="500" height="430" rx="28" fill="#ffffff" opacity="0.74" filter="url(#softShadow)"/>
  <text x="112" y="146" width="360" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="16" font-weight="700" letter-spacing="3" fill="#d96738">MARKET MOMENTUM</text>
  <line x1="112" y1="170" x2="232" y2="170" stroke="#e97b42" stroke-width="5" stroke-linecap="round"/>

  <text x="112" y="236" width="430" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="56" font-weight="800" fill="#30333a">
    Translucent
    <tspan x="112" dy="64" fill="#30333a">Growth Lattice</tspan>
  </text>

  <text x="114" y="370" width="410" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="22" font-weight="300" fill="#62666f">
    A premium vector backdrop for sparse chart summaries, section dividers, and data story openers.
  </text>

  <!-- Small data chips to connect the visual language to chart/data slides -->
  <rect x="112" y="435" width="120" height="54" rx="16" fill="#fff3eb" stroke="#f1b183" stroke-width="1"/>
  <text x="132" y="468" width="80" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="22" font-weight="800" fill="#d96435">+18%</text>

  <rect x="252" y="435" width="120" height="54" rx="16" fill="#fff3eb" stroke="#f1b183" stroke-width="1"/>
  <text x="272" y="468" width="82" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="22" font-weight="800" fill="#d96435">Q4</text>

  <rect x="392" y="435" width="120" height="54" rx="16" fill="#fff3eb" stroke="#f1b183" stroke-width="1"/>
  <text x="412" y="468" width="78" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="22" font-weight="800" fill="#d96435">3.2×</text>

  <text x="114" y="560" width="420" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" fill="#8a8f98">
    Keep data concise; let the angled translucent system carry the energy of the page.
  </text>
</svg>
```

## Avoid in this skill
- ❌ Do not build the lattice from thin stroked lines only; the effect depends on broad translucent rectangular planes creating visible overlap zones.
- ❌ Do not place dense charts or paragraph text over the lattice-heavy side; transparency still creates visual activity and can reduce legibility.
- ❌ Do not use `skewX`, `skewY`, or matrix transforms to fake perspective; use simple `rotate(45 cx cy)` and `rotate(-45 cx cy)` transforms.
- ❌ Do not rely on masks or clipping for the bars; let oversized rotated rectangles bleed naturally off-canvas.

## Composition notes
- Keep the strongest lattice weight on the right edge and corners; reserve the left third to half of the slide for title, labels, or a compact data summary.
- Use 3–5 opacity levels, typically from `0.20` to `0.65`, so intersections create depth without turning muddy.
- Oversize every diagonal bar well beyond the 1280×720 canvas to avoid visible endpoints and preserve the premium “infinite system” feel.
- Pair warm translucent oranges with dark slate typography; repeat the accent color in small rules or metric chips for cohesion.