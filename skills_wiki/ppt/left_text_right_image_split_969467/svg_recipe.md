# SVG Recipe — Left Text Right Image Split

## Visual mechanism
A premium editorial split: the left half is calm negative space for headline, copy, and a small proof point; the right half is a full-height hero image cropped by a soft curved diagonal edge. Subtle gradients, translucent overlays, and a floating accent card make the split feel intentional rather than like a simple two-column grid.

## SVG primitives needed
- 1× `<rect>` for the warm slide background
- 1× `<image>` for the right-side full-height hero photo
- 1× `<clipPath>` with `<path>` to crop the hero image into a curved split shape
- 3× `<linearGradient>` for the background wash, image vignette, and accent fills
- 1× `<radialGradient>` for a soft decorative glow behind the text
- 2× `<filter>` definitions for soft card shadow and text glow
- 4× `<path>` for the image overlay, curved separator highlight, decorative blob, and small brand mark
- 3× `<rect>` for eyebrow pill, CTA button, and floating image caption card
- 1× `<line>` for a simple divider/accent rule
- 7× `<text>` elements with explicit `width` attributes for headline, body, eyebrow, CTA, metric, metric label, and image caption

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgWash" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#F7F1E8"/>
      <stop offset="62%" stop-color="#FBF8F2"/>
      <stop offset="100%" stop-color="#EEF2F4"/>
    </linearGradient>

    <linearGradient id="imageVignette" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#0E1726" stop-opacity="0.58"/>
      <stop offset="42%" stop-color="#0E1726" stop-opacity="0.18"/>
      <stop offset="100%" stop-color="#0E1726" stop-opacity="0.06"/>
    </linearGradient>

    <linearGradient id="goldAccent" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#D8B56D"/>
      <stop offset="100%" stop-color="#A67835"/>
    </linearGradient>

    <radialGradient id="leftGlow" cx="50%" cy="50%" r="55%">
      <stop offset="0%" stop-color="#F0C987" stop-opacity="0.34"/>
      <stop offset="100%" stop-color="#F0C987" stop-opacity="0"/>
    </radialGradient>

    <filter id="softShadow" x="-30%" y="-30%" width="160%" height="160%">
      <feOffset dx="0" dy="14"/>
      <feGaussianBlur stdDeviation="16"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="subtleGlow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="2.5"/>
    </filter>

    <clipPath id="rightImageClip">
      <path d="M664 0 H1280 V720 H552 C625 588 637 472 621 357 C604 238 610 122 664 0 Z"/>
    </clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgWash)"/>

  <path d="M82 92 C168 38 286 58 331 148 C382 249 307 337 189 332 C83 328 31 263 42 185 C48 142 58 110 82 92 Z"
        fill="url(#leftGlow)" opacity="0.9"/>

  <image href="https://images.example.com/premium-hero-photo-modern-architecture-interior-with-warm-light.jpg"
         x="520" y="0" width="760" height="720" preserveAspectRatio="xMidYMid slice"
         clip-path="url(#rightImageClip)"/>

  <path d="M664 0 H1280 V720 H552 C625 588 637 472 621 357 C604 238 610 122 664 0 Z"
        fill="url(#imageVignette)"/>

  <path d="M642 0 C585 130 585 242 602 357 C619 474 604 593 538 720"
        fill="none" stroke="#FFFFFF" stroke-opacity="0.58" stroke-width="2"/>

  <path d="M98 122 L119 110 L140 122 L140 147 L119 160 L98 147 Z"
        fill="url(#goldAccent)"/>
  <text x="158" y="142" width="260" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="15" font-weight="700" letter-spacing="2.8" fill="#9A6A2E">SIGNAL / 2026</text>

  <rect x="88" y="184" width="182" height="34" rx="17" fill="#FFFFFF" opacity="0.82"/>
  <text x="108" y="207" width="145" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="13" font-weight="700" letter-spacing="1.9" fill="#6B7280">EDITORIAL SPLIT</text>

  <text x="86" y="294" width="500" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="64" font-weight="750" line-height="1.02" fill="#172033">
    <tspan x="86" dy="0">Designing</tspan>
    <tspan x="86" dy="68">for decisive</tspan>
    <tspan x="86" dy="68">moments.</tspan>
  </text>

  <text x="90" y="474" width="485" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="20" line-height="1.45" fill="#536071">
    <tspan x="90" dy="0">Use the left side for the idea, implication, or strategic</tspan>
    <tspan x="90" dy="30">message. Let the image own the emotional context</tspan>
    <tspan x="90" dy="30">without competing for reading attention.</tspan>
  </text>

  <line x1="90" y1="585" x2="338" y2="585" stroke="#C9B28B" stroke-width="2"/>

  <text x="90" y="638" width="130" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="46" font-weight="760" fill="#172033">72%</text>
  <text x="205" y="625" width="250" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="15" line-height="1.35" fill="#667085">
    <tspan x="205" dy="0">faster executive read-through</tspan>
    <tspan x="205" dy="22">when one visual owns the slide.</tspan>
  </text>

  <rect x="430" y="606" width="154" height="46" rx="23" fill="#172033" filter="url(#softShadow)"/>
  <text x="462" y="635" width="96" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="15" font-weight="700" letter-spacing="1.4" fill="#FFFFFF">VIEW CASE</text>

  <rect x="842" y="548" width="298" height="92" rx="22" fill="#FFFFFF" opacity="0.92" filter="url(#softShadow)"/>
  <path d="M872 593 C884 568 923 567 936 593 C922 618 884 620 872 593 Z"
        fill="#172033" opacity="0.92"/>
  <circle cx="904" cy="593" r="9" fill="url(#goldAccent)"/>
  <text x="958" y="585" width="150" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="13" font-weight="700" letter-spacing="1.3" fill="#98A2B3">VISUAL ANCHOR</text>
  <text x="958" y="612" width="155" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="18" font-weight="700" fill="#172033">Image carries mood</text>
</svg>
```

## Avoid in this skill
- ❌ A hard 50/50 vertical rectangle split with no edge treatment; it will look like a template, not an editorial keynote slide.
- ❌ Applying `clip-path` to overlay shapes; only clip the `<image>` and draw matching overlay paths separately.
- ❌ Dense bullet lists on the left; the layout works best with one strong headline, one short paragraph, and one proof point.
- ❌ Low-contrast image areas behind important right-side labels; add a vignette overlay or white caption card if text must sit over the photo.
- ❌ Using `marker-end` on curved paths for arrows; if an arrow is needed, use a native `<line>` with arrow styling handled separately.

## Composition notes
- Keep the left text block inside roughly `x=80–590`; preserve generous margins so the curved image edge has room to breathe.
- Let the hero image occupy the full slide height and at least the right 55% of the canvas for cinematic impact.
- Use a soft curved or diagonal image crop to create motion while keeping the left reading column stable.
- Repeat one accent color, such as warm gold, in the brand mark, divider, and small image detail to tie both halves together.