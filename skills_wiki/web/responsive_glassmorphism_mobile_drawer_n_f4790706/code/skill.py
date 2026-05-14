def create_component(
    output_dir: str,
    title_text: str = "Space Tourism",
    body_text: str = "Explore the galaxy with our modern, glassmorphism mobile navigation drawer. Resize the window to see the responsive layout.",
    color_scheme: str = "dark",
    accent_color: str = "#00bfff",
    width_px: int = 1000,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Responsive Glassmorphism Mobile Drawer.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Derive theme properties
    if color_scheme == "dark":
        bg_base = "#0b0d17"
        text_color = "#ffffff"
        text_muted = "#d0d6f9"
        glass_bg = "rgba(255, 255, 255, 0.05)"
        glass_border = "rgba(255, 255, 255, 0.1)"
        fallback_bg = "rgba(11, 13, 23, 0.95)"
        gradient_bg = "linear-gradient(135deg, #0b0d17 0%, #1a1525 100%)"
    else:
        bg_base = "#f0f2f5"
        text_color = "#0b0d17"
        text_muted = "#333333"
        glass_bg = "rgba(255, 255, 255, 0.6)"
        glass_border = "rgba(255, 255, 255, 0.8)"
        fallback_bg = "rgba(240, 242, 245, 0.95)"
        gradient_bg = "linear-gradient(135deg, #f0f2f5 0%, #e0e5ec 100%)"

    css = f"""/* Responsive Glassmorphism Mobile Drawer Navigation */
:root {{
    --clr-base: {bg_base};
    --clr-text: {text_color};
    --clr-muted: {text_muted};
    --clr-accent: {accent_color};
    --glass-bg: {glass_bg};
    --glass-border: {glass_border};
    --fallback-bg: {fallback_bg};
    --width: {width_px}px;
    --height: {height_px}px;
}}

/* Resets */
*, *::before, *::after {{
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}}

body {{
    font-family: 'Inter', system-ui, sans-serif;
    color: var(--clr-text);
    background: {gradient_bg};
    min-height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
}}

/* Preview Container (Simulating a device/browser window) */
.preview-window {{
    width: 100%;
    max-width: var(--width);
    height: var(--height);
    background-image: url('https://images.unsplash.com/photo-1462331940025-496dfbfc7564?q=80&w=2048&auto=format&fit=crop');
    background-size: cover;
    background-position: center;
    position: relative;
    overflow: hidden;
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
    border-radius: 12px;
}}

/* Layout Utility */
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

/* Header */
.primary-header {{
    align-items: center;
    justify-content: space-between;
    padding: 2rem clamp(1.5rem, 5vw, 3rem);
    position: relative;
    z-index: 1000; /* Ensure header sits above content */
}}

.logo {{
    font-size: 1.5rem;
    font-weight: 700;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: var(--clr-text);
    text-decoration: none;
    display: flex;
    align-items: center;
    gap: 0.75rem;
}}

.logo-circle {{
    width: 40px;
    height: 40px;
    background: var(--clr-text);
    border-radius: 50%;
    display: inline-block;
}}

/* Mobile Toggle Button */
.mobile-nav-toggle {{
    display: none;
    position: absolute;
    z-index: 9999;
    right: 2rem;
    top: 2rem;
    background: transparent;
    border: 0;
    cursor: pointer;
    width: 2rem;
    aspect-ratio: 1;
}}

.mobile-nav-toggle svg {{
    fill: var(--clr-text);
    width: 100%;
    height: 100%;
    transition: transform 0.3s ease;
}}

.icon-close {{
    display: none;
}}

.mobile-nav-toggle[aria-expanded="true"] .icon-hamburger {{
    display: none;
}}

.mobile-nav-toggle[aria-expanded="true"] .icon-close {{
    display: block;
}}

/* Navigation */
.primary-navigation {{
    --gap: clamp(1.5rem, 5vw, 3rem);
    list-style: none;
    background: var(--fallback-bg);
}}

/* Glassmorphism progressive enhancement */
@supports (backdrop-filter: blur(1rem)) {{
    .primary-navigation {{
        background: var(--glass-bg);
        backdrop-filter: blur(1.5rem);
        border-left: 1px solid var(--glass-border);
    }}
}}

.primary-navigation a {{
    text-decoration: none;
    color: var(--clr-text);
    font-weight: 400;
    letter-spacing: 2px;
    text-transform: uppercase;
    font-size: 0.9rem;
    display: block;
    padding: 0.5rem 0;
    position: relative;
    transition: color 0.2s ease;
}}

.primary-navigation a:hover,
.primary-navigation a:focus {{
    color: var(--clr-accent);
}}

.primary-navigation span[aria-hidden="true"] {{
    font-weight: 700;
    margin-right: 0.5em;
    color: var(--clr-text);
    opacity: 0.6;
}}

/* Mobile Styles */
@media (max-width: 45em) {{
    .mobile-nav-toggle {{
        display: block;
    }}

    .primary-navigation {{
        flex-direction: column;
        position: absolute;
        z-index: 1000;
        inset: 0 0 0 30%; /* Start 30% from the left, cover rest */
        padding: clamp(6rem, 20vh, 10rem) 2rem;
        
        /* The Animation */
        transform: translateX(100%);
        transition: transform 350ms cubic-bezier(0.4, 0, 0.2, 1);
    }}

    .primary-navigation[data-visible="true"] {{
        transform: translateX(0);
    }}
}}

/* Desktop Styles */
@media (min-width: 45em) {{
    .primary-navigation {{
        padding-block: 2rem;
        padding-inline: clamp(3rem, 7vw, 7rem);
        /* Adding the glass styling to the desktop nav bar as well */
        background: var(--glass-bg);
        backdrop-filter: blur(1.5rem);
        border-left: 0;
    }}
    
    .primary-navigation span[aria-hidden="true"] {{
        display: none; /* Hide numbers on desktop for cleaner look */
    }}
}}

/* Hero Content */
.hero-content {{
    padding: clamp(2rem, 10vw, 6rem);
    max-width: 600px;
    position: relative;
    z-index: 1;
}}

.hero-subtitle {{
    text-transform: uppercase;
    letter-spacing: 4px;
    color: var(--clr-accent);
    font-size: 1.25rem;
    margin-bottom: 1rem;
}}

.hero-title {{
    font-size: clamp(3rem, 8vw, 6rem);
    line-height: 1.1;
    font-weight: 300;
    text-transform: uppercase;
    margin-bottom: 2rem;
}}

.hero-body {{
    color: var(--clr-muted);
    font-size: 1.125rem;
    line-height: 1.8;
}}
"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text} - Responsive Nav</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>

    <div class="preview-window">
        <header class="primary-header flex">
            <a href="#" class="logo">
                <span class="logo-circle"></span>
                <span>{title_text}</span>
            </a>
            
            <button class="mobile-nav-toggle" aria-controls="primary-navigation" aria-expanded="false">
                <span class="sr-only">Menu</span>
                <!-- Hamburger Icon -->
                <svg class="icon-hamburger" viewBox="0 0 100 80" width="40" height="40">
                    <rect width="100" height="15"></rect>
                    <rect y="30" width="100" height="15"></rect>
                    <rect y="60" width="100" height="15"></rect>
                </svg>
                <!-- Close Icon -->
                <svg class="icon-close" viewBox="0 0 100 100" width="40" height="40">
                    <polygon points="100,10.6 89.4,0 50,39.4 10.6,0 0,10.6 39.4,50 0,89.4 10.6,100 50,60.6 89.4,100 100,89.4 60.6,50 "/>
                </svg>
            </button>

            <nav>
                <ul id="primary-navigation" data-visible="false" class="primary-navigation flex">
                    <li><a href="#"><span aria-hidden="true">00</span>Home</a></li>
                    <li><a href="#"><span aria-hidden="true">01</span>Destination</a></li>
                    <li><a href="#"><span aria-hidden="true">02</span>Crew</a></li>
                    <li><a href="#"><span aria-hidden="true">03</span>Technology</a></li>
                </ul>
            </nav>
        </header>

        <main class="hero-content">
            <p class="hero-subtitle">So, you want to travel to</p>
            <h1 class="hero-title">{title_text}</h1>
            <p class="hero-body">{body_text}</p>
        </main>
    </div>

    <script src="script.js"></script>
</body>
</html>"""

    js = """document.addEventListener('DOMContentLoaded', () => {
    const nav = document.querySelector('.primary-navigation');
    const navToggle = document.querySelector('.mobile-nav-toggle');

    // Toggle navigation drawer on click
    navToggle.addEventListener('click', () => {
        // Get the current state
        const visibility = nav.getAttribute('data-visible');
        
        // Toggle the states
        if (visibility === "false") {
            nav.setAttribute('data-visible', "true");
            navToggle.setAttribute('aria-expanded', "true");
        } else {
            nav.setAttribute('data-visible', "false");
            navToggle.setAttribute('aria-expanded', "false");
        }
    });

    // Accessibility & UX Improvement: Close menu on hitting 'Escape'
    document.addEventListener('keydown', (e) => {
        if (e.key === "Escape" && nav.getAttribute('data-visible') === "true") {
            nav.setAttribute('data-visible', "false");
            navToggle.setAttribute('aria-expanded', "false");
            navToggle.focus(); // Return focus to the button
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
