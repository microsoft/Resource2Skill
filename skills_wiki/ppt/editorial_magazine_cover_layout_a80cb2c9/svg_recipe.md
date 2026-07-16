# SVG Recipe — Editorial Magazine Cover Layout

## Visual mechanism
A 16:9 slide is treated as a stage for a centered portrait “magazine cover” panel, using a thick inset frame, oversized masthead, editorial teaser typography, and a central cutout subject layered above the masthead and border. The key effect is depth: the subject appears to pop out of the printed cover while the surrounding text behaves like premium magazine cover lines.

## SVG primitives needed
- 3× `<rect>` for the outer slide backdrop, portrait paper panel, and thick no-fill editorial frame
- 10–18× small `<rect>` for barcode bars and small editorial label blocks
- 1× `<image>` for the transparent-background central subject cutout
- 2× `<ellipse>` for soft cast shadow and subject glow
- 3× `<path>` for organic accent shapes, sticker bursts, or graphic editorial ornaments
- 14–22× `<text>` for masthead, metadata, teaser headlines, subtitles, issue labels, and barcode caption
- 1× `<linearGradient>` for the slide backdrop
- 1× `<linearGradient>` for the paper panel
- 1× `<radialGradient>` for a subtle accent halo behind the subject
- 1× `<filter id="pageShadow">` applied to the portrait panel
- 1× `<filter id="softShadow">` applied to subject shadow/accent shapes

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="stageBg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#2A2A2F"/>
      <stop offset="58%" stop-color="#111114"/>
      <stop offset="100%" stop-color="#3A141D"/>
    </linearGradient>

    <linearGradient id="paperFill" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#FAFAF7"/>
      <stop offset="100%" stop-color="#ECE9E3"/>
    </linearGradient>

    <radialGradient id="haloRed" cx="50%" cy="45%" r="56%">
      <stop offset="0%" stop-color="#DC143C" stop-opacity="0.24"/>
      <stop offset="70%" stop-color="#DC143C" stop-opacity="0.06"/>
      <stop offset="100%" stop-color="#DC143C" stop-opacity="0"/>
    </radialGradient>

    <filter id="pageShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feOffset dx="0" dy="14"/>
      <feGaussianBlur stdDeviation="18"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="softShadow" x="-35%" y="-35%" width="170%" height="170%">
      <feGaussianBlur stdDeviation="14"/>
    </filter>
  </defs>

  <!-- 16:9 stage -->
  <rect x="0" y="0" width="1280" height="720" fill="url(#stageBg)"/>

  <!-- editorial portrait cover panel -->
  <rect x="362" y="28" width="556" height="664" rx="8" fill="url(#paperFill)" filter="url(#pageShadow)"/>

  <!-- subtle paper margin accents -->
  <rect x="382" y="48" width="4" height="624" fill="#DC143C" opacity="0.18"/>
  <rect x="891" y="48" width="2" height="624" fill="#111111" opacity="0.08"/>

  <!-- thick inset magazine frame, placed below masthead/subject so they can overlap it -->
  <rect x="410" y="62" width="474" height="598" fill="none" stroke="#DC143C" stroke-width="9"/>

  <!-- metadata -->
  <text x="410" y="49" width="474" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#696969" letter-spacing="2">
    VOL. 42  •  MARCH 2025  •  FUTURE WORK ISSUE
  </text>

  <!-- large masthead -->
  <text x="647" y="137" width="500" text-anchor="middle" font-family="Impact, Segoe UI, Microsoft YaHei" font-size="82" font-weight="900" fill="#DC143C" letter-spacing="-2">
    VANGUARD
  </text>
  <text x="650" y="148" width="500" text-anchor="middle" font-family="Impact, Segoe UI, Microsoft YaHei" font-size="82" font-weight="900" fill="#111111" opacity="0.08" letter-spacing="-2">
    VANGUARD
  </text>

  <!-- small deck/category tag -->
  <rect x="430" y="166" width="96" height="24" fill="#111111"/>
  <text x="478" y="183" width="88" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="11" font-weight="800" fill="#FFFFFF" letter-spacing="1.5">
    STRATEGY
  </text>

  <!-- decorative halo and editorial graphic ornaments behind subject -->
  <ellipse cx="652" cy="390" rx="205" ry="250" fill="url(#haloRed)"/>
  <path d="M790 205 C838 225 850 277 826 308 C801 341 736 326 721 282 C708 244 744 184 790 205 Z"
        fill="#DC143C" opacity="0.11" filter="url(#softShadow)"/>
  <path d="M464 450 C423 416 430 358 470 332 C511 306 561 338 558 391 C555 444 504 483 464 450 Z"
        fill="#111111" opacity="0.08" filter="url(#softShadow)"/>

  <!-- subject shadow -->
  <ellipse cx="655" cy="630" rx="142" ry="24" fill="#000000" opacity="0.26" filter="url(#softShadow)"/>

  <!-- central isolated subject; use transparent PNG/SVG cutout in production -->
  <image x="480" y="165" width="350" height="480"
         href="https://images.example.com/cutouts/editorial-founder-full-body-transparent.png"
         preserveAspectRatio="xMidYMid meet"/>

  <!-- optional editable accent burst placed above subject -->
  <path d="M828 365 L848 374 L839 393 L860 397 L845 411 L858 430 L835 425 L829 447 L815 428 L794 438 L804 416 L783 407 L805 396 L798 374 L818 383 Z"
        fill="#DC143C"/>
  <text x="822" y="404" width="72" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="900" fill="#FFFFFF">
    NEW
  </text>

  <!-- left cover teasers -->
  <line x1="430" y1="218" x2="525" y2="218" stroke="#DC143C" stroke-width="4"/>
  <text x="430" y="244" width="155" font-family="Segoe UI, Microsoft YaHei" font-size="25" font-weight="800" fill="#111111">
    The AI
  </text>
  <text x="430" y="272" width="170" font-family="Segoe UI, Microsoft YaHei" font-size="25" font-weight="800" fill="#111111">
    Operating
  </text>
  <text x="430" y="300" width="170" font-family="Segoe UI, Microsoft YaHei" font-size="25" font-weight="800" fill="#DC143C">
    Model
  </text>
  <text x="430" y="323" width="165" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#4E4E4E">
    How leading teams redesign decision loops for speed.
  </text>

  <text x="430" y="410" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="800" fill="#DC143C">
    INSIDE:
  </text>
  <text x="430" y="434" width="160" font-family="Segoe UI, Microsoft YaHei" font-size="18" font-weight="800" fill="#111111">
    7 Signals
  </text>
  <text x="430" y="458" width="165" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#4E4E4E">
    What executives should watch before the market turns.
  </text>

  <!-- right cover teasers -->
  <line x1="765" y1="214" x2="858" y2="214" stroke="#DC143C" stroke-width="4"/>
  <text x="747" y="242" width="120" text-anchor="end" font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="900" fill="#111111">
    Culture
  </text>
  <text x="747" y="266" width="120" text-anchor="end" font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="900" fill="#111111">
    as a
  </text>
  <text x="747" y="290" width="120" text-anchor="end" font-family="Segoe UI, Microsoft YaHei" font-size="20" font-weight="900" fill="#DC143C">
    Product
  </text>
  <text x="707" y="314" width="155" text-anchor="end" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#4E4E4E">
    Designing rituals that scale trust, talent, and urgency.
  </text>

  <rect x="769" y="505" width="88" height="30" fill="#DC143C"/>
  <text x="813" y="525" width="78" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="900" fill="#FFFFFF" letter-spacing="1">
    SPECIAL
  </text>
  <text x="705" y="561" width="155" text-anchor="end" font-family="Segoe UI, Microsoft YaHei" font-size="22" font-weight="900" fill="#111111">
    Boardroom
  </text>
  <text x="705" y="588" width="155" text-anchor="end" font-family="Segoe UI, Microsoft YaHei" font-size="22" font-weight="900" fill="#111111">
    Playbook
  </text>

  <!-- bottom headline -->
  <text x="647" y="607" width="360" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="28" font-weight="900" fill="#111111">
    The Next Growth System
  </text>
  <text x="647" y="631" width="330" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#555555">
    A cover-story layout for executive summaries, launches, and keynote section breaks.
  </text>

  <!-- barcode -->
  <rect x="797" y="616" width="5" height="34" fill="#111111"/>
  <rect x="806" y="616" width="2" height="34" fill="#111111"/>
  <rect x="813" y="616" width="7" height="34" fill="#111111"/>
  <rect x="825" y="616" width="3" height="34" fill="#111111"/>
  <rect x="833" y="616" width="9" height="34" fill="#111111"/>
  <rect x="847" y="616" width="2" height="34" fill="#111111"/>
  <rect x="853" y="616" width="5" height="34" fill="#111111"/>
  <text x="828" y="665" width="80" text-anchor="middle" font-family="Segoe UI, Microsoft YaHei" font-size="8" fill="#333333">
    9 771422 03125
  </text>

  <!-- rotated spine label -->
  <text x="386" y="555" width="300" transform="rotate(-90 386 555)" font-family="Segoe UI, Microsoft YaHei" font-size="11" font-weight="800" fill="#DC143C" letter-spacing="2">
    VANGUARD / EXECUTIVE EDITION
  </text>
</svg>
```

## Avoid in this skill
- ❌ Do not use `<textPath>` or SVG warping to curve the masthead; approximate editorial WordArt with oversized type, tracking, layering, and manual positioning.
- ❌ Do not use `<mask>` to remove a photo background; supply a transparent PNG/SVG cutout as the central `<image>`.
- ❌ Do not place the thick border above the subject if you want the “popping out of the cover” effect; the subject must overlap the frame.
- ❌ Do not apply `clip-path` to groups, rectangles, or paths for this technique; clipping is only reliable on `<image>`.
- ❌ Do not change the SVG canvas to portrait dimensions; keep `viewBox="0 0 1280 720"` and build the portrait cover as a centered panel inside it.

## Composition notes
- Keep the portrait cover panel tall and centered, occupying roughly 75–90% of slide height; the surrounding dark stage makes the cover feel premium and intentional.
- Put the masthead very high and very large, then let the cutout subject overlap its lower portion for magazine-style depth.
- Reserve narrow left and right columns for teaser headlines; avoid placing dense text over the subject’s face or torso.
- Repeat one strong accent color across the frame, masthead, rules, labels, and burst shapes to create editorial rhythm.