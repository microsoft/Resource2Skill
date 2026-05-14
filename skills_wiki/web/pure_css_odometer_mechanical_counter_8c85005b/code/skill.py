def create_component(
    output_dir: str,
    title_text: str = "Live Server Metrics",
    body_text: str = "Pure CSS mechanical counter relying entirely on logarithmic animation steps.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#00bfff",     # CSS hex color for border accent
    width_px: int = 1000,
    height_px: int = 600,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Pure CSS Odometer visual effect.
    
    Optional kwargs:
    - digit_count (int): Number of rolling digits (default: 3)
    - base_speed (float): Duration in seconds for the fastest digit (default: 1.0)
    """
    import os

    os.makedirs(output_dir, exist_ok=True)
    
    digit_count = kwargs.get("digit_count", 3)
    base_speed = kwargs.get("base_speed", 1.0)

    # === Derive theme colors from color_scheme ===
    if color_scheme == "dark":
        bg_color = "#121212"
        text_color = "#ffffff"
        surface_color = "#222222"
        border_color = accent_color if accent_color else "#444"
        shadow = "rgba(0,0,0,0.6)"
    else:
        bg_color = "#f4f4f9"
        text_color = "#111111"
        surface_color = "#ffffff"
        border_color = accent_color if accent_color else "#ddd"
        shadow = "rgba(0,0,0,0.15)"

    # === Generate Digit Elements and CSS rules dynamically ===
    html_digits = ""
    css_digits = ""
    
    for i in range(digit_count):
        # i=0 is the leftmost (slowest), i=digit_count-1 is the rightmost (fastest)
        power = digit_count - 1 - i
        duration = base_speed * (10 ** power)
        
        html_digits += f'            <span class="digit digit-{i}" aria-hidden="true"></span>\n'
        css_digits += f"""
.digit-{i}::after {{
    animation: roll {duration}s steps(10) infinite;
}}"""

    # The string must have a space after \A to terminate the hex escape, 
    # the parser consumes the space so it won't render.
    content_str = r"0\A 1\A 2\A 3\A 4\A 5\A 6\A 7\A 8\A 9"

    # === CSS ===
    css = f"""/* Pure CSS Odometer — generated component */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --text: {text_color};
    --accent: {border_color};
    --surface: {surface_color};
    --shadow: {shadow};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Inter', system-ui, sans-serif;
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
    position: relative;
}}

.title {{
    font-size: 2.5rem;
    font-weight: 600;
    margin-bottom: 0.5rem;
    letter-spacing: -0.03em;
}}

.body-text {{
    font-size: 1rem;
    opacity: 0.7;
    margin-bottom: 4rem;
    max-width: 500px;
    text-align: center;
}}

.counter-wrapper {{
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 0.1em;
    font-size: clamp(4rem, 12vw, 10rem); /* Responsive scaling */
}}

.digit {{
    font-family: 'Oswald', sans-serif;
    display: inline-flex;
    justify-content: center;
    overflow: hidden;
    height: 1.2em;
    line-height: 1.2em;
    color: var(--text);
    background-color: var(--surface);
    /* 3D Drum cylinder effect */
    background-image: linear-gradient(to bottom, rgba(0,0,0,0.3) 0%, transparent 20%, transparent 80%, rgba(0,0,0,0.3) 100%);
    border: 0.03em solid var(--accent);
    border-radius: 0.15em;
    padding: 0 0.2em;
    box-shadow: inset 0 0.1em 0.2em var(--shadow), 0 0.1em 0.3em var(--shadow);
}}

.digit::after {{
    content: "{content_str}";
    position: relative;
    white-space: pre;
    text-align: center;
    /* GPU Acceleration */
    will-change: transform;
}}

/* Keyframe Animation */
@keyframes roll {{
    0% {{
        transform: translateY(0);
    }}
    100% {{
        /* Translates up exactly its own full height */
        transform: translateY(-100%);
    }}
}}
{css_digits}
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
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&family=Oswald:wght@700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        <h1 class="title">{title_text}</h1>
        <p class="body-text">{body_text}</p>
        
        <div class="counter-wrapper" aria-label="Rolling number counter animation" role="img">
{html_digits}        </div>
    </div>
    
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Pure CSS Effect — No JavaScript Required for the core logic
document.addEventListener('DOMContentLoaded', () => {{
    console.log("Odometer initialized - running on pure CSS.");
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
