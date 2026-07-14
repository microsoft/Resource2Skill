# SVG Recipe — Sequential Isometric Build-Up Diagram

## Visual mechanism
A flat, line-art isometric scene is assembled in logical layers: base plate first, then ground zones, buildings, environment assets, and finally annotations. The illusion comes from consistent 30° diamond geometry, shaded prism faces, and clearly separated layer groups that can be revealed across slides for a sequential build-up.

## SVG primitives needed
- 1× `<rect>` for the full-slide soft blueprint background
- 1× `<radialGradient>` and several `<linearGradient>` fills for premium depth on the background, base slab, and building faces
- 1× `<filter id="softShadow">` applied to isometric slabs, buildings, and floating label cards
- 1× `<filter id="glow">` applied to the active focus ring / highlight zone
- 20+ `<path>` elements for isometric diamonds, prism faces, greenery patches, roads, icons, and arrowheads
- 12+ `<line>` elements for base grid lines and annotation connectors
- 10+ `<circle>` / `<ellipse>` elements for trees, people markers, and step badges
- 7× `<text>` elements with explicit `width` for title, subtitle, labels, and build-step numbering
- 5× grouped layer blocks (`<g id="build-...">`) so the same artwork can be copied across multiple slides and progressively revealed

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <radialGradient id="bgGlow" cx="50%" cy="42%" r="70%">
      <stop offset="0%" stop-color="#ffffff"/>
      <stop offset="58%" stop-color="#f7fafc"/>
      <stop offset="100%" stop-color="#e9eef3"/>
    </radialGradient>
    <linearGradient id="baseTop" x1="360" y1="220" x2="910" y2="510" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#ffffff"/>
      <stop offset="100%" stop-color="#edf1f4"/>
    </linearGradient>
    <linearGradient id="baseLeft" x1="348" y1="420" x2="640" y2="590" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#dce3e8"/>
      <stop offset="100%" stop-color="#c7d1d8"/>
    </linearGradient>
    <linearGradient id="baseRight" x1="640" y1="590" x2="930" y2="420" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#cfd9e0"/>
      <stop offset="100%" stop-color="#b8c5cf"/>
    </linearGradient>
    <linearGradient id="greenIso" x1="480" y1="310" x2="790" y2="455" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#dff5df"/>
      <stop offset="100%" stop-color="#9fd8b0"/>
    </linearGradient>
    <linearGradient id="roofBlue" x1="560" y1="190" x2="770" y2="330" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#ffffff"/>
      <stop offset="100%" stop-color="#dfe9f6"/>
    </linearGradient>
    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="14" in="SourceAlpha" result="off"/>
      <feGaussianBlur in="off" stdDeviation="12" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="glow" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="8" result="coloredBlur"/>
      <feMerge>
        <feMergeNode in="coloredBlur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGlow)"/>
  <text x="72" y="78" width="430" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="700" fill="#17202a">Mixed-use district build-up</text>
  <text x="74" y="112" width="420" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#687786">Sequential isometric layers reveal spatial logic without overwhelming the audience.</text>

  <g id="build-01-base" filter="url(#softShadow)">
    <path d="M640 178 L935 348 L640 518 L345 348 Z" fill="url(#baseTop)" stroke="#50606b" stroke-width="2"/>
    <path d="M345 348 L640 518 L640 574 L345 404 Z" fill="url(#baseLeft)" stroke="#50606b" stroke-width="2"/>
    <path d="M935 348 L640 518 L640 574 L935 404 Z" fill="url(#baseRight)" stroke="#50606b" stroke-width="2"/>
    <path d="M345 404 L640 574 L935 404" fill="none" stroke="#82919b" stroke-width="1.5"/>
    <line x1="443" y1="292" x2="738" y2="462" stroke="#d2dbe1" stroke-width="1.3"/>
    <line x1="492" y1="264" x2="787" y2="434" stroke="#d2dbe1" stroke-width="1.3"/>
    <line x1="542" y1="235" x2="837" y2="405" stroke="#d2dbe1" stroke-width="1.3"/>
    <line x1="591" y1="207" x2="886" y2="377" stroke="#d2dbe1" stroke-width="1.3"/>
    <line x1="837" y1="292" x2="542" y2="462" stroke="#d2dbe1" stroke-width="1.3"/>
    <line x1="787" y1="264" x2="492" y2="434" stroke="#d2dbe1" stroke-width="1.3"/>
    <line x1="738" y1="235" x2="443" y2="405" stroke="#d2dbe1" stroke-width="1.3"/>
    <line x1="689" y1="207" x2="394" y2="377" stroke="#d2dbe1" stroke-width="1.3"/>
  </g>

  <g id="build-02-ground-zones">
    <path d="M540 300 L705 395 L617 446 L452 351 Z" fill="url(#greenIso)" stroke="#5aa96f" stroke-width="2" filter="url(#glow)"/>
    <path d="M665 262 L820 352 L756 389 L601 299 Z" fill="#eef3f7" stroke="#a9b5bd" stroke-width="2"/>
    <path d="M492 380 L616 452 L556 486 L432 414 Z" fill="#e8edf1" stroke="#a9b5bd" stroke-width="2"/>
    <path d="M385 346 L443 313 L895 574 L837 607 Z" fill="#d5dce2" opacity="0.78"/>
    <path d="M381 346 L443 310" stroke="#8c98a3" stroke-width="2" fill="none"/>
    <path d="M837 607 L895 574" stroke="#8c98a3" stroke-width="2" fill="none"/>
  </g>

  <g id="build-03-buildings" filter="url(#softShadow)">
    <path d="M585 193 L690 254 L690 338 L585 277 Z" fill="#d2dae3" stroke="#495661" stroke-width="2"/>
    <path d="M690 254 L760 214 L760 298 L690 338 Z" fill="#bcc8d2" stroke="#495661" stroke-width="2"/>
    <path d="M585 193 L655 153 L760 214 L690 254 Z" fill="url(#roofBlue)" stroke="#495661" stroke-width="2"/>
    <line x1="612" y1="215" x2="665" y2="246" stroke="#9aa7b2" stroke-width="1.5"/>
    <line x1="612" y1="243" x2="665" y2="274" stroke="#9aa7b2" stroke-width="1.5"/>
    <line x1="715" y1="251" x2="742" y2="236" stroke="#8f9ca7" stroke-width="1.5"/>
    <line x1="715" y1="280" x2="742" y2="265" stroke="#8f9ca7" stroke-width="1.5"/>

    <path d="M720 323 L812 376 L812 445 L720 392 Z" fill="#dce3ea" stroke="#495661" stroke-width="2"/>
    <path d="M812 376 L876 339 L876 408 L812 445 Z" fill="#c1cbd5" stroke="#495661" stroke-width="2"/>
    <path d="M720 323 L784 286 L876 339 L812 376 Z" fill="#ffffff" stroke="#495661" stroke-width="2"/>

    <path d="M470 363 L548 408 L548 465 L470 420 Z" fill="#e2e8ee" stroke="#495661" stroke-width="2"/>
    <path d="M548 408 L604 376 L604 433 L548 465 Z" fill="#c8d2dc" stroke="#495661" stroke-width="2"/>
    <path d="M470 363 L526 331 L604 376 L548 408 Z" fill="#ffffff" stroke="#495661" stroke-width="2"/>
  </g>

  <g id="build-04-environment">
    <ellipse cx="548" cy="356" rx="15" ry="8" fill="#7dc78f" opacity="0.35"/>
    <circle cx="548" cy="338" r="14" fill="#66bd7b" stroke="#3d8d52" stroke-width="1.5"/>
    <path d="M548 351 L548 374" stroke="#7a5a3b" stroke-width="3" fill="none"/>
    <ellipse cx="625" cy="401" rx="15" ry="8" fill="#7dc78f" opacity="0.35"/>
    <circle cx="625" cy="382" r="15" fill="#77ca89" stroke="#3d8d52" stroke-width="1.5"/>
    <path d="M625 397 L625 420" stroke="#7a5a3b" stroke-width="3" fill="none"/>
    <ellipse cx="772" cy="383" rx="13" ry="7" fill="#7dc78f" opacity="0.35"/>
    <circle cx="772" cy="367" r="12" fill="#6fc083" stroke="#3d8d52" stroke-width="1.5"/>
    <path d="M772 379 L772 399" stroke="#7a5a3b" stroke-width="3" fill="none"/>

    <circle cx="705" cy="464" r="6" fill="#ffb24a"/>
    <path d="M705 470 L697 489 M705 470 L714 487" stroke="#4b5560" stroke-width="2" fill="none"/>
    <circle cx="676" cy="448" r="5" fill="#3d8bfd"/>
    <path d="M676 453 L669 469 M676 453 L684 467" stroke="#4b5560" stroke-width="2" fill="none"/>
  </g>

  <g id="build-05-annotations">
    <rect x="860" y="112" width="248" height="78" rx="18" fill="#ffffff" stroke="#dce3ea" stroke-width="1.5" filter="url(#softShadow)"/>
    <circle cx="888" cy="151" r="14" fill="#1f6feb"/>
    <text x="883" y="157" width="18" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#ffffff">1</text>
    <text x="912" y="144" width="170" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#17202a">Civic core</text>
    <text x="912" y="166" width="175" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#66727e">Tall mixed-use spine anchors density.</text>
    <line x1="860" y1="181" x2="733" y2="259" stroke="#6a7782" stroke-width="1.5" stroke-dasharray="5 5"/>
    <path d="M733 259 L748 259 L740 269 Z" fill="#6a7782"/>

    <rect x="140" y="462" width="250" height="82" rx="18" fill="#ffffff" stroke="#dce3ea" stroke-width="1.5" filter="url(#softShadow)"/>
    <circle cx="169" cy="503" r="14" fill="#43a463"/>
    <text x="164" y="509" width="18" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#ffffff">2</text>
    <text x="194" y="496" width="160" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#17202a">Green connector</text>
    <text x="194" y="519" width="172" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#66727e">Park layer appears after the slab to clarify open space.</text>
    <line x1="390" y1="492" x2="540" y2="365" stroke="#6a7782" stroke-width="1.5" stroke-dasharray="5 5"/>
    <path d="M540 365 L532 378 L527 364 Z" fill="#6a7782"/>

    <text x="72" y="650" width="410" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#7b8792">Build order: base plate → ground uses → structures → assets → annotation layer.</text>
  </g>
</svg>
```

## Avoid in this skill
- ❌ Do not flatten the whole scene into one PNG if editability matters; keep each slab, face, label, and icon as native SVG shapes.
- ❌ Do not use `<use>` / `<symbol>` to repeat trees or buildings; duplicate the actual circles, paths, and lines instead.
- ❌ Do not put `marker-end` on connector `<path>` elements; create arrowheads as small filled `<path>` triangles, or use plain `<line>` connectors.
- ❌ Do not apply `filter` to `<line>` grid or connector strokes; shadows should be on paths, cards, circles, or text only.
- ❌ Do not use skew/matrix transforms to fake isometric projection; draw the diamond and prism face coordinates explicitly.

## Composition notes
- Keep the isometric model centered in the middle 60% of the slide, with wide negative space for callouts on the left and right.
- Build the diagram as named groups so each slide can reveal one additional group, simulating the PowerPoint drop/morph build-up.
- Use a disciplined color rhythm: white/gray architecture, muted blue-gray outlines, one soft green environmental layer, and one accent blue for priority labels.
- Preserve the same 30° diamond geometry for every road, park, roof, and face; inconsistent angles immediately break the isometric illusion.