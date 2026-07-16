# SVG Recipe — Hierarchical Cloud Architecture Schematic

## Visual mechanism
Use nested rounded containers to show ownership and network boundaries, then place elevated service nodes inside them and connect nodes with disciplined left-to-right flow lines. The hierarchy explains “where things live,” while orthogonal arrows explain “how traffic moves.”

## SVG primitives needed
- 1× full-slide `<rect>` for the soft background surface
- 3× large rounded `<rect>` containers for Cloud Project, Region, and VPC / private network boundaries
- 9× smaller rounded `<rect>` node cards for users, edge, compute, data, and operations services
- 12× `<text>` labels for title, container labels, and node names; every text element requires explicit `width`
- 10× `<line>` connector segments for orthogonal routing, with `marker-end` only on final arrow segments
- 1× `<marker>` in `<defs>` for native arrowheads on `<line>` elements
- 1× `<filter id="cardShadow">` using `feOffset`, `feGaussianBlur`, and `feMerge` for elevated service cards
- 1× `<filter id="softGlow">` using `feGaussianBlur` for a subtle cloud-zone glow
- 3× `<linearGradient>` fills for background, container atmosphere, and primary service nodes
- 8× small `<path>` icon glyphs inside cards for cloud, gateway, compute, database, queue, lock, chart, and user concepts
- 2× dashed `<rect>` outlines for security / platform boundaries

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#F7FAFF"/>
      <stop offset="55%" stop-color="#EEF4FB"/>
      <stop offset="100%" stop-color="#F8FBFF"/>
    </linearGradient>
    <linearGradient id="vpcFill" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#F1F7FF"/>
      <stop offset="100%" stop-color="#EAF2FE"/>
    </linearGradient>
    <linearGradient id="nodeBlue" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="100%" stop-color="#F5F9FF"/>
    </linearGradient>
    <filter id="cardShadow" x="-20%" y="-25%" width="140%" height="160%">
      <feOffset dx="0" dy="8" in="SourceAlpha" result="off"/>
      <feGaussianBlur stdDeviation="8" in="off" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="softGlow" x="-25%" y="-25%" width="150%" height="150%">
      <feGaussianBlur stdDeviation="18"/>
    </filter>
    <marker id="arrowDark" markerWidth="10" markerHeight="8" refX="9" refY="4" orient="auto">
      <path d="M0,0 L10,4 L0,8 Z" fill="#5F6368"/>
    </marker>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>
  <text x="64" y="58" width="720" font-family="Segoe UI, Microsoft YaHei" font-size="28" font-weight="700" fill="#202124">Hierarchical Cloud Architecture Schematic</text>
  <text x="64" y="88" width="760" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#5F6368">Nested containment communicates ownership, region, private network, and service flow.</text>

  <rect x="300" y="114" width="900" height="538" rx="28" fill="#FFFFFF" stroke="#9AA0A6" stroke-width="2" stroke-dasharray="10 8"/>
  <text x="326" y="148" width="300" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#5F6368">CLOUD PROJECT: retail-platform-prod</text>

  <rect x="338" y="172" width="824" height="438" rx="24" fill="#FAFCFF" stroke="#DADCE0" stroke-width="1.5"/>
  <text x="364" y="204" width="300" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#5F6368">REGION: us-central1</text>

  <rect x="374" y="226" width="748" height="334" rx="22" fill="url(#vpcFill)" stroke="#AECBFA" stroke-width="2"/>
  <rect x="394" y="248" width="708" height="290" rx="18" fill="none" stroke="#C7D2FE" stroke-width="1.5" stroke-dasharray="8 7"/>
  <text x="404" y="258" width="360" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#3C4043">PRIVATE VPC NETWORK / ZERO-TRUST SERVICE MESH</text>

  <ellipse cx="750" cy="390" rx="310" ry="170" fill="#DDEBFF" opacity="0.35" filter="url(#softGlow)"/>

  <rect x="70" y="294" width="150" height="86" rx="18" fill="#FFFFFF" stroke="#F9AB00" stroke-width="2.5" filter="url(#cardShadow)"/>
  <path d="M132 326 c0-13 10-23 23-23 c10 0 19 6 22 15 c10 1 18 10 18 20 c0 12-9 21-21 21 h-48 c-10 0-18-8-18-18 c0-9 6-16 14-18 c2-10 4-17 10-21 z" fill="#FFF7E0" stroke="#F9AB00" stroke-width="2"/>
  <text x="92" y="366" width="106" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#3C4043">Customers</text>

  <rect x="314" y="292" width="150" height="88" rx="16" fill="url(#nodeBlue)" stroke="#4285F4" stroke-width="2.5" filter="url(#cardShadow)"/>
  <path d="M359 318 h60 a12 12 0 0 1 12 12 v14 a12 12 0 0 1-12 12 h-60 a12 12 0 0 1-12-12 v-14 a12 12 0 0 1 12-12 z M359 337 h60" fill="none" stroke="#4285F4" stroke-width="2.5"/>
  <text x="389" y="368" width="120" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#3C4043">Global HTTPS LB</text>

  <rect x="506" y="292" width="150" height="88" rx="16" fill="#FFFFFF" stroke="#34A853" stroke-width="2.5" filter="url(#cardShadow)"/>
  <path d="M564 318 l34 0 l18 18 l-18 18 l-34 0 l-18-18 z" fill="#E6F4EA" stroke="#34A853" stroke-width="2.5"/>
  <text x="581" y="368" width="120" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#3C4043">API Gateway</text>

  <rect x="704" y="278" width="164" height="90" rx="16" fill="#FFFFFF" stroke="#4285F4" stroke-width="2.5" filter="url(#cardShadow)"/>
  <path d="M760 305 h52 v36 h-52 z M770 314 h32 M770 323 h32 M770 332 h22" fill="none" stroke="#4285F4" stroke-width="2.4"/>
  <text x="786" y="356" width="132" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#3C4043">Kubernetes Services</text>

  <rect x="704" y="420" width="164" height="90" rx="16" fill="#FFFFFF" stroke="#A142F4" stroke-width="2.5" filter="url(#cardShadow)"/>
  <path d="M752 446 h68 M752 465 h68 M752 484 h68 M762 437 l-18 18 l18 18 M810 437 l18 18 l-18 18" fill="none" stroke="#A142F4" stroke-width="2.4"/>
  <text x="786" y="498" width="132" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#3C4043">Async Workers</text>

  <rect x="514" y="442" width="150" height="82" rx="16" fill="#FFFFFF" stroke="#F9AB00" stroke-width="2.5" filter="url(#cardShadow)"/>
  <path d="M552 468 h74 M552 482 h74 M552 496 h74 M566 459 l-16 16 l16 16" fill="none" stroke="#F9AB00" stroke-width="2.4"/>
  <text x="589" y="512" width="120" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#3C4043">Pub/Sub Queue</text>

  <rect x="930" y="278" width="150" height="90" rx="16" fill="#FFFFFF" stroke="#34A853" stroke-width="2.5" filter="url(#cardShadow)"/>
  <path d="M970 312 c0-8 16-15 35-15 s35 7 35 15 v34 c0 8-16 15-35 15 s-35-7-35-15 z M970 312 c0 8 16 15 35 15 s35-7 35-15 M970 329 c0 8 16 15 35 15 s35-7 35-15" fill="#E6F4EA" stroke="#34A853" stroke-width="2.3"/>
  <text x="1005" y="356" width="120" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#3C4043">Cloud SQL</text>

  <rect x="930" y="420" width="150" height="90" rx="16" fill="#FFFFFF" stroke="#EA4335" stroke-width="2.5" filter="url(#cardShadow)"/>
  <path d="M978 458 v-10 c0-14 11-25 27-25 s27 11 27 25 v10 M970 458 h70 v36 h-70 z" fill="#FCE8E6" stroke="#EA4335" stroke-width="2.4"/>
  <text x="1005" y="498" width="120" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#3C4043">Secrets / KMS</text>

  <rect x="384" y="590" width="220" height="44" rx="14" fill="#FFFFFF" stroke="#BDC1C6" stroke-width="1.5"/>
  <path d="M412 617 l13-15 l14 10 l15-24 l18 29" fill="none" stroke="#5F6368" stroke-width="2.4"/>
  <text x="482" y="619" width="130" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#5F6368">Observability</text>

  <line x1="220" y1="337" x2="314" y2="337" stroke="#5F6368" stroke-width="2.2" marker-end="url(#arrowDark)"/>
  <line x1="464" y1="337" x2="506" y2="337" stroke="#5F6368" stroke-width="2.2" marker-end="url(#arrowDark)"/>
  <line x1="656" y1="337" x2="704" y2="337" stroke="#5F6368" stroke-width="2.2" marker-end="url(#arrowDark)"/>
  <line x1="868" y1="323" x2="930" y2="323" stroke="#5F6368" stroke-width="2.2" marker-end="url(#arrowDark)"/>
  <line x1="786" y1="368" x2="786" y2="420" stroke="#5F6368" stroke-width="2.2" marker-end="url(#arrowDark)"/>
  <line x1="704" y1="465" x2="664" y2="465" stroke="#5F6368" stroke-width="2.2"/>
  <line x1="664" y1="465" x2="664" y2="483" stroke="#5F6368" stroke-width="2.2"/>
  <line x1="664" y1="483" x2="664" y2="483" stroke="#5F6368" stroke-width="2.2" marker-end="url(#arrowDark)"/>
  <line x1="868" y1="465" x2="930" y2="465" stroke="#5F6368" stroke-width="2.2" marker-end="url(#arrowDark)"/>
  <line x1="1005" y1="420" x2="1005" y2="368" stroke="#5F6368" stroke-width="2.2" stroke-dasharray="6 6" marker-end="url(#arrowDark)"/>
</svg>
```

## Avoid in this skill
- ❌ Do not use `marker-end` on `<path>` elbow connectors; arrowheads may disappear. Use separate `<line>` segments and put `marker-end` directly on the final `<line>`.
- ❌ Do not rely on auto-routed connectors; SVG should explicitly place each connector segment so the PowerPoint result remains editable and predictable.
- ❌ Do not apply filters to `<line>` connectors; shadows and glows should be limited to cards, containers, paths, or text.
- ❌ Do not create text without a `width` attribute; architecture labels are especially prone to clipping in PowerPoint.
- ❌ Do not overfill containers with nodes; the nested boundary system needs whitespace to remain legible.

## Composition notes
- Keep the outer provider/project container large and calm; it should frame the system, not compete with service cards.
- Reserve the far left for external actors, the middle for ingress and compute, and the right side for durable data and security dependencies.
- Use dashed borders for conceptual or administrative boundaries, and solid tinted fills for active network/runtime boundaries.
- Use color rhythm consistently: blue for traffic/compute, green for data, amber for messaging, red for secrets or security-sensitive services.