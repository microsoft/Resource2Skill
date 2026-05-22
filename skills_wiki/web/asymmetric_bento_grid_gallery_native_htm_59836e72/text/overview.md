# Asymmetric Bento Grid Gallery & Native HTML5 Accordion

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Asymmetric Bento Grid Gallery & Native HTML5 Accordion

* **Core Visual Mechanism**: This component merges two highly effective, lightweight web patterns. First, an **Asymmetric Bento Grid** uses CSS `grid-template-areas` to map out a semantic, magazine-like layout (one large feature image alongside a grid of smaller supporting images) that fluidly collapses into a single column on mobile. Second, a **Zero-JS Interactive Accordion** utilizes native HTML5 `<details>` and `<summary>` tags to create an expandable FAQ/details section, providing interactivity natively without JavaScript overhead.

* **Why Use This Skill (Rationale)**: 
  * *Bento Grids* establish an immediate visual hierarchy. By giving one item 4x the spatial weight of the others, you guide the user's eye naturally to the primary content while keeping supporting content structured.
  * *Native Accordions* drastically reduce payload size and complexity. Relying on browser-native behavior ensures maximum accessibility (keyboard navigation comes built-in) and zero script-parsing delay.

* **Overall Applicability**: Perfect for minimalist portfolio sites, product feature highlights, photography galleries, and landing page FAQ sections where clean, fast-loading, and responsive design is prioritized over heavy JavaScript animations.

* **Value Addition**: Compared to a standard stacked list of images or text, this pattern adds a structured, editorial feel to media and keeps text-heavy information (like FAQs) cleanly tucked away until requested, reducing cognitive load.

* **Browser Compatibility**: 
  * CSS Grid & `grid-template-areas`: Universally supported in all modern browsers (Edge, Chrome, Safari, Firefox, iOS Safari).
  * HTML5 `<details>`/`<summary>`: Fully supported across all modern browsers.
  * `object-fit: cover`: Fully supported.

### 2. Visual & Technical Breakdown

* **Step A: Core Visual Elements**
  * **Color Logic**: Dependent on theme, but relies heavily on a high-contrast text-to-background ratio with a subtle, low-opacity "surface" color for the accordion cards (e.g., `rgba(255,255,255,0.05)` in dark mode).
  * **Typographic Hierarchy**: Features a dual-font strategy. An elegant serif (like *Merriweather*) for headings to provide an editorial look, and a clean sans-serif (like *Poppins* or *Inter*) for readable body text and UI elements.
  * **Key CSS Properties**: 
    * Layout: `display: grid`, `grid-template-areas`, `gap`.
    * Media: `object-fit: cover` to ensure images perfectly fill their varied grid tracks without distortion.
    * Interactivity: `transform: scale(1.05)` combined with `overflow: hidden` on the image wrappers to create an elegant "zoom-in" effect on hover.

* **Step B: Layout & Compositional Style**
  * **Grid Blueprint**: The desktop grid is 4 columns by 2 rows. 
    * `img-1` spans 2 rows and 2 columns (a 2x2 square).
    * `img-2`, `img-3`, `img-4`, `img-5` each span 1 column and 1 row (1x1 squares).
  * **Spacing**: A generous `gap` (e.g., `1rem` or `1.5rem`) keeps the bento box distinct, while `margin: 0 auto` combined with `width: min(1000px, 100%)` ensures the container stays centered and doesn't stretch endlessly on ultra-wide screens.
  * **Responsive Collapse**: At smaller viewports (e.g., `< 768px`), the grid shifts from `display: grid` to `display: flex` with `flex-direction: column`, instantly converting the complex grid into a mobile-friendly scrollable feed.

* **Step C: Interactive Behavior & Animations**
  * **Hover Zoom**: Images scale up slightly on hover (`transition: 0.3s ease`). Because their container has `overflow: hidden`, the image appears to zoom inwards without breaking the grid boundary.
  * **Native Toggles**: Clicking the `<summary>` element natively toggles the `open` attribute on the `<details>` parent, revealing the nested `<p>` tag instantly.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| Asymmetric Gallery Layout | CSS Grid (`grid-template-areas`) | Allows visual, string-based mapping of the layout ("img-1 img-2..."), making complex spans incredibly easy to read and maintain. |
| Responsive Layout Shift | CSS Media Queries + Flexbox fallback | Changing from `grid` to `flex` at a breakpoint is the cleanest way to collapse a 2D layout into a 1D vertical feed. |
| Image Sizing | `object-fit: cover` | Ensures placeholder (or real) images fill the dynamic grid cells perfectly without stretching. |
| Expandable FAQ | HTML5 `<details>` & `<summary>` | Native browser feature. Completely eliminates the need for JavaScript state management or event listeners. |
| Hover Animations | CSS `transform` & `transition` | GPU-accelerated scaling (`scale: 1.05`) is highly performant and requires no JS. |

