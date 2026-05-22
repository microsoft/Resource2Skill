### 1. High-level Design Pattern Extraction

> **Skill Name**: Cinematic High-Conversion Hero Layout

* **Core Visual Mechanism**: A split-composition hero section that balances a high-impact, cinematic visual on one side with dense, conversion-optimized typography on the other. It utilizes a dark, dramatic aesthetic (deep space/dark mode) paired with a high-contrast accent color (like stark red) to draw the eye to primary calls-to-action. The design is layered to create depth, often having a foreground element (the ship) subtly break the grid by overlapping the background or text area.
* **Why Use This Skill (Rationale)**: This layout is engineered for immediate emotional impact and user conversion. The cinematic visual establishes a mood and captures attention, while the left-aligned text ensures the value proposition is the first thing read (in LTR languages). Crucially, it integrates psychological triggers seamlessly into the design: minimizing friction ("Join for free"), providing social proof (avatars + user count), and establishing authority ("As seen on" logos) right above the fold.
* **Overall Applicability**: Ideal for SaaS landing pages, game launches, high-end product showcases, and campaign sites where establishing a strong brand mood and driving immediate sign-ups or purchases is the primary goal.
* **Value Addition**: Transforms a standard "text-next-to-image" layout into a narrative experience. The inclusion of integrated trust elements (social proof, authority logos) directly within the hero section prevents users from needing to scroll to build trust, increasing the likelihood of immediate conversion.
* **Browser Compatibility**: Excellent. Uses standard CSS Flexbox/Grid, CSS variables, and basic transform animations. Fully supported in all modern browsers (Edge, Chrome, Firefox, Safari).

### 2. Visual & Technical Breakdown

* **Step A: Core Visual Elements**
  *   **Color Logic**: Dark, atmospheric background (`#0b0f19` to `#1a1f2e` gradient) creating a "deep space" or premium dark mode feel. High contrast text (`#ffffff` for headings, `#a0aec0` for body/secondary text). A vibrant, aggressive accent color (`#e53e3e` red or similar) reserved almost exclusively for calls to action.
  *   **Typographic Hierarchy**:
      *   Headings: Extremely bold, tightly tracked sans-serif (mimicking Titling Gothic/Impact). Sizes usually `3.5rem` to `5rem`.
      *   Body: Clean, readable sans-serif (like Inter or Roboto) at `1.125rem`.
      *   Microcopy (Social proof, "free" text): Small (`0.875rem`), slightly muted, but legible.
  *   **Textures/Depth**: Use of radial gradients to create lighting effects (a glow behind the main visual) and subtle drop shadows on text and buttons to lift them off the dark background.

* **Step B: Layout & Compositional Style**
  *   **Layout System**: CSS Flexbox for the overarching column structure (Header, Main Content, Footer bar) and CSS Grid for the split main content area.
  *   **Spatial Feel**: Ample padding (`2rem` to `4rem`) around the edges. The left text column usually takes up `45-50%` of the width, leaving the rest for the visual to breathe.
  *   **Trust Bar**: A distinct, lower-opacity row at the bottom of the hero containing brand logos, anchored by "As seen on" or "Trusted by" text.

* **Step C: Interactive Behavior & Animations**
  *   **Entrance**: Elements should fade and slide up sequentially (staggered animation) to build the scene rather than loading statically. (e.g., Header -> Headline -> Body -> CTA -> Trust Bar).
  *   **Hover States**: Buttons scale slightly (`1.05`) with increased shadow glow. Ghost buttons reverse out to solid on hover.
  *   **Implementation**: Pure CSS for hover states. JavaScript used strictly to add a `.loaded` class on mount to trigger the initial CSS keyframe animations.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| Split Layout & Trust Bar | CSS Flexbox & Grid | Provides the most robust, responsive control over the alignment of the distinct hero zones. |
| Cinematic Atmosphere | CSS Radial Gradients | Creates depth and lighting without requiring heavy external image assets, ensuring the component is self-contained. |
| Social Proof Avatars | CSS Overlapping Divs | Simple, lightweight way to create the "stacked avatar" look using negative margins and border-radii. |
| Entrance Animation | CSS Keyframes + JS trigger | Smooth, performant stagger effect using CSS `animation-delay` driven by a simple JS `DOMContentLoaded` event. |
| Brand Logos | CSS Styled Text/Shapes | Simulates the "As seen on" logos without external SVG dependencies for a standalone component. |

#### 3b. Complete Reproduction Code

