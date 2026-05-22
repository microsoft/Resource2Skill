def create_component(
    output_dir: str,
    title_text: str = "Escher's Geometry",
    body_text: str = "A pure CSS 3D isometric pattern inspired by MC Escher.",
    color_scheme: str = "dark",
    accent_color: str = "#00bfff",
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the CSS 3D Isometric Escher Pattern.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Derive 3-tone lighting colors for the 3D cubes based on theme
    if color_scheme == "dark":
        bg_color = "#08080c"
        color_1 = "#e5e5e5"     # Top (Lit floor)
        color_2 = accent_color  # Front-Left (Midtone wall)
        color_3 = "#151515"     # Front-Right (Shadow wall)
    else:
        bg_color = "#f0f2f5"
        color_1 = "#ffffff"     # Top (Lit floor)
        color_2 = accent_color  # Front-Left (Midtone wall)
        color_3 = "#2a2a2a"     # Front-Right (Shadow wall)

    css = f"""/* CSS 3D Isometric Escher Pattern */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --color-1: {color_1};
    --color-2: {color_2};
    --color-3: {color_3};
    --width: {width_px}px;
    --height: {height_px}px;
    
    /* Base geometry size */
    --S: 60px; 
    --s: calc(var(--S) / 2);
}}

body {{
    font-family: 'Inter', system-ui, sans-serif;
    background: var(--bg);
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 100vh;
    overflow: hidden;
}}

.container {{
    width: var(--width);
    height: var(--height);
    position: relative;
    overflow: hidden;
    background: var(--bg);
    border-radius: 12px;
    box-shadow: 0 24px 48px rgba(0,0,0,0.2);
}}

.pattern-grid {{
    position: absolute;
    top: 0; 
    left: 0;
    width: 100%; 
    height: 100%;
    /* Infinite seamless scrolling animation */
    animation: isometricScroll 15s linear infinite;
}}

@media (prefers-reduced-motion: reduce) {{
    .pattern-grid {{
        animation-play-state: paused;
    }}
}}

.cell {{
    position: absolute;
    transform: translate(-50%, -50%);
    transition: z-index 0s;
}}

/* Dynamic z-index sorting on hover to prevent clipping */
.cell:has(.side:hover) {{
    z-index: 100;
    transition-delay: 0s;
}}
.cell:not(:has(.side:hover)) {{
    transition-delay: 0.4s;
}}

.cube {{
    position: relative;
    transform-style: preserve-3d;
    /* True Isometric Projection */
    transform: rotateX(-35.264deg) rotateY(45deg);
    transition: transform 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    pointer-events: none;
}}

/* Pop out effect when hovered */
.cube:has(.side:hover) {{
    transform: rotateX(-35.264deg) rotateY(45deg) translateZ(25px);
}}

.side {{
    position: absolute;
    transform-origin: center;
    pointer-events: auto;
    cursor: pointer;
    transition: filter 0.3s ease;
}}

.side:hover {{
    filter: brightness(1.25);
}}

.large {{
    width: var(--S);
    height: var(--S);
    margin-left: calc(var(--S) * -0.5);
    margin-top: calc(var(--S) * -0.5);
}}

.small {{
    width: var(--s);
    height: var(--s);
    margin-left: calc(var(--s) * -0.5);
    margin-top: calc(var(--s) * -0.5);
}}

/* --- Large Concave Corner (Pushed BACK into the screen) --- */
/* scale(1.01) subtly prevents 1px transparency gaps from anti-aliasing */
.large.face-top {{ 
    transform: rotateX(90deg) translateZ(calc(var(--S) * -0.5)) scale(1.01); 
    background: var(--color-1); 
}}
.large.face-right {{ 
    transform: rotateY(0deg) translateZ(calc(var(--S) * -0.5)) scale(1.01); 
    background: var(--color-2); 
}}
.large.face-left {{ 
    transform: rotateY(-90deg) translateZ(calc(var(--S) * -0.5)) scale(1.01); 
    background: var(--color-3); 
}}

/* --- Small Convex Cube (Pushed OUT from the screen) --- */
.small.face-top {{ 
    transform: rotateX(90deg) translateZ(calc(var(--s) * 0.5)) scale(1.01); 
    background: var(--color-1); 
}}
.small.face-right {{ 
    transform: rotateY(0deg) translateZ(calc(var(--s) * 0.5)) scale(1.01); 
    background: var(--color-2); 
}}
.small.face-left {{ 
    transform: rotateY(-90deg) translateZ(calc(var(--s) * 0.5)) scale(1.01); 
    background: var(--color-3); 
}}

@keyframes isometricScroll {{
    from {{ transform: translate(0, 0); }}
    to {{ transform: translate(var(--scroll-x), var(--scroll-y)); }}
}}

/* --- Overlay Content --- */
.overlay {{
    position: absolute;
    inset: 0;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    pointer-events: none; /* Let clicks pass through to the pattern */
    background: radial-gradient(circle at center, rgba(0,0,0,0) 20%, var(--bg) 110%);
}}

.title {{
    color: var(--color-1);
    font-size: 3.5rem;
    font-weight: 800;
    letter-spacing: -0.03em;
    text-shadow: 0 8px 24px rgba(0,0,0,0.6);
    margin-bottom: 1rem;
    text-align: center;
}}

.body-text {{
    color: var(--color-1);
    font-size: 1.125rem;
    font-weight: 400;
    max-width: 500px;
    text-align: center;
    text-shadow: 0 4px 12px rgba(0,0,0,0.6);
    line-height: 1.6;
    opacity: 0.9;
}}
"""

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
    <div class="container">
        <!-- 3D Grid Injected via JS -->
        <div class="pattern-grid" id="grid"></div>
        
        <div class="overlay">
            <h1 class="title">{title_text}</h1>
            <p class="body-text">{body_text}</p>
        </div>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    js = f"""// Core isometric pattern math and generation
document.addEventListener('DOMContentLoaded', () => {{
    const grid = document.getElementById('grid');
    const container = document.querySelector('.container');
    
    // S must match CSS --S variable
    const S = 60; 
    
    // Calculate perfect interlocking steps for a rotated hexagon projection
    const colStep = S * Math.sqrt(2);
    const rowStep = S * Math.sqrt(1.5);

    // Calculate shifting distance for a seamless CSS loop
    // Moving 1 column horizontally and 2 rows vertically brings the pattern to an identical repeating state
    const scrollX = colStep;
    const scrollY = 2 * rowStep;
    document.documentElement.style.setProperty('--scroll-x', `-${{scrollX}}px`);
    document.documentElement.style.setProperty('--scroll-y', `-${{scrollY}}px`);

    // Determine grid bounds (add padding to allow for off-screen scrolling)
    const width = container.clientWidth;
    const height = container.clientHeight;
    
    const padCols = 4;
    const padRows = 4;
    const cols = Math.ceil(width / colStep) + padCols;
    const rows = Math.ceil(height / rowStep) + padRows;
    
    const startC = -2;
    const startR = -2;

    const fragment = document.createDocumentFragment();

    for (let r = startR; r < rows; r++) {{
        for (let c = startC; c < cols; c++) {{
            // Calculate 2D position
            let x = c * colStep;
            // Shift every odd row by half a column to interlock
            if (Math.abs(r) % 2 === 1) {{
                x += colStep / 2;
            }}
            let y = r * rowStep;

            const cell = document.createElement('div');
            cell.className = 'cell';
            cell.style.left = `${{x}}px`;
            cell.style.top = `${{y}}px`;

            // Every cell gets the large concave corner
            let html = `
                <div class="cube">
                    <!-- Large Concave -->
                    <div class="side large face-top"></div>
                    <div class="side large face-right"></div>
                    <div class="side large face-left"></div>
            `;

            // MC Escher pattern: Nest a small convex cube inside the corner ONLY on even rows
            if (Math.abs(r) % 2 === 0) {{
                html += `
                    <!-- Small Convex -->
                    <div class="side small face-top"></div>
                    <div class="side small face-right"></div>
                    <div class="side small face-left"></div>
                `;
            }}

            html += `</div>`;
            cell.innerHTML = html;
            fragment.appendChild(cell);
        }}
    }}

    grid.appendChild(fragment);
}});
"""

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
