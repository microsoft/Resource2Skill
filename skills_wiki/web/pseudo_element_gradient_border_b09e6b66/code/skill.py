def create_component(
    output_dir: str,
    title_text: str = "Gradient Border Button",
    body_text: str = "Hover over the button to see the flowing gradient border effect.",
    color_scheme: str = "dark",
    accent_color: str = "#00bfff",
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Pseudo-Element Gradient Border visual effect.
    """
    import os
    import html as html_lib

    os.makedirs(output_dir, exist_ok=True)

    safe_title = html_lib.escape(title_text)
    safe_body = html_lib.escape(body_text)

    # Derive theme colors
    if color_scheme == "dark":
        bg_color = "#0b0f19"
        text_color = "#f8fafc"
        surface_color = "#151b2b"
        accent_secondary = "#8b5cf6" # Violet to pair with accents
    else:
        bg_color = "#f1f5f9"
        text_color = "#0f172a"
        surface_color = "#ffffff"
        accent_secondary = "#f43f5e" # Rose to pair with accents

    css = f"""/* Pseudo-Element Gradient Border — generated component */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --text: {text_color};
    --surface: {surface_color};
    --accent: {accent_color};
    --accent-sec: {accent_secondary};
    --width: {width_px}px;
    --height: {height_px}px;
    --border-thickness: 3px;
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
    width: var(--width);
    height: var(--height);
    max-width: 100vw;
    max-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    padding: 2rem;
}}

.title {{
    font-size: 2.5rem;
    font-weight: 700;
    margin-bottom: 1rem;
    letter-spacing: -0.02em;
}}

.body-text {{
    font-size: 1.1rem;
    color: var(--text);
    opacity: 0.7;
    margin-bottom: 4rem;
    max-width: 500px;
    line-height: 1.5;
}}

/* === Core Skill: Gradient Border Button === */

.gradient-btn {{
    position: relative;
    /* CRITICAL: Creates a new stacking context. Prevents z-index: -1 from going behind body */
    isolation: isolate; 
    
    appearance: none;
    background-color: var(--surface);
    color: var(--text);
    font-family: inherit;
    font-size: 1.125rem;
    font-weight: 600;
    padding: 18px 40px;
    border: none;
    border-radius: 999px; /* Pill shape */
    cursor: pointer;
    transition: transform 0.2s cubic-bezier(0.34, 1.56, 0.64, 1), box-shadow 0.2s ease;
    outline: none;
}}

/* The Faux Border */
.gradient-btn::before {{
    content: '';
    position: absolute;
    /* Negative inset pushes the pseudo-element outside the button bounds */
    inset: calc(var(--border-thickness) * -1); 
    z-index: -1;
    
    /* Complex Gradient */
    background: linear-gradient(
        120deg, 
        var(--accent), 
        var(--accent-sec), 
        var(--accent)
    );
    background-size: 200% 200%;
    
    /* Match parent's border radius exactly */
    border-radius: inherit; 
    
    /* Flow animation */
    animation: gradient-flow 3s linear infinite;
}}

/* Subtle glow behind the button matching the gradient */
.gradient-btn::after {{
    content: '';
    position: absolute;
    inset: 0;
    z-index: -2;
    background: inherit;
    border-radius: inherit;
    box-shadow: 0 0 20px 0 var(--accent);
    opacity: 0;
    transition: opacity 0.3s ease;
}}

/* Interactions */
.gradient-btn:hover {{
    transform: translateY(-3px) scale(1.02);
}}

.gradient-btn:hover::after {{
    opacity: 0.4;
}}

.gradient-btn:active {{
    transform: translateY(1px) scale(0.98);
}}

/* Accessibility Focus State */
.gradient-btn:focus-visible {{
    box-shadow: 0 0 0 6px var(--bg), 0 0 0 9px var(--accent);
}}

@keyframes gradient-flow {{
    0% {{ background-position: 0% 50%; }}
    50% {{ background-position: 100% 50%; }}
    100% {{ background-position: 0% 50%; }}
}}
"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{safe_title}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        <h1 class="title">{safe_title}</h1>
        {f'<p class="body-text">{safe_body}</p>' if safe_body else ''}
        
        <button class="gradient-btn">
            Unlock Premium Features
        </button>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    js = """// Pseudo-Element Gradient Border — interactive behavior
document.addEventListener('DOMContentLoaded', () => {
    // Pure CSS handles the core visual effect and animation.
    // JS is included here for extensibility (e.g., handling click events).
    const btn = document.querySelector('.gradient-btn');
    
    btn.addEventListener('click', () => {
        // Simple ripple or confirmation effect could be added here
        btn.style.transform = 'scale(0.95)';
        setTimeout(() => {
            btn.style.transform = '';
        }, 150);
    });
});
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
