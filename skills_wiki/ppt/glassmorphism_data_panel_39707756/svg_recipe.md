# SVG Recipe — Glassmorphism Data Panel

## Visual mechanism
A semi-transparent rounded data panel floats above a rich photographic background, using a clipped pre-blurred crop of the same background to simulate frosted glass. Soft shadow, faint white border, translucent overlays, and crisp KPI content create a premium “glass UI” layer suitable for Morph-style slide movement.

## SVG primitives needed
- 1× full-slide `<image>` for the sharp photographic background
- 1× clipped `<image>` for the pre-blurred background crop inside the glass panel
- 1× `<clipPath>` with rounded `<rect>` for the glass panel crop
- 1× `<filter id="panelShadow">` using `feOffset + feGaussianBlur + feMerge` for floating panel depth
- 1× `<filter id="softGlow">` using `feGaussianBlur` for accent glow behind the call-to-action
- 5× large `<rect>` for glass body, border, top highlight, KPI tiles, and button surfaces
- 4× `<path>` for decorative trend lines, UI glyphs, and organic light streaks
- 3× `<circle>` for status dots and small decorative bokeh accents
- Multiple `<text>` elements with explicit `width` attributes for title, subtitle, metrics, labels, and button copy
- 2× `<linearGradient>` for glass sheen and accent button fill
- 1× `<radialGradient>` for atmospheric background glow

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <clipPath id="glassClip">
      <rect x="650" y="86" width="492" height="548" rx="34" ry="34"/>
    </clipPath>

    <linearGradient id="glassSheen" x1="650" y1="86" x2="1142" y2="634" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#FFFFFF" stop-opacity="0.46"/>
      <stop offset="0.42" stop-color="#FFFFFF" stop-opacity="0.12"/>
      <stop offset="1" stop-color="#FFFFFF" stop-opacity="0.04"/>
    </linearGradient>

    <linearGradient id="buttonGrad" x1="806" y1="552" x2="990" y2="552" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#FF9A3D"/>
      <stop offset="1" stop-color="#F05A28"/>
    </linearGradient>

    <radialGradient id="warmGlow" cx="28%" cy="28%" r="62%">
      <stop offset="0" stop-color="#FAD18A" stop-opacity="0.45"/>
      <stop offset="0.55" stop-color="#A55723" stop-opacity="0.12"/>
      <stop offset="1" stop-color="#12161F" stop-opacity="0"/>
    </radialGradient>

    <filter id="panelShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="20" result="off"/>
      <feGaussianBlur in="off" stdDeviation="22" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="softGlow" x="-80%" y="-80%" width="260%" height="260%">
      <feGaussianBlur stdDeviation="20"/>
    </filter>
  </defs>

  <image x="0" y="0" width="1280" height="720" preserveAspectRatio="xMidYMid slice"
         href="https://images.example.com/hero-background/wheat-calculator-coins-flatlay.jpg"/>

  <rect x="0" y="0" width="1280" height="720" fill="#111722" opacity="0.35"/>
  <rect x="0" y="0" width="1280" height="720" fill="url(#warmGlow)"/>

  <path d="M44,602 C196,520 298,650 452,574 C548,527 592,443 696,461"
        fill="none" stroke="#FFFFFF" stroke-opacity="0.16" stroke-width="2"/>
  <path d="M82,640 C234,562 354,684 508,610 C610,560 640,500 746,512"
        fill="none" stroke="#F79A32" stroke-opacity="0.22" stroke-width="3"/>

  <text x="88" y="128" width="470" font-family="Segoe UI, Microsoft YaHei" font-size="18"
        letter-spacing="3" fill="#FFFFFF" opacity="0.74">MARKET INTELLIGENCE</text>
  <text x="88" y="202" width="520" font-family="Segoe UI, Microsoft YaHei" font-size="58"
        font-weight="700" fill="#FFFFFF">Food economics</text>
  <text x="92" y="256" width="500" font-family="Segoe UI, Microsoft YaHei" font-size="22"
        fill="#FFFFFF" opacity="0.76">Live commodity signals, margin pressure, and regional demand patterns in one executive view.</text>

  <circle cx="138" cy="334" r="6" fill="#FF9A3D"/>
  <text x="158" y="342" width="300" font-family="Segoe UI, Microsoft YaHei" font-size="18"
        fill="#FFFFFF" opacity="0.82">Updated 08:45 GMT</text>
  <circle cx="138" cy="376" r="6" fill="#6FE7C8"/>
  <text x="158" y="384" width="300" font-family="Segoe UI, Microsoft YaHei" font-size="18"
        fill="#FFFFFF" opacity="0.82">12 markets monitored</text>

  <rect x="650" y="86" width="492" height="548" rx="34" ry="34"
        fill="#0B1018" opacity="0.20" filter="url(#panelShadow)"/>

  <image x="650" y="86" width="492" height="548" preserveAspectRatio="xMidYMid slice"
         clip-path="url(#glassClip)"
         href="https://images.example.com/hero-background/wheat-calculator-coins-flatlay-blurred-crop-panel.png"/>

  <rect x="650" y="86" width="492" height="548" rx="34" ry="34" fill="url(#glassSheen)" opacity="0.88"/>
  <rect x="650.5" y="86.5" width="491" height="547" rx="34" ry="34"
        fill="none" stroke="#FFFFFF" stroke-opacity="0.48" stroke-width="1.4"/>
  <rect x="681" y="118" width="430" height="1" fill="#FFFFFF" opacity="0.42"/>

  <text x="700" y="154" width="330" font-family="Segoe UI, Microsoft YaHei" font-size="17"
        letter-spacing="2.5" fill="#FFFFFF" opacity="0.72">PRICE DASHBOARD</text>
  <text x="700" y="205" width="360" font-family="Segoe UI, Microsoft YaHei" font-size="42"
        font-weight="700" fill="#FFFFFF">$284.6B</text>
  <text x="932" y="198" width="120" font-family="Segoe UI, Microsoft YaHei" font-size="18"
        font-weight="700" fill="#6FE7C8">+8.4%</text>
  <text x="700" y="238" width="380" font-family="Segoe UI, Microsoft YaHei" font-size="18"
        fill="#FFFFFF" opacity="0.72">Projected global trade value, next 12 months</text>

  <rect x="700" y="282" width="180" height="116" rx="22" ry="22" fill="#FFFFFF" opacity="0.13"/>
  <rect x="904" y="282" width="180" height="116" rx="22" ry="22" fill="#FFFFFF" opacity="0.10"/>
  <rect x="700" y="422" width="384" height="86" rx="24" ry="24" fill="#FFFFFF" opacity="0.11"/>

  <text x="724" y="326" width="130" font-family="Segoe UI, Microsoft YaHei" font-size="34"
        font-weight="700" fill="#FFFFFF">17%</text>
  <text x="724" y="360" width="128" font-family="Segoe UI, Microsoft YaHei" font-size="15"
        fill="#FFFFFF" opacity="0.70">grain inflation</text>

  <text x="928" y="326" width="130" font-family="Segoe UI, Microsoft YaHei" font-size="34"
        font-weight="700" fill="#FFFFFF">42</text>
  <text x="928" y="360" width="132" font-family="Segoe UI, Microsoft YaHei" font-size="15"
        fill="#FFFFFF" opacity="0.70">supply alerts</text>

  <path d="M732,472 L778,444 L825,459 L872,431 L925,448 L975,418 L1050,438"
        fill="none" stroke="#FF9A3D" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M732,472 L778,444 L825,459 L872,431 L925,448 L975,418 L1050,438 L1050,486 L732,486 Z"
        fill="#FF9A3D" opacity="0.13"/>

  <ellipse cx="898" cy="556" rx="118" ry="36" fill="#F05A28" opacity="0.30" filter="url(#softGlow)"/>
  <rect x="806" y="528" width="184" height="58" rx="29" ry="29" fill="url(#buttonGrad)"/>
  <text x="852" y="565" width="100" font-family="Segoe UI, Microsoft YaHei" font-size="17"
        font-weight="700" letter-spacing="1.6" fill="#FFFFFF">SELECT</text>

  <circle cx="1084" cy="132" r="5" fill="#6FE7C8"/>
  <text x="1040" y="139" width="70" font-family="Segoe UI, Microsoft YaHei" font-size="13"
        fill="#FFFFFF" opacity="0.75">LIVE</text>
</svg>
```

## Avoid in this skill
- ❌ Do not use SVG `<animate>` or `<animateTransform>` for the sliding glass effect; create separate SVG slides/keyframes and use PowerPoint Morph after import.
- ❌ Do not rely on CSS `backdrop-filter`; PowerPoint will not preserve it as editable glass.
- ❌ Do not apply `clip-path` to a grouped panel or non-image overlay; only the blurred crop image should use the clip path.
- ❌ Do not use `<mask>` for the frosted panel edge or fade; masks are a hard-fail risk.
- ❌ Do not use `marker-end` on paths for trend arrows; draw arrowheads manually with small paths if needed.

## Composition notes
- Keep the glass panel on one side or in one third of the slide so the background remains visible and the floating effect has room to breathe.
- Use a detailed background image, but darken it slightly with a translucent overlay so white text and glass borders remain legible.
- For the frosted illusion, export or source a separate blurred crop that matches the panel’s position; clip it to the same rounded rectangle as the panel.
- For animation, duplicate the slide, move the entire glass-panel group to a new position, update the blurred crop to match that new position, and apply PowerPoint Morph.