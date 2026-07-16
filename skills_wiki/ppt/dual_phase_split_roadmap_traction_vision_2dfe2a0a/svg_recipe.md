# SVG Recipe — Dual-Phase Split Roadmap (Traction & Vision)

## Visual mechanism
A pitch-deck timeline is split into two equal color fields: grounded dark “traction already achieved” on the left and energetic “vision / roadmap” on the right. A single continuous axis crosses the split, with milestone nodes alternating above and below to imply execution momentum carrying into future ambition.

## SVG primitives needed
- 2× large `<rect>` for the 50/50 past/future background split
- 4× translucent `<rect>` overlays for soft depth, header bands, and milestone label panels
- 1× `<rect>` for the continuous horizontal timeline axis
- 1× narrow `<rect>` for the “TODAY” divider tick
- 7× `<circle>` for timeline nodes and inner dots
- 6× small rounded `<rect>` cards for partner/customer logo pills
- 2× large low-opacity `<text>` labels for ghosted era typography
- 18× `<text>` blocks for title, era headers, dates, metrics, captions, and logo labels
- 2× `<linearGradient>` definitions for premium background toning and metric card fills
- 1× `<filter id="nodeShadow">` applied to circles for floating node depth
- 1× `<filter id="softShadow">` applied to milestone cards and logo pills

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="pastDepth" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#0F172A"/>
      <stop offset="100%" stop-color="#172554"/>
    </linearGradient>
    <linearGradient id="futureDepth" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#FF6B6B"/>
      <stop offset="100%" stop-color="#F97316"/>
    </linearGradient>
    <linearGradient id="glassCard" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.24"/>
      <stop offset="100%" stop-color="#FFFFFF" stop-opacity="0.10"/>
    </linearGradient>
    <filter id="nodeShadow" x="-40%" y="-40%" width="180%" height="180%">
      <feOffset dx="0" dy="8"/>
      <feGaussianBlur stdDeviation="7"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="softShadow" x="-25%" y="-25%" width="150%" height="150%">
      <feOffset dx="0" dy="10"/>
      <feGaussianBlur stdDeviation="10"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <!-- Split background -->
  <rect x="0" y="0" width="640" height="720" fill="url(#pastDepth)"/>
  <rect x="640" y="0" width="640" height="720" fill="url(#futureDepth)"/>
  <rect x="0" y="0" width="640" height="720" fill="#020617" opacity="0.16"/>
  <rect x="640" y="0" width="640" height="720" fill="#FFFFFF" opacity="0.06"/>

  <!-- Ghost era labels -->
  <text x="44" y="122" width="560" font-family="Segoe UI, Microsoft YaHei" font-size="76" font-weight="800" fill="#FFFFFF" opacity="0.08">TRACTION</text>
  <text x="690" y="122" width="540" font-family="Segoe UI, Microsoft YaHei" font-size="76" font-weight="800" fill="#FFFFFF" opacity="0.16">VISION</text>

  <!-- Main title and section headers -->
  <text x="58" y="58" width="520" font-family="Segoe UI, Microsoft YaHei" font-size="30" font-weight="700" fill="#FFFFFF">Traction &amp; Roadmap</text>
  <text x="58" y="166" width="360" font-family="Segoe UI, Microsoft YaHei" font-size="28" font-weight="800" fill="#FFFFFF">PAST 9 MONTHS</text>
  <text x="864" y="166" width="360" font-family="Segoe UI, Microsoft YaHei" font-size="28" font-weight="800" text-anchor="end" fill="#FFFFFF">NEXT 9 MONTHS</text>
  <text x="1024" y="58" width="200" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" text-anchor="end" fill="#FFFFFF" opacity="0.78">Investor update · Q3</text>

  <!-- Timeline axis -->
  <rect x="86" y="398" width="1108" height="8" rx="4" fill="#FFFFFF" opacity="0.94"/>
  <rect x="637" y="342" width="6" height="120" rx="3" fill="#FFFFFF" opacity="0.92"/>
  <text x="590" y="328" width="100" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="800" text-anchor="middle" fill="#FFFFFF">TODAY</text>

  <!-- Past milestone cards -->
  <rect x="92" y="214" width="188" height="126" rx="22" fill="url(#glassCard)" stroke="#FFFFFF" stroke-opacity="0.18" filter="url(#softShadow)"/>
  <text x="118" y="252" width="140" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#CBD5E1">Month 1</text>
  <text x="118" y="292" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="800" fill="#FFFFFF">MVP</text>
  <text x="118" y="319" width="142" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#DDE7F3">Launched private beta</text>

  <rect x="296" y="468" width="204" height="128" rx="22" fill="url(#glassCard)" stroke="#FFFFFF" stroke-opacity="0.18" filter="url(#softShadow)"/>
  <text x="322" y="506" width="152" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#CBD5E1">Month 5</text>
  <text x="322" y="546" width="156" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="800" fill="#FFFFFF">€150K</text>
  <text x="322" y="573" width="156" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#DDE7F3">Booked annual revenue</text>

  <rect x="456" y="214" width="172" height="126" rx="22" fill="url(#glassCard)" stroke="#FFFFFF" stroke-opacity="0.18" filter="url(#softShadow)"/>
  <text x="482" y="252" width="120" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#CBD5E1">Month 9</text>
  <text x="482" y="292" width="124" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="800" fill="#FFFFFF">12</text>
  <text x="482" y="319" width="124" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#DDE7F3">Enterprise pilots live</text>

  <!-- Future milestone cards -->
  <rect x="688" y="468" width="198" height="128" rx="22" fill="#FFFFFF" opacity="0.22" stroke="#FFFFFF" stroke-opacity="0.32" filter="url(#softShadow)"/>
  <text x="714" y="506" width="146" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#FFE7E7">Month 12</text>
  <text x="714" y="546" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="800" fill="#FFFFFF">3×</text>
  <text x="714" y="573" width="148" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#FFF2F2">Pipeline conversion push</text>

  <rect x="892" y="214" width="188" height="126" rx="22" fill="#FFFFFF" opacity="0.22" stroke="#FFFFFF" stroke-opacity="0.32" filter="url(#softShadow)"/>
  <text x="918" y="252" width="136" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#FFE7E7">Month 15</text>
  <text x="918" y="292" width="140" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="800" fill="#FFFFFF">US</text>
  <text x="918" y="319" width="136" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#FFF2F2">Launch first market pod</text>

  <rect x="1032" y="468" width="164" height="128" rx="22" fill="#FFFFFF" opacity="0.22" stroke="#FFFFFF" stroke-opacity="0.32" filter="url(#softShadow)"/>
  <text x="1058" y="506" width="112" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#FFE7E7">Month 18</text>
  <text x="1058" y="546" width="116" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="800" fill="#FFFFFF">€1.2M</text>
  <text x="1058" y="573" width="112" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#FFF2F2">ARR target run-rate</text>

  <!-- Timeline nodes -->
  <circle cx="178" cy="402" r="22" fill="#FFFFFF" filter="url(#nodeShadow)"/>
  <circle cx="178" cy="402" r="8" fill="#38BDF8"/>
  <circle cx="398" cy="402" r="22" fill="#FFFFFF" filter="url(#nodeShadow)"/>
  <circle cx="398" cy="402" r="8" fill="#38BDF8"/>
  <circle cx="542" cy="402" r="22" fill="#FFFFFF" filter="url(#nodeShadow)"/>
  <circle cx="542" cy="402" r="8" fill="#38BDF8"/>
  <circle cx="787" cy="402" r="24" fill="#FFFFFF" filter="url(#nodeShadow)"/>
  <circle cx="787" cy="402" r="8" fill="#FF6B6B"/>
  <circle cx="986" cy="402" r="24" fill="#FFFFFF" filter="url(#nodeShadow)"/>
  <circle cx="986" cy="402" r="8" fill="#FF6B6B"/>
  <circle cx="1114" cy="402" r="24" fill="#FFFFFF" filter="url(#nodeShadow)"/>
  <circle cx="1114" cy="402" r="8" fill="#FF6B6B"/>

  <!-- Partner/logo proof strip -->
  <text x="58" y="655" width="240" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#CBD5E1" opacity="0.9">Current customers</text>
  <rect x="58" y="672" width="86" height="28" rx="14" fill="#FFFFFF" opacity="0.16"/>
  <text x="101" y="691" width="70" font-family="Segoe UI, Microsoft YaHei" font-size="11" font-weight="800" text-anchor="middle" fill="#FFFFFF">ACME</text>
  <rect x="154" y="672" width="86" height="28" rx="14" fill="#FFFFFF" opacity="0.16"/>
  <text x="197" y="691" width="70" font-family="Segoe UI, Microsoft YaHei" font-size="11" font-weight="800" text-anchor="middle" fill="#FFFFFF">NOVA</text>
  <rect x="250" y="672" width="86" height="28" rx="14" fill="#FFFFFF" opacity="0.16"/>
  <text x="293" y="691" width="70" font-family="Segoe UI, Microsoft YaHei" font-size="11" font-weight="800" text-anchor="middle" fill="#FFFFFF">MILO</text>

  <text x="908" y="655" width="240" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#FFF1F2" opacity="0.95">Target partners</text>
  <rect x="908" y="672" width="86" height="28" rx="14" fill="#FFFFFF" opacity="0.22"/>
  <text x="951" y="691" width="70" font-family="Segoe UI, Microsoft YaHei" font-size="11" font-weight="800" text-anchor="middle" fill="#FFFFFF">AWS</text>
  <rect x="1004" y="672" width="86" height="28" rx="14" fill="#FFFFFF" opacity="0.22"/>
  <text x="1047" y="691" width="70" font-family="Segoe UI, Microsoft YaHei" font-size="11" font-weight="800" text-anchor="middle" fill="#FFFFFF">HubSpot</text>
  <rect x="1100" y="672" width="86" height="28" rx="14" fill="#FFFFFF" opacity="0.22"/>
  <text x="1143" y="691" width="70" font-family="Segoe UI, Microsoft YaHei" font-size="11" font-weight="800" text-anchor="middle" fill="#FFFFFF">Stripe</text>
</svg>
```

## Avoid in this skill
- ❌ Using a single-color timeline background; it weakens the psychological separation between achieved traction and projected roadmap.
- ❌ Placing every milestone above the axis; alternate top/bottom cards to preserve breathing room and rhythm.
- ❌ Using `marker-end` arrows on the timeline path; if you need directionality, use a tapered `<path>` or simple text labels instead.
- ❌ Applying `clip-path` to text, cards, or nodes; keep clipping only for images if you add customer logos or founder photos.
- ❌ Making the future side visually quieter than the past side; the future half should feel energetic but still credible.

## Composition notes
- Keep the vertical split exactly at x=640 on a 1280×720 canvas; the hard boundary is the core storytelling device.
- Place the axis slightly below center, around y=400, leaving generous space for large milestone cards above and below.
- Use cool colors and factual labels on the left, warm colors and aspirational metrics on the right.
- Add logo pills near the bottom edge as proof points, but keep them secondary so the timeline nodes remain the visual focus.