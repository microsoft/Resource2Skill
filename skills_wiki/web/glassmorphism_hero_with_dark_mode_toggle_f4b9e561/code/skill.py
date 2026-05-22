def create_component(
    output_dir: str,
    title_text: str = "Why not Your own Services?",
    body_text: str = "Start Your Self-Hosting Journey with us!",
    color_scheme: str = "light",
    accent_color: str = "#fa39ad",
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Glassmorphism Hero with Dark Mode Toggle.
    
    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Secondary gradient color derived for the blob
    gradient_secondary = "#ff6c4c"
    
    # Determine initial theme state for the toggle
    is_dark = color_scheme == "dark"
    theme_attr = 'data-theme="dark"' if is_dark else ''
    checkbox_checked = 'checked' if is_dark else ''

    # === CSS ===
    css = f"""/* Glassmorphism Hero with Theme Toggle */
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

:root {{
    /* Light Theme Defaults */
    --bg-base: #f4f5f7;
    --text-main: #111827;
    --text-muted: #6b7280;
    --glass-bg: rgba(255, 255, 255, 0.5);
    --glass-border: rgba(255, 255, 255, 0.4);
    --card-bg: rgba(255, 255, 255, 0.7);
    --card-hover-border: rgba(17, 24, 39, 0.2);
    --card-shadow: rgba(0, 0, 0, 0.05);
    
    /* Accent Variables */
    --accent-primary: {accent_color};
    --accent-secondary: {gradient_secondary};
}}

[data-theme="dark"] {{
    /* Dark Theme Overrides */
    --bg-base: #0f172a;
    --text-main: #f9fafb;
    --text-muted: #9ca3af;
    --glass-bg: rgba(15, 23, 42, 0.6);
    --glass-border: rgba(255, 255, 255, 0.08);
    --card-bg: rgba(30, 41, 59, 0.5);
    --card-hover-border: rgba(255, 255, 255, 0.2);
    --card-shadow: rgba(0, 0, 0, 0.2);
}}

*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: 'Poppins', sans-serif;
    background-color: var(--bg-base);
    color: var(--text-main);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: background-color 0.4s ease, color 0.4s ease;
    overflow-x: hidden;
}}

.viewport {{
    width: 100%;
    max-width: {width_px}px;
    min-height: {height_px}px;
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 2rem;
}}

/* The Vibrant Background Blob */
.gradient-blob {{
    position: absolute;
    width: 500px;
    height: 500px;
    background: linear-gradient(135deg, var(--accent-primary) 0%, var(--accent-secondary) 100%);
    border-radius: 50%;
    filter: blur(120px);
    z-index: 0;
    opacity: 0.8;
    pointer-events: none;
}}

/* Main Glassmorphism Container */
.glass-panel {{
    position: relative;
    z-index: 1;
    width: 100%;
    background: var(--glass-bg);
    backdrop-filter: blur(30px);
    -webkit-backdrop-filter: blur(30px);
    border: 1px solid var(--glass-border);
    border-radius: 24px;
    padding: 3rem;
    box-shadow: 0 25px 50px -12px var(--card-shadow);
    display: flex;
    flex-direction: column;
    gap: 4rem;
    transition: background-color 0.4s ease, border-color 0.4s ease;
}}

/* Header & Toggle Area */
.panel-header {{
    display: flex;
    justify-content: space-between;
    align-items: center;
}}

.logo-dots {{
    display: flex;
    gap: 8px;
}}

.dot {{
    width: 12px;
    height: 12px;
    border-radius: 50%;
}}
.dot.red {{ background-color: #ef4444; }}
.dot.yellow {{ background-color: #f59e0b; }}
.dot.green {{ background-color: #10b981; }}

.theme-controls {{
    display: flex;
    align-items: center;
    gap: 12px;
    font-weight: 500;
    font-size: 0.9rem;
}}

/* Custom Toggle Switch */
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
    background-color: #cbd5e1;
    transition: 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    border-radius: 26px;
}}

.slider:before {{
    position: absolute;
    content: "";
    height: 18px;
    width: 18px;
    left: 4px;
    bottom: 4px;
    background-color: white;
    transition: 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    border-radius: 50%;
    box-shadow: 0 2px 4px rgba(0,0,0,0.2);
}}

input:checked + .slider {{
    background-color: var(--accent-primary);
}}

input:checked + .slider:before {{
    transform: translateX(24px);
}}

[data-theme="dark"] .slider {{
    background-color: #475569;
}}
[data-theme="dark"] input:checked + .slider {{
    background-color: var(--accent-primary);
}}

/* Hero Section */
.hero-content {{
    text-align: center;
    max-width: 800px;
    margin: 0 auto;
}}

.hero-content h1 {{
    font-size: 3.5rem;
    font-weight: 700;
    line-height: 1.2;
    margin-bottom: 1rem;
    letter-spacing: -0.02em;
}}

.hero-content p {{
    font-size: 1.25rem;
    color: var(--text-muted);
    font-weight: 400;
}}

/* Cards Section */
.cards-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 1.5rem;
}}

.card {{
    background: var(--card-bg);
    border: 1px solid var(--glass-border);
    border-radius: 16px;
    padding: 1.5rem;
    transition: all 0.3s ease;
    cursor: pointer;
}}

.card:hover {{
    transform: translateY(-4px);
    border-color: var(--card-hover-border);
    box-shadow: 0 10px 25px -5px var(--card-shadow);
}}

.card-label {{
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: var(--text-muted);
    font-weight: 600;
    margin-bottom: 0.5rem;
    display: block;
}}

.card-title {{
    font-size: 1.1rem;
    font-weight: 600;
}}

/* Responsive Adjustments */
@media (max-width: 768px) {{
    .hero-content h1 {{
        font-size: 2.5rem;
    }}
    .glass-panel {{
        padding: 2rem;
    }}
}}
"""

    # === HTML ===
    html = f"""<!DOCTYPE html>
<html lang="en" {theme_attr}>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text}</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    
    <div class="viewport">
        <!-- Blurred Background Blob -->
        <div class="gradient-blob"></div>

        <!-- Foreground Glassmorphism Panel -->
        <main class="glass-panel">
            
            <!-- Header -->
            <header class="panel-header">
                <div class="logo-dots">
                    <div class="dot red"></div>
                    <div class="dot yellow"></div>
                    <div class="dot green"></div>
                </div>
                
                <div class="theme-controls">
                    <span>Lights</span>
                    <label class="switch">
                        <input type="checkbox" id="themeToggle" {checkbox_checked}>
                        <span class="slider"></span>
                    </label>
                </div>
            </header>

            <!-- Hero Copy -->
            <section class="hero-content">
                <h1>{title_text}</h1>
                <p>{body_text}</p>
            </section>

            <!-- Interactive Cards -->
            <section class="cards-grid">
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
                    <h3 class="card-title">HomeLab (Self-Hosting)</h3>
                </article>
            </section>

        </main>
    </div>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Theme Toggle Logic
document.addEventListener('DOMContentLoaded', () => {{
    const themeToggle = document.getElementById('themeToggle');
    const htmlElement = document.documentElement;

    themeToggle.addEventListener('change', (e) => {{
        if (e.target.checked) {{
            htmlElement.setAttribute('data-theme', 'dark');
        }} else {{
            htmlElement.removeAttribute('data-theme');
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
