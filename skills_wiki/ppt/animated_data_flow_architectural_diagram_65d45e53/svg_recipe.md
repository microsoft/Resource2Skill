# SVG Recipe — Animated Data Flow Architectural Diagram

## Visual mechanism
A technical architecture is staged as a clean left-to-right system map, with muted connector routes and a high-contrast glowing “data packet” placed on one route segment. To create the animation in PowerPoint, duplicate the slide several times and move only the packet group along the same connector path so Morph interpolates the request flow.

## SVG primitives needed
- 1× `<rect>` for the off-white canvas background
- 4× `<rect>` for elevated architecture node cards
- 1× `<image>` clipped inside the client card to suggest a real product/app surface
- 1× `<clipPath>` with rounded `<rect>` for the client screenshot crop
- 6× `<line>` for primary and secondary data routes
- 6× `<path>` for custom arrowheads at the end of routes
- 8× `<path>` for node icons, database cylinder surfaces, cloud gateway, and decorative circuit traces
- 4× `<circle>` for the animated data packet, packet glow core, and small endpoint status dots
- 7× `<text>` labels with explicit `width` attributes
- 3× `<linearGradient>` for node fills, packet accent, and background wash
- 1× `<radialGradient>` for the packet halo
- 2× `<filter>` effects: soft card shadow and neon packet glow

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgWash" x1="0" y1="0" x2="1280" y2="720">
      <stop offset="0%" stop-color="#F8FAFC"/>
      <stop offset="58%" stop-color="#F3F7FB"/>
      <stop offset="100%" stop-color="#EAF6FF"/>
    </linearGradient>
    <linearGradient id="nodeFill" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="100%" stop-color="#F1F5F9"/>
    </linearGradient>
    <linearGradient id="packetFill" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#22D3EE"/>
      <stop offset="52%" stop-color="#0EA5E9"/>
      <stop offset="100%" stop-color="#6366F1"/>
    </linearGradient>
    <radialGradient id="packetHalo" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#67E8F9" stop-opacity="0.75"/>
      <stop offset="70%" stop-color="#22D3EE" stop-opacity="0.22"/>
      <stop offset="100%" stop-color="#22D3EE" stop-opacity="0"/>
    </radialGradient>
    <filter id="cardShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="14"/>
      <feGaussianBlur stdDeviation="14"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="packetGlow" x="-120%" y="-120%" width="340%" height="340%">
      <feGaussianBlur stdDeviation="8"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <clipPath id="clientShotClip">
      <rect x="88" y="278" width="120" height="74" rx="16"/>
    </clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgWash)"/>
  <path d="M1015 82 C1092 72 1156 110 1188 168 C1234 251 1186 333 1115 344 C1056 353 1010 322 986 278 C949 211 952 103 1015 82 Z" fill="#DBEAFE" opacity="0.45"/>
  <path d="M65 628 C145 582 235 594 295 655 C230 707 124 716 65 628 Z" fill="#CCFBF1" opacity="0.5"/>

  <text x="72" y="70" width="760" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="700" fill="#172033">Data Flow Through Modern Service Architecture</text>
  <text x="73" y="108" width="620" font-family="Segoe UI, Microsoft YaHei" font-size="16" fill="#64748B">Duplicate this slide and move the glowing packet to create a Morph-based animated request journey.</text>

  <line x1="230" y1="352" x2="394" y2="352" stroke="#CBD5E1" stroke-width="5" stroke-linecap="round"/>
  <path d="M394 352 L377 342 L377 362 Z" fill="#CBD5E1"/>
  <line x1="520" y1="352" x2="684" y2="352" stroke="#CBD5E1" stroke-width="5" stroke-linecap="round"/>
  <path d="M684 352 L667 342 L667 362 Z" fill="#CBD5E1"/>
  <line x1="810" y1="352" x2="974" y2="352" stroke="#CBD5E1" stroke-width="5" stroke-linecap="round"/>
  <path d="M974 352 L957 342 L957 362 Z" fill="#CBD5E1"/>

  <line x1="753" y1="432" x2="753" y2="514" stroke="#94A3B8" stroke-width="3" stroke-dasharray="9 9" stroke-linecap="round"/>
  <path d="M753 514 L743 498 L763 498 Z" fill="#94A3B8"/>
  <line x1="615" y1="550" x2="686" y2="550" stroke="#94A3B8" stroke-width="3" stroke-dasharray="9 9" stroke-linecap="round"/>
  <path d="M686 550 L670 540 L670 560 Z" fill="#94A3B8"/>
  <line x1="888" y1="550" x2="959" y2="550" stroke="#94A3B8" stroke-width="3" stroke-dasharray="9 9" stroke-linecap="round"/>
  <path d="M959 550 L943 540 L943 560 Z" fill="#94A3B8"/>

  <rect x="68" y="228" width="180" height="226" rx="28" fill="url(#nodeFill)" stroke="#E2E8F0" stroke-width="1.5" filter="url(#cardShadow)"/>
  <image href="https://images.example.com/app-dashboard-screenshot-for-client-node.png" x="88" y="278" width="120" height="74" clip-path="url(#clientShotClip)"/>
  <path d="M133 245 L183 245 C191 245 198 252 198 260 L198 370 C198 379 191 386 183 386 L133 386 C124 386 118 379 118 370 L118 260 C118 252 124 245 133 245 Z M143 257 L173 257" fill="none" stroke="#334155" stroke-width="5" stroke-linecap="round"/>
  <circle cx="158" cy="371" r="5" fill="#334155"/>
  <text x="88" y="424" width="140" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" text-anchor="middle" fill="#172033">Client App</text>

  <rect x="392" y="232" width="130" height="240" rx="30" fill="#172033" filter="url(#cardShadow)"/>
  <path d="M435 296 C435 278 450 264 468 264 C486 264 501 278 501 296 C501 314 486 328 468 328 L444 328 L431 341 L433 322 C422 315 416 306 416 296 Z" fill="#38BDF8"/>
  <path d="M440 376 L478 376 M440 400 L493 400 M440 424 L470 424" stroke="#94A3B8" stroke-width="8" stroke-linecap="round"/>
  <text x="414" y="518" width="96" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" text-anchor="middle" fill="#172033">API Gateway</text>

  <rect x="682" y="232" width="130" height="240" rx="30" fill="url(#nodeFill)" stroke="#D8E2EE" stroke-width="1.5" filter="url(#cardShadow)"/>
  <path d="M724 286 C732 265 763 265 771 286 C789 288 800 302 800 318 C800 337 785 350 765 350 L724 350 C703 350 690 337 690 319 C690 303 704 289 724 286 Z" fill="#EEF6FF" stroke="#2563EB" stroke-width="4"/>
  <path d="M717 392 L777 392 M717 416 L777 416 M717 440 L757 440" stroke="#334155" stroke-width="8" stroke-linecap="round"/>
  <text x="704" y="518" width="96" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" text-anchor="middle" fill="#172033">Service Mesh</text>

  <rect x="972" y="232" width="180" height="240" rx="30" fill="#0F172A" filter="url(#cardShadow)"/>
  <ellipse cx="1062" cy="294" rx="58" ry="22" fill="#67E8F9"/>
  <path d="M1004 294 C1004 307 1030 316 1062 316 C1094 316 1120 307 1120 294 L1120 408 C1120 421 1094 430 1062 430 C1030 430 1004 421 1004 408 Z" fill="#164E63"/>
  <ellipse cx="1062" cy="408" rx="58" ry="22" fill="#0891B2"/>
  <path d="M1004 332 C1004 345 1030 354 1062 354 C1094 354 1120 345 1120 332 M1004 370 C1004 383 1030 392 1062 392 C1094 392 1120 383 1120 370" fill="none" stroke="#67E8F9" stroke-width="3" opacity="0.8"/>
  <text x="1002" y="518" width="120" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" text-anchor="middle" fill="#172033">Data Store</text>

  <rect x="570" y="516" width="84" height="68" rx="18" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1.5"/>
  <text x="590" y="557" width="44" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" text-anchor="middle" fill="#475569">Auth</text>
  <rect x="700" y="516" width="106" height="68" rx="18" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1.5"/>
  <text x="723" y="557" width="60" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" text-anchor="middle" fill="#475569">Queue</text>
  <rect x="962" y="516" width="106" height="68" rx="18" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1.5"/>
  <text x="985" y="557" width="60" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" text-anchor="middle" fill="#475569">Cache</text>

  <circle cx="602" cy="352" r="34" fill="url(#packetHalo)" filter="url(#packetGlow)"/>
  <circle cx="602" cy="352" r="15" fill="url(#packetFill)" stroke="#FFFFFF" stroke-width="4"/>
  <path d="M596 347 L608 352 L596 357 Z" fill="#FFFFFF"/>
  <text x="534" y="305" width="136" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" text-anchor="middle" fill="#0EA5E9">REQUEST PACKET</text>

  <circle cx="230" cy="352" r="7" fill="#22C55E"/>
  <circle cx="684" cy="352" r="7" fill="#F59E0B"/>
  <circle cx="974" cy="352" r="7" fill="#22C55E"/>
</svg>
```

## Avoid in this skill
- ❌ SVG `<animate>` or `<animateMotion>` for the packet; PowerPoint will not preserve it. Use multiple slides with Morph instead.
- ❌ `marker-end` on `<path>` connectors; arrowheads may disappear. Draw arrowheads as small triangle `<path>` shapes.
- ❌ Filters on `<line>` routes; line filters are dropped. Put glow only on the packet circles or node cards.
- ❌ `clip-path` on node cards or shapes; use clipping only on `<image>` elements.
- ❌ Dense all-to-all connector webs; motion storytelling works best when the next packet destination is obvious.

## Composition notes
- Keep the architecture nodes horizontally aligned through the visual center, leaving large whitespace above for title/subtitle and below for optional supporting services.
- Use muted gray routes so the cyan/magenta packet becomes the narrative focus.
- For animation, create 4–6 slide states: packet at client, between client/API, at gateway, between gateway/service, at service, at database.
- Maintain identical node and connector positions across all states; only move the packet group so PowerPoint Morph creates a clean continuous flow.