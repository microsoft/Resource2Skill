def create_component(
    output_dir: str,
    title_text: str = "John Doe",
    body_text: str = "UI & UX FRONT-END DEVELOPER",
    color_scheme: str = "dark",        
    accent_color: str = "#c500d6",     
    width_px: int = 280,
    height_px: int = 420,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the 3D Profile Flip Card visual effect.
    
    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme and accent_color ===
    if color_scheme == "dark":
        bg_color = "#f0f2f5" # Body background
        front_bg = "#24203b"
        text_color = "#ffffff"
        skill_bg = "#ffffff"
        skill_text = "#24203b"
    else:
        bg_color = "#121212" # Body background
        front_bg = "#ffffff"
        text_color = "#333333"
        skill_bg = "#f0f0f0"
        skill_text = "#333333"

    # === CSS ===
    css = f"""/* 3D Profile Flip Card — generated component */
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700&display=swap');

*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --body-bg: {bg_color};
    --front-bg: {front_bg};
    --back-bg: {accent_color};
    --text-color: {text_color};
    --skill-bg: {skill_bg};
    --skill-text: {skill_text};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Montserrat', sans-serif;
    background: var(--body-bg);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
}}

/* The 3D Perspective Wrapper */
.flip-container {{
    width: var(--width);
    height: var(--height);
    perspective: 1000px; /* Establishes the 3D space */
}}

/* The element that actually rotates */
.flip-inner-container {{
    position: relative;
    width: 100%;
    height: 100%;
    text-align: center;
    transition: transform 0.8s cubic-bezier(0.4, 0.2, 0.2, 1);
    transform-style: preserve-3d; /* Allows children to live in 3D space */
    border-radius: 12px;
    box-shadow: 0 15px 35px rgba(0,0,0,0.2);
}}

/* Trigger rotation on hover and keyboard focus */
.flip-container:hover .flip-inner-container,
.flip-container:focus-within .flip-inner-container {{
    transform: rotateY(180deg);
}}

/* Shared styles for both front and back faces */
.flip-front, 
.flip-back {{
    position: absolute;
    width: 100%;
    height: 100%;
    backface-visibility: hidden; /* Hides the backside of the panel when turned away */
    border-radius: 12px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 20px;
    color: var(--text-color);
    overflow: hidden;
}}

/* Front Face */
.flip-front {{
    background-color: var(--front-bg);
}}

/* Back Face */
.flip-back {{
    background-color: var(--back-bg);
    transform: rotateY(180deg); /* Pre-rotate so it faces the correct way when parent flips */
}}

/* --- Front Content Styling --- */
.profile-image {{
    width: 120px;
    height: 120px;
    border-radius: 50%;
    border: 4px solid var(--back-bg);
    background-image: url('https://i.pravatar.cc/300?img=11'); /* Placeholder image */
    background-size: cover;
    background-position: center;
    margin-bottom: 15px;
}}

.flip-front h3 {{
    font-size: 1.2rem;
    font-weight: 700;
    margin-bottom: 5px;
    text-transform: uppercase;
    letter-spacing: 1px;
}}

.flip-front h6 {{
    font-size: 0.7rem;
    font-weight: 400;
    margin-bottom: 20px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    opacity: 0.8;
}}

.skills-title {{
    font-size: 0.85rem;
    font-weight: 700;
    margin-bottom: 10px;
    border-bottom: 1px solid rgba(255,255,255,0.2);
    padding-bottom: 5px;
    width: 80%;
    text-transform: uppercase;
}}

.skills {{
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 8px;
}}

.skills span {{
    background-color: var(--skill-bg);
    color: var(--skill-text);
    padding: 4px 8px;
    font-size: 0.65rem;
    font-weight: 600;
    border-radius: 4px;
    text-transform: uppercase;
}}

/* --- Back Content Styling --- */
.flip-back h2 {{
    font-size: 1.8rem;
    font-weight: 700;
    margin-bottom: 30px;
    text-transform: uppercase;
}}

.btn {{
    display: inline-block;
    width: 80%;
    padding: 12px 0;
    margin-bottom: 15px;
    background-color: var(--front-bg);
    color: var(--text-color);
    text-decoration: none;
    font-size: 0.9rem;
    font-weight: 600;
    text-transform: uppercase;
    border-radius: 25px;
    transition: background-color 0.3s, transform 0.2s;
}}

.btn:hover, .btn:focus {{
    background-color: #1a172a; /* Slightly darker */
    transform: translateY(-2px);
    outline: 2px solid white;
    outline-offset: 2px;
}}
"""

    # === HTML ===
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>3D Flip Card</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>

    <div class="flip-container" tabindex="0" aria-label="Profile card for {title_text}">
        <div class="flip-inner-container">
            
            <!-- Front of the Card -->
            <div class="flip-front" aria-hidden="false">
                <div class="profile-image" role="img" aria-label="{title_text} Profile Picture"></div>
                <h3>{title_text}</h3>
                <h6>{body_text}</h6>
                
                <div class="skills-title">Skills</div>
                <div class="skills">
                    <span>UI & UX</span>
                    <span>Front-end</span>
                    <span>HTML</span>
                    <span>CSS</span>
                    <span>JavaScript</span>
                    <span>React</span>
                </div>
            </div>
            
            <!-- Back of the Card -->
            <div class="flip-back" aria-hidden="true">
                <h2>{title_text}</h2>
                <a href="#" class="btn btn_hire">Hire</a>
                <a href="#" class="btn btn_message">Message</a>
            </div>

        </div>
    </div>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    # For a purely CSS-driven hover effect, JS isn't strictly necessary.
    # However, to improve accessibility, we can toggle aria-hidden attributes 
    # when the card is hovered or focused via keyboard.
    js = f"""// 3D Profile Flip Card — Accessibility enhancements
document.addEventListener('DOMContentLoaded', () => {{
    const container = document.querySelector('.flip-container');
    const front = document.querySelector('.flip-front');
    const back = document.querySelector('.flip-back');

    const handleFlipIn = () => {{
        front.setAttribute('aria-hidden', 'true');
        back.setAttribute('aria-hidden', 'false');
    }};

    const handleFlipOut = () => {{
        front.setAttribute('aria-hidden', 'false');
        back.setAttribute('aria-hidden', 'true');
    }};

    // Mouse interactions
    container.addEventListener('mouseenter', handleFlipIn);
    container.addEventListener('mouseleave', handleFlipOut);

    // Keyboard interactions
    container.addEventListener('focusin', handleFlipIn);
    container.addEventListener('focusout', handleFlipOut);
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
