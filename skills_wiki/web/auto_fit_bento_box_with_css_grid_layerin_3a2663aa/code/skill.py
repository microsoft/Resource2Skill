def create_component(
    output_dir: str,
    title_text: str = "Overview",
    body_text: str = "Real-time metrics flowing dynamically without media queries.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#8b5cf6",     # Primary accent (e.g., purple)
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Auto-Fit Bento Box Grid.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Theme logic mapping
    if color_scheme == "dark":
        bg_color = "#09090b"
        text_color = "#f8fafc"
        text_muted = "#94a3b8"
        surface_color = "rgba(255, 255, 255, 0.03)"
        border_color = "rgba(255, 255, 255, 0.08)"
        blend_mode = "screen"
    else:
        bg_color = "#f8fafc"
        text_color = "#0f172a"
        text_muted = "#64748b"
        surface_color = "#ffffff"
        border_color = "rgba(0, 0, 0, 0.08)"
        blend_mode = "multiply"

    # === CSS ===
    css = f"""/* Auto-Fit Bento Grid — generated component */
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
    --border: {border_color};
    --blend: {blend_mode};
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
    padding: 24px;
}}

.container {{
    width: 100%;
    max-width: var(--width);
    height: var(--height);
    display: grid;
    grid-template-rows: max-content 1fr; /* Header stays top, Grid takes remainder */
    gap: 32px;
    overflow-y: auto;
    padding: 8px; /* Room for card hover shadows */
}}

/* Typography */
.header {{
    display: grid;
    gap: 8px;
}}

.title {{
    font-size: 2.5rem;
    font-weight: 700;
    letter-spacing: -0.02em;
}}

.body-text {{
    font-size: 1.1rem;
    color: var(--text-muted);
}}

/* === The Climax Technique: Media-Queryless Responsive Grid === */
.dashboard-grid {{
    display: grid;
    /* Create as many 260px columns as fit, stretch remaining space */
    grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
    /* Implicit rows height */
    grid-auto-rows: 180px;
    gap: 24px;
    /* Prevent rows from stretching to fill vertical space if few items exist */
    align-content: start; 
}}

/* === The Layering Technique: Z-Axis stacking in Grid === */
.card {{
    display: grid;
    /* Create an explicit 1x1 grid to safely use negative line numbers */
    grid-template-columns: 1fr;
    grid-template-rows: 1fr;
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 16px;
    overflow: hidden;
    cursor: pointer;
    transition: transform 0.2s cubic-bezier(0.4, 0, 0.2, 1), box-shadow 0.2s ease;
    
    /* Entrance animation setup */
    opacity: 0;
    animation: slideUp 0.6s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}}

.card:hover, .card:focus-visible {{
    transform: translateY(-4px);
    box-shadow: 0 12px 24px rgba(0, 0, 0, 0.15);
    outline: none;
}}

.card:focus-visible {{
    border-color: var(--accent);
}}

/* Force all direct children into the exact same 1x1 grid cell */
.card > * {{
    grid-area: 1 / 1 / -1 / -1; 
}}

/* Layer 0: Decorative Background */
.card-bg {{
    z-index: 0;
    background: radial-gradient(circle at 100% 0%, var(--card-accent, var(--accent)), transparent 70%);
    opacity: 0.15;
    mix-blend-mode: var(--blend);
}}

/* Layer 1: Actual Content */
.card-content {{
    z-index: 1;
    display: grid;
    /* Internal grid to space header, value, and footer */
    grid-template-rows: max-content 1fr max-content;
    padding: 24px;
    gap: 12px;
}}

/* Layer 2: Badge positioned via Grid Alignment */
.card-badge {{
    z-index: 2;
    /* Pushes to top-right corner of the grid cell */
    justify-self: end;
    align-self: start;
    margin: 16px;
    padding: 6px 12px;
    background: var(--card-accent, var(--accent));
    color: #fff;
    font-size: 0.75rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    border-radius: 99px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}}

.card-header {{
    font-size: 0.9rem;
    color: var(--text-muted);
    font-weight: 500;
}}

.card-value {{
    font-size: 2.2rem;
    font-weight: 700;
    color: var(--text);
    /* Vertically center the value in its flex/grid space */
    align-self: center; 
}}

.card-footer {{
    font-size: 0.85rem;
    color: var(--text-muted);
}}

@keyframes slideUp {{
    from {{ opacity: 0; transform: translateY(20px); }}
    to {{ opacity: 1; transform: translateY(0); }}
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
    <div class="container">
        <header class="header">
            <h1 class="title">{title_text}</h1>
            <p class="body-text">{body_text}</p>
        </header>
        
        <main class="dashboard-grid">
            <article class="card" tabindex="0">
                <div class="card-bg" style="--card-accent: #3b82f6;" aria-hidden="true"></div>
                <div class="card-content">
                    <h2 class="card-header">Total Revenue</h2>
                    <div class="card-value">$45,231</div>
                    <div class="card-footer">+20.1% from last month</div>
                </div>
            </article>

            <article class="card" tabindex="0">
                <div class="card-bg" style="--card-accent: #10b981;" aria-hidden="true"></div>
                <div class="card-badge">Live</div>
                <div class="card-content">
                    <h2 class="card-header">Active Users</h2>
                    <div class="card-value">2,314</div>
                    <div class="card-footer">+180 since last hour</div>
                </div>
            </article>

            <article class="card" tabindex="0">
                <div class="card-bg" style="--card-accent: var(--accent);" aria-hidden="true"></div>
                <div class="card-content">
                    <h2 class="card-header">Conversion Rate</h2>
                    <div class="card-value">4.3%</div>
                    <div class="card-footer">Consistent performance</div>
                </div>
            </article>

            <article class="card" tabindex="0">
                <div class="card-bg" style="--card-accent: #f59e0b;" aria-hidden="true"></div>
                <div class="card-badge">Warning</div>
                <div class="card-content">
                    <h2 class="card-header">Server Load</h2>
                    <div class="card-value">87%</div>
                    <div class="card-footer">High traffic detected</div>
                </div>
            </article>
            
            <article class="card" tabindex="0">
                <div class="card-bg" style="--card-accent: #ec4899;" aria-hidden="true"></div>
                <div class="card-content">
                    <h2 class="card-header">Customer Satisfaction</h2>
                    <div class="card-value">4.9/5</div>
                    <div class="card-footer">Based on 1,204 reviews</div>
                </div>
            </article>
        </main>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Auto-Fit Bento Grid — Staggered Entrance
document.addEventListener('DOMContentLoaded', () => {{
    const cards = document.querySelectorAll('.card');
    
    // Assign a staggered CSS animation delay based on DOM order
    cards.forEach((card, index) => {{
        // Base delay of 0.1s + 0.08s per card
        card.style.animationDelay = `${{0.1 + (index * 0.08)}}s`;
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
