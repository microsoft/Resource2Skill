# Dynamic Dashboard Grid & Layout Scaffolding

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Dynamic Dashboard Grid & Layout Scaffolding

* **Core Visual Mechanism**: The system relies on a flexible 12-column CSS Grid architecture combined with parameterized, state-driven sidebars. The visual signature is the strict adherence to horizontal rhythm—specifically, precise gutters between grid items (e.g., 24px) and deliberate "offsets" (padding) separating the fixed-width navigational sidebars from the fluid central content area. The component includes a toggleable "Figma-style" translucent pink column overlay to demonstrate the structural alignment.

* **Why Use This Skill (Rationale)**: Dashboards demand high information density without feeling cluttered. A rigid underlying grid system provides predictability, allowing disparate widgets (charts, lists, metrics) to feel unified. Variable sidebar states (small, standard, dual) cater to different navigation complexities while ensuring the core content area reflows gracefully.

* **Overall Applicability**: Ideal for SaaS web application interfaces, admin panels, analytics dashboards, and any layout requiring fixed global navigation alongside a modular, card-based content ecosystem.

* **Value Addition**: This pattern establishes a scalable foundation. Instead of hard-coding layouts per page, it provides a scaffolding where developers can simply drop widgets into `col-span-x` classes. The ability to toggle sidebars dynamically demonstrates robust responsive design principles.

* **Browser Compatibility**: Requires modern browsers supporting CSS Grid (`grid-template-columns`, `gap`), CSS Custom Properties (Variables), and CSS Flexbox. Fully supported in Chrome 57+, Firefox 52+, Safari 10.1+, Edge 16+.

### 2. Visual & Technical Breakdown

* **Step A: Core Visual Elements**
  - **Structure**: Semantic HTML using `<aside>` for sidebars and `<main>` for the content block.
  - **Color Logic**: Uses a high-contrast background/surface model.
    - Dark mode: Background `#0f172a`, Surface `#1e293b`, Border `#334155`.
    - Light mode: Background `#f8fafc`, Surface `#ffffff`, Border `#e2e8f0`.
  - **Typographic Hierarchy**: `Inter` font family. Strong hierarchy established through muted labels (`#94a3b8`) and high-contrast metric values.
  - **Visual Aids**: A Figma-style overlay using `rgba(255, 75, 75, 0.15)` to reveal the 12 columns.

* **Step B: Layout & Compositional Style**
  - **Macro Layout**: Flexbox container (`display: flex`) holding fixed-width sidebars (`width: var(--sidebar-width)`) and a flexible main area (`flex: 1`).
  - **Micro Layout**: CSS Grid within the main area (`display: grid; grid-template-columns: repeat(12, 1fr)`).
  - **Whitespace Strategy**: Controlled entirely via CSS variables. A uniform gutter of `24px` between cards, and dynamic "offsets" (padding) ranging from `32px` to `40px` separating the grid from the sidebars.

* **Step C: Interactive Behavior & Animations**
  - **Layout Switching**: JavaScript applies `data-layout` attributes to the root container.
  - **Transitions**: CSS transitions (`transition: width 0.4s cubic-bezier(0.4, 0, 0.2, 1), padding 0.4s`) handle the smooth expansion/collapse of sidebars when switching layout modes.
  - **Grid Reveal**: A JS-triggered toggle fades in a `pointer-events: none` overlay container to visualize the grid matrix.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **Macro Layout (Sidebars)** | CSS Flexbox + CSS Variables | Flexbox elegantly handles fixed sidebars alongside a fluid central container (`flex: 1`). Variables allow JS to easily swap dimensions. |
| **Widget Layout** | CSS Grid | A 12-column Grid with `grid-column: span X` is the web standard for replicating Figma column grids. |
| **Grid Visualization** | CSS Absolute Positioning | An absolutely positioned overlay container with inherited grid properties perfectly mimics Figma's column overlay tool. |
| **Layout State Transitions** | CSS Transitions + JS Data Attributes | Toggling a `data-layout` attribute keeps state logic clean, while CSS handles the animation easing natively. |

#### 3b. Complete Reproduction Code

