### 1. High-level Design Pattern Extraction

> **Skill Name**: Dual-Background Split Hero with Staggered Quotes

*   **Core Visual Mechanism**: This pattern relies on a **layered background strategy** paired with **outward-pushed typography**. It combines a repeating geometric background pattern with a large, center-bottom anchored subject image (like a portrait cutout). The content is placed in a central flex container, but the left text block and right quote block are explicitly pushed outward using relative positioning (`right: 20vh`, `left: 4vh`) to create a physical "gap" in the center where the background subject is revealed.
*   **Why Use This Skill (Rationale)**: Pushing content outward from the center creates a strong focal point. It integrates the background subject into the layout, making the person/product feel like it's standing *amongst* the text rather than just sitting behind it. The staggered margin on the right-side quotes adds an organic, editorial asymmetry that breaks the rigid grid feel.
*   **Overall Applicability**: Perfect for personal portfolios, agency hero sections, or product landing pages where a primary figure or item needs to take center stage, flanked by introductory copy and social proof/testimonials.
*   **Value Addition**: Transforms a standard left-aligned hero into an immersive 2.5D composition. The staggered quotes draw the eye diagonally, enhancing read flow and visual interest.
*   **Browser Compatibility**: Fully supported across all modern browsers. Relies on standard CSS Flexbox and multiple `background-image` declarations.

### 2. Visual & Technical Breakdown

*   **Step A: Core Visual Elements**
    *   **Color Logic**: High contrast. Dark, saturated background (`#1a253a`), stark white text (`#ffffff`), and a vibrant accent color (`#c13584` magenta) used for left-borders and call-to-action buttons.
    *   **Typography**: A heavy, brutalist approach for the heading (e.g., Roboto, 96px, font-weight 800, uppercase). Body text is readable and airy (18px, 30px line-height).
    *   **Layering**: Accomplished purely via `background-image: url(portrait.png), url(pattern.png);`. The first image (portrait) is rendered on top of the second image (pattern).

*   **Step B: Layout & Compositional Style**
    *   **Flex-Center Base**: The main wrapper uses `display: flex; justify-content: center; align-items: center;`.
    *   **Relative Displacement**: Instead of relying on margins to push things apart, `.main-intro` uses `position: relative; right: 10vw;` and `.main-quotes` uses `position: relative; left: 10vw;`. This literally offsets them from their centered flex position.
    *   **Staggered Accent**: The right column uses an `nth-child(2)` selector with `margin-left: 100px;` to push the second quote further right, creating a diagonal stepped effect.

*   **Step C: Interactive Behavior & Animations**
    *   **Hover States**: The CTA button uses a standard background brightness/color shift on hover to indicate clickability.
    *   **Static Depth**: While static, the sizing of the background subject (`background-size: 70vh`) ensures it scales dynamically with the browser window height, maintaining the composition's proportions.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
| :--- | :--- | :--- |
| **Layered Subject & Pattern** | Multiple CSS `background-image` | Cleanest way to stack a cutout subject over a repeating pattern without extra DOM elements or z-index wars. |
| **Outward Displacement** | Flexbox + `position: relative` | Faithfully reproduces the tutorial's specific technique of centering the flow and shifting elements to expose the center. |
| **Staggered Quotes** | CSS `:nth-child` | Allows targeted indentation of alternating paragraphs without requiring extra HTML classes. |
| **Missing Asset Fallback** | SVG Data URIs | Ensures the generated code is 100% self-contained and verifiable without relying on external image hosts. |

#### 3b. Complete Reproduction Code

