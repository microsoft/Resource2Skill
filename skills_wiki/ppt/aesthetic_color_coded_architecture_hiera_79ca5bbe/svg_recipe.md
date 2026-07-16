# SVG Recipe — Aesthetic Color-Coded Architecture Hierarchy

## Visual mechanism
A top-down hierarchy tree becomes easier to read by assigning each major branch a semantic hue, then using lighter tints for its child nodes. Rounded card-like nodes, soft shadows, and pale minimalist connectors make dense architecture feel organized, modern, and executive-ready.

## SVG primitives needed
- 1× `<rect>` for the full-slide soft gradient background
- 2× decorative `<path>` blobs for subtle premium depth behind the chart
- 1× `<rect>` for a translucent title accent bar
- 17× rounded `<rect>` nodes: one root, four branch heads, twelve leaf nodes
- 1× `<filter id="softShadow">` applied to hierarchy nodes for card elevation
- 1× `<filter id="blobBlur">` applied to background blobs for atmospheric color
- 5× `<linearGradient>` definitions: background plus branch-specific node fills
- 32× `<line>` connector segments for clean hierarchy relationships
- 18× `<text>` labels with explicit `width` attributes for PowerPoint-safe text layout
- Multiple nested `<tspan>` elements for subtitle emphasis and node micro-label styling

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1280" y2="720">
      <stop offset="0%" stop-color="#F8FAFC"/>
      <stop offset="55%" stop-color="#EEF3F7"/>
      <stop offset="100%" stop-color="#F6F1EA"/>
    </linearGradient>

    <linearGradient id="tealGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#2A7E8D"/>
      <stop offset="100%" stop-color="#1F5E6B"/>
    </linearGradient>
    <linearGradient id="coralGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#D5655F"/>
      <stop offset="100%" stop-color="#B84B47"/>
    </linearGradient>
    <linearGradient id="sageGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#7EA487"/>
      <stop offset="100%" stop-color="#5E8067"/>
    </linearGradient>
    <linearGradient id="goldGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#D5A15A"/>
      <stop offset="100%" stop-color="#B77F38"/>
    </linearGradient>
    <linearGradient id="rootGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#2F3E55"/>
      <stop offset="100%" stop-color="#172335"/>
    </linearGradient>

    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="8"/>
      <feGaussianBlur stdDeviation="8"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="blobBlur" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="28"/>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>

  <path d="M70,140 C150,40 305,55 360,150 C420,250 300,310 190,290 C80,270 20,220 70,140 Z"
        fill="#D9EEF2" opacity="0.55" filter="url(#blobBlur)"/>
  <path d="M1040,520 C1150,440 1250,500 1265,610 C1280,705 1120,735 1010,690 C925,655 945,590 1040,520 Z"
        fill="#F3D8C1" opacity="0.45" filter="url(#blobBlur)"/>

  <text x="70" y="58" width="720" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="30" font-weight="700" fill="#253041">
    Corporate Organizational Architecture
  </text>
  <text x="70" y="90" width="760" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" fill="#6B7480">
    <tspan>Semantic color branches clarify ownership, while lighter child cards show operational detail.</tspan>
  </text>
  <rect x="1015" y="42" width="190" height="38" rx="19" fill="#FFFFFF" opacity="0.86"/>
  <text x="1110" y="66" width="170" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" font-weight="700" fill="#697386">
    Q4 OPERATING MODEL
  </text>

  <!-- hierarchy connectors -->
  <line x1="640" y1="166" x2="640" y2="228" stroke="#C8D0D8" stroke-width="2"/>
  <line x1="210" y1="228" x2="1070" y2="228" stroke="#C8D0D8" stroke-width="2"/>
  <line x1="210" y1="228" x2="210" y2="270" stroke="#C8D0D8" stroke-width="2"/>
  <line x1="470" y1="228" x2="470" y2="270" stroke="#C8D0D8" stroke-width="2"/>
  <line x1="730" y1="228" x2="730" y2="270" stroke="#C8D0D8" stroke-width="2"/>
  <line x1="990" y1="228" x2="990" y2="270" stroke="#C8D0D8" stroke-width="2"/>

  <line x1="210" y1="336" x2="210" y2="405" stroke="#D2D8DE" stroke-width="2"/>
  <line x1="210" y1="461" x2="210" y2="486" stroke="#D2D8DE" stroke-width="2"/>
  <line x1="210" y1="542" x2="210" y2="567" stroke="#D2D8DE" stroke-width="2"/>
  <line x1="470" y1="336" x2="470" y2="405" stroke="#D2D8DE" stroke-width="2"/>
  <line x1="470" y1="461" x2="470" y2="486" stroke="#D2D8DE" stroke-width="2"/>
  <line x1="470" y1="542" x2="470" y2="567" stroke="#D2D8DE" stroke-width="2"/>
  <line x1="730" y1="336" x2="730" y2="405" stroke="#D2D8DE" stroke-width="2"/>
  <line x1="730" y1="461" x2="730" y2="486" stroke="#D2D8DE" stroke-width="2"/>
  <line x1="730" y1="542" x2="730" y2="567" stroke="#D2D8DE" stroke-width="2"/>
  <line x1="990" y1="336" x2="990" y2="405" stroke="#D2D8DE" stroke-width="2"/>
  <line x1="990" y1="461" x2="990" y2="486" stroke="#D2D8DE" stroke-width="2"/>
  <line x1="990" y1="542" x2="990" y2="567" stroke="#D2D8DE" stroke-width="2"/>

  <!-- root node -->
  <rect x="510" y="105" width="260" height="62" rx="23" fill="url(#rootGrad)" filter="url(#softShadow)"/>
  <text x="640" y="133" width="230" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="16" font-weight="700" fill="#FFFFFF">
    Board of Directors
    <tspan x="640" dy="19" font-size="11" font-weight="400" fill="#CFD7E2">enterprise governance</tspan>
  </text>

  <!-- branch heads -->
  <rect x="120" y="270" width="180" height="66" rx="20" fill="url(#tealGrad)" filter="url(#softShadow)"/>
  <rect x="380" y="270" width="180" height="66" rx="20" fill="url(#coralGrad)" filter="url(#softShadow)"/>
  <rect x="640" y="270" width="180" height="66" rx="20" fill="url(#sageGrad)" filter="url(#softShadow)"/>
  <rect x="900" y="270" width="180" height="66" rx="20" fill="url(#goldGrad)" filter="url(#softShadow)"/>

  <text x="210" y="298" width="160" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" font-weight="700" fill="#FFFFFF">Marketing Dept<tspan x="210" dy="18" font-size="11" font-weight="400">growth engine</tspan></text>
  <text x="470" y="298" width="160" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" font-weight="700" fill="#FFFFFF">Operations Dept<tspan x="470" dy="18" font-size="11" font-weight="400">delivery engine</tspan></text>
  <text x="730" y="298" width="160" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" font-weight="700" fill="#FFFFFF">Finance Dept<tspan x="730" dy="18" font-size="11" font-weight="400">capital engine</tspan></text>
  <text x="990" y="298" width="160" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" font-weight="700" fill="#FFFFFF">Tech & Dev<tspan x="990" dy="18" font-size="11" font-weight="400">platform engine</tspan></text>

  <!-- leaf nodes -->
  <rect x="125" y="405" width="170" height="56" rx="18" fill="#69AAB5" filter="url(#softShadow)"/>
  <rect x="125" y="486" width="170" height="56" rx="18" fill="#7AB7C1" filter="url(#softShadow)"/>
  <rect x="125" y="567" width="170" height="56" rx="18" fill="#8AC4CD" filter="url(#softShadow)"/>
  <rect x="385" y="405" width="170" height="56" rx="18" fill="#E1857E" filter="url(#softShadow)"/>
  <rect x="385" y="486" width="170" height="56" rx="18" fill="#EA9892" filter="url(#softShadow)"/>
  <rect x="385" y="567" width="170" height="56" rx="18" fill="#F0AAA5" filter="url(#softShadow)"/>
  <rect x="645" y="405" width="170" height="56" rx="18" fill="#95B69E" filter="url(#softShadow)"/>
  <rect x="645" y="486" width="170" height="56" rx="18" fill="#A6C4AE" filter="url(#softShadow)"/>
  <rect x="645" y="567" width="170" height="56" rx="18" fill="#B8D1BE" filter="url(#softShadow)"/>
  <rect x="905" y="405" width="170" height="56" rx="18" fill="#DEB47C" filter="url(#softShadow)"/>
  <rect x="905" y="486" width="170" height="56" rx="18" fill="#E7C392" filter="url(#softShadow)"/>
  <rect x="905" y="567" width="170" height="56" rx="18" fill="#EED1A9" filter="url(#softShadow)"/>

  <text x="210" y="438" width="150" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" font-weight="600" fill="#FFFFFF">Digital Marketing</text>
  <text x="210" y="519" width="150" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" font-weight="600" fill="#FFFFFF">Brand Strategy</text>
  <text x="210" y="600" width="150" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" font-weight="600" fill="#FFFFFF">PR & Events</text>
  <text x="470" y="438" width="150" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" font-weight="600" fill="#FFFFFF">Supply Chain</text>
  <text x="470" y="519" width="150" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" font-weight="600" fill="#FFFFFF">Logistics</text>
  <text x="470" y="600" width="150" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" font-weight="600" fill="#FFFFFF">Customer Success</text>
  <text x="730" y="438" width="150" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" font-weight="600" fill="#FFFFFF">Accounting</text>
  <text x="730" y="519" width="150" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" font-weight="600" fill="#FFFFFF">Investment</text>
  <text x="730" y="600" width="150" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" font-weight="600" fill="#FFFFFF">Audit</text>
  <text x="990" y="438" width="150" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" font-weight="600" fill="#FFFFFF">Frontend</text>
  <text x="990" y="519" width="150" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" font-weight="600" fill="#FFFFFF">Backend</text>
  <text x="990" y="600" width="150" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" font-weight="600" fill="#FFFFFF">Data Science</text>
</svg>
```

## Avoid in this skill
- ❌ Overusing identical colors for all branches; it defeats the visual chunking that makes the hierarchy readable.
- ❌ Heavy black connector lines; they compete with the node labels and make the tree feel mechanical.
- ❌ Sharp-corner rectangles for every node; dense hierarchy charts become harsher and less premium.
- ❌ Applying `filter` effects to `<line>` connectors; filters on lines may be dropped by the translator.
- ❌ Using `<use>` or `<symbol>` to repeat nodes; duplicate the editable SVG primitives directly instead.

## Composition notes
- Keep the root centered in the upper third, with 40–70 px of breathing room before the branch row.
- Assign each primary branch a distinct hue; child nodes should use lighter tints, not unrelated colors.
- Put connectors behind the cards and keep them pale grey so relationships are visible but secondary.
- Use generous horizontal spacing between branches; the empty space is what makes the architecture feel intentional rather than crowded.