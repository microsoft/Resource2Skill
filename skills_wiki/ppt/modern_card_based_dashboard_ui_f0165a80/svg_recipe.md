# SVG Recipe — Modern Card-Based Dashboard UI

## Visual mechanism
A dark, app-like canvas is divided into elevated rounded cards that organize KPIs, charts, and status summaries on a strict grid. Subtle shadows, muted borders, generous padding, and restrained accent colors create a premium dashboard feel while keeping every element editable.

## SVG primitives needed
- 1× `<rect>` for the full-slide dark background
- 2× `<ellipse>` for soft ambient background glows
- 7× `<rect>` for primary rounded dashboard cards
- 6× `<rect>` for small status pills and progress/bar elements
- 10× `<line>` for chart gridlines and dividers
- 8× `<path>` for sparklines, area chart fills, trend strokes, and decorative chart curves
- 3× `<circle>` for donut/progress indicators and tiny legend dots
- 1× `<image>` clipped to a circular avatar
- 1× `<clipPath>` with `<circle>` for the avatar crop
- 4× `<linearGradient>` for background, cards, chart fill, and accent strokes
- 1× `<radialGradient>` for ambient glow coloration
- 2× `<filter>`: one soft drop shadow for cards, one blur glow for ambient decorative shapes
- Multiple `<text>` elements with explicit `width` attributes for titles, KPIs, labels, and chart annotations

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" font-family="Segoe UI, Microsoft YaHei, sans-serif">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1280" y2="720">
      <stop offset="0" stop-color="#0B1020"/>
      <stop offset="1" stop-color="#111827"/>
    </linearGradient>
    <linearGradient id="cardGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#22283D"/>
      <stop offset="1" stop-color="#1B2133"/>
    </linearGradient>
    <linearGradient id="areaBlue" x1="0" y1="285" x2="0" y2="585">
      <stop offset="0" stop-color="#38BDF8" stop-opacity="0.36"/>
      <stop offset="1" stop-color="#38BDF8" stop-opacity="0.02"/>
    </linearGradient>
    <linearGradient id="accentStroke" x1="80" y1="0" x2="590" y2="0">
      <stop offset="0" stop-color="#38BDF8"/>
      <stop offset="0.55" stop-color="#818CF8"/>
      <stop offset="1" stop-color="#F472B6"/>
    </linearGradient>
    <radialGradient id="ambient" cx="50%" cy="50%" r="50%">
      <stop offset="0" stop-color="#38BDF8" stop-opacity="0.35"/>
      <stop offset="1" stop-color="#38BDF8" stop-opacity="0"/>
    </radialGradient>
    <filter id="cardShadow" x="-15%" y="-15%" width="130%" height="140%">
      <feOffset dx="0" dy="12"/>
      <feGaussianBlur stdDeviation="14"/>
      <feColorMatrix type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 .24 0"/>
      <feMerge><feMergeNode/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <filter id="softGlow" x="-60%" y="-60%" width="220%" height="220%">
      <feGaussianBlur stdDeviation="38"/>
    </filter>
    <clipPath id="avatarClip">
      <circle cx="1188" cy="64" r="22"/>
    </clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>
  <ellipse cx="1050" cy="72" rx="250" ry="120" fill="url(#ambient)" filter="url(#softGlow)"/>
  <ellipse cx="190" cy="690" rx="310" ry="140" fill="#7C3AED" opacity="0.13" filter="url(#softGlow)"/>

  <text x="56" y="55" width="520" fill="#FFFFFF" font-size="30" font-weight="700">Performance Tracking 2024</text>
  <text x="56" y="84" width="460" fill="#94A3B8" font-size="14">Live operating dashboard · updated 8 minutes ago</text>
  <rect x="1036" y="42" width="104" height="36" rx="18" fill="#122D29" stroke="#1E7A65"/>
  <circle cx="1057" cy="60" r="5" fill="#34D399"/>
  <text x="1070" y="66" width="60" fill="#A7F3D0" font-size="13" font-weight="600">On Track</text>
  <image href="https://images.example.com/avatars/executive-portrait-for-dashboard.jpg" x="1166" y="42" width="44" height="44" clip-path="url(#avatarClip)"/>
  <text x="1218" y="67" width="42" fill="#CBD5E1" font-size="13" font-weight="600">AM</text>

  <rect x="56" y="110" width="274" height="130" rx="22" fill="url(#cardGrad)" stroke="#303854" filter="url(#cardShadow)"/>
  <rect x="354" y="110" width="274" height="130" rx="22" fill="url(#cardGrad)" stroke="#303854" filter="url(#cardShadow)"/>
  <rect x="652" y="110" width="274" height="130" rx="22" fill="url(#cardGrad)" stroke="#303854" filter="url(#cardShadow)"/>
  <rect x="950" y="110" width="274" height="130" rx="22" fill="url(#cardGrad)" stroke="#303854" filter="url(#cardShadow)"/>

  <text x="82" y="145" width="150" fill="#94A3B8" font-size="13" font-weight="600">REVENUE</text>
  <text x="82" y="185" width="140" fill="#FFFFFF" font-size="34" font-weight="800">$8.42M</text>
  <rect x="236" y="128" width="68" height="26" rx="13" fill="#063B35"/>
  <text x="250" y="147" width="42" fill="#6EE7B7" font-size="12" font-weight="700">+12%</text>
  <path d="M82 214 C112 196,132 224,158 207 S206 196,232 212 S276 202,304 190" fill="none" stroke="#34D399" stroke-width="4" stroke-linecap="round"/>

  <text x="380" y="145" width="150" fill="#94A3B8" font-size="13" font-weight="600">ACTIVE USERS</text>
  <text x="380" y="185" width="150" fill="#FFFFFF" font-size="34" font-weight="800">184K</text>
  <rect x="536" y="128" width="66" height="26" rx="13" fill="#2E245A"/>
  <text x="550" y="147" width="40" fill="#C4B5FD" font-size="12" font-weight="700">+8%</text>
  <path d="M380 213 C407 218,432 190,458 198 S506 229,532 202 S578 188,604 199" fill="none" stroke="#818CF8" stroke-width="4" stroke-linecap="round"/>

  <text x="678" y="145" width="150" fill="#94A3B8" font-size="13" font-weight="600">CHURN RISK</text>
  <text x="678" y="185" width="140" fill="#FFFFFF" font-size="34" font-weight="800">2.7%</text>
  <rect x="824" y="128" width="76" height="26" rx="13" fill="#3B1725"/>
  <text x="838" y="147" width="50" fill="#FDA4AF" font-size="12" font-weight="700">-0.4%</text>
  <path d="M678 198 C708 190,730 204,755 198 S806 182,830 190 S875 206,900 184" fill="none" stroke="#F472B6" stroke-width="4" stroke-linecap="round"/>

  <text x="976" y="145" width="150" fill="#94A3B8" font-size="13" font-weight="600">NPS SCORE</text>
  <text x="976" y="185" width="130" fill="#FFFFFF" font-size="34" font-weight="800">71</text>
  <circle cx="1168" cy="176" r="34" fill="none" stroke="#334155" stroke-width="10"/>
  <circle cx="1168" cy="176" r="34" fill="none" stroke="#38BDF8" stroke-width="10" stroke-dasharray="165 214" stroke-linecap="round" transform="rotate(-90 1168 176)"/>
  <text x="1154" y="183" width="36" fill="#E0F2FE" font-size="16" font-weight="800">83%</text>

  <rect x="56" y="264" width="574" height="380" rx="24" fill="url(#cardGrad)" stroke="#303854" filter="url(#cardShadow)"/>
  <text x="86" y="306" width="300" fill="#FFFFFF" font-size="19" font-weight="750">Revenue momentum</text>
  <text x="86" y="330" width="360" fill="#94A3B8" font-size="13">Quarterly recurring revenue by segment</text>
  <circle cx="498" cy="302" r="5" fill="#38BDF8"/><text x="510" y="307" width="45" fill="#CBD5E1" font-size="12">Cloud</text>
  <circle cx="560" cy="302" r="5" fill="#F472B6"/><text x="572" y="307" width="45" fill="#CBD5E1" font-size="12">Data</text>
  <line x1="96" y1="382" x2="590" y2="382" stroke="#334155" stroke-width="1"/>
  <line x1="96" y1="438" x2="590" y2="438" stroke="#334155" stroke-width="1"/>
  <line x1="96" y1="494" x2="590" y2="494" stroke="#334155" stroke-width="1"/>
  <line x1="96" y1="550" x2="590" y2="550" stroke="#334155" stroke-width="1"/>
  <path d="M96 564 L96 514 C144 500,178 468,222 480 C270 494,302 420,346 430 C390 440,424 380,468 392 C512 404,546 344,590 354 L590 564 Z" fill="url(#areaBlue)"/>
  <path d="M96 514 C144 500,178 468,222 480 C270 494,302 420,346 430 C390 440,424 380,468 392 C512 404,546 344,590 354" fill="none" stroke="url(#accentStroke)" stroke-width="5" stroke-linecap="round"/>
  <path d="M96 540 C146 532,182 520,226 526 C274 532,308 488,352 496 C398 504,430 468,474 476 C520 484,548 438,590 446" fill="none" stroke="#F472B6" stroke-width="3" stroke-linecap="round" opacity="0.8"/>
  <text x="94" y="598" width="42" fill="#64748B" font-size="12">Jan</text>
  <text x="210" y="598" width="42" fill="#64748B" font-size="12">Mar</text>
  <text x="330" y="598" width="42" fill="#64748B" font-size="12">May</text>
  <text x="450" y="598" width="42" fill="#64748B" font-size="12">Jul</text>
  <text x="560" y="598" width="42" fill="#64748B" font-size="12">Sep</text>

  <rect x="654" y="264" width="570" height="170" rx="24" fill="url(#cardGrad)" stroke="#303854" filter="url(#cardShadow)"/>
  <text x="684" y="306" width="260" fill="#FFFFFF" font-size="19" font-weight="750">Regional pipeline</text>
  <text x="684" y="330" width="340" fill="#94A3B8" font-size="13">Weighted opportunities by territory</text>
  <rect x="684" y="362" width="490" height="12" rx="6" fill="#334155"/><rect x="684" y="362" width="360" height="12" rx="6" fill="#38BDF8"/>
  <rect x="684" y="392" width="490" height="12" rx="6" fill="#334155"/><rect x="684" y="392" width="284" height="12" rx="6" fill="#818CF8"/>
  <text x="684" y="356" width="120" fill="#CBD5E1" font-size="12">North America</text><text x="1132" y="356" width="50" fill="#CBD5E1" font-size="12">$3.1M</text>
  <text x="684" y="386" width="120" fill="#CBD5E1" font-size="12">Europe</text><text x="1132" y="386" width="50" fill="#CBD5E1" font-size="12">$2.4M</text>

  <rect x="654" y="458" width="270" height="166" rx="24" fill="url(#cardGrad)" stroke="#303854" filter="url(#cardShadow)"/>
  <text x="684" y="500" width="170" fill="#FFFFFF" font-size="18" font-weight="750">Team capacity</text>
  <text x="684" y="525" width="190" fill="#94A3B8" font-size="13">Utilization across squads</text>
  <circle cx="792" cy="570" r="38" fill="none" stroke="#334155" stroke-width="12"/>
  <circle cx="792" cy="570" r="38" fill="none" stroke="#34D399" stroke-width="12" stroke-dasharray="188 239" stroke-linecap="round" transform="rotate(-90 792 570)"/>
  <text x="770" y="579" width="48" fill="#FFFFFF" font-size="22" font-weight="800">79%</text>

  <rect x="954" y="458" width="270" height="166" rx="24" fill="url(#cardGrad)" stroke="#303854" filter="url(#cardShadow)"/>
  <text x="984" y="500" width="170" fill="#FFFFFF" font-size="18" font-weight="750">Executive notes</text>
  <text x="984" y="530" width="210" fill="#CBD5E1" font-size="14">Enterprise renewals are ahead of plan; hiring constraints remain the largest delivery risk.</text>
  <line x1="984" y1="558" x2="1194" y2="558" stroke="#334155" stroke-width="1"/>
  <text x="984" y="590" width="185" fill="#94A3B8" font-size="13">Next review: Monday 10:00</text>
</svg>
```

## Avoid in this skill
- ❌ Uneven card gutters or inconsistent corner radii; the technique depends on a disciplined UI grid.
- ❌ Heavy black shadows with hard edges; use soft low-opacity elevation instead.
- ❌ Dense chart labels that touch card edges; preserve generous internal padding.
- ❌ Applying `clip-path` to card rectangles or chart paths; only use clipping on `<image>` elements.
- ❌ Building dashboard cards as screenshots when the content can be native SVG shapes and editable text.

## Composition notes
- Keep a 48–64 px outer margin and 24 px gutters so the layout feels intentional rather than crowded.
- Use KPI cards across the top, one dominant analysis card below, and smaller support cards on the right for hierarchy.
- Let the dark canvas show through between cards; the negative space is part of the premium UI effect.
- Restrict accents to 2–4 colors and repeat them consistently across pills, sparklines, legends, and progress rings.