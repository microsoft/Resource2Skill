def create_component(
    output_dir: str,
    title_text: str = "Theme Toggle Example",
    body_text: str = "Experience a seamless transition between light and dark modes.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#ec4899",     # Pink accent color
    width_px: int = 600,
    height_px: int = 400,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing a seamless dark mode toggle with glassmorphism.
    
    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)
    
    # Determine initial state flags based on the requested color scheme
    is_dark = color_scheme.lower() == "dark"
    body_class = ' class="dark-mode"' if is_dark else ''
    checked_attr = ' checked' if is_dark else ''

    # === CSS ===
    css = f"""/* Theme Toggle — Generated Component */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    /* Light Theme Tokens */
    --bg-light: #f3f4f6;
    --text-light: #1f2937;
    --surface-light: rgba(255, 255, 255, 0.65);
    --border-light: rgba(255, 255, 255, 0.5);
    --blob-opacity-light: 0.3;
    
    /* Dark Theme Tokens */
    --bg-dark: #0f172a;
    --text-dark: #f9fafb;
    --surface-dark: rgba(30, 41, 59, 0.65);
    --border-dark: rgba(255, 255, 255, 0.08);
    --blob-opacity-dark: 0.15;

    /* Shared / Dynamic Properties */
    --accent: {accent_color};
    --container-width: {width_px}px;
    --container-height: {height_px}px;
}}

/* Apply Light Mode by Default */
body {{
    --bg: var(--bg-light);
    --text: var(--text-light);
    --surface: var(--surface-light);
    --border: var(--border-light);
    --blob-opacity: var(--blob-opacity-light);
}}

/* Override with Dark Mode Tokens */
body.dark-mode {{
    --bg: var(--bg-dark);
    --text: var(--text-dark);
    --surface: var(--surface-dark);
    --border: var(--border-dark);
    --blob-opacity: var(--blob-opacity-dark);
}}

body {{
    font-family: 'Poppins', system-ui, -apple-system, sans-serif;
    background-color: var(--bg);
    color: var(--text);
    /* The core transition for the seamless theme swap */
    transition: background-color 0.5s ease, color 0.5s ease;
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
    position: relative;
}}

/* Decorative Ambient Background */
.ambient-blob {{
    position: absolute;
    width: 60vw;
    height: 60vw;
    max-width: 800px;
    max-height: 800px;
    background: radial-gradient(circle, var(--accent) 0%, transparent 60%);
    filter: blur(80px);
    opacity: var(--blob-opacity);
    z-index: -1;
    pointer-events: none;
    transition: opacity 0.5s ease;
}}

/* Main Glassmorphism Card */
.card {{
    width: var(--container-width);
    min-height: var(--container-height);
    max-width: 90vw;
    padding: 3rem 2rem;
    border-radius: 24px;
    background: var(--surface);
    backdrop-filter: blur(24px);
    -webkit-backdrop-filter: blur(24px);
    border: 1px solid var(--border);
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.15);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    transition: background-color 0.5s ease, border-color 0.5s ease, box-shadow 0.5s ease;
}}

body.dark-mode .card {{
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.4);
}}

.title {{
    font-size: 2.25rem;
    font-weight: 600;
    margin-bottom: 1rem;
    letter-spacing: -0.02em;
}}

.body-text {{
    font-size: 1.125rem;
    line-height: 1.6;
    opacity: 0.8;
    margin-bottom: 2.5rem;
    max-width: 80%;
}}

/* Custom Toggle Switch Container */
.toggle-wrapper {{
    display: flex;
    align-items: center;
    gap: 1rem;
    font-size: 1.5rem;
    background: rgba(0, 0, 0, 0.05);
    padding: 1rem 1.5rem;
    border-radius: 999px;
    border: 1px solid var(--border);
    transition: background-color 0.5s ease;
}}

body.dark-mode .toggle-wrapper {{
    background: rgba(0, 0, 0, 0.3);
}}

/* The Hidden Input */
.switch {{
    position: relative;
    display: inline-block;
    width: 64px;
    height: 34px;
}}

.switch input {{
    opacity: 0;
    width: 0;
    height: 0;
}}

/* The Sliding Track */
.slider {{
    position: absolute;
    cursor: pointer;
    top: 0; left: 0; right: 0; bottom: 0;
    background-color: rgba(0, 0, 0, 0.2);
    transition: background-color 0.4s ease;
    border-radius: 34px;
    box-shadow: inset 0 2px 4px rgba(0,0,0,0.1);
}}

body.dark-mode .slider {{
    background-color: rgba(255, 255, 255, 0.1);
}}

/* The Thumb Indicator */
.slider::before {{
    position: absolute;
    content: "";
    height: 26px;
    width: 26px;
    left: 4px;
    bottom: 4px;
    background-color: white;
    border-radius: 50%;
    transition: transform 0.4s cubic-bezier(0.4, 0.0, 0.2, 1);
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
}}

/* Checked States */
input:checked + .slider {{
    background-color: var(--accent);
}}

input:checked + .slider::before {{
    transform: translateX(30px);
}}

/* Accessibility Focus */
input:focus-visible + .slider {{
    outline: 2px solid var(--text);
    outline-offset: 2px;
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
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body{body_class}>
    <div class="ambient-blob"></div>
    
    <div class="card">
        <h1 class="title">{title_text}</h1>
        <p class="body-text">{body_text}</p>
        
        <div class="toggle-wrapper">
            <span class="icon" aria-hidden="true">☀️</span>
            <label class="switch" aria-label="Toggle Theme">
                <input type="checkbox" id="theme-toggle"{checked_attr}>
                <span class="slider"></span>
            </label>
            <span class="icon" aria-hidden="true">🌙</span>
        </div>
    </div>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Theme Toggle Interaction Logic
document.addEventListener('DOMContentLoaded', () => {{
    const themeToggle = document.getElementById('theme-toggle');
    
    themeToggle.addEventListener('change', function() {{
        // Toggle the dark-mode class on the body based on checkbox state
        if (this.checked) {{
            document.body.classList.add('dark-mode');
        }} else {{
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
