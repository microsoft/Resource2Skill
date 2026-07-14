# SVG Recipe — Split Content with Sidebar

## Visual mechanism
A wide, rounded primary content panel occupies the left two-thirds of the slide while a narrower, visually distinct sidebar anchors the right edge. The layout feels editorial and executive by combining a strong color-block split, card-like bullet rows, subtle depth, and a sidebar that can hold context, notes, or a supporting takeaway.

## SVG primitives needed
- 1× `<rect>` for the full-slide gradient background
- 2× large rounded `<rect>` panels for the main content area and sidebar
- 4× small rounded `<rect>` bullet cards inside the primary panel
- 4× `<circle>` number badges for bullet sequencing
- 2× decorative `<path>` blobs for premium abstract depth behind panels
- 1× `<image>` clipped into a rounded rectangle for a sidebar thumbnail / contextual visual
- 1× `<clipPath>` with rounded `<rect>` applied to the sidebar image
- 3× `<linearGradient>` fills for background, main panel, and sidebar surface
- 1× `<filter id="softShadow">` applied to panels and cards
- Multiple `<text>` elements with explicit `width` attributes for headline, lead, bullets, and sidebar copy
- Thin `<rect>` dividers and accent bars for structure and hierarchy

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#071827"/>
      <stop offset="58%" stop-color="#102A43"/>
      <stop offset="100%" stop-color="#173B57"/>
    </linearGradient>

    <linearGradient id="mainPanelGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#F7FAFC"/>
      <stop offset="100%" stop-color="#E6EEF6"/>
    </linearGradient>

    <linearGradient id="sidePanelGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#16324A"/>
      <stop offset="100%" stop-color="#0B1F33"/>
    </linearGradient>

    <linearGradient id="accentGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#2DD4BF"/>
      <stop offset="100%" stop-color="#38BDF8"/>
    </linearGradient>

    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="14" result="offset"/>
      <feGaussianBlur in="offset" stdDeviation="18" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="glow" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="24"/>
    </filter>

    <clipPath id="sidebarPhotoClip">
      <rect x="990" y="98" width="196" height="124" rx="24" ry="24"/>
    </clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>

  <path d="M-80,520 C120,430 190,640 390,575 C560,520 640,615 780,720 L-80,720 Z"
        fill="#2DD4BF" opacity="0.18" filter="url(#glow)"/>
  <path d="M1030,-60 C1150,10 1235,30 1340,10 L1340,285 C1220,250 1120,230 1010,285 C940,320 895,210 945,120 C965,84 990,35 1030,-60 Z"
        fill="#38BDF8" opacity="0.14" filter="url(#glow)"/>

  <rect x="56" y="56" width="834" height="608" rx="34" fill="url(#mainPanelGrad)" filter="url(#softShadow)"/>
  <rect x="922" y="56" width="302" height="608" rx="34" fill="url(#sidePanelGrad)" filter="url(#softShadow)"/>
  <rect x="922" y="56" width="12" height="608" rx="6" fill="url(#accentGrad)"/>

  <text x="104" y="118" width="340" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="13" font-weight="700" letter-spacing="2.4" fill="#0F766E">OPERATING MODEL</text>

  <text x="102" y="176" width="350" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="47" font-weight="800" fill="#102A43">
    <tspan x="102" dy="0">Split focus,</tspan>
    <tspan x="102" dy="54">clear action</tspan>
  </text>

  <rect x="104" y="270" width="54" height="5" rx="2.5" fill="url(#accentGrad)"/>

  <text x="102" y="318" width="352" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="22" font-weight="650" fill="#24435A">
    <tspan x="102" dy="0">Use the main panel for the argument,</tspan>
    <tspan x="102" dy="31">then reserve the sidebar for proof,</tspan>
    <tspan x="102" dy="31">constraints, or next-step context.</tspan>
  </text>

  <text x="104" y="462" width="320" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="15" fill="#62748A">
    <tspan x="104" dy="0">Best when the audience needs to scan a structured</tspan>
    <tspan x="104" dy="24">set of decisions while keeping one persistent note</tspan>
    <tspan x="104" dy="24">visible on the right.</tspan>
  </text>

  <rect x="462" y="108" width="2" height="504" rx="1" fill="#CBD5E1"/>

  <rect x="500" y="118" width="328" height="94" rx="22" fill="#FFFFFF" opacity="0.92" filter="url(#softShadow)"/>
  <circle cx="538" cy="165" r="18" fill="url(#accentGrad)"/>
  <text x="532" y="172" width="16" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="18" font-weight="800" fill="#FFFFFF">1</text>
  <text x="572" y="150" width="220" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="18" font-weight="750" fill="#102A43">Frame the split</text>
  <text x="572" y="178" width="230" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="14" fill="#5F6F82">Name the primary question before showing evidence.</text>

  <rect x="500" y="236" width="328" height="94" rx="22" fill="#FFFFFF" opacity="0.92" filter="url(#softShadow)"/>
  <circle cx="538" cy="283" r="18" fill="#102A43"/>
  <text x="532" y="290" width="16" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="18" font-weight="800" fill="#FFFFFF">2</text>
  <text x="572" y="268" width="220" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="18" font-weight="750" fill="#102A43">Group the bullets</text>
  <text x="572" y="296" width="235" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="14" fill="#5F6F82">Each card should hold one clear recommendation.</text>

  <rect x="500" y="354" width="328" height="94" rx="22" fill="#FFFFFF" opacity="0.92" filter="url(#softShadow)"/>
  <circle cx="538" cy="401" r="18" fill="#102A43"/>
  <text x="532" y="408" width="16" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="18" font-weight="800" fill="#FFFFFF">3</text>
  <text x="572" y="386" width="220" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="18" font-weight="750" fill="#102A43">Anchor the detail</text>
  <text x="572" y="414" width="238" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="14" fill="#5F6F82">Use the sidebar for supporting nuance, not more bullets.</text>

  <rect x="500" y="472" width="328" height="94" rx="22" fill="#FFFFFF" opacity="0.92" filter="url(#softShadow)"/>
  <circle cx="538" cy="519" r="18" fill="#102A43"/>
  <text x="532" y="526" width="16" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="18" font-weight="800" fill="#FFFFFF">4</text>
  <text x="572" y="504" width="220" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="18" font-weight="750" fill="#102A43">Close with action</text>
  <text x="572" y="532" width="238" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="14" fill="#5F6F82">End the sequence with a concrete owner or decision.</text>

  <image x="990" y="98" width="196" height="124" preserveAspectRatio="xMidYMid slice"
         href="https://images.example.com/executive-workshop-whiteboard.jpg"
         clip-path="url(#sidebarPhotoClip)"/>

  <text x="982" y="268" width="210" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="13" font-weight="700" letter-spacing="2.2" fill="#67E8F9">SIDEBAR NOTE</text>

  <text x="982" y="318" width="212" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="30" font-weight="800" fill="#FFFFFF">
    <tspan x="982" dy="0">Decision lens</tspan>
  </text>

  <text x="982" y="368" width="212" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="16" fill="#C8D7E5">
    <tspan x="982" dy="0">The sidebar should remain visually quieter than the</tspan>
    <tspan x="982" dy="24">main panel, but strong enough to hold persistent</tspan>
    <tspan x="982" dy="24">context while the audience scans the list.</tspan>
  </text>

  <rect x="982" y="470" width="210" height="76" rx="20" fill="#FFFFFF" opacity="0.10"/>
  <text x="1004" y="502" width="160" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" fill="#A7F3D0">Recommended density</text>
  <text x="1004" y="531" width="160" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="24" font-weight="800" fill="#FFFFFF">3–4 bullets</text>

  <rect x="982" y="566" width="210" height="1" fill="#FFFFFF" opacity="0.18"/>
  <text x="982" y="604" width="210" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="14" font-weight="650" fill="#E0F2FE">Keep this area for caveats, definitions, proof points, or the final takeaway.</text>
</svg>
```

## Avoid in this skill
- ❌ Do not make the sidebar the same visual weight as the main panel; it should support, not compete.
- ❌ Do not use more than four primary bullet cards or the left panel will become crowded.
- ❌ Do not place a `clip-path` on text, cards, or decorative shapes; use clipping only on the sidebar `<image>`.
- ❌ Do not use `<foreignObject>` for rich text blocks; use SVG `<text>` and `<tspan>` with explicit `width`.
- ❌ Do not rely on `<pattern>` fills for the panel texture; use gradients, opacity, and simple decorative paths instead.

## Composition notes
- Keep the main panel around 65–70% of slide width and the sidebar around 22–25%, with a visible gutter between them.
- Use the left side of the main panel for the headline and lead, then reserve the middle-right of that panel for stacked bullet cards.
- The sidebar works best with a small image or icon at top, a short title, one paragraph, and one compact metric or callout.
- Maintain color rhythm by using one accent gradient repeatedly: title rule, sidebar strip, first badge, and small labels.