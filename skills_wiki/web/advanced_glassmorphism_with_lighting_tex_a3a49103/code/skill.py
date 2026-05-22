def create_component(
    output_dir: str,
    title_text: str = "Glassmorphism UI",
    body_text: str = "A deep dive into layered transparency, background blur, and lighting effects to create tactile web interfaces.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#00bfff",     # CSS hex color for accent
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Advanced Glassmorphism visual effect.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors ===
    if color_scheme == "dark":
        bg_base = "#0f111a"
        text_main = "#ffffff"
        text_muted = "rgba(255, 255, 255, 0.7)"
        glass_fill = "rgba(30, 32, 40, 0.45)"
        glass_border_tl = "rgba(255, 255, 255, 0.25)"
        glass_border_br = "rgba(255, 255, 255, 0.05)"
        glass_shadow = "rgba(0, 0, 0, 0.5)"
        orb1_color = "rgba(0, 191, 255, 0.6)"
        orb2_color = "rgba(138, 43, 226, 0.6)"
        pat_start = "rgba(255, 255, 255, 0.15)"
        pat_end = "rgba(0, 0, 0, 0.3)"
    else:
        bg_base = "#e2e8f0"
        text_main = "#0f172a"
        text_muted = "rgba(15, 23, 42, 0.7)"
        glass_fill = "rgba(255, 255, 255, 0.5)"
        glass_border_tl = "rgba(255, 255, 255, 0.9)"
        glass_border_br = "rgba(255, 255, 255, 0.2)"
        glass_shadow = "rgba(30, 41, 59, 0.1)"
        orb1_color = "rgba(0, 191, 255, 0.4)"
        orb2_color = "rgba(255, 105, 180, 0.4)"
        pat_start = "rgba(255, 255, 255, 0.8)"
        pat_end = "rgba(0, 0, 0, 0.05)"

    # Escape HTML inputs safely
    import html as html_lib
    safe_title = html_lib.escape(title_text)
    safe_body = html_lib.escape(body_text)

    # === CSS ===
    css = f"""/* Advanced Glassmorphism — generated component */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg-base: {bg_base};
    --text-main: {text_main};
    --text-muted: {text_muted};
    --accent: {accent_color};
    --glass-fill: {glass_fill};
    --glass-border-tl: {glass_border_tl};
    --glass-border-br: {glass_border_br};
    --glass-shadow: {glass_shadow};
    --orb-1: {orb1_color};
    --orb-2: {orb2_color};
    --pat-start: {pat_start};
    --pat-end: {pat_end};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background-color: #000;
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
}}

.scene {{
    width: var(--width);
    height: var(--height);
    background-color: var(--bg-base);
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
}}

/* Dynamic Background Orbs */
.background-orbs {{
    position: absolute;
    top: 0; left: 0; width: 100%; height: 100%;
    z-index: 1;
    pointer-events: none;
}}

.orb-wrapper {{
    position: absolute;
    transition: transform 0.1s ease-out;
}}

.orb-1-wrapper {{ top: 15%; left: 25%; }}
.orb-2-wrapper {{ bottom: 15%; right: 20%; }}

.orb {{
    border-radius: 50%;
    filter: blur(80px);
    animation: float 8s infinite alternate ease-in-out;
}}

.orb-1 {{
    width: 400px; height: 400px;
    background: var(--orb-1);
}}

.orb-2 {{
    width: 500px; height: 500px;
    background: var(--orb-2);
    animation-delay: -4s;
}}

@keyframes float {{
    0% {{ transform: translate(0, 0) scale(1); }}
    100% {{ transform: translate(40px, -40px) scale(1.1); }}
}}

/* Glass Cards Layout */
.cards-container {{
    display: flex;
    gap: 40px;
    z-index: 10;
    padding: 20px;
}}

.glass-card {{
    width: 380px;
    border-radius: 24px;
    padding: 40px 32px;
    color: var(--text-main);
    
    /* Core Glass Blur Engine */
    -webkit-backdrop-filter: blur(24px);
    backdrop-filter: blur(24px);
    
    /* Edge Lighting Simulation */
    border: 1px solid transparent;
    border-top-color: var(--glass-border-tl);
    border-left-color: var(--glass-border-tl);
    border-bottom-color: var(--glass-border-br);
    border-right-color: var(--glass-border-br);
    
    box-shadow: 0 16px 40px var(--glass-shadow);
    transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1), box-shadow 0.3s ease;
}}

.glass-card:hover {{
    transform: translateY(-8px);
    box-shadow: 0 24px 48px var(--glass-shadow);
}}

/* Level 2: Clean Glass Fill */
.glass-card.clean {{
    background-color: var(--glass-fill);
}}

/* Level 3: Textured / Ribbed Glass */
.glass-card.patterned {{
    background-color: transparent;
    background-image: linear-gradient(
        120deg, 
        var(--pat-start), 
        var(--pat-end)
    );
    /* Bounding the gradient to force repeating, creating the ridge */
    background-size: 30px 30px;
    background-repeat: repeat;
}}

/* Typography & Content inside Glass */
.badge {{
    display: inline-block;
    padding: 6px 14px;
    border-radius: 20px;
    background: rgba(128, 128, 128, 0.2);
    color: var(--text-main);
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-bottom: 20px;
    border: 1px solid var(--glass-border-tl);
}}

.title {{
    font-size: 1.75rem;
    font-weight: 700;
    margin-bottom: 12px;
    line-height: 1.2;
}}

.body-text {{
    font-size: 1rem;
    color: var(--text-muted);
    line-height: 1.6;
    margin-bottom: 32px;
}}

.footer {{
    display: flex;
    gap: 12px;
}}

.btn {{
    padding: 12px 24px;
    border-radius: 12px;
    font-size: 0.95rem;
    font-weight: 600;
    cursor: pointer;
    background: rgba(255, 255, 255, 0.05);
    color: var(--text-main);
    border: 1px solid var(--glass-border-tl);
    transition: all 0.2s ease;
}}

.btn:hover {{
    background: rgba(255, 255, 255, 0.15);
}}

.btn.primary {{
    background: var(--accent);
    color: #fff;
    border: none;
}}

.btn.primary:hover {{
    filter: brightness(1.15);
    box-shadow: 0 0 20px rgba(0, 0, 0, 0.2);
}}
"""

    # === HTML ===
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Advanced Glassmorphism</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="scene">
        
        <div class="background-orbs">
            <div class="orb-wrapper orb-1-wrapper">
                <div class="orb orb-1"></div>
            </div>
            <div class="orb-wrapper orb-2-wrapper">
                <div class="orb orb-2"></div>
            </div>
        </div>
        
        <div class="cards-container">
            <!-- Level 2 Technique: Clean fill via RGBA -->
            <div class="glass-card clean">
                <span class="badge">Clean Glass</span>
                <h2 class="title">{safe_title}</h2>
                <p class="body-text">{safe_body}</p>
                <div class="footer">
                    <button class="btn primary">Explore</button>
                </div>
            </div>

            <!-- Level 3 Technique: Ribbed Texture via Gradient Size -->
            <div class="glass-card patterned">
                <span class="badge">Textured Glass</span>
                <h2 class="title">Physical Ridges</h2>
                <p class="body-text">By repeating a linear gradient at a small background size, we simulate the lighting physics of ribbed architectural glass.</p>
                <div class="footer">
                    <button class="btn">View Source</button>
                </div>
            </div>
        </div>

    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Mouse Parallax for Background Orbs to highlight the real-time blur effect
document.addEventListener('DOMContentLoaded', () => {{
    const scene = document.querySelector('.scene');
    const orbWrappers = document.querySelectorAll('.orb-wrapper');

    scene.addEventListener('mousemove', (e) => {{
        const rect = scene.getBoundingClientRect();
        // Normalize mouse coordinates from -0.5 to 0.5
        const x = (e.clientX - rect.left) / rect.width - 0.5;
        const y = (e.clientY - rect.top) / rect.height - 0.5;

        orbWrappers.forEach((wrapper, index) => {{
            // Deeper elements move faster for parallax depth
            const speed = (index + 1) * 80; 
            const xOffset = x * speed;
            const yOffset = y * speed;
            wrapper.style.transform = `translate(${{xOffset}}px, ${{yOffset}}px)`;
        }});
    }});
    
    // Smooth reset when mouse leaves
    scene.addEventListener('mouseleave', () => {{
        orbWrappers.forEach((wrapper) => {{
            wrapper.style.transform = `translate(0px, 0px)`;
        }});
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
