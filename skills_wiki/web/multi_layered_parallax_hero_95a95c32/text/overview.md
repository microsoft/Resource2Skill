# Multi-Layered Parallax Hero

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Multi-Layered Parallax Hero 

* **Core Visual Mechanism**: This pattern creates a deep sense of 3D space by stacking multiple separate visual layers (sky, distant celestial body, background mountains, typography, foreground terrain) and moving them at different fractional speeds in response to the user's vertical scroll (`window.scrollY`). A bottom gradient overlay is used to seamlessly blend the parallax container into the subsequent page content.

* **Why Use This Skill (Rationale)**: True parallax (where elements move at distinct rates rather than just a fixed background) creates an immersive, cinematic introduction to a webpage. It rewards the user's scroll action with immediate visual feedback, establishing a premium, storytelling-driven aesthetic.

* **Overall Applicability**: Ideal for landing page heroes, storytelling experiences, portfolio introductions, and long-form editorial articles where establishing a strong visual mood is critical before presenting standard text content.

* **Value Addition**: Unlike a static hero image, a layered parallax section turns the header into an interactive diorama. It draws the user's eye directly to the typography (which usually moves faster or in contrast to the background) and creates a smooth, highly stylized transition into the page's main content.

* **Browser Compatibility**: Broadly supported. Relies on standard CSS positioning, Z-indexing, and fundamental JavaScript `scroll` event listeners. (Note: While the original tutorial uses `top` and `left` for animation, modern best practices dictate using CSS `transform` for hardware-accelerated rendering, which works in all modern browsers).


### 2. Visual & Technical Breakdown

* **Step A: Core Visual Elements**
  - **Layers**: Multiple full-bleed overlapping elements positioned absolutely.
  - **Color Logic**: A unified monochromatic or duotone scheme (e.g., deep space blues `#0a2a43`) that matches the body background color. This ensures the bottom gradient seamlessly transitions into the remaining page content.
  - **Typographic Hierarchy**: Large, bold, sans-serif typography (e.g., Poppins, Inter) placed in the middle of the Z-index stack so it sits behind the foreground but in front of the background.
  - **Gradient Fades**: `linear-gradient` applied to a pseudo-element (`::before`) fixed to the bottom of the section, fading from transparent to the exact background color of the body.

* **Step B: Layout & Compositional Style**
  - **Hero Container**: `position: relative`, `height: 100vh`, `width: 100%`, and critically `overflow: hidden` to ensure moving elements don't create horizontal scrollbars or bleed out of the hero area.
  - **Flexbox Centering**: `display: flex; justify-content: center; align-items: center;` on the container effortlessly centers the text.
  - **Z-Index Strategy**: 
    1. Background (Sky/Stars)
    2. Distant Objects (Moon)
    3. Midground (Mountains)
    4. Text (`z-index` higher than midground)
    5. Foreground (Road/Terrain - `z-index` highest)
    6. Fade Overlay (Highest `z-index` to cover all layers smoothly)

* **Step C: Interactive Behavior & Animations**
  - **Trigger**: `window.addEventListener('scroll', ...)`
  - **Logic**: Read `window.scrollY`. Multiply this value by a decimal (e.g., `0.5`, `0.15`) to create a parallax coefficient. 
  - **Application**: Apply the calculated value to the element's position. Objects further away move slower (coefficient closer to 0 or moving opposite to scroll), objects closer move faster (coefficient closer to 1).


### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **Layer Stacking** | Absolute Positioning + `z-index` | The only reliable way to stack elements on top of each other while allowing them to move independently. |
| **Parallax Scrolling** | Vanilla JS `scroll` listener | Matches the tutorial's technique, simple to implement, and allows for distinct math logic per layer. |
| **Performance Optimization** | CSS `transform: translate3d()` | **Crucial Upgrade**: The original tutorial animates `top` and `left`, which causes constant expensive layout repaints. Using `transform` delegates the animation to the GPU, guaranteeing a 60fps jank-free experience. |
| **Layer Graphics** | Inline SVG & CSS Shapes | To ensure the component is 100% self-contained without relying on missing external image assets, CSS and inline SVGs are used to recreate the sky, moon, and mountain layers. |

#### 3b. Complete Reproduction Code

