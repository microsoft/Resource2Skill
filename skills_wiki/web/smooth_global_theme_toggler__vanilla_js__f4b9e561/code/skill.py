def create_component(
    output_dir: str,
    title_text: str = "Why Not Your Own Services?",
    body_text: str = "Start Your Self-Hosting Journey with us!",
    color_scheme: str = "light",       # "dark" or "light"
    accent_color: str = "#ec4899",     # Pink accent similar to the video
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Smooth Global Theme Toggler.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)
    
    # Pre-calculate boolean for the toggle input based on the requested scheme
    is_dark = "checked" if color_scheme == "dark" else ""
    body_class = 'class="dark"' if color_scheme == "dark" else ""

    # === CSS ===
    css = f"""/* Smooth Global Theme Toggler */
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

:root {{
    /* Light Theme Variables (Default) */
    --bg-base: #ffffff;
    --bg-surface: #f8f9fa;
    --text-main: #1a1a2e;
    --text-muted: #64748b;
    --border-color: #e2e8f0;
    --card-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
    
    --accent: {accent_color};
    --toggle-track: #cbd5e1;
    --toggle-thumb: #ffffff;
    
    --width: {width_px}px;
    --height: {height_px}px;
}}

body.dark {{
    /* Dark Theme Variables (Overrides) */
    --bg-base: #0a1111; 
    --bg-surface: #102121;
    --text-main: #f0fdfa;
    --text-muted: #5eead4;
    --border-color: #115e59;
    --card-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.3), 0 4px 6px -2px rgba(0, 0, 0, 0.15);
    
    --toggle-track: var(--accent);
    --toggle-thumb: #ffffff;
}}

*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: 'Poppins', system-ui, sans-serif;
    background-color: var(--bg-base);
    color: var(--text-main);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
    /* The magic of the smooth theme swap */
    transition: background-color 0.4s ease, color 0.4s ease;
}}

.app-container {{
    width: var(--width);
    height: var(--height);
    max-width: 100vw;
    max-height: 100vh;
    position: relative;
    padding: 2rem 4rem;
    display: flex;
    flex-direction: column;
}}

/* Navbar */
header {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding-bottom: 2rem;
}}

.logo {{
    font-weight: 700;
    font-size: 1.25rem;
    letter-spacing: -0.5px;
}}

.nav-controls {{
    display: flex;
    align-items: center;
    gap: 1.5rem;
}}

.theme-label {{
    font-size: 0.875rem;
    font-weight: 500;
}}

/* Toggle Switch CSS */
.switch {{
    position: relative;
    display: inline-block;
    width: 50px;
    height: 26px;
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
    background-color: var(--toggle-track);
    transition: background-color 0.4s ease;
    border-radius: 30px;
}}

.slider:before {{
    position: absolute;
    content: "";
    height: 20px;
    width: 20px;
    left: 3px;
    bottom: 3px;
    background-color: var(--toggle-thumb);
    border-radius: 50%;
    transition: transform 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    box-shadow: 0 2px 4px rgba(0,0,0,0.2);
}}

input:checked + .slider {{
    background-color: var(--toggle-track);
}}

input:checked + .slider:before {{
    transform: translateX(24px);
}}

input:focus-visible + .slider {{
    outline: 2px solid var(--accent);
    outline-offset: 2px;
}}

/* Hero Section */
.hero {{
    flex: 1;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;
    margin-bottom: 3rem;
}}

.hero h1 {{
    font-size: 3.5rem;
    font-weight: 600;
    margin-bottom: 1rem;
    letter-spacing: -1px;
}}

.hero p {{
    color: var(--text-muted);
    font-size: 1.125rem;
    max-width: 600px;
    transition: color 0.4s ease;
}}

/* Cards Section */
.cards-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 1.5rem;
    padding-bottom: 2rem;
}}

.card {{
    background-color: var(--bg-surface);
    border: 1px solid var(--border-color);
    border-radius: 16px;
    padding: 1.5rem;
    box-shadow: var(--card-shadow);
    transition: background-color 0.4s ease, border-color 0.4s ease, transform 0.3s ease, box-shadow 0.3s ease;
    cursor: pointer;
}}

.card:hover {{
    transform: translateY(-4px);
    box-shadow: 0 12px 20px -5px rgba(0, 0, 0, 0.1);
    border-color: var(--accent);
}}

.card-category {{
    font-size: 0.75rem;
    text-transform: uppercase;
    font-weight: 600;
    color: var(--text-muted);
    margin-bottom: 0.5rem;
    transition: color 0.4s ease;
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
    <link rel="stylesheet" href="style.css">
</head>
<body {body_class}>
    <div class="app-container">
        
        <!-- Header & Nav -->
        <header>
            <div class="logo">echoesofping</div>
            <div class="nav-controls">
                <span class="theme-label">Lights</span>
                <label class="switch" aria-label="Toggle Dark Mode">
                    <input type="checkbox" id="theme-toggle" {is_dark}>
                    <span class="slider"></span>
                </label>
            </div>
        </header>

        <!-- Hero Content -->
        <main class="hero">
            <h1>{title_text}</h1>
            <p>{body_text}</p>
        </main>

        <!-- Service Cards -->
        <section class="cards-grid">
            <div class="card">
                <div class="card-category">Installation Guide</div>
                <div class="card-title">Speedtest-Tracker</div>
            </div>
            <div class="card">
                <div class="card-category">Setup</div>
                <div class="card-title">Uptime-Kuma</div>
            </div>
            <div class="card">
                <div class="card-category">Playlist</div>
                <div class="card-title">HomeLab (Self-hosting)</div>
            </div>
        </section>

    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Smooth Global Theme Toggler Script
document.addEventListener('DOMContentLoaded', () => {{
    const themeToggle = document.getElementById('theme-toggle');

    // Sync input state with current body class (in case of dynamic template rendering)
    if (document.body.classList.contains('dark')) {{
        themeToggle.checked = true;
    }}

    // Listen for toggle changes
    themeToggle.addEventListener('change', (e) => {{
        if (e.target.checked) {{
            // Enable dark mode
            document.body.classList.add('dark');
        }} else {{
            // Revert to light mode
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
