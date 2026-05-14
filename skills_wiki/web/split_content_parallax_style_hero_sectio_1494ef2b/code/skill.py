def create_component(
    output_dir: str,
    title_text: str = "WELCOME TO MY FIRST WEBSITE",
    body_text: str = "This layout uses flexbox and relative positioning to create a striking, editorial-style hero section. The text naturally flows around the central focal area.",
    color_scheme: str = "dark",
    accent_color: str = "#C13584",
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Split-Content Parallax-Style Hero Section.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Base theme configuration
    if color_scheme == "dark":
        bg_color = "#0d1423" # Deep dark blue/slate
        text_color = "#ffffff"
        quote_text_color = "#e2e8f0"
        grid_color = "rgba(255, 255, 255, 0.03)"
        spotlight_color = "rgba(255, 255, 255, 0.08)"
    else:
        bg_color = "#f8fafc"
        text_color = "#0f172a"
        quote_text_color = "#334155"
        grid_color = "rgba(0, 0, 0, 0.04)"
        spotlight_color = "rgba(0, 0, 0, 0.06)"

    # CSS Content
    css = f"""@import url('https://fonts.googleapis.com/css2?family=Roboto:ital,wght@0,400;0,700;1,400&display=swap');

*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg-color: {bg_color};
    --text-color: {text_color};
    --quote-color: {quote_text_color};
    --accent-color: {accent_color};
    --grid-color: {grid_color};
    --spotlight-color: {spotlight_color};
    --container-width: {width_px}px;
    --container-height: {height_px}px;
}}

body {{
    font-family: 'Roboto', sans-serif;
    background-color: #000;
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
}}

.hero-main {{
    width: var(--container-width);
    height: var(--container-height);
    background-color: var(--bg-color);
    
    /* Multi-layered background replicating the tutorial's composite image approach */
    background-image: 
        /* Foreground focal point (Simulating the portrait) */
        radial-gradient(ellipse at bottom center, var(--spotlight-color) 0%, transparent 60%),
        /* Background subtle texture grid */
        linear-gradient(var(--grid-color) 1px, transparent 1px),
        linear-gradient(90deg, var(--grid-color) 1px, transparent 1px);
    background-size: 
        100% 75%, /* Spotlight scale */
        30px 30px, 
        30px 30px;
    background-position: bottom center, 0 0, 0 0;
    background-repeat: no-repeat, repeat, repeat;
    
    display: flex;
    justify-content: center;
    align-items: center;
    position: relative;
    overflow: hidden;
    color: var(--text-color);
}}

/* -- Left Column: Intro -- */
.main-intro {{
    position: relative;
    /* Pushing left to make room for central graphic */
    right: 12%; 
    max-width: 420px;
    padding-bottom: 6%;
    z-index: 2;
}}

.main-intro h1 {{
    font-size: 72px; /* Scaled slightly from 96px for generic fit */
    line-height: 1.1;
    font-weight: 700;
    text-transform: uppercase;
    margin-bottom: 24px;
}}

.main-intro p {{
    font-size: 18px;
    line-height: 1.6;
    margin-bottom: 30px;
}}

.main-intro a {{
    display: inline-block;
    background-color: var(--accent-color);
    color: #ffffff;
    padding: 12px 24px;
    text-decoration: none;
    font-weight: 700;
    text-transform: uppercase;
    font-size: 14px;
    letter-spacing: 1px;
    transition: opacity 0.2s ease;
}}

.main-intro a:hover {{
    opacity: 0.85;
}}

/* -- Right Column: Quotes -- */
.main-quotes {{
    position: relative;
    /* Pushing right to clear the center */
    left: 8%; 
    max-width: 380px;
    padding-bottom: 6%;
    z-index: 2;
}}

.main-quotes p {{
    font-size: 16px;
    line-height: 1.6;
    color: var(--quote-color);
    border-left: 4px solid var(--accent-color);
    padding-left: 20px;
    margin-bottom: 40px;
}}

.main-quotes p strong {{
    display: block;
    margin-top: 8px;
    font-size: 14px;
    color: var(--text-color);
}}

/* Asymmetrical layout trick applied to the nth-child */
.main-quotes p:nth-child(2) {{
    margin-left: 80px;
}}
"""

    # HTML Content
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Split-Content Parallax Hero</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <main class="hero-main">
        <!-- Left Side: Main Title and CTA -->
        <div class="main-intro">
            <h1>{title_text}</h1>
            <p>{body_text}</p>
            <a href="#work">My Work</a>
        </div>

        <!-- Right Side: Secondary Content / Quotes -->
        <div class="main-quotes">
            <p>
                "The more that you read, the more things you will know. The more that you learn, the more places you'll go."
                <strong>- Dr. Seuss</strong>
            </p>
            <p>
                "An investment in knowledge always pays the best interest."
                <strong>- Benjamin Franklin</strong>
            </p>
        </div>
    </main>
    <script src="script.js"></script>
</body>
</html>"""

    # JS Content (Empty for this static CSS layout, ready for parallax extension)
    js = """document.addEventListener('DOMContentLoaded', () => {
    // Structural layout handled entirely via CSS.
    // This script file is ready for Intersection Observers or Parallax scroll listeners.
});"""

    # Write files
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
