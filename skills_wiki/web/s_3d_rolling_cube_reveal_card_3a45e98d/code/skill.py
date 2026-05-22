def create_component(
    output_dir: str,
    title_text: str = "Wash Hands",
    body_text: str = "Scrub your hands with soap and water for at least 20 seconds to remove viruses.",
    color_scheme: str = "dark",
    accent_color: str = "#fa1e34",
    width_px: int = 1000,
    height_px: int = 600,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the 3D Rolling Cube Reveal Card effect.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Theme definitions matching the tutorial's high-contrast reveal pattern
    if color_scheme == "dark":
        bg_color = "#1e1e1e"
        front_bg = "#333333"
        front_text = "#ffffff"
        reveal_bg = "#ffffff"
        reveal_text = "#1e1e1e"
    else:
        bg_color = "#f8f9fa"
        front_bg = "#ffffff"
        front_text = "#1e1e1e"
        reveal_bg = "#1e1e1e"
        reveal_text = "#ffffff"

    # Fallback for empty body text
    body_text_final = body_text if body_text else "Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod."

    css = f"""/* 3D Rolling Cube Reveal Card */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg-color: {bg_color};
    --front-bg: {front_bg};
    --front-text: {front_text};
    --reveal-bg: {reveal_bg};
    --reveal-text: {reveal_text};
    --accent: {accent_color};
    --card-w: 250px;
    --card-h: 150px;
}}

body {{
    font-family: 'Poppins', sans-serif;
    background: var(--bg-color);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow-x: hidden;
}}

.container {{
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    align-items: center;
    gap: 30px;
    width: 100%;
    max-width: {width_px}px;
    padding: 40px 20px;
}}

.card {{
    width: var(--card-w);
    height: var(--card-h);
    position: relative;
    cursor: pointer;
    /* Removed overflow:hidden so the corners can "bow" out during the 3D roll */
}}

/* The front face (Icon + Title) */
.card .logo {{
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: var(--front-bg);
    color: var(--front-text);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    
    /* Origin at the bottom edge so it folds upwards from its base */
    transform-origin: bottom;
    transform: translateY(0) rotateX(0deg);
    transition: all 0.5s ease-in-out;
}}

.card .logo i {{
    font-size: 3rem;
    margin-bottom: 12px;
}}

.card .logo h3 {{
    font-size: 1.1rem;
    font-weight: 500;
    letter-spacing: 0.5px;
}}

/* The reveal face (Detailed Text) */
.card .content {{
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: var(--reveal-bg);
    color: var(--reveal-text);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    padding: 20px;
    
    /* Origin at the top edge. Initially translated down and rotated backward */
    transform-origin: top;
    transform: translateY(100%) rotateX(90deg);
    transition: all 0.5s ease-in-out;
}}

.card .content h2 {{
    font-size: 1.2rem;
    font-weight: 600;
    margin-bottom: 8px;
}}

.card .content p {{
    font-size: 0.8rem;
    line-height: 1.5;
    opacity: 0.85;
}}

/* === Hover & Focus Interactions === */

.card:hover .logo,
.card:focus-within .logo {{
    /* Translate UP by 100% and rotate backward 90deg */
    transform: translateY(-100%) rotateX(90deg);
    /* Flash the accent color during the fold */
    background: var(--accent);
}}

.card:hover .content,
.card:focus-within .content {{
    /* Translate back to 0 and flatten out to 0deg */
    transform: translateY(0) rotateX(0deg);
}}
"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>3D Rolling Cube Reveal Cards</title>
    <!-- Google Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600&display=swap" rel="stylesheet">
    <!-- Font Awesome -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        <!-- Card 1 -->
        <div class="card" tabindex="0">
            <div class="content">
                <h2>{title_text}</h2>
                <p>{body_text_final}</p>
            </div>
            <div class="logo">
                <i class="fas fa-hands-wash" aria-hidden="true"></i>
                <h3>{title_text}</h3>
            </div>
        </div>
        
        <!-- Card 2 -->
        <div class="card" tabindex="0">
            <div class="content">
                <h2>Wear Mask</h2>
                <p>Always wear a properly fitted mask when in crowded public spaces or indoors with others.</p>
            </div>
            <div class="logo">
                <i class="fas fa-head-side-mask" aria-hidden="true"></i>
                <h3>Wear Mask</h3>
            </div>
        </div>

        <!-- Card 3 -->
        <div class="card" tabindex="0">
            <div class="content">
                <h2>Stay Home</h2>
                <p>If you feel unwell or exhibit any symptoms, stay home to protect yourself and your community.</p>
            </div>
            <div class="logo">
                <i class="fas fa-house-user" aria-hidden="true"></i>
                <h3>Stay Home</h3>
            </div>
        </div>
    </div>
    
    <script src="script.js"></script>
</body>
</html>"""

    js = """// 3D Rolling Cube Reveal Card
// This component relies entirely on CSS transforms and transitions for its core visual effect.
document.addEventListener('DOMContentLoaded', () => {
    // Optional: Add keyboard interaction listeners if needed beyond :focus-within
    console.log("3D Rolling Cube Cards initialized.");
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
