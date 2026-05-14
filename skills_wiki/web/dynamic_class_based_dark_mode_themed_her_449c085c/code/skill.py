def create_component(
    output_dir: str,
    title_text: str = "Why Not Your Own Services?",
    body_text: str = "Start Your Self-hosting Journey with us!",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#ec4899",     # Pinkish accent from the video
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Class-Based Dark Mode Hero effect.
    
    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)
    
    # Determine initial state flags based on chosen color_scheme
    is_dark = color_scheme.lower() == "dark"
    body_class = "dark" if is_dark else ""
    toggle_checked = "checked" if is_dark else ""

    # === CSS ===
    css = f"""/* Dynamic Dark Mode Theme — Generated Component */
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

:root {{
    /* Light Mode Variables (Default) */
    --bg-color: #f8f9fa;
    --surface-color: #ffffff;
    --text-main: #0f172a;
    --text-muted: #64748b;
    --border-color: #e2e8f0;
    --shadow-color: rgba(0, 0, 0, 0.05);
    
    /* Global Variables */
    --accent: {accent_color};
    --width: {width_px}px;
    --height: {height_px}px;
}}

/* Dark Mode Variables */
body.dark {{
    --bg-color: #0b1117;
    --surface-color: #151e29;
    --text-main: #f8fafc;
    --text-muted: #94a3b8;
    --border-color: #1e293b;
    --shadow-color: rgba(0, 0, 0, 0.3);
}}

* {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

/* Global Smooth Transitions */
body, .surface, h1, p, span, .nav-btn, .card {{
    transition: background-color 0.4s ease, color 0.4s ease, border-color 0.4s ease, box-shadow 0.4s ease;
}}

body {{
    font-family: 'Poppins', sans-serif;
    background-color: var(--bg-color);
    color: var(--text-main);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow-x: hidden;
}}

.app-container {{
    width: 100%;
    max-width: var(--width);
    min-height: var(--height);
    display: flex;
    flex-direction: column;
    padding: 2rem;
}}

/* Header & Nav */
header {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding-bottom: 4rem;
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

.dot {{ width: 10px; height: 10px; border-radius: 50%; }}
.dot-1 {{ background: #ef4444; }}
.dot-2 {{ background: #eab308; }}
.dot-3 {{ background: #22c55e; }}

.nav-actions {{
    display: flex;
    align-items: center;
    gap: 1.5rem;
}}

.nav-btn {{
    background: var(--surface-color);
    color: var(--text-main);
    border: 1px solid var(--border-color);
    padding: 0.5rem 1rem;
    border-radius: 8px;
    font-family: inherit;
    font-weight: 500;
    cursor: pointer;
    display: flex;
    align-items: center;
    gap: 0.5rem;
    box-shadow: 0 2px 4px var(--shadow-color);
}}

.nav-btn:hover {{
    border-color: var(--accent);
    color: var(--accent);
}}

/* Theme Toggle Switch */
.theme-switch-wrapper {{
    display: flex;
    align-items: center;
    gap: 0.75rem;
    font-weight: 500;
}}

.toggle-input {{
    display: none;
}}

.toggle-label {{
    position: relative;
    display: block;
    width: 50px;
    height: 26px;
    background-color: var(--border-color);
    border-radius: 50px;
    cursor: pointer;
    transition: background-color 0.4s ease;
}}

.toggle-label::after {{
    content: '';
    position: absolute;
    top: 3px;
    left: 3px;
    width: 20px;
    height: 20px;
    background-color: #ffffff;
    border-radius: 50%;
    transition: transform 0.4s cubic-bezier(0.4, 0.0, 0.2, 1);
    box-shadow: 0 2px 4px rgba(0,0,0,0.2);
}}

.toggle-input:checked + .toggle-label {{
    background-color: var(--accent);
}}

.toggle-input:checked + .toggle-label::after {{
    transform: translateX(24px);
}}

/* Hero Section */
.hero {{
    text-align: center;
    margin-bottom: 4rem;
    flex-grow: 1;
    display: flex;
    flex-direction: column;
    justify-content: center;
}}

.hero h1 {{
    font-size: 3.5rem;
    font-weight: 700;
    margin-bottom: 1rem;
    letter-spacing: -0.5px;
}}

.hero p {{
    font-size: 1.25rem;
    color: var(--text-muted);
}}

/* Cards Section */
.cards-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 2rem;
    padding-top: 2rem;
    border-top: 1px solid var(--border-color);
}}

.card {{
    background: var(--surface-color);
    padding: 1.5rem;
    border-radius: 12px;
    border: 1px solid var(--border-color);
    box-shadow: 0 4px 6px var(--shadow-color);
    cursor: pointer;
    transform: translateY(0);
    transition: transform 0.3s ease, border-color 0.3s ease, box-shadow 0.3s ease, background-color 0.4s ease;
}}

.card:hover {{
    transform: translateY(-5px);
    border-color: var(--accent);
    box-shadow: 0 8px 15px var(--shadow-color);
}}

.card-label {{
    font-size: 0.85rem;
    color: var(--text-muted);
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 0.5rem;
}}

.card-title {{
    font-size: 1.25rem;
    font-weight: 600;
    color: var(--text-main);
}}

/* Gradient accents behind UI (like the video's glowing orbs) */
.glow {{
    position: absolute;
    width: 600px;
    height: 600px;
    background: radial-gradient(circle, var(--accent) 0%, transparent 70%);
    opacity: 0.05;
    z-index: -1;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    pointer-events: none;
}}
body.dark .glow {{
    opacity: 0.15;
}}
"""

    # === HTML ===
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text}</title>
    <!-- External Dependencies for Typography and Icons -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link rel="stylesheet" href="style.css">
