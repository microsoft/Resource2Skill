def create_component(
    output_dir: str,
    title_text: str = "Why Not Your Own Services?",
    body_text: str = "Start Your Self-Hosting Journey with us!",
    color_scheme: str = "light",        # "dark" or "light"
    accent_color: str = "#b464ff",     # CSS hex color for accent
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Ambient Glassmorphism Theme Toggle effect.
    
    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)
    
    # Determine initial state flags based on selected theme
    is_dark = color_scheme == "dark"
    body_class = "dark-mode" if is_dark else ""
    checkbox_checked = "checked" if is_dark else ""

    # === CSS ===
    css = f"""/* Ambient Glassmorphism with Theme Transition */
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    /* Light Theme Variables */
    --bg-base: #fdfdfd;
    --text-main: #111827;
    --text-muted: #4b5563;
    
    /* Glass settings */
    --glass-bg: rgba(255, 255, 255, 0.7);
    --glass-border: rgba(255, 255, 255, 0.5);
    --glass-shadow: rgba(0, 0, 0, 0.05);
    
    /* Ambient Blobs Light */
    --blob-1: #ffc2e2;
    --blob-2: #f0c2ff;
    --blob-3: #ffeec2;
    
    /* Accent */
    --accent: {accent_color};
    --toggle-bg: #e5e7eb;
}}

body.dark-mode {{
    /* Dark Theme Variables */
    --bg-base: #0b0f19;
    --text-main: #f8fafc;
    --text-muted: #94a3b8;
    
    /* Glass settings */
    --glass-bg: rgba(17, 24, 39, 0.6);
    --glass-border: rgba(255, 255, 255, 0.08);
    --glass-shadow: rgba(0, 0, 0, 0.3);
    
    /* Ambient Blobs Dark */
    --blob-1: #00f2fe;
    --blob-2: #4facfe;
    --blob-3: #ff0844;
    
    /* Accent */
    --toggle-bg: var(--accent);
}}

body {{
    font-family: 'Poppins', sans-serif;
    background-color: var(--bg-base);
    color: var(--text-main);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow-x: hidden;
    transition: background-color 0.6s ease, color 0.6s ease;
}}

/* Component Dimensions Constraint */
.app-wrapper {{
    width: 100%;
    max-width: {width_px}px;
    min-height: {height_px}px;
    position: relative;
    display: flex;
    flex-direction: column;
    padding: 2rem;
}}

/* === Ambient Background Blobs === */
.ambient-background {{
    position: absolute;
    top: 0; left: 0; right: 0; bottom: 0;
    overflow: hidden;
    z-index: -1;
    pointer-events: none;
}}

.blob {{
    position: absolute;
    border-radius: 50%;
    filter: blur(80px);
    opacity: 0.6;
    transition: background-color 1s ease;
    animation: float 10s infinite alternate ease-in-out;
}}

.blob-1 {{
    width: 400px; height: 400px;
    background-color: var(--blob-1);
    bottom: -100px; right: 10%;
    animation-delay: 0s;
}}

.blob-2 {{
    width: 500px; height: 500px;
    background-color: var(--blob-2);
    bottom: -150px; left: 5%;
    animation-delay: -3s;
}}

.blob-3 {{
    width: 300px; height: 300px;
    background-color: var(--blob-3);
    top: 20%; left: 30%;
    animation-delay: -6s;
    opacity: 0.4;
}}

@keyframes float {{
    0% {{ transform: translate(0, 0) scale(1); }}
    50% {{ transform: translate(20px, -30px) scale(1.05); }}
    100% {{ transform: translate(-20px, 10px) scale(0.95); }}
}}

/* === Main Layout === */
header {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 4rem;
    z-index: 10;
}}

.logo {{
    font-weight: 700;
    font-size: 1.25rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}}

.logo i {{ color: var(--accent); }}

.hero {{
    text-align: center;
    margin-bottom: 4rem;
    z-index: 10;
}}

.hero h1 {{
    font-size: 3rem;
    font-weight: 600;
    margin-bottom: 1rem;
}}

.hero p {{
    font-size: 1.1rem;
    color: var(--text-muted);
}}

/* === Glassmorphism Container === */
.glass-panel {{
    background: var(--glass-bg);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    border: 1px solid var(--glass-border);
    border-radius: 1.5rem;
    padding: 2rem;
    box-shadow: 0 10px 30px var(--glass-shadow);
    z-index: 10;
    transition: background 0.5s ease, border-color 0.5s ease, box-shadow 0.5s ease;
}}

/* Navigation inside glass */
.glass-nav {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid var(--glass-border);
    padding-bottom: 1.5rem;
    margin-bottom: 1.5rem;
}}

.nav-links {{
    display: flex;
    gap: 2rem;
}}

.nav-links a {{
    color: var(--text-muted);
    text-decoration: none;
    font-weight: 500;
    transition: color 0.3s;
}}

.nav-links a:hover, .nav-links a.active {{
    color: var(--text-main);
}}

/* === Toggle Switch === */
.theme-switch-wrapper {{
    display: flex;
    align-items: center;
    gap: 0.75rem;
    font-weight: 500;
}}

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
    top: 0; left: 0; right: 0; bottom: 0;
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
    background-color: white;
    transition: .4s;
    border-radius: 50%;
    box-shadow: 0 2px 5px rgba(0,0,0,0.2);
}}

input:checked + .slider:before {{
    transform: translateX(24px);
}}

/* === Card Grid === */
.card-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 1.5rem;
}}

.glass-card {{
    background: var(--glass-bg);
    border: 1px solid var(--glass-border);
    border-radius: 1rem;
    padding: 1.5rem;
    transition: transform 0.3s ease, border-color 0.3s ease;
    cursor: pointer;
}}

.glass-card:hover {{
    transform: translateY(-5px);
    border-color: var(--accent);
}}

.card-label {{
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: var(--text-muted);
    margin-bottom: 0.5rem;
    display: block;
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
    <title>Theme Toggle Component</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link rel="stylesheet" href="style.css">
</head>
<body class="{body_class}">
    
    <!-- Ambient Background Layer -->
    <div class="ambient-background">
        <div class="blob blob-1"></div>
        <div class="blob blob-2"></div>
        <div class="blob blob-3"></div>
    </div>

    <!-- Main App Container -->
    <div class="app-wrapper">
        
        <header>
            <div class="logo">
                <i class="fa-solid fa-server"></i>
                <span>EchoesOfPing</span>
            </div>
            <div class="header-actions">
                <a href="#" style="color: var(--text-main); text-decoration: none; font-weight: 500;">Join now <i class="fa-solid fa-user"></i></a>
            </div>
        </header>

        <div class="hero">
            <h1>{title_text}</h1>
            <p>{body_text}</p>
        </div>

        <!-- Glassmorphism Panel -->
        <div class="glass-panel">
            
            <div class="glass-nav">
                <div class="nav-links">
                    <a href="#">Posts</a>
                    <a href="#">Blogs</a>
                    <a href="#" class="active">Videos</a>
                </div>
                
                <!-- Toggle Switch -->
                <div class="theme-switch-wrapper">
                    <span>Lights</span>
                    <label class="theme-switch" for="checkbox">
                        <input type="checkbox" id="checkbox" {checkbox_checked}>
                        <div class="slider round"></div>
                    </label>
                </div>
            </div>

            <div class="card-grid">
                <div class="glass-card">
                    <span class="card-label">Installation Guide</span>
                    <div class="card-title">Speedtest-Tracker</div>
                </div>
                <div class="glass-card">
                    <span class="card-label">Setup</span>
                    <div class="card-title">Uptime-Kuma</div>
                </div>
                <div class="glass-card">
                    <span class="card-label">Playlist</span>
                    <div class="card-title">HomeLab (Self-hosting)</div>
                </div>
            </div>
            
        </div>
    </div>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Theme Toggle Logic
document.addEventListener('DOMContentLoaded', () => {{
    const toggleSwitch = document.getElementById('checkbox');
    const body = document.body;

    // Listen for toggle changes
    toggleSwitch.addEventListener('change', function(e) {{
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
