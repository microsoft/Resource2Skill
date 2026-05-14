def create_component(
    output_dir: str,
    title_text: str = "Space Tourism",
    body_text: str = "Click the menu icon on a mobile screen to see the glassmorphism slide-out navigation. Resize your browser to see the layout adapt.",
    color_scheme: str = "dark",        
    accent_color: str = "#00bfff",     
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Glassmorphism Slide-Out Navigation effect.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Base theme derivations
    if color_scheme == "dark":
        bg_gradient = "linear-gradient(135deg, #0b0d17 0%, #15192b 100%)"
        text_color = "#ffffff"
        glass_bg = "rgba(255, 255, 255, 0.05)"
        solid_fallback_bg = "#15192b"
        hover_color = "rgba(255, 255, 255, 0.5)"
    else:
        bg_gradient = "linear-gradient(135deg, #e0e5ec 0%, #ffffff 100%)"
        text_color = "#0b0d17"
        glass_bg = "rgba(0, 0, 0, 0.05)"
        solid_fallback_bg = "#e0e5ec"
        hover_color = "rgba(0, 0, 0, 0.5)"

    css = f"""/* Glassmorphism Slide-Out Navigation */
:root {{
    --clr-text: {text_color};
    --clr-accent: {accent_color};
    --clr-glass: {glass_bg};
    --clr-solid-fallback: {solid_fallback_bg};
    --clr-hover: {hover_color};
    --gap: 2rem;
}}

*, *::before, *::after {{
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}}

body {{
    font-family: 'Inter', system-ui, sans-serif;
    background: {bg_gradient};
    color: var(--clr-text);
    min-height: 100vh;
    overflow-x: hidden;
}}

/* Typography Utilities */
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

/* Page Layout */
.primary-header {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 2rem;
}}

.logo {{
    font-weight: 700;
    font-size: 1.5rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}}

.logo-circle {{
    width: 40px;
    height: 40px;
    background: var(--clr-text);
    border-radius: 50%;
    display: inline-block;
}}

/* Navigation Baseline */
.primary-navigation {{
    list-style: none;
    display: flex;
    gap: var(--gap, 2rem);
}}

.primary-navigation a {{
    text-decoration: none;
    color: var(--clr-text);
    text-transform: uppercase;
    letter-spacing: 2px;
    font-size: 0.9rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding-bottom: 0.5rem;
    border-bottom: 2px solid transparent;
    transition: border-color 0.2s ease;
}}

.primary-navigation a:hover {{
    border-color: var(--clr-hover);
}}

.primary-navigation a > span {{
    font-weight: 700;
    color: var(--clr-accent);
}}

/* Mobile Nav Toggle Button */
.mobile-nav-toggle {{
    display: none;
    background: transparent;
    border: 0;
    color: var(--clr-text);
    cursor: pointer;
    z-index: 9999;
}}

.mobile-nav-toggle svg {{
    width: 2rem;
    height: 2rem;
    fill: currentColor;
    transition: transform 0.3s ease;
}}

.icon-close {{
    display: none;
}}

/* Mobile Layout - Media Query */
@media (max-width: 45rem) {{
    .primary-navigation {{
        position: fixed;
        /* Logical property shorthand for top:0, right:0, bottom:0, left:30% */
        inset: 0 0 0 30%; 
        flex-direction: column;
        padding: min(30vh, 10rem) 2rem;
        background: var(--clr-glass);
        transform: translateX(100%);
        transition: transform 350ms ease-out;
        z-index: 1000;
    }}
    
    /* The Glassmorphism Effect */
    @supports (backdrop-filter: blur(1rem)) {{
        .primary-navigation {{
            background: var(--clr-glass);
            backdrop-filter: blur(1rem);
        }}
    }}
    /* Fallback for browsers without backdrop-filter */
    @supports not (backdrop-filter: blur(1rem)) {{
        .primary-navigation {{
            background: var(--clr-solid-fallback);
        }}
    }}

    .primary-navigation[data-visible="true"] {{
        transform: translateX(0%);
    }}

    .mobile-nav-toggle {{
        display: block;
        position: absolute;
        right: 2rem;
        top: 2rem;
    }}

    /* Toggle Icon States */
    .mobile-nav-toggle[aria-expanded="true"] .icon-hamburger {{
        display: none;
    }}
    .mobile-nav-toggle[aria-expanded="true"] .icon-close {{
        display: block;
    }}
}}

/* Decorative Hero Content */
.hero-content {{
    max-width: 600px;
    margin: 10rem auto;
    padding: 2rem;
    text-align: center;
}}

.hero-content h1 {{
    font-size: clamp(2.5rem, 5vw, 5rem);
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-bottom: 1.5rem;
}}

.hero-content p {{
    font-size: 1.125rem;
    line-height: 1.6;
    color: var(--clr-hover);
}}
"""

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
            <span class="logo-circle"></span>
            LOGO
        </div>

        <!-- Mobile Navigation Toggle -->
        <button class="mobile-nav-toggle" aria-controls="primary-navigation" aria-expanded="false">
            <span class="sr-only">Menu</span>
            <!-- Hamburger Icon -->
            <svg class="icon-hamburger" viewBox="0 0 100 80" aria-hidden="true">
                <rect width="100" height="15" rx="8"></rect>
                <rect y="32" width="100" height="15" rx="8"></rect>
                <rect y="64" width="100" height="15" rx="8"></rect>
            </svg>
            <!-- Close Icon -->
            <svg class="icon-close" viewBox="0 0 100 100" aria-hidden="true">
                <rect x="10" y="42" width="100" height="15" rx="8" transform="rotate(45 50 50)"></rect>
                <rect x="10" y="42" width="100" height="15" rx="8" transform="rotate(-45 50 50)"></rect>
            </svg>
        </button>

        <!-- Primary Navigation -->
        <nav>
            <ul id="primary-navigation" class="primary-navigation" data-visible="false">
                <li>
                    <a href="#">
                        <span aria-hidden="true">00</span>Home
                    </a>
                </li>
                <li>
                    <a href="#">
                        <span aria-hidden="true">01</span>Destination
                    </a>
                </li>
                <li>
                    <a href="#">
                        <span aria-hidden="true">02</span>Crew
                    </a>
                </li>
                <li>
                    <a href="#">
                        <span aria-hidden="true">03</span>Technology
                    </a>
                </li>
            </ul>
        </nav>
    </header>

    <main class="hero-content">
        <h1>{title_text}</h1>
        <p>{body_text}</p>
    </main>

    <script src="script.js"></script>
</body>
</html>"""

    js = """// Mobile Navigation Toggle Logic
document.addEventListener('DOMContentLoaded', () => {
    const navToggle = document.querySelector('.mobile-nav-toggle');
    const primaryNav = document.querySelector('#primary-navigation');

    if (!navToggle || !primaryNav) return;

    navToggle.addEventListener('click', () => {
        // Read the current visibility state as a string
        const visibility = primaryNav.getAttribute('data-visible');

        if (visibility === 'false') {
            // Open menu
            primaryNav.setAttribute('data-visible', 'true');
            navToggle.setAttribute('aria-expanded', 'true');
        } else {
            // Close menu
            primaryNav.setAttribute('data-visible', 'false');
            navToggle.setAttribute('aria-expanded', 'false');
        }
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
