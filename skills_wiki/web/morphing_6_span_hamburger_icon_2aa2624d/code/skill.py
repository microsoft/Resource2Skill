def create_component(
    output_dir: str,
    title_text: str = "Animated Hamburger Icon",
    body_text: str = "Click the icon to toggle the menu state.",
    color_scheme: str = "light",        
    accent_color: str = "#2a1929",     
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Morphing 6-Span Hamburger Icon effect.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Derive theme colors from color_scheme
    if color_scheme == "dark":
        bg_default = "#0d111c"
        bg_active = "#1a2235"
        text_color = "#f0f0f0"
    else:
        bg_default = "#ebebeb"
        bg_active = "#f2e9ca"
        text_color = "#1a1a2e"

    # === CSS ===
    css = f"""/* Morphing 6-Span Hamburger Icon — generated component */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg-default: {bg_default};
    --bg-active: {bg_active};
    --text: {text_color};
    --accent: {accent_color};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background-color: var(--bg-default);
    color: var(--text);
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    transition: background-color 0.4s linear;
    overflow: hidden;
}}

/* Active State Background Transition */
body.nav-open {{
    background-color: var(--bg-active);
}}

.container {{
    width: var(--width);
    max-width: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 3rem;
    text-align: center;
}}

.title {{
    font-weight: 700;
    letter-spacing: -0.02em;
}}

.body-text {{
    font-size: 1.1rem;
    opacity: 0.8;
}}

/* --- Core Component Styles --- */
.nav-icon {{
    position: relative;
    width: 42px;
    height: 32px;
    cursor: pointer;
    background: transparent;
    border: none;
    padding: 0;
    appearance: none;
}}

.nav-icon span {{
    position: absolute;
    width: 50%;
    height: 6px;
    background: var(--accent);
    transition: all 0.25s ease-in-out;
}}

/* Left-side spans (1, 3, 5) */
.nav-icon span:nth-child(odd) {{
    left: 0;
    border-radius: 9px 0 0 9px;
}}

/* Right-side spans (2, 4, 6) */
.nav-icon span:nth-child(even) {{
    left: 50%;
    border-radius: 0 9px 9px 0;
}}

/* Base Vertical Positioning */
.nav-icon span:nth-child(1), 
.nav-icon span:nth-child(2) {{
    top: 0px;
}}

.nav-icon span:nth-child(3), 
.nav-icon span:nth-child(4) {{
    top: 13px;
}}

.nav-icon span:nth-child(5), 
.nav-icon span:nth-child(6) {{
    top: 26px;
}}

/* --- Active 'Open' State Transforms --- */

/* Form first diagonal (\) */
.nav-open .nav-icon span:nth-child(1),
.nav-open .nav-icon span:nth-child(6) {{
    transform: rotate(45deg);
}}

/* Form second diagonal (/) */
.nav-open .nav-icon span:nth-child(2),
.nav-open .nav-icon span:nth-child(5) {{
    transform: rotate(-45deg);
}}

/* Re-position top span halves */
.nav-open .nav-icon span:nth-child(1) {{
    top: 8px;
    left: 5px;
}}

.nav-open .nav-icon span:nth-child(2) {{
    top: 8px;
    left: calc(50% - 5px);
}}

/* Shoot out middle span halves */
.nav-open .nav-icon span:nth-child(3) {{
    left: -100%;
    opacity: 0;
}}

.nav-open .nav-icon span:nth-child(4) {{
    left: 150%;
    opacity: 0;
}}

/* Re-position bottom span halves */
.nav-open .nav-icon span:nth-child(5) {{
    top: 19px;
    left: 5px;
}}

.nav-open .nav-icon span:nth-child(6) {{
    top: 19px;
    left: calc(50% - 5px);
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
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        <div>
            <h1 class="title">{title_text}</h1>
            <p class="body-text">{body_text}</p>
        </div>
        
        <!-- The Hamburger Component -->
        <button class="nav-icon" aria-label="Toggle Navigation Menu" aria-expanded="false">
            <span></span>
            <span></span>
            <span></span>
            <span></span>
            <span></span>
            <span></span>
        </button>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Morphing 6-Span Hamburger Icon — interactive behavior
document.addEventListener('DOMContentLoaded', () => {{
    const navIcon = document.querySelector('.nav-icon');

    // Toggle the .nav-open class on the body to trigger all CSS transitions
    navIcon.addEventListener('click', () => {{
        document.body.classList.toggle('nav-open');
        
        // Update ARIA expanded attribute for screen readers
        const isOpen = document.body.classList.contains('nav-open');
        navIcon.setAttribute('aria-expanded', isOpen);
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
