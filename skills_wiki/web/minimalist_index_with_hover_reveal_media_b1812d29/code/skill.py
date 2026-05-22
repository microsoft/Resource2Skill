def create_component(
    output_dir: str,
    title_text: str = "Seyit Yilmaz",
    body_text: str = "Human interface designer at Apple",
    color_scheme: str = "light",        # "dark" or "light"
    accent_color: str = "#0071e3",      # Used for subtle highlights if needed
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Minimalist Index Hover-Reveal effect.
    """
    import os
    import json

    os.makedirs(output_dir, exist_ok=True)

    # Theme colors
    if color_scheme == "dark":
        bg_color = "#161618"
        text_color = "#f5f5f7"
        text_muted = "#86868b"
        shadow_color = "rgba(0, 0, 0, 0.5)"
    else:
        bg_color = "#f5f5f7"
        text_color = "#1d1d1f"
        text_muted = "#86868b"
        shadow_color = "rgba(0, 0, 0, 0.08)"

    # Default project data representing a portfolio
    projects = [
        {"title": "DM Resharing", "year": "2022", "image": "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?q=80&w=600&auto=format&fit=crop"},
        {"title": "Media Viewer", "year": "2022", "image": "https://images.unsplash.com/photo-1551288049-bebda4e38f71?q=80&w=600&auto=format&fit=crop"},
        {"title": "Command System", "year": "2022", "image": "https://images.unsplash.com/photo-1512941937669-90a1b58e7e9c?q=80&w=600&auto=format&fit=crop"},
        {"title": "Send Interaction", "year": "2022", "image": "https://images.unsplash.com/photo-1633356122544-f134324a6cee?q=80&w=600&auto=format&fit=crop"},
        {"title": "Gyro Pride Theme", "year": "2021", "image": "https://images.unsplash.com/photo-1550745165-9bc0b252726f?q=80&w=600&auto=format&fit=crop"}
    ]

    # Generate HTML blocks
    list_html = ""
    media_html = ""
    
    for i, proj in enumerate(projects):
        active_class = "active" if i == 0 else ""
        list_html += f"""
                <li class="project-item {active_class}" data-index="{i}">
                    <span class="p-title">{proj['title']}</span>
                    <span class="p-year">{proj['year']}</span>
                </li>"""
        media_html += f"""
                <img src="{proj['image']}" class="media-item {active_class}" data-index="{i}" alt="{proj['title']}">"""

    # === CSS ===
    css = f"""/* Minimalist Index Hover-Reveal */
:root {{
    --bg: {bg_color};
    --text: {text_color};
    --text-muted: {text_muted};
    --accent: {accent_color};
    --shadow: {shadow_color};
    --width: {width_px}px;
    --height: {height_px}px;
}}

*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: -apple-system, BlinkMacSystemFont, "Inter", "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    background-color: var(--bg);
    color: var(--text);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    -webkit-font-smoothing: antialiased;
}}

.container {{
    width: var(--width);
    height: var(--height);
    max-width: 100vw;
    max-height: 100vh;
    display: flex;
    padding: 4rem;
    gap: 4rem;
}}

/* Left Column: Info & List */
.info-column {{
    flex: 1;
    display: flex;
    flex-direction: column;
    justify-content: center;
    padding-left: 2rem;
}}

header {{
    margin-bottom: 4rem;
}}

h1 {{
    font-size: 1.25rem;
    font-weight: 600;
    letter-spacing: -0.02em;
    margin-bottom: 0.25rem;
}}

.body-text {{
    font-size: 1rem;
    color: var(--text-muted);
    font-weight: 400;
}}

.project-list {{
    list-style: none;
    display: flex;
    flex-direction: column;
    gap: 1rem;
}}

.project-item {{
    display: flex;
    justify-content: space-between;
    width: 280px; /* Fixed width for perfect right-alignment of dates */
    font-size: 1rem;
    font-weight: 500;
    color: var(--text-muted);
    cursor: pointer;
    padding: 0.25rem 0;
    transition: color 0.3s ease, transform 0.3s ease;
}}

.project-item:hover, .project-item.active {{
    color: var(--text);
}}

/* Right Column: Media Reveal */
.media-column {{
    flex: 1;
    display: flex;
    justify-content: center;
    align-items: center;
}}

.media-wrapper {{
    position: relative;
    width: 320px;
    height: 650px;
    border-radius: 32px;
    overflow: hidden;
    background-color: var(--bg);
    box-shadow: 0 24px 48px var(--shadow);
    /* Mimic mobile device frame slightly */
    border: 8px solid var(--bg);
}}

.media-item {{
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    object-fit: cover;
    opacity: 0;
    transform: scale(1.05);
    /* Premium ease curve mimicking native iOS motion */
    transition: opacity 0.6s cubic-bezier(0.16, 1, 0.3, 1), transform 0.6s cubic-bezier(0.16, 1, 0.3, 1);
    pointer-events: none;
}}

.media-item.active {{
    opacity: 1;
    transform: scale(1);
    z-index: 1;
}}

/* Responsive adjustments */
@media (max-width: 900px) {{
    .container {{
        flex-direction: column;
        padding: 2rem;
        height: auto;
    }}
    .media-wrapper {{
        width: 100%;
        height: 400px;
        max-width: 320px;
        margin-top: 2rem;
    }}
    .project-item {{
        width: 100%;
        max-width: 320px;
    }}
}}
"""

    # === HTML ===
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text} - Portfolio</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        <div class="info-column">
            <header>
                <h1>{title_text}</h1>
                <p class="body-text">{body_text}</p>
            </header>
            
            <ul class="project-list">
{list_html}
            </ul>
        </div>
        
        <div class="media-column">
            <div class="media-wrapper">
{media_html}
            </div>
        </div>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = """// Minimalist Index Interactive Behavior
document.addEventListener('DOMContentLoaded', () => {
    const listItems = document.querySelectorAll('.project-item');
    const mediaItems = document.querySelectorAll('.media-item');

    listItems.forEach(item => {
        item.addEventListener('mouseenter', function() {
            // Get index of hovered item
            const index = this.getAttribute('data-index');

            // 1. Update text list state
            listItems.forEach(li => li.classList.remove('active'));
            this.classList.add('active');

            // 2. Update media visibility
            mediaItems.forEach(media => {
                if (media.getAttribute('data-index') === index) {
                    media.classList.add('active');
                } else {
                    media.classList.remove('active');
                }
            });
        });
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
