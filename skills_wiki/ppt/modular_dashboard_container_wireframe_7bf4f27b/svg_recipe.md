# SVG Recipe — Modular Dashboard Container Wireframe

## Visual mechanism
A flat, app-like dashboard shell is built from overlapping borderless rounded rectangles: a high-contrast vertical sidebar, a pale main workspace, and a modular grid of white content cards. Subtle shadows, consistent gutters, and lightweight placeholder charts make the slide feel like a premium BI interface before real data is added.

## SVG primitives needed
- 1× `<rect>` for the full soft-gray slide background
- 2× large `<rect>` for the main workspace panel and accent sidebar
- 11× white rounded `<rect>` for KPI, chart, and lower analysis containers
- 1× `<linearGradient>` for the sidebar accent depth
- 1× `<filter id="cardShadow">` applied to dashboard card rectangles
- 6× small `<circle>` elements for KPI icon badges
- Multiple `<path>` elements for editable icon glyphs, sparklines, mini chart curves, and decorative UI placeholders
- Multiple `<line>` elements for sidebar navigation ticks and chart axes/grid lines
- Multiple `<text>` elements with explicit `width` attributes for headings, KPI labels, and placeholder values

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="sidebarGrad" x1="0" y1="40" x2="150" y2="680" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#008B47"/>
      <stop offset="1" stop-color="#006B36"/>
    </linearGradient>
    <linearGradient id="panelGrad" x1="140" y1="40" x2="1240" y2="690" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#F0F0F0"/>
      <stop offset="1" stop-color="#E7E7E7"/>
    </linearGradient>
    <filter id="cardShadow" x="-10%" y="-10%" width="120%" height="125%">
      <feOffset dx="0" dy="8" result="off"/>
      <feGaussianBlur in="off" stdDeviation="10" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#E6E6E6"/>

  <rect x="96" y="30" width="1154" height="660" rx="26" fill="url(#panelGrad)"/>
  <rect x="30" y="30" width="128" height="660" rx="28" fill="url(#sidebarGrad)"/>

  <circle cx="94" cy="86" r="26" fill="#FFFFFF" opacity="0.18"/>
  <path d="M82 88 L92 76 L106 88 L106 104 L82 104 Z" fill="#FFFFFF"/>
  <text x="58" y="154" width="72" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#FFFFFF" opacity="0.9" text-anchor="middle">DASH</text>
  <line x1="60" y1="218" x2="128" y2="218" stroke="#FFFFFF" stroke-width="5" stroke-linecap="round" opacity="0.95"/>
  <line x1="60" y1="280" x2="118" y2="280" stroke="#FFFFFF" stroke-width="5" stroke-linecap="round" opacity="0.45"/>
  <line x1="60" y1="342" x2="118" y2="342" stroke="#FFFFFF" stroke-width="5" stroke-linecap="round" opacity="0.45"/>
  <line x1="60" y1="404" x2="118" y2="404" stroke="#FFFFFF" stroke-width="5" stroke-linecap="round" opacity="0.45"/>
  <circle cx="94" cy="632" r="22" fill="#FFFFFF" opacity="0.16"/>

  <text x="190" y="78" width="420" font-family="Segoe UI, Microsoft YaHei" font-size="28" font-weight="700" fill="#1E2A24">Executive Dashboard Wireframe</text>
  <text x="190" y="106" width="520" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#6E7A74">Modular KPI, chart, and analysis containers with consistent 28px gutters</text>

  <rect x="190" y="132" width="150" height="96" rx="18" fill="#FFFFFF" filter="url(#cardShadow)"/>
  <circle cx="222" cy="164" r="17" fill="#00803B" opacity="0.14"/>
  <path d="M213 168 L220 160 L226 165 L234 154" fill="none" stroke="#00803B" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
  <text x="250" y="162" width="72" font-family="Segoe UI, Microsoft YaHei" font-size="22" font-weight="700" fill="#1E2A24">84%</text>
  <text x="208" y="202" width="112" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#7C8580">Growth Rate</text>

  <rect x="368" y="132" width="150" height="96" rx="18" fill="#FFFFFF" filter="url(#cardShadow)"/>
  <circle cx="400" cy="164" r="17" fill="#00803B" opacity="0.14"/>
  <path d="M400 152 L400 176 M391 160 C391 154 409 154 409 160 C409 166 391 163 391 170 C391 177 410 177 410 170" fill="none" stroke="#00803B" stroke-width="3.5" stroke-linecap="round"/>
  <text x="428" y="162" width="72" font-family="Segoe UI, Microsoft YaHei" font-size="22" font-weight="700" fill="#1E2A24">$42K</text>
  <text x="386" y="202" width="112" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#7C8580">Revenue</text>

  <rect x="546" y="132" width="150" height="96" rx="18" fill="#FFFFFF" filter="url(#cardShadow)"/>
  <circle cx="578" cy="164" r="17" fill="#00803B" opacity="0.14"/>
  <path d="M569 164 C569 156 578 151 586 156 M587 156 L587 149 M587 156 L580 156 M587 166 C587 174 578 179 570 174 M569 174 L569 181 M569 174 L576 174" fill="none" stroke="#00803B" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"/>
  <text x="606" y="162" width="72" font-family="Segoe UI, Microsoft YaHei" font-size="22" font-weight="700" fill="#1E2A24">12K</text>
  <text x="564" y="202" width="112" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#7C8580">Refreshes</text>

  <rect x="724" y="132" width="150" height="96" rx="18" fill="#FFFFFF" filter="url(#cardShadow)"/>
  <circle cx="756" cy="164" r="17" fill="#00803B" opacity="0.14"/>
  <path d="M746 155 L766 175 M766 175 L766 165 M766 175 L756 175" fill="none" stroke="#00803B" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
  <text x="784" y="162" width="72" font-family="Segoe UI, Microsoft YaHei" font-size="22" font-weight="700" fill="#1E2A24">-6%</text>
  <text x="742" y="202" width="112" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#7C8580">Risk Delta</text>

  <rect x="902" y="132" width="150" height="96" rx="18" fill="#FFFFFF" filter="url(#cardShadow)"/>
  <circle cx="934" cy="164" r="17" fill="#00803B" opacity="0.14"/>
  <path d="M923 156 C923 151 945 151 945 156 L945 172 C945 177 923 177 923 172 Z M923 156 C923 161 945 161 945 156" fill="none" stroke="#00803B" stroke-width="3.2"/>
  <text x="962" y="162" width="72" font-family="Segoe UI, Microsoft YaHei" font-size="22" font-weight="700" fill="#1E2A24">9.7M</text>
  <text x="920" y="202" width="112" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#7C8580">Records</text>

  <rect x="1080" y="132" width="150" height="96" rx="18" fill="#FFFFFF" filter="url(#cardShadow)"/>
  <circle cx="1112" cy="164" r="17" fill="#00803B" opacity="0.14"/>
  <path d="M1103 174 C1104 166 1120 166 1121 174 M1112 160 A6 6 0 1 0 1112 159 M1120 163 C1125 158 1132 161 1132 168" fill="none" stroke="#00803B" stroke-width="3.3" stroke-linecap="round"/>
  <text x="1140" y="162" width="72" font-family="Segoe UI, Microsoft YaHei" font-size="22" font-weight="700" fill="#1E2A24">318</text>
  <text x="1098" y="202" width="112" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#7C8580">Accounts</text>

  <rect x="190" y="258" width="506" height="220" rx="20" fill="#FFFFFF" filter="url(#cardShadow)"/>
  <text x="220" y="296" width="260" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="700" fill="#26332D">Primary Trend Module</text>
  <line x1="232" y1="430" x2="655" y2="430" stroke="#DCE2DF" stroke-width="2"/>
  <line x1="232" y1="382" x2="655" y2="382" stroke="#EEF1EF" stroke-width="2"/>
  <line x1="232" y1="334" x2="655" y2="334" stroke="#EEF1EF" stroke-width="2"/>
  <path d="M236 412 C282 386 300 392 340 356 C390 312 430 358 468 334 C512 307 552 320 592 286 C620 264 640 276 656 258" fill="none" stroke="#00803B" stroke-width="5" stroke-linecap="round"/>
  <path d="M236 430 C286 408 324 418 366 392 C410 365 450 396 492 374 C542 348 594 354 656 318 L656 430 Z" fill="#00803B" opacity="0.08"/>

  <rect x="724" y="258" width="506" height="220" rx="20" fill="#FFFFFF" filter="url(#cardShadow)"/>
  <text x="754" y="296" width="260" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="700" fill="#26332D">Segment Comparison</text>
  <rect x="770" y="386" width="54" height="54" rx="8" fill="#00803B" opacity="0.20"/>
  <rect x="846" y="340" width="54" height="100" rx="8" fill="#00803B" opacity="0.38"/>
  <rect x="922" y="304" width="54" height="136" rx="8" fill="#00803B" opacity="0.70"/>
  <rect x="998" y="360" width="54" height="80" rx="8" fill="#00803B" opacity="0.30"/>
  <rect x="1074" y="322" width="54" height="118" rx="8" fill="#00803B" opacity="0.55"/>
  <line x1="760" y1="440" x2="1162" y2="440" stroke="#DCE2DF" stroke-width="2"/>
  <text x="1084" y="292" width="116" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#7C8580">Editable bars</text>

  <rect x="190" y="508" width="328" height="142" rx="20" fill="#FFFFFF" filter="url(#cardShadow)"/>
  <text x="220" y="548" width="180" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="700" fill="#26332D">Breakdown A</text>
  <circle cx="276" cy="602" r="36" fill="none" stroke="#E2E8E5" stroke-width="12"/>
  <path d="M276 566 A36 36 0 1 1 244 617" fill="none" stroke="#00803B" stroke-width="12" stroke-linecap="round"/>
  <text x="336" y="608" width="110" font-family="Segoe UI, Microsoft YaHei" font-size="24" font-weight="700" fill="#1E2A24">72%</text>

  <rect x="546" y="508" width="328" height="142" rx="20" fill="#FFFFFF" filter="url(#cardShadow)"/>
  <text x="576" y="548" width="180" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="700" fill="#26332D">Breakdown B</text>
  <path d="M590 620 L622 596 L654 608 L686 574 L718 586 L750 558 L814 592" fill="none" stroke="#00803B" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>
  <line x1="590" y1="632" x2="820" y2="632" stroke="#DCE2DF" stroke-width="2"/>

  <rect x="902" y="508" width="328" height="142" rx="20" fill="#FFFFFF" filter="url(#cardShadow)"/>
  <text x="932" y="548" width="180" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="700" fill="#26332D">Breakdown C</text>
  <rect x="934" y="584" width="236" height="12" rx="6" fill="#E8EEEB"/>
  <rect x="934" y="584" width="172" height="12" rx="6" fill="#00803B"/>
  <rect x="934" y="616" width="236" height="12" rx="6" fill="#E8EEEB"/>
  <rect x="934" y="616" width="126" height="12" rx="6" fill="#00803B" opacity="0.65"/>
</svg>
```

## Avoid in this skill
- ❌ Heavy outlines around every card; the technique depends on color blocking, radius, and spacing rather than visible borders.
- ❌ Applying filters to `<line>` chart gridlines or axes; shadows should be reserved for card `<rect>` shapes.
- ❌ Using `<use>` to duplicate KPI cards or icons; repeat the editable SVG primitives directly.
- ❌ Overfilling the wireframe with real chart detail; leave generous blank zones so PowerPoint charts, screenshots, or data labels can be placed later.
- ❌ Large corner radii that make the layout feel playful rather than enterprise-dashboard-like.

## Composition notes
- Keep the sidebar at roughly 10–12% of slide width and let it slightly overlap the main gray workspace for a cohesive app-shell feel.
- Use a strict gutter system: KPI cards, large chart cards, and lower modules should align to the same left/right edges.
- Put KPI cards across the top, primary analysis modules in the middle, and secondary modules at the bottom to create a natural executive scanning path.
- Use white cards on pale gray panels, then repeat the sidebar accent color only in icons, chart placeholders, and progress indicators.