```python
def create_component(
    output_dir: str,
    title_text: str = "WELCOME<br>TO MY FIRST<br>WEBSITE",
    body_text: str = "A deep dive into web design, extracting core visual patterns and building reusable components for the modern web.",
    quote_1: str = "\"The more that you read, the more things you will know. The more that you learn, the more places you'll go.\"",
    quote_1_author: str = "- Dr. Seuss",
    quote_2: str = "\"For the best return on your money, pour your purse into your head.\"",
    quote_2_author: str = "- Benjamin Franklin",
    color_scheme: str = "dark",
    accent_color: str = "#c13584",
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Dual-Background Split Hero effect.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os
    import urllib.parse

    os.makedirs(output_dir, exist_ok=True)

    # Theme definitions
    if color_scheme == "dark":
        bg_color = "#1a253a"
        text_color = "#ffffff"
        silhouette_color = "#212f4a" # Slightly lighter than bg
        pattern_color = "ffffff"
        pattern_opacity = "0.03"
    else:
        bg_color = "#f0f4f8"
        text_color = "#111827"
        silhouette_color = "#e2e8f0"
        pattern_color = "000000"
        pattern_opacity = "0.03"

    # URL encode SVG colors for data URIs
    sil_enc = urllib.parse.quote(silhouette_color)

    # Inline SVG for the geometric background pattern
    pattern_svg = f"data:image/svg+xml,%3Csvg width='40' height='40' viewBox='0 0 40 40' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='%23{pattern_color}' fill-opacity='{pattern_opacity}' fill-rule='evenodd'%3E%3Cpath d='M0 40L40 0H20L0 20M40 40V20L20 40'/%3E%3C/g%3E%3C/svg%3E"
    
    # Inline SVG acting as the generic cutout person/subject
    portrait_svg = f"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 400 600'%3E%3Cpath d='M50,600 C50,400 120,320 200,320 C280,320 350,400 350,600 Z' fill='{sil_enc}'/%3E%3Ccircle cx='200' cy='200' r='90' fill='{sil_enc}'/%3E%3C/svg%3E"

    css = f"""/* Dual-Background Split Hero */
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;800&display=swap');

*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg-color: {bg_color};
    --text-color: {text_color};
    --accent-color: {accent_color};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Roboto', sans-serif;
    background-color: var(--bg-color);
    color: var(--text-color);
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
}}

.hero-wrapper {{
    width: var(--width);
    height: var(--height);
    max-width: 100%;
    min-height: 600px;
    position: relative;
    overflow: hidden;
    
    /* Center the flex layout */
    display: flex;
    justify-content: center;
    align-items: center;
    
    /* Layered Backgrounds: Subject (Top), Pattern (Bottom) */
    background-color: var(--bg-color);
    background-image: url("{portrait_svg}"), url("{pattern_svg}");
    background-size: 75vh, 40px 40px;
    background-repeat: no-repeat, repeat;
    background-position: bottom center, center;
}}

/* Left Column: Intro */
.main-intro {{
    position: relative;
    right: 12vw; /* Push outward from center */
    max-width: 450px;
    z-index: 10;
}}

.main-intro h1 {{
    font-size: clamp(48px, 5.5vw, 96px);
    line-height: 1.1;
    font-weight: 800;
    text-transform: uppercase;
    margin-bottom: 20px;
}}

.main-intro p {{
    font-size: 18px;
    line-height: 1.6;
}}

.btn {{
    display: inline-block;
    background-color: var(--accent-color);
    color: #ffffff;
    padding: 12px 24px;
    text-decoration: none;
    font-weight: 800;
    text-transform: uppercase;
    margin-top: 30px;
    letter-spacing: 1px;
    transition: filter 0.2s ease;
}}

.btn:hover {{
    filter: brightness(0.85);
}}

/* Right Column: Quotes */
.main-quotes {{
    position: relative;
    left: 12vw; /* Push outward from center */
    max-width: 400px;
    z-index: 10;
}}

.main-quotes p {{
    border-left: 4px solid var(--accent-color);
    padding-left: 20px;
    margin-bottom: 40px;
    font-size: 16px;
    line-height: 1.8;
}}

/* Stagger the second quote */
.main-quotes p:nth-child(2) {{
    margin-left: 100px;
}}

/* Responsive Adjustments */
@media (max-width: 1100px) {{
    .hero-wrapper {{
        flex-direction: column;
        justify-content: center;
        background-position: bottom right -10vw, center;
        padding: 40px;
    }}
    
    .main-intro, .main-quotes {{
        position: static;
        max-width: 600px;
        width: 100%;
    }}
    
    .main-intro {{
        margin-bottom: 60px;
    }}
    
    .main-quotes p:nth-child(2) {{
        margin-left: 40px; /* Reduce stagger on smaller screens */
    }}
}}
"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hero Section Pattern</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <main class="hero-wrapper">
        
        <!-- Left Content -->
        <div class="main-intro">
            <h1>{title_text}</h1>
            <p>{body_text}</p>
            <a href="#" class="btn">My Work</a>
        </div>

        <!-- Right Content -->
        <div class="main-quotes">
            <p>{quote_1}<br><br>{quote_1_author}</p>
            <p>{quote_2}<br><br>{quote_2_author}</p>
        </div>

    </main>
    <script src="script.js"></script>
</body>
</html>"""

    js = """// No JavaScript required for the core visual layout and relative offset mechanics.
console.log("Hero layout loaded successfully.");
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

*   **Accessibility**: 
    *   The use of `<br><br>` inside the `<p>` tags for formatting the quote author is structurally poor HTML (though replicated here to match the tutorial's extraction). In a production environment, wrap the quote text in `<q>` or `<blockquote>` and the author in a `<cite>` tag or a separate nested `<span>` for proper screen reader parsing.
    *   Ensure the `accent_color` used for the button maintains a 4.5:1 contrast ratio against the white text (`#ffffff`).
*   **Performance**: 
    *   Using dual `background-image` declarations on a single element is highly performant and avoids creating unnecessary DOM nodes just for aesthetic layering. 
    *   The SVG data URIs mean this component triggers exactly zero external HTTP requests for images, making it instantly renderable.