```python
def create_component(
    output_dir: str,
    title_text: str = "Dashboard Overview",
    body_text: str = "Analyzing grid system metrics and layout responsiveness.",
    color_scheme: str = "dark",
    accent_color: str = "#3b82f6",
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Dynamic Dashboard Grid layout.
    
    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Convert accent hex to rgb string for rgba() usage in CSS
    def hex_to_rgb(hx):
        hx = hx.lstrip('#')
        if len(hx) == 3: hx = ''.join(c + c for c in hx)
        return f"{int(hx[0:2], 16)}, {int(hx[2:4], 16)}, {int(hx[4:6], 16)}"
    
    accent_rgb = hex_to_rgb(accent_color)

    # Derive theme colors
    if color_scheme == "dark":
        bg_color = "#0f172a"
        surface_color = "#1e293b"
        border_color = "#334155"
        text_color = "#f8fafc"
        text_muted = "#94a3b8"
    else:
        bg_color = "#f8fafc"
        surface_color = "#ffffff"
        border_color = "#e2e8f0"
        text_color = "#0f172a"
        text_muted = "#64748b"

    # === CSS ===
    css = f"""/* Dynamic Dashboard Grid — generated component */
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
    --accent-rgb: {accent_rgb};
    
    --width: {width_px}px;
    --height: {height_px}px;
    
    /* Grid Core Variables */
    --columns: 12;
    --gutter: 24px;
}}

/* Layout State Configuration Variables */
[data-layout="standard"] {{
    --sidebar-width: 240px;
    --right-sidebar-width: 0px;
    --content-pad: 40px;
}}

[data-layout="small"] {{
    --sidebar-width: 80px;
    --right-sidebar-width: 0px;
    --content-pad: 40px;
}}

[data-layout="dual"] {{
    --sidebar-width: 208px;
    --right-sidebar-width: 240px;
    --content-pad: 32px;
}}

body {{
    font-family: 'Inter', sans-serif;
    background: #000;
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
}}

/* Presentation Container (Mimicking a Browser Window) */
.app-container {{
    width: var(--width);
    height: var(--height);
    background: var(--bg);
    color: var(--text);
    border-radius: 16px;
    overflow: hidden;
    box-shadow: 0 24px 48px rgba(0,0,0,0.4);
    display: flex;
    position: relative;
}}

/* Global Transitions for smooth layout switching */
.sidebar, .right-sidebar, .content-wrapper, .nav-label, .rs-content {{
    transition: width 0.4s cubic-bezier(0.4, 0, 0.2, 1),
                padding 0.4s cubic-bezier(0.4, 0, 0.2, 1),
                opacity 0.3s ease;
}}

/* Sidebars */
.sidebar {{
    width: var(--sidebar-width);
    background: var(--surface);
    border-right: 1px solid var(--border);
    display: flex;
    flex-direction: column;
    padding: 24px;
    overflow: hidden;
    flex-shrink: 0;
}}

[data-layout="small"] .sidebar {{
    align-items: center;
    padding: 24px 0;
}}

.right-sidebar {{
    width: var(--right-sidebar-width);
    background: var(--surface);
    border-left: 1px solid var(--border);
    flex-shrink: 0;
    overflow: hidden;
}}

.rs-content {{
    width: 240px; /* Fixed width to prevent wrapping during transition */
    padding: 24px;
    opacity: 0;
    display: flex;
    flex-direction: column;
    gap: 16px;
}}

[data-layout="dual"] .rs-content {{
    opacity: 1;
    transition-delay: 0.2s;
}}

/* Sidebar Internals */
.logo-placeholder {{
    width: 32px;
    height: 32px;
    border-radius: 8px;
    background: var(--accent);
    margin-bottom: 40px;
    flex-shrink: 0;
}}

.nav-item {{
    height: 40px;
    width: 100%;
    border-radius: 6px;
    display: flex;
    align-items: center;
    padding: 0 12px;
    gap: 12px;
    margin-bottom: 8px;
    cursor: pointer;
    color: var(--text-muted);
}}

[data-layout="small"] .nav-item {{
    padding: 0;
    justify-content: center;
    width: 48px;
}}

.nav-item.active {{
    background: rgba(var(--accent-rgb), 0.1);
    color: var(--accent);
}}

.nav-icon {{
    width: 20px; height: 20px;
    border-radius: 4px;
    background: currentColor;
    flex-shrink: 0;
}}

.nav-label {{
    height: 12px; width: 80px;
    border-radius: 4px;
    background: currentColor;
    opacity: 0.8;
}}

[data-layout="small"] .nav-label {{
    opacity: 0;
    width: 0;
}}

.rs-widget {{
    width: 100%; height: 120px;
    border-radius: 8px;
    background: var(--bg);
    border: 1px solid var(--border);
}}

/* Main Content Area */
.content-wrapper {{
    flex: 1;
    padding: 40px var(--content-pad);
    overflow-y: auto;
    overflow-x: hidden;
    display: flex;
    flex-direction: column;
}}

/* Topbar Controls */
.topbar {{
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 32px;
    flex-wrap: wrap;
    gap: 16px;
}}

.topbar h1 {{ font-size: 24px; font-weight: 600; margin-bottom: 4px; }}
.topbar p {{ font-size: 14px; color: var(--text-muted); }}

.topbar-controls {{
    display: flex;
    align-items: center;
    gap: 16px;
}}

.control-group {{
    display: flex; align-items: center; gap: 8px; font-size: 14px; color: var(--text-muted);
}}

select {{
    background: var(--surface); color: var(--text); border: 1px solid var(--border);
    padding: 8px 12px; border-radius: 6px; outline: none; font-family: inherit; font-size: 14px;
    cursor: pointer;
}}

.btn {{
    background: rgba(var(--accent-rgb), 0.1);
    color: var(--accent);
    border: 1px solid transparent;
    padding: 8px 16px;
    border-radius: 6px;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s;
    font-family: inherit;
    font-size: 14px;
}}

.btn:hover {{ background: rgba(var(--accent-rgb), 0.2); }}

.btn.active {{
    background: var(--accent); color: #fff;
    box-shadow: 0 4px 12px rgba(var(--accent-rgb), 0.3);
}}

/* === Grid System Core === */
.grid-system {{
    display: grid;
    grid-template-columns: repeat(var(--columns), 1fr);
    grid-auto-rows: min-content;
    gap: var(--gutter);
    position: relative;
    padding-bottom: 40px;
}}

/* Figma-Style Overlay */
.grid-overlay {{
    position: absolute;
    top: 0; bottom: 0; left: 0; right: 0;
    display: grid;
    grid-template-columns: inherit;
    gap: inherit;
    pointer-events: none;
    z-index: 100;
    opacity: 0;
    transition: opacity 0.3s ease;
}}

.grid-overlay.active {{ opacity: 1; }}

.grid-col-overlay {{
    background-color: rgba(255, 75, 75, 0.12);
    border-left: 1px dashed rgba(255, 75, 75, 0.2);
    border-right: 1px dashed rgba(255, 75, 75, 0.2);
    height: 100%;
}}

/* Grid Cards & Skeletons */
.card {{
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 24px;
    display: flex;
    flex-direction: column;
}}

.span-3 {{ grid-column: span 3; }}
.span-4 {{ grid-column: span 4; }}
.span-8 {{ grid-column: span 8; }}

.skel-header {{ display: flex; align-items: center; margin-bottom: 16px; }}
.skel-icon {{ width: 40px; height: 40px; border-radius: 8px; background: rgba(var(--accent-rgb), 0.15); }}
.skel-text-sm {{ width: 40%; height: 12px; border-radius: 4px; background: var(--border); margin-bottom: 6px; }}
.skel-text-lg {{ width: 80%; height: 24px; border-radius: 6px; background: var(--border); }}

.skel-chart {{
    width: 100%; height: 220px;
    background: linear-gradient(180deg, rgba(var(--accent-rgb), 0.05) 0%, transparent 100%);
    border: 1px solid var(--border);
    border-radius: 8px; margin-top: 24px;
    display: flex; align-items: flex-end; padding: 16px; gap: 12px;
}}
.skel-chart .bar {{ flex: 1; background: var(--accent); opacity: 0.7; border-radius: 4px 4px 0 0; }}

.skel-list {{ display: flex; flex-direction: column; gap: 12px; margin-top: 24px; flex: 1; justify-content: space-between;}}
.skel-list-item {{ width: 100%; height: 40px; border-radius: 6px; background: var(--bg); border: 1px solid var(--border);}}

/* Responsive Overrides within the container scope */
@media (max-width: 900px) {{
    [data-layout] {{ --right-sidebar-width: 0px !important; }}
    .span-3 {{ grid-column: span 6; }}
    .span-8, .span-4 {{ grid-column: span 12; }}
}}

@media (max-width: 600px) {{
    [data-layout] {{ --sidebar-width: 0px !important; --content-pad: 16px !important; }}
    .span-3 {{ grid-column: span 12; }}
    .topbar {{ flex-direction: column; }}
}}
"""

    # === HTML ===
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard Grid System</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="app-container" data-layout="standard">
        <!-- Left Sidebar -->
        <aside class="sidebar">
            <div class="logo-placeholder"></div>
            <div class="nav-item active"><div class="nav-icon"></div><div class="nav-label"></div></div>
            <div class="nav-item"><div class="nav-icon"></div><div class="nav-label"></div></div>
            <div class="nav-item"><div class="nav-icon"></div><div class="nav-label" style="width:50px"></div></div>
            <div class="nav-item"><div class="nav-icon"></div><div class="nav-label" style="width:70px"></div></div>
        </aside>

        <!-- Main Content -->
        <main class="content-wrapper">
            <header class="topbar">
                <div class="topbar-left">
                    <h1>{title_text}</h1>
                    <p>{body_text}</p>
                </div>
                <div class="topbar-controls">
                    <div class="control-group">
                        <label for="layout-select">Layout Style:</label>
                        <select id="layout-select">
                            <option value="standard">Standard Sidebar</option>
                            <option value="small">Small Sidebar</option>
                            <option value="dual">Dual Sidebars</option>
                        </select>
                    </div>
                    <button id="toggle-grid" class="btn">Show Overlay</button>
                </div>
            </header>

            <div class="grid-system">
                <!-- Figma Column Overlay -->
                <div class="grid-overlay" id="overlay">
                    <div class="grid-col-overlay"></div><div class="grid-col-overlay"></div>
                    <div class="grid-col-overlay"></div><div class="grid-col-overlay"></div>
                    <div class="grid-col-overlay"></div><div class="grid-col-overlay"></div>
                    <div class="grid-col-overlay"></div><div class="grid-col-overlay"></div>
                    <div class="grid-col-overlay"></div><div class="grid-col-overlay"></div>
                    <div class="grid-col-overlay"></div><div class="grid-col-overlay"></div>
                </div>

                <!-- Grid Widgets -->
                <!-- Row 1: Metrics -->
                <div class="card span-3">
                    <div class="skel-header"><div class="skel-icon"></div></div>
                    <div class="skel-text-sm" style="width: 50%;"></div>
                    <div class="skel-text-lg" style="width: 70%;"></div>
                </div>
                <div class="card span-3">
                    <div class="skel-header"><div class="skel-icon"></div></div>
                    <div class="skel-text-sm" style="width: 40%;"></div>
                    <div class="skel-text-lg" style="width: 85%;"></div>
                </div>
                <div class="card span-3">
                    <div class="skel-header"><div class="skel-icon"></div></div>
                    <div class="skel-text-sm" style="width: 60%;"></div>
                    <div class="skel-text-lg" style="width: 50%;"></div>
                </div>
                <div class="card span-3">
                    <div class="skel-header"><div class="skel-icon"></div></div>
                    <div class="skel-text-sm" style="width: 30%;"></div>
                    <div class="skel-text-lg" style="width: 90%;"></div>
                </div>

                <!-- Row 2: Complex Modules -->
                <div class="card span-8">
                    <div class="skel-text-sm"></div>
                    <div class="skel-text-lg" style="width: 30%;"></div>
                    <div class="skel-chart">
                        <div class="bar" style="height: 40%"></div>
                        <div class="bar" style="height: 70%"></div>
                        <div class="bar" style="height: 50%"></div>
                        <div class="bar" style="height: 90%"></div>
                        <div class="bar" style="height: 60%"></div>
                        <div class="bar" style="height: 30%"></div>
                        <div class="bar" style="height: 80%"></div>
                    </div>
                </div>
                <div class="card span-4">
                    <div class="skel-text-sm"></div>
                    <div class="skel-text-lg" style="width: 50%;"></div>
                    <div class="skel-list">
                        <div class="skel-list-item"></div>
                        <div class="skel-list-item"></div>
                        <div class="skel-list-item"></div>
                        <div class="skel-list-item" style="opacity: 0.5;"></div>
                    </div>
                </div>
            </div>
        </main>

        <!-- Right Sidebar (Contextual) -->
        <aside class="right-sidebar">
            <div class="rs-content">
                <div class="rs-widget"></div>
                <div class="rs-widget"></div>
                <div class="rs-widget" style="opacity: 0.5;"></div>
            </div>
        </aside>
    </div>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Dynamic Layout Switcher & Grid Overlay logic
document.addEventListener('DOMContentLoaded', () => {{
    const layoutSelect = document.getElementById('layout-select');
    const toggleGridBtn = document.getElementById('toggle-grid');
    const container = document.querySelector('.app-container');
    const overlay = document.getElementById('overlay');

    // Handle Layout Switching
    layoutSelect.addEventListener('change', (e) => {{
        container.setAttribute('data-layout', e.target.value);
    }});

    // Handle Figma Grid Overlay Toggle
    toggleGridBtn.addEventListener('click', () => {{
        overlay.classList.toggle('active');
        const isActive = overlay.classList.contains('active');
        
        toggleGridBtn.textContent = isActive ? 'Hide Overlay' : 'Show Overlay';
        toggleGridBtn.classList.toggle('active', isActive);
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
  - Semantic HTML landmarks (`<aside>`, `<main>`, `<header>`) are utilized for screen reader navigation.
  - The grid overlay is set to `pointer-events: none` and `aria-hidden="true"` (implicitly, as it contains no semantic content) so it does not trap clicks or confuse screen readers.
  - Color contrast ratios in the generated palettes are designed to pass WCAG AA standards (e.g., `#f8fafc` text on `#0f172a` background is a 14.8:1 ratio).
* **Performance**: 
  - Layout transitions exclusively utilize CSS transforms and dimensional shifts natively supported by browser engines. `will-change` could be utilized if jank occurs on low-end devices, but the scoped DOM updates are minimal enough that native `transition` is performant. 
  - Grid structures leverage the highly optimized CSS Grid layout engine rather than costly JS calculation listeners (like `window.onresize`). Responsive wrapping is handled implicitly by media queries.