# Role: Agent_Skill_Distiller (Web Component Design & Pattern Extractor)

### 1. High-level Design Pattern Extraction

> **Skill Name**: Asymmetrical Responsive Bento Grid

* **Core Visual Mechanism**: The defining visual idea is the "Bento Box" layout—an asymmetrical, interlocking grid of cards with varying proportions (e.g., a large feature square, wide rectangles, and small squares) that fit together like puzzle pieces. This is achieved natively using CSS Grid's `grid-template-areas` combined with fractional units (`fr`), allowing elements to span multiple columns and rows seamlessly.
* **Why Use This Skill (Rationale)**: The Bento Grid breaks the visual monotony of uniform card layouts. By assigning different spatial weights to different containers, it natively enforces visual hierarchy. Large areas naturally draw the eye (perfect for a hero graphic or primary feature), while smaller areas act as supporting metadata or secondary actions. It feels highly modern, structured, and intentional.
* **Overall Applicability**: This pattern is heavily trending in modern web design, popularized by companies like Apple. It is perfectly suited for SaaS product feature highlights, creative portfolio galleries, dashboard summary widgets, and stylized pricing or "About Us" sections.
* **Value Addition**: Compared to standard Flexbox rows or standard HTML stacking, CSS Grid with named areas provides a two-dimensional layout system that is decoupled from the DOM order. This means you can completely restructure the visual layout for mobile, tablet, and desktop without altering the HTML structure, providing a massive accessibility and SEO advantage.
* **Browser Compatibility**: Fully supported in all modern browsers. CSS Grid (`grid-template-areas`, `fr` units) has been universally supported since late 2017.

### 2. Visual & Technical Breakdown

* **Step A: Core Visual Elements**
  - **Containers**: Distinct semantic `div` or `article` elements representing individual cards.
  - **Styling**: Soft border radiuses (e.g., `16px` to `24px`), subtle box shadows or inner borders, and flat or gently gradated background colors.
  - **Color Logic**: In dark mode, a deep background (`#0d111c`) with slightly elevated card surfaces (`#1a1f2e`). In light mode, a soft off-white background (`#f0f2f5`) with stark white cards (`#ffffff`). The specified accent color highlights icons or key typography.
  - **Typography**: Clean sans-serif hierarchy (Inter or system-ui), with bold, compact titles and subdued, high-contrast body text.

* **Step B: Layout & Compositional Style**
  - **Layout System**: Pure CSS Grid.
  - **Grid Definition**: The parent uses `display: grid; gap: 1.5rem;`.
  - **Desktop Alignment (4 columns)**: 
    ```css
    grid-template-areas: 
      "box-1 box-1 box-2 box-3"
      "box-1 box-1 box-4 box-5";
    ```
    This allocates 50% of the width and 100% of the height to `box-1`, while the other boxes act as quadrants on the right side.
  - **Proportions**: Columns use `1fr` (equal fractional distribution). Rows use `minmax(220px, auto)` to ensure they never collapse too small but can grow if content demands it.

* **Step C: Interactive Behavior & Animations**
  - **Hover Effects**: Pure CSS micro-interactions on the cards—a slight upward lift (`transform: translateY(-4px)`) and a shadow expansion, transitioned smoothly over `0.3s cubic-bezier(0.4, 0, 0.2, 1)`.
  - **Entrance Animation**: JavaScript-driven `IntersectionObserver` that adds a `.visible` class to items as they enter the viewport, triggering a staggered fade-in and slide-up effect (`@keyframes`).

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| Asymmetrical Puzzle Layout | CSS Grid `grid-template-areas` | The most declarative, readable, and robust way to create spanning layouts in 2D space without messy flexbox wrapping. |
| Responsive Restructuring | CSS Media Queries | Natively swaps `grid-template-areas` strings for tablet and mobile sizes, rearranging the layout entirely. |
| Card Aesthetics | CSS standard properties | `border-radius`, `box-shadow`, and `background-color` accurately recreate the clean UI aesthetic. |
| Staggered Entrance | JavaScript `IntersectionObserver` | Highly performant way to detect when the grid enters the viewport and trigger staggered CSS animations. |
| Icons | Font Awesome CDN | Provides immediate, recognizable vector icons to populate the layout without cluttering the HTML with raw SVGs. |

> **Feasibility Assessment**: 100% reproduction. The CSS Grid layout mechanism shown in the tutorial is fully achievable with plain CSS, and the resulting component is highly robust and completely self-contained.

#### 3b. Complete Reproduction Code

