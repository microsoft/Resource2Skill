# SVG Recipe — Kinetic Sliced-Typography Hero Layout

## Visual mechanism
A high-energy poster layout built from oversized white typography, horizontal “slice” interruptions, and a central transparent cutout subject interleaved between background and foreground text. The depth comes from strict Z-order: gradient field → rear text → cutout subject → front sliced headline.

## SVG primitives needed
- 1× `<rect>` for the full-slide saturated gradient background
- 8–12× `<path>` for diagonal speed streaks, angular shards, and kinetic accent slashes
- 6–10× large `<text>` elements for layered background and foreground typography
- 6–12× thin `<rect>` / `<path>` overlays for horizontal slice cuts and displaced glitch strips
- 1× `<image>` for the central transparent PNG cutout subject or product
- 1× `<ellipse>` for the subject ground shadow
- 1× `<linearGradient id="bgGrad">` for the warm purple-to-magenta hero background
- 2–3× accent gradients for cyan/magenta slice flashes
- 1× `<filter id="softShadow">` applied to ellipse/path/text shapes for depth
- 1× `<filter id="typeGlow">` applied sparingly to foreground typography for premium glow

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#35105A"/>
      <stop offset="42%" stop-color="#7E258C"/>
      <stop offset="100%" stop-color="#E3478A"/>
    </linearGradient>

    <linearGradient id="cyanFlash" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#00E5FF" stop-opacity="0"/>
      <stop offset="45%" stop-color="#00E5FF" stop-opacity="0.95"/>
      <stop offset="100%" stop-color="#FFFFFF" stop-opacity="0"/>
    </linearGradient>

    <linearGradient id="hotFlash" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#FF2F7D" stop-opacity="0"/>
      <stop offset="52%" stop-color="#FF2F7D" stop-opacity="0.9"/>
      <stop offset="100%" stop-color="#FFD166" stop-opacity="0"/>
    </linearGradient>

    <filter id="softShadow" x="-30%" y="-30%" width="160%" height="160%">
      <feOffset dx="0" dy="16"/>
      <feGaussianBlur stdDeviation="18"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="typeGlow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="3"/>
    </filter>
  </defs>

  <!-- Saturated poster background -->
  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>

  <!-- Overscale kinetic backdrop streaks -->
  <path d="M-60 118 L454 42 L428 70 L-84 154 Z" fill="#FFFFFF" opacity="0.09"/>
  <path d="M816 28 L1348 0 L1308 36 L792 64 Z" fill="#FFFFFF" opacity="0.10"/>
  <path d="M-80 626 L560 544 L530 584 L-110 676 Z" fill="#FFDAF0" opacity="0.12"/>
  <path d="M742 622 L1394 534 L1364 588 L714 674 Z" fill="#2CF3FF" opacity="0.13"/>
  <path d="M100 280 L380 244 L362 264 L78 304 Z" fill="url(#cyanFlash)" opacity="0.75"/>
  <path d="M894 212 L1216 164 L1196 190 L872 238 Z" fill="url(#hotFlash)" opacity="0.85"/>

  <!-- Background typography: behind the subject -->
  <text x="-46" y="225" width="1420" font-family="Impact, Arial Black, Segoe UI, Microsoft YaHei" font-size="130" font-weight="900"
        letter-spacing="-4" fill="#FFFFFF" opacity="0.24" transform="rotate(-4 620 220)">VELOCITY</text>
  <text x="116" y="347" width="1120" font-family="Impact, Arial Black, Segoe UI, Microsoft YaHei" font-size="92" font-weight="900"
        letter-spacing="8" fill="#FFFFFF" opacity="0.16" transform="rotate(3 650 330)">ACCELERATE</text>
  <text x="618" y="128" width="720" font-family="Impact, Arial Black, Segoe UI, Microsoft YaHei" font-size="72" font-weight="900"
        letter-spacing="10" fill="#FFFFFF" opacity="0.14" transform="rotate(5 920 120)">MOTION</text>

  <!-- Slice cuts over rear type: background-colored bars create interrupted typography -->
  <rect x="42" y="174" width="770" height="13" rx="2" fill="#8B2A8C" opacity="0.98" transform="rotate(-4 420 180)"/>
  <rect x="310" y="258" width="570" height="10" rx="2" fill="#C63D8D" opacity="0.94" transform="rotate(-4 620 260)"/>
  <path d="M134 197 L438 168 L430 180 L126 210 Z" fill="#FFFFFF" opacity="0.54"/>
  <path d="M754 256 L1018 238 L1008 250 L744 270 Z" fill="#00E5FF" opacity="0.62"/>

  <!-- Premium graphic framing shards -->
  <path d="M156 428 L260 392 L288 416 L178 458 Z" fill="#FFFFFF" opacity="0.12"/>
  <path d="M1032 404 L1138 362 L1174 392 L1066 438 Z" fill="#FFFFFF" opacity="0.15"/>
  <path d="M910 88 L936 78 L950 150 L924 160 Z" fill="#FFD166" opacity="0.7"/>
  <path d="M282 98 L312 88 L296 182 L266 192 Z" fill="#00E5FF" opacity="0.62"/>

  <!-- Subject shadow sits between rear type and cutout -->
  <ellipse cx="664" cy="628" rx="220" ry="34" fill="#170820" opacity="0.45" filter="url(#softShadow)"/>

  <!-- Central transparent cutout subject/product. Use a real transparent PNG for production. -->
  <image x="436" y="94" width="420" height="560"
         href="https://images.example.com/transparent-cutout-sprinter-leaping-forward.png"
         xlink:href="https://images.example.com/transparent-cutout-sprinter-leaping-forward.png"/>

  <!-- Foreground headline: in front of subject -->
  <text x="82" y="604" width="1180" font-family="Impact, Arial Black, Segoe UI, Microsoft YaHei" font-size="154" font-weight="900"
        letter-spacing="-7" fill="#FFFFFF" opacity="0.96" filter="url(#typeGlow)">SPRINT</text>

  <!-- Foreground typography slicing: cover bands + displaced white/accent strips -->
  <rect x="58" y="486" width="1120" height="18" rx="3" fill="#B7378C" opacity="0.96" transform="rotate(-2 620 495)"/>
  <rect x="228" y="548" width="850" height="14" rx="2" fill="#63207B" opacity="0.98" transform="rotate(-2 650 554)"/>
  <path d="M122 494 L452 474 L442 490 L112 510 Z" fill="#FFFFFF" opacity="0.86"/>
  <path d="M520 489 L884 466 L874 482 L510 506 Z" fill="url(#cyanFlash)" opacity="0.95"/>
  <path d="M804 558 L1138 538 L1128 554 L794 574 Z" fill="#FFFFFF" opacity="0.78"/>
  <path d="M294 559 L548 540 L540 555 L286 574 Z" fill="url(#hotFlash)" opacity="0.9"/>

  <!-- Offset ghost copies suggest sliced type displacement without clipping text -->
  <text x="99" y="604" width="1180" font-family="Impact, Arial Black, Segoe UI, Microsoft YaHei" font-size="154" font-weight="900"
        letter-spacing="-7" fill="#00E5FF" opacity="0.16">SPRINT</text>
  <text x="63" y="604" width="1180" font-family="Impact, Arial Black, Segoe UI, Microsoft YaHei" font-size="154" font-weight="900"
        letter-spacing="-7" fill="#FF2F7D" opacity="0.13">SPRINT</text>

  <!-- Microcopy blocks balance the chaotic center -->
  <text x="66" y="64" width="330" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700"
        letter-spacing="3" fill="#FFFFFF" opacity="0.84">KINETIC HERO SYSTEM</text>
  <text x="66" y="91" width="350" font-family="Segoe UI, Microsoft YaHei" font-size="12"
        letter-spacing="1.4" fill="#F7CBE3" opacity="0.9">INTERLEAVED TYPE / CUTOUT / MOTION</text>

  <text x="1016" y="72" width="190" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700"
        letter-spacing="2.5" fill="#FFFFFF" opacity="0.86">SEASON 2026</text>
  <text x="1016" y="100" width="210" font-family="Segoe UI, Microsoft YaHei" font-size="36" font-weight="900"
        letter-spacing="-1" fill="#FFFFFF">03</text>

  <rect x="1012" y="608" width="178" height="42" rx="21" fill="none" stroke="#FFFFFF" stroke-width="2" opacity="0.72"/>
  <text x="1040" y="635" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700"
        letter-spacing="2" fill="#FFFFFF">LAUNCH MODE</text>
</svg>
```

## Avoid in this skill
- ❌ Do not use `clip-path` on `<text>` to make the slices; PPT-Master only preserves clipping reliably on `<image>`.
- ❌ Do not rely on SVG `<mask>` for text reveals or cutouts; it will hard-fail or be ignored.
- ❌ Do not use `<textPath>` for curved kinetic typography; it will be dropped.
- ❌ Do not use `skewX`, `skewY`, or `matrix(...)` transforms for speed distortion; use rotated paths and offset duplicate text instead.
- ❌ Do not put the subject image after the foreground headline unless you want to lose the interleaved depth effect.

## Composition notes
- Keep the subject centered or slightly off-center, occupying roughly 45–60% of slide height; it should break through the typography plane.
- Use two typography layers: pale oversized rear words behind the subject, then a dominant white foreground word across the lower third.
- The slice illusion works best with 2–3 thin horizontal cover bands plus displaced white/cyan/magenta strips aligned near letter strokes.
- Reserve small microcopy blocks in opposing corners so the slide feels designed, not merely chaotic.