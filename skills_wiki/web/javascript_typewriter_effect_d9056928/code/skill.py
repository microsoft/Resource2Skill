def create_component(
    output_dir: str,
    title_text: str = "Typewriter Effect",
    body_text: str = "",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#00bfff",     # CSS hex color for accent
    width_px: int = 800,
    height_px: int = 600,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the JavaScript Typewriter Effect.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)
    
    # Provide a default typing string if none is supplied
    if not body_text:
        body_text = "This is how you create a text typing effect with JavaScript 😎"
        
    safe_body_text = body_text.replace('"', '&quot;')

    # === Derive theme colors from color_scheme and accent_color ===
    if color_scheme == "dark":
        bg_color = "#0d111c"
        text_color = "#f0f0f0"
        surface_color = "rgba(255, 255, 255, 0.05)"
    else:
        bg_color = "#f8f9fa"
        text_color = "#1a1a2e"
        surface_color = "rgba(0, 0, 0, 0.05)"

    # === CSS ===
    css = f"""/* JavaScript Typewriter Effect */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --text: {text_color};
    --accent: {accent_color};
    --surface: {surface_color};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Lexend', system-ui, -apple-system, sans-serif;
    background: var(--bg);
    color: var(--text);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
}}

.container {{
    width: var(--width);
    max-width: 90vw;
    height: var(--height);
    background: var(--surface);
    border-radius: 16px;
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    justify-content: center;
    padding: 3rem;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
}}

.title {{
    font-size: 1rem;
    text-transform: uppercase;
    letter-spacing: 2px;
    color: var(--accent);
    margin-bottom: 1.5rem;
    font-weight: 600;
}}

.text-container {{
    font-size: clamp(1.5rem, 4vw, 2.5rem);
    line-height: 1.5;
    font-weight: 500;
    position: relative;
    max-width: 600px;
}}

/* Blinking Typewriter Cursor */
.text-container::after {{
    content: '|';
    color: var(--accent);
    margin-left: 2px;
    animation: blink 1s step-end infinite;
}}

@keyframes blink {{
    0%, 100% {{ opacity: 1; }}
    50% {{ opacity: 0; }}
}}

/* Accessibility: Hide full text visually, but keep for screen readers */
.sr-only {{
    position: absolute;
    width: 1px;
    height: 1px;
    padding: 0;
    margin: -1px;
    overflow: hidden;
    clip: rect(0, 0, 0, 0);
    white-space: nowrap;
    border-width: 0;
}}
"""

    # === HTML ===
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Lexend:wght@400;500;600&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        <h2 class="title">{title_text}</h2>
        
        <!-- Screen reader accessible text -->
        <p class="sr-only">{safe_body_text}</p>
        
        <!-- Visible animating text -->
        <div class="text-container" aria-hidden="true" data-text="{safe_body_text}"></div>
    </div>
    
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// JavaScript Typewriter Effect
document.addEventListener('DOMContentLoaded', () => {{
    const textElement = document.querySelector('.text-container');
    const textToType = textElement.getAttribute('data-text');

    /**
     * Recursively appends characters to an element with a delay.
     * @param {{HTMLElement}} element - The DOM node to populate.
     * @param {{string}} text - The full string to type out.
     * @param {{number}} i - The current character index.
     */
    function textTypingEffect(element, text, i = 0) {{
        // Safety check to clear the element on the first iteration
        if (i === 0) {{
            element.textContent = "";
        }}
        
        // Append the current character
        element.textContent += text[i];
        
        // Stop condition: if we've reached the last character
        if (i === text.length - 1) {{
            return;
        }}
        
        // Call the function again for the next character after 50ms
        setTimeout(() => textTypingEffect(element, text, i + 1), 50);
    }}

    // Initialize the effect
    if (textToType) {{
        textTypingEffect(textElement, textToType);
    }}
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
