### 1. High-level Design Pattern Extraction

> **Skill Name**: Asymmetric Dual-Column Hero with Layered Cutout

* **Core Visual Mechanism**: This pattern utilizes a layered composition where a central, bottom-aligned cutout subject (usually a portrait PNG or illustration) sits in front of a textured background, but *behind* the foreground text. The layout uses an asymmetric dual-column approach—a massive, bold introductory block on the left and a narrower, bordered secondary content block (like quotes or stats) on the right. This naturally frames the central subject, creating a striking "magazine cover" depth effect.

* **Why Use This Skill (Rationale)**: Positioning text blocks asymmetrically around a central visual anchor breaks the standard "text on left, image on right" grid. The use of CSS multiple backgrounds allows for seamless layering of the background texture and the central figure without adding extra HTML DOM elements. The strong left border on the secondary text block creates visual balance against the heavy typographic weight of the main headline.

* **Overall Applicability**: Ideal for personal portfolio hero sections, keynote speaker landing pages, product showcases (with the product in the center), and editorial-style article headers. 

* **Value Addition**: Transforms a flat banner into a dimensional scene. It directs the user's eye from the strong headline (top left) down to the central figure, and across to the secondary context (right), establishing a clear visual hierarchy.

* **Browser Compatibility**: Fully supported in all modern browsers. Uses standard Flexbox and CSS multiple backgrounds (`background-image: url(...), url(...)`).


### 2. Visual & Technical Breakdown

* **Step A: Core Visual Elements**
  - **Background Layering**: Handled natively via the `background` CSS property. The first image defined is the top layer (the portrait cutout), and the second is the bottom layer (the seamless texture).
  - **Color Logic**: Deep background (`#1A253A`) paired with bright white text (`#FFFFFF`) and a high-contrast accent color (`#c13584` magenta) applied to the Call-to-Action button and structural borders.
  - **Typography**: Heavily contrasting weights. The `H1` is massive (up to `96px`), solid (`600` weight), and uppercase. Secondary text is standard size (`18px`), creating intense typographic scale.
  - **Borders**: A solid `4px` left border on the quote container visually separates it from the central subject and anchors it to the right side of the screen.

* **Step B: Layout & Compositional Style**
  - **Container System**: A full-width/height flexbox container (`justify-content: space-between` or spaced center offsets) that pulls the intro to the mid-left and the quotes to the mid-right.
  - **Subject Placement**: The cutout image is anchored using `background-position: bottom center`. Using `vh` or `vmin` units for its `background-size` ensures it scales proportionally with the viewport height, preventing it from overwhelming the screen on wide monitors.

* **Step C: Interactive Behavior & Animations**
  - **Hover States**: The primary CTA uses a simple background color shift on hover, drawing immediate attention for interaction.
  - **Static Elegance**: The primary strength is compositional rather than animated, relying on bold negative space around the central visual.


### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **Layered Hero Visuals** | CSS Multiple Backgrounds | Allows combining a repeating texture and a bottom-aligned central subject directly on the container without extra HTML nodes. |
| **Cutout Subject** | Inline SVG Data URI | Ensures the component is 100% self-contained and reproducible without relying on external transparent PNG links that might break. |
| **Asymmetric Layout** | Flexbox (`space-between`) | Naturally pushes the intro block left and the quote block right, perfectly framing the central background subject. |
| **Typography** | Google Fonts (Inter) | Provides the clean, geometric starkness needed for the massive uppercase headlines shown in the tutorial. |

> **Feasibility Assessment**: 100% reproduction of the layout and styling logic. Instead of an external PNG portrait, a sleek, generic SVG silhouette is generated dynamically within the CSS to ensure the depth and layout effect works flawlessly out-of-the-box.

#### 3b. Complete Reproduction Code

