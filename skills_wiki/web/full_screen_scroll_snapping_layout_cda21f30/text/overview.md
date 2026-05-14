# Full-Screen Scroll Snapping Layout

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Full-Screen Scroll Snapping Layout

* **Core Visual Mechanism**: This pattern relies on CSS Scroll Snapping to create a presentation-like experience on a website. Instead of fluid, continuous scrolling, the viewport acts as a fixed frame, and each section "snaps" perfectly into view. It pairs large, bold typography with vibrant linear gradients and high-contrast vector illustrations, utilizing Flexbox to ensure perfect vertical and horizontal centering regardless of screen size.
* **Why Use This Skill (Rationale)**: Native scroll snapping provides an app-like, highly polished feel without relying on heavy JavaScript libraries (like fullPage.js). It forces the user to digest one primary piece of information at a time, making it excellent for storytelling, portfolios, or feature highlights. 
* **Overall Applicability**: Best used for hero sections, personal portfolios, product feature tours, presentation decks converted to web format, or single-page landing pages.
* **Value Addition**: Compared to standard sequential scrolling, scroll snapping adds intentionality to the user's journey. It guarantees that the visual composition the designer intended is exactly what the user sees, preventing them from stopping "halfway" between two sections.
* **Browser Compatibility**: CSS Scroll Snap (`scroll-snap-type`, `scroll-snap-align`) is natively supported in all modern browsers (Chrome 69+, Firefox 68+, Safari 11+).

### 2. Visual & Technical Breakdown

* **Step A: Core Visual Elements**
  - **Containers**: A parent `.container` and multiple child `.slide` elements.
  - **Color Logic**: Full-bleed linear gradients with a consistent ~45-degree angle. Text is set to pure white (`#ffffff`) for dark themes or stark dark blue/black for light themes, ensuring high contrast.
  - **Typographic Hierarchy**: Minimalist and bold. Headings (`h2`) are massive (`clamp(2rem, 5vw, 4.5rem)`), weight `700`, using a clean sans-serif like 'Inter' or 'Poppins'.
  - **CSS Properties**: The heavy lifting is done by `overflow-y: scroll`, `scroll-snap-type: y mandatory` on the parent, and `scroll-snap-align: start`, `scroll-snap-stop: always` on the children.

* **Step B: Layout & Compositional Style**
  - **Layout System**: The parent defines the scrollable boundary. Each child slide is exactly `100%` width and `100%` height of the parent. 
  - **Centering**: Flexbox is used within each slide (`display: flex; align-items: center; justify-content: center; gap: 50px`).
  - **Responsive Adjustments**: On smaller screens, the layout shifts from a row (side-by-side image and text) to a column to prevent cramping.

* **Step C: Interactive Behavior & Animations**
  - **Scroll Physics**: The interaction is completely native. The browser's physics engine handles the deceleration and snapping momentum.
  - **Scrollbar Hiding**: To maximize the "slide" illusion, scrollbars are visually hidden using `::-webkit-scrollbar { display: none; }` and `scrollbar-width: none`.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **Full-page snap scrolling** | Native CSS `scroll-snap` | Performant, built-in browser physics, requires zero JS calculations, works on mobile naturally. |
| **Slide layout & centering** | CSS Flexbox | `align-items: center; justify-content: center` reliably pins content to the absolute middle of the slide. |
| **Responsive scaling** | CSS `clamp()` | Automatically scales typography and image sizes smoothly between mobile and desktop without rigid media query jumps. |
| **Illustrations** | Inline Data URI SVGs | Allows the component to be entirely self-contained without needing external image assets. |

#### 3b. Complete Reproduction Code

