# Web Design-System Primer

Foundational reference for building polished web pages programmatically. Use these tokens, scales, and technique helpers to keep custom code visually coherent with the skills you compose.

## Color Tokens — Dark Scheme (default for SaaS / cyberpunk / neon / dev portfolios)

```css
:root {
  /* Backgrounds */
  --bg-primary:    #0a0f1a;   /* page body                */
  --bg-surface:    #121c2a;   /* cards, panels             */
  --bg-elevated:   #1a2840;   /* hover states, modals      */
  --border-subtle: #263a58;   /* card borders, dividers    */

  /* Accent palette */
  --accent:        #00c8ff;   /* primary CTA, links        */
  --accent-alt:    #7864ff;   /* secondary highlights       */
  --success:       #32d282;   /* positive indicators        */
  --warning:       #ffb941;   /* caution indicators         */
  --danger:        #ff4d6a;   /* error states               */

  /* Text hierarchy */
  --text-primary:  #f0f5ff;   /* headings, body            */
  --text-muted:    #8ca2bc;   /* captions, timestamps      */
  --text-disabled: #4a5e78;   /* placeholders              */

  /* Gradients */
  --gradient-brand: linear-gradient(135deg, #00c8ff 0%, #7864ff 100%);
  --gradient-glow:  linear-gradient(180deg, rgba(0,200,255,0.15) 0%, transparent 60%);
}
```

## Color Tokens — Light Scheme (when brief calls for it: editorial, bright SaaS, e-comm)

```css
:root {
  --bg-primary:    #f8f9fc;
  --bg-surface:    #ffffff;
  --bg-elevated:   #eef1f6;
  --border-subtle: #d8dde6;
  --accent:        #0066ff;
  --accent-alt:    #6b4eff;
  --text-primary:  #1a1e2e;
  --text-muted:    #6b7a90;
}
```

## Color Tokens — Warm/Editorial (cream, terracotta, cinematic)

```css
:root {
  --bg-primary:    #faf7f2;
  --bg-surface:    #ffffff;
  --accent:        #c2410c;   /* terracotta */
  --accent-alt:    #e08e45;
  --text-primary:  #2d1a0f;
  --text-muted:    #6f5a4a;
}
```

## Typography Hierarchy

```css
body { font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; }

h1 { font-size: clamp(2.5rem, 5vw, 4rem);  font-weight: 800; line-height: 1.05; letter-spacing: -0.02em; }
h2 { font-size: clamp(1.75rem, 3vw, 2.5rem); font-weight: 700; line-height: 1.2; }
h3 { font-size: 1.5rem;  font-weight: 600; line-height: 1.3; }
p  { font-size: 1rem;    font-weight: 400; line-height: 1.6; }
.caption { font-size: 0.875rem; color: var(--text-muted); }

/* Display heading variant — pair with gradient-text */
.display { font-size: clamp(3rem, 7vw, 5.5rem); font-weight: 800; letter-spacing: -0.03em; line-height: 0.95; }
```

## Spacing Conventions

```css
:root {
  --space-xs:  0.25rem;  /* 4px  */
  --space-sm:  0.5rem;   /* 8px  */
  --space-md:  1rem;     /* 16px */
  --space-lg:  2rem;     /* 32px */
  --space-xl:  4rem;     /* 64px */
  --space-2xl: 8rem;     /* 128px */
}
```

Section padding: `var(--space-2xl) var(--space-lg)`. Card padding: `var(--space-lg)`. Card gap: `var(--space-lg)`. Container max width: 1200px centered with `margin: 0 auto`.

## CSS Technique Helpers

### Flexbox primitives
```css
.flex-center  { display: flex; align-items: center; justify-content: center; }
.flex-between { display: flex; align-items: center; justify-content: space-between; }
.flex-col     { display: flex; flex-direction: column; gap: var(--space-md); }
```

### Responsive grid
```css
.grid-auto {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: var(--space-lg);
}
.grid-3 {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: var(--space-lg);
}
@media (max-width: 768px) { .grid-3 { grid-template-columns: 1fr; } }
```

### Gradient text
```css
.gradient-text {
  background: var(--gradient-brand);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}
```

### Glassmorphism
```css
.glass {
  background: rgba(18, 28, 42, 0.6);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 16px;
}
```

### Smooth hover lift
```css
.hover-lift { transition: transform 0.3s ease, box-shadow 0.3s ease; }
.hover-lift:hover { transform: translateY(-6px); box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3); }
```

### Fade-in on scroll (Intersection Observer)
```js
const observer = new IntersectionObserver((entries) => {
  entries.forEach(e => { if (e.isIntersecting) { e.target.classList.add('visible'); observer.unobserve(e.target); } });
}, { threshold: 0.15 });
document.querySelectorAll('.fade-in').forEach(el => observer.observe(el));
```
```css
.fade-in { opacity: 0; transform: translateY(30px); transition: opacity .6s ease, transform .6s ease; }
.fade-in.visible { opacity: 1; transform: translateY(0); }
```

