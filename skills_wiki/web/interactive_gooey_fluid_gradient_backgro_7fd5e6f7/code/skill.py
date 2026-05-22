def create_component(
    output_dir: str,
    title_text: str = "Fluid Motion",
    body_text: str = "Hover and move your mouse to interact with the background.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#00bfff",     # CSS hex color for interactive bubble
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Interactive Gooey Fluid Gradient Background.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Helper to convert hex to comma-separated RGB for CSS variables
    def hex_to_rgb_str(hex_code):
        hex_code = hex_code.lstrip('#')
        if len(hex_code) == 3:
            hex_code = ''.join(c+c for c in hex_code)
        return f"{int(hex_code[0:2], 16)}, {int(hex_code[2:4], 16)}, {int(hex_code[4:6], 16)}"

    interactive_rgb = hex_to_rgb_str(accent_color)

    if color_scheme == "dark":
        text_color = "#ffffff"
        bg_linear_start = "18, 0, 42"        # Deep purple
        bg_linear_end = "0, 10, 46"          # Deep blue
        # Vibrant neon colors for hard-light blend mode
        color1 = "18, 113, 255"              # Blue
        color2 = "221, 74, 255"              # Magenta
        color3 = "100, 220, 255"             # Cyan
        color4 = "200, 50, 50"               # Red
        blend_mode = "hard-light"
    else:
        text_color = "#1a1a2e"
        bg_linear_start = "240, 244, 255"    # Soft blue-white
        bg_linear_end = "255, 240, 245"      # Soft pink-white
        # Pastel but saturated colors for multiply blend mode in light theme
        color1 = "100, 150, 255"             # Soft Blue
        color2 = "255, 120, 200"             # Soft Pink
        color3 = "120, 230, 210"             # Soft Teal
        color4 = "255, 180, 100"             # Soft Orange
        blend_mode = "multiply"

    # === CSS ===
    css = f"""/* Gooey Interactive Gradient Background */
:root {{
    --bg-start: {bg_linear_start};
    --bg-end: {bg_linear_end};
    --color1: {color1};
    --color2: {color2};
    --color3: {color3};
    --color4: {color4};
    --color-interactive: {interactive_rgb};
    --circle-size: 80%;
    --blending: {blend_mode};
    --width: {width_px}px;
    --height: {height_px}px;
}}

* {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background-color: rgb(var(--bg-start));
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 100vh;
}}

/* Main Component Wrapper */
.component-wrapper {{
    width: var(--width);
    height: var(--height);
    position: relative;
    overflow: hidden;
    border-radius: 16px;
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
    background: linear-gradient(40deg, rgb(var(--bg-start)), rgb(var(--bg-end)));
}}

/* Text Content Overlay */
.content {{
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    z-index: 10;
    color: {text_color};
    pointer-events: none; /* Let mouse pass through to background */
    padding: 2rem;
}}

.content h1 {{
    font-size: 4rem;
    font-weight: 700;
    letter-spacing: -0.02em;
    margin-bottom: 1rem;
    text-shadow: 0 4px 24px rgba(0,0,0,0.1);
}}

.content p {{
    font-size: 1.25rem;
    font-weight: 300;
    max-width: 600px;
    opacity: 0.9;
}}

/* The Magic Goo Filter Container */
.gradients-container {{
    width: 100%;
    height: 100%;
    filter: url(#goo) blur(40px);
    position: absolute;
    top: 0;
    left: 0;
    z-index: 0;
}}

.g1, .g2, .g3, .g4, .interactive {{
    position: absolute;
    mix-blend-mode: var(--blending);
    width: var(--circle-size);
    height: var(--circle-size);
    top: calc(50% - var(--circle-size) / 2);
    left: calc(50% - var(--circle-size) / 2);
    opacity: 1;
}}

.g1 {{
    background: radial-gradient(circle at center, rgba(var(--color1), 0.8) 0, rgba(var(--color1), 0) 50%) no-repeat;
    transform-origin: center center;
    animation: moveVertical 30s ease infinite;
}}

.g2 {{
    background: radial-gradient(circle at center, rgba(var(--color2), 0.8) 0, rgba(var(--color2), 0) 50%) no-repeat;
    transform-origin: calc(50% - 400px);
    animation: moveInCircle 20s reverse infinite;
}}

.g3 {{
    background: radial-gradient(circle at center, rgba(var(--color3), 0.8) 0, rgba(var(--color3), 0) 50%) no-repeat;
    top: calc(50% - var(--circle-size) / 2 + 200px);
    left: calc(50% - var(--circle-size) / 2 - 500px);
    transform-origin: calc(50% + 400px);
    animation: moveInCircle 40s linear infinite;
}}

.g4 {{
    background: radial-gradient(circle at center, rgba(var(--color4), 0.8) 0, rgba(var(--color4), 0) 50%) no-repeat;
    transform-origin: calc(50% - 200px);
    animation: moveHorizontal 40s ease infinite;
    opacity: 0.7;
}}

.interactive {{
    background: radial-gradient(circle at center, rgba(var(--color-interactive), 0.8) 0, rgba(var(--color-interactive), 0) 50%) no-repeat;
    width: 100%;
    height: 100%;
    top: -50%;
    left: -50%;
    opacity: 0.7;
}}

/* Autonomous Animations */
@keyframes moveInCircle {{
    0% {{ transform: rotate(0deg); }}
    50% {{ transform: rotate(180deg); }}
    100% {{ transform: rotate(360deg); }}
}}

@keyframes moveVertical {{
    0% {{ transform: translateY(-50%); }}
    50% {{ transform: translateY(50%); }}
    100% {{ transform: translateY(-50%); }}
}}

@keyframes moveHorizontal {{
    0% {{ transform: translateX(-50%) translateY(-10%); }}
    50% {{ transform: translateX(50%) translateY(10%); }}
    100% {{ transform: translateX(-50%) translateY(-10%); }}
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
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    
    <!-- Component Starts Here -->
    <div class="component-wrapper">
        
        <!-- SVG Goo Filter Definition -->
        <svg xmlns="http://www.w3.org/2000/svg" style="display: none;">
            <defs>
                <filter id="goo">
                    <feGaussianBlur in="SourceGraphic" stdDeviation="10" result="blur" />
                    <!-- Alpha thresholding matrix: creates the fluid surface tension -->
                    <feColorMatrix in="blur" mode="matrix" values="1 0 0 0 0  0 1 0 0 0  0 0 1 0 0  0 0 0 18 -8" result="goo" />
                    <feBlend in="SourceGraphic" in2="goo" />
                </filter>
            </defs>
        </svg>

        <!-- Foreground Content -->
        <div class="content">
            <h1>{title_text}</h1>
            <p>{body_text}</p>
        </div>

        <!-- Animated Background Gradients -->
        <div class="gradients-container">
            <div class="g1"></div>
            <div class="g2"></div>
            <div class="g3"></div>
            <div class="g4"></div>
            <div class="interactive"></div>
        </div>

    </div>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Gooey Fluid Background - Interaction Logic
document.addEventListener('DOMContentLoaded', () => {{
    const container = document.querySelector('.component-wrapper');
    const interBubble = document.querySelector('.interactive');
    
    // Physics / Easing variables
    let curX = 0;
    let curY = 0;
    let tgX = 0;
    let tgY = 0;
    
    // Lerp factor (higher = smoother but slower, lower = faster but stiffer)
    const ease = 0.05;

    // Track mouse coordinates relative to the component container
    container.addEventListener('mousemove', (e) => {{
        const rect = container.getBoundingClientRect();
        // Calculate target X/Y so the bubble centers on the cursor
        tgX = e.clientX - rect.left;
        tgY = e.clientY - rect.top;
    }});

    // Animation Loop
    function move() {{
        // Linear interpolation (Lerp) for smooth following
        curX += (tgX - curX) * ease;
        curY += (tgY - curY) * ease;
        
        // Apply transformation
        // Using Math.round to prevent sub-pixel rendering blur/jank on some screens
        interBubble.style.transform = `translate(${{Math.round(curX)}}px, ${{Math.round(curY)}}px)`;
        
        requestAnimationFrame(move);
    }}
    
    // Start animation loop
    move();
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
