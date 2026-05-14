def create_component(
    output_dir: str,
    title_text: str = "Grid Dashboard",
    body_text: str = "CSS Grid enables complex app layouts. This module uses named areas for the shell, auto-fit for fluid cards, and same-cell overlapping for overlays.",
    color_scheme: str = "dark",
    accent_color: str = "#8b5cf6",
    width_px: int = 1000,
    height_px: int = 700,
    **kwargs,
) -> dict:
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Helper to calculate rgba values for gradients
    def hex_to_rgba(h, alpha):
        h = h.lstrip('#')
        if len(h) == 3: h = ''.join([c*2 for c in h])
        r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
        return f"rgba({r}, {g}, {b}, {alpha})"

    if color_scheme == "dark":
        bg_color = "#0f1115"
        text_color = "#ffffff"
        text_muted = "#9ca3af"
        surface_color = "rgba(255, 255, 255, 0.04)"
        border_color = "rgba(255, 255, 255, 0.08)"
        body_bg = "#050505"
        overlay_grad = "rgba(0,0,0,0.85)"
    else:
        bg_color = "#ffffff"
        text_color = "#111827"
        text_muted = "#4b5563"
        surface_color = "rgba(0, 0, 0, 0.03)"
        border_color = "rgba(0, 0, 0, 0.08)"
        body_bg = "#e5e7eb"
        overlay_grad = "rgba(0,0,0,0.7)"

    accent_alpha = hex_to_rgba(accent_color, 0.15)

    css = f"""/* Grid Dashboard Component */
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
    --border: {border_color};
    --accent: {accent_color};
    --accent-alpha: {accent_alpha};
    --overlay: {overlay_grad};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Inter', system-ui, sans-serif;
    background: {body_bg};
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 20px;
}}

.container {{
    width: 100%;
    max-width: var(--width);
    height: var(--height);
    background: var(--bg);
    color: var(--text);
    border-radius: 16px;
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
    padding: 24px;
    /* Establishes a container context for macro-layout responsiveness */
    container-type: inline-size;
    overflow: hidden;
}}

/* MACRO LAYOUT: The App Shell */
.app-shell {{
    display: grid;
    grid-template-areas:
        "header header"
        "main aside"
        "footer footer";
    grid-template-columns: 1fr 280px;
    grid-template-rows: 60px 1fr 40px;
    gap: 20px;
    height: 100%;
}}

/* App Shell Component Panels */
.shell-panel {{
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 16px 20px;
}}

.header {{
    grid-area: header;
    display: grid;
    align-items: center;
}}

.header h1 {{
    font-size: 1.25rem;
    font-weight: 600;
}}

.aside {{
    grid-area: aside;
    display: grid;
    align-content: start;
    gap: 16px;
}}

.aside h3 {{
    color: var(--accent);
    font-size: 0.9rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    font-weight: 700;
}}

.aside p {{
    color: var(--text-muted);
    font-size: 0.9rem;
    line-height: 1.6;
}}

.stats {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 12px;
}}

.stat-box {{
    background: var(--bg);
    border: 1px solid var(--border);
    padding: 12px;
    border-radius: 8px;
    display: grid;
    gap: 4px;
}}

.stat-value {{
    font-size: 1.25rem;
    font-weight: 700;
    color: var(--accent);
}}

.stat-label {{
    font-size: 0.75rem;
    color: var(--text-muted);
}}

.footer {{
    grid-area: footer;
    display: grid;
    align-items: center;
    justify-items: center;
    font-size: 0.85rem;
    color: var(--text-muted);
}}

/* MICRO LAYOUT: Fluid Inner Gallery */
.main {{
    grid-area: main;
    overflow-y: auto;
    padding-right: 8px;
    display: grid;
    /* Zero-media-query responsiveness! */
    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    /* Implicit grid rule */
    grid-auto-rows: 150px; 
    gap: 16px;
    align-content: start;
}}

/* Custom Scrollbar for the main area */
.main::-webkit-scrollbar {{ width: 6px; }}
.main::-webkit-scrollbar-track {{ background: transparent; }}
.main::-webkit-scrollbar-thumb {{ background: var(--border); border-radius: 10px; }}

/* NANO LAYOUT: Layered Card Component */
.card {{
    /* Explicit 1x1 grid to support layering */
    display: grid;
    grid-template-columns: 1fr;
    grid-template-rows: 1fr;
    border-radius: 12px;
    overflow: hidden;
    cursor: pointer;
    border: 1px solid var(--border);
    animation: fadeUp 0.6s ease-out backwards;
}}

.span-2 {{
    grid-column: span 2;
}}

/* Layer 0: Background */
.card-bg {{
    grid-column: 1 / -1;
    grid-row: 1 / -1;
    background: linear-gradient(135deg, var(--surface), var(--accent-alpha));
    transition: transform 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}}

/* Layer 1: Text Overlay */
.card-content {{
    grid-column: 1 / -1;
    grid-row: 1 / -1;
    z-index: 1; /* Elevates above background */
    display: grid;
    align-self: end; /* Pins to bottom */
    padding: 16px;
    background: linear-gradient(to top, var(--overlay) 0%, transparent 100%);
    color: #ffffff;
    font-weight: 500;
    font-size: 0.95rem;
}}

/* Layer 2: Floating Badge */
.card-badge {{
    grid-column: 1 / -1;
    grid-row: 1 / -1;
    z-index: 2;
    justify-self: end; /* Pins to right */
    align-self: start; /* Pins to top */
    margin: 12px;
    background: var(--accent);
    color: #fff;
    padding: 4px 10px;
    border-radius: 20px;
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    box-shadow: 0 4px 12px rgba(0,0,0,0.2);
}}

/* Interaction */
.card:hover .card-bg {{
    transform: scale(1.08);
}}

@keyframes fadeUp {{
    from {{ opacity: 0; transform: translateY(15px); }}
    to {{ opacity: 1; transform: translateY(0); }}
}}

/* CONTAINER QUERY: Responsive Macro Layout */
@container (max-width: 650px) {{
    .app-shell {{
        grid-template-areas:
            "header"
            "main"
            "aside"
            "footer";
        grid-template-columns: 1fr;
        grid-template-rows: auto 1fr auto auto;
    }}
    .span-2 {{
        grid-column: span 1; /* Reset spans on small screens */
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
    <div class="container">
        <div class="app-shell">
            
            <header class="header shell-panel">
                <h1>{title_text}</h1>
            </header>

            <main class="main">
                <!-- Static span-2 item -->
                <div class="card span-2" style="animation-delay: 0s;">
                    <div class="card-bg"></div>
                    <div class="card-badge">Featured</div>
                    <div class="card-content">System Overview</div>
                </div>
                <!-- Dynamic items injected by JS -->
            </main>

            <aside class="aside shell-panel">
                <h3>Insights</h3>
                <p>{body_text}</p>
                <div class="stats">
                    <div class="stat-box">
                        <span class="stat-value">142</span>
                        <span class="stat-label">Projects</span>
                    </div>
                    <div class="stat-box">
                        <span class="stat-value">98%</span>
                        <span class="stat-label">Uptime</span>
                    </div>
                </div>
            </aside>

            <footer class="footer shell-panel">
                <p>&copy; 2024 CSS Grid System. All elements positioned declaratively.</p>
            </footer>

        </div>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    js = """// Implicit Grid Generation
document.addEventListener('DOMContentLoaded', () => {
    const gallery = document.querySelector('.main');
    
    // Simulate fetching widgets
    const widgets = [
        'Analytics Engine', 
        'Server Logs', 
        'Network Traffic', 
        'User Metrics', 
        'Database Load',
        'Security Audits'
    ];

    widgets.forEach((widget, index) => {
        const card = document.createElement('div');
        card.className = 'card';
        // Staggered animation
        card.style.animationDelay = `${(index + 1) * 0.1}s`;

        card.innerHTML = `
            <div class="card-bg"></div>
            ${index === 1 ? '<div class="card-badge">Alert</div>' : ''}
            <div class="card-content">
                <span>${widget}</span>
            </div>
        `;
        gallery.appendChild(card);
    });
});
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
