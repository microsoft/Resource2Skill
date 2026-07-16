# SVG Recipe — Aerodynamic Process Flow

## Visual mechanism
A tapered, expanding “jet stream” sweeps from left to right, using an image-filled aerodynamic shape as the visual metaphor for progress. Milestones attach to the stream’s upper and lower edges, creating a dynamic roadmap that feels like acceleration toward a destination.

## SVG primitives needed
- 1× `<rect>` for the clean white slide background
- 2× `<ellipse>` for oversized translucent decorative rings behind the flow
- 1× `<clipPath>` with a custom `<path>` defining the jet stream image crop
- 1× `<image>` clipped to the jet stream shape for the city / destination photo fill
- 3× `<path>` for the jet stream shadow base, image outline, and edge highlight
- 1× `<filter id="softShadow">` applied to the stream base and milestone cards
- 1× `<linearGradient>` for the stream rim / accent stroke
- 1× `<radialGradient>` for the background ring accent
- 1× grouped airplane illustration built from editable `<path>`, `<ellipse>`, and `<line>` elements
- 6× `<circle>` for milestone anchor dots on the stream edge
- 6× `<line>` for milestone connector stems
- 6× small rounded `<rect>` milestone cards
- 7× `<text>` blocks with explicit `width` attributes for title, year labels, and milestone copy
- Several translucent `<path>` wisps to reinforce motion and airflow

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="streamRim" x1="160" y1="250" x2="1230" y2="560" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#7DB7FF"/>
      <stop offset="0.48" stop-color="#2F6FD6"/>
      <stop offset="1" stop-color="#123E86"/>
    </linearGradient>
    <radialGradient id="ringGlow" cx="50%" cy="50%" r="60%">
      <stop offset="0" stop-color="#4D9BFF" stop-opacity="0"/>
      <stop offset="0.68" stop-color="#4D9BFF" stop-opacity="0.05"/>
      <stop offset="1" stop-color="#1C4587" stop-opacity="0.22"/>
    </radialGradient>
    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="14"/>
      <feGaussianBlur stdDeviation="14"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <clipPath id="jetStreamClip">
      <path d="M166 366 C270 294 416 254 616 242 C844 228 1070 254 1225 317 L1225 563 C1042 527 836 491 627 452 C430 415 286 389 166 366 Z"/>
    </clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#FFFFFF"/>

  <ellipse cx="1045" cy="354" rx="250" ry="250" fill="none" stroke="url(#ringGlow)" stroke-width="54"/>
  <ellipse cx="1038" cy="354" rx="178" ry="178" fill="none" stroke="#D8E8FF" stroke-width="2" opacity="0.75"/>

  <text x="56" y="74" width="560" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="700" fill="#1C4587">Aerodynamic Growth Roadmap</text>
  <text x="58" y="108" width="520" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#6B7280">A visual timeline for strategy, product expansion, and market acceleration</text>

  <text x="930" y="122" width="250" font-family="Segoe UI, Microsoft YaHei" font-size="74" font-weight="700" fill="#E8F1FF">2030</text>

  <path d="M166 366 C270 294 416 254 616 242 C844 228 1070 254 1225 317 L1225 563 C1042 527 836 491 627 452 C430 415 286 389 166 366 Z"
        fill="#DCE9FA" opacity="0.8" filter="url(#softShadow)"/>
  <image href="https://images.example.com/panoramic-futuristic-city-skyline-blue-glass.jpg"
         x="160" y="225" width="1080" height="360" preserveAspectRatio="xMidYMid slice"
         clip-path="url(#jetStreamClip)"/>
  <path d="M166 366 C270 294 416 254 616 242 C844 228 1070 254 1225 317 L1225 563 C1042 527 836 491 627 452 C430 415 286 389 166 366 Z"
        fill="none" stroke="url(#streamRim)" stroke-width="4"/>
  <path d="M201 357 C338 300 470 275 633 266 C824 257 1015 275 1185 329"
        fill="none" stroke="#FFFFFF" stroke-width="3" opacity="0.7"/>

  <path d="M92 356 C130 345 158 352 190 366 C158 381 130 389 92 378 C104 371 104 363 92 356 Z" fill="#1C4587"/>
  <path d="M154 347 L211 319 L196 359 Z" fill="#2F6FD6"/>
  <path d="M154 386 L211 414 L196 374 Z" fill="#2F6FD6"/>
  <path d="M94 367 L58 350 L64 368 L58 386 Z" fill="#7DB7FF"/>
  <ellipse cx="124" cy="367" rx="13" ry="7" fill="#FFFFFF" opacity="0.9"/>
  <line x1="36" y1="336" x2="122" y2="354" stroke="#CFE3FF" stroke-width="2"/>
  <line x1="30" y1="398" x2="124" y2="380" stroke="#CFE3FF" stroke-width="2"/>

  <path d="M120 330 C235 292 350 274 480 270" fill="none" stroke="#A9CCFF" stroke-width="2" opacity="0.45"/>
  <path d="M118 404 C275 438 430 458 620 486" fill="none" stroke="#A9CCFF" stroke-width="2" opacity="0.35"/>
  <path d="M220 342 C325 316 450 302 595 300" fill="none" stroke="#FFFFFF" stroke-width="2" opacity="0.55"/>

  <line x1="335" y1="292" x2="280" y2="178" stroke="#9AB6D8" stroke-width="2"/>
  <circle cx="335" cy="292" r="7" fill="#FFFFFF" stroke="#1C4587" stroke-width="3"/>
  <rect x="198" y="100" width="190" height="78" rx="18" fill="#FFFFFF" filter="url(#softShadow)"/>
  <text x="218" y="130" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#1C4587">2019 Launch</text>
  <text x="218" y="154" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#595959">Initial platform concept and first pilot customers.</text>

  <line x1="515" y1="262" x2="555" y2="132" stroke="#9AB6D8" stroke-width="2"/>
  <circle cx="515" cy="262" r="7" fill="#FFFFFF" stroke="#1C4587" stroke-width="3"/>
  <rect x="500" y="54" width="205" height="78" rx="18" fill="#FFFFFF" filter="url(#softShadow)"/>
  <text x="520" y="84" width="160" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#1C4587">2021 Scale</text>
  <text x="520" y="108" width="160" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#595959">Regional rollout, repeatable delivery model, and partner onboarding.</text>

  <line x1="745" y1="262" x2="802" y2="152" stroke="#9AB6D8" stroke-width="2"/>
  <circle cx="745" cy="262" r="7" fill="#FFFFFF" stroke="#1C4587" stroke-width="3"/>
  <rect x="760" y="74" width="218" height="78" rx="18" fill="#FFFFFF" filter="url(#softShadow)"/>
  <text x="780" y="104" width="175" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#1C4587">2023 Expansion</text>
  <text x="780" y="128" width="175" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#595959">New verticals, enterprise security, and integrated analytics.</text>

  <line x1="420" y1="414" x2="365" y2="548" stroke="#9AB6D8" stroke-width="2"/>
  <circle cx="420" cy="414" r="7" fill="#FFFFFF" stroke="#1C4587" stroke-width="3"/>
  <rect x="260" y="548" width="205" height="78" rx="18" fill="#FFFFFF" filter="url(#softShadow)"/>
  <text x="280" y="578" width="160" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#1C4587">2020 Proof</text>
  <text x="280" y="602" width="160" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#595959">Validated unit economics and strengthened customer success loops.</text>

  <line x1="685" y1="462" x2="740" y2="596" stroke="#9AB6D8" stroke-width="2"/>
  <circle cx="685" cy="462" r="7" fill="#FFFFFF" stroke="#1C4587" stroke-width="3"/>
  <rect x="688" y="596" width="220" height="78" rx="18" fill="#FFFFFF" filter="url(#softShadow)"/>
  <text x="708" y="626" width="175" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#1C4587">2025 Automation</text>
  <text x="708" y="650" width="175" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#595959">AI-assisted operations and lower-touch implementation at scale.</text>

  <line x1="1010" y1="522" x2="1084" y2="632" stroke="#9AB6D8" stroke-width="2"/>
  <circle cx="1010" cy="522" r="7" fill="#FFFFFF" stroke="#1C4587" stroke-width="3"/>
  <rect x="1010" y="632" width="210" height="64" rx="18" fill="#FFFFFF" filter="url(#softShadow)"/>
  <text x="1030" y="660" width="165" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#1C4587">2030 Destination</text>
  <text x="1030" y="683" width="165" font-family="Segoe UI, Microsoft YaHei" font-size="11" fill="#595959">Global operating network and category leadership.</text>
</svg>
```

## Avoid in this skill
- ❌ Do not use `<mask>` to crop the jet stream photo; use `<clipPath>` applied directly to the `<image>`.
- ❌ Do not apply `clip-path` to a `<g>` or `<path>` for the photo fill; the crop should be on the `<image>` only.
- ❌ Do not use `marker-end` arrows for the flow direction; the aerodynamic stream shape itself should imply motion.
- ❌ Do not use `filter` on connector `<line>` elements; keep shadows on cards, stream paths, and text only.
- ❌ Do not build the flow as a plain rectangle or chevron chain; the value of this technique is the custom organic widening silhouette.

## Composition notes
- Keep the stream vertically centered and let it occupy roughly 80% of the slide width, starting narrow near the airplane and widening toward the destination.
- Stagger milestone cards above and below the stream so the composition feels rhythmic rather than like a static table.
- Use a cool blue palette for professional momentum: dark blue titles, pale connector lines, white cards, and a blue-toned destination image.
- Preserve generous white space around the top-left title and around the airplane nose so the slide feels premium and cinematic.