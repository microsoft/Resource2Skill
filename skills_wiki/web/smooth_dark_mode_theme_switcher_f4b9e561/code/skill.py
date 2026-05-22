def create_component(
    output_dir: str,
    title_text: str = "Why Not Your Own Services?",
    body_text: str = "Start Your Self-Hosting Journey with us!",
    color_scheme: str = "light",       # "dark" or "light"
    accent_color: str = "#ec4899",     # Pink accent similar to the tutorial
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Smooth Dark Mode Theme Switcher.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)
    
    # Pre-calculate boolean for starting state
    is_dark = color_scheme == "dark"
    body_class = ' class="dark-mode"' if is_dark else ""

    # === CSS ===
    css = f"""/* Smooth Dark Mode Theme Switcher */
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600&display=swap');

:root {{
    /* Light Mode Variables (Default) */
    --bg-main: #f8f9fa;
    --bg-surface: #ffffff;
    --text-primary: #1a1a2e;
    --text-secondary: #64748b;
    --accent-color: {accent_color};
    --border-color: #e2e8f0;
    --toggle-track: #cbd5e1;
    --shadow-sm: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
}}

body.dark-mode {{
    /* Dark Mode Variables */
    --bg-main: #0c1a1a;
    --bg-surface: #152a2a;
    --text-primary: #f8fafc;
    --text-secondary: #94a3b8;
    --border-color: #1e3a3a;
    --toggle-track: #334155;
    --shadow-sm: 0 4px 6px -1px rgba(0, 0, 0, 0.2);
}}

*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: 'Poppins', sans-serif;
    background-color: var(--bg-main);
    color: var(--text-primary);
    /* The magic of the effect: global smooth transition */
    transition: background-color 0.4s ease, color 0.4s ease;
    min-height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
}}

/* Universal surface transition to sync with body */
.surface {{
    background-color: var(--bg-surface);
    border: 1px solid var(--border-color);
    box-shadow: var(--shadow-sm);
    transition: background-color 0.4s ease, border-color 0.4s ease, box-shadow 0.4s ease;
}}

.app-container {{
    width: 100%;
    max-width: {width_px}px;
    min-height: {height_px}px;
    padding: 40px;
    display: flex;
    flex-direction: column;
}}

/* Header & Typography */
.header {{
    text-align: center;
    margin-top: 60px;
    margin-bottom: 60px;
}}

.title {{
    font-size: 2.5rem;
    font-weight: 600;
    margin-bottom: 12px;
}}

.subtitle {{
    font-size: 1.1rem;
    color: var(--text-secondary);
    font-weight: 400;
    transition: color 0.4s ease;
}}

/* Layout Navigation / Top Bar */
.nav-bar {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 30px;
    padding: 0 20px;
}}

.nav-links {{
    display: flex;
    gap: 30px;
}}

.nav-link {{
    font-weight: 500;
    color: var(--text-secondary);
    cursor: pointer;
    transition: color 0.3s ease;
}}

.nav-link.active, .nav-link:hover {{
    color: var(--text-primary);
}}

/* Custom Toggle Switch */
.toggle-wrapper {{
    display: flex;
    align-items: center;
    gap: 12px;
    background-color: var(--bg-surface);
    padding: 8px 16px;
    border-radius: 99px;
}}

.toggle-label-text {{
    font-weight: 500;
    font-size: 0.95rem;
}}

.theme-checkbox {{
    display: none;
}}

.theme-label {{
    display: inline-block;
    width: 50px;
    height: 28px;
    background-color: var(--toggle-track);
    border-radius: 99px;
    position: relative;
    cursor: pointer;
    transition: background-color 0.4s ease;
}}

.theme-label::after {{
    content: '';
    position: absolute;
    top: 4px;
    left: 4px;
    width: 20px;
    height: 20px;
    background-color: #ffffff;
    border-radius: 50%;
    transition: transform 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    box-shadow: 0 2px 4px rgba(0,0,0,0.2);
}}

.theme-checkbox:checked + .theme-label {{
    background-color: var(--accent-color);
}}

.theme-checkbox:checked + .theme-label::after {{
    transform: translateX(22px);
}}

/* Grid Cards */
.grid-container {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 24px;
}}

.card {{
    padding: 24px;
    border-radius: 16px;
    cursor: pointer;
}}

.card:hover {{
    border-color: var(--accent-color);
}}

.card-tag {{
    font-size: 0.8rem;
    font-weight: 600;
    color: var(--text-secondary);
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-bottom: 8px;
}}

.card-title {{
    font-size: 1.25rem;
    font-weight: 600;
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
<body{body_class}>
    <div class="app-container">
        
        <div class="header">
            <h1 class="title">{title_text}</h1>
            <p class="subtitle">{body_text}</p>
        </div>

        <div class="nav-bar">
            <div class="nav-links">
                <span class="nav-link">Posts</span>
                <span class="nav-link">Blogs</span>
                <span class="nav-link active">Videos</span>
            </div>
            
            <div class="toggle-wrapper surface">
                <span class="toggle-label-text">Lights</span>
                <input type="checkbox" id="themeToggle" class="theme-checkbox">
                <label for="themeToggle" class="theme-label" aria-label="Toggle Dark Mode"></label>
            </div>
        </div>

        <div class="grid-container">
            <div class="card surface">
                <div class="card-tag">Installation Guide</div>
                <div class="card-title">Speedtest-Tracker</div>
            </div>
            
            <div class="card surface">
                <div class="card-tag">Setup</div>
                <div class="card-title">Uptime-Kuma</div>
            </div>
            
            <div class="card surface">
                <div class="card-tag">Playlist</div>
                <div class="card-title">HomeLab (Self-hosting)</div>
            </div>
        </div>

    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Smooth Dark Mode Theme Switcher - Interaction Logic
document.addEventListener('DOMContentLoaded', () => {{
    const themeToggle = document.getElementById('themeToggle');
    
    // Sync the physical toggle state with the initial configuration
    if (document.body.classList.contains('dark-mode')) {{
        themeToggle.checked = true;
    }}

    // Listen for toggle interactions
    themeToggle.addEventListener('change', function() {{
        // Toggle the global theme class
        if (this.checked) {{
            document.body.classList.add('dark-mode');
        }} else {{
            document.body.classList.remove('dark-mode');
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