```python
def create_component(
    output_dir: str,
    title_text: str = "Features that adapt to you.",
    body_text: str = "Our bento-style dashboard organizes everything you need into a beautiful, glanceable hierarchy.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#6366f1",     # CSS hex color for accent (Indigo)
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Asymmetrical Responsive Bento Grid.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors ===
    if color_scheme == "dark":
        bg_color = "#0b0f19"
        text_primary = "#f8fafc"
        text_secondary = "#94a3b8"
        card_bg = "#111827"
        card_border = "rgba(255, 255, 255, 0.05)"
        shadow = "0 10px 30px -10px rgba(0, 0, 0, 0.5)"
        hover_shadow = "0 20px 40px -10px rgba(0, 0, 0, 0.7)"
    else:
        bg_color = "#f1f5f9"
        text_primary = "#0f172a"
        text_secondary = "#475569"
        card_bg = "#ffffff"
        card_border = "rgba(0, 0, 0, 0.05)"
        shadow = "0 10px 30px -10px rgba(0, 0, 0, 0.05)"
        hover_shadow = "0 20px 40px -10px rgba(0, 0, 0, 0.1)"

    # === CSS ===
    css = f"""/* Asymmetrical Responsive Bento Grid */
:root {{
    --bg-color: {bg_color};
    --text-primary: {text_primary};
    --text-secondary: {text_secondary};
    --accent-color: {accent_color};
    --card-bg: {card_bg};
    --card-border: {card_border};
    --shadow: {shadow};
    --hover-shadow: {hover_shadow};
    --max-width: {width_px}px;
}}

* {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background-color: var(--bg-color);
    color: var(--text-primary);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 2rem;
}}

.bento-wrapper {{
    width: 100%;
    max-width: var(--max-width);
    display: flex;
    flex-direction: column;
    gap: 3rem;
}}

.bento-header {{
    text-align: center;
    max-width: 600px;
    margin: 0 auto;
}}

.bento-header h1 {{
    font-size: clamp(2rem, 4vw, 3rem);
    font-weight: 700;
    letter-spacing: -0.02em;
    margin-bottom: 1rem;
    line-height: 1.1;
}}

.bento-header p {{
    font-size: 1.125rem;
    color: var(--text-secondary);
    line-height: 1.6;
}}

/* === Grid Layout Core === */
.bento-grid {{
    display: grid;
    gap: 1.5rem;
    /* Desktop layout by default */
    grid-template-columns: repeat(4, 1fr);
    grid-auto-rows: minmax(240px, auto);
    grid-template-areas: 
        "box-1 box-1 box-2 box-3"
        "box-1 box-1 box-4 box-5";
}}

/* Grid Area Assignments */
.box-1 {{ grid-area: box-1; }}
.box-2 {{ grid-area: box-2; }}
.box-3 {{ grid-area: box-3; }}
.box-4 {{ grid-area: box-4; }}
.box-5 {{ grid-area: box-5; }}

/* === Card Styling === */
.bento-card {{
    background: var(--card-bg);
    border: 1px solid var(--card-border);
    border-radius: 24px;
    padding: 2rem;
    box-shadow: var(--shadow);
    transition: transform 0.4s cubic-bezier(0.16, 1, 0.3, 1), box-shadow 0.4s ease;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    overflow: hidden;
    position: relative;
    
    /* Animation initial state */
    opacity: 0;
    transform: translateY(30px);
}}

.bento-card:hover {{
    transform: translateY(-8px);
    box-shadow: var(--hover-shadow);
}}

.bento-card.visible {{
    opacity: 1;
    transform: translateY(0);
}}

/* Staggering the entrance animation */
.box-1.visible {{ transition-delay: 0.1s; }}
.box-2.visible {{ transition-delay: 0.2s; }}
.box-3.visible {{ transition-delay: 0.3s; }}
.box-4.visible {{ transition-delay: 0.4s; }}
.box-5.visible {{ transition-delay: 0.5s; }}

/* Card Internal Layout */
.card-icon {{
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 48px;
    height: 48px;
    border-radius: 12px;
    background: color-mix(in srgb, var(--accent-color) 15%, transparent);
    color: var(--accent-color);
    font-size: 1.5rem;
    margin-bottom: 1.5rem;
}}

.box-1 .card-icon {{
    width: 64px;
    height: 64px;
    font-size: 2rem;
    border-radius: 16px;
}}

.card-content h3 {{
    font-size: 1.25rem;
    font-weight: 600;
    margin-bottom: 0.5rem;
}}

.box-1 .card-content h3 {{
    font-size: 2rem;
    margin-bottom: 1rem;
}}

.card-content p {{
    color: var(--text-secondary);
    font-size: 0.95rem;
    line-height: 1.5;
}}

.box-1 .card-content p {{
    font-size: 1.1rem;
}}

/* Decorative Background Element */
.bento-card::before {{
    content: '';
    position: absolute;
    top: 0;
    right: 0;
    width: 150px;
    height: 150px;
    background: radial-gradient(circle, color-mix(in srgb, var(--accent-color) 20%, transparent) 0%, transparent 70%);
    border-radius: 50%;
    transform: translate(30%, -30%);
    z-index: 0;
    pointer-events: none;
}}

/* === Responsive Layout Adjustments === */

/* Tablet Layout */
@media (max-width: 1024px) {{
    .bento-grid {{
        grid-template-columns: repeat(3, 1fr);
        grid-template-areas: 
            "box-1 box-1 box-2"
            "box-1 box-1 box-3"
            "box-4 box-5 box-5";
    }}
}}

/* Small Tablet / Large Mobile Layout */
@media (max-width: 768px) {{
    .bento-grid {{
        grid-template-columns: repeat(2, 1fr);
        grid-template-areas: 
            "box-1 box-1"
            "box-2 box-3"
            "box-4 box-5";
    }}
}}

/* Mobile Layout */
@media (max-width: 480px) {{
    .bento-grid {{
        grid-template-columns: 1fr;
        grid-template-areas: 
            "box-1"
            "box-2"
            "box-3"
            "box-4"
            "box-5";
    }}
    .bento-card {{
        padding: 1.5rem;
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
    <!-- Inter Font -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <!-- Font Awesome Icons -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link rel="stylesheet" href="style.css">
</head>
<body>

    <div class="bento-wrapper">
        <header class="bento-header">
            <h1>{title_text}</h1>
            <p>{body_text}</p>
        </header>

        <main class="bento-grid">
            <!-- Box 1: Large Feature -->
            <article class="bento-card box-1">
                <div class="card-icon">
                    <i class="fa-solid fa-chart-line"></i>
                </div>
                <div class="card-content">
                    <h3>Powerful Analytics</h3>
                    <p>Gain deep insights into your workflow with our advanced metrics engine. See exactly where your time goes and optimize processes in real-time without leaving your dashboard.</p>
                </div>
            </article>

            <!-- Box 2: Standard Card -->
            <article class="bento-card box-2">
                <div class="card-icon">
                    <i class="fa-solid fa-bolt"></i>
                </div>
                <div class="card-content">
                    <h3>Lightning Fast</h3>
                    <p>Optimized for speed and efficiency.</p>
                </div>
            </article>

            <!-- Box 3: Standard Card -->
            <article class="bento-card box-3">
                <div class="card-icon">
                    <i class="fa-solid fa-shield-halved"></i>
                </div>
                <div class="card-content">
                    <h3>Secure Core</h3>
                    <p>Enterprise-grade security built-in.</p>
                </div>
            </article>

            <!-- Box 4: Standard Card -->
            <article class="bento-card box-4">
                <div class="card-icon">
                    <i class="fa-solid fa-cloud-arrow-up"></i>
                </div>
                <div class="card-content">
                    <h3>Cloud Sync</h3>
                    <p>Always backed up, everywhere.</p>
                </div>
            </article>

            <!-- Box 5: Standard Card -->
            <article class="bento-card box-5">
                <div class="card-icon">
                    <i class="fa-solid fa-wand-magic-sparkles"></i>
                </div>
                <div class="card-content">
                    <h3>AI Assisted</h3>
                    <p>Smart tools that learn your habits and adapt to you.</p>
                </div>
            </article>
        </main>
    </div>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Intersection Observer for Staggered Entrance Animations
document.addEventListener('DOMContentLoaded', () => {{
    const bentoCards = document.querySelectorAll('.bento-card');

    const observerOptions = {{
        root: null,
        rootMargin: '0px',
        threshold: 0.15 // Trigger when 15% of the card is visible
    }};

    const cardObserver = new IntersectionObserver((entries, observer) => {{
        entries.forEach(entry => {{
            if (entry.isIntersecting) {{
                // Add visible class to trigger CSS transition
                entry.target.classList.add('visible');
                // Stop observing once animated
                observer.unobserve(entry.target);
            }}
        }});
    }}, observerOptions);

    // Initialize observer for each card
    bentoCards.forEach(card => {{
        cardObserver.observe(card);
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
  - The layout order via `grid-template-areas` visually changes the presentation, but the underlying HTML DOM structure remains logical (Box 1 through 5 sequentially). Screen readers will read the content in this correct DOM order regardless of where CSS Grid visually places the boxes.
  - Semantic `<article>`, `<header>`, and `<main>` tags are utilized to clearly outline page regions to assistive technologies.
  - The `color-mix` utility used to generate background tints around icons ensures a cohesive aesthetic while maintaining the high contrast needed for WCAG AA text legibility on both dark and light modes.
* **Performance**:
  - **CSS Grid Native Power**: The responsive shifts completely avoid JavaScript `window.resize` listeners. `grid-template-areas` combined with media queries is natively optimized by browser rendering engines.
  - **Animation Optimization**: The hover and entrance animations exclusively animate `opacity` and `transform`. This pushes the workload to the GPU compositor thread, preventing layout thrashing and repaints. 
  - **Intersection Observer**: Avoids costly `scroll` event listeners. The API runs asynchronously without blocking the main JavaScript thread, keeping the entrance animations buttery smooth (60fps).