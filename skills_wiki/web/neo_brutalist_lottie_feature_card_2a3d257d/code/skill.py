def create_component(
    output_dir: str,
    title_text: str = "Explore your new skills",
    body_text: str = "New skills diversify your job options and help you to keep up with the fast-changing world.",
    color_scheme: str = "light",        # "dark" or "light"
    accent_color: str = "#6C5CE7",     # CSS hex color for the call-to-action
    width_px: int = 420,
    height_px: int = 700,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Neo-Brutalist Lottie Feature Card.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme ===
    if color_scheme == "dark":
        bg_color = "#121212"
        text_color = "#ffffff"
        border_color = "#ffffff"
        card_bg = "#1e1e1e"
        lottie_bg = "#2a2a2a"
        btn_text = "#000000"
    else:
        bg_color = "#F4EFE6"
        text_color = "#000000"
        border_color = "#000000"
        card_bg = "#FFFBF2"
        lottie_bg = "#FFC5C5"
        btn_text = "#ffffff"

    # Using the exact animation URL generated in the video tutorial
    # If the file is inaccessible, the player fails gracefully.
    lottie_url = "https://lottie.host/48bfaa2f-8364-4384-9964-b508431398ae/6rZxAJjQ89.json"

    # === CSS ===
    css = f"""/* Neo-Brutalist Lottie Feature Card */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --text: {text_color};
    --accent: {accent_color};
    --border-color: {border_color};
    --card-bg: {card_bg};
    --lottie-bg: {lottie_bg};
    --btn-text: {btn_text};
    --width: {width_px}px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background: var(--bg);
    color: var(--text);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 2rem;
    overflow-x: hidden;
}}

.card {{
    width: 100%;
    max-width: var(--width);
    background: var(--card-bg);
    border: 4px solid var(--border-color);
    border-radius: 16px;
    box-shadow: 8px 8px 0px var(--border-color);
    overflow: hidden;
    display: flex;
    flex-direction: column;
    /* Spring-like transition for brutalist interaction */
    transition: transform 0.2s cubic-bezier(0.25, 1, 0.5, 1), box-shadow 0.2s cubic-bezier(0.25, 1, 0.5, 1);
}}

.card:hover {{
    transform: translate(-4px, -4px);
    box-shadow: 12px 12px 0px var(--border-color);
}}

.lottie-container {{
    background: var(--lottie-bg);
    border-bottom: 4px solid var(--border-color);
    padding: 2rem;
    display: flex;
    justify-content: center;
    align-items: center;
    position: relative;
}}

lottie-player {{
    width: 100%;
    height: 240px;
    transition: transform 0.3s ease;
}}

.card:hover lottie-player {{
    transform: scale(1.05);
}}

.card-content {{
    padding: 2.5rem 2rem;
    display: flex;
    flex-direction: column;
    gap: 1.25rem;
}}

.title {{
    font-family: 'Space Grotesk', sans-serif;
    font-size: 2.25rem;
    line-height: 1.1;
    font-weight: 700;
    letter-spacing: -0.02em;
}}

.body-text {{
    font-size: 1.05rem;
    line-height: 1.6;
    font-weight: 500;
    opacity: 0.9;
}}

.btn {{
    background: var(--accent);
    color: var(--btn-text);
    border: 4px solid var(--border-color);
    border-radius: 8px;
    padding: 1rem 1.5rem;
    font-family: 'Space Grotesk', sans-serif;
    font-weight: 700;
    font-size: 1.15rem;
    box-shadow: 4px 4px 0px var(--border-color);
    cursor: pointer;
    transition: all 0.15s ease;
    align-self: flex-start;
    margin-top: 0.5rem;
}}

.btn:hover {{
    transform: translate(-2px, -2px);
    box-shadow: 6px 6px 0px var(--border-color);
    background: var(--text);
    color: var(--bg);
}}

.btn:active {{
    transform: translate(4px, 4px);
    box-shadow: 0px 0px 0px var(--border-color);
}}
"""

    # === HTML ===
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Neo-Brutalist Lottie Feature Card</title>
    
    <!-- Google Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@600;700&family=Inter:wght@400;500&display=swap" rel="stylesheet">
    
    <!-- Custom CSS -->
    <link rel="stylesheet" href="style.css">
    
    <!-- Lottie Player Web Component -->
    <script src="https://unpkg.com/@lottiefiles/lottie-player@latest/dist/lottie-player.js"></script>
</head>
<body>

    <article class="card">
        <header class="lottie-container">
            <!-- 
               If the tutorial's exact URL expires, the player fails gracefully. 
               Feel free to swap the src attribute with any valid Lottie JSON.
            -->
            <lottie-player 
                src="{lottie_url}" 
                background="transparent" 
                speed="1" 
                loop 
                autoplay>
            </lottie-player>
        </header>
        <div class="card-content">
            <h2 class="title">{title_text}</h2>
            <p class="body-text">{body_text}</p>
            <button class="btn">Start Learning</button>
        </div>
    </article>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Lottie Interaction Logic
document.addEventListener('DOMContentLoaded', () => {{
    const card = document.querySelector('.card');
    const player = document.querySelector('lottie-player');
    const btn = document.querySelector('.btn');

    // Make the animation react dynamically to user interaction
    card.addEventListener('mouseenter', () => {{
        // Speed up animation to reward hover intent
        if(player && typeof player.setSpeed === 'function') {{
            player.setSpeed(1.5);
        }}
    }});

    card.addEventListener('mouseleave', () => {{
        // Return to passive speed
        if(player && typeof player.setSpeed === 'function') {{
            player.setSpeed(1.0);
        }}
    }});
    
    // Wire the Call-to-Action to reset/restart the animation timeline
    btn.addEventListener('click', (e) => {{
        if(player && typeof player.seek === 'function' && typeof player.play === 'function') {{
            player.seek(0);
            player.play();
        }}
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
