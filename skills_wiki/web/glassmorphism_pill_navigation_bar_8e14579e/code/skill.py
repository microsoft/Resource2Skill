def create_component(
    output_dir: str,
    title_text: str = "Glassmorphism",
    body_text: str = "Scroll down to see the fixed navigation bar float over the content.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#ffda79",     # CSS hex color for accent (yellowish from tutorial)
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Glassmorphism Pill Navigation Bar.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme ===
    if color_scheme == "dark":
        text_color = "#ffffff"
        nav_bg = "rgba(255, 255, 255, 0.1)"
        nav_border = "rgba(255, 255, 255, 0.2)"
        nav_shadow = "rgba(0, 0, 0, 0.5)"
        # Using a beautiful dark nature landscape from Unsplash as background
        bg_image = "https://images.unsplash.com/photo-1506748686214-e9df14d4d9d0?ixlib=rb-4.0.3&auto=format&fit=crop&w=1920&q=80" 
    else:
        text_color = "#1a1a2e"
        nav_bg = "rgba(255, 255, 255, 0.4)"
        nav_border = "rgba(255, 255, 255, 0.6)"
        nav_shadow = "rgba(0, 0, 0, 0.1)"
        # Using a bright abstract landscape
        bg_image = "https://images.unsplash.com/photo-1472214103451-9374bd1c798e?ixlib=rb-4.0.3&auto=format&fit=crop&w=1920&q=80"

    # === CSS ===
    css = f"""/* Glassmorphism Pill Navigation Bar */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --text: {text_color};
    --accent: {accent_color};
    --nav-bg: {nav_bg};
    --nav-border: {nav_border};
    --nav-shadow: {nav_shadow};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Inter', 'Segoe UI', system-ui, sans-serif;
    color: var(--text);
    /* Set a background image to make the glass effect visible */
    background-image: url('{bg_image}');
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
    min-height: 200vh; /* Extra height to demonstrate fixed positioning */
    overflow-x: hidden;
}}

/* Page container just to frame it for the requested dimensions */
.demo-container {{
    width: var(--width);
    max-width: 100vw;
    margin: 0 auto;
    padding-top: 150px; /* Space for the fixed navbar */
    text-align: center;
}}

h1 {{
    font-size: 3rem;
    margin-bottom: 1rem;
    text-shadow: 0 2px 10px rgba(0,0,0,0.5);
    color: #ffffff; /* Always white for readability on image */
}}

p {{
    font-size: 1.2rem;
    text-shadow: 0 2px 10px rgba(0,0,0,0.5);
    color: #e0e0e0;
}}

/* --- Core Component Styles --- */

.glass-nav {{
    position: fixed;
    top: 2rem;
    left: 50%;
    transform: translateX(-50%);
    width: 80%; /* Responsive width */
    max-width: 1000px;
    padding: 1rem 2rem;
    z-index: 1000;
    
    /* Glassmorphism magic */
    background: var(--nav-bg);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px); /* Safari support */
    
    /* Shape and depth */
    border-radius: 50px;
    border: 1px solid var(--nav-border);
    box-shadow: 0 6px 15px var(--nav-shadow);
}}

.nav-list {{
    list-style: none;
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 3rem; /* Spacing between links */
    flex-wrap: wrap; /* Allows wrapping on very small screens */
}}

.nav-item {{
    /* Optional: can add styles here if needed */
}}

.nav-link {{
    text-decoration: none;
    color: var(--accent); /* Default link color */
    font-weight: 500;
    font-size: 1.1rem;
    padding: 5px 0;
    position: relative;
    transition: color 0.3s ease;
    text-shadow: 0 1px 4px rgba(0,0,0,0.4);
}}

.nav-link:hover,
.nav-link:focus-visible {{
    color: #ffffff;
    outline: none;
}}

/* Center-out expanding underline animation */
.nav-link::after {{
    content: '';
    position: absolute;
    bottom: 0;
    left: 50%;
    transform: translateX(-50%);
    width: 0;
    height: 2px;
    background-color: #ffffff;
    transition: width 0.3s ease;
}}

.nav-link:hover::after,
.nav-link:focus-visible::after {{
    width: 100%;
}}

/* Responsive adjustments */
@media (max-width: 768px) {{
    .glass-nav {{
        width: 95%;
        padding: 1rem;
    }}
    .nav-list {{
        gap: 1.5rem;
    }}
    .nav-link {{
        font-size: 1rem;
    }}
}}
"""

    # === HTML ===
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <!-- The Component -->
    <nav class="glass-nav" aria-label="Main Navigation">
        <ul class="nav-list">
            <li class="nav-item"><a href="#home" class="nav-link">Home</a></li>
            <li class="nav-item"><a href="#about" class="nav-link">About</a></li>
            <li class="nav-item"><a href="#services" class="nav-link">Services</a></li>
            <li class="nav-item"><a href="#portfolio" class="nav-link">Portfolio</a></li>
            <li class="nav-item"><a href="#contact" class="nav-link">Contact</a></li>
        </ul>
    </nav>

    <!-- Context container to demonstrate layout -->
    <div class="demo-container">
        <h1>{title_text}</h1>
        <p>{body_text}</p>
    </div>
    
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// No JavaScript required for the core visual layout or CSS hover effects.
// Added a simple scroll listener just to show interaction potential.

document.addEventListener('DOMContentLoaded', () => {{
    const nav = document.querySelector('.glass-nav');
    
    // Example: Optional dynamic styling on scroll
    window.addEventListener('scroll', () => {{
        if (window.scrollY > 50) {{
            // Can modify styles via JS if needed, but CSS handles the core aesthetic
            // nav.style.boxShadow = '0 10px 20px rgba(0,0,0,0.8)';
        }} else {{
            // nav.style.boxShadow = '';
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
