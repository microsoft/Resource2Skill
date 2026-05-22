# Dual-Method Parallax Scrolling (JS Fractional & CSS Fixed)

## Analysis

Here is a comprehensive strategy for extracting and reproducing the parallax scrolling web component demonstrated in the tutorial.

### 1. High-level Design Pattern Extraction

> **Skill Name**: Dual-Method Parallax Scrolling (JS Fractional & CSS Fixed)

* **Core Visual Mechanism**: This pattern establishes depth by decoupling the background image scroll speed from the document scroll speed. It demonstrates two distinct techniques:
  1. **Fractional Parallax (JavaScript)**: Modifying `background-position-y` via a scroll event listener, multiplied by a fraction (e.g., `0.7`), causing the background to scroll *slower* than the foreground.
  2. **Fixed Parallax (Pure CSS)**: Using `background-attachment: fixed`, which locks the background to the viewport while foreground elements slide over it.
* **Why Use This Skill (Rationale)**: True 3D depth cannot be natively rendered on standard web pages without WebGL. Parallax creates a "2.5D" illusion of depth, drawing the user's eye, breaking up long blocks of monotonous content, and creating a sense of narrative progression as the user scrolls.
* **Overall Applicability**: Ideal for storytelling articles, SaaS product landing pages, portfolio hero sections, and dividing distinct sections of content on long one-page websites.
* **Value Addition**: Transforms a static scrolling experience into an immersive, dynamic environment. It establishes visual hierarchy by clearly separating "foreground content" (cards/text) from "background atmosphere" (images).
* **Browser Compatibility**: Fully supported across all modern browsers. `background-attachment: fixed` has well-known quirks on iOS Safari, so a media query fallback is often used in production, though it works perfectly on desktop and standard mobile browsers.

### 2. Visual & Technical Breakdown

* **Step A: Core Visual Elements**
  - **Structure**: A vertical stack of full-viewport `div` containers.
  - **Color & Contrast**: High-contrast foreground cards (e.g., `#eeeeee` background with `#333333` text) set against dark, rich, or photographic backgrounds to ensure text legibility regardless of the image underneath.
  - **Typography**: Bold, oversized headings (e.g., `font-size: 60px; font-weight: bold;`) inside the cards to act as focal anchors.
  - **CSS Properties**: `background-size: cover` ensures images fill the viewport without distortion, while `border-radius: 16px` and `padding` create the floating card aesthetic.

* **Step B: Layout & Compositional Style**
  - **Layout System**: CSS Flexbox (`display: flex; align-items: center; justify-content: center;`) effortlessly centers the text cards within each full-screen (`100vh`) section.
  - **Z-index Layering**: Implicit stacking context. The text is naturally painted on top of the backgrounds. 

* **Step C: Interactive Behavior & Animations**
  - **Scroll Binding (JS)**: The `window` scroll event continuously reads `pageYOffset` and updates the inline CSS `background-position-y`. A multiplier of `0.7` means for every 10px scrolled, the background moves 7px, creating the illusion of distance.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **Fractional Scrolling** | JavaScript `scroll` event | CSS cannot mathematically couple scroll position to background coordinates. JS is required to calculate the offset dynamically. |
| **Fixed Scrolling** | CSS `background-attachment` | Native, performant implementation that locks the image to the viewport. Requires zero JS execution. |
| **Centering Content** | CSS Flexbox | Simplest and most robust way to perfectly center text blocks both vertically and horizontally within a full-screen section. |

#### 3b. Complete Reproduction Code