*Feasibility Assessment*: 100% of the tutorial's core layout and accordion functionality can be reproduced perfectly using just HTML and CSS, staying true to the "no JavaScript" philosophy highlighted in the original tutorial.

#### 3b. Complete Reproduction Code

```python
def create_component(
    output_dir: str,
    title_text: str = "My Work & FAQs",
    body_text: str = "A curated selection of recent photography and common questions.",
    color_scheme: str = "light",       # "dark" or "light"
    accent_color: str = "#ff7a59",     # CSS hex color for accent
    width_px: int = 1000,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Asymmetric Bento Grid & Native Accordion.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors ===
    if color_scheme == "dark":
        bg_color = "#121212"
        text_color = "#f4f4f5"
        text_muted = "#a1a1aa"
        surface_color = "#1f1f22"
        surface_hover = "#27272a"
        border_color = "#3f3f46"
    else:
        bg_color = "#fafafa"
        text_color = "#18181b"
        text_muted = "#52525b"
        surface_color = "#ffffff"
        surface_hover = "#f4f4f5"
        border_color = "#e4e4e7"

    # === CSS ===
    css = f"""/* Bento Grid & Accordion Component */
@import url('https://fonts.googleapis.com/css2?family=Merriweather:wght@400;700&family=Inter:wght@400;500&display=swap');

*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --text: {text_color};
    --text-muted: {text_muted};
    --accent: {accent_color};
    --surface: {surface_color};
    --surface-hover: {surface_hover};
    --border: {border_color};
    --max-width: {width_px}px;
}}

body {{
    font-family: 'Inter', system-ui, sans-serif;
    background: var(--bg);
    color: var(--text);
    min-height: 100vh;
    padding: 2rem 1rem;
    line-height: 1.6;
}}

/* Typography */
h2, h3 {{
    font-family: 'Merriweather', serif;
    color: var(--text);
    margin-bottom: 1rem;
}}

.header-text {{
    text-align: center;
    margin-bottom: 3rem;
}}

.header-text p {{
    color: var(--text-muted);
    max-width: 600px;
    margin: 0 auto;
}}

/* Section Constraints */
.section-container {{
    width: min(var(--max-width), 100%);
    margin: 0 auto 5rem auto;
}}

/* === BENTO GRID GALLERY === */
.grid-container {{
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    grid-template-rows: repeat(2, 1fr);
    grid-template-areas: 
        "img-1 img-1 img-2 img-3"
        "img-1 img-1 img-4 img-5";
    gap: 1rem;
    aspect-ratio: 16 / 9; /* Keeps layout proportional on desktop */
}}

.grid-item {{
    overflow: hidden;
    border-radius: 12px;
    background: var(--surface);
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
}}

.grid-item img {{
    width: 100%;
    height: 100%;
    object-fit: cover;
    transition: transform 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94);
}}

.grid-item:hover img {{
    transform: scale(1.08);
}}

/* Area Assignments */
.img-1 {{ grid-area: img-1; }}
.img-2 {{ grid-area: img-2; }}
.img-3 {{ grid-area: img-3; }}
.img-4 {{ grid-area: img-4; }}
.img-5 {{ grid-area: img-5; }}

/* === NATIVE ACCORDION FAQ === */
.faq-container {{
    display: flex;
    flex-direction: column;
    gap: 1rem;
}}

details {{
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 8px;
    overflow: hidden;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
}}

summary {{
    padding: 1.25rem;
    font-weight: 500;
    cursor: pointer;
    list-style: none; /* Hide default arrow in some browsers */
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: var(--surface);
    transition: background 0.2s ease;
}}

summary:hover {{
    background: var(--surface-hover);
}}

/* Custom Arrow indicator */
summary::after {{
    content: "▼";
    font-size: 0.8rem;
    color: var(--accent);
    transition: transform 0.3s ease;
}}

details[open] summary::after {{
    transform: rotate(180deg);
}}

/* Hide standard marker */
summary::-webkit-details-marker {{
    display: none;
}}

details p {{
    padding: 0 1.25rem 1.25rem 1.25rem;
    color: var(--text-muted);
    border-top: 1px solid transparent;
}}

details[open] summary {{
    border-bottom: 1px solid var(--border);
    margin-bottom: 1rem;
}}

/* === RESPONSIVE FALLBACKS === */
@media (max-width: 768px) {{
    .grid-container {{
        display: flex;
        flex-direction: column;
        aspect-ratio: auto;
    }}
    
    .grid-item {{
        height: 250px; /* Give flex items a set height on mobile */
    }}
    
    .img-1 {{
        height: 400px; /* Make the hero image taller */
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
    <link rel="stylesheet" href="style.css">
</head>
<body>

    <!-- Header Section -->
    <header class="section-container header-text">
        <h2>{title_text}</h2>
        <p>{body_text}</p>
    </header>

    <!-- Bento Grid Gallery Section -->
    <section class="section-container">
        <div class="grid-container">
            <div class="grid-item img-1">
                <img src="https://images.unsplash.com/photo-1469474968028-56623f02e42e?auto=format&fit=crop&q=80&w=1200" alt="Nature landscape hero">
            </div>
            <div class="grid-item img-2">
                <img src="https://images.unsplash.com/photo-1501854140801-50d01698950b?auto=format&fit=crop&q=80&w=600" alt="Mountain view">
            </div>
            <div class="grid-item img-3">
                <img src="https://images.unsplash.com/photo-1472214103451-9374bd1c798e?auto=format&fit=crop&q=80&w=600" alt="Forest valley">
            </div>
            <div class="grid-item img-4">
                <img src="https://images.unsplash.com/photo-1426604966848-d7adac402bff?auto=format&fit=crop&q=80&w=600" alt="Sunset over hills">
            </div>
            <div class="grid-item img-5">
                <img src="https://images.unsplash.com/photo-1470071131384-001b85755b36?auto=format&fit=crop&q=80&w=600" alt="Morning mist">
            </div>
        </div>
    </section>

    <!-- Native Accordion FAQ Section -->
    <section class="section-container">
        <h3 style="text-align: center; margin-bottom: 2rem;">Common Questions</h3>
        <div class="faq-container">
            <details>
                <summary>How much does a photoshoot cost?</summary>
                <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Similique qui explicabo voluptatum tenetur. Praesentium voluptatum repellendus asperiores eos.</p>
            </details>
            <details>
                <summary>Do you do weddings?</summary>
                <p>Assumenda dolore dolor aliquid totam nostrum libero repellendus architecto. Ut enim ad minima veniam, quis nostrum exercitationem.</p>
            </details>
            <details>
                <summary>How can I contact you?</summary>
                <p>You can reach out via the contact form on my main portfolio page or send a direct message to my official Instagram account linked above.</p>
            </details>
        </div>
    </section>

    <!-- Intentionally empty JS as the tutorial focuses on a zero-JS approach -->
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = """// No JavaScript required!
// This component relies entirely on HTML5 native <details>/<summary> tags for the accordion 
// and CSS Grid for the responsive layout, maximizing performance and accessibility.
console.log('Component loaded successfully without JavaScript dependencies.');
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

#### 3c. Verification Checklist
- [x] Does the code produce valid HTML5 that passes basic validation?
- [x] Does `index.html` work when opened directly in a browser (`file://` protocol)?
- [x] Are all color values explicit hex or rgba? *(Handled via Python variable injection into CSS `:root`)*
- [x] Are all external resources loaded from CDN URLs? *(Unsplash for images, Google Fonts for typography)*
- [x] Does the component respect the `width_px` parameters? *(Used as `--max-width` to ensure responsiveness)*
- [x] Does `color_scheme="dark"` produce a dark theme and `"light"` a light theme?
- [x] Does `accent_color` propagate to all accent elements? *(Used for the custom accordion arrows)*
- [x] Does it produce a visually recognizable reproduction of the tutorial's effect? *(Perfectly mimics the 4-column Bento grid and the clean FAQ blocks).*

### 4. Accessibility & Performance Notes

* **Accessibility (a11y)**:
  * Using native `<details>` and `<summary>` tags is best practice for accessibility. Browsers automatically handle keyboard focus (`Tab`), expansion toggling (`Enter` / `Space`), and screen reader state announcements (`aria-expanded` is handled natively under the hood).
  * Hover states on the gallery are strictly visual (`transform: scale`). Content order remains logical in the DOM, meaning screen readers will read the images sequentially regardless of the grid shape. 
* **Performance**:
  * **Zero JavaScript execution overhead**. All interactions (accordions and hover effects) are handled by the browser's native rendering engine.
  * The CSS hover animation uses `transform`, which is GPU-accelerated. It avoids repainting the layout (unlike animating `width` or `margin`), guaranteeing a silky 60fps interaction even on lower-end mobile devices.
  * Images use `object-fit: cover` and are loaded directly from Unsplash with appropriate width flags (`&w=600`, `&w=1200`) mapped roughly to their display sizes, optimizing bandwidth.