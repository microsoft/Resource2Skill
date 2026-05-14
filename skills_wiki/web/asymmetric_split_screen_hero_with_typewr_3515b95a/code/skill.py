def create_component(
    output_dir: str,
    title_text: str = "I am a",
    body_text: str = "Based in Manila, Philippines",
    color_scheme: str = "dark",
    accent_color: str = "#20c997",
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Asymmetric Split-Screen Hero with Typewriter Effect.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors ===
    if color_scheme == "dark":
        bg_color = "#111418"
        text_color = "#ffffff"
        sub_text_color = "#a0aab2"
        surface_color = "rgba(255, 255, 255, 0.05)"
    else:
        bg_color = "#ffffff"
        text_color = "#111418"
        sub_text_color = "#4a5568"
        surface_color = "rgba(0, 0, 0, 0.05)"

    # === CSS ===
    css = f"""/* Asymmetric Split-Screen Hero — generated component */
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@300;400;600;700;800&display=swap');

*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --text: {text_color};
    --sub-text: {sub_text_color};
    --accent: {accent_color};
    --surface: {surface_color};
}}

body {{
    font-family: 'Nunito', sans-serif;
    background-color: #000; /* Outer background to frame the component */
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 100vh;
}}

.portfolio-hero {{
    width: {width_px}px;
    height: {height_px}px;
    background-color: var(--bg);
    display: flex;
    overflow: hidden;
    border-radius: 12px;
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
}}

/* Left Side: Avatar */
.left-side {{
    flex: 3.5;
    position: relative;
    background-color: var(--surface);
}}

.left-side img {{
    width: 100%;
    height: 100%;
    object-fit: cover;
    display: block;
}}

/* Right Side: Content */
.right-side {{
    flex: 6.5;
    display: flex;
    flex-direction: column;
    justify-content: center;
    padding: 0 6rem;
    color: var(--text);
    position: relative;
}}

.greeting {{
    font-size: 1.5rem;
    font-weight: 600;
    margin-bottom: 0.5rem;
    color: var(--sub-text);
}}

.main-title {{
    font-size: 4.5rem;
    font-weight: 800;
    line-height: 1.1;
    margin-bottom: 1.5rem;
    display: flex;
    align-items: center;
    flex-wrap: wrap;
}}

.typewriter-wrapper {{
    display: inline-block;
    margin-left: 0.8rem;
    color: var(--accent);
}}

.cursor {{
    display: inline-block;
    width: 4px;
    height: 4.5rem;
    background-color: var(--text);
    margin-left: 4px;
    vertical-align: middle;
    animation: blink 1s step-end infinite;
}}

@keyframes blink {{
    0%, 100% {{ opacity: 1; }}
    50% {{ opacity: 0; }}
}}

.location {{
    font-size: 1.125rem;
    font-weight: 400;
    color: var(--sub-text);
    margin-bottom: 2.5rem;
}}

/* Interactive Elements */
.cta-button {{
    align-self: flex-start;
    padding: 1rem 2.5rem;
    font-size: 1rem;
    font-weight: 700;
    font-family: inherit;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: var(--text);
    background: transparent;
    border: 2px solid var(--text);
    border-radius: 4px;
    cursor: pointer;
    transition: all 0.3s ease;
    margin-bottom: 3rem;
}}

.cta-button:hover {{
    background-color: var(--accent);
    border-color: var(--accent);
    color: {bg_color}; /* Invert color */
}}

.social-links {{
    display: flex;
    gap: 1.5rem;
}}

.social-links a {{
    color: var(--text);
    font-size: 1.5rem;
    transition: all 0.3s ease;
    text-decoration: none;
}}

.social-links a:hover {{
    color: var(--accent);
    transform: translateY(-3px);
}}

/* Responsive adjustments for component rendering */
@media (max-width: 900px) {{
    .portfolio-hero {{
        flex-direction: column;
    }}
    .left-side {{
        flex: 4;
    }}
    .right-side {{
        flex: 6;
        padding: 0 3rem;
    }}
    .main-title {{
        font-size: 3rem;
    }}
    .cursor {{
        height: 3rem;
    }}
}}
"""

    # === HTML ===
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Portfolio Hero</title>
    <!-- FontAwesome for Social Icons -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" crossorigin="anonymous" referrerpolicy="no-referrer" />
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="portfolio-hero">
        
        <!-- Left Side: Avatar Image -->
        <div class="left-side">
            <img src="https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?q=80&w=1000&auto=format&fit=crop" alt="Profile Portrait">
        </div>

        <!-- Right Side: Content -->
        <div class="right-side">
            <p class="greeting">Hello</p>
            
            <h1 class="main-title">
                {title_text} 
                <div class="typewriter-wrapper">
                    <span class="typewriter" aria-hidden="true"></span><span class="cursor"></span>
                </div>
            </h1>
            
            <p class="location">{body_text}</p>
            
            <button class="cta-button">Hire Me</button>
            
            <div class="social-links">
                <a href="#" aria-label="GitHub"><i class="fa-brands fa-github"></i></a>
                <a href="#" aria-label="LinkedIn"><i class="fa-brands fa-linkedin-in"></i></a>
                <a href="#" aria-label="Twitter"><i class="fa-brands fa-twitter"></i></a>
            </div>
        </div>

    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Typewriter Effect Logic
document.addEventListener('DOMContentLoaded', () => {{
    const words = ["Designer.", "Photographer.", "Web Developer.", "Software Engineer."];
    const typeNode = document.querySelector('.typewriter');
    
    let currentWordIndex = 0;
    const typingSpeed = 100;
    const deletingSpeed = 50;
    const pauseBeforeDelete = 2000;
    const pauseBeforeType = 500;

    function typeEffect() {{
        let currentWord = words[currentWordIndex];
        let currentCharIndex = 0;

        const typeChar = () => {{
            if (currentCharIndex < currentWord.length) {{
                typeNode.textContent = currentWord.substring(0, currentCharIndex + 1);
                currentCharIndex++;
                setTimeout(typeChar, typingSpeed);
            }} else {{
                // Word completely typed out, wait before deleting
                setTimeout(deleteEffect, pauseBeforeDelete);
            }}
        }};
        
        typeChar();
    }}

    function deleteEffect() {{
        let currentWord = words[currentWordIndex];
        let currentCharIndex = currentWord.length;

        const deleteChar = () => {{
            if (currentCharIndex > 0) {{
                typeNode.textContent = currentWord.substring(0, currentCharIndex - 1);
                currentCharIndex--;
                setTimeout(deleteChar, deletingSpeed);
            }} else {{
                // Word completely deleted, move to next word
                currentWordIndex = (currentWordIndex + 1) % words.length;
                setTimeout(typeEffect, pauseBeforeType);
            }}
        }};
        
        deleteChar();
    }}

    // Start the animation
    setTimeout(typeEffect, 1000); // Initial delay before starting
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
