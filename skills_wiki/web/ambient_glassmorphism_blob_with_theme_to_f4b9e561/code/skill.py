def create_component(
    output_dir: str,
    title_text: str = "Why not Your own Services?",
    body_text: str = "Start Your Self-Hosting Journey with us!",
    color_scheme: str = "light",        # "dark" or "light"
    accent_color: str = "#ec4899",      # Pink accent matching the video
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Ambient Glassmorphism Theme Toggle effect.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Determine initial state for the toggle based on python args
    is_dark = color_scheme.lower() == "dark"
    initial_theme = "dark" if is_dark else "light"
    checkbox_checked = "checked" if is_dark else ""

    # === CSS ===
    css = f"""/* Glassmorphism Ambient Blob Component */
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap');

:root {{
    /* Base Variables (Light Mode Default) */
    --bg-color: #f8f9fa;
    --text-main: #1e293b;
    --text-muted: #64748b;
    --surface-bg: rgba(255, 255, 255, 0.85);
    --surface-shadow: rgba(0, 0, 0, 0.05);
    --blob-gradient: linear-gradient(135deg, #fbc2eb 0%, #a6c1ee 100%);
    --accent: {accent_color};
    --toggle-bg: #cbd5e1;
    --width: {width_px}px;
    --height: {height_px}px;
}}

/* Dark Mode Variables Override */
[data-theme="dark"] {{
    --bg-color: #0f172a;
    --text-main: #f8f9fa;
    --text-muted: #94a3b8;
    --surface-bg: rgba(30, 41, 59, 0.75);
    --surface-shadow: rgba(0, 0, 0, 0.3);
    --blob-gradient: linear-gradient(135deg, #00cdac 0%, #02aab0 100%);
    --toggle-bg: #334155;
}}

*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: 'Poppins', sans-serif;
    background-color: var(--bg-color);
    color: var(--text-main);
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 100vh;
    overflow: hidden;
    transition: background-color 0.5s ease, color 0.5s ease;
}}

.app-container {{
    width: var(--width);
    height: var(--height);
    max-width: 100vw;
    max-height: 100vh;
    position: relative;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    overflow: hidden;
}}

/* The Ambient Blob */
.ambient-blob {{
    position: absolute;
    width: 400px;
    height: 400px;
    background: var(--blob-gradient);
    border-radius: 50%;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    filter: blur(120px);
    z-index: 1;
    opacity: 0.8;
    transition: background 0.5s ease;
    pointer-events: none;
}}

/* Foreground Content */
.content-wrapper {{
    position: relative;
    z-index: 10;
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
    gap: 3rem;
}}

.header h1 {{
    font-size: 2.5rem;
    font-weight: 600;
    margin-bottom: 0.5rem;
    letter-spacing: -0.02em;
}}

.header p {{
    font-size: 1rem;
    color: var(--text-muted);
    font-weight: 400;
}}

/* Navigation Pill */
.nav-pill {{
    display: flex;
    align-items: center;
    gap: 1.5rem;
    background: var(--surface-bg);
    padding: 0.75rem 1.5rem;
    border-radius: 3rem;
    box-shadow: 0 10px 30px var(--surface-shadow);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    transition: background-color 0.5s ease, box-shadow 0.5s ease;
}}

.nav-item {{
    text-decoration: none;
    color: var(--text-muted);
    font-weight: 500;
    font-size: 0.95rem;
    padding: 0.5rem 1rem;
    position: relative;
    transition: color 0.3s ease;
}}

.nav-item:hover {{
    color: var(--text-main);
}}

.nav-item.active {{
    color: var(--text-main);
}}

/* Active underline accent */
.nav-item.active::after {{
    content: '';
    position: absolute;
    bottom: 0;
    left: 50%;
    transform: translateX(-50%);
    width: 60%;
    height: 3px;
    background-color: var(--accent);
    border-radius: 2px;
}}

/* Toggle Switch Styles */
.theme-switch-wrapper {{
    display: flex;
    align-items: center;
    gap: 0.75rem;
    padding-left: 1.5rem;
    border-left: 1px solid var(--toggle-bg);
}}

.theme-switch-label {{
    font-weight: 500;
    font-size: 0.95rem;
    color: var(--text-main);
}}

.switch {{
    position: relative;
    display: inline-block;
    width: 46px;
    height: 24px;
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
    border-radius: 24px;
}}

.slider:before {{
    position: absolute;
    content: "";
    height: 18px;
    width: 18px;
    left: 3px;
    bottom: 3px;
    background-color: white;
    transition: .4s;
    border-radius: 50%;
    box-shadow: 0 2px 4px rgba(0,0,0,0.2);
}}

input:checked + .slider {{
    background-color: var(--accent);
}}

input:focus + .slider {{
    box-shadow: 0 0 1px var(--accent);
}}

input:checked + .slider:before {{
    transform: translateX(22px);
}}
"""

    # === HTML ===
    html = f"""<!DOCTYPE html>
<html lang="en" data-theme="{initial_theme}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text}</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="app-container">
        
        <!-- The blurred ambient background element -->
        <div class="ambient-blob"></div>

        <!-- The foreground UI -->
        <div class="content-wrapper">
            <header class="header">
                <h1>{title_text}</h1>
                <p>{body_text}</p>
            </header>

            <nav class="nav-pill">
                <a href="#" class="nav-item">Posts</a>
                <a href="#" class="nav-item">Blogs</a>
                <a href="#" class="nav-item active">Videos</a>
                
                <div class="theme-switch-wrapper">
                    <span class="theme-switch-label">Lights</span>
                    <label class="switch" aria-label="Toggle Dark Mode">
                        <input type="checkbox" id="themeToggle" {checkbox_checked}>
                        <span class="slider"></span>
                    </label>
                </div>
            </nav>
        </div>

    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Theme Toggle Logic
document.addEventListener('DOMContentLoaded', () => {{
    const themeToggle = document.getElementById('themeToggle');
    const htmlElement = document.documentElement;

    themeToggle.addEventListener('change', (event) => {{
        if (event.target.checked) {{
            // Switch to dark mode
            htmlElement.setAttribute('data-theme', 'dark');
        }} else {{
            // Switch to light mode
            htmlElement.setAttribute('data-theme', 'light');
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
