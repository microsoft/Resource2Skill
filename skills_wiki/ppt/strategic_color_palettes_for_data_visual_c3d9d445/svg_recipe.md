# SVG Recipe — Strategic Color Palettes for Data Visualization

## Visual mechanism
Show four miniature charts as “palette decision cards,” where each card uses the same simple bar-chart skeleton but a different color logic: sequential, divergent, categorical, and highlight. The slide teaches that color encodes data meaning, not decoration, by pairing each palette with a concise rule and a visible data-story example.

## SVG primitives needed
- 1× `<rect>` for the full-slide premium gradient background
- 4× large rounded `<rect>` cards for the palette examples
- 4× subtle header/pill `<rect>` elements for palette type labels
- 27× small `<rect>` bars for the four miniature bar charts
- 4× thin `<line>` baselines for chart grounding
- 2× decorative `<path>` shapes for soft executive-keynote atmosphere
- 1× `<linearGradient>` for the slide background
- 1× `<linearGradient>` for the sequential palette strip
- 1× `<linearGradient>` for the divergent palette strip
- 1× `<filter id="cardShadow">` for soft card depth
- 1× `<filter id="accentGlow">` for emphasizing the highlighted bar
- Multiple `<text>` elements with explicit `width` for title, subtitles, labels, and short explanations

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#071826"/>
      <stop offset="55%" stop-color="#0D2333"/>
      <stop offset="100%" stop-color="#102D3D"/>
    </linearGradient>
    <linearGradient id="seqStrip" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#FFF2E6"/>
      <stop offset="100%" stop-color="#E67E22"/>
    </linearGradient>
    <linearGradient id="divStrip" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#2471A3"/>
      <stop offset="50%" stop-color="#F4F6F7"/>
      <stop offset="100%" stop-color="#D35400"/>
    </linearGradient>
    <filter id="cardShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="14"/>
      <feGaussianBlur stdDeviation="14"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="accentGlow" x="-60%" y="-60%" width="220%" height="220%">
      <feGaussianBlur stdDeviation="8" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bgGrad)"/>
  <path d="M-40,590 C150,505 235,665 410,585 C555,518 610,430 770,480 C930,530 1010,705 1320,590 L1320,760 L-40,760 Z" fill="#163C50" opacity="0.42"/>
  <path d="M990,-30 C1110,25 1165,105 1298,80 L1298,-40 Z" fill="#2FB7A3" opacity="0.14"/>

  <text x="70" y="72" width="760" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="34" font-weight="700" fill="#FFFFFF">Strategic Color Palettes for Data Visualization</text>
  <text x="72" y="108" width="720" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="16" fill="#AFC4CF">Choose the palette structure that matches the data story: magnitude, opposition, grouping, or focus.</text>

  <rect x="930" y="52" width="250" height="42" rx="21" fill="#FFFFFF" opacity="0.08"/>
  <circle cx="956" cy="73" r="7" fill="#2FB7A3"/>
  <text x="974" y="79" width="180" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="14" font-weight="600" fill="#D7E6EC">Color = meaning, not styling</text>

  <!-- Card 1: Sequential -->
  <g transform="translate(70 160)">
    <rect x="0" y="0" width="270" height="405" rx="24" fill="#F7FAFC" filter="url(#cardShadow)"/>
    <rect x="22" y="22" width="132" height="30" rx="15" fill="#FFE7D2"/>
    <text x="38" y="43" width="110" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" font-weight="800" fill="#C45E12">SEQUENTIAL</text>
    <text x="22" y="84" width="226" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="20" font-weight="700" fill="#1F2D36">Low → high magnitude</text>
    <text x="22" y="112" width="226" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" fill="#61717A">Use one hue that increases in intensity as values rise.</text>
    <rect x="28" y="322" width="214" height="10" rx="5" fill="url(#seqStrip)"/>
    <text x="28" y="354" width="60" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="11" font-weight="700" fill="#87939A">LOW</text>
    <text x="190" y="354" width="60" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="11" font-weight="700" fill="#87939A">HIGH</text>
    <line x1="28" y1="286" x2="242" y2="286" stroke="#DCE5EA" stroke-width="2"/>
    <rect x="35" y="238" width="20" height="48" rx="5" fill="#FFF2E6"/>
    <rect x="65" y="222" width="20" height="64" rx="5" fill="#FAD9BD"/>
    <rect x="95" y="205" width="20" height="81" rx="5" fill="#F5BF93"/>
    <rect x="125" y="182" width="20" height="104" rx="5" fill="#F0A86F"/>
    <rect x="155" y="166" width="20" height="120" rx="5" fill="#EC934D"/>
    <rect x="185" y="147" width="20" height="139" rx="5" fill="#E67E22"/>
    <rect x="215" y="128" width="20" height="158" rx="5" fill="#C96A18"/>
  </g>

  <!-- Card 2: Divergent -->
  <g transform="translate(365 160)">
    <rect x="0" y="0" width="270" height="405" rx="24" fill="#F7FAFC" filter="url(#cardShadow)"/>
    <rect x="22" y="22" width="122" height="30" rx="15" fill="#EAF2F8"/>
    <text x="38" y="43" width="100" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" font-weight="800" fill="#2471A3">DIVERGENT</text>
    <text x="22" y="84" width="226" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="20" font-weight="700" fill="#1F2D36">Below vs. above target</text>
    <text x="22" y="112" width="226" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" fill="#61717A">Use two hues that meet at a neutral midpoint.</text>
    <rect x="28" y="322" width="214" height="10" rx="5" fill="url(#divStrip)"/>
    <text x="28" y="354" width="80" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="11" font-weight="700" fill="#87939A">NEGATIVE</text>
    <text x="112" y="354" width="60" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="11" font-weight="700" fill="#87939A">TARGET</text>
    <text x="190" y="354" width="70" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="11" font-weight="700" fill="#87939A">POSITIVE</text>
    <line x1="28" y1="225" x2="242" y2="225" stroke="#DCE5EA" stroke-width="2"/>
    <rect x="35" y="141" width="17" height="84" rx="4" fill="#2471A3"/>
    <rect x="58" y="159" width="17" height="66" rx="4" fill="#5DADE2"/>
    <rect x="81" y="179" width="17" height="46" rx="4" fill="#AED6F1"/>
    <rect x="104" y="198" width="17" height="27" rx="4" fill="#D6EAF8"/>
    <rect x="127" y="211" width="17" height="14" rx="4" fill="#F4F6F7"/>
    <rect x="150" y="225" width="17" height="20" rx="4" fill="#FAD7A0"/>
    <rect x="173" y="225" width="17" height="48" rx="4" fill="#F5B041"/>
    <rect x="196" y="225" width="17" height="71" rx="4" fill="#E67E22"/>
    <rect x="219" y="225" width="17" height="92" rx="4" fill="#D35400"/>
  </g>

  <!-- Card 3: Categorical -->
  <g transform="translate(660 160)">
    <rect x="0" y="0" width="270" height="405" rx="24" fill="#F7FAFC" filter="url(#cardShadow)"/>
    <rect x="22" y="22" width="135" height="30" rx="15" fill="#EFE8F7"/>
    <text x="38" y="43" width="115" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" font-weight="800" fill="#7D3C98">CATEGORICAL</text>
    <text x="22" y="84" width="226" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="20" font-weight="700" fill="#1F2D36">Separate peer groups</text>
    <text x="22" y="112" width="226" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" fill="#61717A">Use distinct hues for discrete categories; keep the set short.</text>
    <line x1="28" y1="286" x2="242" y2="286" stroke="#DCE5EA" stroke-width="2"/>
    <rect x="41" y="184" width="26" height="102" rx="6" fill="#2980B9"/>
    <rect x="78" y="151" width="26" height="135" rx="6" fill="#27AE60"/>
    <rect x="115" y="202" width="26" height="84" rx="6" fill="#F1C40F"/>
    <rect x="152" y="132" width="26" height="154" rx="6" fill="#E67E22"/>
    <rect x="189" y="170" width="26" height="116" rx="6" fill="#8E44AD"/>
    <circle cx="46" cy="334" r="6" fill="#2980B9"/>
    <circle cx="86" cy="334" r="6" fill="#27AE60"/>
    <circle cx="126" cy="334" r="6" fill="#F1C40F"/>
    <circle cx="166" cy="334" r="6" fill="#E67E22"/>
    <circle cx="206" cy="334" r="6" fill="#8E44AD"/>
    <text x="28" y="360" width="214" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="11" font-weight="700" fill="#87939A">5 MAXIMUM FOR FAST RECOGNITION</text>
  </g>

  <!-- Card 4: Highlight -->
  <g transform="translate(955 160)">
    <rect x="0" y="0" width="270" height="405" rx="24" fill="#F7FAFC" filter="url(#cardShadow)"/>
    <rect x="22" y="22" width="103" height="30" rx="15" fill="#D8F3EE"/>
    <text x="38" y="43" width="86" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" font-weight="800" fill="#138D75">HIGHLIGHT</text>
    <text x="22" y="84" width="226" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="20" font-weight="700" fill="#1F2D36">Direct attention</text>
    <text x="22" y="112" width="226" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="13" fill="#61717A">Keep context neutral; reserve saturation for the point that matters.</text>
    <line x1="28" y1="286" x2="242" y2="286" stroke="#DCE5EA" stroke-width="2"/>
    <rect x="42" y="202" width="28" height="84" rx="6" fill="#D0D3D4"/>
    <rect x="82" y="177" width="28" height="109" rx="6" fill="#D0D3D4"/>
    <rect x="122" y="126" width="28" height="160" rx="6" fill="#16A085" filter="url(#accentGlow)"/>
    <rect x="162" y="214" width="28" height="72" rx="6" fill="#D0D3D4"/>
    <rect x="202" y="190" width="28" height="96" rx="6" fill="#D0D3D4"/>
    <circle cx="136" cy="108" r="18" fill="#16A085" opacity="0.16"/>
    <text x="102" y="104" width="90" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="12" font-weight="800" fill="#138D75">KEY DRIVER</text>
    <rect x="38" y="327" width="194" height="30" rx="15" fill="#EEF2F3"/>
    <text x="58" y="347" width="160" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="11" font-weight="700" fill="#87939A">1 ACCENT COLOR ONLY</text>
  </g>

  <text x="70" y="645" width="1120" font-family="Segoe UI, Microsoft YaHei, sans-serif" font-size="15" fill="#B8CBD4">Decision rule: if the data has order, use value progression; if it has a center point, use divergence; if it has names, use distinct hues; if it has a message, mute everything except the answer.</text>
</svg>
```

## Avoid in this skill
- ❌ Using rainbow gradients for ordered data; they add false boundaries and make “high vs. low” harder to read.
- ❌ Applying categorical colors to every bar when the story is actually a single highlighted outlier.
- ❌ Using more than five or six categorical hues in a compact executive slide; recognition drops quickly.
- ❌ Red/green-only divergent palettes without redundancy; they can be inaccessible and culturally ambiguous.
- ❌ Heavy axes, gridlines, and legends that compete with the palette lesson.

## Composition notes
- Keep the four examples equally sized so the audience compares color logic rather than chart scale.
- Use a dark, quiet background and white cards to create a premium teaching-board feel.
- Place explanatory text inside each card, but let the bars occupy the strongest visual zone.
- Reserve the most saturated color for either the divergent extremes or the highlight card’s key bar; this creates a clear color rhythm across the slide.