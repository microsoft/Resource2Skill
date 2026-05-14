def create_component(
    output_dir: str,
    title_text: str = "Why Not Your Own Services?",
    body_text: str = "Start Your Self-Hosting Journey with us!",
    color_scheme: str = "light",       # "dark" or "light"
    accent_color: str = "#ec4899",     # Pink accent mapped from video
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Glassmorphism Hero with Theming visual effect.
    
    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Determine initial checked state for the toggle based on color_scheme
    is_dark = color_scheme == "dark"
    checked_attr = "checked" if is_dark else ""
    initial_theme = "dark" if is_dark else "light"

    # === CSS ===
    css = f"""/* Glassmorphism Hero Component */
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

:root {{
    /* Light Theme Variables */
    --bg-color: #f8f9fa;
    --text-main: #1e293b;
    --text-muted: #64748b;
    --glass-bg: rgba(255, 255, 255, 0.65);
    --glass-border: rgba(255, 255, 255, 0.4);
    --card-bg: rgba(255, 255, 255, 0.8);
    --card-hover: rgba(255, 255, 255, 1);
    
    /* Orb Colors */
    --orb-1: #ffb800; /* Yellow */
    --orb-2: {accent_color}; /* Pink/Accent */
    --orb-3: #00d2ff; /* Cyan */
    
    --accent: {accent_color};
}}

[data-theme="dark"] {{
    /* Dark Theme Variables */
    --bg-color: #0f172a;
    --text-main: #f8fafc;
    --text-muted: #94a3b8;
    --glass-bg: rgba(15, 23, 42, 0.65);
    --glass-border: rgba(255, 255, 255, 0.08);
    --card-bg: rgba(30, 41, 59, 0.7);
    --card-hover: rgba(51, 65, 85, 0.9);
}}

*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: 'Poppins', sans-serif;
    background-color: var(--bg-color);
    color: var(--text-main);
    transition: background-color 0.4s ease, color 0.4s ease;
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
    overflow-x: hidden;
}}

.app-wrapper {{
    width: 100%;
    max-width: {width_px}px;
    height: {height_px}px;
    position: relative;
    overflow: hidden;
    border-radius: 24px;
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
    background-color: var(--bg-color);
}}

/* Abstract Background Orbs */
.orbs {{
    position: absolute;
    top: 0; left: 0; width: 100%; height: 100%;
    overflow: hidden;
    z-index: 0;
    pointer-events: none;
}}

.orb {{
    position: absolute;
    border-radius: 50%;
    filter: blur(80px);
    opacity: 0.7;
    animation: float 12s infinite ease-in-out alternate;
}}

.orb-1 {{
    width: 400px; height: 400px;
    background: var(--orb-1);
    top: -100px; left: -100px;
    animation-delay: 0s;
}}

.orb-2 {{
    width: 500px; height: 500px;
    background: var(--orb-2);
    bottom: -150px; right: -100px;
    animation-delay: -4s;
}}

.orb-3 {{
    width: 350px; height: 350px;
    background: var(--orb-3);
    top: 40%; left: 30%;
    animation-delay: -8s;
}}

@keyframes float {{
    0% {{ transform: translate(0, 0) scale(1); }}
    100% {{ transform: translate(40px, -40px) scale(1.1); }}
}}

/* Glassmorphism Surface */
.glass-surface {{
    position: relative;
    z-index: 10;
    width: 100%;
    height: 100%;
    background: var(--glass-bg);
    backdrop-filter: blur(120px);
    -webkit-backdrop-filter: blur(120px);
    border: 1px solid var(--glass-border);
    display: flex;
    flex-direction: column;
    padding: 2rem;
    transition: background 0.4s ease, border-color 0.4s ease;
}}

/* Header / Nav */
.header {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1rem 2rem;
    width: 100%;
}}

.logo-group {{
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-weight: 600;
    font-size: 1.1rem;
}}

.logo-dots {{
    display: flex;
    gap: 4px;
}}

.dot {{
    width: 10px; height: 10px;
    border-radius: 50%;
}}
.dot.red {{ background-color: #ef4444; }}
.dot.yellow {{ background-color: #eab308; }}
.dot.green {{ background-color: #22c55e; }}

.nav-links {{
    display: flex;
    gap: 2rem;
    align-items: center;
}}

.nav-item {{
    text-decoration: none;
    color: var(--text-main);
    font-weight: 500;
    font-size: 0.95rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
    transition: color 0.2s;
}}

.nav-item:hover {{
    color: var(--accent);
}}

/* Hero Content */
.hero-main {{
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    gap: 1rem;
}}

.hero-title {{
    font-size: 3.5rem;
    font-weight: 700;
    letter-spacing: -1px;
}}

.hero-subtitle {{
    font-size: 1.25rem;
    color: var(--text-muted);
    font-weight: 400;
    margin-bottom: 3rem;
}}

/* Feature Cards Grid */
.grid-container {{
    display: flex;
    flex-direction: column;
    gap: 1rem;
    width: 100%;
    max-width: 900px;
}}

.tabs-row {{
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 1rem;
}}

.cards-row {{
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1rem;
}}

.card {{
    background: var(--card-bg);
    border: 1px solid var(--glass-border);
    padding: 1.5rem;
    border-radius: 16px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    transition: all 0.3s ease;
    cursor: pointer;
}}

.card:hover {{
    background: var(--card-hover);
    transform: translateY(-2px);
    box-shadow: 0 10px 20px -10px rgba(0,0,0,0.1);
}}

.card-label {{
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: uppercase;
    color: var(--text-muted);
    margin-bottom: 0.25rem;
}}

.card-title {{
    font-size: 1.1rem;
    font-weight: 600;
}}

/* Toggle Switch */
.toggle-wrapper {{
    display: flex;
    align-items: center;
    justify-content: space-between;
}}

.toggle-switch {{
    position: relative;
    display: inline-block;
    width: 56px;
    height: 28px;
}}

.toggle-switch input {{
    opacity: 0;
    width: 0;
    height: 0;
}}

.slider {{
    position: absolute;
    cursor: pointer;
    top: 0; left: 0; right: 0; bottom: 0;
    background-color: rgba(0,0,0,0.1);
    border: 1px solid var(--glass-border);
    transition: .4s;
    border-radius: 34px;
}}

[data-theme="dark"] .slider {{
    background-color: rgba(255,255,255,0.1);
}}

.slider:before {{
    position: absolute;
    content: "";
    height: 20px;
    width: 20px;
    left: 4px;
    bottom: 3px;
    background-color: var(--text-main);
    transition: .4s;
    border-radius: 50%;
}}

input:checked + .slider {{
    background-color: var(--accent);
}}

input:checked + .slider:before {{
    transform: translateX(28px);
    background-color: white;
}}
"""

    # === HTML ===
    html = f"""<!DOCTYPE html>
<html lang="en" data-theme="{initial_theme}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text}</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="app-wrapper">
        <!-- Abstract Animated Background -->
        <div class="orbs">
            <div class="orb orb-1"></div>
            <div class="orb orb-2"></div>
            <div class="orb orb-3"></div>
        </div>

        <!-- Glassmorphism Foreground -->
        <div class="glass-surface">
            
            <header class="header">
                <div class="logo-group">
                    <div class="logo-dots">
                        <div class="dot red"></div>
                        <div class="dot yellow"></div>
                        <div class="dot green"></div>
                    </div>
                    <span>echoesofping.dev</span>
                </div>
                <div class="nav-links">
                    <a href="#" class="nav-item"><i class="fa-brands fa-youtube"></i> YouTube</a>
                    <a href="#" class="nav-item"><i class="fa-regular fa-user"></i> Join now</a>
                </div>
            </header>

            <main class="hero-main">
                <h1 class="hero-title">{title_text}</h1>
                <p class="hero-subtitle">{body_text}</p>

                <div class="grid-container">
                    <div class="tabs-row">
                        <div class="card">
                            <span class="card-title" style="text-align:center;">Posts</span>
                        </div>
                        <div class="card">
                            <span class="card-title" style="text-align:center;">Blogs</span>
                        </div>
                        <div class="card" style="border-bottom: 3px solid var(--accent);">
                            <span class="card-title" style="text-align:center; color: var(--accent);">Videos</span>
                        </div>
                        <div class="card toggle-wrapper">
                            <span class="card-title">Lights</span>
                            <label class="toggle-switch">
                                <input type="checkbox" id="theme-toggle" {checked_attr} aria-label="Toggle Dark Mode">
                                <span class="slider"></span>
                            </label>
                        </div>
                    </div>

                    <div class="cards-row">
                        <div class="card">
                            <span class="card-label">Installation Guide</span>
                            <span class="card-title">Speedtest-Tracker</span>
                        </div>
                        <div class="card">
                            <span class="card-label">Setup</span>
                            <span class="card-title">Uptime-Kuma</span>
                        </div>
                        <div class="card">
                            <span class="card-label">Playlist</span>
                            <span class="card-title">HomeLab (Self-hosting)</span>
                        </div>
                    </div>
                </div>
            </main>
        </div>
    </div>
    
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = """// Glassmorphism Hero - Theme Toggle Logic
document.addEventListener('DOMContentLoaded', () => {
    const toggle = document.getElementById('theme-toggle');
    const root = document.documentElement;

    toggle.addEventListener('change', (e) => {
        if (e.target.checked) {
            root.setAttribute('data-theme', 'dark');
        } else {
            root.setAttribute('data-theme', 'light');
        }
    });
});
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
