def create_component(
    output_dir: str,
    title_text: str = "I am",
    body_text: str = "", # Not actively used in this specific hero pattern, but accepted by signature
    color_scheme: str = "light",
    accent_color: str = "#ff4500",
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Auto-Typing Text Cycler visual effect.
    
    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os
    import json

    os.makedirs(output_dir, exist_ok=True)

    # Allow custom words via kwargs, fallback to tutorial defaults
    words = kwargs.get("words", ["YouTuber", "Web Developer", "Freelancer", "Instructor"])
    typing_speed = kwargs.get("typing_speed", 250) # ms per character

    # === Derive theme colors ===
    if color_scheme == "dark":
        bg_color = "#121212"
        text_color = "#e0e0e0"
        # Ensure accent is visible on dark
        theme_accent = accent_color if accent_color != "#111111" else "#4da6ff" 
    else:
        bg_color = "#FA8072" # Signature Salmon color from the tutorial
        text_color = "#111111"
        theme_accent = accent_color

    # === CSS ===
    css = f"""/* Auto Text Effect Animation — generated component */
@import url('https://fonts.googleapis.com/css2?family=Permanent+Marker&display=swap');

*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --text: {text_color};
    --accent: {theme_accent};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Permanent Marker', cursive, system-ui, sans-serif;
    background-color: var(--bg);
    color: var(--text);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
}}

.container {{
    width: var(--width);
    height: var(--height);
    display: flex;
    align-items: center;
    justify-content: center;
    text-align: center;
    padding: 2rem;
}}

.dynamic-headline {{
    font-size: clamp(2.5rem, 6vw, 5rem);
    letter-spacing: 2px;
    line-height: 1.2;
}}

.typed-word {{
    color: var(--accent);
}}

/* Optional cursor effect to enhance the tutorial's base pattern */
.typed-word::after {{
    content: '|';
    animation: blink 1s step-start infinite;
    color: var(--text);
    opacity: 0.7;
}}

@keyframes blink {{
    50% {{ opacity: 0; }}
}}
"""

    # === HTML ===
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Auto Text Effect Component</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        <!-- Target container for JavaScript injection -->
        <div id="text-container"></div>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Auto Text Effect Logic
document.addEventListener('DOMContentLoaded', () => {{
    const containerEl = document.getElementById('text-container');
    
    // Configurable parameters injected via Python
    const prefix = "{title_text}";
    const careers = {json.dumps(words)};
    const typingSpeed = {typing_speed};

    let careerIndex = 0;
    let characterIndex = 0;

    function updateText() {{
        characterIndex++;
        let currentWord = careers[careerIndex];

        // Intelligent article selection based on starting vowel
        let firstLetter = currentWord.charAt(0).toUpperCase();
        let article = ['A', 'E', 'I', 'O', 'U'].includes(firstLetter) ? "an" : "a";

        // Inject the HTML with stylized parts
        containerEl.innerHTML = `<h1 class="dynamic-headline">${{prefix}} ${{article}} <span class="typed-word">${{currentWord.slice(0, characterIndex)}}</span></h1>`;

        // Logic to jump to the next word when current word finishes
        if (characterIndex === currentWord.length) {{
            careerIndex++;
            characterIndex = 0;
        }}

        // Logic to loop back to the first word when the array ends
        if (careerIndex === careers.length) {{
            careerIndex = 0;
        }}

        setTimeout(updateText, typingSpeed);
    }}

    // Initialize animation loop
    updateText();
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
