def create_component(
    output_dir: str,
    title_text: str = "Why Not Your Own Services?",
    body_text: str = "Start Your Self-Hosting Journey with us!",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#ec4899",     # Pink accent color similar to the video
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Ambient Glow Dark Mode Toggle & Card Grid.
    
    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)
    
    # Pre-calculate secondary color for the gradient glow based on accent_color
    # For simplicity in this script, we'll pair the accent with a complementary/analogous fixed color
    secondary_glow = "#8b5cf6" # slate/purple blue

    # === CSS ===
    # Notice the double curly braces {{ }} to escape Python's f-string formatting
    css = f"""/* Ambient Glow Dark Mode Toggle Component */
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');

*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    /* Light Theme Defaults */
    --bg-color: #f8f9fa;
    --text-color: #0f172a;
    --text-muted: #64748b;
    --surface-bg: rgba(255, 255, 255, 0.7);
    --surface-border: #e2e8f0;
    --surface-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
    
    /* Brand Colors */
    --accent: {accent_color};
    --glow-secondary: {secondary_glow};
    
    /* Dimensions */
    --max-width: {width_px}px;
}}

body.dark-mode {{
    /* Dark Theme Overrides */
    --bg-color: #0f172a;
    --text-color: #f8fafc;
    --text-muted: #94a3b8;
    --surface-bg: rgba(30, 41, 59, 0.6);
    --surface-border: #334155;
    --surface-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.3), 0 4px 6px -2px rgba(0, 0, 0, 0.15);
}}

body {{
    font-family: 'Poppins', sans-serif;
    background-color: var(--bg-color);
    color: var(--text-color);
    min-height: 100vh;
    display: flex;
    justify-content: center;
    overflow-x: hidden;
    transition: background-color 0.4s ease, color 0.4s ease;
    position: relative;
}}

/* Ambient Background Glow */
.ambient-glow {{
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: 60vw;
    height: 60vw;
    max-width: 800px;
    max-height: 800px;
    background: linear-gradient(135deg, var(--accent), var(--glow-secondary));
    filter: blur(120px);
    border-radius: 50%;
    z-index: -1;
    opacity: 0.3;
    pointer-events: none;
    transition: opacity 0.5s ease;
}}

body.dark-mode .ambient-glow {{
    opacity: 0.15; /* Adjusted for dark mode contrast */
}}

/* Layout */
.app-container {{
    width: 100%;
    max-width: var(--max-width);
    padding: 2rem;
    display: flex;
    flex-direction: column;
    min-height: {height_px}px;
    position: relative;
    z-index: 1;
}}

/* Top Navigation & Toggle */
.navbar {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding-bottom: 2rem;
}}

.logo {{
    font-weight: 700;
    font-size: 1.25rem;
    letter-spacing: -0.5px;
}}

.toggle-wrapper {{
    display: flex;
    align-items: center;
    gap: 1rem;
}}

.toggle-label-text {{
    font-size: 0.875rem;
    font-weight: 600;
}}

/* Custom Toggle Switch */
.theme-switch {{
    position: relative;
    display: inline-block;
    width: 56px;
    height: 30px;
}}

.theme-switch input {{
    opacity: 0;
    width: 0;
    height: 0;
}}

.slider {{
    position: absolute;
    cursor: pointer;
    top: 0; left: 0; right: 0; bottom: 0;
    background-color: #cbd5e1;
    transition: .4s;
    border-radius: 30px;
}}

.slider:before {{
    position: absolute;
    content: "";
    height: 22px;
    width: 22px;
    left: 4px;
    bottom: 4px;
    background-color: white;
    transition: .4s cubic-bezier(0.4, 0.0, 0.2, 1);
    border-radius: 50%;
    box-shadow: 0 2px 4px rgba(0,0,0,0.2);
}}

input:checked + .slider {{
    background-color: var(--accent);
}}

input:checked + .slider:before {{
    transform: translateX(26px);
}}

/* Hero Section */
.hero {{
    text-align: center;
    margin: 4rem 0;
}}

.hero h1 {{
    font-size: 3rem;
    font-weight: 700;
    margin-bottom: 1rem;
    letter-spacing: -1px;
}}

.hero p {{
    font-size: 1.125rem;
    color: var(--text-muted);
}}

/* Horizontal Menu Links */
.sub-nav {{
    display: flex;
    justify-content: center;
    gap: 2rem;
    margin-bottom: 3rem;
    border-bottom: 1px solid var(--surface-border);
    padding-bottom: 1rem;
}}

.sub-nav a {{
    text-decoration: none;
    color: var(--text-muted);
    font-weight: 600;
    font-size: 1rem;
    transition: color 0.3s ease;
    position: relative;
}}

.sub-nav a:hover, .sub-nav a.active {{
    color: var(--text-color);
}}

.sub-nav a.active::after {{
    content: '';
    position: absolute;
    bottom: -17px;
    left: 0;
    width: 100%;
    height: 3px;
    background-color: var(--accent);
    border-radius: 3px 3px 0 0;
}}

/* Card Grid */
.card-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 1.5rem;
}}

.card {{
    background: var(--surface-bg);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border: 1px solid var(--surface-border);
    border-radius: 1rem;
    padding: 1.5rem;
    box-shadow: var(--surface-shadow);
    transition: transform 0.3s ease, box-shadow 0.3s ease, border-color 0.3s ease;
    cursor: pointer;
}}

.card:hover {{
    transform: translateY(-5px);
    box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 8px 10px -6px rgba(0, 0, 0, 0.1);
    border-color: var(--accent);
}}

.card-label {{
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: var(--text-muted);
    margin-bottom: 0.5rem;
    font-weight: 600;
}}

.card-title {{
    font-size: 1.25rem;
    font-weight: 600;
}}
"""

    # Format initialization for dark mode based on python parameter
    dark_class = ' class="dark-mode"' if color_scheme == 'dark' else ''
    checked_attr = 'checked' if color_scheme == 'dark' else ''

    # === HTML ===
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text}</title>
    <link rel="stylesheet" href="style.css">
    <!-- FontAwesome for icons (if needed later) -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
</head>
<body{dark_class}>
    <div class="ambient-glow"></div>
    
    <div class="app-container">
        <!-- Navigation -->
        <nav class="navbar">
            <div class="logo">Echoes of Ping</div>
            
            <div class="toggle-wrapper">
                <span class="toggle-label-text">Lights</span>
                <label class="theme-switch">
                    <input type="checkbox" id="themeToggle" {checked_attr}>
                    <span class="slider"></span>
                </label>
            </div>
        </nav>

        <!-- Hero -->
        <section class="hero">
            <h1>{title_text}</h1>
            <p>{body_text}</p>
        </section>

        <!-- Category Links -->
        <div class="sub-nav">
            <a href="#">Posts</a>
            <a href="#">Blogs</a>
            <a href="#" class="active">Videos</a>
        </div>

        <!-- Grid -->
        <div class="card-grid">
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
    </div>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Ambient Glow Theme Toggle Logic
document.addEventListener('DOMContentLoaded', () => {{
    const toggleSwitch = document.getElementById('themeToggle');
    const body = document.body;

    // Listen for toggle changes
    toggleSwitch.addEventListener('change', function() {{
        if (this.checked) {{
            body.classList.add('dark-mode');
        }} else {{
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
