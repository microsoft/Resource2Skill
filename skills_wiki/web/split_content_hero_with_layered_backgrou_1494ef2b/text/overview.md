### 1. High-level Design Pattern Extraction

> **Skill Name**: Split-Content Hero with Layered Backgrounds

* **Core Visual Mechanism**: A full-viewport hero layout utilizing a central vertical axis of symmetry created by a background subject, flanked by asymmetrical content blocks. It achieves depth by combining multiple CSS background images on a single container—layering a repeating geometric pattern underneath a large, centrally anchored subject image.
* **Why Use This Skill (Rationale)**: This layout solves the common problem of integrating a human subject (or product) into a hero section without sacrificing text legibility. By anchoring the subject to the bottom center of the background and pushing the typography to the left and right margins, you create a balanced, engaging composition that naturally guides the eye across the entire screen.
* **Overall Applicability**: Ideal for personal portfolios, agency landing pages, and product showcases where establishing a human connection or highlighting a central figure is key, while still needing substantial room for a primary headline and secondary descriptive text.
* **Value Addition**: Compared to a standard split-screen (50/50 text and image) layout, this technique feels more integrated and immersive. The subject appears to exist *within* the environment of the text rather than adjacent to it.
* **Browser Compatibility**: Fully supported in all modern browsers. CSS Multiple Backgrounds and Flexbox have been web standards for over a decade.

### 2. Visual & Technical Breakdown

* **Step A: Core Visual Elements**
  - **Layered Backgrounds**: Utilizes CSS `background-image` with multiple URLs (a pattern and a subject) combined with a solid fallback background color (`#1A253A`).
  - **Typography**: Heavily relies on contrast. The primary headline uses a bold, uppercase sans-serif font (Roboto, 96px, weight 600) with tight line-height to create a solid visual block. The secondary text uses a readable size (18px) with relaxed line-height (30px).
  - **Accents**: A single vivid accent color (e.g., magenta `#C13584`) is used sparingly but deliberately for the Call-To-Action background and a thick structural border on the quote block to anchor the right side.

* **Step B: Layout & Compositional Style**
  - **System**: Flexbox is used for the main horizontal alignment.
  - **Composition**: The layout uses a `space-between` alignment logic. The left block (Headline + CTA) carries high visual weight, which is balanced on the right by a taller, lighter block of quote text anchored by a left border.
  - **Background Scaling**: The background subject is typically sized using viewport units (e.g., `70vh`) and anchored `bottom center`, ensuring the subject remains grounded regardless of screen dimensions.

* **Step C: Interactive Behavior & Animations**
  - **Hover States**: The CTA button uses a simple transition to brighten on hover, providing immediate tactile feedback.
  - **Responsive Reflow**: While the tutorial manually pushed elements using `position: relative` (which is fragile), the extracted best practice uses a robust flexbox container that naturally adjusts spacing.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **Layout & Spacing** | CSS Flexbox | Provides robust `justify-content: space-between` logic, replacing the fragile manual pixel shifting from the tutorial. |
| **Layered Environment** | CSS Multiple Backgrounds | Allows combining a repeating geometric pattern and a central subject on a single HTML element effortlessly. |
| **Self-Contained Graphics** | SVG Data URIs | Ensures the background pattern and the central subject silhouette render immediately without relying on external image hosts. |
| **Typography** | Google Fonts CDN | Injects the exact 'Roboto' font family required to replicate the visual weight of the typography. |

#### 3b. Complete Reproduction Code

