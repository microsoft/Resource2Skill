# SVG Recipe — Modular Technical Architecture Layout

## Visual mechanism
A modular technical architecture diagram turns an abstract system into stacked logical zones, with colored component cards placed on a strict grid and connected by directional flow arrows. The premium look comes from soft layer panels, subtle shadows, restrained gradients, and clear visual categorization for UI, service, integration, and data components.

## SVG primitives needed
- 3× large `<rect>` for horizontal architecture zones / swimlanes
- 8× `<rect>` for service/component modules, badges, and small status pills
- 4× `<path>` for database-cylinder bodies and subtle decorative circuit traces
- 4× `<ellipse>` for cylinder tops/bottoms and small hub accents
- 7× `<line>` for straight directional connectors with arrowheads
- 1× `<marker>` definition for triangular arrowheads applied directly to each connector `<line>`
- 3× `<linearGradient>` for background, blue UI nodes, and green service nodes
- 1× `<radialGradient>` for the soft architecture focus glow
- 1× `<filter id="cardShadow">` applied to nodes and cylinders
- Multiple `<text>` elements with explicit `width` attributes for titles, layer labels, module names, and technology captions

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#F8FAFC"/>
      <stop offset="100%" stop-color="#EEF3F8"/>
    </linearGradient>
    <radialGradient id="focusGlow" cx="50%" cy="44%" r="58%">
      <stop offset="0%" stop-color="#DDEBFF" stop-opacity="0.75"/>
      <stop offset="100%" stop-color="#DDEBFF" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="uiBlue" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#37A8F4"/>
      <stop offset="100%" stop-color="#246BFD"/>
    </linearGradient>
    <linearGradient id="svcGreen" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#35D48B"/>
      <stop offset="100%" stop-color="#16A765"/>
    </linearGradient>
    <linearGradient id="dataPurple" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#A86BF2"/>
      <stop offset="100%" stop-color="#7B3FC8"/>
    </linearGradient>
    <filter id="cardShadow" x="-20%" y="-25%" width="140%" height="160%">
      <feOffset dx="0" dy="8"/>
      <feGaussianBlur stdDeviation="10"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <marker id="arrow" markerWidth="12" markerHeight="12" refX="10" refY="6" orient="auto">
      <path d="M2,2 L10,6 L2,10 Z" fill="#506070"/>
    </marker>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>
  <ellipse cx="660" cy="360" rx="520" ry="250" fill="url(#focusGlow)"/>

  <text x="58" y="58" width="760" font-family="Segoe UI, Microsoft YaHei" font-size="28" font-weight="700" fill="#263241">ENTERPRISE SYSTEM ARCHITECTURE</text>
  <text x="60" y="86" width="690" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#748193">Logical topology, runtime boundaries, and principal data flows</text>
  <rect x="1010" y="42" width="190" height="32" rx="16" fill="#EAF1F9" stroke="#D5E0EC"/>
  <text x="1034" y="64" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#607086">REFERENCE MODEL</text>

  <path d="M100 145 C180 118, 222 120, 310 142" fill="none" stroke="#D4DDE8" stroke-width="2" stroke-dasharray="6 8"/>
  <path d="M1020 615 C1095 590, 1124 545, 1182 520" fill="none" stroke="#D4DDE8" stroke-width="2" stroke-dasharray="6 8"/>

  <rect x="58" y="125" width="1164" height="150" rx="26" fill="#F7F9FC" stroke="#DDE5EF"/>
  <rect x="58" y="310" width="1164" height="150" rx="26" fill="#F7F9FC" stroke="#DDE5EF"/>
  <rect x="58" y="495" width="1164" height="150" rx="26" fill="#F7F9FC" stroke="#DDE5EF"/>

  <text x="82" y="153" width="210" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#8B97A7">PRESENTATION LAYER</text>
  <text x="82" y="338" width="210" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#8B97A7">APPLICATION & SERVICE LAYER</text>
  <text x="82" y="523" width="210" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#8B97A7">DATA ACCESS LAYER</text>

  <line x1="360" y1="222" x2="550" y2="345" stroke="#506070" stroke-width="2.5" marker-end="url(#arrow)"/>
  <line x1="920" y1="222" x2="730" y2="345" stroke="#506070" stroke-width="2.5" marker-end="url(#arrow)"/>
  <line x1="640" y1="408" x2="640" y2="520" stroke="#506070" stroke-width="2.5" marker-end="url(#arrow)"/>
  <line x1="565" y1="408" x2="360" y2="530" stroke="#506070" stroke-width="2.5" marker-end="url(#arrow)"/>
  <line x1="715" y1="408" x2="920" y2="530" stroke="#506070" stroke-width="2.5" marker-end="url(#arrow)"/>
  <line x1="478" y1="385" x2="548" y2="385" stroke="#506070" stroke-width="2.5" marker-end="url(#arrow)"/>
  <line x1="732" y1="385" x2="802" y2="385" stroke="#506070" stroke-width="2.5" marker-end="url(#arrow)"/>

  <rect x="235" y="160" width="250" height="84" rx="18" fill="url(#uiBlue)" filter="url(#cardShadow)"/>
  <text x="262" y="193" width="196" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#FFFFFF">Web Client</text>
  <text x="262" y="218" width="196" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#DCEEFF">React · Browser SPA</text>

  <rect x="795" y="160" width="250" height="84" rx="18" fill="url(#uiBlue)" filter="url(#cardShadow)"/>
  <text x="822" y="193" width="196" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#FFFFFF">Mobile App</text>
  <text x="822" y="218" width="196" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#DCEEFF">Flutter · iOS / Android</text>

  <rect x="548" y="342" width="184" height="86" rx="16" fill="url(#svcGreen)" filter="url(#cardShadow)"/>
  <text x="572" y="375" width="136" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#FFFFFF">API Gateway</text>
  <text x="572" y="400" width="136" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#DDF8EA">REST · Auth · Routing</text>

  <rect x="295" y="346" width="182" height="78" rx="16" fill="#1E293B" filter="url(#cardShadow)"/>
  <text x="320" y="378" width="132" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="700" fill="#FFFFFF">Identity Svc</text>
  <text x="320" y="401" width="132" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#B9C6D8">OIDC · RBAC</text>

  <rect x="803" y="346" width="182" height="78" rx="16" fill="#1E293B" filter="url(#cardShadow)"/>
  <text x="828" y="378" width="132" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="700" fill="#FFFFFF">Event Bus</text>
  <text x="828" y="401" width="132" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#B9C6D8">Kafka · Async I/O</text>

  <path d="M250 548 C250 530, 470 530, 470 548 L470 600 C470 618, 250 618, 250 600 Z" fill="url(#dataPurple)" filter="url(#cardShadow)"/>
  <ellipse cx="360" cy="548" rx="110" ry="20" fill="#B98BFA"/>
  <ellipse cx="360" cy="600" rx="110" ry="20" fill="#6E35B8"/>
  <text x="286" y="573" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="700" fill="#FFFFFF" text-anchor="middle">User Profiles</text>
  <text x="286" y="596" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#E9DDFB" text-anchor="middle">PostgreSQL</text>

  <path d="M810 548 C810 530, 1030 530, 1030 548 L1030 600 C1030 618, 810 618, 810 600 Z" fill="url(#dataPurple)" filter="url(#cardShadow)"/>
  <ellipse cx="920" cy="548" rx="110" ry="20" fill="#B98BFA"/>
  <ellipse cx="920" cy="600" rx="110" ry="20" fill="#6E35B8"/>
  <text x="846" y="573" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="700" fill="#FFFFFF" text-anchor="middle">Transaction Ledger</text>
  <text x="846" y="596" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#E9DDFB" text-anchor="middle">MongoDB Cluster</text>

  <circle cx="640" cy="385" r="7" fill="#FFFFFF" stroke="#16A765" stroke-width="3"/>
  <circle cx="386" cy="385" r="5" fill="#65D39C"/>
  <circle cx="894" cy="385" r="5" fill="#65D39C"/>
</svg>
```

## Avoid in this skill
- ❌ Curved connector `<path>` arrows with `marker-end`; arrowheads may disappear. Use straight `<line>` connectors and apply `marker-end` directly to each line.
- ❌ Putting `marker-end` on a parent `<g>` and expecting child connectors to inherit it.
- ❌ Filters on connector `<line>` elements; keep shadows on nodes, panels, paths, or text only.
- ❌ Overcrowding each swimlane with too many modules; the technique works because the hierarchy remains instantly scannable.
- ❌ Using clip paths or masks for normal architecture boxes; reserve clipping for actual images only.

## Composition notes
- Keep title and metadata in the top 10–15% of the canvas; reserve the central area for the architecture model.
- Use wide horizontal layer panels spanning roughly 90% of slide width to establish system boundaries.
- Place connectors underneath nodes in the visual stack so arrows feel integrated, not pasted on top.
- Limit the palette to one color per logical category: blue for clients, green for services, purple for data, charcoal for security/integration utilities.