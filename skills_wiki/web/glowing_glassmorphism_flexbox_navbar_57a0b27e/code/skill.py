def create_component(
    output_dir: str,
    title_text: str = "DevSnippets",
    body_text: str = "",
    color_scheme: str = "dark",
    accent_color: str = "#38bdf8",
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Glowing Glassmorphism Flexbox Navbar.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Derive theme colors dynamically
    if color_scheme == "dark":
        bg_color = "#0f172a"          # Slate 900
        bg_accent = "#1e293b"         # Slate 800
        text_color = "#e2e8f0"        # Slate 200
        nav_bg = "rgba(255, 255, 255, 0.05)"
        nav_border = "rgba(255, 255, 255, 0.1)"
        btn_text = "#0f172a"
        btn_hover_bg = "#0ea5e9"      # Darker cyan
    else:
        bg_color = "#f8fafc"          # Slate 50
        bg_accent = "#e2e8f0"         # Slate 200
        text_color = "#334155"        # Slate 700
        nav_bg = "rgba(0, 0, 0, 0.05)"
        nav_border = "rgba(0, 0, 0, 0.1)"
        btn_text = "#ffffff"
        btn_hover_bg = "#0284c7"

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text} - Navbar</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="view-container">
        <!-- Floating shapes to demonstrate glassmorphism blur -->
        <div class="bg-shape shape-1"></div>
        <div class="bg-shape shape-2"></div>

        <nav class="navbar">
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
        
        <main class="hero-content">
            <h1>Welcome to {title_text}</h1>
            <p>Scroll down or hover over the navigation items to experience the Flexbox layout and glowing glassmorphism effects.</p>
        </main>
    </div>

    <script src="script.js"></script>
</body>
</html>"""

    css = f"""/* Base & Reset */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg-color: {bg_color};
    --bg-accent: {bg_accent};
    --text-color: {text_color};
    --accent-color: {accent_color};
    --nav-bg: {nav_bg};
    --nav-border: {nav_border};
    --btn-text: {btn_text};
    --btn-hover-bg: {btn_hover_bg};
}}

body {{
    font-family: 'Poppins', sans-serif;
    background-color: var(--bg-color);
    color: var(--text-color);
    min-height: 100vh;
    overflow-x: hidden;
}}

/* Container sizing explicitly to requested dimensions */
.view-container {{
    width: 100%;
    max-width: {width_px}px;
    min-height: {height_px}px;
    margin: 0 auto;
    position: relative;
    padding-top: 2rem;
}}

/* Background shapes to highlight the blur effect */
.bg-shape {{
    position: absolute;
    border-radius: 50%;
    filter: blur(80px);
    z-index: -1;
    opacity: 0.6;
}}
.shape-1 {{
    width: 400px;
    height: 400px;
    background: var(--accent-color);
    top: -100px;
    left: -100px;
}}
.shape-2 {{
    width: 300px;
    height: 300px;
    background: #8b5cf6; /* Complementary purple */
    bottom: 100px;
    right: 50px;
}}

/* =========================================
   Flexbox Navbar Styling (Type 1 Layout)
   ========================================= */
.navbar {{
    width: 100%;
    padding: 1rem 5%;
    background: var(--nav-bg);
    border: 1px solid var(--nav-border);
    border-radius: 12px;
    
    /* Glassmorphism */
    -webkit-backdrop-filter: blur(15px);
    backdrop-filter: blur(15px);
    
    /* Flexbox Layout Mechanics */
    display: flex;
    align-items: center;
    justify-content: space-between;
    
    /* Layout transition for responsiveness */
    transition: all 0.3s ease;
}}

/* Brand Logo */
.logo {{
    font-size: 1.8rem;
    font-weight: 700;
    color: var(--accent-color);
    letter-spacing: 1px;
    cursor: pointer;
}}

/* Navigation Links */
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
    color: var(--text-color);
    transition: color 0.3s ease, text-shadow 0.3s ease;
}}

.nav-links li a:hover {{
    color: var(--accent-color);
    text-shadow: 0 0 10px var(--accent-color);
}}

/* Action Button Container */
.btns {{
    display: flex;
}}

/* Action Button Styling */
.btn {{
    padding: 0.5rem 1.5rem;
    border-radius: 30px;
    font-weight: 600;
    font-size: 1rem;
    background: var(--accent-color);
    color: var(--btn-text);
    border: none;
    cursor: pointer;
    box-shadow: 0 0 15px var(--accent-color);
    transition: background 0.3s ease, box-shadow 0.3s ease, transform 0.1s ease;
    font-family: inherit;
}}

.btn:hover {{
    background: var(--btn-hover-bg);
    box-shadow: 0 0 25px var(--btn-hover-bg);
}}

.btn:active {{
    transform: scale(0.95);
}}

/* Dummy Content below Navbar */
.hero-content {{
    margin-top: 6rem;
    text-align: center;
    padding: 0 2rem;
}}

.hero-content h1 {{
    font-size: 3rem;
    margin-bottom: 1rem;
}}

.hero-content p {{
    font-size: 1.2rem;
    opacity: 0.8;
    max-width: 600px;
    margin: 0 auto;
    line-height: 1.6;
}}

/* Simple Responsive Adaptation */
@media (max-width: 768px) {{
    .navbar {{
        flex-direction: column;
        gap: 1.5rem;
        padding: 1.5rem 5%;
    }}
    .nav-links {{
        flex-wrap: wrap;
        justify-content: center;
        gap: 1rem;
    }}
}}
"""

    js = """// Flexbox Navbar Interaction Logic
document.addEventListener('DOMContentLoaded', () => {
    // Add subtle click effects to nav links
    const navLinks = document.querySelectorAll('.nav-links a');
    
    navLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault(); // Prevent jump to top for demo
            
            // Remove active style from all, apply to clicked
            navLinks.forEach(l => {
                l.style.color = '';
                l.style.textShadow = '';
            });
            
            e.target.style.color = getComputedStyle(document.documentElement).getPropertyValue('--accent-color').trim();
            e.target.style.textShadow = `0 0 10px ${e.target.style.color}`;
        });
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
