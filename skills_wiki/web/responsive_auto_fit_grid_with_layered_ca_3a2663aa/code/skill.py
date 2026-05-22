def create_component(
    output_dir: str,
    title_text: str = "Fluid Auto-Fit Grid",
    body_text: str = "A fully responsive layout achieved with zero media queries, utilizing CSS Grid's auto-fit, minmax, and structural layering techniques.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#ec4899",     # CSS hex color for accent (pinkish by default)
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Responsive Auto-Fit Grid with Layered Cards.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Derive theme colors explicitly
    if color_scheme == "dark":
        body_bg = "#05070a"
        wrapper_bg = "#0b0f19"
        text_primary = "#f8fafc"
        text_secondary = "#94a3b8"
        surface_color = "rgba(255, 255, 255, 0.04)"
        border_color = "rgba(255, 255, 255, 0.08)"
        hover_border = accent_color
        shadow_color = "rgba(0, 0, 0, 0.4)"
        title_gradient = f"linear-gradient(to right, #ffffff, {accent_color})"
    else:
        body_bg = "#e2e8f0"
        wrapper_bg = "#f8fafc"
        text_primary = "#0f172a"
        text_secondary = "#475569"
        surface_color = "#ffffff"
        border_color = "#cbd5e1"
        hover_border = accent_color
        shadow_color = "rgba(0, 0, 0, 0.05)"
        title_gradient = f"linear-gradient(to right, #0f172a, {accent_color})"

    # === CSS ===
    css = f"""/* Responsive Auto-Fit Grid — Generated Component */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --body-bg: {body_bg};
    --wrapper-bg: {wrapper_bg};
    --text-primary: {text_primary};
    --text-secondary: {text_secondary};
    --surface-color: {surface_color};
    --border-color: {border_color};
    --hover-border: {hover_border};
    --shadow-color: {shadow_color};
    --accent: {accent_color};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background: var(--body-bg);
    color: var(--text-primary);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 2rem;
}}

.app-wrapper {{
    width: var(--width);
    max-width: 100vw;
    height: var(--height);
    max-height: 90vh;
    background: var(--wrapper-bg);
    border: 1px solid var(--border-color);
    border-radius: 24px;
    box-shadow: 0 25px 50px -12px var(--shadow-color);
    padding: 3rem;
    overflow-y: auto;
    display: flex;
    flex-direction: column;
}}

/* Custom scrollbar for the wrapper */
.app-wrapper::-webkit-scrollbar {{
    width: 8px;
}}
.app-wrapper::-webkit-scrollbar-track {{
    background: transparent;
}}
.app-wrapper::-webkit-scrollbar-thumb {{
    background: var(--border-color);
    border-radius: 4px;
}}

.page-header {{
    text-align: center;
    margin-bottom: 3rem;
}}

.title {{
    font-size: clamp(2rem, 4vw, 3rem);
    font-weight: 700;
    margin-bottom: 1rem;
    background: {title_gradient};
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    letter-spacing: -0.02em;
}}

.body-text {{
    color: var(--text-secondary);
    max-width: 600px;
    margin: 0 auto 2rem auto;
    line-height: 1.6;
    font-size: 1.05rem;
}}

.add-btn {{
    background: var(--accent);
    color: #ffffff;
    border: none;
    padding: 0.75rem 1.75rem;
    font-size: 1rem;
    font-weight: 600;
    border-radius: 8px;
    cursor: pointer;
    transition: transform 0.2s ease, filter 0.2s ease, box-shadow 0.2s ease;
    font-family: inherit;
    box-shadow: 0 4px 14px 0 rgba(0, 0, 0, 0.2);
}}

.add-btn:hover {{
    transform: translateY(-2px);
    filter: brightness(1.1);
    box-shadow: 0 6px 20px 0 rgba(0, 0, 0, 0.3);
}}

.add-btn:focus-visible {{
    outline: 2px solid var(--text-primary);
    outline-offset: 2px;
}}

/* 
 * 1. THE AUTO-FIT GRID TRICK 
 * Automatically wraps items and stretches them across remaining space without media queries.
 */
.grid-container {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 1.5rem;
    width: 100%;
    /* Dictates how tall newly added (implicit) rows should be */
    grid-auto-rows: minmax(180px, auto);
}}

/* 
 * 2. GRID AREA LAYERING
 * Using grid line coordinates to stack background, content, and badge along Z-axis
 */
.layered-card {{
    display: grid;
    grid-template-columns: 1fr;
    grid-template-rows: 1fr;
    border-radius: 16px;
    background: var(--surface-color);
    border: 1px solid var(--border-color);
    box-shadow: 0 4px 6px -1px var(--shadow-color);
    overflow: hidden;
    transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1), box-shadow 0.3s ease, border-color 0.3s ease;
}}

.layered-card:hover {{
    transform: translateY(-4px);
    box-shadow: 0 10px 15px -3px var(--shadow-color);
    border-color: var(--hover-border);
}}

/* Hero spans full width of available grid columns */
.layered-card.hero {{
    grid-column: 1 / -1;
}}

.card-bg-gradient {{
    grid-area: 1 / 1 / -1 / -1;
    background: radial-gradient(circle at top right, var(--accent) 0%, transparent 60%);
    opacity: 0.08;
    z-index: 1;
    transition: opacity 0.3s ease;
}}

.layered-card:hover .card-bg-gradient {{
    opacity: 0.18;
}}

.card-content {{
    grid-area: 1 / 1 / -1 / -1;
    z-index: 2;
    padding: 1.75rem;
    display: flex;
    flex-direction: column;
    justify-content: center;
}}

.card-content h3, .card-content h2 {{
    color: var(--text-primary);
    margin-bottom: 0.75rem;
    font-weight: 600;
}}

.card-content p {{
    color: var(--text-secondary);
    line-height: 1.6;
    font-size: 0.95rem;
}}

.card-badge {{
    grid-area: 1 / 1 / -1 / -1;
    z-index: 3;
    /* Grid Box Alignment Module */
    justify-self: end;
    align-self: start;
    margin: 1rem;
    padding: 0.25rem 0.75rem;
    border-radius: 9999px;
    background: var(--accent);
    color: #ffffff;
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    box-shadow: 0 2px 4px rgba(0,0,0,0.2);
}}

/* Animation for dynamically added grid items */
.new-card {{
    animation: slideUpFade 0.5s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}}

@keyframes slideUpFade {{
    from {{
        opacity: 0;
        transform: translateY(20px);
    }}
    to {{
        opacity: 1;
        transform: translateY(0);
    }}
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
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="app-wrapper">
        <header class="page-header">
            <h1 class="title">{title_text}</h1>
            <p class="body-text">{body_text}</p>
            <button id="add-card-btn" class="add-btn">Add Implicit Grid Item</button>
        </header>

        <main class="grid-container" id="grid-container">
            <!-- Hero Card -->
            <article class="layered-card hero">
                <div class="card-bg-gradient"></div>
                <div class="card-content">
                    <h2>Zero Media Queries</h2>
                    <p>This layout seamlessly reflows its columns using CSS Grid's <code>repeat(auto-fit, minmax(280px, 1fr))</code>. This specific card uses <code>grid-column: 1 / -1</code> to dynamically span all implicitly available column tracks, no matter screen size.</p>
                </div>
                <div class="card-badge">Hero Span</div>
            </article>

            <!-- Standard Cards -->
            <article class="layered-card">
                <div class="card-bg-gradient"></div>
                <div class="card-content">
                    <h3>Grid Layering</h3>
                    <p>Elements inside this card are stacked along the Z-axis without absolute positioning. By assigning them to the exact same grid area (<code>1 / 1 / -1 / -1</code>), they overlap naturally.</p>
                </div>
                <div class="card-badge">Concept</div>
            </article>

            <article class="layered-card">
                <div class="card-bg-gradient"></div>
                <div class="card-content">
                    <h3>Fractional Sizing</h3>
                    <p>Grid items calculate their width utilizing the <code>1fr</code> unit, meaning they absorb all remaining empty space evenly after satisfying the <code>280px</code> min-width requirement.</p>
                </div>
                <div class="card-badge">Scale</div>
            </article>

            <article class="layered-card">
                <div class="card-bg-gradient"></div>
                <div class="card-content">
                    <h3>Alignment Control</h3>
                    <p>The badges sitting in the top right corners are positioned using <code>justify-self: end</code> and <code>align-self: start</code>, showcasing Grid's highly precise box-alignment module.</p>
                </div>
                <div class="card-badge">Layout</div>
            </article>
        </main>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Responsive Auto-Fit Grid Behavior
document.addEventListener('DOMContentLoaded', () => {{
    const container = document.getElementById('grid-container');
    const addBtn = document.getElementById('add-card-btn');
    let dynamicCount = 0;

    addBtn.addEventListener('click', () => {{
        dynamicCount++;
        
        // Create new article element
        const card = document.createElement('article');
        card.className = 'layered-card new-card';
        
        // Define layered internal structure matching the grid technique
        card.innerHTML = `
            <div class="card-bg-gradient"></div>
            <div class="card-content">
                <h3>Implicit Track Added</h3>
                <p>Dynamically added Item #${dynamicCount}. Because it falls outside explicitly defined rows, CSS Grid automatically generates a new implicit row to hold it, styled by <code>grid-auto-rows</code>.</p>
            </div>
            <div class="card-badge">Dynamic</div>
        `;
        
        container.appendChild(card);
        
        // Auto-scroll the wrapper to show the newly added grid item
        const wrapper = document.querySelector('.app-wrapper');
        setTimeout(() => {{
            wrapper.scrollTo({{
                top: wrapper.scrollHeight,
                behavior: 'smooth'
            }});
        }}, 100);
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
