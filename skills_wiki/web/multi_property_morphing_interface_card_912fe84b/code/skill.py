def create_component(
    output_dir: str,
    title_text: str = "CSS Transitions",
    body_text: str = "Hover over the shape below to trigger a smooth multi-property morphing effect.",
    color_scheme: str = "dark",        
    accent_color: str = "#ffff24",     # The yellow used in the video
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Multi-Property Morphing Interface Card.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Derive theme colors
    if color_scheme == "dark":
        bg_color = "#0d111c"
        text_color = "#f0f0f0"
        surface_color = "rgba(255, 255, 255, 0.06)"
        # Use the coral color from the video for the hover state
        hover_color = "#ff7f50" 
    else:
        bg_color = "#f8f9fa"
        text_color = "#1a1a2e"
        surface_color = "rgba(0, 0, 0, 0.04)"
        hover_color = "#ff7f50"

    # === CSS ===
    css = f"""/* Multi-Property Morphing Card — generated component */
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
    --hover-color: {hover_color};
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
    width: var(--width);
    height: var(--height);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 4rem;
    padding: 2rem;
}}

.header {{
    text-align: center;
    max-width: 600px;
}}

.title {{
    font-size: 2.5rem;
    font-weight: 700;
    margin-bottom: 1rem;
    letter-spacing: -0.02em;
}}

.body-text {{
    color: var(--text);
    opacity: 0.7;
    font-size: 1.1rem;
    line-height: 1.6;
}}

/* Safe zone for the scaling animation to prevent layout shifts */
.morph-wrapper {{
    position: relative;
    width: 350px;
    height: 350px;
    display: flex;
    align-items: center;
    justify-content: center;
    /* Optional: uncomment to preview cubic-bezier path */
    /* border: 1px dashed var(--surface); */
}}

/* The Core Shape */
.morph-box {{
    width: 160px;
    height: 160px;
    background-color: var(--accent);
    border-radius: 16px;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15);
    cursor: pointer;
    
    /* THE CORE TECHNIQUE: Transition shorthand applying to all properties */
    transition: all 1s cubic-bezier(0.4, 0, 0.2, 1);
}}

/* The Transformed State */
.morph-wrapper:hover .morph-box,
.morph-box.is-locked {{
    transform: rotate(135deg) scale(1.6);
    background-color: var(--hover-color);
    border-radius: 40px; /* Morphs from square to rounded diamond/circle */
    box-shadow: 0 20px 40px rgba(255, 127, 80, 0.3);
}}

/* Inner Content Stabilization */
.morph-content {{
    display: flex;
    flex-direction: column;
    align-items: center;
    color: #111; /* Dark text for contrast on yellow/coral */
    font-weight: 600;
    /* Transition must match the parent's timing exactly */
    transition: transform 1s cubic-bezier(0.4, 0, 0.2, 1), color 0.5s ease;
}}

/* Counter-rotate the inner content to keep it legible */
.morph-wrapper:hover .morph-content,
.morph-box.is-locked .morph-content {{
    transform: rotate(-135deg);
    color: #fff;
}}

.icon {{
    width: 40px;
    height: 40px;
    fill: currentColor;
    margin-bottom: 8px;
    transition: transform 0.3s ease;
}}

.morph-wrapper:hover .icon {{
    transform: scale(1.2);
}}

/* Accessibility: Respect user motion preferences */
@media (prefers-reduced-motion: reduce) {{
    .morph-box, .morph-content {{
        transition-duration: 0.1s !important;
    }}
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
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        <div class="header">
            <h1 class="title">{title_text}</h1>
            <p class="body-text">{body_text}</p>
        </div>
        
        <div class="morph-wrapper">
            <div class="morph-box" role="button" tabindex="0" aria-label="Interactive morphing shape">
                <div class="morph-content">
                    <!-- Inline SVG Icon for visual interest -->
                    <svg class="icon" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                        <path d="M12 2L2 22h20L12 2zm0 3.83L18.17 20H5.83L12 5.83z"/>
                    </svg>
                    <span>HOVER</span>
                </div>
            </div>
        </div>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Multi-Property Morphing Card — interactive behavior
document.addEventListener('DOMContentLoaded', () => {{
    const morphBox = document.querySelector('.morph-box');

    // Add keyboard support for accessibility
    morphBox.addEventListener('keydown', (e) => {{
        if (e.key === 'Enter' || e.key === ' ') {{
            e.preventDefault();
            morphBox.classList.toggle('is-locked');
        }}
    }});

    // Optional click interaction to lock the state
    morphBox.addEventListener('click', () => {{
        morphBox.classList.toggle('is-locked');
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
