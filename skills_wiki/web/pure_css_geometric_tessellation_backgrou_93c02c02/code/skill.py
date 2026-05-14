def create_component(
    output_dir: str,
    title_text: str = "CSS Tessellation Patterns",
    body_text: str = "Select a pattern below. These intricate backgrounds are generated entirely using mathematically offset CSS gradients—no images or SVGs required.",
    color_scheme: str = "dark",        
    accent_color: str = "#00bfff",     
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Pure CSS Tessellation Patterns.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os
    import html

    os.makedirs(output_dir, exist_ok=True)
    
    # Escape user text
    safe_title = html.escape(title_text)
    safe_body = html.escape(body_text)

    # Base theme variables
    if color_scheme == "dark":
        bg_color = "#0a0d14"
        text_color = "#ffffff"
        surface_color = "rgba(10, 13, 20, 0.7)"
        card_border = "rgba(255, 255, 255, 0.1)"
    else:
        bg_color = "#f4f6f8"
        text_color = "#111827"
        surface_color = "rgba(255, 255, 255, 0.7)"
        card_border = "rgba(0, 0, 0, 0.1)"

    # === CSS ===
    css = f"""/* Pure CSS Geometric Tessellation Backgrounds */
:root {{
    --bg-color: {bg_color};
    --text-color: {text_color};
    --accent-color: {accent_color};
    --surface-color: {surface_color};
    --card-border: {card_border};
    --width: {width_px}px;
    --height: {height_px}px;
    
    /* Pattern Configuration */
    --pattern-bg: var(--bg-color);
    --pattern-fg: var(--accent-color);
    --pattern-size: 4rem;
    --pattern-half: calc(var(--pattern-size) / 2);
}}

*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background-color: var(--bg-color);
    color: var(--text-color);
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 100vh;
}}

.pattern-container {{
    width: var(--width);
    height: var(--height);
    max-width: 100vw;
    max-height: 100vh;
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
    transition: background 0.5s ease;
    
    /* Animation for infinite sliding */
    animation: slidePattern 20s linear infinite;
}}

@keyframes slidePattern {{
    from {{ background-position: 0 0, var(--pos-x2, 0) var(--pos-y2, 0), var(--pos-x3, 0) var(--pos-y3, 0), var(--pos-x4, 0) var(--pos-y4, 0); }}
    to {{ background-position: var(--pattern-size) var(--pattern-size), calc(var(--pos-x2, 0) + var(--pattern-size)) calc(var(--pos-y2, 0) + var(--pattern-size)), calc(var(--pos-x3, 0) + var(--pattern-size)) calc(var(--pos-y3, 0) + var(--pattern-size)), calc(var(--pos-x4, 0) + var(--pattern-size)) calc(var(--pos-y4, 0) + var(--pattern-size)); }}
}}

/* =========================================
   PATTERN 1: ZIG-ZAG
   Uses rotated linear-gradients cut in half
========================================== */
.pattern-zigzag {{
    background-color: var(--pattern-bg);
    background-image: 
        linear-gradient(135deg, var(--pattern-fg) 25%, transparent 25%),
        linear-gradient(225deg, var(--pattern-fg) 25%, transparent 25%),
        linear-gradient(315deg, var(--pattern-fg) 25%, transparent 25%),
        linear-gradient(45deg, var(--pattern-fg) 25%, transparent 25%);
    background-size: var(--pattern-size) var(--pattern-size);
    
    /* Offsets to interlock the triangles into zigzags */
    --pos-x2: 0; --pos-y2: 0;
    --pos-x3: var(--pattern-half); --pos-y3: var(--pattern-half);
    --pos-x4: var(--pattern-half); --pos-y4: var(--pattern-half);
    
    background-position: 
        0 0, 
        var(--pos-x2) var(--pos-y2), 
        var(--pos-x3) var(--pos-y3), 
        var(--pos-x4) var(--pos-y4);
}}

/* =========================================
   PATTERN 2: THE PLUS SIGN
   Overlapping circles with transparent holes
========================================== */
.pattern-plus {{
    /* Base color is the accent, holes reveal the background color */
    background-color: var(--pattern-fg);
    /* Pattern size needs to be a bit larger for breathing room */
    --pattern-size: 5rem;
    --hole-size: 1rem;
    
    background-image: 
        radial-gradient(circle, transparent var(--hole-size), var(--pattern-bg) var(--hole-size)),
        radial-gradient(circle, transparent var(--hole-size), var(--pattern-bg) var(--hole-size));
    background-size: var(--pattern-size) var(--pattern-size);
    
    /* Offset second layer by exactly half */
    --pos-x2: var(--pattern-half); --pos-y2: var(--pattern-half);
    
    background-position: 
        0 0, 
        var(--pos-x2) var(--pos-y2);
}}

/* =========================================
   PATTERN 3: CONIC TRIANGLES
   Spinning gradients offset to interlock
========================================== */
.pattern-conic {{
    background-color: var(--pattern-bg);
    background-image: 
        conic-gradient(from 150deg at 50% 30%, var(--pattern-fg) 60deg, transparent 60deg),
        conic-gradient(from 330deg at 50% 70%, var(--pattern-fg) 60deg, transparent 60deg);
    background-size: var(--pattern-size) var(--pattern-size);
    
    /* Offset second layer to fit into the gaps */
    --pos-x2: var(--pattern-half); --pos-y2: calc(var(--pattern-size) * -0.25);
    
    background-position: 
        0 0, 
        var(--pos-x2) var(--pos-y2);
}}


/* UI Layout */
.content-card {{
    background: var(--surface-color);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    padding: 3rem;
    border-radius: 1.5rem;
    border: 1px solid var(--card-border);
    max-width: 600px;
    text-align: center;
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
    z-index: 10;
}}

.title {{
    font-size: 2.5rem;
    font-weight: 700;
    margin-bottom: 1rem;
    letter-spacing: -0.025em;
}}

.body-text {{
    font-size: 1.125rem;
    line-height: 1.6;
    margin-bottom: 2.5rem;
    opacity: 0.9;
}}

.controls {{
    display: flex;
    gap: 1rem;
    justify-content: center;
    flex-wrap: wrap;
}}

.btn {{
    background: transparent;
    color: var(--text-color);
    border: 2px solid var(--accent-color);
    padding: 0.75rem 1.5rem;
    border-radius: 0.5rem;
    font-size: 1rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s ease;
}}

.btn:hover, .btn.active {{
    background: var(--accent-color);
    color: {bg_color}; /* Ensure contrast against accent */
}}
"""

    # === HTML ===
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{safe_title}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="pattern-container pattern-plus" id="bg-container">
        <div class="content-card">
            <h1 class="title">{safe_title}</h1>
            <p class="body-text">{safe_body}</p>
            
            <div class="controls">
                <button class="btn" data-pattern="pattern-zigzag">Zig-Zag</button>
                <button class="btn active" data-pattern="pattern-plus">Plus Signs</button>
                <button class="btn" data-pattern="pattern-conic">Conic Triangles</button>
            </div>
        </div>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = """// Pure CSS Geometric Pattern Switcher
document.addEventListener('DOMContentLoaded', () => {
    const container = document.getElementById('bg-container');
    const buttons = document.querySelectorAll('.btn');

    buttons.forEach(btn => {
        btn.addEventListener('click', (e) => {
            // Remove active class from all buttons
            buttons.forEach(b => b.classList.remove('active'));
            // Add active class to clicked button
            e.target.classList.add('active');

            // Get target pattern class
            const patternClass = e.target.getAttribute('data-pattern');

            // Remove existing pattern classes
            container.classList.remove('pattern-zigzag', 'pattern-plus', 'pattern-conic');
            
            // Add new pattern class
            container.classList.add(patternClass);
        });
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
