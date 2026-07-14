# SVG Recipe — Minimalist Swimlane Roadmap

## Visual mechanism
A clean swimlane roadmap uses a pale, rigid time grid with muted horizontal task bars to turn a complex plan into an executive-readable schedule. The technique depends on mathematical alignment, low-contrast lane backgrounds, thin gridlines, and compact white labels inside flat color blocks.

## SVG primitives needed
- 3× `<rect>` for full-width pale swimlane backgrounds
- 14× `<rect>` for roadmap task bars with muted category colors
- 15× `<line>` for monthly vertical gridlines
- 5× `<line>` for quarter boundary ticks above the grid
- 5× `<text>` for quarter labels
- 15× `<text>` for month labels
- 3× rotated `<text>` for swimlane labels
- 14× `<text>` with nested `<tspan>` for task labels inside bars
- 8× `<rect>` for right-side note headers and small status tags
- 8× `<text>` for right-side explanatory notes
- 2× `<path>` plus 2× `<rect>` for the stylized PowerPoint-like source badge
- 1× `<filter id="softShadow">` applied only to logo/card shapes, not lines

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feOffset dx="2" dy="4"/>
      <feGaussianBlur stdDeviation="3"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#ffffff"/>

  <!-- Stylized deck/source badge -->
  <rect x="73" y="27" width="104" height="120" rx="3" fill="#ffffff" stroke="#d72f18" stroke-width="5" filter="url(#softShadow)"/>
  <path d="M88 61 A32 32 0 1 1 88 62 L120 62 L120 30 A32 32 0 0 0 88 61 Z" fill="#e2361b"/>
  <rect x="103" y="84" width="50" height="7" fill="#e2361b"/>
  <rect x="103" y="105" width="50" height="7" fill="#e2361b"/>
  <rect x="103" y="126" width="50" height="7" fill="#e2361b"/>
  <path d="M13 25 L111 9 L111 168 L13 152 Z" fill="#e2361b" filter="url(#softShadow)"/>
  <text x="38" y="116" width="62" font-family="Segoe UI, Microsoft YaHei" font-size="72" font-weight="700" fill="#ffffff">P</text>

  <!-- Quarter labels -->
  <text x="215" y="130" width="135" font-family="Segoe UI, Microsoft YaHei" font-size="24" fill="#111111">Q1<tspan font-size="16" dx="8">2018</tspan></text>
  <text x="380" y="130" width="135" font-family="Segoe UI, Microsoft YaHei" font-size="24" fill="#111111">Q2<tspan font-size="16" dx="8">2018</tspan></text>
  <text x="545" y="130" width="135" font-family="Segoe UI, Microsoft YaHei" font-size="24" fill="#111111">Q3<tspan font-size="16" dx="8">2018</tspan></text>
  <text x="710" y="130" width="135" font-family="Segoe UI, Microsoft YaHei" font-size="24" fill="#111111">Q4<tspan font-size="16" dx="8">2018</tspan></text>
  <text x="875" y="130" width="135" font-family="Segoe UI, Microsoft YaHei" font-size="24" fill="#111111">Q1<tspan font-size="16" dx="8">2019</tspan></text>

  <!-- Quarter tick marks -->
  <line x1="210" y1="129" x2="210" y2="166" stroke="#cfd3d6" stroke-width="1"/>
  <line x1="375" y1="129" x2="375" y2="166" stroke="#cfd3d6" stroke-width="1"/>
  <line x1="540" y1="129" x2="540" y2="166" stroke="#cfd3d6" stroke-width="1"/>
  <line x1="705" y1="129" x2="705" y2="166" stroke="#cfd3d6" stroke-width="1"/>
  <line x1="870" y1="129" x2="870" y2="166" stroke="#cfd3d6" stroke-width="1"/>

  <!-- Month labels -->
  <text x="216" y="155" width="42" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#4b4b4b">Jan</text>
  <text x="272" y="155" width="42" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#4b4b4b">Feb</text>
  <text x="327" y="155" width="42" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#4b4b4b">Mar</text>
  <text x="382" y="155" width="42" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#4b4b4b">Apr</text>
  <text x="438" y="155" width="42" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#4b4b4b">May</text>
  <text x="493" y="155" width="42" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#4b4b4b">Jun</text>
  <text x="548" y="155" width="42" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#4b4b4b">Jul</text>
  <text x="603" y="155" width="42" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#4b4b4b">Aug</text>
  <text x="658" y="155" width="42" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#4b4b4b">Sep</text>
  <text x="713" y="155" width="42" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#4b4b4b">Oct</text>
  <text x="768" y="155" width="42" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#4b4b4b">Nov</text>
  <text x="823" y="155" width="42" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#4b4b4b">Dec</text>
  <text x="878" y="155" width="42" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#4b4b4b">Jan</text>
  <text x="933" y="155" width="42" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#4b4b4b">Feb</text>
  <text x="988" y="155" width="42" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#4b4b4b">Mar</text>

  <!-- Swimlane backgrounds -->
  <rect x="165" y="166" width="880" height="155" fill="#f7f7f7"/>
  <rect x="165" y="328" width="880" height="155" fill="#f7f7f7"/>
  <rect x="165" y="490" width="880" height="162" fill="#f7f7f7"/>

  <!-- Vertical monthly gridlines -->
  <line x1="210" y1="166" x2="210" y2="652" stroke="#e4e6e8" stroke-width="1"/>
  <line x1="265" y1="166" x2="265" y2="652" stroke="#eeeeef" stroke-width="1"/>
  <line x1="320" y1="166" x2="320" y2="652" stroke="#eeeeef" stroke-width="1"/>
  <line x1="375" y1="166" x2="375" y2="652" stroke="#e4e6e8" stroke-width="1"/>
  <line x1="430" y1="166" x2="430" y2="652" stroke="#eeeeef" stroke-width="1"/>
  <line x1="485" y1="166" x2="485" y2="652" stroke="#eeeeef" stroke-width="1"/>
  <line x1="540" y1="166" x2="540" y2="652" stroke="#e4e6e8" stroke-width="1"/>
  <line x1="595" y1="166" x2="595" y2="652" stroke="#eeeeef" stroke-width="1"/>
  <line x1="650" y1="166" x2="650" y2="652" stroke="#eeeeef" stroke-width="1"/>
  <line x1="705" y1="166" x2="705" y2="652" stroke="#e4e6e8" stroke-width="1"/>
  <line x1="760" y1="166" x2="760" y2="652" stroke="#eeeeef" stroke-width="1"/>
  <line x1="815" y1="166" x2="815" y2="652" stroke="#eeeeef" stroke-width="1"/>
  <line x1="870" y1="166" x2="870" y2="652" stroke="#e4e6e8" stroke-width="1"/>
  <line x1="925" y1="166" x2="925" y2="652" stroke="#eeeeef" stroke-width="1"/>
  <line x1="980" y1="166" x2="980" y2="652" stroke="#eeeeef" stroke-width="1"/>

  <!-- Rotated swimlane labels -->
  <text x="193" y="255" width="95" transform="rotate(-90 193 255)" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="700" fill="#9a9a9a">Marketing</text>
  <text x="193" y="462" width="120" transform="rotate(-90 193 462)" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="700" fill="#9a9a9a">Development</text>
  <text x="193" y="604" width="50" transform="rotate(-90 193 604)" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="700" fill="#9a9a9a">KPI</text>

  <!-- Marketing bars -->
  <rect x="212" y="202" width="48" height="34" fill="#a9dfe3"/>
  <rect x="262" y="202" width="110" height="34" fill="#3f7da5"/>
  <rect x="376" y="202" width="213" height="34" fill="#17284a"/>
  <rect x="593" y="202" width="428" height="34" fill="#ed2d45"/>
  <text x="216" y="217" width="42" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#ffffff"><tspan x="216">Press</tspan><tspan x="216" dy="14">Launch</tspan></text>
  <text x="270" y="223" width="92" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#ffffff">Media Campaign</text>
  <text x="384" y="217" width="140" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#ffffff"><tspan x="384">Celebrity</tspan><tspan x="384" dy="15">Partnerships</tspan></text>
  <text x="601" y="217" width="170" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#ffffff"><tspan x="601">Ongoing</tspan><tspan x="601" dy="15">Marketing</tspan></text>

  <!-- Development bars -->
  <rect x="212" y="350" width="225" height="34" fill="#3f7da5"/>
  <rect x="444" y="350" width="143" height="34" fill="#17284a"/>
  <rect x="593" y="350" width="427" height="34" fill="#ed2d45"/>
  <rect x="212" y="393" width="48" height="34" fill="#a9dfe3"/>
  <rect x="262" y="393" width="110" height="34" fill="#3f7da5"/>
  <rect x="376" y="393" width="178" height="34" fill="#17284a"/>
  <rect x="560" y="393" width="337" height="34" fill="#ed2d45"/>
  <rect x="212" y="436" width="48" height="34" fill="#a9dfe3"/>
  <rect x="262" y="436" width="92" height="34" fill="#3f7da5"/>
  <rect x="360" y="436" width="227" height="34" fill="#17284a"/>
  <rect x="593" y="436" width="182" height="34" fill="#ed2d45"/>
  <text x="220" y="364" width="90" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#ffffff"><tspan x="220">Mobile</tspan><tspan x="220" dy="15">Web v1</tspan></text>
  <text x="452" y="364" width="90" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#ffffff"><tspan x="452">Mobile</tspan><tspan x="452" dy="15">Web v2</tspan></text>
  <text x="601" y="364" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#ffffff"><tspan x="601">Ongoing</tspan><tspan x="601" dy="15">Marketing</tspan></text>
  <text x="216" y="408" width="42" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#ffffff"><tspan x="216">Press</tspan><tspan x="216" dy="14">Launch</tspan></text>
  <text x="270" y="414" width="92" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#ffffff">Media Campaign</text>
  <text x="384" y="408" width="135" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#ffffff"><tspan x="384">Celebrity</tspan><tspan x="384" dy="15">Partnerships</tspan></text>
  <text x="568" y="408" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#ffffff"><tspan x="568">Ongoing</tspan><tspan x="568" dy="15">Marketing</tspan></text>

  <!-- KPI bars -->
  <rect x="212" y="518" width="155" height="34" fill="#a9dfe3"/>
  <rect x="376" y="518" width="211" height="34" fill="#17284a"/>
  <rect x="593" y="518" width="427" height="34" fill="#3f7da5"/>
  <text x="216" y="533" width="100" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#ffffff"><tspan x="216">Press</tspan><tspan x="216" dy="15">Launch</tspan></text>
  <text x="384" y="533" width="140" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#ffffff"><tspan x="384">Celebrity</tspan><tspan x="384" dy="15">Partnerships</tspan></text>
  <text x="601" y="533" width="160" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#ffffff"><tspan x="601">Ongoing</tspan><tspan x="601" dy="15">Marketing</tspan></text>

  <!-- Right-side notes -->
  <rect x="1078" y="108" width="117" height="28" fill="#a9dfe3"/>
  <text x="1087" y="128" width="100" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="700" fill="#ffffff">Delivery</text>
  <text x="1083" y="153" width="130" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#111111"><tspan x="1083">Delays expected</tspan><tspan x="1083" dy="17">to version 1</tspan></text>

  <rect x="1078" y="196" width="117" height="28" fill="#3f7da5"/>
  <text x="1087" y="216" width="100" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="700" fill="#ffffff">Budget</text>
  <text x="1083" y="240" width="135" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#111111"><tspan x="1083">Budget will need</tspan><tspan x="1083" dy="17">bolstering Q2 2018</tspan></text>

  <rect x="1078" y="280" width="117" height="28" fill="#17284a"/>
  <text x="1087" y="300" width="100" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="700" fill="#ffffff">Resource</text>
  <text x="1083" y="324" width="130" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#111111"><tspan x="1083">All resource on</tspan><tspan x="1083" dy="17">track</tspan></text>

  <rect x="1078" y="371" width="117" height="28" fill="#ed2d45"/>
  <text x="1087" y="391" width="100" font-family="Segoe UI, Microsoft YaHei" font-size="16" font-weight="700" fill="#ffffff">Marcom</text>
  <text x="1083" y="416" width="135" font-family="Segoe UI, Microsoft YaHei" font-size="15" fill="#111111"><tspan x="1083">Public perception</tspan><tspan x="1083" dy="17">is very healthy</tspan></text>

  <rect x="1084" y="473" width="82" height="15" fill="#a8a6a6"/>
  <text x="1090" y="486" width="90" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#ffffff">/ Risks</text>
  <text x="1084" y="504" width="130" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#111111"><tspan x="1084">Competitor and</tspan><tspan x="1084" dy="16">market</tspan></text>

  <rect x="1084" y="539" width="82" height="15" fill="#a8a6a6"/>
  <text x="1090" y="552" width="90" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#ffffff">/ Issues</text>
  <text x="1084" y="570" width="130" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#111111"><tspan x="1084">Delivery and</tspan><tspan x="1084" dy="16">budget</tspan></text>

  <rect x="1084" y="604" width="94" height="15" fill="#a8a6a6"/>
  <text x="1090" y="617" width="100" font-family="Segoe UI, Microsoft YaHei" font-size="15" font-weight="700" fill="#ffffff">/ On Radar</text>
  <text x="1084" y="635" width="140" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#111111"><tspan x="1084">New opportunities</tspan><tspan x="1084" dy="16">and suppliers</tspan></text>
</svg>
```

## Avoid in this skill
- ❌ Heavy borders around every cell; the roadmap should feel like a quiet editorial grid, not a spreadsheet.
- ❌ Saturated primary colors or random color assignments; use a restrained palette and repeat colors consistently.
- ❌ Eyeballed bar placement; compute task `x` and `width` from the same month unit used by the axis.
- ❌ Shadows, bevels, gradients, or 3D effects on task bars; flat bars are the visual language here.
- ❌ Applying filters to `<line>` gridlines; keep lines plain because line filters are not reliably preserved.

## Composition notes
- Reserve the left 15–17% of the slide for the source badge and rotated lane labels; keep the actual timeline grid aligned from a single shared `timelineStartX`.
- Use pale lane fills and very light monthly dividers so task bars are the dominant visual focus.
- Keep task bars short in height with small vertical gaps; multiple rows can live inside one swimlane without making the grid feel crowded.
- Place risk/status notes in a narrow right column using the same roadmap colors, creating a visual legend without adding chart clutter.