```python
def create_component(
    output_dir: str,
    title_text: str = "Moon Light",
    body_text: str = "Scroll down to experience the multi-layered parallax effect. The background, moon, mountains, and text all move at different speeds to create a sense of depth and immersion.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#ffffff",     # CSS hex color for accent
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Layered Parallax Hero visual effect.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors ===
    if color_scheme == "dark":
        bg_color = "#0a2a43"
        sky_color = "#051624"
        text_color = "#ffffff"
        mountain_back_fill = "#14456b"
        mountain_front_fill = "#0a2a43"
        moon_glow = "rgba(255, 255, 255, 0.8)"
    else:
        bg_color = "#e2e8f0"
        sky_color = "#cbd5e1"
        text_color = "#0f172a"
        mountain_back_fill = "#94a3b8"
        mountain_front_fill = "#e2e8f0"
        moon_glow = "rgba(255, 255, 255, 1)"

    # === CSS ===
    css = f"""/* Vanilla JS Layered Parallax Hero */
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');

*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg-color: {bg_color};
    --sky-color: {sky_color};
    --text-color: {text_color};
    --accent: {accent_color};
    --moon-glow: {moon_glow};
}}

body {{
    font-family: 'Poppins', sans-serif;
    background: var(--bg-color);
    color: var(--text-color);
    min-height: 200vh; /* Allow scrolling */
    overflow-x: hidden;
}}

/* Parallax Section Container */
.parallax-section {{
    position: relative;
    width: 100%;
    height: 100vh;
    overflow: hidden;
    display: flex;
    justify-content: center;
    align-items: center;
    background: var(--sky-color);
}}

/* Bottom Fade Overlay to blend smoothly into content */
.parallax-section::before {{
    content: '';
    position: absolute;
    bottom: 0;
    left: 0;
    width: 100%;
    height: 150px;
    background: linear-gradient(to top, var(--bg-color), transparent);
    z-index: 100;
}}

/* Common styling for all image/shape layers */
.parallax-layer {{
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    pointer-events: none;
    will-change: transform;
}}

/* Sky Layer (Starry Background) */
.layer-sky {{
    background-image: 
        radial-gradient(2px 2px at 20px 30px, #eee, rgba(0,0,0,0)),
        radial-gradient(2px 2px at 40px 70px, #fff, rgba(0,0,0,0)),
        radial-gradient(2px 2px at 50px 160px, #ddd, rgba(0,0,0,0)),
        radial-gradient(2px 2px at 90px 40px, #fff, rgba(0,0,0,0)),
        radial-gradient(2px 2px at 130px 80px, #fff, rgba(0,0,0,0)),
        radial-gradient(2px 2px at 160px 120px, #ddd, rgba(0,0,0,0));
    background-repeat: repeat;
    background-size: 200px 200px;
    z-index: 1;
}}

/* Moon Layer */
.layer-moon {{
    z-index: 2;
    display: flex;
    justify-content: flex-end;
    padding: 10% 15% 0 0;
}}
.moon-shape {{
    width: 150px;
    height: 150px;
    background: radial-gradient(circle at 30% 30%, #fff, #f0f0f0);
    border-radius: 50%;
    box-shadow: 0 0 80px 20px var(--moon-glow);
}}

/* Mountain Back Layer */
.layer-mountain-back {{
    z-index: 3;
    display: flex;
    align-items: flex-end;
}}
.layer-mountain-back svg {{
    width: 100vw;
    height: auto;
    min-height: 60vh;
    display: block;
}}

/* Typography Layer */
.parallax-title {{
    position: relative;
    color: var(--text-color);
    font-size: clamp(4rem, 10vw, 10rem);
    font-weight: 700;
    text-align: center;
    text-transform: capitalize;
    z-index: 4;
    text-shadow: 0 4px 20px rgba(0,0,0,0.3);
    will-change: transform;
}}

/* Mountain Front Layer */
.layer-mountain-front {{
    z-index: 5;
    display: flex;
    align-items: flex-end;
}}
.layer-mountain-front svg {{
    width: 100vw;
    height: auto;
    min-height: 40vh;
    display: block;
}}

/* Standard Page Content Setup */
.content-section {{
    position: relative;
    z-index: 10;
    padding: 80px 10%;
    background: var(--bg-color);
    min-height: 100vh;
}}
.content-section h2 {{
    font-size: 2.5rem;
    margin-bottom: 20px;
}}
.content-section p {{
    font-size: 1.2rem;
    line-height: 1.8;
    max-width: 800px;
    opacity: 0.8;
}}
"""

    # === HTML ===
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text}</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>

    <section class="parallax-section">
        
        <!-- Sky / Stars -->
        <div class="parallax-layer layer-sky" id="sky"></div>
        
        <!-- Moon -->
        <div class="parallax-layer layer-moon" id="moon">
            <div class="moon-shape"></div>
        </div>
        
        <!-- Distant Mountains -->
        <div class="parallax-layer layer-mountain-back" id="mountain-back">
            <svg viewBox="0 0 1440 600" preserveAspectRatio="none">
                <path d="M0,600 L0,300 L200,200 L400,450 L700,100 L1000,400 L1250,250 L1440,400 L1440,600 Z" fill="{mountain_back_fill}"></path>
            </svg>
        </div>
        
        <!-- Main Text -->
        <h2 class="parallax-title" id="text">{title_text}</h2>
        
        <!-- Foreground Mountains/Terrain -->
        <div class="parallax-layer layer-mountain-front" id="mountain-front">
            <svg viewBox="0 0 1440 400" preserveAspectRatio="none">
                <path d="M0,400 L0,150 L300,50 L600,200 L900,0 L1200,150 L1440,50 L1440,400 Z" fill="{mountain_front_fill}"></path>
            </svg>
        </div>

    </section>

    <!-- Post-Hero Content to enable scrolling -->
    <section class="content-section">
        <h2>Journey Continues</h2>
        <p>{body_text}</p>
        <br><br>
        <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aliquam nec efficitur turpis. Fusce eget lacus eget tellus ullamcorper vestibulum vel eget lectus. Integer pulvinar dui vitae est varius tristique. Nullam tristique dui in augue luctus tincidunt.</p>
    </section>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Vanilla JS Layered Parallax Hero Animation

document.addEventListener('DOMContentLoaded', () => {{
    // Select layers
    const sky = document.getElementById('sky');
    const moon = document.getElementById('moon');
    const mountainBack = document.getElementById('mountain-back');
    const mountainFront = document.getElementById('mountain-front');
    const text = document.getElementById('text');

    // Scroll event listener
    window.addEventListener('scroll', () => {{
        // Get current scroll position
        let value = window.scrollY;

        // Apply distinct translation factors to each layer.
        // We use translate3d instead of 'top' or 'left' for GPU hardware acceleration
        // and to avoid expensive layout repaints on scroll.

        // Sky moves down slowly
        if (sky) sky.style.transform = `translate3d(0, ${{value * 0.5}}px, 0)`;
        
        // Moon moves left and down
        if (moon) moon.style.transform = `translate3d(${{value * -0.5}}px, ${{value * 0.5}}px, 0)`;
        
        // Back mountains move down slightly (creates depth)
        if (mountainBack) mountainBack.style.transform = `translate3d(0, ${{value * 0.25}}px, 0)`;
        
        // Text moves down faster than mountains, slower than foreground
        if (text) text.style.transform = `translate3d(0, ${{value * 1.2}}px, 0)`;
        
        // Front mountains remain anchored or move slightly to ground them
        // In some effects they are static (`translateY(0)`), here we move them very subtly
        if (mountainFront) mountainFront.style.transform = `translate3d(0, ${{value * 0.05}}px, 0)`;
    }});
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

### 4. Accessibility & Performance Notes

* **Performance Optimization (Reflow vs GPU Compositing)**: The original video tutorial applies calculated scroll values to the `top` and `left` CSS attributes. Animating layout-altering properties like `top` triggers a complete recalculation of the document structure (Reflow) on every single pixel of scroll, causing jitter and high CPU usage. The extracted code intentionally upgrades this to use `transform: translate3d(...)` which offloads the animation math to the GPU, guaranteeing a perfectly smooth 60fps experience.
* **will-change**: We added `will-change: transform;` to the moving layers in CSS. This gives the browser a hint to optimize memory allocation for these layers ahead of time.
* **Accessibility**: Large auto-playing animations attached to the scroll wheel can trigger motion sickness for users with vestibular disorders. In a production environment, wrap the JS scroll event initialization in a check for `window.matchMedia('(prefers-reduced-motion: reduce)').matches`.
* **Scalability**: By utilizing SVG graphics inline rather than static JPEGs/PNGs, this reproduction maintains perfect resolution and zero network dependency regardless of how large the screen gets.