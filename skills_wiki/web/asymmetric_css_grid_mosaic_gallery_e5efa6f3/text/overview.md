# Asymmetric CSS Grid Mosaic Gallery

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Asymmetric CSS Grid Mosaic Gallery

* **Core Visual Mechanism**: A non-uniform, responsive image gallery ("masonry" or mosaic style) built entirely with CSS Grid. Images dynamically span across varying numbers of columns and rows within an 8×5 structural grid, creating a heavily art-directed, magazine-like layout. A subtle opacity transition draws focus to images upon hover.
* **Why Use This Skill (Rationale)**: Uniform, perfectly symmetrical grids can feel monotonous and static. An asymmetric mosaic creates visual hierarchy, allowing certain images to act as anchors (spanning 4 columns or multiple rows) while others serve as textural filler. This mimics the organic, curated feel of an editorial spread and encourages the user's eye to wander.
* **Overall Applicability**: Ideal for photography portfolios, case study showcases, event galleries, and e-commerce lookbooks where visual impact takes precedence over dense information delivery.
* **Value Addition**: It elevates a standard list of images into a cohesive, structured piece of visual art without requiring any JavaScript calculating positioning or complex absolute coordinates. 
* **Browser Compatibility**: Fully supported in all modern browsers (CSS Grid, `minmax()`, grid spanning, object-fit).

### 2. Visual & Technical Breakdown

* **Step A: Core Visual Elements**
  - **Structure**: A container div wrapping a gallery div, which contains directly nested `<img>` tags.
  - **Color Logic**: The gallery uses a solid background panel (e.g., `#151515`) to ground the images. The images themselves feature a contrasting border (`#ededed`) to create sharp, defined edges between the densely packed grid cells. 
  - **Image Treatment**: Images use `object-fit: cover` to ensure they fill their designated grid areas without stretching.
  - **Typography**: The core component is pure imagery, but any surrounding typography should be clean and sans-serif (e.g., `Inter`) to contrast with the rich visual content.

* **Step B: Layout & Compositional Style**
  - **Grid System**: The defining technical trait is the underlying CSS Grid setup: `grid-template-columns: repeat(8, minmax(10px, 1fr))` combined with `grid-template-rows: repeat(5, 1fr)`. 
  - **Placement Logic**: Individual images are mapped to exact grid coordinates using `grid-column: start / end` and `grid-row: start / end`. This allows for highly customized, overlapping-like layouts (e.g., a 3x2 image sitting next to a 1x2 and a 2x1).
  - **Spacing**: A strict `gap: 15px` ensures consistent negative space across the entire mosaic, while `padding: 15px` on the wrapper ensures the outer bounds match the inner gutters perfectly.

* **Step C: Interactive Behavior & Animations**
  - **Hover State**: Images sit at `opacity: 0.7` by default. On hover, they transition to `opacity: 1`. 
  - **Timing**: `transition: opacity 0.5s ease-out`. The relatively long duration (`0.5s`) gives the interaction a relaxed, cinematic feel rather than a sharp, sudden flash.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| Asymmetric Mosaic Layout | CSS Grid | Native, purely declarative layout logic. Using `grid-column` and `grid-row` precisely recreates the 8x5 spanning structure without JS masonry libraries. |
| Image cropping | `object-fit: cover` | Prevents aspect-ratio distortion when images are forced into varying rectangular grid cells. |
| Interactive focus | CSS Transitions | `opacity` transition on `:hover` is hardware-accelerated, performant, and requires zero JavaScript. |

#### 3b. Complete Reproduction Code

