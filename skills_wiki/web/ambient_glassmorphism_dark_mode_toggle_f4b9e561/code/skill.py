def create_component(
    output_dir: str,
    title_text: str = "Why not Your own Services?",
    body_text: str = "Start Your Self-Hosting Journey with us! Toggle the lights to see the magic.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#00ffaa",     # CSS hex color for accent (used heavily in dark mode)
    width_px: int = 1000,
    height_px: int = 600,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Ambient Glassmorphism Dark Mode Toggle.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Base HTML string
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ambient Glassmorphism Toggle</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body data-theme="{color_scheme}">
    <div class="ambient-orb"></div>
    
    <main class="glass-container">
        <header>
            <h1 class="title">{title_text}</h1>
            <p class="body-text">{body_text}</p>
        </header>

        <section class="card-grid">
            <div class="glass-card">
                <h3>Installation Guide</h3>
                <p>Speedtest-Tracker</p>
            </div>
            <div class="glass-card">
                <h3>Setup</h3>
                <p>Uptime-Kuma</p>
            </div>
            <div class="glass-card">
                <h3>Playlist</h3>
                <p>HomeLab</p>
            </div>
        </section>

        <div class="toggle-container">
            <span class="toggle-label">Lights</span>
            <label class="theme-switch" for="themeToggle">
                <input type="checkbox" id="themeToggle" class="theme-switch-checkbox" {"checked" if color_scheme == "dark" else ""} />
                <div class="theme-switch-track">
                    <div class="theme-switch-thumb"></div>
                </div>
            </label>
        </div>
    </main>

    <script src="script.js"></script>
</body>
</html>"""

    # Base CSS string leveraging custom properties
    css = f"""/* Ambient Glassmorphism Toggle Variables */
:root {{
    --bg-color: #f0f4f8;
    --text-color: #1e293b;
    --surface-bg: rgba(255, 255, 255, 0.6);
    --card-bg: rgba(255, 255, 255, 0.7);
    --border-color: rgba(255, 255, 255, 0.5);
    --orb-gradient: linear-gradient(135deg, #ff9a9e, #fecfef);
    --switch-track: #cbd5e1;
    --switch-thumb: #ffffff;
    --accent: {accent_color};
}}

[data-theme="dark"] {{
    --bg-color: #0f172a;
    --text-color: #f8fafc;
    --surface-bg: rgba(30, 41, 59, 0.45);
    --card-bg: rgba(30, 41, 59, 0.65);
    --border-color: rgba(255, 255, 255, 0.08);
    --orb-gradient: linear-gradient(135deg, var(--accent), #3b82f6);
    --switch-track: var(--accent);
    --switch-thumb: #0f172a;
}}

* {{
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}}

body {{
    font-family: 'Poppins', sans-serif;
    background-color: var(--bg-color);
    color: var(--text-color);
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
    overflow: hidden;
    transition: background-color 0.5s ease, color 0.5s ease;
}}

/* The Diffused Background Glow */
.ambient-orb {{
    position: absolute;
    width: clamp(300px, 50vw, 800px);
    height: clamp(300px, 50vw, 800px);
    border-radius: 50%;
    background: var(--orb-gradient);
    filter: blur(120px);
    z-index: 0;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    transition: background 0.8s ease;
    pointer-events: none;
}}

/* Main Glass Foreground */
.glass-container {{
    position: relative;
    z-index: 1;
    width: {width_px}px;
    max-width: 95vw;
    height: {height_px}px;
    max-height: 95vh;
    background: var(--surface-bg);
    backdrop-filter: blur(40px);
    -webkit-backdrop-filter: blur(40px);
    border: 1px solid var(--border-color);
    border-radius: 32px;
    padding: 40px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    align-items: center;
    text-align: center;
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.15);
    transition: background 0.5s ease, border-color 0.5s ease;
}}

header {{
    margin-top: 20px;
}}

.title {{
    font-size: clamp(1.8rem, 4vw, 3rem);
    font-weight: 600;
    margin-bottom: 12px;
    letter-spacing: -0.02em;
}}

.body-text {{
    font-size: 1.1rem;
    opacity: 0.8;
    max-width: 600px;
    margin: 0 auto;
}}

.card-grid {{
    display: flex;
    gap: 24px;
    width: 100%;
    justify-content: center;
    flex-wrap: wrap;
    margin: 32px 0;
}}

.glass-card {{
    background: var(--card-bg);
    border: 1px solid var(--border-color);
    padding: 24px 32px;
    border-radius: 20px;
    flex: 1;
    min-width: 220px;
    max-width: 320px;
    box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.05);
    transition: background 0.5s ease, border-color 0.5s ease, transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    text-align: left;
    cursor: pointer;
}}

.glass-card:hover {{
    transform: translateY(-8px);
}}

.glass-card h3 {{
    font-size: 0.85rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    opacity: 0.7;
    margin-bottom: 8px;
    font-weight: 600;
}}

.glass-card p {{
    font-size: 1.25rem;
    font-weight: 500;
}}

/* Custom Toggle Switch */
.toggle-container {{
    display: flex;
    align-items: center;
    gap: 16px;
    background: var(--card-bg);
    padding: 12px 28px;
    border-radius: 50px;
    border: 1px solid var(--border-color);
    transition: background 0.5s ease, border-color 0.5s ease;
    margin-bottom: 20px;
}}

.toggle-label {{
    font-weight: 500;
    font-size: 1.05rem;
}}

.theme-switch {{
    display: inline-block;
    position: relative;
    cursor: pointer;
}}

.theme-switch-checkbox {{
    display: none;
}}

.theme-switch-track {{
    width: 56px;
    height: 30px;
    background-color: var(--switch-track);
    border-radius: 30px;
    position: relative;
    transition: background-color 0.4s ease;
}}

.theme-switch-thumb {{
    width: 24px;
    height: 24px;
    background-color: var(--switch-thumb);
    border-radius: 50%;
    position: absolute;
    top: 3px;
    left: 3px;
    transition: transform 0.4s cubic-bezier(0.4, 0, 0.2, 1), background-color 0.4s ease;
    box-shadow: 0 2px 5px rgba(0,0,0,0.2);
}}

.theme-switch-checkbox:checked ~ .theme-switch-track .theme-switch-thumb {{
    transform: translateX(26px);
}}
"""

    # Base Javascript logic
    js = f"""// Handles theme toggling
document.addEventListener('DOMContentLoaded', () => {{
    const themeToggle = document.getElementById('themeToggle');

    themeToggle.addEventListener('change', (e) => {{
        // When checked, set theme to dark, otherwise light
        if (e.target.checked) {{
            document.body.setAttribute('data-theme', 'dark');
        }} else {{
            document.body.setAttribute('data-theme', 'light');
        }}
    }});
}});
"""

    # Write the files
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
