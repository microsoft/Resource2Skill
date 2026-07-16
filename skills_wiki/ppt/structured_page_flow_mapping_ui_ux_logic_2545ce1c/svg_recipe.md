# SVG Recipe — Structured Page Flow Mapping (UI/UX Logic Diagrams)

## Visual mechanism
Represent UX states as structured “page cards” with dark headers and standardized body sections, then place high-contrast action pills and decision diamonds directly on the connective pathways. The rigid grid, arrow routing, and semantic color coding separate states, triggers, and logic so the user journey reads like a clean product blueprint.

## SVG primitives needed
- 1× `<rect>` full-slide background for a neutral canvas
- 3× translucent `<rect>` swimlane bands for journey phases
- 5× `<rect>` page card bodies with soft shadows, borders, and pale fills
- 5× `<path>` rounded-top header shapes for page card titles
- 5× `<text>` header labels with page number and title
- 5× `<text>` body blocks using nested `<tspan>` rows for key contents/functions
- 4× `<rect>` action pills in coral/red for user triggers
- 2× `<path>` decision diamonds in amber for system logic checks
- Multiple `<line>` connectors with `marker-end` applied directly to each arrow line
- 1× `<filter id="cardShadow">` applied to cards, pills, and diamonds
- 1× `<linearGradient>` for page card fill and 1× `<linearGradient>` for the title accent
- Optional dashed `<line>` grid guides for alignment scaffolding

