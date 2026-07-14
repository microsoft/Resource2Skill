# SVG Recipe — Cyber-Teal Circuit Overlay with Neon Callout

## Visual mechanism
A deep navy-to-teal gradient field is overlaid with faint cyan circuit traces concentrated on the left edge, creating a technical atmosphere without competing with the message. A glowing neon-green arrow callout interrupts the calm dark layout and points attention back toward the headline/subtitle zone.

## SVG primitives needed
- 1× full-slide `<rect>` for the moody vertical background gradient
- 2× large translucent `<circle>` / `<ellipse>` radial glow fields for teal depth and vignette
- 8–14× thin `<path>` strokes for angular circuit-board traces
- 12–20× `<circle>` nodes for circuit terminals and glowing connection points
- 6–10× low-opacity `<rect>` slivers for subtle scanline / panel accents
- 1× neon callout `<path>` shaped like a left-pointing arrow
- 1× `<filter id="neonGlow">` using `feGaussianBlur` + `feMerge` applied to the arrow and selected nodes
- 1× `<filter id="softShadow">` using `feOffset` + `feGaussianBlur` + `feMerge` applied to the text panel and callout
- 3–5× `<text>` elements with explicit `width` attributes for editable title, subtitle, label, and small metadata text
- 2× `<linearGradient>` definitions for the cyber background and neon arrow fill
- 1× `<radialGradient>` definition for ambient teal light

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGradient" x1="0" y1="0" x2="0" y2="720">
      <stop offset="0%" stop-color="#062737"/>
      <stop offset="48%" stop-color="#0B3142"/>
      <stop offset="100%" stop-color="#0F5257"/>
    </linearGradient>

    <radialGradient id="tealBloom" cx="18%" cy="42%" r="65%">
      <stop offset="0%" stop-color="#00FFFF" stop-opacity="0.20"/>
      <stop offset="45%" stop-color="#00A7B3" stop-opacity="0.08"/>
      <stop offset="100%" stop-color="#00151F" stop-opacity="0"/>
    </radialGradient>

    <linearGradient id="neonArrow" x1="705" y1="375" x2="1035" y2="455">
      <stop offset="0%" stop-color="#CFFF69"/>
      <stop offset="45%" stop-color="#8CD26E"/>
      <stop offset="100%" stop-color="#38F2A0"/>
    </linearGradient>

    <filter id="neonGlow" x="-35%" y="-35%" width="170%" height="170%">
      <feGaussianBlur in="SourceGraphic" stdDeviation="6" result="blur1"/>
      <feGaussianBlur in="SourceGraphic" stdDeviation="14" result="blur2"/>
      <feMerge>
        <feMergeNode in="blur2"/>
        <feMergeNode in="blur1"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feOffset dx="0" dy="8" in="SourceAlpha" result="off"/>
      <feGaussianBlur in="off" stdDeviation="12" result="shadow"/>
      <feMerge>
        <feMergeNode in="shadow"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGradient)"/>
  <circle cx="170" cy="320" r="430" fill="url(#tealBloom)"/>
  <ellipse cx="1070" cy="655" rx="430" ry="180" fill="#002735" opacity="0.38"/>

  <g opacity="0.16">
    <rect x="0" y="92" width="1280" height="1.5" fill="#00FFFF"/>
    <rect x="0" y="218" width="1280" height="1" fill="#00FFFF"/>
    <rect x="0" y="346" width="1280" height="1.2" fill="#00FFFF"/>
    <rect x="0" y="512" width="1280" height="1" fill="#00FFFF"/>
    <rect x="98" y="0" width="1.2" height="720" fill="#00FFFF"/>
    <rect x="242" y="0" width="1" height="720" fill="#00FFFF"/>
    <rect x="386" y="0" width="1.2" height="720" fill="#00FFFF"/>
  </g>

  <g fill="none" stroke="#00FFFF" stroke-linecap="round" stroke-linejoin="round">
    <path d="M0 86 H132 L188 142 H312" stroke-width="2.4" opacity="0.24"/>
    <path d="M18 166 H106 L152 120 H250 L304 174 H405" stroke-width="2" opacity="0.18"/>
    <path d="M0 260 H88 L142 314 H270 L334 250 H436" stroke-width="2.6" opacity="0.22"/>
    <path d="M42 392 H154 L214 332 H315 L392 409 H506" stroke-width="2" opacity="0.17"/>
    <path d="M0 506 H116 L180 570 H286 L350 506 H455" stroke-width="2.5" opacity="0.22"/>
    <path d="M76 640 H168 L222 586 H338" stroke-width="2" opacity="0.18"/>
    <path d="M264 42 V118 L318 172 V266" stroke-width="1.8" opacity="0.16"/>
    <path d="M366 150 V236 L428 298 V386" stroke-width="1.8" opacity="0.15"/>
    <path d="M198 430 V492 L244 538 V676" stroke-width="2.1" opacity="0.18"/>
  </g>

  <g fill="#00FFFF" stroke="#00FFFF">
    <circle cx="132" cy="86" r="5" opacity="0.34" filter="url(#neonGlow)"/>
    <circle cx="188" cy="142" r="4" opacity="0.28"/>
    <circle cx="312" cy="142" r="7" fill="none" stroke-width="2" opacity="0.30"/>
    <circle cx="152" cy="120" r="5" opacity="0.24"/>
    <circle cx="304" cy="174" r="6" fill="none" stroke-width="2" opacity="0.28"/>
    <circle cx="142" cy="314" r="4" opacity="0.30"/>
    <circle cx="270" cy="314" r="7" fill="none" stroke-width="2" opacity="0.24"/>
    <circle cx="334" cy="250" r="5" opacity="0.30" filter="url(#neonGlow)"/>
    <circle cx="214" cy="332" r="4" opacity="0.26"/>
    <circle cx="392" cy="409" r="7" fill="none" stroke-width="2" opacity="0.25"/>
    <circle cx="180" cy="570" r="5" opacity="0.28"/>
    <circle cx="350" cy="506" r="6" fill="none" stroke-width="2" opacity="0.26"/>
    <circle cx="222" cy="586" r="4" opacity="0.28"/>
    <circle cx="318" cy="172" r="5" opacity="0.25"/>
    <circle cx="428" cy="298" r="6" fill="none" stroke-width="2" opacity="0.22"/>
    <circle cx="244" cy="538" r="5" opacity="0.25"/>
  </g>

  <rect x="485" y="165" width="590" height="255" rx="26" fill="#031B28" opacity="0.28" filter="url(#softShadow)"/>
  <text x="780" y="252" width="650" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="54" font-weight="700"
        letter-spacing="2.5" fill="#FFFFFF">
    CLOUD NATIVE OPS
  </text>
  <text x="780" y="312" width="610" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="25" font-weight="400"
        letter-spacing="1.4" fill="#D9F4F5" opacity="0.88">
    SECURE INFRASTRUCTURE • LIVE TELEMETRY • ZERO-DOWNTIME RELEASES
  </text>
  <text x="780" y="363" width="560" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="17"
        fill="#9CC8CC" opacity="0.78">
    A high-confidence operating model for teams shipping critical software at scale.
  </text>

  <path d="M704 412 L770 369 L770 391 H1012 Q1033 391 1033 412 V444 Q1033 465 1012 465 H770 V488 Z"
        fill="url(#neonArrow)" opacity="0.98" filter="url(#neonGlow)"/>
  <path d="M704 412 L770 369 L770 391 H1012 Q1033 391 1033 412 V444 Q1033 465 1012 465 H770 V488 Z"
        fill="none" stroke="#E9FF9E" stroke-width="2" opacity="0.75"/>

  <text x="890" y="439" width="260" text-anchor="middle"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="28" font-weight="800"
        letter-spacing="0.8" fill="#083B2F">
    CHECK HERE
  </text>

  <text x="82" y="674" width="330"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" font-weight="600"
        letter-spacing="2.2" fill="#6DEBEE" opacity="0.62">
    SYSTEM STATUS / ENCRYPTED CHANNEL
  </text>
</svg>
```

## Avoid in this skill
- ❌ Do not use `<pattern>` for the circuit grid; many PowerPoint translators drop pattern fills, and manual faint lines give better editable control.
- ❌ Do not put `filter` on `<line>` elements for glowing circuits; use `<path>` strokes and glowing `<circle>` nodes instead.
- ❌ Do not use `marker-end` for arrowheads; create the neon callout as a single editable `<path>`.
- ❌ Do not use a mask to fade the circuit overlay; use opacity on grouped paths/circles and radial gradient glows.
- ❌ Do not clip non-image shapes for the callout or background effects; keep the arrow and circuits as native editable paths.

## Composition notes
- Keep the circuit overlay mostly within the left 30–40% of the canvas so it frames the slide rather than competing with the central message.
- Place the primary text block slightly right of center, with ample negative space around it for a premium keynote feel.
- Use cyan only as a low-opacity atmospheric accent; reserve the saturated neon green for the single callout so the eye knows where to land.
- The arrow should overlap the lower edge of the text zone and point back toward the subtitle or key phrase, creating deliberate visual interruption without clutter.