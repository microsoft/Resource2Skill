# Asymmetric Split-Screen Hero with Animated Marquee

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Asymmetric Split-Screen Hero with Animated Marquee

* **Core Visual Mechanism**: A bold, modern 50/50 vertical split layout. One side anchors the user with high-contrast typography on a solid background, while the other side showcases a rich, edge-to-edge photograph. A prominent, infinite-scrolling marquee at the top of the screen introduces a dynamic, "editorial" feel, providing secondary information without cluttering the primary focal point.
* **Why Use This Skill (Rationale)**: Split-screen designs effectively solve the problem of balancing heavy copy with high-impact imagery. By completely separating them, text remains 100% legible without needing dark overlays on the image. The marquee adds a subtle layer of motion that catches the eye, signaling a premium, modern brand identity (heavily popularized by high-end fashion and architectural web design).
* **Overall Applicability**: Ideal for luxury brand landing pages, real estate/architectural portfolios, high-end e-commerce storefronts, and digital agency homepages.
* **Value Addition**: Transforms a standard "text-over-image" hero into an asymmetric, magazine-like layout. The entrance animations (fade-in-right) and continuous marquee scroll create an immediate sense of polish and high production value.
* **Browser Compatibility**: Excellent. Relies on standard CSS Flexbox for layout, and CSS `@keyframes` with `transform: translateX` for animations. Fully supported in all modern browsers (Chrome, Firefox, Safari, Edge).

### 2. Visual & Technical Breakdown

* **Step A: Core Visual Elements**
  * **Color Logic**: High contrast. Dark theme utilizes a deep charcoal/black (`#111111`) with stark white text (`#ffffff`). The accent color is applied to interactive elements like buttons and hovered links.
  * **Typographic Hierarchy**: Bold, geometric sans-serif (e.g., 'Inter', 'Rubik'). Large primary headline (e.g., `5rem`), distinct secondary description (`1.4rem`), and tracked-out uppercase UI text for buttons and navigation (letter-spacing: `2px`).
  * **Stylistic Triggers**: Minimalist. No drop shadows on text, flat solid colors, sharp or slightly rounded corners, and generous padding.

* **Step B: Layout & Compositional Style**
  * **Layout System**: CSS Flexbox handles the macro-layout. A main wrapper is set to display flex. The left content container and right image container both use `flex: 1` or `width: 50%` to divide the space equally.
  * **Spatial Feel**: Heavy use of whitespace in the text block. The text container itself is usually treated as a flex-column with `justify-content: center` to vertically align the copy perfectly beside the image.
  * **Z-index Layering**: Very flat. The focus is on a 2D plane with motion providing the depth, rather than overlapping elements.

* **Step C: Interactive Behavior & Animations**
  * **Marquee**: Pure CSS animation translating an inline element from `100%` (off-screen right) to `-100%` (off-screen left) in an infinite linear loop.
  * **Entrance Animation**: The image utilizes an `@keyframes` animation (`opacity: 0`, `transform: translateX(50px)` to `opacity: 1`, `transform: translateX(0)`) running on page load over ~1-2 seconds with an `ease-out` timing function.
  * **Hover States**: Links and buttons feature smooth color transitions (`transition: all 0.3s ease`).

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| Split-Screen Layout | CSS Flexbox | Simplest and most robust way to align two 50/50 columns and vertically center the text within its column. |
| Scrolling Ticker/Marquee | Pure CSS `@keyframes` | Highly performant using `transform: translateX` and requires zero JavaScript overhead. |
| Image Reveal Animation | Pure CSS `@keyframes` | Triggers automatically on page load. Clean, GPU-accelerated transition. |
| Responsive Stacking | CSS `@media` queries | Allows the 50/50 split to elegantly collapse into a stacked column on mobile devices. |

> **Feasibility Assessment**: 100%. The visual layout, typography structure, marquee animation, and image reveal demonstrated in the tutorial can be perfectly reproduced using pure HTML and CSS. A touch of JS is included purely to populate the marquee text to keep the HTML clean and reusable.

#### 3b. Complete Reproduction Code

