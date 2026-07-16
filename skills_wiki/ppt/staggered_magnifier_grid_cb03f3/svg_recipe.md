# SVG Recipe — Staggered Magnifier Grid

## Visual mechanism
A three-column feature grid is made more dynamic by vertically staggering oversized magnifying-glass icons, so each feature feels “inspected” or “discovered” rather than merely listed. Each magnifier overlaps a soft card, with bold lens rims, translucent fills, and small symbolic details inside the glass.

## SVG primitives needed
- 1× `<rect>` for the full-slide background
- 3× large rounded `<rect>` cards for the staggered feature containers
- 3× `<circle>` for magnifier lens fills
- 3× `<circle>` for magnifier lens rims
- 3× rotated rounded `<rect>` for magnifier handles
- 6× small `<ellipse>` / `<path>` highlights inside lenses for reflective glass effects
- 9–12× small `<rect>`, `<circle>`, and `<path>` primitives for simplified feature symbols inside the lenses
- 2× decorative organic `<path>` blobs in the background
- 1× dashed `<path>` connector running behind the staggered grid
- 1× `<linearGradient>` for the background
- 3× `<linearGradient>` fills for lens tinting
- 1× `<filter id="softShadow">` for card and magnifier depth
- Multiple `<text>` elements with explicit `width` attributes for headline, eyebrow, feature titles, and descriptions

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#F7FAFF"/>
      <stop offset="58%" stop-color="#EEF4FF"/>
      <stop offset="100%" stop-color="#EAF7F3"/>
    </linearGradient>

    <linearGradient id="lensBlue" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.88"/>
      <stop offset="100%" stop-color="#BFD9FF" stop-opacity="0.62"/>
    </linearGradient>
    <linearGradient id="lensMint" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.9"/>
      <stop offset="100%" stop-color="#B8F2E0" stop-opacity="0.64"/>
    </linearGradient>
    <linearGradient id="lensGold" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.9"/>
      <stop offset="100%" stop-color="#FFE29A" stop-opacity="0.66"/>
    </linearGradient>

    <filter id="softShadow" x="-30%" y="-30%" width="160%" height="170%">
      <feOffset dx="0" dy="14"/>
      <feGaussianBlur stdDeviation="16"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="halo" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="9"/>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>

  <path d="M-58 139 C87 47 201 92 258 183 C316 275 217 342 92 321 C-30 301 -132 232 -58 139 Z"
        fill="#D7E7FF" opacity="0.55"/>
  <path d="M1050 40 C1169 -2 1287 45 1321 143 C1356 244 1248 292 1149 262 C1055 234 975 78 1050 40 Z"
        fill="#CFF5E9" opacity="0.58"/>

  <text x="92" y="72" width="180" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700"
        letter-spacing="2.6" fill="#3B65D9">FEATURE SCAN</text>
  <text x="92" y="125" width="620" font-family="Segoe UI, Microsoft YaHei" font-size="42" font-weight="800"
        fill="#172033">Stagger the lens to reveal what matters</text>
  <text x="92" y="162" width="540" font-family="Segoe UI, Microsoft YaHei" font-size="18"
        fill="#5E6B82">Use oversized magnifiers as playful anchors for a low-density feature grid.</text>

  <path d="M214 338 C371 255 493 393 643 329 C796 264 886 202 1068 300"
        fill="none" stroke="#8FA9D9" stroke-width="3" stroke-dasharray="10 14" opacity="0.55"/>

  <!-- Card 1 -->
  <rect x="112" y="255" width="300" height="310" rx="34" fill="#FFFFFF" filter="url(#softShadow)"/>
  <circle cx="262" cy="265" r="92" fill="#6B8CFF" opacity="0.18" filter="url(#halo)"/>
  <rect x="320" y="323" width="38" height="132" rx="19" fill="#20304D"
        transform="rotate(-38 339 389)" filter="url(#softShadow)"/>
  <circle cx="242" cy="240" r="92" fill="url(#lensBlue)" stroke="#20304D" stroke-width="18"/>
  <circle cx="242" cy="240" r="68" fill="none" stroke="#FFFFFF" stroke-width="3" opacity="0.75"/>
  <ellipse cx="211" cy="202" rx="31" ry="13" fill="#FFFFFF" opacity="0.72" transform="rotate(-28 211 202)"/>
  <path d="M212 257 C229 218 269 218 283 257 C263 270 235 270 212 257 Z"
        fill="#3B65D9" opacity="0.95"/>
  <circle cx="247" cy="234" r="16" fill="#FFFFFF"/>
  <circle cx="247" cy="234" r="7" fill="#3B65D9"/>
  <text x="142" y="432" width="240" font-family="Segoe UI, Microsoft YaHei" font-size="24" font-weight="800"
        fill="#172033">Scan the signal</text>
  <text x="142" y="468" width="236" font-family="Segoe UI, Microsoft YaHei" font-size="16"
        fill="#607086">Surface the strongest customer, market, or operational signal before the team dives into detail.</text>

  <!-- Card 2, lower stagger -->
  <rect x="490" y="330" width="300" height="310" rx="34" fill="#FFFFFF" filter="url(#softShadow)"/>
  <circle cx="642" cy="343" r="96" fill="#27C6A2" opacity="0.17" filter="url(#halo)"/>
  <rect x="705" y="404" width="38" height="132" rx="19" fill="#173A3A"
        transform="rotate(-38 724 470)" filter="url(#softShadow)"/>
  <circle cx="622" cy="318" r="92" fill="url(#lensMint)" stroke="#173A3A" stroke-width="18"/>
  <circle cx="622" cy="318" r="68" fill="none" stroke="#FFFFFF" stroke-width="3" opacity="0.75"/>
  <ellipse cx="590" cy="281" rx="31" ry="13" fill="#FFFFFF" opacity="0.74" transform="rotate(-28 590 281)"/>
  <rect x="574" y="318" width="96" height="18" rx="9" fill="#18A886"/>
  <rect x="594" y="286" width="18" height="82" rx="9" fill="#18A886"/>
  <circle cx="574" cy="327" r="8" fill="#FFFFFF"/>
  <circle cx="670" cy="327" r="8" fill="#FFFFFF"/>
  <text x="520" y="508" width="240" font-family="Segoe UI, Microsoft YaHei" font-size="24" font-weight="800"
        fill="#172033">Spot the gap</text>
  <text x="520" y="544" width="236" font-family="Segoe UI, Microsoft YaHei" font-size="16"
        fill="#607086">Make friction visible by contrasting where the process works with where the handoff breaks.</text>

  <!-- Card 3 -->
  <rect x="868" y="255" width="300" height="310" rx="34" fill="#FFFFFF" filter="url(#softShadow)"/>
  <circle cx="1020" cy="265" r="94" fill="#F3B63F" opacity="0.2" filter="url(#halo)"/>
  <rect x="1082" y="323" width="38" height="132" rx="19" fill="#3B2A13"
        transform="rotate(-38 1101 389)" filter="url(#softShadow)"/>
  <circle cx="1000" cy="240" r="92" fill="url(#lensGold)" stroke="#3B2A13" stroke-width="18"/>
  <circle cx="1000" cy="240" r="68" fill="none" stroke="#FFFFFF" stroke-width="3" opacity="0.75"/>
  <ellipse cx="968" cy="202" rx="31" ry="13" fill="#FFFFFF" opacity="0.72" transform="rotate(-28 968 202)"/>
  <path d="M956 272 L987 200 L1010 242 L1032 222 L1051 272 Z" fill="#E49D13"/>
  <circle cx="987" cy="200" r="9" fill="#FFFFFF"/>
  <circle cx="1032" cy="222" r="9" fill="#FFFFFF"/>
  <text x="898" y="432" width="240" font-family="Segoe UI, Microsoft YaHei" font-size="24" font-weight="800"
        fill="#172033">Zoom on value</text>
  <text x="898" y="468" width="236" font-family="Segoe UI, Microsoft YaHei" font-size="16"
        fill="#607086">Translate findings into one crisp value story that executives can repeat after the meeting.</text>

  <text x="1005" y="668" width="190" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700"
        fill="#7B8798">3 lenses · 3 discoveries</text>
</svg>
```

## Avoid in this skill
- ❌ Do not use `<use>` or `<symbol>` to duplicate the magnifier; draw each editable lens and handle explicitly.
- ❌ Do not apply `filter` to `<line>` elements for handles or connectors; use rotated rounded `<rect>` handles instead.
- ❌ Do not rely on `clip-path` for non-image lens contents; clipping non-image shapes will be ignored, so keep internal symbols visually contained inside the circle.
- ❌ Do not make all three cards perfectly aligned; the stagger is the key visual mechanism.
- ❌ Do not use marker-based arrows on the dashed connector; if arrows are needed, create them as explicit `<line>` or `<path>` shapes.

## Composition notes
- Keep the headline in the upper-left quadrant and let the magnifier grid occupy the middle and lower two-thirds of the slide.
- Stagger the center card downward by roughly 70–90 px to create a playful rhythm without destroying alignment.
- Let each magnifying glass overlap the top edge of its card; this makes the icons feel like dimensional objects rather than flat badges.
- Use one dominant color per lens, but keep card fills white and body copy muted so the slide remains executive-friendly.