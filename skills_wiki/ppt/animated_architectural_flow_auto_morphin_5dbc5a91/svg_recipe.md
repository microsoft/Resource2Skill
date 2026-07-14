# SVG Recipe — Animated Architectural Flow (Auto-Morphing)

## Visual mechanism
A dark, high-contrast architecture diagram is kept static while a small neon “data packet” orb appears at a different point along the system path on each duplicated slide. PowerPoint Morph then interpolates the orb’s position, creating a cinematic flow animation without timeline-based animation.

## SVG primitives needed
- 1× `<rect>` for the full-slide cosmic gradient background
- 1× `<radialGradient>` and 1× `<linearGradient>` for the premium dark/teal atmosphere
- 2× `<filter>` definitions: one soft shadow for cards/text, one Gaussian blur glow for active packets
- 1× `<rect>` for the main architecture canvas/frame
- 6× `<rect>` for grouped cloud zones, availability zones, and subnet containers
- 8× `<rect>` for service nodes such as Client, DNS, CDN, Load Balancer, Compute, Queue, Database, Observability
- 12× `<line>` for orthogonal architecture connections and flow rails
- 10× `<circle>` for packet checkpoints, glowing current packet, and small junction highlights
- 10× `<text>` blocks with explicit `width` attributes for labels and slide guidance
- 4× `<path>` for decorative service icons, a white hand-drawn flow arrow, and a Terraform-like cube mark
- 1× `<image>` optional background texture/photo on the right panel, clipped by a rounded rectangle if desired

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#070B1A"/>
      <stop offset="52%" stop-color="#17102D"/>
      <stop offset="100%" stop-color="#05353B"/>
    </linearGradient>
    <radialGradient id="aura" cx="72%" cy="38%" r="58%">
      <stop offset="0%" stop-color="#2DF7FF" stop-opacity="0.42"/>
      <stop offset="45%" stop-color="#6A37FF" stop-opacity="0.16"/>
      <stop offset="100%" stop-color="#000000" stop-opacity="0"/>
    </radialGradient>
    <filter id="shadow" x="-30%" y="-30%" width="160%" height="160%">
      <feOffset dx="0" dy="8"/>
      <feGaussianBlur stdDeviation="8"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="packetGlow" x="-180%" y="-180%" width="460%" height="460%">
      <feGaussianBlur stdDeviation="10" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <clipPath id="rightPhotoClip">
      <rect x="630" y="0" width="650" height="720" rx="0"/>
    </clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>
  <rect x="0" y="0" width="1280" height="720" fill="url(#aura)"/>
  <image href="https://images.example.com/teal-mountain-cloud-texture.jpg" x="630" y="0" width="650" height="720" opacity="0.28" clip-path="url(#rightPhotoClip)"/>

  <rect x="32" y="48" width="560" height="624" rx="8" fill="#080B19" stroke="#94A3B8" stroke-opacity="0.55" stroke-width="2" filter="url(#shadow)"/>
  <text x="56" y="82" width="210" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#FFFFFF" font-weight="700">AWS Cloud</text>
  <text x="56" y="118" width="250" font-family="Segoe UI, Microsoft YaHei" font-size="28" fill="#FFFFFF" opacity="0.16" font-weight="700">architecture</text>

  <rect x="72" y="220" width="475" height="400" rx="4" fill="#130A2B" stroke="#8B5CF6" stroke-width="2" opacity="0.78"/>
  <text x="86" y="248" width="230" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#D8B4FE">Virtual private cloud / production VPC</text>

  <rect x="92" y="262" width="170" height="120" rx="2" fill="#071725" stroke="#22D3EE" stroke-width="1.5"/>
  <rect x="92" y="426" width="170" height="120" rx="2" fill="#071725" stroke="#22D3EE" stroke-width="1.5"/>
  <rect x="357" y="262" width="170" height="120" rx="2" fill="#071725" stroke="#22D3EE" stroke-width="1.5"/>
  <rect x="357" y="426" width="170" height="120" rx="2" fill="#071725" stroke="#22D3EE" stroke-width="1.5"/>

  <rect x="113" y="296" width="118" height="48" rx="8" fill="#271149" stroke="#A78BFA" stroke-width="1.5"/>
  <text x="126" y="326" width="95" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#FFFFFF">NAT gateway</text>
  <rect x="113" y="462" width="118" height="48" rx="8" fill="#3B1605" stroke="#FB923C" stroke-width="1.5"/>
  <text x="128" y="491" width="92" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#FFFFFF">EC2 service</text>
  <rect x="380" y="462" width="118" height="48" rx="8" fill="#3B1605" stroke="#FB923C" stroke-width="1.5"/>
  <text x="396" y="491" width="90" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#FFFFFF">EC2 worker</text>
  <rect x="113" y="568" width="118" height="48" rx="8" fill="#2B0B4F" stroke="#E879F9" stroke-width="1.5"/>
  <text x="130" y="598" width="86" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#FFFFFF">RDS primary</text>
  <rect x="380" y="568" width="118" height="48" rx="8" fill="#2B0B4F" stroke="#E879F9" stroke-width="1.5"/>
  <text x="398" y="598" width="84" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#FFFFFF">RDS replica</text>

  <rect x="252" y="86" width="56" height="40" rx="7" fill="#3B1C85" stroke="#A78BFA" stroke-width="1.5"/>
  <text x="225" y="72" width="125" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#C4B5FD">app.example.com</text>
  <text x="258" y="111" width="46" font-family="Segoe UI, Microsoft YaHei" font-size="10" fill="#FFFFFF">Route 53</text>
  <rect x="252" y="164" width="56" height="40" rx="7" fill="#312E81" stroke="#60A5FA" stroke-width="1.5"/>
  <text x="244" y="191" width="72" font-family="Segoe UI, Microsoft YaHei" font-size="10" fill="#FFFFFF">CloudFront</text>
  <rect x="252" y="274" width="56" height="40" rx="7" fill="#4C1D95" stroke="#C084FC" stroke-width="1.5"/>
  <text x="238" y="301" width="86" font-family="Segoe UI, Microsoft YaHei" font-size="10" fill="#FFFFFF">Load balancer</text>
  <rect x="252" y="422" width="56" height="40" rx="7" fill="#B45309" stroke="#FDBA74" stroke-width="1.5"/>
  <text x="248" y="448" width="70" font-family="Segoe UI, Microsoft YaHei" font-size="10" fill="#FFFFFF">Auto Scale</text>

  <line x1="280" y1="126" x2="280" y2="164" stroke="#8B5CF6" stroke-width="2"/>
  <line x1="280" y1="204" x2="280" y2="274" stroke="#8B5CF6" stroke-width="2"/>
  <line x1="280" y1="314" x2="280" y2="422" stroke="#8B5CF6" stroke-width="2"/>
  <line x1="280" y1="442" x2="172" y2="442" stroke="#22D3EE" stroke-width="2"/>
  <line x1="280" y1="442" x2="439" y2="442" stroke="#22D3EE" stroke-width="2"/>
  <line x1="172" y1="510" x2="172" y2="568" stroke="#A78BFA" stroke-width="2"/>
  <line x1="439" y1="510" x2="439" y2="568" stroke="#A78BFA" stroke-width="2"/>
  <line x1="172" y1="616" x2="439" y2="616" stroke="#64748B" stroke-width="1.5" stroke-dasharray="7 7"/>

  <circle cx="280" cy="106" r="4" fill="#E0E7FF"/>
  <circle cx="280" cy="184" r="4" fill="#C084FC"/>
  <circle cx="280" cy="294" r="4" fill="#C084FC"/>
  <circle cx="280" cy="442" r="4" fill="#22D3EE"/>
  <circle cx="172" cy="442" r="4" fill="#22D3EE"/>
  <circle cx="439" cy="442" r="4" fill="#22D3EE"/>
  <circle cx="172" cy="568" r="4" fill="#E879F9"/>
  <circle cx="439" cy="568" r="4" fill="#E879F9"/>

  <circle id="packet_slide_04_same_name_each_slide" cx="439" cy="442" r="10" fill="#FFD84D" filter="url(#packetGlow)"/>
  <circle cx="421" cy="442" r="5" fill="#A78BFA" opacity="0.65" filter="url(#packetGlow)"/>
  <circle cx="395" cy="442" r="3.5" fill="#60A5FA" opacity="0.45" filter="url(#packetGlow)"/>

  <rect x="618" y="214" width="116" height="116" rx="2" fill="#050816" stroke="#FFFFFF" stroke-opacity="0.5"/>
  <path d="M674 236 L715 259 L674 282 L633 259 Z M633 268 L674 292 L674 326 L633 302 Z M715 268 L674 292 L674 326 L715 302 Z" fill="#7C3AED"/>
  <path d="M585 338 C545 286 500 262 453 286 C431 297 423 317 441 329 C464 345 522 313 498 300 C475 287 421 303 361 334" fill="none" stroke="#FFFFFF" stroke-width="10" stroke-linecap="round" stroke-linejoin="round" filter="url(#shadow)"/>

  <text x="960" y="88" width="260" font-family="Segoe UI, Microsoft YaHei" font-size="74" fill="#FFFFFF" font-weight="900" text-anchor="middle" filter="url(#shadow)">create</text>
  <text x="930" y="214" width="520" font-family="Segoe UI, Microsoft YaHei" font-size="96" fill="#FFD84D" font-weight="900" text-anchor="middle" filter="url(#shadow)">ANIMATED</text>
  <text x="925" y="374" width="610" font-family="Segoe UI, Microsoft YaHei" font-size="92" fill="#FFFFFF" font-weight="900" text-anchor="middle" filter="url(#shadow)">DIAGRAMS</text>
  <text x="934" y="514" width="440" font-family="Segoe UI, Microsoft YaHei" font-size="66" fill="#FFFFFF" font-weight="900" text-anchor="middle" filter="url(#shadow)">in minutes</text>

  <rect x="690" y="604" width="455" height="52" rx="26" fill="#000000" opacity="0.34"/>
  <text x="720" y="638" width="400" font-family="Segoe UI, Microsoft YaHei" font-size="20" fill="#DFFBFF" font-weight="600">Duplicate slide → move packet → apply Morph, 0.4–0.6s auto advance</text>
</svg>
```

## Avoid in this skill
- ❌ Do not use SVG `<animate>` or `<animateTransform>`; the motion should be created by duplicated PowerPoint slides plus Morph, not embedded SVG animation.
- ❌ Do not apply `filter` to `<line>` connectors; PowerPoint translation may drop line filters. Use glowing circles at junctions instead.
- ❌ Do not use `<mask>` or clip non-image objects for packet trails; build trails from editable circles with opacity.
- ❌ Do not use `<use>`/`<symbol>` for repeated nodes or icons; duplicate the editable shapes directly so Morph can track them reliably.
- ❌ Do not rely on `marker-end` on `<path>` arrows; use visible stroked paths for decorative arrows or `<line>` with direct marker settings only if necessary.

## Composition notes
- Keep the architecture diagram locked to the left 45–50% of the canvas; it should feel like a technical artifact, dense but readable.
- Use one bright packet color per narrative path, typically yellow/cyan/purple, and keep all static infrastructure muted.
- For Morph, duplicate the slide and move only the packet circle/trail group; keep every static shape in exactly the same position.
- In PowerPoint, give the moving packet shape the same object name on every slide, ideally prefixed with `!!`, so Morph treats it as the same object.