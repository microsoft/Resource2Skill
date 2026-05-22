# Pure CSS Geometric Art Illustration

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Pure CSS Geometric Art Illustration 

* **Core Visual Mechanism**: This pattern relies entirely on the CSS box model, `border-radius` manipulation, and `radial-gradient` backgrounds to create a complex, stylized illustration (in this case, a sleepy turtle) without using any external images or SVGs. It uses absolute positioning within a relative container, stacking pseudo-elements (`::before`/`::after`) and layers via `z-index` to build depth.
* **Why Use This Skill (Rationale)**: Pure CSS art has a distinct, playful vector aesthetic that renders instantly, scales flawlessly to any resolution (via `em` or `%` units), and requires zero network requests. It's an excellent way to demonstrate technical CSS mastery while adding charm to a UI.
* **Overall Applicability**: Perfect for 404 error pages, empty states, loading screens, easter eggs, or playful mascot integrations in modern web apps. 
* **Value Addition**: Transforms standard HTML `<div>` tags into rich, scalable vector graphics, reducing payload size while providing developers absolute programmatic control over the colors and layout (allowing for seamless light/dark mode transitions).
* **Browser Compatibility**: Excellent. Relies on standard CSS2/CSS3 properties (`border-radius`, `box-shadow`, `radial-gradient`, `calc()`) which are supported universally across all modern browsers.

### 2. Visual & Technical Breakdown

* **Step A: Core Visual Elements**
  - **Shapes**: Every body part is a CSS box. The shell is a half-circle (`border-radius: 50% 50% 0 0`), the head is a perfect circle (`50%`), the legs are rounded rectangles (`border-radius: 0 0 0.5em 0.5em`), and the tail is a quarter-circle (`border-radius: 0 0 0 100%`).
  - **Color Logic**: A vibrant, earthy palette. The shell uses warm browns (`#703225` with `#9b4a2a` spots), the skin uses a rich green (`#009f40`), and the toes are an off-white (`#d5cd8e`).
  - **Textures**: The shell spots are achieved cleanly by layering multiple `radial-gradient` rules within a single `background-image` property, eliminating the need for extra DOM nodes.

* **Step B: Layout & Compositional Style**
  - **Layout System**: Absolute positioning relative to a wrapper element (`.turtle`).
  - **Scalability**: By assigning a dynamically calculated `font-size` to the `.turtle` wrapper based on the container dimensions, all internal measurements using `em` units scale up and down perfectly in unison.
  - **Z-Index Layering**: Depth is created by stacking: Shadow (0) < Tail/Legs (1) < Neck (2) < Head (3) < Shell (4) < Collar (5).

* **Step C: Interactive Behavior & Animations**
  - **Subtle Life**: CSS `@keyframes` are used to apply a gentle, continuous "nodding" animation to the head, making the character feel asleep rather than inanimate.
  - **Parallax Sensation**: A vanilla JavaScript `mousemove` listener applies a slight translational transform to the entire turtle, making it feel rooted in a 3D space as the user interacts with the page.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| Vector Shapes | CSS `border-radius` | Native, extremely fast, perfectly smooth edges. |
| Shell Texture | CSS `radial-gradient` | Allows multiple spot layers on a single element without cluttering the DOM. |
| Duplicated Toes | CSS `box-shadow` offset | A single pseudo-element creates the first toe, and a horizontal box-shadow duplicates it exactly to create the second. |
| Responsiveness | `em` units + `calc()` | Setting a root font-size based on container bounds ensures the entire complex illustration scales automatically without media queries. |
| Interactivity | JS `mousemove` | Adds an engaging, low-cost parallax floating effect to the vector graphic. |

#### 3b. Complete Reproduction Code

