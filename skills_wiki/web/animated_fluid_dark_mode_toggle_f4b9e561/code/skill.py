def create_component(
    output_dir: str,
    title_text: str = "Why not Your own Services?",
    body_text: str = "Start Your Self-Hosting Journey with us! Experience seamless light and dark mode transitions.",
    color_scheme: str = "light",       # "dark" or "light"
    accent_color: str = "#00ffaa",     # Vivid mint green from the video
    width_px: int = 1000,
    height_px: int = 600,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Animated Fluid Dark Mode Toggle effect.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)
    
    # Pre-calculate state variables based on requested color_scheme
    is_dark = color_scheme.lower() == "dark"
    body_class = 'class="dark-mode"' if is_dark else ""
    checkbox_checked = 'checked' if is_dark else ""

    # === CSS ===
    css = f"""/* Animated Fluid Dark Mode Toggle */

:root {{
    /* Base Light Theme */
    --bg-color: #f0f4f8;
    --surface-color: #ffffff;
    --text-main: #1e293b;
    --text-muted: #64748b;
    --border-color: #e2e8f0;
    
    /* Toggle Specifics */
    --toggle-inactive: #cbd5e1;
    --toggle-active: {accent_color};
    --toggle-circle: #ffffff;
    
    /* Application Settings */
    --accent: {accent_color};
    --container-width: {width_px}px;
    --container-height: {height_px}px;
}}

/* Dark Theme Overrides */
body.dark-mode {{
    --bg-color: #0d1117;
    --surface-color: #1e293b;
    --text-main: #f8fafc;
    --text-muted: #94a3b8;
    --border-color: #334155;
}}

* {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: 'Poppins', -apple-system, BlinkMacSystemFont, sans-serif;
    background-color: var(--bg-color);
    color: var(--text-main);
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
    
    /* The magic of smooth theme transitioning */
    transition: background-color 0.5s ease, color 0.5s ease;
}}

.app-container {{
    width: 100%;
    max-width: var(--container-width);
    min-height: var(--container-height);
    background-color: var(--surface-color);
    border: 1px solid var(--border-color);
    border-radius: 24px;
    padding: 48px;
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.08);
    display: flex;
    flex-direction: column;
    
    /* Smooth transition for surfaces */
    transition: background-color 0.5s ease, border-color 0.5s ease, box-shadow 0.5s ease;
}}

/* -- Header & Navigation -- */
.header {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding-bottom: 32px;
    border-bottom: 1px solid var(--border-color);
    margin-bottom: 48px;
    transition: border-color 0.5s ease;
}}

.nav-links {{
    display: flex;
    gap: 32px;
    font-weight: 500;
    color: var(--text-muted);
}}

/* -- Main Content -- */
.hero {{
    text-align: center;
    flex-grow: 1;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
}}

.title {{
    font-size: 3rem;
    font-weight: 600;
    margin-bottom: 16px;
    letter-spacing: -0.5px;
}}

.subtitle {{
    font-size: 1.1rem;
    color: var(--text-muted);
    max-width: 600px;
    line-height: 1.6;
    transition: color 0.5s ease;
}}

/* === TOGGLE SWITCH COMPONENT === */
.theme-switch-wrapper {{
    display: flex;
    align-items: center;
    gap: 12px;
}}

.theme-switch-label {{
    font-size: 0.9rem;
    font-weight: 600;
    cursor: pointer;
}}

/* Hide the native checkbox, but keep it accessible for focus */
.sr-only {{
    position: absolute;
    width: 1px;
    height: 1px;
    padding: 0;
    margin: -1px;
    overflow: hidden;
    clip: rect(0, 0, 0, 0);
    white-space: nowrap;
    border: 0;
}}

.toggle-switch {{
    position: relative;
    width: 52px;
    height: 28px;
    background-color: var(--toggle-inactive);
    border-radius: 999px;
    cursor: pointer;
    transition: background-color 0.4s ease;
}}

.toggle-circle {{
    position: absolute;
    top: 4px;
    left: 4px;
    width: 20px;
    height: 20px;
    background-color: var(--toggle-circle);
    border-radius: 50%;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
    /* Transform is hardware accelerated */
    transition: transform 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}}

/* Keyboard Accessibility Focus State */
.sr-only:focus-visible + .toggle-switch {{
    outline: 2px solid var(--accent);
    outline-offset: 2px;
}}

/* Checked State Interactions */
.sr-only:checked + .toggle-switch {{
    background-color: var(--toggle-active);
}}

.sr-only:checked + .toggle-switch .toggle-circle {{
    /* Move circle to the right */
    transform: translateX(24px);
}}
"""

    # === HTML ===
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Animated Dark Mode Toggle</title>
    <!-- Use Poppins font to match the modern aesthetic -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body {body_class}>
    <div class="app-container">
        
        <!-- Navigation & Toggle -->
        <header class="header">
            <div class="nav-links">
                <span>Posts</span>
                <span>Blogs</span>
                <span style="color: var(--text-main);">Videos</span>
            </div>
            
            <!-- Accessible Toggle Switch -->
            <div class="theme-switch-wrapper">
                <span class="theme-switch-label" id="toggle-label">Lights</span>
                <label for="theme-toggle" aria-labelledby="toggle-label">
                    <input type="checkbox" id="theme-toggle" class="sr-only" {checkbox_checked}>
                    <div class="toggle-switch">
                        <div class="toggle-circle"></div>
                    </div>
                </label>
            </div>
        </header>

        <!-- Content -->
        <main class="hero">
            <h1 class="title">{title_text}</h1>
            <p class="subtitle">{body_text}</p>
        </main>

    </div>
    
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Wait for DOM to load
document.addEventListener('DOMContentLoaded', () => {{
    const themeToggle = document.getElementById('theme-toggle');
    
    // Listen for changes on the hidden checkbox
    themeToggle.addEventListener('change', (event) => {{
        const isChecked = event.target.checked;
        
        // Toggle the .dark-mode class on the body element
        // The CSS handles all the color variable swapping and smooth transitions
        document.body.classList.toggle('dark-mode', isChecked);
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