```python
def create_component(
    output_dir: str,
    title_text: str = "DIV 1: JS Parallax",
    body_text: str = "Scroll down to experience the depth",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#800000",     # CSS hex color for accent (e.g., maroon)
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Dual-Method Parallax Scrolling visual effect.
    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme ===
    # The cards will contrast against the background scheme
    if color_scheme == "dark":
        card_bg = "#eeeeee"
        card_text = "#1a1a2e"
        secondary_color = "#00adb5" # Aqua variant from the tutorial
    else:
        card_bg = "#1a1a2e"
        card_text = "#eeeeee"
        secondary_color = "#a8d8ea"

    # === CSS ===
    css = f"""/* Dual-Method Parallax Scrolling — Generated Component */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --accent: {accent_color};
    --secondary: {secondary_color};
    --card-bg: {card_bg};
    --card-text: {card_text};
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    /* Hide x-overflow to prevent horizontal scrollbars during parallax calculation */
    overflow-x: hidden; 
}}

/* Sections represent the distinct visual blocks */
.section {{
    display: flex;
    align-items: center;
    justify-content: center;
    /* Use dynamic viewport height, but respect the minimum requested height */
    height: 100vh;
    min-height: {height_px}px;
    width: 100%;
    position: relative;
}}

/* High-contrast foreground cards */
.card {{
    background: var(--card-bg);
    color: var(--card-text);
    padding: 24px 48px;
    border-radius: 16px;
    text-align: center;
    box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    z-index: 10;
}}

.card h2 {{
    font-size: 3.5rem;
    font-weight: 800;
    margin-bottom: 0.5rem;
    letter-spacing: -1px;
}}

.card p {{
    font-size: 1.25rem;
    opacity: 0.8;
}}

/* -- Parallax Implementations -- */

.js-parallax {{
    background-image: url('https://images.unsplash.com/photo-1555066931-4365d14bab8c?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80');
    background-size: cover;
    background-position: center 0px;
    background-repeat: no-repeat;
    /* Hint to browser for scroll performance */
    will-change: background-position;
}}

.css-parallax {{
    background-image: url('https://images.unsplash.com/photo-1517694712202-14dd9538aa97?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80');
    background-size: cover;
    background-position: center center;
    background-repeat: no-repeat;
    /* Native CSS Parallax */
    background-attachment: fixed;
}}

/* Solid color dividing sections */
.solid-accent {{
    background-color: var(--accent);
}}

.solid-secondary {{
    background-color: var(--secondary);
}}

/* Accessibility: Disable parallax for users sensitive to motion */
@media (prefers-reduced-motion: reduce) {{
    .js-parallax, .css-parallax {{
        background-attachment: scroll !important;
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
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    
    <!-- Section 1: Javascript-driven Fractional Parallax -->
    <div class="section js-parallax" id="parallax">
        <div class="card">
            <h2>{title_text}</h2>
            <p>{body_text}</p>
        </div>
    </div>

    <!-- Section 2: Solid Dividing Block -->
    <div class="section solid-accent">
        <div class="card">
            <h2>DIV 2</h2>
            <p>Solid Color Divider</p>
        </div>
    </div>

    <!-- Section 3: CSS-driven Fixed Parallax -->
    <div class="section css-parallax">
        <div class="card">
            <h2>DIV 3: CSS Parallax</h2>
            <p>background-attachment: fixed</p>
        </div>
    </div>

    <!-- Section 4: Secondary Solid Dividing Block -->
    <div class="section solid-secondary">
        <div class="card">
            <h2>DIV 4</h2>
            <p>End of Sequence</p>
        </div>
    </div>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Dual-Method Parallax Scrolling Logic
document.addEventListener('DOMContentLoaded', () => {{
    const parallaxEl = document.getElementById('parallax');
    
    // Check if user has requested reduced motion for accessibility
    const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');

    // Use requestAnimationFrame to optimize scroll event handling and prevent layout jank
    let ticking = false;

    window.addEventListener('scroll', () => {{
        // Abort calculation if reduced motion is enabled
        if (prefersReducedMotion.matches) return;

        let offset = window.pageYOffset || document.documentElement.scrollTop;

        if (!ticking) {{
            window.requestAnimationFrame(() => {{
                // Multiplier 0.7 makes the background image move slightly slower 
                // than the page scroll, creating a sense of distance.
                parallaxEl.style.backgroundPositionY = (offset * 0.7) + 'px';
                ticking = false;
            }});
            ticking = true;
        }}
    }});
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

* **Accessibility (`prefers-reduced-motion`)**: The provided code explicitly implements a media query check in CSS and a `matchMedia` check in Javascript. If a user has "Reduced Motion" configured at the OS level, the backgrounds will gracefully fallback to standard scrolling (`background-attachment: scroll`), preventing nausea or discomfort.
* **Performance (Scroll Jank)**: Rather than firing DOM style updates directly inside the `scroll` event listener (which can fire dozens of times per second and block the main thread), the JavaScript wraps the recalculation in `requestAnimationFrame`. This guarantees the style updates are synchronized with the display's refresh rate. Additionally, `will-change: background-position;` is set in CSS to trigger GPU layer promotion.