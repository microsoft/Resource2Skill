def create_component(
    output_dir: str,
    title_text: str = "Analytics Dashboard",
    body_text: str = "A zero-media-query fluid grid built entirely with modern CSS Grid. Resize the window to watch the auto-fit behavior naturally cascade the elements.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#6366f1",     # Indigo
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Zero-Media-Query Fluid Grid Architecture.
    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme ===
    if color_scheme == "dark":
        bg_color = "#0f172a"
        surface_color = "#1e293b"
        card_bg = "rgba(255, 255, 255, 0.03)"
        card_hover = "rgba(255, 255, 255, 0.06)"
        text_color = "#f8fafc"
        text_muted = "#94a3b8"
        border_color = "rgba(255, 255, 255, 0.08)"
        shadow = "rgba(0, 0, 0, 0.4)"
    else:
        bg_color = "#f8fafc"
        surface_color = "#ffffff"
        card_bg = "#ffffff"
        card_hover = "rgba(0, 0, 0, 0.02)"
        text_color = "#0f172a"
        text_muted = "#64748b"
        border_color = "rgba(0, 0, 0, 0.08)"
        shadow = "rgba(0, 0, 0, 0.06)"

    # === CSS ===
    css = f"""/* Zero-Media-Query Fluid Grid — Generated CSS */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --surface: {surface_color};
    --card-bg: {card_bg};
    --card-hover: {card_hover};
    --text: {text_color};
    --text-muted: {text_muted};
    --accent: {accent_color};
    --border: {border_color};
    --shadow: {shadow};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    background: var(--bg);
    color: var(--text);
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 100vh;
    padding: 20px;
    overflow: hidden;
}}

.viewport {{
    width: var(--width);
    height: var(--height);
    max-width: 100vw;
    max-height: 100vh;
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 24px;
    padding: 40px;
    overflow-y: auto;
    box-shadow: 0 24px 48px var(--shadow);
    display: flex;
    flex-direction: column;
}}

/* Header Typography */
.header-wrapper {{
    margin-bottom: 40px;
}}

.title {{
    font-size: 2rem;
    font-weight: 700;
    letter-spacing: -0.03em;
    margin-bottom: 8px;
}}

.body-text {{
    font-size: 1rem;
    color: var(--text-muted);
    line-height: 1.6;
    max-width: 650px;
}}

/* ==========================================================
   MACRO LAYOUT: The Zero-Media-Query Responsive Grid Container 
   ========================================================== */
.grid-container {{
    display: grid;
    /* Automatically creates columns based on width, ensuring a minimum of 280px */
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    /* Implicit rows get a consistent minimum height */
    grid-auto-rows: minmax(180px, auto);
    gap: 24px;
}}

/* ==========================================================
   MICRO LAYOUT: Semantic Area Grid inside the Card 
   ========================================================== */
.card {{
    background: var(--card-bg);
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 24px;
    position: relative;
    overflow: hidden;
    cursor: pointer;
    transition: transform 0.3s ease, background 0.3s ease, border-color 0.3s ease, box-shadow 0.3s ease;
    
    /* Tutorial: Grid Areas */
    display: grid;
    grid-template-areas:
        "icon status"
        "title title"
        "value value";
    grid-template-columns: auto 1fr;
    grid-template-rows: auto 1fr auto;
    gap: 12px;
    
    /* Animation initial state */
    opacity: 0;
    animation: fadeUp 0.6s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}}

.card:hover {{
    transform: translateY(-6px);
    background: var(--card-hover);
    border-color: var(--accent);
    box-shadow: 0 12px 24px rgba(0,0,0,0.1);
}}

/* Tutorial: Z-Index Layering */
.card > * {{
    position: relative;
    z-index: 1; /* Keep content above the decorative glow */
}}

/* Decorative glow representing absolute positioning beneath grid content */
.card::after {{
    content: '';
    position: absolute;
    top: -40px;
    right: -40px;
    width: 120px;
    height: 120px;
    background: var(--accent);
    filter: blur(50px);
    opacity: 0.1;
    z-index: 0;
    border-radius: 50%;
    transition: opacity 0.3s ease;
    pointer-events: none;
}}

.card:hover::after {{
    opacity: 0.25;
}}

/* Mapping Elements to Grid Areas */
.card-icon {{
    grid-area: icon;
    width: 52px;
    height: 52px;
    background: var(--accent);
    color: #ffffff;
    border-radius: 14px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 700;
    font-size: 1.25rem;
    box-shadow: 0 8px 16px rgba(0,0,0,0.15);
}}

/* Tutorial: Justify-Self individual alignment */
.card-status {{
    grid-area: status;
    justify-self: end;  /* Pin to the right of the 'status' area */
    align-self: start;  /* Pin to the top of the 'status' area */
    padding: 6px 12px;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 0.5px;
}}

.card-title {{
    grid-area: title;
    align-self: end;    /* Push title to the bottom of its area cell */
    font-size: 0.85rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: var(--text-muted);
    font-weight: 600;
    margin-top: 16px;
}}

.card-value {{
    grid-area: value;
    font-size: 2.5rem;
    font-weight: 700;
    letter-spacing: -0.02em;
    color: var(--text);
}}

/* Entrance Animation */
@keyframes fadeUp {{
    from {{ opacity: 0; transform: translateY(30px); }}
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
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="viewport">
        <div class="header-wrapper">
            <h1 class="title">{title_text}</h1>
            <p class="body-text">{body_text}</p>
        </div>
        
        <div class="grid-container" id="grid">
            <!-- Grid cards will be populated seamlessly by JavaScript -->
        </div>
    </div>
    
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Component Logic
document.addEventListener('DOMContentLoaded', () => {{
    const gridContainer = document.getElementById('grid');
    
    // Dataset demonstrating practical grid consumption
    const cards = [
        {{ title: "Total Revenue", value: "$124,500", status: "+14.2%", isPositive: true }},
        {{ title: "Active Subscribers", value: "34,200", status: "+5.1%", isPositive: true }},
        {{ title: "Bounce Rate", value: "42.8%", status: "-2.4%", isPositive: false }},
        {{ title: "Server Uptime", value: "99.9%", status: "Stable", isPositive: true }},
        {{ title: "Support Tickets", value: "142", status: "+12", isPositive: false }},
        {{ title: "Avg. Session", value: "04:23", status: "+8.0%", isPositive: true }}
    ];

    cards.forEach((card, index) => {{
        const el = document.createElement('article');
        el.className = 'card';
        // Staggered entrance animation delay mapped to the grid order
        el.style.animationDelay = `${{index * 0.08}}s`;
        
        // Dynamic status coloring
        const statusColor = card.isPositive ? '#10b981' : '#ef4444';
        const statusBg = card.isPositive ? 'rgba(16, 185, 129, 0.15)' : 'rgba(239, 68, 68, 0.15)';
        
        el.innerHTML = `
            <div class="card-icon">0${{index + 1}}</div>
            <div class="card-status" style="color: ${{statusColor}}; background: ${{statusBg}}">
                ${{card.status}}
            </div>
            <div class="card-title">${{card.title}}</div>
            <div class="card-value">${{card.value}}</div>
        `;
        gridContainer.appendChild(el);
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
