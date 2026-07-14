# SVG Recipe — Deconstructed 3D Gradient Typography

## Visual mechanism
A single oversized word is duplicated into separated typographic layers: a dark stacked extrusion, a hot gradient face, a translucent glass fill, and a white wireframe outline. Offsetting these layers up-left and down-right turns flat typography into a floating architectural object with faux-3D depth.

## SVG primitives needed
- 1× `<rect>` for the full-slide radial gradient background.
- 2× `<radialGradient>` / `<linearGradient>` definitions for the moody background and hero text fill.
- 1× `<filter id="deepShadow">` applied to the distant shadow text.
- 1× `<filter id="neonGlow">` applied to the hero gradient text for luminous edge bloom.
- 12–18× `<text>` for the stacked dark extrusion layers, each offset slightly down/right.
- 1× `<text>` for the distant black drop shadow.
- 1× `<text>` for the main gradient face.
- 1× `<text>` for the translucent glass layer offset up-left.
- 1× `<text>` for the white wireframe outline offset further up-left.
- 6–10× `<path>` for angular neon shards and depth accents around the type.
- 2–4× `<line>` for subtle perspective streaks or energy rays.

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <radialGradient id="bgRadial" cx="48%" cy="42%" r="76%">
      <stop offset="0%" stop-color="#3A0CA3"/>
      <stop offset="46%" stop-color="#21055F"/>
      <stop offset="100%" stop-color="#0B0228"/>
    </radialGradient>

    <linearGradient id="heroGrad" x1="300" y1="230" x2="980" y2="470" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#FF007F"/>
      <stop offset="38%" stop-color="#FF4FD8"/>
      <stop offset="72%" stop-color="#FF8A00"/>
      <stop offset="100%" stop-color="#FFD700"/>
    </linearGradient>

    <linearGradient id="shardGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#00E5FF" stop-opacity="0.95"/>
      <stop offset="100%" stop-color="#FF007F" stop-opacity="0.12"/>
    </linearGradient>

    <filter id="deepShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="18" dy="28"/>
      <feGaussianBlur stdDeviation="9"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="neonGlow" x="-15%" y="-20%" width="130%" height="140%">
      <feGaussianBlur stdDeviation="4"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgRadial)"/>

  <path d="M91 151 L268 111 L245 132 L96 173 Z" fill="url(#shardGrad)" opacity="0.45"/>
  <path d="M1015 170 L1194 118 L1170 148 L1028 198 Z" fill="#FF007F" opacity="0.22"/>
  <path d="M930 555 L1178 510 L1150 546 L919 589 Z" fill="url(#shardGrad)" opacity="0.28"/>
  <path d="M122 535 L342 585 L304 603 L99 557 Z" fill="#FFD700" opacity="0.18"/>
  <path d="M835 105 L878 75 L952 86 L891 123 Z" fill="#00E5FF" opacity="0.18"/>
  <path d="M315 246 L360 230 L392 242 L335 265 Z" fill="#FFFFFF" opacity="0.16"/>

  <line x1="96" y1="386" x2="318" y2="322" stroke="#00E5FF" stroke-width="2" opacity="0.34"/>
  <line x1="960" y1="326" x2="1192" y2="258" stroke="#FF007F" stroke-width="2" opacity="0.35"/>
  <line x1="855" y1="488" x2="1118" y2="432" stroke="#FFD700" stroke-width="1.5" opacity="0.28"/>

  <text x="640" y="410" width="1280" text-anchor="middle"
        font-family="Arial Black, Segoe UI, Microsoft YaHei" font-size="158" font-weight="900"
        letter-spacing="-8" fill="#000000" opacity="0.42" filter="url(#deepShadow)">VELOCITY</text>

  <text x="650" y="395" width="1280" text-anchor="middle" font-family="Arial Black, Segoe UI, Microsoft YaHei" font-size="158" font-weight="900" letter-spacing="-8" fill="#25004D" opacity="0.96">VELOCITY</text>
  <text x="646" y="390" width="1280" text-anchor="middle" font-family="Arial Black, Segoe UI, Microsoft YaHei" font-size="158" font-weight="900" letter-spacing="-8" fill="#310063" opacity="0.96">VELOCITY</text>
  <text x="642" y="385" width="1280" text-anchor="middle" font-family="Arial Black, Segoe UI, Microsoft YaHei" font-size="158" font-weight="900" letter-spacing="-8" fill="#3C007A" opacity="0.96">VELOCITY</text>
  <text x="638" y="380" width="1280" text-anchor="middle" font-family="Arial Black, Segoe UI, Microsoft YaHei" font-size="158" font-weight="900" letter-spacing="-8" fill="#470091" opacity="0.96">VELOCITY</text>
  <text x="634" y="375" width="1280" text-anchor="middle" font-family="Arial Black, Segoe UI, Microsoft YaHei" font-size="158" font-weight="900" letter-spacing="-8" fill="#5200A8" opacity="0.96">VELOCITY</text>
  <text x="630" y="370" width="1280" text-anchor="middle" font-family="Arial Black, Segoe UI, Microsoft YaHei" font-size="158" font-weight="900" letter-spacing="-8" fill="#5D00BF" opacity="0.94">VELOCITY</text>
  <text x="626" y="365" width="1280" text-anchor="middle" font-family="Arial Black, Segoe UI, Microsoft YaHei" font-size="158" font-weight="900" letter-spacing="-8" fill="#6700D6" opacity="0.92">VELOCITY</text>
  <text x="622" y="360" width="1280" text-anchor="middle" font-family="Arial Black, Segoe UI, Microsoft YaHei" font-size="158" font-weight="900" letter-spacing="-8" fill="#7200EE" opacity="0.88">VELOCITY</text>

  <text x="612" y="339" width="1280" text-anchor="middle"
        font-family="Arial Black, Segoe UI, Microsoft YaHei" font-size="158" font-weight="900"
        letter-spacing="-8" fill="#FFFFFF" opacity="0.18">VELOCITY</text>

  <text x="640" y="354" width="1280" text-anchor="middle"
        font-family="Arial Black, Segoe UI, Microsoft YaHei" font-size="158" font-weight="900"
        letter-spacing="-8" fill="url(#heroGrad)" stroke="#FFFFFF" stroke-width="1.2"
        opacity="1" filter="url(#neonGlow)">VELOCITY</text>

  <text x="592" y="319" width="1280" text-anchor="middle"
        font-family="Arial Black, Segoe UI, Microsoft YaHei" font-size="158" font-weight="900"
        letter-spacing="-8" fill="none" stroke="#FFFFFF" stroke-width="2.4"
        opacity="0.92">VELOCITY</text>

  <text x="640" y="610" width="1280" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei" font-size="22" font-weight="600"
        letter-spacing="6" fill="#FFFFFF" opacity="0.72">DECONSTRUCTED MOTION SYSTEM</text>
</svg>
```

## Avoid in this skill
- ❌ Do not use `<textPath>` to bend the hero word; it will not translate reliably and weakens the architectural stacked-text mechanism.
- ❌ Do not use `<mask>` or clip-path on text to fake broken letters; clipping is only safe for `<image>` in this workflow.
- ❌ Do not rely on SVG/CSS blend modes such as `mix-blend-mode`, because PowerPoint will not preserve them as editable typography.
- ❌ Do not use `skewX`, `skewY`, or matrix transforms for perspective; build depth with repeated offset text layers instead.
- ❌ Do not put `filter` on `<line>` energy streaks; filters on lines are dropped.

## Composition notes
- Keep the word huge, usually 75–95% of slide width, with the face layer centered and extrusion drifting down/right.
- Leave generous dark negative space around the top-left wireframe offset so the separated layer reads clearly.
- Use a tight palette: deep violet background, indigo extrusion, white outlines, and one aggressive gradient such as pink-to-gold or cyan-to-magenta.
- Add only a few angular shards or streaks; they should amplify motion and depth, not compete with the typography.