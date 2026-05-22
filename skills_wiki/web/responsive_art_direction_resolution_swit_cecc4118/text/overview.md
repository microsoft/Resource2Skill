# Responsive Art Direction & Resolution Switching (<picture>)

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Responsive Art Direction & Resolution Switching (`<picture>`)

* **Core Visual Mechanism**: The HTML5 `<picture>` element is used to serve dynamically adapted images based on the user's viewport width and device pixel density. Instead of just scaling down a single large image, this mechanism utilizes `<source>` tags with `media` and `srcset` attributes to deliver completely different crops (Art Direction) or appropriately sized files (Resolution Switching) tailored to the device context.
* **Why Use This Skill (Rationale)**: 
  - **Contextual Framing**: A wide panoramic image that looks great on desktop becomes unreadable when shrunk to fit a mobile screen. Art direction allows you to serve a tighter, square crop on mobile so the core subject remains prominent.
  - **Performance**: Prevents mobile users on slow connections from downloading a 3MB 4K desktop image when a 200KB version is sufficient for their screen width.
  - **Crispness**: Allows delivery of `@2x` or `@3x` resolution images specifically for Retina/high-DPI screens, ensuring visual sharpness without penalizing low-DPI users.
* **Overall Applicability**: Essential for hero sections, editorial banner images, product galleries, and full-bleed background images across modern web applications.
* **Value Addition**: Transforms a static `<img>` into an intelligent, context-aware component powered natively by the browser's rendering engine without requiring JavaScript to observe resizing or calculate device metrics.
* **Browser Compatibility**: Fully supported in all modern browsers (Chrome, Safari, Firefox, Edge).

### 2. Visual & Technical Breakdown

* **Step A: Core Visual Elements**
  - **HTML Structure**: The `<picture>` element wraps multiple `<source>` tags and a fallback `<img>` tag.
  - **`media` Attribute**: Uses standard CSS media queries (e.g., `(max-width: 480px)`) to set conditions for when an image source should be used.
  - **`srcset` Attribute**: Defines the image URL(s). It can also map multiple URLs to display densities (e.g., `image-1x.jpg 1x, image-2x.jpg 2x`).
  - **Fallback**: The `<img>` tag is mandatory. If the browser does not support `<picture>`, or if none of the `<source>` conditions are met, it renders the `<img>`. 
  
* **Step B: Layout & Compositional Style**
  - To support responsive behavior, the fallback `<img>` element must be styled with `width: 100%` and `height: auto` in CSS. This ensures that whichever image the browser selects from the `<source>` list will scale fluidly within its parent container.
  - Placed inside a semantic `<figure>` container to bind the visual asset with an optional `<figcaption>`.

* **Step C: Interactive Behavior & Animations**
  - **Native Browser Handling**: The switching behavior is 100% handled by the browser. As the viewport resizes, the browser evaluates the `media` queries from top to bottom. Once a condition is met, it swaps the internal source of the `<img />` node. 
  - **No JS Required**: This requires zero JavaScript for the core functionality, avoiding the layout jank associated with JS-based window resize event listeners.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| Image Switching | HTML `<picture>` & `<source>` | Native browser API designed specifically for responsive art direction; zero JS required. |
| Viewport Conditions | `media` attribute | Utilizes native CSS media queries directly inside HTML for logic routing. |
| Retina Support | `srcset` with `2x` | Automatically handles high-DPI displays without writing complex CSS `@media` density queries. |
| Live Feedback (Demo) | JS `resize` listener | Used purely to render a floating badge showing the current viewport width, making the native image switching threshold obvious. |

> **Feasibility Assessment**: 100%. The HTML5 `<picture>` spec operates exactly as described. For demonstration purposes, this code dynamically generates images of different sizes and crops via a placeholder CDN (`placehold.co`) so the "art direction" effect is visually obvious upon resizing the browser.

#### 3b. Complete Reproduction Code

