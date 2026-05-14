def create_component(
    output_dir: str,
    title_text: str = "Why Not Your Own Services?",
    body_text: str = "Start your self-hosting journey with us! Discover modern, beautiful architectures.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#fa39ad",     # Accent color for hovers/toggles
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Ambient Glassmorphism with Theme Toggle effect.
    
    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Determine initial mode class based on color_scheme
    body_class = "dark-mode" if color_scheme == "dark" else ""
    toggle_checked = "checked" if color_scheme == "dark" else ""

    # === CSS ===
    css = f"""/* Base & Reset */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    /* Default (Light Mode) Variables */
    --bg-base: #f3f3f3;
    --text-primary: #1a1a2e;
    --text-secondary: #4a4a68;
    --card-bg: rgba(255, 255, 255, 0.7);
    --card-border: rgba(255, 255, 255, 0.5);
    --card-border-hover: {accent_color};
    --orb-gradient: linear-gradient(to bottom, #fa39ad 30%, #fa6c4c 70%);
    --toggle-bg: #ccc;
    --accent: {accent_color};
}}

body.dark-mode {{
    /* Dark Mode Variables */
    --bg-base: #001515;
    --text-primary: #ffffff;
    --text-secondary: #a0b0b0;
    --card-bg: rgba(17, 34, 34, 0.6);
    --card-border: rgba(255, 255, 255, 0.1);
    --card-border-hover: #00ffaa; /* Specific dark mode accent */
    --orb-gradient: linear-gradient(to bottom, #00ffaa 40%, #0066ff 80%);
    --toggle-bg: #334444;
    --accent: #00ffaa;
}}

body {{
    font-family: 'Poppins', system-ui, sans-serif;
    background-color: var(--bg-base);
    color: var(--text-primary);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow-x: hidden;
    position: relative;
    transition: background-color 0.4s ease, color 0.4s ease;
}}

.app-wrapper {{
    width: 100%;
    max-width: {width_px}px;
    min-height: {height_px}px;
    position: relative;
    padding: 2rem;
    display: flex;
    flex-direction: column;
}}

/* === Ambient Glowing Orb === */
.ambient-orb {{
    position: absolute;
    bottom: -10%;
    left: 50%;
    transform: translateX(-50%);
    width: 500px;
    height: 500px;
    border-radius: 50%;
    background: var(--orb-gradient);
    filter: blur(140px);
    z-index: 0;
    opacity: 0.8;
    pointer-events: none;
    transition: background 0.5s ease;
}}

/* === Main Layout (Above Orb) === */
.content-layer {{
    position: relative;
    z-index: 10;
    display: flex;
    flex-direction: column;
    gap: 3rem;
    flex: 1;
}}

/* === Header & Toggle === */
header {{
    display: flex;
    justify-content: flex-end;
    align-items: center;
    padding: 1rem 0;
}}

.theme-toggle-wrapper {{
    display: flex;
    align-items: center;
    gap: 12px;
    font-weight: 500;
    font-size: 0.9rem;
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
    transition: 0.4s;
    border-radius: 34px;
}}

.slider:before {{
    position: absolute;
    content: "";
    height: 20px;
    width: 20px;
    left: 4px;
    bottom: 4px;
    background-color: white;
    transition: 0.4s;
    border-radius: 50%;
}}

input:checked + .slider {{
    background-color: var(--accent);
}}

input:checked + .slider:before {{
    transform: translateX(22px);
}}

/* === Hero Section === */
.hero {{
    text-align: center;
    margin-top: 2rem;
}}

.hero h1 {{
    font-size: clamp(2rem, 4vw, 3.5rem);
    font-weight: 600;
    margin-bottom: 1rem;
    letter-spacing: -0.02em;
}}

.hero p {{
    font-size: 1.1rem;
    color: var(--text-secondary);
    max-width: 600px;
    margin: 0 auto;
}}

/* === Glassmorphic Cards Grid === */
.grid-container {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 1.5rem;
    margin-top: 2rem;
}}

.glass-card {{
    background: var(--card-bg);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border: 2px solid var(--card-border);
    border-radius: 1.5rem;
    padding: 2rem;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.05);
    transition: transform 0.3s ease, border-color 0.3s ease, box-shadow 0.3s ease;
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
    cursor: pointer;
}}

.glass-card:hover {{
    transform: translateY(-5px);
    border-color: var(--card-border-hover);
    box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1);
}}

.glass-card h3 {{
    font-size: 1.25rem;
    font-weight: 600;
}}

.glass-card span.badge {{
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: var(--text-secondary);
    font-weight: 500;
}}
"""

    # === HTML ===
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text}</title>
    <!-- Google Fonts for typography styling -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body class="{body_class}">
    <div class="ambient-orb"></div>
    
    <div class="app-wrapper">
        <div class="content-layer">
            
            <header>
                <div class="theme-toggle-wrapper">
                    <span>Lights</span>
                    <label class="switch">
                        <input type="checkbox" id="themeToggle" {toggle_checked}>
                        <span class="slider"></span>
                    </label>
                </div>
            </header>

            <section class="hero">
                <h1>{title_text}</h1>
                <p>{body_text}</p>
            </section>

            <section class="grid-container">
                <div class="glass-card">
                    <span class="badge">Installation Guide</span>
                    <h3>Speedtest-Tracker</h3>
                </div>
                <div class="glass-card">
                    <span class="badge">Setup</span>
                    <h3>Uptime-Kuma</h3>
                </div>
                <div class="glass-card">
                    <span class="badge">Playlist</span>
                    <h3>HomeLab (Self-hosting)</h3>
                </div>
                <div class="glass-card">
                    <span class="badge">Network</span>
                    <h3>Nginx Proxy Manager</h3>
                </div>
            </section>
            
        </div>
    </div>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = """document.addEventListener('DOMContentLoaded', () => {
    const themeToggle = document.getElementById('themeToggle');

    // Toggle theme by adding/removing 'dark-mode' class on the body
    themeToggle.addEventListener('change', (e) => {
        if (e.target.checked) {
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
