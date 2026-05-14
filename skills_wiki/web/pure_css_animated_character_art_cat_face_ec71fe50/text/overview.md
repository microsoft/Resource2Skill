# Pure CSS Animated Character Art (Cat Face)

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Pure CSS Animated Character Art (Cat Face)

* **Core Visual Mechanism**: This component demonstrates pure CSS illustration techniques. It uses CSS fundamental properties—`absolute` positioning, `border-radius` (with complex multi-axis values for organic shaping), `radial-gradient` for simulated 3D depth, and CSS `@keyframes`—to draw and animate a fully recognizable character face without any external images, SVGs, or Canvas.
* **Why Use This Skill (Rationale)**: Pure CSS art has an incredibly small payload, scales infinitely without pixelation, and naturally hooks into CSS animation timelines. It forces the developer to think spatially and geometrically, breaking down complex visual elements into base HTML boxes manipulated by CSS.
* **Overall Applicability**: This technique is perfect for playful brand elements, interactive mascots, empty states, 404 error pages, and loading screens where you want to inject personality and delight without heavy graphic assets.
* **Value Addition**: By avoiding external raster/vector assets, the component allows dynamic real-time theming (e.g., changing the background, nose, and eye color automatically using CSS variables) and extremely cheap native DOM animations.
* **Browser Compatibility**: Fully supported in all modern browsers. It relies on established CSS standards (gradients, border-radius, transforms, keyframes) with complete cross-browser compatibility.

### 2. Visual & Technical Breakdown

* **Step A: Core Visual Elements**
  * **Anatomy**: The character is constructed from stacked `<div>` elements: a main `.face-area` wrapper, containing `.ear`, `.eye`, `.pupil`, `.nose`, `.mouth`, and `.whisker` descendants.
  * **Color Logic**:
    * Body Base: Deep charcoal `#2A2F30` fading to darker `#1C2526` via a `radial-gradient` to create a spherical illusion.
    * Eyes: White `#FFFFFF` with an inner grey shadow `#D3D3D3` mimicking eyeball curvature.
    * Contrast/Accent: The background and the cat's nose use the same vivid accent color (e.g., `#FFB800` yellow) to create a negative-space aesthetic.
  * **Shaping**: Multi-axis `border-radius` is heavily utilized. For instance, the face uses `border-radius: 50% 50% 40% 40% / 60% 60% 40% 40%`, which creates a shape that is slightly taller and wider at the top, mimicking animal cheeks and a crown.

* **Step B: Layout & Compositional Style**
  * **Layout System**: The main container centers the art using CSS Flexbox. Inside `.face-area`, everything relies on `position: absolute`.
  * **Symmetry**: `left`, `right`, and `transform: translateX(-50%)` (for center alignment) strictly enforce facial symmetry.
  * **Layering**: Ears are pushed behind using natural DOM order or `z-index`, while eyes, nose, and whiskers sit on top. `overflow: hidden` on the eyes ensures the pupil doesn't bleed out of the sclera during animation.

* **Step C: Interactive Behavior & Animations**
  * **Eye Darting**: The `.pupil` elements move rapidly left and right using `@keyframes move` mapping `translateX(-12px)` to `translateX(12px)`. The `ease-in-out` timing function makes the eye movements feel natural and deliberate.
  * **Head Sway**: The entire `.face-area` undergoes a slow, continuous rotation (`@keyframes tilt`) from `-3deg` to `3deg`, creating an idle breathing/swaying loop that keeps the character feeling alive.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **Character Drawing** | Pure HTML/CSS | Demonstrates the core tutorial skill: utilizing `border-radius` and absolute positioning for vector-free illustration. |
| **Depth and Shading** | CSS `radial-gradient` | Provides an instant 3D sphere illusion without complex shadow stacking. |
| **Animation Loop** | CSS `@keyframes` | Highly performant, running on the compositor thread for smooth continuous idle motion without JS overhead. |
| **Component Scaling** | CSS `transform: scale()` | Allows the fixed-pixel art to responsively fit container bounds without complex CSS variable overrides on every width/height rule. |

#### 3b. Complete Reproduction Code

