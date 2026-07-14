# SVG Recipe — Brutalist Minimalist Hero (Oversized Repeating Typography)

## Visual mechanism
A warm neutral canvas is dominated by huge repeated typography: one solid black line, one hollow outlined echo, then another solid line, all tightly stacked. Minimal website-like corner microcopy and subtle low-contrast geometric blocks make the slide feel like a premium web hero rather than a conventional presentation title.

## SVG primitives needed
- 1× `<rect>` for the warm off-white slide background
- 5× `<rect>` for subtle translucent geometric background blocks behind the title
- 1× `<rect>` for a thin “web page” boundary panel
- 1× `<rect>` for a small pill navigation button
- 7× `<text>` for logo, navigation, button label, vertical scroll hint, and repeating hero typography
- 1× `<line>` with arrow marker for the minimal scroll/gesture indicator
- 1× `<marker>` for the standard triangle arrowhead

## Safe-subset SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrowTip" viewBox="0 0 10 10" refX="10" refY="5" markerWidth="10" markerHeight="10" orient="auto">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#1A1A1A"/>
    </marker>
  </defs>

  <!-- warm paper background -->
  <rect x="0" y="0" width="1280" height="720" fill="#F2F2F0"/>

  <!-- faint brutalist geometry, kept low-contrast and editable -->
  <rect x="436" y="178" width="198" height="370" fill="#D8D8D3" opacity="0.42"/>
  <rect x="512" y="142" width="326" height="112" fill="#E1E1DC" opacity="0.62"/>
  <rect x="676" y="174" width="184" height="374" fill="#D2D2CC" opacity="0.36"/>
  <rect x="470" y="300" width="410" height="92" fill="#CACAC4" opacity="0.32"/>
  <rect x="520" y="456" width="380" height="86" fill="#BEBEB8" opacity="0.24"/>

  <!-- minimal web-shell frame -->
  <rect x="86" y="72" width="1108" height="576" fill="none" stroke="#1A1A1A" stroke-width="1" opacity="0.2"/>

  <!-- top-left logo -->
  <text x="104" y="112" width="180"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="17" font-weight="800" fill="#1A1A1A">huyng*</text>

  <!-- top-right navigation -->
  <text x="812" y="110" width="270"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="12" font-weight="700" fill="#1A1A1A"
        text-anchor="end">about    services    projects</text>

  <rect x="1100" y="91" width="84" height="28" rx="14" ry="14" fill="#1A1A1A"/>
  <text x="1142" y="110" width="76"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="11" font-weight="700" fill="#F2F2F0"
        text-anchor="middle">Let's Talk</text>

  <!-- oversized repeating typography -->
  <text x="640" y="292" width="900"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="76" font-weight="900" fill="#1A1A1A"
        text-anchor="middle" letter-spacing="-3">HEY, I'M HUY</text>

  <text x="640" y="374" width="900"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="76" font-weight="900" fill="#F2F2F0" stroke="#1A1A1A"
        stroke-width="2.4" text-anchor="middle" letter-spacing="-3">HEY, I'M HUY</text>

  <text x="640" y="456" width="900"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="76" font-weight="900" fill="#1A1A1A"
        text-anchor="middle" letter-spacing="-3">HEY, I'M HUY</text>

  <!-- small scroll indicator without rotation -->
  <text x="1108" y="590" width="90"
        font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="11" font-weight="700" fill="#1A1A1A">scroll</text>
  <line x1="1150" y1="586" x2="1180" y2="586" stroke="#1A1A1A" stroke-width="1.4"
        marker-end="url(#arrowTip)"/>
</svg>
```

## Avoid in this skill
- ❌ Do not use `<clipPath>`, `<mask>`, or image crops to fake the hollow typography; use editable SVG text with `fill` plus `stroke`.
- ❌ Do not rotate the scroll label or background geometry; complex transforms are not safe for clean PowerPoint translation.
- ❌ Do not use `<path>` or `<polygon>` for the abstract background. Use translucent rectangles/ellipses instead.
- ❌ Do not apply filters to the hero text; filtered text may rasterize and stop being editable.
- ❌ Do not make the background geometry high contrast. It should sit behind the typography, not compete with it.

## Composition notes
- Keep the repeated hero text centered and oversized, occupying roughly the middle 45–55% of slide height.
- Use very tight vertical rhythm: the outlined echo should feel like a continuation of the solid text, not a separate subtitle.
- Put microcopy in the extreme top corners to create a rigid web-navigation frame around the aggressive center.
- Limit the palette to paper beige, black, and muted warm greys; the drama comes from scale and contrast, not color variety.