```python
def create_component(
    output_dir: str,
    title_text: str = "WELCOME<br>TO MY FIRST<br>WEBSITE",
    body_text: str = "Nam interdum felis at felis placerat, sed varius massa ultricies. Integer quis nisi non dolor scelerisque efficitur at sed turpis.",
    color_scheme: str = "dark",
    accent_color: str = "#c13584",
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Asymmetric Dual-Column Hero.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Base themes
    if color_scheme == "dark":
        bg_color = "#1A253A"
        text_color = "#FFFFFF"
        pattern_color = "rgba(255, 255, 255, 0.03)"
        sil_fill = "rgba(255, 255, 255, 0.08)"
    else:
        bg_color = "#F0F4F8"
        text_color = "#1A253A"
        pattern_color = "rgba(0, 0, 0, 0.03)"
        sil_fill = "rgba(0, 0, 0, 0.1)"

    # Hover color derivation (slightly darker/shifted accent)
    # For simplicity in this demo, we'll use a CSS brightness filter on hover, 
    # but define the base variable here.
    
    # SVG Data URI for the central portrait silhouette
    svg_portrait = f"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 400 600'%3E%3Cpath fill='{sil_fill.replace(' ', '%20').replace(',','%2C')}' d='M200 120c-33 0-60 27-60 60s27 60 60 60 60-27 60-60-27-60-60-60zm-90 150c-33 0-60 27-60 60v270h300V330c0-33-27-60-60-60H110z'/%3E%3C/svg%3E"

    css = f"""/* Asymmetric Layered Hero */
:root {{
    --bg-color: {bg_color};
    --text-color: {text_color};
    --accent-color: {accent_color};
    --pattern-color: {pattern_color};
    --width: {width_px}px;
    --height: {height_px}px;
}}

* {{
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}}

body {{
    font-family: 'Inter', sans-serif;
    background-color: #000;
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
}}

/* The main hero container */
.hero-main {{
    width: 100%;
    max-width: var(--width);
    height: var(--height);
    background-color: var(--bg-color);
    
    /* Layer 1: Cutout Subject, Layer 2: Texture Pattern */
    background-image: 
        url("{svg_portrait}"),
        repeating-linear-gradient(45deg, var(--pattern-color) 25%, transparent 25%, transparent 75%, var(--pattern-color) 75%, var(--pattern-color)),
        repeating-linear-gradient(45deg, var(--pattern-color) 25%, transparent 25%, transparent 75%, var(--pattern-color) 75%, var(--pattern-color));
    
    background-position: 
        bottom center, 
        0 0, 
        20px 20px;
        
    background-size: 
        65vh, /* Subject size */
        40px 40px, /* Pattern sizing */
        40px 40px;
        
    background-repeat: 
        no-repeat, 
        repeat, 
        repeat;

    /* Flex layout to push left and right columns apart */
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0 8vw;
    position: relative;
    overflow: hidden;
}}

/* Left Column: Main Introduction */
.main-intro {{
    max-width: 450px;
    color: var(--text-color);
    z-index: 2; /* Ensure it stays above background layers */
}}

.main-intro h1 {{
    font-size: clamp(48px, 6vw, 84px);
    line-height: 1.05;
    font-weight: 800;
    text-transform: uppercase;
    margin-bottom: 24px;
    letter-spacing: -0.02em;
}}

.main-intro p {{
    font-size: 18px;
    line-height: 1.6;
    margin-bottom: 32px;
    opacity: 0.9;
}}

/* CTA Button */
.cta-btn {{
    display: inline-block;
    background-color: var(--accent-color);
    color: #FFF;
    text-decoration: none;
    padding: 16px 32px;
    font-weight: 700;
    text-transform: uppercase;
    font-size: 14px;
    letter-spacing: 0.05em;
    transition: filter 0.3s ease, transform 0.2s ease;
}}

.cta-btn:hover {{
    filter: brightness(1.15);
    transform: translateY(-2px);
}}

/* Right Column: Quotes / Secondary Context */
.main-quotes {{
    max-width: 320px;
    border-left: 4px solid var(--accent-color);
    padding-left: 24px;
    color: var(--text-color);
    z-index: 2;
}}

.main-quotes p {{
    font-size: 15px;
    line-height: 1.7;
    margin-bottom: 24px;
    opacity: 0.85;
    font-style: italic;
}}

.main-quotes p:last-child {{
    margin-bottom: 0;
}}

.quote-author {{
    display: block;
    margin-top: 12px;
    font-weight: 700;
    font-style: normal;
    color: var(--accent-color);
}}

/* Responsive behavior for smaller screens */
@media (max-width: 900px) {{
    .hero-main {{
        flex-direction: column;
        justify-content: center;
        text-align: center;
        background-position: bottom center, 0 0, 20px 20px;
        background-size: 80vw, 40px 40px, 40px 40px;
        padding: 40px 24px;
    }}

    .main-intro {{
        max-width: 100%;
        margin-bottom: 60vh; /* Leave gap for the central subject */
    }}

    .main-quotes {{
        max-width: 100%;
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
    <title>Hero Section Concept</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:ital,wght@0,400;0,700;0,800;1,400&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>

    <main class="hero-main">
        
        <!-- Left Side: Intro -->
        <section class="main-intro">
            <h1>{title_text}</h1>
            <p>{body_text}</p>
            <a href="#" class="cta-btn">My Work</a>
        </section>

        <!-- Right Side: Quotes -->
        <section class="main-quotes">
            <p>"The more that you read, the more things you will know. The more that you learn, the more places you'll go."
                <span class="quote-author">- Dr. Seuss</span>
            </p>
            <p>"For the best return on your money, pour your purse into your head."
                <span class="quote-author">- Benjamin Franklin</span>
            </p>
        </section>

    </main>

    <script src="script.js"></script>
</body>
</html>
"""

    js = """// Interactive behavior
document.addEventListener('DOMContentLoaded', () => {
    const btn = document.querySelector('.cta-btn');
    
    // Simple click ripple effect
    btn.addEventListener('mousedown', () => {
        btn.style.transform = 'scale(0.96)';
    });
    
    btn.addEventListener('mouseup', () => {
        btn.style.transform = 'translateY(-2px)';
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
  - The color contrast ratio between the white text (`#FFFFFF`) and dark background (`#1A253A`) is highly accessible, far exceeding WCAG AAA requirements.
  - The call to action uses standard `<a>` tags ensuring natural keyboard navigation and screen-reader flow.
  - Quotes are marked up structurally; in a production build, switching the `<p>` tags to `<blockquote>` and `<cite>` would improve semantic a11y.

* **Performance**:
  - The implementation entirely bypasses the need for external, heavy `.png` assets by using inline SVG code within the CSS background property. This results in instant rendering with zero network requests for the central image subject.
  - Generative CSS gradients are used instead of massive repeating tile images, keeping the file size incredibly lightweight and rendering extremely fast via GPU acceleration.