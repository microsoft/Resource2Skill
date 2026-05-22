def create_component(
    output_dir: str,
    title_text: str = "Why not Your own Services?",
    body_text: str = "Start Your Self-Hosting Journey with us!",
    color_scheme: str = "light",
    accent_color: str = "#8b5cf6",
    width_px: int = 800,
    height_px: int = 500,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Smooth Theme Toggle Switch visual effect.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Determine initial state for HTML templating
    is_dark = color_scheme == "dark"
    body_class = ' class="dark-mode"' if is_dark else ""
    checkbox_checked = " checked" if is_dark else ""

    # === CSS ===
    css = f"""/* Smooth Theme Toggle Switch — generated component */
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    /* Light Theme Variables */
    --bg-color: #f8fafc;
    --surface-color: #ffffff;
    --text-primary: #1e293b;
    --text-secondary: #64748b;
    --accent-color: {accent_color};
    --toggle-track: #cbd5e1;
    --toggle-thumb: #ffffff;
    --card-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
}}

body.dark-mode {{
    /* Dark Theme Variables */
    --bg-color: #0f172a;
    --surface-color: #1e293b;
    --text-primary: #f8fafc;
    --text-secondary: #94a3b8;
    --toggle-track: {accent_color};
    --toggle-thumb: #ffffff;
    --card-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.5), 0 4px 6px -2px rgba(0, 0, 0, 0.3);
}}

body {{
    font-family: 'Poppins', sans-serif;
    background-color: var(--bg-color);
    color: var(--text-primary);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    /* The magic that makes the whole page theme transition smooth */
    transition: background-color 0.4s ease, color 0.4s ease;
}}

.container {{
    width: {width_px}px;
    max-width: 90vw;
    height: {height_px}px;
    background-color: var(--surface-color);
    border-radius: 24px;
    box-shadow: var(--card-shadow);
    padding: 40px;
    display: flex;
    flex-direction: column;
    align-items: center;
    position: relative;
    text-align: center;
    transition: background-color 0.4s ease, box-shadow 0.4s ease;
}}

.header-controls {{
    width: 100%;
    display: flex;
    justify-content: flex-end;
    align-items: center;
    margin-bottom: 40px;
}}

.theme-toggle-label {{
    display: flex;
    align-items: center;
    gap: 12px;
    cursor: pointer;
    font-weight: 500;
    font-size: 14px;
    color: var(--text-secondary);
    transition: color 0.4s ease;
}}

.theme-toggle-label:hover {{
    color: var(--text-primary);
}}

/* Hide default checkbox */
.theme-toggle-checkbox {{
    display: none;
}}

/* Custom Toggle Track */
.toggle-track {{
    width: 64px;
    height: 34px;
    background-color: var(--toggle-track);
    border-radius: 999px;
    position: relative;
    transition: background-color 0.4s ease;
    box-shadow: inset 0 2px 4px rgba(0,0,0,0.1);
}}

/* Custom Toggle Thumb */
.toggle-thumb {{
    width: 26px;
    height: 26px;
    background-color: var(--toggle-thumb);
    border-radius: 50%;
    position: absolute;
    top: 4px;
    left: 4px;
    display: flex;
    justify-content: center;
    align-items: center;
    box-shadow: 0 2px 5px rgba(0,0,0,0.2);
    /* Transition transform for movement */
    transition: transform 0.4s cubic-bezier(0.4, 0.0, 0.2, 1), background-color 0.4s ease;
}}

/* Icon styles inside thumb */
.toggle-thumb i {{
    font-size: 14px;
    color: #f59e0b; /* Sun color */
    transition: opacity 0.3s ease;
    position: absolute;
}}

.toggle-thumb .fa-moon {{
    color: #3b82f6; /* Moon color */
    opacity: 0;
}}

/* Checked State Styles */
.theme-toggle-checkbox:checked + .toggle-track .toggle-thumb {{
    transform: translateX(30px);
}}

.theme-toggle-checkbox:checked + .toggle-track .toggle-thumb .fa-sun {{
    opacity: 0;
}}

.theme-toggle-checkbox:checked + .toggle-track .toggle-thumb .fa-moon {{
    opacity: 1;
}}

/* Content Styles */
.title {{
    font-size: 32px;
    font-weight: 700;
    margin-bottom: 16px;
    background: linear-gradient(to right, var(--text-primary), var(--accent-color));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    transition: all 0.4s ease;
}}

.body-text {{
    font-size: 18px;
    color: var(--text-secondary);
    line-height: 1.6;
    transition: color 0.4s ease;
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
<body{body_class}>
    <div class="container">
        
        <div class="header-controls">
            <label class="theme-toggle-label" for="themeToggle">
                Lights
                <input type="checkbox" id="themeToggle" class="theme-toggle-checkbox"{checkbox_checked}>
                <div class="toggle-track">
                    <div class="toggle-thumb">
                        <i class="fas fa-sun"></i>
                        <i class="fas fa-moon"></i>
                    </div>
                </div>
            </label>
        </div>

        <h1 class="title">{title_text}</h1>
        <p class="body-text">{body_text}</p>
        
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Smooth Theme Toggle Switch — interactive behavior
document.addEventListener('DOMContentLoaded', () => {{
    const themeToggle = document.getElementById('themeToggle');
    
    // Listen for change events on the checkbox
    themeToggle.addEventListener('change', (e) => {{
        // Toggle the 'dark-mode' class on the body based on checked state
        if (e.target.checked) {{
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