```python
def create_component(
    output_dir: str,
    title_text: str = "404 - Not Found",
    body_text: str = "Looks like you're lost. Want to head back?",
    color_scheme: str = "dark",
    accent_color: str = "#FFB800",     # Vivid yellow by default
    width_px: int = 800,
    height_px: int = 600,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Pure CSS Animated Cat Face.
    
    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Base theme resolution
    if color_scheme == "dark":
        text_color = "#FFFFFF"
        body_bg = "#121212"
    else:
        text_color = "#1A1A2E"
        body_bg = "#F8F9FA"

    # CSS Generation
    css = f"""/* CSS Cat Face Component */
:root {{
    --accent: {accent_color};
    --bg: {body_bg};
    --text: {text_color};
    
    /* Cat specific colors */
    --cat-fur-light: #2A2F30;
    --cat-fur-dark: #1C2526;
    --cat-eye: #FFFFFF;
    --cat-eye-shadow: #D3D3D3;
    --cat-whisker: rgba(255, 255, 255, 0.5);
    --cat-mouth: #555555;
}}

* {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background-color: var(--bg);
    color: var(--text);
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    overflow: hidden;
}}

.component-container {{
    width: {width_px}px;
    height: {height_px}px;
    max-width: 100%;
    position: relative;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    background: var(--accent);
    border-radius: 24px;
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
    padding: 2rem;
    text-align: center;
    overflow: hidden;
}}

.text-content {{
    margin-top: 2rem;
    z-index: 20;
    /* Ensure text contrasts against the accent background */
    color: #111; 
}}

.text-content h1 {{
    font-size: 2.5rem;
    font-weight: 700;
    margin-bottom: 0.5rem;
}}

.text-content p {{
    font-size: 1.125rem;
    font-weight: 400;
    opacity: 0.9;
}}

/* === CSS Art: Cat Face === */
.art-wrapper {{
    position: relative;
    width: 200px;
    height: 220px;
    /* Scale gracefully based on container height to prevent overflow */
    transform: scale(calc(min(1, {height_px} / 500)));
    z-index: 10;
}}

.face-area {{
    position: absolute;
    width: 100%;
    height: 100%;
    background: radial-gradient(circle at 50% 40%, var(--cat-fur-light) 40%, var(--cat-fur-dark) 100%);
    border-radius: 50% 50% 40% 40% / 60% 60% 40% 40%;
    animation: tilt 4s ease-in-out infinite;
    box-shadow: 0 15px 35px rgba(0,0,0,0.2);
}}

/* Ears */
.ear {{
    position: absolute;
    width: 60px;
    height: 80px;
    background: var(--cat-fur-light);
    border-radius: 50% 50% 0 0;
    top: -30px;
    z-index: -1;
}}

.ear.left {{
    left: 10px;
    transform: rotate(-30deg);
}}

.ear.right {{
    right: 10px;
    transform: rotate(30deg);
}}

/* Eyes */
.eye {{
    position: absolute;
    width: 45px;
    height: 35px;
    background: radial-gradient(circle at 50% 30%, var(--cat-eye) 50%, var(--cat-eye-shadow) 100%);
    border-radius: 50%;
    top: 70px;
    overflow: hidden;
}}

.eye.left {{
    left: 40px;
}}

.eye.right {{
    right: 40px;
}}

.pupil {{
    position: absolute;
    width: 12px;
    height: 25px;
    background: var(--cat-fur-dark);
    border-radius: 50px;
    top: 5px;
    left: 16px;
    animation: move 3s ease-in-out infinite;
}}

/* Nose (using accent color for negative space effect) */
.nose {{
    position: absolute;
    width: 40px;
    height: 20px;
    background: var(--accent);
    border-radius: 50% 50% 30% 30%;
    top: 130px;
    left: 50%;
    transform: translateX(-50%);
}}

/* Mouth */
.mouth {{
    position: absolute;
    width: 30px;
    height: 15px;
    background: var(--cat-mouth);
    border-radius: 0 0 50px 50px;
    top: 160px;
    left: 50%;
    transform: translateX(-50%);
}}

/* Whiskers */
.whisker {{
    position: absolute;
    width: 60px;
    height: 2px;
    background: var(--cat-whisker);
    border-radius: 2px;
}}

.whisker.left {{
    left: -20px;
    transform-origin: right center;
}}

.whisker.right {{
    right: -20px;
    transform-origin: left center;
}}

.w-top.left {{ top: 130px; transform: rotate(10deg); }}
.w-mid.left {{ top: 145px; transform: rotate(0deg); }}
.w-bot.left {{ top: 160px; transform: rotate(-10deg); }}

.w-top.right {{ top: 130px; transform: rotate(-10deg); }}
.w-mid.right {{ top: 145px; transform: rotate(0deg); }}
.w-bot.right {{ top: 160px; transform: rotate(10deg); }}


/* Animations */
@keyframes tilt {{
    0%, 100% {{ transform: rotate(0deg); }}
    25% {{ transform: rotate(3deg); }}
    75% {{ transform: rotate(-3deg); }}
}}

@keyframes move {{
    0%, 100% {{ transform: translateX(0); }}
    15% {{ transform: translateX(-12px); }}
    35% {{ transform: translateX(-12px); }}
    65% {{ transform: translateX(12px); }}
    85% {{ transform: translateX(12px); }}
}}
"""

    # HTML Generation
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="component-container">
        
        <!-- CSS Art Area -->
        <div class="art-wrapper">
            <div class="face-area">
                <div class="ear left"></div>
                <div class="ear right"></div>
                
                <div class="eye left">
                    <div class="pupil"></div>
                </div>
                <div class="eye right">
                    <div class="pupil"></div>
                </div>
                
                <div class="nose"></div>
                <div class="mouth"></div>
                
                <div class="whisker left w-top"></div>
                <div class="whisker left w-mid"></div>
                <div class="whisker left w-bot"></div>
                
                <div class="whisker right w-top"></div>
                <div class="whisker right w-mid"></div>
                <div class="whisker right w-bot"></div>
            </div>
        </div>

        <div class="text-content">
            <h1>{title_text}</h1>
            <p>{body_text}</p>
        </div>
        
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # JS Generation (Minimal since effect is pure CSS)
    js = """// Pure CSS Character Art
// JavaScript is included here for extensibility, 
// such as adding mouse-tracking to override the idle eye animation.

document.addEventListener('DOMContentLoaded', () => {
    console.log("CSS Cat initialized. CSS Keyframes are handling the animation.");
});
"""

    # Write files
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

* **Accessibility**: Pure CSS art elements are invisible to screen readers, which is actually correct for decorative imagery. However, ensure that the `.art-wrapper` or its container has an `aria-hidden="true"` attribute if injected dynamically into a broader UI. Ensure text overlapping the `accent_color` (the yellow background) passes WCAG contrast checks—in the reproduction, the text over the accent color defaults to dark `#111` to ensure legibility.
* **Performance**: This is highly performant. The animations (`tilt`, `move`) only utilize `transform: rotate()` and `transform: translateX()`, which offload seamlessly to the GPU compositor thread without triggering layouts or repaints.
* **Responsiveness**: Because the art uses absolute positioning and fixed pixels internally, wrapping it in a `.art-wrapper` with a `transform: scale(...)` formula is an elegant way to maintain the rigid vector ratios while safely fitting within responsive container boundaries.