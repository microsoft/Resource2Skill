def create_component(
    output_dir: str,
    title_text: str = "WebMrj Creations",
    body_text: str = "YouTube Channel",
    color_scheme: str = "dark",        # "dark" or "light" (controls page background)
    accent_color: str = "#e74c3c",     # CSS hex color for the card's back face
    width_px: int = 340,
    height_px: int = 480,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the 3D Flip Card visual effect.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)
    
    # Fallback image if not provided in kwargs
    image_url = kwargs.get("image_url", "https://images.unsplash.com/photo-1551698618-1dfe5d97d256?q=80&w=600&auto=format&fit=crop")

    # Set page background based on color_scheme
    if color_scheme == "dark":
        bg_color = "#1a1a2e"
    else:
        bg_color = "#2980b9" # The blue from the tutorial

    # === CSS ===
    css = f"""/* Interactive 3D Profile Card Flip */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg-color: {bg_color};
    --accent-color: {accent_color};
    --card-width: {width_px}px;
    --card-height: {height_px}px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background: var(--bg-color);
    min-height: 100vh;
    /* Center the card in the viewport */
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
}}

/* Card Container */
.card-container {{
    width: var(--card-width);
    height: var(--card-height);
    position: relative;
    /* Perspective can be applied here with transform-style, but we follow 
       the tutorial's approach of applying it directly to the transforms */
}}

/* Card Elements Wrapper */
.card {{
    width: 100%;
    height: 100%;
    position: absolute;
    cursor: pointer;
}}

/* Shared styles for both faces */
.front, .back {{
    width: 100%;
    height: 100%;
    position: absolute;
    top: 0;
    left: 0;
    overflow: hidden;
    backface-visibility: hidden; /* Hides the reverse side */
    transition: transform 0.6s cubic-bezier(0.4, 0, 0.2, 1); /* Smoother easing than linear */
    border-radius: 8px; /* Optional: adds subtle rounding */
    box-shadow: 0 15px 35px rgba(0,0,0,0.25);
}}

/* Front Face */
.front {{
    transform: perspective(600px) rotateY(0deg);
}}

.front img {{
    width: 100%;
    height: 100%;
    object-fit: cover;
    display: block;
}}

/* Back Face */
.back {{
    background: var(--accent-color);
    /* Initially flipped 180 degrees so it's hidden */
    transform: perspective(600px) rotateY(180deg);
    
    /* Flexbox used to center content instead of absolute positioning */
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    color: #ffffff;
    text-align: center;
    padding: 2rem;
}}

.back h2 {{
    font-size: 1.8rem;
    font-weight: 700;
    margin-bottom: 0.5rem;
    letter-spacing: 0.5px;
}}

.back span {{
    font-size: 1rem;
    font-weight: 300;
    opacity: 0.9;
    margin-bottom: 2rem;
}}

/* Hover Interactions */
/* We rotate the front to -180 and bring the back to 0 */
.card:hover .front,
.card:focus-within .front {{
    transform: perspective(600px) rotateY(-180deg);
}}

.card:hover .back,
.card:focus-within .back {{
    transform: perspective(600px) rotateY(0deg);
}}

/* Social Icons Container */
.social-icons {{
    display: flex;
    gap: 12px;
}}

.social-icons a {{
    color: #ffffff;
    font-size: 1.2rem;
    width: 45px;
    height: 45px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    text-decoration: none;
    border-radius: 50%;
    transition: background-color 0.3s ease, transform 0.2s ease;
}}

.social-icons a:hover,
.social-icons a:focus {{
    background-color: rgba(255, 255, 255, 0.2);
    transform: translateY(-3px);
    outline: none;
}}
"""

    # === HTML ===
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text} - 3D Flip Card</title>
    <!-- Google Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;700&display=swap" rel="stylesheet">
    <!-- Font Awesome for Icons -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    
    <div class="card-container">
        <!-- tabindex allows the card to receive keyboard focus -->
        <div class="card" tabindex="0" aria-label="Profile card for {title_text}">
            
            <!-- Front Face -->
            <div class="front" aria-hidden="true">
                <img src="{image_url}" alt="Cover Image">
            </div>
            
            <!-- Back Face -->
            <div class="back">
                <h2>{title_text}</h2>
                <span>{body_text}</span>
                
                <div class="social-icons">
                    <a href="#" aria-label="Facebook"><i class="fab fa-facebook-f"></i></a>
                    <a href="#" aria-label="Twitter"><i class="fab fa-twitter"></i></a>
                    <a href="#" aria-label="YouTube"><i class="fab fa-youtube"></i></a>
                    <a href="#" aria-label="Instagram"><i class="fab fa-instagram"></i></a>
                </div>
            </div>
            
        </div>
    </div>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// 3D Flip Card
// No JavaScript is required for the core 3D flip effect, as it is handled entirely by CSS.
// We include this file to satisfy the component structure and to allow for future enhancements
// (e.g., handling touch events on mobile if :hover behaves inconsistently).

document.addEventListener('DOMContentLoaded', () => {{
    console.log("Flip card initialized. Hover or tab to the card to interact.");
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
