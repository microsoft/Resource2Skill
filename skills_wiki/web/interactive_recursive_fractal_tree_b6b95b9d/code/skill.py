def create_component(
    output_dir: str,
    title_text: str = "Recursive Growth",
    body_text: str = "Move your mouse across the area to shape the fractal.",
    color_scheme: str = "dark",        
    accent_color: str = "#ffffff",     
    width_px: int = 1000,
    height_px: int = 700,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Interactive Recursive Fractal Tree visual effect.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors ===
    if color_scheme == "dark":
        bg_color = "#111111"
        text_color = "#f0f0f0"
        shadow_color = "rgba(0, 0, 0, 0.5)"
    else:
        bg_color = "#f4f4f5"
        text_color = "#18181b"
        shadow_color = "rgba(0, 0, 0, 0.1)"
        
    # If accent is white on a light theme, fallback to a dark color for visibility
    if color_scheme == "light" and accent_color.lower() in ["#ffffff", "#fff", "white"]:
        tree_color = "#18181b"
    else:
        tree_color = accent_color

    # === CSS ===
    css = f"""/* Interactive Recursive Fractal Tree */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --text: {text_color};
    --tree-color: {tree_color};
    --shadow: {shadow_color};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background: #000; /* Outer body background */
    color: var(--text);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
}}

.container {{
    width: var(--width);
    height: var(--height);
    max-width: 100vw;
    max-height: 100vh;
    position: relative;
    background: var(--bg);
    overflow: hidden;
    border-radius: 12px;
    box-shadow: 0 10px 40px var(--shadow);
}}

#fractal-canvas {{
    display: block;
    width: 100%;
    height: 100%;
    cursor: crosshair;
}}

.content-overlay {{
    position: absolute;
    top: 2rem;
    left: 2rem;
    pointer-events: none; /* Allows mouse events to pass through to canvas */
    z-index: 10;
    max-width: 400px;
    background: color-mix(in srgb, var(--bg) 60%, transparent);
    padding: 1.5rem;
    border-radius: 8px;
    backdrop-filter: blur(4px);
}}

.title {{
    font-size: 2rem;
    font-weight: 700;
    margin-bottom: 0.5rem;
    letter-spacing: -0.02em;
}}

.body-text {{
    font-size: 1rem;
    line-height: 1.5;
    opacity: 0.8;
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
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        <div class="content-overlay">
            <h1 class="title">{title_text}</h1>
            <p class="body-text">{body_text}</p>
        </div>
        <canvas id="fractal-canvas"></canvas>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Interactive Recursive Fractal Tree Logic
document.addEventListener('DOMContentLoaded', () => {{
    const container = document.querySelector('.container');
    const canvas = document.getElementById('fractal-canvas');
    const ctx = canvas.getContext('2d');

    let cw, ch;
    let mouseX, mouseY;

    // Initialize dimensions
    function resize() {{
        cw = canvas.width = container.clientWidth;
        ch = canvas.height = container.clientHeight;
        
        // Start mouse in the center by default
        if (mouseX === undefined) {{
            mouseX = cw / 2;
            mouseY = ch / 2;
        }}
    }}
    
    window.addEventListener('resize', resize);
    resize();

    // Track mouse position relative to the canvas
    container.addEventListener('mousemove', (e) => {{
        const rect = canvas.getBoundingClientRect();
        mouseX = e.clientX - rect.left;
        mouseY = e.clientY - rect.top;
    }});

    // Handle touch devices
    container.addEventListener('touchmove', (e) => {{
        const rect = canvas.getBoundingClientRect();
        mouseX = e.touches[0].clientX - rect.left;
        mouseY = e.touches[0].clientY - rect.top;
    }}, {{ passive: true }});

    // Get color from CSS variable
    const computedStyles = getComputedStyle(document.documentElement);
    const treeColor = computedStyles.getPropertyValue('--tree-color').trim();

    function drawTree() {{
        // Clear canvas for next frame
        ctx.clearRect(0, 0, cw, ch);

        const initialLen = ch / 3.5;  // Trunk length relative to container height
        const initialWidth = 10;      // Starting trunk thickness
        
        // Map mouseX to the branch spread angle (0 to 90 degrees)
        const angleVar = (mouseX / cw) * (Math.PI / 2);
        
        // Map mouseY to the branch length modifier.
        // Capped between 0.5 and 0.75 to prevent infinite recursion/performance crashes.
        const lenMod = 0.5 + (mouseY / ch) * 0.25;

        // Recursive drawing function
        function drawBranch(x, y, len, angle, branchWidth) {{
            ctx.beginPath();
            ctx.save();
            
            ctx.strokeStyle = treeColor;
            ctx.lineWidth = branchWidth;
            ctx.lineCap = 'round';
            
            // Shorter branches become slightly transparent
            ctx.globalAlpha = Math.max(0.15, len / initialLen);

            // Move context to the start of the branch and rotate
            ctx.translate(x, y);
            ctx.rotate(angle);

            // Draw the line segment upwards
            ctx.moveTo(0, 0);
            ctx.lineTo(0, -len);
            ctx.stroke();

            // Base case: Stop recursion if branch is too short
            if (len < 8) {{
                ctx.restore();
                return;
            }}

            // Recursive calls for left and right branches
            // Origin is now the end of the current branch (0, -len)
            drawBranch(0, -len, len * lenMod, -angleVar, branchWidth * 0.7);
            drawBranch(0, -len, len * lenMod, angleVar, branchWidth * 0.7);

            // Restore context to previous state for other branches
            ctx.restore();
        }}

        // Start drawing from bottom center, pointing straight up (0 angle)
        drawBranch(cw / 2, ch, initialLen, 0, initialWidth);

        // Loop animation
        requestAnimationFrame(drawTree);
    }}

    // Kick off animation loop
    drawTree();
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
