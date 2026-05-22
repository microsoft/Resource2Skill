def create_component(
    output_dir: str,
    title_text: str = "Why not Your own Services?",
    body_text: str = "Start Your Self-hosting Journey with us!",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#00bfff",     # CSS hex color for accent
    width_px: int = 1000,
    height_px: int = 600,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Ambient Glassmorphism Interface with Theming.
    
    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Determine initial checkbox state based on theme parameter
    is_dark = color_scheme.lower() == "dark"
    checkbox_checked = "checked" if is_dark else ""

    # === CSS ===
    css = f"""/* Ambient Glassmorphism Interface */
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

/* Light Theme Variables (Default) */
:root {{
    --bg-color: #f8fafc;
    --text-main: #0f172a;
    --text-muted: #64748b;
    --glow-1: #fbc2eb;
    --glow-2: #a6c1ee;
    
    --panel-bg: rgba(255, 255, 255, 0.6);
    --panel-border: rgba(255, 255, 255, 0.4);
    --panel-shadow: rgba(0, 0, 0, 0.05);
    
    --card-bg: rgba(255, 255, 255, 0.5);
    --card-hover: rgba(255, 255, 255, 0.9);
    
    --accent: {accent_color};
    --width: {width_px}px;
    --height: {height_px}px;
}}

/* Dark Theme Variables */
[data-theme="dark"] {{
    --bg-color: #0f172a;
    --text-main: #f8fafc;
    --text-muted: #94a3b8;
    --glow-1: #00bfff;
    --glow-2: #00ffa3;
    
    --panel-bg: rgba(15, 23, 42, 0.65);
    --panel-border: rgba(255, 255, 255, 0.08);
    --panel-shadow: rgba(0, 0, 0, 0.3);
    
    --card-bg: rgba(30, 41, 59, 0.5);
    --card-hover: rgba(30, 41, 59, 0.9);
}}

body {{
    font-family: 'Poppins', sans-serif;
    background-color: var(--bg-color);
    color: var(--text-main);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
    transition: background-color 0.5s ease, color 0.5s ease;
}}

/* Ambient Glow Layer */
.ambient-glow {{
    position: absolute;
    width: 600px;
    height: 600px;
    border-radius: 50%;
    background: linear-gradient(135deg, var(--glow-1), var(--glow-2));
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    filter: blur(100px);
    z-index: 0;
    transition: background 0.6s ease;
}}

/* Main Glass Window */
.glass-window {{
    position: relative;
    z-index: 1;
    width: var(--width);
    max-width: 95vw;
    height: var(--height);
    background: var(--panel-bg);
    backdrop-filter: blur(24px);
    -webkit-backdrop-filter: blur(24px);
    border: 1px solid var(--panel-border);
    border-radius: 24px;
    box-shadow: 0 25px 50px -12px var(--panel-shadow);
    display: flex;
    flex-direction: column;
    overflow: hidden;
    transition: background 0.5s ease, border-color 0.5s ease, box-shadow 0.5s ease;
}}

/* macOS Style Header */
.window-header {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 20px 24px;
}}

.window-controls {{
    display: flex;
    gap: 8px;
}}

.dot {{
    width: 12px;
    height: 12px;
    border-radius: 50%;
}}
.dot.red {{ background: #ff5f56; }}
.dot.yellow {{ background: #ffbd2e; }}
.dot.green {{ background: #27c93f; }}

.header-actions {{
    display: flex;
    gap: 16px;
    align-items: center;
}}

.btn {{
    background: transparent;
    border: 1px solid var(--panel-border);
    color: var(--text-main);
    padding: 8px 16px;
    border-radius: 20px;
    font-family: inherit;
    font-size: 0.9rem;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.3s ease;
    display: flex;
    align-items: center;
    gap: 8px;
}}

.btn:hover {{
    background: var(--card-hover);
}}

/* Hero Content */
.hero-content {{
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    padding: 0 20px;
}}

.hero-content h1 {{
    font-size: 2.8rem;
    font-weight: 600;
    margin-bottom: 12px;
    letter-spacing: -0.5px;
}}

.hero-content p {{
    font-size: 1.1rem;
    color: var(--text-muted);
    font-weight: 400;
    transition: color 0.5s ease;
}}

/* Footer Grid */
.window-footer {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 24px;
    border-top: 1px solid var(--panel-border);
    transition: border-color 0.5s ease;
}}

.nav-cards {{
    display: flex;
    gap: 16px;
    flex: 1;
}}

.card {{
    background: var(--card-bg);
    padding: 12px 20px;
    border-radius: 12px;
    cursor: pointer;
    transition: all 0.3s ease;
    border: 1px solid transparent;
}}

.card:hover {{
    background: var(--card-hover);
    transform: translateY(-2px);
    border-color: var(--panel-border);
}}

.card-label {{
    font-size: 0.75rem;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 1px;
    font-weight: 600;
    margin-bottom: 4px;
}}

.card-title {{
    font-size: 0.95rem;
    font-weight: 500;
}}

/* Toggle Switch */
.toggle-wrapper {{
    display: flex;
    align-items: center;
    gap: 12px;
    margin-left: 24px;
}}

.toggle-label {{
    font-size: 0.9rem;
    font-weight: 500;
}}

.switch {{
    position: relative;
    display: inline-block;
    width: 52px;
    height: 28px;
}}

.switch input {{
    opacity: 0;
    width: 0;
    height: 0;
}}

.slider {{
    position: absolute;
    cursor: pointer;
    top: 0; left: 0; right: 0; bottom: 0;
    background-color: rgba(0, 0, 0, 0.15);
    transition: 0.4s;
    border-radius: 30px;
    border: 1px solid var(--panel-border);
}}

[data-theme="dark"] .slider {{
    background-color: rgba(255, 255, 255, 0.1);
}}

.slider:before {{
    position: absolute;
    content: "";
    height: 20px;
    width: 20px;
    left: 3px;
    bottom: 3px;
    background-color: #fff;
    transition: 0.4s cubic-bezier(0.4, 0.0, 0.2, 1);
    border-radius: 50%;
    box-shadow: 0 2px 4px rgba(0,0,0,0.2);
}}

input:checked + .slider {{
    background-color: var(--accent);
    border-color: var(--accent);
}}

input:checked + .slider:before {{
    transform: translateX(24px);
}}
"""

    # === HTML ===
    html = f"""<!DOCTYPE html>
<html lang="en" data-theme="{color_scheme.lower()}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text}</title>
    <!-- FontAwesome CDN for Icons -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link rel="stylesheet" href="style.css">
</head>
<body>

    <!-- Blurred background light source -->
    <div class="ambient-glow"></div>

    <!-- Main Glass UI -->
    <div class="glass-window">
        
        <!-- Header -->
        <div class="window-header">
            <div class="window-controls">
                <span class="dot red"></span>
                <span class="dot yellow"></span>
                <span class="dot green"></span>
            </div>
            <div class="header-actions">
                <button class="btn"><i class="fa-brands fa-youtube" style="color: #ff0000;"></i> YouTube</button>
                <button class="btn">Join now <i class="fa-solid fa-angle-down"></i></button>
            </div>
        </div>

        <!-- Center Content -->
        <div class="hero-content">
            <h1>{title_text}</h1>
            <p>{body_text}</p>
        </div>

        <!-- Footer Elements -->
        <div class="window-footer">
            <div class="nav-cards">
                <div class="card">
                    <div class="card-label">Installation Guide</div>
                    <div class="card-title">Speedtest-Tracker</div>
                </div>
                <div class="card">
                    <div class="card-label">Setup</div>
                    <div class="card-title">Uptime-Kuma</div>
                </div>
                <div class="card">
                    <div class="card-label">Playlist</div>
                    <div class="card-title">HomeLab (Self-hosting)</div>
                </div>
            </div>
            
            <div class="toggle-wrapper">
                <span class="toggle-label">Lights</span>
                <label class="switch">
                    <input type="checkbox" id="themeToggle" {checkbox_checked}>
                    <span class="slider"></span>
                </label>
            </div>
        </div>

    </div>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Dynamic Theming Logic
document.addEventListener('DOMContentLoaded', () => {{
    const themeToggle = document.getElementById('themeToggle');
    const rootElement = document.documentElement;

    // Listen for toggle changes
    themeToggle.addEventListener('change', (e) => {{
        if (e.target.checked) {{
            // Switch to Dark Mode
            rootElement.setAttribute('data-theme', 'dark');
        }} else {{
            // Switch to Light Mode
            rootElement.setAttribute('data-theme', 'light');
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
