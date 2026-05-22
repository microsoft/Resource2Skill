def create_component(
    output_dir: str,
    title_text: str = "SPACE",
    body_text: str = "SO, YOU WANT TO TRAVEL TO SPACE",
    color_scheme: str = "dark",
    accent_color: str = "#d0d6f9",
    width_px: int = 1000,
    height_px: int = 700,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Frosted Glass Off-Canvas Navigation.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme ===
    if color_scheme == "dark":
        bg_image = "https://images.unsplash.com/photo-1451187580459-43490279c0fa?q=80&w=2072&auto=format&fit=crop" # Space background
        text_color = "#ffffff"
        nav_bg = "rgba(255, 255, 255, 0.05)"
        nav_border = "rgba(255, 255, 255, 0.1)"
    else:
        bg_image = "https://images.unsplash.com/photo-1506459225024-1428097a7e18?q=80&w=2000&auto=format&fit=crop" # Light sky
        text_color = "#0b0d17"
        nav_bg = "rgba(0, 0, 0, 0.15)"
        nav_border = "rgba(0, 0, 0, 0.1)"

    # === CSS ===
    css = f"""/* Frosted Glass Off-Canvas Mobile Navigation */
*, *::before, *::after {{
    box-sizing: border-box;
}}

body, h1, h2, h3, p {{
    margin: 0;
}}

body {{
    font-family: 'Inter', sans-serif;
    color: {text_color};
    /* Placeholder background to demonstrate the glassmorphism blur effect */
    background-image: url('{bg_image}');
    background-size: cover;
    background-position: center;
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow-x: hidden;
}}

/* Mock viewport container for the demo */
.viewport-container {{
    width: 100%;
    max-width: {width_px}px;
    height: {height_px}px;
    position: relative;
    overflow-x: hidden;
    border: 1px solid rgba(255,255,255,0.2);
    border-radius: 12px;
    box-shadow: 0 20px 40px rgba(0,0,0,0.4);
}}

/* --- HEADER & LAYOUT --- */
.primary-header {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 2rem;
}}

.logo {{
    font-size: 1.5rem;
    font-weight: 700;
    letter-spacing: 4px;
    z-index: 1000; /* Stays above the blur */
}}

/* --- NAVIGATION LIST --- */
.primary-navigation {{
    list-style: none;
    padding: 0;
    margin: 0;
    display: flex;
    gap: clamp(1.5rem, 5vw, 4rem); /* Responsive gap */
}}

.primary-navigation a {{
    text-decoration: none;
    color: {text_color};
    text-transform: uppercase;
    letter-spacing: 2px;
    font-size: 0.9rem;
    font-weight: 500;
    display: flex;
    align-items: center;
    gap: 0.5em;
}}

.primary-navigation span {{
    font-weight: 700;
    margin-inline-end: 0.25em;
}}

.primary-navigation a:hover {{
    color: {accent_color};
}}

/* --- MOBILE TOGGLE BUTTON --- */
.mobile-nav-toggle {{
    display: none; /* Hidden on desktop */
    position: absolute;
    z-index: 9999;
    background: transparent;
    border: 0;
    width: 2rem;
    aspect-ratio: 1;
    cursor: pointer;
    top: 2rem;
    right: 2rem;
}}

/* Accessibility class */
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

/* Self-contained CSS Hamburger Icon */
.hamburger-line,
.hamburger-line::before,
.hamburger-line::after {{
    content: '';
    display: block;
    width: 100%;
    height: 3px;
    background-color: {text_color};
    position: absolute;
    transition: transform 300ms ease-in-out, opacity 300ms ease-in-out;
}}
.hamburger-line {{ top: 50%; transform: translateY(-50%); }}
.hamburger-line::before {{ top: -8px; }}
.hamburger-line::after {{ bottom: -8px; }}

.mobile-nav-toggle[aria-expanded="true"] .hamburger-line {{ background-color: transparent; }}
.mobile-nav-toggle[aria-expanded="true"] .hamburger-line::before {{ transform: translateY(8px) rotate(45deg); }}
.mobile-nav-toggle[aria-expanded="true"] .hamburger-line::after {{ transform: translateY(-8px) rotate(-45deg); }}

/* --- RESPONSIVE MOBILE NAVIGATION --- */
/* Breakpoint roughly equivalent to 35em used in the tutorial */
@media (max-width: 45em) {{
    .primary-navigation {{
        position: fixed;
        z-index: 1000;
        /* Logical property shorthand: top, right, bottom, left */
        inset: 0 0 0 30%; 
        flex-direction: column;
        
        /* The Tutorial's specific responsive padding technique */
        padding: min(30vh, 10rem) 2em;
        
        background: {nav_bg};
        border-left: 1px solid {nav_border};
        
        /* The Core Glassmorphism Effect */
        backdrop-filter: blur(1.5rem);
        -webkit-backdrop-filter: blur(1.5rem); /* Safari support */
        
        /* Slide off-screen setup */
        transform: translateX(100%);
        transition: transform 350ms ease-out;
    }}
    
    /* State triggered by JS */
    .primary-navigation[data-visible="true"] {{
        transform: translateX(0);
    }}

    .mobile-nav-toggle {{
        display: block; /* Show hamburger on mobile */
    }}
}}

/* Demo content styling */
.hero-content {{
    padding: 4rem 2rem;
    max-width: 600px;
}}
.hero-content h2 {{ font-size: clamp(3rem, 8vw, 6rem); margin-top: 1rem; }}
.hero-content p {{ color: {accent_color}; letter-spacing: 2px; }}
"""

    # === HTML ===
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Responsive Glassmorphism Nav</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>

<div class="viewport-container">
    <header class="primary-header">
        <div class="logo">{title_text}</div>
        
        <!-- Hamburger Button with Accessibility Hooks -->
        <button class="mobile-nav-toggle" aria-controls="primary-navigation" aria-expanded="false">
            <span class="sr-only">Menu</span>
            <div class="hamburger-line"></div>
        </button>

        <!-- Navigation Menu -->
        <nav>
            <ul id="primary-navigation" data-visible="false" class="primary-navigation">
                <li><a href="#"><span>00</span> Home</a></li>
                <li><a href="#"><span>01</span> Destination</a></li>
                <li><a href="#"><span>02</span> Crew</a></li>
                <li><a href="#"><span>03</span> Technology</a></li>
            </ul>
        </nav>
    </header>

    <main>
        <div class="hero-content">
            <p>{body_text}</p>
            <h2>EXPLORE</h2>
        </div>
    </main>
</div>

<script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = """// Mobile Navigation Logic extracted from tutorial
const nav = document.querySelector(".primary-navigation");
const navToggle = document.querySelector(".mobile-nav-toggle");

// Event listener for the hamburger button
navToggle.addEventListener("click", () => {
    // Check the custom data attribute state
    const visibility = nav.getAttribute("data-visible");

    // If it's closed, open it
    if (visibility === "false") {
        nav.setAttribute("data-visible", "true");
        navToggle.setAttribute("aria-expanded", "true");
    } 
    // If it's open, close it
    else {
        nav.setAttribute("data-visible", "false");
        navToggle.setAttribute("aria-expanded", "false");
    }
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
