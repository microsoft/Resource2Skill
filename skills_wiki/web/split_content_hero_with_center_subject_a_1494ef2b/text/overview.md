### 1. High-level Design Pattern Extraction

> **Skill Name**: Split-Content Hero with Center Subject Anchor

* **Core Visual Mechanism**: This pattern utilizes a centralized flexbox layout with intentionally displaced child elements. Two text containers (intro text and quotes) are horizontally centered using flexbox, but then pushed apart using `position: relative` and `left`/`right` properties. This creates a framed negative space perfectly in the center, allowing a background image (typically a portrait or product) to act as the central visual anchor without overlapping the text.
* **Why Use This Skill (Rationale)**: Manually displacing flex items provides a way to maintain vertical alignment while wrapping content around a central focal point. It immediately draws the user's eye to the center (the subject) while balancing textual information on either side, creating a classic, highly symmetrical editorial layout.
* **Overall Applicability**: Perfect for personal portfolios (with a portrait in the center), product landing pages (with the product in the center), and editorial hero sections where narrative text and testimonials need to be presented alongside a strong visual subject.
* **Value Addition**: Compared to a standard split-screen (50/50) layout, this 3-column "implied" layout creates much stronger symmetry and visual depth. By layering the background behind the displaced text, it integrates the imagery deeply into the typography.
* **Browser Compatibility**: Fully supported across all modern browsers. Relies on fundamental CSS features (Flexbox, `position: relative`, `background-image`).

### 2. Visual & Technical Breakdown

* **Step A: Core Visual Elements**
  - **Containers**: A full-width/height `<main>` wrapper acting as the hero, containing two `<div>` blocks (`.main-intro` and `.main-quotes`).
  - **Color Logic**: A deep navy background (`#1A253A`) paired with a vibrant magenta/pink accent (`#c13584`). Text is pure white (`#ffffff`) for high contrast.
  - **Typography**: Uses a sans-serif font (Roboto/Inter). The `<h1>` is massive (96px) and uppercase, serving as graphic art as much as text. Body text is legible at 18px.
  - **Graphic Flourishes**: A subtle repeating grid pattern overlaid with a solid center silhouette via multiple background images. Left-aligned borders on quotes using the accent color.

* **Step B: Layout & Compositional Style**
  - **Layout System**: `display: flex; justify-content: center; align-items: center;` creates the initial cluster.
  - **Displacement Strategy**: `.main-intro` uses `position: relative; right: 10vw;` and `.main-quotes` uses `position: relative; left: 10vw;`. This literally splits the flex cluster apart to make room for the central background image.
  - **Asymmetric Elements**: The second quote block is given a forced `margin-left` (e.g., 100px) to break the rigid grid and add dynamic editorial flow.

* **Step C: Interactive Behavior & Animations**
  - Primarily static layout based on CSS.
  - Button uses a simple background color transition on hover.
  - *Added for polish*: A very subtle mouse-move parallax effect on the background images to give life to the "center subject" concept.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **Center Anchoring + Text Wrapping** | CSS Flexbox + Relative Positioning | Accurately reproduces the tutorial's specific approach to pushing centered items apart (`left`/`right`). |
