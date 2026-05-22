# Agent_Skill_Distiller: Split-Layout Hero Section

### 1. High-level Design Pattern Extraction

> **Skill Name**: Split-Layout Hero with Layered Portrait

* **Core Visual Mechanism**: A full-viewport hero section characterized by a central "cut-out" subject (portrait) flanked by deeply split typography. It uses multiple background layers (`background-image` with comma separation) to stack a subject image over a textured background. The content layout uses high-contrast, oversized typography pushed to the extreme left and right, framing the central subject.

* **Why Use This Skill (Rationale)**: This layout breaks the standard "text on left, image on right" hero convention. By placing the subject centrally and floating text around them, it creates a more magazine-like, editorial aesthetic. The deep space in the center draws the eye immediately to the subject, while the flanking text serves as framing context.

* **Overall Applicability**: Ideal for personal portfolios, agency sites, or character-driven landing pages where the personal brand or a specific subject/product needs to be the absolute focal point.

* **Value Addition**: Transforms a standard landing page into a highly personalized, immersive introduction. The structural framing forces users to scan the subject first, then the primary value proposition (H1), and finally secondary credibility markers (quotes/testimonials).

* **Browser Compatibility**: Fully supported in all modern browsers. Relies on standard Flexbox and multiple background images.


### 2. Visual & Technical Breakdown

* **Step A: Core Visual Elements**
  - **Background Layers**: Utilizes the CSS `background-image` property to accept multiple values: a foreground subject and a background texture/gradient.
  - **Color Logic**:
    - Dark mode background: Deep navy `#1a253a`.
    - Accent colors: Magenta `#c13584` and dark pink `#9e2f6e` for borders and hover states.
    - Text: Pure white `#ffffff`.
  - **Typography**: Roboto font family. Extremely large, bold, uppercase `h1` (`96px`, `600` weight) with tight line-height (`106px`) to create solid text blocks. Paragraphs are legible at `18px` with generous `30px` line-heights.

* **Step B: Layout & Compositional Style**
  - **Layout System**: CSS Flexbox on the main container (`display: flex`, `justify-content: center`, `align-items: center`).
  - **Framing**: Content is split into two `div` blocks. In the tutorial, these are pushed outward using `position: relative` and `left`/`right` offsets using `vh` units. (A more robust, modern approach used in the reproduction relies on Flexbox `gap` and `max-width` to achieve the exact same wide-split visual framing).
  - **Asymmetry**: The right side features blockquotes where the second quote is indented (`margin-left: 100px`) to break rigid grid lines and add visual interest.

* **Step C: Interactive Behavior & Animations**
  - **Call to Action (CTA)**: The CTA button is treated as an inline block with solid background color, utilizing a distinct accent color hover state to encourage interaction.
  - **Static Grandeur**: The primary impact relies on static composition and scale rather than complex animation.


### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| Split Content Framing | CSS Flexbox & `gap` | Provides a cleaner, inherently responsive way to split content around a center point compared to relative positioning offsets. |
| Layered Portrait | CSS Multiple Backgrounds | Replicates the tutorial's exact technique of layering a transparent PNG/SVG subject over a base texture using a single CSS property. |
| Typographic Scale | CSS explicit pixel values & `rem` | Ensures the massive impact of the `96px` header is maintained on desktop, while scaling down gracefully on smaller screens. |
| Quotes Layout | CSS `nth-child` & Margins | Precisely recreates the staggered, left-bordered blockquote design from the right column. |

> **Feasibility Assessment**: 100%. The visual layout, layered backgrounds, and staggered blockquote typography are fully reproduced. A transparent SVG avatar placeholder is used to mimic the tutorial's cut-out portrait photograph.

#### 3b. Complete Reproduction Code

