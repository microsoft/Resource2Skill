# SVG Recipe — Geometric Anchored Character Profile (几何锚定人物介绍排版)

## Visual mechanism
A bold geometric color block anchors a circular portrait, while an offset wireframe and overlapping avatar create a polished 2.5D editorial layout. The right side stays text-forward with strict hierarchy: name, role, credentials, and compact proof points.

## SVG primitives needed
- 3× `<rect>` for the full-slide background, left anchor color block, and offset wireframe frame
- 1× `<image>` clipped by a circular `<clipPath>` for the portrait avatar
- 3× `<circle>` for avatar backing, white portrait border, and decorative dot accents
- 2× `<path>` for angular geometric accents / triangular brand decorations
- 1× `<line>` for a clean text divider
- 8× `<text>` for label, name, role, section heading, bullets, and small metadata
- 1× `<linearGradient>` for the blue anchor block
- 1× `<filter id="softShadow">` applied to the avatar backing and small card elements
- 1× `<filter id="blueGlow">` applied to geometric accent shapes for subtle depth
- 1× `<clipPath>` with a `<circle>` applied only to the portrait `<image>`

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="anchorBlue" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#1C6FAE"/>
      <stop offset="55%" stop-color="#2980B9"/>
      <stop offset="100%" stop-color="#4AA3DF"/>
    </linearGradient>

    <linearGradient id="palePanel" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="100%" stop-color="#F3F7FA"/>
    </linearGradient>

    <filter id="softShadow" x="-30%" y="-30%" width="160%" height="160%">
      <feOffset dx="0" dy="14" result="off"/>
      <feGaussianBlur in="off" stdDeviation="16" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="blueGlow" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="8"/>
    </filter>

    <clipPath id="avatarClip">
      <circle cx="438" cy="338" r="158"/>
    </clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#palePanel)"/>

  <rect x="0" y="0" width="430" height="720" fill="url(#anchorBlue)"/>
  <rect x="74" y="58" width="438" height="604" rx="0" fill="none" stroke="#111827" stroke-width="3"/>

  <path d="M42 610 L156 610 L88 676 Z" fill="#0F3555" opacity="0.25" filter="url(#blueGlow)"/>
  <path d="M332 82 L390 118 L332 154 Z" fill="#FFFFFF" opacity="0.18"/>
  <circle cx="102" cy="136" r="5" fill="#FFFFFF" opacity="0.45"/>
  <circle cx="128" cy="136" r="5" fill="#FFFFFF" opacity="0.45"/>
  <circle cx="154" cy="136" r="5" fill="#FFFFFF" opacity="0.45"/>

  <circle cx="438" cy="338" r="184" fill="#0B2540" opacity="0.16"/>
  <circle cx="438" cy="338" r="172" fill="#FFFFFF" filter="url(#softShadow)"/>
  <image
    href="https://images.example.com/executive-portrait-confident-founder-neutral-background.jpg"
    x="280" y="180" width="316" height="316"
    preserveAspectRatio="xMidYMid slice"
    clip-path="url(#avatarClip)"/>
  <circle cx="438" cy="338" r="158" fill="none" stroke="#FFFFFF" stroke-width="12"/>
  <circle cx="438" cy="338" r="171" fill="none" stroke="#111827" stroke-width="2" opacity="0.9"/>

  <text x="108" y="620" width="250" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#FFFFFF" opacity="0.8" letter-spacing="3">
    EXECUTIVE PROFILE
  </text>

  <text x="610" y="128" width="460" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#2980B9" letter-spacing="4">
    FOUNDER SPOTLIGHT
  </text>

  <text x="608" y="205" width="560" font-family="Segoe UI, Microsoft YaHei" font-size="58" font-weight="800" fill="#141414">
    <tspan>李彦宏</tspan>
    <tspan dx="18" font-size="38" font-weight="600" fill="#2D3748">Robin</tspan>
  </text>

  <text x="612" y="252" width="560" font-family="Segoe UI, Microsoft YaHei" font-size="24" font-weight="600" fill="#2980B9">
    百度公司创始人 / 董事长兼首席执行官
  </text>

  <line x1="612" y1="290" x2="1010" y2="290" stroke="#111827" stroke-width="2" opacity="0.18"/>

  <text x="612" y="335" width="520" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#111827">
    CAREER ANCHORS
  </text>

  <circle cx="622" cy="378" r="5" fill="#2980B9"/>
  <text x="642" y="384" width="500" font-family="Segoe UI, Microsoft YaHei" font-size="20" fill="#555B63">
    大数据科学与产业研究院名誉院长
  </text>

  <circle cx="622" cy="426" r="5" fill="#2980B9"/>
  <text x="642" y="432" width="500" font-family="Segoe UI, Microsoft YaHei" font-size="20" fill="#555B63">
    纽约州立大学计算机科学硕士
  </text>

  <circle cx="622" cy="474" r="5" fill="#2980B9"/>
  <text x="642" y="480" width="520" font-family="Segoe UI, Microsoft YaHei" font-size="20" fill="#555B63">
    引领中国搜索引擎与人工智能发展
  </text>

  <circle cx="622" cy="522" r="5" fill="#2980B9"/>
  <text x="642" y="528" width="540" font-family="Segoe UI, Microsoft YaHei" font-size="20" fill="#555B63">
    提出并践行“技术改变世界”的理念
  </text>

  <rect x="608" y="580" width="430" height="64" rx="18" fill="#FFFFFF" filter="url(#softShadow)"/>
  <text x="635" y="607" width="360" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#2980B9">
    DESIGN NOTE
  </text>
  <text x="635" y="632" width="360" font-family="Segoe UI, Microsoft YaHei" font-size="17" fill="#5E6670">
    Circular crop hides photo clutter; geometry creates authority.
  </text>
</svg>
```

## Avoid in this skill
- ❌ Do not use `<mask>` to cut out the portrait; use `<clipPath>` on the `<image>` only.
- ❌ Do not apply `clip-path` to decorative circles, frames, or text; PowerPoint translation preserves clipping reliably for images only.
- ❌ Do not use `<textPath>` for curved profile labels; keep profile labels as normal editable `<text>`.
- ❌ Do not build arrowheads with `marker-end`; this layout rarely needs arrows, and marker heads may disappear.
- ❌ Avoid a centered passport-photo layout; the impact comes from asymmetric overlap between the color block, portrait, and text field.

## Composition notes
- Keep the left 35–40% as the geometric anchor zone; the portrait should overlap the vertical boundary into the white text area.
- Reserve the right 55–60% for clean hierarchy: small label, large name, role, divider, then credentials.
- Use one dominant accent color, then repeat it in bullets, labels, and tiny geometric accents for rhythm.
- The wireframe should be offset from the solid block and intersect the avatar to create architectural depth without crowding the face.