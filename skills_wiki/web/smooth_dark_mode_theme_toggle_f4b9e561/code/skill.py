def create_component(
    output_dir: str,
    title_text: str = "Why Not Your Own Services?",
    body_text: str = "Start Your Self-Hosting Journey with us! Toggle the switch to see the magic.",
    color_scheme: str = "light",  # "dark" or "light" sets initial state
    accent_color: str = "#d946ef", # Pink accent from the video
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Smooth Dark Mode Theme Toggle effect.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)
    
    # Determine initial states based on parameters
    initial_theme_attr = 'data-theme="dark"' if color_scheme == "dark" else ''
    checkbox_checked = 'checked' if color_scheme == "dark" else ''

    # === CSS ===
    css = f"""/* Theme Toggle Component */
:root {{
    /* Light Theme Variables (Default) */
    --bg-color: #f3f3f3;
    --surface-color: #ffffff;
    --text-primary: #1a1a1a;
    --text-secondary: #666666;
    --border-color: #e5e5e5;
    --accent-color: {accent_color};
    --toggle-bg: #e5e5e5;
    --toggle-thumb: #ffffff;
    
    /* Configurable dimensions */
    --container-width: {width_px}px;
    --container-height: {height_px}px;
    
    /* Transition settings */
    --theme-transition: background-color 0.4s ease, color 0.4s ease, border-color 0.4s ease, box-shadow 0.4s ease;
}}

/* Dark Theme Variables */
[data-theme="dark"] {{
    --bg-color: #0c1a1a;       /* Deep slate/teal from video */
    --surface-color: #112222;  /* Slightly lighter surface */
    --text-primary: #ddf9f8;   /* Soft cyan text */
    --text-secondary: #8ab4b2;
    --border-color: #1f3a3a;
    --toggle-bg: var(--accent-color);
    --toggle-thumb: #ffffff;
}}

*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: 'Poppins', system-ui, -apple-system, sans-serif;
    background-color: var(--bg-color);
    color: var(--text-primary);
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 100vh;
    /* Apply transition globally to body */
    transition: var(--theme-transition);
}}

/* Container to restrict size based on params */
.wrapper {{
    width: 100%;
    max-width: var(--container-width);
    min-height: var(--container-height);
    padding: 40px;
    display: flex;
    flex-direction: column;
    position: relative;
}}

/* Header Area */
header {{
    text-align: center;
    margin-top: 10vh;
    margin-bottom: 60px;
    /* Elements inside also need the transition */
    transition: var(--theme-transition);
}}

h1 {{
    font-size: 3.5rem;
    font-weight: 600;
    margin-bottom: 16px;
    transition: var(--theme-transition);
}}

p.subtitle {{
    font-size: 1.2rem;
    color: var(--text-secondary);
    transition: var(--theme-transition);
}}

/* Toolbar (containing toggle) */
.toolbar {{
    display: flex;
    justify-content: flex-end;
    align-items: center;
    gap: 16px;
    margin-bottom: 40px;
    padding-bottom: 20px;
    border-bottom: 2px solid var(--border-color);
    transition: var(--theme-transition);
}}

.toolbar-label {{
    font-weight: 500;
    font-size: 1rem;
}}

/* Toggle Switch Styles */
.theme-switch {{
    position: relative;
    display: inline-block;
    width: 60px;
    height: 32px;
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
    background-color: var(--toggle-bg);
    border-radius: 32px;
    transition: .4s;
}}

.slider:before {{
    position: absolute;
    content: "";
    height: 24px;
    width: 24px;
    left: 4px;
    bottom: 4px;
    background-color: var(--toggle-thumb);
    border-radius: 50%;
    transition: transform .4s cubic-bezier(0.4, 0.0, 0.2, 1);
    box-shadow: 0 2px 4px rgba(0,0,0,0.2);
}}

/* Move thumb when checked */
input:checked + .slider:before {{
    transform: translateX(28px);
}}

/* Content Grid to demonstrate theming */
.grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 24px;
}}

.card {{
    background-color: var(--surface-color);
    padding: 32px;
    border-radius: 16px;
    border: 2px solid var(--border-color);
    transition: var(--theme-transition);
}}

.card-tag {{
    font-size: 0.85rem;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: var(--accent-color);
    font-weight: 600;
    margin-bottom: 12px;
    display: block;
}}

.card h3 {{
    font-size: 1.5rem;
    margin-bottom: 8px;
}}
"""

    # === HTML ===
    html = f"""<!DOCTYPE html>
<html lang="en" {initial_theme_attr}>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="wrapper">
        
        <header>
            <h1>{title_text}</h1>
            <p class="subtitle">{body_text}</p>
        </header>

        <div class="toolbar">
            <span class="toolbar-label">Lights</span>
            <label class="theme-switch" for="theme-toggle">
                <input type="checkbox" id="theme-toggle" {checkbox_checked}>
                <span class="slider"></span>
            </label>
        </div>

        <div class="grid">
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
        </div>

    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Smooth Dark Mode Theme Toggle Logic
document.addEventListener('DOMContentLoaded', () => {{
    const toggleSwitch = document.getElementById('theme-toggle');
    const rootElement = document.documentElement;

    // Listen for changes on the checkbox
    toggleSwitch.addEventListener('change', function(e) {{
        if (e.target.checked) {{
            // Switch to Dark Mode
            rootElement.setAttribute('data-theme', 'dark');
        }} else {{
            // Switch to Light Mode (remove attribute to use root defaults)
            rootElement.removeAttribute('data-theme');
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
