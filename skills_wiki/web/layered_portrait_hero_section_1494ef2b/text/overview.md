# Agent_Skill_Distiller: Pattern Extraction

### 1. High-level Design Pattern Extraction

> **Skill Name**: Layered Portrait Hero Section

* **Core Visual Mechanism**: A full-viewport split-content hero section that leverages CSS `background-image` layering to create depth. By stacking a bottom-aligned silhouette/portrait image over a textured backdrop, and wrapping the foreground typography around the subject's negative space using `position: relative`, it creates a compelling 2.5D spatial layout.
* **Why Use This Skill (Rationale)**: This layout breaks the monotony of standard left-aligned or center-aligned hero sections. It places the subject (the portrait or product) at the focal center, while organizing primary messaging (headline, CTA) and secondary messaging (social proof, quotes) into distinct visual buckets that frame the subject.
* **Overall Applicability**: Ideal for personal portfolios, agency landing pages, consultant sites, or any brand where a human element or central product needs to be highly visible without compromising typographic space.
* **Value Addition**: Compared to standard grid or flex layouts with `<img>` tags, using multi-layered background images prevents complex z-index issues and keeps the DOM incredibly lightweight. The use of relative positioning to offset the text blocks creates a dynamic, magazine-like editorial layout.
* **Browser Compatibility**: Fully supported in all modern browsers. Relies on standard CSS Flexbox and multiple backgrounds.

### 2. Visual & Technical Breakdown

* **Step A: Core Visual Elements**
  - **Layered Backgrounds**: Utilizes comma-separated values in `background-image` to layer a subject image (`background-size: 70vh; background-position: bottom center`) over a base texture (`cover`).
  - **Typography**: Heavy, uppercase sans-serif headers (e.g., `96px`, `font-weight: 800`) to anchor the left side, contrasted with smaller, legible paragraph text (`18px`) on the right.
  - **Color Logic**: Deep atmospheric background (`#1A253A`) with bright, high-contrast text (`#ffffff`) and a vibrant brand accent (`#C13584`) applied to buttons and structural borders.

* **Step B: Layout & Compositional Style**
  - **Layout System**: A central Flexbox container (`display: flex; justify-content: center; align-items: center;`) groups the two content blocks together.
  - **Spatial Feel**: Instead of relying on rigid CSS Grid columns, the design uses `position: relative` with horizontal offsets (e.g., `right: 15%` on the left block, `left: 5%` on the right block) to push the content apart, leaving a "hole" in the middle for the background portrait to shine through.
  - **Secondary Block Styling**: The secondary content (quotes) is anchored by a thick left border (`4px solid`), creating a strong vertical line that mirrors the edge of the central portrait.

* **Step C: Interactive Behavior & Animations**
  - **Button Hover**: High-contrast background color shift.
  - **Entrance**: The text blocks fade and slide up sequentially, allowing the user to process the background subject first, followed by the headline, then the secondary text.
  - **Parallax (Enhancement)**: JavaScript tracks mouse movement and lightly shifts the `background-position` of the portrait, amplifying the sense of depth between the foreground text and the background subject.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **Layered Imagery** | CSS `background-image` | Allows stacking the portrait and the texture in a single element, avoiding extra DOM nodes and strict `z-index` management. |
| **Split Wrapping Layout** | CSS Flexbox + `position: relative` | Centers the items naturally, while relative offsets (`left`/`right`) visually push them apart without breaking document flow. |
| **Responsive Typography** | CSS `clamp()` | Replaces the tutorial's rigid `96px` font sizes with fluid scaling, preventing breakage on smaller viewports. |
| **Depth Interaction** | JS Mousemove Event | Shifting the `background-position` based on cursor coordinates creates a cheap but highly effective parallax illusion. |

#### 3b. Complete Reproduction Code

