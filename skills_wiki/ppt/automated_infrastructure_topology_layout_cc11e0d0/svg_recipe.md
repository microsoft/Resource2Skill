# SVG Recipe — Automated Infrastructure Topology Layout

## Visual mechanism
A polished infrastructure topology uses strict top-down hierarchy, pale security-zone containers, semantic node icons, and orthogonal elbow connectors to make invisible systems feel orderly and navigable. The premium look comes from disciplined alignment, subtle shadows, color-coded layers, and a few recognizable network symbols such as cloud, firewall shield, switch, servers, database, and clients.

## SVG primitives needed
- 1× `<rect>` full-slide background for a clean technical canvas
- 3× large dashed `<rect>` zone containers for DMZ, secure application subnet, and data subnet
- 12× `<path>` for elbow-routed topology connections and semantic icons such as cloud and firewall shield
- 20× `<rect>` for switches, server bodies, status lights, ports, device cards, and callout plates
- 4× `<ellipse>` for database cylinder caps and soft endpoint indicators
- 8× `<circle>` for server LEDs, client avatars, and health/status dots
- 1× `<linearGradient>` for premium blue network-node fills
- 1× `<linearGradient>` for firewall/security fills
- 1× `<filter id="shadow">` applied to node plates and icon bodies
- 1× `<filter id="softGlow">` applied to the core switch to emphasize the central routing layer
- Multiple `<text>` elements with explicit `width` attributes for title, zone labels, node labels, and technical annotations

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgWash" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#F8FBFF"/>
      <stop offset="100%" stop-color="#EEF4F9"/>
    </linearGradient>
    <linearGradient id="blueNode" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#2E9BEF"/>
      <stop offset="100%" stop-color="#1B5FA7"/>
    </linearGradient>
    <linearGradient id="redNode" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#FF6B5D"/>
      <stop offset="100%" stop-color="#C83228"/>
    </linearGradient>
    <filter id="shadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="8"/>
      <feGaussianBlur stdDeviation="8"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="softGlow" x="-35%" y="-35%" width="170%" height="170%">
      <feGaussianBlur stdDeviation="7"/>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgWash)"/>
  <text x="54" y="54" width="760" font-family="Segoe UI, Microsoft YaHei" font-size="32" font-weight="700" fill="#243447">Enterprise Network Architecture</text>
  <text x="56" y="86" width="720" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#6B7C88">High-level topology mapping, security boundaries, and critical data flows</text>
  <rect x="1030" y="38" width="170" height="32" rx="16" fill="#EAF3FF" stroke="#B7D6F6"/>
  <circle cx="1052" cy="54" r="5" fill="#27AE60"/>
  <text x="1066" y="60" width="120" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#2C3E50">LIVE TARGET</text>

  <rect x="70" y="128" width="1140" height="128" rx="24" fill="#FFFFFF" stroke="#CBD6DF" stroke-dasharray="8 7"/>
  <text x="92" y="154" width="240" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#8A99A6">PUBLIC / DMZ EDGE</text>
  <rect x="70" y="284" width="1140" height="192" rx="24" fill="#FFFFFF" stroke="#CBD6DF" stroke-dasharray="8 7"/>
  <text x="92" y="310" width="260" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#8A99A6">SECURE APPLICATION SUBNET</text>
  <rect x="70" y="504" width="1140" height="146" rx="24" fill="#FFFFFF" stroke="#CBD6DF" stroke-dasharray="8 7"/>
  <text x="92" y="530" width="240" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#8A99A6">DATA / OPERATIONS SUBNET</text>

  <path d="M640 200 V270" stroke="#8FA3B1" stroke-width="2.4" fill="none"/>
  <path d="M640 374 V416" stroke="#8FA3B1" stroke-width="2.4" fill="none"/>
  <path d="M640 452 V492" stroke="#8FA3B1" stroke-width="2.4" fill="none"/>
  <path d="M640 452 H362 V548" stroke="#8FA3B1" stroke-width="2.4" fill="none"/>
  <path d="M640 452 H918 V548" stroke="#8FA3B1" stroke-width="2.4" fill="none"/>
  <path d="M640 492 H214 V552" stroke="#8FA3B1" stroke-width="2.4" fill="none" stroke-dasharray="7 7"/>
  <path d="M640 492 H1066 V552" stroke="#8FA3B1" stroke-width="2.4" fill="none" stroke-dasharray="7 7"/>
  <path d="M522 172 H274 V206" stroke="#8FA3B1" stroke-width="2.4" fill="none"/>
  <path d="M758 172 H1006 V206" stroke="#8FA3B1" stroke-width="2.4" fill="none"/>

  <path d="M532 171 C532 143 554 124 582 129 C592 99 635 92 653 121 C682 116 707 137 707 165 C733 168 748 188 744 211 C738 238 710 242 688 238 L570 238 C541 238 520 218 522 195 C523 183 526 176 532 171 Z" fill="#F0F4F7" stroke="#AAB7C0" stroke-width="2" filter="url(#shadow)"/>
  <text x="592" y="190" width="96" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="700" fill="#263646">Internet</text>
  <text x="612" y="213" width="70" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#6D7E89">T1 / VPN</text>

  <rect x="210" y="170" width="128" height="64" rx="14" fill="#F6FAFD" stroke="#C4D2DC" filter="url(#shadow)"/>
  <circle cx="244" cy="202" r="19" fill="#DDEBFF" stroke="#8CB8E8"/>
  <circle cx="292" cy="202" r="19" fill="#DDEBFF" stroke="#8CB8E8"/>
  <text x="198" y="260" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#34495E" text-anchor="middle">Remote Users</text>

  <rect x="942" y="170" width="128" height="64" rx="14" fill="#F6FAFD" stroke="#C4D2DC" filter="url(#shadow)"/>
  <rect x="972" y="190" width="68" height="34" rx="6" fill="#7FC0F2" stroke="#4C8EC2"/>
  <rect x="982" y="181" width="50" height="16" rx="4" fill="#B9DDF8" stroke="#7BAED4"/>
  <text x="930" y="260" width="154" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#34495E" text-anchor="middle">Partner Cloud</text>

  <path d="M640 270 L712 298 L712 342 C712 386 674 410 640 424 C606 410 568 386 568 342 L568 298 Z" fill="url(#redNode)" stroke="#9D271F" stroke-width="2" filter="url(#shadow)"/>
  <path d="M640 287 V405 M586 317 H694 M586 342 H694 M600 367 H680" stroke="#FFFFFF" stroke-width="2" opacity="0.62"/>
  <text x="592" y="337" width="96" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#FFFFFF" text-anchor="middle">Firewall</text>
  <text x="594" y="357" width="92" font-family="Segoe UI, Microsoft YaHei" font-size="10" fill="#FFE7E4" text-anchor="middle">WAF + IPS</text>

  <ellipse cx="640" cy="435" rx="132" ry="44" fill="#2E9BEF" opacity="0.16" filter="url(#softGlow)"/>
  <rect x="505" y="396" width="270" height="78" rx="18" fill="url(#blueNode)" stroke="#164F8A" stroke-width="2" filter="url(#shadow)"/>
  <text x="558" y="429" width="170" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="700" fill="#FFFFFF" text-anchor="middle">Core Switch</text>
  <text x="558" y="450" width="170" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#CFE8FF" text-anchor="middle">24 Port Hub / VLAN Routing</text>
  <rect x="532" y="458" width="12" height="6" rx="2" fill="#BFE4FF"/>
  <rect x="552" y="458" width="12" height="6" rx="2" fill="#BFE4FF"/>
  <rect x="572" y="458" width="12" height="6" rx="2" fill="#BFE4FF"/>
  <rect x="592" y="458" width="12" height="6" rx="2" fill="#BFE4FF"/>
  <rect x="612" y="458" width="12" height="6" rx="2" fill="#BFE4FF"/>
  <rect x="632" y="458" width="12" height="6" rx="2" fill="#BFE4FF"/>
  <rect x="652" y="458" width="12" height="6" rx="2" fill="#BFE4FF"/>
  <rect x="672" y="458" width="12" height="6" rx="2" fill="#BFE4FF"/>

  <rect x="318" y="534" width="88" height="84" rx="10" fill="#74838C" stroke="#4E5C64" stroke-width="2" filter="url(#shadow)"/>
  <rect x="333" y="550" width="58" height="11" rx="3" fill="#9BA8AE"/>
  <rect x="333" y="568" width="58" height="11" rx="3" fill="#9BA8AE"/>
  <rect x="333" y="586" width="58" height="11" rx="3" fill="#9BA8AE"/>
  <circle cx="385" cy="555" r="3.5" fill="#27AE60"/>
  <text x="286" y="644" width="152" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#34495E" text-anchor="middle">App Server 01</text>

  <rect x="874" y="534" width="88" height="84" rx="10" fill="#74838C" stroke="#4E5C64" stroke-width="2" filter="url(#shadow)"/>
  <rect x="889" y="550" width="58" height="11" rx="3" fill="#9BA8AE"/>
  <rect x="889" y="568" width="58" height="11" rx="3" fill="#9BA8AE"/>
  <rect x="889" y="586" width="58" height="11" rx="3" fill="#9BA8AE"/>
  <circle cx="941" cy="555" r="3.5" fill="#27AE60"/>
  <text x="842" y="644" width="152" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#34495E" text-anchor="middle">App Server 02</text>

  <ellipse cx="214" cy="558" rx="43" ry="13" fill="#A9C9E8" stroke="#6F9EC8" stroke-width="2"/>
  <rect x="171" y="558" width="86" height="54" fill="#D9ECFA" stroke="#6F9EC8" stroke-width="2"/>
  <ellipse cx="214" cy="612" rx="43" ry="13" fill="#CDE5F7" stroke="#6F9EC8" stroke-width="2"/>
  <text x="154" y="644" width="120" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#34495E" text-anchor="middle">SQL Cluster</text>

  <rect x="1026" y="546" width="80" height="52" rx="10" fill="#E8F4FF" stroke="#8CB8E8" stroke-width="2" filter="url(#shadow)"/>
  <circle cx="1049" cy="572" r="12" fill="#2E9BEF"/>
  <circle cx="1082" cy="572" r="12" fill="#2E9BEF"/>
  <text x="1000" y="644" width="132" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#34495E" text-anchor="middle">Admin Clients</text>

  <rect x="808" y="88" width="220" height="74" rx="8" fill="#FFFFFF" stroke="#D6DEE5" filter="url(#shadow)" transform="rotate(-7 918 125)"/>
  <text x="828" y="119" width="180" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#2C3E50" transform="rotate(-7 918 125)">New Exchange Server</text>
  <text x="828" y="139" width="180" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#4F5F6B" transform="rotate(-7 918 125)">600 MHz · 256 MB RAM · RAID 5</text>
</svg>
```

## Avoid in this skill
- ❌ `marker-end` on `<path>` for arrowheads; PowerPoint translation drops path markers, so use plain orthogonal paths or draw arrowheads as small separate paths only if needed.
- ❌ Applying `filter` to connector `<line>` elements; use unfiltered `<path>` connectors and reserve shadows/glows for nodes.
- ❌ `<use>` or `<symbol>` to repeat server/client icons; duplicate the editable primitive shapes instead.
- ❌ `clip-path` on zone rectangles or node shapes; clipping is reliable for images only, and this topology should remain fully editable.
- ❌ Dense diagonal spaghetti lines; preserve the topology’s executive-readability by using 90-degree elbow routes and shared bus trunks.

## Composition notes
- Keep the internet/cloud layer near the top, the firewall/security layer in the upper middle, the core switch centered, and compute/data resources aligned along the bottom.
- Use pale dashed containers behind nodes to show security boundaries without competing with the topology itself.
- Put all connectors behind nodes and above zone backgrounds; this makes the diagram feel routed, not randomly overlaid.
- Reserve saturated color for critical layers: red for firewall/security, blue for core networking, gray for compute, and soft blue for users/data endpoints.