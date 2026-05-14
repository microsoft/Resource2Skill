# Responsive Bento Dashboard

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Responsive Bento Dashboard 

* **Core Visual Mechanism**: This pattern establishes a modular, highly responsive administrative interface. It relies on a structural philosophy: a flexible macro-layout (using `display: flex` for the overall app shell and sticky sidebar) combined with a rigid, mathematical micro-layout (using `display: grid` with `auto-fit` and `minmax()` for the bento-box style data widgets). The visual signature is clean, card-based data visualization that reflows seamlessly across any device without requiring dozens of hard-coded media queries.
* **Why Use This Skill (Rationale)**: Complex data applications often break on varying screen sizes. By strictly applying the CSS Box Model and understanding the "Parent-Child" relationship, this layout abstracts complexity. The rule "It's Flexbox until proven Grid-y" ensures that elements flow naturally by default, while Grid is reserved specifically for the rigorous alignment required by dashboard cards.
* **Overall Applicability**: Perfect for SaaS product interfaces, analytical dashboards, user portals, and admin panels that must display varied data types (charts, lists, numeric KPIs) consistently from 4K monitors down to mobile phones.
* **Value Addition**: It drastically reduces CSS bloat. Instead of fighting the browser with absolute positioning or endless pixel tweaks, this pattern leans into the browser's native calculation engine, providing a fluid, bulletproof user experience with minimal code.
* **Browser Compatibility**: Uses CSS Custom Properties, CSS Grid (`minmax`, `auto-fit`), CSS Flexbox, and `position: sticky`. Fully supported in all modern browsers (Edge, Chrome, Firefox, Safari). Minimum browser versions are roughly 2017+ (e.g., Safari 10.1, Chrome 57).

### 2. Visual & Technical Breakdown

* **Step A: Core Visual Elements**
  - **Containers**: Semantic HTML5 elements (`<aside>`, `<main>`, `<header>`) function as the primary structural boxes.
  - **Color Logic**: Utilizes a highly constrained "zinc" grayscale palette for depth, plus one vibrant accent color. In dark mode: background (`#09090b`), elevated surfaces (`#18181b`), subtle borders (`#27272a`), and high-contrast text (`#f4f4f5`). 
  - **Typography**: Uses 'Inter' (sans-serif) to maintain geometric legibility for numeric data. Hierarchical sizing (e.g., 2rem for key metrics, 0.875rem uppercase for widget labels).
  - **CSS Properties**: `border-radius: 0.75rem` for friendly edges, `border` for definition without relying on heavy box-shadows (which can clutter dense UI).

* **Step B: Layout & Compositional Style**
  - **Macro-Layout (Flexbox)**: The outermost wrapper is a flex container. The left sidebar has a fixed width (`260px`) and `position: sticky; top: 0; height: 100vh` to remain visible while the main content scrolls.
  - **Micro-Layout (Grid)**: The dashboard content area uses `display: grid; gap: 1.5rem; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));`. This single line of CSS forces cards to fill available space and automatically wrap when they shrink below 300px, effectively achieving responsiveness without media queries.
  - **Exceptions**: Specific widgets use `grid-column: 1 / -1` to span full width (like charts) or `grid-row: span 2` to span vertically.

* **Step C: Interactive Behavior & Animations**
  - **Mobile State**: A `@media (max-width: 1024px)` query breaks the macro-layout. The sticky sidebar converts to `position: fixed` and translates off-screen (`transform: translateX(-100%)`). 
  - **JavaScript**: A lightweight JS event listener toggles an `.open` class on the sidebar and a semi-transparent backdrop overlay, sliding the menu into view with a smooth `transition: transform 0.3s ease`.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| Macro-Layout (App Shell) | CSS Flexbox & `position: sticky` | Flexbox excels at aligning 1D elements (sidebar next to main content). Sticky positioning keeps the menu in view effortlessly. |
