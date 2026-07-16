# SVG Recipe — Precision Color Control with RGB & HSL Models

## Visual mechanism
Show color precision as a premium “color lab” comparison: two large editable color specimens sit inside dark glass panels, with RGB shown as direct channel control and HSL shown as perceptual hue/saturation/lightness control. The slide teaches that every swatch is defined by exact numeric values, not theme defaults.

## SVG primitives needed
- 1× `<rect>` for the full-slide dark gradient background
- 2× `<path>` for soft abstract decorative blobs behind the content
- 2× `<rect>` for glass-style comparison panels with shadow
- 2× `<rect>` for large rounded color specimen cards
- 6× `<rect>` for RGB and HSL component tracks
- 6× `<circle>` for slider handles on component tracks
- 1× `<rect>` with a multi-stop hue gradient for the HSL hue strip
- 3× `<line>` for subtle vertical dividers and callout connectors
- Multiple `<text>` elements with explicit `width` for title, labels, numeric color values, and teaching notes
- 1× `<filter id="softShadow">` applied to panels and specimen cards
- 1× `<filter id="glow">` applied to the active color specimens
- Multiple `<linearGradient>` definitions for background, panels, RGB channel bars, and HSL hue strip

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1280" y2="720">
      <stop offset="0%" stop-color="#0B1020"/>
      <stop offset="55%" stop-color="#121A33"/>
      <stop offset="100%" stop-color="#070A12"/>
    </linearGradient>
    <linearGradient id="panelFill" x1="0" y1="80" x2="0" y2="650">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.13"/>
      <stop offset="100%" stop-color="#FFFFFF" stop-opacity="0.045"/>
    </linearGradient>
    <linearGradient id="rBar" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#230000"/><stop offset="100%" stop-color="#FF0000"/>
    </linearGradient>
    <linearGradient id="gBar" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#001800"/><stop offset="100%" stop-color="#00FF55"/>
    </linearGradient>
    <linearGradient id="bBar" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#000A22"/><stop offset="100%" stop-color="#0077FF"/>
    </linearGradient>
    <linearGradient id="hueBar" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#FF0000"/><stop offset="16.6%" stop-color="#FFFF00"/>
      <stop offset="33.3%" stop-color="#00FF00"/><stop offset="50%" stop-color="#00FFFF"/>
      <stop offset="66.6%" stop-color="#0000FF"/><stop offset="83.3%" stop-color="#FF00FF"/>
      <stop offset="100%" stop-color="#FF0000"/>
    </linearGradient>
    <linearGradient id="satBar" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#8C8C8C"/><stop offset="100%" stop-color="#2B9CED"/>
    </linearGradient>
    <linearGradient id="lightBar" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#000000"/><stop offset="50%" stop-color="#2B9CED"/><stop offset="100%" stop-color="#FFFFFF"/>
    </linearGradient>
    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="18"/>
      <feGaussianBlur stdDeviation="18"/>
      <feMerge><feMergeNode/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <filter id="glow" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="10"/>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="url(#bg)"/>
  <path d="M-30,115 C140,12 260,55 330,155 C405,260 250,330 110,295 C-25,260 -95,190 -30,115 Z" fill="#FF5722" opacity="0.16"/>
  <path d="M1025,420 C1165,335 1290,385 1345,500 C1400,615 1255,710 1110,665 C970,622 900,500 1025,420 Z" fill="#2B9CED" opacity="0.18"/>

  <text x="72" y="70" width="820" font-family="Segoe UI, Microsoft YaHei" font-size="38" font-weight="700" fill="#FFFFFF">Precision Color Control</text>
  <text x="73" y="108" width="760" font-family="Segoe UI, Microsoft YaHei" font-size="18" fill="#AEB9D6">Use exact RGB values for digital fidelity; use HSL values to tune perception, mood, and hierarchy.</text>
  <text x="1060" y="82" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#7EE6FF" text-anchor="middle">BRAND-SAFE COLOR</text>

  <rect x="70" y="145" width="540" height="500" rx="34" fill="url(#panelFill)" stroke="#FFFFFF" stroke-opacity="0.18" filter="url(#softShadow)"/>
  <rect x="670" y="145" width="540" height="500" rx="34" fill="url(#panelFill)" stroke="#FFFFFF" stroke-opacity="0.18" filter="url(#softShadow)"/>

  <text x="105" y="202" width="360" font-family="Segoe UI, Microsoft YaHei" font-size="25" font-weight="700" fill="#FFFFFF">RGB model</text>
  <text x="105" y="232" width="390" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#B9C3DD">Direct additive light channels: Red, Green, Blue.</text>
  <rect x="105" y="270" width="210" height="190" rx="28" fill="#FF5722" filter="url(#glow)"/>
  <rect x="105" y="270" width="210" height="190" rx="28" fill="#FF5722" stroke="#FFD0C2" stroke-opacity="0.55"/>
  <text x="345" y="316" width="200" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#FFB39E">EXACT INPUT</text>
  <text x="345" y="352" width="210" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="800" fill="#FFFFFF">#FF5722</text>
  <text x="345" y="386" width="220" font-family="Segoe UI, Microsoft YaHei" font-size="17" fill="#D7DCEF">rgb(255, 87, 34)</text>

  <text x="105" y="503" width="40" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#FF9A9A">R</text>
  <rect x="145" y="489" width="330" height="14" rx="7" fill="url(#rBar)"/>
  <circle cx="475" cy="496" r="13" fill="#FFFFFF" stroke="#FF5722" stroke-width="4"/>
  <text x="495" y="503" width="40" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#FFFFFF">255</text>
  <text x="105" y="545" width="40" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#7CFF97">G</text>
  <rect x="145" y="531" width="330" height="14" rx="7" fill="url(#gBar)"/>
  <circle cx="258" cy="538" r="13" fill="#FFFFFF" stroke="#20C35A" stroke-width="4"/>
  <text x="495" y="545" width="40" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#FFFFFF">87</text>
  <text x="105" y="587" width="40" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#82B7FF">B</text>
  <rect x="145" y="573" width="330" height="14" rx="7" fill="url(#bBar)"/>
  <circle cx="189" cy="580" r="13" fill="#FFFFFF" stroke="#2D80FF" stroke-width="4"/>
  <text x="495" y="587" width="40" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#FFFFFF">34</text>

  <line x1="640" y1="180" x2="640" y2="610" stroke="#FFFFFF" stroke-opacity="0.16" stroke-width="1"/>

  <text x="705" y="202" width="360" font-family="Segoe UI, Microsoft YaHei" font-size="25" font-weight="700" fill="#FFFFFF">HSL model</text>
  <text x="705" y="232" width="415" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#B9C3DD">Perceptual controls: Hue angle, Saturation, Lightness.</text>
  <rect x="705" y="270" width="210" height="190" rx="28" fill="#2B9CED" filter="url(#glow)"/>
  <rect x="705" y="270" width="210" height="190" rx="28" fill="#2B9CED" stroke="#BDE9FF" stroke-opacity="0.55"/>
  <text x="945" y="316" width="200" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#93DCFF">HSL → RGB</text>
  <text x="945" y="352" width="210" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="800" fill="#FFFFFF">#2B9CED</text>
  <text x="945" y="386" width="230" font-family="Segoe UI, Microsoft YaHei" font-size="17" fill="#D7DCEF">hsl(205°, 85%, 55%)</text>

  <text x="705" y="503" width="40" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#D9E6FF">H</text>
  <rect x="745" y="489" width="330" height="14" rx="7" fill="url(#hueBar)"/>
  <circle cx="933" cy="496" r="13" fill="#FFFFFF" stroke="#2B9CED" stroke-width="4"/>
  <text x="1095" y="503" width="55" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#FFFFFF">205°</text>
  <text x="705" y="545" width="40" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#D9E6FF">S</text>
  <rect x="745" y="531" width="330" height="14" rx="7" fill="url(#satBar)"/>
  <circle cx="1026" cy="538" r="13" fill="#FFFFFF" stroke="#2B9CED" stroke-width="4"/>
  <text x="1095" y="545" width="55" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#FFFFFF">85%</text>
  <text x="705" y="587" width="40" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#D9E6FF">L</text>
  <rect x="745" y="573" width="330" height="14" rx="7" fill="url(#lightBar)"/>
  <circle cx="927" cy="580" r="13" fill="#FFFFFF" stroke="#2B9CED" stroke-width="4"/>
  <text x="1095" y="587" width="55" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#FFFFFF">55%</text>

  <line x1="315" y1="365" x2="345" y2="365" stroke="#FFFFFF" stroke-opacity="0.35" stroke-width="2"/>
  <line x1="915" y1="365" x2="945" y2="365" stroke="#FFFFFF" stroke-opacity="0.35" stroke-width="2"/>
  <text x="410" y="635" width="460" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="600" fill="#FFFFFF" text-anchor="middle">Design rule: store both the visual swatch and the numeric definition so edits remain repeatable.</text>
</svg>
```

## Avoid in this skill
- ❌ Relying on PowerPoint theme colors or generic palette names when the point is exact color control
- ❌ Using CSS variables or external stylesheets for color values; keep fills/strokes explicit on each SVG element
- ❌ Using `<pattern>` fills to simulate color systems; they translate poorly and distract from the numeric color lesson
- ❌ Applying filters to `<line>` elements for slider tracks or connectors; use filters only on shapes/text that support them
- ❌ Using HSL strings if the workflow requires exact PowerPoint interoperability; annotate HSL, but set the actual shape fill as the converted RGB/hex color

## Composition notes
- Place RGB and HSL panels side by side so the viewer compares “channel precision” versus “perceptual tuning” instantly.
- Give the specimen cards generous size; the color itself should be the hero, with numeric values immediately adjacent.
- Use a dark neutral background so saturated colors appear luminous and premium without changing their defined values.
- Keep sliders subtle and clean: they explain the model, while the large swatch proves the final applied color.