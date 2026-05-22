def create_component(
    output_dir: str,
    title_text: str = "Fluid Gradient",
    body_text: str = "A smooth, infinite pastel background animation using pure CSS.",
    color_scheme: str = "light",
    accent_color: str = "#ffffff",
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Animated Fluid Radial Background.
    
    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors ===
    if color_scheme == "dark":
        # Rich, dark ethereal tones inspired by the Aurora Borealis
        c1 = "#4a00e0"
        c2 = "#8e2de2"
        c3 = "#f000ff"
        c4 = "#00c6ff"
        c5 = "#0072ff"
        c6 = "#3a7bd5"
        c7 = "#0f0c29"
        text_color = "#ffffff"
        card_bg = "rgba(0, 0, 0, 0.25)"
        card_border = "rgba(255, 255, 255, 0.1)"
    else:
        # The exact pastel palette extracted from the tutorial
        c1 = "#ffadad"
        c2 = "#ffd6a5"
        c3 = "#fdffb6"
        c4 = "#caffbf"
        c5 = "#9bf6ff"
        c6 = "#bdb2ff"
        c7 = "#ffc6ff"
        text_color = "#1a1a2e"
        card_bg = "rgba(255, 255, 255, 0.35)"
        card_border = "rgba(255, 255, 255, 0.5)"

    # === CSS ===
    css = f"""/* Animated Fluid Radial Background */
:root {{
    --color-1: {c1};
    --color-2: {c2};
    --color-3: {c3};
    --color-4: {c4};
    --color-5: {c5};
    --color-6: {c6};
    --color-7: {c7};
    --text: {text_color};
    --accent: {accent_color};
    --card-bg: {card_bg};
    --card-border: {card_border};
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
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 100vh;
    background-color: #000;
}}

/* The Core Effect Container */
.gradient-container {{
    width: var(--width);
    height: var(--height);
    max-width: 100vw;
    max-height: 100vh;
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
    border-radius: 8px; /* Optional framing for component view */
    
    /* Fallback color */
    background-color: var(--color-6);
    
    /* The core technique */
    background-image: radial-gradient(
        var(--color-1),
        var(--color-2),
        var(--color-3),
        var(--color-4),
        var(--color-5),
        var(--color-6),
        var(--color-7)
    );
    background-size: 500% 500%;
    animation: flowBackground 10s ease-in-out alternate infinite;
}}

@keyframes flowBackground {{
    0% {{
        background-position: 0% 0%;
    }}
    100% {{
        background-position: 100% 100%;
    }}
}}

/* A11y: Reduce motion for sensitive users */
@media (prefers-reduced-motion: reduce) {{
    .gradient-container {{
        animation-duration: 60s; /* Greatly slow down instead of abruptly stopping */
    }}
}}

/* Content Card to ensure text readability over bright shifting colors */
.content-card {{
    background: var(--card-bg);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    border: 1px solid var(--card-border);
    padding: 3rem 4rem;
    border-radius: 24px;
    text-align: center;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    color: var(--text);
    max-width: 80%;
    z-index: 10;
}}

.content-card h1 {{
    font-size: 3rem;
    font-weight: 700;
    margin-bottom: 1rem;
    letter-spacing: -0.05em;
}}

.content-card p {{
    font-size: 1.25rem;
    font-weight: 400;
    line-height: 1.6;
    opacity: 0.9;
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
    <div class="gradient-container">
        <div class="content-card">
            <h1>{title_text}</h1>
            <p>{body_text}</p>
        </div>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = """// Pure CSS effect. No JavaScript required for the core visual mechanism.
document.addEventListener('DOMContentLoaded', () => {
    console.log('Fluid gradient initialized via CSS.');
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