## SVG snippet
```svg
<svg viewBox="0 0 1280 720" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <defs>
    <linearGradient id="pageFill" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#F8FBFF"/>
      <stop offset="100%" stop-color="#EAF0F6"/>
    </linearGradient>
    <linearGradient id="titleAccent" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#2C3E50"/>
      <stop offset="100%" stop-color="#34495E"/>
    </linearGradient>
    <filter id="cardShadow" x="-20%" y="-20%" width="140%" height="150%">
      <feOffset dx="0" dy="7" result="off"/>
      <feGaussianBlur in="off" stdDeviation="8" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <marker id="arrow" markerWidth="12" markerHeight="12" refX="10" refY="6" orient="auto" markerUnits="strokeWidth">
      <path d="M2,2 L10,6 L2,10 Z" fill="#7F8C8D"/>
    </marker>
  </defs>

  <rect x="0" y="0" width="1280" height="720" fill="#FAFAFA"/>
  <rect x="54" y="102" width="356" height="566" rx="24" fill="#ECF3FA" opacity="0.62"/>
  <rect x="462" y="102" width="356" height="566" rx="24" fill="#F7F1E6" opacity="0.48"/>
  <rect x="870" y="102" width="356" height="566" rx="24" fill="#EAF6F0" opacity="0.56"/>

  <line x1="60" y1="372" x2="1220" y2="372" stroke="#D7DEE6" stroke-width="1.2" stroke-dasharray="8 8"/>
  <line x1="436" y1="118" x2="436" y2="660" stroke="#D7DEE6" stroke-width="1.2" stroke-dasharray="8 8"/>
  <line x1="844" y1="118" x2="844" y2="660" stroke="#D7DEE6" stroke-width="1.2" stroke-dasharray="8 8"/>

  <text x="60" y="54" width="760" font-family="Segoe UI, Microsoft YaHei" font-size="30" font-weight="700" fill="#2C3E50">User Authentication Page Flow</text>
  <text x="60" y="84" width="860" font-family="Segoe UI, Microsoft YaHei" font-size="14" fill="#697A89">States are page cards; red pills are user actions; amber diamonds are logic gates.</text>

  <text x="158" y="132" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#6B7B8C" text-anchor="middle">ENTRY</text>
  <text x="640" y="132" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#9A6A11" text-anchor="middle">AUTH LOGIC</text>
  <text x="1048" y="132" width="150" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#46755E" text-anchor="middle">DESTINATIONS</text>

  <rect x="80" y="170" width="276" height="166" rx="14" fill="url(#pageFill)" stroke="#2C3E50" stroke-width="1.5" filter="url(#cardShadow)"/>
  <path d="M94 170 H342 Q356 170 356 184 V214 H80 V184 Q80 170 94 170 Z" fill="url(#titleAccent)"/>
  <text x="218" y="198" width="250" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#FFFFFF" text-anchor="middle">P01 | Landing</text>
  <text x="104" y="238" width="232" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#34495E">
    <tspan x="104" dy="0" font-weight="700">Key Contents / Functions:</tspan>
    <tspan x="104" dy="22">• Hero value proposition</tspan>
    <tspan x="104" dy="20">• Login and sign-up CTAs</tspan>
    <tspan x="104" dy="20">• Feature trust badges</tspan>
  </text>

  <rect x="80" y="450" width="276" height="166" rx="14" fill="url(#pageFill)" stroke="#2C3E50" stroke-width="1.5" filter="url(#cardShadow)"/>
  <path d="M94 450 H342 Q356 450 356 464 V494 H80 V464 Q80 450 94 450 Z" fill="url(#titleAccent)"/>
  <text x="218" y="478" width="250" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#FFFFFF" text-anchor="middle">P02 | Sign Up</text>
  <text x="104" y="518" width="232" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#34495E">
    <tspan x="104" dy="0" font-weight="700">Key Contents / Functions:</tspan>
    <tspan x="104" dy="22">• Email / password form</tspan>
    <tspan x="104" dy="20">• Terms consent checkbox</tspan>
    <tspan x="104" dy="20">• Account creation handler</tspan>
  </text>

  <rect x="502" y="170" width="276" height="166" rx="14" fill="url(#pageFill)" stroke="#2C3E50" stroke-width="1.5" filter="url(#cardShadow)"/>
  <path d="M516 170 H764 Q778 170 778 184 V214 H502 V184 Q502 170 516 170 Z" fill="url(#titleAccent)"/>
  <text x="640" y="198" width="250" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#FFFFFF" text-anchor="middle">P03 | Login</text>
  <text x="526" y="238" width="232" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#34495E">
    <tspan x="526" dy="0" font-weight="700">Key Contents / Functions:</tspan>
    <tspan x="526" dy="22">• Credential input fields</tspan>
    <tspan x="526" dy="20">• Forgot password link</tspan>
    <tspan x="526" dy="20">• Submit authentication</tspan>
  </text>

  <rect x="924" y="170" width="276" height="166" rx="14" fill="url(#pageFill)" stroke="#2C3E50" stroke-width="1.5" filter="url(#cardShadow)"/>
  <path d="M938 170 H1186 Q1200 170 1200 184 V214 H924 V184 Q924 170 938 170 Z" fill="url(#titleAccent)"/>
  <text x="1062" y="198" width="250" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#FFFFFF" text-anchor="middle">P04 | Dashboard</text>
  <text x="948" y="238" width="232" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#34495E">
    <tspan x="948" dy="0" font-weight="700">Key Contents / Functions:</tspan>
    <tspan x="948" dy="22">• Personalized summary</tspan>
    <tspan x="948" dy="20">• Primary navigation</tspan>
    <tspan x="948" dy="20">• Session persistence</tspan>
  </text>

  <rect x="924" y="450" width="276" height="166" rx="14" fill="url(#pageFill)" stroke="#2C3E50" stroke-width="1.5" filter="url(#cardShadow)"/>
  <path d="M938 450 H1186 Q1200 450 1200 464 V494 H924 V464 Q924 450 938 450 Z" fill="url(#titleAccent)"/>
  <text x="1062" y="478" width="250" font-family="Segoe UI, Microsoft YaHei" font-size="14" font-weight="700" fill="#FFFFFF" text-anchor="middle">P05 | Error Recovery</text>
  <text x="948" y="518" width="232" font-family="Segoe UI, Microsoft YaHei" font-size="13" fill="#34495E">
    <tspan x="948" dy="0" font-weight="700">Key Contents / Functions:</tspan>
    <tspan x="948" dy="22">• Inline error message</tspan>
    <tspan x="948" dy="20">• Retry credentials</tspan>
    <tspan x="948" dy="20">• Password reset route</tspan>
  </text>

  <line x1="356" y1="253" x2="455" y2="253" stroke="#7F8C8D" stroke-width="2.2" marker-end="url(#arrow)"/>
  <rect x="378" y="228" width="112" height="50" rx="25" fill="#E74C3C" filter="url(#cardShadow)"/>
  <text x="434" y="258" width="104" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#FFFFFF" text-anchor="middle">Click Login</text>

  <line x1="218" y1="336" x2="218" y2="397" stroke="#7F8C8D" stroke-width="2.2" marker-end="url(#arrow)"/>
  <rect x="153" y="361" width="130" height="50" rx="25" fill="#E74C3C" filter="url(#cardShadow)"/>
  <text x="218" y="391" width="120" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#FFFFFF" text-anchor="middle">Create Account</text>

  <line x1="778" y1="253" x2="870" y2="253" stroke="#7F8C8D" stroke-width="2.2" marker-end="url(#arrow)"/>
  <path d="M870 253 L920 205 L970 253 L920 301 Z" fill="#F39C12" stroke="#B9770E" stroke-width="1.4" filter="url(#cardShadow)"/>
  <text x="920" y="248" width="92" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#FFFFFF" text-anchor="middle">Valid</text>
  <text x="920" y="263" width="92" font-family="Segoe UI, Microsoft YaHei" font-size="12" font-weight="700" fill="#FFFFFF" text-anchor="middle">session?</text>
  <line x1="970" y1="253" x2="924" y2="253" stroke="#7F8C8D" stroke-width="2.2" marker-end="url(#arrow)"/>

  <line x1="920" y1="301" x2="920" y2="386" stroke="#7F8C8D" stroke-width="2.2"/>
  <line x1="920" y1="386" x2="1062" y2="386" stroke="#7F8C8D" stroke-width="2.2"/>
  <line x1="1062" y1="386" x2="1062" y2="450" stroke="#7F8C8D" stroke-width="2.2" marker-end="url(#arrow)"/>
  <rect x="978" y="360" width="112" height="50" rx="25" fill="#E74C3C" filter="url(#cardShadow)"/>
  <text x="1034" y="390" width="104" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#FFFFFF" text-anchor="middle">Show Error</text>

  <line x1="1062" y1="450" x2="1062" y2="407" stroke="#7F8C8D" stroke-width="2.2"/>
  <line x1="1062" y1="407" x2="640" y2="407" stroke="#7F8C8D" stroke-width="2.2"/>
  <line x1="640" y1="407" x2="640" y2="336" stroke="#7F8C8D" stroke-width="2.2" marker-end="url(#arrow)"/>
  <rect x="585" y="382" width="110" height="50" rx="25" fill="#E74C3C" filter="url(#cardShadow)"/>
  <text x="640" y="412" width="102" font-family="Segoe UI, Microsoft YaHei" font-size="13" font-weight="700" fill="#FFFFFF" text-anchor="middle">Retry</text>

  <rect x="914" y="52" width="240" height="42" rx="21" fill="#FFFFFF" stroke="#D8DEE6" stroke-width="1"/>
  <rect x="932" y="66" width="28" height="14" rx="7" fill="#E74C3C"/>
  <text x="970" y="78" width="70" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#566573">Action</text>
  <path d="M1040 73 L1054 59 L1068 73 L1054 87 Z" fill="#F39C12"/>
  <text x="1078" y="78" width="70" font-family="Segoe UI, Microsoft YaHei" font-size="12" fill="#566573">Decision</text>
</svg>
```

## Avoid in this skill
- ❌ Using free-floating boxes without a repeated page-card syntax; the technique depends on consistent state containers.
- ❌ Putting `marker-end` on `<path>` connectors or inherited from a parent `<g>`; apply arrowheads directly to each `<line>`.
- ❌ Over-routing with diagonal spaghetti connectors; prefer orthogonal or short straight lines aligned to card centers.
- ❌ Clipping or masking non-image shapes for card headers; use simple `<rect>` or editable `<path>` header shapes instead.
- ❌ Omitting explicit `width` on text elements; PowerPoint text boxes will not size correctly.

## Composition notes
- Keep page cards on a strict grid: entry states left, logic in the center, destination states right.
- Reserve the open space between cards for action pills and decision diamonds; avoid placing labels inside the page cards unless they describe state content.
- Use dark navy for stable page states, coral for user-triggered actions, amber for conditional logic, and gray for connectors.
- Add faint swimlane bands or dashed guide lines to make the flow feel intentional and executive-ready without overwhelming the diagram.