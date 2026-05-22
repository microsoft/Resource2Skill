def create_component(
    output_dir: str,
    title_text: str = "Why not Your own Services?",
    body_text: str = "Start Your Self-Hosting Journey with us! Toggle the lights to see the magic.",
    color_scheme: str = "light",       # "dark" or "light"
    accent_color: str = "#8b5cf6",     # CSS hex color for accent (e.g., purple)
    width_px: int = 1000,
    height_px: int = 700,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Dynamic Theme Toggle & Glassmorphism UI.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Determine initial states based on parameter
    is_dark = color_scheme.lower() == "dark"
    body_class = ' class="dark-mode"' if is_dark else ''
    checked_attr = 'checked' if is_dark else ''

    # === CSS ===
    css = f"""/* Theme Toggle & Glassmorphism UI */
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap');

:root {{
    /* Light Theme Variables */
    --bg-base: #f1f5f9;
    --bg-surface: rgba(255, 255, 255, 0.6);
    --bg-surface-hover: rgba(255, 255, 255, 0.9);
    --text-main: #0f172a;
    --text-muted: #64748b;
    --border-color: rgba(255, 255, 255, 0.5);
    
    /* Toggle Specifics */
    --toggle-track: #cbd5e1;
    --toggle-thumb: #ffffff;
    --toggle-accent: {accent_color};
    
    /* Ambient Glows */
    --glow-1: rgba(139, 92, 246, 0.4);
    --glow-2: rgba(236, 72, 153, 0.3);
    
    --app-width: {width_px}px;
    --app-height: {height_px}px;
}}

body.dark-mode {{
    /* Dark Theme Variables */
    --bg-base: #020617;
    --bg-surface: rgba(30, 41, 59, 0.6);
    --bg-surface-hover: rgba(30, 41, 59, 0.9);
    --text-main: #f8f9fa;
    --text-muted: #94a3b8;
    --border-color: rgba(255, 255, 255, 0.1);
    
    /* Toggle Specifics */
    --toggle-track: #334155;
    --toggle-thumb: #0f172a;
    --toggle-accent: {accent_color};
    
    /* Ambient Glows */
    --glow-1: rgba(139, 92, 246, 0.15);
    --glow-2: rgba(16, 185, 129, 0.15);
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
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 100vh;
    overflow: hidden;
    /* Smooth global theme transition */
    transition: background-color 0.5s ease, color 0.5s ease;
}}

/* Ambient Background Orbs */
.ambient-bg {{
    position: fixed;
    top: 0; left: 0; right: 0; bottom: 0;
    z-index: -1;
    overflow: hidden;
    pointer-events: none;
}}
.ambient-bg::before, .ambient-bg::after {{
    content: '';
    position: absolute;
    border-radius: 50%;
    filter: blur(80px);
    transition: background 0.5s ease;
}}
.ambient-bg::before {{
    width: 60vw; height: 60vw;
    background: var(--glow-1);
    top: -20%; left: -10%;
}}
.ambient-bg::after {{
    width: 50vw; height: 50vw;
    background: var(--glow-2);
    bottom: -10%; right: -10%;
}}

.app-container {{
    width: 100%;
    max-width: var(--app-width);
    min-height: var(--app-height);
    padding: 2rem;
    display: flex;
    flex-direction: column;
    gap: 3rem;
}}

/* Header & Navigation */
header {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1.5rem 2rem;
    background: var(--bg-surface);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    border: 1px solid var(--border-color);
    border-radius: 100px;
    transition: all 0.4s ease;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
}}

.nav-links {{
    display: flex;
    gap: 2rem;
    font-weight: 500;
}}

/* The Toggle Switch UI */
.theme-toggle-wrapper {{
    display: flex;
    align-items: center;
    gap: 1rem;
    font-weight: 500;
    font-size: 0.95rem;
}}

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
    background-color: var(--toggle-track);
    transition: .4s cubic-bezier(0.4, 0.0, 0.2, 1);
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
    transition: .4s cubic-bezier(0.4, 0.0, 0.2, 1);
    border-radius: 50%;
    box-shadow: 0 2px 4px rgba(0,0,0,0.2);
}}

input:checked + .slider {{
    background-color: var(--toggle-accent);
}}

input:focus + .slider {{
    box-shadow: 0 0 0 2px rgba(139, 92, 246, 0.4);
}}

input:checked + .slider:before {{
    transform: translateX(24px);
}}

/* Hero Section */
.hero {{
    text-align: center;
    margin-top: 2rem;
}}

.hero h1 {{
    font-size: 3.5rem;
    font-weight: 700;
    margin-bottom: 1rem;
    letter-spacing: -0.05em;
}}

.hero p {{
    color: var(--text-muted);
    font-size: 1.1rem;
    max-width: 600px;
    margin: 0 auto;
    transition: color 0.4s ease;
}}

/* Glassmorphism Cards Grid */
.card-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 1.5rem;
    margin-top: 2rem;
}}

.glass-card {{
    background: var(--bg-surface);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border: 1px solid var(--border-color);
    padding: 2rem;
    border-radius: 24px;
    transition: all 0.4s ease;
    box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.05), 0 4px 6px -2px rgba(0, 0, 0, 0.02);
}}

.glass-card:hover {{
    transform: translateY(-5px);
    background: var(--bg-surface-hover);
    box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
}}

.glass-card h3 {{
    font-size: 1.25rem;
    margin-bottom: 0.5rem;
}}

.glass-card p {{
    color: var(--text-muted);
    font-size: 0.95rem;
}}

@media (max-width: 768px) {{
    header {{
        flex-direction: column;
        gap: 1.5rem;
        border-radius: 24px;
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
<body{body_class}>
    <div class="ambient-bg"></div>
    
    <div class="app-container">
        <!-- Header & Nav -->
        <header>
            <div class="logo"><strong>Echoes</strong>UI</div>
            <nav class="nav-links">
                <div>Posts</div>
                <div>Blogs</div>
                <div>Videos</div>
            </nav>
            
            <!-- Dark Mode Toggle -->
            <div class="theme-toggle-wrapper">
                <span id="theme-label">Lights</span>
                <label class="switch" aria-label="Toggle Dark Mode">
                    <input type="checkbox" id="themeToggle" {checked_attr}>
                    <span class="slider"></span>
                </label>
            </div>
        </header>

        <!-- Main Content -->
        <main>
            <section class="hero">
                <h1>{title_text}</h1>
                <p>{body_text}</p>
            </section>

            <section class="card-grid">
                <div class="glass-card">
                    <h3>Speedtest-Tracker</h3>
                    <p>Installation Guide & Setup Instructions</p>
                </div>
                <div class="glass-card">
                    <h3>Uptime-Kuma</h3>
                    <p>Setup your monitoring dashboard seamlessly.</p>
                </div>
                <div class="glass-card">
                    <h3>HomeLab</h3>
                    <p>Playlist covering self-hosting best practices.</p>
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
    const themeLabel = document.getElementById('theme-label');
    
    // Set initial label text based on initial state
    updateLabel(themeToggle.checked);

    themeToggle.addEventListener('change', (e) => {{
        const isDark = e.target.checked;
        
        // Toggle the class on the body to drive CSS variable changes
        if (isDark) {{
            document.body.classList.add('dark-mode');
        }} else {{
            document.body.classList.remove('dark-mode');
        }}
        
        updateLabel(isDark);
    }});
    
    function updateLabel(isDark) {{
        // Optional: you can change the text entirely, e.g. "Dark Mode" vs "Light Mode"
        // Here we stick to "Lights" to match the tutorial's aesthetic, but you could expand it.
    }}
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
