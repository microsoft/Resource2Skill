def create_component(
    output_dir: str,
    title_text: str = "Auto-Fit CSS Grid",
    body_text: str = "Drag the bottom-right corner of the dashed container to watch the grid fluidly recalculate columns.",
    color_scheme: str = "dark",
    accent_color: str = "#e91e63",
    width_px: int = 800,
    height_px: int = 500,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Responsive Auto-Fit Grid.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors ===
    if color_scheme == "dark":
        bg_color = "#0b0e14"
        container_bg = "#151b2b"
        text_color = "#f0f0f0"
        border_color = "rgba(255, 255, 255, 0.2)"
        shadow = "0 8px 16px rgba(0, 0, 0, 0.4)"
    else:
        bg_color = "#f0f2f5"
        container_bg = "#ffffff"
        text_color = "#1a1a2e"
        border_color = "rgba(0, 0, 0, 0.15)"
        shadow = "0 8px 16px rgba(0, 0, 0, 0.08)"

    # === CSS ===
    css = f"""/* Responsive Auto-Fit Grid */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --container-bg: {container_bg};
    --text: {text_color};
    --accent: {accent_color};
    --border: {border_color};
    --shadow: {shadow};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background: var(--bg);
    color: var(--text);
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 2rem;
}}

.header {{
    text-align: center;
    margin-bottom: 2rem;
    max-width: var(--width);
}}

.header h1 {{
    font-size: 2rem;
    margin-bottom: 0.5rem;
    font-weight: 700;
}}

.header p {{
    color: var(--text);
    opacity: 0.8;
    line-height: 1.5;
}}

/* The Resizable Demo Wrapper */
.resize-wrapper {{
    width: 100%;
    max-width: var(--width);
    height: var(--height);
    background: var(--container-bg);
    border: 2px dashed var(--border);
    border-radius: 12px;
    padding: 1.5rem;
    resize: both;
    overflow: auto;
    position: relative;
    box-shadow: var(--shadow);
    /* Smoothly animate width when not actively resizing */
    transition: box-shadow 0.3s ease;
}}

.resize-wrapper::-webkit-resizer {{
    background-color: var(--accent);
    border-radius: 50%;
}}

.resize-wrapper::after {{
    content: "Drag to resize \u21F2";
    position: absolute;
    bottom: 8px;
    right: 12px;
    font-size: 0.75rem;
    font-weight: 600;
    color: var(--accent);
    pointer-events: none;
    opacity: 0.7;
}}

/* --- THE CORE PATTERN --- */
.grid-container {{
    display: grid;
    /* 
       auto-fit: Creates as many columns as will fit in the container.
       minmax(120px, 1fr): Each column is at least 120px. 
       If there is leftover space, distribute it equally (1fr).
    */
    grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
    /* Automatically set the height of implicitly created rows */
    grid-auto-rows: 100px;
    gap: 16px;
    height: 100%;
}}

.grid-item {{
    background-color: var(--accent);
    color: #ffffff;
    border-radius: 8px;
    padding: 12px 16px;
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    justify-content: flex-start;
    font-family: 'Fira Code', monospace;
    font-size: 1.2rem;
    font-weight: bold;
    box-shadow: inset 0 0 0 1px rgba(255, 255, 255, 0.2);
    /* A subtle hover lift to make the UI feel tangible */
    transition: transform 0.2s cubic-bezier(0.4, 0, 0.2, 1), filter 0.2s ease;
    cursor: default;
}}

.grid-item:hover {{
    transform: translateY(-2px);
    filter: brightness(1.1);
}}

.item-index {{
    background: rgba(255, 255, 255, 0.2);
    padding: 2px 8px;
    border-radius: 4px;
    font-size: 0.8rem;
    margin-bottom: auto;
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
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&family=Fira+Code:wght@500&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="header">
        <h1>{title_text}</h1>
        <p>{body_text}</p>
    </div>

    <!-- The wrapper exists purely to allow easy resize testing on desktop -->
    <div class="resize-wrapper">
        <div class="grid-container" id="grid">
            <!-- Grid items injected by JS -->
        </div>
    </div>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Generate Grid Items Dynamically
document.addEventListener('DOMContentLoaded', () => {{
    const gridContainer = document.getElementById('grid');
    const itemCount = 12; // Number of items to demonstrate wrapping

    for (let i = 1; i <= itemCount; i++) {{
        const item = document.createElement('div');
        item.className = 'grid-item';
        
        const label = document.createElement('span');
        label.className = 'item-index';
        label.textContent = i;
        
        item.appendChild(label);
        gridContainer.appendChild(item);
    }}
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
