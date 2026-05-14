def create_component(
    output_dir: str,
    title_text: str = "BrandName",
    body_text: str = "Scroll down to see the sticky navigation in action. Try resizing the window to see the mobile hamburger menu.",
    color_scheme: str = "dark",
    accent_color: str = "#39ffde",
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Responsive Sticky Hamburger Navigation visual effect.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme ===
    if color_scheme == "dark":
        page_bg = "#222222"
        nav_bg = "#ffffff"
        nav_text = "#111111"
        text_color = "#f0f0f0"
    else:
        page_bg = "#f5f7fa"
        nav_bg = "#111111"
        nav_text = "#ffffff"
        text_color = "#333333"

    # === CSS ===
    css = f"""/* Responsive Navigation Bar */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --page-bg: {page_bg};
    --nav-bg: {nav_bg};
    --nav-text: {nav_text};
    --accent: {accent_color};
    --text: {text_color};
}}

body {{
    font-family: 'Inter', system-ui, sans-serif;
    background-color: #1a1a1a; /* Outer wrapper dark backdrop */
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
}}

/* Preview container acting as the viewport */
.preview-window {{
    width: {width_px}px;
    height: {height_px}px;
    max-width: 100%;
    max-height: 100vh;
    background-color: var(--page-bg);
    position: relative;
    overflow-y: auto;
    overflow-x: hidden;
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
}}

/* Navigation Core Styles */
nav {{
    position: sticky;
    top: 0;
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0 20px;
    background-color: var(--nav-bg);
    z-index: 100;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}}

/* Logo */
.logo {{
    display: flex;
    align-items: center;
    height: 80px;
}}

.logo svg {{
    width: 32px;
    height: 32px;
    fill: var(--nav-text);
    margin-right: 12px;
}}

.logo h3 {{
    color: var(--nav-text);
    font-size: 20px;
    font-weight: 700;
}}

/* Hamburger Icon (Hidden on Desktop) */
.hamburger {{
    display: none;
    cursor: pointer;
    width: 34px;
}}

.hamburger .bar {{
    flex-basis: 100%;
    height: 4px;
    background-color: var(--nav-text);
    margin: 3px 0;
    border-radius: 2px;
    transition: all 0.3s ease;
}}

/* Navigation Links */
.nav-links {{
    display: flex;
    align-items: center;
    list-style: none;
    height: 100%;
}}

.nav-links li {{
    height: 100%;
    display: flex;
    align-items: center;
}}

.nav-links a {{
    display: block;
    padding: 12px 18px;
    color: var(--nav-text);
    text-decoration: none;
    text-transform: uppercase;
    font-size: 14px;
    font-weight: 600;
    letter-spacing: 0.5px;
    transition: all 150ms ease-in-out;
    border-radius: 4px;
}}

.nav-links a:hover {{
    background-color: var(--accent);
    color: var(--nav-bg);
}}

/* Specific Call to Action Button */
.nav-cta-button a {{
    padding: 10px 24px !important;
    margin-left: 16px;
    border: 2px solid var(--accent);
    border-radius: 50px;
    color: var(--accent);
}}

.nav-cta-button a:hover {{
    background-color: var(--accent);
    color: var(--nav-bg);
}}

/* Dummy Content below nav */
.content {{
    padding: 60px 40px;
    color: var(--text);
    line-height: 1.6;
}}

.content h1 {{
    font-size: 48px;
    margin-bottom: 20px;
}}

.content p {{
    font-size: 18px;
    margin-bottom: 30px;
    max-width: 800px;
    opacity: 0.9;
}}

.spacer {{
    height: 1500px;
    background: repeating-linear-gradient(
      45deg,
      transparent,
      transparent 20px,
      rgba(128, 128, 128, 0.05) 20px,
      rgba(128, 128, 128, 0.05) 40px
    );
    border-radius: 8px;
    border: 1px dashed rgba(128, 128, 128, 0.2);
}}

/* --- Responsive Breakpoint --- */
@media (max-width: 768px) {{
    nav {{
        flex-wrap: wrap;
        padding: 0 15px;
    }}
    
    .hamburger {{
        display: flex;
        flex-wrap: wrap;
    }}
    
    /* Hide links by default on mobile, let JS toggle the .active class */
    .nav-links {{
        display: none;
        flex-basis: 100%;
        flex-direction: column;
        width: 100%;
        background-color: var(--nav-bg);
        padding-bottom: 20px;
    }}
    
    .nav-links.active {{
        display: flex;
    }}
    
    .nav-links li {{
        width: 100%;
        justify-content: center;
    }}
    
    .nav-links a {{
        width: 100%;
        text-align: center;
        padding: 16px 20px;
    }}
    
    .nav-cta-button a {{
        margin-left: 0;
        margin-top: 10px;
        width: 80%;
    }}
}}
"""

    # === HTML ===
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text} - Responsive Nav</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>

    <!-- Bounded window to simulate device viewport based on python params -->
    <div class="preview-window">
        
        <nav>
            <div class="logo">
                <svg viewBox="0 0 24 24">
                    <path d="M12 2L2 22h20L12 2zm0 3.83L19.17 20H4.83L12 5.83z"/>
                </svg>
                <h3>{title_text}</h3>
            </div>
            
            <div class="hamburger">
                <div class="bar"></div>
                <div class="bar"></div>
                <div class="bar"></div>
            </div>
            
            <ul class="nav-links">
                <li><a href="#">Home</a></li>
                <li><a href="#">About</a></li>
                <li><a href="#">Cases</a></li>
                <li><a href="#">Services</a></li>
                <li class="nav-cta-button"><a href="#">Contact</a></li>
            </ul>
        </nav>

        <main class="content">
            <h1>Welcome to {title_text}</h1>
            <p>{body_text}</p>
            <div class="spacer"></div>
        </main>

    </div>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""document.addEventListener('DOMContentLoaded', () => {{
    const hamburger = document.querySelector('.hamburger');
    const navLinks = document.querySelector('.nav-links');

    // Toggle menu visibility on click
    hamburger.addEventListener('click', () => {{
        navLinks.classList.toggle('active');
        
        // Optional: Animate hamburger bars into an 'X' (not in original tutorial, but good practice)
        // Here we just toggle the display class to faithfully match the tutorial's logic, 
        // upgraded to use a CSS class instead of brittle inline styles.
    }});

    // Ensure menu resets if window is resized past the mobile breakpoint
    window.addEventListener('resize', () => {{
        if (window.innerWidth > 768) {{
            navLinks.classList.remove('active');
        }}
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