```python
def create_component(
    output_dir: str,
    title_text: str = "WELCOME<br>TO MY<br>PORTFOLIO",
    body_text: str = "I build interactive, immersive web experiences. Let's create something memorable together.",
    color_scheme: str = "dark",
    accent_color: str = "#C13584",
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Layered Portrait Hero Section.
    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Theme colors based on the tutorial's aesthetic
    if color_scheme == "dark":
        bg_color = "#1A253A"
        text_color = "#ffffff"
        text_muted = "rgba(255, 255, 255, 0.7)"
        overlay = "rgba(26, 37, 58, 0.8)"
    else:
        bg_color = "#e2e8f0"
        text_color = "#0f172a"
        text_muted = "rgba(15, 23, 42, 0.7)"
        overlay = "rgba(226, 232, 240, 0.8)"

    # CSS Generation
    css = f"""/* Layered Portrait Hero Section */
:root {{
    --bg-color: {bg_color};
    --text-color: {text_color};
    --text-muted: {text_muted};
    --accent: {accent_color};
    --overlay: {overlay};
    --width: {width_px}px;
    --height: {height_px}px;
}}

*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background: var(--bg-color);
    color: var(--text-color);
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
}}

.container {{
    width: var(--width);
    height: var(--height);
    max-width: 100vw;
    position: relative;
    display: flex;
    justify-content: center;
    align-items: center;
    overflow: hidden;
    
    /* 
       Multiple backgrounds: 
       1. Top layer: The portrait (SVG data URI placeholder)
       2. Bottom layer: A radial gradient texture
    */
    background-image: 
        url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 400 500'%3E%3Cpath d='M80,500 C80,350 130,280 200,280 C270,280 320,350 320,500 Z' fill='{text_color.replace('#', '%23')}' opacity='0.15'/%3E%3Ccircle cx='200' cy='180' r='80' fill='{text_color.replace('#', '%23')}' opacity='0.15'/%3E%3C/svg%3E"),
        radial-gradient(circle at center, var(--overlay) 0%, var(--bg-color) 100%);
    background-size: 70vh, cover;
    background-repeat: no-repeat, no-repeat;
    background-position: bottom center, center;
    transition: background-position 0.1s ease-out;
}}

/* Left Block - Primary Info */
.main-intro {{
    position: relative;
    right: 12%; /* Pushes the block left, away from the portrait */
    max-width: 450px;
    z-index: 10;
    animation: fadeInUp 0.8s cubic-bezier(0.2, 0.8, 0.2, 1) forwards;
}}

.main-intro h1 {{
    font-size: clamp(2.5rem, 5vw, 5rem);
    line-height: 1.05;
    font-weight: 800;
    text-transform: uppercase;
    margin-bottom: 24px;
    letter-spacing: -0.02em;
}}

.main-intro p {{
    font-size: 18px;
    line-height: 1.6;
    color: var(--text-muted);
    margin-bottom: 40px;
}}

.cta-button {{
    display: inline-block;
    background-color: var(--accent);
    color: #ffffff;
    text-decoration: none;
    padding: 16px 32px;
    font-size: 14px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1px;
    border-radius: 2px;
    transition: filter 0.2s ease, transform 0.2s ease;
}}

.cta-button:hover {{
    filter: brightness(1.2);
    transform: translateY(-2px);
}}

/* Right Block - Secondary Info */
.main-quotes {{
    position: relative;
    left: 8%; /* Pushes the block right, away from the portrait */
    max-width: 320px;
    border-left: 4px solid var(--accent);
    padding-left: 24px;
    z-index: 10;
    opacity: 0;
    animation: fadeInUp 0.8s cubic-bezier(0.2, 0.8, 0.2, 1) 0.3s forwards;
}}

.quote-item {{
    margin-bottom: 32px;
}}

.quote-item:last-child {{
    margin-bottom: 0;
}}

.quote-item p {{
    font-size: 16px;
    line-height: 1.7;
    margin-bottom: 12px;
    font-style: italic;
}}

.quote-author {{
    font-size: 14px;
    font-weight: 600;
    color: var(--accent);
}}

/* Keyframes */
@keyframes fadeInUp {{
    from {{
        opacity: 0;
        transform: translateY(30px);
    }}
    to {{
        opacity: 1;
        transform: translateY(0);
    }}
}}

/* Basic Responsiveness for smaller preview windows */
@media (max-width: 900px) {{
    .container {{
        flex-direction: column;
        justify-content: center;
        padding: 40px;
        background-position: bottom right -10vw, center;
    }}
    .main-intro, .main-quotes {{
        position: static;
        max-width: 100%;
        margin: 20px 0;
    }}
}}
"""

    # HTML Generation
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hero Section Component</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        
        <div class="main-intro">
            <h1>{title_text}</h1>
            <p>{body_text}</p>
            <a href="#" class="cta-button">View My Work</a>
        </div>

        <div class="main-quotes">
            <div class="quote-item">
                <p>"The more that you read, the more things you will know. The more that you learn, the more places you'll go."</p>
                <span class="quote-author">— Dr. Seuss</span>
            </div>
            <div class="quote-item">
                <p>"An investment in knowledge pays the best interest."</p>
                <span class="quote-author">— Benjamin Franklin</span>
            </div>
        </div>

    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # JS Generation (Adds Parallax enhancement)
    js = """document.addEventListener('DOMContentLoaded', () => {
    const container = document.querySelector('.container');

    // Add subtle mousemove parallax to the background portrait
    container.addEventListener('mousemove', (e) => {
        // Calculate normalized mouse position (-1 to 1)
        const x = (e.clientX / window.innerWidth - 0.5) * 2;
        const y = (e.clientY / window.innerHeight - 0.5) * 2;

        // Shift background position slightly (offsetting the 'bottom center' default)
        const shiftX = x * -20; // Move up to 20px opposite to mouse
        const shiftY = y * -10; 

        // Update the first background (portrait), leave the second (texture) alone
        container.style.backgroundPosition = `calc(50% + ${shiftX}px) calc(100% + ${shiftY}px), center`;
    });

    // Reset smoothly on mouse leave
    container.addEventListener('mouseleave', () => {
        container.style.backgroundPosition = 'bottom center, center';
        container.style.transition = 'background-position 0.5s ease-out';
        
        // Remove transition after reset so mousemove is snappy again
        setTimeout(() => {
            container.style.transition = 'none';
        }, 500);
    });
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

* **Accessibility**:
  - The heavy reliance on background images means important subject imagery is purely decorative. If the central portrait is conceptually vital, standard `<img>` tags with `alt` text and grid layouts would be more semantically appropriate.
  - The `clamp()` function ensures typography remains readable across devices without breaking layout boundaries or requiring horizontal scrolling.
  - Button styling uses sufficient padding (`16px 32px`) to provide an accessible minimum touch target size.
* **Performance**:
  - `background-image` is generally performant, but animating `background-position` via JavaScript on `mousemove` triggers style recalculations and repaints. While inexpensive on modern devices for a single container, in high-complexity apps it may be better to use absolute positioning with `transform: translate3d()` for hardware-accelerated parallax.
  - Using inline SVG data URIs for the background prevents extra HTTP requests, ensuring instant visual rendering.