def create_component(
    output_dir: str,
    title_text: str = "BrandName",
    body_text: str = "Scroll down to see the sticky navigation bar in action. This is placeholder content to demonstrate the viewport scrolling.",
    color_scheme: str = "dark",
    accent_color: str = "#39ffde",
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Responsive Flexbox Navigation visual effect.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os
    import html

    os.makedirs(output_dir, exist_ok=True)

    # Escape user text
    safe_title = html.escape(title_text)
    safe_body = html.escape(body_text)

    # Color scheme logic
    if color_scheme == "dark":
        bg_color = "#121212"
        text_color = "#e0e0e0"
        nav_bg = "#1f1f1f"
        nav_text = "#ffffff"
        hover_text = "#000000"
    else:
        bg_color = "#f4f4f4"
        text_color = "#333333"
        nav_bg = "#ffffff"
        nav_text = "#111111"
        hover_text = "#ffffff"

    # Repeat body text to ensure scrollability
    repeated_body = "<br><br>".join([safe_body] * 12)

    # === CSS ===
    css = f"""/* Responsive Flexbox Navigation */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --text: {text_color};
    --nav-bg: {nav_bg};
    --nav-text: {nav_text};
    --accent: {accent_color};
    --hover-text: {hover_text};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background: #333; /* Outer sandbox background */
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 100vh;
}}

/* Simulates the browser window to respect width_px/height_px */
#app-container {{
    width: var(--width);
    max-width: 100%;
    height: var(--height);
    background: var(--bg);
    color: var(--text);
    box-shadow: 0 10px 40px rgba(0,0,0,0.4);
    display: flex;
    flex-direction: column;
    overflow: hidden;
}}

.viewport-content {{
    flex: 1;
    overflow-y: auto;
    container-type: inline-size; /* Enables component-level media queries */
    position: relative;
}}

/* ================= Navbar Styles ================= */
.navbar {{
    position: sticky;
    top: 0;
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0 30px;
    background-color: var(--nav-bg);
    min-height: 70px;
    z-index: 1000;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}}

.logo {{
    display: flex;
    align-items: center;
    gap: 10px;
    color: var(--nav-text);
    font-size: 1.2rem;
    font-weight: 700;
    letter-spacing: 0.5px;
}}

.logo-icon {{
    width: 24px;
    height: 24px;
    fill: var(--nav-text);
}}

.nav-links {{
    display: flex;
    align-items: center;
    list-style: none;
}}

.nav-links li a {{
    display: block;
    padding: 10px 18px;
    color: var(--nav-text);
    text-decoration: none;
    text-transform: uppercase;
    font-size: 0.85rem;
    font-weight: 500;
    letter-spacing: 1px;
    transition: background-color 0.2s ease, color 0.2s ease;
    border-radius: 4px;
}}

.nav-links li a:hover {{
    background-color: var(--accent);
    color: var(--hover-text);
}}

.nav-cta-button {{
    margin-left: 15px;
    border: 2px solid var(--accent);
    border-radius: 50px !important;
}}

.hamburger {{
    display: none; /* Hidden on desktop */
    flex-direction: column;
    justify-content: space-between;
    width: 30px;
    height: 21px;
    cursor: pointer;
}}

.hamburger .bar {{
    height: 3px;
    width: 100%;
    background-color: var(--nav-text);
    border-radius: 3px;
    transition: all 0.3s ease;
}}

/* ================= Mobile Layout (Container Query) ================= */
@container (max-width: 768px) {{
    .navbar {{
        flex-wrap: wrap;
        padding: 15px 20px;
    }}
    
    .hamburger {{
        display: flex;
    }}
    
    .nav-links {{
        display: none; /* Toggled by JS */
        flex-basis: 100%;
        flex-direction: column;
        width: 100%;
        padding-top: 15px;
    }}
    
    /* State class added via JavaScript */
    .nav-links.active {{
        display: flex;
    }}
    
    .nav-links li {{
        width: 100%;
        text-align: center;
    }}
    
    .nav-links li a {{
        padding: 15px;
        font-size: 1rem;
    }}
    
    .nav-cta-button {{
        margin-left: 0;
        margin-top: 10px;
        display: inline-block;
        width: fit-content;
        align-self: center;
    }}
}}

/* Dummy page content styling */
.page-content {{
    padding: 40px;
    max-width: 800px;
    margin: 0 auto;
    line-height: 1.6;
}}
.page-content h1 {{
    margin-bottom: 20px;
    font-size: 2.5rem;
}}
"""

    # === HTML ===
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{safe_title} - Navigation</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>

    <!-- App Container simulates the dynamic width constraints -->
    <div id="app-container">
        <div class="viewport-content">
            
            <nav class="navbar">
                <div class="logo">
                    <svg class="logo-icon" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                        <path d="M12 2L2 22h20L12 2zm0 4.5l6.5 13h-13L12 6.5z"/>
                    </svg>
                    <span>{safe_title}</span>
                </div>
                
                <div class="hamburger">
                    <div class="bar"></div>
                    <div class="bar"></div>
                    <div class="bar"></div>
                </div>
                
                <ul class="nav-links">
                    <li><a href="#home">Home</a></li>
                    <li><a href="#about">About</a></li>
                    <li><a href="#cases">Cases</a></li>
                    <li><a href="#services">Services</a></li>
                    <li><a class="nav-cta-button" href="#contact">Contact</a></li>
                </ul>
            </nav>

            <main class="page-content">
                <h1>Welcome to {safe_title}</h1>
                <p>{repeated_body}</p>
            </main>
            
        </div>
    </div>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Responsive Flexbox Navigation
document.addEventListener('DOMContentLoaded', () => {{
    const hamburger = document.querySelector('.hamburger');
    const navLinks = document.querySelector('.nav-links');

    // Toggle mobile menu visibility
    hamburger.addEventListener('click', () => {{
        navLinks.classList.toggle('active');
        
        // Optional: Animate hamburger into an 'X'
        // This is a common enhancement to the basic logic
        const bars = hamburger.querySelectorAll('.bar');
        if (navLinks.classList.contains('active')) {{
            bars[0].style.transform = 'translateY(9px) rotate(45deg)';
            bars[1].style.opacity = '0';
            bars[2].style.transform = 'translateY(-9px) rotate(-45deg)';
        }} else {{
            bars[0].style.transform = 'none';
            bars[1].style.opacity = '1';
            bars[2].style.transform = 'none';
        }}
    }});
}});
"""

    # === Write files ===
    files = []
    for fname, content in [("index.html", html_content), ("style.css", css), ("script.js", js)]:
        path = os.path.join(output_dir, fname)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        files.append(path)

    return {
        "html": html_content,
        "css": css,
        "js": js,
        "files": files,
    }
