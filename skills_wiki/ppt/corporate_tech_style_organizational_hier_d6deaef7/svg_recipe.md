# SVG Recipe — Corporate Tech-Style Organizational Hierarchy (科技风企业组织架构图)

## Visual mechanism
A premium dark-mode organization chart uses glowing blue rounded nodes, crisp orthogonal connector rails, and a “standard + hanging” hierarchy: one executive node, horizontally distributed department heads, then vertically stacked sub-teams beneath each department. The tech feeling comes from a navy radial background, faint circuit traces, cyan highlights, and uniform node geometry.

## SVG primitives needed
- 1× `<rect>` for the full-slide dark gradient background
- 2× `<radialGradient>` / `<linearGradient>` definitions for tech lighting and node fills
- 1× `<filter id="softShadow">` for node depth
- 1× `<filter id="cyanGlow">` for subtle cyan emphasis on the top node and title accent
- 8× `<path>` for faint circuit-board background strokes and decorative angular corner accents
- 20× thin `<rect>` connector segments for orthogonal hierarchy rails
- 17× rounded `<rect>` for hierarchy nodes
- 17× small accent `<rect>` strips inside nodes
- 18× `<text>` elements with explicit `width` attributes for title and node labels
- 12× small `<circle>` elements for connector junction dots and tech background particles

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <radialGradient id="bgGlow" cx="50%" cy="28%" r="70%">
      <stop offset="0%" stop-color="#18345A"/>
      <stop offset="45%" stop-color="#0D1628"/>
      <stop offset="100%" stop-color="#080B13"/>
    </radialGradient>
    <linearGradient id="topNode" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#20D9FF"/>
      <stop offset="100%" stop-color="#0066CC"/>
    </linearGradient>
    <linearGradient id="midNode" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#187BDB"/>
      <stop offset="100%" stop-color="#0A4F9F"/>
    </linearGradient>
    <linearGradient id="subNode" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#2297F2"/>
      <stop offset="100%" stop-color="#1168B8"/>
    </linearGradient>
    <filter id="softShadow" x="-20%" y="-30%" width="140%" height="170%">
      <feOffset dx="0" dy="8"/>
      <feGaussianBlur stdDeviation="8"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="cyanGlow" x="-40%" y="-50%" width="180%" height="200%">
      <feGaussianBlur stdDeviation="5"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGlow)"/>
  <path d="M70 122 H210 V166 H310" fill="none" stroke="#1F6FAF" stroke-width="1.2" opacity="0.24"/>
  <path d="M1020 118 H1150 V218 H1210" fill="none" stroke="#20D9FF" stroke-width="1.1" opacity="0.18"/>
  <path d="M88 604 H190 V560 H294" fill="none" stroke="#20D9FF" stroke-width="1.1" opacity="0.17"/>
  <path d="M980 590 H1118 V548 H1192" fill="none" stroke="#1F6FAF" stroke-width="1.2" opacity="0.22"/>
  <path d="M42 42 H170" fill="none" stroke="#20D9FF" stroke-width="3" opacity="0.55" filter="url(#cyanGlow)"/>
  <path d="M42 42 V118" fill="none" stroke="#20D9FF" stroke-width="3" opacity="0.55" filter="url(#cyanGlow)"/>
  <path d="M1238 678 H1110" fill="none" stroke="#20D9FF" stroke-width="3" opacity="0.35"/>
  <path d="M1238 678 V604" fill="none" stroke="#20D9FF" stroke-width="3" opacity="0.35"/>

  <circle cx="310" cy="166" r="4" fill="#20D9FF" opacity="0.45"/>
  <circle cx="1150" cy="218" r="4" fill="#20D9FF" opacity="0.35"/>
  <circle cx="190" cy="560" r="4" fill="#20D9FF" opacity="0.35"/>
  <circle cx="1118" cy="548" r="4" fill="#20D9FF" opacity="0.28"/>

  <text x="640" y="62" width="620" text-anchor="middle" font-family="Microsoft YaHei, Segoe UI" font-size="34" font-weight="700" fill="#FFFFFF">公司组织架构图</text>
  <text x="640" y="91" width="620" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#8ECFFF" letter-spacing="2">CORPORATE TECHNOLOGY ORGANIZATION</text>

  <rect x="640" y="172" width="4" height="38" fill="#6FCBFF" opacity="0.85"/>
  <rect x="295" y="208" width="660" height="4" fill="#6FCBFF" opacity="0.72"/>
  <rect x="293" y="208" width="4" height="37" fill="#6FCBFF" opacity="0.72"/>
  <rect x="513" y="208" width="4" height="37" fill="#6FCBFF" opacity="0.72"/>
  <rect x="733" y="208" width="4" height="37" fill="#6FCBFF" opacity="0.72"/>
  <rect x="953" y="208" width="4" height="37" fill="#6FCBFF" opacity="0.72"/>

  <rect x="540" y="118" width="200" height="54" rx="14" fill="url(#topNode)" filter="url(#softShadow)" stroke="#7DEBFF" stroke-width="1.5"/>
  <rect x="554" y="129" width="5" height="32" rx="2.5" fill="#B9F7FF"/>
  <text x="640" y="146" width="180" text-anchor="middle" font-family="Microsoft YaHei, Segoe UI" font-size="18" font-weight="700" fill="#FFFFFF">董事会 / CEO</text>
  <text x="640" y="162" width="180" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="10" fill="#D9F8FF">Executive Office</text>

  <rect x="210" y="245" width="170" height="48" rx="12" fill="url(#midNode)" filter="url(#softShadow)"/>
  <rect x="430" y="245" width="170" height="48" rx="12" fill="url(#midNode)" filter="url(#softShadow)"/>
  <rect x="650" y="245" width="170" height="48" rx="12" fill="url(#midNode)" filter="url(#softShadow)"/>
  <rect x="870" y="245" width="170" height="48" rx="12" fill="url(#midNode)" filter="url(#softShadow)"/>
  <rect x="224" y="256" width="5" height="26" rx="2.5" fill="#7DEBFF"/><text x="295" y="275" width="150" text-anchor="middle" font-family="Microsoft YaHei, Segoe UI" font-size="15" font-weight="700" fill="#FFFFFF">产品研发中心</text>
  <rect x="444" y="256" width="5" height="26" rx="2.5" fill="#7DEBFF"/><text x="515" y="275" width="150" text-anchor="middle" font-family="Microsoft YaHei, Segoe UI" font-size="15" font-weight="700" fill="#FFFFFF">市场增长中心</text>
  <rect x="664" y="256" width="5" height="26" rx="2.5" fill="#7DEBFF"/><text x="735" y="275" width="150" text-anchor="middle" font-family="Microsoft YaHei, Segoe UI" font-size="15" font-weight="700" fill="#FFFFFF">运营交付中心</text>
  <rect x="884" y="256" width="5" height="26" rx="2.5" fill="#7DEBFF"/><text x="955" y="275" width="150" text-anchor="middle" font-family="Microsoft YaHei, Segoe UI" font-size="15" font-weight="700" fill="#FFFFFF">职能支持中心</text>

  <rect x="293" y="293" width="4" height="206" fill="#4AADEB" opacity="0.68"/>
  <rect x="513" y="293" width="4" height="206" fill="#4AADEB" opacity="0.68"/>
  <rect x="733" y="293" width="4" height="206" fill="#4AADEB" opacity="0.68"/>
  <rect x="953" y="293" width="4" height="206" fill="#4AADEB" opacity="0.68"/>

  <rect x="215" y="330" width="160" height="40" rx="10" fill="url(#subNode)"/><rect x="226" y="340" width="4" height="20" rx="2" fill="#B9F7FF"/><text x="295" y="355" width="140" text-anchor="middle" font-family="Microsoft YaHei, Segoe UI" font-size="13" fill="#FFFFFF">平台架构部</text>
  <rect x="215" y="395" width="160" height="40" rx="10" fill="url(#subNode)"/><rect x="226" y="405" width="4" height="20" rx="2" fill="#B9F7FF"/><text x="295" y="420" width="140" text-anchor="middle" font-family="Microsoft YaHei, Segoe UI" font-size="13" fill="#FFFFFF">应用开发部</text>
  <rect x="215" y="460" width="160" height="40" rx="10" fill="url(#subNode)"/><rect x="226" y="470" width="4" height="20" rx="2" fill="#B9F7FF"/><text x="295" y="485" width="140" text-anchor="middle" font-family="Microsoft YaHei, Segoe UI" font-size="13" fill="#FFFFFF">测试质量部</text>

  <rect x="435" y="330" width="160" height="40" rx="10" fill="url(#subNode)"/><rect x="446" y="340" width="4" height="20" rx="2" fill="#B9F7FF"/><text x="515" y="355" width="140" text-anchor="middle" font-family="Microsoft YaHei, Segoe UI" font-size="13" fill="#FFFFFF">品牌传播部</text>
  <rect x="435" y="395" width="160" height="40" rx="10" fill="url(#subNode)"/><rect x="446" y="405" width="4" height="20" rx="2" fill="#B9F7FF"/><text x="515" y="420" width="140" text-anchor="middle" font-family="Microsoft YaHei, Segoe UI" font-size="13" fill="#FFFFFF">渠道拓展部</text>
  <rect x="435" y="460" width="160" height="40" rx="10" fill="url(#subNode)"/><rect x="446" y="470" width="4" height="20" rx="2" fill="#B9F7FF"/><text x="515" y="485" width="140" text-anchor="middle" font-family="Microsoft YaHei, Segoe UI" font-size="13" fill="#FFFFFF">客户成功部</text>

  <rect x="655" y="330" width="160" height="40" rx="10" fill="url(#subNode)"/><rect x="666" y="340" width="4" height="20" rx="2" fill="#B9F7FF"/><text x="735" y="355" width="140" text-anchor="middle" font-family="Microsoft YaHei, Segoe UI" font-size="13" fill="#FFFFFF">项目管理部</text>
  <rect x="655" y="395" width="160" height="40" rx="10" fill="url(#subNode)"/><rect x="666" y="405" width="4" height="20" rx="2" fill="#B9F7FF"/><text x="735" y="420" width="140" text-anchor="middle" font-family="Microsoft YaHei, Segoe UI" font-size="13" fill="#FFFFFF">交付实施部</text>
  <rect x="655" y="460" width="160" height="40" rx="10" fill="url(#subNode)"/><rect x="666" y="470" width="4" height="20" rx="2" fill="#B9F7FF"/><text x="735" y="485" width="140" text-anchor="middle" font-family="Microsoft YaHei, Segoe UI" font-size="13" fill="#FFFFFF">数据运营部</text>

  <rect x="875" y="330" width="160" height="40" rx="10" fill="url(#subNode)"/><rect x="886" y="340" width="4" height="20" rx="2" fill="#B9F7FF"/><text x="955" y="355" width="140" text-anchor="middle" font-family="Microsoft YaHei, Segoe UI" font-size="13" fill="#FFFFFF">人力资源部</text>
  <rect x="875" y="395" width="160" height="40" rx="10" fill="url(#subNode)"/><rect x="886" y="405" width="4" height="20" rx="2" fill="#B9F7FF"/><text x="955" y="420" width="140" text-anchor="middle" font-family="Microsoft YaHei, Segoe UI" font-size="13" fill="#FFFFFF">财务法务部</text>
  <rect x="875" y="460" width="160" height="40" rx="10" fill="url(#subNode)"/><rect x="886" y="470" width="4" height="20" rx="2" fill="#B9F7FF"/><text x="955" y="485" width="140" text-anchor="middle" font-family="Microsoft YaHei, Segoe UI" font-size="13" fill="#FFFFFF">行政采购部</text>

  <circle cx="295" cy="210" r="4" fill="#B9F7FF"/><circle cx="515" cy="210" r="4" fill="#B9F7FF"/><circle cx="735" cy="210" r="4" fill="#B9F7FF"/><circle cx="955" cy="210" r="4" fill="#B9F7FF"/>
  <text x="640" y="650" width="860" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#7EA6C8">Standard top distribution + hanging sub-departments · editable rounded rectangles and connector rails</text>
</svg>
```

## Avoid in this skill
- ❌ PowerPoint SmartArt-style auto-layout assumptions; draw every node and connector explicitly for predictable PPT editing.
- ❌ Diagonal connectors or freeform spaghetti lines; the hierarchy should use orthogonal rails only.
- ❌ Applying `filter` to `<line>` elements; use thin `<rect>` connector bars if shadows or precise rendering are needed.
- ❌ Using `<use>`, `<symbol>`, `<mask>`, `<foreignObject>`, or `marker-end`; these can break or disappear in translation.
- ❌ Text without explicit `width`; every label must set `width` to prevent PowerPoint overflow surprises.

## Composition notes
- Keep the hierarchy centered in the middle 70% of the slide; reserve the top 90px for the title and the bottom 60px for a caption or legend.
- Use one bright cyan executive node, medium blue department nodes, and slightly lighter subordinate nodes to create clear level separation.
- The connector system should be visually quieter than the nodes: thin cyan rails at 60–75% opacity are enough.
- Leave generous negative space around the chart; tech background circuits should frame the layout, not compete with the organization labels.