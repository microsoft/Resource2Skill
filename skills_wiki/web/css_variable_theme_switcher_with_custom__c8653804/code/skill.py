def create_component(
    output_dir: str,
    title_text: str = "THIS IS TITLE",
    body_text: str = "Lorem ipsum dolor sit amet consectetur adipisicing elit. Provident, laudantium laboriosam optio ipsum, corrupti possimus necessitatibus reprehenderit, sint vero sunt explicabo. Ea eligendi porro laborum? Inventore, molestias commodi.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#00bfff",     # CSS hex color for accent
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Theme Switcher visual effect.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os
    import html

    os.makedirs(output_dir, exist_ok=True)
    
    # Safe text injection
    safe_title = html.escape(title_text)
    safe_body = html.escape(body_text)
    
    # Determine initial states based on configured default theme
    is_dark = color_scheme == "dark"
    initial_theme = "dark" if is_dark else "light"
    checked_attr = "checked" if is_dark else ""

    # === CSS ===
    # We use a slightly optimized version of the tutorial's logic:
    # `transform: translateX` is used instead of `left` for the toggle animation (better performance).
    css = f"""/* Theme Switcher Generated Component */
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700&display=swap');

*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

/* Light Theme Variables (Default fallback) */
:root, body[data-theme="light"] {{
    --bg-color: #c4dcf1;
    --surface-color: #ffffff;
    --text-primary: #1e1f26;
    --text-secondary: #50526e;
    --toggle-bg: #1e1f26;
    --toggle-thumb: #ffffff;
    --accent: {accent_color};
}}

/* Dark Theme Variables */
body[data-theme="dark"] {{
    --bg-color: #1e1f26;
    --surface-color: #292c33;
    --text-primary: #ffffff;
    --text-secondary: #babaca;
    --toggle-bg: {accent_color};
    --toggle-thumb: #ffffff;
    --accent: {accent_color};
}}

body {{
    font-family: 'Montserrat', sans-serif;
    background-color: var(--bg-color);
    color: var(--text-primary);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
    /* Smooth crossfade for theme switching */
    transition: background-color 0.5s ease, color 0.5s ease;
}}

.layout-wrapper {{
    width: {width_px}px;
    height: {height_px}px;
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
}}

/* --- Custom Theme Switcher --- */
.theme-switcher {{
    position: absolute;
    top: 30px;
    right: 40px;
    display: flex;
    align-items: center;
}}

.theme-switcher input[type="checkbox"] {{
    width: 0;
    height: 0;
    visibility: hidden;
    position: absolute;
}}

.theme-switcher label {{
    display: block;
    width: 60px;
    height: 30px;
    background-color: var(--toggle-bg);
    border-radius: 50px;
    cursor: pointer;
    position: relative;
    transition: background-color 0.4s ease;
    box-shadow: inset 0 2px 5px rgba(0,0,0,0.2);
}}

.theme-switcher label::after {{
    content: '';
    position: absolute;
    top: 50%;
    left: 5px;
    width: 20px;
    height: 20px;
    background-color: var(--toggle-thumb);
    border-radius: 50px;
    /* Combine translateY (centering) with translateX (horizontal movement) */
    transform: translateY(-50%) translateX(0);
    transition: transform 0.4s cubic-bezier(0.4, 0.0, 0.2, 1), background-color 0.4s ease;
    box-shadow: 0 2px 4px rgba(0,0,0,0.2);
}}

/* Checked State */
.theme-switcher input:checked + label::after {{
    /* 60px width - 20px thumb - 10px total padding (5px each side) = 30px translation */
    transform: translateY(-50%) translateX(30px);
}}

/* --- Content Card --- */
.card {{
    background-color: var(--surface-color);
    padding: 40px;
    border-radius: 12px;
    max-width: 480px;
    box-shadow: 0 15px 35px rgba(0, 0, 0, 0.05);
    transition: background-color 0.5s ease, box-shadow 0.5s ease;
}}

.card h1 {{
    font-size: 28px;
    font-weight: 700;
    letter-spacing: 1px;
    text-transform: uppercase;
    margin-bottom: 20px;
    color: var(--text-primary);
    transition: color 0.5s ease;
}}

.card p {{
    font-size: 15px;
    line-height: 1.6;
    color: var(--text-secondary);
    margin-bottom: 30px;
    transition: color 0.5s ease;
}}

.card button {{
    background-color: var(--toggle-bg);
    color: var(--surface-color);
    border: none;
    padding: 12px 30px;
    font-family: inherit;
    font-size: 14px;
    font-weight: 600;
    letter-spacing: 1px;
    text-transform: uppercase;
    border-radius: 6px;
    cursor: pointer;
    transition: background-color 0.4s ease, color 0.4s ease, transform 0.2s ease;
}}

.card button:hover {{
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(0,0,0,0.1);
}}
"""

    # === HTML ===
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Theme Switcher Component</title>
    <link rel="stylesheet" href="style.css">
</head>
<body data-theme="{initial_theme}">
    <div class="layout-wrapper">
        
        <!-- Theme Switcher UI -->
        <div class="theme-switcher">
            <input type="checkbox" id="switcher" {checked_attr} aria-label="Toggle dark mode">
            <label for="switcher"></label>
        </div>

        <!-- Main Content -->
        <section class="card">
            <h1>{safe_title}</h1>
            <p>{safe_body}</p>
            <button type="button">HELLO!</button>
        </section>

    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Theme Switcher Logic
document.addEventListener('DOMContentLoaded', () => {{
    const switcher = document.getElementById('switcher');
    const body = document.body;

    // Listen for state changes on the checkbox
    switcher.addEventListener('change', (e) => {{
        if (e.target.checked) {{
            // If checked, switch to dark theme
            body.setAttribute('data-theme', 'dark');
        }} else {{
            // If unchecked, switch to light theme
            body.setAttribute('data-theme', 'light');
        }}
    }});
}});
"""

    # === Write files ===
    files = []
    for fname, content in [("index.html", html_content), ("style.css", css), ("script.js", js)]:
        path = os.path.join(output_dir, fname)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        files.append(path)

    return {
        "html": html_content,
        "css": css,
        "js": js,
        "files": files,
    }
