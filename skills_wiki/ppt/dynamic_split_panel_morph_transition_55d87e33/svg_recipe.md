# SVG Recipe — Dynamic Split-Panel Morph Transition

## Visual mechanism
A full-bleed cinematic image is overlaid by three tall, dark vertical panels that become the new slide structure. In PowerPoint, create two matching slides with the same panel objects: on the first slide the panels sit staggered below the canvas; on the second they fill the screen, so Morph produces a cascading split-panel reveal.

## SVG primitives needed
- 1× `<image>` for the persistent full-bleed hero photo background
- 1× `<rect>` for the semi-transparent navy image wash
- 3× `<rect>` for morphing vertical split panels, each with a subtly different dark gradient
- 3× `<line>` for fine panel divider highlights
- 3× icon systems built from `<circle>`, `<line>`, and `<path>` for premium editable pillar symbols
- 9× `<text>` blocks for panel labels, headings, and body copy; every text element includes explicit `width`
- 1× `<linearGradient>` for the background overlay
- 3× `<linearGradient>` fills for the three panels
- 1× `<filter id="panelShadow">` applied to panel rectangles
- 1× `<filter id="softGlow">` applied to accent icon paths and title text

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="imageWash" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#08101f" stop-opacity="0.78"/>
      <stop offset="55%" stop-color="#111a2b" stop-opacity="0.62"/>
      <stop offset="100%" stop-color="#020612" stop-opacity="0.84"/>
    </linearGradient>

    <linearGradient id="panelOne" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#50647e"/>
      <stop offset="100%" stop-color="#334157"/>
    </linearGradient>
    <linearGradient id="panelTwo" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#41546f"/>
      <stop offset="100%" stop-color="#29384f"/>
    </linearGradient>
    <linearGradient id="panelThree" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#31445f"/>
      <stop offset="100%" stop-color="#1d2c42"/>
    </linearGradient>

    <filter id="panelShadow" x="-15%" y="-5%" width="130%" height="115%">
      <feOffset dx="0" dy="16"/>
      <feGaussianBlur stdDeviation="18"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="softGlow" x="-60%" y="-60%" width="220%" height="220%">
      <feGaussianBlur stdDeviation="4"/>
    </filter>
  </defs>

  <image id="morph-bg-photo" href="https://images.unsplash.com/photo-1497366216548-37526070297c?q=80&amp;w=1600&amp;auto=format&amp;fit=crop" x="0" y="0" width="1280" height="720" preserveAspectRatio="xMidYMid slice"/>
  <rect id="morph-bg-wash" x="0" y="0" width="1280" height="720" fill="url(#imageWash)"/>

  <text id="hero-kicker" x="80" y="84" width="420" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" letter-spacing="3" fill="#78d7ff">STRATEGIC OPERATING MODEL</text>
  <text id="hero-title" x="80" y="144" width="620" font-family="Segoe UI, Microsoft YaHei" font-size="54" font-weight="800" fill="#ffffff" filter="url(#softGlow)">Three pillars, one motion.</text>
  <text id="hero-subtitle" x="82" y="190" width="560" font-family="Segoe UI, Microsoft YaHei" font-size="18" fill="#cbd6e6">Use Morph to turn a cinematic opener into a structured executive agenda without breaking visual continuity.</text>

  <rect id="morph-panel-1" x="0" y="0" width="426.7" height="720" fill="url(#panelOne)" filter="url(#panelShadow)"/>
  <rect id="morph-panel-2" x="426.7" y="0" width="426.6" height="720" fill="url(#panelTwo)" filter="url(#panelShadow)"/>
  <rect id="morph-panel-3" x="853.3" y="0" width="426.7" height="720" fill="url(#panelThree)" filter="url(#panelShadow)"/>

  <line id="divider-1" x1="426.7" y1="0" x2="426.7" y2="720" stroke="#ffffff" stroke-opacity="0.13" stroke-width="1"/>
  <line id="divider-2" x1="853.3" y1="0" x2="853.3" y2="720" stroke="#ffffff" stroke-opacity="0.13" stroke-width="1"/>
  <line id="top-glint" x1="0" y1="1" x2="1280" y2="1" stroke="#9fe7ff" stroke-opacity="0.25" stroke-width="2"/>

  <circle id="icon-ring-1" cx="213" cy="154" r="42" fill="none" stroke="#78d7ff" stroke-width="2" stroke-opacity="0.82"/>
  <path id="icon-compass-1" d="M213 124 L228 162 L213 184 L198 162 Z" fill="none" stroke="#ffffff" stroke-width="3" stroke-linejoin="round"/>
  <circle id="icon-dot-1" cx="213" cy="162" r="4" fill="#78d7ff"/>
  <text id="panel-num-1" x="72" y="248" width="110" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" letter-spacing="3" fill="#78d7ff">01 / SENSE</text>
  <text id="panel-head-1" x="72" y="304" width="280" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="800" fill="#ffffff">Market Signals</text>
  <text id="panel-body-1" x="74" y="354" width="278" font-family="Segoe UI, Microsoft YaHei" font-size="17" fill="#d6deea">Map weak signals, customer shifts, and competitor moves into a shared strategic radar.</text>

  <circle id="icon-ring-2" cx="640" cy="154" r="42" fill="none" stroke="#78d7ff" stroke-width="2" stroke-opacity="0.82"/>
  <path id="icon-bolt-2" d="M650 116 L617 160 L638 160 L628 193 L665 145 L643 145 Z" fill="#78d7ff" fill-opacity="0.95"/>
  <path id="icon-bolt-glow-2" d="M650 116 L617 160 L638 160 L628 193 L665 145 L643 145 Z" fill="none" stroke="#ffffff" stroke-width="2" stroke-opacity="0.7" filter="url(#softGlow)"/>
  <text id="panel-num-2" x="499" y="248" width="120" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" letter-spacing="3" fill="#78d7ff">02 / BUILD</text>
  <text id="panel-head-2" x="499" y="304" width="282" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="800" fill="#ffffff">Rapid Engines</text>
  <text id="panel-body-2" x="501" y="354" width="276" font-family="Segoe UI, Microsoft YaHei" font-size="17" fill="#d6deea">Convert opportunity areas into funded experiments, repeatable playbooks, and launch-ready teams.</text>

  <circle id="icon-ring-3" cx="1067" cy="154" r="42" fill="none" stroke="#78d7ff" stroke-width="2" stroke-opacity="0.82"/>
  <line id="chart-axis-x" x1="1038" y1="178" x2="1096" y2="178" stroke="#ffffff" stroke-width="3" stroke-linecap="round"/>
  <line id="chart-axis-y" x1="1038" y1="178" x2="1038" y2="125" stroke="#ffffff" stroke-width="3" stroke-linecap="round"/>
  <path id="chart-line-3" d="M1045 166 C1055 158 1061 160 1069 146 C1078 130 1087 137 1094 122" fill="none" stroke="#78d7ff" stroke-width="4" stroke-linecap="round"/>
  <text id="panel-num-3" x="926" y="248" width="120" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" letter-spacing="3" fill="#78d7ff">03 / SCALE</text>
  <text id="panel-head-3" x="926" y="304" width="282" font-family="Segoe UI, Microsoft YaHei" font-size="34" font-weight="800" fill="#ffffff">Enterprise Lift</text>
  <text id="panel-body-3" x="928" y="354" width="276" font-family="Segoe UI, Microsoft YaHei" font-size="17" fill="#d6deea">Scale the proven motions across operating units with governance, metrics, and executive cadence.</text>

  <line id="footer-rule-1" x1="72" y1="610" x2="350" y2="610" stroke="#ffffff" stroke-opacity="0.18" stroke-width="1"/>
  <line id="footer-rule-2" x1="499" y1="610" x2="777" y2="610" stroke="#ffffff" stroke-opacity="0.18" stroke-width="1"/>
  <line id="footer-rule-3" x1="926" y1="610" x2="1204" y2="610" stroke="#ffffff" stroke-opacity="0.18" stroke-width="1"/>
  <text id="footer-1" x="72" y="644" width="250" font-family="Segoe UI, Microsoft YaHei" font-size="13" letter-spacing="2" fill="#aebbd0">RADAR → PRIORITIES</text>
  <text id="footer-2" x="499" y="644" width="250" font-family="Segoe UI, Microsoft YaHei" font-size="13" letter-spacing="2" fill="#aebbd0">SPRINTS → PROOF</text>
  <text id="footer-3" x="926" y="644" width="250" font-family="Segoe UI, Microsoft YaHei" font-size="13" letter-spacing="2" fill="#aebbd0">ADOPTION → GROWTH</text>
