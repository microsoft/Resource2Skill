def create_component(
    output_dir: str,
    title_text: str = "SPACE TOURISM",
    body_text: str = "Explore the universe with our new frosted-glass navigation bar.",
    color_scheme: str = "dark",
    accent_color: str = "#d0d6f9",
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Responsive Glassmorphism Navbar.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Base theme configurations
    if color_scheme == "dark":
        text_col = "#ffffff"
        nav_bg = "rgba(255, 255, 255, 0.05)"
        page_bg = "radial-gradient(circle at bottom right, #0b0d17, #15192b, #05060b)"
    else:
        text_col = "#0b0d17"
        nav_bg = "rgba(0, 0, 0, 0.05)"
        page_bg = "radial-gradient(circle at bottom right, #ffffff, #d0d6f9, #f0f0f0)"

    css = f"""/* Responsive Glassmorphism Navigation */
:root {{
    --clr-text: {text_col};
    --clr-accent: {accent_color};
    --clr-nav-bg: {nav_bg};
    --nav-blur: 1.5rem;
    --transition-speed: 350ms;
}}

/* Resets */
*, *::before, *::after {{
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}}

body {{
    font-family: 'Inter', sans-serif;
    color: var(--clr-text);
    background: {page_bg};
    min-height: 100vh;
    overflow-x: hidden;
    line-height: 1.5;
}}

/* Decorative background elements to show off the glass blur */
body::before, body::after {{
    content: '';
    position: absolute;
    border-radius: 50%;
    z-index: -1;
}}
body::before {{
    width: 300px;
    height: 300px;
    background: linear-gradient(45deg, #ff00cc, #3333ff);
    top: 10%;
    left: 15%;
    filter: blur(80px);
    opacity: 0.5;
}}
body::after {{
    width: 400px;
    height: 400px;
    background: linear-gradient(45deg, #00ffff, #00ffcc);
    bottom: 20%;
    right: 5%;
    filter: blur(100px);
    opacity: 0.4;
}}

/* Utility Classes */
.flex {{ display: flex; gap: var(--gap, 1rem); }}
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

/* --- Header & Layout --- */
.primary-header {{
    justify-content: space-between;
    align-items: center;
    padding-top: 1.5rem;
    padding-left: clamp(1.5rem, 5vw, 3.5rem);
}}

.logo svg {{
    fill: var(--clr-text);
    width: 48px;
    height: 48px;
}}

/* --- Mobile Nav Toggle Button --- */
.mobile-nav-toggle {{
    display: none; /* Hidden on desktop */
    background: transparent;
    border: 0;
    cursor: pointer;
    position: absolute;
    z-index: 9999;
    right: 1.5rem;
    top: 2rem;
    width: 2rem;
    aspect-ratio: 1;
}}

.mobile-nav-toggle svg {{
    width: 100%;
    height: 100%;
    fill: var(--clr-text);
    transition: opacity 250ms ease-in-out;
}}

/* Toggle SVG visibility based on aria-expanded */
.mobile-nav-toggle .icon-close {{ display: none; }}
.mobile-nav-toggle[aria-expanded="true"] .icon-hamburger {{ display: none; }}
.mobile-nav-toggle[aria-expanded="true"] .icon-close {{ display: block; }}


/* --- Primary Navigation --- */
.primary-navigation {{
    list-style: none;
    margin: 0;
    background: var(--clr-nav-bg);
    backdrop-filter: blur(var(--nav-blur));
    -webkit-backdrop-filter: blur(var(--nav-blur));
}}

.primary-navigation a {{
    text-decoration: none;
    color: var(--clr-text);
    text-transform: uppercase;
    letter-spacing: 2px;
    font-size: 0.9rem;
    font-weight: 400;
    display: block;
    padding: 0.5rem 0;
    border-bottom: 2px solid transparent;
    transition: border-color 0.2s ease;
}}

.primary-navigation a:hover,
.primary-navigation a:focus {{
    border-bottom-color: var(--clr-accent);
}}

.primary-navigation span[aria-hidden="true"] {{
    font-weight: 700;
    margin-right: 0.5em;
}}

/* --- Mobile Styles --- */
@media (max-width: 35em) {{
    .primary-navigation {{
        --gap: 2rem;
        position: fixed;
        inset: 0 0 0 30%; /* Top, Right, Bottom, Left. Covers right 70% */
        flex-direction: column;
        padding: min(30vh, 10rem) 2rem;
        z-index: 1000;
        
        /* Animation setup */
        transform: translateX(100%);
        transition: transform var(--transition-speed) ease-out;
    }}
    
    /* Open State */
    .primary-navigation[data-visible="true"] {{
        transform: translateX(0%);
    }}

    .mobile-nav-toggle {{
        display: block;
    }}
}}

/* --- Desktop/Tablet Styles --- */
@media (min-width: 35em) {{
    .primary-navigation {{
        --gap: clamp(1.5rem, 5vw, 3rem);
        padding-block: 2rem;
        padding-inline: clamp(3rem, 7vw, 10rem);
    }}
    
    /* Hide the numbers on medium screens for space, show on large */
    @media (min-width: 35em) and (max-width: 55em) {{
        .primary-navigation span[aria-hidden="true"] {{
            display: none;
        }}
    }}
}}

/* Demo Content Page Styles */
main {{
    padding: 4rem clamp(1.5rem, 5vw, 3.5rem);
    max-width: 800px;
}}
h1 {{
    font-size: clamp(2.5rem, 8vw, 5rem);
    text-transform: uppercase;
    letter-spacing: 4px;
    margin-bottom: 1rem;
}}
p {{
    font-size: 1.1rem;
    color: var(--clr-accent);
    max-width: 60ch;
}}
"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>

    <header class="primary-header flex">
        <div class="logo">
            <!-- Simulated Logo SVG -->
            <svg viewBox="0 0 48 48" xmlns="http://www.w3.org/2000/svg">
                <circle cx="24" cy="24" r="24" fill="currentColor"/>
                <path d="M24 0c0 13.255-10.745 24-24 24 13.255 0 24 10.745 24 24 0-13.255 10.745-24 24-24-13.255 0-24-10.745-24-24z" fill="var(--clr-accent)"/>
            </svg>
        </div>

        <button class="mobile-nav-toggle" aria-controls="primary-navigation" aria-expanded="false">
            <span class="sr-only">Menu</span>
            <!-- Hamburger Icon -->
            <svg class="icon-hamburger" viewBox="0 0 24 21" xmlns="http://www.w3.org/2000/svg">
                <g fill="currentColor" fill-rule="evenodd">
                    <path d="M0 0h24v3H0zM0 9h24v3H0zM0 18h24v3H0z"/>
                </g>
            </svg>
            <!-- Close (X) Icon -->
            <svg class="icon-close" viewBox="0 0 20 21" xmlns="http://www.w3.org/2000/svg">
                <g fill="currentColor" fill-rule="evenodd">
                    <path d="M2.575.954l16.97 16.97-2.12 2.122L.455 3.076z"/>
                    <path d="M.454 17.925L17.424.955l2.122 2.12-16.97 16.97z"/>
                </g>
            </svg>
        </button>

        <nav>
            <ul id="primary-navigation" class="primary-navigation flex" data-visible="false">
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

    <main>
        <h1>{title_text}</h1>
        <p>{body_text}</p>
    </main>

    <script src="script.js"></script>
</body>
</html>"""

    js = f"""// Responsive Navbar Interaction Logic
document.addEventListener('DOMContentLoaded', () => {{
    const nav = document.querySelector('.primary-navigation');
    const navToggle = document.querySelector('.mobile-nav-toggle');

    if (!nav || !navToggle) return;

    navToggle.addEventListener('click', () => {{
        // Read current state
        const visibility = nav.getAttribute('data-visible');
        
        // Toggle logic
        if (visibility === "false") {{
            nav.setAttribute('data-visible', "true");
            navToggle.setAttribute('aria-expanded', "true");
        }} else {{
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
