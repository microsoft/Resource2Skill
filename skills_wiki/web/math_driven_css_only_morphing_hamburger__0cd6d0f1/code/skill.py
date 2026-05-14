def create_component(
    output_dir: str,
    title_text: str = "Math-Driven CSS Hamburger",
    body_text: str = "Click the hamburger menu to see the pure CSS morphing animation. It triggers the sidebar without any JavaScript.",
    color_scheme: str = "dark",        
    accent_color: str = "#00E5FF",     
    width_px: int = 1000,
    height_px: int = 600,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Math-Driven CSS-Only Morphing Hamburger Menu.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    if color_scheme == "dark":
        bg_color = "#0B0E14"
        text_color = "#FFFFFF"
        sidebar_bg = "#1A1F2B"
    else:
        bg_color = "#F0F4F8"
        text_color = "#111827"
        sidebar_bg = "#FFFFFF"

    css = f"""/* Math-Driven CSS-Only Morphing Hamburger Menu */
*, *::before, *::after {{
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}}

:root {{
    /* Theme Colors */
    --bg-color: {bg_color};
    --text-color: {text_color};
    --sidebar-bg: {sidebar_bg};
    
    /* Hamburger Configurable Variables */
    --bar-width: 60px;
    --bar-height: 8px;
    --hamburger-gap: 8px;
    --foreground: {accent_color};
    --background: var(--bg-color);
    --animation-timing: 300ms ease-in-out;
    
    /* Mathematical Calculations (Do Not Edit) */
    --hamburger-height: calc(var(--bar-height) * 3 + var(--hamburger-gap) * 2);
    /* 1.414... is the square root of 2, used to find the diagonal length of a square */
    --x-width: calc(var(--hamburger-height) * 1.41421356237);
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background-color: var(--bg-color);
    color: var(--text-color);
    min-height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
    overflow-x: hidden;
}}

/* Presentation Container */
.app-container {{
    width: {width_px}px;
    max-width: 100%;
    height: {height_px}px;
    max-height: 100vh;
    position: relative;
    background: var(--bg-color);
    border: 1px solid rgba(128, 128, 128, 0.2);
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
}}

/* Content Area */
.main-content {{
    padding: 80px 40px 40px;
    max-width: 600px;
}}

.main-content h1 {{
    font-size: 2.5rem;
    margin-bottom: 1rem;
    font-weight: 700;
    line-height: 1.2;
}}

.main-content p {{
    font-size: 1.1rem;
    opacity: 0.8;
    line-height: 1.6;
}}

/* =========================================
   CORE SKILL: CSS HAMBURGER MENU
========================================= */

.hamburger-menu {{
    display: flex;
    flex-direction: column;
    gap: var(--hamburger-gap);
    width: max-content;
    position: absolute;
    top: 24px;
    right: 24px;
    z-index: 100;
    cursor: pointer;
}}

/* The pseudo-elements act as the top and bottom bars */
.hamburger-menu::before,
.hamburger-menu::after,
.hamburger-menu input {{
    content: "";
    width: var(--bar-width);
    height: var(--bar-height);
    background-color: var(--foreground);
    border-radius: 9999px;
    transform-origin: left center;
    transition: 
        opacity var(--animation-timing), 
        width var(--animation-timing), 
        rotate var(--animation-timing), 
        translate var(--animation-timing), 
        background-color var(--animation-timing);
}}

/* The hidden checkbox acts as the middle bar */
.hamburger-menu input {{
    appearance: none; /* Removes default checkbox styling */
    padding: 0;
    margin: 0;
    outline: none;
    pointer-events: none; /* Let the label handle the click */
}}

/* --- CHECKED STATE (The 'X' Morph) --- */

/* When the inner checkbox is checked, trigger the animations */
.hamburger-menu:has(input:checked)::before {{
    rotate: 45deg;
    width: var(--x-width);
    translate: 0 calc(var(--bar-height) / -2);
}}

.hamburger-menu:has(input:checked)::after {{
    rotate: -45deg;
    width: var(--x-width);
    translate: 0 calc(var(--bar-height) / 2);
}}

.hamburger-menu input:checked {{
    opacity: 0;
    width: 0;
}}

/* Optional: Swap color when active (e.g., if moving over a colored sidebar) */
.hamburger-menu:has(input:checked)::before,
.hamburger-menu:has(input:checked)::after {{
    background-color: var(--foreground); 
}}

/* --- ACCESSIBILITY (Keyboard Navigation) --- */
.hamburger-menu:has(input:focus-visible)::before,
.hamburger-menu:has(input:focus-visible)::after,
.hamburger-menu input:focus-visible {{
    border: 1px solid var(--background);
    box-shadow: 0 0 0 2px var(--foreground);
}}

/* =========================================
   SIDEBAR DEMONSTRATION
========================================= */

.sidebar {{
    position: absolute;
    top: 0;
    right: 0;
    width: 320px;
    height: 100%;
    background-color: var(--sidebar-bg);
    padding: 100px 32px 32px;
    translate: 100% 0; /* Hidden by default */
    transition: translate var(--animation-timing);
    box-shadow: -10px 0 30px rgba(0, 0, 0, 0.2);
    z-index: 50;
}}

.sidebar nav {{
    display: flex;
    flex-direction: column;
    gap: 20px;
}}

.sidebar nav a {{
    color: var(--text-color);
    text-decoration: none;
    font-size: 1.5rem;
    font-weight: 600;
    opacity: 0.7;
    transition: opacity 0.2s, color 0.2s;
}}

.sidebar nav a:hover {{
    opacity: 1;
    color: var(--foreground);
}}

/* Trigger sidebar when hamburger is checked */
.app-container:has(.hamburger-menu input:checked) .sidebar {{
    translate: 0 0;
}}
"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="app-container">
        <!-- Pure CSS Hamburger Menu -->
        <label class="hamburger-menu" aria-label="Toggle navigation">
            <input type="checkbox" aria-hidden="true">
        </label>

        <!-- Sidebar Navigation -->
        <aside class="sidebar">
            <nav>
                <a href="#">Home</a>
                <a href="#">Services</a>
                <a href="#">Portfolio</a>
                <a href="#">Contact</a>
            </nav>
        </aside>

        <!-- Page Content -->
        <main class="main-content">
            <h1>{title_text}</h1>
            <p>{body_text}</p>
        </main>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    js = """// No JavaScript required for this component!
// The entire morphing animation and state management is handled 
// via the CSS Checkbox Hack and the :has() pseudo-class.

console.log("Component loaded: Zero JS required for navigation state.");
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
