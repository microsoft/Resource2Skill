def create_component(
    output_dir: str,
    title_text: str = "Pure CSS Mascot",
    body_text: str = "A fully animated character drawn entirely with HTML and CSS.",
    color_scheme: str = "light",        # "dark" or "light"
    accent_color: str = "#e63946",     # Red for the mushroom hat
    width_px: int = 1000,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Pure CSS Character Art visual effect.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme ===
    if color_scheme == "dark":
        bg_color = "#111827"
        text_color = "#f3f4f6"
        sky_color = "#1e3a8a"
        ground_color = "#064e3b"
        skin_color = "#fef3c7"
    else:
        bg_color = "#f9fafb"
        text_color = "#1f2937"
        sky_color = "#7dd3fc"
        ground_color = "#34d399"
        skin_color = "#fef3c7"

    line_color = "#111827" # The thick comic outline color

    # === CSS ===
    css = f"""/* Pure CSS Character Art Mascot */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --text: {text_color};
    --accent: {accent_color};
    --sky: {sky_color};
    --ground: {ground_color};
    --skin: {skin_color};
    --line: {line_color};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Inter', system-ui, sans-serif;
    background: var(--bg);
    color: var(--text);
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    overflow: hidden;
}}

.header {{
    text-align: center;
    margin-bottom: 2rem;
    z-index: 10;
}}

.header h1 {{
    font-size: 2.5rem;
    font-weight: 800;
    margin-bottom: 0.5rem;
    letter-spacing: -0.02em;
}}

.header p {{
    font-size: 1.1rem;
    opacity: 0.8;
}}

/* -- CSS ART SCENE -- */
.scene-container {{
    width: min(var(--width), 90vw);
    height: 500px;
    display: flex;
    align-items: center;
    justify-content: center;
    position: relative;
}}

.polaroid {{
    width: 320px;
    height: 420px;
    background: linear-gradient(to bottom, var(--sky) 0%, var(--sky) 75%, var(--ground) 75%, var(--ground) 100%);
    border: 6px solid var(--line);
    border-radius: 16px;
    position: relative;
    box-shadow: 12px 12px 0 rgba(0,0,0,0.1);
    overflow: hidden;
}}

/* -- CHARACTER STYLING -- */
.character {{
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    animation: breathe 3s ease-in-out infinite;
}}

.shadow {{
    position: absolute;
    bottom: 80px;
    left: 50%;
    transform: translateX(-50%);
    width: 120px;
    height: 20px;
    background: rgba(0, 0, 0, 0.3);
    border-radius: 50%;
    animation: shadowScale 3s ease-in-out infinite;
}}

.leg {{
    position: absolute;
    bottom: 85px;
    width: 14px;
    height: 60px;
    background: var(--skin);
    border: 4px solid var(--line);
    z-index: 1;
}}
.leg.left {{ left: 120px; border-radius: 0 0 4px 4px; }}
.leg.right {{ right: 120px; border-radius: 0 0 4px 4px; }}

.arm {{
    position: absolute;
    top: 220px;
    width: 12px;
    height: 70px;
    background: var(--skin);
    border: 4px solid var(--line);
    z-index: 1;
    border-radius: 0 0 12px 12px;
}}
.arm.left {{
    left: 80px;
    transform-origin: top center;
    transform: rotate(20deg);
}}
.arm.right {{
    right: 80px;
    transform-origin: top center;
    transform: rotate(-130deg);
}}

/* Hand/Bird Placeholder */
.bird {{
    position: absolute;
    top: 150px;
    right: 40px;
    width: 32px;
    height: 32px;
    background: #fcd34d;
    border: 4px solid var(--line);
    border-radius: 50% 50% 50% 20%;
    z-index: 5;
    animation: bounce 2s ease-in-out infinite;
}}
.bird::after {{
    content: '';
    position: absolute;
    top: 8px;
    right: 6px;
    width: 6px;
    height: 6px;
    background: var(--line);
    border-radius: 50%;
}}

.body {{
    position: absolute;
    top: 180px;
    left: 50%;
    transform: translateX(-50%);
    width: 130px;
    height: 120px;
    background: var(--skin);
    border: 5px solid var(--line);
    border-radius: 45% 45% 40% 40% / 60% 60% 40% 40%;
    z-index: 2;
}}

.eye {{
    position: absolute;
    top: 30px;
    width: 30px;
    height: 36px;
    background: var(--line);
    border-radius: 50%;
}}
.eye.left {{ left: 20px; }}
.eye.right {{ right: 20px; }}

.eye::after {{
    content: '';
    position: absolute;
    top: 6px;
    left: 14px;
    width: 10px;
    height: 10px;
    background: white;
    border-radius: 50%;
}}

.mouth {{
    position: absolute;
    top: 65px;
    left: 50%;
    transform: translateX(-50%);
    width: 18px;
    height: 10px;
    border-bottom: 4px solid var(--line);
    border-radius: 0 0 20px 20px;
}}

.hat {{
    position: absolute;
    top: 80px;
    left: 50%;
    transform: translateX(-50%);
    width: 260px;
    height: 130px;
    background-color: var(--accent);
    /* Multiple radial gradients to create spots! */
    background-image: 
        radial-gradient(circle at 20% 40%, white 18px, transparent 19px),
        radial-gradient(circle at 50% 20%, white 25px, transparent 26px),
        radial-gradient(circle at 80% 50%, white 20px, transparent 21px),
        radial-gradient(circle at 35% 80%, white 12px, transparent 13px),
        radial-gradient(circle at 65% 75%, white 14px, transparent 15px);
    border: 6px solid var(--line);
    border-radius: 50% 50% 20% 20% / 70% 70% 25% 25%;
    z-index: 3;
    box-shadow: inset -10px -10px 0 rgba(0,0,0,0.15);
}}

/* -- ANIMATIONS -- */
@keyframes breathe {{
    0%, 100% {{ transform: translateY(0); }}
    50% {{ transform: translateY(-8px); }}
}}

@keyframes shadowScale {{
    0%, 100% {{ transform: translateX(-50%) scale(1); opacity: 0.3; }}
    50% {{ transform: translateX(-50%) scale(0.85); opacity: 0.15; }}
}}

@keyframes bounce {{
    0%, 100% {{ transform: translateY(0); }}
    50% {{ transform: translateY(-4px); }}
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
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="header">
        <h1>{title_text}</h1>
        <p>{body_text}</p>
    </div>

    <div class="scene-container">
        <div class="polaroid" aria-label="A pure CSS illustration of a cute mushroom mascot character standing outside">
            
            <div class="shadow"></div>
            
            <!-- Character grouping for animation -->
            <div class="character">
                <div class="leg left"></div>
                <div class="leg right"></div>
                
                <div class="arm left"></div>
                <div class="arm right"></div>
                
                <div class="hat"></div>
                
                <div class="body">
                    <div class="eye left"></div>
                    <div class="eye right"></div>
                    <div class="mouth"></div>
                </div>

                <div class="bird"></div>
            </div>
            
        </div>
    </div>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Pure CSS Mascot — Interactive Behavior
document.addEventListener('DOMContentLoaded', () => {{
    const character = document.querySelector('.character');
    const bird = document.querySelector('.bird');

    // Add a simple interactive tilt effect on mouse movement over the polaroid
    const polaroid = document.querySelector('.polaroid');
    
    polaroid.addEventListener('mousemove', (e) => {{
        const rect = polaroid.getBoundingClientRect();
        const x = e.clientX - rect.left - rect.width / 2;
        const y = e.clientY - rect.top - rect.height / 2;
        
        // Slight parallax effect to give the CSS art depth
        requestAnimationFrame(() => {{
            character.style.transform = `translate(${{x * 0.05}}px, ${{y * 0.05}}px)`;
            bird.style.transform = `translate(${{x * 0.1}}px, ${{y * 0.1}}px) rotate(${{x * 0.1}}deg)`;
        }});
    }});

    polaroid.addEventListener('mouseleave', () => {{
        requestAnimationFrame(() => {{
            character.style.transform = `translate(0px, 0px)`;
            bird.style.transform = `translate(0px, 0px) rotate(0deg)`;
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
