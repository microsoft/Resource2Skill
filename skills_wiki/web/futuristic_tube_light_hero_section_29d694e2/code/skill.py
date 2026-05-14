def create_component(
    output_dir: str,
    title_text: str = "Find Every Hidden Threat in Your System — Before It Finds You.",
    body_text: str = "Futuristic Mask scans your system, detects AI-level threats, and fixes them instantly — securing your future today.",
    color_scheme: str = "dark",
    accent_color: str = "#0052ff", # Vibrant tech blue
    width_px: int = 1440,
    height_px: int = 900,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Futuristic Tube Light Hero Section.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Convert hex to RGB for CSS rgba() manipulation
    def hex_to_rgb(hex_code):
        hex_code = hex_code.lstrip('#')
        if len(hex_code) == 3:
            hex_code = ''.join(c + c for c in hex_code)
        return tuple(int(hex_code[i:i+2], 16) for i in (0, 2, 4))

    r, g, b = hex_to_rgb(accent_color)
    accent_rgb = f"{r}, {g}, {b}"

    # Theme logic
    if color_scheme == "dark":
        bg_color = "#040914"
        text_main = "#ffffff"
        text_muted = "#94a3b8"
        core_color = "#ffffff" # White hot core
        nav_text = "#e2e8f0"
    else:
        bg_color = "#f8fafc"
        text_main = "#0f172a"
        text_muted = "#475569"
        core_color = accent_color # Colored core for visibility on light bg
        nav_text = "#334155"

    css = f"""/* Futuristic Tube Light Hero Section */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg-color: {bg_color};
    --text-main: {text_main};
    --text-muted: {text_muted};
    --nav-text: {nav_text};
    --accent-hex: {accent_color};
    --accent-rgb: {accent_rgb};
    --core-color: {core_color};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background: #000;
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 100vh;
    overflow: hidden;
}}

.hero-container {{
    width: var(--width);
    height: var(--height);
    background-color: var(--bg-color);
    position: relative;
    overflow: hidden;
    display: flex;
    flex-direction: column;
    /* Optional: subtle ambient glow in the center */
    background-image: radial-gradient(circle at 50% 100%, rgba(var(--accent-rgb), 0.15) 0%, transparent 60%);
}}

/* Navigation */
.navbar {{
    position: relative;
    z-index: 10;
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 2.5rem 4rem;
}}

.logo {{
    font-size: 1.5rem;
    font-weight: 700;
    color: var(--text-main);
    letter-spacing: 0.05em;
}}

.nav-links {{
    display: flex;
    gap: 3rem;
}}

.nav-links a {{
    color: var(--nav-text);
    text-decoration: none;
    font-size: 1rem;
    font-weight: 500;
    transition: color 0.2s ease;
}}

.nav-links a:hover {{
    color: var(--accent-hex);
}}

/* Buttons */
.btn {{
    background: var(--accent-hex);
    color: #ffffff;
    border: none;
    padding: 0.75rem 1.75rem;
    border-radius: 2rem;
    font-size: 1rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
    box-shadow: 0 4px 14px rgba(var(--accent-rgb), 0.3);
}}

.btn:hover {{
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(var(--accent-rgb), 0.5);
    filter: brightness(1.1);
}}

/* Main Hero Content */
.hero-content {{
    position: relative;
    z-index: 10;
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    padding: 0 2rem;
    max-width: 900px;
    margin: 0 auto;
    margin-top: -5%; /* Visual centering adjustment */
}}

.hero-title {{
    color: var(--text-main);
    font-size: clamp(2.5rem, 4.5vw, 4.5rem);
    line-height: 1.1;
    font-weight: 700;
    margin-bottom: 1.5rem;
    letter-spacing: -0.02em;
}}

.hero-subtitle {{
    color: var(--text-muted);
    font-size: 1.125rem;
    line-height: 1.6;
    max-width: 650px;
    margin-bottom: 3rem;
}}

/* Tube Light Effect */
.tube-light-wrapper {{
    position: absolute;
    bottom: 0;
    left: 0;
    width: 100%;
    height: 60%;
    pointer-events: none;
    z-index: 1;
    display: flex;
    justify-content: center;
}}

/* The atmospheric upward beam */
.tube-beam {{
    position: absolute;
    bottom: 0;
    width: 80%;
    height: 100%;
    background: 
        radial-gradient(ellipse 80% 100% at 50% 100%, rgba(var(--accent-rgb), 0.35) 0%, transparent 60%),
        conic-gradient(from 260deg at 50% 100%, transparent 0deg, rgba(var(--accent-rgb), 0.15) 100deg, transparent 200deg);
    mix-blend-mode: screen;
    animation: beam-pulse 6s ease-in-out infinite;
}}

/* The physical neon hardware line */
.tube-core {{
    position: absolute;
    bottom: 0;
    width: 60%;
    height: 5px;
    background: var(--core-color);
    border-radius: 10px 10px 0 0;
    box-shadow:
        0 -2px 10px 1px rgba(var(--accent-rgb), 0.8),
        0 -8px 25px 4px rgba(var(--accent-rgb), 0.6),
        0 -15px 50px 8px rgba(var(--accent-rgb), 0.4),
        0 -30px 100px 20px rgba(var(--accent-rgb), 0.2);
}}

/* Cursor interactive glow */
.cursor-glow {{
    position: absolute;
    width: 600px;
    height: 600px;
    background: radial-gradient(circle, rgba(var(--accent-rgb), 0.1) 0%, transparent 60%);
    border-radius: 50%;
    pointer-events: none;
    transform: translate(-50%, -50%);
    z-index: 2;
    opacity: 0;
    transition: opacity 0.5s ease;
    mix-blend-mode: screen;
}}

.hero-container:hover .cursor-glow {{
    opacity: 1;
}}

@keyframes beam-pulse {{
    0%, 100% {{ opacity: 0.8; transform: scaleY(0.95); transform-origin: bottom; }}
    50% {{ opacity: 1; transform: scaleY(1.05); transform-origin: bottom; }}
}}
"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hero Section</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="hero-container">
        <!-- Interactive cursor glow -->
        <div class="cursor-glow"></div>
        
        <nav class="navbar">
            <div class="logo">MASKFU</div>
            <div class="nav-links">
                <a href="#">About</a>
                <a href="#">Pricing</a>
                <a href="#">Roadmap</a>
                <a href="#">Blog</a>
            </div>
            <button class="btn nav-btn">Contact Us</button>
        </nav>
        
        <main class="hero-content">
            <h1 class="hero-title">{title_text}</h1>
            <p class="hero-subtitle">{body_text}</p>
            <button class="btn main-btn">Join the Future</button>
        </main>
        
        <!-- The glowing element at the bottom -->
        <div class="tube-light-wrapper">
            <div class="tube-beam"></div>
            <div class="tube-core"></div>
        </div>
    </div>

    <script src="script.js"></script>
</body>
</html>"""

    js = """document.addEventListener('DOMContentLoaded', () => {
    const container = document.querySelector('.hero-container');
    const cursorGlow = document.querySelector('.cursor-glow');
    
    // Subtle cursor tracking for ambient light effect
    let mouseX = window.innerWidth / 2;
    let mouseY = window.innerHeight / 2;
    let glowX = mouseX;
    let glowY = mouseY;
    
    container.addEventListener('mousemove', (e) => {
        const rect = container.getBoundingClientRect();
        mouseX = e.clientX - rect.left;
        mouseY = e.clientY - rect.top;
    });

    // Smooth interpolation for the glow follow effect
    function animateGlow() {
        // Ease towards mouse position
        glowX += (mouseX - glowX) * 0.1;
        glowY += (mouseY - glowY) * 0.1;
        
        cursorGlow.style.left = `${glowX}px`;
        cursorGlow.style.top = `${glowY}px`;
        
        requestAnimationFrame(animateGlow);
    }
    
    animateGlow();
});"""

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
