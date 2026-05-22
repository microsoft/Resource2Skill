# Modern SVG Animation Toolkit

## Analysis

# High-level Design Pattern Extraction

> **Skill Name**: Modern SVG Animation Toolkit

* **Core Visual Mechanism**: This pattern leverages native Scalable Vector Graphics (SVG) combined with modern CSS capabilities to create a suite of high-performance, visually engaging animations. The core techniques include:
  1. **Path Line-Drawing**: Using `stroke-dasharray` and `stroke-dashoffset` controlled by CSS keyframes and a dynamic JavaScript length calculation to make an outline draw itself before filling.
  2. **Morphing Shapes**: Utilizing the modern CSS `d: path()` property animation to fluidly transition an SVG path between different blob states.
  3. **Progressive Scroll Reveals**: Hooking SVG transforms into the CSS View-Timeline API (`animation-timeline: view()`) to scale, rotate, and slide elements as they enter the viewport.
  4. **SMIL & CSS Transforms**: Using native SVG `<animate>` tags and CSS keyframes for infinite pulsing and floating background details.

* **Why Use This Skill (Rationale)**: SVGs are mathematically rendered, meaning they are infinitely scalable, incredibly lightweight, and sharp on all retina displays. Animating them directly via CSS or SMIL offloads work to the browser's graphics pipeline, ensuring buttery-smooth 60fps animations without heavy JavaScript libraries like GSAP or Lottie.

* **Overall Applicability**: Perfect for high-conversion SaaS landing pages, immersive hero sections, product feature highlights, and interactive data visualization dashboards.

* **Browser Compatibility**: 
  - *Line-drawing & CSS/SMIL Transforms*: Universally supported across all modern browsers.
  - *Scroll-driven Animations (`animation-timeline`)*: Supported in Chrome 115+ and Edge 115+. Gracefully degrades to static visible elements in Safari/Firefox via `@supports` feature queries.
  - *CSS Path Morphing (`d: path()`)*: Supported in Chrome 115+ and Firefox 128+. Gracefully degrades to a static shape in Safari.

---

# Visual & Technical Breakdown

* **Step A: Core Visual Elements**
  - **HTML/SVG**: Semantic structure wrapping inline `<svg>` elements. Paths, circles, and rects are used as the primary building blocks.
  - **Color Logic**: Utilizes a dynamic custom property system. In dark mode, deep slate backgrounds (`#0f172a`) are paired with semi-transparent white surfaces (`rgba(255, 255, 255, 0.05)`). Accents use vivid tech colors (cyan, magenta, amber) to create a neon-glow feel against the dark canvas.
  - **Typography**: Clean, geometric sans-serif ('Inter') with tight letter-spacing for the hero title to match the vector aesthetic.
  - **CSS Properties**: `stroke-dashoffset`, `backdrop-filter: blur()`, `drop-shadow()`, and `transform`.

* **Step B: Layout & Compositional Style**
  - **Hero Layout**: Full viewport height (`100vh`) using CSS Flexbox for absolute centering. The morphing blob and SMIL orbs are absolutely positioned (`z-index: 0`) behind the typography and line-drawing logo (`z-index: 1`).
  - **Component Cards**: Standard CSS Grid layout with frosted-glass aesthetic (backdrop filter + low opacity borders) to contain sub-animations.

* **Step C: Interactive Behavior & Animations**
  - **Drawing Effect**: Starts with `stroke-dashoffset` equal to the total path length (calculated dynamically via JS) and animates to `0`. A delayed `fill` transition completes the solidifying effect.
  - **Pulse Effect**: `r` (radius) and `opacity` are animated on circles with staggered `animation-delay`s (`0s`, `0.2s`, `0.4s`) to create a fluid wave.
  - **Scroll Bindings**: `animation-range: entry 0% cover 50%` ensures the animation maps directly to the user's scroll wheel position as the element crosses the viewport threshold.

---

# Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **Line-Drawing Logo** | CSS Keyframes + minimal JS | CSS handles the GPU-accelerated transition. JS is uniquely required to mathematically calculate `.getTotalLength()` so the dash array precisely matches any path. |
| **Morphing Background Blob** | Pure CSS `d: path()` | Modern, lightweight, and keeps timeline logic inside the CSS stylesheet without JS interpolation. |
| **Scroll Animations** | CSS `animation-timeline` | The new CSS native View-Timeline API provides completely jank-free scroll scrubbing without expensive `window.addEventListener('scroll')` logic. |
| **Pulsing Loader** | Pure CSS Keyframes | Animating the presentation attributes (`r`, `opacity`) via CSS is cleaner than SMIL for coordinated staggered delays. |

