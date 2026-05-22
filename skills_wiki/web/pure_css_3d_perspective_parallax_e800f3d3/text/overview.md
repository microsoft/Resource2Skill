# Pure CSS 3D Perspective Parallax

## Analysis

# Role: Agent_Skill_Distiller

### 1. High-level Design Pattern Extraction

> **Skill Name**: Pure CSS 3D Perspective Parallax

* **Core Visual Mechanism**: This technique creates a true depth-of-field parallax effect using only native CSS 3D transforms. By applying `perspective` to a scrolling container and pushing child layers backward along the Z-axis (`translateZ`), the browser natively renders the layers moving at different speeds as the user scrolls. Scaling (`scale`) is mathematically applied to compensate for the perspective distortion, maintaining the elements' intended visual sizes.
* **Why Use This Skill (Rationale)**: Traditional JavaScript-based parallax effects bind to the `scroll` event, which often causes jank, stuttering, and high CPU usage because it runs on the main browser thread. This pure CSS method offloads the visual calculations directly to the browser's compositor thread (GPU), resulting in a buttery-smooth, 60FPS scroll experience that feels physically authentic.
* **Overall Applicability**: Ideal for highly immersive hero sections, storytelling landing pages, editorial web articles, and portfolios where depth, layering, and visual storytelling are paramount. 
* **Value Addition**: It adds profound spatial depth to flat layouts. By separating background imagery, typography, and foreground framing elements into distinct 3D planes, it transforms a static webpage into a window-like viewport. 
* **Browser Compatibility**: Excellent across all modern browsers (Chrome, Firefox, Safari, Edge). The `transform-style: preserve-3d` and `perspective` properties are natively supported without prefixes in modern environments. 

### 2. Visual & Technical Breakdown

* **Step A: Core Visual Elements**
  - **Layers**: Relies on a specific HTML hierarchy—a scrolling viewport wrapper (`.container`), a 3D context section (`.parallax-section`), and individual absolute-positioned layers for background, midground (text), and foreground.
  - **Color Logic**: Uses a dark base (`#0d111c`) with white typography (`#ffffff`) for high contrast against the photographic background. A subtle dark overlay (`rgba(0, 0, 0, 0.4)`) is blended over the background image to ensure text legibility.
  - **Typography**: Heavy, bold sans-serif (`font-weight: 800`, `letter-spacing: -0.02em`) for the hero title to anchor the composition visually, with drop shadows (`text-shadow: 0 10px 30px rgba(0,0,0,0.5)`) to enhance separation from the background.
  - **CSS Properties**: The effect is entirely driven by `perspective`, `transform-style: preserve-3d`, `translateZ`, and `scale`.

* **Step B: Layout & Compositional Style**
  - **Layout System**: Absolute positioning is used to stack the `.parallax-layer` elements exactly on top of one another within the `.parallax-section`.
  - **Mathematical Scaling**: When an element is pushed back, it appears smaller. To restore its original size, the formula `scale = (perspective - translateZ) / perspective` is used. With `perspective: 1px` and `translateZ(-1px)`, the required scale is `(1 - (-1)) / 1 = 2`.
  - **Z-Index Layering**: `translateZ` primarily dictates depth, but explicit `z-index` (e.g., `-2`, `-1`, `1`) ensures rendering consistency across different browser engines (especially Safari).

* **Step C: Interactive Behavior & Animations**
  - **Scroll Behavior**: Purely native vertical scrolling. The background layer moves at exactly 50% speed, the text layer at 75% speed, and the foreground layer at 100% speed.
  - **Transitions**: An Intersection Observer (JS) is added to gracefully fade in the standard content once the user scrolls past the parallax hero, adding a layer of entry polish.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **Multi-speed Parallax** | Pure CSS 3D Transforms | Bypasses JS scroll event jank; uses GPU compositing for flawless 60FPS motion. |
| **Depth of Field Blur** | CSS `filter: blur()` | Simulates a camera focus effect on the furthest background layer natively. |
| **Foreground Framing** | Inline SVG shape | Creates a seamless, organic visual bridge between the parallax section and the standard content block below it. |
| **Content Fade-in** | JS `IntersectionObserver` | Provides a performant way to trigger entrance animations without monitoring scroll position on every frame. |

> **Feasibility Assessment**: 100%. The code precisely recreates the pure CSS parallax mechanism demonstrated in the video tutorial, generalized with placeholder assets and SVG framing so it works immediately without external local files.

#### 3b. Complete Reproduction Code

