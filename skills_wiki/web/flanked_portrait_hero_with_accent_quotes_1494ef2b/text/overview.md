### 1. High-level Design Pattern Extraction

> **Skill Name**: Flanked Portrait Hero with Accent Quotes

* **Core Visual Mechanism**: A symmetrical, split-layout hero section built around a central, masked focal image (a portrait). The layout uses negative space and absolute positioning to float large, bold typography on the left and staggered, accent-bordered text blocks on the right. A subtle geometric pattern sits in the background to provide texture and depth without distracting from the content.
* **Why Use This Skill (Rationale)**: This layout breaks away from the standard "text on left, image on right" binary grid. By centering the subject and pulling the text to the extreme edges, it creates a "framing" effect that inherently draws the user's eye to the center, making it feel highly personal, confident, and editorial. The staggered quotes on the right provide visual counterbalance to the massive heading on the left.
* **Overall Applicability**: Ideal for personal portfolios, consulting sites, creative agency landing pages, or any scenario where personal branding (a founder, author, or creator) is the primary selling point.
* **Browser Compatibility**: Fully supported across all modern browsers. The component uses standard Flexbox for layout and standard CSS properties. The image masking uses `mask-image` which has broad support (often requiring the `-webkit-` prefix).

### 2. Visual & Technical Breakdown

* **Step A: Core Visual Elements**
  - **Colors**: Deep midnight blue background (`#1a253a`) which feels premium and tech-adjacent. Text is pure white (`#ffffff`). The accent color is a vibrant magenta (`#c13584`) used sparingly for high-contrast CTA buttons and typographic borders.
  - **Typography**: Uses a sans-serif stack (Roboto/Inter) with extreme contrast. The `h1` is massive (`~96px`), uppercase, and tightly leaded (`line-height: 1.1`). The body text is small (`18px`) and breathable (`line-height: 1.6`).
  - **Texture**: A subtle repeating radial-gradient pattern sits on the background container to add a low-opacity grid texture.

* **Step B: Layout & Compositional Style**
  - **Composition**: The container uses `display: flex` with `justify-content: space-between`. 
  - **Layering (Z-Index)**: The portrait is `position: absolute` in the dead center and anchored to the bottom. The text columns sit above the portrait layer (`z-index: 2`) so they can slightly overlap the image on medium screens.
  - **Staggered Rhythm**: The right-hand column features two quotes. The second quote utilizes a `margin-left` offset to create an asymmetrical, cascading visual rhythm that breaks up rigid grid lines.

* **Step C: Interactive Behavior & Animations**
  - Hover states on the CTA button darken the background via `filter: brightness(0.85)` and implement a slight upward transform for tactile feedback.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| Split-Edge Layout | CSS Flexbox | `justify-content: space-between` provides a robust way to frame the central image without hardcoding fragile `left`/`right` offsets. |
| Central Cutout Portrait | CSS `mask-image` + Absolute Positioning | Recreates the "transparent PNG" overlay effect from the tutorial using any standard un-cut rectangular photo via an arched mask. |
| Background Texture | CSS `radial-gradient` | Achieves the subtle repeating background pattern without requiring an external image asset. |
| Staggered Quotes | CSS `:nth-child()` | Accurately targets the second quote block to apply the layout shift, exactly as demonstrated in the tutorial. |

#### 3b. Complete Reproduction Code

