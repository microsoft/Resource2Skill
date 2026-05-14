# Skill Extraction: Flexbox Split-Hero Section with Layered Backgrounds

### 1. High-level Design Pattern Extraction

> **Skill Name**: Flexbox Split-Hero Section with Layered Backgrounds

* **Core Visual Mechanism**: This pattern establishes a full-screen entry section (hero) using layered `background-image` properties (a fixed center portrait sitting over a radial background gradient). The content is horizontally split around the center focal point using CSS Flexbox, framing the central image with strong, highly-contrasting typography and staggered asymmetrical text blocks.

* **Why Use This Skill (Rationale)**: Splitting the content creates a dramatic, balanced visual frame that immediately draws the eye to the central graphical element (the portrait). Asymmetrical styling (like the indented second quote block) breaks up rigid grid expectations, leading to a more dynamic and engaging compositional flow.

* **Overall Applicability**: Ideal for personal portfolios, prominent SaaS product landing pages, or event websites where a central subject or product image needs to be framed prominently by an introduction and supporting testimonials or value propositions.

* **Value Addition**: Compared to a standard stacked hero (text above image), this layout creates depth by sandwiching the visual focus (the background subject) behind the text elements but centered between them. 

* **Browser Compatibility**: Fully supported in all modern browsers. Uses standard CSS Flexbox, multiple background images, and pseudo-class selectors (`:nth-child`).

### 2. Visual & Technical Breakdown

* **Step A: Core Visual Elements**
  - **Layered Backgrounds**: Utilizes CSS multiple backgrounds. The foreground layer is a focal image anchored `bottom center`, and the background layer is a subtle `radial-gradient` that prevents the base from looking flat. 
  - **Color Logic**: A deep navy background (`#1A253A`) provides high contrast against crisp white text (`#ffffff`). A vivid magenta accent (`#c13584`) is used sparingly for the CTA button background and structural quote borders.
  - **Typography**: Heavily relies on *Roboto*. The main heading is massive (`~64px`/`4rem`), `900` weight, and uppercase. Body text uses relaxed line heights (`1.5` to `1.6`) to improve readability against dark backgrounds.

* **Step B: Layout & Compositional Style**
  - **Flexbox Centering**: The main container is a flex container (`display: flex; justify-content: center; align-items: center`). 
  - **Framing with Spacing**: A responsive `gap` (or manually applied opposite margins/relative positioning) pushes the left content block (intro) and right content block (quotes) to the edges of the central portrait.
  - **Staggered Asymmetry**: The second quote paragraph is indented using `margin-left` (e.g., `3rem`), creating a cascading visual staircase that breaks up the boxy layout.
  - **Vertical Shift**: The content columns are translated slightly upwards (`transform: translateY(-5%)` or `padding-bottom`) to optically balance with the bottom-anchored center portrait.

* **Step C: Interactive Behavior & Animations**
  - **Hover States**: The CTA button uses a simple, immediate transition (e.g., `filter: brightness(0.85)`) to indicate interactivity without distracting from the typography.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **Layout Framing** | CSS Flexbox + `gap` | Flexbox ensures perfect vertical centering, and a relative `gap` cleanly pushes the split text blocks apart to frame the background image without relying on fragile absolute positioning. |
| **Layered Depth** | Multiple `background-image`s | Native CSS feature allowing us to stack a focal image (portrait) on top of a base gradient, achieving the composite look efficiently. |
| **Staggered Quotes** | CSS `:nth-child()` | Provides the cascading indentation on the right column cleanly without modifying the HTML structure with extra classes. |
| **Typography** | Google Fonts API | Directly loads *Roboto* for exact reproduction of the distinct, bold sans-serif weight used in the source tutorial. |

#### 3b. Complete Reproduction Code

