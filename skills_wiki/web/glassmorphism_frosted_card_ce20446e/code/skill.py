def create_component(
    output_dir: str,
    title_text: str = "Glass-Effect",
    body_text: str = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Dicta sapiente illo ut rerum at nemo in sed cupiditate odio voluptatum excepturi reprehenderit eum maxime, labore.",
    color_scheme: str = "dark",        # "dark" (white glass) or "light" (dark glass)
    accent_color: str = "#ffffff",     # Accent color for title
    width_px: int = 400,
    height_px: int = 500,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Glassmorphism Frosted Card visual effect.
    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme ===
    if color_scheme == "dark":
        # White frosted glass for dark backgrounds
        text_color = "#ffffff"
        body_text_color = "rgba(255, 255, 255, 0.85)"
        glass_bg = "rgba(255, 255, 255, 0.05)"
        glass_border_top = "rgba(255, 255, 255, 0.4)"
        glass_border_left = "rgba(255, 255, 255, 0.3)"
        shadow = "rgba(0, 0, 0, 0.1)"
        bg_image_url = "https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?ixlib=rb-4.0.3&auto=format&fit=crop&w=1600&q=80" # Dark mountain landscape
    else:
        # Dark frosted glass for light backgrounds
        text_color = "#111827"
        body_text_color = "rgba(17, 24, 39, 0.85)"
        glass_bg = "rgba(0, 0, 0, 0.05)"
        glass_border_top = "rgba(255, 255, 255, 0.6)"
        glass_border_left = "rgba(255, 255, 255, 0.4)"
        shadow = "rgba(0, 0, 0, 0.05)"
        bg_image_url = "https://images.unsplash.com/photo-1490750967868-88cb44cb2e1b?ixlib=rb-4.0.3&auto=format&fit=crop&w=1600&q=80" # Light bright landscape

    # === CSS ===
    css = f"""/* Glassmorphism Card — generated component */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --text-main: {text_color};
    --text-body: {body_text_color};
    --accent: {accent_color};
    --glass-bg: {glass_bg};
    --glass-border-top: {glass_border_top};
    --glass-border-left: {glass_border_left};
    --shadow: {shadow};
    --card-width: {width_px}px;
    --card-height: {height_px}px;
}}

body {{
    font-family: 'Poppins', sans-serif;
    height: 100vh;
    width: 100vw;
    display: flex;
    justify-content: center;
    align-items: center;
    background: url('{bg_image_url}') center/cover no-repeat fixed;
    overflow: hidden;
}}

/* The core Glassmorphism container */
.glass-container {{
    width: 90%;
    max-width: var(--card-width);
    min-height: var(--card-height);
    padding: 40px;
    border-radius: 30px;
    
    /* 1. Subtle semi-transparent background */
    background-color: var(--glass-bg);
    
    /* 2. The core blur effect */
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    
    /* 3. Simulated light reflections on edges */
    border-top: 1px solid var(--glass-border-top);
    border-left: 1px solid var(--glass-border-left);
    
    /* 4. Subtle drop shadow */
    box-shadow: 5px 5px 15px var(--shadow);
    
    /* Internal layout */
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: flex-start;
    
    /* Animation polish */
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}}

.glass-container:hover {{
    transform: translateY(-5px);
    box-shadow: 8px 8px 25px var(--shadow);
}}

h1 {{
    font-size: 2rem;
    font-weight: 600;
    margin-bottom: 20px;
    color: var(--text-main);
    letter-spacing: 0.5px;
}}

p {{
    font-size: 1rem;
    line-height: 1.6;
    color: var(--text-body);
    text-align: justify;
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
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="glass-container">
        <h1>{title_text}</h1>
        <p>{body_text}</p>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Glassmorphism Card — Interactive behavior (Shell)
document.addEventListener('DOMContentLoaded', () => {{
    const card = document.querySelector('.glass-container');
    
    // Optional: Add a subtle dynamic light reflection effect on mousemove
    card.addEventListener('mousemove', (e) => {{
        const rect = card.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        
        // Example: dynamically altering background based on cursor position (disabled by default to preserve pure CSS effect)
        // card.style.background = `radial-gradient(circle at ${{x}}px ${{y}}px, rgba(255,255,255,0.1), rgba(255,255,255,0.02) 50%)`;
    }});
    
    card.addEventListener('mouseleave', () => {{
        // Reset styles if changed
        // card.style.background = 'var(--glass-bg)';
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