```python
def create_component(
    output_dir: str,
    title_text: str = "DEPTH",
    body_text: str = "Experience true CSS-driven 3D parallax without the performance overhead of JavaScript scroll listeners. This section represents standard content flowing naturally after the immersive hero.",
    color_scheme: str = "dark",
    accent_color: str = "#00bfff",
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Pure CSS 3D Perspective Parallax visual effect.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme ===
    if color_scheme == "dark":
        bg_color = "#0a0a0f"
        text_color = "#f0f0f0"
        card_bg = "#15151e"
    else:
        bg_color = "#f8f9fa"
        text_color = "#1a1a2e"
        card_bg = "#ffffff"

    # Background image (high-res mountain landscape from Unsplash)
    bg_image_url = "https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?q=80&w=2000&auto=format&fit=crop"

    # === CSS ===
    css = f"""/* Pure CSS 3D Parallax Component */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --text: {text_color};
    --accent: {accent_color};
    --card-bg: {card_bg};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background: #000;
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 100vh;
    overflow: hidden; /* Hide outer scrollbar to enforce component scrolling */
}}

/* The critical scroll container */
.container {{
    width: var(--width);
    height: var(--height);
    max-width: 100vw;
    background: var(--bg);
    position: relative;
    
    /* 3D Parallax Magic */
    overflow-x: hidden;
    overflow-y: auto;
    perspective: 1px; /* Defines the 3D space */
    perspective-origin: center center;
    scroll-behavior: smooth;
}}

/* The 3D context block */
.parallax-section {{
    position: relative;
    height: var(--height); /* Matches viewport height */
    transform-style: preserve-3d;
    z-index: -1;
}}

/* Base class for all layers */
.parallax-layer {{
    position: absolute;
    inset: 0; /* top:0, right:0, bottom:0, left:0 */
    display: flex;
    align-items: center;
    justify-content: center;
}}

/* Deepest Layer: Background moves slowest (50% speed) */
/* Formula: scale = (perspective - translateZ) / perspective = (1 - (-1)) / 1 = 2 */
.layer-back {{
    transform: translateZ(-1px) scale(2);
    z-index: -2;
    background: linear-gradient(to bottom, rgba(0,0,0,0.2), rgba(0,0,0,0.6)), url('{bg_image_url}') center/cover no-repeat;
    /* Optional: depth of field blur */
    filter: blur(2px);
}}

/* Middle Layer: Text moves at 75% speed */
/* scale = (1 - (-0.5)) / 1 = 1.5 */
.layer-mid {{
    transform: translateZ(-0.5px) scale(1.5);
    z-index: -1;
}}

.hero-title {{
    font-size: clamp(4rem, 12vw, 10rem);
    font-weight: 800;
    color: #ffffff;
    letter-spacing: -0.04em;
    text-transform: uppercase;
    text-shadow: 0 15px 40px rgba(0, 0, 0, 0.6);
}}

/* Front Layer: Moves at normal scroll speed (100%) */
.layer-front {{
    transform: translateZ(0) scale(1);
    z-index: 1;
    align-items: flex-end; /* Align SVG to the bottom */
}}

.layer-front svg {{
    width: 100%;
    height: auto;
    display: block;
    margin-bottom: -1px; /* Prevents 1px rendering gap */
}}

/* Standard scrolling content below the hero */
.normal-section {{
    position: relative;
    z-index: 2; /* Ensures it scrolls OVER the background layer */
    background: var(--bg);
    color: var(--text);
    min-height: calc(var(--height) * 0.8);
    padding: 6rem 4rem;
    display: flex;
    flex-direction: column;
    align-items: center;
}}

.content-block {{
    max-width: 800px;
    background: var(--card-bg);
    padding: 3rem;
    border-radius: 16px;
    box-shadow: 0 20px 40px rgba(0,0,0,0.1);
    border-top: 4px solid var(--accent);
    
    /* Animation initial state */
    opacity: 0;
    transform: translateY(30px);
    transition: opacity 0.8s ease-out, transform 0.8s ease-out;
}}

.content-block.visible {{
    opacity: 1;
    transform: translateY(0);
}}

.content-block h2 {{
    font-size: 2.5rem;
    margin-bottom: 1.5rem;
    font-weight: 700;
}}

.content-block p {{
    font-size: 1.25rem;
    line-height: 1.7;
    color: var(--text);
    opacity: 0.8;
}}
"""

    # === HTML ===
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Pure CSS Parallax</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>

    <!-- 
      The .container acts as the scrollable viewport. 
      It defines the 'perspective' space. 
    -->
    <div class="container">
        
        <!-- The 3D context wrapper -->
        <section class="parallax-section">
            
            <!-- Layer 1: Background (-1px Z) -->
            <div class="parallax-layer layer-back"></div>
            
            <!-- Layer 2: Midground Text (-0.5px Z) -->
            <div class="parallax-layer layer-mid">
                <h1 class="hero-title">{title_text}</h1>
            </div>
            
            <!-- Layer 3: Foreground shape (0 Z) -->
            <div class="parallax-layer layer-front">
                <!-- SVG Transition shape masking the transition to normal content -->
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1440 250" preserveAspectRatio="none">
                    <path fill="{bg_color}" fill-opacity="1" d="M0,160L48,144C96,128,192,96,288,106.7C384,117,480,171,576,181.3C672,192,768,160,864,133.3C960,107,1056,85,1152,90.7C1248,96,1344,128,1392,144L1440,160L1440,320L1392,320C1344,320,1248,320,1152,320C1056,320,960,320,864,320C768,320,672,320,576,320C480,320,384,320,288,320C192,320,96,320,48,320L0,320Z"></path>
                </svg>
            </div>
            
        </section>

        <!-- Normal scrolling block -->
        <section class="normal-section">
            <div class="content-block">
                <h2>The Illusion of Depth</h2>
                <p>{body_text}</p>
                <br>
                <p>Scroll up and down to observe how the background, text, and SVG wave move independently, creating a convincing optical illusion without a single scroll event listener.</p>
            </div>
        </section>

    </div>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Intersection Observer to trigger fade-in animations
// This is purely for the standard content below the CSS parallax layer.
document.addEventListener('DOMContentLoaded', () => {{
    const observer = new IntersectionObserver((entries) => {{
        entries.forEach(entry => {{
            if (entry.isIntersecting) {{
                entry.target.classList.add('visible');
                // Optional: stop observing once faded in
                observer.unobserve(entry.target);
            }}
        }});
    }}, {{
        // Trigger when 10% of the element is visible
        threshold: 0.1 
    }});

    const contentBlock = document.querySelector('.content-block');
    if (contentBlock) {{
        observer.observe(contentBlock);
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