# SVG Recipe — Structured Network Topology Diagram

## Visual mechanism
A technical system is made readable by separating the slide into a large topology canvas and a structured legend, then using a consistent visual language for nodes, links, labels, and connection types. The premium look comes from restrained color coding, soft shadows, gradient node fills, rounded grouping containers, and small interface labels that make the network feel precise without becoming cluttered.

## SVG primitives needed
- 2× large `<rect>` for the main topology canvas and bottom legend panel
- 10–14× small `<rect>` for endpoint devices, label pills, firewall, legend rows, and grouped zones
- 3× `<circle>` for primary router/core nodes
- 8–12× `<line>` for solid Ethernet / serial connectors and small icon details
- 3–5× `<path>` for organic WAN cloud, router glyphs, and the wavy wireless link
- 1× `<linearGradient>` for panel and device fills
- 1× `<radialGradient>` for router node depth
- 1× `<filter id="softShadow">` applied to panels and node shapes, not lines
- Multiple `<text>` elements with explicit `width` attributes for title, component labels, interface labels, and legend entries
- Optional dashed strokes via `stroke-dasharray` for serial or wireless-style links

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="panelFill" x1="0" y1="80" x2="0" y2="560" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#FFFFFF"/>
      <stop offset="1" stop-color="#F7FBF4"/>
    </linearGradient>
    <linearGradient id="deviceFill" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#FFFFFF"/>
      <stop offset="1" stop-color="#ECEFF3"/>
    </linearGradient>
    <linearGradient id="legendFill" x1="0" y1="570" x2="0" y2="705" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#FFFFFF"/>
      <stop offset="1" stop-color="#F4F7FA"/>
    </linearGradient>
    <radialGradient id="routerFill" cx="35%" cy="25%" r="70%">
      <stop offset="0" stop-color="#FFFFFF"/>
      <stop offset="0.52" stop-color="#EEF4FF"/>
      <stop offset="1" stop-color="#D7E4F7"/>
    </radialGradient>
    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="5"/>
      <feGaussianBlur stdDeviation="6"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#FFFFFF"/>
  <text x="640" y="48" width="1100" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="700" fill="#111827">Structured Network Topology</text>
  <text x="640" y="73" width="900" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#64748B">Standardized nodes, coded links, and a self-explanatory legend for complex systems</text>

  <rect x="40" y="92" width="1200" height="455" rx="28" fill="url(#panelFill)" stroke="#92D050" stroke-width="3" filter="url(#softShadow)"/>
  <text x="82" y="125" width="260" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#5B8E2B">PRODUCTION NETWORK MAP</text>

  <path d="M690 171 C695 142 730 132 754 150 C770 123 816 130 828 162 C862 158 886 181 882 212 C905 224 898 263 868 267 L704 267 C668 265 653 228 678 207 C663 189 672 174 690 171 Z" fill="#F3F7FF" stroke="#C7D7FF" stroke-width="2"/>
  <text x="780" y="221" width="190" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#5B6B8A">WAN / CORE</text>

  <line x1="214" y1="190" x2="410" y2="190" stroke="#FF0000" stroke-width="3"/>
  <line x1="490" y1="190" x2="740" y2="250" stroke="#FF0000" stroke-width="3"/>
  <line x1="450" y1="230" x2="450" y2="376" stroke="#FF0000" stroke-width="3"/>
  <line x1="820" y1="250" x2="1002" y2="210" stroke="#FF0000" stroke-width="3"/>
  <line x1="813" y1="282" x2="1018" y2="385" stroke="#FF0000" stroke-width="3" stroke-dasharray="10 8"/>
  <line x1="208" y1="405" x2="390" y2="405" stroke="#FF0000" stroke-width="3"/>
  <line x1="450" y1="434" x2="300" y2="486" stroke="#FF0000" stroke-width="3"/>
  <line x1="450" y1="434" x2="450" y2="484" stroke="#FF0000" stroke-width="3"/>
  <line x1="510" y1="434" x2="610" y2="486" stroke="#FF0000" stroke-width="3"/>
  <line x1="510" y1="405" x2="764" y2="405" stroke="#FF0000" stroke-width="3"/>
  <path d="M150 434 C132 455 168 468 150 490 C132 512 168 520 150 540" fill="none" stroke="#00B0F0" stroke-width="4" stroke-dasharray="8 6"/>

  <rect x="92" y="160" width="122" height="60" rx="12" fill="url(#deviceFill)" stroke="#595959" stroke-width="2" filter="url(#softShadow)"/>
  <rect x="118" y="176" width="68" height="30" rx="4" fill="#EAF0F7" stroke="#7B8794"/>
  <text x="153" y="247" width="120" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#111827">PC-01</text>

  <circle cx="450" cy="190" r="42" fill="url(#routerFill)" stroke="#595959" stroke-width="2.5" filter="url(#softShadow)"/>
  <path d="M426 190 L474 190 M450 166 L450 214 M432 174 L426 190 L432 206 M468 174 L474 190 L468 206" fill="none" stroke="#4B5563" stroke-width="3" stroke-linecap="round"/>
  <text x="450" y="250" width="150" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#111827">Access Router</text>

  <circle cx="780" cy="250" r="42" fill="url(#routerFill)" stroke="#595959" stroke-width="2.5" filter="url(#softShadow)"/>
  <path d="M756 250 L804 250 M780 226 L780 274 M762 234 L756 250 L762 266 M798 234 L804 250 L798 266" fill="none" stroke="#4B5563" stroke-width="3" stroke-linecap="round"/>
  <text x="780" y="310" width="150" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#111827">Internet Router</text>

  <rect x="1002" y="160" width="34" height="100" rx="8" fill="#FFF1F0" stroke="#C2410C" stroke-width="2.5" filter="url(#softShadow)"/>
  <line x1="1008" y1="184" x2="1030" y2="184" stroke="#C2410C" stroke-width="2"/>
  <line x1="1008" y1="210" x2="1030" y2="210" stroke="#C2410C" stroke-width="2"/>
  <line x1="1008" y1="236" x2="1030" y2="236" stroke="#C2410C" stroke-width="2"/>
  <text x="1019" y="282" width="110" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#111827">Firewall</text>

  <circle cx="1050" cy="405" r="42" fill="url(#routerFill)" stroke="#595959" stroke-width="2.5" filter="url(#softShadow)"/>
  <path d="M1026 405 L1074 405 M1050 381 L1050 429 M1032 389 L1026 405 L1032 421 M1068 389 L1074 405 L1068 421" fill="none" stroke="#4B5563" stroke-width="3" stroke-linecap="round"/>
  <text x="1050" y="465" width="150" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#111827">Branch Router</text>

  <rect x="390" y="376" width="120" height="58" rx="12" fill="url(#deviceFill)" stroke="#595959" stroke-width="2" filter="url(#softShadow)"/>
  <line x1="408" y1="393" x2="492" y2="393" stroke="#6B7280" stroke-width="2"/>
  <line x1="408" y1="405" x2="492" y2="405" stroke="#6B7280" stroke-width="2"/>
  <line x1="408" y1="417" x2="492" y2="417" stroke="#6B7280" stroke-width="2"/>
  <text x="450" y="461" width="140" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#111827">Access Switch</text>

  <rect x="92" y="376" width="116" height="58" rx="12" fill="url(#deviceFill)" stroke="#595959" stroke-width="2" filter="url(#softShadow)"/>
  <circle cx="150" cy="405" r="14" fill="#E0F2FE" stroke="#0284C7"/>
  <path d="M132 405 C140 392 160 392 168 405 M139 414 C145 407 155 407 161 414" fill="none" stroke="#0284C7" stroke-width="2"/>
  <text x="150" y="461" width="130" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#111827">Wireless AP</text>

  <rect x="96" y="540" width="108" height="50" rx="10" fill="url(#deviceFill)" stroke="#595959" stroke-width="2" filter="url(#softShadow)"/>
  <path d="M120 552 L180 552 L172 576 L128 576 Z" fill="#EAF0F7" stroke="#7B8794"/>
  <text x="150" y="614" width="110" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#111827">Laptop</text>

  <rect x="250" y="486" width="100" height="58" rx="12" fill="url(#deviceFill)" stroke="#595959" stroke-width="2" filter="url(#softShadow)"/>
  <rect x="283" y="498" width="34" height="34" rx="5" fill="#EAF0F7" stroke="#7B8794"/>
  <text x="300" y="568" width="120" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#111827">IP Phone</text>

  <rect x="400" y="486" width="100" height="58" rx="12" fill="url(#deviceFill)" stroke="#595959" stroke-width="2" filter="url(#softShadow)"/>
  <rect x="422" y="500" width="56" height="28" rx="4" fill="#EAF0F7" stroke="#7B8794"/>
  <text x="450" y="568" width="110" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#111827">PC-02</text>

  <rect x="580" y="486" width="60" height="76" rx="10" fill="url(#deviceFill)" stroke="#595959" stroke-width="2" filter="url(#softShadow)"/>
  <circle cx="610" cy="506" r="4" fill="#22C55E"/>
  <line x1="594" y1="522" x2="626" y2="522" stroke="#6B7280" stroke-width="2"/>
  <line x1="594" y1="536" x2="626" y2="536" stroke="#6B7280" stroke-width="2"/>
  <text x="610" y="586" width="110" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#111827">App Server</text>

  <rect x="764" y="376" width="138" height="58" rx="12" fill="url(#deviceFill)" stroke="#595959" stroke-width="2" filter="url(#softShadow)"/>
  <circle cx="790" cy="405" r="8" fill="#DBEAFE" stroke="#2563EB"/>
  <circle cx="824" cy="405" r="8" fill="#DBEAFE" stroke="#2563EB"/>
  <circle cx="858" cy="405" r="8" fill="#DBEAFE" stroke="#2563EB"/>
  <text x="833" y="461" width="160" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#111827">WLAN Controller</text>

  <rect x="355" y="278" width="140" height="24" rx="12" fill="#FFFFFF" stroke="#E5E7EB"/>
  <text x="425" y="295" width="140" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#374151">192.168.1.0/24</text>
  <rect x="882" y="236" width="70" height="24" rx="12" fill="#FFFFFF" stroke="#E5E7EB"/>
  <text x="917" y="253" width="70" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#374151">Gi0/1</text>
  <rect x="915" y="330" width="70" height="24" rx="12" fill="#FFFFFF" stroke="#E5E7EB"/>
  <text x="950" y="347" width="70" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#374151">S0/0</text>
  <rect x="540" y="418" width="72" height="24" rx="12" fill="#FFFFFF" stroke="#E5E7EB"/>
  <text x="576" y="435" width="72" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#374151">Gi0/11</text>

  <rect x="80" y="575" width="1120" height="105" rx="22" fill="url(#legendFill)" stroke="#D9E2EC" stroke-width="1.5" filter="url(#softShadow)"/>
  <text x="112" y="608" width="130" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#111827">Legend</text>
  <line x1="240" y1="625" x2="310" y2="625" stroke="#FF0000" stroke-width="4"/>
  <text x="325" y="630" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#111827">Ethernet / wired link</text>
  <line x1="500" y1="625" x2="570" y2="625" stroke="#FF0000" stroke-width="4" stroke-dasharray="10 8"/>
  <text x="585" y="630" width="130" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#111827">Serial WAN link</text>
  <path d="M740 625 C755 607 775 643 790 625 C805 607 825 643 840 625" fill="none" stroke="#00B0F0" stroke-width="4" stroke-dasharray="8 6"/>
  <text x="858" y="630" width="140" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#111827">Wireless link</text>
  <circle cx="1040" cy="625" r="18" fill="url(#routerFill)" stroke="#595959" stroke-width="2"/>
  <text x="1070" y="630" width="110" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#111827">Router / core</text>
  <rect x="240" y="646" width="46" height="24" rx="6" fill="url(#deviceFill)" stroke="#595959" stroke-width="1.5"/>
  <text x="300" y="664" width="175" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#111827">Endpoint or service node</text>
  <rect x="500" y="646" width="18" height="36" rx="4" fill="#FFF1F0" stroke="#C2410C" stroke-width="1.5"/>
  <text x="535" y="664" width="160" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#111827">Security boundary</text>
  <rect x="740" y="646" width="62" height="24" rx="12" fill="#FFFFFF" stroke="#E5E7EB"/>
  <text x="818" y="664" width="210" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#111827">Interface / subnet label</text>
</svg>
```

## Avoid in this skill
- ❌ Do not use `marker-end` arrowheads for connectors; they may disappear. If direction is required, draw a small triangular `<path>` manually at the line end.
- ❌ Do not apply filters to `<line>` connectors; shadows/glows on lines are dropped. Keep filters on node shapes, panels, and paths only.
- ❌ Do not build reusable device icons with `<use>` or `<symbol>`; duplicate the editable primitive shapes directly.
- ❌ Do not rely on unlabeled color alone. Always pair coded links with a legend and/or small text labels.
- ❌ Do not overcrowd the topology canvas with every possible interface label; reserve labels for subnets, WAN ports, or items that change interpretation.

## Composition notes
- Keep the slide in three zones: title at the top, topology canvas in the middle, legend at the bottom.
- Put connectors behind nodes, then draw nodes, then draw labels last so the diagram remains readable.
- Use one strong accent color per relationship type: red for wired/serial, blue for wireless, green for the outer map frame.
- Preserve generous negative space around routers and aggregation points; dense links should terminate at a switch or hub rather than crisscrossing the whole canvas.