def create_component(
    output_dir: str,
    title_text: str = "Space Exploration",
    body_text: str = "Click the hamburger menu on small screens to see the glassmorphism off-canvas navigation.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#00bfff",     # CSS hex color for accent
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Responsive Glassmorphism Off-Canvas Navigation.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme and accent_color ===
    if color_scheme == "dark":
        bg_gradient = "linear-gradient(135deg, #0f2027, #203a43, #2c5364)"
        text_color = "#ffffff"
        menu_bg_fallback = "rgba(15, 32, 39, 0.95)"
        menu_bg_glass = "rgba(255, 255, 255, 0.05)"
        nav_hover_bg = "rgba(255, 255, 255, 0.1)"
    else:
        bg_gradient = "linear-gradient(135deg, #e0eafc, #cfdef3)"
        text_color = "#1a1a2e"
        menu_bg_fallback = "rgba(255, 255, 255, 0.95)"
        menu_bg_glass = "rgba(255, 255, 255, 0.4)"
        nav_hover_bg = "rgba(0, 0, 0, 0.05)"

    # === CSS ===
    css = f"""/* Responsive Glassmorphism Off-Canvas Navigation */
:root {{
    --text-color: {text_color};
    --accent-color: {accent_color};
    --menu-bg-fallback: {menu_bg_fallback};
    --menu-bg-glass: {menu_bg_glass};
    --nav-hover-bg: {nav_hover_bg};
}}

*, *::before, *::after {{
    box-sizing: border-box;
}}

body, h1, h2, h3, p, ul {{
    margin: 0;
    padding: 0;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    color: var(--text-color);
    background: {bg_gradient};
    background-size: cover;
    background-attachment: fixed;
    min-height: 100vh;
    overflow-x: hidden;
}}

/* -- Utility Classes -- */
.sr-only {{
    position: absolute;
    width: 1px;
    height: 1px;
    padding: 0;
    margin: -1px;
    overflow: hidden;
    clip: rect(0, 0, 0, 0);
    white-space: nowrap;
    border: 0;
}}

/* -- Layout -- */
.primary-header {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 2rem;
}}

.logo svg {{
    width: 3rem;
    height: 3rem;
    fill: var(--text-color);
}}

/* -- Navigation Styles (Mobile First) -- */
.primary-navigation {{
    list-style: none;
    margin: 0;
    padding: 0;
    
    /* Layout */
    display: flex;
    flex-direction: column;
    gap: 2rem;
    
    /* Positioning & Sizing */
    position: fixed;
    z-index: 1000;
    inset: 0 0 0 30%; /* Covers 70% of screen from right */
    padding: min(20vh, 10rem) 2em;
    
    /* Glassmorphism Defaults */
    background: var(--menu-bg-fallback);
    
    /* Animation */
    transform: translateX(100%);
    transition: transform 350ms ease-out;
}}

/* Progressive Enhancement for Glassmorphism */
@supports (backdrop-filter: blur(1rem)) or (-webkit-backdrop-filter: blur(1rem)) {{
    .primary-navigation {{
        background: var(--menu-bg-glass);
        backdrop-filter: blur(1rem);
        -webkit-backdrop-filter: blur(1rem);
    }}
}}

/* Active State (Triggered by JS) */
.primary-navigation[data-visible="true"] {{
    transform: translateX(0%);
}}

/* Nav Links */
.primary-navigation a {{
    text-decoration: none;
    color: var(--text-color);
    text-transform: uppercase;
    letter-spacing: 2px;
    font-size: 1rem;
    display: flex;
    align-items: center;
    gap: 1rem;
    padding: 0.5rem;
    border-radius: 4px;
    transition: background-color 0.2s ease, color 0.2s ease;
}}

.primary-navigation a:hover,
.primary-navigation a:focus {{
    background-color: var(--nav-hover-bg);
    color: var(--accent-color);
}}

.primary-navigation span[aria-hidden="true"] {{
    font-weight: 700;
    color: var(--accent-color);
}}

/* -- Mobile Toggle Button -- */
.mobile-nav-toggle {{
    display: block;
    position: absolute;
    z-index: 9999;
    top: 2.5rem;
    right: 2rem;
    background: transparent;
    border: 0;
    cursor: pointer;
    width: 2rem;
    aspect-ratio: 1;
    color: var(--text-color);
}}

.mobile-nav-toggle svg {{
    width: 100%;
    height: 100%;
    fill: currentColor;
    transition: transform 0.3s ease;
}}

/* Icon Swapping Logic based on aria-expanded */
.icon-close {{
    display: none;
}}

.mobile-nav-toggle[aria-expanded="true"] .icon-hamburger {{
    display: none;
}}

.mobile-nav-toggle[aria-expanded="true"] .icon-close {{
    display: block;
}}

/* -- Main Content Area -- */
.hero-section {{
    padding: clamp(2rem, 5vw, 5rem);
    max-width: {width_px}px;
    margin: 0 auto;
}}

.hero-section h1 {{
    font-size: clamp(2.5rem, 5vw, 4rem);
    margin-bottom: 1rem;
    font-weight: 300;
}}

.hero-section p {{
    font-size: 1.25rem;
    line-height: 1.6;
    max-width: 60ch;
    opacity: 0.8;
}}

/* -- Desktop Media Query -- */
@media (min-width: 45em) {{
    .mobile-nav-toggle {{
        display: none;
    }}
    
    .primary-navigation {{
        /* Reset positioning */
        position: static;
        inset: auto;
        transform: translateX(0);
        
        /* Change Layout */
        flex-direction: row;
        gap: clamp(1.5rem, 4vw, 3rem);
        padding: 0;
        
        /* Remove Glass Effect */
        background: transparent;
        backdrop-filter: none;
        -webkit-backdrop-filter: none;
    }}
    
    .primary-navigation a {{
        padding: 2rem 0;
        border-radius: 0;
        position: relative;
    }}
    
    /* Desktop Hover Indicator */
    .primary-navigation a::after {{
        content: '';
        position: absolute;
        bottom: 0;
        left: 0;
        width: 100%;
        height: 3px;
        background-color: var(--accent-color);
        transform: scaleX(0);
        transform-origin: right;
        transition: transform 0.3s ease;
    }}
    
    .primary-navigation a:hover::after,
    .primary-navigation a:focus::after {{
        transform: scaleX(1);
        transform-origin: left;
    }}
    
    .primary-navigation a:hover,
    .primary-navigation a:focus {{
        background-color: transparent;
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
    <header class="primary-header">
        <div class="logo">
            <!-- Example Logo SVG -->
            <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                <circle cx="12" cy="12" r="10" fill="none" stroke="currentColor" stroke-width="2"/>
                <circle cx="12" cy="12" r="4" fill="currentColor"/>
                <path d="M12 2 L12 6 M12 18 L12 22 M2 12 L6 12 M18 12 L22 12" stroke="currentColor" stroke-width="2"/>
            </svg>
        </div>
        
        <!-- Mobile Toggle Button -->
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

        <!-- Navigation Array -->
        <nav>
            <ul id="primary-navigation" data-visible="false" class="primary-navigation">
                <li><a href="#"><span aria-hidden="true">00</span> Home</a></li>
                <li><a href="#"><span aria-hidden="true">01</span> Destination</a></li>
                <li><a href="#"><span aria-hidden="true">02</span> Crew</a></li>
                <li><a href="#"><span aria-hidden="true">03</span> Technology</a></li>
            </ul>
        </nav>
    </header>

    <main class="hero-section">
        <h1>{title_text}</h1>
        <p>{body_text}</p>
    </main>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Responsive Glassmorphism Off-Canvas Navigation Logic
document.addEventListener('DOMContentLoaded', () => {{
    const primaryNav = document.querySelector('.primary-navigation');
    const navToggle = document.querySelector('.mobile-nav-toggle');

    if (!primaryNav || !navToggle) return;

    navToggle.addEventListener('click', () => {{
        // Get current visibility state from the data attribute
        const visibility = primaryNav.getAttribute('data-visible');

        if (visibility === 'false') {{
            // Open the menu
            primaryNav.setAttribute('data-visible', 'true');
            navToggle.setAttribute('aria-expanded', 'true');
        }} else {{
            // Close the menu
            primaryNav.setAttribute('data-visible', 'false');
            navToggle.setAttribute('aria-expanded', 'false');
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
