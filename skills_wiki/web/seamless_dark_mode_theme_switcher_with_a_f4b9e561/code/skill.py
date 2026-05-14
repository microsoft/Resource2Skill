def create_component(
    output_dir: str,
    title_text: str = "Why Not Your Own Services?",
    body_text: str = "Start Your Self-hosting Journey with us!",
    color_scheme: str = "dark",
    accent_color: str = "#ec4899",
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing a seamless Dark Mode switch with ambient background blurs.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)
    
    # Determine initial class state based on parameter
    body_class = "dark-mode" if color_scheme == "dark" else ""
    toggle_checked = "checked" if color_scheme == "dark" else ""

    css = f"""/* Theme Switcher Component */
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

/* Light Theme Variables (Default) */
:root {{
    --bg-base: #f8fafc;
    --surface: #ffffff;
    --text-strong: #0f172a;
    --text-muted: #64748b;
    --border: #e2e8f0;
    --accent: {accent_color};
    --shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
    
    --orb-gradient: linear-gradient(135deg, rgba(236, 72, 153, 0.2), rgba(168, 85, 247, 0.2));
    
    --toggle-bg: #cbd5e1;
    --toggle-thumb: #ffffff;
    
    --width: {width_px}px;
    --height: {height_px}px;
}}

/* Dark Theme Variables */
body.dark-mode {{
    --bg-base: #0b0f19;
    --surface: #111827;
    --text-strong: #f8fafc;
    --text-muted: #94a3b8;
    --border: #1e293b;
    --shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3), 0 2px 4px -1px rgba(0, 0, 0, 0.2);
    
    --orb-gradient: linear-gradient(135deg, rgba(45, 212, 191, 0.15), rgba(59, 130, 246, 0.15));
    
    --toggle-bg: var(--accent);
    --toggle-thumb: #ffffff;
}}

body {{
    font-family: 'Poppins', sans-serif;
    background-color: var(--bg-base);
    color: var(--text-strong);
    min-height: 100vh;
    display: flex;
    justify-content: center;
    position: relative;
    overflow-x: hidden;
    /* The magic of seamless theme switching */
    transition: background-color 0.4s ease, color 0.4s ease;
}}

/* Ambient Blurred Background */
.ambient-orb {{
    position: fixed;
    top: 20%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: 60vw;
    height: 400px;
    background: var(--orb-gradient);
    filter: blur(120px);
    border-radius: 50%;
    z-index: -1;
    pointer-events: none;
    transition: background 0.6s ease;
}}

.container {{
    width: 100%;
    max-width: var(--width);
    padding: 2rem;
    display: flex;
    flex-direction: column;
}}

/* Header & Toggle */
header {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1rem 0;
    margin-bottom: 4rem;
}}

.nav-links {{
    display: flex;
    gap: 2rem;
    font-weight: 500;
    color: var(--text-muted);
}}

.nav-links span.active {{
    color: var(--accent);
    position: relative;
}}

.nav-links span.active::after {{
    content: '';
    position: absolute;
    bottom: -4px;
    left: 0;
    width: 100%;
    height: 2px;
    background-color: var(--accent);
    border-radius: 2px;
}}

.theme-controls {{
    display: flex;
    align-items: center;
    gap: 1rem;
    font-weight: 500;
}}

/* Toggle Switch Styles */
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
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
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
    background-color: var(--toggle-thumb);
    transition: .4s cubic-bezier(0.4, 0.0, 0.2, 1);
    border-radius: 50%;
    box-shadow: 0 2px 4px rgba(0,0,0,0.2);
}}

input:checked + .slider:before {{
    transform: translateX(24px);
}}

/* Hero Section */
.hero {{
    text-align: center;
    margin-bottom: 5rem;
}}

.hero h1 {{
    font-size: 3.5rem;
    font-weight: 600;
    margin-bottom: 1rem;
    letter-spacing: -0.02em;
}}

.hero p {{
    font-size: 1.125rem;
    color: var(--text-muted);
    transition: color 0.4s ease;
}}

/* Grid & Cards */
.grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
    gap: 1.5rem;
}}

.card {{
    background-color: var(--surface);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 1.75rem;
    box-shadow: var(--shadow);
    transition: background-color 0.4s ease, border-color 0.4s ease, box-shadow 0.4s ease, transform 0.2s ease;
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
    cursor: pointer;
}}

.card:hover {{
    transform: translateY(-4px);
    border-color: var(--accent);
}}

.card-label {{
    font-size: 0.875rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: var(--text-muted);
    font-weight: 600;
}}

.card-title {{
    font-size: 1.25rem;
    font-weight: 600;
    color: var(--text-strong);
}}
"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text}</title>
    <link rel="stylesheet" href="style.css">
    <!-- FontAwesome for icons -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
</head>
<body class="{body_class}">
    <div class="ambient-orb"></div>
    
    <div class="container">
        <header>
            <div class="nav-links">
                <span>Posts</span>
                <span>Blogs</span>
                <span class="active">Videos</span>
            </div>
            
            <div class="theme-controls">
                <span>Lights</span>
                <label class="switch" aria-label="Toggle Dark Mode">
                    <input type="checkbox" id="themeToggle" {toggle_checked}>
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
            </section>
        </main>
    </div>

    <script src="script.js"></script>
</body>
</html>"""

    js = f"""// Theme Switcher Logic
document.addEventListener('DOMContentLoaded', () => {{
    const themeToggle = document.getElementById('themeToggle');
    
    // Listen for toggle interactions
    themeToggle.addEventListener('change', (e) => {{
        if (e.target.checked) {{
            document.body.classList.add('dark-mode');
        }} else {{
            document.body.classList.remove('dark-mode');
        }}
    }});
}});
"""

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
