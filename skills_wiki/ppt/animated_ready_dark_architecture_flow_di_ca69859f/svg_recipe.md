# SVG Recipe — Animated-Ready Dark Architecture Flow Diagram

## Visual mechanism
A dark, nested cloud-architecture topology uses thin neon boundary strokes and dashed route paths to make infrastructure feel stable while bright orange “payload tokens” become obvious animation targets. The slide is built so the dashed paths are the visual rails and the tokens can later receive PowerPoint motion-path animations.

## SVG primitives needed
- 1× `<rect>` for the full dark background with a subtle gradient fill
- 2–3× large rounded `<rect>` elements for nested architecture boundaries such as Region, VPC, and Subnet
- 5× dark filled rounded `<rect>` cards for infrastructure nodes/services
- Multiple `<text>` elements with explicit `width` for the title, boundary labels, node labels, and animation instructions
- 4× dashed `<path>` connectors for elbow-style network routes
- 4× small filled `<path>` arrowheads placed manually at route ends
- 5× orange `<circle>` / `<rect>` payload tokens positioned on the dashed paths as motion-animation handles
- Several small `<path>`, `<circle>`, and `<line>` details for service icons, status LEDs, and background topology texture
- 1× `<linearGradient>` for the dark background
- 2× `<linearGradient>` fills for cards and boundary label chips
- 1× `<filter id="cardShadow">` for soft elevation on node cards
- 1× `<filter id="tokenGlow">` for high-contrast glowing data tokens

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1280" y2="720">
      <stop offset="0%" stop-color="#111827"/>
      <stop offset="55%" stop-color="#182233"/>
      <stop offset="100%" stop-color="#232F3E"/>
    </linearGradient>
    <linearGradient id="nodeGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#334155"/>
      <stop offset="100%" stop-color="#1E293B"/>
    </linearGradient>
    <linearGradient id="chipGrad" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#0F172A"/>
      <stop offset="100%" stop-color="#1E293B"/>
    </linearGradient>
    <filter id="cardShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="10"/>
      <feGaussianBlur stdDeviation="12"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="tokenGlow" x="-120%" y="-120%" width="340%" height="340%">
      <feGaussianBlur stdDeviation="7" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>

  <!-- subtle dark-mode topology texture -->
  <path d="M72 132 H238 V206 H326" fill="none" stroke="#3B4B63" stroke-width="1" opacity="0.22" stroke-dasharray="4 9"/>
  <path d="M1022 96 H1140 V182 H1210" fill="none" stroke="#3B4B63" stroke-width="1" opacity="0.20" stroke-dasharray="4 9"/>
  <path d="M80 650 H270 V592 H384" fill="none" stroke="#3B4B63" stroke-width="1" opacity="0.18" stroke-dasharray="4 9"/>
  <circle cx="238" cy="206" r="3" fill="#64748B" opacity="0.45"/>
  <circle cx="1140" cy="182" r="3" fill="#64748B" opacity="0.45"/>
  <circle cx="270" cy="592" r="3" fill="#64748B" opacity="0.45"/>

  <text x="52" y="62" width="760" font-family="Segoe UI, Microsoft YaHei" font-size="31" font-weight="700" fill="#FFFFFF">Cloud Architecture Data Flow</text>
  <text x="54" y="94" width="760" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#A7B4C7">Static infrastructure stays readable; orange tokens are positioned for PowerPoint motion-path animation.</text>

  <rect x="1010" y="45" width="210" height="42" rx="21" fill="#0B1220" stroke="#475569" stroke-width="1"/>
  <circle cx="1035" cy="66" r="7" fill="#FF9900" filter="url(#tokenGlow)"/>
  <text x="1052" y="71" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="600" fill="#CBD5E1">Animated payload</text>

  <!-- nested cloud boundaries -->
  <rect x="72" y="130" width="1136" height="526" rx="26" fill="none" stroke="#7AA33E" stroke-width="2.5"/>
  <rect x="92" y="113" width="235" height="34" rx="17" fill="url(#chipGrad)" stroke="#7AA33E" stroke-width="1"/>
  <text x="111" y="136" width="190" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#9FD66A">AWS Region: us-east-1</text>

  <rect x="118" y="178" width="1044" height="430" rx="22" fill="none" stroke="#3F8624" stroke-width="2.5"/>
  <rect x="138" y="161" width="225" height="34" rx="17" fill="#101A25" stroke="#3F8624" stroke-width="1"/>
  <text x="157" y="184" width="180" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#73C84E">Virtual Private Cloud</text>

  <rect x="160" y="238" width="948" height="306" rx="20" fill="rgba(0,124,182,0.04)" stroke="#007CB6" stroke-width="2.5"/>
  <rect x="180" y="221" width="180" height="34" rx="17" fill="#101A25" stroke="#007CB6" stroke-width="1"/>
  <text x="199" y="244" width="140" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#4FC3F7">Public Subnet</text>

  <!-- node cards -->
  <rect x="206" y="384" width="190" height="112" rx="14" fill="url(#nodeGrad)" stroke="#CBD5E1" stroke-width="1.2" filter="url(#cardShadow)"/>
  <rect x="206" y="384" width="190" height="7" rx="3.5" fill="#60A5FA"/>
  <circle cx="236" cy="426" r="15" fill="#0F172A" stroke="#60A5FA" stroke-width="1.4"/>
  <path d="M226 426 h20 M236 416 v20" stroke="#60A5FA" stroke-width="2" fill="none"/>
  <text x="260" y="425" width="110" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#FFFFFF">Client</text>
  <text x="260" y="449" width="115" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#CBD5E1">Local repo / CLI</text>

  <rect x="535" y="286" width="210" height="122" rx="14" fill="url(#nodeGrad)" stroke="#E2E8F0" stroke-width="1.2" filter="url(#cardShadow)"/>
  <rect x="535" y="286" width="210" height="7" rx="3.5" fill="#F59E0B"/>
  <circle cx="570" cy="332" r="17" fill="#0F172A" stroke="#F59E0B" stroke-width="1.5"/>
  <path d="M562 333 c8 -14 24 -5 13 7 c-5 6 -15 8 -21 1 c-8 -9 1 -21 12 -20" fill="none" stroke="#F59E0B" stroke-width="2"/>
  <text x="600" y="327" width="120" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#FFFFFF">Automation</text>
  <text x="600" y="351" width="120" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#CBD5E1">Build + deploy runner</text>

  <rect x="866" y="384" width="190" height="112" rx="14" fill="url(#nodeGrad)" stroke="#CBD5E1" stroke-width="1.2" filter="url(#cardShadow)"/>
  <rect x="866" y="384" width="190" height="7" rx="3.5" fill="#22C55E"/>
  <circle cx="896" cy="426" r="15" fill="#0F172A" stroke="#22C55E" stroke-width="1.4"/>
  <rect x="887" y="417" width="18" height="18" rx="3" fill="none" stroke="#22C55E" stroke-width="2"/>
  <line x1="891" y1="423" x2="901" y2="423" stroke="#22C55E" stroke-width="2"/>
  <line x1="891" y1="429" x2="901" y2="429" stroke="#22C55E" stroke-width="2"/>
  <text x="920" y="425" width="110" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#FFFFFF">Target Node</text>
  <text x="920" y="449" width="115" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#CBD5E1">App server / host</text>

  <rect x="535" y="492" width="210" height="78" rx="14" fill="#172033" stroke="#64748B" stroke-width="1"/>
  <circle cx="570" cy="531" r="12" fill="#0F172A" stroke="#94A3B8" stroke-width="1.3"/>
  <path d="M562 531 h16 M570 523 v16" stroke="#94A3B8" stroke-width="1.7"/>
  <text x="596" y="526" width="125" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#E2E8F0">Artifact Store</text>
  <text x="596" y="548" width="125" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#94A3B8">Package cache</text>

  <rect x="535" y="186" width="210" height="62" rx="14" fill="#172033" stroke="#64748B" stroke-width="1"/>
  <circle cx="570" cy="217" r="11" fill="#0F172A" stroke="#A78BFA" stroke-width="1.3"/>
  <path d="M563 217 h14 M570 210 v14" stroke="#A78BFA" stroke-width="1.6"/>
  <text x="596" y="213" width="130" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#E2E8F0">Control Plane</text>
  <text x="596" y="234" width="130" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#94A3B8">Policy + audit</text>

  <!-- dashed routes: leave these visually traceable for PPT motion paths -->
  <path d="M396 440 H466 Q486 440 486 420 V360 Q486 347 499 347 H535" fill="none" stroke="#E5E7EB" stroke-width="2.2" stroke-dasharray="10 8" opacity="0.92"/>
  <path d="M745 347 H800 Q820 347 820 367 V420 Q820 440 840 440 H866" fill="none" stroke="#E5E7EB" stroke-width="2.2" stroke-dasharray="10 8" opacity="0.92"/>
  <path d="M640 408 V462 Q640 480 640 492" fill="none" stroke="#94A3B8" stroke-width="1.9" stroke-dasharray="7 7" opacity="0.82"/>
  <path d="M640 286 V265 Q640 248 640 248" fill="none" stroke="#94A3B8" stroke-width="1.9" stroke-dasharray="7 7" opacity="0.82"/>

  <!-- manual arrowheads, not SVG markers -->
  <path d="M526 338 L542 347 L526 356 Z" fill="#E5E7EB"/>
  <path d="M856 431 L872 440 L856 449 Z" fill="#E5E7EB"/>
  <path d="M632 480 L640 497 L648 480 Z" fill="#94A3B8"/>
  <path d="M632 262 L640 245 L648 262 Z" fill="#94A3B8"/>

  <!-- high-contrast animated payload tokens -->
  <circle id="payload-01" cx="450" cy="440" r="9" fill="#FF9900" filter="url(#tokenGlow)"/>
  <rect id="payload-02" x="602" y="338" width="18" height="18" rx="4" fill="#FF9900" filter="url(#tokenGlow)"/>
  <circle id="payload-03" cx="810" cy="396" r="9" fill="#FF9900" filter="url(#tokenGlow)"/>
  <rect id="payload-04" x="631" y="456" width="18" height="18" rx="4" fill="#FF9900" filter="url(#tokenGlow)"/>
  <circle id="payload-05" cx="640" cy="266" r="8" fill="#FF9900" filter="url(#tokenGlow)"/>

  <rect x="830" y="588" width="300" height="42" rx="12" fill="#0B1220" stroke="#334155" stroke-width="1"/>
  <text x="850" y="614" width="260" font-family="Segoe UI, Microsoft YaHei" font-size="12.5" fill="#CBD5E1">Tip: animate each orange token along the nearest dashed route with PowerPoint’s motion path tool.</text>
</svg>
```

## Avoid in this skill
- ❌ Do not use `<animate>` or `<animateTransform>`; create animation-ready tokens visually, then apply native PowerPoint motion paths later.
- ❌ Do not use `marker-end` on `<path>` connectors; arrowheads should be separate small filled `<path>` triangles.
- ❌ Do not put filters on `<line>` elements; apply glow only to token circles/rectangles or shadows to node rectangles.
- ❌ Do not rely on transparent masks for boundary overlays; use transparent fills and colored strokes instead.
- ❌ Do not create a crowded grid of equal boxes; the technique needs nested boundaries, hierarchy, and a clear route narrative.

## Composition notes
- Keep the diagram centered inside a large nested boundary system; reserve the top 100 px for title, subtitle, and legend.
- Use thin, bright boundary strokes on a deep blue-gray background so the infrastructure reads as stable and technical.
- Put orange payload tokens directly on dashed routes, not inside node cards, so presenters can easily select and animate them.
- Maintain high negative space between service cards; the dashed path geometry should be traceable by eye before any animation is added.