```python
def create_component(
    output_dir: str,
    title_text: str = "WELCOME<br>TO MY FIRST<br>WEBSITE",
    body_text: str = "Nam interdum felis at felis placerat, sed varius massa ultricies. Integer quis nisi non dolor scelerisque efficitur at sed turpis.",
    quote1_text: str = "\"The more that you read, the more things you will know. The more that you learn, the more places you'll go.\"<br><br>- Dr. Seuss",
    quote2_text: str = "\"For the best return on your money, pour your purse into your head.\"<br><br>- Benjamin Franklin",
    cta_text: str = "MY WORK",
    color_scheme: str = "dark",
    accent_color: str = "#c13584",
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Flexbox Split-Hero Section.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Derive theme colors
    if color_scheme == "dark":
        bg_color = "#1A253A"
        bg_alt = "#2A354A"
        text_main = "#ffffff"
        text_muted = "#e2e8f0"
    else:
        bg_color = "#f0f2f5"
        bg_alt = "#e4e6ea"
        text_main = "#1A253A"
        text_muted = "#4a5568"

    # We use a base64 encoded SVG portrait silhouette so the component functions entirely standalone
    # while still matching the layered background logic of the tutorial.
    svg_fill = bg_alt.replace("#", "%23")
    portrait_svg = f"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='400' height='400' viewBox='0 0 400 400'%3E%3Ccircle cx='200' cy='150' r='75' fill='{svg_fill}'/%3E%3Cpath d='M80,400 Q80,240 200,240 Q320,240 320,400' fill='{svg_fill}'/%3E%3C/svg%3E"

    css = f"""/* Flexbox Split-Hero Section */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --bg-alt: {bg_alt};
    --text-main: {text_main};
    --text-muted: {text_muted};
    --accent: {accent_color};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Roboto', sans-serif;
    background-color: #000; /* Outer page canvas */
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 100vh;
}}

.hero-viewport {{
    width: var(--width);
    height: var(--height);
    background-color: var(--bg);
    /* Layered Backgrounds: Portrait on top, Radial Gradient behind */
    background-image: 
        url("{portrait_svg}"),
        radial-gradient(circle at center, var(--bg-alt) 0%, var(--bg) 100%);
    background-size: min(500px, calc(var(--height) * 0.8)), cover;
    background-repeat: no-repeat, no-repeat;
    background-position: bottom center, center;
    
    position: relative;
    overflow: hidden;
    display: flex;
    justify-content: center;
    align-items: center;
    
    /* This gap pushes the columns outward, framing the central background portrait */
    gap: max(40px, calc(var(--width) * 0.18));
    padding: 0 4%;
}}

/* Left Column */
.main-intro {{
    position: relative;
    max-width: 380px;
    z-index: 10;
    /* Optical vertical balance over the portrait */
    transform: translateY(-8%);
}}

.main-intro h1 {{
    font-size: clamp(2.5rem, calc(var(--width) * 0.05), 4rem);
    line-height: 1.05;
    font-weight: 900;
    text-transform: uppercase;
    color: var(--text-main);
    margin-bottom: 1.5rem;
}}

.main-intro p {{
    font-size: 1.125rem;
    line-height: 1.6;
    color: var(--text-muted);
    margin-bottom: 2rem;
}}

.main-intro .cta-btn {{
    display: inline-block;
    background-color: var(--accent);
    color: #ffffff; /* fixed white to ensure CTA contrast */
    text-decoration: none;
    padding: 0.75rem 1.5rem;
    font-weight: 700;
    font-size: 0.9rem;
    text-transform: uppercase;
    transition: filter 0.2s ease;
}}

.main-intro .cta-btn:hover {{
    filter: brightness(0.85);
}}

/* Right Column */
.main-quotes {{
    position: relative;
    max-width: 320px;
    z-index: 10;
    transform: translateY(-8%);
}}

.main-quotes p {{
    font-size: 1rem;
    line-height: 1.6;
    color: var(--text-muted);
    border-left: 4px solid var(--accent);
    padding-left: 1.25rem;
    margin-bottom: 2.5rem;
}}

/* Staggered block effect */
.main-quotes p:nth-child(2) {{
    margin-left: 3.5rem;
    margin-bottom: 0;
}}
"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Flexbox Split-Hero Section</title>
    <!-- Google Fonts: Roboto -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;700;900&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="hero-viewport">
        <!-- Left content column -->
        <div class="main-intro">
            <h1>{title_text}</h1>
            <p>{body_text}</p>
            <a href="#" class="cta-btn">{cta_text}</a>
        </div>
        
        <!-- Right content column -->
        <div class="main-quotes">
            <p>{quote1_text}</p>
            <p>{quote2_text}</p>
        </div>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    js = """// No complex JavaScript required for this purely structural CSS flexbox pattern.
document.addEventListener('DOMContentLoaded', () => {
    console.log("Flexbox Split-Hero Initialized.");
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
  - Ensure the custom accent color (`#c13584`) applied to the CTA button against its white text passes the WCAG AA minimum 4.5:1 contrast ratio.
  - Heading hierarchy is maintained efficiently through the `<h1>` block without extraneous nested tags, which optimizes screen-reader traversal.
* **Performance**:
  - The design is highly performant, leaning exclusively on standard CSS features without Javascript-calculated layout repaints.
  - Loading the background silhouette as a base64 encoded inline-SVG data URI inherently minimizes HTTP requests, speeding up time to First Contentful Paint. External image calls are mitigated altogether here.