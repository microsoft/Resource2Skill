# Pure CSS Liquid Wave Background

## Analysis

### 1. High-level Design Pattern Extraction

**Skill Name**: Pure CSS Liquid Wave Background

**Core Visual Mechanism**:
This component creates a soothing, liquid-like wave animation at the bottom of the screen using purely CSS. The visual trick is remarkably simple but effective: instead of complex vector paths or `clip-path` math, it uses massive, overlapping circular `div` elements (`border-radius: 50%`) that are 2.5 times wider than the viewport/container. By placing these circles near the bottom of the container and translating them horizontally back and forth, the flat top-arcs of the circles glide across the screen. When multiple semi-transparent circles are layered with different animation delays, their intersecting arcs create a deep, dynamic liquid swelling effect. This is paired with an animated background gradient to give the scene life.

**Why Use This Skill (Rationale)**:
- **Performance**: Relying on CSS `transform: translateX` and `opacity` means the animation is entirely hardware-accelerated by the GPU. It avoids the layout thrashing and high CPU usage associated with canvas-based particle waves or SVG path morphing.
- **Aesthetic**: It provides a calm, premium "ambient" feel that makes a layout feel alive without distracting from the main content.
- **Simplicity**: It achieves a complex organic shape using basic geometric primitives (circles) and linear translation.

**Overall Applicability**:
Ideal for hero sections, landing pages, login screens, or dynamic data dashboard backgrounds where you want to communicate fluidity, ease, and modern aesthetics (commonly seen in SaaS, crypto, or modern web app landing pages).

**Browser Compatibility**:
Excellent. It relies on standard CSS (`border-radius`, `transform`, `keyframes`, `rgba`, and `color-mix()`). `color-mix()` is supported in all modern browsers (Chrome 111+, Safari 16.4+, Firefox 109+).

---

### 2. Visual & Technical Breakdown

* **Step A: Core Visual Elements**
  - **Animated Gradient**: A smoothly transitioning linear gradient that scales to 400% of the container size and shifts its background position.
  - **Wave Shapes**: `div` elements turned into perfect circles via `border-radius: 50%`. They use semi-transparent background colors (e.g., `rgba(255, 255, 255, 0.08)` for dark mode) so that when they overlap, the alpha channels multiply, creating "depth" in the liquid.
  - **Glassmorphism Overlay**: Added a frosted glass card overlay for the text content to sit beautifully above the moving waves, utilizing `backdrop-filter: blur(8px)`.

* **Step B: Layout & Compositional Style**
  - **Relative Container**: The main wrapper hides overflow (`overflow: hidden`) so the massive circular shapes don't cause horizontal scrolling.
  - **Absolute Positioning**: The waves are absolutely positioned at `top: 65%` of the container. Because their size is `250%` of the container width (`aspect-ratio: 1 / 1`), only the top chord of the massive circles is visible, resembling a flat wave.
  - **Z-Index Layering**: Background gradient -> Waves (z-index: 1, 2, 3) -> Content Card (z-index: 10).

* **Step C: Interactive Behavior & Animations**
  - **Wave Oscillation**: The waves animate infinitely using `alternate` so they swing left, then right. They translate from `-15%` to `-45%` of their own width.
  - **Phase Shifting**: By giving the three waves staggered `animation-delay` values (0s, -4s, -8s) on a 12s cycle, they move out of sync, creating the illusion of intersecting liquid ripples.
  - **Micro-interaction**: Added a subtle JavaScript-driven 3D tilt effect on the foreground content card that tracks the mouse, enhancing the modern feel.

---

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **Liquid Wave Shapes** | CSS `border-radius` + `transform` | The tutorial's core trick. Massive circles translating X creates perfect waves with zero JS or SVG overhead. GPU accelerated. |
| **Organic Overlap** | CSS `rgba` transparency | Layering semi-transparent elements natively blends their opacities to create visual depth in the waves. |
| **Dynamic Background** | CSS `@keyframes` on `background-position` | Smoothly shifting a 400% sized gradient creates a breathing color effect without JS. |
| **Adaptive Colors** | CSS `color-mix()` | Dynamically blends the user's chosen `accent_color` with the dark/light base themes for a cohesive palette. |
| **Card Interactivity** | JS Mouse Event Listener | Adds a modern 3D parallax tilt to the text container, separating foreground from the animated background. |

