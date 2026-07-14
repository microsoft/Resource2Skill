# SVG Recipe — Fintech Dark Mode Pricing Tiers

## Visual mechanism
A darkened trading/workspace photo creates a premium “secure finance” atmosphere, while neon lime typography and glows pull attention to the offer. Three horizontally spaced pricing cards use metallic tier colors, glassy dark fills, and sharp feature rows to feel like high-end fintech product packages.

## SVG primitives needed
- 1× `<image>` for the full-bleed dark fintech background photo
- 1× `<rect>` for the black photo-darkening overlay
- 1× `<rect>` for the subtle top-to-bottom vignette wash
- 3× large rounded `<rect>` for the tier card shells
- 3× rounded `<rect>` for colored tier header bands
- 3× `<rect>` for price badges
- 12× `<line>` for feature dividers and thin fintech UI rails
- 9× `<circle>` for status dots and small metric accents
- 3× `<ellipse>` for soft neon/colored glows behind the cards
- 6× `<path>` for angular card corner details, mini shield/check icons, and decorative circuit strokes
- 14× `<text>` blocks with explicit `width` for title, subtitle, tier names, prices, and feature copy
- 5× `<linearGradient>` for background wash, card glass, and tier metallic headers
- 2× `<filter>`: one soft shadow for cards, one neon glow for accent objects/text

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="vignette" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#050707" stop-opacity="0.25"/>
      <stop offset="48%" stop-color="#080A0C" stop-opacity="0.78"/>
      <stop offset="100%" stop-color="#000000" stop-opacity="0.96"/>
    </linearGradient>
    <linearGradient id="cardGlass" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#252A2F" stop-opacity="0.96"/>
      <stop offset="55%" stop-color="#15191D" stop-opacity="0.94"/>
      <stop offset="100%" stop-color="#0A0D10" stop-opacity="0.98"/>
    </linearGradient>
    <linearGradient id="silverTier" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#82888F"/>
      <stop offset="48%" stop-color="#E6E9EC"/>
      <stop offset="100%" stop-color="#8C9298"/>
    </linearGradient>
    <linearGradient id="blueTier" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#0A6FB2"/>
      <stop offset="52%" stop-color="#39C9FF"/>
      <stop offset="100%" stop-color="#1451D8"/>
    </linearGradient>
    <linearGradient id="redTier" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#8F1320"/>
      <stop offset="50%" stop-color="#FF4E62"/>
      <stop offset="100%" stop-color="#C3182B"/>
    </linearGradient>
    <filter id="softShadow" x="-30%" y="-30%" width="160%" height="170%">
      <feOffset dx="0" dy="16"/>
      <feGaussianBlur stdDeviation="18"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="neonGlow" x="-60%" y="-60%" width="220%" height="220%">
      <feGaussianBlur stdDeviation="8"/>
    </filter>
  </defs>

  <image href="https://images.example.com/fintech-dark-trading-desk-laptop-charts.jpg" x="0" y="0" width="1280" height="720" preserveAspectRatio="xMidYMid slice"/>
  <rect x="0" y="0" width="1280" height="720" fill="#020304" opacity="0.72"/>
  <rect x="0" y="0" width="1280" height="720" fill="url(#vignette)"/>

  <ellipse cx="318" cy="446" rx="175" ry="112" fill="#B9C0C7" opacity="0.13" filter="url(#neonGlow)"/>
  <ellipse cx="640" cy="446" rx="190" ry="122" fill="#96D232" opacity="0.18" filter="url(#neonGlow)"/>
  <ellipse cx="962" cy="446" rx="175" ry="112" fill="#FF4056" opacity="0.15" filter="url(#neonGlow)"/>

  <path d="M78 96 L182 96 L202 116 L338 116" fill="none" stroke="#96D232" stroke-width="2" opacity="0.7"/>
  <path d="M1048 92 L1168 92 L1192 116 L1228 116" fill="none" stroke="#96D232" stroke-width="2" opacity="0.55"/>
  <line x1="74" y1="150" x2="420" y2="150" stroke="#96D232" stroke-width="3"/>
  <line x1="980" y1="150" x2="1208" y2="150" stroke="#FFFFFF" stroke-width="1" opacity="0.18"/>

  <text x="74" y="72" width="760" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" letter-spacing="3" fill="#96D232">SECURE ACCESS PACKAGES</text>
  <text x="74" y="136" width="760" font-family="Segoe UI, Microsoft YaHei" font-size="55" font-weight="800" letter-spacing="-1" fill="#FFFFFF">
    FINTECH <tspan fill="#96D232">PRICING</tspan> TIERS
  </text>
  <text x="74" y="188" width="610" font-family="Segoe UI, Microsoft YaHei" font-size="20" fill="#D7DDE2" opacity="0.92">Choose the investment intelligence layer that matches your team’s trading velocity and risk controls.</text>
  <text x="1000" y="76" width="190" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#FFFFFF" opacity="0.72">Q4 ENTERPRISE OFFER</text>
  <text x="1000" y="105" width="190" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="800" fill="#96D232">+27%</text>
  <text x="1074" y="105" width="140" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#DDE5EA" opacity="0.8">avg. conversion lift</text>

  <rect x="176" y="238" width="284" height="404" rx="26" fill="url(#cardGlass)" stroke="#C9CED2" stroke-width="1.8" filter="url(#softShadow)"/>
  <rect x="176" y="238" width="284" height="82" rx="26" fill="url(#silverTier)"/>
  <path d="M176 294 L176 320 L460 320 L460 294 C430 314 204 314 176 294 Z" fill="#0A0D10" opacity="0.22"/>
  <path d="M426 254 L444 254 L444 272 L426 290 L408 290 L408 272 Z" fill="none" stroke="#FFFFFF" stroke-width="2" opacity="0.7"/>
  <text x="204" y="289" width="210" font-family="Segoe UI, Microsoft YaHei" font-size="28" font-weight="800" fill="#071014">ELEMENTAL</text>
  <text x="204" y="363" width="210" font-family="Segoe UI, Microsoft YaHei" font-size="42" font-weight="800" fill="#FFFFFF">300 PV</text>
  <rect x="204" y="388" width="112" height="32" rx="16" fill="#C9CED2" opacity="0.16"/>
  <text x="222" y="411" width="88" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#E9ECEF">STARTER</text>
  <line x1="204" y1="455" x2="432" y2="455" stroke="#FFFFFF" stroke-width="1" opacity="0.15"/>
  <line x1="204" y1="506" x2="432" y2="506" stroke="#FFFFFF" stroke-width="1" opacity="0.15"/>
  <line x1="204" y1="557" x2="432" y2="557" stroke="#FFFFFF" stroke-width="1" opacity="0.15"/>
  <circle cx="218" cy="438" r="5" fill="#C9CED2"/><circle cx="218" cy="489" r="5" fill="#C9CED2"/><circle cx="218" cy="540" r="5" fill="#C9CED2"/>
  <text x="236" y="443" width="180" font-family="Segoe UI, Microsoft YaHei" font-size="16" fill="#DDE1E5">Market overview signals</text>
  <text x="236" y="494" width="180" font-family="Segoe UI, Microsoft YaHei" font-size="16" fill="#DDE1E5">Weekly portfolio briefing</text>
  <text x="236" y="545" width="180" font-family="Segoe UI, Microsoft YaHei" font-size="16" fill="#DDE1E5">Basic risk dashboard</text>
  <rect x="204" y="586" width="228" height="36" rx="18" fill="#FFFFFF" opacity="0.08"/>
  <text x="246" y="611" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="800" fill="#FFFFFF">SELECT PACK</text>

  <rect x="498" y="218" width="284" height="424" rx="28" fill="url(#cardGlass)" stroke="#96D232" stroke-width="2.8" filter="url(#softShadow)"/>
  <rect x="498" y="218" width="284" height="86" rx="28" fill="url(#blueTier)"/>
  <rect x="568" y="196" width="144" height="34" rx="17" fill="#96D232"/>
  <text x="590" y="219" width="105" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="900" fill="#071014">MOST CHOSEN</text>
  <path d="M742 236 L762 236 L762 256 L742 278 L722 278 L722 256 Z" fill="none" stroke="#FFFFFF" stroke-width="2.2" opacity="0.8"/>
  <text x="526" y="272" width="200" font-family="Segoe UI, Microsoft YaHei" font-size="29" font-weight="800" fill="#FFFFFF">SUPREME</text>
  <text x="526" y="354" width="210" font-family="Segoe UI, Microsoft YaHei" font-size="46" font-weight="800" fill="#96D232" filter="url(#neonGlow)">500 PV</text>
  <text x="526" y="354" width="210" font-family="Segoe UI, Microsoft YaHei" font-size="46" font-weight="800" fill="#FFFFFF">500 PV</text>
  <rect x="526" y="386" width="126" height="32" rx="16" fill="#96D232" opacity="0.18"/>
  <text x="546" y="409" width="98" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="800" fill="#96D232">PRO TRADER</text>
  <line x1="526" y1="455" x2="754" y2="455" stroke="#96D232" stroke-width="1" opacity="0.25"/>
  <line x1="526" y1="506" x2="754" y2="506" stroke="#96D232" stroke-width="1" opacity="0.25"/>
  <line x1="526" y1="557" x2="754" y2="557" stroke="#96D232" stroke-width="1" opacity="0.25"/>
  <circle cx="540" cy="438" r="5" fill="#96D232"/><circle cx="540" cy="489" r="5" fill="#96D232"/><circle cx="540" cy="540" r="5" fill="#96D232"/>
  <text x="558" y="443" width="178" font-family="Segoe UI, Microsoft YaHei" font-size="16" fill="#EEF5EE">Real-time trade alerts</text>
  <text x="558" y="494" width="178" font-family="Segoe UI, Microsoft YaHei" font-size="16" fill="#EEF5EE">AI sentiment scanner</text>
  <text x="558" y="545" width="178" font-family="Segoe UI, Microsoft YaHei" font-size="16" fill="#EEF5EE">Priority analyst sessions</text>
  <rect x="526" y="586" width="228" height="38" rx="19" fill="#96D232"/>
  <text x="588" y="612" width="120" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="900" fill="#071014">ACTIVATE</text>

  <rect x="820" y="238" width="284" height="404" rx="26" fill="url(#cardGlass)" stroke="#FF4E62" stroke-width="1.8" filter="url(#softShadow)"/>
  <rect x="820" y="238" width="284" height="82" rx="26" fill="url(#redTier)"/>
  <path d="M1068 254 L1086 254 L1086 272 L1068 290 L1050 290 L1050 272 Z" fill="none" stroke="#FFFFFF" stroke-width="2" opacity="0.75"/>
  <text x="848" y="289" width="210" font-family="Segoe UI, Microsoft YaHei" font-size="28" font-weight="800" fill="#FFFFFF">ADVANCED</text>
  <text x="848" y="363" width="210" font-family="Segoe UI, Microsoft YaHei" font-size="42" font-weight="800" fill="#FFFFFF">1K PV</text>
  <rect x="848" y="388" width="132" height="32" rx="16" fill="#FF4E62" opacity="0.18"/>
  <text x="869" y="411" width="102" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="800" fill="#FF6878">INSTITUTION</text>
  <line x1="848" y1="455" x2="1076" y2="455" stroke="#FFFFFF" stroke-width="1" opacity="0.15"/>
  <line x1="848" y1="506" x2="1076" y2="506" stroke="#FFFFFF" stroke-width="1" opacity="0.15"/>
  <line x1="848" y1="557" x2="1076" y2="557" stroke="#FFFFFF" stroke-width="1" opacity="0.15"/>
  <circle cx="862" cy="438" r="5" fill="#FF4E62"/><circle cx="862" cy="489" r="5" fill="#FF4E62"/><circle cx="862" cy="540" r="5" fill="#FF4E62"/>
  <text x="880" y="443" width="180" font-family="Segoe UI, Microsoft YaHei" font-size="16" fill="#F2E7E9">Custom liquidity models</text>
  <text x="880" y="494" width="180" font-family="Segoe UI, Microsoft YaHei" font-size="16" fill="#F2E7E9">Dedicated strategy desk</text>
  <text x="880" y="545" width="180" font-family="Segoe UI, Microsoft YaHei" font-size="16" fill="#F2E7E9">Enterprise compliance pack</text>
  <rect x="848" y="586" width="228" height="36" rx="18" fill="#FFFFFF" opacity="0.08"/>
  <text x="900" y="611" width="130" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="800" fill="#FFFFFF">CONTACT SALES</text>
</svg>
```

## Avoid in this skill
- ❌ Using a plain black background only; the premium fintech look depends on a darkened photo plus overlay depth.
- ❌ Applying `filter` to `<line>` elements for glowing dividers; use glowing ellipses/rects/paths behind them instead.
- ❌ Building the pricing table as a dense grid; this style needs spacious, card-based tiers with strong hierarchy.
- ❌ Using `<mask>` or clipping non-image shapes for card effects; rely on rounded rects, gradients, and layered paths.
- ❌ Using muted accent colors for the primary CTA; the neon lime must be highly saturated to cut through the dark mode.

## Composition notes
- Reserve the top-left 25% for the headline system: small uppercase kicker, large white title, and neon-highlighted keyword.
- Keep the three pricing cards centered across the lower 60% with generous gutters; make the middle card slightly taller or brighter for emphasis.
- Use neon lime sparingly: title accent, selected badge, CTA, and a few divider/status details.
- Let tier colors identify hierarchy: silver for entry, blue/neon for primary, red for advanced or institutional.