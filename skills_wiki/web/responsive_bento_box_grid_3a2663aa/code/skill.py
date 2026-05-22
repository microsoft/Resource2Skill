def create_component(
    output_dir: str,
    title_text: str = "Bento Grid Dashboard",
    body_text: str = "A responsive, interlocking card grid using CSS Grid auto-fit and dense packing.",
    color_scheme: str = "dark",        
    accent_color: str = "#6366f1",     
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Responsive Bento Box Grid layout.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors ===
    if color_scheme == "dark":
        bg_color = "#0b0f19"
        text_color = "#f1f5f9"
        text_muted = "#94a3b8"
        surface_color = "rgba(30, 41, 59, 0.4)"
        surface_border = "rgba(255, 255, 255, 0.08)"
        glow_color = accent_color + "22" # 13% opacity hex
    else:
        bg_color = "#f8fafc"
        text_color = "#0f172a"
        text_muted = "#64748b"
        surface_color = "rgba(255, 255, 255, 0.8)"
        surface_border = "rgba(0, 0, 0, 0.08)"
        glow_color = accent_color + "22"

    # === CSS ===
    css = f"""/* Responsive Bento Box Grid */
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
    --border: {surface_border};
    --glow: {glow_color};
    --width: {width_px}px;
    --min-height: {height_px}px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background: var(--bg);
    color: var(--text);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 2rem;
}}

.page-wrapper {{
    width: 100%;
    max-width: var(--width);
    min-height: var(--min-height);
    display: flex;
    flex-direction: column;
    gap: 2rem;
}}

.header {{
    text-align: center;
}}

.header h1 {{
    font-size: 2.5rem;
    font-weight: 700;
    margin-bottom: 0.5rem;
    letter-spacing: -0.02em;
}}

.header p {{
    color: var(--text-muted);
    font-size: 1.1rem;
}}

/* Grid Container Strategy */
.bento-container {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
    grid-auto-rows: 200px;
    grid-auto-flow: dense;
    gap: 1.25rem;
    position: relative;
}}

/* Grid Items */
.bento-item {{
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 24px;
    padding: 1.5rem;
    display: flex;
    flex-direction: column;
    position: relative;
    overflow: hidden;
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    transition: transform 0.3s ease, border-color 0.3s ease;
}}

.bento-item:hover {{
    transform: translateY(-4px);
    border-color: var(--accent);
}}

/* Mouse Spotlight Effect */
.bento-item::before {{
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; bottom: 0;
    background: radial-gradient(
        600px circle at var(--mouse-x, 0) var(--mouse-y, 0), 
        var(--glow),
        transparent 40%
    );
    opacity: 0;
    transition: opacity 0.3s ease;
    pointer-events: none;
    z-index: 0;
}}

.bento-container:hover .bento-item::before {{
    opacity: 1;
}}

/* Item Content (z-index protects it from glow overlay) */
.item-content {{
    position: relative;
    z-index: 1;
    height: 100%;
    display: flex;
    flex-direction: column;
}}

/* Explicit Spans for Layout Variety */
.item-hero {{
    grid-column: span 2;
    grid-row: span 2;
    background: linear-gradient(135deg, var(--surface) 0%, rgba(0,0,0,0) 100%);
}}

.item-wide {{
    grid-column: span 2;
}}

.item-tall {{
    grid-row: span 2;
}}

/* Responsive Override: Prevent grid break on small screens */
@media (max-width: 650px) {{
    .item-hero, .item-wide {{
        grid-column: span 1;
    }}
    .item-hero, .item-tall {{
        grid-row: span 1;
    }}
    .bento-container {{
        grid-auto-rows: auto;
        min-height: 200px;
    }}
}}

/* Internal Styling */
.icon {{
    font-size: 1.25rem;
    color: var(--accent);
    background: var(--glow);
    width: 44px;
    height: 44px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 12px;
    margin-bottom: 1rem;
}}

.item-content h2 {{ font-size: 1.5rem; font-weight: 600; margin-bottom: 0.5rem; }}
.item-content h3 {{ font-size: 1.1rem; font-weight: 500; color: var(--text-muted); margin-bottom: 0.5rem; }}
.item-content p {{ font-size: 0.95rem; color: var(--text-muted); line-height: 1.5; }}
.item-content .stat {{ font-size: 2.5rem; font-weight: 700; color: var(--text); margin-top: auto; line-height: 1; }}

/* Aesthetics */
.chart-mockup {{
    margin-top: auto;
    height: 120px;
    display: flex;
    align-items: flex-end;
    gap: 8px;
    padding-top: 1rem;
}}

.chart-mockup .bar {{
    flex: 1;
    background: var(--accent);
    border-radius: 4px 4px 0 0;
    opacity: 0.8;
    transition: height 1s ease-out;
}}

.activity-list {{
    list-style: none;
    margin-top: auto;
    display: flex;
    flex-direction: column;
    gap: 12px;
}}

.activity-list li {{
    font-size: 0.9rem;
    display: flex;
    align-items: center;
    gap: 12px;
    color: var(--text-muted);
}}

.activity-list span {{
    display: block;
    width: 8px;
    height: 8px;
    background: var(--accent);
    border-radius: 50%;
    box-shadow: 0 0 8px var(--accent);
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
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="page-wrapper">
        <header class="header">
            <h1>{title_text}</h1>
            <p>{body_text}</p>
        </header>
        
        <main class="bento-container">
            <!-- Hero Item (2x2) -->
            <div class="bento-item item-hero">
                <div class="item-content">
                    <i class="fa-solid fa-chart-line icon"></i>
                    <h2>Main Analytics</h2>
                    <p>Comprehensive overview of all your primary metrics, compiled in real-time across your active deployments.</p>
                    <div class="chart-mockup">
                        <div class="bar" style="height: 40%"></div>
                        <div class="bar" style="height: 70%"></div>
                        <div class="bar" style="height: 50%"></div>
                        <div class="bar" style="height: 90%"></div>
                        <div class="bar" style="height: 30%"></div>
                        <div class="bar" style="height: 80%"></div>
                    </div>
                </div>
            </div>
            
            <!-- Standard Item (1x1) -->
            <div class="bento-item">
                <div class="item-content">
                    <i class="fa-solid fa-users icon"></i>
                    <h3>Total Users</h3>
                    <p class="stat">24.5K</p>
                </div>
            </div>
            
            <!-- Standard Item (1x1) -->
            <div class="bento-item">
                <div class="item-content">
                    <i class="fa-solid fa-arrow-trend-up icon"></i>
                    <h3>Conversion</h3>
                    <p class="stat">4.2%</p>
                </div>
            </div>
            
            <!-- Tall Item (1x2) -->
            <div class="bento-item item-tall">
                <div class="item-content">
                    <i class="fa-solid fa-bolt icon"></i>
                    <h3>Live Activity</h3>
                    <ul class="activity-list">
                        <li><span></span> User 'Alex' signed up</li>
                        <li><span></span> Database backed up</li>
                        <li><span></span> Payment processed</li>
                        <li><span></span> System updated</li>
                        <li><span></span> Cache cleared</li>
                    </ul>
                </div>
            </div>
            
            <!-- Wide Item (2x1) -->
            <div class="bento-item item-wide">
                <div class="item-content">
                    <i class="fa-solid fa-shield-halved icon"></i>
                    <h3>Security Status</h3>
                    <p>All core systems operating normally. No recent vulnerability breaches or anomalies detected in the last 30 days.</p>
                </div>
            </div>
            
            <!-- Standard Item (1x1) -->
            <div class="bento-item">
                <div class="item-content">
                    <i class="fa-solid fa-cloud icon"></i>
                    <h3>Storage Used</h3>
                    <p class="stat">78%</p>
                </div>
            </div>
            
            <!-- Standard Item (1x1) -->
            <div class="bento-item">
                <div class="item-content">
                    <i class="fa-solid fa-gear icon"></i>
                    <h3>System Settings</h3>
                    <p>Configure routing and application preferences.</p>
                </div>
            </div>
            
        </main>
    </div>
    
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Mouse Spotlight Tracking Logic
document.addEventListener('DOMContentLoaded', () => {{
    const container = document.querySelector('.bento-container');
    const cards = document.querySelectorAll('.bento-item');
    
    // Track mouse position on container and update CSS variables on cards
    container.addEventListener('mousemove', (e) => {{
        for (const card of cards) {{
            const rect = card.getBoundingClientRect();
            // Calculate coordinates relative to each card
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            
            card.style.setProperty('--mouse-x', `${{x}}px`);
            card.style.setProperty('--mouse-y', `${{y}}px`);
        }}
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
