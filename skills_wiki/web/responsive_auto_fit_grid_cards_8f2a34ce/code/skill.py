def create_component(
    output_dir: str,
    title_text: str = "This is Responsive!",
    body_text: str = "Drag the bottom-right corner of the container below to see the grid automatically reflow and resize the cards.",
    color_scheme: str = "dark",
    accent_color: str = "#4a90e2",
    width_px: int = 1100,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Responsive Auto-Fit Grid.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Derived colors based on color_scheme
    if color_scheme == "dark":
        bg_color = "rgb(13, 13, 20)"
        card_bg = "#222429"
        card_border = "rgb(75, 82, 92)"
        text_color = "#ffffff"
        text_muted = "#a0aab8"
    else:
        bg_color = "#f4f5f7"
        card_bg = "#ffffff"
        card_border = "#e2e8f0"
        text_color = "#1e293b"
        text_muted = "#64748b"

    # HTML content
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Responsive Auto-Fit Grid</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="page-wrapper">
        <header class="header">
            <h1 class="title">{title_text}</h1>
            <p class="body-text">{body_text}</p>
        </header>

        <!-- The wrapper has resize: horizontal to demonstrate the effect -->
        <div class="demo-wrapper">
            <div class="grid-container" id="grid">
                <!-- Cards will be injected here via JS to keep HTML clean -->
            </div>
        </div>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # CSS content
    css = f"""/* Base Reset */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg-color: {bg_color};
    --card-bg: {card_bg};
    --card-border: {card_border};
    --text-color: {text_color};
    --text-muted: {text_muted};
    --accent: {accent_color};
    --default-width: {width_px}px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background-color: var(--bg-color);
    color: var(--text-color);
    min-height: 100vh;
    padding: 40px 20px;
    display: flex;
    justify-content: center;
}}

.page-wrapper {{
    width: 100%;
    max-width: 1400px;
    display: flex;
    flex-direction: column;
    align-items: center;
}}

.header {{
    text-align: center;
    margin-bottom: 40px;
}}

.title {{
    font-size: 2.5rem;
    font-weight: 700;
    margin-bottom: 10px;
}}

.body-text {{
    color: var(--text-muted);
    font-size: 1.1rem;
    max-width: 600px;
    margin: 0 auto;
}}

/* Interactive Demo Wrapper */
.demo-wrapper {{
    width: 100%;
    max-width: var(--default-width);
    /* Adding resize to allow manual testing of the responsive grid */
    resize: horizontal;
    overflow: hidden;
    border: 2px dashed var(--card-border);
    border-radius: 16px;
    padding: 30px;
    background-color: rgba(0,0,0,0.1);
    box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    min-width: 340px; /* Minimum width to show at least one card */
}}

/* === THE CORE GRID SKILL === */
.grid-container {{
    display: grid;
    /* This is the magic responsive line from the tutorial */
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 15px;
    justify-content: center;
}}

.card {{
    background-color: var(--card-bg);
    border: 1px solid var(--card-border);
    border-radius: 10px;
    padding: 2em;
    text-align: center;
    transition: transform 0.2s ease, border-color 0.2s ease;
}}

.card:hover {{
    transform: translateY(-2px);
    border-color: var(--accent);
}}

.card h2 {{
    font-size: 1.5rem;
    margin-bottom: 12px;
    font-weight: 600;
}}

.card p {{
    font-size: 0.95rem;
    line-height: 1.6;
    color: var(--text-muted);
}}
"""

    # JS content
    js = f"""document.addEventListener('DOMContentLoaded', () => {{
    const gridContainer = document.getElementById('grid');
    
    // Data for generating cards (simulating a CMS or Database)
    const cardsData = [
        {{ title: "Lorem Ipsum", content: "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Distinctio placeat iure aliquid eaque sed aliquam dicta maiores cupiditate earum quasi." }},
        {{ title: "Lorem Ipsum", content: "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Distinctio placeat iure aliquid eaque sed aliquam dicta maiores cupiditate earum quasi." }},
        {{ title: "Lorem Ipsum", content: "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Distinctio placeat iure aliquid eaque sed aliquam dicta maiores cupiditate earum quasi." }},
        {{ title: "Lorem Ipsum", content: "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Distinctio placeat iure aliquid eaque sed aliquam dicta maiores cupiditate earum quasi." }},
        {{ title: "Lorem Ipsum", content: "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Distinctio placeat iure aliquid eaque sed aliquam dicta maiores cupiditate earum quasi." }},
        {{ title: "Lorem Ipsum", content: "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Distinctio placeat iure aliquid eaque sed aliquam dicta maiores cupiditate earum quasi." }}
    ];

    // Inject cards into the grid
    cardsData.forEach(card => {{
        const cardEl = document.createElement('div');
        cardEl.className = 'card';
        cardEl.innerHTML = `
            <h2>${{card.title}}</h2>
            <p>${{card.content}}</p>
        `;
        gridContainer.appendChild(cardEl);
    }});
}});
"""

    # Write files
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