```python
def create_component(
    output_dir: str,
    title_text: str = "WELCOME\nTO MY FIRST\nWEBSITE",
    body_text: str = "Nam interdum felis at felis placerat, sed varius massa ultricies. Integer quis nisi non dolor scelerisque efficitur at sed turpis.",
    color_scheme: str = "dark",
    accent_color: str = "#C13584",
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Split-Content Layered Hero effect.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os
    import urllib.parse

    os.makedirs(output_dir, exist_ok=True)

    # Convert newlines in title to break tags for the massive headline effect
    formatted_title = title_text.replace('\n', '<br>')

    # Theme configuration
    if color_scheme == "dark":
        bg_color = "#1A253A"
        text_color = "#FFFFFF"
        pattern_fill = "rgba(255, 255, 255, 0.03)"
        subject_fill = "rgba(255, 255, 255, 0.05)"
        quote_text_color = "rgba(255, 255, 255, 0.85)"
    else:
        bg_color = "#F1F5F9"
        text_color = "#0F172A"
        pattern_fill = "rgba(0, 0, 0, 0.03)"
        subject_fill = "rgba(0, 0, 0, 0.05)"
        quote_text_color = "rgba(15, 23, 42, 0.85)"

    # SVG Data URIs for self-contained backgrounds
    pattern_svg = f"""<svg xmlns='http://www.w3.org/2000/svg' width='40' height='40'><rect width='40' height='40' fill='none'/><path d='M0 0h10v10H0zM20 20h10v10H20z' fill='{pattern_fill}'/></svg>"""
    pattern_data_uri = "data:image/svg+xml," + urllib.parse.quote(pattern_svg)

    # Minimalist abstract person silhouette
    subject_svg = f"""<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 200 200'><circle cx='100' cy='60' r='40' fill='{subject_fill}'/><path d='M30 200 Q 30 130 100 130 Q 170 130 170 200 Z' fill='{subject_fill}'/></svg>"""
    subject_data_uri = "data:image/svg+xml," + urllib.parse.quote(subject_svg)

    css = f"""/* Split-Content Hero - Generated Component */
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;600;700&display=swap');

*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg-color: {bg_color};
    --text-color: {text_color};
    --quote-color: {quote_text_color};
    --accent-color: {accent_color};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Roboto', sans-serif;
    background-color: #000;
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
}}

.hero-wrapper {{
    width: var(--width);
    height: var(--height);
    max-width: 100vw;
    background-color: var(--bg-color);
    /* The magic of multiple backgrounds: subject on top of pattern */
    background-image: 
        url("{subject_data_uri}"), 
        url("{pattern_data_uri}");
    background-size: 
        auto 85%, 
        40px 40px;
    background-repeat: 
        no-repeat, 
        repeat;
    background-position: 
        bottom center, 
        top left;
    position: relative;
    overflow: hidden;
    display: flex;
    align-items: center;
    justify-content: center;
}}

.hero-content {{
    width: 100%;
    max-width: 1400px;
    padding: 0 5%;
    display: flex;
    justify-content: space-between;
    align-items: center;
    z-index: 10;
}}

/* Left Column */
.hero-intro {{
    flex: 0 1 450px;
    color: var(--text-color);
}}

.hero-intro h1 {{
    font-size: clamp(3rem, 5vw, 5.5rem);
    line-height: 1.1;
    font-weight: 700;
    text-transform: uppercase;
    margin-bottom: 24px;
}}

.hero-intro p {{
    font-size: 1.125rem;
    line-height: 1.6;
    margin-bottom: 32px;
}}

.cta-button {{
    display: inline-block;
    background-color: var(--accent-color);
    color: #ffffff;
    text-decoration: none;
    padding: 14px 32px;
    font-size: 1rem;
    font-weight: 600;
    text-transform: uppercase;
    transition: filter 0.3s ease;
}}

.cta-button:hover {{
    filter: brightness(1.15);
}}

/* Right Column */
.hero-quotes {{
    flex: 0 1 350px;
    border-left: 4px solid var(--accent-color);
    padding-left: 24px;
    color: var(--text-color);
}}

.hero-quotes p {{
    font-size: 1.125rem;
    line-height: 1.6;
    color: var(--quote-color);
    margin-bottom: 24px;
}}

.hero-quotes p:last-child {{
    margin-bottom: 0;
}}

/* Responsive adjustments for component robustness */
@media (max-width: 900px) {{
    .hero-content {{
        flex-direction: column;
        justify-content: center;
        gap: 60px;
        text-align: center;
    }}
    .hero-quotes {{
        border-left: none;
        border-top: 4px solid var(--accent-color);
        padding-left: 0;
        padding-top: 24px;
    }}
}}
"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hero Section</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <main class="hero-wrapper">
        <div class="hero-content">
            
            <section class="hero-intro">
                <h1>{formatted_title}</h1>
                <p>{body_text}</p>
                <a href="#" class="cta-button">My Work</a>
            </section>

            <aside class="hero-quotes">
                <p>"The more that you read, the more things you will know. The more that you learn, the more places you'll go."<br><br>— Dr. Seuss</p>
                <p>"For the best return on your money, pour your purse into your head."<br><br>— Benjamin Franklin</p>
            </aside>

        </div>
    </main>
    <script src="script.js"></script>
</body>
</html>"""

    js = """// Split-Content Hero 
document.addEventListener('DOMContentLoaded', () => {
    // Layout logic is handled purely by Flexbox and CSS multiple-backgrounds.
    console.log("Hero section initialized.");
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
  - Structural HTML elements (`<main>`, `<section>`, `<aside>`) are utilized for logical document flow.
  - The contrast ratio on text defaults ensures compliance (pure white against deep dark blue easily passes WCAG AAA).
  - The CTA button uses standard anchoring but relies on CSS for appearance. To ensure keyboard navigability, standard focus outlines are implicitly retained from the browser reset.
* **Performance**: 
  - Using CSS `background-image` layering is highly performant.
  - SVG generation via Data URIs entirely eliminates the need for HTTP network requests for images, reducing Cumulative Layout Shift (CLS) to nearly zero.
  - No JavaScript layout calculation is required; CSS Flexbox naturally natively handles browser resizing.