| Micro-Layout (Widgets) | CSS Grid | `repeat(auto-fit, minmax())` is mathematically designed for responsive card grids, avoiding JS resize logic. |
| Mobile Navigation | CSS Transforms + JS | Toggling a class that applies `transform: translateX()` ensures hardware-accelerated, 60fps sliding animations for the mobile drawer. |
| Vector Charts | Inline SVG | Scalable, styleable via CSS variables, and requires zero external chart libraries for aesthetic reproduction. |
| Iconography | Font Awesome CDN | Provides immediate, recognizable UI metaphors (hamburger menu, active states) without bloat. |

#### 3b. Complete Reproduction Code

```python
def create_component(
    output_dir: str,
    title_text: str = "Dashboard Overview",
    body_text: str = "Welcome back. Here is your performance summary for this week.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#eab308",     # CSS hex color for accent (yellow/gold in video)
    width_px: int = 1440,
    height_px: int = 900,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Responsive Bento Dashboard visual effect.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Theme Setup ===
    if color_scheme == "dark":
        bg_color = "#09090b"      # Zinc 950
        surface_color = "#18181b" # Zinc 900
        border_color = "#27272a"  # Zinc 800
        text_color = "#f4f4f5"    # Zinc 100
        text_muted = "#a1a1aa"    # Zinc 400
        positive_color = "#10b981"
        negative_color = "#ef4444"
    else:
        bg_color = "#ffffff"
        surface_color = "#f4f4f5" # Zinc 100
        border_color = "#e4e4e7"  # Zinc 200
        text_color = "#09090b"    # Zinc 950
        text_muted = "#71717a"    # Zinc 500
        positive_color = "#059669"
        negative_color = "#dc2626"

    # === CSS ===
    css = f"""/* Responsive Bento Dashboard */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --surface: {surface_color};
    --border: {border_color};
    --text: {text_color};
    --text-muted: {text_muted};
    --accent: {accent_color};
    --positive: {positive_color};
    --negative: {negative_color};
}}

body {{
    font-family: 'Inter', system-ui, sans-serif;
    background: var(--bg);
    color: var(--text);
    line-height: 1.5;
    -webkit-font-smoothing: antialiased;
    overflow-x: hidden;
}}

/* Macro Layout */
.layout-wrapper {{
    display: flex;
    min-height: 100vh;
    width: 100%;
    max-width: {width_px}px;
    margin: 0 auto;
    position: relative;
}}

/* Sidebar Elements */
.sidebar {{
    width: 260px;
    background: var(--bg);
    border-right: 1px solid var(--border);
    position: sticky;
    top: 0;
    height: 100vh;
    display: flex;
    flex-direction: column;
    transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    z-index: 40;
}}

.sidebar-header {{
    height: 70px;
    padding: 0 1.5rem;
    display: flex;
    align-items: center;
    border-bottom: 1px solid var(--border);
}}

.sidebar-header h2 {{
    font-size: 1.25rem;
    font-weight: 700;
    letter-spacing: -0.025em;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}}

.sidebar-nav {{
    padding: 1.5rem 1rem;
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
}}

.sidebar-link {{
    padding: 0.75rem 1rem;
    border-radius: 0.5rem;
    color: var(--text-muted);
    text-decoration: none;
    font-weight: 500;
    display: flex;
    align-items: center;
    gap: 0.75rem;
    transition: all 0.2s ease;
}}

.sidebar-link:hover {{
    color: var(--text);
    background: var(--surface);
}}

.sidebar-link.active {{
    color: var(--text);
    background: var(--surface);
}}

.sidebar-link i {{
    width: 20px;
    text-align: center;
}}

.sidebar-overlay {{
    display: none;
    position: fixed;
    inset: 0;
    background: rgba(0,0,0,0.6);
    backdrop-filter: blur(4px);
    z-index: 30;
    opacity: 0;
    transition: opacity 0.3s ease;
}}

/* Main Content Area */
.main-wrapper {{
    flex: 1;
    min-width: 0; /* Prevents flex children from blowing out */
    display: flex;
    flex-direction: column;
}}

.header {{
    height: 70px;
    padding: 0 2rem;
    border-bottom: 1px solid var(--border);
    display: flex;
    align-items: center;
    justify-content: space-between;
    position: sticky;
    top: 0;
    background: rgba({int(bg_color[1:3], 16)}, {int(bg_color[3:5], 16)}, {int(bg_color[5:7], 16)}, 0.8);
    backdrop-filter: blur(12px);
    z-index: 20;
}}

.menu-toggle {{
    display: none;
    background: transparent;
    border: none;
    color: var(--text);
    font-size: 1.25rem;
    cursor: pointer;
    padding: 0.5rem;
}}

.search-container {{
    display: flex;
    align-items: center;
    background: var(--surface);
    border: 1px solid var(--border);
    padding: 0.5rem 1rem;
    border-radius: 0.5rem;
    width: 320px;
    gap: 0.75rem;
    color: var(--text-muted);
}}

.search-container input {{
    background: transparent;
    border: none;
    color: var(--text);
    outline: none;
    width: 100%;
    font-family: inherit;
}}

.header-actions {{
    display: flex;
    align-items: center;
    gap: 1.5rem;
}}

.btn-magic {{
    background: var(--surface);
    color: var(--text);
    border: 1px solid var(--border);
    padding: 0.5rem 1rem;
    border-radius: 0.5rem;
    font-weight: 500;
    font-family: inherit;
    cursor: pointer;
    display: flex;
    align-items: center;
    gap: 0.5rem;
    transition: border-color 0.2s ease;
}}

.btn-magic:hover {{
    border-color: var(--accent);
}}

.btn-magic span {{
    color: var(--accent);
}}

.avatar {{
    width: 36px;
    height: 36px;
    border-radius: 50%;
    background: var(--border);
    overflow: hidden;
}}

/* Dashboard Grid */
.dashboard-content {{
    padding: 2rem;
    display: flex;
    flex-direction: column;
    gap: 2rem;
}}

.content-header h1 {{
    font-size: 1.875rem;
    font-weight: 700;
    margin-bottom: 0.25rem;
    letter-spacing: -0.025em;
}}

.content-header p {{
    color: var(--text-muted);
}}

.grid {{
    display: grid;
    gap: 1.5rem;
    /* The magic responsive grid line */
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    grid-auto-rows: minmax(min-content, max-content);
}}

.widget {{
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 0.75rem;
    padding: 1.5rem;
    display: flex;
    flex-direction: column;
}}

.widget-large {{
    grid-column: 1 / -1; /* Spans all columns */
}}

.widget-tall {{
    grid-row: span 2;
}}

.widget-title {{
    font-size: 0.875rem;
    font-weight: 600;
    color: var(--text-muted);
    margin-bottom: 1rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    display: flex;
    justify-content: space-between;
    align-items: center;
}}

.widget-value {{
    font-size: 2.25rem;
    font-weight: 700;
    margin-bottom: 0.25rem;
    letter-spacing: -0.025em;
}}

.trend {{
    font-size: 0.875rem;
    font-weight: 500;
    display: flex;
    align-items: center;
    gap: 0.25rem;
}}

.trend.up {{ color: var(--positive); }}
.trend.down {{ color: var(--negative); }}

/* specific widget interior layouts */
.chart-container {{
    flex: 1;
    min-height: 240px;
    margin-top: 1rem;
    width: 100%;
}}

.transaction-list {{
    display: flex;
    flex-direction: column;
    gap: 1rem;
}}

.transaction-item {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding-bottom: 1rem;
    border-bottom: 1px solid var(--border);
}}

.transaction-item:last-child {{
    border-bottom: none;
    padding-bottom: 0;
}}

.tx-info {{
    display: flex;
    align-items: center;
    gap: 1rem;
}}

.tx-icon {{
    width: 40px;
    height: 40px;
    border-radius: 0.5rem;
    background: var(--bg);
    display: flex;
    align-items: center;
    justify-content: center;
    border: 1px solid var(--border);
}}

.tx-details h4 {{ font-size: 0.875rem; font-weight: 500; }}
.tx-details p {{ font-size: 0.75rem; color: var(--text-muted); }}
.tx-amount {{ font-weight: 600; }}

/* Responsive Overrides (The final rule: adding complexity with @media) */
@media (max-width: 1024px) {{
    .sidebar {{
        position: fixed;
        transform: translateX(-100%);
    }}
    .sidebar.open {{
        transform: translateX(0);
    }}
    .sidebar-overlay.open {{
        display: block;
        opacity: 1;
    }}
    .menu-toggle {{
        display: block;
    }}
    .search-container {{
        display: none; /* Hide on smaller screens to save space */
    }}
    .header {{
        padding: 0 1.5rem;
        gap: 1rem;
    }}
    .dashboard-content {{
        padding: 1.5rem;
    }}
}}

@media (max-width: 640px) {{
    .grid {{
        grid-template-columns: 1fr;
    }}
    .widget-tall {{
        grid-row: span 1;
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
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
</head>
<body>
    <div class="layout-wrapper">
        <div class="sidebar-overlay"></div>
        
        <aside class="sidebar">
            <div class="sidebar-header">
                <h2><i class="fa-solid fa-shapes" style="color: var(--accent);"></i> Bento</h2>
            </div>
            <nav class="sidebar-nav">
                <a href="#" class="sidebar-link active"><i class="fa-solid fa-house"></i> Dashboard</a>
                <a href="#" class="sidebar-link"><i class="fa-solid fa-chart-pie"></i> Analytics</a>
                <a href="#" class="sidebar-link"><i class="fa-solid fa-wallet"></i> Transactions</a>
                <a href="#" class="sidebar-link"><i class="fa-solid fa-users"></i> Community</a>
                <div style="flex-grow: 1;"></div>
                <a href="#" class="sidebar-link"><i class="fa-solid fa-gear"></i> Settings</a>
            </nav>
        </aside>

        <main class="main-wrapper">
            <header class="header">
                <div style="display: flex; align-items: center; gap: 1rem;">
                    <button class="menu-toggle" aria-label="Toggle Menu"><i class="fa-solid fa-bars"></i></button>
                    <div class="search-container">
                        <i class="fa-solid fa-magnifying-glass"></i>
                        <input type="text" placeholder="Search data...">
                    </div>
                </div>
                <div class="header-actions">
                    <button class="btn-magic"><span>✦</span> Magic</button>
                    <div class="avatar">
                        <img src="https://ui-avatars.com/api/?name=Admin&background=random&color=fff" alt="User" style="width:100%; height:100%; object-fit:cover;">
                    </div>
                </div>
            </header>

            <div class="dashboard-content">
                <div class="content-header">
                    <h1>{title_text}</h1>
                    <p>{body_text}</p>
                </div>

                <div class="grid">
                    <!-- Widget 1: Large Chart -->
                    <div class="widget widget-large">
                        <div class="widget-title">
                            Revenue Overview
                            <i class="fa-solid fa-ellipsis"></i>
                        </div>
                        <div class="chart-container">
                            <svg preserveAspectRatio="none" viewBox="0 0 100 100" style="width:100%; height:100%; overflow:visible;">
                                <defs>
                                    <linearGradient id="chartGrad" x1="0" y1="0" x2="0" y2="1">
                                        <stop offset="0%" stop-color="var(--accent)" stop-opacity="0.2"/>
                                        <stop offset="100%" stop-color="var(--accent)" stop-opacity="0"/>
                                    </linearGradient>
                                </defs>
                                <path d="M0,80 Q10,50 20,60 T40,40 T60,60 T80,30 T100,45 L100,100 L0,100 Z" fill="url(#chartGrad)" />
                                <path d="M0,80 Q10,50 20,60 T40,40 T60,60 T80,30 T100,45" fill="none" stroke="var(--accent)" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
                            </svg>
                        </div>
                    </div>

                    <!-- Widget 2: Stat Card -->
                    <div class="widget">
                        <div class="widget-title">Total Users</div>
                        <div class="widget-value">24,592</div>
                        <div class="trend up"><i class="fa-solid fa-arrow-trend-up"></i> +12.5% from last month</div>
                    </div>

                    <!-- Widget 3: Stat Card -->
                    <div class="widget">
                        <div class="widget-title">Active Sessions</div>
                        <div class="widget-value">1,205</div>
                        <div class="trend down"><i class="fa-solid fa-arrow-trend-down"></i> -3.2% from last month</div>
                    </div>

                    <!-- Widget 4: Tall List -->
                    <div class="widget widget-tall">
                        <div class="widget-title">Recent Transactions</div>
                        <div class="transaction-list">
                            <div class="transaction-item">
                                <div class="tx-info">
                                    <div class="tx-icon"><i class="fa-brands fa-stripe" style="color: #6366f1;"></i></div>
                                    <div class="tx-details">
                                        <h4>Stripe Payment</h4>
                                        <p>Today, 2:45 PM</p>
                                    </div>
                                </div>
                                <div class="tx-amount">+$2,500.00</div>
                            </div>
                            <div class="transaction-item">
                                <div class="tx-info">
                                    <div class="tx-icon"><i class="fa-brands fa-paypal" style="color: #0ea5e9;"></i></div>
                                    <div class="tx-details">
                                        <h4>PayPal Transfer</h4>
                                        <p>Today, 11:20 AM</p>
                                    </div>
                                </div>
                                <div class="tx-amount">+$850.00</div>
                            </div>
                            <div class="transaction-item">
                                <div class="tx-info">
                                    <div class="tx-icon"><i class="fa-solid fa-building-columns" style="color: var(--text-muted);"></i></div>
                                    <div class="tx-details">
                                        <h4>Bank Withdrawal</h4>
                                        <p>Yesterday, 4:00 PM</p>
                                    </div>
                                </div>
                                <div class="tx-amount" style="color: var(--text);">-$12,000.00</div>
                            </div>
                            <div class="transaction-item">
                                <div class="tx-info">
                                    <div class="tx-icon"><i class="fa-brands fa-apple" style="color: var(--text);"></i></div>
                                    <div class="tx-details">
                                        <h4>Apple Pay</h4>
                                        <p>May 25, 1:15 PM</p>
                                    </div>
                                </div>
                                <div class="tx-amount">+$420.00</div>
                            </div>
                            <div class="transaction-item">
                                <div class="tx-info">
                                    <div class="tx-icon"><i class="fa-brands fa-google" style="color: #ea4335;"></i></div>
                                    <div class="tx-details">
                                        <h4>Google Pay</h4>
                                        <p>May 24, 9:30 AM</p>
                                    </div>
                                </div>
                                <div class="tx-amount">+$1,150.00</div>
                            </div>
                        </div>
                    </div>

                    <!-- Widget 5: Stat Card -->
                    <div class="widget">
                        <div class="widget-title">Conversion Rate</div>
                        <div class="widget-value">4.62%</div>
                        <div class="trend up"><i class="fa-solid fa-arrow-trend-up"></i> +0.5% from last month</div>
                    </div>
                </div>
            </div>
        </main>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Responsive Sidebar Toggle Logic
document.addEventListener('DOMContentLoaded', () => {{
    const toggleBtn = document.querySelector('.menu-toggle');
    const sidebar = document.querySelector('.sidebar');
    const overlay = document.querySelector('.sidebar-overlay');

    function toggleMenu() {{
        sidebar.classList.toggle('open');
        overlay.classList.toggle('open');
        
        // Accessibility toggle
        const isExpanded = toggleBtn.getAttribute('aria-expanded') === 'true';
        toggleBtn.setAttribute('aria-expanded', !isExpanded);
    }}

    if(toggleBtn && sidebar && overlay) {{
        toggleBtn.addEventListener('click', toggleMenu);
        overlay.addEventListener('click', toggleMenu); // Click background to close
    }}
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
  - Semantic landmark tags (`<header>`, `<nav>`, `<aside>`, `<main>`) are used so screen readers can easily parse the layout structure.
  - The menu toggle button includes an `aria-label`. The JS updates `aria-expanded` state for assistive technologies.
  - The color palette is selected specifically to maintain high contrast ratios (Zinc-400 against Zinc-900 maintains WCAG AA compliance for secondary text).
* **Performance**: 
  - **Zero Layout Thrashing**: By utilizing CSS Grid `minmax()` math, the browser reflows the cards entirely via the native CSS engine. No JavaScript resize-observers or window event listeners are needed to recalculate card widths.
  - **Animation Optimization**: The mobile sidebar animation targets `transform: translateX` and `opacity` exclusively. These properties are handled by the GPU compositor layer, preventing expensive main-thread layout recalculations and ensuring buttery 60fps transitions even on low-end mobile devices.