```python
def create_component(
    output_dir: str,
    title_text: str = "WELCOME<br>TO MY FIRST<br>WEBSITE",
    body_text: str = "Nam interdum felis at felis placerat, sed varius massa ultricies. Integer quis nisi non dolor scelerisque efficitur at sed turpis.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#c13584",     # Authentic magenta from tutorial
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Flanked Portrait Hero layout.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Derive theme colors
    if color_scheme == "dark":
        bg_color = "#1a253a"  # Tutorial specific dark blue
        text_color = "#ffffff"
        pattern_color = "rgba(255, 255, 255, 0.04)"
    else:
        bg_color = "#f4f6f8"
        text_color = "#1a253a"
        pattern_color = "rgba(0, 0, 0, 0.05)"

    css = f"""/* Flanked Portrait Hero Component */
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
    background: #000; /* Outer canvas */
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 100vh;
}}

.hero-container {{
    position: relative;
    width: var(--width);
    height: var(--height);
    max-width: 100%;
    background-color: var(--bg);
    background-image: radial-gradient(circle at center, var(--pattern) 2px, transparent 2px);
    background-size: 24px 24px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0 6vw;
    overflow: hidden;
    color: var(--text);
}}

/* Central Masked Portrait */
.hero-portrait {{
    position: absolute;
    bottom: 0;
    left: 50%;
    transform: translateX(-50%);
    width: 38%;
    max-width: 450px;
    height: 85%;
    /* Using a placeholder portrait image */
    background-image: url('https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?auto=format&fit=crop&w=800&q=80');
    background-size: cover;
    background-position: top center;
    border-radius: 300px 300px 0 0;
    
    /* Fades out the bottom of the image into the background */
    -webkit-mask-image: linear-gradient(to bottom, black 70%, transparent 100%);
    mask-image: linear-gradient(to bottom, black 70%, transparent 100%);
    
    z-index: 1;
    filter: grayscale(15%) contrast(1.1);
}}

/* Left Column: Intro */
.hero-intro {{
    position: relative;
    z-index: 2;
    max-width: 380px;
    padding-bottom: 5vh; /* Slight upward shift */
}}

.hero-intro h1 {{
    font-size: clamp(2.5rem, 5.5vw, 5.5rem);
    line-height: 1.1;
    font-weight: 700;
    text-transform: uppercase;
    margin-bottom: 1.5rem;
    letter-spacing: -0.02em;
    text-shadow: 0 4px 20px rgba(0,0,0,0.3); /* Ensure legibility if overlapping image */
}}

.hero-intro p {{
    font-size: 1.1rem;
    line-height: 1.6;
    opacity: 0.9;
    margin-bottom: 2.5rem;
    text-shadow: 0 2px 10px rgba(0,0,0,0.4);
}}

.hero-cta {{
    display: inline-block;
    background-color: var(--accent);
    color: #ffffff; /* Hardcoded white for contrast on accent */
    text-decoration: none;
    padding: 0.8rem 2rem;
    font-size: 0.9rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    border-radius: 3px;
    transition: filter 0.2s ease, transform 0.2s ease;
}}

.hero-cta:hover {{
    filter: brightness(0.85);
    transform: translateY(-2px);
}}

/* Right Column: Quotes */
.hero-quotes {{
    position: relative;
    z-index: 2;
    max-width: 320px;
    padding-bottom: 5vh;
}}

.hero-quotes p {{
    border-left: 4px solid var(--accent);
    padding-left: 1.25rem;
    margin-bottom: 2.5rem;
    font-size: 0.95rem;
    line-height: 1.7;
    opacity: 0.9;
    text-shadow: 0 2px 10px rgba(0,0,0,0.4);
}}

/* Staggered Layout for second quote */
.hero-quotes p:nth-child(2) {{
    margin-left: 3.5rem;
}}

.quote-author {{
    display: block;
    margin-top: 1rem;
    font-style: italic;
    opacity: 0.8;
}}

/* Responsive Fallback */
@media (max-width: 900px) {{
    .hero-container {{
        flex-direction: column;
        justify-content: center;
        padding: 4rem 2rem;
        height: auto;
        min-height: var(--height);
    }}
    .hero-portrait {{
        opacity: 0.15;
        width: 80%;
        height: 60%;
        border-radius: 200px 200px 0 0;
    }}
    .hero-intro, .hero-quotes {{
        max-width: 100%;
        padding-bottom: 2rem;
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
    <title>Hero Component</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Roboto:ital,wght@0,400;0,600;0,700;1,400&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="hero-container">
        
        <!-- Central Image Layer -->
        <div class="hero-portrait"></div>
        
        <!-- Left Content -->
        <div class="hero-intro">
            <h1>{title_text}</h1>
            <p>{body_text}</p>
            <a href="#" class="hero-cta">MY WORK</a>
        </div>
        
        <!-- Right Content -->
        <div class="hero-quotes">
            <p>
                "The more that you read, the more things you will know. The more that you learn, the more places you'll go."
                <span class="quote-author">- Dr. Seuss</span>
            </p>
            <p>
                "For the best return on your money, pour your purse into your head."
                <span class="quote-author">- Benjamin Franklin</span>
            </p>
        </div>

    </div>
    <script src="script.js"></script>
</body>
</html>"""

    js = """// Interaction logic (empty by default for structural hero)
document.addEventListener('DOMContentLoaded', () => {
    console.log("Hero layout loaded and ready.");
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
  - Text overlaid on imagery utilizes a subtle `text-shadow` in the generated CSS. This ensures that even if the portrait heavily overlaps the text on mid-sized screens, the text retains sufficient contrast to meet WCAG AA standards.
  - The `<br>` tags within the `h1` format the text visually but maintain a unified semantic heading for screen readers.
* **Performance**: 
  - The pattern generation completely omits network payloads by leaning on CSS `radial-gradient` instead of loading a tiling PNG.
  - `mask-image` is fully hardware accelerated, generating smooth vector-like cuts out of the loaded portrait raster image without heavy DOM overhead.