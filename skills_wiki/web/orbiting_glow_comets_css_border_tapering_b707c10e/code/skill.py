def create_component(
    output_dir: str,
    title_text: str = "Processing Data",
    body_text: str = "Please wait while we establish a secure connection...",
    color_scheme: str = "dark",
    accent_color: str = "#ffd700", # Outer comet color (Gold)
    width_px: int = 800,
    height_px: int = 600,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Orbiting Glow Comets loader.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Base colors
    if color_scheme == "dark":
        bg_color = "#191918"
        text_color = "#ffffff"
    else:
        bg_color = "#e0e5ec"
        text_color = "#1a1a2e"

    # Define a secondary vibrant color for the inner comet (Lime green)
    # This maintains the visual contrast seen in the original design.
    accent_2 = "#32cd32" 

    css = f"""/* Orbiting Glow Comets — generated component */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --text: {text_color};
    --accent-1: {accent_color};
    --accent-2: {accent_2};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background-color: var(--bg);
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

.header {{
    text-align: center;
}}

.title {{
    font-weight: 300;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    font-size: 1.5rem;
    margin-bottom: 0.5rem;
    opacity: 0.9;
}}

.body-text {{
    font-size: 0.9rem;
    opacity: 0.5;
    max-width: 350px;
}}

/* === Core Loader Mechanics === */
.loader {{
    /* Using em units tied to font-size allows easy scaling */
    font-size: clamp(10px, 2vmin, 20px);
    width: 16em;
    height: 16em;
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    transition: transform 0.3s ease;
}}

.loader:hover {{
    transform: scale(1.05);
}}

.loader .face {{
    position: absolute;
    border-radius: 50%;
    border-style: solid;
    animation: animate 3s linear infinite;
    transition: animation-duration 0.3s ease;
}}

/* Outer Comet (Clockwise) */
.loader .face-outer {{
    width: 100%;
    height: 100%;
    color: var(--accent-1);
    /* Top and Left borders are colored */
    border-color: currentColor transparent transparent currentColor;
    /* Top and Right borders have width -> Left has 0 width, causing taper */
    border-width: 0.2em 0.2em 0em 0em;
    --deg: -45deg; /* Position of the thickest point */
    animation-direction: normal;
}}

/* Inner Comet (Counter-Clockwise) */
.loader .face-inner {{
    width: 70%;
    height: 70%;
    color: var(--accent-2);
    /* Top and Right borders are colored */
    border-color: currentColor currentColor transparent transparent;
    /* Top and Left borders have width -> Right has 0 width, causing taper */
    border-width: 0.2em 0em 0em 0.2em;
    --deg: -135deg; /* Position of the thickest point */
    animation-direction: reverse;
}}

/* The radius arm that positions the glowing dot */
.loader .face .circle {{
    position: absolute;
    width: 50%;
    height: 0.1em;
    top: 50%;
    left: 50%;
    background-color: transparent;
    transform: rotate(var(--deg));
    transform-origin: left;
}}

/* The Glowing Dot */
.loader .face .circle::before {{
    content: '';
    position: absolute;
    top: -0.45em; /* Centers the 1em dot on the 0.1em line */
    right: -0.5em;
    width: 1em;
    height: 1em;
    background-color: currentColor;
    border-radius: 50%;
    /* Layered shadows inheriting currentColor for an ambient bloom */
    box-shadow: 
        0 0 2em currentColor,
        0 0 4em currentColor,
        0 0 6em currentColor,
        0 0 8em currentColor,
        0 0 10em currentColor,
        0 0 0 0.5em rgba(255, 255, 255, 0.05);
}}

@keyframes animate {{
    0% {{
        transform: rotate(0deg);
    }}
    100% {{
        transform: rotate(360deg);
    }}
}}
"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        <div class="header">
            <h1 class="title">{title_text}</h1>
            <p class="body-text">{body_text}</p>
        </div>
        
        <div class="loader" aria-label="Loading animation" role="progressbar">
            <div class="face face-outer">
                <div class="circle"></div>
            </div>
            <div class="face face-inner">
                <div class="circle"></div>
            </div>
        </div>
    </div>
    
    <script src="script.js"></script>
</body>
</html>"""

    js = f"""// Orbiting Glow Comets — interactive behavior
document.addEventListener('DOMContentLoaded', () => {{
    const loader = document.querySelector('.loader');
    const faces = document.querySelectorAll('.face');

    // Add a satisfying interaction: hovering speeds up the comets
    loader.addEventListener('mouseenter', () => {{
        faces.forEach(face => {{
            face.style.animationDuration = '1s';
        }});
    }});

    loader.addEventListener('mouseleave', () => {{
        faces.forEach(face => {{
            face.style.animationDuration = '3s';
        }});
    }});
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
