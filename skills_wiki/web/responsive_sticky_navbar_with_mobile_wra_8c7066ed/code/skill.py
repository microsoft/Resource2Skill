def create_component(
    output_dir: str,
    title_text: str = "BrandName",
    body_text: str = "Scroll down to see the navigation bar remain sticky at the top of the viewport. Resize the window below 768px to see the responsive hamburger menu in action.",
    color_scheme: str = "dark",
    accent_color: str = "#39ffde",
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Responsive Sticky Navbar visual effect.
    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Derive theme colors
    if color_scheme == "dark":
        nav_bg = "#1a1a2e"
        nav_text = "#f0f0f0"
        page_bg = "#0d111c"
        page_text = "#a0a0b0"
        border_color = "rgba(255, 255, 255, 0.1)"
        hover_bg = "rgba(255, 255, 255, 0.05)"
    else:
        nav_bg = "#ffffff"
        nav_text = "#111111"
        page_bg = "#f4f4f9"
        page_text = "#444444"
        border_color = "rgba(0, 0, 0, 0.1)"
        hover_bg = "rgba(0, 0, 0, 0.03)"

    css = f"""/* Responsive Sticky Navbar */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --width: {width_px}px;
    --height: {height_px}px;
    --nav-bg: {nav_bg};
    --nav-text: {nav_text};
    --nav-accent: {accent_color};
    --page-bg: {page_bg};
    --page-text: {page_text};
    --border-color: {border_color};
    --hover-bg: {hover_bg};
}}

body {{
    background: #000;
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
}}

/* Device viewport container to enforce specified dimensions */
.device-container {{
    width: var(--width);
    height: var(--height);
    max-width: 100vw;
    max-height: 100vh;
    background: var(--page-bg);
    overflow-y: auto;
    position: relative;
    color: var(--page-text);
    box-shadow: 0 0 20px rgba(0, 0, 0, 0.5);
}}

/* Scrollbar styling for device container */
.device-container::-webkit-scrollbar {{ width: 8px; }}
.device-container::-webkit-scrollbar-track {{ background: var(--page-bg); }}
.device-container::-webkit-scrollbar-thumb {{ background: var(--border-color); border-radius: 4px; }}

/* Navigation Bar Core */
.navbar {{
    position: sticky;
    top: 0;
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap; /* Crucial for mobile row-wrapping */
    padding: 0 40px;
    background-color: var(--nav-bg);
    color: var(--nav-text);
    min-height: 70px;
    z-index: 1000;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.15);
}}

/* Branding / Logo */
.logo {{
    display: flex;
    align-items: center;
    gap: 12px;
}}

.logo svg {{
    width: 28px;
    height: 28px;
    fill: var(--nav-text);
}}

.logo h3 {{
    font-size: 1.25rem;
    font-weight: 700;
    letter-spacing: -0.5px;
}}

/* Desktop Links */
.nav-links {{
    display: flex;
    align-items: center;
    list-style: none;
    gap: 10px;
}}

.nav-links li a {{
    color: var(--nav-text);
    text-decoration: none;
    padding: 10px 15px;
    display: block;
    font-size: 0.85rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    transition: color 0.2s ease, background-color 0.2s ease;
    border-radius: 4px;
}}

.nav-links li a:hover:not(.nav-cta-button) {{
    color: var(--nav-accent);
    background-color: var(--hover-bg);
}}

/* CTA Button Specifics */
.nav-cta-button {{
    margin-left: 10px;
    border: 2px solid var(--nav-accent);
    border-radius: 50px;
    padding: 10px 24px !important;
}}

.nav-links li a.nav-cta-button:hover {{
    background-color: var(--nav-accent);
    color: var(--nav-bg);
}}

/* Hamburger Icon (Hidden on Desktop) */
.hamburger {{
    display: none;
    flex-direction: column;
    cursor: pointer;
    gap: 5px;
    padding: 5px;
}}

.hamburger .bar {{
    width: 26px;
    height: 3px;
    background-color: var(--nav-text);
    border-radius: 2px;
    transition: all 0.3s ease;
}}

/* Page Content Formatting */
.content {{
    padding: 60px 40px;
    max-width: 800px;
    margin: 0 auto;
}}

.content h1 {{
    color: var(--nav-text);
    font-size: 2.5rem;
    margin-bottom: 20px;
}}

.content p {{
    font-size: 1.1rem;
    line-height: 1.6;
}}

.dummy-scroll-space {{
    height: 150vh;
    background: linear-gradient(to bottom, transparent, var(--border-color));
    margin-top: 40px;
    border-radius: 8px;
}}

/* === Mobile Responsive Layout === */
@media (max-width: 768px) {{
    .navbar {{
        padding: 15px 20px;
    }}

    .hamburger {{
        display: flex;
    }}

    .nav-links {{
        display: none; /* Hidden by default */
        width: 100%;   /* Forces wrap to new line */
        flex-direction: column;
        margin-top: 15px;
        padding-top: 10px;
        border-top: 1px solid var(--border-color);
        gap: 0;
    }}

    .nav-links.active {{
        display: flex; /* Toggled by JS */
    }}

    .nav-links li {{
        width: 100%;
    }}

    .nav-links li a {{
        padding: 16px 0;
        text-align: center;
        border-radius: 0;
        border-bottom: 1px solid var(--border-color);
    }}

    .nav-links li:last-child a {{
        border-bottom: none;
    }}

    .nav-cta-button {{
        margin: 20px auto 10px auto;
        display: inline-block;
        width: max-content;
    }}
}}
"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text} - Responsive Navbar</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="device-container">
        
        <nav class="navbar">
            <div class="logo">
                <svg viewBox="0 0 24 24">
                    <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/>
                </svg>
                <h3>{title_text}</h3>
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

        <main class="content">
            <h1>Welcome to {title_text}</h1>
            <p>{body_text}</p>
            <div class="dummy-scroll-space"></div>
        </main>

    </div>
    <script src="script.js"></script>
</body>
</html>"""

    js = f"""// Responsive Navbar Interaction
document.addEventListener('DOMContentLoaded', () => {{
    const hamburger = document.querySelector('.hamburger');
    const navLinks = document.querySelector('.nav-links');

    // Toggle menu open/close on mobile
    hamburger.addEventListener('click', () => {{
        navLinks.classList.toggle('active');
        
        // Optional: Animate hamburger bars to 'X' (not required but good UX)
        // You would add CSS for .hamburger.active .bar to handle the transforms
    }});

    // Close menu when a link is clicked (good UX practice)
    const links = document.querySelectorAll('.nav-links li a');
    links.forEach(link => {{
        link.addEventListener('click', () => {{
            navLinks.classList.remove('active');
        }});
    }});
}});
"""

    # Write files
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
