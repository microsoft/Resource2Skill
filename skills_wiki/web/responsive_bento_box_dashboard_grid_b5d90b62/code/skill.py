def create_component(
    output_dir: str,
    title_text: str = "Dashboard Overview",
    body_text: str = "Welcome back. Here is your daily summary.",
    color_scheme: str = "light",
    accent_color: str = "#f97316", # Default orange accent matching video vibe
    width_px: int = 1000,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Responsive Bento-Box Dashboard Grid.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Derive theme colors based on scheme
    if color_scheme == "dark":
        bg_color = "#09090b"
        surface_color = "#18181b"
        text_color = "#fafafa"
        muted_text = "#a1a1aa"
        border_color = "#27272a"
        shadow = "0 8px 16px rgba(0, 0, 0, 0.4)"
        hover_shadow = "0 12px 24px rgba(0, 0, 0, 0.6)"
    else:
        bg_color = "#f4f4f5"
        surface_color = "#ffffff"
        text_color = "#09090b"
        muted_text = "#71717a"
        border_color = "#e4e4e7"
        shadow = "0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -2px rgba(0, 0, 0, 0.05)"
        hover_shadow = "0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -4px rgba(0, 0, 0, 0.1)"

    css = f"""/* Responsive Bento-Box Dashboard Grid */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --surface: {surface_color};
    --text: {text_color};
    --muted: {muted_text};
    --border: {border_color};
    --accent: {accent_color};
    --shadow: {shadow};
    --hover-shadow: {hover_shadow};
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
    padding: 1rem;
}}

/* The isolated component wrapper */
.app-container {{
    width: 100%;
    max-width: var(--width);
    height: var(--height);
    background: var(--bg);
    border: 1px solid var(--border);
    border-radius: 12px;
    display: flex;
    flex-direction: column;
    overflow: hidden;
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
    /* Establish Container Query context */
    container-type: inline-size;
    container-name: dashboard;
}}

.dashboard-header {{
    padding: 1.5rem 2rem;
    background: var(--surface);
    border-bottom: 1px solid var(--border);
    display: flex;
    flex-direction: column;
    gap: 0.25rem;
}}

.dashboard-header h1 {{
    font-size: 1.25rem;
    font-weight: 600;
}}

.dashboard-header p {{
    font-size: 0.875rem;
    color: var(--muted);
}}

/* === CORE GRID LAYOUT === */
.dashboard-main {{
    flex: 1;
    overflow-y: auto;
    padding: 1.5rem 2rem;
    
    /* Base Mobile Layout: Single Column */
    display: grid;
    gap: 1.25rem;
    grid-template-columns: 1fr;
    grid-auto-rows: min-content;
}}

/* Card Styling */
.card {{
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 1.25rem;
    min-block-size: 8rem;
    display: flex;
    flex-direction: column;
    box-shadow: var(--shadow);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}}

.card:hover {{
    transform: translateY(-2px);
    box-shadow: var(--hover-shadow);
}}

.card h2 {{
    font-size: 0.875rem;
    font-weight: 500;
    color: var(--muted);
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-bottom: 0.5rem;
}}

.card .value {{
    margin-top: auto;
    font-size: 1.75rem;
    font-weight: 700;
    color: var(--text);
}}

/* Hero Card Styling */
.card-1 {{
    background: var(--accent);
    color: #ffffff;
    position: relative;
    overflow: hidden;
    border: none;
    min-block-size: 10rem;
    justify-content: center;
}}

.card-1::before {{
    content: "";
    position: absolute;
    inset: 0;
    background: linear-gradient(135deg, rgba(255,255,255,0.3) 0%, rgba(0,0,0,0.1) 100%);
    mix-blend-mode: overlay;
    pointer-events: none;
}}

.card-1 h2 {{
    color: rgba(255, 255, 255, 0.9);
    font-size: 1.5rem;
    font-weight: 600;
    text-transform: none;
    letter-spacing: normal;
    margin: 0;
}}


/* === MEDIUM BREAKPOINT (using Container Queries) === */
@container dashboard (min-width: 600px) {{
    .dashboard-main {{
        grid-template-columns: repeat(4, 1fr);
    }}
    
    .card-1 {{
        grid-column: span 4;
    }}
    
    /* All other cards span 2 columns */
    .card {{
        grid-column: span 2;
    }}
}}


/* === LARGE BREAKPOINT (Complex Bento Box) === */
@container dashboard (min-width: 900px) {{
    .card-2, .card-3 {{
        grid-area: auto; /* Resets to 1 column width */
    }}
    
    /* Explicit placement: row-start / col-start / row-end / col-end */
    .card-4 {{
        grid-area: 3 / 1 / 4 / 2;
    }}
    
    .card-5 {{
        grid-area: 3 / 2 / 4 / 3;
    }}
    
    /* Span vertically across 2 rows, automatically flow into next available columns */
    .card-6, .card-7 {{
        grid-area: span 2 / auto; 
    }}
    
    /* Cards 8 and 9 implicitly inherit `span 2` columns from the medium media query, creating a wide row */
    
    /* Reset bottom cards to strictly 1 column width */
    .card-10, .card-11, .card-12, .card-13 {{
        grid-column: auto; 
    }}
}}

/* Custom scrollbar for inner view */
.dashboard-main::-webkit-scrollbar {{
    width: 8px;
}}
.dashboard-main::-webkit-scrollbar-track {{
    background: transparent;
}}
.dashboard-main::-webkit-scrollbar-thumb {{
    background-color: var(--border);
    border-radius: 4px;
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
    <div class="app-container">
        <header class="dashboard-header">
            <h1>{title_text}</h1>
            <p>{body_text}</p>
        </header>
        
        <main class="dashboard-main">
            <!-- Row 1 spans 4 columns -->
            <div class="card card-1">
                <h2>Welcome John Doe!</h2>
            </div>
            
            <!-- Dynamic flow area -->
            <div class="card card-2"><h2>Orders</h2><div class="value">1,204</div></div>
            <div class="card card-3"><h2>Shipped</h2><div class="value">983</div></div>
            <div class="card card-4"><h2>Pending</h2><div class="value">221</div></div>
            <div class="card card-5"><h2>Revenue</h2><div class="value">$45K</div></div>
            
            <!-- Taller vertical spanning cards -->
            <div class="card card-6"><h2>Users</h2><div class="value">12.5K</div></div>
            <div class="card card-7"><h2>Subscriptions</h2><div class="value">3,190</div></div>
            
            <!-- Wide horizontal spanning cards -->
            <div class="card card-8"><h2>Analytics Traffic</h2><div class="value">84,912</div></div>
            <div class="card card-9"><h2>Active Inbox</h2><div class="value">14</div></div>
            
            <!-- Standard 1x1 base cards -->
            <div class="card card-10"><h2>Calendar</h2><div class="value">3 events</div></div>
            <div class="card card-11"><h2>User Activity</h2><div class="value">+11%</div></div>
            <div class="card card-12"><h2>Sales Dyn.</h2><div class="value">Level 2</div></div>
            <div class="card card-13"><h2>Tasks</h2><div class="value">8 open</div></div>
        </main>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    js = """// No JavaScript required for this component.
// The complex reflowing logic is handled entirely by native CSS Grid and Container Queries.
document.addEventListener('DOMContentLoaded', () => {
    console.log('Dashboard layout initialized successfully.');
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
