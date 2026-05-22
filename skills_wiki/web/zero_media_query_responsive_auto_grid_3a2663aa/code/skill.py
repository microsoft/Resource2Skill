def create_component(
    output_dir: str,
    title_text: str = "Zero-Media-Query Grid",
    body_text: str = "Drag the bottom-right corner of this container to resize it. Watch the grid automatically calculate columns and reflow without any CSS breakpoints.",
    color_scheme: str = "dark",        
    accent_color: str = "#e11d48",     
    width_px: int = 1000,
    height_px: int = 700,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Zero-Media-Query Auto-Grid visual effect.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors ===
    if color_scheme == "dark":
        app_bg = "#000000"
        container_bg = "#0f172a"
        text_color = "#f8fafc"
        border_color = "rgba(255, 255, 255, 0.1)"
    else:
        app_bg = "#e2e8f0"
        container_bg = "#ffffff"
        text_color = "#0f172a"
        border_color = "rgba(0, 0, 0, 0.1)"

    # === CSS ===
    css = f"""/* Zero-Media-Query Auto-Grid — generated component */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --app-bg: {app_bg};
    --container-bg: {container_bg};
    --text: {text_color};
    --accent: {accent_color};
    --border: {border_color};
    --width: {width_px}px;
    --height: {height_px}px;
    --min-card-width: 150px;
}}

body {{
    font-family: 'Roboto', system-ui, -apple-system, sans-serif;
    background: var(--app-bg);
    color: var(--text);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 2rem;
}}

/* Interactive container simulating a resizable browser window */
.resizable-container {{
    width: 100%;
    max-width: var(--width);
    height: var(--height);
    background: var(--container-bg);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 2.5rem;
    overflow-y: auto;
    overflow-x: hidden;
    resize: horizontal; /* The magic allowing real-time testing */
    min-width: 320px;
    max-width: 100%;
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
    display: flex;
    flex-direction: column;
    gap: 2.5rem;
}}

/* Style the native resizer handle */
.resizable-container::-webkit-resizer {{
    background-color: var(--accent);
    border-radius: 50%;
    border: 3px solid var(--container-bg);
}}

.header {{
    text-align: center;
}}

.title {{
    font-size: 2.2rem;
    font-weight: 700;
    margin-bottom: 0.75rem;
    letter-spacing: -0.025em;
}}

.body-text {{
    font-size: 1rem;
    opacity: 0.7;
    max-width: 500px;
    margin: 0 auto;
    line-height: 1.6;
}}

/* THE CORE SKILL: Auto-fit grid */
.auto-grid {{
    display: grid;
    /* This single line dictates all responsive behavior */
    grid-template-columns: repeat(auto-fit, minmax(var(--min-card-width), 1fr));
    gap: 1.5rem;
    width: 100%;
}}

/* Card Styling */
.grid-item {{
    background: var(--accent);
    border-radius: 12px;
    min-height: 160px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 3rem;
    font-weight: 700;
    color: #ffffff;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    cursor: pointer;
    
    /* Animation initial state */
    opacity: 0;
    transform: translateY(30px) scale(0.95);
    
    /* We handle the transition dynamically in JS to allow hover effects post-load */
}}

/* Entrance state */
.grid-item.loaded {{
    opacity: 1;
    transform: translateY(0) scale(1);
}}

/* Hover interaction */
.grid-item:hover {{
    transform: translateY(-8px) scale(1.03) !important;
    box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.3), 0 10px 10px -5px rgba(0, 0, 0, 0.1);
    filter: brightness(1.15);
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
    <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="resizable-container">
        <header class="header">
            <h1 class="title">{title_text}</h1>
            <p class="body-text">{body_text}</p>
        </header>
        
        <main class="auto-grid" id="grid">
            <!-- Grid items injected by JS -->
        </main>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// [Skill Name] — Zero-Media-Query Grid Generation & Animation
document.addEventListener('DOMContentLoaded', () => {{
    const grid = document.getElementById('grid');
    const numItems = 15; // Number of items to demonstrate the flow
    
    // 1. Generate Grid Items dynamically
    const fragment = document.createDocumentFragment();
    for (let i = 1; i <= numItems; i++) {{
        const item = document.createElement('div');
        item.classList.add('grid-item');
        item.textContent = i;
        fragment.appendChild(item);
    }}
    grid.appendChild(fragment);
    
    // 2. Staggered Entrance Animation
    const items = document.querySelectorAll('.grid-item');
    items.forEach((item, index) => {{
        setTimeout(() => {{
            // Apply the transition property right before the class so it animates in
            item.style.transition = 'transform 0.5s cubic-bezier(0.34, 1.56, 0.64, 1), opacity 0.5s ease';
            
            // Trigger layout recalculation to ensure transition plays
            void item.offsetWidth; 
            
            item.classList.add('loaded');
            
            // After entrance animation finishes, swap to the hover transition profile
            setTimeout(() => {{
                item.style.transition = 'transform 0.25s cubic-bezier(0.2, 0, 0, 1), box-shadow 0.25s ease, filter 0.25s ease';
            }}, 500);
            
        }}, index * 60); // 60ms stagger per item
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
