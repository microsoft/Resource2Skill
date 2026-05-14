### 1. High-level Design Pattern Extraction

> **Skill Name**: Split-Content Parallax Hero with Synchronized `vh` Scaling

* **Core Visual Mechanism**: This pattern centers around a dual-layer background where a central subject (a bottom-anchored portrait) is layered over a repeating texture using CSS multiple backgrounds (`background-image: url(portrait), radial-gradient(...)`). Text blocks flank the central subject and are pushed outward using `right` and `left` relative positioning properties based on viewport height (`vh`) units. 
* **Why Use This Skill (Rationale)**: 
  * **Synchronized Scaling**: By setting both the portrait's size (`background-size: auto 75vh`) and the horizontal spacing of the text (`right: 25vh`) using `vh` units, the text acts as a frame that perfectly tracks the physical size of the image across different widescreen aspect ratios. As the window gets shorter, the image gets smaller, and the text gap proportionally narrows.
  * **DOM Cleanliness**: Rendering the hero image and the texture inside a single element's `background` eliminates the need for complex absolute-positioned `<img>` tags and z-index wrangling.
* **Overall Applicability**: Ideal for personal portfolios, consulting sites, or product landing pages where a single human subject or focal product should anchor the page, flanked by high-contrast typography and testimonials/quotes.
* **Value Addition**: Transforms a standard grid layout into a dimensional, editorial composition that feels highly responsive to browser dimensions without requiring Javascript. 
* **Browser Compatibility**: Fully supported in all modern browsers. Uses fundamental Flexbox, CSS variables, and multiple background layers natively.

### 2. Visual & Technical Breakdown

* **Step A: Core Visual Elements**
  - **Layers**: 
    1. Background texture (e.g., repeating dot matrix or grid).
    2. Foreground portrait anchored `bottom center`.
    3. Foreground HTML content floated via Flexbox.
  - **Color Logic**: A high-contrast split. E.g., Dark theme: Background `#151821`, muted secondary text `#9ba3b5`, white primary text, with a stark vivid accent (e.g., Magenta `#c13584` or Cyan) used sparingly for borders and buttons.
  - **Typography**: Heavily contrasting hierarchy. An oversized, bold, uppercase `H1` (e.g., 96px) juxtaposed against airy `18px` body text and quotes.
  - **CSS Properties**: `background-image` (comma-separated), `background-size`, `position: relative`, `border-left`.

* **Step B: Layout & Compositional Style**
  - **Container System**: A full `100vh` flex container set to `justify-content: center` and `align-items: center`. 
  - **Viewport Shifts**: Instead of using standard `gap` or `margins`, the left introductory block and the right quote block exist naturally in the center but are repelled outward. The left element uses `position: relative; right: 20vh;`, and the right element uses `left: 15vh;`. 
  - **Asymmetry**: The design purposely shifts the left block slightly more and adds extra offset logic (e.g., padding bottoms) so it aligns naturally with the visual weight of the central image's shoulders/torso, creating an organic, non-rigid feel.

* **Step C: Interactive Behavior & Animations**
  - Pure CSS hover states on the CTA button using simple `filter: brightness()` or color swaps. 
  - The "animation" is primarily layout-driven: resizing the browser window causes the text to slide inward/outward perfectly in sync with the portrait shrinking/growing.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **Layered Subject & Texture** | CSS Multiple Backgrounds | Extremely clean DOM; allows positioning a raster/SVG subject perfectly over a procedural CSS pattern in a single rule. |
| **Viewport-Locked Framing** | `vh` units on `right/left` | Anchors the horizontal spacing of the text to the vertical height of the window, syncing it seamlessly with the portrait's `75vh` height. |
| **Quote Styling** | CSS `border-left` + `padding` | Native, lightweight semantic styling for blockquotes that scales seamlessly with content length. |
| **Portrait Asset** | Data URI SVG | Ensures the component is 100% reproducible and offline-compatible by embedding a procedural human silhouette. |

#### 3b. Complete Reproduction Code

