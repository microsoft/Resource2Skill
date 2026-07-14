# SVG Recipe — Dynamic Cloud Architecture Flow Diagram

## Visual mechanism
A static cloud blueprint becomes an active process narrative by combining dashed logical boundaries, color-coded service cards, and bright cyan dashed arrows that read as “data in motion.” The slide should feel ordered and technical: client/source on the left, cloud execution zone on the right, with connectors guiding the eye through the architecture.

## SVG primitives needed
- 1× `<rect>` full-slide background with a subtle gradient.
- 4× large `<rect>` grouping boundaries for “Client Environment,” “AWS Cloud,” and internal VPC/subnet zones.
- 7× rounded `<rect>` service cards with white fills, shadows, and color-coded borders.
- 10–14× `<line>` segments for dashed cyan flow connectors; put `marker-end` directly on the final `<line>` of each arrow.
- 4–6× `<path>` glow strokes behind elbow flows, plus small vector service icons inside cards.
- 6–8× `<circle>` elements for icon accents and numbered flow badges.
- 1× `<marker id="arrowCyan">` for editable arrowheads on lines.
- 1× `<filter id="cardShadow">` for service card elevation.
- 1× `<filter id="flowGlow">` applied to decorative path glows behind connectors.
- 2× `<linearGradient>` definitions for premium background and cloud header styling.
- Multiple `<text>` elements with explicit `width` attributes for title, labels, service names, and callouts.

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#F8FAFC"/>
      <stop offset="62%" stop-color="#FFFFFF"/>
      <stop offset="100%" stop-color="#EEF6FF"/>
    </linearGradient>
    <linearGradient id="cloudHeader" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#232F3E"/>
      <stop offset="100%" stop-color="#334155"/>
    </linearGradient>
    <filter id="cardShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="6"/>
      <feGaussianBlur stdDeviation="7"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="flowGlow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="4"/>
    </filter>
    <marker id="arrowCyan" markerWidth="12" markerHeight="12" refX="10" refY="6" orient="auto" markerUnits="strokeWidth">
      <path d="M2,2 L10,6 L2,10 Z" fill="#00BFFF"/>
    </marker>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>
  <text x="54" y="58" width="760" font-family="Segoe UI, Microsoft YaHei" font-size="30" font-weight="700" fill="#111827">Serverless Event Processing Architecture</text>
  <text x="56" y="88" width="760" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#64748B">Dashed cyan paths emphasize runtime data movement across isolated cloud boundaries.</text>

  <rect x="48" y="142" width="240" height="480" rx="22" fill="#F9FAFB" stroke="#6B7280" stroke-width="2" stroke-dasharray="8 8"/>
  <text x="72" y="176" width="190" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#4B5563">Client Environment</text>

  <rect x="326" y="118" width="888" height="528" rx="26" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="2"/>
  <rect x="326" y="118" width="888" height="56" rx="26" fill="url(#cloudHeader)"/>
  <text x="358" y="154" width="270" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="700" fill="#FFFFFF">AWS Cloud</text>
  <text x="1040" y="154" width="140" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#CBD5E1">us-east-1</text>

  <rect x="366" y="206" width="370" height="360" rx="18" fill="#F8FAFC" stroke="#94A3B8" stroke-width="1.7" stroke-dasharray="7 7"/>
  <text x="390" y="235" width="230" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#64748B">Public API + Compute Subnet</text>
  <rect x="766" y="206" width="398" height="360" rx="18" fill="#F8FAFC" stroke="#94A3B8" stroke-width="1.7" stroke-dasharray="7 7"/>
  <text x="790" y="235" width="250" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#64748B">Event + Data Services</text>

  <rect x="88" y="292" width="150" height="108" rx="18" fill="#FFFFFF" stroke="#475569" stroke-width="3" filter="url(#cardShadow)"/>
  <circle cx="132" cy="330" r="18" fill="#E0F2FE" stroke="#0284C7" stroke-width="2"/>
  <path d="M121 331 C126 319, 139 319, 143 331 C146 340, 138 346, 132 346 C126 346, 118 340, 121 331 Z" fill="#0284C7"/>
  <text x="109" y="375" width="108" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" text-anchor="middle" fill="#111827">Web Client</text>

  <rect x="374" y="292" width="150" height="108" rx="18" fill="#FFFFFF" stroke="#8B5CF6" stroke-width="4" filter="url(#cardShadow)"/>
  <path d="M423 319 L456 319 L467 340 L456 361 L423 361 L412 340 Z" fill="#F3E8FF" stroke="#8B5CF6" stroke-width="2"/>
  <circle cx="440" cy="340" r="9" fill="#8B5CF6"/>
  <text x="399" y="381" width="100" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" text-anchor="middle" fill="#111827">API Gateway</text>

  <rect x="565" y="292" width="150" height="108" rx="18" fill="#FFFFFF" stroke="#D86613" stroke-width="4" filter="url(#cardShadow)"/>
  <path d="M626 317 L653 317 L653 363 L626 363 Z" fill="#FFF7ED" stroke="#D86613" stroke-width="2"/>
  <path d="M632 329 L647 340 L632 351 Z" fill="#D86613"/>
  <text x="590" y="381" width="100" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" text-anchor="middle" fill="#111827">Lambda</text>

  <rect x="565" y="438" width="150" height="88" rx="18" fill="#FFFFFF" stroke="#E11D48" stroke-width="4" filter="url(#cardShadow)"/>
  <circle cx="640" cy="467" r="18" fill="#FFE4E6" stroke="#E11D48" stroke-width="2"/>
  <path d="M630 467 L650 467 M640 457 L640 477" stroke="#E11D48" stroke-width="4" stroke-linecap="round"/>
  <text x="592" y="506" width="96" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" text-anchor="middle" fill="#111827">Auth Check</text>

  <rect x="800" y="292" width="150" height="108" rx="18" fill="#FFFFFF" stroke="#D86613" stroke-width="4" filter="url(#cardShadow)"/>
  <path d="M847 320 C865 310, 888 320, 895 340 C887 360, 864 370, 847 360 C835 350, 835 330, 847 320 Z" fill="#FFF7ED" stroke="#D86613" stroke-width="2"/>
  <path d="M850 340 L894 340" stroke="#D86613" stroke-width="3"/>
  <text x="823" y="381" width="105" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" text-anchor="middle" fill="#111827">EventBridge</text>

  <rect x="998" y="210" width="132" height="84" rx="16" fill="#FFFFFF" stroke="#3355DA" stroke-width="4" filter="url(#cardShadow)"/>
  <ellipse cx="1064" cy="234" rx="31" ry="10" fill="#DBEAFE" stroke="#3355DA" stroke-width="2"/>
  <path d="M1033 234 L1033 262 C1033 268,1095 268,1095 262 L1095 234" fill="#DBEAFE" stroke="#3355DA" stroke-width="2"/>
  <text x="1024" y="283" width="82" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" text-anchor="middle" fill="#111827">DynamoDB</text>

  <rect x="998" y="320" width="132" height="84" rx="16" fill="#FFFFFF" stroke="#3F8624" stroke-width="4" filter="url(#cardShadow)"/>
  <path d="M1042 342 L1086 342 L1093 370 L1035 370 Z" fill="#DCFCE7" stroke="#3F8624" stroke-width="2"/>
  <path d="M1048 336 L1080 336 L1086 342 L1042 342 Z" fill="#BBF7D0" stroke="#3F8624" stroke-width="2"/>
  <text x="1029" y="393" width="72" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" text-anchor="middle" fill="#111827">S3 Bucket</text>

  <rect x="998" y="430" width="132" height="84" rx="16" fill="#FFFFFF" stroke="#64748B" stroke-width="4" filter="url(#cardShadow)"/>
  <circle cx="1064" cy="459" r="22" fill="#F1F5F9" stroke="#64748B" stroke-width="2"/>
  <path d="M1051 464 L1060 455 L1068 462 L1078 447" fill="none" stroke="#64748B" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
  <text x="1019" y="503" width="90" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" text-anchor="middle" fill="#111827">CloudWatch</text>

  <path d="M238 346 L374 346" stroke="#00BFFF" stroke-width="10" stroke-opacity="0.16" fill="none" filter="url(#flowGlow)"/>
  <line x1="238" y1="346" x2="374" y2="346" stroke="#00BFFF" stroke-width="4" stroke-dasharray="13 9" marker-end="url(#arrowCyan)"/>
  <line x1="524" y1="346" x2="565" y2="346" stroke="#00BFFF" stroke-width="4" stroke-dasharray="13 9" marker-end="url(#arrowCyan)"/>
  <line x1="715" y1="346" x2="800" y2="346" stroke="#00BFFF" stroke-width="4" stroke-dasharray="13 9" marker-end="url(#arrowCyan)"/>

  <path d="M640 400 L640 438" stroke="#00BFFF" stroke-width="10" stroke-opacity="0.14" fill="none" filter="url(#flowGlow)"/>
  <line x1="640" y1="400" x2="640" y2="438" stroke="#00BFFF" stroke-width="4" stroke-dasharray="13 9" marker-end="url(#arrowCyan)"/>

  <path d="M950 346 L970 346 L970 252 L998 252" stroke="#00BFFF" stroke-width="10" stroke-opacity="0.14" fill="none" filter="url(#flowGlow)"/>
  <line x1="950" y1="346" x2="970" y2="346" stroke="#00BFFF" stroke-width="4" stroke-dasharray="13 9"/>
  <line x1="970" y1="346" x2="970" y2="252" stroke="#00BFFF" stroke-width="4" stroke-dasharray="13 9"/>
  <line x1="970" y1="252" x2="998" y2="252" stroke="#00BFFF" stroke-width="4" stroke-dasharray="13 9" marker-end="url(#arrowCyan)"/>

  <line x1="950" y1="362" x2="998" y2="362" stroke="#00BFFF" stroke-width="4" stroke-dasharray="13 9" marker-end="url(#arrowCyan)"/>

  <path d="M950 378 L970 378 L970 472 L998 472" stroke="#00BFFF" stroke-width="10" stroke-opacity="0.14" fill="none" filter="url(#flowGlow)"/>
  <line x1="950" y1="378" x2="970" y2="378" stroke="#00BFFF" stroke-width="4" stroke-dasharray="13 9"/>
  <line x1="970" y1="378" x2="970" y2="472" stroke="#00BFFF" stroke-width="4" stroke-dasharray="13 9"/>
  <line x1="970" y1="472" x2="998" y2="472" stroke="#00BFFF" stroke-width="4" stroke-dasharray="13 9" marker-end="url(#arrowCyan)"/>

  <circle cx="306" cy="346" r="13" fill="#00BFFF"/>
  <text x="302" y="351" width="10" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#FFFFFF">1</text>
  <circle cx="545" cy="346" r="13" fill="#00BFFF"/>
  <text x="541" y="351" width="10" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#FFFFFF">2</text>
  <circle cx="756" cy="346" r="13" fill="#00BFFF"/>
  <text x="752" y="351" width="10" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#FFFFFF">3</text>
  <circle cx="972" cy="405" r="13" fill="#00BFFF"/>
  <text x="968" y="410" width="10" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#FFFFFF">4</text>

  <rect x="366" y="594" width="798" height="34" rx="17" fill="#E0F2FE" stroke="#7DD3FC" stroke-width="1"/>
  <text x="390" y="616" width="740" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#0369A1">Design cue: cyan dashed arrows indicate runtime event flow; gray dashed boxes indicate ownership and network boundaries.</text>
</svg>
```

## Avoid in this skill
- ❌ Do not use `marker-end` on `<path>` connectors; arrowheads may disappear. Use `<line>` segments and place `marker-end` directly on the final line of each arrow.
- ❌ Do not apply filters to `<line>` elements; create separate decorative `<path>` glow strokes behind the lines instead.
- ❌ Do not rely on real SVG animation such as `<animate>` or dash-offset animation; represent motion with dashed cyan strokes and numbered flow badges.
- ❌ Do not create dense spaghetti routing; use orthogonal connector segments with generous spacing between service cards.
- ❌ Do not use clip paths or masks on shapes for boundary shading; keep grouping boxes as editable rounded rectangles.

## Composition notes
- Reserve the left 20–25% of the canvas for external clients or source systems; allocate the right 70–75% to the cloud boundary.
- Use pale gray dashed containers for logical ownership zones, then place high-contrast white service cards inside them.
- Keep the primary flow horizontally centered and make secondary fan-out flows branch to the right, not back across the diagram.
- Use one vivid connector color, usually cyan, so the flow layer is visually distinct from infrastructure boundaries and service-type colors.