def create_component(
    output_dir: str,
    title_text: str = "Why Not Your Own Services?",
    body_text: str = "Start Your Self-Hosting Journey with us!",
    color_scheme: str = "light",       # "dark" or "light"
    accent_color: str = "#ec4899",     # Primary accent color (defaults to pinkish)
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Ambient Glassmorphism Hero effect.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os
    import colorsys

    os.makedirs(output_dir, exist_ok=True)

    # Base HTML template variables
    initial_theme_class = "dark" if color_scheme == "dark" else ""
    checked_state = "checked" if color_scheme == "dark" else ""

    # === CSS ===
    css = f"""/* Ambient Glassmorphism Hero - CSS */
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

:root {{
    /* Light Theme Base Variables */
    --bg-color: #f8fafc;
    --text-primary: #0f172a;
    --text-secondary: #475569;
    
    --glass-bg: rgba(255, 255, 255, 0.65);
    --glass-border: rgba(255, 255, 255, 0.4);
    --glass-shadow: rgba(0, 0, 0, 0.05);
    
    --card-bg: rgba(255, 255, 255, 0.8);
    --card-hover: rgba(255, 255, 255, 1);
    
    --accent-color: {accent_color};
    --glow-1: {accent_color};
    --glow-2: #8b5cf6; /* Secondary ambient color */
    
    --toggle-bg: #cbd5e1;
    --toggle-knob: #ffffff;
}}

body.dark {{
    /* Dark Theme Variables */
    --bg-color: #020617;
    --text-primary: #f8fafc;
    --text-secondary: #94a3b8;
    
    --glass-bg: rgba(15, 23, 42, 0.6);
    --glass-border: rgba(255, 255, 255, 0.08);
    --glass-shadow: rgba(0, 0, 0, 0.2);
    
    --card-bg: rgba(30, 41, 59, 0.7);
    --card-hover: rgba(30, 41, 59, 0.95);
    
    --glow-1: #2dd4bf; /* Dark mode secondary accent */
    --glow-2: #3b82f6; 
    
    --toggle-bg: var(--accent-color);
    --toggle-knob: #020617;
}}

*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
    transition: background-color 0.4s ease, color 0.4s ease, border-color 0.4s ease, box-shadow 0.4s ease;
}}

body {{
    font-family: 'Poppins', sans-serif;
    background-color: var(--bg-color);
    color: var(--text-primary);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow-x: hidden;
    position: relative;
}}

/* Set requested bounds if applied inside an iframe/container */
.viewport-wrapper {{
    width: 100%;
    max-width: {width_px}px;
    height: 100%;
    min-height: {height_px}px;
    position: relative;
    padding: 2rem;
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 0 auto;
}}

/* --- Ambient Glowing Backgrounds --- */
.ambient-glow {{
    position: absolute;
    border-radius: 50%;
    filter: blur(120px);
    z-index: 0;
    opacity: 0.6;
    animation: drift 10s infinite alternate ease-in-out;
}}

.glow-1 {{
    width: 400px;
    height: 400px;
    background: var(--glow-1);
    top: 10%;
    left: 20%;
}}

.glow-2 {{
    width: 350px;
    height: 350px;
    background: var(--glow-2);
    bottom: 10%;
    right: 20%;
    animation-delay: -5s;
}}

@keyframes drift {{
    0% {{ transform: translate(0, 0) scale(1); }}
    100% {{ transform: translate(30px, 50px) scale(1.1); }}
}}

/* --- Glassmorphism Container --- */
.glass-panel {{
    position: relative;
    z-index: 10;
    width: 100%;
    background: var(--glass-bg);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border: 1px solid var(--glass-border);
    border-radius: 24px;
    padding: 2.5rem;
    box-shadow: 0 25px 50px -12px var(--glass-shadow);
    display: flex;
    flex-direction: column;
    gap: 3rem;
}}

/* --- Header / Nav --- */
header {{
    display: flex;
    justify-content: space-between;
    align-items: center;
}}

.logo-container {{
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-weight: 600;
    font-size: 1.1rem;
}}

.logo-dot {{
    width: 12px;
    height: 12px;
    background-color: var(--accent-color);
    border-radius: 50%;
}}

.nav-actions {{
    display: flex;
    align-items: center;
    gap: 1.5rem;
}}

.btn-primary {{
    background: transparent;
    color: var(--text-primary);
    border: 1px solid var(--glass-border);
    padding: 0.5rem 1.25rem;
    border-radius: 99px;
    font-family: inherit;
    font-weight: 500;
    cursor: pointer;
    text-decoration: none;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}}
.btn-primary:hover {{
    background: var(--accent-color);
    color: #fff;
    border-color: var(--accent-color);
}}

/* --- Hero Content --- */
.hero-content {{
    text-align: center;
    max-width: 800px;
    margin: 0 auto;
    padding: 2rem 0;
}}

.hero-content h1 {{
    font-size: clamp(2rem, 5vw, 3.5rem);
    font-weight: 700;
    line-height: 1.2;
    margin-bottom: 1rem;
}}

.hero-content p {{
    font-size: 1.1rem;
    color: var(--text-secondary);
}}

/* --- Dashboard Section --- */
.dashboard-section {{
    background: var(--glass-border); /* Slightly darker inner section */
    border-radius: 16px;
    padding: 2rem;
}}

.dashboard-nav {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 2rem;
    flex-wrap: wrap;
    gap: 1rem;
}}

.nav-tabs {{
    display: flex;
    gap: 2rem;
    font-weight: 500;
    color: var(--text-secondary);
}}

.nav-tabs span {{
    cursor: pointer;
    padding-bottom: 0.25rem;
    border-bottom: 2px solid transparent;
}}

.nav-tabs span.active, .nav-tabs span:hover {{
    color: var(--text-primary);
    border-bottom-color: var(--accent-color);
}}

/* --- Theme Toggle Switch --- */
.theme-toggle-wrapper {{
    display: flex;
    align-items: center;
    gap: 0.75rem;
    font-weight: 500;
}}

.toggle-switch {{
    position: relative;
    display: inline-block;
    width: 50px;
    height: 28px;
}}

.toggle-switch input {{
    opacity: 0;
    width: 0;
    height: 0;
}}

.slider {{
    position: absolute;
    cursor: pointer;
    top: 0; left: 0; right: 0; bottom: 0;
    background-color: var(--toggle-bg);
    border-radius: 34px;
    transition: .4s;
}}

.slider:before {{
    position: absolute;
    content: "";
    height: 20px;
    width: 20px;
    left: 4px;
    bottom: 4px;
    background-color: var(--toggle-knob);
    border-radius: 50%;
    transition: .4s cubic-bezier(0.4, 0.0, 0.2, 1);
}}

input:checked + .slider:before {{
    transform: translateX(22px);
}}

/* --- Grid Cards --- */
.card-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 1.5rem;
}}

.card {{
    background: var(--card-bg);
    padding: 1.5rem;
    border-radius: 12px;
    border: 1px solid var(--glass-border);
    cursor: pointer;
    transform: translateY(0);
    transition: transform 0.3s ease, background-color 0.3s ease, box-shadow 0.3s ease;
}}

.card:hover {{
    background: var(--card-hover);
    transform: translateY(-4px);
    box-shadow: 0 10px 20px -10px var(--glass-shadow);
}}

.card-label {{
    font-size: 0.8rem;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: var(--text-secondary);
    margin-bottom: 0.5rem;
    display: block;
}}

.card-title {{
    font-size: 1.25rem;
    font-weight: 600;
}}

@media(max-width: 768px) {{
    .glass-panel {{ padding: 1.5rem; gap: 2rem; }}
    .nav-actions span {{ display: none; }}
    .nav-tabs {{ gap: 1rem; }}
}}
"""

    # === HTML ===
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text}</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link rel="stylesheet" href="style.css">
</head>
<body class="{initial_theme_class}">

    <div class="viewport-wrapper">
        <!-- Ambient Background Glows -->
        <div class="ambient-glow glow-1"></div>
        <div class="ambient-glow glow-2"></div>

        <!-- Main Glass Container -->
        <div class="glass-panel">
            
            <!-- Header -->
            <header>
                <div class="logo-container">
                    <div class="logo-dot"></div>
                    <span>EchoesOfPing</span>
                </div>
                <div class="nav-actions">
                    <a href="#" class="btn-primary">
                        <i class="fa-brands fa-youtube"></i> YouTube
                    </a>
                    <span>Join now</span>
                    <i class="fa-regular fa-user"></i>
                </div>
            </header>

            <!-- Hero Section -->
            <section class="hero-content">
                <h1>{title_text}</h1>
                <p>{body_text}</p>
            </section>

            <!-- Interactive Dashboard Area -->
            <section class="dashboard-section">
                <div class="dashboard-nav">
                    <div class="nav-tabs">
                        <span>Posts</span>
                        <span>Blogs</span>
                        <span class="active">Videos</span>
                    </div>
                    
                    <div class="theme-toggle-wrapper">
                        <span>Lights</span>
                        <label class="toggle-switch">
                            <input type="checkbox" id="themeToggle" {checked_state}>
                            <span class="slider"></span>
                        </label>
                    </div>
                </div>

                <div class="card-grid">
                    <div class="card">
                        <span class="card-label">Installation Guide</span>
                        <h3 class="card-title">Speedtest-Tracker</h3>
                    </div>
                    <div class="card">
                        <span class="card-label">Setup</span>
                        <h3 class="card-title">Uptime-Kuma</h3>
                    </div>
                    <div class="card">
                        <span class="card-label">Playlist</span>
                        <h3 class="card-title">HomeLab (Self-hosting)</h3>
                    </div>
                </div>
            </section>

        </div>
    </div>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = """// Ambient Glassmorphism Hero - JS
document.addEventListener('DOMContentLoaded', () => {
    const themeToggle = document.getElementById('themeToggle');
    
    // Listen for toggle switch changes
    themeToggle.addEventListener('change', (e) => {
        if (e.target.checked) {
            document.body.classList.add('dark');
        } else {
            document.body.classList.remove('dark');
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
