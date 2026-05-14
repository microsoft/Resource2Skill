def create_component(
    output_dir: str,
    title_text: str = "Why not Your own Services?",
    body_text: str = "Start Your Self-hosting Journey with us!",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#a855f7",     # Purple accent matching the video vibe
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Animated Dark Mode Toggle switch.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Pre-calculate state based on initial color_scheme
    is_dark = color_scheme.lower() == "dark"
    body_class = ' class="dark-mode"' if is_dark else ""
    checked_attr = "checked" if is_dark else ""

    # === CSS ===
    css = f"""/* Animated Dark Mode Toggle — generated component */
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap');

*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    /* Light Theme Variables (Default) */
    --bg-color: #f8f9fa;
    --text-color: #1e293b;
    --text-muted: #64748b;
    --surface-color: #ffffff;
    --border-color: #e2e8f0;
    --toggle-bg: #cbd5e1;
    --toggle-thumb: #ffffff;
    
    --accent: {accent_color};
    --width: {width_px}px;
    --height: {height_px}px;
}}

/* Dark Theme Overrides */
body.dark-mode {{
    --bg-color: #0f172a;
    --text-color: #f8fafc;
    --text-muted: #94a3b8;
    --surface-color: #1e293b;
    --border-color: #334155;
    --toggle-bg: var(--accent);
    --toggle-thumb: #ffffff;
}}

body {{
    font-family: 'Poppins', sans-serif;
    background-color: var(--bg-color);
    color: var(--text-color);
    /* Smooth transition for theme switching */
    transition: background-color 0.4s ease, color 0.4s ease;
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
}}

.app-container {{
    width: 100%;
    max-width: var(--width);
    min-height: var(--height);
    padding: 2rem;
    position: relative;
    display: flex;
    flex-direction: column;
}}

/* --- Header & Toggle Layout --- */
.header {{
    display: flex;
    justify-content: flex-end;
    padding-bottom: 2rem;
}}

/* Toggle Switch Styles */
.theme-switch-wrapper {{
    display: flex;
    align-items: center;
    gap: 12px;
}}

.theme-switch-wrapper span {{
    font-weight: 600;
    font-size: 0.9rem;
    color: var(--text-color);
    transition: color 0.4s ease;
}}

.theme-switch {{
    position: relative;
    display: inline-block;
    width: 52px;
    height: 28px;
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
    transition: 0.4s ease-in-out;
    border-radius: 34px;
}}

.slider:before {{
    position: absolute;
    content: "";
    height: 20px;
    width: 20px;
    left: 4px;
    bottom: 4px;
    background-color: var(--toggle-thumb);
    transition: transform 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    border-radius: 50%;
    box-shadow: 0 2px 4px rgba(0,0,0,0.2);
}}

/* Active State Transform */
.theme-switch input:checked + .slider:before {{
    transform: translateX(24px);
}}

/* --- Hero & Content Styles (To match video context) --- */
.hero {{
    text-align: center;
    margin-top: 4rem;
    margin-bottom: 4rem;
}}

.hero h1 {{
    font-size: 3.5rem;
    font-weight: 700;
    margin-bottom: 1rem;
    color: var(--text-color);
    transition: color 0.4s ease;
}}

.hero p {{
    font-size: 1.25rem;
    color: var(--accent);
    font-weight: 600;
}}

.card-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 1.5rem;
    margin-top: 2rem;
}}

.card {{
    background-color: var(--surface-color);
    padding: 1.5rem;
    border-radius: 12px;
    border: 1px solid var(--border-color);
    transition: background-color 0.4s ease, border-color 0.4s ease, transform 0.2s ease;
    cursor: pointer;
}}

.card:hover {{
    transform: translateY(-4px);
}}

.card h3 {{
    font-size: 0.85rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: var(--text-muted);
    margin-bottom: 0.5rem;
}}

.card p {{
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
    <div class="app-container">
        
        <!-- Header with Dark Mode Toggle -->
        <header class="header">
            <label class="theme-switch-wrapper" for="checkbox" aria-label="Toggle dark mode">
                <span>Lights</span>
                <div class="theme-switch">
                    <input type="checkbox" id="checkbox" {checked_attr} />
                    <div class="slider"></div>
                </div>
            </label>
        </header>

        <!-- Contextual Hero Content -->
        <main>
            <section class="hero">
                <h1>{title_text}</h1>
                <p>{body_text}</p>
            </section>

            <div class="card-grid">
                <div class="card">
                    <h3>Installation Guide</h3>
                    <p>Speedtest-Tracker</p>
                </div>
                <div class="card">
                    <h3>Setup</h3>
                    <p>Uptime-Kuma</p>
                </div>
                <div class="card">
                    <h3>Playlist</h3>
                    <p>HomeLab(Self-hosting)</p>
                </div>
            </div>
        </main>

    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Animated Dark Mode Toggle — interactive behavior
document.addEventListener('DOMContentLoaded', () => {{
    const toggleSwitch = document.querySelector('.theme-switch input[type="checkbox"]');
    const currentTheme = document.body.classList.contains('dark-mode') ? 'dark' : 'light';

    // Listen for toggle interaction
    toggleSwitch.addEventListener('change', function(e) {{
        if (e.target.checked) {{
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
