# Split Flexbox Hero with Layered Background Portrait

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Split Flexbox Hero with Layered Background Portrait

* **Core Visual Mechanism**: This pattern utilizes a full-viewport split layout where a central "negative space" is intentionally created between two columns of text. This gap reveals a composite CSS background: a repeating geometric pattern covering the entire section, overlaid with a transparent foreground image (a portrait or product) anchored to the bottom center. The layered `background-image` property creates a faux-3D depth effect without requiring extra DOM elements.
* **Why Use This Skill (Rationale)**: By pushing the textual content (intro and secondary quotes) to the visual extremes (left and right), the design creates a natural focal point in the center. Anchoring a human face or product in this central background slot establishes immediate eye contact or product focus, while maintaining a clean, easily readable typographic hierarchy on the sides.
* **Overall Applicability**: Ideal for personal portfolios, SaaS landing page hero sections, or feature highlights where a human element or hero product needs to be showcased alongside substantial introductory copy and social proof (quotes/testimonials).
* **Value Addition**: It replaces a standard flat background with a dynamic, layered composition. By combining the foreground subject and background texture into the CSS `background-image` property, it keeps the HTML structure exceptionally clean and semantic, allowing Flexbox to easily handle the foreground text alignment.
* **Browser Compatibility**: Fully supported in all modern browsers. Relies on standard CSS Flexbox, Multiple Backgrounds, and `clamp()` for responsive typography.

### 2. Visual & Technical Breakdown

* **Step A: Core Visual Elements**
  - **Color Logic**: The tutorial utilizes a deep dark navy/slate background (`#1A253A`) paired with pure white text (`#ffffff`). The energetic focal point is driven by a vibrant magenta/pink accent color (`#c13584` with a hover state of `#9e2f6e`).
  - **Typography**: Heavy, uppercase headers (`font-size: 96px` scaled responsively, `font-weight: 600`) contrasted against highly legible paragraph text (`18px` with generous `30px` line-height). Font family is a clean sans-serif (Roboto/Inter).
  - **CSS Constructs**: Heavy reliance on CSS multiple backgrounds. The syntax `background-image: url(portrait.png), url(pattern.png);` is used, where the first image renders on top. `border-left` is used on secondary paragraphs to create stylized blockquotes.

* **Step B: Layout & Compositional Style**
  - **Layout System**: The main container is a Flexbox container (`display: flex; justify-content: space-between; align-items: center`).
  - **Spatial Feel**: High tension and wide margins. The left column contains the primary CTA, while the right column contains stacked blockquotes.
  - **Staggering**: The second quote on the right side uses an `nth-child(2)` selector to apply a `margin-left` (e.g., `100px`), breaking the rigid grid and adding a diagonal, asymmetric visual flow.

* **Step C: Interactive Behavior & Animations**
  - Hover transitions on the Call-to-Action button (color shift).
  - While the original tutorial relies strictly on static CSS layout, introducing a staggered intersection observer to fade the text blocks up upon loading elevates the premium feel of the split layout.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| Split Content Layout | CSS Flexbox | `justify-content: space-between` provides the exact wide-gap structure needed without hacky relative positioning. |
