def create_component(
    output_dir: str,
    title_text: str = "Space Tourism",
    body_text: str = "Let's face it; if you want to go to space, you might as well genuinely go to outer space and not hover kind of on the edge of it. Well sit back, and relax because we'll give you a truly out of this world experience!",
    color_scheme: str = "dark",        
    accent_color: str = "#00bfff",     
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    import os
    import urllib.parse

    os.makedirs(output_dir, exist_ok=True)

    # === Theme Processing ===
    if color_scheme == "dark":
        bg_color = "#0B0D17"
        text_color = "#FFFFFF"
        text_muted = "#D0D6F9"
        glass_bg = "hsl(0 0% 100% / 0.05)"
        glass_fallback = "hsl(230 35% 7% / 0.95)"
    else:
        bg_color = "#F2F4F8"
        text_color = "#0B0D17"
        text_muted = "#3B3D4A"
        glass_bg = "hsl(0 0% 0% / 0.05)"
        glass_fallback = "hsl(0 0% 95% / 0.95)"

    # Generate SVGs dynamically with proper coloring
    hamburger_svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="24" height="21" fill="{text_muted}"><path d="M0 0h24v3H0zM0 9h24v3H0zM0 18h24v3H0z"/></svg>'
    close_svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="{text_muted}"><path d="M2.4.2l21.2 21.2-2.1 2.1L.3 2.3z"/><path d="M23.6.2L2.4 21.4.3 19.3 21.5.1z"/></svg>'
    logo_svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" fill="{text_color}"><circle cx="24" cy="24" r="24" fill="{text_color}"/><path fill="{bg_color}" d="M24 0c0 16-8 24-24 24 15.718.114 23.718 8.114 24 24 0-16 8-24 24-24-16 0-24-8-24-24z"/></svg>'

    ham_url = f"data:image/svg+xml;charset=utf-8,{urllib.parse.quote(hamburger_svg)}"
    close_url = f"data:image/svg+xml;charset=utf-8,{urllib.parse.quote(close_svg)}"
    logo_url = f"data:image/svg+xml;charset=utf-8,{urllib.parse.quote(logo_svg)}"

    # Background photo placeholder (abstract gradient)
    bg_image = f"radial-gradient(ellipse at bottom right, {accent_color}33, transparent 50%), radial-gradient(ellipse at top left, {text_color}22, transparent 50%)"

    # === CSS ===
    css = f"""/* Glassmorphic Slide-Out Mobile Menu */
:root {{
    --clr-bg: {bg_color};
    --clr-text: {text_color};
    --clr-text-muted: {text_muted};
    --clr-accent: {accent_color};
    --glass-bg: {glass_bg};
    --glass-fallback: {glass_fallback};
    
    --ff-sans: 'Inter', system-ui, sans-serif;
    --ff-cond: 'Oswald', system-ui, sans-serif;
}}

*, *::before, *::after {{
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}}

body {{
    font-family: var(--ff-sans);
    background-color: var(--clr-bg);
    color: var(--clr-text);
    min-height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
}}

/* Viewport Container for accurate preview */
.app-container {{
    position: relative;
    width: 100%;
    max-width: {width_px}px;
    height: 100vh;
    max-height: {height_px}px;
    background-image: {bg_image};
    background-color: var(--clr-bg);
    overflow-x: hidden;
}}

/* Utility Classes */
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

/* --- Primary Header --- */
.primary-header {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 2rem;
}}

.logo {{
    width: 48px;
    height: 48px;
    background-image: url('{logo_url}');
    background-repeat: no-repeat;
    background-size: contain;
}}

/* --- Primary Navigation --- */
.primary-navigation {{
    list-style: none;
    display: flex;
    gap: clamp(1.5rem, 5vw, 3rem);
    padding: 0 3rem;
    margin: 0;
    
    /* Desktop Glass Effect */
    background: var(--glass-bg);
    backdrop-filter: blur(1.5rem);
}}

/* Fallback for browsers that don't support backdrop-filter */
@supports not (backdrop-filter: blur(1.5rem)) {{
    .primary-navigation {{
        background: var(--glass-fallback);
    }}
}}

.primary-navigation a {{
    text-decoration: none;
    color: var(--clr-text);
    font-family: var(--ff-cond);
    text-transform: uppercase;
    letter-spacing: 2px;
    font-size: 1rem;
    display: block;
    padding: 2rem 0;
    border-bottom: 3px solid transparent;
    transition: border-color 0.2s ease;
}}

.primary-navigation a:hover,
.primary-navigation a:focus {{
    border-color: rgba(255, 255, 255, 0.5);
}}

.primary-navigation .active a {{
    border-color: var(--clr-text);
}}

.primary-navigation span[aria-hidden="true"] {{
    font-weight: 700;
    margin-right: 0.5em;
}}

/* Mobile Toggle Button */
.mobile-nav-toggle {{
    display: none;
}}

/* --- Content Demo --- */
.hero-content {{
    padding: 4rem 2rem;
    max-width: 600px;
}}
.hero-subtitle {{
    color: var(--clr-accent);
    font-family: var(--ff-cond);
    letter-spacing: 4px;
    text-transform: uppercase;
    margin-bottom: 1.5rem;
}}
.hero-title {{
    font-size: clamp(4rem, 8vw, 8rem);
    text-transform: uppercase;
    line-height: 1;
    margin-bottom: 2rem;
}}
.hero-body {{
    color: var(--clr-text-muted);
    font-size: 1.1rem;
    line-height: 1.7;
}}

/* --- Mobile Breakpoint --- */
@media (max-width: 45em) {{
    .primary-navigation {{
        /* Switch to slide-out sidebar */
        position: absolute; /* Using absolute relative to .app-container instead of fixed for demo embedding */
        z-index: 1000;
        inset: 0 0 0 30%;
        flex-direction: column;
        padding: min(30vh, 10rem) 2em;
        
        transform: translateX(100%);
        transition: transform 350ms ease-out;
    }}
    
    .primary-navigation[data-visible="true"] {{
        transform: translateX(0%);
    }}
    
    .primary-navigation a {{
        border-bottom: 0;
        border-right: 3px solid transparent;
        padding: 0.5rem 0;
    }}
    
    .mobile-nav-toggle {{
        display: block;
        position: absolute;
        z-index: 9999;
        background-color: transparent;
        background-image: url('{ham_url}');
        background-repeat: no-repeat;
        background-position: center;
        width: 1.5rem;
        aspect-ratio: 1;
        border: 0;
        top: 3.5rem;
        right: 2rem;
        cursor: pointer;
    }}
    
    .mobile-nav-toggle[aria-expanded="true"] {{
        background-image: url('{close_url}');
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
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700&family=Oswald:wght@400;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="app-container">
        
        <!-- Header & Nav -->
        <header class="primary-header">
            <div class="logo"></div>
            
            <button class="mobile-nav-toggle" aria-controls="primary-navigation" aria-expanded="false">
                <span class="sr-only">Menu</span>
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

        <!-- Page Content -->
        <main class="hero-content">
            <p class="hero-subtitle">So, you want to travel to</p>
            <h1 class="hero-title">{title_text}</h1>
            <p class="hero-body">{body_text}</p>
        </main>

    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = """// Glassmorphic Mobile Menu Logic
document.addEventListener('DOMContentLoaded', () => {
    const nav = document.querySelector('.primary-navigation');
    const navToggle = document.querySelector('.mobile-nav-toggle');

    // Toggle navigation on button click
    navToggle.addEventListener('click', () => {
        // Read current state from the data attribute (returns string "false" or "true")
        const visibility = nav.getAttribute('data-visible');
        
        if (visibility === "false") {
            // Open menu
            nav.setAttribute('data-visible', "true");
            navToggle.setAttribute('aria-expanded', "true");
        } else {
            // Close menu
            nav.setAttribute('data-visible', "false");
            navToggle.setAttribute('aria-expanded', "false");
        }
    });
    
    // Accessibility: close menu on Escape key press
    document.addEventListener('keydown', (e) => {
        if (e.key === "Escape" && nav.getAttribute('data-visible') === "true") {
            nav.setAttribute('data-visible', "false");
            navToggle.setAttribute('aria-expanded', "false");
            navToggle.focus(); // return focus to button
        }
    });
});
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
