# SVG Recipe — Isometric 3D IT Infrastructure Mapping

## Visual mechanism
Build a clean architectural topology map by projecting all objects onto a shared isometric floor plane: red network spines sit flat on the rhombus platform while servers, databases, gateways, and clients are drawn as editable multi-face SVG volumes. The 3D illusion comes from stacked paths, ellipses, face-specific gradients, bevel highlights, and soft shadows rather than flat icon clip-art.

## SVG primitives needed
- 1× `<rect>` for the slide background.
- 3× `<path>` for layered isometric floor plates and inner platform panels.
- 12–18× `<line>` for faint isometric floor grid construction lines.
- 5× stroked `<path>` for thick red network routing spines and branching connections.
- 2× server tower groups made from multiple `<path>` faces, rack-detail `<line>` elements, and small highlight `<path>` strips.
- 3× database / cylinder nodes made from `<ellipse>` tops, `<path>` side walls, and bottom shadow `<ellipse>` elements.
- 2× compact appliance / firewall nodes made from small cuboid `<path>` faces.
- 1× client laptop / workstation made from editable `<path>` screen and base shapes.
- 1× antenna / edge device made from `<line>`, `<circle>`, and small `<path>` shapes.
- Multiple `<linearGradient>` definitions for top, left, and right faces of isometric objects.
- 1× `<radialGradient>` for glossy database-cylinder tops.
- 2× `<filter>` definitions using `feOffset`, `feGaussianBlur`, and `feMerge` for platform and node shadows.
- 8× `<text>` labels with explicit `width` attributes, some rotated to align with isometric routes.

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="floorGlow" x1="220" y1="280" x2="1040" y2="660" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#FAFBFC"/>
      <stop offset="0.6" stop-color="#EBEDF0"/>
      <stop offset="1" stop-color="#D9DCE2"/>
    </linearGradient>
    <linearGradient id="serverLeft" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#3A3D59"/>
      <stop offset="1" stop-color="#171925"/>
    </linearGradient>
    <linearGradient id="serverRight" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#2B2D42"/>
      <stop offset="1" stop-color="#090A10"/>
    </linearGradient>
    <linearGradient id="serverTop" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#5C607C"/>
      <stop offset="1" stop-color="#202234"/>
    </linearGradient>
    <linearGradient id="appliance" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#4E5368"/>
      <stop offset="1" stop-color="#11131D"/>
    </linearGradient>
    <radialGradient id="dbTop" cx="35%" cy="30%" r="75%">
      <stop offset="0" stop-color="#D8DEE8"/>
      <stop offset="0.48" stop-color="#8D99AE"/>
      <stop offset="1" stop-color="#3B4254"/>
    </radialGradient>
    <linearGradient id="dbSide" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#8D99AE"/>
      <stop offset="1" stop-color="#2B2D42"/>
    </linearGradient>
    <filter id="softShadow" x="-30%" y="-30%" width="160%" height="170%">
      <feOffset dx="0" dy="12" result="off"/>
      <feGaussianBlur in="off" stdDeviation="10" result="blur"/>
      <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <filter id="floorShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="18" result="off"/>
      <feGaussianBlur in="off" stdDeviation="18" result="blur"/>
      <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#F4F5F7"/>
  <text x="82" y="82" width="720" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="700" fill="#2B2D42">ISOMETRIC IT INFRASTRUCTURE</text>
  <text x="84" y="116" width="560" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#7A8090">Editable network topology map with volumetric infrastructure nodes</text>

  <path d="M170 545 L585 305 L1120 530 L704 675 Z" fill="#C9CDD5" opacity="0.38" filter="url(#floorShadow)"/>
  <path d="M155 520 L580 270 L1130 505 L700 655 Z" fill="url(#floorGlow)" stroke="#DDE0E6" stroke-width="2"/>
  <path d="M300 508 L598 335 L980 500 L690 618 Z" fill="#FFFFFF" opacity="0.38" stroke="#E3E6EB" stroke-width="1.5"/>

  <line x1="280" y1="593" x2="708" y2="344" stroke="#D9DDE4" stroke-width="1"/>
  <line x1="380" y1="635" x2="809" y2="386" stroke="#D9DDE4" stroke-width="1"/>
  <line x1="480" y1="675" x2="910" y2="427" stroke="#D9DDE4" stroke-width="1"/>
  <line x1="260" y1="458" x2="792" y2="676" stroke="#E1E4EA" stroke-width="1"/>
  <line x1="390" y1="382" x2="930" y2="602" stroke="#E1E4EA" stroke-width="1"/>
  <line x1="520" y1="306" x2="1060" y2="526" stroke="#E1E4EA" stroke-width="1"/>

  <path d="M295 486 L520 356" fill="none" stroke="#8A1F2B" stroke-width="9" stroke-linecap="round" opacity="0.22"/>
  <path d="M295 486 L520 356" fill="none" stroke="#E63946" stroke-width="5" stroke-linecap="round"/>
  <path d="M438 535 L690 390" fill="none" stroke="#E63946" stroke-width="5" stroke-linecap="round"/>
  <path d="M690 390 L760 532 L900 564 L1040 488" fill="none" stroke="#E63946" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M520 356 L690 390 L860 472" fill="none" stroke="#E63946" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>

  <ellipse cx="295" cy="486" rx="54" ry="22" fill="#1A1C2A" opacity="0.25" filter="url(#softShadow)"/>
  <path d="M253 430 C253 418 337 418 337 430 L337 485 C337 497 253 497 253 485 Z" fill="url(#dbSide)"/>
  <ellipse cx="295" cy="430" rx="42" ry="20" fill="url(#dbTop)" stroke="#B7BFCC" stroke-width="1"/>
  <ellipse cx="295" cy="456" rx="42" ry="20" fill="none" stroke="#C8CED8" stroke-width="2" opacity="0.45"/>
  <ellipse cx="295" cy="480" rx="42" ry="20" fill="none" stroke="#C8CED8" stroke-width="2" opacity="0.35"/>

  <ellipse cx="438" cy="535" rx="54" ry="22" fill="#1A1C2A" opacity="0.22" filter="url(#softShadow)"/>
  <path d="M396 479 C396 467 480 467 480 479 L480 535 C480 547 396 547 396 535 Z" fill="url(#dbSide)"/>
  <ellipse cx="438" cy="479" rx="42" ry="20" fill="url(#dbTop)" stroke="#B7BFCC" stroke-width="1"/>
  <ellipse cx="438" cy="506" rx="42" ry="20" fill="none" stroke="#D3D8E1" stroke-width="2" opacity="0.42"/>

  <ellipse cx="520" cy="356" rx="62" ry="24" fill="#1A1C2A" opacity="0.23" filter="url(#softShadow)"/>
  <path d="M475 181 L520 156 L565 181 L520 207 Z" fill="url(#serverTop)" stroke="#767B92" stroke-width="1"/>
  <path d="M475 181 L520 207 L520 356 L475 330 Z" fill="url(#serverLeft)"/>
  <path d="M520 207 L565 181 L565 330 L520 356 Z" fill="url(#serverRight)"/>
  <path d="M482 194 L512 211 L512 219 L482 202 Z" fill="#FFFFFF" opacity="0.18"/>
  <line x1="532" y1="221" x2="556" y2="207" stroke="#C7CDD8" stroke-width="2"/>
  <line x1="532" y1="242" x2="556" y2="228" stroke="#C7CDD8" stroke-width="2"/>
  <line x1="532" y1="263" x2="556" y2="249" stroke="#C7CDD8" stroke-width="2"/>
  <circle cx="543" cy="286" r="3" fill="#E63946"/>

  <ellipse cx="690" cy="390" rx="62" ry="24" fill="#1A1C2A" opacity="0.22" filter="url(#softShadow)"/>
  <path d="M645 215 L690 190 L735 215 L690 241 Z" fill="url(#serverTop)" stroke="#767B92" stroke-width="1"/>
  <path d="M645 215 L690 241 L690 390 L645 364 Z" fill="url(#serverLeft)"/>
  <path d="M690 241 L735 215 L735 364 L690 390 Z" fill="url(#serverRight)"/>
  <path d="M652 228 L682 245 L682 253 L652 236 Z" fill="#FFFFFF" opacity="0.18"/>
  <line x1="702" y1="255" x2="726" y2="241" stroke="#C7CDD8" stroke-width="2"/>
  <line x1="702" y1="276" x2="726" y2="262" stroke="#C7CDD8" stroke-width="2"/>
  <line x1="702" y1="297" x2="726" y2="283" stroke="#C7CDD8" stroke-width="2"/>
  <circle cx="713" cy="320" r="3" fill="#E63946"/>

  <ellipse cx="760" cy="532" rx="35" ry="14" fill="#1A1C2A" opacity="0.22" filter="url(#softShadow)"/>
  <path d="M732 454 L760 438 L788 454 L760 470 Z" fill="#6B7288"/>
  <path d="M732 454 L760 470 L760 532 L732 516 Z" fill="#25283A"/>
  <path d="M760 470 L788 454 L788 516 L760 532 Z" fill="url(#appliance)"/>
  <circle cx="776" cy="492" r="3" fill="#E63946"/>

  <ellipse cx="900" cy="564" rx="46" ry="16" fill="#1A1C2A" opacity="0.20" filter="url(#softShadow)"/>
  <path d="M866 512 L900 492 L936 512 L902 532 Z" fill="#BCC4D1"/>
  <path d="M866 512 L902 532 L902 565 L866 544 Z" fill="#4C5365"/>
  <path d="M902 532 L936 512 L936 544 L902 565 Z" fill="#202332"/>
  <line x1="918" y1="525" x2="930" y2="518" stroke="#E63946" stroke-width="2"/>

  <line x1="818" y1="592" x2="850" y2="510" stroke="#2B2D42" stroke-width="4" stroke-linecap="round"/>
  <circle cx="850" cy="510" r="7" fill="#E63946"/>
  <path d="M805 600 L832 584 L858 598 L832 613 Z" fill="#2B2D42"/>

  <ellipse cx="1040" cy="488" rx="46" ry="16" fill="#1A1C2A" opacity="0.18" filter="url(#softShadow)"/>
  <path d="M1018 421 L1058 444 L1058 484 L1018 461 Z" fill="#151823"/>
  <path d="M1025 431 L1051 446 L1051 471 L1025 456 Z" fill="#E8EDF5"/>
  <path d="M1000 488 L1040 465 L1084 489 L1044 512 Z" fill="#2B2D42"/>
  <path d="M1019 488 L1040 476 L1064 489 L1043 501 Z" fill="#E63946" opacity="0.85"/>

  <text x="232" y="421" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="600" fill="#2B2D42" transform="rotate(-30 232 421)">DATA LAKE</text>
  <text x="493" y="152" width="160" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#2B2D42" transform="rotate(25 493 152)">APP SERVER</text>
  <text x="668" y="186" width="170" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#2B2D42" transform="rotate(25 668 186)">CORE SERVER</text>
  <text x="704" y="448" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="600" fill="#2B2D42" transform="rotate(-30 704 448)">API GATEWAY</text>
  <text x="836" y="500" width="160" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="600" fill="#2B2D42" transform="rotate(-30 836 500)">SECURITY EDGE</text>
  <text x="995" y="424" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="600" fill="#2B2D42" transform="rotate(25 995 424)">CLIENT APPS</text>
</svg>
```

## Avoid in this skill
- ❌ Do not use PowerPoint-only 3D extrusion assumptions in SVG; simulate the isometric volume with explicit editable path faces instead.
- ❌ Do not use `<use>` to duplicate servers or cylinders; duplicate the actual path/ellipse primitives so the translator keeps every node editable.
- ❌ Do not put `filter` on `<line>` grid or connector elements; use filtered ellipses/paths underneath nodes for shadows.
- ❌ Do not apply `clip-path` to paths or groups for floor masking; if a connection must appear hidden, layer the node shapes above the connection instead.
- ❌ Do not use `skewX`, `skewY`, or matrix transforms for isometric projection; draw rhombus/parallelogram coordinates directly with `<path>`.

## Composition notes
- Keep the isometric floor in the lower two-thirds of the slide, leaving the top-left area for a crisp executive title and short explanatory subtitle.
- Network paths should be drawn before nodes so the volumetric servers and databases naturally cover route joints and create depth.
- Use one vivid accent color for all data-flow spines; keep infrastructure volumes dark slate and cool gray for a premium technical look.
- Labels work best as flat annotations placed just off the objects, with a few rotated to echo the 30-degree isometric routing direction.