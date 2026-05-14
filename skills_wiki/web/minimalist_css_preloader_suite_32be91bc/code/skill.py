def create_component(
    output_dir: str,
    title_text: str = "CSS Preloader Suite",
    body_text: str = "Lightweight, GPU-accelerated loading animations using pure CSS.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#00bfff",     # CSS hex color for accent
    width_px: int = 1000,
    height_px: int = 600,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing minimalist CSS preloaders.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors ===
    if color_scheme == "dark":
        bg_color = "#0d111c"
        text_color = "#f0f0f0"
        surface_color = "rgba(255, 255, 255, 0.04)"
        border_color = "rgba(255, 255, 255, 0.08)"
    else:
        bg_color = "#f8f9fa"
        text_color = "#1a1a2e"
        surface_color = "#ffffff"
        border_color = "rgba(0, 0, 0, 0.1)"

    # Hardcoded vibrant palette for the flip animation stages
    c2 = "#ff4757" # Red
    c3 = "#eccc68" # Yellow
    c4 = "#2ed573" # Green

    # === CSS ===
    css = f"""/* CSS Preloader Suite */
:root {{
    --bg: {bg_color};
    --text: {text_color};
    --accent: {accent_color};
    --surface: {surface_color};
    --border: {border_color};
    --width: {width_px}px;
    --height: {height_px}px;
    
    --c2: {c2};
    --c3: {c3};
    --c4: {c4};
}}

*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: 'Inter', system-ui, sans-serif;
    background: var(--bg);
    color: var(--text);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 2rem;
}}

.container {{
    width: 100%;
    max-width: var(--width);
    min-height: var(--height);
    display: flex;
    flex-direction: column;
    gap: 3rem;
}}

.header {{
    text-align: center;
}}

.title {{
    font-size: 2.5rem;
    font-weight: 700;
    letter-spacing: -0.03em;
    margin-bottom: 0.5rem;
}}

.body-text {{
    font-size: 1.1rem;
    opacity: 0.7;
}}

/* Grid Layout for Cards */
.loader-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 2rem;
}}

.card {{
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 3rem 2rem;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 3rem;
    box-shadow: 0 10px 30px rgba(0,0,0,0.05);
    transition: transform 0.3s ease;
}}

.card:hover {{
    transform: translateY(-5px);
}}

.card-label {{
    font-size: 0.9rem;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    font-weight: 600;
    opacity: 0.8;
}}

/* =========================================
   1. Pulse Ripple Loader
   ========================================= */
.loader-pulse {{
    position: relative;
    width: 80px;
    height: 80px;
    display: flex;
    justify-content: center;
    align-items: center;
}}

.pulse-core {{
    width: 24px;
    height: 24px;
    background-color: var(--accent);
    border-radius: 50%;
    position: relative;
    z-index: 2;
}}

.pulse-ring {{
    position: absolute;
    width: 100%;
    height: 100%;
    background-color: var(--accent);
    border-radius: 50%;
    opacity: 0;
    animation: pulse-anim 2s cubic-bezier(0.215, 0.61, 0.355, 1) infinite;
}}

.pulse-ring:nth-child(2) {{ animation-delay: 0.6s; }}
.pulse-ring:nth-child(3) {{ animation-delay: 1.2s; }}

@keyframes pulse-anim {{
    0% {{
        transform: scale(0.3);
        opacity: 0.8;
    }}
    100% {{
        transform: scale(1.5);
        opacity: 0;
    }}
}}

/* =========================================
   2. Morphing Flip Loader
   ========================================= */
.loader-flip {{
    width: 50px;
    height: 50px;
    background-color: var(--accent);
    animation: flip-anim 2.4s infinite ease-in-out;
    border-radius: 4px;
}}

@keyframes flip-anim {{
    0% {{ 
        transform: perspective(120px) rotateX(0deg) rotateY(0deg); 
        background-color: var(--accent);
    }}
    25% {{ 
        transform: perspective(120px) rotateX(-180deg) rotateY(0deg); 
        background-color: var(--c2);
    }}
    50% {{ 
        transform: perspective(120px) rotateX(-180deg) rotateY(-180deg); 
        background-color: var(--c3);
    }}
    75% {{ 
        transform: perspective(120px) rotateX(0deg) rotateY(-180deg); 
        background-color: var(--c4);
    }}
    100% {{ 
        transform: perspective(120px) rotateX(0deg) rotateY(0deg); 
        background-color: var(--accent);
    }}
}}

/* =========================================
   3. Orbit Spinner Loader
   ========================================= */
.loader-orbit {{
    position: relative;
    width: 80px;
    height: 80px;
    animation: spin-anim 2s linear infinite;
}}

.orbit-core {{
    position: absolute;
    top: 50%; left: 50%;
    transform: translate(-50%, -50%);
    width: 20px; height: 20px;
    background-color: var(--accent);
    border-radius: 50%;
}}

.orbit-satellite {{
    position: absolute;
    width: 14px; height: 14px;
    border-radius: 50%;
}}

.orbit-satellite.s1 {{
    top: 0; left: 50%;
    transform: translateX(-50%);
    background-color: var(--c2);
}}

.orbit-satellite.s2 {{
    bottom: 0; left: 50%;
    transform: translateX(-50%);
    background-color: var(--c3);
}}

.orbit-satellite.s3 {{
    top: 50%; left: 0;
    transform: translateY(-50%);
    background-color: var(--c4);
}}

@keyframes spin-anim {{
    0% {{ transform: rotate(0deg); }}
    100% {{ transform: rotate(360deg); }}
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
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        <header class="header">
            <h1 class="title">{title_text}</h1>
            <p class="body-text">{body_text}</p>
        </header>

        <div class="loader-grid">
            
            <!-- Card 1: Pulse Ripple -->
            <div class="card">
                <div class="loader-pulse">
                    <div class="pulse-ring"></div>
                    <div class="pulse-ring"></div>
                    <div class="pulse-ring"></div>
                    <div class="pulse-core"></div>
                </div>
                <div class="card-label">Pulse Ripple</div>
            </div>

            <!-- Card 2: Morphing Flip -->
            <div class="card">
                <div class="loader-flip"></div>
                <div class="card-label">Morphing Flip</div>
            </div>

            <!-- Card 3: Orbit Spinner -->
            <div class="card">
                <div class="loader-orbit">
                    <div class="orbit-core"></div>
                    <div class="orbit-satellite s1"></div>
                    <div class="orbit-satellite s2"></div>
                    <div class="orbit-satellite s3"></div>
                </div>
                <div class="card-label">Orbit Spinner</div>
            </div>

        </div>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// CSS Preloader Suite
document.addEventListener('DOMContentLoaded', () => {{
    // The preloaders in this suite are 100% CSS-driven for maximum performance.
    // JavaScript is not required for the animations.
    
    console.log("Preloaders initialized. Running on compositor thread.");
    
    // Example: Logic to hide preloaders after load could go here.
    /*
    setTimeout(() => {{
        document.querySelector('.loader-grid').style.opacity = '0';
    }}, 5000);
    */
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
