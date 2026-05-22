def create_component(
    output_dir: str,
    title_text: str = "CSSnippets",
    body_text: str = "Explore five standard Flexbox navigation patterns.",
    color_scheme: str = "dark",        
    accent_color: str = "#38bdf8",     
    width_px: int = 1200,
    height_px: int = 1000,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the 5 Flexbox Glassmorphism Navbars.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    if color_scheme == "dark":
        bg_color = "#0f172a"
        text_color = "#ffffff"
        text_muted = "#94a3b8"
        surface_color = "rgba(255, 255, 255, 0.05)"
        border_color = "rgba(255, 255, 255, 0.1)"
        btn_text = "#0f172a"
        blob_color2 = "#8b5cf6" 
    else:
        bg_color = "#f0f4f8"
        text_color = "#0f172a"
        text_muted = "#475569"
        surface_color = "rgba(255, 255, 255, 0.6)"
        border_color = "rgba(255, 255, 255, 0.8)"
        btn_text = "#ffffff"
        blob_color2 = "#3b82f6" 

    css = f"""/* Glassmorphism Flexbox Navbars */
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap');

*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --text: {text_color};
    --text-muted: {text_muted};
    --accent: {accent_color};
    --surface: {surface_color};
    --border: {border_color};
    --btn-text: {btn_text};
    --blob-2: {blob_color2};
}}

body {{
    font-family: 'Poppins', system-ui, sans-serif;
    background: var(--bg);
    color: var(--text);
    min-height: 100vh;
    overflow-x: hidden;
    position: relative;
}}

/* Ambient Background to showcase Glassmorphism */
.blob {{
    position: fixed;
    border-radius: 50%;
    filter: blur(100px);
    z-index: -1;
    pointer-events: none;
}}
.blob-1 {{
    top: 10%; left: -5%; width: 40vw; height: 40vw;
    background: var(--accent);
    opacity: 0.15;
}}
.blob-2 {{
    bottom: 10%; right: -5%; width: 35vw; height: 35vw;
    background: var(--blob-2);
    opacity: 0.15;
}}

.container {{
    width: 100%;
    max-width: {width_px}px;
    margin: 0 auto;
    padding: 3rem 2rem;
    position: relative;
    z-index: 1;
}}

.header-text {{
    text-align: center;
    margin-bottom: 3rem;
}}
.header-text h1 {{ color: var(--text); font-size: 2rem; margin-bottom: 0.5rem; }}
.header-text p {{ color: var(--text-muted); font-size: 1rem; }}

.nav-label {{
    margin-bottom: 0.8rem;
    font-size: 0.85rem;
    color: var(--accent);
    text-transform: uppercase;
    letter-spacing: 2px;
    font-weight: 600;
}}

/* Base Navbar Styles */
nav {{
    width: 100%;
    padding: 1rem 3%;
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    backdrop-filter: blur(15px);
    -webkit-backdrop-filter: blur(15px);
    margin-bottom: 4rem;
    display: flex;
    align-items: center;
    box-shadow: 0 10px 30px rgba(0,0,0,0.1);
}}

.logo {{
    font-size: 1.6rem;
    font-weight: 700;
    color: var(--accent);
    letter-spacing: 1px;
    cursor: pointer;
}}

.nav-links {{
    list-style: none;
    display: flex;
    gap: 2rem;
}}

.nav-links li a {{
    text-decoration: none;
    color: var(--text-muted);
    font-size: 1rem;
    font-weight: 500;
    transition: all 0.3s ease;
}}

.nav-links li a:hover {{
    color: var(--accent);
    text-shadow: 0 0 10px var(--accent);
}}

.btns {{
    display: flex;
}}

.btn {{
    padding: 0.6rem 1.8rem;
    border-radius: 30px;
    background: var(--accent);
    color: var(--btn-text);
    border: none;
    font-weight: 600;
    font-family: inherit;
    font-size: 0.95rem;
    cursor: pointer;
    box-shadow: 0 0 15px var(--accent);
    transition: all 0.3s ease;
}}

.btn:hover {{
    filter: brightness(1.15);
    box-shadow: 0 0 25px var(--accent);
    transform: translateY(-1px);
}}

/* --- Layout Variations --- */

/* Type 1: Space Between (Default balance) */
.nav-v1 {{
    justify-content: space-between;
}}

/* Type 2: Flex End (Logo pushed left via auto margin) */
.nav-v2 {{
    justify-content: flex-end;
}}
.nav-v2 .logo {{
    margin-right: auto;
}}
.nav-v2 .nav-links {{
    margin-right: 2rem;
}}

/* Type 3: Grouped Left (Wrapper aligns logo & links) */
.nav-v3 {{
    justify-content: space-between;
}}
.nav-v3 .nav-group {{
    display: flex;
    align-items: center;
    gap: 2rem;
}}

/* Type 4: Centered Logo 
   Improved over tutorial: uses flex: 1 on children instead of fixed margins 
   to ensure perfect centering on all screen sizes. */
.nav-v4 {{
    justify-content: space-between;
}}
.nav-v4 > * {{
    flex: 1;
    display: flex;
    align-items: center;
}}
.nav-v4 .nav-links {{
    justify-content: flex-start;
}}
.nav-v4 .logo {{
    justify-content: center;
}}
.nav-v4 .btns {{
    justify-content: flex-end;
}}

/* Type 5: Split Links (Logo in middle, no button) */
.nav-v5 {{
    justify-content: center;
    gap: 3rem;
}}
"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text} - Flexbox Navbars</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="blob blob-1"></div>
    <div class="blob blob-2"></div>
    
    <div class="container">
        <div class="header-text">
            <h1>{title_text} Layouts</h1>
            <p>{body_text}</p>
        </div>

        <!-- Type 1: Space Between -->
        <h3 class="nav-label">Navbar Type-1 (Space Between)</h3>
        <nav class="nav-v1">
            <div class="logo">{title_text}</div>
            <ul class="nav-links">
                <li><a href="#">Home</a></li>
                <li><a href="#">Services</a></li>
                <li><a href="#">Portfolio</a></li>
                <li><a href="#">About</a></li>
            </ul>
            <div class="btns">
                <button class="btn">Login</button>
            </div>
        </nav>

        <!-- Type 2: Flex End with Auto Margin -->
        <h3 class="nav-label">Navbar Type-2 (Flex End & Margin Auto)</h3>
        <nav class="nav-v2">
            <div class="logo">{title_text}</div>
            <ul class="nav-links">
                <li><a href="#">Home</a></li>
                <li><a href="#">Services</a></li>
                <li><a href="#">Portfolio</a></li>
                <li><a href="#">About</a></li>
            </ul>
            <div class="btns">
                <button class="btn">Login</button>
            </div>
        </nav>

        <!-- Type 3: Grouped Left -->
        <h3 class="nav-label">Navbar Type-3 (Grouped Items)</h3>
        <nav class="nav-v3">
            <div class="nav-group">
                <div class="logo">{title_text}</div>
                <ul class="nav-links">
                    <li><a href="#">Home</a></li>
                    <li><a href="#">Services</a></li>
                    <li><a href="#">Portfolio</a></li>
                    <li><a href="#">About</a></li>
                </ul>
            </div>
            <div class="btns">
                <button class="btn">Login</button>
            </div>
        </nav>

        <!-- Type 4: Centered Logo -->
        <h3 class="nav-label">Navbar Type-4 (Centered Logo)</h3>
        <nav class="nav-v4">
            <ul class="nav-links">
                <li><a href="#">Home</a></li>
                <li><a href="#">Services</a></li>
                <li><a href="#">Portfolio</a></li>
                <li><a href="#">About</a></li>
            </ul>
            <div class="logo">{title_text}</div>
            <div class="btns">
                <button class="btn">Login</button>
            </div>
        </nav>

        <!-- Type 5: Split Links -->
        <h3 class="nav-label">Navbar Type-5 (Split Links)</h3>
        <nav class="nav-v5">
            <ul class="nav-links">
                <li><a href="#">Home</a></li>
                <li><a href="#">Services</a></li>
            </ul>
            <div class="logo">{title_text}</div>
            <ul class="nav-links">
                <li><a href="#">Portfolio</a></li>
                <li><a href="#">About</a></li>
            </ul>
        </nav>

    </div>
    <script src="script.js"></script>
</body>
</html>"""

    js = """// Interaction logic (Empty as effect is entirely CSS-based)
document.addEventListener('DOMContentLoaded', () => {
    // Navbars act as structural templates. 
    // Additional mobile hamburger menu toggling would be implemented here if required.
    console.log("Flexbox Navbars initialized.");
});
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
