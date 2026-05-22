def create_component(
    output_dir: str,
    title_text: str = "Space Tourism",
    body_text: str = "SO, YOU WANT TO TRAVEL TO SPACE",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#d0d6f9",     # CSS hex color for accent/hover
    width_px: int = 400,               # Defaulting to mobile width to show effect
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Glassmorphism Mobile Slide-Out Drawer.
    
    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme ===
    if color_scheme == "dark":
        bg_gradient = "linear-gradient(135deg, #0b0d17 0%, #1a1e3a 100%)"
        text_color = "#ffffff"
        nav_bg = "rgba(11, 13, 23, 0.75)" # Dark frosted glass
        nav_blur = "blur(1.5rem)"
        num_color = "rgba(255, 255, 255, 0.5)"
    else:
        bg_gradient = "linear-gradient(135deg, #f0f2fa 0%, #c4c7d6 100%)"
        text_color = "#0b0d17"
        nav_bg = "rgba(255, 255, 255, 0.6)" # Light frosted glass
        nav_blur = "blur(1.5rem)"
        num_color = "rgba(11, 13, 23, 0.5)"

    # === CSS ===
    css = f"""/* Glassmorphism Mobile Nav — generated component */
:root {{
    --clr-text: {text_color};
    --clr-accent: {accent_color};
    --clr-nav-bg: {nav_bg};
    --nav-blur: {nav_blur};
    --clr-num: {num_color};
}}

*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: 'Inter', system-ui, sans-serif;
    color: var(--clr-text);
    background: {bg_gradient};
    min-height: 100vh;
    overflow-x: hidden; /* Prevent scrollbar from hidden off-canvas menu */
}}

.app-wrapper {{
    width: 100%;
    max-width: {width_px}px;
    height: {height_px}px;
    margin: 0 auto;
    position: relative;
    overflow-x: hidden;
    background: url('https://images.unsplash.com/photo-1451187580459-43490279c0fa?q=80&w=1000&auto=format&fit=crop') center/cover;
    border: 1px solid rgba(255,255,255,0.1);
    box-shadow: 0 20px 40px rgba(0,0,0,0.5);
}}

/* Header & Logo placeholder */
.primary-header {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 2rem;
}}

.logo {{
    width: 48px;
    height: 48px;
    background: #fff;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #000;
    font-weight: bold;
    text-decoration: none;
}}

/* Mobile Nav Toggle Button */
.mobile-nav-toggle {{
    display: block;
    position: absolute;
    z-index: 9999;
    background: transparent;
    border: 0;
    top: 2rem;
    right: 2rem;
    cursor: pointer;
    width: 2rem;
    aspect-ratio: 1;
}}

.mobile-nav-toggle svg {{
    width: 100%;
    height: 100%;
    fill: var(--clr-text);
    transition: transform 0.3s ease;
}}

.icon-close {{ display: none; }}
.mobile-nav-toggle[aria-expanded="true"] .icon-hamburger {{ display: none; }}
.mobile-nav-toggle[aria-expanded="true"] .icon-close {{ display: block; transform: rotate(90deg); }}

.sr-only {{
    position: absolute;
    width: 1px;
    height: 1px;
    padding: 0;
    margin: -1px;
    overflow: hidden;
    clip: rect(0, 0, 0, 0);
    border: 0;
}}

/* Primary Navigation (The Drawer) */
.primary-navigation {{
    list-style: none;
    padding: 0;
    margin: 0;
    
    /* Layout */
    display: flex;
    flex-direction: column;
    gap: 2rem;
    padding-block: min(20vh, 10rem);
    padding-inline: 2rem;
    
    /* Positioning */
    position: fixed;
    z-index: 1000;
    /* inset: top right bottom left */
    inset: 0 0 0 30%; 
    
    /* Glassmorphism */
    background: var(--clr-nav-bg);
    backdrop-filter: var(--nav-blur);
    -webkit-backdrop-filter: var(--nav-blur); /* Safari support */
    
    /* Animation */
    transform: translateX(100%);
    transition: transform 350ms ease-out;
}}

@supports not (backdrop-filter: blur(1rem)) {{
    /* Fallback for browsers that don't support backdrop-filter */
    .primary-navigation {{
        background: { "#111" if color_scheme == "dark" else "#eee" };
    }}
}}

/* Open State */
.primary-navigation[data-visible="true"] {{
    transform: translateX(0%);
}}

/* Navigation Links */
.primary-navigation a {{
    text-decoration: none;
    color: var(--clr-text);
    text-transform: uppercase;
    letter-spacing: 2px;
    font-size: 1rem;
    display: flex;
    gap: 0.75rem;
    transition: color 0.2s ease;
}}

.primary-navigation a:hover,
.primary-navigation a:focus {{
    color: var(--clr-accent);
}}

.primary-navigation a span {{
    font-weight: 700;
    color: var(--clr-num);
}}

/* Page Content */
.main-content {{
    padding: 2rem;
    margin-top: 4rem;
}}

.main-content h1 {{
    font-size: 1.5rem;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: var(--clr-accent);
    margin-bottom: 1rem;
}}

.main-content p {{
    font-size: 4rem;
    font-weight: 300;
    text-transform: uppercase;
    line-height: 1.1;
}}

/* Desktop/Tablet Override */
@media (min-width: 35em) {{
    .mobile-nav-toggle {{
        display: none;
    }}
    
    .primary-navigation {{
        position: static;
        flex-direction: row;
        inset: auto;
        padding-block: 2rem;
        padding-inline: clamp(3rem, 5vw, 5rem);
        transform: translateX(0);
        background: rgba(255,255,255,0.05);
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
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="app-wrapper">
        <header class="primary-header">
            <a href="#" class="logo">LOGO</a>
            
            <button class="mobile-nav-toggle" aria-controls="primary-navigation" aria-expanded="false">
                <span class="sr-only">Menu</span>
                <!-- Hamburger Icon -->
                <svg class="icon-hamburger" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                    <path d="M3 12h18M3 6h18M3 18h18" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
                <!-- Close Icon -->
                <svg class="icon-close" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                    <path d="M18 6L6 18M6 6l12 12" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
            </button>

            <nav>
                <ul id="primary-navigation" data-visible="false" class="primary-navigation">
                    <li>
                        <a href="#"><span aria-hidden="true">00</span>Home</a>
                    </li>
                    <li>
                        <a href="#"><span aria-hidden="true">01</span>Destination</a>
                    </li>
                    <li>
                        <a href="#"><span aria-hidden="true">02</span>Crew</a>
                    </li>
                    <li>
                        <a href="#"><span aria-hidden="true">03</span>Technology</a>
                    </li>
                </ul>
            </nav>
        </header>

        <main class="main-content">
            <h1>{title_text}</h1>
            <p>{body_text}</p>
        </main>
    </div>
    
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Glassmorphism Navigation — Interactive Behavior
document.addEventListener('DOMContentLoaded', () => {{
    const primaryNav = document.querySelector('.primary-navigation');
    const navToggle = document.querySelector('.mobile-nav-toggle');

    navToggle.addEventListener('click', () => {{
        // Read current state
        const visibility = primaryNav.getAttribute('data-visible');

        if (visibility === "false") {{
            // Open menu
            primaryNav.setAttribute('data-visible', "true");
            navToggle.setAttribute('aria-expanded', "true");
        }} else {{
            // Close menu
            primaryNav.setAttribute('data-visible', "false");
            navToggle.setAttribute('aria-expanded', "false");
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
