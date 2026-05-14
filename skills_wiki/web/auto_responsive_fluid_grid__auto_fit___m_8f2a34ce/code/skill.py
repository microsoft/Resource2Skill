def create_component(
    output_dir: str,
    title_text: str = "Auto-Responsive Grid",
    body_text: str = "Drag the handle in the bottom right to resize the container and watch the grid automatically adapt without a single media query.",
    color_scheme: str = "dark",
    accent_color: str = "#6366f1",
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    import os

    os.makedirs(output_dir, exist_ok=True)

    if color_scheme == "dark":
        bg_color = "#0f111a"
        text_color = "#f8f9fa"
        muted_text = "rgba(255, 255, 255, 0.6)"
        card_bg = "rgba(255, 255, 255, 0.04)"
        card_border = "rgba(255, 255, 255, 0.08)"
        card_hover_bg = "rgba(255, 255, 255, 0.08)"
    else:
        bg_color = "#f4f5f7"
        text_color = "#0f111a"
        muted_text = "rgba(0, 0, 0, 0.6)"
        card_bg = "#ffffff"
        card_border = "rgba(0, 0, 0, 0.08)"
        card_hover_bg = "#ffffff"

    css = f"""/* Auto-Responsive Grid Component */
:root {{
    --bg-color: {bg_color};
    --text-color: {text_color};
    --muted-text: {muted_text};
    --card-bg: {card_bg};
    --card-border: {card_border};
    --card-hover-bg: {card_hover_bg};
    --accent-color: {accent_color};
    --card-min-width: 280px;
}}

*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background-color: var(--bg-color);
    color: var(--text-color);
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 40px 20px;
}}

.header {{
    text-align: center;
    max-width: 600px;
    margin-bottom: 40px;
}}

.header h1 {{
    font-size: 2.5rem;
    font-weight: 700;
    margin-bottom: 12px;
    letter-spacing: -0.02em;
}}

.header p {{
    font-size: 1.1rem;
    color: var(--muted-text);
    line-height: 1.6;
}}

/* Resizable wrapper to demonstrate the fluid grid */
.demo-wrapper {{
    width: 100%;
    max-width: {width_px}px;
    /* Adding resize to allow manual testing of responsiveness */
    resize: horizontal;
    overflow: hidden;
    padding: 24px;
    border: 2px dashed var(--card-border);
    border-radius: 16px;
    background: rgba(0, 0, 0, 0.02);
}}

/* THE CORE SKILL: Auto-wrapping, auto-sizing Grid */
.grid-container {{
    display: grid;
    /* min(100%, 280px) ensures it doesn't break on < 280px screens */
    grid-template-columns: repeat(auto-fit, minmax(min(100%, var(--card-min-width)), 1fr));
    gap: 24px;
    justify-content: center;
}}

/* Card Styling */
.card {{
    background: var(--card-bg);
    border: 1px solid var(--card-border);
    border-radius: 12px;
    padding: 24px;
    display: flex;
    flex-direction: column;
    gap: 12px;
    transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1), 
                border-color 0.3s ease, 
                background-color 0.3s ease,
                box-shadow 0.3s ease;
    cursor: pointer;
}}

.card:hover {{
    transform: translateY(-6px);
    border-color: var(--accent-color);
    background: var(--card-hover-bg);
    box-shadow: 0 12px 24px rgba(0, 0, 0, 0.1);
}}

.card-icon {{
    width: 48px;
    height: 48px;
    border-radius: 10px;
    background: rgba(99, 102, 241, 0.1); /* fallback soft accent */
    color: var(--accent-color);
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 8px;
}}

.card-title {{
    font-size: 1.25rem;
    font-weight: 600;
}}

.card-text {{
    font-size: 0.95rem;
    color: var(--muted-text);
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
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="header">
        <h1>{title_text}</h1>
        <p>{body_text}</p>
    </div>

    <div class="demo-wrapper">
        <div class="grid-container" id="grid">
            <!-- Cards will be injected by JS -->
        </div>
    </div>

    <script src="script.js"></script>
</body>
</html>"""

    js = f"""// Generates dummy data to populate the responsive grid
document.addEventListener('DOMContentLoaded', () => {{
    const gridContainer = document.getElementById('grid');
    const cardCount = 8;

    const dummyText = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Praesent at eros sed dui pretium dapibus.";

    for (let i = 1; i <= cardCount; i++) {{
        const card = document.createElement('div');
        card.className = 'card';
        
        card.innerHTML = `
            <div class="card-icon">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <rect x="3" y="3" width="7" height="7"></rect>
                    <rect x="14" y="3" width="7" height="7"></rect>
                    <rect x="14" y="14" width="7" height="7"></rect>
                    <rect x="3" y="14" width="7" height="7"></rect>
                </svg>
            </div>
            <h2 class="card-title">Grid Item ${{i}}</h2>
            <p class="card-text">${{dummyText}}</p>
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
