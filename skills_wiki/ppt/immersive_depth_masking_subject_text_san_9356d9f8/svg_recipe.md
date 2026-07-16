# SVG Recipe — Immersive Depth Masking (Subject-Text Sandwich)

## Visual mechanism
Create depth by stacking a cutout photographic subject in front of oversized typography, so the subject occludes part of the word and forces the viewer to mentally complete it. Add a dark cinematic background, text shadow, and subtle particle trails behind the text to make the slide feel like an editorial keynote cover rather than a flat title card.

## SVG primitives needed
- 1× `<rect>` for the full-bleed black background
- 1× `<radialGradient>` for a soft warm vignette glow behind the title
- 1× `<linearGradient>` for a metallic gray title fill
- 2× `<filter>` definitions: one soft glow for particles, one deep shadow for typography/subject
- 10× `<path>` for abstract luminous motion trails behind the title
- 40+× `<circle>` for small particle nodes along the trails
- 2× `<text>` for the giant stacked title words, placed behind the subject
- 1× transparent `<image>` for the foreground cutout subject
- 1× grouped PowerPoint-style decorative icon built from `<circle>`, `<rect>`, and `<text>` to echo the presentation theme
- Optional 1× `<text>` eyebrow/caption for context, kept small so it does not compete with the sandwich effect

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <radialGradient id="warmVignette" cx="72%" cy="46%" r="58%">
      <stop offset="0%" stop-color="#2a1c13"/>
      <stop offset="46%" stop-color="#090807"/>
      <stop offset="100%" stop-color="#000000"/>
    </radialGradient>

    <linearGradient id="titleMetal" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#ffffff"/>
      <stop offset="48%" stop-color="#cfcfcf"/>
      <stop offset="100%" stop-color="#8e8e8e"/>
    </linearGradient>

    <filter id="textDepth" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="14" result="off"/>
      <feGaussianBlur in="off" stdDeviation="12" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="particleGlow" x="-80%" y="-80%" width="260%" height="260%">
      <feGaussianBlur stdDeviation="3"/>
    </filter>

    <filter id="subjectShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feOffset dx="18" dy="10" result="off"/>
      <feGaussianBlur in="off" stdDeviation="18" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <!-- Layer 1: cinematic background -->
  <rect x="0" y="0" width="1280" height="720" fill="url(#warmVignette)"/>
  <rect x="0" y="0" width="1280" height="720" fill="#000000" opacity="0.55"/>

  <!-- Layer 2: abstract motion trails behind typography -->
  <g opacity="0.72" fill="none" stroke-linecap="round">
    <path d="M650 105 C760 40, 835 165, 935 92 C1010 38, 1108 62, 1250 16" stroke="#d7c8ad" stroke-width="1.2" opacity="0.62"/>
    <path d="M670 126 C820 88, 850 235, 1010 175 C1120 135, 1180 210, 1265 160" stroke="#f1e2c3" stroke-width="0.8" opacity="0.48"/>
    <path d="M570 195 C705 135, 800 210, 925 228 C1065 248, 1130 330, 1270 292" stroke="#bfae91" stroke-width="1.1" opacity="0.58"/>
    <path d="M610 430 C735 325, 880 415, 1010 360 C1130 310, 1190 438, 1270 390" stroke="#e8d9bd" stroke-width="1.1" opacity="0.55"/>
    <path d="M690 510 C810 445, 890 560, 1020 515 C1150 468, 1185 610, 1268 560" stroke="#c8b899" stroke-width="0.9" opacity="0.50"/>
    <path d="M780 80 C740 175, 880 220, 820 310 C760 400, 920 430, 875 545" stroke="#988973" stroke-width="0.8" opacity="0.46"/>
    <path d="M1035 35 C955 155, 1115 220, 1045 338 C970 462, 1110 520, 1048 665" stroke="#f6e8cb" stroke-width="0.9" opacity="0.45"/>
    <path d="M620 360 C705 305, 740 455, 820 390 C900 328, 965 404, 1035 330" stroke="#ffffff" stroke-width="0.7" opacity="0.32"/>
    <path d="M900 640 C1005 560, 1085 705, 1195 600 C1235 562, 1260 560, 1280 578" stroke="#d6c6a6" stroke-width="1.0" opacity="0.50"/>
    <path d="M735 235 C810 315, 720 385, 802 462 C865 522, 955 452, 1020 488" stroke="#b19f84" stroke-width="0.8" opacity="0.42"/>
  </g>

  <!-- Particle nodes on top of trails -->
  <g fill="#e9dac0" filter="url(#particleGlow)" opacity="0.86">
    <circle cx="690" cy="99" r="2.4"/><circle cx="735" cy="82" r="1.8"/><circle cx="815" cy="136" r="2.1"/>
    <circle cx="900" cy="106" r="1.7"/><circle cx="980" cy="83" r="2.5"/><circle cx="1115" cy="61" r="1.8"/>
    <circle cx="1208" cy="36" r="2.2"/><circle cx="705" cy="162" r="1.9"/><circle cx="785" cy="190" r="2.2"/>
    <circle cx="895" cy="220" r="1.6"/><circle cx="1018" cy="183" r="2.5"/><circle cx="1168" cy="210" r="1.8"/>
    <circle cx="638" cy="414" r="2.1"/><circle cx="735" cy="360" r="1.7"/><circle cx="840" cy="395" r="2.3"/>
    <circle cx="960" cy="380" r="1.8"/><circle cx="1085" cy="334" r="2.2"/><circle cx="1215" cy="395" r="1.7"/>
    <circle cx="710" cy="525" r="2.2"/><circle cx="805" cy="486" r="1.8"/><circle cx="920" cy="548" r="2.4"/>
    <circle cx="1030" cy="515" r="1.6"/><circle cx="1145" cy="520" r="2.1"/><circle cx="1238" cy="560" r="1.8"/>
    <circle cx="790" cy="78" r="1.5"/><circle cx="838" cy="302" r="2.0"/><circle cx="870" cy="540" r="1.6"/>
    <circle cx="1035" cy="36" r="2.1"/><circle cx="1048" cy="322" r="1.8"/><circle cx="1050" cy="650" r="2.2"/>
  </g>

  <!-- Layer 3: massive typography, intentionally behind the subject -->
  <g filter="url(#textDepth)">
    <text x="480" y="258" width="725" fill="url(#titleMetal)"
          font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="112"
          font-weight="900" letter-spacing="5">ANIMATED</text>
    <text x="475" y="374" width="745" fill="#ffffff"
          font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="122"
          font-weight="900" letter-spacing="3">MASKING</text>
  </g>

  <!-- Small supporting label; still behind subject -->
  <text x="485" y="430" width="380" fill="#b7a78d" opacity="0.82"
        font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="20"
        font-weight="600" letter-spacing="4">SUBJECT · TEXT · DEPTH</text>

  <!-- Layer 4: foreground transparent PNG subject occluding the text -->
  <image x="-35" y="48" width="640" height="670" preserveAspectRatio="xMidYMid meet"
         filter="url(#subjectShadow)"
         href="https://images.example.com/transparent-cutout-black-and-white-panda-facing-camera.png"/>

  <!-- Optional deck/product cue, placed in front but away from the main text sandwich -->
  <g transform="translate(812 485)" filter="url(#particleGlow)">
    <circle cx="75" cy="75" r="82" fill="#ffffff" opacity="0.24"/>
    <circle cx="75" cy="75" r="70" fill="#f56f43"/>
    <path d="M75 5 A70 70 0 0 1 145 75 L75 75 Z" fill="#ff9b78" opacity="0.88"/>
    <path d="M75 75 L145 75 A70 70 0 0 1 35 130 Z" fill="#d94822" opacity="0.82"/>
    <rect x="-35" y="25" width="100" height="100" rx="8" fill="#c9412a"/>
    <text x="-4" y="91" width="70" fill="#ffffff"
          font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="70"
          font-weight="400">P</text>
  </g>
</svg>
```

## Avoid in this skill
- ❌ Using an ordinary rectangular photo as the foreground subject; the effect depends on a transparent cutout PNG or carefully pre-isolated subject image.
- ❌ Applying `clip-path` or masks to text to fake the overlap; PowerPoint editability is better when the subject image simply sits above the text in z-order.
- ❌ Thin or small typography; the word must be oversized and heavy enough that partial occlusion still reads clearly.
- ❌ Busy backgrounds directly behind the subject’s edges; keep the subject silhouette readable with dark negative space or a subtle halo.
- ❌ SVG `<mask>`, `<textPath>`, `<pattern>`, or `<use>`; these are unnecessary here and may not translate cleanly.

## Composition notes
- Put the background and decorative trails first, the giant title second, and the transparent subject last so the subject physically covers the letters.
- Let the subject occupy 40–55% of slide width and anchor it to the bottom edge; this makes the overlap feel intentional and dimensional.
- Keep the title centered vertically but shifted toward the open side of the subject, with 5–10% of the first letters hidden behind the subject.
- Use a restrained palette: black base, white/gray type, warm beige particles, and one saturated accent only if a logo or product cue is needed.