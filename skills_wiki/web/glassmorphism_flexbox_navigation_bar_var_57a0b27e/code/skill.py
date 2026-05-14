def create_component(
    output_dir: str,
    title_text: str = "Flexbox Navbar Variations",
    body_text: str = "Showcasing 5 distinct navigation layouts using CSS Flexbox and Glassmorphism.",
    color_scheme: str = "dark",
    accent_color: str = "#38bdf8",
    width_px: int = 1200,
    height_px: int = 1000,
    **kwargs,
) -> dict:
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Derive theme colors
    if color_scheme == "dark":
        bg_color = "#0f172a"
        text_color = "#f8fafc"
        text_muted = "#e2e8f0"
        surface_color = "rgba(255, 255, 255, 0.05)"
        border_color = "rgba(255, 255, 255, 0.1)"
        btn_text = bg_color  # Dark text on bright accent button
    else:
        bg_color = "#f8fafc"
        text_color = "#0f172a"
        text_muted = "#475569"
        surface_color = "rgba(0, 0, 0, 0.03)"
        border_color = "rgba(0, 0, 0, 0.1)"
        btn_text = "#ffffff" # Light text on accent button

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
}}

body {{
    font-family: 'Poppins', system-ui, -apple-system, sans-serif;
    background-color: var(--bg);
    color: var(--text);
    min-height: 100vh;
    padding: 3rem 0;
    /* Subtle background ambient orbs to enhance glassmorphism visibility */
    background-image: 
        radial-gradient(circle at 10% 20%, rgba(56, 189, 248, 0.15), transparent 40%),
        radial-gradient(circle at 90% 80%, rgba(56, 189, 248, 0.15), transparent 40%);
    background-attachment: fixed;
}}

.container {{
    width: 100%;
    max-width: {width_px}px;
    margin: 0 auto;
    padding: 0 2rem;
}}

.header {{
    text-align: center;
    margin-bottom: 4rem;
}}

.header h1 {{
    font-size: 2.5rem;
    margin-bottom: 0.5rem;
}}

.header p {{
    color: var(--text-muted);
    font-size: 1.1rem;
}}

.variation-label {{
    font-size: 0.85rem;
    color: var(--text-muted);
    margin-bottom: 0.8rem;
    text-transform: uppercase;
    letter-spacing: 2px;
    font-weight: 600;
}}

/* Base Navbar Styling */
nav {{
    width: 100%;
    padding: 1rem 2rem;
    background: var(--surface);
    border-bottom: 1px solid var(--border);
    border-radius: 12px;
    backdrop-filter: blur(15px);
    -webkit-backdrop-filter: blur(15px);
    margin-bottom: 4rem;
    display: flex;
    align-items: center;
}}

.logo {{
    font-size: 1.8rem;
    font-weight: 700;
    color: var(--accent);
    letter-spacing: 1px;
}}

.nav-links {{
    list-style: none;
    display: flex;
    gap: 2rem;
}}

.nav-links li a {{
    position: relative;
    font-size: 1.05rem;
    font-weight: 500;
    text-decoration: none;
    color: var(--text-muted);
    transition: 0.3s ease;
}}

.nav-links li a:hover,
.nav-links li a.active {{
    color: var(--accent);
    text-shadow: 0 0 10px var(--accent);
}}

.btns {{
    display: flex;
}}

.btn {{
    padding: 0.5rem 1.5rem;
    border-radius: 30px;
    font-weight: 600;
    font-size: 1rem;
    background: var(--accent);
    color: var(--btn-text);
    box-shadow: 0 0 15px var(--accent);
    border: none;
    cursor: pointer;
    transition: 0.3s ease;
    font-family: inherit;
}}

.btn:hover {{
    filter: brightness(1.15);
    box-shadow: 0 0 25px var(--accent);
}}

/* =========================================
   FLEXBOX LAYOUT VARIATIONS
========================================= */

/* Layout 1: Space Between (Classic) */
.nav-1 {{
    justify-content: space-between;
}}

