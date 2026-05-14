def create_component(
    output_dir: str,
    title_text: str = "Why Not Your Own Services?",
    body_text: str = "Start your self-hosting journey with us! Toggle the switch to change the ambiance.",
    color_scheme: str = "light",       # "dark" or "light" (Initial state)
    accent_color: str = "#fa39ad",     # Accent color for the toggle and highlights
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Smooth Global Theme Toggle effect.
    
    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)
    
    is_dark = color_scheme == "dark"
    body_class = ' class="dark-mode"' if is_dark else ''
    input_checked = ' checked' if is_dark else ''

    # === CSS ===
    css = f"""/* Smooth Theme Toggle Component */
:root {{
    /* Light Theme Palette */
    --bg-light: #f4f6f8;
    --text-light: #1e293b;
    --surface-light: #ffffff;
    --border-light: rgba(0, 0, 0, 0.08);
    --shadow-light: 0 10px 25px rgba(0, 0, 0, 0.05);

    /* Dark Theme Palette */
    --bg-dark: #0f172a;
    --text-dark: #f8fafc;
    --surface-dark: #1e293b;
    --border-dark: rgba(255, 255, 255, 0.08);
    --shadow-dark: 0 10px 25px rgba(0, 0, 0, 0.4);

    /* Active Theme Pointers (Defaults to Light) */
    --bg: var(--bg-light);
    --text: var(--text-light);
    --surface: var(--surface-light);
    --border: var(--border-light);
    --shadow: var(--shadow-light);
    
    /* Configurable Variables */
    --accent: {accent_color};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body.dark-mode {{
    /* Override pointers for Dark Mode */
    --bg: var(--bg-dark);
    --text: var(--text-dark);
    --surface: var(--surface-dark);
    --border: var(--border-dark);
    --shadow: var(--shadow-dark);
}}

*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: 'Poppins', system-ui, -apple-system, sans-serif;
    background-color: var(--bg);
    color: var(--text);
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    overflow-x: hidden;
    /* The magic that smooths the global theme switch */
    transition: background-color 0.4s ease, color 0.4s ease;
}}

.app-container {{
    width: 100%;
    max-width: var(--width);
    min-height: var(--height);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 2rem;
}}

/* Navbar / Header */
.navbar {{
    width: 100%;
    display: flex;
    justify-content: flex-end;
    padding: 1.5rem 0;
    margin-bottom: 2rem;
}}

/* Hero Section */
.hero {{
    text-align: center;
    margin-bottom: 4rem;
}}

.hero h1 {{
    font-size: 3rem;
    font-weight: 700;
    margin-bottom: 1rem;
    transition: color 0.4s ease;
}}

.hero p {{
    font-size: 1.125rem;
    opacity: 0.8;
    max-width: 600px;
    margin: 0 auto;
}}

/* Content Cards */
.cards-grid {{
    display: flex;
    gap: 2rem;
    width: 100%;
    justify-content: center;
    flex-wrap: wrap;
}}

.card {{
    background-color: var(--surface);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 2rem;
    width: 300px;
    box-shadow: var(--shadow);
    transition: background-color 0.4s ease, border-color 0.4s ease, box-shadow 0.4s ease, transform 0.3s ease;
    cursor: pointer;
}}

.card:hover {{
    transform: translateY(-5px);
    border-color: var(--accent);
}}

.card h3 {{
    font-size: 1.25rem;
    margin-bottom: 0.5rem;
}}

.card p {{
    font-size: 0.95rem;
    opacity: 0.7;
}}

/* ========================================= */
/* THEME TOGGLE SWITCH STYLES                */
/* ========================================= */

.theme-toggle {{
    position: relative;
    display: flex;
    align-items: center;
    gap: 12px;
    cursor: pointer;
}}

.theme-toggle-label-text {{
    font-weight: 500;
    font-size: 0.9rem;
    user-select: none;
}}

/* Visually hide the checkbox */
.theme-toggle-checkbox {{
    position: absolute;
    opacity: 0;
    width: 0;
    height: 0;
}}

/* The Pill */
.theme-toggle-pill {{
    position: relative;
    width: 64px;
    height: 32px;
    background-color: var(--surface);
    border: 2px solid var(--border);
    border-radius: 32px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 8px;
    transition: background-color 0.4s ease, border-color 0.4s ease;
    box-shadow: inset 0 2px 4px rgba(0,0,0,0.06);
}}

/* Icons inside the pill */
.theme-toggle-icon {{
    font-size: 12px;
    z-index: 1;
    color: var(--text);
    opacity: 0.5;
    transition: opacity 0.4s ease;
}}

.theme-toggle-checkbox:checked ~ .theme-toggle-pill .icon-moon {{
    opacity: 1;
    color: var(--accent);
}}

.theme-toggle-checkbox:not(:checked) ~ .theme-toggle-pill .icon-sun {{
    opacity: 1;
    color: #eab308; /* Sun yellow */
}}

/* The Sliding Thumb */
.theme-toggle-circle {{
    position: absolute;
    left: 2px;
    top: 2px;
    width: 24px;
    height: 24px;
    background-color: var(--accent);
    border-radius: 50%;
    z-index: 2;
    transition: transform 0.4s cubic-bezier(0.4, 0.0, 0.2, 1);
    box-shadow: 0 2px 5px rgba(0,0,0,0.2);
}}

/* The Slide Action */
.theme-toggle-checkbox:checked ~ .theme-toggle-pill .theme-toggle-circle {{
    transform: translateX(32px);
}}
"""

    # === HTML ===
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text}</title>
    <!-- Google Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <!-- FontAwesome -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    
    <link rel="stylesheet" href="style.css">
</head>
<body{body_class}>
    <div class="app-container">
        
        <!-- Header with Toggle -->
        <header class="navbar">
            <label class="theme-toggle" aria-label="Toggle Dark Mode" for="theme-switch">
                <span class="theme-toggle-label-text">Lights</span>
                <input type="checkbox" id="theme-switch" class="theme-toggle-checkbox"{input_checked}>
                <div class="theme-toggle-pill">
                    <i class="fas fa-sun theme-toggle-icon icon-sun"></i>
                    <i class="fas fa-moon theme-toggle-icon icon-moon"></i>
                    <div class="theme-toggle-circle"></div>
                </div>
            </label>
        </header>

        <!-- Main Content -->
        <main>
            <div class="hero">
                <h1>{title_text}</h1>
                <p>{body_text}</p>
            </div>

            <div class="cards-grid">
                <div class="card">
                    <h3>Speedtest-Tracker</h3>
                    <p>Installation Guide</p>
                </div>
                <div class="card">
                    <h3>Uptime-Kuma</h3>
                    <p>Monitoring Setup</p>
                </div>
                <div class="card">
                    <h3>HomeLab Server</h3>
                    <p>Playlist (Self-hosting)</p>
                </div>
            </div>
        </main>

    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Smooth Global Theme Toggle Logic
document.addEventListener('DOMContentLoaded', () => {{
    const themeSwitch = document.getElementById('theme-switch');
    
    // Listen for changes on the hidden checkbox
    themeSwitch.addEventListener('change', (e) => {{
        if (e.target.checked) {{
            // Enable Dark Mode
            document.body.classList.add('dark-mode');
        }} else {{
            // Enable Light Mode
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
