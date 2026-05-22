def create_component(
    output_dir: str,
    title_text: str = "Why not Your own Services?",
    body_text: str = "Start Your Self-hosting Journey with us!",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#00ffaa",     # Base accent color (used heavily in dark mode orb)
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Glassmorphism Theme Toggle effect.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os
    os.makedirs(output_dir, exist_ok=True)

    # === CSS ===
    css = f"""/* Glassmorphism Dynamic Theme Component */
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600&display=swap');

*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --width: {width_px}px;
    --height: {height_px}px;
    --accent: {accent_color};
}}

/* Light Theme Variables */
:root[data-theme="light"] {{
    --bg-main: #f8fafc;
    --text-main: #0f172a;
    --text-muted: #64748b;
    --surface-bg: rgba(255, 255, 255, 0.6);
    --surface-border: rgba(255, 255, 255, 0.8);
    --surface-shadow: 0 8px 32px rgba(0, 0, 0, 0.04);
    --tab-active-border: #fa39ad;
}}

/* Dark Theme Variables */
:root[data-theme="dark"] {{
    --bg-main: #0b1121;
    --text-main: #f8fafc;
    --text-muted: #94a3b8;
    --surface-bg: rgba(17, 24, 39, 0.65);
    --surface-border: rgba(255, 255, 255, 0.08);
    --surface-shadow: 0 8px 32px rgba(0, 0, 0, 0.25);
    --tab-active-border: var(--accent);
}}

body {{
    background: #000; /* Outer canvas */
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
    font-family: 'Poppins', sans-serif;
}}

.app-wrapper {{
    width: var(--width);
    height: var(--height);
    background: var(--bg-main);
    position: relative;
    overflow: hidden;
    border-radius: 24px;
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
    transition: background-color 0.5s ease;
}}

/* Ambient Glowing Orb */
.orb-container {{
    position: absolute;
    top: 0; left: 0; right: 0; bottom: 0;
    overflow: hidden;
    z-index: 0;
    pointer-events: none;
}}

.orb {{
    position: absolute;
    top: 40%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: 550px;
    height: 550px;
    filter: blur(120px);
}}

.orb::before, .orb::after {{
    content: '';
    position: absolute;
    inset: 0;
    border-radius: 50%;
    transition: opacity 0.8s ease;
}}

/* Cross-fading pseudo-elements for smooth gradient transition */
.orb::before {{
    background: linear-gradient(135deg, #fa39ad, #fac64c); /* Light mode glow */
    opacity: 1;
}}

.orb::after {{
    background: linear-gradient(135deg, var(--accent), #0066ff); /* Dark mode glow */
    opacity: 0;
}}

[data-theme="dark"] .orb::before {{ opacity: 0; }}
[data-theme="dark"] .orb::after {{ opacity: 1; }}

/* Foreground Content */
.content {{
    position: relative;
    z-index: 10;
    height: 100%;
    display: flex;
    flex-direction: column;
    padding: 32px 48px;
}}

.header {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding-bottom: 40px;
}}

.logo {{
    font-weight: 600;
    color: var(--text-main);
    font-size: 1.1rem;
}}

.nav-links a {{
    color: var(--text-main);
    text-decoration: none;
    font-size: 0.95rem;
    font-weight: 500;
    margin-left: 24px;
}}

.hero {{
    text-align: center;
    margin-top: 20px;
    margin-bottom: 60px;
}}

.hero h1 {{
    color: var(--text-main);
    font-size: 3rem;
    font-weight: 600;
    margin-bottom: 12px;
}}

.hero p {{
    color: var(--text-muted);
    font-size: 1.1rem;
}}

.controls-bar {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 32px;
    padding: 0 16px;
}}

.tabs {{
    display: flex;
    gap: 32px;
}}

.tab {{
    color: var(--text-muted);
    font-size: 1rem;
    font-weight: 500;
    cursor: pointer;
    padding-bottom: 8px;
    border-bottom: 2px solid transparent;
    transition: color 0.3s;
}}

.tab:hover {{
    color: var(--text-main);
}}

.tab.active {{
    color: var(--text-main);
    border-bottom-color: var(--tab-active-border);
}}

/* Toggle Switch */
.toggle-wrapper {{
    display: flex;
    align-items: center;
    gap: 16px;
    cursor: pointer;
    user-select: none;
}}

.toggle-label {{
    color: var(--text-main);
    font-weight: 500;
}}

.glass-panel {{
    background: var(--surface-bg);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border: 1px solid var(--surface-border);
    box-shadow: var(--surface-shadow);
}}

.switch {{
    position: relative;
    width: 52px;
    height: 28px;
    border-radius: 14px;
    padding: 3px;
    display: flex;
    align-items: center;
    transition: background 0.3s, border-color 0.3s;
}}

.switch-thumb {{
    width: 20px;
    height: 20px;
    background: var(--text-main);
    border-radius: 50%;
    transition: transform 0.3s cubic-bezier(0.4, 0.0, 0.2, 1), background 0.3s;
    transform: translateX(0);
}}

[data-theme="dark"] .switch-thumb {{
    transform: translateX(24px);
}}

/* Cards Grid */
.cards-grid {{
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 24px;
}}

.card {{
    border-radius: 16px;
    padding: 24px;
    cursor: pointer;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}}

.card:hover {{
    transform: translateY(-4px);
    box-shadow: 0 12px 40px rgba(0, 0, 0, 0.15);
}}

.card-label {{
    display: block;
    font-size: 0.75rem;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 0.05em;
    font-weight: 600;
    margin-bottom: 8px;
}}

.card-title {{
    font-size: 1.25rem;
    color: var(--text-main);
    font-weight: 600;
}}
"""

    # === HTML ===
    html = f"""<!DOCTYPE html>
<html lang="en" data-theme="{color_scheme}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Theme Toggle UI</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>

    <div class="app-wrapper">
        <div class="orb-container">
            <div class="orb"></div>
        </div>

        <div class="content">
            <header class="header">
                <div class="logo">✦ echoesofping</div>
                <div class="nav-links">
                    <a href="#">YouTube</a>
                    <a href="#">Join now</a>
                </div>
            </header>

            <main class="hero">
                <h1>{title_text}</h1>
                <p>{body_text}</p>
            </main>

            <div class="controls-bar">
                <div class="tabs">
                    <div class="tab">Posts</div>
                    <div class="tab">Blogs</div>
                    <div class="tab active">Videos</div>
                </div>

                <div class="toggle-wrapper" id="themeToggle">
                    <span class="toggle-label">Lights</span>
                    <div class="switch glass-panel">
                        <div class="switch-thumb"></div>
                    </div>
                </div>
            </div>

            <div class="cards-grid">
                <div class="card glass-panel">
                    <span class="card-label">Installation Guide</span>
                    <h3 class="card-title">Speedtest-Tracker</h3>
                </div>
                <div class="card glass-panel">
                    <span class="card-label">Setup</span>
                    <h3 class="card-title">Uptime-Kuma</h3>
                </div>
                <div class="card glass-panel">
                    <span class="card-label">Playlist</span>
                    <h3 class="card-title">HomeLab (Self-hosting)</h3>
                </div>
            </div>
        </div>
    </div>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Theme Toggle Interaction
document.addEventListener('DOMContentLoaded', () => {{
    const toggleBtn = document.getElementById('themeToggle');
    const root = document.documentElement;

    toggleBtn.addEventListener('click', () => {{
        // Read current theme state from HTML attribute
        const currentTheme = root.getAttribute('data-theme');
        
        // Determine new theme
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
        
        // Update DOM, triggering CSS transitions automatically
        root.setAttribute('data-theme', newTheme);
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