#### 3b. Complete Reproduction Code

```python
def create_component(
    output_dir: str,
    title_text: str = "SVG Animation Mastery",
    body_text: str = "High-performance vector animations using native CSS, SMIL, and scroll timelines.",
    color_scheme: str = "dark",        
    accent_color: str = "#0ea5e9",     
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Modern SVG Animation Toolkit.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Derive theme colors
    if color_scheme == "dark":
        bg_color = "#0f172a"
        text_color = "#f8fafc"
        surface_color = "rgba(255, 255, 255, 0.05)"
        surface_border = "rgba(255, 255, 255, 0.1)"
    else:
        bg_color = "#f8fafc"
        text_color = "#0f172a"
        surface_color = "rgba(0, 0, 0, 0.04)"
        surface_border = "rgba(0, 0, 0, 0.1)"

    css = f"""/* Modern SVG Animation Toolkit — Generated Component */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');

*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --text: {text_color};
    --accent: {accent_color};
    --surface: {surface_color};
    --surface-border: {surface_border};
}}

body {{
    font-family: 'Inter', system-ui, sans-serif;
    background: var(--bg);
    color: var(--text);
    min-height: 100vh;
    overflow-x: hidden;
    line-height: 1.6;
}}

/* =========================================
   1. HERO SECTION & MORPHING BLOB
========================================= */
.hero {{
    position: relative;
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    padding: 2rem;
    overflow: hidden;
}}

.morph-bg {{
    position: absolute;
    width: 90vmin;
    height: 90vmin;
    max-width: 800px;
    z-index: 0;
}}

.morph-path {{
    fill: var(--surface);
    /* Morphing fallback for unsupported browsers is just static shape */
    animation: morphBlob 8s ease-in-out infinite alternate;
}}

@keyframes morphBlob {{
    0%   {{ d: path("M50,5 C75,5 95,25 95,50 C95,75 75,95 50,95 C25,95 5,75 5,50 C5,25 25,5 50,5 Z"); }}
    50%  {{ d: path("M50,15 C85,5 95,35 85,50 C75,85 65,95 50,85 C15,95 5,65 15,50 C5,15 35,5 50,15 Z"); }}
    100% {{ d: path("M50,5 C70,15 95,20 95,50 C95,80 70,85 50,95 C30,85 5,80 5,50 C5,20 30,15 50,5 Z"); }}
}}

/* Native SMIL Orbs in background */
.smil-orbs {{
    position: absolute;
    top: 0; left: 0;
    width: 100%; height: 100%;
    z-index: 0;
    pointer-events: none;
}}

/* =========================================
   2. SVG LINE DRAWING EFFECT
========================================= */
.hero-logo {{
    width: 140px;
    height: 140px;
    z-index: 1;
    margin-bottom: 2rem;
    filter: drop-shadow(0 0 20px rgba(14, 165, 233, 0.2));
}}

.draw-path {{
    fill: transparent;
    stroke: var(--accent);
    stroke-width: 2.5px;
    stroke-linejoin: round;
    stroke-linecap: round;
    
    /* Variables dynamically updated via JS for pixel-perfect path length */
    stroke-dasharray: var(--path-length, 1000);
    stroke-dashoffset: var(--path-length, 1000);
    
    animation: drawAndFill 4s cubic-bezier(0.4, 0, 0.2, 1) forwards;
    animation-delay: 0.3s;
}}

@keyframes drawAndFill {{
    0% {{ stroke-dashoffset: var(--path-length, 1000); fill: transparent; }}
    60% {{ fill: transparent; }}
    100% {{ stroke-dashoffset: 0; fill: var(--accent); }}
}}

.title {{
    font-size: clamp(2.5rem, 5vw, 4.5rem);
    font-weight: 800;
    letter-spacing: -0.03em;
    margin-bottom: 1rem;
    z-index: 1;
}}

.subtitle {{
    font-size: 1.25rem;
    opacity: 0.8;
    max-width: 600px;
    z-index: 1;
}}

.scroll-indicator {{
    position: absolute;
    bottom: 2rem;
    z-index: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0.5rem;
    opacity: 0.5;
    font-size: 0.9rem;
    animation: float 2s ease-in-out infinite;
}}

@keyframes float {{
    0%, 100% {{ transform: translateY(0); }}
    50% {{ transform: translateY(-10px); }}
}}

/* =========================================
   3. COMPONENTS LAYOUT & SVG LOADER
========================================= */
.content-wrapper {{
    max-width: 1200px;
    margin: 0 auto;
    padding: 4rem 2rem;
    display: flex;
    flex-direction: column;
    gap: 6rem;
}}

.card {{
    background: var(--surface);
    border: 1px solid var(--surface-border);
    border-radius: 24px;
    padding: 3rem;
    text-align: center;
    box-shadow: 0 25px 50px -12px rgba(0,0,0,0.25);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
}}

.card h2 {{
    margin-bottom: 2rem;
    font-weight: 600;
}}

.loader-svg {{
    width: 120px;
    height: 60px;
    overflow: visible;
}}

.loader-dot {{
    fill: var(--accent);
    animation: dotPulse 1.4s cubic-bezier(0.4, 0, 0.2, 1) infinite;
}}

.loader-dot:nth-child(1) {{ animation-delay: 0s; }}
.loader-dot:nth-child(2) {{ animation-delay: 0.2s; }}
.loader-dot:nth-child(3) {{ animation-delay: 0.4s; }}

@keyframes dotPulse {{
    0%, 100% {{ r: 5px; opacity: 0.2; }}
    50% {{ r: 12px; opacity: 1; filter: drop-shadow(0 0 8px var(--accent)); }}
}}

/* =========================================
   4. SCROLL TIMELINE ANIMATIONS
========================================= */
.scroll-demo-container {{
    min-height: 80vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
}}

.scroll-shapes-svg {{
    width: 100%;
    max-width: 600px;
    height: auto;
    margin-top: 3rem;
    overflow: visible;
}}

/* Default fallback states (Visible if animation-timeline unsupported) */
.scroll-circle, .scroll-rect, .scroll-square {{
    opacity: 1;
    transform: none;
}}

.scroll-circle {{ fill: #ec4899; }} /* Pink */
.scroll-rect {{ fill: #f59e0b; }}   /* Amber */
.scroll-square {{ fill: #8b5cf6; }} /* Purple */

/* Progressive Enhancement: Only apply if browser supports View Timelines */
@supports (animation-timeline: view()) {{
    .scroll-circle {{
        transform-origin: 50px 100px;
        animation: scrollScale linear forwards;
        animation-timeline: view();
        animation-range: entry 0% cover 40%;
    }}
    .scroll-rect {{
        animation: scrollSlide linear forwards;
        animation-timeline: view();
        animation-range: entry 10% cover 50%;
    }}
    .scroll-square {{
        transform-origin: 220px 90px;
        animation: scrollRotate linear forwards;
        animation-timeline: view();
        animation-range: entry 20% cover 60%;
    }}

    @keyframes scrollScale {{
        from {{ transform: scale(0); opacity: 0; }}
        to {{ transform: scale(1.5); opacity: 1; }}
    }}
    @keyframes scrollSlide {{
        from {{ transform: translateX(-100px); opacity: 0; }}
        to {{ transform: translateX(0); opacity: 1; }}
    }}
    @keyframes scrollRotate {{
        from {{ transform: rotate(-180deg) scale(0.5); opacity: 0; }}
        to {{ transform: rotate(0deg) scale(1.2); opacity: 1; }}
    }}
}}
"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text}</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>

    <!-- 1. HERO SECTION -->
    <section class="hero">
        
        <!-- Morphing Blob Background -->
        <svg class="morph-bg" viewBox="0 0 100 100" preserveAspectRatio="xMidYMid meet">
            <path class="morph-path" d="M50,5 C75,5 95,25 95,50 C95,75 75,95 50,95 C25,95 5,75 5,50 C5,25 25,5 50,5 Z"></path>
        </svg>

        <!-- Native SMIL Floating Orbs -->
        <svg class="smil-orbs" viewBox="0 0 100 100" preserveAspectRatio="xMidYMid slice">
            <circle cx="15" cy="80" r="2" fill="var(--accent)">
                <animate attributeName="cy" values="80; 60; 80" dur="5s" repeatCount="indefinite" />
                <animate attributeName="opacity" values="0.1; 0.6; 0.1" dur="5s" repeatCount="indefinite" />
            </circle>
            <circle cx="85" cy="20" r="3" fill="var(--accent)">
                <animate attributeName="cy" values="20; 35; 20" dur="7s" repeatCount="indefinite" />
                <animate attributeName="opacity" values="0.1; 0.8; 0.1" dur="7s" repeatCount="indefinite" />
            </circle>
        </svg>

        <!-- Line Drawing Geometric Logo -->
        <svg class="hero-logo" viewBox="0 0 100 100" preserveAspectRatio="xMidYMid meet">
            <!-- Isometric Cube / Crystal Path -->
            <path class="draw-path" d="M50 5 L95 25 L95 75 L50 95 L5 75 L5 25 Z M50 5 L50 50 M5 25 L50 50 M95 25 L50 50 M5 75 L50 50 M95 75 L50 50 M50 95 L50 50" />
        </svg>

        <h1 class="title">{title_text}</h1>
        <p class="subtitle">{body_text}</p>

        <div class="scroll-indicator">
            <span>Scroll to Explore</span>
            <span>↓</span>
        </div>
    </section>

    <!-- 2. COMPONENTS SHOWCASE -->
    <main class="content-wrapper">
        
        <!-- Animated Pulse Loader -->
        <div class="card">
            <h2>CSS Animated SVG Loader</h2>
            <p style="margin-bottom: 2rem; opacity: 0.8;">Presentation attributes like radius (r) animated natively with CSS keyframes.</p>
            
            <svg class="loader-svg" viewBox="0 0 100 50">
                <circle class="loader-dot" cx="20" cy="25" r="5" />
                <circle class="loader-dot" cx="50" cy="25" r="5" />
                <circle class="loader-dot" cx="80" cy="25" r="5" />
            </svg>
        </div>

        <!-- Scroll-Timeline Reveals -->
        <div class="card scroll-demo-container">
            <h2>Scroll-Driven Shape Reveals</h2>
            <p style="opacity: 0.8;">Powered by the native CSS <code>animation-timeline: view()</code>. Scroll up and down to scrub the timeline.</p>
            
            <svg class="scroll-shapes-svg" viewBox="0 0 300 200">
                <circle class="scroll-circle" cx="50" cy="100" r="30" />
                <rect class="scroll-rect" x="120" y="70" width="40" height="40" rx="8" />
                <rect class="scroll-square" x="200" y="70" width="40" height="40" rx="8" />
            </svg>
        </div>

    </main>

    <script src="script.js"></script>
</body>
</html>"""

    js = f"""// Modern SVG Animation Toolkit - Interaction Logic
document.addEventListener('DOMContentLoaded', () => {{
    
    // 1. DYNAMIC SVG PATH LENGTH CALCULATOR
    // This script calculates the exact mathematical length of any SVG path
    // and feeds it back to CSS as a custom property. This ensures perfect
    // line-drawing animations regardless of how complex the SVG path is.
    
    const drawPaths = document.querySelectorAll('.draw-path');
    
    drawPaths.forEach(path => {{
        // Get the exact pixel length of the vector path
        const length = Math.ceil(path.getTotalLength());
        
        // Pass the length to CSS custom property
        path.style.setProperty('--path-length', length);
        
        // Force a browser reflow to reset the animation state
        // This guarantees the animation uses the newly injected length variable
        path.style.animation = 'none';
        void path.offsetHeight; // Reflow trigger
        path.style.animation = null; 
    }});

}});
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

* **Accessibility**: 
  - To respect user preferences, you should ideally wrap infinite animations (like the morphing blob and loader) in a `@media (prefers-reduced-motion: reduce)` query to pause or display a static state.
  - SVG elements used for purely decorative backgrounds should include `aria-hidden="true"`.
* **Performance**: 
  - **CSS View Timelines**: `animation-timeline: view()` runs natively on the compositor thread. It is significantly more performant than attaching JavaScript `scroll` event listeners.
  - **Dynamic Path Sizing**: The JavaScript logic calculating `.getTotalLength()` runs exactly once on `DOMContentLoaded`. It acts as an initializer, avoiding continuous DOM querying.
  - **Hardware Acceleration**: Transforms (`scale`, `translate`, `rotate`) and `opacity` changes on SVG elements map directly to GPU operations, maintaining high framerates.