```python
def create_component(
    output_dir: str,
    title_text: str = "WELCOME TO MY FIRST WEBSITE",
    body_text: str = "Nam interdum felis at felis placerat, sed varius massa ultricies. Integer quis nisi non dolor scelerisque efficitur at sed turpis.",
    color_scheme: str = "dark",
    accent_color: str = "#c13584",
    width_px: int = 1440,
    height_px: int = 900,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Split-Layout Hero Section.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Derived colors
    bg_base = "#1a253a" if color_scheme == "dark" else "#e0e5ec"
    text_main = "#ffffff" if color_scheme == "dark" else "#111111"
    text_muted = "rgba(255, 255, 255, 0.85)" if color_scheme == "dark" else "rgba(0, 0, 0, 0.75)"
    btn_bg = "#9e2f6e"
    btn_hover = "#6b1f4a"

    # SVG Avatar acting as the cut-out portrait
    portrait_url = "https://api.dicebear.com/7.x/open-peeps/svg?seed=Felix&backgroundColor=transparent&pose=standing"

    css = f"""/* Split-Layout Hero Section */
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;600;700&display=swap');

:root {{
    --bg-base: {bg_base};
    --text-main: {text_main};
    --text-muted: {text_muted};
    --accent: {accent_color};
    --btn-bg: {btn_bg};
    --btn-hover: {btn_hover};
    --width: {width_px}px;
    --height: {height_px}px;
}}

*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: 'Roboto', sans-serif;
    background-color: #000;
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
}}

.hero-container {{
    width: 100%;
    max-width: var(--width);
    height: var(--height);
    background-color: var(--bg-base);
    
    /* Layered Backgrounds: Portrait over a radial pattern */
    background-image: 
        url('{portrait_url}'),
        radial-gradient(circle at center, rgba(255,255,255,0.05) 0%, rgba(0,0,0,0.2) 100%);
    background-size: 
        auto 85%, /* Portrait height */
        cover;    /* Pattern covers everything */
    background-position: 
        bottom center, 
        center;
    background-repeat: no-repeat;
    
    position: relative;
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0 6vw;
    overflow: hidden;
}}

/* Left Column: Intro */
.main-intro {{
    max-width: 500px;
    z-index: 10;
    padding-bottom: 8vh;
}}

.main-intro h1 {{
    font-size: clamp(48px, 6vw, 96px);
    line-height: 1.1;
    font-weight: 700;
    text-transform: uppercase;
    color: var(--text-main);
    margin-bottom: 30px;
}}

.main-intro p {{
    font-size: 18px;
    line-height: 30px;
    color: var(--text-muted);
    margin-bottom: 40px;
}}

.btn-work {{
    display: inline-block;
    background-color: var(--btn-bg);
    color: #fff;
    text-decoration: none;
    padding: 12px 24px;
    font-weight: 600;
    text-transform: uppercase;
    font-size: 14px;
    letter-spacing: 1px;
    transition: background-color 0.2s ease;
}}

.btn-work:hover {{
    background-color: var(--btn-hover);
}}

/* Right Column: Quotes */
.main-quotes {{
    max-width: 450px;
    z-index: 10;
    display: flex;
    flex-direction: column;
    gap: 40px;
}}

.quote-block {{
    border-left: 4px solid var(--accent);
    padding-left: 20px;
}}

.quote-block:nth-child(2) {{
    margin-left: 80px; /* Staggered offset mimicking the tutorial */
}}

.quote-text {{
    font-size: 16px;
    line-height: 28px;
    color: var(--text-muted);
    font-style: italic;
    margin-bottom: 15px;
}}

.quote-author {{
    font-size: 14px;
    font-weight: 600;
    color: var(--text-main);
}}

/* Responsive Adjustments */
@media (max-width: 1024px) {{
    .hero-container {{
        flex-direction: column;
        justify-content: center;
        gap: 60px;
        background-position: bottom right -20%, center;
        background-size: auto 60%, cover;
        padding: 40px 5vw;
        align-items: flex-start;
    }}
    .main-intro, .main-quotes {{
        max-width: 100%;
        background: rgba(26, 37, 58, 0.7); /* ensure readable text over image */
        padding: 20px;
        border-radius: 8px;
        backdrop-filter: blur(4px);
    }}
    .quote-block:nth-child(2) {{
        margin-left: 20px;
    }}
}}
"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text}</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="hero-container">
        
        <!-- Left Side: Main Introduction -->
        <div class="main-intro">
            <h1>{title_text}</h1>
            <p>{body_text}</p>
            <a href="#" class="btn-work">My Work</a>
        </div>

        <!-- Right Side: Secondary Quotes -->
        <div class="main-quotes">
            <div class="quote-block">
                <p class="quote-text">"The more that you read, the more things you will know. The more that you learn, the more places you'll go."</p>
                <p class="quote-author">- Dr. Seuss</p>
            </div>
            <div class="quote-block">
                <p class="quote-text">"For the best return on your money, pour your purse into your head."</p>
                <p class="quote-author">- Benjamin Franklin</p>
            </div>
        </div>

    </div>
    <script src="script.js"></script>
</body>
</html>"""

    js = """// Split-Layout Hero interactions
document.addEventListener('DOMContentLoaded', () => {
    // Optional: Add subtle parallax effect to the backgrounds on mouse move
    const hero = document.querySelector('.hero-container');
    
    hero.addEventListener('mousemove', (e) => {
        const x = (window.innerWidth - e.pageX * 2) / 90;
        const y = (window.innerHeight - e.pageY * 2) / 90;
        
        // Slightly shift the background image position
        hero.style.backgroundPosition = `calc(50% + ${x}px) calc(100% + ${y}px), center`;
    });
    
    hero.addEventListener('mouseleave', () => {
        hero.style.backgroundPosition = `bottom center, center`;
    });
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
  - Structural HTML elements (`h1`, `p`) maintain semantic hierarchy.
  - The `background-image` approach means the portrait acts as decoration. If the portrait conveyed important meaning, an inline `<img alt="...">` should be used instead.
  - Color contrast between the pure white text and the dark navy background easily exceeds WCAG AA requirements (4.5:1).
* **Performance**: 
  - Using a single `div` with multiple `background-image` layers is highly performant and keeps the DOM shallow.
  - A small JS parallax effect is included utilizing `background-position`. For lower-end devices, updating `background-position` on mouse move can trigger repaints. It is mapped tightly to bounds to limit performance hits, but for strict high-performance targets, it can be disabled or updated using `transform: translate3d` on an inner pseudo-element.