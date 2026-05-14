def create_component(
    output_dir: str,
    title_text: str = "Auto-Responsive Grid",
    body_text: str = "Drag the bottom-right corner of this container to see CSS Grid auto-fit and minmax() seamlessly wrap and resize items without a single media query.",
    color_scheme: str = "dark",
    accent_color: str = "#3b82f6",
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the media-query-free CSS Grid layout.
    
    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors ===
    if color_scheme == "dark":
        bg_color = "#050505"
        surface_bg = "#121212"
        card_bg = "#1a1c23"
        text_color = "#f3f4f6"
        text_muted = "rgba(255, 255, 255, 0.65)"
        border_color = "rgba(255, 255, 255, 0.1)"
    else:
        bg_color = "#e5e7eb"
        surface_bg = "#f9fafb"
        card_bg = "#ffffff"
        text_color = "#111827"
        text_muted = "rgba(0, 0, 0, 0.65)"
        border_color = "rgba(0, 0, 0, 0.1)"

    # === CSS ===
    css = f"""/* Auto-Responsive Grid Component */
:root {{
    --bg-page: {bg_color};
    --bg-surface: {surface_bg};
    --bg-card: {card_bg};
    --text-main: {text_color};
    --text-muted: {text_muted};
    --border: {border_color};
    --accent: {accent_color};
    --target-width: {width_px}px;
    --target-height: {height_px}px;
}}

*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background: var(--bg-page);
    color: var(--text-main);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 2rem;
}}

/* Interactive Resizable Demo Container */
.demo-window {{
    width: 100%;
    max-width: var(--target-width);
    height: var(--target-height);
    background: var(--bg-surface);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 2.5rem;
    overflow-y: auto;
    overflow-x: hidden;
    /* Enable horizontal resize so users can test the grid */
    resize: horizontal; 
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
    display: flex;
    flex-direction: column;
    gap: 2rem;
}}

/* Header Typography */
header h1 {{
    font-size: 2rem;
    font-weight: 700;
    margin-bottom: 0.5rem;
    letter-spacing: -0.025em;
}}

header p {{
    color: var(--text-muted);
    line-height: 1.6;
    max-width: 600px;
}}

/* 
 * THE CORE SKILL: Media-Query-Free CSS Grid 
 * repeat(auto-fit) - Creates as many columns as fit, drops empty ones.
 * minmax(min(100%, 280px), 1fr) - Minimum 280px (or 100% on tiny screens), expands equally (1fr).
 */
.grid-container {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(min(100%, 280px), 1fr));
    gap: 1.5rem;
    width: 100%;
}}

/* Card Styles */
.card {{
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.5rem;
    display: flex;
    flex-direction: column;
    gap: 1rem;
    transition: transform 0.2s cubic-bezier(0.4, 0, 0.2, 1), 
                border-color 0.2s ease,
                box-shadow 0.2s ease;
}}

.card:hover {{
    transform: translateY(-4px);
    border-color: var(--accent);
    box-shadow: 0 10px 20px -10px rgba(0, 0, 0, 0.3);
}}

.card-header {{
    display: flex;
    align-items: center;
    gap: 0.75rem;
}}

.card-icon {{
    width: 32px;
    height: 32px;
    border-radius: 8px;
    background: color-mix(in srgb, var(--accent) 15%, transparent);
    color: var(--accent);
    display: flex;
    align-items: center;
    justify-content: center;
}}

.card h2 {{
    font-size: 1.125rem;
    font-weight: 600;
}}

.card p {{
    color: var(--text-muted);
    font-size: 0.925rem;
    line-height: 1.6;
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
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="demo-window" title="Drag the bottom right corner to resize and test grid fluidity!">
        <header>
            <h1>{title_text}</h1>
            <p>{body_text}</p>
        </header>
        
        <main class="grid-container" id="grid">
            <!-- Cards will be dynamically injected by script.js -->
        </main>
    </div>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Dynamic Data Injection to populate the grid
document.addEventListener('DOMContentLoaded', () => {{
    const grid = document.getElementById('grid');
    
    const cardData = [
        {{ title: "Flexbox Pitfalls", desc: "Flexbox with flex-grow leaves you with wildly stretching orphan items on the last row if they don't perfectly fill it." }},
        {{ title: "The Grid Solution", desc: "CSS Grid with auto-fit and minmax() locks elements into uniform column tracks natively." }},
        {{ title: "Intrinsic Sizing", desc: "This technique relies on the content's intrinsic size rather than forcing layout changes via explicit breakpoints." }},
        {{ title: "Fractional Units", desc: "Minimum width is maintained (e.g., 280px). Any leftover horizontal space is distributed evenly via the 1fr unit." }},
        {{ title: "Auto-Fit Magic", desc: "Empty tracks are collapsed by auto-fit, but populated tracks strictly dictate the width of the entire column." }},
        {{ title: "Mobile Safeguard", desc: "Using min(100%, 280px) guarantees that if a screen is 250px wide, the card won't cause horizontal scrolling." }},
        {{ title: "Try Resizing", desc: "Drag the bottom right corner of this modal inward. Watch the columns elegantly drop from 3 to 2 to 1." }},
        {{ title: "Highly Reusable", desc: "Because it lacks media queries, this grid adapts based on its parent container, making it a perfect modular component." }}
    ];

    // Create SVG icon
    const svgIcon = `<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="7" height="7"></rect><rect x="14" y="3" width="7" height="7"></rect><rect x="14" y="14" width="7" height="7"></rect><rect x="3" y="14" width="7" height="7"></rect></svg>`;

    cardData.forEach((data, index) => {{
        const card = document.createElement('div');
        card.className = 'card';
        card.innerHTML = `
            <div class="card-header">
                <div class="card-icon">${{svgIcon}}</div>
                <h2>${{data.title}}</h2>
            </div>
            <p>${{data.desc}}</p>
        `;
        grid.appendChild(card);
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
