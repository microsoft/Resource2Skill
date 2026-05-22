def create_component(
    output_dir: str,
    title_text: str = "Streamline Your Workflow",
    body_text: str = "Powerful features packaged in a modular, responsive grid system.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#3b82f6",     # CSS hex color for accent
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Auto-Wrapping Responsive Bento Grid.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os
    import json

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors ===
    if color_scheme == "dark":
        bg_color = "#0f172a"
        text_color = "#f8fafc"
        text_muted = "rgba(248, 250, 252, 0.7)"
        surface_color = "#1e293b"
        border_color = "rgba(255, 255, 255, 0.08)"
        shadow = "0 10px 25px rgba(0, 0, 0, 0.3)"
        hover_shadow = "0 15px 35px rgba(0, 0, 0, 0.4)"
    else:
        bg_color = "#f8fafc"
        text_color = "#0f172a"
        text_muted = "rgba(15, 23, 42, 0.7)"
        surface_color = "#ffffff"
        border_color = "rgba(0, 0, 0, 0.05)"
        shadow = "0 4px 6px rgba(0, 0, 0, 0.05), 0 10px 15px rgba(0, 0, 0, 0.02)"
        hover_shadow = "0 10px 25px rgba(0, 0, 0, 0.08), 0 20px 25px rgba(0, 0, 0, 0.04)"

    # Content data for the grid
    cards = [
        {"icon": "fa-bolt", "title": "Lightning Fast", "desc": "Built for speed and optimized for performance across all devices."},
        {"icon": "fa-shield-halved", "title": "Bank-Grade Security", "desc": "Your data is encrypted at rest and in transit with standard protocols."},
        {"icon": "fa-chart-pie", "title": "Advanced Analytics", "desc": "Gain deep insights into your workflow with our comprehensive dashboards."},
        {"icon": "fa-layer-group", "title": "Seamless Integration", "desc": "Connect effortlessly with your favorite tools and existing infrastructure."},
        {"icon": "fa-arrows-rotate", "title": "Auto Sync", "desc": "Changes are instantly synced across your entire team's workspace."},
        {"icon": "fa-fingerprint", "title": "Biometric Auth", "desc": "Secure your account with cutting-edge device-native biometric logins."}
    ]

    # === HTML ===
    cards_html = ""
    for i, card in enumerate(cards):
        cards_html += f"""
        <article class="bento-card hidden" style="--anim-order: {i};">
            <div class="card-icon"><i class="fa-solid {card['icon']}"></i></div>
            <h3 class="card-title">{card['title']}</h3>
            <p class="card-desc">{card['desc']}</p>
        </article>
        """

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text}</title>
    <!-- Google Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <!-- FontAwesome for Icons -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <!-- Component CSS -->
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="viewport-wrapper">
        <div class="container">
            <header class="header">
                <h1 class="title">{title_text}</h1>
                <p class="body-text">{body_text}</p>
            </header>
            
            <!-- THE MAGIC GRID -->
            <section class="bento-grid">
                {cards_html}
            </section>
        </div>
    </div>
    
    <script src="script.js"></script>
</body>
</html>"""

    # === CSS ===
    css = f"""/* Auto-Wrapping Responsive Bento Grid */

:root {{
    --bg: {bg_color};
    --text: {text_color};
    --text-muted: {text_muted};
    --surface: {surface_color};
    --border: {border_color};
    --accent: {accent_color};
    --shadow: {shadow};
    --hover-shadow: {hover_shadow};
    
    --max-width: {width_px}px;
    --min-height: {height_px}px;
}}

*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background: var(--bg);
    color: var(--text);
    line-height: 1.5;
}}

/* Wrapper to simulate the requested height while allowing scroll if needed */
.viewport-wrapper {{
    min-height: var(--min-height);
    width: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 4rem 2rem;
}}

.container {{
    width: 100%;
    max-width: var(--max-width);
    display: flex;
    flex-direction: column;
    gap: 3rem;
}}

/* Header Styling */
.header {{
    text-align: center;
    max-width: 600px;
    margin: 0 auto;
}}

.title {{
    font-size: clamp(2rem, 4vw, 3rem);
    font-weight: 700;
    letter-spacing: -0.02em;
    margin-bottom: 1rem;
}}

.body-text {{
    font-size: 1.125rem;
    color: var(--text-muted);
}}

/* --- THE CSS GRID MAGIC --- */
.bento-grid {{
    display: grid;
    /* This single line eliminates media queries! 
       It fits as many 280px columns as possible, and stretches them (1fr) to fill space */
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 1.5rem;
    width: 100%;
}}

/* Card Styling */
.bento-card {{
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 1rem; /* 16px */
    padding: 2rem;
    display: flex;
    flex-direction: column;
    gap: 1rem;
    box-shadow: var(--shadow);
    transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1), box-shadow 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    
    /* Animation Base State */
    opacity: 0;
    transform: translateY(30px);
}}

.bento-card:hover {{
    transform: translateY(-6px);
    box-shadow: var(--hover-shadow);
    border-color: var(--accent);
}}

.card-icon {{
    display: flex;
    align-items: center;
    justify-content: center;
    width: 48px;
    height: 48px;
    background: rgba(59, 130, 246, 0.1);
    color: var(--accent);
    border-radius: 12px;
    font-size: 1.25rem;
    margin-bottom: 0.5rem;
}}

.card-title {{
    font-size: 1.25rem;
    font-weight: 600;
    letter-spacing: -0.01em;
}}

.card-desc {{
    font-size: 0.95rem;
    color: var(--text-muted);
    flex-grow: 1;
}}

/* CSS Animation Classes */
@keyframes cascadeIn {{
    to {{
        opacity: 1;
        transform: translateY(0);
    }}
}}

.bento-card.animate-in {{
    /* Using CSS variable injected from HTML to stagger the animation */
    animation: cascadeIn 0.6s cubic-bezier(0.2, 0.8, 0.2, 1) forwards;
    animation-delay: calc(var(--anim-order) * 0.1s);
}}
"""

    # === JavaScript ===
    js = f"""// Staggered reveal animation on load
document.addEventListener('DOMContentLoaded', () => {{
    const cards = document.querySelectorAll('.bento-card');
    
    // Add a tiny timeout to ensure CSS is ready and transition feels intentional
    setTimeout(() => {{
        cards.forEach(card => {{
            card.classList.add('animate-in');
            card.classList.remove('hidden');
        }});
    }}, 100);
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
