# SVG Recipe — Dark-Theme BI Dashboard Panel

## Visual mechanism
A dark executive “command center” built from layered navy panels, crisp metric typography, and electric accent charts. The structure uses a strict grid with one dominant trend panel, KPI cards, navigation slicers, and compact secondary visualizations to make many metrics feel organized rather than crowded.

## SVG primitives needed
- 1× `<rect>` for the full-slide dark background
- 12–18× `<rect>` for rounded dashboard panels, KPI cards, sidebar slicers, progress bars, and subtle separators
- 8–12× `<line>` for chart gridlines and axes
- 6–10× `<path>` for area fills, line charts, donut segments, gauge arcs, and tiny sparkline shapes
- 10–18× `<circle>` for chart markers, status dots, donut centers, and glowing KPI bullets
- 20–30× `<text>` with explicit `width` for dashboard title, KPI values, labels, axis ticks, slicer labels, and annotations
- 2× `<linearGradient>` for premium panel fills and cyan chart accents
- 1× `<radialGradient>` for the low-contrast background glow
- 1× `<filter id="panelShadow">` applied to rounded panels for depth
- 1× `<filter id="softGlow">` applied to highlighted chart paths and metric dots

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <radialGradient id="bgGlow" cx="72%" cy="18%" r="70%">
      <stop offset="0%" stop-color="#183769"/>
      <stop offset="45%" stop-color="#0A1429"/>
      <stop offset="100%" stop-color="#070D1B"/>
    </radialGradient>
    <linearGradient id="panelFill" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#182A50"/>
      <stop offset="100%" stop-color="#101D38"/>
    </linearGradient>
    <linearGradient id="cyanGrad" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#00BFFF"/>
      <stop offset="100%" stop-color="#30FFD6"/>
    </linearGradient>
    <filter id="panelShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feOffset dx="0" dy="10"/>
      <feGaussianBlur stdDeviation="12"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="softGlow" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="5"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGlow)"/>

  <!-- Sidebar -->
  <rect x="34" y="32" width="220" height="656" rx="24" fill="#101D38" stroke="#263B6B" stroke-width="1.2" filter="url(#panelShadow)"/>
  <text x="58" y="72" width="170" font-family="Segoe UI, Microsoft YaHei" font-size="24" font-weight="700" fill="#F2F6FF">BI Pulse</text>
  <text x="58" y="100" width="160" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#7F91B8" letter-spacing="1.5">EXECUTIVE SUMMARY</text>
  <line x1="58" y1="126" x2="230" y2="126" stroke="#2A3F70" stroke-width="1"/>

  <text x="58" y="166" width="120" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#7F91B8">REGION</text>
  <rect x="56" y="184" width="150" height="34" rx="17" fill="url(#cyanGrad)" opacity="0.95"/>
  <text x="78" y="207" width="90" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#061525">Global</text>
  <circle cx="220" cy="201" r="5" fill="#30FFD6" filter="url(#softGlow)"/>
  <rect x="56" y="232" width="150" height="34" rx="17" fill="#162846" stroke="#2A3F70"/>
  <text x="78" y="255" width="90" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#C7D3EA">Americas</text>
  <rect x="56" y="280" width="150" height="34" rx="17" fill="#162846" stroke="#2A3F70"/>
  <text x="78" y="303" width="90" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#C7D3EA">EMEA</text>
  <rect x="56" y="328" width="150" height="34" rx="17" fill="#162846" stroke="#2A3F70"/>
  <text x="78" y="351" width="90" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#C7D3EA">APAC</text>

  <text x="58" y="430" width="130" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#7F91B8">STATUS MIX</text>
  <circle cx="76" cy="462" r="6" fill="#2ECC71"/>
  <text x="92" y="467" width="110" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#DCE6F6">On track 68%</text>
  <circle cx="76" cy="494" r="6" fill="#F39C12"/>
  <text x="92" y="499" width="110" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#DCE6F6">Watch 21%</text>
  <circle cx="76" cy="526" r="6" fill="#FF5C7A"/>
  <text x="92" y="531" width="110" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#DCE6F6">Risk 11%</text>

  <rect x="56" y="596" width="150" height="52" rx="16" fill="#0C172D" stroke="#28406D"/>
  <text x="76" y="619" width="120" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#7F91B8">LAST REFRESH</text>
  <text x="76" y="642" width="120" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="700" fill="#F2F6FF">09:45 UTC</text>

  <!-- Header -->
  <text x="292" y="64" width="520" font-family="Segoe UI, Microsoft YaHei" font-size="30" font-weight="700" fill="#F5F8FF">Quarterly Performance Dashboard</text>
  <text x="292" y="91" width="610" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#8FA4CC">Revenue, pipeline, conversion, and operational health across all active markets</text>
  <rect x="1014" y="42" width="190" height="40" rx="20" fill="#12223F" stroke="#2A3F70"/>
  <text x="1040" y="67" width="130" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#C7D3EA">FY2026 · Q2</text>

  <!-- KPI cards -->
  <rect x="292" y="118" width="205" height="94" rx="20" fill="url(#panelFill)" stroke="#29416F" filter="url(#panelShadow)"/>
  <text x="314" y="146" width="140" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#8FA4CC">TOTAL REVENUE</text>
  <text x="314" y="184" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="800" fill="#F5F8FF">$24.8M</text>
  <text x="420" y="184" width="60" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#2ECC71">▲ 18%</text>

  <rect x="517" y="118" width="205" height="94" rx="20" fill="url(#panelFill)" stroke="#29416F" filter="url(#panelShadow)"/>
  <text x="539" y="146" width="140" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#8FA4CC">PIPELINE</text>
  <text x="539" y="184" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="800" fill="#F5F8FF">$61.2M</text>
  <text x="646" y="184" width="60" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#00BFFF">●</text>

  <rect x="742" y="118" width="205" height="94" rx="20" fill="url(#panelFill)" stroke="#29416F" filter="url(#panelShadow)"/>
  <text x="764" y="146" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#8FA4CC">CONVERSION</text>
  <text x="764" y="184" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="800" fill="#F5F8FF">37.4%</text>
  <text x="872" y="184" width="60" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#2ECC71">▲ 4.1</text>

  <rect x="967" y="118" width="237" height="94" rx="20" fill="url(#panelFill)" stroke="#29416F" filter="url(#panelShadow)"/>
  <text x="989" y="146" width="160" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#8FA4CC">CUSTOMER HEALTH</text>
  <text x="989" y="184" width="110" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="800" fill="#F5F8FF">82</text>
  <rect x="1074" y="162" width="96" height="10" rx="5" fill="#263B6B"/>
  <rect x="1074" y="162" width="78" height="10" rx="5" fill="url(#cyanGrad)"/>
  <text x="1074" y="195" width="110" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#8FA4CC">+7 pts vs target</text>

  <!-- Main trend panel -->
  <rect x="292" y="238" width="612" height="410" rx="24" fill="url(#panelFill)" stroke="#29416F" filter="url(#panelShadow)"/>
  <text x="322" y="276" width="270" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#F5F8FF">Revenue Trend</text>
  <text x="322" y="299" width="270" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#8FA4CC">Monthly booked revenue, USD millions</text>
  <line x1="342" y1="574" x2="856" y2="574" stroke="#36517D" stroke-width="1"/>
  <line x1="342" y1="514" x2="856" y2="514" stroke="#263B6B" stroke-width="1" stroke-dasharray="5 7"/>
  <line x1="342" y1="454" x2="856" y2="454" stroke="#263B6B" stroke-width="1" stroke-dasharray="5 7"/>
  <line x1="342" y1="394" x2="856" y2="394" stroke="#263B6B" stroke-width="1" stroke-dasharray="5 7"/>
  <line x1="342" y1="334" x2="856" y2="334" stroke="#263B6B" stroke-width="1" stroke-dasharray="5 7"/>
  <path d="M350 548 C405 520, 455 532, 510 486 C565 440, 622 460, 672 386 C724 310, 774 362, 848 318 L848 574 L350 574 Z" fill="#00BFFF" opacity="0.12"/>
  <path d="M350 548 C405 520, 455 532, 510 486 C565 440, 622 460, 672 386 C724 310, 774 362, 848 318" fill="none" stroke="url(#cyanGrad)" stroke-width="4" stroke-linecap="round" filter="url(#softGlow)"/>
  <circle cx="350" cy="548" r="6" fill="#00BFFF" stroke="#F5F8FF" stroke-width="2"/>
  <circle cx="510" cy="486" r="6" fill="#00BFFF" stroke="#F5F8FF" stroke-width="2"/>
  <circle cx="672" cy="386" r="7" fill="#30FFD6" stroke="#F5F8FF" stroke-width="2" filter="url(#softGlow)"/>
  <circle cx="848" cy="318" r="7" fill="#30FFD6" stroke="#F5F8FF" stroke-width="2"/>
  <text x="338" y="606" width="40" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#7F91B8">Jan</text>
  <text x="498" y="606" width="40" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#7F91B8">Mar</text>
  <text x="660" y="606" width="40" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#7F91B8">May</text>
  <text x="836" y="606" width="40" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#7F91B8">Jul</text>

  <!-- Right analytics panels -->
  <rect x="928" y="238" width="276" height="192" rx="24" fill="url(#panelFill)" stroke="#29416F" filter="url(#panelShadow)"/>
  <text x="954" y="276" width="190" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#F5F8FF">Deal Stage Mix</text>
  <path d="M1066 324 A54 54 0 1 1 1012 378 L1036 378 A30 30 0 1 0 1066 348 Z" fill="#00BFFF"/>
  <path d="M1012 378 A54 54 0 0 1 1088 428 L1076 404 A30 30 0 0 0 1036 378 Z" fill="#F39C12"/>
  <path d="M1088 428 A54 54 0 0 1 1066 324 L1066 348 A30 30 0 0 0 1076 404 Z" fill="#2ECC71"/>
  <circle cx="1066" cy="378" r="28" fill="#101D38"/>
  <text x="1046" y="383" width="45" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="800" fill="#F5F8FF">58%</text>
  <text x="954" y="410" width="90" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#8FA4CC">Qualified</text>
  <text x="1132" y="334" width="60" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#00BFFF">New</text>
  <text x="1132" y="360" width="60" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#2ECC71">Won</text>
  <text x="1132" y="386" width="60" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#F39C12">Review</text>

  <rect x="928" y="456" width="276" height="192" rx="24" fill="url(#panelFill)" stroke="#29416F" filter="url(#panelShadow)"/>
  <text x="954" y="494" width="180" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#F5F8FF">Forecast Confidence</text>
  <path d="M978 594 A88 88 0 0 1 1154 594" fill="none" stroke="#263B6B" stroke-width="20" stroke-linecap="round"/>
  <path d="M978 594 A88 88 0 0 1 1118 524" fill="none" stroke="url(#cyanGrad)" stroke-width="20" stroke-linecap="round" filter="url(#softGlow)"/>
  <circle cx="1066" cy="594" r="9" fill="#F5F8FF"/>
  <line x1="1066" y1="594" x2="1120" y2="536" stroke="#F5F8FF" stroke-width="4" stroke-linecap="round"/>
  <text x="1028" y="630" width="90" font-family="Segoe UI, Microsoft YaHei" font-size="28" font-weight="800" fill="#F5F8FF">74%</text>
</svg>
```

## Avoid in this skill
- ❌ Flat white chart backgrounds; they break the cohesive BI-console illusion.
- ❌ Overusing neon accents on every element; reserve cyan/green/orange for data meaning and highlight states.
- ❌ Applying `filter` to `<line>` chart gridlines; shadows/glows on lines are dropped, so apply glow to `<path>` trend lines instead.
- ❌ Using native SVG chart libraries, `<foreignObject>`, `<pattern>`, or `<textPath>`; build the charts directly from editable SVG primitives.
- ❌ Tiny labels without explicit `width`; every `<text>` must include `width` so PowerPoint does not reflow unpredictably.

## Composition notes
- Keep a left sidebar at roughly 15–20% of slide width; use it for slicers, status legends, or reporting metadata.
- Allocate the largest central panel to the primary narrative chart, usually a trend line or revenue bridge.
- Use small KPI cards across the top to establish the headline numbers before the viewer reads detailed charts.
- Maintain generous dark negative space between panels; the premium look depends on disciplined spacing and restrained accent color.