# Agent_Skill_Distiller: Web Component Design & Pattern Extractor

### 1. High-level Design Pattern Extraction

> **Skill Name**: Asymmetrical Layered Hero Section

* **Core Visual Mechanism**: A full-viewport hero section characterized by an offset, asymmetrical two-column layout placed over a visually layered background. The design creates a dynamic central negative space (traditionally meant for a large portrait or product image). The primary focal point is heavily weighted typographic contrast, balanced by secondary staggered textual elements on the opposite side.
* **Why Use This Skill (Rationale)**: This layout breaks the traditional rigid "text left, image right" grid grid, creating an editorial, magazine-like spatial experience. The central negative space acts as a framing device, pulling the user's eye inward, while the staggered content encourages diagonal scanning across the entire viewport. 
* **Overall Applicability**: Ideal for personal portfolio homepages, agency landing pages, SaaS hero sections, or any prominent header space featuring a spokesperson, mascot, or central hero graphic.
* **Value Addition**: It elevates a basic header into a dimensional composition. By utilizing relative positioning offsets, it creates an illusion of elements floating independently across a deep background, significantly increasing visual engagement without relying on complex JavaScript animations.
* **Browser Compatibility**: Fully supported in all modern browsers. Relies entirely on standard CSS Flexbox, CSS Backgrounds, and CSS Selectors. The use of `color-mix()` for dynamic background glows is supported in browsers from ~2023 onward, degrading gracefully to a solid background in older versions.

### 2. Visual & Technical Breakdown

* **Step A: Core Visual Elements**
  - **Color Logic**: Utilizes a deep, authoritative background (e.g., `#1A253A`) contrasted with stark white text (`#FFFFFF`) to ensure maximum legibility. A high-contrast, energetic accent color (e.g., Magenta `#C13584`) is used sparingly but purposefully on interaction targets (buttons) and structural anchors (borders).
  - **Typographic Hierarchy**: Driven by a robust Sans-Serif (Roboto/Inter). 
    - The `<h1>` is massive (up to 96px / 6rem), uppercase, and bold to establish immediate hierarchy.
    - Paragraph text is kept highly legible at 18px with generous 30px line height to facilitate easy reading.
  - **Decorations**: Left-aligned 4px solid borders on the secondary text blocks act as visual anchors, tying the scattered text back into the overall design system.

* **Step B: Layout & Compositional Style**
  - **Layout System**: The macro-layout uses standard CSS Flexbox (`justify-content: center; align-items: center;`) to center content vertically and horizontally.
  - **Asymmetrical Offsets**: The micro-layout breaks the grid. The left column is pushed outward using `position: relative; right: 15%;`, and the right column is pushed outward using `position: relative; left: 5%;`. This manually crafts a central "void" for background elements to shine through.
  - **Staggered Flow**: The secondary quotes use `:nth-child(2)` with `margin-left: 100px;` to step outward, adding rhythm and structural interest to otherwise static text.

* **Step C: Interactive Behavior & Animations**
  - Interactions are intentionally subdued to maintain an editorial feel. The Call-to-Action button utilizes a simple brightness shift on hover. 
  - The layout scales relative to the viewport container, reflowing into a standard stacked column on smaller mobile devices to ensure readability isn't compromised.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| Macro Layout & Centering | CSS Flexbox | Provides effortless vertical/horizontal centering for the child columns. |
| Asymmetrical Void | CSS `position: relative` | Allows the flex items to render in flow, but shifts them outward visually to create the central framing space. |
| Staggered Quotes | CSS `:nth-child` & Margins | Natively offsets specific sibling elements without requiring extra wrapper `div`s. |
| Layered Background | Multiple CSS Backgrounds | Simulates the layered texture/portrait aesthetic from the tutorial entirely in CSS, ensuring the component is self-contained without needing external image assets. |

> **Feasibility Assessment**: 100% reproduction of the layout and styling logic. The specific custom images from the video (the portrait and exact background pattern PNG) are simulated using layered CSS linear and radial gradients to ensure the generated code works instantly and independently as a plug-and-play component.

#### 3b. Complete Reproduction Code