</head>
<body class="{body_class}">
    <div class="glow"></div>
    <div class="app-container">
        
        <!-- Top Navigation -->
        <header>
            <div class="logo-group">
                <div class="logo-dots">
                    <div class="dot dot-1"></div>
                    <div class="dot dot-2"></div>
                    <div class="dot dot-3"></div>
                </div>
                <span>Echoes of Ping</span>
            </div>
            
            <div class="nav-actions">
                <button class="nav-btn"><i class="fa-brands fa-youtube" style="color: #ff0000;"></i> YouTube</button>
                <button class="nav-btn">Join now <i class="fa-solid fa-user"></i></button>
            </div>
        </header>

        <!-- Main Hero Content -->
        <main class="hero">
            <h1>{title_text}</h1>
            <p>{body_text}</p>
        </main>

        <!-- Theme Toggle & Categories -->
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 2rem;">
            <div style="display: flex; gap: 2rem; font-weight: 600; color: var(--text-muted);">
                <span style="color: var(--accent); border-bottom: 2px solid var(--accent); padding-bottom: 0.5rem; cursor:pointer;">Videos</span>
                <span style="cursor:pointer; hover:color:var(--text-main);">Posts</span>
                <span style="cursor:pointer; hover:color:var(--text-main);">Blogs</span>
            </div>

            <div class="theme-switch-wrapper">
                <span>Lights</span>
                <input type="checkbox" id="themeToggle" class="toggle-input" {toggle_checked}>
                <label for="themeToggle" class="toggle-label" aria-label="Toggle Dark Mode"></label>
            </div>
        </div>

        <!-- Cards -->
        <div class="cards-grid">
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
    js = f"""// Dynamic Dark Mode Toggle Logic
document.addEventListener('DOMContentLoaded', () => {{
    const themeToggle = document.getElementById('themeToggle');
    
    // Listen for changes on the checkbox
    themeToggle.addEventListener('change', (e) => {{
        if (e.target.checked) {{
            // Add 'dark' class to body
            document.body.classList.add('dark');
        }} else {{
            // Remove 'dark' class from body
            document.body.classList.remove('dark');
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
