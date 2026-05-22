# Role: Agent_Skill_Distiller (Web Component Design & Pattern Extractor)

### 1. High-level Design Pattern Extraction

> **Skill Name**: Responsive Bento Grid Showcase

* **Core Visual Mechanism**: The "Bento Grid" is an asymmetric, interlocking card layout inspired by Japanese bento boxes. It uses CSS `grid-template-areas` to assign specific HTML elements to exact, multi-row and multi-column spatial slots. This creates a highly structured but dynamic masonry-like puzzle where "hero" items take up large blocks (e.g., 2x2) while secondary features occupy smaller blocks (1x1 or 2x1), creating a bounded, perfect rectangular silhouette.
* **Why Use This Skill (Rationale)**: The Bento Grid excels at visual hierarchy. By mixing varying card dimensions within a unified, rigid grid, it guides the user's eye from the most critical information (the largest box) to supporting details (smaller boxes) without overwhelming them. It feels clean, highly organized, and mathematically satisfying.
* **Overall Applicability**: This is a trending layout pattern for SaaS product feature sections, personal portfolios, dashboard overviews, and Apple-style hardware specification pages.
* **Value Addition**: Compared to standard linear columns or rows, a Bento Grid breaks the monotony of uniform lists. It injects a sense of premium editorial design and allows developers to showcase different types of content (images, charts, short text, bold numbers) together without them clashing.
* **Browser Compatibility**: Fully supported in all modern browsers (Chrome, Firefox, Safari, Edge) as it relies on standard CSS Grid (`display: grid`, `grid-template-areas`, `gap`). 

### 2. Visual & Technical Breakdown

* **Step A: Core Visual Elements**
  - **Containers**: A parent `.bento-grid` containing multiple `.bento-item` children (cards).
  - **Color Logic**: A distinct contrast between the main background and the cards. For dark mode, a deep background (`#0a0e17`) with lighter cards (`rgba(255, 255, 255, 0.05)`) and a subtle inner border (`rgba(255, 255, 255, 0.1)`) creates a premium glass/surface effect.
  - **Typography**: Clean, sans-serif fonts (e.g., Inter) with strong weight contrasts (bold titles, subdued light-grey descriptions).
  - **CSS Properties**: `border-radius` (typically large, e.g., 24px, to emphasize the "box" feel), `gap` (consistent spacing, e.g., 1.5rem), and `box-shadow` for depth.

* **Step B: Layout & Compositional Style**
  - **Layout System**: CSS Grid. 
  - **Strategy**: Instead of letting elements flow automatically, the layout explicitly draws a map using `grid-template-areas`. 
  - **Proportions**: A 4-column layout on desktop, condensing to a 2-column layout on tablets, and a 1-column stack on mobile. `grid-auto-rows: minmax(180px, auto)` ensures boxes have a uniform baseline height but can stretch if content demands it.

* **Step C: Interactive Behavior & Animations**
  - **Hover Effects**: A pure CSS scale effect (`transform: translateY(-4px) scale(1.01)`) with a subtle shadow boost to make the cards feel tactile.
  - **JS Enhancement**: A modern "glow" effect where JavaScript tracks the mouse position over the grid and translates it into CSS variables (`--mouse-x`, `--mouse-y`), moving a soft radial gradient highlight across the card surfaces.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| Asymmetric layout | CSS `grid-template-areas` | Allows precise, visual string-based mapping of how boxes span columns and rows. |
| Responsive breakpoints | CSS Media Queries | Effortlessly redraws the `grid-template-areas` map for tablet and mobile without touching JS. |
| Uniform card sizing | CSS `grid-auto-rows` | Ensures all baseline rows share a minimum height (`minmax`), keeping the Bento boxes perfectly aligned. |
| Interactive hover glow | JS + CSS Custom Properties | JS computes local mouse coordinates and passes them to CSS for a performant `radial-gradient` mask. |

#### 3b. Complete Reproduction Code