/* Layout 2: Right Aligned (Flex End + Auto Margin) */
.nav-2 {{
    justify-content: flex-end;
}}
.nav-2 .logo {{
    margin-right: auto; /* Pushes everything else to the right */
}}
.nav-2 .nav-links {{
    margin-right: 2rem; /* Spacing between links and button */
}}

/* Layout 3: Left Grouped (Nested Flex Wrapper) */
.nav-3 {{
    justify-content: space-between;
}}
.nav-group {{
    display: flex;
    align-items: center;
    gap: 3rem;
}}

/* Layout 4: Centered Logo (Proportional Flex Allocation) */
.nav-4 {{
    justify-content: space-between;
}}
.nav-4 .nav-links {{
    flex: 1; /* Consumes exact same space as right flex item */
}}
.nav-4 .btns {{
    flex: 1;
    justify-content: flex-end; /* Aligns button to far right */
}}
.nav-4 .logo {{
    text-align: center;
}}

/* Layout 5: Split Links (No Button) */
.nav-5 {{
    justify-content: center;
    gap: 4rem;
}}
"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text}</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>{title_text}</h1>
            <p>{body_text}</p>
        </div>

        <div class="variation-label">Type 1: Space Between Distribution</div>
        <nav class="nav-1">
            <div class="logo">Brand</div>
            <ul class="nav-links">
                <li><a href="#" class="active">Home</a></li>
                <li><a href="#">Services</a></li>
                <li><a href="#">Portfolio</a></li>
                <li><a href="#">About</a></li>
            </ul>
            <div class="btns"><button class="btn">Login</button></div>
        </nav>

        <div class="variation-label">Type 2: Flex End + Auto Margin Push</div>
        <nav class="nav-2">
            <div class="logo">Brand</div>
            <ul class="nav-links">
                <li><a href="#" class="active">Home</a></li>
                <li><a href="#">Services</a></li>
                <li><a href="#">Portfolio</a></li>
                <li><a href="#">About</a></li>
            </ul>
            <div class="btns"><button class="btn">Login</button></div>
        </nav>

        <div class="variation-label">Type 3: Left Grouped Architecture</div>
        <nav class="nav-3">
            <div class="nav-group">
                <div class="logo">Brand</div>
                <ul class="nav-links">
                    <li><a href="#" class="active">Home</a></li>
                    <li><a href="#">Services</a></li>
                    <li><a href="#">Portfolio</a></li>
                    <li><a href="#">About</a></li>
                </ul>
            </div>
            <div class="btns"><button class="btn">Login</button></div>
        </nav>

        <div class="variation-label">Type 4: True Centered Logo Strategy</div>
        <nav class="nav-4">
            <ul class="nav-links">
                <li><a href="#" class="active">Home</a></li>
                <li><a href="#">Services</a></li>
            </ul>
            <div class="logo">Brand</div>
            <div class="btns"><button class="btn">Login</button></div>
        </nav>

        <div class="variation-label">Type 5: Split Links / Symmetrical</div>
        <nav class="nav-5">
            <ul class="nav-links">
                <li><a href="#" class="active">Home</a></li>
                <li><a href="#">Services</a></li>
            </ul>
            <div class="logo">Brand</div>
            <ul class="nav-links">
                <li><a href="#">Portfolio</a></li>
                <li><a href="#">About</a></li>
            </ul>
        </nav>
    </div>
    
    <script src="script.js"></script>
</body>
</html>"""

    js = f"""// Navigation interactions
document.addEventListener('DOMContentLoaded', () => {{
    // Add simple click state toggling to demonstrate interactivity
    const navbars = document.querySelectorAll('nav');
    
    navbars.forEach(nav => {{
        const links = nav.querySelectorAll('.nav-links a');
        
        links.forEach(link => {{
            link.addEventListener('click', (e) => {{
                e.preventDefault();
                // Remove active class from all links in this specific navbar
                links.forEach(l => l.classList.remove('active'));
                // Add active class to clicked link
                link.classList.add('active');
            }});
        }});
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
