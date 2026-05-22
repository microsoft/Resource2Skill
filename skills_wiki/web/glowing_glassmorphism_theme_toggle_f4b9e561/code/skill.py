def create_component(
    output_dir: str,
    title_text: str = "Why not Your own Services?",
    body_text: str = "Start Your Self-hosting Journey with us!",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#ff007f",     # CSS hex color for accent
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Glowing Glassmorphism Theme Toggle effect.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Determine initial state based on color_scheme
    is_dark = color_scheme == "dark"
    body_class = ' class="dark-mode"' if is_dark else ""
    checkbox_checked = " checked" if is_dark else ""

    # === CSS ===
    css = f"""/* Glowing Glassmorphism Theme Toggle */
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

:root {{
    /* Base Light Theme Variables */
    --bg-color: #f8f9fa;
    --text-color: #1a1a2e;
    --text-muted: #4a5568;
    --surface-color: rgba(255, 255, 255, 0.6);
    --border-color: rgba(0, 0, 0, 0.05);
    --orb-gradient: linear-gradient(135deg, #ff9a9e 0%, #fecfef 99%, #fecfef 100%);
    --switch-bg: #cbd5e0;
    --accent: {accent_color};
}}

body.dark-mode {{
    /* Dark Theme Variables */
    --bg-color: #0d111c;
    --text-color: #ffffff;
    --text-muted: #a0aec0;
    --surface-color: rgba(255, 255, 255, 0.03);
    --border-color: rgba(255, 255, 255, 0.08);
    --orb-gradient: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
    --switch-bg: #2d3748;
}}

*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: 'Poppins', sans-serif;
    background-color: var(--bg-color);
    color: var(--text-color);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: background-color 0.5s ease, color 0.5s ease;
    overflow-x: hidden;
    position: relative;
}}

/* Animated Background Orb */
.background-orb {{
    position: absolute;
    top: 50%;
    left: 50%;
    width: 60vw;
    height: 60vw;
    max-width: 800px;
    max-height: 800px;
    border-radius: 50%;
    background: var(--orb-gradient);
    filter: blur(120px);
    transform: translate(-50%, -50%);
    z-index: -1;
    opacity: 0.7;
    animation: orb-float 15s ease-in-out infinite alternate;
    transition: background 0.8s ease;
    pointer-events: none;
}}

@keyframes orb-float {{
    0% {{ transform: translate(-50%, -50%) scale(1); }}
    100% {{ transform: translate(-40%, -60%) scale(1.1); }}
}}

/* Main Layout */
.app-wrapper {{
    width: 100%;
    max-width: {width_px}px;
    padding: 2rem;
    display: flex;
    flex-direction: column;
    gap: 3rem;
}}

/* Header & Toggle */
.header {{
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
    gap: 1rem;
}}

.header h1 {{
    font-size: clamp(2rem, 4vw, 3.5rem);
    font-weight: 600;
    letter-spacing: -1px;
}}

.header p {{
    color: var(--text-muted);
    font-size: 1.1rem;
}}

/* Glassmorphic Container */
.glass-panel {{
    background: var(--surface-color);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border: 1px solid var(--border-color);
    border-radius: 24px;
    padding: 2rem;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.05);
    transition: all 0.5s ease;
}}

/* Controls Bar */
.controls-bar {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid var(--border-color);
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
    transition: color 0.3s ease;
}}

.nav-links a.active, .nav-links a:hover {{
    color: var(--text-color);
    border-bottom: 2px solid var(--accent);
    padding-bottom: 0.5rem;
}}

.theme-toggle-wrapper {{
    display: flex;
    align-items: center;
    gap: 1rem;
    font-weight: 500;
}}

/* The Custom Switch */
.switch {{
    position: relative;
    display: inline-block;
    width: 60px;
    height: 32px;
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
    background-color: var(--switch-bg);
    transition: .4s;
    border-radius: 34px;
    box-shadow: inset 0 2px 4px rgba(0,0,0,0.1);
}}

.slider:before {{
    position: absolute;
    content: "";
    height: 24px;
    width: 24px;
    left: 4px;
    bottom: 4px;
    background-color: #fff;
    transition: transform .4s cubic-bezier(0.4, 0.0, 0.2, 1), background-color 0.4s;
    border-radius: 50%;
    box-shadow: 0 2px 5px rgba(0,0,0,0.2);
}}

input:checked + .slider {{
    background-color: var(--switch-bg);
}}

input:focus + .slider {{
    box-shadow: 0 0 1px var(--accent);
}}

input:checked + .slider:before {{
    transform: translateX(28px);
    background-color: var(--accent);
}}

/* Content Cards Grid */
.cards-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 1.5rem;
}}

.card {{
    background: var(--surface-color);
    border: 1px solid var(--border-color);
    border-radius: 16px;
    padding: 1.5rem;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}}

.card:hover {{
    transform: translateY(-5px);
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
}}

.card-tag {{
    font-size: 0.8rem;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: var(--text-muted);
    margin-bottom: 0.5rem;
}}

.card h3 {{
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
    <div class="background-orb"></div>
    
    <div class="app-wrapper">
        <header class="header">
            <h1>{title_text}</h1>
            <p>{body_text}</p>
        </header>

        <main class="glass-panel">
            <div class="controls-bar">
                <nav class="nav-links">
                    <a href="#">Posts</a>
                    <a href="#">Blogs</a>
                    <a href="#" class="active">Videos</a>
                </nav>
                
                <div class="theme-toggle-wrapper">
                    <span>Lights</span>
                    <label class="switch" for="theme-toggle" aria-label="Toggle Dark Mode">
                        <input type="checkbox" id="theme-toggle"{checkbox_checked}>
                        <span class="slider"></span>
                    </label>
                </div>
            </div>

            <div class="cards-grid">
                <div class="card">
                    <div class="card-tag">Installation Guide</div>
                    <h3>Speedtest-Tracker</h3>
                </div>
                <div class="card">
                    <div class="card-tag">Setup</div>
                    <h3>Uptime-Kuma</h3>
                </div>
                <div class="card">
                    <div class="card-tag">Playlist</div>
                    <h3>HomeLab (Self-hosting)</h3>
                </div>
            </div>
        </main>
    </div>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = """document.addEventListener('DOMContentLoaded', () => {
    const themeToggle = document.getElementById('theme-toggle');
    
    // Listen for toggle changes
    themeToggle.addEventListener('change', function() {
        // Toggle the dark-mode class on the body
        if (this.checked) {
            document.body.classList.add('dark-mode');
        } else {
            document.body.classList.remove('dark-mode');
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