```python
def create_component(
    output_dir: str,
    title_text: str = "404 - Taking it slow",
    body_text: str = "We couldn't find that page. Our little friend here is looking for it, but it might take a while.",
    color_scheme: str = "light",
    accent_color: str = "#e9a100",
    width_px: int = 1000,
    height_px: int = 700,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Pure CSS Geometric Turtle Art.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Color definitions matching the CSS Art style
    if color_scheme == "dark":
        bg_color = "#12121c"
        text_color = "#f0f0f0"
        surface_color = "rgba(255, 255, 255, 0.05)"
        shell_color = "#5c2a1e"
        spot_color = "#7a3826"
        spot_alt = "#8c4430"
        skin_color = "#007a33"
        toes_color = "#b0aa76"
    else:
        bg_color = "#f2bd2f" # Signature warm yellow background
        text_color = "#333333"
        surface_color = "rgba(255, 255, 255, 0.3)"
        shell_color = "#703225"
        spot_color = "#833825"
        spot_alt = "#9b4a2a"
        skin_color = "#009f40"
        toes_color = "#d5cd8e"

    css = f"""/* Pure CSS Geometric Art — Turtle Component */
:root {{
    --bg: {bg_color};
    --text: {text_color};
    --surface: {surface_color};
    --accent: {accent_color};
    
    /* Turtle Palette */
    --shell: {shell_color};
    --spot: {spot_color};
    --spot-alt: {spot_alt};
    --skin: {skin_color};
    --toes: {toes_color};
    --eye: #2c2c2c;
    
    --width: {width_px}px;
    --height: {height_px}px;
}}

* {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: 'Inter', system-ui, sans-serif;
    background: var(--bg);
    color: var(--text);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
}}

.page-wrapper {{
    width: var(--width);
    height: var(--height);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    background: var(--surface);
    border-radius: 24px;
    box-shadow: 0 20px 40px rgba(0,0,0,0.1);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.1);
    padding: 40px;
    position: relative;
}}

.text-container {{
    text-align: center;
    z-index: 10;
    margin-bottom: 2rem;
}}

.title {{
    font-size: 2.5rem;
    font-weight: 700;
    margin-bottom: 0.5rem;
    letter-spacing: -0.02em;
}}

.body-text {{
    font-size: 1.1rem;
    opacity: 0.8;
    max-width: 500px;
    line-height: 1.6;
    margin: 0 auto;
}}

/* =========================================
   PURE CSS TURTLE ART
   ========================================= */

.turtle-container {{
    /* Dynamically scale the artwork based on container size */
    font-size: calc(min(var(--width), var(--height)) / 45);
    width: 40em;
    height: 20em;
    position: relative;
    /* Smooth parallax movement */
    transition: transform 0.1s ease-out;
}}

.shadow {{
    position: absolute;
    bottom: 0.5em;
    left: 5em;
    width: 26em;
    height: 1.5em;
    background: rgba(0, 0, 0, 0.15);
    border-radius: 50%;
    filter: blur(0.3em);
    z-index: 0;
}}

.leg {{
    position: absolute;
    bottom: 2em;
    width: 3.2em;
    height: 5em;
    background: var(--skin);
    border-radius: 0 0 0.6em 0.6em;
    z-index: 1;
    box-shadow: inset -0.3em -0.5em 1em rgba(0,0,0,0.15);
}}

/* Utilizing ::after to create two toes via box-shadow duplication */
.leg::after {{
    content: '';
    position: absolute;
    bottom: 0;
    left: 0.4em;
    width: 0.8em;
    height: 1.2em;
    border-radius: 0.4em 0.4em 0 0;
    background: var(--toes);
    box-shadow: 1.6em 0 0 0 var(--toes);
}}

.leg-1 {{ left: 8em; }}
.leg-2 {{ left: 13em; }}
.leg-3 {{ left: 18em; }}
.leg-4 {{ left: 23em; }}

.tail {{
    position: absolute;
    bottom: 6em;
    left: 4em;
    width: 3.5em;
    height: 3.5em;
    background: var(--skin);
    border-radius: 0 0 0 100%;
    z-index: 1;
}}

.shell {{
    position: absolute;
    bottom: 6em;
    left: 6em;
    width: 22em;
    height: 11em;
    background-color: var(--shell);
    border-radius: 11em 11em 0 0;
    z-index: 4;
    overflow: hidden;
    /* Layered radial gradients to create spots */
    background-image:
        radial-gradient(circle at 20% 75%, var(--spot) 2.2em, transparent 2.25em),
        radial-gradient(circle at 50% 75%, var(--spot-alt) 2.8em, transparent 2.85em),
        radial-gradient(circle at 80% 75%, var(--spot) 2.2em, transparent 2.25em),
        radial-gradient(circle at 35% 35%, var(--spot-alt) 2.2em, transparent 2.25em),
        radial-gradient(circle at 65% 35%, var(--spot) 2.2em, transparent 2.25em);
    box-shadow: inset -1em -1em 2em rgba(0,0,0,0.25);
}}

.neck {{
    position: absolute;
    bottom: 6em;
    left: 24em;
    width: 5em;
    height: 3.5em;
    background: var(--skin);
    z-index: 2;
}}

.head {{
    position: absolute;
    bottom: 6em;
    left: 28.5em;
    width: 5em;
    height: 5em;
    border-radius: 50%;
    background: var(--skin);
    z-index: 3;
    box-shadow: inset -0.5em -0.5em 1em rgba(0,0,0,0.15);
    transform-origin: left bottom;
    animation: head-nod 6s ease-in-out infinite;
}}

/* The sleepy eye */
.head::after {{
    content: '';
    position: absolute;
    top: 1.6em;
    right: 1em;
    width: 1.4em;
    height: 1.4em;
    border-radius: 50%;
    border: 0.25em solid transparent;
    border-bottom-color: var(--eye);
}}

.collar {{
    position: absolute;
    bottom: 5.5em;
    left: 27.5em;
    width: 1.5em;
    height: 4.5em;
    background: var(--accent);
    border-radius: 0.75em;
    z-index: 5;
    box-shadow: 0.2em 0.2em 0.5em rgba(0,0,0,0.15);
}}

/* Subtle sleeping animation */
@keyframes head-nod {{
    0%, 100% {{ transform: rotate(0deg); }}
    50% {{ transform: rotate(4deg); }}
}}
"""

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
    <div class="page-wrapper">
        <div class="text-container">
            <h1 class="title">{title_text}</h1>
            <p class="body-text">{body_text}</p>
        </div>
        
        <div class="turtle-container">
            <div class="shadow"></div>
            <div class="tail"></div>
            <div class="leg leg-1"></div>
            <div class="leg leg-2"></div>
            <div class="leg leg-3"></div>
            <div class="leg leg-4"></div>
            <div class="neck"></div>
            <div class="shell"></div>
            <div class="head"></div>
            <div class="collar"></div>
        </div>
    </div>

    <script src="script.js"></script>
</body>
</html>"""

    js = """// Adds a subtle parallax effect mapping to mouse movement
document.addEventListener('DOMContentLoaded', () => {
    const turtle = document.querySelector('.turtle-container');
    const shadow = document.querySelector('.shadow');

    document.addEventListener('mousemove', (e) => {
        // Calculate offset based on window center
        const xAxis = (window.innerWidth / 2 - e.pageX) / 40;
        const yAxis = (window.innerHeight / 2 - e.pageY) / 40;
        
        // Apply transform to the whole turtle container
        turtle.style.transform = `translate(${xAxis}px, ${yAxis}px)`;
        
        // Counter-animate the shadow slightly to maintain grounded perspective
        shadow.style.transform = `translate(${-xAxis * 0.3}px, ${-yAxis * 0.3}px)`;
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