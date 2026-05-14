# Agent_Skill_Distiller Report

### 1. High-level Design Pattern Extraction

> **Skill Name**: Split-Layout Portrait Hero

* **Core Visual Mechanism**: This design pattern centers around a layered, depth-driven composition. A large, central subject (typically a portrait without a background) is anchored to the bottom of the viewport. Content is split into two flanking columns using Flexbox and relative positioning, creating a frame around the subject. A subtle repeating pattern acts as the base layer, while vibrant typographic accents pull the user's eye through the text.

* **Why Use This Skill (Rationale)**: By placing a human subject at the absolute center and allowing them to overlap the background but sit behind (or alongside) the text, the design creates a strong focal point and a sense of three-dimensional depth (parallax aesthetic). The asymmetrical text layout (heavy headline on the left, smaller offset quotes on the right) creates dynamic visual tension that feels modern and engaging.

* **Overall Applicability**: Ideal for personal portfolio websites, consultant landing pages, or product pages where a specific persona or mascot needs to be front-and-center.

* **Value Addition**: Compared to a standard split-screen (50/50 image and text) hero, this layered approach feels much more integrated. The text and the image share the same space rather than being boxed into separate containers, resulting in a more premium, magazine-like editorial feel.

* **Browser Compatibility**: Fully supported in all modern browsers. Uses standard CSS Flexbox, custom properties (CSS variables), multiple background images, and `calc()`.


### 2. Visual & Technical Breakdown

* **Step A: Core Visual Elements**
  - **Layering**: The background uses multiple images via the `background-image` property. A repeating texture is the base, and the portrait is layered on top, scaled using `background-size: 70vh` to remain proportionally anchored to the viewport height.
  - **Color Logic**: High contrast is key. The background is a deep, dark hue (e.g., `#1A253A`), text is pure white (`#FFFFFF`), and interactive/structural elements use a vibrant accent color (e.g., magenta `#c13584`).
  - **Typography**: Heavily relies on geometric sans-serif fonts (like Roboto or Inter). The main headline is massive (`~96px`), uppercase, and tightly leaded.
  - **Accents**: The right-hand column uses thick, solid left borders to group related textual elements (quotes or testimonials) together visually.

* **Step B: Layout & Compositional Style**
  - **Flexbox Architecture**: The main container is a `100vh` flex container centering its children. 
  - **Asymmetrical Spacing**: The layout deliberately offsets balance. The left column (`main-intro`) is pulled slightly left and up, while the right column (`main-quotes`) is pushed down significantly (`margin-top: 100px`) and offset to the right. This prevents the text from obscuring the central portrait.
  - **Negative Space**: Large gaps (`column-gap` or relative left/right positioning) carve out an empty center column specifically for the background portrait to occupy.

* **Step C: Interactive Behavior & Animations**
  - While the tutorial sets up a static layout, this composition naturally lends itself to subtle scroll-parallax (where the text moves at a different speed than the background portrait) or entrance animations. We will include a subtle staggered fade-in via CSS.


### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **Layered Subject & Texture** | CSS Multiple `background-image` | Allows stacking a repeating pattern and a responsive portrait (`70vh`) in a single DOM element without extra markup. |
| **Split Flanking Layout** | CSS Flexbox + `gap` | Cleanly aligns the two text columns and creates the central void for the portrait. |
| **Offset Positioning** | `position: relative` & `margin-top` | Recreates the asymmetrical, editorial shift of the text columns from the tutorial without breaking document flow. |
| **Standalone Assets** | SVG Data URIs | Ensures the generated code runs immediately offline without relying on external image hosts that might break. |

#### 3b. Complete Reproduction Code

