def create_component(
    output_dir: str,
    title_text: str = "Why not Your own Services?",
    body_text: str = "Start Your Self-Hosting Journey with us!",
    color_scheme: str = "dark",       # "dark" or "light"
    accent_color: str = "#d946ef",    # Vivid pink/purple from the tutorial
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Glassmorphism Dark Mode Toggle effect.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Determine initial state for HTML markup
    body_class = ' class="dark-mode"' if color_scheme == "dark" else ""
    toggle_checked = "checked" if color_scheme == "dark" else ""

    # === CSS ===
    css = f"""/* Glassmorphism Dark Mode Toggle */
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap');

*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    /* Light Theme Variables */
    --bg-base: #f3f4f6;
    --text-main: #1f2937;
    --text-muted: #6b7280;
    --glass-bg: rgba(255, 255, 255, 0.6);
    --glass-border: rgba(255, 255, 255, 0.4);
    --card-bg: rgba(255, 255, 255, 0.8);
    --blob-a: #fbcfe8;
    --blob-b: #bfdbfe;
    --toggle-track: #d1d5db;
    --toggle-thumb: #ffffff;
    --accent: {accent_color};
    --border-divider: rgba(0, 0, 0, 0.05);
}}

body.dark-mode {{
    /* Dark Theme Variables */
    --bg-base: #030712;
    --text-main: #f9fafb;
    --text-muted: #9ca3af;
    --glass-bg: rgba(17, 24, 39, 0.6);
    --glass-border: rgba(255, 255, 255, 0.05);
    --card-bg: rgba(31, 41, 55, 0.8);
    --blob-a: #831843;
    --blob-b: #1e3a8a;
    --toggle-track: #374151;
    --toggle-thumb: #ffffff;
    --border-divider: rgba(255, 255, 255, 0.05);
}}

body {{
    font-family: 'Poppins', sans-serif;
    background-color: var(--bg-base);
    color: var(--text-main);
    transition: background-color 0.5s ease, color 0.5s ease;
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 100vh;
    overflow-x: hidden;
}}

.demo-viewport {{
    width: {width_px}px;
    height: {height_px}px;
    max-width: 100vw;
    max-height: 100vh;
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 2rem;
    overflow: hidden;
}}

/* Decorative Blobs */
.bg-shape {{
    position: absolute;
    border-radius: 50%;
    filter: blur(100px);
    z-index: -1;
    opacity: 0.8;
    transition: background-color 0.5s ease;
}}

.shape-1 {{
    top: 10%;
    left: 10%;
    width: 400px;
    height: 400px;
    background-color: var(--blob-a);
}}

.shape-2 {{
    bottom: 10%;
    right: 10%;
    width: 500px;
    height: 500px;
    background-color: var(--blob-b);
}}

/* Glass Container */
.app-container {{
    background: var(--glass-bg);
    backdrop-filter: blur(24px);
    -webkit-backdrop-filter: blur(24px);
    border: 1px solid var(--glass-border);
    border-radius: 24px;
    padding: 3rem;
    width: 100%;
    max-width: 900px;
    box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
    display: flex;
    flex-direction: column;
    gap: 3rem;
    transition: background-color 0.5s ease, border-color 0.5s ease;
}}

/* Header Typography */
.header {{
    text-align: center;
}}

.title {{
    font-size: 2.5rem;
    font-weight: 600;
    margin-bottom: 0.5rem;
}}

.subtitle {{
    font-size: 1rem;
    color: var(--text-muted);
    font-weight: 500;
    transition: color 0.5s ease;
}}

/* Navigation & Controls */
.controls-bar {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid var(--border-divider);
    padding-bottom: 1.5rem;
    flex-wrap: wrap;
    gap: 1.5rem;
    transition: border-color 0.5s ease;
}}

.tabs {{
    display: flex;
    list-style: none;
    gap: 2.5rem;
}}

.tabs li {{
    font-weight: 600;
    font-size: 1.1rem;
    color: var(--text-muted);
    cursor: pointer;
    position: relative;
    transition: color 0.3s ease;
}}

.tabs li:hover {{
    color: var(--text-main);
}}

.tabs li.active {{
    color: var(--accent);
}}

.tabs li.active::after {{
    content: '';
    position: absolute;
    bottom: -1.6rem;
    left: 0;
    width: 100%;
    height: 3px;
    background-color: var(--accent);
    border-radius: 3px 3px 0 0;
}}

/* Toggle Switch Component */
.toggle-wrapper {{
    display: flex;
    align-items: center;
    gap: 1rem;
    font-weight: 500;
}}

.theme-switch {{
    position: relative;
    display: inline-block;
    width: 56px;
    height: 30px;
}}

.theme-switch input {{
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
    background-color: var(--toggle-track);
    transition: 0.4s;
    border-radius: 30px;
}}

.slider:before {{
    position: absolute;
    content: "";
    height: 22px;
    width: 22px;
    left: 4px;
    bottom: 4px;
    background-color: var(--toggle-thumb);
    transition: 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    border-radius: 50%;
    box-shadow: 0 2px 4px rgba(0,0,0,0.2);
}}

input:checked + .slider {{
    background-color: var(--accent);
}}

input:checked + .slider:before {{
    transform: translateX(26px);
}}

/* Cards Grid */
.card-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 1.5rem;
}}

.card {{
    background: var(--card-bg);
    padding: 1.5rem;
    border-radius: 16px;
    border: 1px solid var(--glass-border);
    transition: background-color 0.5s ease, transform 0.2s ease;
}}

.card:hover {{
    transform: translateY(-2px);
}}

.card-label {{
    font-size: 0.85rem;
    font-weight: 600;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 0.05em;
    display: block;
    margin-bottom: 0.5rem;
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
    <title>Theme Toggle Pattern</title>
    <link rel="stylesheet" href="style.css">
</head>
<body{body_class}>
    <div class="demo-viewport">
        <!-- Ambient Background Shapes -->
        <div class="bg-shape shape-1"></div>
        <div class="bg-shape shape-2"></div>

        <!-- Main Glass Container -->
        <main class="app-container">
            <header class="header">
                <h1 class="title">{title_text}</h1>
                <p class="subtitle">{body_text}</p>
            </header>
            
            <nav class="controls-bar">
                <ul class="tabs">
                    <li>Posts</li>
                    <li>Blogs</li>
                    <li class="active">Videos</li>
                </ul>
                <div class="toggle-wrapper">
                    <span>Lights</span>
                    <label class="theme-switch" aria-label="Toggle Dark Mode">
                        <input type="checkbox" id="darkToggle" {toggle_checked}>
                        <span class="slider"></span>
                    </label>
                </div>
            </nav>

            <section class="card-grid">
                <article class="card">
                    <span class="card-label">Installation Guide</span>
                    <h3 class="card-title">Speedtest-Tracker</h3>
                </article>
                <article class="card">
                    <span class="card-label">Setup</span>
                    <h3 class="card-title">Uptime-Kuma</h3>
                </article>
                <article class="card">
                    <span class="card-label">Playlist</span>
                    <h3 class="card-title">HomeLab (Self-hosting)</h3>
                </article>
            </section>
        </main>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Select the toggle input
document.addEventListener('DOMContentLoaded', () => {{
    const themeToggle = document.getElementById('darkToggle');
    
    // Listen for changes on the checkbox
    themeToggle.addEventListener('change', (event) => {{
        if (event.target.checked) {{
            // Apply dark mode class to body
            document.body.classList.add('dark-mode');
        }} else {{
            // Remove dark mode class from body
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
