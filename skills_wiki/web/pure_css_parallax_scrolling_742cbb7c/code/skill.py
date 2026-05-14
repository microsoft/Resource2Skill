def create_component(
    output_dir: str,
    title_text: str = "Header One",
    body_text: str = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Eius tempore corporis ad numquam. Quaerat repellendus magnam in incidunt est, nostrum voluptas, dicta ipsa impedit hic accusantium molestiae laudantium omnis quo aliquam architecto eligendi enim quis voluptatem vel veniam expedita earum, porro adipisci! Autem delectus vitae, velit minus similique quam neque!",
    color_scheme: str = "dark",
    accent_color: str = "#ffffff",
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Pure CSS Parallax effect.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Theme logic based on the tutorial's stark contrast style
    if color_scheme == "dark":
        text_bg = "#000000"
        text_color = "#ffffff"
    else:
        text_bg = "#ffffff"
        text_color = "#111111"

    css = f"""/* Pure CSS Parallax — generated component */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg-content: {text_bg};
    --text-color: {text_color};
    --accent: {accent_color};
    --comp-width: {width_px}px;
    --comp-height: {height_px}px;
}}

body {{
    font-family: 'Lato', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background: #e0e0e0;
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
}}

/* Container restricts the parallax to a specific component size */
/* For a full page website, these styles would apply to body/html */
.parallax-wrapper {{
    width: 100%;
    max-width: var(--comp-width);
    height: var(--comp-height);
    overflow-y: scroll;
    overflow-x: hidden;
    background: var(--bg-content);
    box-shadow: 0 20px 40px rgba(0,0,0,0.2);
}}

/* The Magic Parallax Class */
.parallax-bg {{
    width: 100%;
    min-height: 100%; /* Matches container height */
    background-attachment: fixed;
    background-position: center center;
    background-size: cover;
    background-repeat: no-repeat;
}}

/* Placeholder Images */
.bg-1 {{
    background-image: url('https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?auto=format&fit=crop&q=80&w=1600&h=900');
}}

.bg-2 {{
    background-image: url('https://images.unsplash.com/photo-1444464666168-49b6264240ce?auto=format&fit=crop&q=80&w=1600&h=900');
}}

.bg-3 {{
    background-image: url('https://images.unsplash.com/photo-1472396961693-142e6e269027?auto=format&fit=crop&q=80&w=1600&h=900');
}}

/* Content Sections */
.text-area {{
    background: var(--bg-content);
    color: var(--text-color);
    padding: 100px 20px;
    text-align: center;
}}

.text-area h2 {{
    font-size: clamp(28px, 4vw, 40px);
    margin: 0 0 20px 0;
    text-transform: uppercase;
    letter-spacing: 2px;
    color: var(--accent);
}}

.text-area p {{
    font-size: 18px;
    line-height: 1.6;
    width: 100%;
    max-width: 900px;
    margin: 0 auto;
    opacity: 0.9;
}}
"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CSS Parallax Effect</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Lato:wght@300;400;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>

    <div class="parallax-wrapper">
        <!-- Parallax Image 1 -->
        <div class="parallax-bg bg-1"></div>
        
        <!-- Text Content 1 -->
        <div class="text-area">
            <h2>{title_text}</h2>
            <p>{body_text}</p>
        </div>

        <!-- Parallax Image 2 -->
        <div class="parallax-bg bg-2"></div>
        
        <!-- Text Content 2 -->
        <div class="text-area">
            <h2>Header Two</h2>
            <p>{body_text}</p>
        </div>

        <!-- Parallax Image 3 -->
        <div class="parallax-bg bg-3"></div>
        
        <!-- Text Content 3 -->
        <div class="text-area">
            <h2>Header Three</h2>
            <p>{body_text}</p>
        </div>
    </div>

    <script src="script.js"></script>
</body>
</html>"""

    js = """// Pure CSS Parallax requires no JavaScript for the core effect.
// This file is included for extensibility.
document.addEventListener('DOMContentLoaded', () => {
    console.log('Parallax component loaded.');
});
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