#### 3b. Complete Reproduction Code

```python
def create_component(
    output_dir: str,
    title_text: str = "Fluid Elegance",
    body_text: str = "A highly performant, pure CSS liquid wave background paired with a glassmorphism interface and interactive 3D card tilt.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#8f86e7",     # CSS hex color for accent
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Pure CSS Liquid Wave Background.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors ===
    if color_scheme == "dark":
        bg_base = "#0b0f19"
        bg_alt = "#161b2e"
        text_color = "#ffffff"
        wave_bg = "rgba(255, 255, 255, 0.05)"
        card_bg = "rgba(11, 15, 25, 0.4)"
        card_border = "rgba(255, 255, 255, 0.08)"
    else:
        bg_base = "#f4f7f9"
        bg_alt = "#e2e8f0"
        text_color = "#1a202c"
        wave_bg = "rgba(255, 255, 255, 0.6)"
        card_bg = "rgba(255, 255, 255, 0.4)"
        card_border = "rgba(255, 255, 255, 0.5)"

    # === CSS ===
    css = f"""/* Pure CSS Wave Background — generated component */
:root {{
    --accent: {accent_color};
    --bg-base: {bg_base};
    --bg-alt: {bg_alt};
    --text: {text_color};
    --wave-bg: {wave_bg};
    --card-bg: {card_bg};
    --card-border: {card_border};
    --comp-width: {width_px}px;
    --comp-height: {height_px}px;
}}

*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background-color: #000;
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 2rem;
}}

.container {{
    width: 100%;
    max-width: var(--comp-width);
    height: var(--comp-height);
    position: relative;
    border-radius: 24px;
    overflow: hidden;
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
    
    /* Animated Gradient Background */
    background: linear-gradient(
        120deg, 
        var(--bg-base), 
        color-mix(in srgb, var(--accent) 30%, var(--bg-base)), 
        var(--bg-alt), 
        color-mix(in srgb, var(--accent) 15%, var(--bg-alt))
    );
    background-size: 400% 400%;
    animation: gradientShift 15s ease infinite;
    
    /* Layout for centered content */
    display: flex;
    align-items: center;
    justify-content: center;
    perspective: 1000px;
}}

/* -- The Wave Mechanics -- */
.wave-body {{
    position: absolute;
    width: 100%;
    height: 100%;
    top: 65%; /* Start waves below center */
    left: 0;
    pointer-events: none; /* Let clicks pass through to background if needed */
    z-index: 1;
}}

.wave {{
    position: absolute;
    background-color: var(--wave-bg);
    /* Massive scale relative to container width */
    width: 250%;
    aspect-ratio: 1 / 1; 
    border-radius: 50%;
    animation: waveSlide 12s linear infinite alternate;
}}

/* Stagger the animations to create intersecting ripples */
.wave:nth-child(1) {{
    animation-delay: 0s;
    z-index: 3;
}}
.wave:nth-child(2) {{
    animation-delay: -4s;
    z-index: 2;
}}
.wave:nth-child(3) {{
    animation-delay: -8s;
    z-index: 1;
}}

/* -- Foreground Content -- */
.content-card {{
    position: relative;
    z-index: 10;
    max-width: 600px;
    text-align: center;
    padding: 3.5rem 2.5rem;
    border-radius: 20px;
    
    /* Glassmorphism */
    background: var(--card-bg);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border: 1px solid var(--card-border);
    box-shadow: 0 30px 60px rgba(0, 0, 0, 0.1);
    
    /* 3D Transform Defaults */
    transform-style: preserve-3d;
    transition: transform 0.4s cubic-bezier(0.25, 0.8, 0.25, 1);
}}

.title {{
    font-size: clamp(2rem, 5vw, 3.5rem);
    font-weight: 800;
    letter-spacing: -0.03em;
    margin-bottom: 1rem;
    color: var(--text);
    /* Subtle gradient text matching the accent */
    background: linear-gradient(to bottom right, var(--text) 40%, var(--accent));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    transform: translateZ(30px); /* 3D pop */
}}

.body-text {{
    font-size: 1.125rem;
    line-height: 1.7;
    color: color-mix(in srgb, var(--text) 80%, transparent);
    margin-bottom: 2.5rem;
    transform: translateZ(20px); /* 3D pop */
}}

.cta-button {{
    display: inline-block;
    text-decoration: none;
    padding: 1rem 2.5rem;
    border-radius: 50px;
    background: var(--accent);
    color: { "#ffffff" if color_scheme == "light" else "#000000" };
    font-weight: 600;
    font-size: 1rem;
    transition: all 0.3s ease;
    box-shadow: 0 8px 20px color-mix(in srgb, var(--accent) 40%, transparent);
    transform: translateZ(40px); /* 3D pop */
}}

.cta-button:hover {{
    transform: translateZ(40px) translateY(-3px);
    box-shadow: 0 12px 25px color-mix(in srgb, var(--accent) 60%, transparent);
    filter: brightness(1.1);
}}

/* -- Keyframes -- */
@keyframes gradientShift {{
    0% {{ background-position: 0% 50%; }}
    50% {{ background-position: 100% 50%; }}
    100% {{ background-position: 0% 50%; }}
}}

@keyframes waveSlide {{
    0% {{ transform: translateX(-15%); }}
    100% {{ transform: translateX(-45%); }}
}}

/* Accessibility: Respect reduced motion preferences */
@media (prefers-reduced-motion: reduce) {{
    .container, .wave {{
        animation-play-state: paused;
    }}
    .content-card {{
        transition: none;
        transform: none !important;
    }}
}}
"""

    # === HTML ===
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        
        <!-- Background Waves -->
        <div class="wave-body">
            <div class="wave"></div>
            <div class="wave"></div>
            <div class="wave"></div>
        </div>

        <!-- Foreground Content -->
        <div class="content-card">
            <h1 class="title">{title_text}</h1>
            <p class="body-text">{body_text}</p>
            <a href="#" class="cta-button">Explore Features</a>
        </div>

    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Fluid Elegance — Interactive 3D Card Tilt
document.addEventListener('DOMContentLoaded', () => {{
    const container = document.querySelector('.container');
    const card = document.querySelector('.content-card');

    // Only apply hover effects if the user hasn't requested reduced motion
    const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    if (!prefersReducedMotion) {{
        container.addEventListener('mousemove', (e) => {{
            const rect = container.getBoundingClientRect();
            
            // Calculate mouse position relative to the container
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            
            // Calculate center
            const xCenter = rect.width / 2;
            const yCenter = rect.height / 2;
            
            // Calculate rotation limits (max 8 degrees)
            const rotateX = ((y - yCenter) / yCenter) * -8; 
            const rotateY = ((x - xCenter) / xCenter) * 8;
            
            // Apply transform dynamically without transition for real-time tracking
            card.style.transition = 'none';
            card.style.transform = `rotateX(${{rotateX}}deg) rotateY(${{rotateY}}deg)`;
        }});

        container.addEventListener('mouseleave', () => {{
            // Smoothly snap back to center when mouse leaves
            card.style.transition = 'transform 0.6s cubic-bezier(0.25, 0.8, 0.25, 1)';
            card.style.transform = `rotateX(0deg) rotateY(0deg)`;
        }});
        
        container.addEventListener('mouseenter', () => {{
            // Ensure transition is ready for the first mouse movement jump
            card.style.transition = 'transform 0.1s ease-out';
        }});
    }}
}});
"""

    # === Write files ===
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