def create_component(
    output_dir: str,
    title_text: str = "Why Not Your Own Services?",
    body_text: str = "Start Your Self-Hosting Journey with us! Toggle the switch to change themes.",
    color_scheme: str = "light",       # "dark" or "light"
    accent_color: str = "#fa39ad",     # Pink accent like the video
    width_px: int = 1000,
    height_px: int = 600,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Smooth Dark Mode Toggle effect.
    
    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Determine initial state based on color_scheme
    initial_theme = "dark-theme" if color_scheme == "dark" else "light-theme"
    is_checked = "checked" if color_scheme == "dark" else ""

    # === CSS ===
    css = f"""/* Theme Toggle Component — Generated */
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap');

*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

/* Theme Variable Definitions */
body.light-theme {{
    --bg-color: #f3f3f3;
    --text-color: #1a1a2e;
    --surface-color: #ffffff;
    --track-bg: #cbd5e1;
    --accent-color: {accent_color};
}}

body.dark-theme {{
    --bg-color: #0d111c;
    --text-color: #f0f0f0;
    --surface-color: #1a1f2e;
    --track-bg: #334155;
    --accent-color: {accent_color};
}}

body {{
    font-family: 'Poppins', sans-serif;
    background-color: var(--bg-color);
    color: var(--text-color);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: background-color 0.4s ease, color 0.4s ease;
}}

/* Container constraints */
.wrapper {{
    width: 100%;
    max-width: {width_px}px;
    min-height: {height_px}px;
    padding: 40px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 32px;
    text-align: center;
}}

/* Typography */
h1 {{
    font-size: 3rem;
    font-weight: 600;
    letter-spacing: -0.5px;
}}

p {{
    font-size: 1.125rem;
    opacity: 0.8;
    max-width: 600px;
}}

/* Hero Card (Surface) */
.hero-card {{
    background-color: var(--surface-color);
    padding: 40px 60px;
    border-radius: 24px;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.05);
    transition: background-color 0.4s ease, box-shadow 0.4s ease;
}}

body.dark-theme .hero-card {{
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
}}

/* --- Custom Toggle Switch --- */
.theme-switch-wrapper {{
    display: flex;
    align-items: center;
    gap: 16px;
    margin-top: 20px;
}}

.switch-label {{
    font-weight: 500;
    font-size: 1.1rem;
}}

.switch {{
    position: relative;
    display: inline-block;
    width: 56px;
    height: 30px;
}}

.switch input {{
    opacity: 0;
    width: 0;
    height: 0;
}}

/* The Track */
.slider {{
    position: absolute;
    cursor: pointer;
    top: 0; left: 0; right: 0; bottom: 0;
    background-color: var(--track-bg);
    border-radius: 30px;
    transition: background-color 0.4s ease;
}}

/* The Knob */
.slider::before {{
    position: absolute;
    content: "";
    height: 22px;
    width: 22px;
    left: 4px;
    bottom: 4px;
    background-color: white;
    border-radius: 50%;
    transition: transform 0.4s cubic-bezier(0.4, 0.0, 0.2, 1);
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
}}

/* Checked State */
input:checked + .slider {{
    background-color: var(--accent-color);
}}

input:checked + .slider::before {{
    transform: translateX(26px);
}}

/* Focus Outline for Accessibility */
input:focus-visible + .slider {{
    outline: 2px solid var(--text-color);
    outline-offset: 2px;
}}
"""

    # === HTML ===
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dark Mode Toggle</title>
    <link rel="stylesheet" href="style.css">
</head>
<body class="{initial_theme}">
    <div class="wrapper">
        <div class="hero-card">
            <h1>{title_text}</h1>
            <p>{body_text}</p>
            
            <div class="theme-switch-wrapper">
                <span class="switch-label">Lights</span>
                <label class="switch" aria-label="Toggle Dark Mode">
                    <input type="checkbox" id="themeToggle" {is_checked}>
                    <span class="slider"></span>
                </label>
            </div>
        </div>
    </div>
    
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = """// Smooth Theme Toggle Logic
document.addEventListener('DOMContentLoaded', () => {
    const themeToggle = document.getElementById('themeToggle');
    
    themeToggle.addEventListener('change', (e) => {
        if (e.target.checked) {
            // Switch to Dark Mode
            document.body.classList.replace('light-theme', 'dark-theme');
        } else {
            // Switch to Light Mode
            document.body.classList.replace('dark-theme', 'light-theme');
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