</svg>
```

## Avoid in this skill
- ❌ Do not try to encode the motion with SVG `<animate>` or `<animateTransform>`; PowerPoint Morph must create the movement.
- ❌ Do not use `<mask>` to reveal the panels; use actual panel rectangles whose `y` positions differ between the two Morph slides.
- ❌ Do not put all three panels into one grouped image or screenshot; each panel must remain an editable rectangle so Morph can track it.
- ❌ Do not rely on `marker-end` for animated arrows during the transition; if arrows are needed, use native `<line>` elements and simple path arrowheads.
- ❌ Do not apply filters to `<line>` dividers; shadows/glows should be on panels, paths, circles, or text only.

## Composition notes
- Build this as a two-slide pair: Slide 1 uses the same background and panel rectangles, but set panel `y` values below the canvas, for example `y="760"`, `y="880"`, and `y="810"`; Slide 2 uses `y="0"` as shown.
- Keep the element IDs and creation order identical across both slides for the moving panels; add the panel content only on Slide 2 so Morph dissolves it in as the columns arrive.
- The background photo should remain fixed across the transition; the audience perceives continuity while the split panels reorganize the content space.
- Use a strict thirds grid: each panel occupies roughly 426.7 px width, with generous internal margins of 70–75 px for executive-style breathing room.