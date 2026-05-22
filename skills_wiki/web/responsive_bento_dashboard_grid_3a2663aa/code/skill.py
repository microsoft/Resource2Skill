def create_component(
    output_dir: str,
    title_text: str = "Bento Dashboard",
    body_text: str = "CSS Grid Architecture",
    color_scheme: str = "dark",
    accent_color: str = "#e91e63",
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Responsive Bento Dashboard Grid.
    
    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors ===
    if color_scheme == "dark":
        bg_color = "#0a0c10"
        text_color = "#f0f6fc"
        surface_color = "#161b22"
        surface_border = "rgba(255, 255, 255, 0.1)"
        shadow = "rgba(0, 0, 0, 0.5)"
    else:
        bg_color = "#f6f8fa"
        text_color = "#24292f"
        surface_color = "#ffffff"
        surface_border = "rgba(0, 0, 0, 0.1)"
        shadow = "rgba(0, 0, 0, 0.08)"

    # === CSS ===
    css = f"""/* Responsive Bento Dashboard Grid */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --text: {text_color};
    --accent: {accent_color};
    --surface: {surface_color};
    --border: {surface_border};
    --shadow: {shadow};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background: var(--bg);
    color: var(--text);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
}}

/* MACRO LAYOUT: The App Shell */
.app-container {{
    width: 100%;
    max-width: var(--width);
    min-height: calc(var(--height) * 0.9);
    padding: 24px;
    
    display: grid;
    /* 3 fractional units for main, 1 for sidebar */
    grid-template-columns: 3fr 1fr;
    grid-template-rows: auto 1fr auto;
    
    /* Explicit visual placement mapping */
    grid-template-areas:
        "header header"
        "main sidebar"
        "footer footer";
    gap: 24px;
}}

/* Shell Structural Areas */
.header {{ grid-area: header; }}
.main {{ grid-area: main; }}
.sidebar {{ grid-area: sidebar; }}
.footer {{ grid-area: footer; }}

.header, .sidebar, .footer {{
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 24px;
    box-shadow: 0 8px 24px var(--shadow);
    display: flex;
    flex-direction: column;
    justify-content: center;
}}

.header h1 {{
    font-size: 1.5rem;
    font-weight: 700;
    letter-spacing: -0.02em;
}}

.header p {{
    font-size: 0.9rem;
    opacity: 0.7;
    margin-top: 4px;
}}

.sidebar, .footer {{
    align-items: center;
    font-weight: 500;
    font-size: 1.2rem;
    opacity: 0.8;
}}

/* MICRO LAYOUT: The Auto-Fit Grid */
.responsive-grid {{
    display: grid;
    /* The magic formula: Zero media-query responsiveness */
    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    /* Implicit row sizing */
    grid-auto-rows: 140px;
    /* Auto-flow dense to fill gaps caused by spanning items */
    grid-auto-flow: dense;
    gap: 16px;
}}

.card {{
    background: var(--accent);
    color: #ffffff;
    border-radius: 12px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    font-size: 2rem;
    font-weight: 700;
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    cursor: pointer;
    transition: transform 0.2s cubic-bezier(0.4, 0, 0.2, 1), box-shadow 0.2s ease;
}}

.card:hover {{
    transform: translateY(-4px) scale(1.02);
    box-shadow: 0 12px 24px rgba(0,0,0,0.25);
}}

/* Demonstrate spanning capabilities */
.card.span-col {{
    grid-column: span 2;
}}

.card.span-row {{
    grid-row: span 2;
}}

.card.span-both {{
    grid-column: span 2;
    grid-row: span 2;
    font-size: 3rem;
}}

/* Fallback macro-layout for small screens */
@media (max-width: 800px) {{
    .app-container {{
        grid-template-columns: 1fr;
        grid-template-areas:
            "header"
            "main"
            "sidebar"
            "footer";
    }}
    
    .card.span-col, .card.span-both {{
        grid-column: span 1; /* Reset span on small screens to prevent overflow */
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
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="app-container">
        
        <header class="header">
            <h1>{title_text}</h1>
            <p>{body_text}</p>
        </header>

        <main class="main">
            <!-- Micro Layout: The Auto-Fit Grid -->
            <div class="responsive-grid">
                <div class="card span-both" style="background: color-mix(in srgb, var(--accent) 80%, black);">1</div>
                <div class="card">2</div>
                <div class="card span-row">3</div>
                <div class="card">4</div>
                <div class="card span-col" style="background: color-mix(in srgb, var(--accent) 90%, white);">5</div>
                <div class="card">6</div>
                <div class="card">7</div>
            </div>
        </main>

        <aside class="sidebar">
            Sidebar Info
        </aside>

        <footer class="footer">
            Footer Area
        </footer>

    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Responsive Bento Dashboard Grid - Logic
document.addEventListener('DOMContentLoaded', () => {{
    const cards = document.querySelectorAll('.card');
    
    // Add simple interaction to demonstrate dynamic nature
    cards.forEach(card => {{
        card.addEventListener('click', () => {{
            // Toggle a span class on click to watch the dense auto-flow rearrange the grid
            if (!card.classList.contains('span-both')) {{
                card.classList.toggle('span-col');
            }}
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
