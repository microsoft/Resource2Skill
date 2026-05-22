def create_component(
    output_dir: str,
    title_text: str = "Why Not Your Own Services?",
    body_text: str = "Start Your Self-Hosting Journey with us!",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#ec4899",     # Used for primary accents
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Animated Glassmorphism Theme Toggle.
    
    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Determine initial state for the HTML toggle
    is_dark = color_scheme == "dark"
    body_class = "dark-mode" if is_dark else ""
    checked_attr = "checked" if is_dark else ""

    # === CSS ===
    css = f"""/* Theme Toggle & Glassmorphism System */
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    /* Default (Light) Theme Variables */
    --bg-main: #f3f3f3;
    --text-main: #1a1a1a;
    --text-muted: #6b7280;
    --card-bg: rgba(255, 255, 255, 0.6);
    --card-border: rgba(255, 255, 255, 0.4);
    --blob-1: #ffb6ff;
    --blob-2: #a7f3d0;
    --toggle-track: #e5e7eb;
    --toggle-thumb: #ffffff;
    --accent: {accent_color};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body.dark-mode {{
    /* Dark Theme Variables */
    --bg-main: #0c1a1a;
    --text-main: #d6f9f0;
    --text-muted: #8aa8a0;
    --card-bg: rgba(255, 255, 255, 0.03);
    --card-border: rgba(255, 255, 255, 0.08);
    --blob-1: #1e3a8a;
    --blob-2: #064e3b;
    --toggle-track: rgba(255, 255, 255, 0.15);
    --toggle-thumb: #d6f9f0;
}}

body {{
    font-family: 'Poppins', sans-serif;
    background-color: var(--bg-main);
    color: var(--text-main);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
    /* Smooth transition for theme colors */
    transition: background-color 0.5s ease, color 0.5s ease;
}}

.app-container {{
    width: var(--width);
    height: var(--height);
    position: relative;
    overflow: hidden;
    display: flex;
    flex-direction: column;
    padding: 40px 60px;
    background: transparent;
    border-radius: 24px;
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.1);
    /* For standalone demo bounding box */
    border: 1px solid var(--card-border);
}}

/* Decorative Gradient Blobs */
.blob {{
    position: absolute;
    border-radius: 50%;
    filter: blur(80px);
    z-index: 0;
    transition: background-color 0.8s ease;
}}
.blob-1 {{
    top: 50%;
    left: 40%;
    width: 500px;
    height: 500px;
    background-color: var(--blob-1);
    transform: translate(-50%, -30%);
}}
.blob-2 {{
    top: -10%;
    right: 10%;
    width: 400px;
    height: 400px;
    background-color: var(--blob-2);
}}

/* Main Content Layer */
.content-layer {{
    position: relative;
    z-index: 10;
    display: flex;
    flex-direction: column;
    height: 100%;
}}

/* Header & Toggle */
header {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    width: 100%;
    margin-bottom: 60px;
}}

.logo {{
    font-size: 20px;
    font-weight: 700;
    letter-spacing: 0.5px;
}}

.controls {{
    display: flex;
    align-items: center;
    gap: 20px;
}}

.theme-switch-wrapper {{
    display: flex;
    align-items: center;
    gap: 12px;
    background: var(--card-bg);
    padding: 8px 16px;
    border-radius: 30px;
    border: 1px solid var(--card-border);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    transition: all 0.5s ease;
}}

.theme-switch-label {{
    font-size: 14px;
    font-weight: 500;
}}

/* The Toggle Switch UI */
.theme-switch {{
    position: relative;
    display: inline-block;
    width: 48px;
    height: 26px;
}}

.theme-switch input {{
    opacity: 0;
    width: 0;
    height: 0;
}}

.switch-track {{
    position: absolute;
    cursor: pointer;
    top: 0; left: 0; right: 0; bottom: 0;
    background-color: var(--toggle-track);
    transition: .4s;
    border-radius: 34px;
}}

.switch-thumb {{
    position: absolute;
    content: "";
    height: 20px;
    width: 20px;
    left: 3px;
    bottom: 3px;
    background-color: var(--toggle-thumb);
    transition: transform 0.4s cubic-bezier(0.4, 0.0, 0.2, 1), background-color 0.4s ease;
    border-radius: 50%;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}}

/* Toggle Check State */
.theme-switch input:checked + .switch-track .switch-thumb {{
    transform: translateX(22px);
}}

/* Hero Section */
.hero {{
    text-align: center;
    margin-top: 40px;
    margin-bottom: 60px;
}}

.hero h1 {{
    font-size: 48px;
    font-weight: 600;
    margin-bottom: 16px;
    transition: color 0.5s ease;
}}

.hero p {{
    font-size: 18px;
    color: var(--text-muted);
    transition: color 0.5s ease;
}}

/* Glassmorphic Feature Cards */
.cards-grid {{
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 24px;
    margin-top: auto;
}}

.card {{
    background: var(--card-bg);
    border: 1px solid var(--card-border);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    padding: 32px 24px;
    border-radius: 16px;
    transition: transform 0.3s ease, background 0.5s ease, border-color 0.5s ease;
    cursor: pointer;
}}

.card:hover {{
    transform: translateY(-5px);
}}

.card-tag {{
    font-size: 12px;
    text-transform: uppercase;
    letter-spacing: 1px;
    font-weight: 600;
    color: var(--accent);
    margin-bottom: 8px;
    display: block;
}}

.card h3 {{
    font-size: 20px;
    font-weight: 500;
}}
"""

    # === HTML ===
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text}</title>
    <link rel="stylesheet" href="style.css">
</head>
<body class="{body_class}">
    <div class="app-container">
        
        <!-- Abstract Background Layers -->
        <div class="blob blob-1"></div>
        <div class="blob blob-2"></div>

        <!-- Foreground Content -->
        <div class="content-layer">
            <header>
                <div class="logo">Echoes</div>
                
                <div class="controls">
                    <div class="theme-switch-wrapper">
                        <span class="theme-switch-label">Lights</span>
                        <label class="theme-switch">
                            <input type="checkbox" id="theme-toggle" {checked_attr}>
                            <div class="switch-track">
                                <div class="switch-thumb"></div>
                            </div>
                        </label>
                    </div>
                </div>
            </header>

            <main class="hero">
                <h1>{title_text}</h1>
                <p>{body_text}</p>
            </main>

            <div class="cards-grid">
                <div class="card">
                    <span class="card-tag">Installation Guide</span>
                    <h3>Speedtest-Tracker</h3>
                </div>
                <div class="card">
                    <span class="card-tag">Setup</span>
                    <h3>Uptime-Kuma</h3>
                </div>
                <div class="card">
                    <span class="card-tag">Playlist</span>
                    <h3>HomeLab (Self-hosting)</h3>
                </div>
            </div>
        </div>

    </div>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Theme Toggling Logic
document.addEventListener('DOMContentLoaded', () => {{
    const themeToggle = document.getElementById('theme-toggle');
    const body = document.body;

    themeToggle.addEventListener('change', (e) => {{
        if (e.target.checked) {{
            // Switch to Dark Mode
            body.classList.add('dark-mode');
        }} else {{
            // Switch to Light Mode
            body.classList.remove('dark-mode');
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
