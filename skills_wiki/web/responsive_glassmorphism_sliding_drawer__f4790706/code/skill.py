def create_component(
    output_dir: str,
    title_text: str = "Space Elements",
    body_text: str = "Explore the fluid frosted-glass navigation menu. Resize the browser to see the layout adapt, and click the menu toggle on mobile sizes.",
    color_scheme: str = "dark",
    accent_color: str = "#00bfff",
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Responsive Glassmorphism Sliding Drawer Navigation.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme and accent_color ===
    if color_scheme == "dark":
        bg_gradient = "radial-gradient(circle at bottom right, #1a0b2e, #0d111c, #000000)"
        text_color = "#ffffff"
        text_muted = "rgba(255, 255, 255, 0.6)"
        surface_color = "rgba(255, 255, 255, 0.05)"
        hover_bg = "rgba(255, 255, 255, 0.1)"
    else:
        bg_gradient = "radial-gradient(circle at top left, #f0f4ff, #e5e9f0, #ffffff)"
        text_color = "#0b0c10"
        text_muted = "rgba(0, 0, 0, 0.5)"
        surface_color = "rgba(255, 255, 255, 0.6)"
        hover_bg = "rgba(0, 0, 0, 0.05)"

    # === CSS ===
    css = f"""/* Responsive Glassmorphism Navigation */
:root {{
    --clr-text: {text_color};
    --clr-muted: {text_muted};
    --clr-accent: {accent_color};
    --clr-surface: {surface_color};
    --clr-hover: {hover_bg};
    
    --ff-sans: 'Inter', system-ui, -apple-system, sans-serif;
    --ff-condensed: 'Oswald', sans-serif;
    
    --gap: 2rem;
}}

/* Reset */
*, *::before, *::after {{
    box-sizing: border-box;
}}

body, h1, h2, h3, p, ul, li {{
    margin: 0;
    padding: 0;
}}

body {{
    font-family: var(--ff-sans);
    background: {bg_gradient};
    color: var(--clr-text);
    min-height: 100vh;
    overflow-x: hidden; /* Prevent horizontal scroll from off-canvas menu */
    display: flex;
    flex-direction: column;
}}

/* Utility Classes */
.flex {{
    display: flex;
    gap: var(--gap, 1rem);
}}

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

/* Header Layout */
.primary-header {{
    align-items: center;
    justify-content: space-between;
    padding: 2rem;
    position: relative;
    z-index: 1000;
}}

.logo svg {{
    width: 48px;
    height: 48px;
    fill: var(--clr-text);
}}

/* Mobile Nav Toggle Button */
.mobile-nav-toggle {{
    display: none;
    background: transparent;
    border: 0;
    cursor: pointer;
    position: absolute;
    z-index: 9999;
    right: 2rem;
    top: 2rem;
    padding: 0.5rem;
}}

.mobile-nav-toggle svg {{
    width: 24px;
    height: 24px;
    fill: var(--clr-text);
    transition: transform 0.3s ease;
}}

.mobile-nav-toggle .icon-close {{
    display: none;
}}

.mobile-nav-toggle[aria-expanded="true"] .icon-hamburger {{
    display: none;
}}

.mobile-nav-toggle[aria-expanded="true"] .icon-close {{
    display: block;
}}

/* Primary Navigation Styles */
.primary-navigation {{
    list-style: none;
    padding: 0;
    margin: 0;
}}

.primary-navigation a {{
    text-decoration: none;
    color: var(--clr-text);
    text-transform: uppercase;
    font-family: var(--ff-condensed);
    letter-spacing: 2px;
    font-size: 1rem;
    display: flex;
    align-items: center;
    gap: 0.75em;
    padding: 0.5rem 0;
    position: relative;
}}

.primary-navigation a::after {{
    content: '';
    position: absolute;
    bottom: -0.5rem;
    left: 0;
    width: 100%;
    height: 2px;
    background: var(--clr-text);
    transform: scaleX(0);
    transform-origin: right;
    transition: transform 0.3s ease;
}}

.primary-navigation a:hover::after,
.primary-navigation a:focus::after {{
    transform: scaleX(1);
    transform-origin: left;
}}

.primary-navigation a span {{
    font-weight: 700;
    color: var(--clr-muted);
}}

/* Mobile specific styling */
@media (max-width: 45em) {{
    .primary-navigation {{
        --gap: 2em;
        position: fixed;
        inset: 0 0 0 30%; /* Drawer width: 70% of viewport */
        flex-direction: column;
        padding: min(20vh, 10rem) 2em;
        z-index: 1000;
        
        /* Glassmorphism */
        background: var(--clr-surface);
        backdrop-filter: blur(1rem);
        -webkit-backdrop-filter: blur(1rem);
        border-left: 1px solid rgba(255, 255, 255, 0.1);
        
        /* Off-canvas setup */
        transform: translateX(100%);
        transition: transform 350ms ease-out;
    }}
    
    /* Fallback for browsers that don't support backdrop-filter */
    @supports not (backdrop-filter: blur(1rem)) {{
        .primary-navigation {{
            background: {bg_gradient};
        }}
    }}

    .primary-navigation[data-visible="true"] {{
        transform: translateX(0%);
    }}

    .mobile-nav-toggle {{
        display: block;
    }}
}}

/* Desktop specific styling */
@media (min-width: 45em) {{
    .primary-navigation {{
        --gap: clamp(1.5rem, 5vw, 3rem);
        padding-block: 2rem;
        padding-inline: clamp(3rem, 7vw, 10rem);
        
        /* Glassmorphism Inline Header */
        background: var(--clr-surface);
        backdrop-filter: blur(1rem);
        -webkit-backdrop-filter: blur(1rem);
    }}
}}

/* Main Content Area */
main {{
    flex-grow: 1;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 2rem;
}}

.hero-content {{
    max-width: 600px;
    text-align: center;
}}

.hero-content h1 {{
    font-size: clamp(2rem, 5vw, 4rem);
    font-family: var(--ff-condensed);
    text-transform: uppercase;
    letter-spacing: 4px;
    margin-bottom: 1rem;
}}

.hero-content h1 span {{
    color: var(--clr-accent);
}}

.hero-content p {{
    font-size: 1.125rem;
    line-height: 1.6;
    color: var(--clr-muted);
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
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700&family=Oswald:wght@400;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <header class="primary-header flex">
        <div class="logo">
            <!-- Mock Logo SVG -->
            <svg viewBox="0 0 48 48" xmlns="http://www.w3.org/2000/svg">
                <circle cx="24" cy="24" r="20" fill="none" stroke="currentColor" stroke-width="4" stroke-dasharray="10 5" />
                <circle cx="24" cy="24" r="10" fill="currentColor"/>
            </svg>
        </div>

        <button class="mobile-nav-toggle" aria-controls="primary-navigation" aria-expanded="false">
            <span class="sr-only">Menu</span>
            <!-- Hamburger Icon -->
            <svg class="icon-hamburger" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                <rect y="4" width="24" height="3" rx="1.5"/>
                <rect y="11" width="24" height="3" rx="1.5"/>
                <rect y="18" width="24" height="3" rx="1.5"/>
            </svg>
            <!-- Close Icon -->
            <svg class="icon-close" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                <path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12 19 6.41z"/>
            </svg>
        </button>

        <nav>
            <ul id="primary-navigation" data-visible="false" class="primary-navigation flex">
                <li class="active"><a href="#"><span aria-hidden="true">00</span> Home</a></li>
                <li><a href="#"><span aria-hidden="true">01</span> Destination</a></li>
                <li><a href="#"><span aria-hidden="true">02</span> Crew</a></li>
                <li><a href="#"><span aria-hidden="true">03</span> Technology</a></li>
            </ul>
        </nav>
    </header>

    <main>
        <div class="hero-content">
            <h1>Explore <span>{title_text}</span></h1>
            <p>{body_text}</p>
        </div>
    </main>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Responsive Navigation State Management
document.addEventListener('DOMContentLoaded', () => {{
    const primaryNav = document.querySelector('.primary-navigation');
    const navToggle = document.querySelector('.mobile-nav-toggle');

    if (!primaryNav || !navToggle) return;

    navToggle.addEventListener('click', () => {{
        // Get the current state as a string from the custom data attribute
        const visibility = primaryNav.getAttribute('data-visible');

        // Toggle state based on the current value
        if (visibility === "false") {{
            primaryNav.setAttribute('data-visible', "true");
            navToggle.setAttribute('aria-expanded', "true");
        }} else {{
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
