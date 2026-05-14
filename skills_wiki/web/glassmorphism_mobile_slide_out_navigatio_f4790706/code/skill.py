def create_component(
    output_dir: str,
    title_text: str = "SPACE EXPLORATION",
    body_text: str = "Experience the universe like never before.",
    color_scheme: str = "dark",        
    accent_color: str = "#ffffff",     
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Glassmorphism Mobile Nav effect.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors ===
    if color_scheme == "dark":
        bg_image = "https://images.unsplash.com/photo-1451187580459-43490279c0fa?q=80&w=2072&auto=format&fit=crop"
        text_color = "#ffffff"
        nav_bg_fallback = "rgba(11, 13, 23, 0.9)"
        nav_bg_glass = "rgba(255, 255, 255, 0.05)"
        text_muted = "rgba(255, 255, 255, 0.5)"
    else:
        bg_image = "https://images.unsplash.com/photo-1518066000714-58c45f1a2c08?q=80&w=2000&auto=format&fit=crop"
        text_color = "#0b0d17"
        nav_bg_fallback = "rgba(255, 255, 255, 0.9)"
        nav_bg_glass = "rgba(0, 0, 0, 0.05)"
        text_muted = "rgba(0, 0, 0, 0.5)"

    # === CSS ===
    css = f"""/* Glassmorphism Mobile Nav Navigation */
:root {{
    --clr-text: {text_color};
    --clr-text-muted: {text_muted};
    --clr-accent: {accent_color};
    --bg-nav-fallback: {nav_bg_fallback};
    --bg-nav-glass: {nav_bg_glass};
    --font-sans: 'Inter', system-ui, sans-serif;
    --font-cond: 'Oswald', system-ui, sans-serif;
}}

*, *::before, *::after {{
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}}

body {{
    font-family: var(--font-sans);
    color: var(--clr-text);
    /* Demo background to make glassmorphism visible */
    background-image: url('{bg_image}');
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
    min-height: 100vh;
    overflow-x: hidden;
}}

.sr-only {{
    position: absolute; 
    width: 1px;
    height: 1px;
    padding: 0;
    margin: -1px; 
    overflow: hidden;
    clip: rect(0, 0, 0, 0);
    white-space: nowrap; /* added line */
    border: 0;
}}

/* Header Layout */
.primary-header {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 2rem;
}}

.logo {{
    font-family: var(--font-cond);
    font-size: 1.5rem;
    font-weight: 700;
    letter-spacing: 2px;
    color: var(--clr-text);
    text-decoration: none;
    z-index: 9999; /* Stay above nav if needed */
}}

/* Mobile Nav Toggle Button */
.mobile-nav-toggle {{
    display: none;
    background: transparent;
    border: 0;
    cursor: pointer;
    z-index: 9999;
    padding: 0.5rem;
}}

.mobile-nav-toggle svg {{
    fill: var(--clr-text);
    width: 2rem;
    height: 2rem;
    transition: transform 0.3s ease;
}}

.icon-close {{ display: none; }}

/* Toggle State Logic for SVGs */
.mobile-nav-toggle[aria-expanded="true"] .icon-hamburger {{ display: none; }}
.mobile-nav-toggle[aria-expanded="true"] .icon-close {{ display: block; transform: rotate(90deg); }}

/* Navigation Styles */
.primary-navigation {{
    list-style: none;
    display: flex;
    gap: clamp(1.5rem, 5vw, 3rem);
    padding: 0;
    margin: 0;
}}

.primary-navigation a {{
    text-decoration: none;
    color: var(--clr-text);
    font-family: var(--font-cond);
    text-transform: uppercase;
    letter-spacing: 2.7px;
    display: flex;
    align-items: center;
    gap: 0.75em;
    padding-bottom: 0.5rem;
    border-bottom: 2px solid transparent;
    transition: border-color 0.2s ease;
}}

.primary-navigation a:hover,
.primary-navigation a:focus {{
    border-color: var(--clr-text-muted);
}}

.primary-navigation span {{
    font-weight: 700;
    color: var(--clr-text);
}}

/* Mobile Specific Styles */
@media (max-width: 45em) {{
    .mobile-nav-toggle {{
        display: block;
    }}

    .primary-navigation {{
        position: fixed;
        inset: 0 0 0 30%; /* Anchor right, take up 70% width */
        z-index: 1000;
        flex-direction: column;
        padding: min(30vh, 10rem) 2em;
        
        background: var(--bg-nav-fallback);
        
        transform: translateX(100%);
        transition: transform 350ms ease-out;
    }}

    /* Glassmorphism enhancement */
    @supports (backdrop-filter: blur(1rem)) {{
        .primary-navigation {{
            background: var(--bg-nav-glass);
            backdrop-filter: blur(1.5rem);
        }}
    }}

    /* When JS sets data-visible to true */
    .primary-navigation[data-visible="true"] {{
        transform: translateX(0%);
    }}
}}

/* Desktop Specific Adjustments */
@media (min-width: 45em) {{
    .primary-navigation {{
        /* Adding desktop glass background */
        background: var(--bg-nav-glass);
        backdrop-filter: blur(1.5rem);
        padding-inline: clamp(3rem, 7vw, 7rem);
        padding-block: 2rem;
    }}
}}

/* Main Content Demo Formatting */
.hero {{
    text-align: center;
    padding: 20vh 2rem;
}}

.hero h1 {{
    font-family: var(--font-cond);
    font-size: clamp(3rem, 8vw, 8rem);
    line-height: 1;
    margin-bottom: 1rem;
}}

.hero p {{
    font-size: 1.25rem;
    color: var(--clr-accent);
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

    <header class="primary-header">
        <a href="#" class="logo">LOGO.</a>
        
        <button class="mobile-nav-toggle" aria-controls="primary-navigation" aria-expanded="false">
            <span class="sr-only">Menu</span>
            <!-- Hamburger Icon -->
            <svg class="icon-hamburger" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                <rect y="4" width="24" height="3"/>
                <rect y="11" width="24" height="3"/>
                <rect y="18" width="24" height="3"/>
            </svg>
            <!-- Close Icon -->
            <svg class="icon-close" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                <path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12 19 6.41z"/>
            </svg>
        </button>

        <nav>
            <ul id="primary-navigation" class="primary-navigation" data-visible="false">
                <li>
                    <a href="#">
                        <span aria-hidden="true">00</span> Home
                    </a>
                </li>
                <li>
                    <a href="#">
                        <span aria-hidden="true">01</span> Destination
                    </a>
                </li>
                <li>
                    <a href="#">
                        <span aria-hidden="true">02</span> Crew
                    </a>
                </li>
                <li>
                    <a href="#">
                        <span aria-hidden="true">03</span> Technology
                    </a>
                </li>
            </ul>
        </nav>
    </header>

    <main class="hero">
        <h1>{title_text}</h1>
        <p>{body_text}</p>
    </main>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Navigation State Controller
document.addEventListener('DOMContentLoaded', () => {{
    const primaryNav = document.querySelector('#primary-navigation');
    const navToggle = document.querySelector('.mobile-nav-toggle');

    navToggle.addEventListener('click', () => {{
        // Get current state
        const visibility = primaryNav.getAttribute('data-visible');

        // Toggle state
        if (visibility === "false") {{
            // Open Menu
            primaryNav.setAttribute('data-visible', "true");
            navToggle.setAttribute('aria-expanded', "true");
        }} else {{
            // Close Menu
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
