def create_component(
    output_dir: str,
    title_text: str = "Flexbox Navbar Variations",
    body_text: str = "Scroll down to see the glassmorphism effect against the background.",
    color_scheme: str = "dark",
    accent_color: str = "#38bdf8",
    width_px: int = 1200,
    height_px: int = 900,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing 5 Flexbox Navbar layout patterns.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Theme colors based on selection
    if color_scheme == "dark":
        bg_gradient = "radial-gradient(circle at top right, #1e293b, #020617 80%)"
        text_primary = "#f8fafc"
        text_secondary = "#94a3b8"
        nav_bg = "rgba(255, 255, 255, 0.03)"
        nav_border = "rgba(255, 255, 255, 0.08)"
        btn_text = "#020617"
    else:
        bg_gradient = "radial-gradient(circle at top right, #e2e8f0, #f8fafc 80%)"
        text_primary = "#0f172a"
        text_secondary = "#475569"
        nav_bg = "rgba(0, 0, 0, 0.03)"
        nav_border = "rgba(0, 0, 0, 0.08)"
        btn_text = "#ffffff"

    # Hex to RGBA helper for glow effects
    def hex_to_rgba(hex_code, alpha):
        hex_code = hex_code.lstrip('#')
        if len(hex_code) == 3:
            hex_code = ''.join([c*2 for c in hex_code])
        rgb = tuple(int(hex_code[i:i+2], 16) for i in (0, 2, 4))
        return f"rgba({rgb[0]}, {rgb[1]}, {rgb[2]}, {alpha})"
    
    accent_glow = hex_to_rgba(accent_color, 0.6)

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <!-- Background decorative elements for glassmorphism demonstration -->
    <div class="bg-orb orb-1"></div>
    <div class="bg-orb orb-2"></div>

    <div class="page-container">
        <header class="header-intro">
            <h1>{title_text}</h1>
            <p>{body_text}</p>
        </header>

        <!-- Layout 1: Space Between (Standard) -->
        <div class="label">Type 1: Space Between (Left - Center - Right)</div>
        <nav class="nav-type-1">
            <div class="logo">Brand<span>.</span></div>
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

        <!-- Layout 2: Right Aligned (Auto Margin) -->
        <div class="label">Type 2: Right Aligned Links (Margin-Right: Auto on Logo)</div>
        <nav class="nav-type-2">
            <div class="logo">Brand<span>.</span></div>
            <ul class="nav-links">
                <li><a href="#">Home</a></li>
                <li><a href="#">Services</a></li>
                <li><a href="#">Portfolio</a></li>
            </ul>
            <div class="btns">
                <button class="btn">Login</button>
            </div>
        </nav>

        <!-- Layout 3: Grouped Left -->
        <div class="label">Type 3: Grouped Left (Flex Wrapper around Logo & Links)</div>
        <nav class="nav-type-3">
            <div class="nav-group">
                <div class="logo">Brand<span>.</span></div>
                <ul class="nav-links">
                    <li><a href="#">Home</a></li>
                    <li><a href="#">Services</a></li>
                    <li><a href="#">About</a></li>
                </ul>
            </div>
            <div class="btns">
                <button class="btn">Login</button>
            </div>
        </nav>

        <!-- Layout 4: Logo Centered (Equal Flex Columns) -->
        <div class="label">Type 4: Logo Centered (Using flex: 1 columns)</div>
        <nav class="nav-type-4">
            <ul class="nav-links col-left">
                <li><a href="#">Home</a></li>
                <li><a href="#">Services</a></li>
            </ul>
            <div class="logo col-center">Brand<span>.</span></div>
            <div class="btns col-right">
                <button class="btn">Login</button>
            </div>
        </nav>

        <!-- Layout 5: Split Links -->
        <div class="label">Type 5: Split Links (Justify Center with Gap)</div>
        <nav class="nav-type-5">
            <ul class="nav-links">
                <li><a href="#">Home</a></li>
                <li><a href="#">Services</a></li>
            </ul>
            <div class="logo">Brand<span>.</span></div>
            <ul class="nav-links">
                <li><a href="#">Portfolio</a></li>
                <li><a href="#">Contact</a></li>
            </ul>
        </nav>
        
        <div class="spacer"></div>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    css = f"""/* Base Reset */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --accent: {accent_color};
    --accent-glow: {accent_glow};
    --text-primary: {text_primary};
    --text-secondary: {text_secondary};
    --nav-bg: {nav_bg};
    --nav-border: {nav_border};
    --btn-text: {btn_text};
}}

body {{
    font-family: 'Poppins', sans-serif;
    background: {bg_gradient};
    color: var(--text-primary);
    min-height: 100vh;
    overflow-x: hidden;
    position: relative;
}}

/* Background Orbs to demonstrate glassmorphism */
.bg-orb {{
    position: fixed;
    border-radius: 50%;
    filter: blur(80px);
    z-index: -1;
    opacity: 0.5;
}}
.orb-1 {{
    width: 400px;
    height: 400px;
    background: var(--accent);
    top: -100px;
    left: -100px;
}}
.orb-2 {{
    width: 300px;
    height: 300px;
    background: #8b5cf6;
    bottom: 20%;
    right: -50px;
}}

.page-container {{
    max-width: {width_px}px;
    margin: 0 auto;
    padding: 2rem;
}}

.header-intro {{
    text-align: center;
    margin-bottom: 4rem;
}}

.header-intro h1 {{
    font-size: 2.5rem;
    font-weight: 700;
    margin-bottom: 0.5rem;
}}

.header-intro p {{
    color: var(--text-secondary);
}}

.label {{
    font-size: 0.85rem;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: var(--text-secondary);
    margin-bottom: 0.5rem;
    margin-left: 1rem;
    font-weight: 600;
}}

.spacer {{
    height: 10vh;
}}

/* =========================================
   COMMON NAVBAR STYLES (The Glassmorphism)
   ========================================= */
nav {{
    width: 100%;
    padding: 1rem 2.5rem;
    background: var(--nav-bg);
    border: 1px solid var(--nav-border);
    border-radius: 12px;
    backdrop-filter: blur(15px);
    -webkit-backdrop-filter: blur(15px);
    margin-bottom: 3rem;
}}

.logo {{
    font-size: 1.6rem;
    font-weight: 700;
    color: var(--text-primary);
    letter-spacing: 1px;
    white-space: nowrap;
}}

.logo span {{
    color: var(--accent);
    text-shadow: 0 0 10px var(--accent-glow);
}}

.nav-links {{
    display: flex;
    list-style: none;
    gap: 2.5rem;
}}

.nav-links li a {{
    color: var(--text-secondary);
    text-decoration: none;
    font-weight: 500;
    font-size: 0.95rem;
    transition: all 0.3s ease;
    position: relative;
}}

.nav-links li a:hover {{
    color: var(--accent);
    text-shadow: 0 0 8px var(--accent-glow);
}}

.btns {{
    display: flex;
    align-items: center;
}}

.btn {{
    padding: 0.6rem 1.8rem;
    border-radius: 30px;
    font-family: inherit;
    font-weight: 600;
    font-size: 0.95rem;
    background: var(--accent);
    color: var(--btn-text);
    border: none;
    cursor: pointer;
    transition: all 0.3s ease;
    box-shadow: 0 4px 15px var(--accent-glow);
}}

.btn:hover {{
    transform: translateY(-2px);
    box-shadow: 0 8px 25px var(--accent-glow);
    filter: brightness(1.1);
}}


/* =========================================
   LAYOUT SPECIFIC FLEXBOX PATTERNS
   ========================================= */

/* Type 1: Space Between */
.nav-type-1 {{
    display: flex;
    align-items: center;
    justify-content: space-between;
}}

/* Type 2: Right Aligned Links */
.nav-type-2 {{
    display: flex;
    align-items: center;
    justify-content: flex-end; /* Push items to end */
    gap: 2.5rem; /* Gap between links and button */
}}
.nav-type-2 .logo {{
    margin-right: auto; /* Consumes remaining left space, pushing everything right */
}}

/* Type 3: Grouped Left */
.nav-type-3 {{
    display: flex;
    align-items: center;
    justify-content: space-between;
}}
.nav-type-3 .nav-group {{
    display: flex;
    align-items: center;
    gap: 3rem; /* Spacing between Logo and Links */
}}

/* Type 4: Logo Centered (Robust Column Approach) */
.nav-type-4 {{
    display: flex;
    align-items: center;
    justify-content: space-between;
}}
.nav-type-4 > * {{
    flex: 1; /* Assigns equal width to all 3 columns */
}}
.col-left {{
    justify-content: flex-start;
}}
.col-center {{
    display: flex;
    justify-content: center;
}}
.col-right {{
    justify-content: flex-end;
}}

/* Type 5: Split Links */
.nav-type-5 {{
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 4rem; /* Defines space around the central logo */
}}

/* Responsive behavior */
@media (max-width: 900px) {{
    nav {{
        padding: 1rem;
    }}
    .nav-links {{
        display: none; /* Hide links on smaller screens for this demo */
    }}
    .nav-type-4 > *, .nav-type-5 {{
        justify-content: space-between;
    }}
}}
"""

    js = """// Flexbox Navbar Variations
document.addEventListener('DOMContentLoaded', () => {
    // Optional: Add scroll effect to show dynamic backdrop-filter
    const navs = document.querySelectorAll('nav');
    
    // Smooth appearance animation
    navs.forEach((nav, index) => {
        nav.style.opacity = '0';
        nav.style.transform = 'translateY(20px)';
        nav.style.transition = 'all 0.6s cubic-bezier(0.16, 1, 0.3, 1)';
        
        setTimeout(() => {
            nav.style.opacity = '1';
            nav.style.transform = 'translateY(0)';
        }, 150 * (index + 1));
    });
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
