### 1. High-level Design Pattern Extraction

> **Skill Name**: Split-Content Centered-Portrait Hero

* **Core Visual Mechanism**: This design relies on CSS multiple backgrounds to anchor a central "cutout" image (like a portrait or product) and a subtle repeating background pattern. CSS Flexbox is used to center the primary content, but `position: relative` combined with horizontal offsets (`left`, `right`) pushes the text outwardly. This visually flanks the central subject with bold primary copy on one side and secondary elements (like staggered blockquotes) on the other side, without causing document overflow or breaking the structural alignment.
* **Why Use This Skill (Rationale)**: Standard web design heavily relies on split-screen (text left, image right) or centered-stack (text above image) layouts. This pattern creates a distinct, magazine-like editorial feel. The centered focal image creates an immediate human connection or product focus, while the flanking content provides immediate context and social proof (quotes) in the negative space.
* **Overall Applicability**: Keynote speaker landing pages, personal developer/designer portfolios, high-end creative agency sites, or product feature spotlights.
* **Value Addition**: It solves the common problem of "floating heads" in web design by deliberately framing the portrait with typography. The use of multiple CSS backgrounds instead of absolute-positioned `<img>` tags makes the structure lightweight, easy to align, and highly performant.
* **Browser Compatibility**: Fully supported in all modern browsers. Relies on standard CSS Flexbox and Multiple Backgrounds.

### 2. Visual & Technical Breakdown

* **Step A: Core Visual Elements**
  - **Color Logic**: A deep, solid background (e.g., `#1A253A`) with a vibrant accent color (e.g., `#c13584` magenta). Secondary text is dimmed via lower opacity `rgba(255,255,255,0.7)`.
  - **Typography**: Employs a stark typographic hierarchy. The main heading is oversized, uppercase, and tightly tracked (`font-size: 4rem; line-height: 1.1; font-weight: 800`).
  - **Accents**: The secondary quotes are unified through thick, accent-colored left borders (`border-left: 4px solid var(--accent)`).

* **Step B: Layout & Compositional Style**
  - **Layout System**: The wrapper uses CSS Flexbox (`justify-content: center; align-items: center`).
  - **Spatial Feel**: The central column of the screen is intentionally left blank for the background portrait. The left block (`.hero-intro`) is shifted using `right: 15%` and the right block (`.hero-quotes`) is shifted using `left: 15%`.
  - **Staggering**: The blockquotes are given an asymmetrical rhythm by targeting the second child (`nth-child(2)`) and pushing it horizontally (`margin-left: 4rem`).

* **Step C: Interactive Behavior & Animations**
  - **Button Hover**: A sharp, simple hover effect on the Call-to-Action button using CSS `filter: brightness(1.2)`.
  - **Parallax Enhancements**: While the tutorial uses static backgrounds, this style is perfectly suited for a lightweight JavaScript mousemove parallax. Mapping the cursor position to the `background-position` properties makes the portrait and pattern shift independently, creating a pseudo-3D depth effect.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **Layered Portrait & Pattern** | CSS Multiple Backgrounds | `background-image` allows layering an unlimited number of image/SVG URLs onto a single container, perfect for keeping the DOM clean. |
| **Placeholder Graphics** | SVG Data URIs | Ensures the code is completely self-contained and immediately viewable without fetching external image assets. |
| **Content Flanking** | Flexbox + Relative Offsets | Allows vertical centering while easily pushing elements away from the face of the portrait without breaking layout flow. |
| **Hover / Depth** | JS Mousemove Event | Dynamically updating `background-position` adds significant premium feel (parallax) to the static layout taught in the tutorial. |

#### 3b. Complete Reproduction Code

