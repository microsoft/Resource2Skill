# SVG Recipe — 3D Out-of-Bounds Profile Card

## Visual mechanism
Layer a transparent cutout portrait over a bold geometric anchor or card band so the subject’s head and shoulders break past the boundary while the base remains visually grounded. The illusion comes from strict back-to-front ordering: background typography → geometric anchor/card → portrait cutout → foreground bio text and device/card details.

## SVG primitives needed
- 5× `<rect>` for background split, laptop/card screen, navy content band, device bezel, and metallic base
- 2× `<ellipse>` for the profile anchor halo and laptop base highlight
- 4× `<path>` for bracket decorations, laptop base contour, and small abstract accent shapes
- 1× `<image>` for a transparent-background executive portrait cutout
- 1× `<linearGradient>` for the metallic laptop base
- 1× `<radialGradient>` for the subtle profile anchor highlight
- 2× `<filter>` with blur/offset for premium card shadows and soft portrait depth
- Multiple `<text>` elements with explicit `width` for oversized intro typography, name, role, labels, and bio copy
- Several `<line>` elements for fine editorial dividers and callout rules

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="metalBase" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#6f7378"/>
      <stop offset="0.18" stop-color="#e5e8eb"/>
      <stop offset="0.5" stop-color="#aeb4ba"/>
      <stop offset="0.82" stop-color="#f4f5f6"/>
      <stop offset="1" stop-color="#666a70"/>
    </linearGradient>
    <radialGradient id="anchorGlow" cx="45%" cy="38%" r="65%">
      <stop offset="0" stop-color="#123d82"/>
      <stop offset="0.7" stop-color="#082b66"/>
      <stop offset="1" stop-color="#061f4c"/>
    </radialGradient>
    <filter id="deepShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="10"/>
      <feGaussianBlur stdDeviation="10"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="softPortraitShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="8"/>
      <feGaussianBlur stdDeviation="6"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#ffffff"/>
  <rect x="0" y="0" width="1280" height="405" fill="#082b66"/>

  <text x="54" y="281" width="260" font-family="Segoe UI, Microsoft YaHei" font-size="36" font-weight="800" fill="#ffffff">BIOGRAPHY</text>
  <text x="306" y="190" width="160" font-family="Microsoft YaHei, Segoe UI" font-size="74" font-weight="900" fill="#ffffff">
    <tspan x="306" dy="0">人物</tspan>
    <tspan x="306" dy="84">介绍</tspan>
  </text>
  <path d="M157 248 L157 211 L301 211" fill="none" stroke="#5b76a8" stroke-width="1.4"/>
  <path d="M465 211 L496 211 L496 333 L157 333 L157 291" fill="none" stroke="#5b76a8" stroke-width="1.4"/>
  <text x="169" y="307" width="330" font-family="Segoe UI, Microsoft YaHei" font-size="12" letter-spacing="0.5" fill="#ffffff">
    DETAILED INTRODUCTION TO THE CHARACTERS,
  </text>
  <text x="169" y="324" width="330" font-family="Segoe UI, Microsoft YaHei" font-size="12" letter-spacing="0.5" fill="#ffffff">
    EMPLOYMENT EXPERIENCE, ETC
  </text>

  <g filter="url(#deepShadow)">
    <rect x="622" y="125" width="532" height="322" rx="20" fill="#020204"/>
    <rect x="637" y="141" width="502" height="291" rx="4" fill="#ffffff"/>
  </g>
  <rect x="637" y="270" width="502" height="119" fill="#082b66"/>
  <rect x="637" y="141" width="502" height="129" fill="#ffffff"/>
  <ellipse cx="884" cy="459" rx="322" ry="17" fill="#000000" opacity="0.16"/>
  <path d="M562 453 C674 470,1044 470,1213 453 L1213 464 C1082 479,692 479,562 464 Z" fill="url(#metalBase)"/>
  <rect x="844" y="448" width="89" height="9" rx="5" fill="#8d9298" opacity="0.7"/>

  <ellipse cx="772" cy="291" rx="112" ry="125" fill="url(#anchorGlow)"/>
  <path d="M672 197 C704 175,765 174,805 202 C780 192,712 192,672 197 Z" fill="#061f4c" opacity="0.55"/>
  <image x="659" y="151" width="208" height="291" preserveAspectRatio="xMidYMid meet"
         href="https://images.example.com/transparent-cutout-executive-in-navy-suit-alpha.png"
         filter="url(#softPortraitShadow)"/>

  <text x="849" y="242" width="160" font-family="Segoe UI, Microsoft YaHei" font-size="24" font-weight="800" fill="#082b66">SANJAY</text>
  <line x1="849" y1="249" x2="929" y2="249" stroke="#082b66" stroke-width="1.5"/>
  <line x1="951" y1="249" x2="976" y2="249" stroke="#9aa5b8" stroke-width="1"/>
  <text x="849" y="256" width="132" font-family="Segoe UI, Microsoft YaHei" font-size="5.5" letter-spacing="3" fill="#6b7280">PROJECT FOUNDER</text>

  <text x="963" y="226" width="126" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="800" fill="#cfd4dc">BIOGRAPHY</text>
  <rect x="1001" y="199" width="116" height="47" fill="none" stroke="#d5d9e2" stroke-width="1"/>
  <text x="1052" y="191" width="54" font-family="Microsoft YaHei, Segoe UI" font-size="28" font-weight="900" fill="#082b66">
    <tspan x="1052" dy="0">人物</tspan>
    <tspan x="1052" dy="31">介绍</tspan>
  </text>
  <text x="999" y="235" width="108" font-family="Segoe UI, Microsoft YaHei" font-size="4.5" fill="#a3a8b3">DETAILED INTRODUCTION TO THE CHARACTERS.</text>
  <text x="999" y="241" width="108" font-family="Segoe UI, Microsoft YaHei" font-size="4.5" fill="#a3a8b3">EMPLOYMENT EXPERIENCE, ETC</text>

  <text x="849" y="295" width="250" font-family="Microsoft YaHei, Segoe UI" font-size="7.2" fill="#ffffff">
    <tspan x="849" dy="0">拥有超过十五年战略、组织、国际市场、创新增长、团队管理经验。</tspan>
    <tspan x="849" dy="15">擅长将复杂业务目标转化为清晰的执行路径，推动跨部门协作。</tspan>
    <tspan x="849" dy="15">长期关注数字化转型、品牌升级与高绩效组织建设。</tspan>
  </text>
  <text x="849" y="352" width="245" font-family="Microsoft YaHei, Segoe UI" font-size="6.8" fill="#ffffff">
    <tspan x="849" dy="0">• 互联网平台、云服务与人工智能中心负责人</tspan>
    <tspan x="849" dy="14">• 分阶段主导多项增长与组织变革项目</tspan>
    <tspan x="849" dy="14">• 人才梯队与跨国运营体系建设专家</tspan>
  </text>
  <text x="1065" y="377" width="72" font-family="Segoe UI, Microsoft YaHei" font-size="17" font-weight="800" fill="#6c7fa7" opacity="0.75">Sanjay</text>

  <path d="M1112 166 C1123 157,1137 164,1140 178 C1128 174,1119 174,1112 166 Z" fill="#082b66"/>
  <circle cx="935" cy="249" r="2.4" fill="#aeb7c8"/>
</svg>
```

## Avoid in this skill
- ❌ Using a normal rectangular portrait crop; the effect requires a transparent cutout subject that can overlap the anchor/card boundary.
- ❌ Clipping the whole portrait to the circle or card; that destroys the “out-of-bounds” illusion.
- ❌ Applying `clip-path` to groups or shapes for containment; PPT-Master only preserves clipping reliably on `<image>`.
- ❌ Putting the portrait behind all shapes; it must sit above the geometric anchor but below selected foreground text if you want interlaced depth.
- ❌ Overcrowding the bio side with dense paragraphs; the profile card should feel editorial and spacious.

## Composition notes
- Keep the portrait/anchor mass on one side and reserve the opposite side for name, role, and short bio copy.
- Let the cutout head rise clearly above the geometric boundary by 15–30% of the anchor height.
- Use a deep brand color for the anchor or content band, then repeat it in the name and dividers for cohesion.
- Add oversized pale or white typography in the background to create a magazine-cover feel without competing with the portrait.