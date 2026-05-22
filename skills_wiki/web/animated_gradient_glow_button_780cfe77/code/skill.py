def create_component(
    output_dir: str,
    title_text: str = "Hover Me!",
    body_text: str = "",
    color_scheme: str = "dark",        
    accent_color: str = "#00bfff",     
    width_px: int = 800,
    height_px: int = 600,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Animated Gradient Glow Button visual effect.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors ===
    if color_scheme == "dark":
        bg_color = "#161616"
        text_color = "#FFFFFF"
        active_text_color = "#000000"
    else:
        bg_color = "#F8F9FA"
        text_color = "#161616"
        active_text_color = "#FFFFFF"

    # === CSS ===
    css = f"""/* Animated Gradient Glow Button */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg-color: {bg_color};
    --text-color: {text_color};
    --active-text: {active_text_color};
    --accent: {accent_color};
    /* A vibrant rainbow gradient that integrates the user's accent color */
    --glow-gradient: linear-gradient(
        45deg, 
        #FF0000, 
        #FF7300, 
        #FFFB00, 
        #48FF00, 
        var(--accent), 
        #002BFF, 
        #FF00C8, 
        #FF0000
    );
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
    height: var(--height);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 30px;
}}

.body-text {{
    font-size: 1rem;
    opacity: 0.7;
    text-align: center;
    max-width: 60%;
}}

/* Button Core Style */
.glow-btn {{
    position: relative;
    padding: 15px 40px;
    font-size: 1.1rem;
    color: var(--text-color);
    background-color: transparent; /* Must be transparent to let pseudo-elements show */
    border: none;
    outline: none;
    cursor: pointer;
    border-radius: 12px;
    z-index: 1; /* Establishes stacking context */
    transition: color 0.1s ease-in-out, font-weight 0.1s;
}}

/* Inner solid background (hides the center of the gradient) */
.glow-btn::after {{
    content: "";
    position: absolute;
    inset: 0; /* Shorthand for top, left, right, bottom: 0 */
    background-color: var(--bg-color);
    border-radius: inherit;
    z-index: -1; /* Sits behind the text, above the glow */
    transition: background-color 0.1s ease-in-out;
}}

/* Outer Glowing Gradient */
.glow-btn::before {{
    content: "";
    position: absolute;
    /* Pushes the gradient slightly outside the button bounds */
    top: -2px;
    left: -2px;
    right: -2px;
    bottom: -2px;
    background: var(--glow-gradient);
    background-size: 600%;
    z-index: -2; /* Sits at the very back */
    filter: blur(8px);
    opacity: 0.3; /* Subtle glow when idle */
    transition: opacity 0.3s ease-in-out;
    border-radius: inherit;
    animation: glowing-anim 20s linear infinite;
}}

/* Hover Interaction */
.glow-btn:hover::before {{
    opacity: 1; /* Intense glow on hover */
}}

/* Active/Click Interaction */
.glow-btn:active {{
    color: var(--active-text);
    font-weight: 700;
}}

/* Hide the solid background on click, revealing the entire gradient inside */
.glow-btn:active::after {{
    background-color: transparent;
}}

/* Keyframes for continuously rotating the gradient background */
@keyframes glowing-anim {{
    0% {{
        background-position: 0 0;
    }}
    50% {{
        background-position: 400% 0;
    }}
    100% {{
        background-position: 0 0;
    }}
}}

/* Accessibility: Respect reduced motion preference */
@media (prefers-reduced-motion: reduce) {{
    .glow-btn::before {{
        animation: none;
        background-size: 100%;
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
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        <!-- The Animated Glow Button -->
        <button class="glow-btn">{title_text}</button>
        
        <!-- Optional body text from parameters -->
        <p class="body-text">{body_text}</p>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// [Animated Gradient Glow Button]
document.addEventListener('DOMContentLoaded', () => {{
    const btn = document.querySelector('.glow-btn');
    
    // The visual effects are entirely CSS-driven.
    // This script file ensures functionality triggers if needed in a real app.
    btn.addEventListener('click', () => {{
        console.log('Glowing button clicked!');
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
