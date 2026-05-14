# Animated Sidebar to Bottom-Nav with Grid Height Transitions

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Animated Sidebar to Bottom-Nav with Grid Height Transitions

* **Core Visual Mechanism**: A modern, responsive navigation system that utilizes a dual-state design. On large screens, it behaves as a fixed sidebar with smoothly animated accordion dropdowns. On smaller screens, it seamlessly transforms into a fixed bottom navigation bar, with submenus popping up from the bottom. The defining technical signature is the use of `grid-template-rows: 0fr` to `1fr` for animating the height of the dropdown menus, entirely avoiding clunky JavaScript height calculations.
* **Why Use This Skill (Rationale)**: This pattern solves the ubiquitous challenge of complex navigation hierarchies on mobile devices. By transforming an expansive desktop sidebar into an app-like bottom navigation bar, the UI remains highly accessible for thumb-reachability. The CSS Grid height transition ensures buttery-smooth animations (60fps) because the browser handles the interpolation natively.
* **Overall Applicability**: Ideal for SaaS application dashboards, admin panels, complex documentation sites, and progressive web apps (PWAs) that require multi-level navigation.
* **Browser Compatibility**: Requires modern browsers supporting CSS Grid (widely supported), CSS Grid transitions (supported in Chrome 107+, Safari 16.4+, Firefox 109+), and CSS Container Queries (supported in all major browsers since late 2022). 

### 2. Visual & Technical Breakdown

* **Step A: Core Visual Elements**
  - **Color Logic**: Utilizes a semantic color token system (Background, Surface, Border, Text, Text Muted, Accent, Hover). The sidebar and cards rest on a slightly elevated `Surface` color, distinct from the deep `Background`.
  - **Typography**: Clean, sans-serif stack (`'Inter', system-ui`) focused on legibility. Links have a weight of 500, with a muted text color that brightens on hover.
  - **Icons**: SVG paths with `currentColor` strokes for easy theming. Active states dynamically swap the stroke to the accent color.

* **Step B: Layout & Compositional Style**
  - **Container Queries over Media Queries**: The main wrapper acts as an inline-size container. This makes the sidebar responsive to its *parent container's width*, making the component highly modular and isolated from global viewport constraints.
  - **Desktop Layout**: CSS Grid defining a `260px` fixed column for the sidebar and `1fr` for the main content.
  - **Mobile Layout**: Modifies the grid to a single column, pinning the navigation to the bottom (`grid-row: 2; height: 70px`). The links switch to `flex-direction: row`, hiding text labels and arrows to maximize space.

* **Step C: Interactive Behavior & Animations**
  - **Dropdown Expansion**: A pure CSS mechanism using `display: grid; grid-template-rows: 0fr; transition: 300ms ease`. Applying a `.show` class changes it to `1fr`, naturally animating the height.
  - **Arrow Rotation**: The right-aligned chevron SVG rotates `180deg` via a CSS `transform` when the dropdown is active.
  - **Event Logic**: Minimal JavaScript is used strictly for state management—toggling the `.show` class on the clicked element and removing it from sibling dropdowns to ensure an accordion effect.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **Layout Structure** | CSS Grid | Handles the `260px` to `1fr` split cleanly, and easily restructures for the bottom nav. |
| **Dropdown Animation** | CSS `grid-template-rows` | The most robust modern way to animate to `auto` height without JavaScript `scrollHeight` measurements. |
| **Responsiveness** | CSS Container Queries | Encapsulates the component. It adapts based on available width, making it reusable anywhere, not just as a full-page layout. |
| **State Management** | Vanilla JS | A lightweight script simply toggles classes (`.show`), keeping concerns separated. |

#### 3b. Complete Reproduction Code

