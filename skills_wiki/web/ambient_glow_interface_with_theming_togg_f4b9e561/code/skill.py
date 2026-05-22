def create_component(
    output_dir: str,
    title_text: str = "Why not Your own Services?",
    body_text: str = "Start Your Self-Hosting Journey with us!",
    color_scheme: str = "light",       # "dark" or "light" (Initial state)
    accent_color: str = "#0ea5e9",     # Used for the toggle and dark mode glow
    width_px: int = 1000,
    height_px: int = 700,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Ambient Glow Interface with Theming Toggle.
    
    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)
    
    # Determine initial theme attribute
    theme_attr = 'data-theme="dark"' if color_scheme == "dark" else ""
    is_checked = "checked" if color_scheme == "dark" else ""

    # === CSS ===
    css = f"""/* Ambient Glow Interface — Generated Component */
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600&display=swap');

:root {{
    --bg-color: #f8fafc;
    --text-primary: #0f172a;
    --text-secondary: #475569;
    --surface-bg: rgba(255, 255, 255, 0.7);
    --surface-border: rgba(0, 0, 0, 0.05);
    --glow-bg: linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%);
    --accent: {accent_color};
    --toggle-bg: #cbd5e1;
    --toggle-knob: #ffffff;
}}

[data-theme="dark"] {{
    --bg-color: #0b1120;
    --text-primary: #f8fafc;
    --text-secondary: #94a3b8;
    --surface-bg: rgba(30, 41, 59, 0.6);
    --surface-border: rgba(255, 255, 255, 0.05);
    --glow-bg: linear-gradient(135deg, #0284c7 0%, var(--accent) 100%);
    --toggle-bg: #334155;
    --toggle-knob: #ffffff;
}}

*, *::before, *::after {{
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}}

body {{
    font-family: 'Poppins', sans-serif;
    background-color: var(--bg-color);
    color: var(--text-primary);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: background-color 0.4s ease, color 0.4s ease;
    overflow: hidden;
}}

/* Main App Container */
.app-wrapper {{
    width: {width_px}px;
    height: {height_px}px;
    max-width: 95vw;
    max-height: 95vh;
    position: relative;
    border-radius: 24px;
    overflow: hidden;
    display: flex;
    flex-direction: column;
}}

/* The Ambient Orb */
.ambient-orb {{
    position: absolute;
    top: 40%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: 60%;
    height: 60%;
    background: var(--glow-bg);
    filter: blur(120px);
    border-radius: 50%;
    z-index: 0;
    opacity: 0.7;
    transition: background 0.6s ease;
    pointer-events: none;
}}

/* Foreground Content */
.content-layer {{
    position: relative;
    z-index: 1;
    width: 100%;
    height: 100%;
    display: flex;
    flex-direction: column;
}}

/* Top Navigation / Browser Bar */
.top-bar {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 20px 32px;
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
.dot.close {{ background-color: #ef4444; }}
.dot.min {{ background-color: #f59e0b; }}
.dot.max {{ background-color: #10b981; }}

.nav-actions {{
    display: flex;
    align-items: center;
    gap: 24px;
    font-weight: 500;
    font-size: 0.9rem;
}}

.join-btn {{
    background: transparent;
    border: none;
    color: var(--text-primary);
    font-family: inherit;
    font-weight: 600;
    cursor: pointer;
    transition: color 0.3s;
}}
.join-btn:hover {{
    color: var(--accent);
}}

/* Hero Section */
.hero {{
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    padding: 0 20px;
}}

.hero h1 {{
    font-size: clamp(2rem, 4vw, 3.5rem);
    font-weight: 600;
    margin-bottom: 16px;
    letter-spacing: -0.02em;
}}

.hero p {{
    font-size: 1.1rem;
    color: var(--text-secondary);
    font-weight: 400;
}}

/* Feature Navigation & Toggle */
.feature-nav {{
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 40px;
    padding: 20px 0;
    border-bottom: 1px solid var(--surface-border);
    margin-bottom: 40px;
    width: 80%;
    margin-left: auto;
    margin-right: auto;
}}

.nav-link {{
    text-decoration: none;
    color: var(--text-secondary);
    font-weight: 500;
    transition: color 0.2s;
}}
.nav-link:hover, .nav-link.active {{
    color: var(--text-primary);
}}

/* Toggle Switch Styles */
.theme-switch-wrapper {{
    display: flex;
    align-items: center;
    gap: 12px;
}}

.theme-switch-wrapper span {{
    font-weight: 500;
    color: var(--text-secondary);
}}

.switch {{
    position: relative;
    display: inline-block;
    width: 50px;
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
    background-color: var(--toggle-bg);
    transition: .4s;
    border-radius: 34px;
}}

.slider:before {{
    position: absolute;
    content: "";
    height: 20px;
    width: 20px;
    left: 4px;
    bottom: 4px;
    background-color: var(--toggle-knob);
    transition: .4s cubic-bezier(0.4, 0, 0.2, 1);
    border-radius: 50%;
    box-shadow: 0 2px 4px rgba(0,0,0,0.2);
}}

input:checked + .slider {{
    background-color: var(--accent);
}}

input:checked + .slider:before {{
    transform: translateX(22px);
}}

/* Cards Section */
.cards-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 24px;
    padding: 0 40px 40px;
}}

.card {{
    background: var(--surface-bg);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    border: 1px solid var(--surface-border);
    border-radius: 16px;
    padding: 24px;
    transition: transform 0.3s ease, box-shadow 0.3s ease, background 0.4s ease, border-color 0.4s ease;
}}

.card:hover {{
    transform: translateY(-4px);
    box-shadow: 0 10px 25px rgba(0,0,0,0.05);
}}

.card-subtitle {{
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: var(--text-secondary);
    margin-bottom: 8px;
    font-weight: 600;
}}

.card-title {{
    font-size: 1.25rem;
    font-weight: 600;
    color: var(--text-primary);
}}
"""

    # === HTML ===
    html = f"""<!DOCTYPE html>
<html lang="en" {theme_attr}>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text}</title>
    <link rel="stylesheet" href="style.css">
    <!-- Icons for extra flair -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
</head>
<body>

    <div class="app-wrapper">
        <!-- The Background Glow -->
        <div class="ambient-orb"></div>

        <!-- The Foreground Content -->
        <div class="content-layer">
            
            <!-- Header -->
            <header class="top-bar">
                <div class="window-controls">
                    <div class="dot close"></div>
                    <div class="dot min"></div>
                    <div class="dot max"></div>
                </div>
                <div class="nav-actions">
                    <button class="join-btn">Join now</button>
                    <i class="fa-regular fa-user"></i>
                </div>
            </header>

            <!-- Hero Text -->
            <main class="hero">
                <h1>{title_text}</h1>
                <p>{body_text}</p>
            </main>

            <!-- Navigation & Theme Toggle -->
            <nav class="feature-nav">
                <a href="#" class="nav-link">Posts</a>
                <a href="#" class="nav-link">Blogs</a>
                <a href="#" class="nav-link active">Videos</a>
                
                <div class="theme-switch-wrapper">
                    <span>Lights</span>
                    <label class="switch">
                        <input type="checkbox" id="themeToggle" {is_checked}>
                        <span class="slider"></span>
                    </label>
                </div>
            </nav>

            <!-- Cards Grid -->
            <div class="cards-grid">
                <div class="card">
                    <div class="card-subtitle">Installation Guide</div>
                    <div class="card-title">Speedtest-Tracker</div>
                </div>
                <div class="card">
                    <div class="card-subtitle">Setup</div>
                    <div class="card-title">Uptime-Kuma</div>
                </div>
                <div class="card">
                    <div class="card-subtitle">Playlist</div>
                    <div class="card-title">HomeLab (Self-hosting)</div>
                </div>
            </div>

        </div>
    </div>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = """// Ambient Glow Interface — Theme Toggling Logic
document.addEventListener('DOMContentLoaded', () => {
    const themeToggle = document.getElementById('themeToggle');
    const htmlElement = document.documentElement;

    // Listen for toggle changes
    themeToggle.addEventListener('change', function() {
        if (this.checked) {
            // Switch to Dark Mode
            htmlElement.setAttribute('data-theme', 'dark');
        } else {
            // Switch to Light Mode
            htmlElement.removeAttribute('data-theme');
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