| Layered Portrait + Pattern | CSS Multiple Backgrounds | Allows layering a silhouette over a geometric pattern within a single CSS rule, keeping HTML clean. Inline SVGs are used as data URIs for robust portability. |
| Staggered Quotes | CSS Pseudo-selectors | `:nth-child(2)` allows the second quote to be pushed horizontally, recreating the tutorial's asymmetric visual flow. |
| Entrance Animation | Intersection Observer (JS) | Adds a smooth, staggered fade-up to the text elements as they enter the viewport, enhancing the rigid CSS layout. |

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
    Create a web component reproducing the 'Split Flexbox Hero with Layered Background Portrait' layout.
    
    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors and SVG fills ===
    if color_scheme == "dark":
        bg_color = "#1A253A"
        text_color = "#ffffff"
        svg_fill = "%23ffffff"
        pattern_opacity = "0.03"
        portrait_opacity = "0.08"
    else:
        bg_color = "#f4f7f6"
        text_color = "#111827"
        svg_fill = "%23000000"
        pattern_opacity = "0.04"
        portrait_opacity = "0.06"

    # SVG Data URIs to ensure self-contained rendering
    # 1. Silhouette portrait for foreground
    portrait_svg = f"data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 400 400'><path d='M200 220c-44.1 0-80-35.9-80-80s35.9-80 80-80 80 35.9 80 80-35.9 80-80 80zm-120 180v-40c0-66.3 53.7-120 120-120s120 53.7 120 120v40H80z' fill='{svg_fill}' fill-opacity='{portrait_opacity}'/></svg>"
    # 2. Geometric pattern for background
    pattern_svg = f"data:image/svg+xml;utf8,<svg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'><g fill='none' fill-rule='evenodd'><g fill='{svg_fill}' fill-opacity='{pattern_opacity}'><path d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/></g></g></svg>"

    # === CSS ===
    css = f"""/* Split Flexbox Hero */
:root {{
    --bg-color: {bg_color};
    --text-color: {text_color};
    --accent-color: {accent_color};
    --width: {width_px}px;
    --height: {height_px}px;
}}

* {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: 'Roboto', system-ui, sans-serif;
    background-color: #000; /* Outer canvas */
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
}}

.hero-container {{
    width: var(--width);
    height: var(--height);
    background-color: var(--bg-color);
    color: var(--text-color);
    position: relative;
    overflow: hidden;
    
    /* MULTIPLE BACKGROUNDS: Portrait on top of geometric pattern */
    background-image: 
        url("{portrait_svg}"), 
        url("{pattern_svg}");
    background-position: bottom center, center;
    background-size: 60%, auto;
    background-repeat: no-repeat, repeat;
    
    /* Layout */
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 40px 6vw;
}}

/* === Left Column: Intro === */
.main-intro {{
    position: relative;
    max-width: 420px;
    z-index: 2;
}}

.main-intro h1 {{
    font-size: clamp(2.5rem, 5vw, 4.5rem);
    line-height: 1.1;
    font-weight: 700;
    text-transform: uppercase;
    margin-bottom: 24px;
    letter-spacing: -1px;
}}

.main-intro p {{
    font-size: 18px;
    line-height: 30px;
    opacity: 0.9;
    margin-bottom: 36px;
}}

.btn-work {{
    display: inline-block;
    background-color: var(--accent-color);
    color: #ffffff;
    text-decoration: none;
    padding: 14px 32px;
    font-size: 16px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1px;
    transition: filter 0.2s ease, transform 0.2s ease;
}}

.btn-work:hover {{
    filter: brightness(0.85);
    transform: translateY(-2px);
}}

/* === Right Column: Quotes === */
.main-quotes {{
    position: relative;
    max-width: 380px;
    z-index: 2;
    display: flex;
    flex-direction: column;
    gap: 40px;
}}

.quote-block {{
    border-left: 4px solid var(--accent-color);
    padding-left: 20px;
}}

.quote-block p {{
    font-size: 16px;
    line-height: 28px;
    opacity: 0.85;
}}

/* The signature stagger effect from the tutorial */
.quote-block:nth-child(2) {{
    margin-left: 60px;
}}

/* Animation classes applied via JS */
.fade-up {{
    opacity: 0;
    transform: translateY(30px);
    transition: opacity 0.8s ease, transform 0.8s cubic-bezier(0.2, 0.8, 0.2, 1);
}}

.fade-up.visible {{
    opacity: 1;
    transform: translateY(0);
}}

/* Responsive adjustments */
@media (max-width: 900px) {{
    .hero-container {{
        flex-direction: column;
        justify-content: center;
        text-align: center;
        gap: 60px;
        background-size: 80%, auto;
        padding-top: 80px;
        padding-bottom: 80px;
        overflow-y: auto;
    }}

    .main-intro, .main-quotes {{
        max-width: 100%;
    }}

    .quote-block {{
        text-align: left;
        border-left: none;
        border-top: 4px solid var(--accent-color);
        padding-left: 0;
        padding-top: 16px;
    }}

    .quote-block:nth-child(2) {{
        margin-left: 0;
    }}
}}
"""

    # === HTML ===
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hero Section</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Roboto:ital,wght@0,400;0,600;0,700;1,400&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>

    <main class="hero-container">
        
        <!-- Left Side -->
        <div class="main-intro">
            <h1 class="fade-up">{title_text}</h1>
            <p class="fade-up">{body_text}</p>
            <a href="#" class="btn-work fade-up">My Work</a>
        </div>

        <!-- Right Side -->
        <div class="main-quotes">
            <div class="quote-block fade-up">
                <p>"The more that you read, the more<br>things you will know. The more that<br>you learn, the more places you'll go."<br><br>- Dr. Seuss</p>
            </div>
            
            <div class="quote-block fade-up">
                <p>"For the best return on your<br>money, pour your purse<br>into your head."<br><br>- Benjamin Franklin</p>
            </div>
        </div>

    </main>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Staggered entrance animation logic
document.addEventListener('DOMContentLoaded', () => {{
    const observerOptions = {{
        root: null,
        rootMargin: '0px',
        threshold: 0.1
    }};

    const observer = new IntersectionObserver((entries, observer) => {{
        entries.forEach(entry => {{
            if (entry.isIntersecting) {{
                // Determine stagger delay based on DOM order
                const elements = Array.from(document.querySelectorAll('.fade-up'));
                const index = elements.indexOf(entry.target);
                
                // Apply a slight delay to each subsequent element
                entry.target.style.transitionDelay = `${{index * 0.15}}s`;
                entry.target.classList.add('visible');
                
                // Stop observing once animated
                observer.unobserve(entry.target);
            }}
        }});
    }}, observerOptions);

    const animatedElements = document.querySelectorAll('.fade-up');
    animatedElements.forEach(el => observer.observe(el));
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