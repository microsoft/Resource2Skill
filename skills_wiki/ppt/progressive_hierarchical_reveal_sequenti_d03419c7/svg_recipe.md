# SVG Recipe — Progressive Hierarchical Reveal (Sequential Builds)

## Visual mechanism
A dark, high-contrast presentation slide keeps all content anchored in fixed positions while each subsequent build slide adds one more bullet or sub-bullet. The visual language uses strong hierarchy, an accent progress rail, and “locked” empty geometry so the audience perceives smooth click-by-click information reveal without relying on fragile PowerPoint animation XML.

## SVG primitives needed
- 1× `<rect>` for the full-slide background
- 1× `<rect>` for the large rounded blue keynote panel
- 1× `<rect>` for the white header band
- 1× `<path>` for the large decorative rounded corner sweep behind the content panel
- 1× `<image>` for an optional presenter/host cutout or topic hero image, clipped to a rounded organic crop
- 1× `<clipPath>` with `<path>` for the hero image crop
- 1× `<filter id="softShadow">` applied to cards and icon shapes
- 1× `<filter id="cyanGlow">` applied to the active reveal indicator
- 1× `<linearGradient>` for the blue content panel
- 1× `<linearGradient>` for the progress rail
- 1× `<radialGradient>` for the PowerPoint-style orange badge
- Multiple `<rect>` elements for bullet cards, hierarchy containers, progress dots, and icon backing plates
- Multiple `<circle>` elements for progress steps and logo/icon details
- Multiple `<line>` elements for hierarchy connectors and divider rules
- Multiple `<text>` elements with explicit `width` attributes for title, build label, bullets, and sub-bullets
- Multiple `<path>` elements for checkmarks, PowerPoint-style “P” icon geometry, and decorative accents

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="panelBlue" x1="0" y1="170" x2="1180" y2="690" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#334a9a"/>
      <stop offset="0.58" stop-color="#455fae"/>
      <stop offset="1" stop-color="#253b86"/>
    </linearGradient>
    <linearGradient id="railGrad" x1="0" y1="0" x2="0" y2="500">
      <stop offset="0" stop-color="#00d4ff"/>
      <stop offset="1" stop-color="#ffc400"/>
    </linearGradient>
    <radialGradient id="pptOrange" cx="45%" cy="35%" r="70%">
      <stop offset="0" stop-color="#ff8a66"/>
      <stop offset="0.62" stop-color="#ef5a35"/>
      <stop offset="1" stop-color="#c93b1f"/>
    </radialGradient>
    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="12"/>
      <feGaussianBlur stdDeviation="14"/>
      <feColorMatrix type="matrix" values="0 0 0 0 0.02 0 0 0 0 0.04 0 0 0 0 0.10 0 0 0 0.28 0"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="cyanGlow" x="-80%" y="-80%" width="260%" height="260%">
      <feGaussianBlur stdDeviation="8" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <clipPath id="hostCrop">
      <path d="M910,155 C990,112 1105,154 1125,258 C1150,388 1088,585 950,620 C815,654 748,548 762,415 C773,303 820,204 910,155 Z"/>
    </clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#ffffff"/>
  <rect x="0" y="0" width="1280" height="120" fill="#ffffff"/>
  <path d="M0,205 C26,177 56,170 98,170 L1280,170 L1280,720 L0,720 Z" fill="url(#panelBlue)"/>

  <text x="50" y="82" width="210" font-family="Segoe UI, Microsoft YaHei" font-size="42" font-weight="800" fill="#3152a3">blue</text>
  <text x="173" y="82" width="180" font-family="Segoe UI, Microsoft YaHei" font-size="38" font-weight="300" fill="#6b95bc">pecan</text>
  <circle cx="70" cy="75" r="18" fill="none" stroke="#f47b20" stroke-width="7"/>
  <circle cx="70" cy="75" r="8" fill="#4e79bb"/>

  <circle cx="1078" cy="170" r="74" fill="url(#pptOrange)" opacity="0.95"/>
  <rect x="982" y="128" width="88" height="88" rx="9" fill="#c74323" filter="url(#softShadow)"/>
  <rect x="992" y="137" width="70" height="70" rx="5" fill="#d94a25"/>
  <text x="1005" y="197" width="52" font-family="Segoe UI, Microsoft YaHei" font-size="70" font-weight="800" fill="#ffffff">P</text>

  <text x="62" y="312" width="560" font-family="Segoe UI, Microsoft YaHei" font-size="82" font-weight="900" fill="#ffc400" letter-spacing="1">MAKE BULLET</text>
  <text x="62" y="448" width="300" font-family="Segoe UI, Microsoft YaHei" font-size="82" font-weight="900" fill="#ffc400" letter-spacing="1">POINTS</text>
  <text x="354" y="448" width="300" font-family="Segoe UI, Microsoft YaHei" font-size="82" font-weight="900" fill="#ffffff" letter-spacing="1">APPEAR</text>
  <text x="88" y="586" width="610" font-family="Segoe UI, Microsoft YaHei" font-size="82" font-weight="900" fill="#ffffff" letter-spacing="1">ONE AT A TIME</text>

  <image href="https://images.example.com/cropped-presenter-torso-no-face.png" x="735" y="122" width="430" height="560" clip-path="url(#hostCrop)" preserveAspectRatio="xMidYMid slice"/>

  <rect x="675" y="245" width="470" height="365" rx="26" fill="#111827" opacity="0.88" filter="url(#softShadow)"/>
  <text x="710" y="292" width="250" font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="700" fill="#9eeaff">BUILD 04 / 08</text>
  <text x="710" y="326" width="360" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="800" fill="#ffffff">Sequential reveal stack</text>
  <line x1="710" y1="348" x2="1085" y2="348" stroke="#34415f" stroke-width="2"/>

  <rect x="716" y="374" width="382" height="52" rx="14" fill="#243250"/>
  <circle cx="740" cy="400" r="8" fill="#00d4ff" filter="url(#cyanGlow)"/>
  <text x="762" y="408" width="310" font-family="Segoe UI, Microsoft YaHei" font-size="23" font-weight="700" fill="#ffffff">Phase 1: Market Research</text>

  <line x1="740" y1="429" x2="740" y2="485" stroke="#3a4b70" stroke-width="2"/>
  <circle cx="762" cy="456" r="5" fill="#9ca3af"/>
  <text x="780" y="463" width="280" font-family="Segoe UI, Microsoft YaHei" font-size="18" fill="#c9d1df">Competitor analysis</text>
  <circle cx="762" cy="488" r="5" fill="#9ca3af"/>
  <text x="780" y="495" width="300" font-family="Segoe UI, Microsoft YaHei" font-size="18" fill="#c9d1df">Customer demographic surveys</text>

  <rect x="716" y="516" width="382" height="52" rx="14" fill="#1b2742"/>
  <circle cx="740" cy="542" r="8" fill="#ffc400"/>
  <text x="762" y="550" width="330" font-family="Segoe UI, Microsoft YaHei" font-size="23" font-weight="700" fill="#ffffff">Phase 2: Product Development</text>

  <rect x="716" y="584" width="382" height="8" rx="4" fill="#33415f"/>
  <rect x="716" y="584" width="205" height="8" rx="4" fill="url(#railGrad)"/>
  <circle cx="716" cy="588" r="7" fill="#00d4ff"/>
  <circle cx="785" cy="588" r="7" fill="#00d4ff"/>
  <circle cx="854" cy="588" r="7" fill="#00d4ff"/>
  <circle cx="923" cy="588" r="7" fill="#ffc400"/>
  <circle cx="992" cy="588" r="7" fill="#5b6680"/>
  <circle cx="1061" cy="588" r="7" fill="#5b6680"/>
</svg>
```

## Avoid in this skill
- ❌ Do not use SVG `<animate>` or PowerPoint timing XML to simulate reveal; create one complete static SVG per build slide instead.
- ❌ Do not let text reflow between builds. Keep identical `x`, `y`, `width`, font size, and line spacing on every duplicated slide.
- ❌ Do not show unrevealed bullets as faint ghosts unless the design explicitly calls for a roadmap preview; true progressive reveal means omitted elements are not present yet.
- ❌ Do not place `clip-path` on text, groups, or cards; only apply clipping to `<image>` elements.
- ❌ Do not rely on `<textPath>`, `<foreignObject>`, `<mask>`, or `<use>` for bullets/icons because these are fragile in editable PowerPoint conversion.

## Composition notes
- Keep the left third as the narrative anchor: brand, headline, or section title remains static across every build.
- Reserve the right two-thirds for the hierarchical reveal stack; every bullet slot should have a fixed coordinate so clicking forward feels like information appearing, not layout shifting.
- Use bright accent dots or a progress rail to imply sequence and speaker control; make the current build visually warmer or brighter than completed sub-points.
- For the build system, duplicate the slide SVG N times and include only items `1...N` on build N; all background, title, hero art, and containers remain identical.