```python
def create_component(
    output_dir: str,
    title_text: str = "Dashboard Overview",
    body_text: str = "This component demonstrates a responsive navigation system. Resize the component to see the sidebar seamlessly transform into a mobile-friendly bottom navigation bar.",
    color_scheme: str = "dark",
    accent_color: str = "#3b82f6",
    width_px: int = 1000,
    height_px: int = 700,
    **kwargs,
) -> dict:
    """
    Create a responsive sidebar-to-bottom-nav component using CSS Grid height animations.
    """
    import os
    os.makedirs(output_dir, exist_ok=True)

    # Derive theme colors
    if color_scheme == "dark":
        bg_color = "#0f172a"
        text_color = "#f8fafc"
        text_muted = "#94a3b8"
        surface_color = "#1e293b"
        hover_color = "#334155"
        border_color = "#334155"
    else:
        bg_color = "#f8fafc"
        text_color = "#0f172a"
        text_muted = "#64748b"
        surface_color = "#ffffff"
        hover_color = "#f1f5f9"
        border_color = "#e2e8f0"

    # Reusable SVGs
    icon_home = '<svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path><polyline points="9 22 9 12 15 12 15 22"></polyline></svg>'
    icon_dashboard = '<svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="7" height="9"></rect><rect x="14" y="3" width="7" height="5"></rect><rect x="14" y="12" width="7" height="9"></rect><rect x="3" y="16" width="7" height="5"></rect></svg>'
    icon_folder = '<svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"></path></svg>'
    icon_list = '<svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="8" y1="6" x2="21" y2="6"></line><line x1="8" y1="12" x2="21" y2="12"></line><line x1="8" y1="18" x2="21" y2="18"></line><line x1="3" y1="6" x2="3.01" y2="6"></line><line x1="3" y1="12" x2="3.01" y2="12"></line><line x1="3" y1="18" x2="3.01" y2="18"></line></svg>'
    icon_arrow = '<svg class="arrow" viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"></polyline></svg>'
    icon_logo = f'<svg viewBox="0 0 24 24" width="28" height="28" fill="none" stroke="var(--accent)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="12 2 2 7 12 12 22 7 12 2"></polygon><polyline points="2 17 12 22 22 17"></polyline><polyline points="2 12 12 17 22 12"></polyline></svg>'

    css = f"""/* Animated Sidebar Component */
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
    --hover: {hover_color};
    --border: {border_color};
}}

body {{
    font-family: 'Inter', system-ui, sans-serif;
    background: #000; /* Contrast body against component */
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 100vh;
}}

.app-wrapper {{
    width: {width_px}px;
    max-width: 100vw;
    height: {height_px}px;
    max-height: 100vh;
    container-type: inline-size;
    container-name: app;
}}

.app-container {{
    display: grid;
    grid-template-columns: 260px 1fr;
    width: 100%;
    height: 100%;
    background: var(--bg);
    color: var(--text);
    overflow: hidden;
    position: relative;
    border-radius: 16px;
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
}}

/* --- SIDEBAR DESKTOP --- */
#sidebar {{
    background: var(--surface);
    border-right: 1px solid var(--border);
    display: flex;
    flex-direction: column;
    overflow-y: auto;
    z-index: 10;
}}

.sidebar-header {{
    padding: 1.5rem;
    display: flex;
    align-items: center;
    gap: 0.75rem;
    font-size: 1.25rem;
    font-weight: 700;
    color: var(--text);
    border-bottom: 1px solid var(--border);
}}

.nav-links {{
    list-style: none;
    padding: 1rem;
    display: flex;
    flex-direction: column;
    gap: 0.25rem;
}}

.nav-links a, .dropdown-btn {{
    display: flex;
    align-items: center;
    gap: 0.75rem;
    padding: 0.75rem 1rem;
    color: var(--text-muted);
    text-decoration: none;
    border-radius: 8px;
    cursor: pointer;
    background: transparent;
    border: none;
    font-size: 0.95rem;
    font-weight: 500;
    font-family: inherit;
    width: 100%;
    text-align: left;
    transition: background 0.2s, color 0.2s;
}}

.nav-links a:hover, .dropdown-btn:hover {{
    background: var(--hover);
    color: var(--text);
}}

/* Active State */
.nav-links li.active > a {{
    color: var(--accent);
    background: var(--hover);
}}

.nav-links li.active > a svg {{
    stroke: var(--accent);
}}

.nav-links a svg, .dropdown-btn svg {{
    flex-shrink: 0;
}}

.arrow {{
    margin-left: auto;
    transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}}

/* --- DROPDOWN GRID ANIMATION --- */
.sub-menu {{
    display: grid;
    grid-template-rows: 0fr;
    transition: grid-template-rows 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}}

.sub-menu-inner {{
    overflow: hidden;
}}

.sub-menu-inner ul {{
    list-style: none;
    padding: 0.5rem 0 0.5rem 2.75rem;
    display: flex;
    flex-direction: column;
    gap: 0.25rem;
}}

.sub-menu-inner a {{
    padding: 0.5rem 1rem;
    font-size: 0.9rem;
    color: var(--text-muted);
}}

.dropdown.show .sub-menu {{
    grid-template-rows: 1fr;
}}

.dropdown.show .arrow {{
    transform: rotate(180deg);
}}

/* --- MAIN CONTENT --- */
#main-content {{
    background: var(--bg);
    overflow-y: auto;
    display: flex;
    flex-direction: column;
}}

.content-header {{
    padding: 2rem;
    border-bottom: 1px solid var(--border);
}}

.content-header h1 {{
    font-size: 1.5rem;
    font-weight: 600;
}}

.content-body {{
    padding: 2rem;
    display: grid;
    gap: 1.5rem;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    align-content: start;
}}

.card {{
    background: var(--surface);
    padding: 1.5rem;
    border-radius: 12px;
    border: 1px solid var(--border);
}}

.card h2 {{
    margin-bottom: 0.75rem;
    font-size: 1.1rem;
    font-weight: 600;
}}

.card p {{
    color: var(--text-muted);
    line-height: 1.6;
    font-size: 0.95rem;
}}

/* --- MOBILE CONTAINER QUERY (Bottom Nav) --- */
@container app (max-width: 800px) {{
    .app-container {{
        grid-template-columns: 1fr;
        grid-template-rows: 1fr 70px;
    }}

    #sidebar {{
        grid-column: 1;
        grid-row: 2;
        flex-direction: row;
        border-right: none;
        border-top: 1px solid var(--border);
        overflow-y: visible;
        overflow-x: visible; /* Allows submenu popups */
    }}

    .sidebar-header {{
        display: none;
    }}

    .nav-links {{
        flex-direction: row;
        padding: 0;
        gap: 0;
        width: 100%;
    }}

    .nav-links > li {{
        flex: 1;
    }}

    .nav-links a, .dropdown-btn {{
        justify-content: center;
        border-radius: 0;
        padding: 0;
        height: 100%;
    }}

    .nav-links span, .arrow {{
        display: none;
    }}

    /* Submenus pop up above the nav bar */
    .dropdown {{
        position: static; 
    }}

    .sub-menu {{
        position: absolute;
        bottom: 70px;
        left: 0;
        width: 100%;
        background: var(--surface);
        border-top: 1px solid var(--border);
        box-shadow: 0 -10px 15px -3px rgba(0, 0, 0, 0.1);
        grid-template-rows: 0fr; /* Animation still works bottom-up! */
    }}

    .sub-menu-inner ul {{
        flex-direction: row;
        padding: 1rem;
        gap: 0.75rem;
        overflow-x: auto;
        white-space: nowrap;
    }}

    .sub-menu-inner a {{
        background: var(--bg);
        border: 1px solid var(--border);
        padding: 0.6rem 1.2rem;
        border-radius: 99px; /* Pill shape */
        display: block;
        color: var(--text);
    }}
    
    .sub-menu-inner a:hover {{
        border-color: var(--accent);
        color: var(--accent);
    }}
}}
"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="app-wrapper">
        <div class="app-container">
            
            <nav id="sidebar">
                <div class="sidebar-header">
                    {icon_logo}
                    <span>BrandUI</span>
                </div>
                
                <ul class="nav-links">
                    <li>
                        <a href="#">
                            {icon_home}
                            <span>Home</span>
                        </a>
                    </li>
                    <li class="active">
                        <a href="#">
                            {icon_dashboard}
                            <span>Dashboard</span>
                        </a>
                    </li>
                    
                    <li class="dropdown">
                        <button class="dropdown-btn">
                            {icon_folder}
                            <span>Projects</span>
                            {icon_arrow}
                        </button>
                        <div class="sub-menu">
                            <div class="sub-menu-inner">
                                <ul>
                                    <li><a href="#">Active Projects</a></li>
                                    <li><a href="#">Archived</a></li>
                                    <li><a href="#">Team Folders</a></li>
                                </ul>
                            </div>
                        </div>
                    </li>
                    
                    <li class="dropdown">
                        <button class="dropdown-btn">
                            {icon_list}
                            <span>Tasks</span>
                            {icon_arrow}
                        </button>
                        <div class="sub-menu">
                            <div class="sub-menu-inner">
                                <ul>
                                    <li><a href="#">My Queue</a></li>
                                    <li><a href="#">Backlog</a></li>
                                    <li><a href="#">Completed</a></li>
                                </ul>
                            </div>
                        </div>
                    </li>
                </ul>
            </nav>

            <main id="main-content">
                <div class="content-header">
                    <h1>{title_text}</h1>
                </div>
                <div class="content-body">
                    <div class="card">
                        <h2>Architecture Note</h2>
                        <p>{body_text}</p>
                    </div>
                    <div class="card">
                        <h2>CSS Grid Animations</h2>
                        <p>The dropdowns expand using <code>grid-template-rows: 0fr</code> to <code>1fr</code>. This avoids heavy JavaScript height calculations and keeps animations performant.</p>
                    </div>
                    <div class="card">
                        <h2>Container Queries</h2>
                        <p>Because the responsive breakpoints are tied to the <code>@container</code> rather than the viewport, this entire component can be embedded anywhere within an app.</p>
                    </div>
                </div>
            </main>

        </div>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    js = f"""document.addEventListener('DOMContentLoaded', () => {{
    const dropdownBtns = document.querySelectorAll('.dropdown-btn');

    dropdownBtns.forEach(btn => {{
        btn.addEventListener('click', (e) => {{
            const currentDropdown = btn.closest('.dropdown');
            
            // Accordion logic: close other dropdowns
            document.querySelectorAll('.dropdown.show').forEach(dropdown => {{
                if (dropdown !== currentDropdown) {{
                    dropdown.classList.remove('show');
                }}
            }});
            
            // Toggle current dropdown
            currentDropdown.classList.toggle('show');
        }});
    }});

    // Optional: Close dropdowns when clicking outside (useful for mobile bottom nav)
    document.addEventListener('click', (e) => {{
        if (!e.target.closest('.dropdown')) {{
            document.querySelectorAll('.dropdown.show').forEach(dropdown => {{
                dropdown.classList.remove('show');
            }});
        }}
    }});
}});"""

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