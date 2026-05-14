def create_component(
    output_dir: str,
    title_text: str = "Why not Your own Services?",
    body_text: str = "Start Your Self-hosting Journey with us!",
    color_scheme: str = "light",  # "dark" or "light" (initial state)
    accent_color: str = "#ec4899", # Pink accent from the video
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Light/Dark Theme Toggle effect.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Determine initial checked state for the toggle based on color_scheme
    is_dark = color_scheme.lower() == "dark"
    checked_attr = "checked" if is_dark else ""
    body_class = "dark-mode" if is_dark else ""

    # === CSS ===
    css = f"""/* Theme Toggle Component */
:root {{
    /* Base configuration */
    --accent-color: {accent_color};
    --width: {width_px}px;
    --height: {height_px}px;
    
    /* Light Theme Variables (Default) */
    --bg-color: #f8fafc;
    --text-primary: #0f172a;
    --text-secondary: #475569;
    --surface-color: #ffffff;
    --border-color: transparent;
    --shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1);
    --glow-opacity: 0.6;
    --toggle-bg: #e2e8f0;
    --toggle-knob: #ffffff;
}}

/* Dark Theme Variables */
body.dark-mode {{
    --bg-color: #0f172a;
    --text-primary: #f8fafc;
    --text-secondary: #94a3b8;
    --surface-color: #1e293b;
    --border-color: #334155;
    --shadow: none;
    --glow-opacity: 0.15;
    --toggle-bg: var(--accent-color);
    --toggle-knob: #ffffff;
}}

/* Global Reset & Base Styles */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: 'Poppins', system-ui, -apple-system, sans-serif;
    background-color: var(--bg-color);
    color: var(--text-primary);
    min-height: 100vh;
    display: flex;
    justify-content: center;
    overflow-x: hidden;
    /* The crucial transition for smooth theme swapping */
    transition: background-color 0.4s ease, color 0.4s ease;
}}

.app-container {{
    width: 100%;
    max-width: var(--width);
    min-height: var(--height);
    position: relative;
    padding: 2rem;
    display: flex;
    flex-direction: column;
}}

/* Decorative Background Glow */
.background-glow {{
    position: absolute;
    top: 20%;
    left: 50%;
    transform: translateX(-50%);
    width: 600px;
    height: 400px;
    background: linear-gradient(to bottom right, var(--accent-color), #8b5cf6);
    border-radius: 50%;
    filter: blur(120px);
    opacity: var(--glow-opacity);
    z-index: -1;
    pointer-events: none;
    transition: opacity 0.4s ease;
}}

/* Navigation & Toggle */
header {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding-bottom: 4rem;
}}

.brand {{
    font-weight: 700;
    font-size: 1.25rem;
    display: flex;
    gap: 0.5rem;
}}

.brand span {{ color: var(--accent-color); }}

.theme-controls {{
    display: flex;
    align-items: center;
    gap: 1rem;
}}

.theme-controls span {{
    font-size: 0.875rem;
    font-weight: 500;
}}

/* Custom Toggle Switch styling */
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
    transition: .4s;
    border-radius: 50%;
    box-shadow: 0 2px 4px rgba(0,0,0,0.2);
}}

input:checked + .slider:before {{
    transform: translateX(22px);
}}

/* Main Content Area */
main {{
    text-align: center;
    flex-grow: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding-top: 4rem;
}}

h1 {{
    font-size: 3rem;
    font-weight: 600;
    margin-bottom: 1rem;
}}

p.subtitle {{
    font-size: 1.125rem;
    color: var(--text-secondary);
    margin-bottom: 4rem;
    transition: color 0.4s ease;
}}

/* Cards Grid */
.cards-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 2rem;
    width: 100%;
    max-width: 1000px;
}}

.card {{
    background-color: var(--surface-color);
    padding: 2rem;
    border-radius: 1rem;
    box-shadow: var(--shadow);
    border: 1px solid var(--border-color);
    text-align: left;
    transition: background-color 0.4s ease, border-color 0.4s ease, box-shadow 0.4s ease, transform 0.2s ease;
}}

.card:hover {{
    transform: translateY(-4px);
}}

.card-tag {{
    font-size: 0.75rem;
    font-weight: 600;
    color: var(--text-secondary);
    text-transform: uppercase;
    letter-spacing: 0.05em;
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
    <title>{title_text}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body class="{body_class}">
    <div class="background-glow"></div>
    
    <div class="app-container">
        <header>
            <div class="brand">
                <span>●</span> Echoes of Ping
            </div>
            
            <div class="theme-controls">
                <span>Lights</span>
                <label class="switch" aria-label="Toggle Dark Mode">
                    <input type="checkbox" id="theme-toggle" {checked_attr}>
                    <span class="slider"></span>
                </label>
            </div>
        </header>

        <main>
            <h1>{title_text}</h1>
            <p class="subtitle">{body_text}</p>

            <div class="cards-grid">
                <div class="card">
                    <span class="card-tag">Installation Guide</span>
                    <div class="card-title">Speedtest-Tracker</div>
                </div>
                <div class="card">
                    <span class="card-tag">Setup</span>
                    <div class="card-title">Uptime-Kuma</div>
                </div>
                <div class="card">
                    <span class="card-tag">Playlist</span>
                    <div class="card-title">HomeLab (Self-hosting)</div>
                </div>
            </div>
        </main>
    </div>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Theme Toggling Logic
document.addEventListener('DOMContentLoaded', () => {{
    const themeToggle = document.getElementById('theme-toggle');
    
    // Listen for changes on the checkbox
    themeToggle.addEventListener('change', () => {{
        // Toggle the 'dark-mode' class on the body element.
        // The CSS handles the transition of variables.
        if (themeToggle.checked) {{
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