```python
def create_component(
    output_dir: str,
    title_text: str = "I'm a Product Designer.",
    body_text: str = "Crafting beautiful digital experiences.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#9553ff",     # CSS hex color for accent
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Full-Screen Scroll Snapping Layout.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors and backgrounds ===
    if color_scheme == "dark":
        text_color = "#ffffff"
        body_bg = "#000000"
        slide1_bg = f"linear-gradient(135deg, #4f4080, {accent_color})"
        slide2_bg = "linear-gradient(135deg, #0d111c, #2a9d8f)"
        slide3_bg = "linear-gradient(135deg, #957495, #e76f51)"
    else:
        text_color = "#1a1a2e"
        body_bg = "#f0f0f0"
        slide1_bg = f"linear-gradient(135deg, #e0c3fc, {accent_color}40)"
        slide2_bg = "linear-gradient(135deg, #d4f0f0, #8cb369)"
        slide3_bg = "linear-gradient(135deg, #ffcbf2, #f3c4fb)"

    # === Generated Inline SVG Placeholders ===
    svg1 = "data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 400 400'><rect x='50' y='100' width='300' height='200' rx='20' fill='white' opacity='0.2'/><circle cx='100' cy='150' r='20' fill='white' opacity='0.8'/><rect x='140' y='140' width='150' height='20' rx='10' fill='white' opacity='0.8'/><rect x='100' y='190' width='200' height='15' rx='7' fill='white' opacity='0.5'/><rect x='100' y='220' width='160' height='15' rx='7' fill='white' opacity='0.5'/></svg>"
    svg2 = "data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 400 400'><rect x='120' y='40' width='160' height='320' rx='25' fill='white' opacity='0.2' stroke='white' stroke-width='4'/><rect x='135' y='60' width='130' height='250' rx='10' fill='white' opacity='0.1'/><circle cx='200' cy='335' r='10' fill='white' opacity='0.5'/></svg>"
    svg3 = "data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 400 400'><circle cx='200' cy='200' r='30' fill='white' opacity='0.9'/><ellipse cx='200' cy='200' rx='140' ry='40' fill='none' stroke='white' stroke-width='4' opacity='0.5'/><ellipse cx='200' cy='200' rx='140' ry='40' fill='none' stroke='white' stroke-width='4' opacity='0.5' transform='rotate(60 200 200)'/><ellipse cx='200' cy='200' rx='140' ry='40' fill='none' stroke='white' stroke-width='4' opacity='0.5' transform='rotate(120 200 200)'/></svg>"

    if color_scheme == "light":
        # Invert SVGs for light mode visibility
        svg1 = svg1.replace("'white'", "'black'")
        svg2 = svg2.replace("'white'", "'black'")
        svg3 = svg3.replace("'white'", "'black'")

    # === CSS ===
    css = f"""/* Full-Screen Scroll Snapping Layout */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --width: {width_px}px;
    --height: {height_px}px;
    --text-color: {text_color};
    --slide1-bg: {slide1_bg};
    --slide2-bg: {slide2_bg};
    --slide3-bg: {slide3_bg};
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background: {body_bg};
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 100vh;
    overflow: hidden; /* Prevent body scrolling so component handles it */
}}

.container {{
    width: var(--width);
    height: var(--height);
    max-width: 100vw;
    max-height: 100vh;
    overflow-y: scroll;
    
    /* Core Snapping Logic */
    scroll-snap-type: y mandatory;
    scroll-behavior: smooth;
    
    /* Aesthetics for modular view */
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
    background: var(--slide1-bg);
    
    /* Hide scrollbars for cleaner UX */
    scrollbar-width: none; /* Firefox */
    -ms-overflow-style: none;  /* IE and Edge */
}}

.container::-webkit-scrollbar {{
    display: none; /* Chrome, Safari and Opera */
}}

.slide {{
    width: 100%;
    height: 100%;
    
    /* Core Snapping Align */
    scroll-snap-align: start;
    scroll-snap-stop: always;
    
    display: flex;
    align-items: center;
    justify-content: center;
    gap: clamp(30px, 5vw, 80px);
    padding: 2rem;
}}

.slide1 {{ background: var(--slide1-bg); }}
.slide2 {{ background: var(--slide2-bg); }}
.slide3 {{ background: var(--slide3-bg); }}

.slide img {{
    width: clamp(200px, 30vw, 400px);
    object-fit: contain;
    filter: drop-shadow(0 20px 30px rgba(0,0,0,0.1));
}}

.slide-content {{
    max-width: 600px;
    color: var(--text-color);
}}

.slide-content h2 {{
    font-size: clamp(2rem, 5vw, 4.5rem);
    font-weight: 700;
    line-height: 1.1;
    margin-bottom: 1rem;
    letter-spacing: -0.02em;
}}

.slide-content p {{
    font-size: clamp(1rem, 1.5vw, 1.5rem);
    opacity: 0.85;
    line-height: 1.5;
}}

/* Responsive behavior */
@media (max-width: 768px) {{
    .slide {{
        flex-direction: column;
        text-align: center;
    }}
    .slide img {{
        width: clamp(150px, 50vw, 250px);
    }}
}}
"""

    # === HTML ===
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        <!-- Slide 1 -->
        <div class="slide slide1">
            <img src="{svg1}" alt="Illustration of a UI Card">
            <div class="slide-content">
                <h2>{title_text}</h2>
                <p>{body_text}</p>
            </div>
        </div>
        
        <!-- Slide 2 -->
        <div class="slide slide2">
            <img src="{svg2}" alt="Illustration of a Mobile App">
            <div class="slide-content">
                <h2>I develop web and mobile apps.</h2>
                <p>Creating seamless cross-platform functionality with modern tech stacks.</p>
            </div>
        </div>
        
        <!-- Slide 3 -->
        <div class="slide slide3">
            <img src="{svg3}" alt="Illustration of an Atom">
            <div class="slide-content">
                <h2>I live in the United States.</h2>
                <p>Collaborating globally while rooted locally.</p>
            </div>
        </div>
    </div>
    
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Intersection Observer to track the currently active snapped slide
document.addEventListener('DOMContentLoaded', () => {{
    const container = document.querySelector('.container');
    const slides = document.querySelectorAll('.slide');

    const observerOptions = {{
        root: container,
        threshold: 0.6 // Trigger when 60% of the slide is visible
    }};

    const observer = new IntersectionObserver((entries) => {{
        entries.forEach(entry => {{
            if (entry.isIntersecting) {{
                // You can trigger entrance animations here based on the active slide
                console.log('Currently viewing:', entry.target.className);
            }}
        }});
    }}, observerOptions);

    slides.forEach(slide => observer.observe(slide));
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

### 4. Accessibility & Performance Notes

* **Accessibility**: 
  - The CSS uses `scrollbar-width: none` which hides the visual indicator of scrolling. While aesthetically pleasing, it can confuse users who rely on scrollbars to understand page length. If used in production, ensure you provide alternate indicators (like pagination dots).
  - High color contrast is maintained programmatically by flipping SVG colors and text colors based on the `color_scheme` chosen.
* **Performance**:
  - CSS Scroll Snapping is incredibly performant because the browser's compositor thread handles the physics. It avoids the "scroll-jank" often associated with older JavaScript libraries like fullPage.js.
  - The SVG illustrations are encoded directly into the HTML to prevent additional HTTP requests and maintain an instant-load feel.