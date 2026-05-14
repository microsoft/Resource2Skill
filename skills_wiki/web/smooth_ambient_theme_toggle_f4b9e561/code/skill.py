def create_component(
    output_dir: str,
    title_text: str = "Why not Your own Services?",
    body_text: str = "Start Your Self-hosting Journey with us!",
    color_scheme: str = "light",       # "dark" or "light"
    accent_color: str = "#ec4899",     # Pink accent from the video
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Smooth Ambient Theme Toggle effect.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)
    
    # Determine initial state flags
    is_dark = color_scheme.lower() == "dark"
    body_class = ' class="dark-mode"' if is_dark else ""
    checkbox_checked = "checked" if is_dark else ""

    # === CSS ===
    css = f"""/* Smooth Ambient Theme Toggle */
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');

*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

/* Light Mode Variables (Default) */
:root {{
    --bg-color: #f8f9fa;
    --text-main: #1a1a2e;
    --text-muted: #6b7280;
    --surface-bg: rgba(255, 255, 255, 0.7);
    --surface-border: rgba(0, 0, 0, 0.05);
    --accent: {accent_color};
    --glow-1: #ff9a9e;
    --glow-2: #fecfef;
    --toggle-bg: #cbd5e1;
    --width: {width_px}px;
    --height: {height_px}px;
}}

/* Dark Mode Variables */
body.dark-mode {{
    --bg-color: #111222;
    --text-main: #f8f9fa;
    --text-muted: #9ca3af;
    --surface-bg: rgba(255, 255, 255, 0.05);
    --surface-border: rgba(255, 255, 255, 0.1);
    --glow-1: #432371;
    --glow-2: #fa709a;
    --toggle-bg: var(--accent);
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
    /* The magic that makes the theme swap smooth */
    transition: background-color 0.4s ease, color 0.4s ease;
}}

/* Set requested dimensions */
.viewport {{
    width: var(--width);
    height: var(--height);
    position: relative;
    max-width: 100vw;
    display: flex;
    flex-direction: column;
    overflow: hidden;
    box-shadow: 0 20px 40px rgba(0,0,0,0.1);
    background-color: var(--bg-color);
    transition: background-color 0.4s ease;
}}

/* Ambient Glow Backgrounds */
.ambient-glow {{
    position: absolute;
    border-radius: 50%;
    filter: blur(120px);
    z-index: 0;
    transition: background 0.6s ease;
}}

.glow-left {{
    top: -10%;
    left: -10%;
    width: 500px;
    height: 500px;
    background: var(--glow-1);
    opacity: 0.5;
}}

.glow-right {{
    bottom: -10%;
    right: -10%;
    width: 600px;
    height: 600px;
    background: var(--glow-2);
    opacity: 0.4;
}}

/* Header & Toggle Area */
header {{
    position: relative;
    z-index: 10;
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 2rem 3rem;
}}

.logo {{
    font-weight: 700;
    font-size: 1.25rem;
    letter-spacing: -0.5px;
}}

.theme-controls {{
    display: flex;
    align-items: center;
    gap: 1rem;
    font-size: 0.9rem;
    font-weight: 600;
}}

/* Pill Toggle Switch Styles */
.switch {{
    position: relative;
    display: inline-block;
    width: 52px;
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
    height: 20px;
    width: 20px;
    left: 4px;
    bottom: 4px;
    background-color: white;
    transition: .4s cubic-bezier(0.4, 0, 0.2, 1);
    border-radius: 50%;
    box-shadow: 0 2px 4px rgba(0,0,0,0.2);
}}

input:checked + .slider:before {{
    transform: translateX(24px);
}}

/* Main Hero Content */
main {{
    position: relative;
    z-index: 10;
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    padding: 2rem;
}}

h1 {{
    font-size: 3.5rem;
    font-weight: 700;
    margin-bottom: 1rem;
    letter-spacing: -1px;
    transition: color 0.4s ease;
}}

p {{
    font-size: 1.25rem;
    color: var(--text-muted);
    margin-bottom: 3rem;
    transition: color 0.4s ease;
}}

/* Glassmorphism Cards */
.cards-container {{
    display: flex;
    gap: 1.5rem;
    flex-wrap: wrap;
    justify-content: center;
}}

.card {{
    background: var(--surface-bg);
    border: 1px solid var(--surface-border);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    padding: 1.5rem 2rem;
    border-radius: 1rem;
    min-width: 200px;
    text-align: left;
    transition: background 0.4s ease, border-color 0.4s ease, transform 0.2s ease;
    box-shadow: 0 4px 6px rgba(0,0,0,0.05);
}}

.card:hover {{
    transform: translateY(-5px);
}}

.card h3 {{
    font-size: 0.85rem;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: var(--text-muted);
    margin-bottom: 0.5rem;
}}

.card h2 {{
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
    <div class="viewport">
        <!-- Ambient Background Glows -->
        <div class="ambient-glow glow-left"></div>
        <div class="ambient-glow glow-right"></div>

        <!-- Header -->
        <header>
            <div class="logo">Echoes</div>
            <div class="theme-controls">
                <span>Lights</span>
                <label class="switch" aria-label="Toggle Dark Mode">
                    <input type="checkbox" id="theme-toggle" {checkbox_checked}>
                    <span class="slider"></span>
                </label>
            </div>
        </header>

        <!-- Main Content -->
        <main>
            <h1>{title_text}</h1>
            <p>{body_text}</p>

            <div class="cards-container">
                <div class="card">
                    <h3>Installation Guide</h3>
                    <h2>Speedtest-Tracker</h2>
                </div>
                <div class="card">
                    <h3>Setup</h3>
                    <h2>Uptime-Kuma</h2>
                </div>
                <div class="card">
                    <h3>Playlist</h3>
                    <h2>HomeLab (Self-hosting)</h2>
                </div>
            </div>
        </main>
    </div>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Smooth Ambient Theme Toggle Logic
document.addEventListener('DOMContentLoaded', () => {{
    const toggleSwitch = document.getElementById('theme-toggle');
    const body = document.body;

    // Listen for toggle changes
    toggleSwitch.addEventListener('change', function() {{
        if (this.checked) {{
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
