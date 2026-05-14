# Full-Screen Immersive Flexbox Hero

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Full-Screen Immersive Flexbox Hero

* **Core Visual Mechanism**: A full-viewport (`100vh`) introductory block that utilizes CSS Flexbox to perfectly center textual content and a Call-to-Action (CTA) over a responsive, edge-to-edge background image (`background-size: cover`).
* **Why Use This Skill (Rationale)**: This layout immediately commands the user's attention, setting the thematic tone of the website through large-scale imagery while keeping the primary value proposition and next step (the button) in the most ergonomically focused area of the screen (the center). 
* **Overall Applicability**: Essential for SaaS product homepages, creative portfolios, agency landing pages, and event registration sites.
* **Value Addition**: Transforms a standard document flow into an immersive, app-like visual experience. It grounds the UI and provides a strong anchor point before the user begins scrolling.
* **Browser Compatibility**: Extremely high. Standard CSS Flexbox and background properties are supported across all modern browsers and have been for years (IE11+).

### 2. Visual & Technical Breakdown

* **Step A: Core Visual Elements**
  - **HTML Structure**: A parent `.hero` container wrapping a `.content` container, which holds an `<h1>` (Title), `<p>` (Subtitle/Body), and `<a>` (Button).
  - **Color Logic**: High contrast text (White `#ffffff`) set against a dark or visually rich background image. The CTA button uses a distinct, highly visible accent color (Primary Blue `#007bff`) that darkens on hover (`#0056b3`).
  - **Typographic Hierarchy**:
    - **Base**: `sans-serif` (clean, modern).
    - **Title**: Massive (`65px`), drawing the eye first.
    - **Subtitle**: Medium (`22px`), providing context.
    - **Button**: Standard (`18px`), matching interactive expectations.

* **Step B: Layout & Compositional Style**
  - **Layout System**: Pure CSS Flexbox on the parent container.
    - `display: flex;`
    - `align-items: center;` (Vertical centering)
    - `justify-content: center;` (Horizontal centering)
  - **Spatial Feel**: Expansive and balanced. The use of `min-height: 100vh` ensures the element fills the browser window regardless of the content's actual height.
  - **Spacing**: Margins push elements down the central axis cleanly (`margin-bottom: 20px` on Title, `margin-bottom: 30px` on Subtitle).

* **Step C: Interactive Behavior & Animations**
  - **Hover Effects**: The CTA button transitions its background color when hovered.
  - **Transition**: Smooth fading interaction via `transition: 0.3s ease` on the button, preventing jarring color swaps.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| Full-viewport sizing | CSS `min-height: 100vh` | Native viewport units guarantee the block touches the bottom of the screen regardless of device resolution. |
| Background Image Scaling | CSS `background-size: cover` | Ensures the image fills the container completely without distorting its aspect ratio. |
| Centering Content | CSS Flexbox | `align-items` and `justify-content` provide the most robust, non-hacky way to center content in both dimensions. |
| Contrast & Legibility | CSS `linear-gradient` | *(Added for robustness)* Applying a subtle dark overlay over the image ensures the white text remains readable regardless of the image passed. |

> **Feasibility Assessment**: 100%. This is a fundamental, native CSS/HTML layout pattern that does not require JavaScript or external dependencies.

#### 3b. Complete Reproduction Code

