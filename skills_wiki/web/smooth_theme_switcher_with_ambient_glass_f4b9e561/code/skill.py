def create_component(
    output_dir: str,
    title_text: str = "Why Not Your Own Services?",
    body_text: str = "Start Your Self-Hosting Journey with us!",
    color_scheme: str = "light",       # "dark" or "light" (initial state)
    accent_color: str = "#00e5ff",     # Cyan accent for primary glowing orb
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Smooth Theme Switcher with Ambient Glassmorphism.
    
    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Base colors (The exact hexes from the video's dark/light modes)
    light_bg = "#f3f3f3"
    light_text = "#111222"
    light_card = "rgba(255, 255, 255, 0.6)"
    light_card_border = "rgba(0, 0, 0, 0.05)"
    light_toggle_bg = "#e2e8f0"
    
    dark_bg = "#0c1a1a"
    dark_text = "#eef4f0"
    dark_card = "rgba(255, 255, 255, 0.03)"
    dark_card_border = "rgba(255, 255, 255, 0.08)"
    dark_toggle_bg = "#1f2937"

    # Pre-calculate boolean for template logic
    is_dark = (color_scheme == "dark")
    body_class = "dark-mode" if is_dark else ""
    checkbox_checked = "checked" if is_dark else ""

    css = f"""/* Smooth Theme Switcher with Ambient Glassmorphism */
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

:root {{
    /* Default Light Theme Variables */
    --bg-color: {light_bg};
    --text-color: {light_text};
    --card-bg: {light_card};
    --card-border: {light_card_border};
    --toggle-bg: {light_toggle_bg};
    --accent-glow: {accent_color};
    --secondary-glow: #ff00ff;
    
    --comp-width: 100%;
    --comp-height: {height_px}px;
}}

body.dark-mode {{
    /* Dark Theme Variables */
    --bg-color: {dark_bg};
    --text-color: {dark_text};
    --card-bg: {dark_card};
    --card-border: {dark_card_border};
    --toggle-bg: {dark_toggle_bg};
}}

* {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: 'Poppins', sans-serif;
    background-color: var(--bg-color);
    color: var(--text-color);
    transition: background-color 0.4s ease, color 0.4s ease;
    min-height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
    overflow-x: hidden;
}}

.app-wrapper {{
    position: relative;
    width: max(100vw, var(--comp-width));
    min-height: var(--comp-height);
    display: flex;
    flex-direction: column;
    padding: 40px 8vw;
    z-index: 1;
}}

/* --- Ambient Glowing Orbs --- */
.ambient-orb {{
    position: absolute;
    border-radius: 50%;
    filter: blur(120px);
    z-index: -1;
    opacity: 0.6;
    animation: float 10s infinite alternate ease-in-out;
}}

.orb-1 {{
    top: -10%;
    left: -10%;
    width: 500px;
    height: 500px;
    background: var(--accent-glow);
}}

.orb-2 {{
    bottom: -20%;
    right: -5%;
    width: 600px;
    height: 600px;
    background: var(--secondary-glow);
    animation-delay: -5s;
}}

@keyframes float {{
    0% {{ transform: translate(0, 0) scale(1); }}
    100% {{ transform: translate(30px, 50px) scale(1.1); }}
}}

/* --- Top Navigation & Toggle --- */
header {{
    display: flex;
    justify-content: flex-end;
    align-items: center;
    margin-bottom: 80px;
}}

.theme-switch-wrapper {{
    display: flex;
    align-items: center;
    gap: 12px;
    font-weight: 500;
    font-size: 0.9rem;
}}

/* Custom Toggle Switch CSS */
.switch {{
    position: relative;
    display: inline-block;
    width: 64px;
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
    background-color: var(--toggle-bg);
    transition: .4s;
    border-radius: 34px;
    border: 1px solid var(--card-border);
}}

.slider:before {{
    position: absolute;
    content: "\\f185"; /* FontAwesome Sun */
    font-family: "Font Awesome 5 Free";
    font-weight: 900;
    height: 24px;
    width: 24px;
    left: 4px;
    bottom: 3px;
    background-color: white;
    color: #f59e0b;
    transition: .4s cubic-bezier(0.4, 0, 0.2, 1);
    border-radius: 50%;
    display: flex;
    justify-content: center;
    align-items: center;
    font-size: 12px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.2);
}}

input:checked + .slider:before {{
    transform: translateX(32px);
    content: "\\f186"; /* FontAwesome Moon */
    color: #1e293b;
}}

/* --- Main Content --- */
main {{
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
    flex-grow: 1;
}}

.hero-title {{
    font-size: clamp(2.5rem, 5vw, 4rem);
    font-weight: 600;
    margin-bottom: 16px;
    letter-spacing: -1px;
}}

.hero-subtitle {{
    font-size: 1.1rem;
    opacity: 0.8;
    margin-bottom: 60px;
    font-weight: 400;
}}

/* Glassmorphism Grid */
.card-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 24px;
    width: 100%;
    max-width: 1000px;
}}

.glass-card {{
    background: var(--card-bg);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    border: 1px solid var(--card-border);
    border-radius: 20px;
    padding: 32px;
    text-align: left;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}}

.glass-card:hover {{
    transform: translateY(-5px);
    box-shadow: 0 10px 30px rgba(0,0,0,0.1);
}}

.card-label {{
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 1px;
    opacity: 0.6;
    margin-bottom: 8px;
    font-weight: 600;
}}

.card-title {{
    font-size: 1.5rem;
    font-weight: 500;
}}
"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text}</title>
    <!-- FontAwesome for Icons -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css">
    <link rel="stylesheet" href="style.css">
</head>
<body class="{body_class}">
    
    <!-- Ambient Background Orbs -->
    <div class="ambient-orb orb-1"></div>
    <div class="ambient-orb orb-2"></div>

    <div class="app-wrapper">
        <header>
            <div class="theme-switch-wrapper">
                <span>Lights</span>
                <label class="switch" aria-label="Toggle Dark Mode">
                    <input type="checkbox" id="theme-toggle" {checkbox_checked}>
                    <span class="slider"></span>
                </label>
            </div>
        </header>

        <main>
            <h1 class="hero-title">{title_text}</h1>
            <p class="hero-subtitle">{body_text}</p>

            <div class="card-grid">
                <div class="glass-card">
                    <div class="card-label">Installation Guide</div>
                    <h2 class="card-title">Speedtest-Tracker</h2>
                </div>
                <div class="glass-card">
                    <div class="card-label">Setup</div>
                    <h2 class="card-title">Uptime-Kuma</h2>
                </div>
                <div class="glass-card">
                    <div class="card-label">Playlist</div>
                    <h2 class="card-title">HomeLab (Self-hosting)</h2>
                </div>
            </div>
        </main>
    </div>

    <script src="script.js"></script>
</body>
</html>"""

    js = """// Wait for DOM to load
document.addEventListener('DOMContentLoaded', () => {
    const themeToggle = document.getElementById('theme-toggle');
    const body = document.body;

    // Listen for toggle switch changes
    themeToggle.addEventListener('change', () => {
        if (themeToggle.checked) {
            body.classList.add('dark-mode');
        } else {
            body.classList.remove('dark-mode');
        }
    });
});
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