```python
def create_component(
    output_dir: str,
    title_text: str = "WELCOME TO MY FIRST WEBSITE",
    body_text: str = "Nam interdum felis at felis placerat, sed varius massa ultricies. Integer quis nisi non dolor scelerisque efficitur at sed turpis.",
    cta_text: str = "MY WORK",
    color_scheme: str = "dark",        
    accent_color: str = "#C13584",     
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Asymmetrical Layered Hero Section.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Base Text overrides mapping to tutorial defaults
    quote1_text = kwargs.get("quote1_text", '"The more that you read, the more things you will know. The more that you learn, the more places you\'ll go."<br><br>- Dr. Seuss')
    quote2_text = kwargs.get("quote2_text", '"For the best return on your money, pour your purse into your head."<br><br>- Benjamin Franklin')

    # Derive theme colors
    if color_scheme == "dark":
        bg_color = "#1A253A"
        text_color = "#FFFFFF"
        pattern_color = "rgba(255, 255, 255, 0.03)"
    else:
        bg_color = "#F0F4F8"
        text_color = "#1A253A"
        pattern_color = "rgba(0, 0, 0, 0.04)"

    css = f"""/* Asymmetrical Layered Hero Section */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --text: {text_color};
    --accent: {accent_color};
    --pattern: {pattern_color};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Roboto', 'Inter', system-ui, sans-serif;
    background-color: var(--bg);
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 100vh;
}}

/* Main Component Wrapper */
.hero-container {{
    width: var(--width);
    height: var(--height);
    max-width: 100%;
    position: relative;
    background-color: var(--bg);
    
    /* Simulate layered background image and central portrait glow */
    background-image: 
        radial-gradient(circle at bottom center, color-mix(in srgb, var(--accent) 15%, transparent) 0%, transparent 65%),
        linear-gradient(45deg, var(--pattern) 25%, transparent 25%, transparent 75%, var(--pattern) 75%, var(--pattern)),
        linear-gradient(45deg, var(--pattern) 25%, transparent 25%, transparent 75%, var(--pattern) 75%, var(--pattern));
    background-size: 100% 100%, 40px 40px, 40px 40px;
    background-position: bottom center, 0 0, 20px 20px;
    
    display: flex;
    justify-content: center;
    align-items: center;
    overflow: hidden;
    color: var(--text);
}}

/* Left Column: Introduction */
.hero-intro {{
    position: relative;
    right: 12%; /* Offset left to create central void */
    max-width: 420px;
    z-index: 10;
}}

.hero-intro h1 {{
    font-size: clamp(3rem, 6vw, 5.5rem);
    line-height: 1.1;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: -1px;
}}

.hero-intro p {{
    font-size: 1.125rem;
    line-height: 1.6;
    margin-top: 1.5rem;
    opacity: 0.9;
}}

.hero-cta {{
    display: inline-block;
    background-color: var(--accent);
    color: #ffffff;
    padding: 0.75rem 1.75rem;
    margin-top: 2rem;
    text-decoration: none;
    text-transform: uppercase;
    font-weight: 600;
    font-size: 0.875rem;
    letter-spacing: 0.5px;
    transition: filter 0.2s ease, transform 0.2s ease;
}}

.hero-cta:hover {{
    filter: brightness(1.15);
    transform: translateY(-2px);
}}

/* Right Column: Quotes & Supporting Info */
.hero-quotes {{
    position: relative;
    left: 8%; /* Offset right */
    max-width: 360px;
    z-index: 10;
}}

.hero-quotes p {{
    border-left: 4px solid var(--accent);
    padding-left: 1.25rem;
    margin-bottom: 2.5rem;
    font-size: 1rem;
    line-height: 1.6;
    opacity: 0.9;
}}

/* Staggered effect for the second quote */
.hero-quotes p:nth-child(2) {{
    margin-left: 4rem;
}}

/* Responsive Fallback */
@media (max-width: 960px) {{
    .hero-container {{
        flex-direction: column;
        justify-content: flex-start;
        padding-top: 4rem;
        padding-bottom: 4rem;
        height: auto;
        min-height: var(--height);
    }}
    
    .hero-intro, 
    .hero-quotes {{
        position: static;
        max-width: 600px;
        width: 90%;
        margin-bottom: 3rem;
    }}
    
    .hero-quotes p:nth-child(2) {{
        margin-left: 2rem;
    }}
}}
"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="hero-container">
        
        <div class="hero-intro">
            <h1>{title_text}</h1>
            <p>{body_text}</p>
            <a href="#" class="hero-cta">{cta_text}</a>
        </div>

        <div class="hero-quotes">
            <p>{quote1_text}</p>
            <p>{quote2_text}</p>
        </div>

    </div>
    <script src="script.js"></script>
</body>
</html>"""

    js = """// Asymmetrical Layered Hero Section
document.addEventListener('DOMContentLoaded', () => {
    // Layout operates entirely on CSS Flexbox and Relative Positioning.
    // No JS strictly required for layout logic.
    console.log("Hero component loaded successfully.");
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
  - The design features inherently high contrast ratios between the text and background, adhering comfortably to WCAG AA guidelines. 
  - The Call-to-Action button utilizes an `<a>` tag with adequate padding, making for a large, easily clickable hit area for both mouse and touch interfaces.
  - The structure uses standard semantic HTML tags (`<h1>`, `<p>`, `<a>`).
* **Performance**:
  - Exceedingly lightweight. It relies purely on the browser's CSS rendering engine without needing heavy JavaScript frameworks or layout recalculations.
  - Using CSS gradients (`radial-gradient`, `linear-gradient`) to simulate textures saves on HTTP requests and bandwidth compared to loading heavy `.png` or `.jpg` background assets.
  - The layout avoids expensive properties like `box-shadow` or `filter` over large areas, ensuring a perfectly smooth 60fps render.