```python
def create_component(
    output_dir: str,
    title_text: str = "WELCOME TO MY FIRST WEBSITE",
    body_text: str = "Nam interdum felis at felis placerat, sed varius massa ultricies. Integer quis nisi non dolor scelerisque efficitur at sed turpis.",
    color_scheme: str = "dark",
    accent_color: str = "#c13584",
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the 'Split-Content Centered-Portrait Hero'.
    
    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os
    import urllib.parse

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme variables ===
    if color_scheme == "dark":
        bg_color = "#1a253a"
        text_color = "#ffffff"
        text_dim = "rgba(255, 255, 255, 0.7)"
        silhouette_color_hex = "#0f172a"
        pattern_color = "rgba(255, 255, 255, 0.03)"
    else:
        bg_color = "#f8f9fa"
        text_color = "#1a253a"
        text_dim = "rgba(26, 37, 58, 0.7)"
        silhouette_color_hex = "#e2e8f0"
        pattern_color = "rgba(0, 0, 0, 0.03)"

    # Generate Self-Contained SVG placeholders
    svg_pattern = f"<svg xmlns='http://www.w3.org/2000/svg' width='60' height='60'><path d='M30 0 L60 30 L30 60 L0 30 Z' fill='none' stroke='{pattern_color}' stroke-width='2'/><circle cx='30' cy='30' r='3' fill='{pattern_color}'/></svg>"
    encoded_pattern = urllib.parse.quote(svg_pattern)

    svg_portrait = f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 400 600'><circle cx='200' cy='150' r='60' fill='{silhouette_color_hex}'/><path d='M200 230 C 120 230 60 300 40 400 L 20 600 L 380 600 L 360 400 C 340 300 280 230 200 230 Z' fill='{silhouette_color_hex}'/></svg>"
    encoded_portrait = urllib.parse.quote(svg_portrait)

    # === CSS ===
    css = f"""/* Split-Content Centered-Portrait Hero */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --text: {text_color};
    --text-dim: {text_dim};
    --accent: {accent_color};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Roboto', system-ui, -apple-system, sans-serif;
    background: var(--bg);
    color: var(--text);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
}}

.hero-container {{
    width: var(--width);
    max-width: 100%;
    height: var(--height);
    background-color: var(--bg);
    /* Multiple backgrounds: Top layer is the portrait, bottom layer is the repeating pattern */
    background-image: 
        url("data:image/svg+xml,{encoded_portrait}"),
        url("data:image/svg+xml,{encoded_pattern}");
    background-size: 70vh, 60px;
    background-repeat: no-repeat, repeat;
    background-position: bottom center, center;
    display: flex;
    justify-content: center;
    align-items: center;
    overflow: hidden;
    position: relative;
    /* Transition for the parallax elastic snap-back */
    transition: background-position 0.1s ease-out;
}}

/* Flanking Content Logic */
.hero-intro {{
    position: relative;
    right: 15%;
    max-width: 400px;
    padding-bottom: 10vh; /* Lift slightly to clear bottom-anchored portrait shoulders */
    z-index: 10;
}}

.hero-quotes {{
    position: relative;
    left: 15%;
    max-width: 320px;
    padding-bottom: 5vh;
    z-index: 10;
}}

/* Typography & Components */
.hero-intro h1 {{
    font-size: 4.5rem;
    line-height: 1.05;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: -0.02em;
    margin-bottom: 1.5rem;
}}

.hero-intro p {{
    font-size: 1.125rem;
    line-height: 1.6;
    color: var(--text-dim);
    margin-bottom: 2.5rem;
}}

.cta-btn {{
    display: inline-block;
    background-color: var(--accent);
    color: #fff;
    padding: 14px 32px;
    text-decoration: none;
    font-weight: 700;
    font-size: 0.875rem;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    transition: filter 0.3s ease;
    border-radius: 2px;
}}

.cta-btn:hover {{
    filter: brightness(1.2);
}}

/* Asymmetrical Quotes */
.quote-block {{
    border-left: 4px solid var(--accent);
    padding-left: 1.5rem;
    margin-bottom: 3rem;
}}

.hero-quotes .quote-block:nth-child(2) {{
    margin-left: 4rem; /* Staggering effect */
}}

.quote-block p {{
    font-size: 1.05rem;
    line-height: 1.7;
    margin-bottom: 0.75rem;
}}

.quote-block .author {{
    font-size: 0.875rem;
    font-weight: 600;
    color: var(--text-dim);
    display: block;
}}

/* Responsive Fallback */
@media (max-width: 900px) {{
    .hero-container {{
        flex-direction: column;
        justify-content: flex-start;
        padding-top: 4rem;
        /* Move portrait out of the way for mobile */
        background-position: bottom right -20%, center;
        background-size: 50vh, 60px;
    }}
    
    .hero-intro, .hero-quotes {{
        right: 0; left: 0;
        max-width: 85%;
        padding-bottom: 2rem;
    }}
    
    .hero-quotes .quote-block:nth-child(2) {{
        margin-left: 2rem;
    }}
    
    .hero-intro h1 {{
        font-size: 3rem;
    }}
}}
"""

    # === HTML ===
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Split-Content Hero</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Roboto:ital,wght@0,400;0,600;0,800;1,400&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="hero-container">
        
        <!-- Left Flank: Primary Content -->
        <div class="hero-intro">
            <h1>{title_text}</h1>
            <p>{body_text}</p>
            <a href="#work" class="cta-btn">My Work</a>
        </div>
        
        <!-- Right Flank: Secondary Content / Quotes -->
        <div class="hero-quotes">
            <div class="quote-block">
                <p>"The more that you read, the more things you will know. The more that you learn, the more places you'll go."</p>
                <span class="author">- Dr. Seuss</span>
            </div>
            <div class="quote-block">
                <p>"For the best return on your money, pour your purse into your head."</p>
                <span class="author">- Benjamin Franklin</span>
            </div>
        </div>

    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Lightweight background parallax logic
document.addEventListener('DOMContentLoaded', () => {{
    const hero = document.querySelector('.hero-container');
    
    // Check if device supports hover (ignore touch devices to prevent jumping)
    if (window.matchMedia("(hover: hover)").matches) {{
        hero.addEventListener('mousemove', (e) => {{
            // Calculate mouse distance from center (-1 to 1)
            const x = (e.clientX / window.innerWidth - 0.5) * 2;
            const y = (e.clientY / window.innerHeight - 0.5) * 2;
            
            // Apply slight opposing movements to portrait (foreground) and pattern (background)
            // Portrait moves subtly with the mouse, pattern moves against it
            const portraitX = x * 10;
            const portraitY = y * 10;
            
            const patternX = x * -20;
            const patternY = y * -20;
            
            hero.style.backgroundPosition = `
                calc(50% + ${portraitX}px) calc(100% + ${portraitY}px), 
                calc(50% + ${patternX}px) calc(50% + ${patternY}px)
            `;
        }});
        
        // Snap back to original position smoothly when mouse leaves
        hero.addEventListener('mouseleave', () => {{
            hero.style.backgroundPosition = 'bottom center, center';
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

### 4. Accessibility & Performance Notes

* **Accessibility**: The background images are applied purely via CSS, rendering them decorative. Screen readers will naturally read the left text block followed by the right quotes without being hindered by dummy structural images. Ensure that `accent_color` paired with white text provides a WCAG compliant contrast ratio (at least 4.5:1).
* **Performance**: Utilizing CSS multiple backgrounds to compose the scene is remarkably performant compared to absolute positioning heavy `<img/>` nodes. The JavaScript interaction checks for pointer capabilities via `window.matchMedia("(hover: hover)")` to avoid triggering heavy recalculations or confusing behaviors on mobile devices. Using native CSS `transition` with `background-position` allows the browser to interpolate the layout without needing an expensive GSAP/RAF animation loop.