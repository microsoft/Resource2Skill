def create_component(
    output_dir: str,
    title_text: str = "Why not Your own Services?",
    body_text: str = "Start Your Self-Hosting Journey with us!",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#10b981",     # Default to a nice teal/green like the video's dark mode
    width_px: int = 1000,
    height_px: int = 700,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Ambient Glassmorphism Theme Toggle.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # We use a complementary color for the light mode ambient glow to mimic the video's pink -> green shift.
    light_ambient = "#f472b6" # Soft pink

    # === CSS ===
    css = f"""/* Ambient Glassmorphism Theme Toggle */
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap');

*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

/* Theme Variable Definitions */
:root[data-theme="light"] {{
    --bg-color: #f8f9fa;
    --text-color: #0f172a;
    --text-muted: #64748b;
    --surface-bg: rgba(255, 255, 255, 0.7);
    --surface-border: rgba(0, 0, 0, 0.05);
    --ambient-color: {light_ambient};
    --toggle-bg: #cbd5e1;
    --toggle-knob: #ffffff;
}}

:root[data-theme="dark"] {{
    --bg-color: #0d111c;
    --text-color: #f8fafc;
    --text-muted: #94a3b8;
    --surface-bg: rgba(255, 255, 255, 0.03);
    --surface-border: rgba(255, 255, 255, 0.08);
    --ambient-color: {accent_color};
    --toggle-bg: {accent_color};
    --toggle-knob: #ffffff;
}}

body {{
    font-family: 'Poppins', system-ui, sans-serif;
    background-color: var(--bg-color);
    color: var(--text-color);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow-x: hidden;
    /* The core smooth transition for the whole theme */
    transition: background-color 0.5s ease, color 0.5s ease;
}}

.app-container {{
    width: 100%;
    max-width: {width_px}px;
    min-height: {height_px}px;
    position: relative;
    display: flex;
    flex-direction: column;
    padding: 40px;
    z-index: 1;
}}

/* Ambient Glowing Orb */
.ambient-glow {{
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: 600px;
    height: 400px;
    background: var(--ambient-color);
    filter: blur(120px);
    border-radius: 50%;
    opacity: 0.35;
    z-index: -1;
    transition: background 0.6s ease, opacity 0.6s ease;
    pointer-events: none;
}}

/* Header & Toggle */
header {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 80px;
}}

.logo-placeholder {{
    font-weight: 700;
    font-size: 1.25rem;
    letter-spacing: -0.5px;
}}

.toggle-wrapper {{
    display: flex;
    align-items: center;
    gap: 12px;
    font-size: 0.9rem;
    font-weight: 500;
}}

/* Custom Checkbox Switch */
.switch {{
    position: relative;
    display: inline-block;
    width: 48px;
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
    background-color: var(--toggle-bg);
    transition: .4s;
    border-radius: 34px;
}}

.slider:before {{
    position: absolute;
    content: "";
    height: 18px;
    width: 18px;
    left: 4px;
    bottom: 4px;
    background-color: var(--toggle-knob);
    transition: .4s cubic-bezier(0.4, 0.0, 0.2, 1);
    border-radius: 50%;
}}

input:checked + .slider:before {{
    transform: translateX(22px);
}}

/* Main Content */
.hero {{
    text-align: center;
    margin-bottom: 60px;
}}

.hero h1 {{
    font-size: 3.5rem;
    font-weight: 600;
    margin-bottom: 12px;
    letter-spacing: -1px;
}}

.hero p {{
    font-size: 1.1rem;
    color: var(--text-muted);
    transition: color 0.5s ease;
}}

/* Glassmorphic Grid */
.grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 24px;
    width: 100%;
}}

.card {{
    background: var(--surface-bg);
    border: 1px solid var(--surface-border);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    border-radius: 16px;
    padding: 32px;
    display: flex;
    flex-direction: column;
    gap: 12px;
    transition: background 0.5s ease, border-color 0.5s ease, transform 0.3s ease, box-shadow 0.3s ease;
    cursor: pointer;
}}

.card:hover {{
    transform: translateY(-4px);
    box-shadow: 0 12px 24px rgba(0,0,0,0.1);
}}

.card-tag {{
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: var(--ambient-color);
    transition: color 0.5s ease;
}}

.card h3 {{
    font-size: 1.25rem;
    font-weight: 600;
}}

/* Responsive adjustments */
@media (max-width: 768px) {{
    .hero h1 {{ font-size: 2.5rem; }}
    .app-container {{ padding: 20px; }}
}}
"""

    # === HTML ===
    html = f"""<!DOCTYPE html>
<html lang="en" data-theme="{color_scheme}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text}</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="ambient-glow"></div>
    
    <div class="app-container">
        <header>
            <div class="logo-placeholder">Echoes of Ping</div>
            <div class="toggle-wrapper">
                <span>Lights</span>
                <label class="switch">
                    <!-- The JS will ensure this matches the initial data-theme -->
                    <input type="checkbox" id="themeToggle">
                    <span class="slider"></span>
                </label>
            </div>
        </header>

        <main>
            <section class="hero">
                <h1>{title_text}</h1>
                <p>{body_text}</p>
            </section>

            <section class="grid">
                <div class="card">
                    <span class="card-tag">Installation Guide</span>
                    <h3>Speedtest-Tracker</h3>
                </div>
                <div class="card">
                    <span class="card-tag">Setup</span>
                    <h3>Uptime-Kuma</h3>
                </div>
                <div class="card">
                    <span class="card-tag">Playlist</span>
                    <h3>HomeLab (Self-hosting)</h3>
                </div>
            </section>
        </main>
    </div>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""document.addEventListener('DOMContentLoaded', () => {{
    const themeToggle = document.getElementById('themeToggle');
    const htmlElement = document.documentElement;
    
    // Set initial toggle state based on the HTML data attribute
    // In this UI logic: "Lights" ON (checked) = Light Theme, OFF (unchecked) = Dark Theme
    const isLightMode = htmlElement.getAttribute('data-theme') === 'light';
    themeToggle.checked = isLightMode;

    themeToggle.addEventListener('change', (e) => {{
        if (e.target.checked) {{
            htmlElement.setAttribute('data-theme', 'light');
        }} else {{
            htmlElement.setAttribute('data-theme', 'dark');
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