```python
def create_component(
    output_dir: str,
    title_text: str = "Welcome to Our Website",
    body_text: str = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt.",
    button_text: str = "Get Started",
    color_scheme: str = "dark",        
    accent_color: str = "#007bff",     
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Full-Screen Immersive Flexbox Hero.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Allow custom background image, default to a high-quality mountain landscape from Unsplash
    bg_image_url = kwargs.get(
        "bg_image_url", 
        "https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?auto=format&fit=crop&w=1920&q=80"
    )

    # Ensure contrast on hover
    # (A simple way to darken the accent color via CSS filters or hardcoded value. 
    # Using a CSS variable with brightness filter for universal applicability).
    
    # === CSS ===
    css = f"""/* Full-Screen Immersive Flexbox Hero — generated component */
* {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
}}

:root {{
    --accent: {accent_color};
    --text-primary: #ffffff;
    --hero-width: {width_px}px;
    --hero-height: {height_px}px;
}}

body {{
    /* Default body behavior to center the component for viewing purposes */
    background: #f4f4f4;
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 100vh;
}}

.hero-wrapper {{
    /* Wrapper added to respect the requested width/height constraint for isolated viewing */
    width: 100%;
    max-width: var(--hero-width);
    height: var(--hero-height);
    position: relative;
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
    overflow: hidden;
}}

.hero {{
    width: 100%;
    height: 100%;
    min-height: 100%; /* Adapting 100vh logic to fit inside the requested dimensions */
    /* Add a subtle gradient overlay to ensure text contrast regardless of the image */
    background-image: linear-gradient(rgba(0, 0, 0, 0.3), rgba(0, 0, 0, 0.4)), url("{bg_image_url}");
    background-position: center;
    background-repeat: no-repeat;
    background-size: cover;
    display: flex;
    justify-content: center;
    align-items: center;
}}

.content {{
    text-align: center;
    color: var(--text-primary);
    padding: 0 20px;
    max-width: 900px;
}}

.content h1 {{
    font-size: clamp(40px, 5vw, 65px); /* Responsive typography adaptation */
    margin-bottom: 20px;
    letter-spacing: -0.02em;
    font-weight: 700;
}}

.content p {{
    font-size: clamp(16px, 2vw, 22px);
    margin-bottom: 30px;
    font-weight: 300;
    line-height: 1.5;
    text-shadow: 0 2px 4px rgba(0,0,0,0.5); /* extra legibility boost */
}}

.content .btn {{
    display: inline-block;
    font-size: 18px;
    font-weight: 500;
    padding: 12px 28px;
    background-color: var(--accent);
    color: var(--text-primary);
    border-radius: 5px;
    text-decoration: none;
    transition: all 0.3s ease;
    border: 2px solid transparent;
}}

.content .btn:hover {{
    filter: brightness(0.85); /* Dynamically darkens any passed accent color */
    transform: translateY(-2px);
    box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2);
}}

/* Responsive fallback */
@media (max-width: 768px) {{
    .hero-wrapper {{
        height: 100vh;
        border-radius: 0;
    }}
}}
"""

    # === HTML ===
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hero Section HTML CSS</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;500;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>

    <!-- Wrapper is added to respect requested width/height boundaries in this isolated environment -->
    <div class="hero-wrapper">
        <div class="hero">
            <div class="content">
                <h1>{title_text}</h1>
                <p>{body_text}</p>
                <a href="#" class="btn">{button_text}</a>
            </div>
        </div>
    </div>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Hero Section interaction logic
document.addEventListener('DOMContentLoaded', () => {{
    // The core layout is completely handled by CSS.
    // Future enhancements like parallax scrolling or typed text effects could be added here.
    const btn = document.querySelector('.btn');
    
    btn.addEventListener('click', (e) => {{
        e.preventDefault();
        console.log('Call to action triggered!');
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

* **Accessibility**: 
  - **Contrast Ratio**: Placing white text directly over unpredictable background images can fail WCAG accessibility standards. To mitigate this, the reproduction code adds a subtle dark `linear-gradient` overlay directly onto the `background-image` stack. Additionally, a slight `text-shadow` was added to the paragraph for extra legibility.
  - **A11y Tags**: Ensure the link (`<a href="#" class="btn">`) has discernible purpose. In production, this should route appropriately.
* **Performance**: 
  - Utilizing `background-size: cover` forces the browser to calculate the image spread, which is heavily optimized. However, relying on massive uncompressed images can impact Largest Contentful Paint (LCP). It's always advised to serve web-optimized (WebP/AVIF) formats for the background resource.
  - Animations are strictly bound to `transform` and `filter` / `background-color` (opacity/compositing), which are cheap for the browser GPU to compute.