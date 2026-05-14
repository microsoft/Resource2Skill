### 1. High-level Design Pattern Extraction

> **Skill Name**: Asymmetrical Layered Flexbox Hero

* **Core Visual Mechanism**: This design pattern relies on an asymmetrical layout constructed via Flexbox, combined with a layered CSS `background-image` technique. A central, cutout subject (like a portrait) is composited directly over a textured background pattern using comma-separated background properties. This removes the need for extra absolute-positioned DOM elements. The text content is symmetrically unbalanced: a massive, bold introduction on the left, counter-weighted by staggered, left-bordered quotes on the right.
* **Why Use This Skill (Rationale)**: The asymmetry forces the eye to bounce across the screen, creating a dynamic, modern feel rather than a static, traditional centered hero. The layering technique creates a pseudo-3D depth effect (foreground subject vs. background texture), making the subject pop out. 
* **Overall Applicability**: Ideal for personal portfolios, agency landing pages, or creator profiles where the central focus is an individual or a hero product, flanked by a core value proposition and social proof (quotes/testimonials).
* **Value Addition**: Compared to a standard column layout, this pattern integrates the imagery seamlessly into the canvas. By staggering the quotes using `:nth-child` offsets, it breaks the rigid grid, providing an editorial, magazine-like aesthetic.
* **Browser Compatibility**: Fully supported in all modern browsers. The multiple background technique and CSS Flexbox have universal support.

### 2. Visual & Technical Breakdown

* **Step A: Core Visual Elements**
  - **Color Logic**: A deep, saturated background (e.g., `#1A253A`) contrasted with stark white text (`#FFFFFF`) and a vibrant accent color (`#c13584` or cyan) for buttons and quote borders.
  - **Typography**: The primary heading (`h1`) is heavily weighted (600+), aggressively large (96px), uppercase, with tight line-height to form a solid typographic block. Paragraphs use a legible sans-serif (18px) with generous line-height (30px) for readability.
  - **Background Compositing**: Achieved via `background-image: url(portrait.png), url(pattern.png);`. The first image renders on top of the second.

* **Step B: Layout & Compositional Style**
  - **Layout System**: The main container is a Flexbox container (`display: flex; justify-content: center; align-items: center;`). 
  - **Forced Asymmetry**: Instead of relying solely on flex margins, the child containers use `position: relative` with `left`/`right` properties to manually pull the content apart and overlay it slightly on the central portrait.
  - **Staggering**: The right-side quotes use `.quotes p:nth-child(2) { margin-left: 100px; }` to create a diagonal reading flow.

* **Step C: Interactive Behavior & Animations**
  - **Hover States**: The CTA button uses a simple brightness/color transition.
  - **Enhancement (Added)**: Because the background relies on layered compositing, tracking the mouse position via JavaScript to subtly shift the `background-position` of the foreground portrait adds a high-end parallax depth effect.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **Layered Imagery** | CSS Multiple `background-image` | The core technique from the tutorial; allows stacking a cutout image over a pattern entirely within CSS without extra DOM nodes. |
| **Asymmetrical Layout** | CSS Flexbox + `position: relative` | Provides robust vertical centering while allowing manual horizontal offsets (`right: 20vh`) to emulate the tutorial's exact spatial logic. |
| **Staggered Content** | CSS `:nth-child()` | Cleanest way to offset specific paragraphs (quotes) without adding utility classes to the HTML. |
| **Depth Effect** | JavaScript `mousemove` | Adds subtle interactive parallax to the background positioning, emphasizing the layered CSS technique. |

#### 3b. Complete Reproduction Code

