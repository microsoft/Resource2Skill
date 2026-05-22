def create_component(
    output_dir: str,
    title_text: str = "BRAND.",
    body_text: str = "Scroll down or open the mobile menu to see the frosted glass effect in action.",
    color_scheme: str = "dark",        
    accent_color: str = "#00bfff",     
    width_px: int = 100, # Percentage based, standard viewport width expected
    height_px: int = 100, # Percentage based, standard viewport height expected
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Responsive Glassmorphism Mobile Slide-Out Navigation.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme ===
    if color_scheme == "dark":
        bg_color = "#0b0d17"
        text_color = "#ffffff"
        menu_fallback_bg = "rgba(0, 0, 0, 0.85)"
        menu_glass_bg = "rgba(255, 255, 255, 0.05)"
        hero_bg_image = "linear-gradient(45deg, #0b0d17, #1a1a2e)"
    else:
        bg_color = "#f8f9fa"
        text_color = "#0b0d17"
        menu_fallback_bg = "rgba(255, 255, 255, 0.95)"
        menu_glass_bg = "rgba(255, 255, 255, 0.5)"
        hero_bg_image = "linear-gradient(45deg, #e0eaf5, #f8f9fa)"

    # === CSS ===
    css = f"""/* Responsive Glassmorphism Mobile Slide-Out Navigation */
:root {{
    --clr-bg: {bg_color};
    --clr-text: {text_color};
    --clr-accent: {accent_color};
    
    --menu-bg-fallback: {menu_fallback_bg};
    --menu-bg-glass: {menu_glass_bg};
    
    --font-base: 'Inter', system-ui, sans-serif;
}}

*, *::before, *::after {{
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}}

body {{
    font-family: var(--font-base);
    background: var(--clr-bg);
    color: var(--clr-text);
    line-height: 1.5;
    min-height: 100vh;
    overflow-x: hidden;
}}

/* Decorative background to show off glass effect */
.page-background {{
    position: fixed;
    inset: 0;
    background: {hero_bg_image};
    z-index: -1;
}}
.page-background::after {{
    content: '';
    position: absolute;
    top: 20%;
    left: 10%;
    width: 40vw;
    height: 40vw;
    background: var(--clr-accent);
    border-radius: 50%;
    filter: blur(100px);
    opacity: 0.3;
}}

/* --- Layout Classes --- */
.flex {{
    display: flex;
    gap: var(--gap, 1rem);
}}

/* --- Header & Branding --- */
.primary-header {{
    justify-content: space-between;
    align-items: center;
    padding: 2rem;
}}

.logo {{
    font-weight: 800;
    font-size: 1.5rem;
    letter-spacing: 2px;
    text-decoration: none;
    color: var(--clr-text);
}}

/* --- Mobile Navigation Toggle --- */
.mobile-nav-toggle {{
    display: block; /* Visible by default on mobile */
    position: absolute;
    z-index: 9999; /* Keep above the menu */
    background: transparent;
    border: 0;
    cursor: pointer;
    right: 2rem;
    top: 2rem;
    width: 2rem;
    aspect-ratio: 1;
    color: var(--clr-text);
}}

.mobile-nav-toggle svg {{
    width: 100%;
    height: 100%;
    fill: currentColor;
    transition: transform 300ms ease;
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

/* --- Primary Navigation --- */
.primary-navigation {{
    list-style: none;
    padding: 0;
    margin: 0;
    
    /* Solid fallback for browsers without backdrop-filter */
    background: var(--menu-bg-fallback);
}}

@supports (backdrop-filter: blur(1rem)) {{
    .primary-navigation {{
        background: var(--menu-bg-glass);
        backdrop-filter: blur(1.5rem);
        -webkit-backdrop-filter: blur(1.5rem);
    }}
}}

.primary-navigation a {{
    text-decoration: none;
    color: var(--clr-text);
    text-transform: uppercase;
    letter-spacing: 2px;
    font-weight: 500;
    font-size: 0.9rem;
    transition: color 200ms ease;
}}

.primary-navigation a:hover,
.primary-navigation a:focus {{
    color: var(--clr-accent);
}}

.primary-navigation span {{
    font-weight: 800;
    margin-inline-end: 0.5em;
    color: var(--clr-accent);
}}

/* --- Mobile Specific Styles --- */
@media (max-width: 35em) {{
    .primary-navigation {{
        --gap: 2em;
        position: fixed;
        z-index: 1000;
        /* inset maps to top, right, bottom, left. Leaves 30% gap on left */
        inset: 0 0 0 30%; 
        flex-direction: column;
        padding: min(30vh, 10rem) 2em;
        
        /* Start off screen */
        transform: translateX(100%);
        transition: transform 350ms ease-out;
    }}
    
    /* Sliding in effect controlled by JS data-attribute */
    .primary-navigation[data-visible="true"] {{
        transform: translateX(0%);
    }}
    
    /* Prevent body scroll when menu is open */
    body.nav-open {{
        overflow: hidden;
    }}
}}

/* --- Desktop Specific Styles --- */
@media (min-width: 35em) {{
    .mobile-nav-toggle {{
        display: none; /* Hide hamburger on desktop */
    }}
    
    .primary-header {{
        padding-inline-end: 0; /* Let nav touch the right edge */
    }}
    
    .primary-navigation {{
        --gap: clamp(1.5rem, 5vw, 3rem);
        padding-block: 2rem;
        padding-inline: clamp(3rem, 7vw, 6rem);
    }}
}}

/* Demo content */
main {{
    padding: 2rem;
    max-width: 800px;
    margin: 4rem auto;
}}
h2 {{ font-size: 2.5rem; margin-bottom: 1rem; }}
p {{ font-size: 1.1rem; opacity: 0.8; margin-bottom: 2rem; }}
"""

    # === HTML ===
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text} Navigation</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="page-background"></div>
    
    <header class="primary-header flex">
        <div>
            <a href="#" class="logo">{title_text}</a>
        </div>

        <button class="mobile-nav-toggle" aria-controls="primary-navigation" aria-expanded="false">
            <span class="sr-only">Menu</span>
            <!-- Inline Hamburger SVG -->
            <svg id="icon-hamburger" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                <rect y="4" width="24" height="2" rx="1"/>
                <rect y="11" width="24" height="2" rx="1"/>
                <rect y="18" width="24" height="2" rx="1"/>
            </svg>
            <!-- Inline Close SVG (Hidden by default in JS) -->
            <svg id="icon-close" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" style="display: none;">
                <path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12 19 6.41z"/>
            </svg>
        </button>

        <nav>
            <ul id="primary-navigation" data-visible="false" class="primary-navigation flex">
                <li class="active">
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

    <main>
        <h2>Responsive Glassmorphism Nav</h2>
        <p>{body_text}</p>
        <p>Shrink the browser window to less than ~560px to see the hamburger menu appear. Click it to trigger the slide-out animation with backdrop filter.</p>
    </main>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Responsive Glassmorphism Mobile Slide-Out Navigation Logic
document.addEventListener('DOMContentLoaded', () => {{
    const nav = document.querySelector('.primary-navigation');
    const navToggle = document.querySelector('.mobile-nav-toggle');
    const iconHamburger = document.getElementById('icon-hamburger');
    const iconClose = document.getElementById('icon-close');

    navToggle.addEventListener('click', () => {{
        // Get the current state
        const isVisible = nav.getAttribute('data-visible');

        // Toggle state
        if (isVisible === "false") {{
            nav.setAttribute('data-visible', "true");
            navToggle.setAttribute('aria-expanded', "true");
            document.body.classList.add('nav-open');
            
            // Swap icons
            iconHamburger.style.display = 'none';
            iconClose.style.display = 'block';
            
            // Add a slight spin animation for visual feedback
            iconClose.style.transform = 'rotate(90deg)';
            setTimeout(() => iconClose.style.transform = 'rotate(0deg)', 50);
        }} else {{
            nav.setAttribute('data-visible', "false");
            navToggle.setAttribute('aria-expanded', "false");
            document.body.classList.remove('nav-open');
            
            // Swap icons
            iconClose.style.display = 'none';
            iconHamburger.style.display = 'block';
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
