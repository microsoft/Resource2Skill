def create_component(
    output_dir: str,
    title_text: str = "Fluid Hamburger Menu",
    body_text: str = "Click the icon below to trigger the fluid CSS transition from a hamburger menu into an exact centered 'X'.",
    color_scheme: str = "dark",
    accent_color: str = "#ffffff",
    width_px: int = 800,
    height_px: int = 600,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Fluid CSS Hamburger-to-Close Animation.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors ===
    if color_scheme == "dark":
        bg_color = "#272727"
        text_color = "#f0f0f0"
    else:
        bg_color = "#e9ecef"
        text_color = "#212529"
        if accent_color.lower() == "#ffffff": 
            accent_color = "#121212" # Ensure contrast in light mode

    # === CSS ===
    css = f"""/* Fluid CSS Hamburger Animation */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --text: {text_color};
    --accent: {accent_color};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background: var(--bg);
    color: var(--text);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
}}

.container {{
    width: var(--width);
    height: var(--height);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 40px;
    text-align: center;
    padding: 2rem;
}}

.text-content h1 {{
    font-weight: 600;
    font-size: 2rem;
    margin-bottom: 0.5rem;
    letter-spacing: -0.02em;
}}

.text-content p {{
    font-weight: 300;
    font-size: 1rem;
    max-width: 400px;
    opacity: 0.8;
    line-height: 1.5;
}}

/* === Hamburger Menu Component === */
.menu-btn {{
    /* Scalable Variables */
    --size: 80px;
    --bar-width: 50px;
    --bar-height: 6px;
    --bar-gap: 16px;
    --anim-duration: 0.5s;
    
    /* Mathematical offset for perfect 45deg X centering: width * sin(45) */
    --anim-offset: calc(var(--bar-width) * 0.7071);
    
    position: relative;
    display: flex;
    justify-content: center;
    align-items: center;
    width: var(--size);
    height: var(--size);
    cursor: pointer;
    transition: all var(--anim-duration) ease-in-out;
    border-radius: 8px;
    outline: none;
}}

/* Focus state for accessibility */
.menu-btn:focus-visible {{
    box-shadow: 0 0 0 3px rgba(255, 255, 255, 0.3);
}}

/* The Lines */
.menu-btn__burger,
.menu-btn__burger::before,
.menu-btn__burger::after {{
    width: var(--bar-width);
    height: var(--bar-height);
    background: var(--accent);
    border-radius: 5px;
    transition: all var(--anim-duration) ease-in-out;
}}

.menu-btn__burger {{
    position: relative;
}}

.menu-btn__burger::before,
.menu-btn__burger::after {{
    content: '';
    position: absolute;
    left: 0;
}}

/* Initial Offsets */
.menu-btn__burger::before {{
    transform: translateY(calc(var(--bar-gap) * -1));
}}
.menu-btn__burger::after {{
    transform: translateY(var(--bar-gap));
}}

/* === OPEN STATE === */

/* Middle bar slides left and disappears */
.menu-btn.open .menu-btn__burger {{
    transform: translateX(calc(var(--bar-width) * -1));
    background: transparent;
}}

/* Top bar rotates and slides to center */
.menu-btn.open .menu-btn__burger::before {{
    transform: rotate(45deg) translate(var(--anim-offset), calc(var(--anim-offset) * -1));
}}

/* Bottom bar rotates and slides to center */
.menu-btn.open .menu-btn__burger::after {{
    transform: rotate(-45deg) translate(var(--anim-offset), var(--anim-offset));
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
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        <div class="text-content">
            <h1>{title_text}</h1>
            <p>{body_text}</p>
        </div>
        
        <!-- Component Target -->
        <div class="menu-btn" id="menu-btn" role="button" aria-label="Toggle menu" aria-expanded="false" tabindex="0">
            <div class="menu-btn__burger"></div>
        </div>
        
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Fluid Hamburger State Logic
document.addEventListener('DOMContentLoaded', () => {{
    const menuBtn = document.getElementById('menu-btn');
    let isMenuOpen = false;

    // Core toggle function
    const toggleMenu = () => {{
        isMenuOpen = !isMenuOpen;
        
        if (isMenuOpen) {{
            menuBtn.classList.add('open');
            menuBtn.setAttribute('aria-expanded', 'true');
        }} else {{
            menuBtn.classList.remove('open');
            menuBtn.setAttribute('aria-expanded', 'false');
        }}
    }};

    // Support Click
    menuBtn.addEventListener('click', toggleMenu);

    // Support Keyboard Navigation (Accessibility)
    menuBtn.addEventListener('keydown', (e) => {{
        if (e.key === 'Enter' || e.key === ' ') {{
            e.preventDefault(); // Prevent page scroll on spacebar
            toggleMenu();
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
