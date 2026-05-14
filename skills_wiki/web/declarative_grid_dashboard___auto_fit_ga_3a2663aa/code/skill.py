def create_component(
    output_dir: str,
    title_text: str = "Grid Layout Engine",
    body_text: str = "Declarative macro-areas and auto-fitting micro-tracks.",
    color_scheme: str = "dark",
    accent_color: str = "#ec4899", # Pinkish accent matching tutorial vibe
    width_px: int = 1000,
    height_px: int = 700,
    **kwargs,
) -> dict:
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Derived theme variables
    if color_scheme == "dark":
        bg_color = "#0b0f19"
        text_color = "#e2e8f0"
        text_muted = "#94a3b8"
        panel_bg = "rgba(255, 255, 255, 0.04)"
        panel_border = "rgba(255, 255, 255, 0.1)"
        grid_line = "rgba(255, 255, 255, 0.03)"
        shadow = "0 8px 32px rgba(0, 0, 0, 0.4)"
    else:
        bg_color = "#e2e8f0"
        text_color = "#0f172a"
        text_muted = "#475569"
        panel_bg = "rgba(255, 255, 255, 0.7)"
        panel_border = "rgba(0, 0, 0, 0.08)"
        grid_line = "rgba(0, 0, 0, 0.03)"
        shadow = "0 8px 32px rgba(0, 0, 0, 0.05)"

    css = f"""/* Base Reset & Variables */
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
    --panel-bg: {panel_bg};
    --panel-border: {panel_border};
    --shadow: {shadow};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background-color: var(--bg);
    /* Subtle background grid pattern to mimic dev tools */
    background-image: 
        linear-gradient(to right, {grid_line} 1px, transparent 1px),
        linear-gradient(to bottom, {grid_line} 1px, transparent 1px);
    background-size: 40px 40px;
    color: var(--text);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
}}

/* === 1. Macro Layout: CSS Grid Areas === */
.dashboard-shell {{
    width: var(--width);
    height: var(--height);
    background: var(--bg);
    border: 1px solid var(--panel-border);
    border-radius: 16px;
    box-shadow: var(--shadow);
    padding: 16px;
    
    /* The Core Technique: Declarative Layout Map */
    display: grid;
    grid-template-columns: 3fr 1fr;   /* Main is 3x wider than Aside */
    grid-template-rows: auto 1fr auto; /* Header and Footer auto-size, Main stretches */
    grid-template-areas: 
        "header header"
        "main aside"
        "footer footer";
    gap: 16px;
    overflow: hidden;
}}

/* Assigning DOM elements to the layout map */
.shell-header {{ grid-area: header; }}
.shell-main   {{ grid-area: main; }}
.shell-aside  {{ grid-area: aside; }}
.shell-footer {{ grid-area: footer; }}

/* Common panel styling */
.panel {{
    background: var(--panel-bg);
    border: 1px dashed var(--panel-border);
    border-radius: 12px;
    padding: 24px;
    display: flex;
    flex-direction: column;
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
}}

.shell-header {{
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
    border-bottom: 2px solid var(--accent);
}}

.shell-header h1 {{
    font-size: 1.5rem;
    font-weight: 600;
}}

.shell-header p {{
    color: var(--text-muted);
    font-size: 0.9rem;
}}

.shell-aside {{
    font-size: 0.9rem;
    color: var(--text-muted);
}}

.shell-footer {{
    text-align: center;
    font-size: 0.8rem;
    color: var(--text-muted);
    padding: 12px;
}}

/* === 2. Micro Layout: Responsive Auto-Fit Grid === */
.shell-main {{
    /* Nested Grid */
    display: grid;
    /* The Core Technique: Zero Media Query Responsive Grid */
    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    grid-auto-rows: 120px; /* Implicit row height */
    gap: 16px;
    
    padding: 0;
    border: none;
    background: transparent;
    overflow-y: auto;
    align-content: start; /* Pack items to top */
    padding-right: 8px; /* Scrollbar breathing room */
}}

/* Custom Scrollbar for Main Area */
.shell-main::-webkit-scrollbar {{
    width: 6px;
}}
.shell-main::-webkit-scrollbar-track {{
    background: transparent;
}}
.shell-main::-webkit-scrollbar-thumb {{
    background: var(--panel-border);
    border-radius: 10px;
}}

/* Gallery Items */
.grid-card {{
    background: var(--panel-bg);
    border: 1px solid var(--panel-border);
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 600;
    font-size: 1.2rem;
    color: var(--text-muted);
    transition: all 0.2s ease;
    cursor: pointer;
    position: relative;
    overflow: hidden;
}}

.grid-card::before {{
    content: '';
    position: absolute;
    top: 0; left: 0; width: 4px; height: 100%;
    background: var(--accent);
    transform: scaleY(0);
    transform-origin: bottom;
    transition: transform 0.3s ease;
}}

.grid-card:hover {{
    border-color: var(--accent);
    color: var(--text);
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}}

.grid-card:hover::before {{
    transform: scaleY(1);
}}

/* Specific item demonstrating spanning */
.card-span-2 {{
    grid-column: span 2;
    background: rgba(236, 72, 153, 0.1); /* Subtle accent tint */
}}
"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>

    <div class="dashboard-shell">
        
        <header class="panel shell-header">
            <h1>{title_text}</h1>
            <p>{body_text}</p>
        </header>

        <aside class="panel shell-aside">
            <h3>Aside Panel</h3>
            <p style="margin-top: 1rem; line-height: 1.5;">Notice how this panel is defined strictly by the grid-template-areas map, keeping the layout logic entirely in CSS.</p>
        </aside>

        <!-- Main content contains the nested auto-fit grid -->
        <main class="shell-main" id="gallery">
            <!-- Cards injected via JS to demonstrate wrapping -->
        </main>

        <footer class="panel shell-footer">
            grid-template-areas: "footer footer"
        </footer>

    </div>

    <script src="script.js"></script>
</body>
</html>"""

    js = f"""document.addEventListener('DOMContentLoaded', () => {{
    const gallery = document.getElementById('gallery');
    
    // Generate sample grid items to demonstrate auto-fit wrapping
    const totalItems = 12;
    
    for (let i = 1; i <= totalItems; i++) {{
        const card = document.createElement('div');
        card.className = 'grid-card';
        
        // Make the 4th item span two columns to show varied sizing
        if (i === 4) {{
            card.classList.add('card-span-2');
            card.textContent = `Span 2`;
        }} else {{
            card.textContent = `Item ${{i}}`;
        }}
        
        gallery.appendChild(card);
    }}
}});
"""

    # Write files
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