```python
def create_component(
    output_dir: str,
    title_text: str = "WELCOME TO MY<br>FIRST WEBSITE",
    body_text: str = "A demonstration of layered background compositing, asymmetrical flexbox alignment, and interactive depth techniques.",
    color_scheme: str = "dark",
    accent_color: str = "#c13584",
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Asymmetrical Layered Flexbox Hero.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Derive theme colors
    if color_scheme == "dark":
        bg_color = "#151b29"
        text_color = "#ffffff"
        header_bg = "#ffffff"
        header_text = "#000000"
        surface_color = "rgba(255, 255, 255, 0.05)"
    else:
        bg_color = "#e5e7eb"
        text_color = "#111827"
        header_bg = "#111827"
        header_text = "#ffffff"
        surface_color = "rgba(0, 0, 0, 0.05)"

    # Inline SVG for the portrait silhouette to ensure self-containment
    svg_portrait = "%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 400 400'%3E%3Cpath fill='{}' d='M200 60c-38.66 0-70 31.34-70 70s31.34 70 70 70 70-31.34 70-70-31.34-70-70-70zm0 160c-77.32 0-140 62.68-140 140v20h280v-20c0-77.32-62.68-140-140-140z'/%3E%3C/svg%3E".format("%23222" if color_scheme == "dark" else "%23ccc")

    css = f"""/* Asymmetrical Layered Hero — generated component */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --text: {text_color};
    --accent: {accent_color};
    --surface: {surface_color};
    --header-bg: {header_bg};
    --header-text: {header_text};
}}

body {{
    font-family: 'Inter', system-ui, sans-serif;
    background: #000;
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
}}

.browser-window {{
    width: {width_px}px;
    height: {height_px}px;
    background: var(--bg);
    position: relative;
    overflow: hidden;
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
}}

/* Mock Header for layout context */
.site-header {{
    position: absolute;
    top: 0;
    width: 100%;
    height: 60px;
    background-color: var(--header-bg);
    color: var(--header-text);
    display: flex;
    align-items: center;
    padding: 0 40px;
    font-weight: 600;
    z-index: 1000;
}}

/* Main Hero Setup */
.hero-section {{
    width: 100%;
    height: calc(100% - 60px);
    margin-top: 60px;
    position: relative;
    display: flex;
    justify-content: center;
    align-items: center;
    
    /* The Layering Technique: Portrait over Pattern */
    background-image: 
        url("data:image/svg+xml,{svg_portrait}"),
        radial-gradient(var(--surface) 3px, transparent 3px);
    background-size: 
        55vh, /* Portrait size */
        30px 30px; /* Pattern scale */
    background-position: 
        50% 100%, /* Portrait anchored bottom center */
        center;
    background-repeat: 
        no-repeat,
        repeat;
}}

/* Asymmetrical Layout Logic */
.hero-intro {{
    position: relative;
    right: 80px; /* Push left manually */
    max-width: 450px;
    padding-bottom: 40px;
}}

.hero-intro h1 {{
    font-size: 72px;
    line-height: 1.1;
    font-weight: 800;
    text-transform: uppercase;
    color: var(--text);
    margin-bottom: 20px;
}}

.hero-intro p {{
    font-size: 16px;
    line-height: 1.6;
    color: var(--text);
    opacity: 0.8;
    margin-bottom: 30px;
}}

.btn {{
    display: inline-block;
    background-color: var(--accent);
    color: #fff;
    text-decoration: none;
    padding: 14px 28px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1px;
    border-radius: 2px;
    transition: filter 0.2s ease;
}}

.btn:hover {{
    filter: brightness(1.2);
}}

/* Quotes Staggering Logic */
.hero-quotes {{
    position: relative;
    left: 40px; /* Push right manually */
    max-width: 320px;
}}

.hero-quotes p {{
    border-left: 4px solid var(--accent);
    padding-left: 20px;
    margin-bottom: 40px;
    font-size: 15px;
    line-height: 1.6;
    color: var(--text);
    opacity: 0.9;
}}

/* The stagger effect */
.hero-quotes p:nth-child(2) {{
    margin-left: 80px;
}}

.quote-author {{
    display: block;
    margin-top: 10px;
    font-weight: 700;
    font-size: 14px;
    opacity: 1;
}}
"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Asymmetrical Layered Hero</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="browser-window">
        <header class="site-header">
            LOGO
        </header>
        
        <main class="hero-section" id="hero">
            <div class="hero-intro">
                <h1>{title_text}</h1>
                <p>{body_text}</p>
                <a href="#" class="btn">My Work</a>
            </div>
            
            <div class="hero-quotes">
                <p>"The more that you read, the more things you will know. The more that you learn, the more places you'll go."
                <span class="quote-author">- Dr. Seuss</span></p>
                
                <p>"For the best return on your money, pour your purse into your head."
                <span class="quote-author">- Benjamin Franklin</span></p>
            </div>
        </main>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    js = """// Parallax interaction for the layered background
document.addEventListener('DOMContentLoaded', () => {
    const hero = document.getElementById('hero');
    
    // Listen for mouse movements on the hero section
    hero.addEventListener('mousemove', (e) => {
        // Calculate mouse position relative to the center of the element
        const rect = hero.getBoundingClientRect();
        const xPos = (e.clientX - rect.left) / rect.width - 0.5;
        
        // Shift the background position. 
        // We only target the first background (the portrait), leaving the pattern static.
        // Base position is 50% X, 100% Y. We apply a subtle offset multiplier (e.g., -30px).
        const offsetX = 50 + (xPos * -6);
        
        hero.style.backgroundPosition = `${offsetX}% 100%, center`;
    });
    
    // Reset position when mouse leaves
    hero.addEventListener('mouseleave', () => {
        hero.style.transition = 'background-position 0.5s ease-out';
        hero.style.backgroundPosition = '50% 100%, center';
        
        setTimeout(() => {
            hero.style.transition = 'none';
        }, 500);
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
  - The contrast ratio relies on the user-provided variables. The default dark mode provides excellent contrast (`#ffffff` on `#151b29`).
  - The CSS `text-transform: uppercase` is applied correctly via CSS rather than HTML hardcoding, ensuring screen readers announce the words naturally rather than spelling out acronyms.
* **Performance**:
  - The multiple `background-image` technique is highly performant as it avoids adding extra DOM nodes to achieve layering, letting the browser composite the textures natively.
  - The parallax JavaScript modifies `background-position`, which triggers repaints. While fine for a simple UI, heavily animated background positions can cause slight CPU overhead. It is throttled by basic math and limited to mouse movement, keeping the footprint minimal.