### Keyframe library
```css
@keyframes float { 0%,100% { transform: translateY(0); } 50% { transform: translateY(-10px); } }
.floating { animation: float 3s ease-in-out infinite; }

@keyframes pulse-glow {
  0%,100% { box-shadow: 0 0 20px rgba(0,200,255,.2); }
  50%     { box-shadow: 0 0 40px rgba(0,200,255,.5); }
}
.glow { animation: pulse-glow 2s ease-in-out infinite; }

@keyframes gradient-shift {
  0%   { background-position: 0% 50%; }
  50%  { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}
.animated-gradient {
  background: linear-gradient(-45deg, #0a0f1a, #1a2840, #0066ff, #7864ff);
  background-size: 400% 400%;
  animation: gradient-shift 15s ease infinite;
}
```

## Composability — How sections fit together

A polished page is assembled from composable section skills layered with custom code:

```
┌──────────────────────────┐
│   navigation             │  sticky nav with logo + links + CTA
├──────────────────────────┤
│   hero                   │  full-width, headline + sub + CTA + visual
├──────────────────────────┤
│   features               │  3-4 card grid
├──────────────────────────┤
│   social proof / stats   │  testimonials, logos, counters
├──────────────────────────┤
│   secondary CTA / form   │  newsletter, signup, demo request
├──────────────────────────┤
│   footer                 │  links, credits
└──────────────────────────┘
```

When composing multiple skills, unify:
- **Colors**: override each skill's palette with the design system tokens
- **Spacing**: enforce consistent section padding, card gaps
- **Typography**: same font stack and size scale throughout
- **Border-radius**: pick one (e.g., 12px cards, 8px buttons) and stick
- **Shadow style**: subtle 4px or dramatic 20px — don't mix
- **Motion**: hover lifts on every card, or none — be consistent

## Composition Patterns That Score Well

- **Layered visual system: strong typography + controlled palette + spacing discipline + modern surface styling** (gradients, glow, glass cards). Premium feel even when animation is modest.
- **Clear structural composition beyond a single hero**: two-column layouts, form/card pairings, hero-plus-supporting cards. Signals broader UI capability.
- **Cohesive thematic styling** carried through multiple components: dark SaaS palette + glowing accents + consistent cards + matching buttons/nav.
- **Distinct identity treatment** when content is limited: neon, synthwave, premium-product art direction boosts perceived quality if hierarchy stays clean.
- **Contemporary UI motifs** applied consistently: pill buttons, rounded modules, glassmorphism, soft gradients.

## Recommended Skill Combos by Page Type

| Page type | Skills to compose | Min count |
|---|---|---|
| Auth (login/signup) | form_design + two_column_layout + gradient_theming + glassmorphism + typography_hierarchy + cta_buttons | 5 |
| SaaS landing | hero_composition + card_layout + navigation + dark_theme_system + glow_or_gradient + section_density + footer_structure | 6 |
| Developer portfolio | brand_identity + hero_layout + project_cards + code_ui_motifs + responsive_spacing + micro_interactions | 5 |
| Product showcase | product_hero + image_framing + feature_cards + cta_design + warm_dark_palette + motion_states | 5 |
| Gallery / interactive art | immersive_background + content_grid + navigation + interactive_canvas + typography_scale + mobile_readability | 6 |

## Visual DNA Inheritance Rule

When you use an anchor skill and then write custom sections, every custom section must:
- Use the SAME color palette (extract accent + bg + surface tokens from the skill)
- Use the SAME shape language (rounded-16px cards or sharp edges — pick one)
- Use the SAME shadow style (subtle 4px or heavy 20px, not both)
- Use the SAME font stack and weight scale

This creates visual continuity — every section feels like it belongs to the same page.

## Responsive Design Required

Every page must be responsive:
```css
/* Mobile first */
/* Tablet */   @media (min-width: 768px)  { ... }
/* Desktop */  @media (min-width: 1024px) { ... }
/* Wide */     @media (min-width: 1440px) { ... }
```

At minimum: nav collapses to hamburger on mobile, grid sections reflow to single column, font sizes scale via `clamp()` or media queries, horizontal padding reduces on small screens.

## Skill Selection — Intent-Driven

Don't browse skills randomly. Match skills to what each section NEEDS:

- Building a **login/signup**? → search `form_ui` for input styles, modals, validation
- Building an **animated hero**? → search `animation` for typewriter, blob, parallax, scroll-reveal
- Building a **data dashboard**? → search `card_layout` for bento grid, stat cards, comparisons
- Building a **canvas/particle background**? → search `canvas_webgl` for WebGL, particles, shaders
- Building a **product showcase**? → `animation` for floating effects + `card_layout` for feature grids
- Building an **image gallery**? → search `card_layout` for masonry, flip-card, hover effects
- Building a **text-heavy blog**? → search `typography` for text effects, reading layouts

**Cross-category composition is encouraged.** A great page might use an `animation` skill for the hero (typewriter), a `card_layout` skill for features (bento grid), a `navigation` skill for the nav (glassmorphism pill), and custom code for the footer (inheriting hero palette).
