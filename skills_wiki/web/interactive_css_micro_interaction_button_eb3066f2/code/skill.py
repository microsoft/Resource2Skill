def create_component(
    output_dir: str,
    title_text: str = "Interactive CSS Buttons",
    body_text: str = "Hover over the buttons below to experience pure CSS micro-interactions.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#FFCE00",     # CSS hex color for first accent
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Interactive CSS Micro-Interaction Buttons.
    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors ===
    if color_scheme == "dark":
        bg_color = "#0f1423"
        text_color = "#f4f4f6"
    else:
        bg_color = "#ffffff"
        text_color = "#1a1a2e"

    # === CSS ===
    css = f"""/* Interactive CSS Micro-Interaction Buttons */
:root {{
    --bg: {bg_color};
    --text: {text_color};
    --btn1-color: {accent_color};
    --btn2-color: #FE4880; /* Vibrant Pink */
    --btn3-color: #68DEA0; /* Sea Green */
    --btn4-color: #4B90E2; /* Soft Blue */
    --width: {width_px}px;
    --height: {height_px}px;
}}

*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background: var(--bg);
    color: var(--text);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
}}

.container {{
    width: var(--width);
    height: var(--height);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 4rem;
}}

.text-content {{
    text-align: center;
}}

.title {{
    font-size: 2.5rem;
    font-weight: 700;
    margin-bottom: 1rem;
}}

.body-text {{
    font-size: 1.1rem;
    opacity: 0.8;
}}

.button-grid {{
    display: flex;
    flex-wrap: wrap;
    gap: 2.5rem;
    justify-content: center;
    max-width: 1000px;
}}

/* =========================================
   BASE BUTTON STYLES
   ========================================= */
.btn {{
    position: relative;
    font-family: inherit;
    font-size: 1.25rem;
    font-weight: 600;
    padding: 1.1rem 2.2rem;
    border-radius: 8px;
    cursor: pointer;
    background: transparent;
    outline: none;
    border: none;
    transition: all 0.4s cubic-bezier(0.25, 1, 0.5, 1);
    z-index: 1;
    display: flex;
    align-items: center;
    justify-content: center;
}}

.btn:focus-visible {{
    outline: 2px dashed var(--text);
    outline-offset: 6px;
}}

/* =========================================
   BUTTON 1: Solid Highlight Fill
   ========================================= */
.btn-1 {{
    color: var(--btn1-color);
    border: 3px solid var(--btn1-color);
}}

.btn-1:hover {{
    background-color: var(--btn1-color);
    color: #111111; /* Enforce high contrast text */
}}

/* =========================================
   BUTTON 2: Slide from Right
   ========================================= */
.btn-2 {{
    color: var(--btn2-color);
    border: 3px solid var(--btn2-color);
    background-image: linear-gradient(to right, transparent 50%, var(--btn2-color) 50%);
    background-size: 200% 100%;
    background-position: 0% 0%; /* Aligns transparent left half */
}}

.btn-2:hover {{
    color: #ffffff;
    background-position: 100% 0%; /* Slides solid right half into view */
}}

/* =========================================
   BUTTON 3: Slide from Bottom
   ========================================= */
.btn-3 {{
    color: var(--btn3-color);
    border: 3px solid var(--btn3-color);
    background-image: linear-gradient(to bottom, transparent 50%, var(--btn3-color) 50%);
    background-size: 100% 200%;
    background-position: 0% 0%; /* Aligns transparent top half */
}}

.btn-3:hover {{
    color: #111111;
    background-position: 0% 100%; /* Slides solid bottom half up into view */
}}

/* =========================================
   BUTTON 4: 3D Physical Press
   ========================================= */
.btn-4 {{
    color: #ffffff;
    background-color: var(--btn4-color);
    box-shadow: inset 0 -8px 0 0 rgba(0, 0, 0, 0.2);
    text-shadow: 0 3px 0 rgba(0, 0, 0, 0.2);
    transition: all 0.1s ease; /* Faster transition for physical feel */
}}

.btn-4:hover {{
    box-shadow: inset 0 -5px 0 0 rgba(0, 0, 0, 0.2);
    transform: translateY(3px); /* Shifts down slightly as rim shrinks */
}}

.btn-4:active {{
    box-shadow: inset 0 -1px 0 0 rgba(0, 0, 0, 0.2);
    text-shadow: 0 1px 0 rgba(0, 0, 0, 0.2);
    transform: translateY(7px); /* Full compression */
}}

/* =========================================
   BUTTON 5: Expanding Cross-hatch Outline
   ========================================= */
.btn-5 {{
    color: var(--text);
    border: 3px solid transparent; /* Maintains layout metrics to match others */
}}

.btn-5::before,
.btn-5::after {{
    content: '';
    position: absolute;
    width: 0;
    height: 0;
    opacity: 0;
    border-radius: 8px; /* Matches parent */
    pointer-events: none; /* Prevents catching hovers meant for nearby elements */
}}

.btn-5::before {{
    top: -3px; /* Offset overlaps the transparent border perfectly */
    left: -3px;
    border-top: 3px solid var(--text);
    border-left: 3px solid var(--text);
    /* Delays opacity fade out until scale down is complete */
    transition: all 0.4s cubic-bezier(0.25, 1, 0.5, 1), opacity 0.1s ease 0.4s;
}}

.btn-5::after {{
    bottom: -3px;
    right: -3px;
    border-bottom: 3px solid var(--text);
    border-right: 3px solid var(--text);
    transition: all 0.4s cubic-bezier(0.25, 1, 0.5, 1), opacity 0.1s ease 0.4s;
}}

.btn-5:hover::before,
.btn-5:hover::after {{
    /* Expands larger than the button to create the cross-hatch overshoot */
    width: calc(100% + 15px);
    height: calc(100% + 15px);
    opacity: 1;
    transition: all 0.4s cubic-bezier(0.25, 1, 0.5, 1), opacity 0.1s ease;
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
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        <div class="text-content">
            <h1 class="title">{title_text}</h1>
            <p class="body-text">{body_text}</p>
        </div>
        
        <div class="button-grid">
            <button class="btn btn-1">Highlight Fill</button>
            <button class="btn btn-2">Slide from Right</button>
            <button class="btn btn-3">Slide from Bottom</button>
            <button class="btn btn-4">3D Press</button>
            <button class="btn btn-5">Cross Outline</button>
        </div>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Interactive CSS Buttons
// These animations are entirely CSS-driven. 
// JavaScript is included here only to ensure standard component structure compliance.

document.addEventListener('DOMContentLoaded', () => {{
    // Optional: Add simple click sound or logging for demonstration
    const buttons = document.querySelectorAll('.btn');
    buttons.forEach(btn => {{
        btn.addEventListener('click', (e) => {{
            console.log(`Action triggered on: ${{e.target.textContent}}`);
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
