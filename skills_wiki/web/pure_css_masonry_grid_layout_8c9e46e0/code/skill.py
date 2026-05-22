def create_component(
    output_dir: str,
    title_text: str = "Pure CSS Masonry Layout",
    body_text: str = "A fluid grid of varying height cards built entirely with CSS columns.",
    color_scheme: str = "light",
    accent_color: str = "#007bff",
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Pure CSS Masonry Grid layout.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors ===
    if color_scheme == "dark":
        bg_color = "#121212"
        surface_color = "#1e1e1e"
        border_color = "#333333"
        text_primary = "#f0f0f0"
        text_secondary = "#a0a0a0"
    else:
        bg_color = "#f8f9fa"
        surface_color = "#ffffff"
        border_color = "#e0e0e0"
        text_primary = "#222222"
        text_secondary = "#555555"

    # === Generate dummy cards with varying text lengths ===
    cards_html = ""
    for i in range(1, 13):
        # Varying content length to demonstrate masonry stacking
        lines = 2 if i % 2 == 0 else (5 if i % 3 == 0 else 3)
        dummy_text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. " * lines
        
        cards_html += f"""
        <div class="box">
            <img src="https://picsum.photos/seed/{i * 10}/400/250" alt="Random sample image {i}">
            <h2 class="card-title">Card Heading or Title {i}</h2>
            <p class="card-text">{dummy_text}</p>
        </div>"""

    # === CSS ===
    css = f"""/* Pure CSS Masonry Grid — generated component */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg-color: {bg_color};
    --surface-color: {surface_color};
    --border-color: {border_color};
    --text-primary: {text_primary};
    --text-secondary: {text_secondary};
    --accent-color: {accent_color};
    --max-width: {width_px}px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background-color: var(--bg-color);
    color: var(--text-primary);
    min-height: 100vh;
    padding: 40px 20px;
}}

.page-header {{
    max-width: var(--max-width);
    margin: 0 auto 40px auto;
    text-align: center;
}}

.page-title {{
    font-size: 2.5rem;
    margin-bottom: 10px;
    color: var(--accent-color);
}}

.page-subtitle {{
    color: var(--text-secondary);
    font-size: 1.1rem;
}}

/* --- Core Masonry Container --- */
.container {{
    max-width: var(--max-width);
    margin: 0 auto;
    
    /* The magic properties */
    column-count: 4;
    column-gap: 20px;
}}

/* --- Core Masonry Item --- */
.box {{
    background-color: var(--surface-color);
    border: 1px solid var(--border-color);
    padding: 20px;
    border-radius: 8px;
    
    /* The magic properties */
    margin-bottom: 20px;
    break-inside: avoid;        /* Modern standard */
    page-break-inside: avoid;   /* Fallback for older browsers */
    
    /* Stability fixes for cross-browser column rendering */
    display: inline-block;
    width: 100%;
    
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    /* Initial state for JS animation */
    opacity: 0;
    transform: translateY(20px);
}}

.box:hover {{
    transform: translateY(-5px);
    box-shadow: 0 12px 24px rgba(0, 0, 0, 0.1);
    border-color: var(--accent-color);
}}

.box img {{
    width: 100%;
    height: 170px;
    object-fit: cover;
    border-radius: 4px;
    margin-bottom: 16px;
    background-color: #ddd;
}}

.card-title {{
    font-size: 1.25rem;
    margin-bottom: 12px;
    color: var(--text-primary);
    line-height: 1.3;
}}

.card-text {{
    font-size: 0.95rem;
    color: var(--text-secondary);
    line-height: 1.6;
}}

/* --- Responsive Breakpoints --- */
@media (max-width: 1024px) {{
    .container {{ column-count: 3; }}
}}

@media (max-width: 768px) {{
    .container {{ column-count: 2; }}
}}

@media (max-width: 480px) {{
    .container {{ column-count: 1; }}
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
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <header class="page-header">
        <h1 class="page-title">{title_text}</h1>
        <p class="page-subtitle">{body_text}</p>
    </header>

    <div class="container">
        {cards_html}
    </div>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = """// Pure CSS Masonry Layout — Polish and entry animations
document.addEventListener('DOMContentLoaded', () => {
    const boxes = document.querySelectorAll('.box');
    
    // Staggered entrance animation
    boxes.forEach((box, index) => {
        // Adjust delay slightly to simulate a natural flow
        const delay = (index % 4) * 100 + Math.floor(index / 4) * 50; 
        
        setTimeout(() => {
            box.style.transition = 'opacity 0.6s ease, transform 0.6s cubic-bezier(0.2, 0.8, 0.2, 1), box-shadow 0.3s ease';
            box.style.opacity = '1';
            box.style.transform = 'translateY(0)';
        }, delay);
    });
});
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
