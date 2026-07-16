# SVG Recipe — Asymmetric Expert Profile & Skill Dashboard

## Visual mechanism
A premium expert-bio slide built from a strong asymmetrical split: a dark, human-centered profile panel on the left and a clean white dashboard canvas on the right. The right side turns credentials into quick-read evidence through a horizontal career timeline and layered proficiency bars.

## SVG primitives needed
- 3× `<rect>` for the outer stage, left dark profile panel, and right white dashboard card
- 1× `<image>` clipped into a circle for the expert avatar
- 1× `<clipPath>` with `<circle>` for the circular portrait crop
- 1× `<circle>` for the avatar border, plus 3× `<circle>` for timeline milestones
- 1× `<rect>` with gradient fill for the timeline connector
- 6× `<rect>` for skill bar tracks and colored fills
- 1× `<path>` for a subtle decorative maroon accent slash on the right panel
- Multiple `<text>` elements with explicit `width` for title, subtitle, bio, dates, labels, captions, stars, and percentages
- 2× `<linearGradient>` for the timeline connector and dark left-panel depth
- 1× `<radialGradient>` for the cool presentation backdrop
- 1× `<filter id="cardShadow">` for the elevated dashboard-card shadow
- 1× `<filter id="softShadow">` for subtle text/card depth

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <radialGradient id="backdrop" cx="25%" cy="35%" r="85%">
      <stop offset="0%" stop-color="#30465c"/>
      <stop offset="55%" stop-color="#142335"/>
      <stop offset="100%" stop-color="#e9eef3"/>
    </radialGradient>

    <linearGradient id="leftDepth" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#1f3348"/>
      <stop offset="100%" stop-color="#17283a"/>
    </linearGradient>

    <linearGradient id="timelineGrad" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#c42f4a"/>
      <stop offset="48%" stop-color="#6f263f"/>
      <stop offset="100%" stop-color="#112b46"/>
    </linearGradient>

    <filter id="cardShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feOffset dx="0" dy="14"/>
      <feGaussianBlur stdDeviation="14"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feOffset dx="3" dy="5"/>
      <feGaussianBlur stdDeviation="4"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <clipPath id="avatarClip">
      <circle cx="282" cy="206" r="106"/>
    </clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#backdrop)"/>

  <rect x="80" y="46" width="1120" height="628" rx="0" fill="#ffffff" filter="url(#cardShadow)"/>
  <rect x="80" y="46" width="452" height="628" fill="url(#leftDepth)"/>

  <path d="M532 46 C575 150 572 276 532 365 L532 46 Z" fill="#223b55" opacity="0.28"/>

  <circle cx="282" cy="206" r="112" fill="none" stroke="#0b1724" stroke-width="8"/>
  <image href="https://images.example.com/expert-profile-outdoor-portrait.jpg" x="176" y="100" width="212" height="212" clip-path="url(#avatarClip)" preserveAspectRatio="xMidYMid slice"/>
  <circle cx="282" cy="206" r="106" fill="none" stroke="#111d2c" stroke-width="2"/>

  <text x="282" y="380" width="260" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="43" font-weight="700" fill="#ffe766" letter-spacing="6">★★★★★</text>

  <text x="160" y="438" width="244" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="17" fill="#d7dde5" line-height="1.35">
    <tspan x="160" dy="0">Strategy leader with deep</tspan>
    <tspan x="160" dy="24">experience turning complex</tspan>
    <tspan x="160" dy="24">customer, product, and data</tspan>
    <tspan x="160" dy="24">signals into executive-ready</tspan>
    <tspan x="160" dy="24">decisions. Known for crisp</tspan>
    <tspan x="160" dy="24">storytelling, modern systems</tspan>
    <tspan x="160" dy="24">thinking, and team enablement.</tspan>
  </text>

  <text x="724" y="140" width="360" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="58" font-weight="800" fill="#13263d">Our expert</text>
  <text x="776" y="188" width="280" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="25" fill="#8b1832">Tagline of this slide</text>

  <text x="592" y="274" width="150" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="24" fill="#111111">Year 2018</text>
  <text x="822" y="274" width="150" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="24" fill="#111111">Year 2020</text>
  <text x="1050" y="274" width="150" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="24" fill="#111111">Year 2024</text>

  <rect x="638" y="299" width="468" height="15" rx="7.5" fill="url(#timelineGrad)"/>
  <circle cx="638" cy="306" r="20" fill="#c42f4a"/>
  <circle cx="872" cy="306" r="20" fill="#6f263f"/>
  <circle cx="1106" cy="306" r="20" fill="#112b46"/>

  <text x="578" y="358" width="150" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="16" fill="#555a60">
    <tspan x="638" dy="0">Led market scan</tspan>
    <tspan x="638" dy="20">and opportunity map</tspan>
  </text>
  <text x="812" y="358" width="150" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="16" fill="#555a60">
    <tspan x="872" dy="0">Built operating model</tspan>
    <tspan x="872" dy="20">for cross-team delivery</tspan>
  </text>
  <text x="1046" y="358" width="150" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="16" fill="#555a60">
    <tspan x="1106" dy="0">Scaled analytics practice</tspan>
    <tspan x="1106" dy="20">across three regions</tspan>
  </text>

  <text x="674" y="448" width="210" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="22" fill="#252525">Product Strategy</text>
  <rect x="670" y="456" width="398" height="26" rx="13" fill="#102944"/>
  <rect x="670" y="456" width="318" height="26" rx="13" fill="#637185"/>
  <text x="1082" y="476" width="60" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="16" fill="#637185">80%</text>

  <text x="674" y="518" width="210" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="22" fill="#252525">Data Storytelling</text>
  <rect x="670" y="526" width="398" height="26" rx="13" fill="#102944"/>
  <rect x="670" y="526" width="354" height="26" rx="13" fill="#637185"/>
  <text x="1082" y="546" width="60" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="16" fill="#637185">89%</text>

  <text x="674" y="588" width="210" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="22" fill="#252525">Team Enablement</text>
  <rect x="670" y="596" width="398" height="26" rx="13" fill="#102944"/>
  <rect x="670" y="596" width="278" height="26" rx="13" fill="#637185"/>
  <text x="1082" y="616" width="60" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="16" fill="#637185">70%</text>

  <path d="M1138 80 L1178 80 L1138 120 Z" fill="#8b1832" opacity="0.12"/>
  <text x="612" y="92" width="150" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" font-weight="700" fill="#8b1832" letter-spacing="2">EXPERT PROFILE</text>
</svg>
```

## Avoid in this skill
- ❌ Do not blur or mask a face using SVG filters; use a clean portrait crop or an abstract/non-identifying avatar image instead.
- ❌ Do not use `<mask>` for the circular avatar; use `<clipPath>` applied directly to the `<image>`.
- ❌ Do not make the dashboard with a centered, symmetrical two-column layout; the visual impact comes from the 35/65 asymmetric split.
- ❌ Do not use a single Unicode line or image for the skill bars; build them from editable rounded rectangles so percentages remain adjustable.
- ❌ Do not place `clip-path` on `<rect>`, `<circle>`, or `<g>` elements; PPT-Master only preserves clipping reliably on `<image>`.

## Composition notes
- Keep the left panel around 35–40% of the card width; it should feel like a dark identity anchor, not a narrow sidebar.
- Reserve the upper-right area for the expert name and tagline, then place timeline in the mid-band and skill bars in the lower-right third.
- Use maroon, navy, and muted slate as the data palette; keep gold only for rating stars or one small highlight.
- Leave generous white space around the timeline and bars so the right panel reads like an executive dashboard rather than a dense résumé.