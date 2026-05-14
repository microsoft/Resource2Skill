def create_component(
    output_dir: str,
    title_text: str = "Try Declutter",
    body_text: str = "A beautiful and intuitive way to clean up your digital life. Experience clarity with our premium tools.",
    color_scheme: str = "dark",
    accent_color: str = "#ec4899", # Pink accent
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Glassmorphism Nav & Organic Mesh visual effect.
    
    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors ===
    if color_scheme == "dark":
        bg_color = "#0f172a"
        text_color = "#f8fafc"
        glass_bg = "rgba(15, 23, 42, 0.4)"
        glass_border = "rgba(255, 255, 255, 0.1)"
        glass_shadow = "rgba(0, 0, 0, 0.2)"
        # Saturated colors for dark mode mesh
        mesh_1 = accent_color
        mesh_2 = "rgba(59, 130, 246, 0.6)"  # Blue
        mesh_3 = "rgba(139, 92, 246, 0.6)"  # Purple
        mesh_4 = "rgba(16, 185, 129, 0.6)"  # Emerald
        overlay_grad = f"linear-gradient(to bottom, rgba(15, 23, 42, 0) 0%, {bg_color} 100%)"
    else:
        bg_color = "#ffffff"
        text_color = "#0f172a"
        glass_bg = "rgba(255, 255, 255, 0.5)"
        glass_border = "rgba(255, 255, 255, 0.6)"
        glass_shadow = "rgba(0, 0, 0, 0.05)"
        # Lighter pastel colors for light mode mesh
        mesh_1 = accent_color
        mesh_2 = "rgba(147, 197, 253, 0.8)" # Blue
        mesh_3 = "rgba(196, 181, 253, 0.8)" # Purple
        mesh_4 = "rgba(110, 231, 183, 0.8)" # Emerald
        overlay_grad = f"linear-gradient(to bottom, rgba(255, 255, 255, 0) 0%, {bg_color} 100%)"

    # === CSS ===
    css = f"""/* Glassmorphism Nav & Mesh Background — generated component */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --text: {text_color};
    --accent: {accent_color};
    --glass-bg: {glass_bg};
    --glass-border: {glass_border};
    --glass-shadow: {glass_shadow};
    --mesh-1: {mesh_1};
    --mesh-2: {mesh_2};
    --mesh-3: {mesh_3};
    --mesh-4: {mesh_4};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background: #000;
    color: var(--text);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
}}

.container {{
    width: var(--width);
    height: var(--height);
    position: relative;
    background: var(--bg);
    overflow: hidden;
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
    /* For standalone component demo rounding */
    border-radius: 12px; 
}}

/* --- 1. The Gradient Mesh --- */
@keyframes mesh-drift {{
    0% {{ transform: scale(1) translate(0, 0); }}
    50% {{ transform: scale(1.1) translate(2%, 3%); }}
    100% {{ transform: scale(1) translate(0, 0); }}
}}

.mesh-bg {{
    position: absolute;
    /* Bleed out edges so animation doesn't show hard cuts */
    inset: -20%; 
    background-color: var(--bg);
    background-image: 
        radial-gradient(circle at 20% 20%, var(--mesh-1) 0%, transparent 50%),
        radial-gradient(circle at 80% 20%, var(--mesh-2) 0%, transparent 50%),
        radial-gradient(circle at 80% 80%, var(--mesh-3) 0%, transparent 50%),
        radial-gradient(circle at 20% 80%, var(--mesh-4) 0%, transparent 50%);
    animation: mesh-drift 15s ease-in-out infinite;
    z-index: 0;
}}

/* --- 2. The Fade Overlay --- */
.mesh-overlay {{
    position: absolute;
    inset: 0;
    background: {overlay_grad};
    pointer-events: none;
    z-index: 1;
}}

/* --- 3. Glassmorphism Navigation --- */
.glass-nav {{
    position: absolute;
    top: 24px;
    left: 24px;
    right: 24px;
    height: 64px;
    padding: 0 32px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    background: var(--glass-bg);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border: 1px solid var(--glass-border);
    border-radius: 16px;
    box-shadow: 0 4px 24px var(--glass-shadow);
    z-index: 10;
}}

.logo {{
    font-weight: 700;
    font-size: 18px;
    display: flex;
    align-items: center;
    gap: 12px;
    letter-spacing: -0.02em;
}}

.logo-icon {{
    width: 24px;
    height: 24px;
    background: var(--accent);
    border-radius: 6px;
}}

.nav-links {{
    display: flex;
    gap: 32px;
}}

.nav-links a {{
    color: var(--text);
    text-decoration: none;
    font-weight: 500;
    font-size: 14px;
    opacity: 0.7;
    transition: opacity 0.2s;
}}

.nav-links a:hover {{
    opacity: 1;
}}

/* --- 4. Hero Content Layout --- */
.hero {{
    position: absolute;
    inset: 0;
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 48px;
    align-items: center;
    padding: 100px 64px 40px; 
    z-index: 2;
}}

.hero-text {{
    max-width: 500px;
}}

.title {{
    font-size: 56px;
    font-weight: 700;
    line-height: 1.1;
    margin-bottom: 24px;
    letter-spacing: -0.02em;
}}

.body-text {{
    font-size: 18px;
    line-height: 1.6;
    margin-bottom: 40px;
    opacity: 0.8;
}}

.buttons {{
    display: flex;
    gap: 16px;
}}

.btn-primary {{
    background: var(--accent);
    color: #fff;
    padding: 14px 28px;
    border-radius: 12px;
    border: none;
    font-family: 'Inter', sans-serif;
    font-weight: 600;
    font-size: 15px;
    cursor: pointer;
    transition: transform 0.2s, box-shadow 0.2s, filter 0.2s;
}}

.btn-primary:hover {{
    transform: translateY(-2px);
    box-shadow: 0 8px 16px var(--glass-shadow);
    filter: brightness(1.1);
}}

.btn-secondary {{
    background: transparent;
    color: var(--text);
    padding: 14px 28px;
    border-radius: 12px;
    border: 1px solid var(--text);
    font-family: 'Inter', sans-serif;
    font-weight: 600;
    font-size: 15px;
    cursor: pointer;
    transition: background 0.2s;
}}

.btn-secondary:hover {{
    background: var(--glass-bg);
}}

/* --- 5. Interactive Glass Asset --- */
.hero-visual {{
    display: flex;
    justify-content: center;
    perspective: 1000px;
}}

.glass-card {{
    width: 100%;
    max-width: 340px;
    height: 480px;
    background: var(--glass-bg);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    border: 1px solid var(--glass-border);
    border-radius: 32px;
    box-shadow: 0 24px 48px var(--glass-shadow);
    display: flex;
    flex-direction: column;
    /* Will be overridden by JS, this is for smooth return to rest */
    transition: transform 0.4s cubic-bezier(0.25, 1, 0.5, 1);
    transform-style: preserve-3d;
}}

.card-header {{
    height: 64px;
    border-bottom: 1px solid var(--glass-border);
    display: flex;
    align-items: center;
    padding: 0 24px;
}}

.card-avatar {{
    width: 28px;
    height: 28px;
    border-radius: 50%;
    background: var(--glass-border);
}}

.card-body {{
    padding: 32px 24px;
    display: flex;
    flex-direction: column;
    gap: 16px;
    flex-grow: 1;
}}

.card-line {{
    height: 12px;
    border-radius: 6px;
    background: var(--glass-border);
}}

.card-line.short {{ width: 60%; }}
.card-line.accent {{ 
    background: var(--accent); 
    opacity: 0.8;
    width: 40%; 
    margin-top: 16px;
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
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        <!-- Background Layers -->
        <div class="mesh-bg"></div>
        <div class="mesh-overlay"></div>
        
        <!-- Floating Glass Navigation -->
        <header class="glass-nav">
            <div class="logo">
                <div class="logo-icon"></div>
                Logoipsum
            </div>
            <nav class="nav-links">
                <a href="#">Home</a>
                <a href="#">About Us</a>
                <a href="#">Contact</a>
            </nav>
        </header>
        
        <!-- Hero Section -->
        <main class="hero">
            <div class="hero-text">
                <h1 class="title">{title_text}</h1>
                <p class="body-text">{body_text}</p>
                <div class="buttons">
                    <button class="btn-primary">Download Now</button>
                    <button class="btn-secondary">Buy Now $19.99</button>
                </div>
            </div>
            
            <div class="hero-visual">
                <div class="glass-card">
                    <div class="card-header">
                        <div class="card-avatar"></div>
                    </div>
                    <div class="card-body">
                        <div class="card-line"></div>
                        <div class="card-line short"></div>
                        <div class="card-line accent"></div>
                    </div>
                </div>
            </div>
        </main>
    </div>
    
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// 3D Glass Card Tilt Interaction
document.addEventListener('DOMContentLoaded', () => {{
    const container = document.querySelector('.container');
    const card = document.querySelector('.glass-card');

    if (!container || !card) return;

    container.addEventListener('mousemove', (e) => {{
        // Disable transition during movement for immediate physical response
        card.style.transition = 'none';

        const rect = container.getBoundingClientRect();
        
        // Calculate mouse position relative to container
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        
        // Find center points
        const centerX = rect.width / 2;
        const centerY = rect.height / 2;
        
        // Calculate rotation based on distance from center (max 8 degrees)
        const rotateX = ((y - centerY) / centerY) * -8;
        const rotateY = ((x - centerX) / centerX) * 8;
        
        card.style.transform = `rotateX(${{rotateX}}deg) rotateY(${{rotateY}}deg)`;
    }});

    // Reset card position on mouse leave
    container.addEventListener('mouseleave', () => {{
        card.style.transition = 'transform 0.5s cubic-bezier(0.25, 1, 0.5, 1)';
        card.style.transform = `rotateX(0deg) rotateY(0deg)`;
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
