def create_component(
    output_dir: str,
    title_text: str = "Initializing Core Components...",
    body_text: str = "Simulating decentralized GPU rendering.",
    color_scheme: str = "light",       # "dark" or "light"
    accent_color: str = "#e5244a",     # Red accent from the tutorial
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the SVG Path Line Drawing animation.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors ===
    if color_scheme == "dark":
        bg_color = "#121212"
        text_color = "#ffffff"
        secondary_stroke = "#888888"
    else:
        bg_color = "#ffffff"
        text_color = "#1a1a1a"
        secondary_stroke = "#242b35" # Dark grey from tutorial

    # === CSS ===
    css = f"""/* SVG Path Line Drawing - Generated Component */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg-color: {bg_color};
    --text-color: {text_color};
    --accent-color: {accent_color};
    --secondary-stroke: {secondary_stroke};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background-color: var(--bg-color);
    color: var(--text-color);
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    overflow: hidden;
}}

.container {{
    width: var(--width);
    max-width: 100%;
    height: var(--height);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
}}

/* Typography */
h1 {{
    font-size: 1.5rem;
    font-weight: 600;
    margin-top: 2rem;
    margin-bottom: 0.5rem;
    opacity: 0;
    animation: fadeIn 1s ease forwards 2s;
}}

p {{
    font-size: 1rem;
    color: var(--secondary-stroke);
    opacity: 0;
    animation: fadeIn 1s ease forwards 2.5s;
}}

/* SVG Styling */
.svg-container {{
    width: 250px;
    height: 250px;
    position: relative;
}}

.svg-icon {{
    width: 100%;
    height: 100%;
    overflow: visible;
}}

/* Base path styling - initial state hidden */
.draw-path {{
    fill: none;
    stroke-linecap: round;
    stroke-linejoin: round;
    /* We use variables set by JS for the array/offset */
    stroke-dasharray: var(--path-length, 0);
    stroke-dashoffset: var(--path-length, 0);
}}

.stroke-accent {{
    stroke: var(--accent-color);
    stroke-width: 4px;
}}

.stroke-secondary {{
    stroke: var(--secondary-stroke);
    stroke-width: 6px;
}}

/* Animation trigger class added by JS */
.animate-draw {{
    /* Using the cubic-bezier from the tutorial for organic motion */
    animation: drawLine var(--duration, 2.3s) cubic-bezier(0.66, 0, 0.34, 1) forwards;
    /* Optional delay staggered via JS */
    animation-delay: var(--delay, 0s); 
}}

@keyframes drawLine {{
    to {{
        stroke-dashoffset: 0;
    }}
}}

@keyframes fadeIn {{
    to {{
        opacity: 1;
    }}
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
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        <div class="svg-container">
            <!-- Custom Microcontroller SVG resembling the tutorial graphic -->
            <svg class="svg-icon" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
                <!-- Outer Brackets (Secondary Color) -->
                <g class="stroke-secondary">
                    <path class="draw-path" d="M 25 10 L 10 10 L 10 25" />
                    <path class="draw-path" d="M 75 10 L 90 10 L 90 25" />
                    <path class="draw-path" d="M 25 90 L 10 90 L 10 75" />
                    <path class="draw-path" d="M 75 90 L 90 90 L 90 75" />
                </g>
                
                <!-- Inner Chip / Microcontroller (Accent Color) -->
                <g class="stroke-accent">
                    <!-- Chip Body -->
                    <rect class="draw-path" x="30" y="30" width="40" height="40" rx="4" />
                    
                    <!-- Chip Identifier dot -->
                    <circle class="draw-path" cx="40" cy="60" r="2" />

                    <!-- Top Pins -->
                    <line class="draw-path" x1="40" y1="20" x2="40" y2="30" />
                    <line class="draw-path" x1="50" y1="20" x2="50" y2="30" />
                    <line class="draw-path" x1="60" y1="20" x2="60" y2="30" />
                    
                    <!-- Bottom Pins -->
                    <line class="draw-path" x1="40" y1="80" x2="40" y2="70" />
                    <line class="draw-path" x1="50" y1="80" x2="50" y2="70" />
                    <line class="draw-path" x1="60" y1="80" x2="60" y2="70" />
                    
                    <!-- Left Pins -->
                    <line class="draw-path" x1="20" y1="40" x2="30" y2="40" />
                    <line class="draw-path" x1="20" y1="50" x2="30" y2="50" />
                    <line class="draw-path" x1="20" y1="60" x2="30" y2="60" />
                    
                    <!-- Right Pins -->
                    <line class="draw-path" x1="80" y1="40" x2="70" y2="40" />
                    <line class="draw-path" x1="80" y1="50" x2="70" y2="50" />
                    <line class="draw-path" x1="80" y1="60" x2="70" y2="60" />
                </g>
            </svg>
        </div>
        
        <h1>{title_text}</h1>
        <p>{body_text}</p>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = """// SVG Path Line Drawing - Animation Logic
document.addEventListener('DOMContentLoaded', () => {
    // Select all paths/lines/shapes that should be animated
    const drawPaths = document.querySelectorAll('.draw-path');
    
    // Iterate over each path to calculate its exact length dynamically
    drawPaths.forEach((path, index) => {
        // 1. Get the total length of the specific path (works for lines, rects, circles too)
        const length = path.getTotalLength();
        
        // 2. Set the exact length as a CSS Custom Property on the element
        path.style.setProperty('--path-length', length);
        
        // 3. Stagger the animations slightly based on the element type or index
        // Inner chip components (accent) start slightly after the outer brackets
        let delay = 0;
        let duration = '2.3s'; // Base duration from tutorial
        
        if (path.closest('.stroke-accent')) {
            delay = 0.3; // Slight delay for the inner chip
            duration = '2.0s'; // Draw slightly faster
        }
        
        // Optional: add tiny stagger to each pin for a sequenced effect
        if (path.tagName.toLowerCase() === 'line') {
            delay += (index * 0.05); 
        }
        
        path.style.setProperty('--delay', `${delay}s`);
        path.style.setProperty('--duration', duration);
        
        // 4. Force a browser reflow so the CSS variables are registered before animating
        path.getBoundingClientRect();
        
        // 5. Add the class that triggers the CSS @keyframes animation
        path.classList.add('animate-draw');
    });
});
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