| **Center Portrait & Grid Pattern** | CSS Multi-Backgrounds with Inline SVG | Avoids external image dependencies while perfectly mimicking the layered visual texture and center subject from the tutorial. |
| **Responsive Typography** | CSS `clamp()` | Ensures the massive 96px header text gracefully scales down without breaking the layout bounds on smaller widths. |
| **Subtle Life / Polish** | JS `mousemove` event | Adds a light parallax effect to the background, enhancing the layered depth of the hero section. |

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
    Create a web component reproducing the 'Split-Content Hero with Center Subject' visual effect.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Derive theme colors to maintain contrast
    if color_scheme == "dark":
        bg_color = "#1A253A"
        text_color = "#FFFFFF"
        subtext_color = "rgba(255, 255, 255, 0.8)"
        pattern_color = "rgba(255, 255, 255, 0.05)"
        silhouette_color = "rgba(0, 0, 0, 0.4)"
        btn_text = "#FFFFFF"
    else:
        bg_color = "#F0F2F5"
        text_color = "#111827"
        subtext_color = "rgba(0, 0, 0, 0.7)"
        pattern_color = "rgba(0, 0, 0, 0.05)"
        silhouette_color = "rgba(0, 0, 0, 0.1)"
        btn_text = "#FFFFFF"

    # Inline SVGs for pure CSS background layers (using rgba to avoid URL hex encoding issues)
    svg_subject = f"<svg width='400' height='600' viewBox='0 0 400 600' xmlns='http://www.w3.org/2000/svg'><path d='M50 600 C50 400 150 350 200 350 C250 350 350 400 350 600 Z' fill='{silhouette_color}'/><circle cx='200' cy='250' r='80' fill='{silhouette_color}'/></svg>"
    svg_pattern = f"<svg width='40' height='40' xmlns='http://www.w3.org/2000/svg'><circle cx='20' cy='20' r='2' fill='{pattern_color}'/></svg>"

    css = f"""/* Split-Content Hero Styles */
:root {{
    --bg: {bg_color};
    --text: {text_color};
    --subtext: {subtext_color};
    --accent: {accent_color};
    --btn-text: {btn_text};
    --width: {width_px}px;
    --height: {height_px}px;
}}

* {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: 'Inter', system-ui, sans-serif;
    background-color: #000;
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
}}

/* Main Hero Container */
.hero {{
    position: relative;
    width: 100%;
    max-width: var(--width);
    height: var(--height);
    background-color: var(--bg);
    
    /* Layer 1: Center Subject, Layer 2: Repeating Grid */
    background-image: 
        url("data:image/svg+xml;utf8,{svg_subject}"),
        url("data:image/svg+xml;utf8,{svg_pattern}");
    background-size: min(70vh, 500px), 40px 40px;
    background-repeat: no-repeat, repeat;
    background-position: bottom center, center;
    
    /* Core Layout Technique */
    display: flex;
    justify-content: center;
    align-items: center;
    overflow: hidden;
    padding-bottom: 8vh; /* Lift content slightly */
}}

/* Left Column: Intro */
.main-intro {{
    position: relative;
    right: 12vw; /* Push away from center */
    width: 400px;
    z-index: 2;
}}

.main-intro h1 {{
    font-size: clamp(3rem, 5vw, 6rem); /* Scales down gracefully */
    line-height: 1.1;
    color: var(--text);
    font-weight: 800;
    text-transform: uppercase;
    margin-bottom: 20px;
}}

.main-intro p {{
    font-size: 1.125rem;
    line-height: 1.6;
    color: var(--subtext);
    margin-bottom: 30px;
}}

.btn {{
    display: inline-block;
    background-color: var(--accent);
    color: var(--btn-text);
    padding: 14px 28px;
    text-decoration: none;
    font-weight: 600;
    text-transform: uppercase;
    transition: filter 0.3s ease;
}}

.btn:hover {{
    filter: brightness(0.85);
}}

/* Right Column: Quotes */
.main-quotes {{
    position: relative;
    left: 8vw; /* Push away from center */
    width: 350px;
    z-index: 2;
}}

.quote-box {{
    border-left: 4px solid var(--accent);
    padding-left: 20px;
    margin-bottom: 40px;
    font-size: 1.125rem;
    line-height: 1.6;
    color: var(--subtext);
}}

/* Offset the second quote for visual interest (as done in tutorial) */
.quote-box:nth-child(2) {{
    margin-left: 80px;
}}

/* Responsive Fallback for smaller iframes/screens */
@media (max-width: 900px) {{
    .hero {{
        flex-direction: column;
        justify-content: flex-start;
        padding-top: 10vh;
        background-position: bottom -100px center, center;
    }}
    .main-intro, .main-quotes {{
        right: 0;
        left: 0;
        width: 85%;
        margin-bottom: 40px;
    }}
    .main-quotes .quote-box:nth-child(2) {{
        margin-left: 20px;
    }}
}}
"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Split-Content Hero</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <main class="hero">
        
        <div class="main-intro">
            <h1>{title_text}</h1>
            <p>{body_text}</p>
            <a href="#" class="btn">My Work</a>
        </div>

        <div class="main-quotes">
            <p class="quote-box">
                "The more that you read, the more things you will know. The more that you learn, the more places you'll go."<br><br>- Dr. Seuss
            </p>
            <p class="quote-box">
                "For the best return on your money, pour your purse into your head."<br><br>- Benjamin Franklin
            </p>
        </div>

    </main>

    <script src="script.js"></script>
</body>
</html>"""

    js = """document.addEventListener('DOMContentLoaded', () => {
    const hero = document.querySelector('.hero');
    
    // Add subtle parallax to the background images on mouse move
    // This adds a modern touch while respecting the CSS layout
    hero.addEventListener('mousemove', (e) => {
        // Calculate offset based on mouse position relative to center
        const xOffset = (window.innerWidth / 2 - e.pageX) / 80;
        const yOffset = (window.innerHeight / 2 - e.pageY) / 80;
        
        // Apply parallax only to the subject (Layer 1), keep the pattern static (Layer 2)
        // Background positions: Layer 1 (bottom center), Layer 2 (center)
        hero.style.backgroundPosition = `calc(50% + ${xOffset}px) calc(100% + ${yOffset}px), center`;
    });
    
    // Reset position on mouse leave
    hero.addEventListener('mouseleave', () => {
        hero.style.backgroundPosition = `bottom center, center`;
    });
});"""

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
  - The color scheme variables are chosen to strictly adhere to WCAG contrast guidelines (especially the high contrast white on navy blue).
  - The layout avoids using float-based hacks, ensuring screen readers will correctly read the `.main-intro` block first, followed by the `.main-quotes` block, maintaining a logical DOM flow.
* **Performance**:
  - The background imagery uses **Inline SVGs** injected directly into the CSS via `data:image/svg+xml`. This results in zero HTTP requests for images and immediate rendering without layout shift.
  - The Javascript parallax effect is bound to `mousemove`. For a high-performance production environment, it is highly recommended to wrap this listener calculation in a `requestAnimationFrame` to ensure it only calculates offsets right before the browser repaints, preventing main-thread blocking or visual jank.