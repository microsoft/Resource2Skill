def create_component(
    output_dir: str,
    title_text: str = "Why not Your own Services?",
    body_text: str = "Start Your Self-Hosting Journey with us! Toggle the switch to change the lighting.",
    color_scheme: str = "light",       # "dark" or "light"
    accent_color: str = "#ec4899",     # Pink accent color from video
    width_px: int = 1000,
    height_px: int = 700,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Animated Theme Switcher.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Determine initial states based on parameter
    is_dark = color_scheme == "dark"
    body_class = ' class="dark-mode"' if is_dark else ""
    checked_attr = " checked" if is_dark else ""

    # === CSS ===
    css = f"""/* Theme Switcher Generated Component */
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');

:root {{
    /* Light Theme Variables */
    --bg-color: #f3f4f6;
    --surface-color: #ffffff;
    --text-primary: #1e293b;
    --text-secondary: #64748b;
    --border-color: #e2e8f0;
    --accent-color: {accent_color};
    --shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.05), 0 4px 6px -2px rgba(0, 0, 0, 0.02);
    
    --width: {width_px}px;
    --height: {height_px}px;
}}

body.dark-mode {{
    /* Dark Theme Variables */
    --bg-color: #0f172a;
    --surface-color: #1e293b;
    --text-primary: #f8fafc;
    --text-secondary: #94a3b8;
    --border-color: #334155;
    --shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.5), 0 4px 6px -2px rgba(0, 0, 0, 0.3);
}}

*, *::before, *::after {{
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}}

body {{
    font-family: 'Poppins', sans-serif;
    background-color: var(--bg-color);
    color: var(--text-primary);
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
    /* This global transition creates the smooth fade between themes */
    transition: background-color 0.4s ease, color 0.4s ease;
    overflow-x: hidden;
}}

/* Decorative Background Blob */
.bg-blob {{
    position: absolute;
    width: 60vw;
    height: 60vh;
    background: linear-gradient(to bottom right, var(--accent-color), #8b5cf6);
    filter: blur(120px);
    opacity: 0.15;
    border-radius: 50%;
    z-index: -1;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    pointer-events: none;
    transition: opacity 0.4s ease;
}}

body.dark-mode .bg-blob {{
    opacity: 0.08; /* Dim the blob slightly in dark mode */
}}

/* Layout Container */
.app-container {{
    width: 100%;
    max-width: var(--width);
    min-height: var(--height);
    display: flex;
    flex-direction: column;
    padding: 2rem;
    position: relative;
}}

/* Navigation / Header */
header {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding-bottom: 3rem;
}}

.logo {{
    font-size: 1.25rem;
    font-weight: 700;
    letter-spacing: -0.5px;
}}

.logo-dot {{
    color: var(--accent-color);
}}

/* Toggle Switch Styles */
.theme-toggle-wrapper {{
    display: flex;
    align-items: center;
    gap: 12px;
}}

.theme-label-text {{
    font-size: 0.9rem;
    font-weight: 600;
    color: var(--text-secondary);
}}

.toggle-checkbox {{
    display: none;
}}

.toggle-label {{
    position: relative;
    display: block;
    width: 56px;
    height: 30px;
    background-color: var(--border-color);
    border-radius: 30px;
    cursor: pointer;
    transition: background-color 0.3s ease;
    box-shadow: inset 0 2px 4px rgba(0,0,0,0.1);
}}

.toggle-label::after {{
    content: '';
    position: absolute;
    top: 3px;
    left: 3px;
    width: 24px;
    height: 24px;
    background-color: #ffffff;
    border-radius: 50%;
    box-shadow: 0 2px 5px rgba(0,0,0,0.2);
    transition: transform 0.3s cubic-bezier(0.4, 0.0, 0.2, 1);
}}

/* Checked State */
.toggle-checkbox:checked + .toggle-label {{
    background-color: var(--accent-color);
}}

.toggle-checkbox:checked + .toggle-label::after {{
    transform: translateX(26px);
}}

/* Hero Section */
.hero {{
    text-align: center;
    margin-top: 4rem;
    margin-bottom: 5rem;
}}

.hero h1 {{
    font-size: clamp(2rem, 5vw, 3.5rem);
    line-height: 1.2;
    margin-bottom: 1rem;
    font-weight: 600;
}}

.hero p {{
    color: var(--text-secondary);
    font-size: 1.1rem;
    max-width: 600px;
    margin: 0 auto;
}}

/* Cards Grid */
.cards-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 1.5rem;
    margin-top: auto;
}}

.card {{
    background-color: var(--surface-color);
    border: 1px solid var(--border-color);
    border-radius: 16px;
    padding: 1.5rem;
    box-shadow: var(--shadow);
    transition: background-color 0.4s ease, border-color 0.4s ease, transform 0.2s ease, box-shadow 0.4s ease;
    cursor: pointer;
}}

.card:hover {{
    transform: translateY(-4px);
}}

.card-category {{
    font-size: 0.8rem;
    text-transform: uppercase;
    font-weight: 600;
    color: var(--accent-color);
    margin-bottom: 0.5rem;
}}

.card-title {{
    font-size: 1.25rem;
    font-weight: 600;
    color: var(--text-primary);
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
    <div class="bg-blob"></div>
    
    <div class="app-container">
        <header>
            <div class="logo">EchoesOfPing<span class="logo-dot">.</span></div>
            
            <div class="theme-toggle-wrapper">
                <span class="theme-label-text">Lights</span>
                <input type="checkbox" id="theme-toggle" class="toggle-checkbox"{checked_attr} aria-label="Toggle Dark Mode">
                <label for="theme-toggle" class="toggle-label"></label>
            </div>
        </header>

        <main>
            <section class="hero">
                <h1>{title_text}</h1>
                <p>{body_text}</p>
            </section>

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
        </main>
    </div>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Animated Theme Switcher Logic
document.addEventListener('DOMContentLoaded', () => {{
    const themeToggle = document.getElementById('theme-toggle');
    const body = document.body;

    // Listen for changes on the checkbox
    themeToggle.addEventListener('change', (e) => {{
        if (e.target.checked) {{
            // Switch to Dark Mode
            body.classList.add('dark-mode');
        }} else {{
            // Switch to Light Mode
            body.classList.remove('dark-mode');
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
