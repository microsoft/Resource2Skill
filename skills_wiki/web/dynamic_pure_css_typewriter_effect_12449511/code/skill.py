def create_component(
    output_dir: str,
    title_text: str = "Typewriter CSS.",
    body_text: str = "A pure CSS animation pattern enhanced with dynamic properties.",
    color_scheme: str = "dark",
    accent_color: str = "#00bfff",
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Typewriter CSS visual effect.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme and accent_color ===
    if color_scheme == "dark":
        bg_color = "#0d111c"
        text_color = "#f0f0f0"
        subtext_color = "#8b949e"
    else:
        bg_color = "#f8f9fa"
        text_color = "#1a1a2e"
        subtext_color = "#57606a"

    # === CSS ===
    css = f"""/* Typewriter CSS Component */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --text: {text_color};
    --accent: {accent_color};
    --subtext: {subtext_color};
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
    width: 100%;
    max-width: var(--width);
    height: var(--height);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 2rem;
}}

/* -- Core Typewriter Component -- */
.typewriter-wrapper {{
    /* Using inline-block so the container wraps tightly to the text */
    display: inline-block;
    margin-bottom: 1.5rem;
}}

.typewriter-text {{
    /* Essential Properties for the effect */
    font-family: 'Fira Code', 'Courier New', Courier, monospace;
    font-weight: 600;
    font-size: clamp(1.5rem, 5vw, 4rem);
    white-space: nowrap;
    overflow: hidden;
    
    /* The blinking cursor */
    border-right: 0.15em solid var(--accent);
    padding-right: 0.1em;
    
    /* Fallback width if JS fails, but JS overrides this */
    width: 0; 
    
    /* Animation: 
       1. typing uses steps() to jump character by character
       2. blink uses step-end for the hard on/off cursor flash */
    animation: 
        typing var(--duration, 2s) steps(var(--steps, 20)) forwards,
        blink 0.8s step-end infinite;
}}

.body-text {{
    font-size: 1.25rem;
    color: var(--subtext);
    opacity: 0;
    transform: translateY(10px);
    text-align: center;
    max-width: 600px;
    line-height: 1.6;
    /* Fades in after the typewriter finishes */
    animation: fade-in 0.8s ease-out var(--duration, 2s) forwards;
}}

/* Keyframes */
@keyframes typing {{
    from {{ width: 0; }}
    to {{ width: calc(var(--steps) * 1ch); }}
}}

@keyframes blink {{
    from, to {{ border-color: transparent; }}
    50% {{ border-color: var(--accent); }}
}}

@keyframes fade-in {{
    to {{
        opacity: 1;
        transform: translateY(0);
    }}
}}
"""

    # === HTML ===
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Typewriter CSS Effect</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <!-- Inter for body font, Fira Code for Monospace Typewriter -->
    <link href="https://fonts.googleapis.com/css2?family=Fira+Code:wght@500;600&family=Inter:wght@400;500&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        <div class="typewriter-wrapper">
            <!-- The JS will read this text, count characters, and set --steps -->
            <h1 class="typewriter-text">{title_text}</h1>
        </div>
        <p class="body-text">{body_text}</p>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Dynamic property setup for the CSS Typewriter
document.addEventListener('DOMContentLoaded', () => {{
    const typewriterElements = document.querySelectorAll('.typewriter-text');
    
    typewriterElements.forEach(el => {{
        // 1. Get the exact text length (including spaces)
        const textLength = el.textContent.length;
        
        // 2. Set the CSS variable for the number of steps
        el.style.setProperty('--steps', textLength);
        
        // 3. Dynamically set duration based on character count (e.g., 150ms per character)
        // This ensures short words type fast, and long sentences don't type impossibly fast.
        const duration = Math.max(1.5, textLength * 0.15); // Minimum 1.5 seconds
        el.style.setProperty('--duration', `${{duration}}s`);
        
        // Pass duration up to the parent container so secondary elements 
        // (like the body text) know when to fade in.
        document.body.style.setProperty('--duration', `${{duration}}s`);
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
