def create_component(
    output_dir: str,
    title_text: str = "GridMaster Dashboard",
    body_text: str = "Responsive bento-box layout using auto-fit and dense packing.",
    color_scheme: str = "dark",
    accent_color: str = "#ec407a",
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors ===
    if color_scheme == "dark":
        bg_color = "#0a0b10"
        grid_dot = "rgba(255,255,255,0.06)"
        surface_color = "rgba(255,255,255,0.03)"
        surface_hover = "rgba(255,255,255,0.06)"
        surface_darker = "rgba(0,0,0,0.2)"
        border_color = "rgba(255,255,255,0.08)"
        text_primary = "#f3f4f6"
        text_secondary = "#9ca3af"
    else:
        bg_color = "#f3f4f6"
        grid_dot = "rgba(0,0,0,0.06)"
        surface_color = "#ffffff"
        surface_hover = "#f9fafb"
        surface_darker = "#e5e7eb"
        border_color = "rgba(0,0,0,0.08)"
        text_primary = "#111827"
        text_secondary = "#4b5563"

    # === CSS ===
    css = f"""/* CSS Grid Master Dashboard */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --grid-dot: {grid_dot};
    --surface: {surface_color};
    --surface-hover: {surface_hover};
    --surface-darker: {surface_darker};
    --border: {border_color};
    --text-primary: {text_primary};
    --text-secondary: {text_secondary};
    --accent: {accent_color};
    --accent-transparent: color-mix(in srgb, var(--accent) 15%, transparent);
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background-color: var(--bg);
    background-image: radial-gradient(var(--grid-dot) 1px, transparent 1px);
    background-size: 24px 24px;
    color: var(--text-primary);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
}}

/* Macro Layout: The App Shell */
.dashboard-container {{
    width: var(--width);
    height: var(--height);
    max-width: 95vw;
    max-height: 95vh;
    display: grid;
    grid-template-columns: 240px 1fr;
    grid-template-rows: 80px 1fr;
    grid-template-areas:
        "sidebar header"
        "sidebar main";
    background: var(--bg);
    border: 1px solid var(--border);
    border-radius: 16px;
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
    overflow: hidden;
}}

/* Sidebar Area */
.sidebar {{
    grid-area: sidebar;
    background: var(--surface-darker);
    border-right: 1px solid var(--border);
    padding: 1.5rem;
    display: flex;
    flex-direction: column;
    gap: 2rem;
}}

.logo {{
    font-size: 1.25rem;
    font-weight: 700;
    display: flex;
    align-items: center;
    gap: 0.5rem;
    color: var(--text-primary);
}}

.logo svg {{
    width: 24px;
    height: 24px;
    color: var(--accent);
}}

.nav-links {{
    list-style: none;
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
}}

.nav-links li {{
    padding: 0.75rem 1rem;
    border-radius: 8px;
    color: var(--text-secondary);
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s ease;
}}

.nav-links li:hover {{
    background: var(--surface);
    color: var(--text-primary);
}}

.nav-links li.active {{
    background: var(--accent-transparent);
    color: var(--accent);
    font-weight: 600;
}}

/* Header Area */
.header {{
    grid-area: header;
    border-bottom: 1px solid var(--border);
    padding: 0 2rem;
    display: flex;
    flex-direction: column;
    justify-content: center;
    background: var(--surface-darker);
}}

.header h1 {{
    font-size: 1.25rem;
    color: var(--text-primary);
    margin-bottom: 0.25rem;
}}

.header p {{
    color: var(--text-secondary);
    font-size: 0.875rem;
}}

/* Micro Layout: The Bento Box Grid */
.bento-grid {{
    grid-area: main;
    display: grid;
    /* Core responsive technique from tutorial */
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    grid-auto-rows: minmax(180px, auto);
    grid-auto-flow: dense; /* Fills gaps left by spanned items */
    gap: 1.5rem;
    padding: 1.5rem;
    overflow-y: auto;
}}

/* Custom Scrollbar for Grid */
.bento-grid::-webkit-scrollbar {{
    width: 8px;
}}
.bento-grid::-webkit-scrollbar-track {{
    background: transparent;
}}
.bento-grid::-webkit-scrollbar-thumb {{
    background: var(--border);
    border-radius: 4px;
}}
.bento-grid::-webkit-scrollbar-thumb:hover {{
    background: var(--text-secondary);
}}

/* Grid Item (Card) Base */
.card {{
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.5rem;
    display: flex;
    flex-direction: column;
    position: relative;
    overflow: hidden;
    transition: transform 0.2s ease, border-color 0.2s ease, box-shadow 0.2s ease;
}}

/* Mouse Follow Glow Effect */
.card::before {{
    content: "";
    position: absolute;
    top: 0; left: 0; width: 100%; height: 100%;
    background: radial-gradient(
        600px circle at var(--mouse-x) var(--mouse-y),
        rgba(255, 255, 255, 0.05),
        transparent 40%
    );
    z-index: 0;
    pointer-events: none;
    opacity: 0;
    transition: opacity 0.3s ease;
}}

.card:hover {{
    border-color: color-mix(in srgb, var(--accent) 40%, var(--border));
    transform: translateY(-2px);
    box-shadow: 0 10px 20px -10px rgba(0,0,0,0.5);
}}

.card:hover::before {{
    opacity: 1;
}}

.card > * {{
    position: relative;
    z-index: 1;
}}

/* Card Content Typography */
.card-title {{
    font-size: 1.125rem;
    font-weight: 600;
    color: var(--text-primary);
    margin-bottom: 0.5rem;
}}

.card-desc {{
    font-size: 0.875rem;
    color: var(--text-secondary);
    line-height: 1.5;
}}

/* Highlighted Accent Card */
.card.accent {{
    background: linear-gradient(135deg, var(--surface), transparent);
    border-color: var(--accent);
}}
.card.accent::after {{
    content: "";
    position: absolute;
    inset: 0;
    background: radial-gradient(
        400px circle at var(--mouse-x) var(--mouse-y),
        var(--accent),
        transparent 40%
    );
    z-index: 0;
    pointer-events: none;
    opacity: 0;
    transition: opacity 0.3s ease;
}}
.card.accent:hover::after {{
    opacity: 0.12; /* Subtle tint on hover */
}}

.stats-large {{
    font-size: 3rem;
    font-weight: 700;
    color: var(--text-primary);
    margin-top: auto;
}}

/* Visual Widgets */
.bar-chart {{
    display: flex;
    align-items: flex-end;
    gap: 8px;
    height: 80px;
    margin-top: auto;
}}
.bar {{
    flex: 1;
    background: var(--surface-hover);
    border-radius: 4px 4px 0 0;
    transition: height 0.3s, background 0.3s;
}}
.card:hover .bar {{
    background: var(--accent);
}}

.circle-chart {{
    margin: auto;
    width: 80px;
    height: 80px;
    border-radius: 50%;
    border: 4px solid var(--accent);
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 700;
    color: var(--accent);
}}

/* Z-Index Overlap Container Demonstration */
.grid-stack {{
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    grid-template-rows: repeat(3, 1fr);
    gap: 0.5rem;
    flex-grow: 1;
    margin-top: 1rem;
}}
.box {{
    border-radius: 6px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.75rem;
    font-weight: 600;
}}
.base-box {{
    grid-column: 1 / 4;
    grid-row: 1 / 3;
    background: var(--surface-hover);
    border: 1px dashed var(--text-secondary);
    color: var(--text-secondary);
}}
.float-box {{
    grid-column: 2 / 4;
    grid-row: 2 / 4;
    background: var(--accent);
    color: #fff;
    z-index: 10;
    box-shadow: 0 10px 15px -3px rgba(0,0,0,0.5);
}}

/* Spanning Modifiers */
@media (min-width: 600px) {{
    .col-span-2 {{ grid-column: span 2; }}
    .row-span-2 {{ grid-row: span 2; }}
}}

/* Responsive Macro Layout Fallback */
@media (max-width: 800px) {{
    .dashboard-container {{
        grid-template-columns: 1fr;
        grid-template-rows: auto auto 1fr;
        grid-template-areas:
            "header"
            "sidebar"
            "main";
    }}
    .sidebar {{
        flex-direction: row;
        padding: 1rem 2rem;
        gap: 1rem;
        overflow-x: auto;
        border-right: none;
        border-bottom: 1px solid var(--border);
    }}
    .nav-links {{
        flex-direction: row;
        align-items: center;
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
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="dashboard-container">
        <!-- Structural Area: Sidebar -->
        <nav class="sidebar">
            <div class="logo">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <rect x="3" y="3" width="7" height="7" rx="1"/>
                    <rect x="14" y="3" width="7" height="7" rx="1"/>
                    <rect x="14" y="14" width="7" height="7" rx="1"/>
                    <rect x="3" y="14" width="7" height="7" rx="1"/>
                </svg>
                GridMaster
            </div>
            <ul class="nav-links">
                <li class="active">Overview</li>
                <li>Layouts</li>
                <li>Components</li>
                <li>Settings</li>
            </ul>
        </nav>

        <!-- Structural Area: Header -->
        <header class="header">
            <h1>{title_text}</h1>
            <p>{body_text}</p>
        </header>

        <!-- Structural Area: Main (Bento Grid) -->
        <main class="bento-grid">
            
            <!-- Grid Item: Explicit Row/Col Spans -->
            <div class="card accent col-span-2 row-span-2">
                <h3 class="card-title">Grid Subsystem Spans</h3>
                <p class="card-desc">This prominent block utilizes <code>grid-column: span 2</code> and <code>grid-row: span 2</code> to secure dominant visual hierarchy within the auto-fit flow.</p>
                <div class="stats-large">CSS Grid</div>
            </div>

            <!-- Grid Item: Fluid Scale -->
            <div class="card">
                <h3 class="card-title">Auto-Fit Columns</h3>
                <p class="card-desc">Tracks resize intrinsically without rigid media queries via <code>minmax()</code>.</p>
            </div>

            <!-- Grid Item: Layered Z-Index -->
            <div class="card row-span-2">
                <h3 class="card-title">Z-Index Stacking</h3>
                <p class="card-desc">Grid items naturally support overlap by mapping to shared tracks.</p>
                <div class="grid-stack">
                    <div class="box base-box">Base Row 1-2</div>
                    <div class="box float-box">Floating Z:10</div>
                </div>
            </div>

            <!-- Grid Item: Generic Content -->
            <div class="card">
                <h3 class="card-title">Fluid Units</h3>
                <p class="card-desc">Leveraging the fractional <code>fr</code> unit.</p>
                <div class="circle-chart">1fr</div>
            </div>

            <!-- Grid Item: Dense Flow Demonstration -->
            <div class="card col-span-2">
                <h3 class="card-title">Grid Auto-Flow: Dense</h3>
                <p class="card-desc">The dense algorithm back-fills gaps caused by spanned items to maintain visual density.</p>
                <div class="bar-chart">
                    <div class="bar" style="height: 60%"></div>
                    <div class="bar" style="height: 80%"></div>
                    <div class="bar" style="height: 40%"></div>
                    <div class="bar" style="height: 100%"></div>
                    <div class="bar" style="height: 70%"></div>
                    <div class="bar" style="height: 90%"></div>
                    <div class="bar" style="height: 50%"></div>
                </div>
            </div>
            
            <div class="card">
                <h3 class="card-title">Track Sizing</h3>
                <p class="card-desc">Implicit row handling limits.</p>
            </div>

        </main>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Mouse-following gradient glow effect for Bento Grid cards
document.addEventListener('DOMContentLoaded', () => {{
    const cards = document.querySelectorAll('.card');

    cards.forEach(card => {{
        card.addEventListener('mousemove', e => {{
            // Calculate mouse position relative to the specific card
            const rect = card.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            
            // Pass coordinates to CSS via custom properties
            card.style.setProperty('--mouse-x', `${{x}}px`);
            card.style.setProperty('--mouse-y', `${{y}}px`);
        }});
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
