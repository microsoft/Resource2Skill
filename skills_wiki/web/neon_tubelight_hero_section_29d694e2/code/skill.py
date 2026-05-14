def create_component(
    output_dir: str,
    title_text: str = "Find Every Hidden Threat in Your System — Before It Finds You.",
    body_text: str = "Futuristic Mask scans your system, detects AI-level threats, and fixes them instantly — securing your future today.",
    color_scheme: str = "dark",
    accent_color: str = "#2563eb",
    width_px: int = 1440,
    height_px: int = 900,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Neon Tubelight Hero visual effect.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Convert Hex to RGB string for CSS variables (to use with rgba())
    hex_color = accent_color.lstrip('#')
    if len(hex_color) == 3:
        hex_color = ''.join(c + c for c in hex_color)
    r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    accent_rgb = f"{r}, {g}, {b}"

    if color_scheme == "dark":
        bg_color = "#070b14"
        text_primary = "#ffffff"
        text_secondary = "rgba(255, 255, 255, 0.7)"
        nav_bg = "rgba(255, 255, 255, 0.05)"
    else:
        # Tubelight effect is inherently a "dark mode" aesthetic. 
        # In light mode, we invert to a bright theme but keep the accent vivid.
        bg_color = "#f4f6fa"
        text_primary = "#0f172a"
        text_secondary = "rgba(15, 23, 42, 0.7)"
        nav_bg = "rgba(0, 0, 0, 0.05)"

    css = f"""/* Neon Tubelight Hero — generated component */
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap');

*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg-color: {bg_color};
    --text-primary: {text_primary};
    --text-secondary: {text_secondary};
    --accent-hex: {accent_color};
    --accent-rgb: {accent_rgb};
    --nav-bg: {nav_bg};
    
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Poppins', sans-serif;
    background: var(--bg-color);
    color: var(--text-primary);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow-x: hidden;
}}

.hero-section {{
    width: 100%;
    max-width: var(--width);
    height: var(--height);
    position: relative;
    overflow: hidden;
    display: flex;
    flex-direction: column;
    background: var(--bg-color);
    box-shadow: 0 0 50px rgba(0,0,0,0.5);
}}

/* --- NAVIGATION --- */
.navbar {{
    position: relative;
    z-index: 10;
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 30px 60px;
}}

.logo {{
    font-size: 24px;
    font-weight: 700;
    letter-spacing: 1px;
    display: flex;
    align-items: center;
    gap: 10px;
}}

.logo-icon {{
    width: 40px;
    height: 40px;
    background: var(--accent-hex);
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 4px 15px rgba(var(--accent-rgb), 0.4);
}}

.logo-icon svg {{
    width: 20px;
    height: 20px;
    fill: #fff;
}}

.nav-links {{
    display: flex;
    gap: 40px;
    list-style: none;
}}

.nav-links a {{
    color: var(--text-secondary);
    text-decoration: none;
    font-size: 15px;
    font-weight: 500;
    transition: color 0.3s ease;
}}

.nav-links a:hover {{
    color: var(--text-primary);
}}

.btn {{
    background: var(--accent-hex);
    color: #ffffff;
    border: none;
    padding: 12px 28px;
    border-radius: 30px;
    font-family: 'Poppins', sans-serif;
    font-weight: 500;
    font-size: 15px;
    cursor: pointer;
    transition: all 0.3s ease;
    box-shadow: 0 4px 15px rgba(var(--accent-rgb), 0.3);
}}

.btn:hover {{
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(var(--accent-rgb), 0.5);
}}

/* --- HERO CONTENT --- */
.hero-content {{
    position: relative;
    z-index: 10;
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    padding: 0 20px;
    margin-top: -50px;
    transform-style: preserve-3d;
}}

.hero-title {{
    font-size: clamp(40px, 5vw, 64px);
    font-weight: 700;
    line-height: 1.2;
    max-width: 900px;
    margin-bottom: 24px;
    letter-spacing: -1px;
}}

.hero-subtitle {{
    font-size: clamp(16px, 2vw, 20px);
    font-weight: 400;
    color: var(--text-secondary);
    max-width: 650px;
    line-height: 1.6;
    margin-bottom: 40px;
}}

/* --- TUBELIGHT EFFECT --- */
.tubelight-container {{
    position: absolute;
    bottom: 0;
    left: 0;
    width: 100%;
    height: 100%;
    pointer-events: none;
    z-index: 1;
    overflow: hidden;
}}

/* 1. The wide, soft volumetric beam spreading upwards */
.tubelight-beam {{
    position: absolute;
    bottom: -10%;
    left: 50%;
    transform: translateX(-50%);
    width: 150%;
    height: 80%;
    background: radial-gradient(ellipse at bottom center, rgba(var(--accent-rgb), 0.6) 0%, rgba(var(--accent-rgb), 0.1) 40%, transparent 70%);
    mix-blend-mode: screen;
    filter: blur(40px);
    animation: pulseGlow 6s ease-in-out infinite alternate;
}}

/* 2. The concentrated neon glow near the base */
.tubelight-glow {{
    position: absolute;
    bottom: -20px;
    left: 50%;
    transform: translateX(-50%);
    width: 60%;
    height: 150px;
    background: rgba(var(--accent-rgb), 0.8);
    filter: blur(80px);
    border-radius: 50%;
    mix-blend-mode: screen;
}}

/* 3. The physical "tube" bulb core - bright white line */
.tubelight-core {{
    position: absolute;
    bottom: -5px;
    left: 50%;
    transform: translateX(-50%);
    width: 40%;
    height: 12px;
    background: #ffffff;
    border-radius: 50%;
    filter: blur(4px);
    box-shadow: 0 -10px 40px 10px rgba(var(--accent-rgb), 1),
                0 0 80px 20px rgba(var(--accent-rgb), 0.8);
}}

@keyframes pulseGlow {{
    0% {{ opacity: 0.8; transform: translateX(-50%) scaleY(1); }}
    100% {{ opacity: 1; transform: translateX(-50%) scaleY(1.05); }}
}}

/* Responsive */
@media (max-width: 768px) {{
    .nav-links {{ display: none; }}
    .navbar {{ padding: 20px; }}
    .tubelight-core {{ width: 80%; }}
}}
"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tubelight Hero Component</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="hero-section">
        
        <!-- Tubelight Background Layers -->
        <div class="tubelight-container">
            <div class="tubelight-beam"></div>
            <div class="tubelight-glow"></div>
            <div class="tubelight-core"></div>
        </div>

        <!-- Navigation -->
        <nav class="navbar">
            <div class="logo">
                <div class="logo-icon">
                    <svg viewBox="0 0 24 24">
                        <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/>
                    </svg>
                </div>
                MASKFU
            </div>
            <ul class="nav-links">
                <li><a href="#">About</a></li>
                <li><a href="#">Pricing</a></li>
                <li><a href="#">Roadmap</a></li>
                <li><a href="#">Blog</a></li>
            </ul>
            <button class="btn">Contact Us</button>
        </nav>

        <!-- Hero Content -->
        <div class="hero-content">
            <h1 class="hero-title">{title_text}</h1>
            <p class="hero-subtitle">{body_text}</p>
            <button class="btn" style="padding: 16px 36px; font-size: 16px;">Join the Future</button>
        </div>

    </div>

    <script src="script.js"></script>
</body>
</html>"""

    js = f"""// Neon Tubelight Hero — Interactive Parallax
document.addEventListener('DOMContentLoaded', () => {{
    const heroSection = document.querySelector('.hero-section');
    const heroContent = document.querySelector('.hero-content');

    // Subtle 3D perspective effect based on mouse movement
    // This gives the impression that the text is floating above the volumetric light
    heroSection.addEventListener('mousemove', (e) => {{
        const rect = heroSection.getBoundingClientRect();
        
        // Calculate mouse position relative to the center of the section (-1 to 1)
        const x = (e.clientX - rect.left) / rect.width - 0.5;
        const y = (e.clientY - rect.top) / rect.height - 0.5;

        // Apply a gentle rotation (max 4 degrees)
        const rotateY = x * 8; 
        const rotateX = y * -8; 

        // Apply transform via requestAnimationFrame for performance
        requestAnimationFrame(() => {{
            heroContent.style.transform = `perspective(1000px) rotateX(${{rotateX}}deg) rotateY(${{rotateY}}deg)`;
        }});
    }});

    // Reset transform when mouse leaves
    heroSection.addEventListener('mouseleave', () => {{
        requestAnimationFrame(() => {{
            heroContent.style.transition = 'transform 0.5s ease';
            heroContent.style.transform = `perspective(1000px) rotateX(0deg) rotateY(0deg)`;
            
            // Remove transition after it completes to restore immediate tracking
            setTimeout(() => {{
                heroContent.style.transition = '';
            }}, 500);
        }});
    }});
}});
"""

    # Write files
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
