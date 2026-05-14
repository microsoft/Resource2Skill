def create_component(
    output_dir: str,
    title_text: str = "Easy Flip Card",
    body_text: str = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam in dui mauris.",
    color_scheme: str = "dark",        
    accent_color: str = "#ffffff",     
    width_px: int = 450,
    height_px: int = 500,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Continuous Looping Flip Card visual effect.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors ===
    if color_scheme == "dark":
        bg_color = "#121212"
        card_bg = "#242424"
        text_color = "#ffffff"
        text_dim = "rgba(255, 255, 255, 0.6)"
        # Default to a nice translucent border if the default accent is provided
        border_color = accent_color if accent_color != "#ffffff" else "rgba(255, 255, 255, 0.3)"
    else:
        bg_color = "#f0f0f0"
        card_bg = "#ffffff"
        text_color = "#121212"
        text_dim = "rgba(0, 0, 0, 0.6)"
        border_color = accent_color if accent_color != "#ffffff" else "rgba(0, 0, 0, 0.2)"

    # === CSS ===
    css = f"""/* Continuous Looping Flip Card Component */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --card-bg: {card_bg};
    --text: {text_color};
    --text-dim: {text_dim};
    --border: {border_color};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background: var(--bg);
    color: var(--text);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
}}

.container {{
    display: grid;
    place-items: center;
}}

.flip-card-wrapper {{
    position: relative;
    z-index: 1;
    perspective: 1000px;
    width: var(--width);
    height: var(--height);
    cursor: pointer;
}}

.flip-card-front, 
.flip-card-back {{
    position: absolute;
    inset: 0;
    backface-visibility: hidden;
    transition: transform 0.8s cubic-bezier(0.4, 0, 0.2, 1);
    padding: 32px;
    border: 1px solid var(--border);
    background: var(--card-bg);
    color: var(--text);
    display: flex;
}}

.flip-card-front {{
    flex-direction: column;
    justify-content: space-between;
    transform: rotateY(0deg);
}}

.flip-card-back {{
    flex-direction: column;
    justify-content: center;
    align-items: center;
    transform: rotateY(-180deg);
    text-align: center;
}}

/* Typography Details */
.card-front-top {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-family: 'Space Mono', monospace;
    font-size: 16px;
    color: var(--text-dim);
    letter-spacing: 1px;
}}

.card-front-top i {{
    font-size: 18px;
    color: var(--text);
}}

.card-front-bottom .title {{
    font-size: clamp(2rem, 8vw, 3rem);
    font-weight: 500;
    line-height: 1.1;
    letter-spacing: -0.5px;
}}

.flip-card-back span {{
    font-size: 1.25rem;
    line-height: 1.6;
    color: var(--text-dim);
    max-width: 80%;
}}
"""

    # === HTML ===
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text}</title>
    <!-- External Fonts and Icons -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500&family=Space+Mono&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        
        <div class="flip-card-wrapper">
            <!-- Front Face -->
            <div class="flip-card-front">
                <div class="card-front-top">
                    <div class="series">[ 01 ]</div>
                    <i class="fa-solid fa-arrow-up-right-from-square"></i>
                </div>
                <div class="card-front-bottom">
                    <span class="title">{title_text}</span>
                </div>
            </div>
            
            <!-- Back Face -->
            <div class="flip-card-back">
                <span>{body_text}</span>
            </div>
        </div>

    </div>
    
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Continuous Looping Flip Card Logic
document.addEventListener('DOMContentLoaded', () => {{
    const flipCards = document.querySelectorAll('.flip-card-wrapper');

    flipCards.forEach(card => {{
        // Initialize state for each card independently
        let rotateYFrontValue = 0;
        let rotateYBackValue = -180;

        // By attaching to both mouseenter and mouseleave and ALWAYS adding 180, 
        // we force the card to continuously spin forward in a loop rather than reversing.
        
        card.addEventListener('mouseenter', function() {{
            const front = this.querySelector('.flip-card-front');
            const back = this.querySelector('.flip-card-back');

            rotateYFrontValue += 180;
            rotateYBackValue += 180;

            front.style.transform = `rotateY(${{rotateYFrontValue}}deg)`;
            back.style.transform = `rotateY(${{rotateYBackValue}}deg)`;
        }});

        card.addEventListener('mouseleave', function() {{
            const front = this.querySelector('.flip-card-front');
            const back = this.querySelector('.flip-card-back');

            rotateYFrontValue += 180;
            rotateYBackValue += 180;

            front.style.transform = `rotateY(${{rotateYFrontValue}}deg)`;
            back.style.transform = `rotateY(${{rotateYBackValue}}deg)`;
        }});
    }});
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
