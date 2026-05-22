def create_component(
    output_dir: str,
    title_text: str = "Gradient text",
    body_text: str = "Hover over the text to see the spotlight effect.",
    color_scheme: str = "dark",
    accent_color: str = "#ffffff",  # Spotlight color
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Interactive Spotlight Text Gradient visual effect.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os
    import html

    os.makedirs(output_dir, exist_ok=True)
    
    # Escape user input
    safe_title = html.escape(title_text)
    safe_body = html.escape(body_text)

    # === Derive theme colors from color_scheme ===
    # For the text to look like it's "lit up" from the dark, 
    # the unlit base should be darker/dimmer than the background.
    if color_scheme == "dark":
        bg_color = "#1e1e24"
        text_base = "#000000" # Fades into deep shadow
        text_highlight = accent_color
        p_color = "#888888"
    else:
        bg_color = "#f4f5f7"
        text_base = "#c0c4cc" # Fades into flat grey
        text_highlight = accent_color if accent_color != "#ffffff" else "#333333"
        p_color = "#666666"

    # === CSS ===
    css = f"""/* Interactive Spotlight Text Gradient — generated component */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --text-highlight: {text_highlight};
    --text-base: {text_base};
    --p-color: {p_color};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background: var(--bg);
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    overflow: hidden;
}}

.container {{
    width: var(--width);
    height: var(--height);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 2rem;
    position: relative;
}}

.interactive-text {{
    /* Default variables for gradient center */
    --x: 50%;
    --y: 50%;
    
    font-size: clamp(4rem, 12vw, 10rem);
    font-weight: 900;
    letter-spacing: -0.03em;
    line-height: 1.1;
    text-align: center;
    
    /* The Spotlight Gradient */
    background: radial-gradient(
        circle at var(--x) var(--y),
        var(--text-highlight) 0%,
        var(--text-base) 80%
    );
    
    /* Apply masking */
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
    
    /* UX */
    cursor: crosshair;
    user-select: none;
    
    /* Smooth return to center when mouse leaves */
    /* Note: Only browsers supporting @property fully transition custom variables, 
       but snapping back is also an acceptable fallback */
    transition: filter 0.3s ease;
}}

.interactive-text:active {{
    filter: brightness(1.2);
}}

.body-text {{
    color: var(--p-color);
    font-size: 1.25rem;
    font-weight: 400;
    text-align: center;
    opacity: 0.8;
}}
"""

    # === HTML ===
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Interactive Spotlight Text</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;900&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        <!-- The core component -->
        <h1 class="interactive-text">{safe_title}</h1>
        
        {f'<p class="body-text">{safe_body}</p>' if body_text else ''}
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Interactive Spotlight Text Behavior
document.addEventListener('DOMContentLoaded', () => {{
    const textElement = document.querySelector('.interactive-text');

    if (!textElement) return;

    // Track mouse movement over the text element
    textElement.addEventListener('mousemove', (e) => {{
        // Get precise dimensions and position of the text node
        const rect = textElement.getBoundingClientRect();
        
        // Calculate relative local coordinates
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;

        // Convert to percentages
        const xPercent = Math.round((x / rect.width) * 100);
        const yPercent = Math.round((y / rect.height) * 100);

        // Update inline CSS custom properties
        textElement.style.setProperty('--x', xPercent + '%');
        textElement.style.setProperty('--y', yPercent + '%');
    }});

    // Reset the spotlight to the center when the mouse leaves
    textElement.addEventListener('mouseleave', () => {{
        textElement.style.setProperty('--x', '50%');
        textElement.style.setProperty('--y', '50%');
    }});
}});
"""

    # === Write files ===
    files = []
    for fname, content in [("index.html", html_content), ("style.css", css), ("script.js", js)]:
        path = os.path.join(output_dir, fname)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        files.append(path)

    return {
        "html": html_content,
        "css": css,
        "js": js,
        "files": files,
    }
