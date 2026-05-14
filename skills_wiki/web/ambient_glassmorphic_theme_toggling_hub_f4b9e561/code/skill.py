def create_component(
    output_dir: str,
    title_text: str = "Why not Your own Services?",
    body_text: str = "Start Your Self-hosting Journey with us!",
    color_scheme: str = "light",        # "dark" or "light" initial state
    accent_color: str = "#d946ef",      # Accent color for glows/buttons
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Ambient Glassmorphic Theme-Toggling Hub.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)
    
    # Determine initial checked state for the toggle
    is_dark = color_scheme == "dark"
    checked_attr = 'checked' if is_dark else ''
    body_class = 'dark' if is_dark else ''

    # === CSS ===
    css = f"""/* Ambient Glassmorphic Theme-Toggling Hub */
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

/* Light Mode Variables (Default) */
:root {{
    --bg-main: #fafafa;
    --text-primary: #111827;
    --text-muted: #6b7280;
    --card-bg: #ffffff;
    --card-border: #e5e7eb;
    --card-hover-border: #d1d5db;
    --glow-color-1: rgba(217, 70, 239, 0.4); /* Pinkish accent */
    --glow-color-2: rgba(99, 102, 241, 0.4); /* Indigo accent */
    --toggle-bg: #e5e7eb;
    --toggle-thumb: #ffffff;
}}

/* Dark Mode Variables */
body.dark {{
    --bg-main: #0d1117;
    --text-primary: #f9fafb;
    --text-muted: #9ca3af;
    --card-bg: #161b22;
    --card-border: #30363d;
    --card-hover-border: #8b949e;
    --glow-color-1: rgba(0, 191, 255, 0.3); /* Cyan accent */
    --glow-color-2: rgba(138, 43, 226, 0.3); /* Purple accent */
    --toggle-bg: #30363d;
    --toggle-thumb: #8b949e;
}}

body {{
    font-family: 'Poppins', sans-serif;
    background-color: var(--bg-main);
    color: var(--text-primary);
    min-height: 100vh;
    display: flex;
    justify-content: center;
    position: relative;
    overflow-x: hidden;
    transition: background-color 0.4s ease, color 0.4s ease;
}}

/* Ambient Background Glows */
.ambient-glow {{
    position: absolute;
    border-radius: 50%;
    filter: blur(150px);
    z-index: -1;
    transition: background-color 0.8s ease;
    opacity: 0.7;
}}

.glow-1 {{
    top: 10%;
    left: 20%;
    width: 400px;
    height: 400px;
    background-color: var(--glow-color-1);
}}

.glow-2 {{
    bottom: 10%;
    right: 20%;
    width: 500px;
    height: 500px;
    background-color: var(--glow-color-2);
}}

/* Main Layout */
.app-container {{
    width: 100%;
    max-width: {width_px}px;
    padding: 40px 24px;
    display: flex;
    flex-direction: column;
}}

/* Top Navigation / Controls */
.top-nav {{
    display: flex;
    justify-content: flex-end;
    align-items: center;
    margin-bottom: 60px;
}}

.toggle-wrapper {{
    display: flex;
    align-items: center;
    gap: 12px;
    font-weight: 500;
    font-size: 0.9rem;
    color: var(--text-primary);
}}

/* Toggle Switch Styling */
.theme-switch {{
    position: relative;
    display: inline-block;
    width: 50px;
    height: 26px;
}}

.theme-switch input {{
    opacity: 0;
    width: 0;
    height: 0;
}}

.slider {{
    position: absolute;
    cursor: pointer;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: var(--toggle-bg);
    transition: .4s;
    border-radius: 34px;
}}

.slider:before {{
    position: absolute;
    content: "";
    height: 18px;
    width: 18px;
    left: 4px;
    bottom: 4px;
    background-color: var(--toggle-thumb);
    transition: .4s;
    border-radius: 50%;
}}

input:checked + .slider {{
    background-color: var(--toggle-bg);
}}

input:checked + .slider:before {{
    transform: translateX(24px);
}}

/* Hero Section */
.hero {{
    text-align: center;
    margin-bottom: 60px;
}}

.hero h1 {{
    font-size: 3rem;
    font-weight: 600;
    margin-bottom: 16px;
    letter-spacing: -0.5px;
}}

.hero p {{
    font-size: 1.1rem;
    color: var(--text-muted);
}}

/* Tab Menu */
.tab-menu {{
    display: flex;
    justify-content: center;
    gap: 40px;
    margin-bottom: 40px;
}}

.tab-link {{
    background: none;
    border: none;
    font-family: inherit;
    font-size: 1rem;
    font-weight: 500;
    color: var(--text-muted);
    cursor: pointer;
    position: relative;
    padding-bottom: 8px;
    transition: color 0.3s;
}}

.tab-link.active {{
    color: var(--text-primary);
}}

.tab-link.active::after {{
    content: '';
    position: absolute;
    bottom: 0;
    left: 0;
    width: 100%;
    height: 2px;
    background-color: var(--text-primary);
    border-radius: 2px;
}}

/* Cards Grid */
.service-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
    gap: 24px;
}}

.service-card {{
    background-color: var(--card-bg);
    border: 1px solid var(--card-border);
    border-radius: 16px;
    padding: 24px;
    display: flex;
    flex-direction: column;
    transition: transform 0.3s ease, border-color 0.3s ease, box-shadow 0.3s ease, background-color 0.4s ease;
    cursor: pointer;
    text-decoration: none;
}}

.service-card:hover {{
    transform: translateY(-4px);
    border-color: var(--card-hover-border);
    box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.05);
}}

body.dark .service-card:hover {{
    box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3);
}}

.card-category {{
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: uppercase;
    color: var(--text-muted);
    margin-bottom: 8px;
    letter-spacing: 0.5px;
}}

.card-title {{
    font-size: 1.25rem;
    font-weight: 600;
    color: var(--text-primary);
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
    <!-- Ambient Background Glows -->
    <div class="ambient-glow glow-1"></div>
    <div class="ambient-glow glow-2"></div>

    <div class="app-container">
        
        <!-- Navigation & Toggle -->
        <nav class="top-nav">
            <div class="toggle-wrapper">
                <span>Lights</span>
                <label class="theme-switch">
                    <input type="checkbox" id="themeToggle" {checked_attr}>
                    <span class="slider"></span>
                </label>
            </div>
        </nav>

        <!-- Hero Section -->
        <header class="hero">
            <h1>{title_text}</h1>
            <p>{body_text}</p>
        </header>

        <!-- Tabs -->
        <div class="tab-menu">
            <button class="tab-link">Posts</button>
            <button class="tab-link">Blogs</button>
            <button class="tab-link active">Videos</button>
        </div>

        <!-- Service Cards Grid -->
        <main class="service-grid">
            <a href="#" class="service-card">
                <span class="card-category">Installation Guide</span>
                <h3 class="card-title">Speedtest-Tracker</h3>
            </a>
            
            <a href="#" class="service-card">
                <span class="card-category">Setup</span>
                <h3 class="card-title">Uptime-Kuma</h3>
            </a>
            
            <a href="#" class="service-card">
                <span class="card-category">Playlist</span>
                <h3 class="card-title">HomeLab (Self-hosting)</h3>
            </a>
        </main>

    </div>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Ambient Glassmorphic Theme-Toggling Hub - Logic
document.addEventListener('DOMContentLoaded', () => {{
    const themeToggle = document.getElementById('themeToggle');
    const body = document.body;

    // Listen for checkbox state change
    themeToggle.addEventListener('change', (e) => {{
        if (e.target.checked) {{
            // Switch to Dark Mode
            body.classList.add('dark');
        }} else {{
            // Switch to Light Mode
            body.classList.remove('dark');
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
