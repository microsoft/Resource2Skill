# Role: Agent_Skill_Distiller (Web Component Design & Pattern Extractor)

### 1. High-level Design Pattern Extraction

> **Skill Name**: Adaptive Bento Dashboard Grid

* **Core Visual Mechanism**: This pattern leverages a modern "Bento Box" aesthetic characterized by modular, perfectly interlocking cards of varying dimensions. It utilizes three advanced CSS Grid paradigms: 
    1. **Grid Areas** (`grid-template-areas`) for asymmetric, puzzle-like visual hierarchy (e.g., a large 2x2 hero card juxtaposed with 1x1 metric cards).
    2. **Grid Stacking** (assigning multiple elements to a single `"stack"` area) to layer backgrounds and text overlays without the brittleness of absolute positioning.
    3. **Auto-wrapping Grids** (`repeat(auto-fit, minmax(...))`) to create fluid item lists that dynamically spawn or collapse columns based on available viewport width, eliminating the need for complex media queries.

* **Why Use This Skill (Rationale)**: The Bento layout excels at chunking dense information into highly scannable, digestible modules. By sizing cards based on importance, it guides the user's eye naturally (e.g., Hero -> Key Metric -> Secondary Metrics). The Grid Stacking technique ensures content remains fluid and contained inside its cell, preventing the dreaded overflow issues typical of absolute positioning on responsive screens.

* **Overall Applicability**: Ideal for SaaS analytics dashboards, modern portfolio overviews, feature showcases on landing pages, and smart home control interfaces. Any scenario where varied data types (charts, text, status indicators) must coexist in a unified, grid-locked aesthetic.

* **Browser Compatibility**: Fully supported in all modern browsers. CSS Grid (`grid-template-areas`, `auto-fit`, `minmax`) has >96% global support. The Intersection Observer API (used for the entrance animation) is universally supported.


### 2. Visual & Technical Breakdown

* **Step A: Core Visual Elements**
  - **Containers**: Semantic `<section>` and `<div>` elements acting as Grid containers and items.
  - **Color Logic**: A deep/clean background (e.g., `#0f111a` dark or `#f9fafb` light) with elevated surface cards using slight transparency (`rgba(255, 255, 255, 0.05)`) and subtle borders (`1px solid rgba(255,255,255,0.1)`) to establish Z-depth.
  - **Typography**: Sans-serif (`Inter`), emphasizing high contrast in font weights—bold (`700`) for data values/headers, regular (`400`) for labels.
  - **CSS Properties**: `grid-template-areas`, `grid-template-columns`, `place-items`, `minmax()`, `backdrop-filter`.

* **Step B: Layout & Compositional Style**
  - **Bento Header**: A 4-column desktop layout. The main hero spans `2x2`, while four stat cards occupy `1x1` spaces each. This degrades gracefully to a 2-column tablet layout and a 1-column mobile stack.
  - **Grid Stacking**: Inside the hero card, `display: grid; grid-template-areas: "stack";` is applied. Both the gradient background and the text content are assigned to `grid-area: stack;`. 
  - **Auto-fit List**: A secondary row utilizes `grid-template-columns: repeat(auto-fit, minmax(240px, 1fr))` to let child cards figure out their own row/column flow automatically.
  - **Whitespace**: Standardized `1.5rem` grid gaps paired with `1.5rem` internal card padding ensures a unified, breathable spatial rhythm.

* **Step C: Interactive Behavior & Animations**
  - **Hover Dynamics**: Pure CSS `transform: translateY(-4px)` with enhanced `box-shadow` on hover provides tactile feedback.
  - **Scroll Reveal**: JavaScript `IntersectionObserver` triggers a cascading opacity and upward-slide reveal as the grid scrolls into view.
  - **Ambient Motion**: The hero card background employs a slow, continuously shifting `@keyframes` CSS gradient to draw primary attention.


### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| Asymmetric Layout | **CSS Grid Areas** | String-based mapping allows radical layout restructuring across breakpoints simply by rewriting the area strings. |
| Content Overlay | **CSS Grid Stacking** | Prevents text from overflowing the container and maintains DOM flow, vastly superior to `position: absolute`. |
| Fluid Item Lists | **Grid Auto-fit** | `repeat(auto-fit, minmax())` hands over column calculation to the browser rendering engine, avoiding JS window resizing math. |
| Cascade Animations | **JS Intersection Observer** | Highly performant native API to detect when cards enter the viewport, triggering CSS class changes without scroll-jank. |
| Iconography | **Font Awesome CDN** | Provides instant access to crisp, scalable vector icons to complete the "dashboard" illusion. |

#### 3b. Complete Reproduction Code

```python
def create_component(
    output_dir: str,
    title_text: str = "Overview Dashboard",
    body_text: str = "Real-time metrics and system status.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#6366f1",     # CSS hex color for accent
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Adaptive Bento Dashboard Grid layout.
    
    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme ===
    if color_scheme == "dark":
        bg_color = "#0f111a"
        text_color = "#f3f4f6"
        text_muted = "#9ca3af"
        surface_color = "rgba(255, 255, 255, 0.05)"
        surface_hover = "rgba(255, 255, 255, 0.08)"
        border_color = "rgba(255, 255, 255, 0.1)"
        shadow_base = "rgba(0, 0, 0, 0.3)"
    else:
        bg_color = "#f9fafb"
        text_color = "#111827"
        text_muted = "#6b7280"
        surface_color = "#ffffff"
        surface_hover = "#f3f4f6"
        border_color = "rgba(0, 0, 0, 0.08)"
        shadow_base = "rgba(0, 0, 0, 0.05)"

    # === CSS ===
    css = f"""/* Adaptive Bento Dashboard Grid — generated component */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --text: {text_color};
    --text-muted: {text_muted};
    --surface: {surface_color};
    --surface-hover: {surface_hover};
    --border: {border_color};
    --accent: {accent_color};
    --shadow: {shadow_base};
    --max-width: {width_px}px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background: var(--bg);
    color: var(--text);
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    overflow-x: hidden;
    padding: 2rem 1rem;
}}

.dashboard-container {{
    width: 100%;
    max-width: var(--max-width);
    display: flex;
    flex-direction: column;
    gap: 3rem;
}}

.header {{
    margin-bottom: 1rem;
}}

.header h1 {{
    font-size: 2.2rem;
    font-weight: 700;
    margin-bottom: 0.5rem;
}}

.header p {{
    color: var(--text-muted);
    font-size: 1.1rem;
}}

/* =========================================
   TECHNIQUE 1: Bento Grid Layout via Areas
   ========================================= */
.bento-section {{
    display: grid;
    gap: 1.5rem;
    grid-auto-rows: minmax(140px, auto);
    /* Mobile First: Stacked */
    grid-template-columns: 1fr;
    grid-template-areas:
        "hero"
        "stat1"
        "stat2"
        "stat3"
        "stat4";
}}

/* Tablet: 2 Columns */
@media (min-width: 600px) {{
    .bento-section {{
        grid-template-columns: repeat(2, 1fr);
        grid-template-areas:
            "hero hero"
            "hero hero"
            "stat1 stat2"
            "stat3 stat4";
    }}
}}

/* Desktop: 4 Columns */
@media (min-width: 900px) {{
    .bento-section {{
        grid-template-columns: repeat(4, 1fr);
        grid-template-areas:
            "hero hero stat1 stat2"
            "hero hero stat3 stat4";
    }}
}}

/* Grid Area Assignments */
.bento-hero {{ grid-area: hero; min-height: 250px; }}
.stat-1 {{ grid-area: stat1; }}
.stat-2 {{ grid-area: stat2; }}
.stat-3 {{ grid-area: stat3; }}
.stat-4 {{ grid-area: stat4; }}


/* =========================================
   TECHNIQUE 2: Grid Stacking (No Absolute Pos)
   ========================================= */
.bento-hero {{
    display: grid;
    grid-template-areas: "stack";
    border-radius: 1.25rem;
    overflow: hidden;
    box-shadow: 0 10px 30px -10px var(--shadow);
}}

/* Both children assigned to "stack" area to overlap perfectly */
.hero-bg {{
    grid-area: stack;
    background: linear-gradient(135deg, var(--accent), #9b59b6, #3498db);
    background-size: 200% 200%;
    animation: gradientShift 10s ease infinite;
    width: 100%;
    height: 100%;
    z-index: 1;
}}

.hero-content {{
    grid-area: stack;
    z-index: 2;
    place-self: end start; /* Aligns to bottom left */
    padding: 2rem;
    color: #ffffff; /* Forced white for gradient contrast */
}}

.hero-content h2 {{
    font-size: 2.5rem;
    font-weight: 700;
    margin-bottom: 0.5rem;
    line-height: 1.1;
}}

.hero-content p {{
    font-size: 1.1rem;
    opacity: 0.9;
}}


/* =========================================
   TECHNIQUE 3: Grid Auto-fit Wrap
   ========================================= */
.autofit-section h3 {{
    font-size: 1.5rem;
    margin-bottom: 1.5rem;
    font-weight: 600;
}}

.grid-list {{
    display: grid;
    gap: 1.5rem;
    /* Automatically spawns columns based on min 260px width */
    grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
}}


/* --- Card Base Styling & Animations --- */
.card {{
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 1rem;
    padding: 1.5rem;
    display: flex;
    flex-direction: column;
    justify-content: center;
    box-shadow: 0 4px 6px -1px var(--shadow);
    /* Entry animation starting state */
    opacity: 0;
    transform: translateY(20px);
    transition: opacity 0.6s cubic-bezier(0.16, 1, 0.3, 1), 
                transform 0.6s cubic-bezier(0.16, 1, 0.3, 1), 
                box-shadow 0.3s ease, background 0.3s ease;
}}

.card.is-visible {{
    opacity: 1;
    transform: translateY(0);
}}

.card.is-visible:hover {{
    transform: translateY(-5px);
    box-shadow: 0 12px 20px -8px var(--shadow);
    background: var(--surface-hover);
}}

/* Stat Card Specifics */
.stat-icon {{
    color: var(--accent);
    font-size: 1.8rem;
    margin-bottom: 1rem;
}}
.stat-value {{
    font-size: 2rem;
    font-weight: 700;
    line-height: 1;
    margin-bottom: 0.25rem;
}}
.stat-label {{
    font-size: 0.95rem;
    color: var(--text-muted);
    font-weight: 500;
}}

/* List Card Specifics */
.list-card {{
    flex-direction: row;
    align-items: center;
    justify-content: space-between;
}}
.list-card-left {{
    display: flex;
    align-items: center;
    gap: 1rem;
    font-weight: 600;
}}
.list-card-left i {{
    color: var(--accent);
    font-size: 1.2rem;
}}
.status-pill {{
    font-size: 0.8rem;
    font-weight: 600;
    padding: 0.3rem 0.8rem;
    border-radius: 2rem;
    background: rgba(16, 185, 129, 0.15);
    color: #10b981;
}}
.status-pill.warn {{
    background: rgba(245, 158, 11, 0.15);
    color: #f59e0b;
}}

/* Animations */
@keyframes gradientShift {{
    0% {{ background-position: 0% 50%; }}
    50% {{ background-position: 100% 50%; }}
    100% {{ background-position: 0% 50%; }}
}}

@media (prefers-reduced-motion: reduce) {{
    .card {{ transition: none; }}
    .hero-bg {{ animation: none; }}
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
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <main class="dashboard-container">
        
        <header class="header">
            <h1>{title_text}</h1>
            <p>{body_text}</p>
        </header>

        <!-- Bento Layout Section -->
        <section class="bento-section">
            <!-- Grid Stacking Hero -->
            <article class="bento-hero card">
                <div class="hero-bg"></div>
                <div class="hero-content">
                    <h2>Systems Nominal</h2>
                    <p>All infrastructure arrays are operating at peak efficiency.</p>
                </div>
            </article>

            <!-- Stat Cards -->
            <article class="card stat-1">
                <div class="stat-icon"><i class="fa-solid fa-users"></i></div>
                <div class="stat-value">14.2k</div>
                <div class="stat-label">Active Users</div>
            </article>
            
            <article class="card stat-2">
                <div class="stat-icon"><i class="fa-solid fa-chart-line"></i></div>
                <div class="stat-value">$84.5k</div>
                <div class="stat-label">Monthly MRR</div>
            </article>

            <article class="card stat-3">
                <div class="stat-icon"><i class="fa-solid fa-server"></i></div>
                <div class="stat-value">99.9%</div>
                <div class="stat-label">Server Uptime</div>
            </article>

            <article class="card stat-4">
                <div class="stat-icon"><i class="fa-solid fa-bolt"></i></div>
                <div class="stat-value">12ms</div>
                <div class="stat-label">Avg Latency</div>
            </article>
        </section>

        <!-- Auto-fit Grid Section -->
        <section class="autofit-section">
            <h3>Connected Nodes</h3>
            <div class="grid-list">
                <article class="card list-card">
                    <div class="list-card-left">
                        <i class="fa-solid fa-database"></i> Node Alpha
                    </div>
                    <div class="status-pill">Online</div>
                </article>
                <article class="card list-card">
                    <div class="list-card-left">
                        <i class="fa-solid fa-database"></i> Node Beta
                    </div>
                    <div class="status-pill">Online</div>
                </article>
                <article class="card list-card">
                    <div class="list-card-left">
                        <i class="fa-solid fa-database"></i> Node Gamma
                    </div>
                    <div class="status-pill warn">Syncing</div>
                </article>
                <article class="card list-card">
                    <div class="list-card-left">
                        <i class="fa-solid fa-database"></i> Node Delta
                    </div>
                    <div class="status-pill">Online</div>
                </article>
            </div>
        </section>

    </main>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Adaptive Bento Dashboard Grid — interactive behavior
document.addEventListener('DOMContentLoaded', () => {{
    
    // Select all cards for entrance animation
    const cards = document.querySelectorAll('.card');
    
    // Set up Intersection Observer for scroll-triggered reveals
    const observerOptions = {{
        root: null,
        rootMargin: '0px',
        threshold: 0.1
    }};

    const cardObserver = new IntersectionObserver((entries, observer) => {{
        entries.forEach((entry) => {{
            if (entry.isIntersecting) {{
                // Apply a slight delay based on DOM order for a cascading effect
                const elementIndex = Array.from(cards).indexOf(entry.target);
                const delay = (elementIndex % 5) * 75; // max delay to prevent excessive waiting
                
                setTimeout(() => {{
                    entry.target.classList.add('is-visible');
                }}, delay);
                
                // Unobserve once animated
                observer.unobserve(entry.target);
            }}
        }});
    }}, observerOptions);

    // Initialize observer
    cards.forEach(card => {{
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

* **Accessibility (a11y)**:
  - Included a `@media (prefers-reduced-motion: reduce)` block in the CSS to disable the infinite gradient background animation and the transition transforms for users who suffer from vestibular disorders.
  - Utilized semantic HTML5 tags (`<main>`, `<header>`, `<section>`, `<article>`) to ensure screen readers correctly interpret the dashboard structure and landmark hierarchy.
  - The `hero-content` text explicitly forces a `#ffffff` color to guarantee WCAG AA compliant contrast against the dynamic gradient background regardless of the overall `color_scheme` choice.

* **Performance**:
  - **CSS Grid Wrapping**: By utilizing native CSS `repeat(auto-fit, minmax(...))` instead of JS `window.resize` event listeners, the browser's layout engine handles responsive reflows efficiently off the main JS thread.
  - **Grid Stacking over Absolute**: Setting `grid-template-areas: "stack"` ensures the browser easily calculates the bounding box of the hero container without triggering expensive layout repaints, which frequently occur when `position: absolute` elements shift out of bounds.
  - **Intersection Observer**: The scroll reveal effect utilizes the asynchronous `IntersectionObserver` API rather than synchronous `scroll` event listeners, keeping the scrolling experience locked at 60fps.