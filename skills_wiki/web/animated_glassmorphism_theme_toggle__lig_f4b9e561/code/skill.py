def create_component(
    output_dir: str,
    title_text: str = "Why not Your own Services?",
    body_text: str = "Start Your Self-hosting Journey with us!",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#0ea5e9",     # Teal/Cyan accent from the tutorial
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Animated Glassmorphism Theme Toggle.
    
    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Validate and process color scheme
    is_dark = "checked" if color_scheme == "dark" else ""
    body_class = "dark-mode" if color_scheme == "dark" else ""

    # === CSS ===
    css = f"""/* Animated Glassmorphism Theme Toggle — generated component */
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

:root {{
    /* Light Theme Variables (Default) */
    --bg-base: #f8fafc;
    --text-main: #0f172a;
    --text-muted: #64748b;
    --surface-bg: rgba(255, 255, 255, 0.6);
    --surface-border: rgba(255, 255, 255, 0.4);
    
    --blob-color: rgba(236, 72, 153, 0.25); /* Pinkish blob */
    
    --switch-bg: #cbd5e1;
    --switch-indicator: #ffffff;
    
    --width: {width_px}px;
    --height: {height_px}px;
}}

/* Dark Theme Variables */
body.dark-mode {{
    --bg-base: #020617;
    --text-main: #f8fafc;
    --text-muted: #94a3b8;
    --surface-bg: rgba(30, 41, 59, 0.6);
    --surface-border: rgba(255, 255, 255, 0.08);
    
    --blob-color: {accent_color}33; /* 33 is approx 20% opacity for hex */
    
    --switch-bg: #334155;
    --switch-indicator: {accent_color};
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
    justify-content: center;
    align-items: center;
    overflow-x: hidden;
    position: relative;
    /* Smooth global transition for theme swap */
    transition: background-color 0.5s ease, color 0.5s ease;
}}

/* Ambient Background Blob */
.ambient-blob {{
    position: absolute;
    bottom: -10%;
    left: 50%;
    transform: translateX(-50%);
    width: 60vw;
    height: 40vh;
    background-color: var(--blob-color);
    filter: blur(120px);
    border-radius: 50%;
    z-index: -1;
    pointer-events: none;
    transition: background-color 0.8s ease;
}}

/* Application Container */
.app-container {{
    width: 100%;
    max-width: var(--width);
    min-height: var(--height);
    padding: 2rem 4rem;
    display: flex;
    flex-direction: column;
    z-index: 1;
}}

/* Header & Navigation */
.header {{
    display: flex;
    justify-content: flex-end;
    align-items: center;
    padding: 1rem 0;
    margin-bottom: 4rem;
}}

/* Theme Toggle Switch */
.theme-switch-wrapper {{
    display: flex;
    align-items: center;
    gap: 1rem;
}}

.theme-switch-label-text {{
    font-size: 0.9rem;
    font-weight: 500;
    color: var(--text-main);
    transition: color 0.5s ease;
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
    background-color: var(--switch-bg);
    transition: 0.4s ease;
    border-radius: 34px;
}}

.slider::before {{
    position: absolute;
    content: "";
    height: 20px;
    width: 20px;
    left: 4px;
    bottom: 4px;
    background-color: var(--switch-indicator);
    transition: transform 0.4s cubic-bezier(0.4, 0, 0.2, 1), background-color 0.4s ease;
    border-radius: 50%;
    box-shadow: 0 2px 4px rgba(0,0,0,0.2);
}}

input:checked + .slider::before {{
    transform: translateX(24px);
}}

/* Hero Section */
.hero {{
    text-align: center;
    margin-bottom: 4rem;
}}

.hero h1 {{
    font-size: 3.5rem;
    font-weight: 600;
    letter-spacing: -0.02em;
    margin-bottom: 0.5rem;
}}

.hero p {{
    font-size: 1.1rem;
    color: var(--text-muted);
    font-weight: 400;
}}

/* Glassmorphism Cards */
.card-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 1.5rem;
}}

.glass-card {{
    background: var(--surface-bg);
    border: 1px solid var(--surface-border);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    border-radius: 1rem;
    padding: 2rem;
    transition: all 0.4s ease;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
}}

.glass-card:hover {{
    transform: translateY(-4px);
    box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
}}

.card-label {{
    font-size: 0.8rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: var(--text-muted);
    margin-bottom: 0.5rem;
    display: block;
}}

.card-title {{
    font-size: 1.25rem;
    font-weight: 600;
    color: var(--text-main);
}}

/* Responsive adjustments */
@media (max-width: 768px) {{
    .app-container {{
        padding: 1.5rem;
    }}
    .hero h1 {{
        font-size: 2.5rem;
    }}
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
<body class="{body_class}">
    <!-- Ambient glowing blob background -->
    <div class="ambient-blob"></div>

    <div class="app-container">
        <!-- Header with Toggle -->
        <header class="header">
            <div class="theme-switch-wrapper">
                <span class="theme-switch-label-text">Lights</span>
                <label class="theme-switch" for="themeToggle">
                    <input type="checkbox" id="themeToggle" {is_dark} aria-label="Toggle Dark Mode" />
                    <span class="slider"></span>
                </label>
            </div>
        </header>

        <!-- Main Hero Content -->
        <main>
            <section class="hero">
                <h1>{title_text}</h1>
                <p>{body_text}</p>
            </section>

            <!-- Sample UI to demonstrate glassmorphism adaptation -->
            <section class="card-grid">
                <div class="glass-card">
                    <span class="card-label">Installation Guide</span>
                    <h2 class="card-title">Speedtest-Tracker</h2>
                </div>
                <div class="glass-card">
                    <span class="card-label">Setup</span>
                    <h2 class="card-title">Uptime-Kuma</h2>
                </div>
                <div class="glass-card">
                    <span class="card-label">Playlist</span>
                    <h2 class="card-title">HomeLab (Self-hosting)</h2>
                </div>
            </section>
        </main>
    </div>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = """// Animated Glassmorphism Theme Toggle — interactive behavior
document.addEventListener('DOMContentLoaded', () => {
    const themeToggle = document.getElementById('themeToggle');
    
    // Listen for toggle switches
    themeToggle.addEventListener('change', (e) => {
        if (e.target.checked) {
            document.body.classList.add('dark-mode');
        } else {
            document.body.classList.remove('dark-mode');
        }
    });
});
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
