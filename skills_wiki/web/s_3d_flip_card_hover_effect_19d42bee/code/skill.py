def create_component(
    output_dir: str,
    title_text: str = "Front Side of the Card",
    body_text: str = "Back Side of the Card\nSecondary details revealed on hover.",
    color_scheme: str = "light",
    accent_color: str = "#007bff",
    width_px: int = 300,
    height_px: int = 400,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the 3D Flip Card Hover Effect.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os
    import html

    os.makedirs(output_dir, exist_ok=True)
    
    # Escape user text to prevent HTML injection
    safe_title = html.escape(title_text)
    safe_body = html.escape(body_text).replace('\n', '<br>')

    # === Derive theme colors from color_scheme ===
    if color_scheme == "dark":
        page_bg = "#0d111c"
        page_text = "#f0f0f0"
        front_bg = accent_color
        front_text = "#ffffff"
        back_bg = "#1a2235"
        back_text = "#ffffff"
        back_border = f"2px solid {accent_color}"
    else:
        page_bg = "#f8f9fa"
        page_text = "#1a1a2e"
        front_bg = accent_color
        front_text = "#ffffff"
        back_bg = "#ffffff"
        back_text = "#1a1a2e"
        back_border = f"2px solid {accent_color}"

    # === CSS ===
    css = f"""/* 3D Flip Card Hover Effect — generated component */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --page-bg: {page_bg};
    --page-text: {page_text};
    --front-bg: {front_bg};
    --front-text: {front_text};
    --back-bg: {back_bg};
    --back-text: {back_text};
    --back-border: {back_border};
    --card-width: {width_px}px;
    --card-height: {height_px}px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background-color: var(--page-bg);
    color: var(--page-text);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 2rem;
}}

/* The container establishes the 3D perspective */
.card-container {{
    perspective: 1000px; /* Lower value = more extreme 3D effect */
    width: var(--card-width);
    max-width: 90vw; /* Responsive safeguard */
    height: var(--card-height);
    max-height: 90vh; /* Responsive safeguard */
    cursor: pointer;
}}

/* The inner card handles the 3D space context and transition */
.card {{
    position: relative;
    width: 100%;
    height: 100%;
    transform-style: preserve-3d;
    transition: transform 0.6s cubic-bezier(0.4, 0, 0.2, 1);
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15);
    border-radius: 12px;
}}

/* Trigger flip on hover (mouse) or focus-within (keyboard tabbing) */
.card-container:hover .card,
.card-container:focus-within .card {{
    transform: rotateY(180deg);
    box-shadow: 0 15px 40px rgba(0, 0, 0, 0.25);
}}

/* Shared styles for both faces */
.front, .back {{
    position: absolute;
    width: 100%;
    height: 100%;
    border-radius: 12px;
    /* Crucial: hides the reverse side when turned around */
    backface-visibility: hidden;
    -webkit-backface-visibility: hidden; /* Safari fallback */
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;
    padding: 2rem;
}}

/* Front face specific styles */
.front {{
    background-color: var(--front-bg);
    color: var(--front-text);
    /* Explicitly state 0deg to prevent visual bugs in some browsers */
    transform: rotateY(0deg); 
}}

.front h2 {{
    font-size: 1.5rem;
    font-weight: 600;
    line-height: 1.3;
}}

/* Back face specific styles */
.back {{
    background-color: var(--back-bg);
    color: var(--back-text);
    border: var(--back-border);
    /* Pre-rotate the back face so it's upside down initially */
    transform: rotateY(180deg);
}}

.back p {{
    font-size: 1.125rem;
    line-height: 1.6;
    opacity: 0.9;
}}

/* Accessibility: respect user preferences for motion */
@media (prefers-reduced-motion: reduce) {{
    .card {{
        transition: none;
    }}
}}
"""

    # === HTML ===
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>3D Flip Card Effect</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <!-- tabindex="0" makes the container keyboard focusable -->
    <div class="card-container" tabindex="0" aria-label="Interactive Flip Card">
        <div class="card">
            <!-- Front side -->
            <div class="front" aria-hidden="true">
                <h2>{safe_title}</h2>
            </div>
            <!-- Back side -->
            <div class="back">
                <p>{safe_body}</p>
            </div>
        </div>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// 3D Flip Card Effect
// The core animation is driven purely by CSS :hover and :focus-within.
// This JS file is included for potential future extensions, such as handling click-to-flip on mobile devices.

document.addEventListener('DOMContentLoaded', () => {{
    const container = document.querySelector('.card-container');
    const card = document.querySelector('.card');

    // Optional: Add toggle behavior for touch devices
    container.addEventListener('click', () => {{
        // If you wanted a purely JS driven toggle state instead of CSS hover:
        // card.style.transform = card.style.transform === 'rotateY(180deg)' ? 'rotateY(0deg)' : 'rotateY(180deg)';
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
