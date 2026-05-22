def create_component(
    output_dir: str,
    title_text: str = "BrandName",
    body_text: str = "Scroll down to see the navigation bar stick to the top of the container.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#39ffde",     # CSS hex color for accent
    width_px: int = 1000,
    height_px: int = 600,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing a responsive sticky navigation bar.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors ===
    if color_scheme == "dark":
        bg_color = "#1a1a1a"
        nav_bg = "#111111"
        text_color = "#f0f0f0"
        surface_color = "#333333"
        hover_text = "#111111"
    else:
        bg_color = "#f8f9fa"
        nav_bg = "#ffffff"
        text_color = "#222222"
        surface_color = "#dddddd"
        hover_text = "#ffffff"

    # === CSS ===
    css = f"""/* Responsive Sticky Navbar */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --nav-bg: {nav_bg};
    --text: {text_color};
    --accent: {accent_color};
    --surface: {surface_color};
    --hover-text: {hover_text};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background: #444; /* Outer background to frame the component */
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
}}

/* The container acts as the 'viewport' for our component */
.device-container {{
    width: var(--width);
    height: var(--height);
    background: var(--bg);
    color: var(--text);
    position: relative;
    overflow-y: auto;
    overflow-x: hidden;
    box-shadow: 0 20px 50px rgba(0,0,0,0.5);
    border-radius: 8px;
    
    /* Establish a container query context for true component isolation */
    container-type: inline-size;
}}

/* --- Navigation Bar Styles --- */
nav {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0 30px;
    background-color: var(--nav-bg);
    position: sticky;
    top: 0;
    z-index: 100;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}}

.logo h3 {{
    font-size: 1.4rem;
    font-weight: 700;
    letter-spacing: 1px;
    padding: 20px 0;
}}

.nav-links {{
    display: flex;
    list-style: none;
    align-items: center;
}}

.nav-links li a {{
    display: block;
    padding: 25px 16px;
    text-decoration: none;
    color: var(--text);
    text-transform: uppercase;
    font-size: 0.85rem;
    font-weight: 600;
    letter-spacing: 0.5px;
    transition: all 0.2s ease-in-out;
}}

.nav-links li a:hover {{
    background-color: var(--accent);
    color: var(--hover-text);
}}

.nav-cta-button {{
    margin-left: 15px;
    border: 2px solid var(--accent);
    padding: 10px 20px !important;
    border-radius: 4px;
}}

.nav-cta-button:hover {{
    background-color: var(--accent);
    color: var(--hover-text);
}}

/* --- Hamburger Menu Styles --- */
.hamburger {{
    display: none;
    cursor: pointer;
    padding: 10px 0;
}}

.hamburger .bar {{
    width: 28px;
    height: 3px;
    background-color: var(--text);
    margin: 5px 0;
    transition: all 0.3s ease-in-out;
    border-radius: 2px;
}}

/* --- Responsive Mobile View (Triggered by Container Width) --- */
@container (max-width: 768px) {{
    nav {{
        flex-wrap: wrap;
        padding: 0 20px;
    }}
    
    .hamburger {{
        display: block;
    }}
    
    /* Transform hamburger into an 'X' when active */
    .hamburger.active .bar:nth-child(1) {{
        transform: translateY(8px) rotate(45deg);
    }}
    .hamburger.active .bar:nth-child(2) {{
        opacity: 0;
    }}
    .hamburger.active .bar:nth-child(3) {{
        transform: translateY(-8px) rotate(-45deg);
    }}
    
    .nav-links {{
        display: none; /* Hidden by default on mobile */
        width: 100%;
        flex-direction: column;
        border-top: 1px solid var(--surface);
    }}
    
    .nav-links.active {{
        display: flex; /* Shown when hamburger is clicked */
    }}
    
    .nav-links li {{
        width: 100%;
        text-align: center;
    }}
    
    .nav-links li a {{
        padding: 16px;
    }}
    
    .nav-cta-button {{
        margin: 10px auto 20px auto;
        display: inline-block !important;
    }}
}}

/* --- Main Content Simulation --- */
.content {{
    padding: 50px 30px;
}}

.content h1 {{
    font-size: 2.5rem;
    margin-bottom: 20px;
}}

.content p {{
    font-size: 1.1rem;
    line-height: 1.6;
    color: var(--text);
    opacity: 0.8;
}}

.scroll-spacer {{
    height: 1200px;
    margin-top: 40px;
    border-radius: 8px;
    background: repeating-linear-gradient(
      45deg,
      transparent,
      transparent 20px,
      var(--surface) 20px,
      var(--surface) 40px
    );
    opacity: 0.3;
}}
"""

    # === HTML ===
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text} Navigation</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="device-container">
        
        <nav>
            <div class="logo">
                <h3>{title_text}</h3>
            </div>
            
            <div class="hamburger" aria-label="Toggle navigation">
                <div class="bar"></div>
                <div class="bar"></div>
                <div class="bar"></div>
            </div>
            
            <ul class="nav-links">
                <li><a href="#home">Home</a></li>
                <li><a href="#about">About</a></li>
                <li><a href="#cases">Cases</a></li>
                <li><a href="#services">Services</a></li>
                <li><a href="#contact" class="nav-cta-button">Contact</a></li>
            </ul>
        </nav>

        <main class="content">
            <h1>Welcome to {title_text}</h1>
            <p>{body_text}</p>
            <p><strong>Note:</strong> To test the mobile responsiveness, set the Python function parameter `width_px` to a value under 768px.</p>
            
            <div class="scroll-spacer"></div>
        </main>

    </div>
    
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Responsive Navigation Logic
document.addEventListener('DOMContentLoaded', () => {{
    const hamburger = document.querySelector('.hamburger');
    const navLinks = document.querySelector('.nav-links');

    if (hamburger && navLinks) {{
        // Toggle mobile menu visibility
        hamburger.addEventListener('click', () => {{
            hamburger.classList.toggle('active');
            navLinks.classList.toggle('active');
        }});

        // Close mobile menu when a link is clicked
        const links = navLinks.querySelectorAll('a');
        links.forEach(link => {{
            link.addEventListener('click', () => {{
                hamburger.classList.remove('active');
                navLinks.classList.remove('active');
            }});
        }});
    }}
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