```python
def create_component(
    output_dir: str,
    title_text: str = "Responsive Art Direction",
    body_text: str = "Resize your browser window to see the image adapt. The browser natively switches between different crops and resolutions based on the viewport width.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#00bfff",     # CSS hex color for accent
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Responsive Picture Element visual effect.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme and accent_color ===
    if color_scheme == "dark":
        bg_color = "#0d111c"
        text_color = "#f0f0f0"
        surface_color = "#1a2235"
    else:
        bg_color = "#f8f9fa"
        text_color = "#1a1a2e"
        surface_color = "#ffffff"
        
    # Strip '#' for the placehold.co URL generation
    surface_hex = surface_color.replace("#", "")
    accent_hex = accent_color.replace("#", "")

    # === CSS ===
    css = f"""/* Responsive Art Direction — generated component */
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
    --max-width: {width_px}px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background: var(--bg);
    color: var(--text);
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 2rem;
}}

.container {{
    max-width: var(--max-width);
    width: 100%;
    background: var(--surface);
    border-radius: 16px;
    padding: 2.5rem;
    box-shadow: 0 12px 32px rgba(0, 0, 0, 0.15);
}}

.title {{
    font-size: 2.25rem;
    font-weight: 700;
    margin-bottom: 1rem;
    color: var(--text);
    letter-spacing: -0.02em;
}}

.body-text {{
    font-size: 1.125rem;
    line-height: 1.6;
    margin-bottom: 2.5rem;
    color: var(--text);
    opacity: 0.8;
    max-width: 800px;
}}

.hero-figure {{
    width: 100%;
    border-radius: 12px;
    overflow: hidden;
    background: var(--bg);
    border: 1px solid rgba(128, 128, 128, 0.1);
}}

/* The critical CSS rule for fluid responsive images */
.responsive-image {{
    display: block;
    width: 100%;
    height: auto;
    object-fit: cover;
}}

figcaption {{
    padding: 1.25rem;
    text-align: center;
    font-size: 0.875rem;
    background: var(--bg);
    color: var(--text);
    opacity: 0.7;
}}

code {{
    background: rgba(128, 128, 128, 0.15);
    padding: 0.2rem 0.4rem;
    border-radius: 4px;
    font-family: 'Menlo', 'Monaco', monospace;
    color: var(--accent);
}}

/* Dynamic Viewport Badge */
.size-display {{
    position: fixed;
    top: 24px;
    right: 24px;
    background: var(--surface);
    color: var(--text);
    padding: 0.75rem 1.25rem;
    border-radius: 8px;
    font-weight: 500;
    font-size: 0.875rem;
    z-index: 1000;
    box-shadow: 0 8px 24px rgba(0,0,0,0.2);
    border: 1px solid rgba(128, 128, 128, 0.1);
}}

.size-display span {{
    color: var(--accent);
    font-weight: 700;
}}

@media (max-width: 600px) {{
    body {{ padding: 1rem; }}
    .container {{ padding: 1.5rem; }}
    .title {{ font-size: 1.75rem; }}
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
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <main class="container">
        <h1 class="title">{title_text}</h1>
        <p class="body-text">{body_text}</p>
        
        <figure class="hero-figure">
            <!-- 
              The <picture> element evaluates <source> tags from top to bottom. 
              The first media query that returns true is selected.
            -->
            <picture>
                <!-- Mobile: Art directed crop (1:1 Square) with Retina display support -->
                <source media="(max-width: 500px)" 
                        srcset="https://placehold.co/500x500/{surface_hex}/{accent_hex}?text=Mobile+Crop+(Square)+1x 1x, 
                                https://placehold.co/1000x1000/{surface_hex}/{accent_hex}?text=Mobile+Retina+(Square)+2x 2x">
                
                <!-- Tablet: Medium size (3:2 Aspect Ratio) -->
                <source media="(max-width: 900px)" 
                        srcset="https://placehold.co/900x600/{surface_hex}/{accent_hex}?text=Tablet+View+(3:2)">
                        
                <!-- Desktop: Wide landscape (2:1 Aspect Ratio) -->
                <source media="(min-width: 901px)" 
                        srcset="https://placehold.co/1600x800/{surface_hex}/{accent_hex}?text=Desktop+View+(2:1)">
                        
                <!-- Fallback: Standard IMG tag. This is required and also acts as the baseline default -->
                <img src="https://placehold.co/1600x800/{surface_hex}/{accent_hex}?text=Desktop+View+(2:1)" 
                     alt="A dynamically responsive demonstration placeholder" 
                     class="responsive-image"
                     loading="lazy">
            </picture>
            <figcaption>
                The image above physically changes its source file as you scale the window past 900px and 500px boundaries.
            </figcaption>
        </figure>
    </main>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Responsive Art Direction — Interactive Behavior
document.addEventListener('DOMContentLoaded', () => {{
    // Create a dynamic badge to show the user the current window width
    // This helps visualize exactly when the <picture> element switches sources
    const sizeDisplay = document.createElement('div');
    sizeDisplay.className = 'size-display';
    document.body.appendChild(sizeDisplay);

    function updateSize() {{
        sizeDisplay.innerHTML = `Viewport width: <span>${{window.innerWidth}}px</span>`;
    }}
    
    // Listen for resize events
    window.addEventListener('resize', () => {{
        // Use requestAnimationFrame to throttle resize events slightly for performance
        window.requestAnimationFrame(updateSize);
    }});
    
    // Initial call
    updateSize();
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

* **Accessibility**: 
  - The fallback `<img>` element is what screen readers interact with. You **must** provide the `alt` attribute on the `<img>` tag, *not* on the `<picture>` or `<source>` tags.
  - The `alt` text should describe the visual content accurately, regardless of which crop is currently being displayed by the browser.
* **Performance**: 
  - **Bandwidth**: By avoiding loading 4K images on a 375px wide smartphone, you significantly improve Time to Interactive (TTI) and First Contentful Paint (FCP).
  - **Lazy Loading**: The `<img loading="lazy">` attribute was added to the fallback image. Because the `<picture>` element inherits attributes off the `<img>`, this native lazy loading propagates seamlessly to whichever `<source>` is currently selected.
  - **Browser Processing**: Because the logic resides in the HTML `media` attributes, the browser pre-parser can fetch the correct image file concurrently with CSS processing, without waiting for the DOM to fully load or JS to execute.