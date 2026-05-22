def create_component(
    output_dir: str,
    title_text: str = "Featured Products",
    body_text: str = "Check out our new and popular products directly from nature.",
    color_scheme: str = "dark",        
    accent_color: str = "#00bfff",     
    width_px: int = 1200,
    height_px: int = 600,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Centered Text Overlay on Image effect.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Use a high-quality landscape image for the background
    image_url = kwargs.get("image_url", "https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?auto=format&fit=crop&w=1600&q=80")

    # CSS Configuration
    css = f"""/* Centered Text Overlay on Image — generated component */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --accent: {accent_color};
    --width: {width_px}px;
    --height: {height_px}px;
    --text-color: #ffffff;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background: #f4f4f5;
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 2rem;
}}

/* The parent container sets the bounds and positioning context */
.image-overlay-container {{
    width: 100%;
    max-width: var(--width);
    height: var(--height);
    position: relative; /* Crucial for bounding absolute children */
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15);
    display: flex; /* Following the tutorial's alignment technique */
    align-items: center;
    justify-content: center;
    cursor: pointer;
}}

/* The image acts as the visual background */
.background-image {{
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    object-fit: cover; /* Prevents distortion */
    z-index: 1;
    transition: transform 0.6s cubic-bezier(0.25, 0.46, 0.45, 0.94);
}}

/* A subtle overlay gradient ensures text readability against any image */
.image-overlay-container::after {{
    content: '';
    position: absolute;
    inset: 0;
    background: linear-gradient(to bottom, rgba(0,0,0,0.2) 0%, rgba(0,0,0,0.6) 100%);
    z-index: 2;
    transition: opacity 0.4s ease;
}}

/* The absolutely positioned text block */
.text-block {{
    position: absolute; /* Allows free movement over the image */
    z-index: 3; /* Places it above the image and gradient */
    text-align: center;
    color: var(--text-color);
    padding: 2rem;
    max-width: 80%;
    /* Flexbox aligns this naturally, but standard absolute centering is a good fallback: */
    /* top: 50%; left: 50%; transform: translate(-50%, -50%); */
}}

.text-title {{
    font-size: clamp(2rem, 5vw, 4rem);
    font-weight: 700;
    letter-spacing: -0.02em;
    margin-bottom: 0.5rem;
    text-shadow: 0 4px 12px rgba(0,0,0,0.4);
}}

.text-body {{
    font-size: clamp(1rem, 2vw, 1.25rem);
    font-weight: 400;
    opacity: 0.9;
    text-shadow: 0 2px 8px rgba(0,0,0,0.4);
}}

/* Optional polish: Hover interaction */
.image-overlay-container:hover .background-image {{
    transform: scale(1.05); /* Slight zoom effect on hover */
}}
"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Centered Text Overlay</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    
    <!-- Component Start -->
    <div class="image-overlay-container">
        <img src="{image_url}" alt="Scenic landscape background" class="background-image">
        
        <div class="text-block">
            <h1 class="text-title">{title_text}</h1>
            <p class="text-body">{body_text}</p>
        </div>
    </div>
    <!-- Component End -->

    <script src="script.js"></script>
</body>
</html>"""

    js = f"""// Component specific interactive behavior
document.addEventListener('DOMContentLoaded', () => {{
    // The core layout is achieved entirely via CSS.
    // This script is ready for future enhancements (e.g., parallax effects or scroll-triggers).
    console.log("Image Overlay Component Initialized.");
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
