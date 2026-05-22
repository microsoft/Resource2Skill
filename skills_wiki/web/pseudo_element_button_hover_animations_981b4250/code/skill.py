def create_component(
    output_dir: str,
    title_text: str = "Pseudo-Element Button Animations",
    body_text: str = "Hover over the buttons below to interact with the CSS pseudo-element animations.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#00bfff",     # CSS hex color for accent
    width_px: int = 1000,
    height_px: int = 600,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the pseudo-element button hover animations.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors ===
    if color_scheme == "dark":
        bg_color = "#0d111c"
        text_color = "#f0f0f0"
        btn_bg = "#1e253c"
        btn_text = "#f0f0f0"
    else:
        bg_color = "#f8f9fa"
        text_color = "#1a1a2e"
        btn_bg = "#e9ecef"
        btn_text = "#1a1a2e"

    # === CSS ===
    css = f"""/* Pseudo-Element Button Animations */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --text: {text_color};
    --accent: {accent_color};
    --btn-bg: {btn_bg};
    --btn-text: {btn_text};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background: var(--bg);
    color: var(--text);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
}}

.container {{
    width: var(--width);
    max-width: 100%;
    height: var(--height);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 4rem;
    padding: 2rem;
}}

.header {{
    text-align: center;
}}

.header h1 {{
    font-size: 2.5rem;
    margin-bottom: 1rem;
    font-weight: 700;
}}

.header p {{
    font-size: 1.1rem;
    opacity: 0.8;
}}

.button-grid {{
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 3rem 4rem;
    width: 100%;
    max-width: 600px;
}}

/* =========================================
   Base Button Styles
   ========================================= */
.btn {{
    background-color: var(--btn-bg);
    color: var(--btn-text);
    padding: 1rem 2rem;
    font-size: 1.15rem;
    font-weight: 600;
    font-family: inherit;
    border: none;
    border-radius: 4px;
    position: relative;
    cursor: pointer;
    z-index: 1; /* Creates stacking context */
    --border-size: 3px;
    transition: color 300ms ease-in-out;
}}

/* =========================================
   1. Border Pop
   ========================================= */
.btn-border-pop::before {{
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; bottom: 0;
    z-index: -1;
    border: var(--border-size) solid var(--btn-bg);
    border-radius: 4px;
    transition: top 150ms ease-in-out, 
                left 150ms ease-in-out, 
                right 150ms ease-in-out, 
                bottom 150ms ease-in-out;
}}
.btn-border-pop:hover::before,
.btn-border-pop:focus-visible::before {{
    top: calc(var(--border-size) * -2);
    left: calc(var(--border-size) * -2);
    right: calc(var(--border-size) * -2);
    bottom: calc(var(--border-size) * -2);
}}

/* =========================================
   2. Background Slide
   ========================================= */
.btn-background-slide::before {{
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; bottom: 0;
    z-index: -1;
    background-color: var(--accent);
    border-radius: 4px;
    transform: scaleX(0);
    transform-origin: left;
    transition: transform 300ms ease-in-out;
}}
.btn-background-slide:hover::before,
.btn-background-slide:focus-visible::before {{
    transform: scaleX(1);
}}
.btn-background-slide:hover,
.btn-background-slide:focus-visible {{
    color: #ffffff;
}}

/* =========================================
   3. Background Circle
   ========================================= */
/* For this effect, the button itself is the accent color, 
   and the pseudo-element acts as a mask of the base color */
.btn-background-circle {{
    background-color: var(--accent);
    color: var(--btn-text);
    overflow: hidden;
    transition: color 500ms ease-in-out;
}}
.btn-background-circle::before {{
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; bottom: 0;
    z-index: -1;
    background-color: var(--btn-bg);
    border-radius: 50%;
    transform: scale(1.5);
    transition: transform 500ms ease-in-out;
}}
.btn-background-circle:hover::before,
.btn-background-circle:focus-visible::before {{
    transform: scale(0);
}}
.btn-background-circle:hover,
.btn-background-circle:focus-visible {{
    color: #ffffff;
}}

/* =========================================
   4. Border Underline
   ========================================= */
.btn-border-underline::before {{
    content: '';
    position: absolute;
    left: 0; right: 0; bottom: 0;
    height: var(--border-size);
    background-color: var(--accent);
    border-radius: 4px;
    transform: scaleX(0);
    /* Default transform-origin is center */
    transition: transform 300ms ease-in-out;
}}
.btn-border-underline:hover::before,
.btn-border-underline:focus-visible::before {{
    transform: scaleX(1);
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
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        <header class="header">
            <h1>{title_text}</h1>
            <p>{body_text}</p>
        </header>
        
        <div class="button-grid">
            <button class="btn btn-border-pop">Border Pop</button>
            <button class="btn btn-background-slide">Background Slide</button>
            <button class="btn btn-background-circle">Background Circle</button>
            <button class="btn btn-border-underline">Border Underline</button>
        </div>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = """// Pure CSS logic handles the animations.
// JavaScript can be used here for dynamic routing or event handling.
document.querySelectorAll('.btn').forEach(button => {
    button.addEventListener('click', function(e) {
        // Optional: add click ripple or sound effect logic here
        console.log(`${this.textContent} clicked.`);
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