```python
def create_component(
    output_dir: str,
    title_text: str = "Discover Our Features",
    body_text: str = "A powerful, asymmetric grid layout for highlighting key capabilities.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#6366f1",     # CSS hex color for accent
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Responsive Bento Grid visual effect.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme ===
    if color_scheme == "dark":
        bg_color = "#0f172a"
        text_primary = "#f8fafc"
        text_secondary = "#94a3b8"
        card_bg = "rgba(30, 41, 59, 0.7)"
        card_border = "rgba(255, 255, 255, 0.08)"
        glow_color = f"{accent_color}33" # 20% opacity hex
    else:
        bg_color = "#f8fafc"
        text_primary = "#0f172a"
        text_secondary = "#64748b"
        card_bg = "rgba(255, 255, 255, 0.9)"
        card_border = "rgba(0, 0, 0, 0.08)"
        glow_color = f"{accent_color}22"

    # === CSS ===
    css = f"""/* Responsive Bento Grid Showcase */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --text-primary: {text_primary};
    --text-secondary: {text_secondary};
    --accent: {accent_color};
    --card-bg: {card_bg};
    --card-border: {card_border};
    --glow-color: {glow_color};
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background: var(--bg);
    color: var(--text-primary);
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 2rem;
}}

/* Header Section */
.header {{
    text-align: center;
    margin-bottom: 3rem;
    max-width: 600px;
}}

.header h1 {{
    font-size: 2.5rem;
    font-weight: 700;
    margin-bottom: 1rem;
    letter-spacing: -0.025em;
}}

.header p {{
    color: var(--text-secondary);
    font-size: 1.125rem;
    line-height: 1.6;
}}

/* Bento Grid Container */
.bento-grid {{
    display: grid;
    width: 100%;
    max-width: {width_px}px;
    gap: 1.5rem;
    
    /* Desktop Layout: 4 columns */
    grid-template-columns: repeat(4, 1fr);
    grid-auto-rows: minmax(180px, auto);
    
    /* The Magic Map */
    grid-template-areas:
        "hero hero item1 item2"
        "hero hero item3 item3"
        "item4 item5 item5 item6";
}}

/* Individual Grid Area Assignments */
.bento-item:nth-child(1) {{ grid-area: hero; }}
.bento-item:nth-child(2) {{ grid-area: item1; }}
.bento-item:nth-child(3) {{ grid-area: item2; }}
.bento-item:nth-child(4) {{ grid-area: item3; }}
.bento-item:nth-child(5) {{ grid-area: item4; }}
.bento-item:nth-child(6) {{ grid-area: item5; }}
.bento-item:nth-child(7) {{ grid-area: item6; }}

/* Bento Card Styling */
.bento-item {{
    background: var(--card-bg);
    border: 1px solid var(--card-border);
    border-radius: 24px;
    padding: 2rem;
    display: flex;
    flex-direction: column;
    justify-content: flex-end;
    position: relative;
    overflow: hidden;
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1), box-shadow 0.3s ease;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
}}

/* JS Mouse Glow Effect */
.bento-item::before {{
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: radial-gradient(
        800px circle at var(--mouse-x, -500px) var(--mouse-y, -500px),
        var(--glow-color),
        transparent 40%
    );
    z-index: 0;
    pointer-events: none;
    opacity: 0;
    transition: opacity 0.5s ease;
}}

.bento-item:hover::before {{
    opacity: 1;
}}

.bento-item:hover {{
    transform: translateY(-4px) scale(1.01);
    box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
}}

/* Content z-index to stay above glow */
.bento-content {{
    position: relative;
    z-index: 1;
}}

.bento-icon {{
    display: flex;
    align-items: center;
    justify-content: center;
    width: 48px;
    height: 48px;
    background: var(--accent);
    color: #fff;
    border-radius: 14px;
    margin-bottom: auto;
    font-size: 1.5rem;
    font-weight: bold;
}}

.bento-title {{
    font-size: 1.25rem;
    font-weight: 600;
    margin-bottom: 0.5rem;
    margin-top: 1.5rem;
}}

.bento-desc {{
    color: var(--text-secondary);
    font-size: 0.95rem;
    line-height: 1.5;
}}

/* Special Hero Styling */
.bento-item:nth-child(1) .bento-title {{
    font-size: 2rem;
}}

.bento-item:nth-child(1) .bento-desc {{
    font-size: 1.1rem;
}}

/* Responsive Design */

/* Tablet Layout */
@media (max-width: 968px) {{
    .bento-grid {{
        grid-template-columns: repeat(2, 1fr);
        grid-template-areas:
            "hero hero"
            "hero hero"
            "item1 item2"
            "item3 item3"
            "item5 item5"
            "item4 item6";
    }}
}}

/* Mobile Layout */
@media (max-width: 640px) {{
    .bento-grid {{
        grid-template-columns: 1fr;
        grid-auto-rows: minmax(200px, auto);
        grid-template-areas:
            "hero"
            "item1"
            "item2"
            "item3"
            "item4"
            "item5"
            "item6";
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
    
    <div class="header">
        <h1>{title_text}</h1>
        <p>{body_text}</p>
    </div>

    <section class="bento-grid">
        <!-- Hero Card (2x2) -->
        <article class="bento-item">
            <div class="bento-content">
                <div class="bento-icon">✦</div>
                <h2 class="bento-title">Absolute Control</h2>
                <p class="bento-desc">Harness the power of CSS Grid template areas to explicitly place elements exactly where they belong across multiple viewports.</p>
            </div>
        </article>

        <!-- Standard Cards (1x1) -->
        <article class="bento-item">
            <div class="bento-content">
                <div class="bento-icon">1</div>
                <h2 class="bento-title">Responsive</h2>
                <p class="bento-desc">Adapts seamlessly from desktop to mobile.</p>
            </div>
        </article>

        <article class="bento-item">
            <div class="bento-content">
                <div class="bento-icon">2</div>
                <h2 class="bento-title">Fluid</h2>
                <p class="bento-desc">Fractional units distribute space perfectly.</p>
            </div>
        </article>

        <!-- Wide Card (2x1) -->
        <article class="bento-item">
            <div class="bento-content">
                <div class="bento-icon">⚡</div>
                <h2 class="bento-title">High Performance</h2>
                <p class="bento-desc">No heavy JS calculations required for the layout geometry.</p>
            </div>
        </article>

        <!-- Standard Card (1x1) -->
        <article class="bento-item">
            <div class="bento-content">
                <div class="bento-icon">3</div>
                <h2 class="bento-title">Clean</h2>
                <p class="bento-desc">Semantic HTML structures.</p>
            </div>
        </article>

        <!-- Wide Card (2x1) -->
        <article class="bento-item">
            <div class="bento-content">
                <div class="bento-icon">∞</div>
                <h2 class="bento-title">Infinite Combinations</h2>
                <p class="bento-desc">Redraw the grid-template map using media queries to completely restructure your UI instantly.</p>
            </div>
        </article>

        <!-- Standard Card (1x1) -->
        <article class="bento-item">
            <div class="bento-content">
                <div class="bento-icon">4</div>
                <h2 class="bento-title">Modern</h2>
                <p class="bento-desc">Apple & Windows UI inspired.</p>
            </div>
        </article>
    </section>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Mouse Glow Tracking
document.addEventListener('DOMContentLoaded', () => {{
    const bentoItems = document.querySelectorAll('.bento-item');

    // Update CSS custom properties based on mouse position
    const handleMouseMove = (e) => {{
        const target = e.currentTarget;
        const rect = target.getBoundingClientRect();
        
        // Calculate mouse position relative to the element
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        
        // Update CSS variables
        target.style.setProperty('--mouse-x', `${{x}}px`);
        target.style.setProperty('--mouse-y', `${{y}}px`);
    }};

    // Attach listeners to all bento cards
    bentoItems.forEach(item => {{
        item.addEventListener('mousemove', handleMouseMove);
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

* **Accessibility**:
  * Semantic HTML (`<section>`, `<article>`, `<h2>`, `<p>`) provides inherent document structure for screen readers.
  * Contrast ratios are deliberately maintained by defining explicit text colors mapped to specific dark/light backgrounds.
  * **To improve**: For production, consider wrapping hover animations inside `@media (prefers-reduced-motion: no-preference) { ... }` so users with vestibular disorders do not experience the Z-axis scaling when navigating with a mouse.
* **Performance**:
  * The layout is achieved using purely native CSS Grid, pushing the layout calculations strictly to the browser engine, avoiding JavaScript layout thrashing.
  * The interaction logic handles the hover "glow" effect extremely efficiently by utilizing a CSS `radial-gradient` that updates its origin coordinates via lightweight JS. This bypasses expensive canvas renders.
  * `transform` and `opacity` are used for hover animations, as these properties are GPU-accelerated and won't trigger browser repaints.