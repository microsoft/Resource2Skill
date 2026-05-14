def create_component(
    output_dir: str,
    title_text: str = "Feature Dashboard",
    body_text: str = "Everything you need to manage your workflow, all in one place.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#6366f1",     # CSS hex color for accent (e.g., Indigo)
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Responsive Bento Grid visual effect.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme and accent_color ===
    if color_scheme == "dark":
        bg_color = "#09090b"
        text_primary = "#fafafa"
        text_secondary = "#a1a1aa"
        card_bg = "rgba(255, 255, 255, 0.03)"
        card_border = "rgba(255, 255, 255, 0.08)"
        card_hover_border = "rgba(255, 255, 255, 0.2)"
        shadow = "0 10px 30px -10px rgba(0, 0, 0, 0.5)"
    else:
        bg_color = "#f4f4f5"
        text_primary = "#09090b"
        text_secondary = "#52525b"
        card_bg = "#ffffff"
        card_border = "rgba(0, 0, 0, 0.08)"
        card_hover_border = "rgba(0, 0, 0, 0.15)"
        shadow = "0 10px 30px -10px rgba(0, 0, 0, 0.05)"

    # === CSS ===
    css = f"""/* Responsive Bento Grid Dashboard — generated component */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --text-primary: {text_primary};
    --text-secondary: {text_secondary};
    --accent: {accent_color};
    --card-bg: {card_bg};
    --card-border: {card_border};
    --card-hover-border: {card_hover_border};
    --shadow: {shadow};
    --max-width: {width_px}px;
    --min-height: {height_px}px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background: var(--bg);
    color: var(--text-primary);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 2rem;
    overflow-x: hidden;
}}

.dashboard-container {{
    width: 100%;
    max-width: var(--max-width);
    min-height: var(--min-height);
    display: flex;
    flex-direction: column;
    gap: 2rem;
}}

.header {{
    text-align: center;
    margin-bottom: 1rem;
}}

.title {{
    font-size: 2.5rem;
    font-weight: 700;
    letter-spacing: -0.025em;
    margin-bottom: 0.75rem;
}}

.subtitle {{
    font-size: 1.125rem;
    color: var(--text-secondary);
    max-width: 600px;
    margin: 0 auto;
}}

/* Bento Grid System */
.bento-grid {{
    display: grid;
    /* Core wrapping logic */
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    grid-auto-rows: 240px;
    grid-auto-flow: dense;
    gap: 1.5rem;
    position: relative;
}}

/* The Card */
.bento-card {{
    background: var(--card-bg);
    border: 1px solid var(--card-border);
    border-radius: 1.5rem;
    padding: 2rem;
    display: flex;
    flex-direction: column;
    position: relative;
    overflow: hidden;
    box-shadow: var(--shadow);
    transition: transform 0.4s cubic-bezier(0.25, 1, 0.5, 1), 
                border-color 0.4s ease;
    cursor: default;
}}

.bento-card:hover {{
    transform: translateY(-4px) scale(1.005);
    border-color: var(--card-hover-border);
}}

/* Interactive Glow Effect using JS injected variables */
.bento-card::before {{
    content: '';
    position: absolute;
    top: 0; left: 0; width: 100%; height: 100%;
    background: radial-gradient(
        800px circle at var(--mouse-x, 50%) var(--mouse-y, 50%), 
        var(--card-hover-border),
        transparent 40%
    );
    opacity: 0;
    transition: opacity 0.5s;
    z-index: 0;
    pointer-events: none;
}}

.bento-grid:hover .bento-card::before {{
    opacity: 1;
}}

/* Card Content Layering */
.card-content {{
    position: relative;
    z-index: 1;
    display: flex;
    flex-direction: column;
    height: 100%;
}}

.card-icon {{
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 48px;
    height: 48px;
    border-radius: 12px;
    background: rgba(128, 128, 128, 0.1);
    color: var(--accent);
    margin-bottom: auto;
    font-size: 1.5rem;
}}

.card-title {{
    font-size: 1.25rem;
    font-weight: 600;
    margin-bottom: 0.5rem;
    margin-top: 1rem;
}}

.card-desc {{
    font-size: 0.95rem;
    color: var(--text-secondary);
    line-height: 1.5;
}}

/* Special Styling for the Accent Card */
.bento-card.accent {{
    background: var(--accent);
    color: #ffffff;
    border: none;
}}
.bento-card.accent .card-desc {{ color: rgba(255, 255, 255, 0.9); }}
.bento-card.accent .card-icon {{ background: rgba(0, 0, 0, 0.2); color: #fff; }}

/* Spanning Utility Classes for Desktop */
@media (min-width: 768px) {{
    .span-col-2 {{ grid-column: span 2; }}
    .span-col-3 {{ grid-column: span 3; }}
    .span-row-2 {{ grid-row: span 2; }}
}}

/* Ensure grid behaves gracefully on very small screens */
@media (max-width: 600px) {{
    .bento-grid {{
        grid-auto-rows: minmax(200px, auto);
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
    <!-- Phosphor Icons for lightweight UI icons -->
    <script src="https://unpkg.com/@phosphor-icons/web"></script>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="dashboard-container">
        <header class="header">
            <h1 class="title">{title_text}</h1>
            <p class="subtitle">{body_text}</p>
        </header>

        <main class="bento-grid" id="bento-grid">
            
            <!-- Large Hero Card -->
            <div class="bento-card span-col-2 span-row-2">
                <div class="card-content">
                    <div class="card-icon"><i class="ph ph-chart-line-up"></i></div>
                    <h2 class="card-title">Real-time Analytics</h2>
                    <p class="card-desc">Monitor your data continuously with sub-second latency. Understand your user flows, identify bottlenecks, and optimize conversion rates natively within your ecosystem.</p>
                </div>
            </div>

            <!-- Standard Card -->
            <div class="bento-card accent">
                <div class="card-content">
                    <div class="card-icon"><i class="ph ph-lightning"></i></div>
                    <h2 class="card-title">Lightning Fast</h2>
                    <p class="card-desc">Edge-optimized delivery ensures your data loads instantly globally.</p>
                </div>
            </div>

            <!-- Tall Card -->
            <div class="bento-card span-row-2">
                <div class="card-content">
                    <div class="card-icon"><i class="ph ph-shield-check"></i></div>
                    <h2 class="card-title">Bank-grade Security</h2>
                    <p class="card-desc">End-to-end encryption with zero-trust architecture. Your data is your own. We utilize AES-256 encryption at rest and TLS 1.3 in transit.</p>
                </div>
            </div>

            <!-- Standard Card -->
            <div class="bento-card">
                <div class="card-content">
                    <div class="card-icon"><i class="ph ph-users-three"></i></div>
                    <h2 class="card-title">Team Collab</h2>
                    <p class="card-desc">Invite unlimited team members with granular permission controls.</p>
                </div>
            </div>

            <!-- Wide Card -->
            <div class="bento-card span-col-2">
                <div class="card-content">
                    <div class="card-icon"><i class="ph ph-plug"></i></div>
                    <h2 class="card-title">Seamless Integrations</h2>
                    <p class="card-desc">Connect with your favorite tools in one click. Slack, Jira, GitHub, and 100+ more apps are supported out of the box.</p>
                </div>
            </div>

        </main>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Responsive Bento Grid Dashboard — Interactive Behavior
document.addEventListener('DOMContentLoaded', () => {{
    const grid = document.getElementById('bento-grid');
    const cards = document.querySelectorAll('.bento-card');

    // Mouse tracking for premium "Spotlight" hover effect
    grid.addEventListener('mousemove', (e) => {{
        for (const card of cards) {{
            const rect = card.getBoundingClientRect();
            // Calculate mouse position relative to each card
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;

            // Set CSS variables for the radial-gradient position
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
