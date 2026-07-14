# SVG Recipe — Bold Split-Background Typographic Transition

## Visual mechanism
A transition card built from full-bleed horizontal color bands and oversized, ultra-heavy all-caps typography. The text block deliberately crosses band boundaries so the flat background becomes a structured graphic field rather than a plain title slide.

## SVG primitives needed
- 3× `<rect>` for the full-width horizontal split-background bands
- 2× `<rect>` for thin separator highlights between bands
- 2× `<path>` for oversized translucent diagonal “edge energy” accents at the right side
- 1× `<filter id="typeShadow">` with `feOffset + feGaussianBlur + feMerge` applied to the main typographic block
- 1× `<text>` with nested `<tspan>` lines for the massive central headline
- 3× `<text>` for small editorial metadata, slide number, and transition cue
- 2× `<line>` for small framing accents

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <filter id="typeShadow" x="-10%" y="-10%" width="120%" height="120%">
      <feOffset dx="0" dy="4" in="SourceAlpha" result="offset"/>
      <feGaussianBlur stdDeviation="3" in="offset" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <!-- full-bleed split background -->
  <rect x="0" y="0" width="1280" height="240" fill="#8ECAC9"/>
  <rect x="0" y="240" width="1280" height="240" fill="#679C9B"/>
  <rect x="0" y="480" width="1280" height="240" fill="#4A7675"/>

  <!-- crisp band seams -->
  <rect x="0" y="239" width="1280" height="2" fill="#FFFFFF" opacity="0.18"/>
  <rect x="0" y="479" width="1280" height="2" fill="#FFFFFF" opacity="0.14"/>

  <!-- oversized translucent graphic accents -->
  <path d="M1040 -40 L1280 -40 L1280 225 L1168 225 Z" fill="#FFFFFF" opacity="0.10"/>
  <path d="M1112 492 L1280 492 L1280 760 L982 760 Z" fill="#143D3C" opacity="0.16"/>

  <!-- small editorial label -->
  <text x="92" y="82" width="520"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="20"
        font-weight="700"
        letter-spacing="3"
        fill="#FFFFFF"
        opacity="0.88">
    QBR PLAYBOOK
  </text>

  <line x1="92" y1="104" x2="250" y2="104" stroke="#FFFFFF" stroke-width="4" opacity="0.75"/>
  <line x1="264" y1="104" x2="310" y2="104" stroke="#143D3C" stroke-width="4" opacity="0.45"/>

  <!-- giant transition headline -->
  <text x="88" y="236" width="1040"
        font-family="Arial Black, Impact, Segoe UI, Microsoft YaHei, sans-serif"
        font-size="98"
        font-weight="900"
        letter-spacing="-3"
        fill="#FFFFFF"
        filter="url(#typeShadow)">
    <tspan x="88" dy="0">MAKE YOUR</tspan>
    <tspan x="88" dy="94">QBR MORE</tspan>
    <tspan x="88" dy="94">INTERESTING</tspan>
  </text>

  <!-- subtle chapter numeral, editable text -->
  <text x="915" y="420" width="320"
        font-family="Arial Black, Impact, Segoe UI, Microsoft YaHei, sans-serif"
        font-size="230"
        font-weight="900"
        letter-spacing="-10"
        fill="#FFFFFF"
        opacity="0.10">
    01
  </text>

  <!-- bottom transition cue -->
  <text x="92" y="646" width="720"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="19"
        font-weight="600"
        letter-spacing="2"
        fill="#FFFFFF"
        opacity="0.76">
    TRANSITION SLIDE  •  PUSH UP INTO NEXT SECTION
  </text>

  <!-- right-side framing accent -->
  <line x1="1168" y1="84" x2="1168" y2="184" stroke="#FFFFFF" stroke-width="6" opacity="0.55"/>
  <text x="1188" y="116" width="70"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="18"
        font-weight="800"
        fill="#FFFFFF"
        opacity="0.82">
    NEXT
  </text>
</svg>
```

## Avoid in this skill
- ❌ Using a single flat background color; the banding is what makes the slide feel intentionally designed.
- ❌ Small or medium-weight typography; this technique depends on extreme scale and heavy font weight.
- ❌ Center-aligning the headline by default; left alignment creates a stronger editorial keynote feel.
- ❌ Simulating the text as an image; keep it native `<text>` so the headline remains editable in PowerPoint.
- ❌ Adding complex icons, charts, or photos; they dilute the bold transition-card purpose.

## Composition notes
- Keep the headline left-aligned with a generous margin, roughly 7–9% of slide width.
- Let the large type overlap the horizontal band seams; this is the main visual interaction.
- Use 2–3 analogous colors with clear value steps, from lighter top band to darker bottom band.
- Reserve small labels and cues for the corners only; the center should be dominated by the giant statement.