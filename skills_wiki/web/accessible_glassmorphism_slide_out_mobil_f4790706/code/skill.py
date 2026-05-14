def create_component(
    output_dir: str,
    title_text: str = "Space Explorer",
    body_text: str = "Scroll down or resize the window to see the responsive navigation behavior. On screens smaller than 560px, the menu converts to a glassmorphism slide-out panel.",
    color_scheme: str = "dark",        
    accent_color: str = "#00bfff",     
    width_px: int = 1000,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Accessible Glassmorphism Slide-Out Navigation.
    """
    import os
    os.makedirs(output_dir, exist_ok=True)

    if color_scheme == "dark":
        bg_color = "#0B0D17"
        text_color = "#FFFFFF"
        surface_fallback = "rgba(11, 13, 23, 0.95)"
        surface_glass = "rgba(255, 255, 255, 0.04)"
        text_muted = "rgba(255, 255, 255, 0.5)"
        bg_image = "radial-gradient(circle at bottom right, #1a233a, #0B0D17)"
    else:
        bg_color = "#F2F4F8"
        text_color = "#0B0D17"
        surface_fallback = "rgba(242, 244, 248, 0.95)"
        surface_glass = "rgba(0, 0, 0, 0.05)"
        text_muted = "rgba(11, 13, 23, 0.5)"
        bg_image = "radial-gradient(circle at top left, #ffffff, #e0e5ec)"

    css = f"""/* Base Reset */
*, *::before, *::after {{
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}}

:root {{
    --clr-bg: {bg_color};
    --clr-text: {text_color};
    --clr-text-muted: {text_muted};
    --clr-accent: {accent_color};
    --clr-surface-fallback: {surface_fallback};
    --clr-surface-glass: {surface_glass};
    
    --ff-sans: 'Inter', system-ui, sans-serif;
}}

body {{
    font-family: var(--ff-sans);
    background: {bg_image};
    background-color: var(--clr-bg);
    color: var(--clr-text);
    min-height: 100vh;
    overflow-x: hidden;
}}

/* Utility for Screen Readers */
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
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 2rem;
    max-width: {width_px}px;
    margin: 0 auto;
}}

.logo {{
    font-size: 1.5rem;
    font-weight: 700;
    letter-spacing: 2px;
    text-transform: uppercase;
}}

/* Navigation Desktop Default */
.primary-navigation {{
    display: flex;
    gap: clamp(1.5rem, 5vw, 3rem);
    list-style: none;
    margin: 0;
    padding: 0;
}}

.primary-navigation a {{
    text-decoration: none;
    color: var(--clr-text);
    text-transform: uppercase;
    letter-spacing: 2px;
    font-size: 0.9rem;
    position: relative;
    padding-block: 0.5rem;
}}

.primary-navigation a::after {{
    content: '';
    position: absolute;
    bottom: 0;
    left: 0;
    width: 100%;
    height: 2px;
    background-color: var(--clr-accent);
    transform: scaleX(0);
    transform-origin: right;
    transition: transform 300ms ease;
}}

.primary-navigation a:hover::after,
.primary-navigation a:focus::after {{
    transform: scaleX(1);
    transform-origin: left;
}}

/* Decorative Numbers */
.nav-number {{
    font-weight: 700;
    margin-inline-end: 0.5em;
    color: var(--clr-text-muted);
}}

/* Mobile Toggle Button */
.mobile-nav-toggle {{
    display: none; /* Hidden on desktop */
}}

/* ========================================= */
/* Mobile Navigation (Max-width approach)    */
/* ========================================= */
@media (max-width: 45em) {{ /* approx 720px */
    .primary-navigation {{
        position: fixed;
        z-index: 1000;
        /* Logical property shorthand: top, right, bottom, left */
        inset: 0 0 0 30%; 
        flex-direction: column;
        padding: min(20vh, 8rem) 2rem;
        
        background: var(--clr-surface-fallback);
        transform: translateX(100%);
        transition: transform 350ms cubic-bezier(0.4, 0, 0.2, 1);
    }}

    /* Apply glassmorphism only if supported */
    @supports (backdrop-filter: blur(1rem)) {{
        .primary-navigation {{
            background: var(--clr-surface-glass);
            backdrop-filter: blur(1.5rem);
        }}
    }}

    .primary-navigation[data-visible="true"] {{
        transform: translateX(0%);
    }}

    /* Mobile Toggle Button */
    .mobile-nav-toggle {{
        display: flex;
        align-items: center;
        justify-content: center;
        position: absolute;
        z-index: 9999;
        right: 2rem;
        top: 2.25rem;
        background: transparent;
        border: 0;
        cursor: pointer;
        width: 2rem;
        aspect-ratio: 1;
    }}
    
    .mobile-nav-toggle svg {{
        fill: var(--clr-text);
        width: 100%;
        transition: transform 300ms ease;
    }}
    
    .mobile-nav-toggle .icon-close {{
        display: none;
    }}

    /* Toggle Icon State Change */
    .mobile-nav-toggle[aria-expanded="true"] .icon-hamburger {{
        display: none;
    }}
    
    .mobile-nav-toggle[aria-expanded="true"] .icon-close {{
        display: block;
    }}
}}

/* Hero Content */
.hero {{
    max-width: 600px;
    margin: 4rem auto;
    padding: 2rem;
    text-align: center;
}}

.hero h1 {{
    font-size: clamp(2rem, 5vw, 4rem);
    margin-bottom: 1rem;
}}

.hero p {{
    line-height: 1.6;
    color: var(--clr-text-muted);
}}
"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>

    <header class="primary-header">
        <div class="logo">
            {title_text}
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
                <path d="M19.707 5.707a1 1 0 00-1.414-1.414L12 10.586 5.707 4.293a1 1 0 00-1.414 1.414L10.586 12l-6.293 6.293a1 1 0 101.414 1.414L12 13.414l6.293 6.293a1 1 0 001.414-1.414L13.414 12l6.293-6.293z"/>
            </svg>
        </button>

        <nav>
            <ul id="primary-navigation" class="primary-navigation" data-visible="false">
                <li class="active">
                    <a href="#">
                        <span class="nav-number" aria-hidden="true">00</span>Home
                    </a>
                </li>
                <li>
                    <a href="#">
                        <span class="nav-number" aria-hidden="true">01</span>Destination
                    </a>
                </li>
                <li>
                    <a href="#">
                        <span class="nav-number" aria-hidden="true">02</span>Crew
                    </a>
                </li>
                <li>
                    <a href="#">
                        <span class="nav-number" aria-hidden="true">03</span>Technology
                    </a>
                </li>
            </ul>
        </nav>
    </header>

    <main class="hero">
        <h1>Welcome Aboard</h1>
        <p>{body_text}</p>
    </main>

    <script src="script.js"></script>
</body>
</html>"""

    js = f"""document.addEventListener('DOMContentLoaded', () => {{
    const nav = document.querySelector('.primary-navigation');
    const navToggle = document.querySelector('.mobile-nav-toggle');

    navToggle.addEventListener('click', () => {{
        const visibility = nav.getAttribute('data-visible');
        
        // If menu is closed, open it
        if (visibility === "false") {{
            nav.setAttribute('data-visible', "true");
            navToggle.setAttribute('aria-expanded', "true");
        }} 
        // If menu is open, close it
        else {{
            nav.setAttribute('data-visible', "false");
            navToggle.setAttribute('aria-expanded', "false");
        }}
    }});
}});
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