```python
def create_component(
    output_dir: str,
    title_text: str = "WELCOME\nTO MY FIRST\nWEBSITE",
    body_text: str = "I build interactive, responsive, and visually appealing web experiences. Always learning and pushing the boundaries of what's possible on the web.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#c13584",     # Tutorial's magenta
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Split-Content Parallax Hero effect.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Process multiline text
    formatted_title = title_text.replace('\n', '<br>')

    # Theme definitions
    if color_scheme == "dark":
        bg_color = "#12141c"
        text_color = "#ffffff"
        text_muted = "#8b94a8"
        pattern_color = "rgba(255, 255, 255, 0.05)"
        svg_fill = "ffffff"
    else:
        bg_color = "#f0f2f5"
        text_color = "#12141c"
        text_muted = "#5d6578"
        pattern_color = "rgba(0, 0, 0, 0.05)"
        svg_fill = "000000"

    # Procedural SVG silhouette injected as a data URI to replace the external portrait asset
    svg_data = f"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 500 700'%3E%3Cdefs%3E%3ClinearGradient id='grad' x1='0%25' y1='0%25' x2='100%25' y2='100%25'%3E%3Cstop offset='0%25' stop-color='%23{svg_fill}' stop-opacity='0.15'/%3E%3Cstop offset='100%25' stop-color='%23{svg_fill}' stop-opacity='0.02'/%3E%3C/linearGradient%3E%3C/defs%3E%3Cpath d='M50,700 C50,500 150,420 250,420 C350,420 450,500 450,700 Z' fill='url(%23grad)'/%3E%3Ccircle cx='250' cy='280' r='110' fill='url(%23grad)'/%3E%3C/svg%3E"

    css = f"""/* Split-Content Parallax Hero */
@import url('https://fonts.googleapis.com/css2?family=Roboto:ital,wght@0,400;0,700;1,400&display=swap');

*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg-color: {bg_color};
    --text-primary: {text_color};
    --text-muted: {text_muted};
    --accent: {accent_color};
    --pattern: {pattern_color};
}}

body {{
    font-family: 'Roboto', sans-serif;
    background-color: var(--bg-color);
    color: var(--text-primary);
    width: {width_px}px;
    height: {height_px}px;
    /* In a real scenario, width/height would be 100vw/100vh */
    max-width: 100vw;
    min-height: 100vh;
    overflow-x: hidden;
}}

/* The core layout mechanism */
.hero-section {{
    position: relative;
    width: 100%;
    height: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
    
    /* Dual layered backgrounds: Subject + Texture */
    background-image: 
        url("{svg_data}"),
        radial-gradient(var(--pattern) 2px, transparent 2px);
    background-size: 
        auto 75vh, /* Subject anchors to viewport height */
        32px 32px; /* Texture repeats at fixed scale */
    background-position: 
        bottom center,
        0 0;
    background-repeat: 
        no-repeat,
        repeat;
}}

/* Left Block: Outward shift using vh */
.main-intro {{
    position: relative;
    right: 20vh; /* Pushes element left, scaling with window height */
    max-width: 400px;
    padding-bottom: 8vh;
    z-index: 10;
}}

.main-intro h1 {{
    font-size: clamp(48px, 6vw, 96px);
    line-height: 1.1;
    font-weight: 700;
    text-transform: uppercase;
    margin-bottom: 30px;
}}

.main-intro p {{
    font-size: 18px;
    line-height: 1.6;
    color: var(--text-muted);
    margin-bottom: 40px;
}}

.btn {{
    display: inline-block;
    padding: 16px 32px;
    background-color: var(--accent);
    color: #fff;
    text-decoration: none;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1px;
    transition: filter 0.2s ease;
}}

.btn:hover {{
    filter: brightness(0.85);
}}

/* Right Block: Outward shift using vh */
.main-quotes {{
    position: relative;
    left: 12vh; /* Pushes element right */
    display: flex;
    flex-direction: column;
    gap: 40px;
    max-width: 340px;
    padding-bottom: 8vh;
    z-index: 10;
}}

.quote-item {{
    border-left: 4px solid var(--accent);
    padding-left: 20px;
}}

.quote-item p {{
    font-size: 18px;
    line-height: 1.6;
    margin-bottom: 12px;
}}

.quote-item .author {{
    display: block;
    font-size: 14px;
    font-style: italic;
    color: var(--text-muted);
}}

/* Graceful degradation for narrow screens (Mobile/Tablet) */
@media (max-aspect-ratio: 4/5), (max-width: 900px) {{
    .hero-section {{
        flex-direction: column;
        justify-content: flex-start;
        align-items: flex-start;
        padding: 10vh 8vw;
        background-position: bottom right -10vw, center;
        background-size: auto 55vh, 32px 32px;
    }}
    
    .main-intro, .main-quotes {{
        right: 0;
        left: 0;
        max-width: 100%;
        padding-bottom: 0;
    }}
    
    .main-quotes {{
        margin-top: 60px;
        padding-bottom: 10vh;
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
    <main class="hero-section">
        
        <!-- Left Content -->
        <div class="main-intro">
            <h1>{formatted_title}</h1>
            <p>{body_text}</p>
            <a href="#" class="btn">My Work</a>
        </div>

        <!-- Right Content -->
        <div class="main-quotes">
            <div class="quote-item">
                <p>"The more that you read, the more things you will know. The more that you learn, the more places you'll go."</p>
                <span class="author">- Dr. Seuss</span>
            </div>
            <div class="quote-item">
                <p>"For the best return on your money, pour your purse into your head."</p>
                <span class="author">- Benjamin Franklin</span>
            </div>
        </div>

    </main>
    <script src="script.js"></script>
</body>
</html>"""

    js = """// No JavaScript required for this purely CSS/layout-driven pattern.
console.log('Hero section initialized perfectly.');
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
  * The implementation uses semantic markup (`<main>`, `<h1>`).
  * Contrast ratios are inherently handled by strictly defining both text and background colors simultaneously via the Python theme generation parameters. 
  * The large touch target size on the `.btn` ensures standard mobile ease-of-use.
* **Performance**: 
  * **Zero HTTP Requests for Assets**: By extracting the concept into a procedural CSS gradient for the texture and an inline SVG data URI for the portrait, this component renders instantly with 0 external network requests for images.
  * **Layout Performance**: Avoids heavy JavaScript DOM mutations for resizing logic. By leveraging viewport units (`vh`, `vw`), the browser’s native rendering engine natively handles dynamic repositioning and scaling efficiently at 60 FPS during window resizes.