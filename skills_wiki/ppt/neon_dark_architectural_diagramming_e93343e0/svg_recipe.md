# SVG Recipe — Neon-Dark Architectural Diagramming

## Visual mechanism
A deep charcoal technical canvas uses neon-filled rounded nodes, glowing duplicate layers, and clean data-flow lines to turn a standard architecture diagram into a premium dark-mode keynote visual. Logic tiers are separated vertically, with cyan for entry/routing, orange for services, green for data, and purple for async/event infrastructure.

## SVG primitives needed
- 1× `<rect>` for the full-slide charcoal background.
- 1× `<rect>` for a dashed rounded “system boundary” container.
- 12–16× `<rect>` for neon service nodes, including blurred glow duplicates behind crisp foreground nodes.
- 8–14× `<line>` for grid accents and data-flow connectors.
- 12–18× `<path>` for arrowhead triangles, decorative circuit traces, and database cylinder bodies.
- 6× `<ellipse>` for database cylinder tops, including glow and crisp layers.
- 2× `<circle>` with radial gradients for large ambient color halos in the background.
- 3× `<radialGradient>` for soft background color blooms.
- 3× `<filter>` using `feGaussianBlur` for cyan, orange, purple, and green neon auras on shapes.
- 1× `<filter>` using `feOffset + feGaussianBlur + feMerge` for subtle depth shadows on node cards.
- Multiple `<text>` elements with explicit `width` attributes for title, labels, and node names.

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <radialGradient id="cyanHalo" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#00D4FF" stop-opacity="0.22"/>
      <stop offset="70%" stop-color="#00D4FF" stop-opacity="0.04"/>
      <stop offset="100%" stop-color="#00D4FF" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="orangeHalo" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#FF9900" stop-opacity="0.16"/>
      <stop offset="75%" stop-color="#FF9900" stop-opacity="0.03"/>
      <stop offset="100%" stop-color="#FF9900" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="greenHalo" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#00DC78" stop-opacity="0.16"/>
      <stop offset="75%" stop-color="#00DC78" stop-opacity="0.03"/>
      <stop offset="100%" stop-color="#00DC78" stop-opacity="0"/>
    </radialGradient>
    <filter id="glowCyan" x="-60%" y="-80%" width="220%" height="260%">
      <feGaussianBlur stdDeviation="9"/>
    </filter>
    <filter id="glowOrange" x="-60%" y="-80%" width="220%" height="260%">
      <feGaussianBlur stdDeviation="8"/>
    </filter>
    <filter id="glowGreen" x="-60%" y="-80%" width="220%" height="260%">
      <feGaussianBlur stdDeviation="9"/>
    </filter>
    <filter id="shadow" x="-30%" y="-40%" width="160%" height="190%">
      <feOffset dx="0" dy="8" result="off"/>
      <feGaussianBlur in="off" stdDeviation="10" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#14161C"/>
  <circle cx="260" cy="145" r="250" fill="url(#cyanHalo)"/>
  <circle cx="1040" cy="540" r="280" fill="url(#greenHalo)"/>
  <circle cx="710" cy="340" r="330" fill="url(#orangeHalo)" opacity="0.75"/>

  <line x1="80" y1="120" x2="1200" y2="120" stroke="#2A2F3A" stroke-width="1"/>
  <line x1="80" y1="240" x2="1200" y2="240" stroke="#242A33" stroke-width="1"/>
  <line x1="80" y1="360" x2="1200" y2="360" stroke="#242A33" stroke-width="1"/>
  <line x1="80" y1="480" x2="1200" y2="480" stroke="#242A33" stroke-width="1"/>
  <line x1="80" y1="600" x2="1200" y2="600" stroke="#242A33" stroke-width="1"/>
  <path d="M98 96 C180 70 240 88 306 130" fill="none" stroke="#00D4FF" stroke-width="2" stroke-opacity="0.22" stroke-dasharray="8 10"/>
  <path d="M1055 110 C1145 168 1130 255 1200 312" fill="none" stroke="#9B5CFF" stroke-width="2" stroke-opacity="0.25" stroke-dasharray="6 9"/>

  <text x="70" y="52" width="640" font-family="Segoe UI, Microsoft YaHei" font-size="30" font-weight="700" fill="#FFFFFF">
    Microservices Architecture
  </text>
  <text x="72" y="80" width="640" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#8E98AA">
    Neon-dark system map: ingress, orchestration, services, events, and persistent stores
  </text>

  <rect x="150" y="136" width="980" height="520" rx="28" fill="none" stroke="#3B4353" stroke-width="1.5" stroke-dasharray="10 8"/>
  <text x="174" y="166" width="190" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#7C879A">
    PRODUCTION VPC
  </text>

  <rect x="530" y="94" width="220" height="54" rx="27" fill="#00D4FF" opacity="0.55" filter="url(#glowCyan)"/>
  <rect x="530" y="94" width="220" height="54" rx="27" fill="#00D4FF" filter="url(#shadow)"/>
  <text x="640" y="128" width="200" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="700" fill="#10141A">
    Client Apps
  </text>

  <line x1="640" y1="148" x2="640" y2="164" stroke="#8D96A8" stroke-width="2"/>
  <path d="M633 164 L647 164 L640 176 Z" fill="#8D96A8"/>

  <rect x="370" y="176" width="540" height="64" rx="24" fill="#00D4FF" opacity="0.58" filter="url(#glowCyan)"/>
  <rect x="370" y="176" width="540" height="64" rx="24" fill="#00D4FF" filter="url(#shadow)"/>
  <text x="640" y="215" width="500" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="19" font-weight="800" fill="#10141A">
    API Gateway / Edge Router
  </text>

  <line x1="640" y1="240" x2="640" y2="280" stroke="#8D96A8" stroke-width="2"/>
  <line x1="272" y1="280" x2="1008" y2="280" stroke="#8D96A8" stroke-width="2"/>
  <line x1="272" y1="280" x2="272" y2="315" stroke="#8D96A8" stroke-width="2"/>
  <line x1="517" y1="280" x2="517" y2="315" stroke="#8D96A8" stroke-width="2"/>
  <line x1="762" y1="280" x2="762" y2="315" stroke="#8D96A8" stroke-width="2"/>
  <line x1="1008" y1="280" x2="1008" y2="315" stroke="#8D96A8" stroke-width="2"/>
  <path d="M265 315 L279 315 L272 326 Z" fill="#8D96A8"/>
  <path d="M510 315 L524 315 L517 326 Z" fill="#8D96A8"/>
  <path d="M755 315 L769 315 L762 326 Z" fill="#8D96A8"/>
  <path d="M1001 315 L1015 315 L1008 326 Z" fill="#8D96A8"/>

  <rect x="190" y="326" width="165" height="72" rx="20" fill="#FF9900" opacity="0.48" filter="url(#glowOrange)"/>
  <rect x="190" y="326" width="165" height="72" rx="20" fill="#FF9900" filter="url(#shadow)"/>
  <text x="272" y="357" width="145" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="800" fill="#18130A">Auth</text>
  <text x="272" y="379" width="145" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#4B2D00">OAuth / SSO</text>

  <rect x="435" y="326" width="165" height="72" rx="20" fill="#FFB000" opacity="0.48" filter="url(#glowOrange)"/>
  <rect x="435" y="326" width="165" height="72" rx="20" fill="#FFB000" filter="url(#shadow)"/>
  <text x="517" y="357" width="145" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="800" fill="#18130A">Orders</text>
  <text x="517" y="379" width="145" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#4B2D00">domain service</text>

  <rect x="680" y="326" width="165" height="72" rx="20" fill="#FF9900" opacity="0.48" filter="url(#glowOrange)"/>
  <rect x="680" y="326" width="165" height="72" rx="20" fill="#FF9900" filter="url(#shadow)"/>
  <text x="762" y="357" width="145" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="800" fill="#18130A">Billing</text>
  <text x="762" y="379" width="145" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#4B2D00">payments API</text>

  <rect x="925" y="326" width="165" height="72" rx="20" fill="#9B5CFF" opacity="0.48" filter="url(#glowCyan)"/>
  <rect x="925" y="326" width="165" height="72" rx="20" fill="#9B5CFF" filter="url(#shadow)"/>
  <text x="1008" y="357" width="145" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="800" fill="#FFFFFF">Notify</text>
  <text x="1008" y="379" width="145" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#E4D9FF">email / push</text>

  <line x1="272" y1="398" x2="355" y2="526" stroke="#697384" stroke-width="2"/>
  <line x1="517" y1="398" x2="640" y2="526" stroke="#697384" stroke-width="2"/>
  <line x1="762" y1="398" x2="640" y2="526" stroke="#697384" stroke-width="2"/>
  <line x1="1008" y1="398" x2="945" y2="526" stroke="#697384" stroke-width="2"/>
  <path d="M349 519 L361 527 L350 534 Z" fill="#697384"/>
  <path d="M634 519 L646 527 L635 534 Z" fill="#697384"/>
  <path d="M646 519 L634 527 L645 534 Z" fill="#697384"/>
  <path d="M938 519 L951 527 L940 535 Z" fill="#697384"/>

  <path d="M260 552 C260 531 450 531 450 552 L450 618 C450 639 260 639 260 618 Z" fill="#00DC78" opacity="0.34" filter="url(#glowGreen)"/>
  <path d="M260 552 C260 531 450 531 450 552 L450 618 C450 639 260 639 260 618 Z" fill="#172820" stroke="#00DC78" stroke-width="2.5"/>
  <ellipse cx="355" cy="552" rx="95" ry="20" fill="#20382C" stroke="#00DC78" stroke-width="2.5"/>
  <path d="M260 618 C260 639 450 639 450 618" fill="none" stroke="#00DC78" stroke-width="2"/>
  <text x="355" y="590" width="160" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="800" fill="#EFFFF7">Identity DB</text>

  <path d="M545 552 C545 531 735 531 735 552 L735 618 C735 639 545 639 545 618 Z" fill="#00DC78" opacity="0.34" filter="url(#glowGreen)"/>
  <path d="M545 552 C545 531 735 531 735 552 L735 618 C735 639 545 639 545 618 Z" fill="#172820" stroke="#00DC78" stroke-width="2.5"/>
  <ellipse cx="640" cy="552" rx="95" ry="20" fill="#20382C" stroke="#00DC78" stroke-width="2.5"/>
  <path d="M545 618 C545 639 735 639 735 618" fill="none" stroke="#00DC78" stroke-width="2"/>
  <text x="640" y="590" width="160" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="800" fill="#EFFFF7">Orders DB</text>

  <path d="M850 552 C850 531 1040 531 1040 552 L1040 618 C1040 639 850 639 850 618 Z" fill="#00DC78" opacity="0.34" filter="url(#glowGreen)"/>
  <path d="M850 552 C850 531 1040 531 1040 552 L1040 618 C1040 639 850 639 850 618 Z" fill="#172820" stroke="#00DC78" stroke-width="2.5"/>
  <ellipse cx="945" cy="552" rx="95" ry="20" fill="#20382C" stroke="#00DC78" stroke-width="2.5"/>
  <path d="M850 618 C850 639 1040 639 1040 618" fill="none" stroke="#00DC78" stroke-width="2"/>
  <text x="945" y="590" width="160" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="800" fill="#EFFFF7">Events Lake</text>
</svg>
```

## Avoid in this skill
- ❌ Applying `filter` directly to `<line>` connectors; line filters are dropped, so use crisp connector lines and glow only the node shapes.
- ❌ Using `marker-end` on `<path>` arrows; draw arrowheads as small filled triangle `<path>` elements instead.
- ❌ Using `<pattern>` for the background grid; use individual low-opacity `<line>` elements for editable PowerPoint output.
- ❌ Using masks or clip paths on diagram nodes for glow; duplicate the shape behind the node and apply `feGaussianBlur`.
- ❌ Overloading the canvas with too many equal-brightness neon colors; reserve the brightest cyan/orange/green for meaningful architecture tiers.

## Composition notes
- Keep the top 15% for title, subtitle, and the single entry/client layer; avoid crowding it with service details.
- Use a vertical hierarchy: ingress at top, gateway beneath, services in the middle, databases at the bottom.
- Neon nodes should sit on a quiet dark field with generous spacing; the glow is most effective when surrounded by negative space.
- Maintain color semantics consistently: cyan for routing, orange for compute/services, green for persistence, and purple for async/event paths.