# SVG Recipe — Dynamic News Broadcast Opener

## Visual mechanism
A high-energy opener built from overlapping diagonal blue panels, bright broadcast accent slashes, dot-matrix textures, and compact “live data” widgets around a bold central title. The asymmetry and angled geometry create the feeling of a fast news bumper frozen at its strongest keyframe.

## SVG primitives needed
- 1× `<rect>` for the full-slide deep blue base
- 5× `<path>` for large angled background panels and dark depth planes
- 3× `<path>` for thick diagonal cyan/yellow broadcast slashes
- 1× `<image>` clipped into a rounded news-thumbnail card
- 1× `<clipPath>` using `<rect rx>` applied only to the image
- 2× `<linearGradient>` for blue panel depth and metallic title glow
- 1× `<radialGradient>` for a subtle center-stage glow
- 2× `<filter>` definitions: one soft shadow and one cyan glow, applied to rect/path/text
- 30–50× `<circle>` for dot-matrix broadcast texture
- 10–16× `<line>` for diagonal grid and ticker guide lines
- 8–12× `<rect>` for data widgets, progress bars, labels, and lower-third elements
- 6–8× `<text>` elements with explicit `width` attributes for main title, side labels, metadata, and ticker text

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bluePanel" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#008CFF"/>
      <stop offset="55%" stop-color="#005DDA"/>
      <stop offset="100%" stop-color="#013C9E"/>
    </linearGradient>
    <linearGradient id="titleMetal" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="45%" stop-color="#DDF6FF"/>
      <stop offset="70%" stop-color="#FFFFFF"/>
      <stop offset="100%" stop-color="#BDEFFF"/>
    </linearGradient>
    <radialGradient id="centerGlow" cx="50%" cy="52%" r="45%">
      <stop offset="0%" stop-color="#00CCEE" stop-opacity="0.42"/>
      <stop offset="60%" stop-color="#0070FF" stop-opacity="0.12"/>
      <stop offset="100%" stop-color="#001E5A" stop-opacity="0"/>
    </radialGradient>
    <filter id="shadow" x="-20%" y="-20%" width="140%" height="140%">
      <feOffset dx="0" dy="10"/>
      <feGaussianBlur stdDeviation="12"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="cyanGlow" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="8"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <clipPath id="newsThumbClip">
      <rect x="902" y="86" width="244" height="132" rx="18"/>
    </clipPath>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#0152CC"/>
  <rect x="0" y="0" width="1280" height="720" fill="url(#centerGlow)"/>

  <path d="M0 0 L510 0 L318 720 L0 720 Z" fill="url(#bluePanel)" opacity="0.9"/>
  <path d="M1280 0 L1280 720 L810 720 L1012 0 Z" fill="#003C9E" opacity="0.62"/>
  <path d="M0 510 L360 250 L770 720 L0 720 Z" fill="#002B78" opacity="0.42"/>
  <path d="M760 0 L1280 0 L1280 250 L950 345 Z" fill="#00A6FF" opacity="0.28"/>
  <path d="M190 0 L410 0 L80 720 L0 720 L0 610 Z" fill="#001D57" opacity="0.38"/>

  <line x1="76" y1="20" x2="1180" y2="700" stroke="#FFFFFF" stroke-opacity="0.12" stroke-width="2"/>
  <line x1="132" y1="0" x2="1236" y2="680" stroke="#FFFFFF" stroke-opacity="0.08" stroke-width="1"/>
  <line x1="0" y1="108" x2="1020" y2="720" stroke="#FFFFFF" stroke-opacity="0.1" stroke-width="1.5"/>
  <line x1="1280" y1="142" x2="192" y2="720" stroke="#00CCEE" stroke-opacity="0.18" stroke-width="2"/>
  <line x1="1280" y1="204" x2="268" y2="720" stroke="#00CCEE" stroke-opacity="0.13" stroke-width="1"/>

  <path d="M-70 82 L1110 720" stroke="#FFDC00" stroke-width="24" stroke-linecap="square" opacity="0.95" filter="url(#shadow)"/>
  <path d="M1280 150 L130 720" stroke="#00CCEE" stroke-width="20" stroke-linecap="square" opacity="0.88" filter="url(#cyanGlow)"/>
  <path d="M-30 610 L760 132" stroke="#FFFFFF" stroke-width="5" stroke-linecap="square" opacity="0.35"/>

  <g opacity="0.62">
    <circle cx="72" cy="298" r="3" fill="#FFFFFF"/><circle cx="96" cy="298" r="3" fill="#FFFFFF"/><circle cx="120" cy="298" r="3" fill="#FFFFFF"/><circle cx="144" cy="298" r="3" fill="#FFFFFF"/>
    <circle cx="72" cy="322" r="3" fill="#FFFFFF"/><circle cx="96" cy="322" r="3" fill="#FFFFFF"/><circle cx="120" cy="322" r="3" fill="#FFFFFF"/><circle cx="144" cy="322" r="3" fill="#FFFFFF"/>
    <circle cx="72" cy="346" r="3" fill="#FFFFFF"/><circle cx="96" cy="346" r="3" fill="#FFFFFF"/><circle cx="120" cy="346" r="3" fill="#FFFFFF"/><circle cx="144" cy="346" r="3" fill="#FFFFFF"/>
    <circle cx="72" cy="370" r="3" fill="#FFFFFF"/><circle cx="96" cy="370" r="3" fill="#FFFFFF"/><circle cx="120" cy="370" r="3" fill="#FFFFFF"/><circle cx="144" cy="370" r="3" fill="#FFFFFF"/>
  </g>

  <g opacity="0.7">
    <circle cx="1032" cy="46" r="3" fill="#DDF6FF"/><circle cx="1056" cy="46" r="3" fill="#DDF6FF"/><circle cx="1080" cy="46" r="3" fill="#DDF6FF"/><circle cx="1104" cy="46" r="3" fill="#DDF6FF"/><circle cx="1128" cy="46" r="3" fill="#DDF6FF"/>
    <circle cx="1032" cy="70" r="3" fill="#DDF6FF"/><circle cx="1056" cy="70" r="3" fill="#DDF6FF"/><circle cx="1080" cy="70" r="3" fill="#DDF6FF"/><circle cx="1104" cy="70" r="3" fill="#DDF6FF"/><circle cx="1128" cy="70" r="3" fill="#DDF6FF"/>
    <circle cx="1032" cy="94" r="3" fill="#DDF6FF"/><circle cx="1056" cy="94" r="3" fill="#DDF6FF"/><circle cx="1080" cy="94" r="3" fill="#DDF6FF"/><circle cx="1104" cy="94" r="3" fill="#DDF6FF"/><circle cx="1128" cy="94" r="3" fill="#DDF6FF"/>
  </g>

  <rect x="880" y="66" width="286" height="178" rx="22" fill="#001D57" opacity="0.76" filter="url(#shadow)"/>
  <image x="902" y="86" width="244" height="132" clip-path="url(#newsThumbClip)"
         href="https://images.example.com/news-broadcast-global-city-skyline-finance-control-room.jpg"/>
  <rect x="916" y="196" width="92" height="10" rx="5" fill="#FFDC00"/>
  <text x="1020" y="207" width="120" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#FFFFFF">GLOBAL FEED</text>

  <rect x="162" y="118" width="178" height="42" rx="8" fill="#001D57" opacity="0.72"/>
  <rect x="174" y="132" width="14" height="14" rx="2" fill="#FFDC00"/>
  <text x="198" y="145" width="130" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#FFFFFF">LIVE SIGNAL</text>

  <rect x="174" y="548" width="250" height="54" rx="10" fill="#001D57" opacity="0.72"/>
  <rect x="194" y="575" width="166" height="7" rx="3.5" fill="#174EA6"/>
  <rect x="194" y="575" width="112" height="7" rx="3.5" fill="#00CCEE"/>
  <text x="194" y="567" width="210" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#D7E8FF">x International · x Finance</text>

  <text x="42" y="118" width="44" font-family="Segoe UI, Microsoft YaHei" font-size="28" font-weight="800" fill="#C8D7EA" opacity="0.58">L<br/>I<br/>V<br/>E</text>
  <text x="1196" y="380" width="54" font-family="Segoe UI, Microsoft YaHei" font-size="25" font-weight="800" fill="#C8D7EA" opacity="0.52">S<br/>T<br/>R<br/>E<br/>A<br/>M</text>

  <rect x="384" y="288" width="514" height="122" rx="20" fill="#001D57" opacity="0.34" filter="url(#shadow)"/>
  <text x="410" y="352" width="470" font-family="Segoe UI, Microsoft YaHei" font-size="70" font-weight="900" letter-spacing="-2" fill="url(#titleMetal)" filter="url(#cyanGlow)">SET iNEWS</text>
  <text x="420" y="389" width="440" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="700" letter-spacing="4" fill="#FFDC00">MARKET INTELLIGENCE · BREAKING INSIGHT</text>

  <rect x="0" y="654" width="1280" height="66" fill="#001844" opacity="0.88"/>
  <rect x="0" y="654" width="176" height="66" fill="#FFDC00"/>
  <text x="32" y="696" width="120" font-family="Segoe UI, Microsoft YaHei" font-size="28" font-weight="900" fill="#001844">NOW</text>
  <text x="204" y="694" width="930" font-family="Segoe UI, Microsoft YaHei" font-size="22" font-weight="700" fill="#FFFFFF">Executive Briefing Opens · Technology, Finance, and Global Trends</text>
  <rect x="1150" y="674" width="72" height="14" rx="7" fill="#00CCEE"/>
  <rect x="1150" y="696" width="44" height="7" rx="3.5" fill="#FFFFFF" opacity="0.75"/>
</svg>
```

## Avoid in this skill
- ❌ Do not use animated SVG wipes or `<animateTransform>` for the broadcast motion; reproduce the strongest static keyframe instead.
- ❌ Do not use `<mask>` for diagonal panel reveals; build panels directly with editable `<path>` geometry.
- ❌ Do not put `filter` on `<line>` elements; use filtered `<path>` strokes for glowing diagonal slashes.
- ❌ Do not use `marker-end` for arrows in data widgets; use small rectangles, circles, and plain lines instead.
- ❌ Do not rely on `<pattern>` for dot matrices; place repeated editable `<circle>` elements.

## Composition notes
- Keep the main title centered but slightly compressed inside a dark translucent title slab so it remains readable over the energetic background.
- Use diagonal elements to connect corners: yellow from upper-left to lower-right, cyan from upper-right to lower-left.
- Reserve the top-right for a clipped “live feed” image card and the lower band for a ticker, creating a believable broadcast system.
- Balance the high-saturation cyan/yellow accents with large fields of deep blue negative space so the slide feels premium, not chaotic.