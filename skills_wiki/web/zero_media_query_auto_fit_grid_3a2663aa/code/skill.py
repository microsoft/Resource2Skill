def create_component(
    output_dir: str,
    title_text: str = "Zero-Media-Query Grid",
    body_text: str = "Drag the bottom-right corner of the dashed container to resize it. Notice how the grid cards automatically wrap, stretch, and reflow without a single CSS media query.",
    color_scheme: str = "dark",
    accent_color: str = "#E91E63",
    width_px: int = 1000,
    height_px: int = 600,
    **kwargs,
) -> dict:
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Theme derivation
    if color_scheme == "dark":
        bg_color = "#0B0C10"
        text_color = "#F0F0F0"
        text_muted = "#A0A5B0"
        surface_color = "#1F2833"
        border_color = "rgba(255, 255, 255, 0.1)"
        dashed_border = "rgba(255, 255, 255, 0.2)"
        accent_light = f"{accent_color}1A" # ~10% opacity hex
    else:
        bg_color = "#F8F9FA"
        text_color = "#111111"
        text_muted = "#666666"
        surface_color = "#FFFFFF"
        border_color = "rgba(0, 0, 0, 0.08)"
        dashed_border = "rgba(0, 0, 0, 0.2)"
        accent_light = f"{accent_color}1A"

    # --- CSS ---
    css = f"""/* Zero-Media-Query Auto-Fit Grid */
:root {{
    --bg: {bg_color};
    --text: {text_color};
    --text-muted: {text_muted};
    --surface: {surface_color};
    --border: {border_color};
    --dashed: {dashed_border};
    --accent: {accent_color};
    --accent-light: {accent_light};
    --width: {width_px}px;
    --min-height: {height_px}px;
}}

* {{
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background-color: var(--bg);
    color: var(--text);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 2rem;
}}

.page-layout {{
    width: 100%;
    max-width: var(--width);
    display: flex;
    flex-direction: column;
    gap: 2rem;
}}

.header-section {{
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
}}

.title {{
    font-size: 2.5rem;
    font-weight: 700;
    letter-spacing: -0.02em;
}}

.body-text {{
    font-size: 1.1rem;
    color: var(--text-muted);
    line-height: 1.5;
    max-width: 600px;
}}

.controls {{
    margin-top: 1rem;
}}

.btn {{
    background-color: var(--accent);
    color: #ffffff;
    border: none;
    padding: 0.75rem 1.5rem;
    border-radius: 8px;
    font-size: 0.95rem;
    font-weight: 600;
    cursor: pointer;
    transition: filter 0.2s ease, transform 0.1s ease;
    box-shadow: 0 4px 12px var(--accent-light);
}}

.btn:hover {{
    filter: brightness(1.15);
}}

.btn:active {{
    transform: scale(0.97);
}}

/* === Core Resizable Wrapper === */
.resize-wrapper {{
    width: 100%;
    min-height: 400px;
    min-width: 280px;
    max-width: 100%;
    resize: horizontal;
    overflow: hidden;
    border: 2px dashed var(--dashed);
    border-radius: 16px;
    padding: 2rem;
    position: relative;
    background: linear-gradient(135deg, rgba(0,0,0,0.02) 0%, transparent 100%);
}}

.resize-hint {{
    position: absolute;
    bottom: 8px;
    right: 8px;
    font-size: 0.75rem;
    color: var(--text-muted);
    pointer-events: none;
    user-select: none;
    font-weight: 500;
}}

/* === The Grid Magic === */
.grid-container {{
    display: grid;
    /* This single line eliminates the need for media queries */
    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    gap: 1.5rem;
}}

/* === Grid Items === */
.grid-item {{
    background-color: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    min-height: 140px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 2.5rem;
    font-weight: 800;
    color: var(--text-muted);
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    cursor: default;
}}

.grid-item:hover {{
    transform: translateY(-6px);
    box-shadow: 0 12px 24px rgba(0, 0, 0, 0.1);
    border-color: var(--accent);
    color: var(--accent);
    background-color: var(--accent-light);
}}

/* Animation for dynamically added items */
@keyframes popIn {{
    0% {{ opacity: 0; transform: scale(0.8) translateY(10px); }}
    100% {{ opacity: 1; transform: scale(1) translateY(0); }}
}}

.grid-item.animate-in {{
    animation: popIn 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards;
}}
"""

    # --- HTML ---
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <main class="page-layout">
        <header class="header-section">
            <h1 class="title">{title_text}</h1>
            <p class="body-text">{body_text}</p>
            <div class="controls">
                <button id="add-btn" class="btn">+ Add Grid Item</button>
            </div>
        </header>

        <div class="resize-wrapper">
            <div class="grid-container" id="grid">
                <div class="grid-item">1</div>
                <div class="grid-item">2</div>
                <div class="grid-item">3</div>
                <div class="grid-item">4</div>
                <div class="grid-item">5</div>
                <div class="grid-item">6</div>
            </div>
            <div class="resize-hint">↘ Drag corner to resize</div>
        </div>
    </main>
    <script src="script.js"></script>
</body>
</html>"""

    # --- JavaScript ---
    js = """document.addEventListener('DOMContentLoaded', () => {
    const grid = document.getElementById('grid');
    const addBtn = document.getElementById('add-btn');
    
    // Track current number of items
    let itemCount = document.querySelectorAll('.grid-item').length;

    addBtn.addEventListener('click', () => {
        itemCount++;
        
        // Create new grid item
        const newItem = document.createElement('div');
        newItem.className = 'grid-item animate-in';
        newItem.textContent = itemCount;
        
        // Append to grid container
        // CSS Grid implicit tracking will automatically place it
        grid.appendChild(newItem);
        
        // Remove animation class after it plays to allow hover effects to run smoothly
        setTimeout(() => {
            newItem.classList.remove('animate-in');
        }, 400);
    });
});"""

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
