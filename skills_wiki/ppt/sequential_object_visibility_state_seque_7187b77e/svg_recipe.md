# SVG Recipe — Sequential Object Visibility & State Sequencing

## Visual mechanism
A dark, stage-like canvas shows a primary “actor” shape between two state endpoints: an object that has appeared on the left and an object that will disappear on the right. The large Pac-Man form, waypoint dots, labels, and endpoint icons create a clear cause-and-effect storyboard for sequential visibility, disappearance, and state changes.

## SVG primitives needed
- 2× `<rect>` for the dark canvas and double-line presentation frame
- 1× `<path>` for the editable Pac-Man actor with a wedge mouth cut out
- 4× `<circle>` for the appear object, disappear object, sequencing dots, and PowerPoint badge
- 10× `<line>` for radiating “visibility state” ticks around the appear/disappear endpoints
- 5× `<text>` for the large state labels and small PowerPoint badge letter
- 4× small `<rect>` / `<path>` elements for the simplified PowerPoint icon inside the badge
- 2× `<radialGradient>` for premium circular fills on the red and orange badge elements
- 1× `<linearGradient>` for the yellow actor highlight
- 1× `<filter id="softShadow">` applied to the main actor, labels, and badge
- 1× `<filter id="stateGlow">` applied to endpoint circles and dots for subtle stage lighting

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="pacYellow" x1="450" y1="120" x2="760" y2="490" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#ffd83a"/>
      <stop offset="0.55" stop-color="#ffc400"/>
      <stop offset="1" stop-color="#f5aa00"/>
    </linearGradient>

    <radialGradient id="redState" cx="42%" cy="35%" r="70%">
      <stop offset="0" stop-color="#e00000"/>
      <stop offset="0.65" stop-color="#c70000"/>
      <stop offset="1" stop-color="#960000"/>
    </radialGradient>

    <radialGradient id="pptBadge" cx="38%" cy="28%" r="75%">
      <stop offset="0" stop-color="#ff744d"/>
      <stop offset="0.65" stop-color="#df4b2d"/>
      <stop offset="1" stop-color="#a83220"/>
    </radialGradient>

    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="5"/>
      <feGaussianBlur stdDeviation="6"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="stateGlow" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="4"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <!-- stage -->
  <rect x="0" y="0" width="1280" height="720" fill="#17142e"/>
  <rect x="16" y="16" width="1248" height="688" fill="none" stroke="#ffffff" stroke-width="2" opacity="0.85"/>
  <rect x="34" y="50" width="1212" height="620" fill="none" stroke="#342c99" stroke-width="9"/>

  <!-- faint sequencing guide -->
  <line x1="230" y1="300" x2="1045" y2="300" stroke="#24204a" stroke-width="3" stroke-dasharray="12 18" opacity="0.45"/>

  <!-- left: appeared state -->
  <circle cx="232" cy="292" r="60" fill="#74b247" filter="url(#stateGlow)"/>
  <line x1="232" y1="196" x2="232" y2="231" stroke="#74b247" stroke-width="7"/>
  <line x1="232" y1="380" x2="233" y2="416" stroke="#74b247" stroke-width="7"/>
  <line x1="142" y1="239" x2="170" y2="262" stroke="#74b247" stroke-width="7"/>
  <line x1="145" y1="374" x2="173" y2="350" stroke="#74b247" stroke-width="7"/>
  <line x1="288" y1="263" x2="313" y2="236" stroke="#74b247" stroke-width="7"/>
  <line x1="287" y1="348" x2="317" y2="373" stroke="#74b247" stroke-width="7"/>

  <!-- consumable sequential dots -->
  <circle cx="386" cy="295" r="26" fill="#ffc400" filter="url(#stateGlow)"/>
  <circle cx="478" cy="294" r="26" fill="#ffc400" filter="url(#stateGlow)"/>

  <!-- primary actor: editable Pac-Man path -->
  <path d="M489 166
           A178 178 0 1 1 476 419
           L609 298
           Z"
        fill="url(#pacYellow)"
        filter="url(#softShadow)"/>

  <!-- right: disappearing target state -->
  <circle cx="1042" cy="300" r="59" fill="url(#redState)" filter="url(#stateGlow)"/>
  <line x1="1042" y1="189" x2="1043" y2="223" stroke="#c40000" stroke-width="7"/>
  <line x1="1047" y1="374" x2="1048" y2="408" stroke="#c40000" stroke-width="7"/>
  <line x1="953" y1="232" x2="980" y2="254" stroke="#c40000" stroke-width="7"/>
  <line x1="1124" y1="229" x2="1097" y2="254" stroke="#c40000" stroke-width="7"/>
  <line x1="955" y1="368" x2="982" y2="344" stroke="#c40000" stroke-width="7"/>
  <line x1="1127" y1="365" x2="1099" y2="342" stroke="#c40000" stroke-width="7"/>

  <!-- labels -->
  <text x="110" y="582" width="360" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="76" font-weight="800" fill="#ffffff" filter="url(#softShadow)">Appear</text>
  <text x="752" y="588" width="430" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="80" font-weight="800" fill="#ffffff" filter="url(#softShadow)">Disappear</text>

  <!-- PowerPoint badge at bottom center -->
  <circle cx="598" cy="622" r="70" fill="url(#pptBadge)" filter="url(#softShadow)"/>
  <rect x="584" y="586" width="57" height="58" rx="4" fill="#ffffff" opacity="0.9"/>
  <rect x="604" y="594" width="31" height="12" fill="#d74a2b"/>
  <rect x="604" y="616" width="30" height="6" fill="#d74a2b"/>
  <rect x="604" y="630" width="29" height="6" fill="#d74a2b"/>
  <path d="M552 591 L606 581 L606 666 L552 657 Z" fill="#ffffff"/>
  <text x="566" y="638" width="34" font-family="Segoe UI, Microsoft YaHei, sans-serif"
        font-size="44" font-weight="800" fill="#c9472b">P</text>
  <path d="M612 598
           A16 16 0 1 1 612 630
           L612 615
           L628 615
           A16 16 0 0 0 612 598 Z"
        fill="#d74a2b" opacity="0.95"/>
</svg>
```

## Avoid in this skill
- ❌ SVG `<animate>` or `<animateTransform>` to model sequencing; create the visual states as editable objects, then add PowerPoint animations natively.
- ❌ `<mask>` to cut the Pac-Man mouth; use one editable `<path>` with the wedge built into the path geometry.
- ❌ `marker-end` arrows for the sequence path; use dots, dashed `<line>`, or explicit triangle paths if direction must be shown.
- ❌ Clip paths on shapes for visibility states; PowerPoint translation only preserves clipping reliably on `<image>`.
- ❌ Overcrowded process diagrams; this technique depends on large negative space so state changes feel deliberate.

## Composition notes
- Keep the actor large and centered, with the appear/disappear endpoints smaller and pushed toward the sides.
- Use a dark stage or sterile white canvas, but keep decorative elements extremely minimal so object visibility changes remain the focus.
- Labels should sit low and outside the motion lane; the viewer’s eye should track left-to-right through dots, actor, and target.
- For a live deck, duplicate the slide into several states: endpoint hidden, endpoint visible, dots removed one-by-one, actor advanced, and final disappearance.