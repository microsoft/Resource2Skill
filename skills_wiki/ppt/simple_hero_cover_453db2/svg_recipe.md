# SVG Recipe — Simple Hero Cover

## Visual mechanism
A minimal editorial cover pairs one oversized headline block with a large, cinematic hero image crop. The image carries the emotional weight, while subtle gradients, soft shadow, and restrained accent shapes make the slide feel premium without adding density.

## SVG primitives needed
- 1× `<rect>` for the full-slide gradient background
- 1× `<image>` for the 16:9 hero photograph
- 1× `<clipPath>` with rounded `<rect>` for the hero image crop
- 2× `<rect>` for the hero card shadow and rounded border/overlay
- 2× `<path>` for soft organic brand-color shapes behind the image
- 1× `<circle>` for a faint radial glow accent
- 1× `<linearGradient>` for the background wash
- 1× `<linearGradient>` for the hero image tonal overlay
- 1× `<linearGradient>` for accent fills
- 1× `<radialGradient>` for the glow accent
- 2× `<filter>` definitions: one soft shadow and one blurred glow
- 4× `<text>` blocks for eyebrow, headline, caption, and small footer metadata
- 2× small `<rect>` capsules for editorial labels/accent bars

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgWash" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#F8FAFC"/>
      <stop offset="52%" stop-color="#EEF4FF"/>
      <stop offset="100%" stop-color="#F9FAFB"/>
    </linearGradient>

    <linearGradient id="brandAccent" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#2563EB"/>
      <stop offset="48%" stop-color="#7C3AED"/>
      <stop offset="100%" stop-color="#06B6D4"/>
    </linearGradient>

    <linearGradient id="photoVeil" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.00"/>
      <stop offset="58%" stop-color="#111827" stop-opacity="0.04"/>
      <stop offset="100%" stop-color="#111827" stop-opacity="0.28"/>
    </linearGradient>

    <radialGradient id="orbGlow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#60A5FA" stop-opacity="0.38"/>
      <stop offset="70%" stop-color="#60A5FA" stop-opacity="0.10"/>
      <stop offset="100%" stop-color="#60A5FA" stop-opacity="0"/>
    </radialGradient>

    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset in="SourceAlpha" dx="0" dy="18" result="offset"/>
      <feGaussianBlur in="offset" stdDeviation="18" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="blurGlow" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="28"/>
    </filter>

    <clipPath id="heroClip">
      <rect x="690" y="72" width="500" height="576" rx="38" ry="38"/>
    </clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgWash)"/>

  <circle cx="1135" cy="112" r="190" fill="url(#orbGlow)"/>

  <path d="M742 94 C810 30 934 36 1018 82 C1114 134 1187 228 1175 326 C1163 425 1042 442 938 421 C834 400 740 377 704 294 C670 216 684 149 742 94 Z"
        fill="url(#brandAccent)" opacity="0.20" filter="url(#blurGlow)"/>

  <path d="M1020 478 C1094 442 1188 472 1222 540 C1260 614 1198 681 1118 690 C1038 700 967 657 958 590 C951 539 974 501 1020 478 Z"
        fill="#06B6D4" opacity="0.16" filter="url(#blurGlow)"/>

  <rect x="690" y="72" width="500" height="576" rx="38" ry="38"
        fill="#111827" opacity="0.20" filter="url(#softShadow)"/>

  <image href="https://images.example.com/hero-cover/futuristic-workspace-wide-16x9.jpg"
         x="690" y="72" width="500" height="576"
         preserveAspectRatio="xMidYMid slice"
         clip-path="url(#heroClip)"/>

  <rect x="690" y="72" width="500" height="576" rx="38" ry="38"
        fill="url(#photoVeil)" opacity="0.92"/>

  <rect x="690" y="72" width="500" height="576" rx="38" ry="38"
        fill="none" stroke="#FFFFFF" stroke-width="2" opacity="0.78"/>

  <rect x="88" y="92" width="112" height="8" rx="4" fill="url(#brandAccent)"/>
  <rect x="88" y="116" width="236" height="30" rx="15" fill="#E0EAFF"/>

  <text x="108" y="137" width="300"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="14" font-weight="700" letter-spacing="2.5"
        fill="#2563EB">2026 STRATEGY BRIEF</text>

  <text x="84" y="238" width="560"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="84" font-weight="800" letter-spacing="-3.2"
        fill="#0F172A">
    <tspan x="84" dy="0">Move</tspan>
    <tspan x="84" dy="94">Faster Than</tspan>
    <tspan x="84" dy="94" fill="#2563EB">the Market</tspan>
  </text>

  <text x="90" y="540" width="470"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="24" font-weight="400" letter-spacing="-0.2"
        fill="#475569">
    A concise executive narrative for launching bold initiatives with clarity, speed, and conviction.
  </text>

  <rect x="728" y="584" width="258" height="44" rx="22"
        fill="#FFFFFF" opacity="0.88"/>

  <text x="752" y="612" width="220"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="15" font-weight="700"
        fill="#0F172A">Hero Image / Core Theme</text>

  <text x="90" y="656" width="380"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="14" font-weight="600" letter-spacing="1.1"
        fill="#94A3B8">CONFIDENTIAL · BOARD READOUT</text>
</svg>
```

## Avoid in this skill
- ❌ Do not place headline text directly over a busy full-bleed photo unless a strong editable gradient veil or solid text panel is added.
- ❌ Do not use `<mask>` for image fades; use rounded image clipping plus editable overlay rectangles instead.
- ❌ Do not clip decorative paths or rectangles; clip only the `<image>` if a custom crop is required.
- ❌ Do not overpopulate the cover with bullets, charts, or multiple content cards; this layout depends on low density.
- ❌ Do not use tiny headline type. The title should feel like the dominant object, not a label.

## Composition notes
- Keep the headline in the left 45–50% of the canvas, with generous negative space around it.
- Let the hero image occupy roughly 40% of slide width and 75–85% of slide height for a keynote-style presence.
- Use soft brand-color glows behind the image to connect the photo and typography without adding clutter.
- Maintain a restrained palette: near-black headline, one vivid accent color, pale background, and photo-derived neutrals.