```python
def create_component(
    output_dir: str,
    title_text: str = "It's your universe, it's time to save it",
    body_text: str = "The Rebel alliance is fighting to get rid of the evil empire. Join the resistance to create a better future for your children.",
    color_scheme: str = "dark", 
    accent_color: str = "#e53e3e", # A cinematic, urgent red
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Cinematic High-Conversion Hero layout.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Force dark theme logic to maintain the "cinematic space" feel from the tutorial,
    # but allow light variables if strictly requested.
    if color_scheme == "light":
        bg_gradient = "linear-gradient(135deg, #f7fafc 0%, #edf2f7 100%)"
        text_primary = "#1a202c"
        text_secondary = "#4a5568"
        border_color = "rgba(0, 0, 0, 0.1)"
        orb_glow = "radial-gradient(circle, rgba(229, 62, 62, 0.1) 0%, transparent 60%)"
    else:
        bg_gradient = "linear-gradient(135deg, #0f121b 0%, #06080c 100%)"
        text_primary = "#ffffff"
        text_secondary = "#a0aec0"
        border_color = "rgba(255, 255, 255, 0.1)"
        orb_glow = "radial-gradient(circle, rgba(229, 62, 62, 0.15) 0%, transparent 60%)"

    css = f"""/* Cinematic High-Conversion Hero Generated Component */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Montserrat:wght@800;900&display=swap');

*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg-grad: {bg_gradient};
    --text-main: {text_primary};
    --text-muted: {text_secondary};
    --accent: {accent_color};
    --border: {border_color};
    --orb-glow: {orb_glow};
    
    --container-width: {width_px}px;
    --container-height: {height_px}px;
}}

body {{
    background-color: #000;
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 100vh;
    font-family: 'Inter', sans-serif;
    color: var(--text-main);
}}

.hero-wrapper {{
    width: var(--container-width);
    height: var(--container-height);
    background: var(--bg-grad);
    position: relative;
    overflow: hidden;
    display: flex;
    flex-direction: column;
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
    border: 1px solid var(--border);
}}

/* -- Lighting Effects -- */
.hero-wrapper::before {{
    content: '';
    position: absolute;
    top: 10%;
    right: 5%;
    width: 600px;
    height: 600px;
    background: var(--orb-glow);
    border-radius: 50%;
    pointer-events: none;
    z-index: 0;
}}

/* -- Header -- */
header {{
    position: relative;
    z-index: 10;
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 2rem 3rem;
}}

.logo {{
    font-family: 'Montserrat', sans-serif;
    font-weight: 900;
    font-size: 1.5rem;
    letter-spacing: -0.5px;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}}

.logo span {{ color: var(--accent); }}

nav {{ display: flex; gap: 2rem; }}
nav a {{
    color: var(--text-muted);
    text-decoration: none;
    font-weight: 500;
    font-size: 0.95rem;
    transition: color 0.2s;
}}
nav a:hover {{ color: var(--text-main); }}

.btn-ghost {{
    background: transparent;
    border: 1px solid var(--border);
    color: var(--text-main);
    padding: 0.5rem 1.25rem;
    border-radius: 4px;
    font-weight: 600;
    font-size: 0.9rem;
    cursor: pointer;
    transition: all 0.2s;
}}
.btn-ghost:hover {{
    border-color: var(--text-main);
    background: rgba(255,255,255,0.05);
}}

/* -- Main Layout -- */
.main-content {{
    position: relative;
    z-index: 10;
    flex: 1;
    display: grid;
    grid-template-columns: 1fr 1fr;
    padding: 0 3rem;
    align-items: center;
}}

/* Left Column: Copy & Conversion */
.copy-area {{
    max-width: 520px;
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
}}

h1 {{
    font-family: 'Montserrat', sans-serif;
    font-weight: 900;
    font-size: 3.5rem;
    line-height: 1.1;
    letter-spacing: -1px;
    text-transform: uppercase;
}}

.lead {{
    font-size: 1.125rem;
    line-height: 1.6;
    color: var(--text-muted);
}}

/* CTA Area */
.cta-group {{
    display: flex;
    align-items: center;
    gap: 1rem;
    margin-top: 0.5rem;
}}

.btn-solid {{
    background: var(--accent);
    color: #fff;
    border: none;
    padding: 1rem 2rem;
    font-family: 'Montserrat', sans-serif;
    font-weight: 800;
    font-size: 1.1rem;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    border-radius: 2px;
    cursor: pointer;
    box-shadow: 0 4px 14px rgba(229, 62, 62, 0.4);
    transition: transform 0.2s, box-shadow 0.2s;
}}
.btn-solid:hover {{
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(229, 62, 62, 0.6);
}}

.free-tag {{
    font-size: 0.85rem;
    font-weight: 600;
    color: var(--accent);
    text-transform: uppercase;
    letter-spacing: 0.5px;
    border: 1px solid var(--accent);
    padding: 0.25rem 0.5rem;
    border-radius: 2px;
}}

/* Social Proof */
.social-proof {{
    display: flex;
    align-items: center;
    gap: 1rem;
    margin-top: 1rem;
    padding-top: 1.5rem;
    border-top: 1px solid var(--border);
}}

.avatars {{ display: flex; }}
.avatar {{
    width: 32px;
    height: 32px;
    border-radius: 50%;
    border: 2px solid #06080c;
    background-size: cover;
    background-position: center;
    margin-left: -10px;
}}
.avatar:first-child {{ margin-left: 0; }}
.av-1 {{ background-image: url('https://i.pravatar.cc/100?img=11'); }}
.av-2 {{ background-image: url('https://i.pravatar.cc/100?img=12'); }}
.av-3 {{ background-image: url('https://i.pravatar.cc/100?img=33'); }}

.proof-text {{
    font-size: 0.875rem;
    color: var(--text-muted);
}}
.proof-text strong {{ color: var(--text-main); font-weight: 600; }}

/* Right Column: Visual */
.visual-area {{
    position: relative;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
}}

/* Abstract representation of the cinematic focal point (ship) */
.cinematic-object {{
    width: 350px;
    height: 350px;
    background: linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0) 100%);
    border-top: 1px solid rgba(255,255,255,0.2);
    border-left: 1px solid rgba(255,255,255,0.1);
    border-radius: 24px;
    transform: perspective(1000px) rotateY(-15deg) rotateX(10deg);
    box-shadow: -20px 20px 40px rgba(0,0,0,0.5);
    backdrop-filter: blur(10px);
    position: relative;
    animation: float 6s ease-in-out infinite;
}}

.cinematic-object::after {{
    content: '';
    position: absolute;
    inset: 20px;
    border: 1px dashed rgba(255,255,255,0.2);
    border-radius: 12px;
}}

@keyframes float {{
    0%, 100% {{ transform: perspective(1000px) rotateY(-15deg) rotateX(10deg) translateY(0); }}
    50% {{ transform: perspective(1000px) rotateY(-15deg) rotateX(10deg) translateY(-20px); }}
}}

/* -- Footer / Trust Bar -- */
.trust-bar {{
    position: relative;
    z-index: 10;
    padding: 1.5rem 3rem;
    display: flex;
    align-items: center;
    gap: 3rem;
    background: rgba(0,0,0,0.2);
    border-top: 1px solid var(--border);
}}

.trust-label {{
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: var(--text-muted);
    font-weight: 600;
}}

.logos {{
    display: flex;
    gap: 2.5rem;
    align-items: center;
    opacity: 0.5;
    filter: grayscale(100%);
    transition: opacity 0.3s;
}}
.hero-wrapper:hover .logos {{ opacity: 0.8; }}

.mock-logo {{
    font-family: 'Montserrat', sans-serif;
    font-weight: 900;
    font-size: 1.25rem;
    letter-spacing: -0.5px;
}}

/* -- Entrance Animations -- */
.animate-element {{
    opacity: 0;
    transform: translateY(20px);
    transition: opacity 0.8s cubic-bezier(0.2, 0.8, 0.2, 1), transform 0.8s cubic-bezier(0.2, 0.8, 0.2, 1);
}}

.hero-wrapper.loaded .animate-element {{
    opacity: 1;
    transform: translateY(0);
}}

.delay-1 {{ transition-delay: 0.1s; }}
.delay-2 {{ transition-delay: 0.2s; }}
.delay-3 {{ transition-delay: 0.3s; }}
.delay-4 {{ transition-delay: 0.4s; }}
.delay-5 {{ transition-delay: 0.5s; }}
"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>High-Conversion Hero</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>

    <div class="hero-wrapper" id="hero">
        
        <header class="animate-element delay-1">
            <div class="logo">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="{accent_color}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/></svg>
                Alliance<span>.</span>
            </div>
            <nav>
                <a href="#">Our Fleet</a>
                <a href="#">Mission</a>
                <a href="#">Donations</a>
            </nav>
            <button class="btn-ghost">Member Login</button>
        </header>

        <main class="main-content">
            <div class="copy-area">
                <h1 class="animate-element delay-2">{title_text}</h1>
                <p class="lead animate-element delay-3">{body_text}</p>
                
                <div class="cta-group animate-element delay-4">
                    <button class="btn-solid">Join The Fight</button>
                    <span class="free-tag">100% Free</span>
                </div>

                <div class="social-proof animate-element delay-5">
                    <div class="avatars">
                        <div class="avatar av-1"></div>
                        <div class="avatar av-2"></div>
                        <div class="avatar av-3"></div>
                    </div>
                    <div class="proof-text">
                        <strong>Obi Wan</strong> and <strong>4,000 others</strong> have already joined
                    </div>
                </div>
            </div>

            <div class="visual-area animate-element delay-3">
                <!-- Abstract Glassmorphic Object representing the focal image -->
                <div class="cinematic-object"></div>
            </div>
        </main>

        <div class="trust-bar animate-element delay-5">
            <span class="trust-label">Intercepted broadcasts on</span>
            <div class="logos">
                <div class="mock-logo">HoloNet</div>
                <div class="mock-logo">CNN Galactic</div>
                <div class="mock-logo">Outer Rim News</div>
            </div>
        </div>

    </div>

    <script src="script.js"></script>
</body>
</html>"""

    js = """// Cinematic High-Conversion Hero - Interaction Logic

document.addEventListener('DOMContentLoaded', () => {
    const heroWrapper = document.getElementById('hero');
    
    // Trigger entrance animation shortly after load to ensure rendering is ready
    requestAnimationFrame(() => {
        setTimeout(() => {
            heroWrapper.classList.add('loaded');
        }, 100);
    });

    // Optional: Subtle parallax effect on mouse move over the hero wrapper
    const visualObject = document.querySelector('.cinematic-object');
    
    heroWrapper.addEventListener('mousemove', (e) => {
        const rect = heroWrapper.getBoundingClientRect();
        const x = e.clientX - rect.left; // x position within the element
        const y = e.clientY - rect.top;  // y position within the element
        
        const centerX = rect.width / 2;
        const centerY = rect.height / 2;
        
        // Calculate offset, dampen the effect with division
        const moveX = (x - centerX) / 40;
        const moveY = (y - centerY) / 40;
        
        // Apply transform. Note: preserves the base rotation from CSS
        visualObject.style.transform = `perspective(1000px) rotateY(-15deg) rotateX(10deg) translate3d(${moveX}px, ${moveY}px, 0)`;
    });

    heroWrapper.addEventListener('mouseleave', () => {
        // Reset transform smoothly
        visualObject.style.transition = 'transform 0.5s ease-out';
        visualObject.style.transform = `perspective(1000px) rotateY(-15deg) rotateX(10deg) translate3d(0, 0, 0)`;
        
        // Remove transition after reset so float animation resumes naturally
        setTimeout(() => {
            visualObject.style.transition = '';
        }, 500);
    });
});
"""

    files = []
    for fname, content in [("index.html", html), ("style.css", css), ("script.js", js)]:
        path = os.path.join(output_dir, fname)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        files.append(path)

    return {
        "html": html,
        "css": css,
        "js": js,
        "files": files,
    }
```

### 4. Accessibility & Performance Notes

*   **Accessibility**: 
    *   Semantic HTML (`<header>`, `<main>`, `<nav>`, `<h1>`) is used to define the document structure.
    *   Contrast ratios in the dark theme between the white text (`#ffffff`) and deep background (`#06080c`) exceed the WCAG AAA requirement (7:1).
    *   The staggering animation uses CSS transforms and opacity, but a `@media (prefers-reduced-motion: reduce)` block should ideally be added in production to disable the `.animate-element` transitions and the `.cinematic-object` floating animation for sensitive users.
*   **Performance**:
    *   The entrance animations rely exclusively on `opacity` and `transform`, which are GPU-accelerated and do not trigger layout repaints, ensuring a smooth 60fps load sequence.
    *   The subtle mouse-move parallax in JavaScript calculates coordinates using standard properties but could be throttled using `requestAnimationFrame` if expanded to move many objects, though for a single abstract object, performance impact is negligible.
    *   No large image dependencies are strictly required (the avatars use a fast placeholder service, and the main visual is rendered via CSS gradients/backdrop-filter), resulting in near-instant load times.