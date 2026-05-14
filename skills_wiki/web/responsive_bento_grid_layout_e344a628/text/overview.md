# Responsive Bento Grid Layout

## Analysis

# Role: Agent_Skill_Distiller (Web Component Design & Pattern Extractor)

## 1. High-level Design Pattern Extraction

> **Skill Name**: Responsive Bento Grid Layout

* **Core Visual Mechanism**: The defining visual idea is a highly structured, compartmentalized layout resembling a Japanese bento box. It uses CSS Grid's `grid-template-areas` to arrange distinct "cards" or "widgets" that span multiple columns and rows, creating a visually pleasing hierarchy of information without rigid uniformity. 
* **Why Use This Skill (Rationale)**: Bento grids excel at organizing heterogeneous content (text, numbers, charts, images) into a unified, scannable format. By giving some items larger spatial footprints (spanning 2x2 grid tracks), designers can establish clear visual primacy for key features or metrics, while secondary information fits neatly into smaller adjacent blocks.
* **Overall Applicability**: This pattern is highly prevalent in modern web design, particularly for SaaS landing pages highlighting product features, application dashboards, portfolio galleries, and "link-in-bio" personal pages.
* **Value Addition**: Compared to standard linear stacking or basic flexbox wrapping, a Bento grid provides a dynamic, magazine-like composition. Using `grid-template-areas` allows developers to map the visual layout directly in the CSS code, making it incredibly intuitive to manage and rearrange across different screen sizes.
* **Browser Compatibility**: Requires modern browsers supporting CSS Grid and `grid-template-areas` (supported in all major browsers since 2017).

## 2. Visual & Technical Breakdown

* **Step A: Core Visual Elements**
  - **Structure**: A parent container (`div.bento-container`) holding multiple child items (`div.bento-item`).
  - **Color Logic**: Usually utilizes a contrasting background to make the cards pop. For a dark theme: Background `#0f172a`, Card Background `rgba(30, 41, 59, 0.7)` with subtle borders `rgba(255, 255, 255, 0.1)`. For light: Background `#f8fafc`, Card Background `#ffffff` with soft shadows.
  - **Typographic Hierarchy**: Bold, clear headings inside cards with secondary text. Font: `Inter` or similar modern sans-serif.
  - **Styling properties**: `border-radius` (typically large, e.g., 24px), `padding`, `gap`, `box-shadow`, and `backdrop-filter` for modern sleekness.

* **Step B: Layout & Compositional Style**
  - **Layout System**: Pure CSS Grid.
  - **Assignment**: Each child element is assigned a unique name using `grid-area: identifier;`.
  - **Composition**: The parent uses `grid-template-areas` to "draw" the layout using strings.
    - Example base layout (4 columns): 
      `"main main top-right far-right"`
      `"main main bottom-mid bottom-right"`
  - **Proportions**: Columns often use `1fr` to divide space evenly. Rows use fixed sizes (e.g., `200px`) or `minmax()` combined with implicit grids (`grid-auto-rows`).

* **Step C: Interactive Behavior & Animations**
  - **Hover Effects**: Subtle scaling (`transform: translateY(-4px)`) and shadow elevation on hover.
  - **Transitions**: Smooth easing on transforms `transition: transform 0.3s ease, box-shadow 0.3s ease`.
  - **Responsiveness**: Media queries redefine the `grid-template-areas` string, instantly snapping the layout into new formations (e.g., from a 4-column desktop layout to a 3-column tablet layout, down to a single-column mobile stack).

## 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| Core Grid Layout | CSS Grid (`grid-template-areas`) | It maps visual layout directly to code via string representations, making complex spanning and rearranging trivial. |
| Area Assignment | CSS `grid-area` property | Native mapping property required by `grid-template-areas`. |
| Responsive Reflow | CSS Media Queries | Redefining the `grid-template-areas` string in media queries is the cleanest way to radically alter a grid layout without JS DOM manipulation. |
| Card Aesthetics | CSS styling (border-radius, shadows) | Provides the distinct "bento box" visual separation. |

#### 3b. Complete Reproduction Code

