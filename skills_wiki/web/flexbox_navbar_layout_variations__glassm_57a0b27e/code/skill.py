def create_component(
    output_dir: str,
    title_text: str = "Flexbox Navbar Variations",
    body_text: str = "Scroll to see 5 different structural layouts achieved entirely through CSS Flexbox.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#38bdf8",     # Cyan blue from the tutorial
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the 5 Flexbox Navbar layouts.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors ===
    if color_scheme == "dark":
        bg_color = "#0f172a"
        text_primary = "#f8fafc"
        text_muted = "#e2e8f0"
        surface_color = "rgba(255, 255, 255, 0.05)"
        border_color = "rgba(255, 255, 255, 0.1)"
    else:
        bg_color = "#f8fafc"
        text_primary = "#0f172a"
        text_muted = "#475569"
        surface_color = "rgba(0, 0, 0, 0.05)"
        border_color = "rgba(0, 0, 0, 0.1)"

    # === CSS ===
    css = f"""/* Flexbox Navbar Layout Variations — generated component */
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap');

*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --text-primary: {text_primary};
    --text-muted: {text_muted};
    --accent: {accent_color};
    --surface: {surface_color};
    --border: {border_color};
    --max-width: {width_px}px;
}}

body {{
    font-family: 'Poppins', sans-serif;
    background: var(--bg);
    color: var(--text-primary);
    min-height: 100vh;
    padding-bottom: 5rem;
}}

/* Presentation wrapper */
.page-container {{
    max-width: var(--max-width);
    margin: 0 auto;
    padding: 2rem;
}}

.header {{
    text-align: center;
    margin-bottom: 4rem;
}}

.header h1 {{ font-size: 2.5rem; margin-bottom: 0.5rem; }}
.header p {{ color: var(--text-muted); font-size: 1.1rem; }}

.section-title {{
    margin: 3rem 0 1rem;
    font-size: 1.2rem;
    color: var(--accent);
    letter-spacing: 1px;
    text-transform: uppercase;
}}

/* Base Navbar Styles (Shared) */
.nav-wrapper {{
    width: 100%;
    padding: 1rem 5%;
    background: var(--surface);
    border-bottom: 1px solid var(--border);
    backdrop-filter: blur(15px);
    -webkit-backdrop-filter: blur(15px);
    border-radius: 8px; /* Added for aesthetic framing in showcase */
    display: flex;
    align-items: center;
}}

.logo {{
    font-size: 1.8rem;
    font-weight: 700;
    color: var(--accent);
    letter-spacing: 1px;
    cursor: pointer;
}}

.nav-links {{
    display: flex;
    gap: 2rem;
    list-style: none;
}}

.nav-links li a {{
    position: relative;
    font-size: 1.05rem;
    font-weight: 500;
    text-decoration: none;
    color: var(--text-muted);
    transition: all 0.3s ease;
}}

.nav-links li a:hover {{
    color: var(--accent);
    text-shadow: 0 0 10px var(--accent);
}}

.btn-container {{
    display: flex;
}}

.btn-login {{
    padding: 0.5rem 1.5rem;
    border-radius: 30px;
    font-weight: 600;
    font-size: 1rem;
    background: var(--accent);
    color: var(--bg);
    border: none;
    cursor: pointer;
    transition: all 0.3s ease;
    box-shadow: 0 0 15px var(--accent);
}}

.btn-login:hover {{
    filter: brightness(0.9);
    box-shadow: 0 0 25px var(--accent);
}}

/* =========================================
   Flexbox Variations (The Core Skill)
   ========================================= */

/* Type 1: Space Between (Default distributed) */
.nav-type-1 {{
    justify-content: space-between;
}}

/* Type 2: Flex End with Auto Margin on Logo */
.nav-type-2 {{
    justify-content: flex-end;
}}
.nav-type-2 .logo {{
    margin-right: auto;
}}
.nav-type-2 .nav-links {{
    margin-right: 30px;
}}

/* Type 3: Grouped (Logo + Links) on left, Button on right */
.nav-type-3 {{
    justify-content: space-between;
}}
.nav-type-3 .nav-group {{
    display: flex;
    align-items: center;
    gap: 2rem;
}}

/* Type 4: Links Left, Logo Center, Button Right */
.nav-type-4 {{
    justify-content: space-between;
}}
.nav-type-4 .logo {{
    /* Offset margin to visually center between unequally sized left/right blocks */
    margin-right: clamp(2rem, 10vw, 15rem); 
}}

/* Type 5: Center Aligned, Split Links, No Button */
.nav-type-5 {{
    justify-content: center;
    gap: 3rem;
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
<body>
    <div class="page-container">
        <header class="header">
            <h1>{title_text}</h1>
            <p>{body_text}</p>
        </header>

        <!-- TYPE 1 -->
        <h2 class="section-title">Type 1: Space Between</h2>
        <nav class="nav-wrapper nav-type-1">
            <div class="logo">CSSnippets</div>
            <ul class="nav-links">
                <li><a href="#">Home</a></li>
                <li><a href="#">Services</a></li>
                <li><a href="#">Portfolio</a></li>
                <li><a href="#">About</a></li>
            </ul>
            <div class="btn-container">
                <button class="btn-login">Login</button>
            </div>
        </nav>

        <!-- TYPE 2 -->
        <h2 class="section-title">Type 2: Flex End + Auto Margin</h2>
        <nav class="nav-wrapper nav-type-2">
            <div class="logo">CSSnippets</div>
            <ul class="nav-links">
                <li><a href="#">Home</a></li>
                <li><a href="#">Services</a></li>
                <li><a href="#">Portfolio</a></li>
                <li><a href="#">About</a></li>
            </ul>
            <div class="btn-container">
                <button class="btn-login">Login</button>
            </div>
        </nav>

        <!-- TYPE 3 -->
        <h2 class="section-title">Type 3: Left Grouping</h2>
        <nav class="nav-wrapper nav-type-3">
            <div class="nav-group">
                <div class="logo">CSSnippets</div>
                <ul class="nav-links">
                    <li><a href="#">Home</a></li>
                    <li><a href="#">Services</a></li>
                    <li><a href="#">Portfolio</a></li>
                    <li><a href="#">About</a></li>
                </ul>
            </div>
            <div class="btn-container">
                <button class="btn-login">Login</button>
            </div>
        </nav>

        <!-- TYPE 4 -->
        <h2 class="section-title">Type 4: Centered Logo (HTML Reordered)</h2>
        <nav class="nav-wrapper nav-type-4">
            <ul class="nav-links">
                <li><a href="#">Home</a></li>
                <li><a href="#">Services</a></li>
                <li><a href="#">Portfolio</a></li>
                <li><a href="#">About</a></li>
            </ul>
            <div class="logo">CSSnippets</div>
            <div class="btn-container">
                <button class="btn-login">Login</button>
            </div>
        </nav>

        <!-- TYPE 5 -->
        <h2 class="section-title">Type 5: Symmetrical Split (No Button)</h2>
        <nav class="nav-wrapper nav-type-5">
            <ul class="nav-links">
                <li><a href="#">Home</a></li>
                <li><a href="#">Services</a></li>
            </ul>
            <div class="logo">CSSnippets</div>
            <ul class="nav-links">
                <li><a href="#">Portfolio</a></li>
                <li><a href="#">About</a></li>
            </ul>
        </nav>

    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Flexbox Navbar layout logic is purely CSS-driven.
// This script exists to initialize interactions if mobile menus were added.
document.addEventListener('DOMContentLoaded', () => {{
    console.log('{title_text} loaded successfully.');
    // In a full production scenario, hamburger menu toggle logic would go here.
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
