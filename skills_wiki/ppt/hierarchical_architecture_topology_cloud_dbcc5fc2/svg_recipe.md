# SVG Recipe — Hierarchical Architecture Topology (Cloud Native)

## Visual mechanism
Use nested, lightly tinted boundary containers to encode cloud hierarchy, then place color-coded service nodes on a strict grid inside them. Orthogonal arrows and numbered badges create a step-by-step narrative path through the topology without turning the slide into a tangled network map.

## SVG primitives needed
- 1× `<rect>` full-slide background with subtle gradient fill
- 1× decorative `<path>` cloud silhouette behind the title for visual theme
- 5× large `<rect>` boundary containers for Cloud, Region, VPC, and Availability Zones
- 9× rounded `<rect>` node cards for client, DNS/CDN, gateway, load balancer, compute, database, queue, cache, and observability services
- 9× small `<path>` or `<circle>` icon marks inside service nodes
- 8× `<line>` connectors with `marker-end` directly on each line for editable arrows
- 5× `<circle>` numbered callout badges with white text
- 1× `<filter id="softShadow">` applied to node cards and callout badges
- 1× `<linearGradient>` for the background and 1× `<linearGradient>` for the title accent
- Multiple `<text>` elements with explicit `width` attributes for labels, node names, and annotations

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#F7FAFF"/>
      <stop offset="58%" stop-color="#FFFFFF"/>
      <stop offset="100%" stop-color="#EEF4FF"/>
    </linearGradient>
    <linearGradient id="titleAccent" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#0073BB"/>
      <stop offset="100%" stop-color="#8C4FFF"/>
    </linearGradient>
    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="6"/>
      <feGaussianBlur stdDeviation="7"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <marker id="arrow" markerWidth="10" markerHeight="8" refX="9" refY="4" orient="auto" markerUnits="strokeWidth">
      <path d="M0,0 L10,4 L0,8 Z" fill="#546B82"/>
    </marker>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bg)"/>
  <path d="M920 56 C948 28 1001 28 1024 66 C1064 62 1094 86 1098 120 C1139 126 1164 153 1158 188 L880 188 C850 184 832 162 838 137 C845 105 879 91 904 102 C902 83 907 67 920 56 Z"
        fill="#EAF2FF" stroke="#D6E3F5" stroke-width="2"/>

  <text x="72" y="60" width="760" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="700" fill="#232F3E">
    Multi-region API Gateway Architecture
  </text>
  <rect x="72" y="82" width="372" height="5" rx="2.5" fill="url(#titleAccent)"/>
  <text x="72" y="118" width="770" font-family="Segoe UI, Microsoft YaHei" font-size="16" fill="#546B82">
    Nested cloud boundaries, grid-aligned services, and numbered request flow for an executive-readable topology.
  </text>

  <rect x="54" y="150" width="1172" height="512" rx="24" fill="#FFFFFF" fill-opacity="0.54" stroke="#879596" stroke-width="2" stroke-dasharray="8 8"/>
  <text x="78" y="178" width="210" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#232F3E">Cloud Provider Account</text>

  <rect x="86" y="202" width="1098" height="410" rx="20" fill="#F8FBFF" fill-opacity="0.7" stroke="#546B82" stroke-width="2"/>
  <text x="110" y="230" width="220" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#232F3E">Primary Region · us-east-1</text>

  <rect x="124" y="258" width="1020" height="294" rx="18" fill="#FFFFFF" fill-opacity="0.72" stroke="#8C4FFF" stroke-width="2" stroke-dasharray="6 6"/>
  <text x="148" y="286" width="180" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#8C4FFF">Application VPC</text>

  <rect x="406" y="304" width="292" height="204" rx="16" fill="#FFF8F1" fill-opacity="0.74" stroke="#ED7100" stroke-width="1.5"/>
  <text x="426" y="329" width="180" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#ED7100">Availability Zone A</text>

  <rect x="734" y="304" width="292" height="204" rx="16" fill="#F3F7FF" fill-opacity="0.78" stroke="#3355DA" stroke-width="1.5"/>
  <text x="754" y="329" width="180" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#3355DA">Availability Zone B</text>

  <rect x="140" y="344" width="130" height="76" rx="16" fill="#FFFFFF" stroke="#646464" stroke-width="3" filter="url(#softShadow)"/>
  <circle cx="166" cy="372" r="13" fill="#646464"/>
  <path d="M158 372 C160 364 172 364 174 372 C172 380 160 380 158 372 Z" fill="#FFFFFF"/>
  <text x="186" y="373" width="70" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#646464">Client</text>
  <text x="186" y="392" width="74" font-family="Segoe UI, Microsoft YaHei" font-size="10" fill="#646464">browser / app</text>

  <rect x="306" y="344" width="142" height="76" rx="16" fill="#FFFFFF" stroke="#8C4FFF" stroke-width="3" filter="url(#softShadow)"/>
  <circle cx="333" cy="374" r="15" fill="none" stroke="#8C4FFF" stroke-width="3"/>
  <line x1="318" y1="374" x2="348" y2="374" stroke="#8C4FFF" stroke-width="2"/>
  <line x1="333" y1="359" x2="333" y2="389" stroke="#8C4FFF" stroke-width="2"/>
  <text x="360" y="373" width="76" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#8C4FFF">DNS + CDN</text>
  <text x="360" y="392" width="72" font-family="Segoe UI, Microsoft YaHei" font-size="10" fill="#8C4FFF">edge routing</text>

  <rect x="500" y="344" width="142" height="76" rx="16" fill="#FFFFFF" stroke="#8C4FFF" stroke-width="3" filter="url(#softShadow)"/>
  <path d="M528 360 L548 372 L548 392 L528 404 L508 392 L508 372 Z" fill="#F4EFFF" stroke="#8C4FFF" stroke-width="2"/>
  <text x="560" y="373" width="70" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#8C4FFF">API GW</text>
  <text x="560" y="392" width="72" font-family="Segoe UI, Microsoft YaHei" font-size="10" fill="#8C4FFF">auth + throttles</text>

  <rect x="674" y="344" width="142" height="76" rx="16" fill="#FFFFFF" stroke="#8C4FFF" stroke-width="3" filter="url(#softShadow)"/>
  <path d="M704 363 L731 382 L704 401 Z" fill="#8C4FFF"/>
  <line x1="696" y1="382" x2="731" y2="382" stroke="#8C4FFF" stroke-width="4"/>
  <text x="738" y="373" width="66" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#8C4FFF">ALB</text>
  <text x="738" y="392" width="66" font-family="Segoe UI, Microsoft YaHei" font-size="10" fill="#8C4FFF">routing</text>

  <rect x="520" y="438" width="142" height="76" rx="16" fill="#FFFFFF" stroke="#ED7100" stroke-width="3" filter="url(#softShadow)"/>
  <path d="M548 455 L570 477 L548 499 L526 477 Z" fill="#FFF1E3" stroke="#ED7100" stroke-width="2"/>
  <text x="582" y="467" width="66" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#ED7100">Lambda</text>
  <text x="582" y="486" width="70" font-family="Segoe UI, Microsoft YaHei" font-size="10" fill="#ED7100">functions</text>

  <rect x="846" y="344" width="142" height="76" rx="16" fill="#FFFFFF" stroke="#ED7100" stroke-width="3" filter="url(#softShadow)"/>
  <rect x="876" y="363" width="22" height="28" rx="4" fill="#FFF1E3" stroke="#ED7100" stroke-width="2"/>
  <line x1="882" y1="397" x2="892" y2="397" stroke="#ED7100" stroke-width="3"/>
  <text x="908" y="373" width="66" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#ED7100">ECS</text>
  <text x="908" y="392" width="70" font-family="Segoe UI, Microsoft YaHei" font-size="10" fill="#ED7100">service pool</text>

  <rect x="846" y="438" width="142" height="76" rx="16" fill="#FFFFFF" stroke="#3355DA" stroke-width="3" filter="url(#softShadow)"/>
  <path d="M875 458 C875 452 903 452 903 458 L903 493 C903 499 875 499 875 493 Z" fill="#EEF3FF" stroke="#3355DA" stroke-width="2"/>
  <path d="M875 458 C875 464 903 464 903 458" fill="none" stroke="#3355DA" stroke-width="2"/>
  <text x="914" y="467" width="60" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#3355DA">Aurora</text>
  <text x="914" y="486" width="62" font-family="Segoe UI, Microsoft YaHei" font-size="10" fill="#3355DA">writer</text>

  <rect x="1032" y="344" width="92" height="76" rx="16" fill="#FFFFFF" stroke="#3355DA" stroke-width="3" filter="url(#softShadow)"/>
  <path d="M1058 364 L1098 364 L1098 392 L1058 392 Z M1064 370 L1078 382 L1092 370" fill="none" stroke="#3355DA" stroke-width="2"/>
  <text x="1048" y="407" width="62" font-family="Segoe UI, Microsoft YaHei" font-size="11" font-weight="700" fill="#3355DA">Queue</text>

  <rect x="1032" y="438" width="92" height="76" rx="16" fill="#FFFFFF" stroke="#0073BB" stroke-width="3" filter="url(#softShadow)"/>
  <circle cx="1078" cy="468" r="17" fill="#E9F6FF" stroke="#0073BB" stroke-width="2"/>
  <path d="M1068 468 L1076 476 L1090 458" fill="none" stroke="#0073BB" stroke-width="3"/>
  <text x="1045" y="501" width="70" font-family="Segoe UI, Microsoft YaHei" font-size="11" font-weight="700" fill="#0073BB">Monitor</text>

  <line x1="270" y1="382" x2="306" y2="382" stroke="#546B82" stroke-width="2" marker-end="url(#arrow)"/>
  <line x1="448" y1="382" x2="500" y2="382" stroke="#546B82" stroke-width="2" marker-end="url(#arrow)"/>
  <line x1="642" y1="382" x2="674" y2="382" stroke="#546B82" stroke-width="2" marker-end="url(#arrow)"/>
  <line x1="816" y1="382" x2="846" y2="382" stroke="#546B82" stroke-width="2" marker-end="url(#arrow)"/>
  <line x1="917" y1="420" x2="917" y2="438" stroke="#546B82" stroke-width="2" marker-end="url(#arrow)"/>
  <line x1="662" y1="476" x2="846" y2="476" stroke="#546B82" stroke-width="2" marker-end="url(#arrow)"/>
  <line x1="988" y1="382" x2="1032" y2="382" stroke="#546B82" stroke-width="2" marker-end="url(#arrow)"/>
  <line x1="988" y1="476" x2="1032" y2="476" stroke="#546B82" stroke-width="2" marker-end="url(#arrow)"/>

  <circle cx="287" cy="356" r="17" fill="#0073BB" filter="url(#softShadow)"/>
  <text x="282" y="362" width="14" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#FFFFFF">1</text>
  <circle cx="474" cy="356" r="17" fill="#0073BB" filter="url(#softShadow)"/>
  <text x="469" y="362" width="14" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#FFFFFF">2</text>
  <circle cx="823" cy="356" r="17" fill="#0073BB" filter="url(#softShadow)"/>
  <text x="818" y="362" width="14" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#FFFFFF">3</text>
  <circle cx="1004" cy="448" r="17" fill="#0073BB" filter="url(#softShadow)"/>
  <text x="999" y="454" width="14" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#FFFFFF">4</text>
  <circle cx="686" cy="476" r="17" fill="#0073BB" filter="url(#softShadow)"/>
  <text x="681" y="482" width="14" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#FFFFFF">5</text>

  <text x="144" y="584" width="850" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#546B82">
    Reading order: user traffic enters from the left, crosses the networking tier, fans into compute, persists in the data tier, then emits async events and telemetry.
  </text>
</svg>
```

## Avoid in this skill
- ❌ Do not use freeform diagonal “spaghetti” connectors; keep request flow orthogonal and grid-aligned.
- ❌ Do not apply `marker-end` to `<path>` connectors; use `<line>` and place `marker-end` on every line directly.
- ❌ Do not rely on `<use>` or `<symbol>` for repeated service cards; duplicate editable SVG primitives instead.
- ❌ Do not clip or mask non-image elements for container effects; use transparent fills, strokes, gradients, and native paths.
- ❌ Do not omit `width` on text labels; topology diagrams need deterministic PowerPoint text boxes.

## Composition notes
- Reserve the top 18–20% of the canvas for title, subtitle, and a small cloud-theme accent; keep the architecture map below it.
- Use large nested containers with 10–15% internal padding so hierarchy is visible before the viewer reads labels.
- Color rhythm should map to function: purple for networking, orange for compute, blue for data, gray/navy for boundaries and connectors.
- Place numbered badges directly beside key transitions, not in a separate legend, so the architecture itself becomes the narrative.