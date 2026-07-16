# SVG Recipe — Icon Array Infographic with Morph Transition

## Visual mechanism
A 100-icon isotype grid makes a percentage feel concrete by coloring the “active” icons in a saturated accent and fading the remainder. For the Morph transition, duplicate the slide, preserve every icon’s `id`, then reposition the same 100 editable icon paths into smaller segment grids so PowerPoint animates the rearrangement.

## SVG primitives needed
- 1× `<rect>` for the full-slide gradient background
- 1× decorative `<path>` for a soft abstract accent blob behind the icon array
- 100× `<path>` person icons, each with a stable `id` such as `icon-001` through `icon-100`
- 1× `<linearGradient>` for the pale executive-style background
- 1× `<radialGradient>` for the soft purple visual glow
- 1× `<filter id="softShadow">` using `feOffset + feGaussianBlur + feMerge`, applied to the large statistic text
- 7× `<text>` elements for eyebrow label, statistic, title, description, and off-canvas segment labels used by the Morph destination slide

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bg" x1="0" y1="720" x2="1280" y2="0"><stop offset="0%" stop-color="#F8F8FB"/><stop offset="100%" stop-color="#E8E8EF"/></linearGradient>
    <radialGradient id="purpleGlow" cx="50%" cy="48%" r="55%"><stop offset="0%" stop-color="#BCA7FF" stop-opacity="0.42"/><stop offset="100%" stop-color="#BCA7FF" stop-opacity="0"/></radialGradient>
    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="140%"><feOffset dx="0" dy="7"/><feGaussianBlur stdDeviation="8"/><feMerge><feMergeNode/><feMergeNode in="SourceGraphic"/></feMerge></filter>
  </defs>
  <rect x="0" y="0" width="1280" height="720" fill="url(#bg)"/>
  <path d="M260 122 C390 34 520 92 654 60 C826 18 1034 84 1076 218 C1128 384 902 442 740 420 C566 398 494 478 340 424 C178 368 132 210 260 122 Z" fill="url(#purpleGlow)"/>
  <text id="eyebrow" x="0" y="86" width="1280" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="22" font-weight="700" letter-spacing="3" fill="#6F44DC">CUSTOMER REACH INDEX</text>
  <g id="people-grid">
    <path id="icon-001" transform="translate(254 136)" fill="#6F44DC" d="M11 0 C15 0 18 3 18 7 C18 11 15 14 11 14 C7 14 4 11 4 7 C4 3 7 0 11 0 Z M3 18 C3 15 5 14 8 14 H14 C17 14 19 15 19 18 V30 C19 33 17 35 14 35 H8 C5 35 3 33 3 30 Z"/>
    <path id="icon-002" transform="translate(294 136)" fill="#6F44DC" d="M11 0 C15 0 18 3 18 7 C18 11 15 14 11 14 C7 14 4 11 4 7 C4 3 7 0 11 0 Z M3 18 C3 15 5 14 8 14 H14 C17 14 19 15 19 18 V30 C19 33 17 35 14 35 H8 C5 35 3 33 3 30 Z"/>
    <path id="icon-003" transform="translate(334 136)" fill="#6F44DC" d="M11 0 C15 0 18 3 18 7 C18 11 15 14 11 14 C7 14 4 11 4 7 C4 3 7 0 11 0 Z M3 18 C3 15 5 14 8 14 H14 C17 14 19 15 19 18 V30 C19 33 17 35 14 35 H8 C5 35 3 33 3 30 Z"/>
    <path id="icon-004" transform="translate(374 136)" fill="#6F44DC" d="M11 0 C15 0 18 3 18 7 C18 11 15 14 11 14 C7 14 4 11 4 7 C4 3 7 0 11 0 Z M3 18 C3 15 5 14 8 14 H14 C17 14 19 15 19 18 V30 C19 33 17 35 14 35 H8 C5 35 3 33 3 30 Z"/>
    <path id="icon-005" transform="translate(414 136)" fill="#6F44DC" d="M11 0 C15 0 18 3 18 7 C18 11 15 14 11 14 C7 14 4 11 4 7 C4 3 7 0 11 0 Z M3 18 C3 15 5 14 8 14 H14 C17 14 19 15 19 18 V30 C19 33 17 35 14 35 H8 C5 35 3 33 3 30 Z"/>
    <path id="icon-006" transform="translate(454 136)" fill="#6F44DC" d="M11 0 C15 0 18 3 18 7 C18 11 15 14 11 14 C7 14 4 11 4 7 C4 3 7 0 11 0 Z M3 18 C3 15 5 14 8 14 H14 C17 14 19 15 19 18 V30 C19 33 17 35 14 35 H8 C5 35 3 33 3 30 Z"/>
    <path id="icon-007" transform="translate(494 136)" fill="#6F44DC" d="M11 0 C15 0 18 3 18 7 C18 11 15 14 11 14 C7 14 4 11 4 7 C4 3 7 0 11 0 Z M3 18 C3 15 5 14 8 14 H14 C17 14 19 15 19 18 V30 C19 33 17 35 14 35 H8 C5 35 3 33 3 30 Z"/>
    <path id="icon-008" transform="translate(534 136)" fill="#6F44DC" d="M11 0 C15 0 18 3 18 7 C18 11 15 14 11 14 C7 14 4 11 4 7 C4 3 7 0 11 0 Z M3 18 C3 15 5 14 8 14 H14 C17 14 19 15 19 18 V30 C19 33 17 35 14 35 H8 C5 35 3 33 3 30 Z"/>
    <path id="icon-009" transform="translate(574 136)" fill="#6F44DC" d="M11 0 C15 0 18 3 18 7 C18 11 15 14 11 14 C7 14 4 11 4 7 C4 3 7 0 11 0 Z M3 18 C3 15 5 14 8 14 H14 C17 14 19 15 19 18 V30 C19 33 17 35 14 35 H8 C5 35 3 33 3 30 Z"/>
    <path id="icon-010" transform="translate(614 136)" fill="#6F44DC" d="M11 0 C15 0 18 3 18 7 C18 11 15 14 11 14 C7 14 4 11 4 7 C4 3 7 0 11 0 Z M3 18 C3 15 5 14 8 14 H14 C17 14 19 15 19 18 V30 C19 33 17 35 14 35 H8 C5 35 3 33 3 30 Z"/>
    <path id="icon-011" transform="translate(654 136)" fill="#6F44DC" d="M11 0 C15 0 18 3 18 7 C18 11 15 14 11 14 C7 14 4 11 4 7 C4 3 7 0 11 0 Z M3 18 C3 15 5 14 8 14 H14 C17 14 19 15 19 18 V30 C19 33 17 35 14 35 H8 C5 35 3 33 3 30 Z"/>
    <path id="icon-012" transform="translate(694 136)" fill="#6F44DC" d="M11 0 C15 0 18 3 18 7 C18 11 15 14 11 14 C7 14 4 11 4 7 C4 3 7 0 11 0 Z M3 18 C3 15 5 14 8 14 H14 C17 14 19 15 19 18 V30 C19 33 17 35 14 35 H8 C5 35 3 33 3 30 Z"/>
    <path id="icon-013" transform="translate(734 136)" fill="#6F44DC" d="M11 0 C15 0 18 3 18 7 C18 11 15 14 11 14 C7 14 4 11 4 7 C4 3 7 0 11 0 Z M3 18 C3 15 5 14 8 14 H14 C17 14 19 15 19 18 V30 C19 33 17 35 14 35 H8 C5 35 3 33 3 30 Z"/>
    <path id="icon-014" transform="translate(774 136)" fill="#6F44DC" d="M11 0 C15 0 18 3 18 7 C18 11 15 14 11 14 C7 14 4 11 4 7 C4 3 7 0 11 0 Z M3 18 C3 15 5 14 8 14 H14 C17 14 19 15 19 18 V30 C19 33 17 35 14 35 H8 C5 35 3 33 3 30 Z"/>
    <path id="icon-015" transform="translate(814 136)" fill="#6F44DC" d="M11 0 C15 0 18 3 18 7 C18 11 15 14 11 14 C7 14 4 11 4 7 C4 3 7 0 11 0 Z M3 18 C3 15 5 14 8 14 H14 C17 14 19 15 19 18 V30 C19 33 17 35 14 35 H8 C5 35 3 33 3 30 Z"/>
    <path id="icon-016" transform="translate(854 136)" fill="#6F44DC" d="M11 0 C15 0 18 3 18 7 C18 11 15 14 11 14 C7 14 4 11 4 7 C4 3 7 0 11 0 Z M3 18 C3 15 5 14 8 14 H14 C17 14 19 15 19 18 V30 C19 33 17 35 14 35 H8 C5 35 3 33 3 30 Z"/>
    <path id="icon-017" transform="translate(894 136)" fill="#6F44DC" d="M11 0 C15 0 18 3 18 7 C18 11 15 14 11 14 C7 14 4 11 4 7 C4 3 7 0 11 0 Z M3 18 C3 15 5 14 8 14 H14 C17 14 19 15 19 18 V30 C19 33 17 35 14 35 H8 C5 35 3 33 3 30 Z"/>
    <path id="icon-018" transform="translate(934 136)" fill="#6F44DC" d="M11 0 C15 0 18 3 18 7 C18 11 15 14 11 14 C7 14 4 11 4 7 C4 3 7 0 11 0 Z M3 18 C3 15 5 14 8 14 H14 C17 14 19 15 19 18 V30 C19 33 17 35 14 35 H8 C5 35 3 33 3 30 Z"/>
    <path id="icon-019" transform="translate(974 136)" fill="#6F44DC" d="M11 0 C15 0 18 3 18 7 C18 11 15 14 11 14 C7 14 4 11 4 7 C4 3 7 0 11 0 Z M3 18 C3 15 5 14 8 14 H14 C17 14 19 15 19 18 V30 C19 33 17 35 14 35 H8 C5 35 3 33 3 30 Z"/>
    <path id="icon-020" transform="translate(1014 136)" fill="#6F44DC" d="M11 0 C15 0 18 3 18 7 C18 11 15 14 11 14 C7 14 4 11 4 7 C4 3 7 0 11 0 Z M3 18 C3 15 5 14 8 14 H14 C17 14 19 15 19 18 V30 C19 33 17 35 14 35 H8 C5 35 3 33 3 30 Z"/>
    <path id="icon-021" transform="translate(254 190)" fill="#6F44DC" d="M11 0 C15 0 18 3 18 7 C18 11 15 14 11 14 C7 14 4 11 4 7 C4 3 7 0 11 0 Z M3 18 C3 15 5 14 8 14 H14 C17 14 19 15 19 18 V30 C19 33 17 35 14 35 H8 C5 35 3 33 3 30 Z"/>
    <path id="icon-022" transform="translate(294 190)" fill="#6F44DC" d="M11 0 C15 0 18 3 18 7 C18 11 15 14 11 14 C7 14 4 11 4 7 C4 3 7 0 11 0 Z M3 18 C3 15 5 14 8 14 H14 C17 14 19 15 19 18 V30 C19 33 17 35 14 35 H8 C5 35 3 33 3 30 Z"/>
    <path id="icon-023" transform="translate(334 190)" fill="#6F44DC" d="M11 0 C15 0 18 3 18 7 C18 11 15 14 11 14 C7 14 4 11 4 7 C4 3 7 0 11 0 Z M3 18 C3 15 5 14 8 14 H14 C17 14 19 15 19 18 V30 C19 33 17 35 14 35 H8 C5 35 3 33 3 30 Z"/>
    <path id="icon-024" transform="translate(374 190)" fill="#6F44DC" d="M11 0 C15 0 18 3 18 7 C18 11 15 14 11 14 C7 14 4 11 4 7 C4 3 7 0 11 0 Z M3 18 C3 15 5 14 8 14 H14 C17 14 19 15 19 18 V30 C19 33 17 35 14 35 H8 C5 35 3 33 3 30 Z"/>
    <path id="icon-025" transform="translate(414 190)" fill="#6F44DC" d="M11 0 C15 0 18 3 18 7 C18 11 15 14 11 14 C7 14 4 11 4 7 C4 3 7 0 11 0 Z M3 18 C3 15 5 14 8 14 H14 C17 14 19 15 19 18 V30 C19 33 17 35 14 35 H8 C5 35 3 33 3 30 Z"/>
    <path id="icon-026" transform="translate(454 190)" fill="#6F44DC" d="M11 0 C15 0 18 3 18 7 C18 11 15 14 11 14 C7 14 4 11 4 7 C4 3 7 0 11 0 Z M3 18 C3 15 5 14 8 14 H14 C17 14 19 15 19 18 V30 C19 33 17 35 14 35 H8 C5 35 3 33 3 30 Z"/>
    <path id="icon-027" transform="translate(494 190)" fill="#6F44DC" d="M11 0 C15 0 18 3 18 7 C18 11 15 14 11 14 C7 14 4 11 4 7 C4 3 7 0 11 0 Z M3 18 C3 15 5 14 8 14 H14 C17 14 19 15 19 18 V30 C19 33 17 35 14 35 H8 C5 35 3 33 3 30 Z"/>
    <path id="icon-028" transform="translate(534 190)" fill="#6F44DC" d="M11 0 C15 0 18 3 18 7 C18 11 15 14 11 14 C7 14 4 11 4 7 C4 3 7 0 11 0 Z M3 18 C3 15 5 14 8 14 H14 C17 14 19 15 19 18 V30 C19 33 17 35 14 35 H8 C5 35 3 33 3 30 Z"/>
    <path id="icon-029" transform="translate(574 190)" fill="#6F44DC" d="M11 0 C15 0 18 3 18 7 C18 11 15 14 11 14 C7 14 4 11 4 7 C4 3 7 0 11 0 Z M3 18 C3 15 5 14 8 14 H14 C17 14 19 15 19 18 V30 C19 33 17 35 14 35 H8 C5 35 3 33 3 30 Z"/>
    <path id="icon-030" transform="translate(614 190)" fill="#6F44DC" d="M11 0 C15 0 18 3 18 7 C18 11 15 14 11 14 C7 14 4 11 4 7 C4 3 7 0 11 0 Z M3 18 C3 15 5 14 8 14 H14 C17 14 19 15 19 18 V30 C19 33 17 35 14 35 H8 C5 35 3 33 3 30 Z"/>
    <path id="icon-031" transform="translate(654 190)" fill="#6F44DC" d="M11 0 C15 0 18 3 18 7 C18 11 15 14 11 14 C7 14 4 11 4 7 C4 3 7 0 11 0 Z M3 18 C3 15 5 14 8 14 H14 C17 14 19 15 19 18 V30 C19 33 17 35 14 35 H8 C5 35 3 33 3 30 Z"/>
    <path id="icon-032" transform="translate(694 190)" fill="#6F44DC" d="M11 0 C15 0 18 3 18 7 C18 11 15 14 11 14 C7 14 4 11 4 7 C4 3 7 0 11 0 Z M3 18 C3 15 5 14 8 14 H14 C17 14 19 15 19 18 V30 C19 33 17 35 14 35 H8 C5 35 3 33 3 30 Z"/>
    <path id="icon-033" transform="translate(734 190)" fill="#6F44DC" d="M11 0 C15 0 18 3 18 7 C18 11 15 14 11 14 C7 14 4 11 4 7 C4 3 7 0 11 0 Z M3 18 C3 15 5 14 8 14 H14 C17 14 19 15 19 18 V30 C19 33 17 35 14 35 H8 C5 35 3 33 3 30 Z"/>
    <path id="icon-034" transform="translate(774 190)" fill="#6F44DC" d="M11 0 C15 0 18 3 18 7 C18 11 15 14 11 14 C7 14 4 11 4 7 C4 3 7 0 11 0 Z M3 18 C3 15 5 14 8 14 H14 C17 14 19 15 19 18 V30 C19 33 17 35 14 35 H8 C5 35 3 33 3 30 Z"/>
    <path id="icon-035" transform="translate(814 190)" fill="#6F44DC" d="M11 0 C15 0 18 3 18 7 C18 11 15 14 11 14 C7 14 4 11 4 7 C4 3 7 0 11 0 Z M3 18 C3 15 5 14 8 14 H14 C17 14 19 15 19 18 V30 C19 33 17 35 14 35 H8 C5 35 3 33 3 30 Z"/>
    <path id="icon-036" transform="translate(854 190)" fill="#6F44DC" d="M11 0 C15 0 18 3 18 7 C18 11 15 14 11 14 C7 14 4 11 4 7 C4 3 7 0 11 0 Z M3 18 C3 15 5 14 8 14 H14 C17 14 19 15 19 18 V30 C19 33 17 35 14 35 H8 C5 35 3 33 3 30 Z"/>
    <path id="icon-037" transform="translate(894 190)" fill="#6F44DC" d="M11 0 C15 0 18 3 18 7 C18 11 15 14 11 14 C7 14 4 11 4 7 C4 3 7 0 11 0 Z M3 18 C3 15 5 14 8 14 H14 C17 14 19 15 19 18 V30 C19 33 17 35 14 35 H8 C5 35 3 33 3 30 Z"/>
    <path id="icon-038" transform="translate(934 190)" fill="#6F44DC" d="M11 0 C15 0 18 3 18 7 C18 11 15 14 11 14 C7 14 4 11 4 7 C4 3 7 0 11 0 Z M3 18 C3 15 5 14 8 14 H14 C17 14 19 15 19 18 V30 C19 33 17 35 14 35 H8 C5 35 3 33 3 30 Z"/>
    <path id="icon-039" transform="translate(974 190)" fill="#6F44DC" d="M11 0 C15 0 18 3 18 7 C18 11 15 14 11 14 C7 14 4 11 4 7 C4 3 7 0 11 0 Z M3 18 C3 15 5 14 8 14 H14 C17 14 19 15 19 18 V30 C19 33 17 35 14 35 H8 C5 35 3 33 3 30 Z"/>
    <path id="icon-040" transform="translate(1014 190)" fill="#6F44DC" d="M11 0 C15