```python
def create_component(
    output_dir: str,
    title_text: str = "WELCOME TO MY FIRST WEBSITE",
    body_text: str = "Nam interdum felis at felis placerat, sed varius massa ultricies. Integer quis nisi non dolor scelerisque efficitur at sed turpis.",
    color_scheme: str = "dark",
    accent_color: str = "#c13584",
    width_px: int = 1920,
    height_px: int = 1080,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Split-Layout Portrait Hero.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Theme handling
    if color_scheme == "dark":
        bg_color = "#1A253A"
        text_color = "#ffffff"
        pattern_color = "rgba(255, 255, 255, 0.03)"
        silhouette_color = "#0f1626"
    else:
        bg_color = "#e9ecef"
        text_color = "#1A253A"
        pattern_color = "rgba(0, 0, 0, 0.05)"
        silhouette_color = "#ced4da"

    # SVG Data URIs for self-contained visual reproduction
    # 1. Subtle geometric pattern background
    pattern_svg = f"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='40' height='40'%3E%3Cpath d='M20 0 L40 20 L20 40 L0 20 Z' fill='none' stroke='{pattern_color}' stroke-width='1'/%3E%3C/svg%3E"
    
    # 2. Placeholder portrait silhouette
    portrait_svg = f"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 400 600'%3E%3Cpath d='M200 120 C 160 120 130 150 130 190 C 130 230 160 260 200 260 C 240 260 270 230 270 190 C 270 150 240 120 200 120 Z M70 600 L70 500 C 70 400 120 330 200 330 C 280 330 330 400 330 500 L330 600 Z' fill='{silhouette_color}'/%3E%3C/svg%3E"

    css = f"""/* Split-Layout Portrait Hero */
:root {{
    --bg-color: {bg_color};
    --text-color: {text_color};
    --accent-color: {accent_color};
}}

* {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: 'Inter', system-ui, sans-serif;
    background-color: var(--bg-color);
    color: var(--text-color);
    overflow-x: hidden;
}}

.hero-section {{
    position: relative;
    width: 100%;
    min-height: 100vh;
    /* Layer 1: Portrait (top), Layer 2: Pattern (bottom) */
    background-image: url("{portrait_svg}"), url("{pattern_svg}");
    background-position: bottom center, center;
    background-size: 75vh, 40px 40px;
    background-repeat: no-repeat, repeat;
    
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 15vw; /* Creates the central void for the portrait */
    padding: 0 5vw;
}}

/* Typography Defaults */
h1 {{
    font-size: clamp(3rem, 5vw, 6rem);
    line-height: 1.1;
    font-weight: 800;
    text-transform: uppercase;
    margin-bottom: 24px;
}}

p {{
    font-size: 1.125rem;
    line-height: 1.6;
    opacity: 0.9;
}}

/* Left Column */
.main-intro {{
    max-width: 450px;
    position: relative;
    /* Offset to fine-tune framing around portrait */
    bottom: 5vh;
    animation: fadeSlideUp 1s ease-out forwards;
}}

.main-intro p {{
    margin-bottom: 30px;
}}

.btn {{
    display: inline-block;
    background-color: var(--accent-color);
    color: #fff;
    text-decoration: none;
    padding: 12px 24px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1px;
    transition: transform 0.2s ease, opacity 0.2s ease;
}}

.btn:hover {{
    transform: translateY(-2px);
    opacity: 0.9;
}}

/* Right Column */
.main-quotes {{
    max-width: 380px;
    position: relative;
    /* Offset to create asymmetrical balance */
    top: 10vh;
    animation: fadeSlideUp 1s ease-out 0.2s forwards;
    opacity: 0;
}}

.main-quotes p {{
    font-size: 1rem;
    border-left: 4px solid var(--accent-color);
    padding-left: 20px;
    margin-bottom: 40px;
    font-style: italic;
}}

/* Entrance Animation */
@keyframes fadeSlideUp {{
    0% {{
        opacity: 0;
        transform: translateY(30px);
    }}
    100% {{
        opacity: 1;
        transform: translateY(0);
    }}
}}

/* Responsive Breakpoints */
@media (max-width: 1024px) {{
    .hero-section {{
        flex-direction: column;
        gap: 5vh;
        background-position: bottom right -10vw, center;
        background-size: 60vh, 40px 40px;
    }}
    
    .main-intro, .main-quotes {{
        top: 0;
        bottom: 0;
        max-width: 600px;
        background: rgba(0,0,0,0.4);
        padding: 2rem;
        backdrop-filter: blur(10px);
        border-radius: 12px;
    }}
}}
"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Split-Layout Hero</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:ital,wght@0,400;0,600;0,800;1,400&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <main class="hero-section">
        <!-- Left Flank -->
        <section class="main-intro">
            <h1>{title_text}</h1>
            <p>{body_text}</p>
            <a href="#" class="btn">My Work</a>
        </section>

        <!-- Right Flank -->
        <section class="main-quotes">
            <p>"The more that you read, the more things you will know. The more that you learn, the more places you'll go."<br><br>— Dr. Seuss</p>
            <p>"For the best return on your money, pour your purse into your head."<br><br>— Benjamin Franklin</p>
        </section>
    </main>
    <script src="script.js"></script>
</body>
</html>"""

    js = """// Optional: Add subtle parallax effect to the background on mousemove
document.addEventListener('DOMContentLoaded', () => {
    const hero = document.querySelector('.hero-section');
    
    hero.addEventListener('mousemove', (e) => {
        const x = (e.clientX / window.innerWidth - 0.5) * 20;
        const y = (e.clientY / window.innerHeight - 0.5) * 20;
        
        // Shift background slightly opposite to mouse movement
        // First bg is portrait (moves more), second is pattern (moves less)
        hero.style.backgroundPosition = `calc(50% - ${x}px) calc(100% - ${y}px), calc(50% - ${x/3}px) calc(50% - ${y/3}px)`;
    });

    // Reset on leave
    hero.addEventListener('mouseleave', () => {
        hero.style.backgroundPosition = 'bottom center, center';
        hero.style.transition = 'background-position 0.5s ease-out';
    });
    
    hero.addEventListener('mouseenter', () => {
        hero.style.transition = 'none';
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

* **Accessibility**: 
  - The generated background images are decorative (applied via CSS) and do not interrupt screen readers. 
  - The contrast ratio of pure white text (`#ffffff`) against the dark background (`#1A253A`) easily exceeds the WCAG AA 4.5:1 requirement. 
  - The button utilizes semantic anchor tags (`<a>`) making it accessible via keyboard (`Tab`).
* **Performance**: 
  - We use layered background images directly on the container. This is highly performant as it prevents the need for absolutely positioned empty div elements acting as background layers.
  - The `background-size` relies on `vh` which avoids expensive recalculations compared to JavaScript-based resizing logic.
  - A mouse-move listener is added for subtle parallax; it calculates simple offsets and relies on CSS string updates. For production environments with heavier DOMs, wrapping the `hero.style.backgroundPosition` update in a `requestAnimationFrame` would ensure optimal 60fps rendering without jank.