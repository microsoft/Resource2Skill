def create_component(
    output_dir: str,
    title_text: str = "Why Not Your Own Services?",
    body_text: str = "Start Your Self-Hosting Journey with us!",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#ec4899",     # CSS hex color (e.g., pink)
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Ambient Glassmorphism Hero Section.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Base initial theme config based on python arguments
    initial_dark = 'true' if color_scheme.lower() == 'dark' else 'false'

    # === CSS ===
    css = f"""/* Ambient Glassmorphism Hero Section */
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap');

:root {{
    /* Default Theme (Light) */
    --bg-base: #f8f9fa;
    --text-main: #1a1a2e;
    --text-muted: #6b7280;
    
    --glass-bg: rgba(255, 255, 255, 0.65);
    --glass-border: rgba(255, 255, 255, 0.8);
    --glass-hover: rgba(255, 255, 255, 0.85);
    
    --accent: {accent_color};
    --blob-gradient: linear-gradient(135deg, var(--accent) 0%, #8b5cf6 100%);
    
    --nav-height: 64px;
}}

[data-theme="dark"] {{
    /* Dark Theme */
    --bg-base: #0f111a;
    --text-main: #f3f4f6;
    --text-muted: #9ca3af;
    
    --glass-bg: rgba(25, 27, 35, 0.4);
    --glass-border: rgba(255, 255, 255, 0.08);
    --glass-hover: rgba(255, 255, 255, 0.12);
    
    --blob-gradient: linear-gradient(135deg, var(--accent) 0%, #3b82f6 100%);
}}

*, *::before, *::after {{
    box-sizing: border-box;
    margin: 0;
    padding: 0;
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
    transition: background-color 0.4s ease, color 0.4s ease;
}}

.app-wrapper {{
    position: relative;
    width: 100%;
    max-width: {width_px}px;
    min-height: {height_px}px;
    padding: 2rem;
    display: flex;
    flex-direction: column;
    overflow: hidden;
}}

/* === Ambient Glow === */
.ambient-blob {{
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: 60%;
    height: 60%;
    background: var(--blob-gradient);
    filter: blur(140px);
    border-radius: 50%;
    z-index: 0;
    opacity: 0.65;
    pointer-events: none;
    transition: background 0.4s ease;
}}

/* === Glassmorphism System === */
.glass-panel {{
    background: var(--glass-bg);
    backdrop-filter: blur(24px);
    -webkit-backdrop-filter: blur(24px);
    border: 1px solid var(--glass-border);
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.05);
    z-index: 10;
    transition: background 0.4s ease, border-color 0.4s ease;
}}

/* === Header / Nav === */
header {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0 1.5rem;
    height: var(--nav-height);
    border-radius: 9999px;
    margin-bottom: 4rem;
}}

.brand {{
    font-weight: 700;
    font-size: 1.25rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}}

.brand-dot {{
    width: 12px;
    height: 12px;
    background: var(--accent);
    border-radius: 50%;
}}

.header-actions {{
    display: flex;
    align-items: center;
    gap: 1.5rem;
}}

.nav-link {{
    text-decoration: none;
    color: var(--text-main);
    font-weight: 500;
    font-size: 0.9rem;
    transition: color 0.2s;
}}

.nav-link:hover {{
    color: var(--accent);
}}

/* Theme Toggle Switch */
.theme-switch {{
    display: flex;
    align-items: center;
    gap: 0.75rem;
    font-size: 0.9rem;
    font-weight: 500;
    cursor: pointer;
}}

.switch-track {{
    position: relative;
    width: 48px;
    height: 24px;
    background: var(--glass-border);
    border-radius: 9999px;
    transition: background 0.3s;
}}

[data-theme="dark"] .switch-track {{
    background: var(--accent);
}}

.switch-thumb {{
    position: absolute;
    top: 3px;
    left: 3px;
    width: 18px;
    height: 18px;
    background: #fff;
    border-radius: 50%;
    transition: transform 0.3s cubic-bezier(0.4, 0.0, 0.2, 1);
}}

[data-theme="dark"] .switch-thumb {{
    transform: translateX(24px);
}}

/* === Hero Section === */
.hero {{
    text-align: center;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    flex-grow: 1;
    z-index: 10;
}}

.hero h1 {{
    font-size: 3.5rem;
    font-weight: 700;
    letter-spacing: -0.02em;
    margin-bottom: 1rem;
    line-height: 1.2;
}}

.hero p {{
    font-size: 1.25rem;
    color: var(--text-muted);
    max-width: 600px;
    margin-bottom: 3rem;
}}

/* === Tab Navigation === */
.tab-container {{
    display: inline-flex;
    gap: 1rem;
    padding: 0.75rem;
    border-radius: 9999px;
}}

.tab-btn {{
    background: transparent;
    border: none;
    color: var(--text-main);
    font-family: inherit;
    font-size: 1rem;
    font-weight: 500;
    padding: 0.75rem 2rem;
    border-radius: 9999px;
    cursor: pointer;
    transition: all 0.3s ease;
}}

.tab-btn:hover {{
    background: var(--glass-hover);
}}

.tab-btn.active {{
    background: var(--accent);
    color: #fff;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}}

/* Responsive adjustments */
@media (max-width: 768px) {{
    .hero h1 {{ font-size: 2.5rem; }}
    .app-wrapper {{ padding: 1rem; }}
    .tab-container {{ flex-wrap: wrap; justify-content: center; border-radius: 24px; }}
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
<body data-theme="{ 'dark' if initial_dark == 'true' else 'light' }">
    
    <div class="app-wrapper">
        <!-- The Ambient Background Glow -->
        <div class="ambient-blob"></div>
        
        <!-- Header Navigation -->
        <header class="glass-panel">
            <div class="brand">
                <div class="brand-dot"></div>
                Echoes
            </div>
            
            <div class="header-actions">
                <a href="#" class="nav-link">Join now</a>
                <div class="theme-switch" id="themeToggle" role="button" aria-label="Toggle Dark Mode">
                    <span>Lights</span>
                    <div class="switch-track">
                        <div class="switch-thumb"></div>
                    </div>
                </div>
            </div>
        </header>

        <!-- Main Hero Content -->
        <main class="hero">
            <h1>{title_text}</h1>
            <p>{body_text}</p>
            
            <!-- Pill Tab Navigation -->
            <div class="glass-panel tab-container">
                <button class="tab-btn">Posts</button>
                <button class="tab-btn">Blogs</button>
                <button class="tab-btn active">Videos</button>
            </div>
        </main>
    </div>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Theme toggling logic
document.addEventListener('DOMContentLoaded', () => {{
    const themeToggleBtn = document.getElementById('themeToggle');
    const body = document.body;

    themeToggleBtn.addEventListener('click', () => {{
        // Toggle the data-theme attribute between 'dark' and 'light'
        const currentTheme = body.getAttribute('data-theme');
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
        body.setAttribute('data-theme', newTheme);
    }});
    
    // Simple tab interaction
    const tabs = document.querySelectorAll('.tab-btn');
    tabs.forEach(tab => {{
        tab.addEventListener('click', () => {{
            tabs.forEach(t => t.classList.remove('active'));
            tab.classList.add('active');
        }});
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
