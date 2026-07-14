# SVG Recipe — 3D Morphing Reveal Window (Spatial Narrative)

## Visual mechanism
A background “destination” image sits behind a pair of wooden window doors; the doors are drawn in closed and opened perspective states so PowerPoint Morph can interpolate them into a sweeping reveal. The illusion comes from hinge-side anchoring, trapezoid perspective panels, thick dark side edges, frosted glass, and a strong directional arrow suggesting the swing path.

## SVG primitives needed
- 1× `<rect>` for the full-slide interior wall background.
- 1× `<radialGradient>` and 2× `<linearGradient>` for wall glow, wood depth, and frosted glass.
- 1× `<filter id="softShadow">` for pane/window depth shadows.
- 1× `<filter id="titleLift">` for the large headline shadow.
- 1× `<clipPath>` with rounded `<rect>` applied only to the reveal `<image>`.
- 1× `<image>` for the city/landscape reveal view.
- 10× `<rect>` for flat closed-window frames, rails, mullions, and central reveal frame.
- 12× `<path>` for perspective open-window trapezoids, side-thickness strips, glass panels, arrow swoosh, arrowhead, and decorative highlights.
- 3× `<circle>` / `<rect>` combinations for the PowerPoint-style icon badge.
- 2× `<text>` elements with explicit `width` for the headline and small cue label.

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <radialGradient id="wallGlow" cx="50%" cy="20%" r="75%">
      <stop offset="0%" stop-color="#f6fbff"/>
      <stop offset="55%" stop-color="#c8e6f7"/>
      <stop offset="100%" stop-color="#79b7df"/>
    </radialGradient>

    <linearGradient id="woodFace" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#a45117"/>
      <stop offset="45%" stop-color="#7a3007"/>
      <stop offset="100%" stop-color="#4e1b03"/>
    </linearGradient>

    <linearGradient id="woodEdge" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#2b0d02"/>
      <stop offset="100%" stop-color="#8b3908"/>
    </linearGradient>

    <linearGradient id="glassTint" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#eefcde" stop-opacity="0.86"/>
      <stop offset="65%" stop-color="#c9edbd" stop-opacity="0.64"/>
      <stop offset="100%" stop-color="#9fc6b0" stop-opacity="0.46"/>
    </linearGradient>

    <linearGradient id="redArrow" x1="410" y1="150" x2="780" y2="265">
      <stop offset="0%" stop-color="#e8172a"/>
      <stop offset="100%" stop-color="#b8071b"/>
    </linearGradient>

    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="8" dy="10" result="off"/>
      <feGaussianBlur in="off" stdDeviation="8" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="titleLift" x="-10%" y="-20%" width="120%" height="150%">
      <feOffset dx="4" dy="5" result="off"/>
      <feGaussianBlur in="off" stdDeviation="2.5" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <clipPath id="revealClip">
      <rect x="682" y="284" width="420" height="334" rx="4"/>
    </clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#wallGlow)"/>

  <!-- PowerPoint-like badge -->
  <circle cx="101" cy="82" r="66" fill="#f46b48" stroke="#ffffff" stroke-width="4" filter="url(#softShadow)"/>
  <path d="M101 16 A66 66 0 0 1 167 82 L101 82 Z" fill="#ff9b81" opacity="0.9"/>
  <path d="M101 82 L167 82 A66 66 0 0 1 101 148 Z" fill="#d94225" opacity="0.85"/>
  <rect x="17" y="44" width="76" height="78" rx="8" fill="#b93b21" stroke="#ffffff" stroke-width="4" filter="url(#softShadow)"/>
  <text x="34" y="102" width="50" font-family="Segoe UI, Microsoft YaHei" font-size="54" font-weight="800" fill="#ffffff">P</text>

  <!-- Headline -->
  <text x="205" y="110" width="930" font-family="Segoe UI, Microsoft YaHei" font-size="76" font-weight="900" letter-spacing="4" fill="#000000" stroke="#ffffff" stroke-width="3" paint-order="stroke" filter="url(#titleLift)">
    <tspan fill="#f30b18">3</tspan><tspan fill="#000000">D WINDOW ANIMATION</tspan>
  </text>

  <!-- Closed state window, left side -->
  <g filter="url(#softShadow)">
    <rect x="12" y="246" width="542" height="412" fill="url(#woodFace)"/>
    <rect x="38" y="273" width="219" height="166" fill="url(#glassTint)" stroke="#cfe8a9" stroke-width="6"/>
    <rect x="307" y="273" width="220" height="166" fill="url(#glassTint)" stroke="#cfe8a9" stroke-width="6"/>
    <rect x="38" y="462" width="219" height="166" fill="url(#glassTint)" stroke="#cfe8a9" stroke-width="6"/>
    <rect x="307" y="462" width="220" height="166" fill="url(#glassTint)" stroke="#cfe8a9" stroke-width="6"/>
    <rect x="12" y="246" width="26" height="412" fill="#8a3709"/>
    <rect x="257" y="246" width="30" height="412" fill="#692303"/>
    <rect x="527" y="246" width="27" height="412" fill="#5d2104"/>
    <rect x="38" y="439" width="489" height="23" fill="#743006"/>
    <rect x="12" y="246" width="542" height="14" fill="#a95618" opacity="0.9"/>
  </g>

  <!-- Red morph cue arrow -->
  <path d="M394 246 C493 144 632 91 692 155 C724 189 727 226 722 242 L777 205 L742 278 L629 233 L709 240 C705 214 695 189 673 170 C611 118 502 159 394 246 Z"
        fill="url(#redArrow)" opacity="0.97"/>
  <text x="486" y="191" width="220" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="700" fill="#b8071b">
    Morph: hinge panes outward
  </text>

  <!-- Open reveal window, right side -->
  <g filter="url(#softShadow)">
    <!-- central revealed view -->
    <rect x="662" y="269" width="462" height="367" fill="url(#woodFace)"/>
    <image href="https://images.example.com/wide-city-park-skyline-reveal.jpg"
           x="682" y="284" width="420" height="334" preserveAspectRatio="xMidYMid slice" clip-path="url(#revealClip)"/>
    <rect x="682" y="284" width="420" height="334" fill="none" stroke="#6f2905" stroke-width="12"/>

    <!-- left door swung inward/outward in perspective -->
    <path d="M572 246 L598 240 L598 664 L572 660 Z" fill="#2b0d02"/>
    <path d="M598 240 L685 274 L685 628 L598 664 Z" fill="url(#woodFace)"/>
    <path d="M611 280 L674 302 L674 434 L611 424 Z" fill="url(#glassTint)" stroke="#cfe8a9" stroke-width="5"/>
    <path d="M611 454 L674 466 L674 599 L611 610 Z" fill="url(#glassTint)" stroke="#cfe8a9" stroke-width="5"/>
    <path d="M598 240 L685 274 L685 289 L598 256 Z" fill="#a95618" opacity="0.8"/>
    <path d="M598 434 L685 447 L685 466 L598 454 Z" fill="#6f2905"/>
    <path d="M652 287 L685 299 L685 622 L652 635 Z" fill="#0b0b0b" opacity="0.14"/>

    <!-- right door swung outward in perspective -->
    <path d="M1102 274 L1234 242 L1254 248 L1122 284 Z" fill="#a95618"/>
    <path d="M1102 274 L1234 242 L1234 660 L1102 628 Z" fill="url(#woodFace)"/>
    <path d="M1234 242 L1254 248 L1254 662 L1234 660 Z" fill="#4a1702"/>
    <path d="M1116 300 L1215 276 L1215 434 L1116 434 Z" fill="url(#glassTint)" stroke="#cfe8a9" stroke-width="5"/>
    <path d="M1116 466 L1215 462 L1215 627 L1116 602 Z" fill="url(#glassTint)" stroke="#cfe8a9" stroke-width="5"/>
    <path d="M1102 434 L1234 435 L1234 462 L1102 466 Z" fill="#6f2905"/>
    <path d="M1102 274 L1122 284 L1122 628 L1102 628 Z" fill="#8a3709"/>
  </g>

  <!-- subtle floor/contact shadows -->
  <ellipse cx="283" cy="670" rx="270" ry="20" fill="#1f5b7a" opacity="0.16"/>
  <ellipse cx="917" cy="668" rx="345" ry="22" fill="#1f5b7a" opacity="0.18"/>
</svg>
```

## Avoid in this skill
- ❌ Do not rely on real SVG or CSS 3D transforms; PPT translation will not preserve `rotateY`, `perspective`, `matrix3d`, or CSS transform origins as editable PowerPoint shapes.
- ❌ Do not use `<mask>` to reveal the city image; use a `<clipPath>` applied directly to the `<image>` only.
- ❌ Do not use `marker-end` for the red arrow; draw the arrow swoosh and arrowhead as filled `<path>` shapes.
- ❌ Do not group pane parts and expect Morph to understand a single “door” unless the PPT author keeps object names consistent across the closed/open slides.
- ❌ Do not apply filters to `<line>` elements; use filtered `<rect>`/`<path>` pane groups instead.

## Composition notes
- Keep the reveal image on the back layer and frame it with a thick central wood border; the doors should visibly sit in front of the photo.
- For the Morph pair, slide 1 should use two flat rectangular panes meeting at center; slide 2 should replace them with hinge-anchored trapezoid panes positioned outward.
- Leave generous negative space above the windows for a large keynote headline and an arc arrow that explains the swing direction.
- Use warm brown wood against a cool blue wall so the window architecture reads clearly while the revealed photo becomes the emotional focal point.