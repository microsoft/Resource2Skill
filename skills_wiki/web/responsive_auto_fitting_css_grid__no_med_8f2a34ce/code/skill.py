def create_component(
    output_dir: str,
    title_text: str = "Responsive Grid Layout",
    body_text: str = "Drag the handle on the bottom-right of the dashed box to resize the container and watch the grid automatically reflow.",
    color_scheme: str = "dark",
    accent_color: str = "#8a2be2",
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Responsive Auto-fitting CSS Grid layout.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    if color_scheme == "dark":
        bg_color = "rgb(13, 13, 20)"
        text_color = "#f0f0f0"
        card_bg = "#222429"
        card_border = "1px solid rgb(75, 82, 92)"
    else:
        bg_color = "#f4f6f8"
        text_color = "#1a1a2e"
        card_bg = "#ffffff"
        card_border = "1px solid #e1e4e8"

    css = f"""/* Responsive Auto-fitting CSS Grid */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --text: {text_color};
    --accent: {accent_color};
    --card-bg: {card_bg};
    --card-border: {card_border};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background-color: var(--bg);
    color: var(--text);
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 40px 20px;
}}

.header {{
    text-align: center;
    margin-bottom: 30px;
    max-width: 800px;
}}

.header h1 {{
    font-size: 2.5rem;
    margin-bottom: 10px;
}}

.header p {{
    opacity: 0.8;
    line-height: 1.5;
}}

/* Interactive container to demonstrate responsiveness */
.resize-demo-wrapper {{
    width: 100%;
    max-width: var(--width);
    min-height: var(--height);
    border: 2px dashed var(--accent);
    padding: 30px;
    border-radius: 12px;
    /* Allows user to drag to resize container manually */
    resize: horizontal;
    overflow: hidden;
    position: relative;
}}

.resize-demo-wrapper::after {{
    content: "↔ Drag to resize";
    position: absolute;
    bottom: 5px;
    right: 20px;
    font-size: 0.8rem;
    color: var(--accent);
    opacity: 0.7;
    pointer-events: none;
}}

/* === CORE SKILL PATTERN === */
.grid-container {{
    display: grid;
    /* 
      1. auto-fit: place as many columns as possible
      2. minmax(300px, 1fr): columns must be at least 300px. 
         If there's extra space, stretch them equally (1fr) 
    */
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 20px;
    justify-content: center;
}}

/* Card Styling for visualization */
.card {{
    background-color: var(--card-bg);
    border: var(--card-border);
    border-radius: 10px;
    padding: 30px 25px;
    text-align: center;
    display: flex;
    flex-direction: column;
    gap: 15px;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}}

.card:hover {{
    transform: translateY(-4px);
    box-shadow: 0 10px 20px rgba(0, 0, 0, 0.15);
}}

.card h2 {{
    font-size: 1.25rem;
}}

.card p {{
    font-size: 0.95rem;
    opacity: 0.85;
    line-height: 1.5;
}}
"""

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
    <div class="header">
        <h1>{title_text}</h1>
        <p>{body_text}</p>
    </div>

    <!-- Wrapper is resizable to demonstrate layout adjustments without changing window size -->
    <div class="resize-demo-wrapper">
        <div class="grid-container" id="grid">
            <!-- Cards injected via JS for brevity -->
        </div>
    </div>

    <script src="script.js"></script>
</body>
</html>"""

    js = f"""// Injecting cards dynamically to keep HTML clean
document.addEventListener('DOMContentLoaded', () => {{
    const gridContainer = document.getElementById('grid');
    const cardCount = 6;

    const dummyText = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Distinctio placeat iure aliquid eaque sed aliquam dicta maiores cupiditate earum quasi.";

    for (let i = 1; i <= cardCount; i++) {{
        const card = document.createElement('div');
        card.className = 'card';
        card.innerHTML = `
            <h2>Lorem Ipsum ${{i}}</h2>
            <p>${{dummyText}}</p>
        `;
        gridContainer.appendChild(card);
    }}
}});
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
