def create_component(
    output_dir: str,
    title_text: str = "Why Not Your Own Services?",
    body_text: str = "Start Your Self-Hosting Journey with us!",
    color_scheme: str = "light",       
    accent_color: str = "#ec4899",     
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Glassmorphic Theme Toggle with Ambient Glow.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Define the dynamic initial state based on color_scheme
    is_dark = color_scheme == "dark"
    dark_class = "dark-mode" if is_dark else ""
    checked_attr = "checked" if is_dark else ""

    css = f"""/* Glassmorphic Theme Toggle with Ambient Glow */
:root {{
    /* Light Theme Variables */
    --bg-base: #f3f4f6;
    --text-main: #111827;
    --text-muted: #4b5563;
    
    --glow-color: {accent_color}80; /* Accent with 50% opacity */
    
    --glass-bg: rgba(255, 255, 255, 0.6);
    --glass-border: rgba(255, 255, 255, 0.8);
    --glass-shadow: 0 10px 30px rgba(0, 0, 0, 0.05);
    
    --toggle-bg: #e5e7eb;
    --toggle-knob: #ffffff;
    
    --card-bg: rgba(255, 255, 255, 0.7);
    --card-hover: rgba(255, 255, 255, 0.9);
}}

body.dark-mode {{
    /* Dark Theme Variables */
    --bg-base: #0d1117;
    --text-main: #f9fafb;
    --text-muted: #9ca3af;
    
    --glow-color: #10b98160; /* Emerald green glow for dark mode */
    
    --glass-bg: rgba(30, 41, 59, 0.4);
    --glass-border: rgba(255, 255, 255, 0.08);
    --glass-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
    
    --toggle-bg: #374151;
    --toggle-knob: #10b981;
    
    --card-bg: rgba(30, 41, 59, 0.6);
    --card-hover: rgba(51, 65, 85, 0.8);
}}

* {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: 'Inter', system-ui, sans-serif;
    background-color: var(--bg-base);
    color: var(--text-main);
    min-height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
    overflow-x: hidden;
    /* The magic that makes the theme transition smooth */
    transition: background-color 0.5s ease, color 0.5s ease;
}}

/* Ambient Glow Orbs */
.ambient-glow {{
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: clamp(300px, 60vw, 600px);
    height: clamp(300px, 60vw, 600px);
    border-radius: 50%;
    background: var(--glow-color);
    filter: blur(120px);
    -webkit-filter: blur(120px);
    z-index: -1;
    transition: background 0.8s ease, transform 0.8s ease;
    pointer-events: none;
}}

body.dark-mode .ambient-glow {{
    transform: translate(-50%, -30%) scale(1.2);
}}

/* Main App Container */
.app-container {{
    width: 100%;
    max-width: {width_px}px;
    min-height: {height_px}px;
    background: var(--glass-bg);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border: 1px solid var(--glass-border);
    border-radius: 24px;
    box-shadow: var(--glass-shadow);
    display: flex;
    flex-direction: column;
    padding: 2rem;
    margin: 2rem;
    transition: background-color 0.5s ease, border-color 0.5s ease, box-shadow 0.5s ease;
}}

/* Mac-like Header */
.app-header {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding-bottom: 2rem;
    border-bottom: 1px solid var(--glass-border);
    transition: border-color 0.5s ease;
}}

.window-controls {{
    display: flex;
    gap: 8px;
}}

.control-dot {{
    width: 12px;
    height: 12px;
    border-radius: 50%;
}}
.dot-red {{ background-color: #ef4444; }}
.dot-yellow {{ background-color: #f59e0b; }}
.dot-green {{ background-color: #10b981; }}

.header-nav {{
    font-weight: 500;
    font-size: 14px;
    letter-spacing: 0.5px;
}}

/* Theme Toggle Switch */
.theme-toggle-wrapper {{
    display: flex;
    align-items: center;
    gap: 12px;
    font-size: 14px;
    font-weight: 500;
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
    border-radius: 34px;
    transition: 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}}

.slider:before {{
    position: absolute;
    content: "";
    height: 20px;
    width: 20px;
    left: 4px;
    bottom: 4px;
    background-color: var(--toggle-knob);
    border-radius: 50%;
    transition: 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}}

input:checked + .slider {{
    background-color: var(--toggle-bg);
}}

input:checked + .slider:before {{
    transform: translateX(22px);
}}

/* Hero Content */
.hero-section {{
    text-align: center;
    margin: 4rem 0;
}}

.hero-section h1 {{
    font-size: 3.5rem;
    font-weight: 700;
    margin-bottom: 1rem;
    letter-spacing: -1px;
}}

.hero-section p {{
    font-size: 1.25rem;
    color: var(--text-muted);
    transition: color 0.5s ease;
}}

/* Tabs / Filters */
.tab-nav {{
    display: flex;
    justify-content: center;
    gap: 3rem;
    margin-bottom: 2rem;
    font-weight: 600;
}}
.tab-nav span {{
    cursor: pointer;
    padding-bottom: 0.5rem;
    color: var(--text-muted);
    transition: color 0.3s;
}}
.tab-nav span.active {{
    color: var(--text-main);
    border-bottom: 2px solid var(--text-main);
}}

/* Card Grid */
.card-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 1.5rem;
}}

.glass-card {{
    background: var(--card-bg);
    border: 1px solid var(--glass-border);
    border-radius: 16px;
    padding: 1.5rem;
    cursor: pointer;
    transition: background 0.3s ease, transform 0.3s ease, border-color 0.5s ease;
}}

.glass-card:hover {{
    background: var(--card-hover);
    transform: translateY(-4px);
}}

.card-label {{
    font-size: 0.85rem;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: var(--text-muted);
    margin-bottom: 0.5rem;
}}

.card-title {{
    font-size: 1.25rem;
    font-weight: 600;
}}
"""

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
<body class="{dark_class}">
    <!-- The ambient blurred light behind the UI -->
    <div class="ambient-glow"></div>

    <div class="app-container">
        <header class="app-header">
            <div class="window-controls">
                <span class="control-dot dot-red"></span>
                <span class="control-dot dot-yellow"></span>
                <span class="control-dot dot-green"></span>
            </div>
            
            <div class="header-nav">
                App Components
            </div>

            <div class="theme-toggle-wrapper">
                <span>Lights</span>
                <label class="switch">
                    <input type="checkbox" id="themeToggle" {checked_attr}>
                    <span class="slider"></span>
                </label>
            </div>
        </header>

        <main>
            <div class="hero-section">
                <h1>{title_text}</h1>
                <p>{body_text}</p>
            </div>

            <div class="tab-nav">
                <span>Posts</span>
                <span>Blogs</span>
                <span class="active">Videos</span>
            </div>

            <div class="card-grid">
                <div class="glass-card">
                    <div class="card-label">Installation Guide</div>
                    <div class="card-title">Speedtest-Tracker</div>
                </div>
                <div class="glass-card">
                    <div class="card-label">Setup</div>
                    <div class="card-title">Uptime-Kuma</div>
                </div>
                <div class="glass-card">
                    <div class="card-label">Playlist</div>
                    <div class="card-title">HomeLab (Self-hosting)</div>
                </div>
            </div>
        </main>
    </div>

    <script src="script.js"></script>
</body>
</html>"""

    js = f"""// Glassmorphic Theme Toggle Logic
document.addEventListener('DOMContentLoaded', () => {{
    const themeToggle = document.getElementById('themeToggle');
    
    // Listen for toggle switch changes
    themeToggle.addEventListener('change', function() {{
        // Toggle the dark-mode class on the body
        // This single class change triggers all the CSS Variable transitions
        if (this.checked) {{
            document.body.classList.add('dark-mode');
        }} else {{
            document.body.classList.remove('dark-mode');
        }}
    }});
}});
"""

    # Write files
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