```python
def create_component(
    output_dir: str,
    title_text: str = "Feature Highlights",
    body_text: str = "Everything you need, neatly organized.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#6366f1",     # Indigo accent
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Responsive Bento Grid Layout.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Derive theme colors
    if color_scheme == "dark":
        bg_color = "#0f172a"          # slate-900
        text_color = "#f8fafc"        # slate-50
        text_muted = "#94a3b8"        # slate-400
        card_bg = "#1e293b"           # slate-800
        card_border = "rgba(255, 255, 255, 0.05)"
        shadow = "0 25px 50px -12px rgba(0, 0, 0, 0.5)"
    else:
        bg_color = "#f8fafc"          # slate-50
        text_color = "#0f172a"        # slate-900
        text_muted = "#64748b"        # slate-500
        card_bg = "#ffffff"           # white
        card_border = "rgba(0, 0, 0, 0.05)"
        shadow = "0 20px 25px -5px rgba(0, 0, 0, 0.05), 0 8px 10px -6px rgba(0, 0, 0, 0.01)"

    # === CSS ===
    css = f"""/* Responsive Bento Grid Layout */
:root {{
    --bg-color: {bg_color};
    --text-main: {text_color};
    --text-muted: {text_muted};
    --card-bg: {card_bg};
    --card-border: {card_border};
    --accent: {accent_color};
    --shadow: {shadow};
    --container-width: {width_px}px;
}}

* {{
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}}

body {{
    font-family: 'Inter', system-ui, sans-serif;
    background-color: var(--bg-color);
    color: var(--text-main);
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 2rem;
}}

header {{
    text-align: center;
    margin-bottom: 3rem;
    max-width: 600px;
}}

header h1 {{
    font-size: 2.5rem;
    font-weight: 700;
    margin-bottom: 0.75rem;
    letter-spacing: -0.025em;
}}

header p {{
    color: var(--text-muted);
    font-size: 1.125rem;
}}

/* Bento Grid Core Logic */
.bento-container {{
    display: grid;
    /* Desktop: 4 columns, roughly 200px rows */
    grid-template-columns: repeat(4, 1fr);
    grid-auto-rows: minmax(220px, auto);
    gap: 1.25rem;
    width: 100%;
    max-width: var(--container-width);
    
    /* The Magic String mapping the layout */
    grid-template-areas:
        "hero hero card1 card2"
        "hero hero card3 card4";
}}

/* Assigning Grid Areas to specific elements */
.item-hero {{ grid-area: hero; }}
.item-1 {{ grid-area: card1; }}
.item-2 {{ grid-area: card2; }}
.item-3 {{ grid-area: card3; }}
.item-4 {{ grid-area: card4; }}

/* Card Aesthetics */
.bento-item {{
    background-color: var(--card-bg);
    border: 1px solid var(--card-border);
    border-radius: 24px;
    padding: 2rem;
    display: flex;
    flex-direction: column;
    justify-content: flex-end;
    overflow: hidden;
    position: relative;
    box-shadow: var(--shadow);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    opacity: 0; /* For JS animation */
    transform: translateY(20px);
}}

.bento-item:hover {{
    transform: translateY(-4px);
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
}}

/* Internal Card Styling */
.card-icon {{
    position: absolute;
    top: 1.5rem;
    left: 1.5rem;
    width: 48px;
    height: 48px;
    background: rgba(99, 102, 241, 0.1);
    color: var(--accent);
    border-radius: 14px;
    display: flex;
    align-items: center;
    justify-content: center;
}}

.card-icon svg {{ width: 24px; height: 24px; fill: currentColor; }}

h3 {{
    font-size: 1.25rem;
    font-weight: 600;
    margin-bottom: 0.5rem;
    z-index: 1;
}}

.item-hero h3 {{
    font-size: 2rem;
}}

p {{
    color: var(--text-muted);
    font-size: 0.95rem;
    line-height: 1.5;
    z-index: 1;
}}

/* Visual flair for the hero item */
.item-hero::before {{
    content: '';
    position: absolute;
    top: -50%;
    right: -20%;
    width: 300px;
    height: 300px;
    background: radial-gradient(circle, var(--accent) 0%, transparent 70%);
    opacity: 0.15;
    filter: blur(40px);
    z-index: 0;
}}

/* === Responsive Layout Reflows === */

/* Tablet (Max 900px) */
@media (max-width: 900px) {{
    .bento-container {{
        grid-template-columns: repeat(3, 1fr);
        grid-template-areas:
            "hero hero card1"
            "hero hero card2"
            "card3 card4 card4";
    }}
}}

/* Mobile (Max 600px) */
@media (max-width: 600px) {{
    .bento-container {{
        grid-template-columns: 1fr;
        grid-template-areas:
            "hero"
            "card1"
            "card2"
            "card3"
            "card4";
    }}
}}

/* JS Animation Class */
.bento-item.visible {{
    opacity: 1;
    transform: translateY(0);
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
    
    <header>
        <h1>{title_text}</h1>
        <p>{body_text}</p>
    </header>

    <div class="bento-container">
        
        <!-- Hero Span (2x2 usually) -->
        <div class="bento-item item-hero" style="transition-delay: 0.1s">
            <div class="card-icon">
                <svg viewBox="0 0 24 24"><path d="M12 2L2 22h20L12 2zm0 3.8l7.5 14.2H4.5L12 5.8z"/></svg>
            </div>
            <h3>Powerful Infrastructure</h3>
            <p>Designed to scale infinitely with your needs, bridging the gap between complexity and performance seamlessly.</p>
        </div>

        <!-- Standard Cards -->
        <div class="bento-item item-1" style="transition-delay: 0.2s">
            <div class="card-icon">
                <svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="8" fill="none" stroke="currentColor" stroke-width="2"/></svg>
            </div>
            <h3>Real-time</h3>
            <p>Sub-millisecond latency.</p>
        </div>

        <div class="bento-item item-2" style="transition-delay: 0.3s">
            <div class="card-icon">
                <svg viewBox="0 0 24 24"><rect x="4" y="4" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2"/></svg>
            </div>
            <h3>Customizable</h3>
            <p>Adapt to any brand.</p>
        </div>

        <div class="bento-item item-3" style="transition-delay: 0.4s">
            <div class="card-icon">
                <svg viewBox="0 0 24 24"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z" fill="none" stroke="currentColor" stroke-width="2"/></svg>
            </div>
            <h3>Secure</h3>
            <p>Enterprise grade.</p>
        </div>

        <div class="bento-item item-4" style="transition-delay: 0.5s">
            <div class="card-icon">
                <svg viewBox="0 0 24 24"><path d="M4 12l6 6L20 6" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
            </div>
            <h3>Reliable</h3>
            <p>99.99% uptime SLA.</p>
        </div>

    </div>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Responsive Bento Grid Layout — Entry Animations
document.addEventListener('DOMContentLoaded', () => {{
    // Simple staggered reveal animation
    const items = document.querySelectorAll('.bento-item');
    
    // Use Intersection Observer for scroll-triggered animation
    const observer = new IntersectionObserver((entries) => {{
        entries.forEach(entry => {{
            if (entry.isIntersecting) {{
                entry.target.classList.add('visible');
                observer.unobserve(entry.target);
            }}
        }});
    }}, {{ threshold: 0.1 }});

    items.forEach(item => {{
        observer.observe(item);
    }});
}});
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

## 4. Accessibility & Performance Notes

* **Accessibility**: The semantic structure is maintained. However, if focus order matters (e.g., users pressing `Tab` to navigate through items), be aware that CSS Grid changes visual order but **not** DOM order. Make sure the HTML DOM source order follows a logical reading structure regardless of how `grid-template-areas` moves them visually. 
* **Performance**: This method is highly performant. CSS Grid calculations are native and GPU accelerated. Responsive reflows utilizing media queries and string reassignment (`grid-template-areas: ...`) avoid heavy JavaScript window resize listeners, preventing layout thrashing and jank. The stagger animations use `transform` and `opacity` which do not trigger expensive layout repaints.