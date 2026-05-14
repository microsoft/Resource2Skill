def create_component(
    output_dir: str,
    title_text: str = "Glassmorphism UI",
    body_text: str = "Scroll down to observe the frosted glass effect floating over the content.",
    color_scheme: str = "light",        # "dark" or "light" (determines glass tint)
    accent_color: str = "#ffd679",     # CSS hex color for link text
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Glassmorphism Navbar effect.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors ===
    if color_scheme == "dark":
        # Dark tinted glass for light backgrounds
        glass_bg = "rgba(10, 10, 15, 0.45)"
        glass_border = "rgba(255, 255, 255, 0.08)"
        glass_shadow = "rgba(0, 0, 0, 0.6)"
        underline_color = "#ffffff"
        text_color = "#f0f0f0"
        bg_url = "https://images.unsplash.com/photo-1550684848-fac1c5b4e853?q=80&w=2564&auto=format&fit=crop"
    else:
        # Light frosted glass for dark/colorful backgrounds (as seen in the tutorial)
        glass_bg = "rgba(255, 255, 255, 0.15)"
        glass_border = "rgba(255, 255, 255, 0.5)"
        glass_shadow = "rgba(0, 0, 0, 0.2)"
        underline_color = "#ffffff"
        text_color = "#ffffff"
        bg_url = "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?q=80&w=2564&auto=format&fit=crop"

    # === CSS ===
    css = f"""/* Glassmorphism Navbar Styles */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --glass-bg: {glass_bg};
    --glass-border: {glass_border};
    --glass-shadow: {glass_shadow};
    --accent: {accent_color};
    --underline: {underline_color};
    --text: {text_color};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    display: flex;
    align-items: center;
    justify-content: center;
    background: #111;
    min-height: 100vh;
}}

/* Mock browser window/viewport to bound the demo */
.viewport {{
    width: var(--width);
    height: var(--height);
    max-width: 100vw;
    max-height: 100vh;
    position: relative;
    overflow-y: auto;
    overflow-x: hidden;
    background-image: url('{bg_url}');
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}}

/* Sticky container to hold the nav at the top */
.nav-wrapper {{
    position: sticky;
    top: 2rem;
    display: flex;
    justify-content: center;
    z-index: 1000;
    width: 100%;
    padding: 0 2rem;
}}

.glass-nav {{
    width: 100%;
    max-width: 900px;
    background: var(--glass-bg);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px); /* Safari support */
    padding: 1.2rem 2rem;
    border-radius: 40px;
    border: 1px solid var(--glass-border);
    box-shadow: 0 6px 15px var(--glass-shadow);
}}

.glass-nav ul {{
    list-style: none;
    display: flex;
    justify-content: center;
    gap: 3rem;
}}

.glass-nav a {{
    text-decoration: none;
    color: var(--accent);
    font-weight: 500;
    font-size: 1.1rem;
    position: relative;
    padding: 5px 0;
    transition: color 0.3s ease;
    letter-spacing: 0.5px;
}}

/* Center-out expanding underline */
.glass-nav a::after {{
    content: '';
    position: absolute;
    width: 0;
    height: 2px;
    background: var(--underline);
    bottom: -2px;
    left: 50%;
    transform: translateX(-50%);
    transition: width 0.3s ease;
    border-radius: 2px;
}}

.glass-nav a:hover::after {{
    width: 100%;
}}

/* Background content to demonstrate scrolling behind glass */
.content-layer {{
    padding: 10rem 3rem 5rem;
    color: var(--text);
    text-align: center;
    max-width: 800px;
    margin: 0 auto;
}}

.content-layer h1 {{
    font-size: 3.5rem;
    margin-bottom: 1.5rem;
    text-shadow: 0 4px 12px rgba(0,0,0,0.4);
}}

.content-layer p {{
    font-size: 1.2rem;
    line-height: 1.6;
    text-shadow: 0 2px 8px rgba(0,0,0,0.4);
}}

.spacer {{
    height: 150vh;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.5rem;
    color: rgba(255,255,255,0.5);
}}
"""

    # === HTML ===
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Glassmorphism Navbar</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="viewport">
        <!-- Floating Glass Navigation -->
        <div class="nav-wrapper">
            <nav class="glass-nav">
                <ul>
                    <li><a href="#">Home</a></li>
                    <li><a href="#">About</a></li>
                    <li><a href="#">Services</a></li>
                    <li><a href="#">Portfolio</a></li>
                    <li><a href="#">Contact</a></li>
                </ul>
            </nav>
        </div>
        
        <!-- Underlying Content -->
        <div class="content-layer">
            <h1 class="hero-title">{title_text}</h1>
            <p>{body_text}</p>
        </div>
        <div class="spacer">
            <p>Scroll up and down to preview the blur effect.</p>
        </div>
    </div>
    
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Minimal JS interaction to enhance the entrance
document.addEventListener('DOMContentLoaded', () => {{
    const nav = document.querySelector('.glass-nav');
    const title = document.querySelector('.hero-title');
    
    // Entrance animation setup
    nav.style.opacity = '0';
    nav.style.transform = 'translateY(-20px)';
    nav.style.transition = 'all 0.8s cubic-bezier(0.16, 1, 0.3, 1)';
    
    title.style.opacity = '0';
    title.style.transform = 'translateY(20px)';
    title.style.transition = 'all 1s cubic-bezier(0.16, 1, 0.3, 1) 0.2s';
    
    // Trigger animations after a slight delay
    setTimeout(() => {{
        nav.style.opacity = '1';
        nav.style.transform = 'translateY(0)';
        
        title.style.opacity = '1';
        title.style.transform = 'translateY(0)';
    }}, 100);
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