```python
def create_component(
    output_dir: str,
    title_text: str = "Design Beyond Time",
    body_text: str = "Experience the future of luxury living with our new exclusive collections and timeless architecture.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#d4af37",     # CSS hex color for accent (e.g., gold)
    width_px: int = 1440,
    height_px: int = 900,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Asymmetric Split-Screen Hero with Marquee.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Derive theme colors
    if color_scheme == "dark":
        bg_color = "#111111"
        text_color = "#ffffff"
        nav_text = "#cccccc"
        marquee_bg = "#000000"
    else:
        bg_color = "#ffffff"
        text_color = "#1a1a1a"
        nav_text = "#555555"
        marquee_bg = "#f4f4f4"

    # Define the marquee content (repeated to ensure infinite scroll coverage)
    marquee_content = "NEW COLLECTION • LUXURY REDEFINED • EXPRESS DESIGN 2025 LAUNCH • TIMELESS BEAUTY • EXPLORE NOW • " * 4

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Rubik:wght@300;400;500;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="app-container">
        <!-- Marquee -->
        <div class="scrolling-text-container">
            <div class="scrolling-text" id="marquee-text" aria-hidden="true"></div>
        </div>

        <!-- Header / Navigation -->
        <header class="header">
            <div class="logo">EXPRESS DESIGNS</div>
            <nav class="main-nav">
                <ul class="main-nav-list">
                    <li><a href="#" class="main-nav-link active">Home</a></li>
                    <li><a href="#" class="main-nav-link">About Us</a></li>
                    <li><a href="#" class="main-nav-link">Services</a></li>
                    <li><a href="#" class="main-nav-link">Testimonials</a></li>
                    <li><a href="#" class="main-nav-link cta-link">Contact Us</a></li>
                </ul>
            </nav>
        </header>

        <!-- Main Hero Section -->
        <main class="hero-section">
            <div class="hero-content">
                <div class="hero-text-box">
                    <h1 class="heading-primary">{title_text}</h1>
                    <p class="hero-description">{body_text}</p>
                    <a href="#" class="btn">DISCOVER MORE</a>
                </div>
            </div>
            
            <div class="hero-image-box">
                <img src="https://images.unsplash.com/photo-1600210492486-724fe5c67fb0?ixlib=rb-4.0.3&auto=format&fit=crop&w=1600&q=80" alt="Luxury modern interior living room" class="hero-img">
            </div>
        </main>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    css = f"""/* Asymmetric Split-Screen Hero CSS */
:root {{
    --bg-color: {bg_color};
    --text-color: {text_color};
    --nav-text: {nav_text};
    --accent-color: {accent_color};
    --marquee-bg: {marquee_bg};
    --comp-width: {width_px}px;
    --comp-height: {height_px}px;
}}

* {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: 'Rubik', sans-serif;
    background-color: var(--bg-color);
    color: var(--text-color);
    min-height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
    overflow-x: hidden;
}}

.app-container {{
    width: 100%;
    max-width: var(--comp-width);
    height: 100vh;
    max-height: var(--comp-height);
    display: flex;
    flex-direction: column;
    position: relative;
    background-color: var(--bg-color);
    box-shadow: 0 20px 40px rgba(0,0,0,0.2);
    overflow: hidden;
}}

/* --- Marquee --- */
.scrolling-text-container {{
    background-color: var(--marquee-bg);
    color: var(--text-color);
    padding: 0.5rem 0;
    overflow: hidden;
    white-space: nowrap;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    display: flex;
    align-items: center;
}}

.scrolling-text {{
    display: inline-block;
    font-size: 0.8rem;
    font-weight: 500;
    letter-spacing: 2px;
    text-transform: uppercase;
    /* Adjust time to speed up or slow down */
    animation: scroll-left 30s linear infinite;
    will-change: transform;
}}

@keyframes scroll-left {{
    0% {{ transform: translateX(0); }}
    100% {{ transform: translateX(-50%); }}
}}

/* --- Header --- */
.header {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1.5rem 4rem;
    z-index: 10;
}}

.logo {{
    font-size: 1.2rem;
    font-weight: 700;
    letter-spacing: 2px;
    text-transform: uppercase;
}}

.main-nav-list {{
    list-style: none;
    display: flex;
    align-items: center;
    gap: 2.5rem;
}}

.main-nav-link {{
    text-decoration: none;
    color: var(--nav-text);
    font-size: 1rem;
    font-weight: 500;
    transition: color 0.3s ease;
}}

.main-nav-link:hover,
.main-nav-link.active {{
    color: var(--text-color);
}}

.cta-link {{
    background-color: var(--text-color);
    color: var(--bg-color) !important;
    padding: 0.8rem 1.5rem;
    border-radius: 4px;
    font-weight: 600;
    transition: background-color 0.3s ease, color 0.3s ease;
}}

.cta-link:hover {{
    background-color: var(--accent-color);
    color: #fff !important;
}}

/* --- Hero Section --- */
.hero-section {{
    display: flex;
    flex: 1; /* Takes remaining height after header */
    height: 100%;
}}

.hero-content {{
    flex: 1;
    display: flex;
    flex-direction: column;
    justify-content: center;
    padding: 0 4rem 4rem 4rem;
}}

.hero-text-box {{
    max-width: 600px;
}}

.heading-primary {{
    font-size: clamp(3rem, 5vw, 5rem);
    line-height: 1.1;
    margin-bottom: 1.5rem;
    font-weight: 700;
}}

.hero-description {{
    font-size: 1.25rem;
    line-height: 1.6;
    color: var(--nav-text);
    margin-bottom: 2.5rem;
    max-width: 85%;
}}

.btn {{
    display: inline-block;
    text-decoration: none;
    color: var(--text-color);
    border: 1px solid var(--text-color);
    padding: 1rem 2.5rem;
    font-size: 0.9rem;
    font-weight: 600;
    letter-spacing: 2px;
    text-transform: uppercase;
    transition: all 0.3s ease;
    background: transparent;
}}

.btn:hover {{
    background-color: var(--accent-color);
    border-color: var(--accent-color);
    color: #fff;
}}

/* --- Hero Image & Animation --- */
.hero-image-box {{
    flex: 1;
    position: relative;
    overflow: hidden;
}}

.hero-img {{
    width: 100%;
    height: 100%;
    object-fit: cover;
    /* Entrance Animation */
    opacity: 0;
    animation: fadeInRight 1.2s cubic-bezier(0.2, 0.8, 0.2, 1) forwards;
    animation-delay: 0.2s;
}}

@keyframes fadeInRight {{
    0% {{
        opacity: 0;
        transform: translateX(100px);
    }}
    100% {{
        opacity: 1;
        transform: translateX(0);
    }}
}}

/* --- Responsive Adjustments --- */
@media (max-width: 1024px) {{
    .header {{
        padding: 1.5rem 2rem;
    }}
    .hero-content {{
        padding: 0 2rem 2rem 2rem;
    }}
}}

@media (max-width: 768px) {{
    .hero-section {{
        flex-direction: column-reverse;
    }}
    
    .hero-image-box {{
        flex: 0 0 40%;
    }}
    
    .hero-content {{
        flex: 0 0 60%;
        padding-top: 2rem;
    }}
    
    .main-nav-list {{
        display: none; /* Hide standard nav on mobile for simplicity in this component */
    }}
    
    .heading-primary {{
        font-size: 2.5rem;
    }}
}}
"""

    js = f"""// Populate marquee text dynamically to avoid long HTML strings
document.addEventListener('DOMContentLoaded', () => {{
    const marqueeText = document.getElementById('marquee-text');
    const content = "{marquee_content}";
    marqueeText.textContent = content;
}});
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

* **Accessibility (A11y)**: 
  * The marquee text is accompanied by `aria-hidden="true"`. Continuous scrolling text is often considered decorative and can interfere with screen readers. Providing it visually but hiding it from the accessibility tree is best practice unless the information is uniquely critical.
  * Contrast ratios between the text and background meet the WCAG AA standard for both light and dark themes as configured in the Python logic.
  * **Enhancement Tip**: For production, wrap the CSS animations in `@media (prefers-reduced-motion: no-preference)` to respect users who suffer from vestibular disorders.
* **Performance**:
  * The marquee animation targets the `transform` property and is flagged with `will-change: transform`. This forces the browser to composite the scrolling element on the GPU, avoiding expensive layout repaints and jitter (jank) during the scroll.
  * The image container forces `object-fit: cover`, which prevents layout shifting. Utilizing responsive image techniques (`srcset`) would be the next step for a production environment.