```python
def create_component(
    output_dir: str,
    title_text: str = "Responsive Grid Gallery",
    body_text: str = "A curated collection of visual moments.",
    color_scheme: str = "dark",
    accent_color: str = "#00bfff",
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Asymmetric CSS Grid Mosaic Gallery visual effect.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Derive theme colors
    if color_scheme == "dark":
        bg_color = "#0d111c"
        text_color = "#f0f0f0"
        surface_color = "#151515"
        border_color = "#ededed"
    else:
        bg_color = "#f8f9fa"
        text_color = "#1a1a2e"
        surface_color = "#e9ecef"
        border_color = "#2c2c2c"

    # === CSS ===
    css = f"""/* Asymmetric CSS Grid Mosaic Gallery */
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
    --border: {border_color};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background: var(--bg);
    color: var(--text);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 2rem;
}}

.container {{
    width: var(--width);
    height: var(--height);
    max-width: 100%;
    max-height: 90vh;
    display: flex;
    flex-direction: column;
}}

.header {{
    text-align: center;
    margin-bottom: 1.5rem;
    flex-shrink: 0;
}}

.title {{
    font-size: 2.5rem;
    font-weight: 700;
    margin-bottom: 0.5rem;
    color: var(--accent);
    letter-spacing: -0.02em;
}}

.body-text {{
    font-size: 1.1rem;
    opacity: 0.8;
}}

.gallery {{
    flex-grow: 1;
    display: grid;
    /* 8 Columns */
    grid-template-columns: repeat(8, minmax(10px, 1fr));
    /* 5 Rows */
    grid-template-rows: repeat(5, 1fr);
    grid-gap: 15px;
    background-color: var(--surface);
    padding: 15px;
    border-radius: 12px;
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15);
    overflow: hidden;
}}

.gallery img {{
    width: 100%;
    height: 100%;
    object-fit: cover;
    opacity: 0.7;
    transition: opacity 0.5s ease-out, transform 0.5s ease-out;
    border: 2px solid var(--border);
    border-radius: 4px;
    background-color: var(--bg); /* loading fallback */
    cursor: pointer;
}}

.gallery img:hover {{
    opacity: 1;
}}

/* Grid Placements matching the 8x5 asymmetric layout */
.img-1  {{ grid-column: 1 / 3; grid-row: 1 / 3; }}
.img-2  {{ grid-column: 3 / 6; grid-row: 1 / 3; }}
.img-3  {{ grid-column: 6 / 7; grid-row: 1 / 3; }}
.img-4  {{ grid-column: 7 / 9; grid-row: 1 / 2; }}
.img-5  {{ grid-column: 7 / 9; grid-row: 2 / 4; }}
.img-6  {{ grid-column: 5 / 7; grid-row: 3 / 4; }}
.img-7  {{ grid-column: 1 / 3; grid-row: 3 / 5; }}
.img-8  {{ grid-column: 3 / 5; grid-row: 3 / 5; }}
.img-9  {{ grid-column: 1 / 5; grid-row: 5 / 6; }}
.img-10 {{ grid-column: 5 / 7; grid-row: 4 / 6; }}
.img-11 {{ grid-column: 7 / 9; grid-row: 4 / 5; }}
.img-12 {{ grid-column: 7 / 9; grid-row: 5 / 6; }}

/* Graceful degradation for smaller screens */
@media (max-width: 768px) {{
    .container {{
        height: auto;
    }}
    .gallery {{
        grid-template-columns: repeat(2, 1fr);
        grid-template-rows: auto;
        grid-auto-rows: 200px;
    }}
    .gallery img {{
        grid-column: span 1 !important;
        grid-row: span 1 !important;
    }}
    /* Keep a slight variation on mobile */
    .img-2, .img-9, .img-10 {{
        grid-column: span 2 !important;
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
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        <div class="header">
            <h1 class="title">{title_text}</h1>
            <p class="body-text">{body_text}</p>
        </div>
        <div class="gallery">
            <!-- Using Unsplash Source via Picsum with specific dimension hints matching their grid areas -->
            <img src="https://picsum.photos/seed/gal1/400/400" class="img-1" alt="Gallery Image 1">
            <img src="https://picsum.photos/seed/gal2/600/400" class="img-2" alt="Gallery Image 2">
            <img src="https://picsum.photos/seed/gal3/200/400" class="img-3" alt="Gallery Image 3">
            <img src="https://picsum.photos/seed/gal4/400/200" class="img-4" alt="Gallery Image 4">
            <img src="https://picsum.photos/seed/gal5/400/400" class="img-5" alt="Gallery Image 5">
            <img src="https://picsum.photos/seed/gal6/400/200" class="img-6" alt="Gallery Image 6">
            <img src="https://picsum.photos/seed/gal7/400/400" class="img-7" alt="Gallery Image 7">
            <img src="https://picsum.photos/seed/gal8/400/400" class="img-8" alt="Gallery Image 8">
            <img src="https://picsum.photos/seed/gal9/800/200" class="img-9" alt="Gallery Image 9">
            <img src="https://picsum.photos/seed/gal10/400/400" class="img-10" alt="Gallery Image 10">
            <img src="https://picsum.photos/seed/gal11/400/200" class="img-11" alt="Gallery Image 11">
            <img src="https://picsum.photos/seed/gal12/400/200" class="img-12" alt="Gallery Image 12">
        </div>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Asymmetric CSS Grid Mosaic Gallery
document.addEventListener('DOMContentLoaded', () => {{
    // The core effect is fully driven by CSS Grid and CSS Transitions.
    // This JS file is included for potential future extensions, such as opening a lightbox on click.
    
    const images = document.querySelectorAll('.gallery img');
    images.forEach(img => {{
        img.addEventListener('click', () => {{
            console.log('Clicked image:', img.src);
            // Lightbox logic could be injected here
        }});
    }});
}});
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

* **Accessibility**: Added standard `alt` tags to the generated images. Since this relies on `opacity`, contrast isn't highly relevant for the images themselves, but text outside the gallery is rendered clearly above the WCAG minimums based on the derived light/dark themes.
* **Performance**: The grid heavily leverages CSS Grid, which is native and highly optimized by modern browser layout engines. The `opacity` transition on hover avoids triggering layout recalculations (reflow/repaint jank) because opacity is composite-only, meaning the GPU handles it smoothly. 
* **Graceful Degradation**: A media query (`max-width: 768px`) is included to prevent the complex 8-column layout from turning into unintelligible, tiny slivers on mobile devices, reflowing safely into a responsive 2-column masonry approximation.