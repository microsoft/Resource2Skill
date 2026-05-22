def create_component(
    output_dir: str,
    title_text: str = "Why not Your own Services?",
    body_text: str = "Start Your Self-hosting Journey with us!",
    color_scheme: str = "light",       # "dark" or "light" (Default initial state)
    accent_color: str = "#8b5cf6",     # Primary accent color (purple)
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Glassmorphism Theme Toggle UI.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Determine initial checked state for the toggle based on color_scheme
    is_dark = color_scheme == "dark"
    body_class = ' class="dark"' if is_dark else ""
    checked_attr = "checked" if is_dark else ""

    # === CSS ===
    css = f"""/* Glassmorphism Theme Toggle UI */
:root {{
    /* Light Theme Variables */
    --bg-color: #f1f5f9;
    --text-color: #0f172a;
    --text-muted: #475569;
    --surface-bg: rgba(255, 255, 255, 0.6);
    --surface-border: rgba(255, 255, 255, 0.8);
    --shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.08);
    --blob-gradient: linear-gradient(135deg, #ff9a9e 0%, #fecfef 99%, #fecfef 100%);
    --toggle-bg: #e2e8f0;
    --toggle-knob: #ffffff;
    --accent-color: {accent_color};
    
    --container-width: {width_px}px;
    --container-height: {height_px}px;
}}

body.dark {{
    /* Dark Theme Variables */
    --bg-color: #0f172a;
    --text-color: #f8f9fa;
    --text-muted: #94a3b8;
    --surface-bg: rgba(30, 41, 59, 0.6);
    --surface-border: rgba(255, 255, 255, 0.1);
    --shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.3);
    --blob-gradient: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
    --toggle-bg: var(--accent-color);
    --toggle-knob: #ffffff;
}}

*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
    transition: background-color 0.4s ease, color 0.4s ease, border-color 0.4s ease, box-shadow 0.4s ease;
}}

body {{
    font-family: 'Poppins', system-ui, sans-serif;
    background-color: var(--bg-color);
    color: var(--text-color);
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
    overflow: hidden;
}}

.app-container {{
    width: var(--container-width);
    max-width: 100%;
    height: var(--container-height);
    position: relative;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 40px;
}}

/* Decorative Glow Blob */
.background-blob {{
    position: absolute;
    width: 600px;
    height: 600px;
    background: var(--blob-gradient);
    border-radius: 50%;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    filter: blur(80px);
    opacity: 0.7;
    z-index: 0;
    transition: background 0.6s ease;
}}

/* Foreground Content */
.content-wrapper {{
    position: relative;
    z-index: 10;
    width: 100%;
    max-width: 800px;
    display: flex;
    flex-direction: column;
    gap: 40px;
}}

/* Hero Section */
.hero-section {{
    text-align: center;
    margin-bottom: 20px;
}}

.hero-section h1 {{
    font-size: 3rem;
    font-weight: 700;
    margin-bottom: 16px;
    letter-spacing: -0.02em;
}}

.hero-section p {{
    font-size: 1.125rem;
    color: var(--text-muted);
}}

/* Control Bar (Tabs + Toggle) */
.control-bar {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    background: var(--surface-bg);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    border: 1px solid var(--surface-border);
    padding: 16px 32px;
    border-radius: 100px;
    box-shadow: var(--shadow);
}}

.tabs {{
    display: flex;
    gap: 32px;
    font-weight: 500;
    color: var(--text-muted);
}}

.tabs span {{
    cursor: pointer;
    transition: color 0.2s;
}}

.tabs span:hover {{
    color: var(--accent-color);
}}

.tabs span.active {{
    color: var(--text-color);
    border-bottom: 2px solid var(--accent-color);
    padding-bottom: 2px;
}}

.toggle-wrapper {{
    display: flex;
    align-items: center;
    gap: 12px;
    font-weight: 600;
}}

/* Custom Toggle Switch */
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
    transition: .4s cubic-bezier(0.4, 0.0, 0.2, 1);
    border-radius: 50%;
    box-shadow: 0 2px 4px rgba(0,0,0,0.2);
}}

input:checked + .slider {{
    background-color: var(--accent-color);
}}

input:checked + .slider:before {{
    transform: translateX(24px);
}}

/* Feature Cards Grid */
.cards-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
    gap: 24px;
}}

.card {{
    background: var(--surface-bg);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    border: 1px solid var(--surface-border);
    padding: 24px;
    border-radius: 16px;
    box-shadow: var(--shadow);
    cursor: pointer;
    transition: transform 0.3s ease, box-shadow 0.3s ease, border-color 0.3s ease;
}}

.card:hover {{
    transform: translateY(-4px);
    border-color: var(--accent-color);
    box-shadow: 0 20px 40px -10px rgba(0, 0, 0, 0.15);
}}

.card-category {{
    font-size: 0.8rem;
    text-transform: uppercase;
    font-weight: 600;
    letter-spacing: 0.05em;
    color: var(--text-muted);
    margin-bottom: 8px;
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
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body{body_class}>
    <div class="app-container">
        
        <!-- Decorative Glow Layer -->
        <div class="background-blob"></div>

        <!-- Main UI Layer -->
        <div class="content-wrapper">
            
            <div class="hero-section">
                <h1>{title_text}</h1>
                <p>{body_text}</p>
            </div>

            <div class="control-bar">
                <div class="tabs">
                    <span>Posts</span>
                    <span>Blogs</span>
                    <span class="active">Videos</span>
                </div>
                
                <div class="toggle-wrapper">
                    <span>Lights</span>
                    <label class="switch">
                        <input type="checkbox" id="theme-toggle" {checked_attr}>
                        <span class="slider"></span>
                    </label>
                </div>
            </div>

            <div class="cards-grid">
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
            </div>

        </div>
    </div>
    
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Glassmorphism Theme Toggle Logic
document.addEventListener('DOMContentLoaded', () => {{
    const themeToggle = document.getElementById('theme-toggle');
    
    // Listen for toggle switch changes
    themeToggle.addEventListener('change', function() {{
        if (this.checked) {{
            // Apply dark theme
            document.body.classList.add('dark');
        }} else {{
            // Remove dark theme, reverting to light
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
