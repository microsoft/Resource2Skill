def create_component(
    output_dir: str,
    title_text: str = "Latest Arrivals",
    body_text: str = "Explore our responsive grid layout adjusting automatically to your screen size.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#6366f1",     # CSS hex color for accent (e.g., Indigo)
    width_px: int = 1400,
    height_px: int = 900,
    card_count: int = 10,              # Number of items to generate
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Responsive Auto-Fit Grid Gallery visual effect.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors ===
    if color_scheme == "dark":
        bg_color = "#0f172a"
        text_color = "#f8fafc"
        muted_text = "#94a3b8"
        surface_color = "#1e293b"
        border_color = "rgba(255, 255, 255, 0.1)"
        shadow = "0 10px 15px -3px rgba(0, 0, 0, 0.5)"
        hover_shadow = "0 20px 25px -5px rgba(0, 0, 0, 0.7)"
    else:
        bg_color = "#f8fafc"
        text_color = "#0f172a"
        muted_text = "#64748b"
        surface_color = "#ffffff"
        border_color = "rgba(0, 0, 0, 0.05)"
        shadow = "0 4px 6px -1px rgba(0, 0, 0, 0.05)"
        hover_shadow = "0 10px 15px -3px rgba(0, 0, 0, 0.1)"

    # === CSS ===
    css = f"""/* Responsive Auto-Fit Grid Gallery */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --text: {text_color};
    --muted: {muted_text};
    --accent: {accent_color};
    --surface: {surface_color};
    --border: {border_color};
    --shadow: {shadow};
    --hover-shadow: {hover_shadow};
    --min-card-width: 280px; 
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background: var(--bg);
    color: var(--text);
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 40px 20px;
}}

.header {{
    text-align: center;
    max-width: 600px;
    margin-bottom: 3rem;
}}

.title {{
    font-size: 2.5rem;
    font-weight: 700;
    letter-spacing: -0.025em;
    margin-bottom: 1rem;
}}

.body-text {{
    color: var(--muted);
    font-size: 1.125rem;
    line-height: 1.6;
}}

/* THE MAGIC FORMULA */
.grid-container {{
    display: grid;
    /* This single line creates a fully responsive grid without media queries */
    grid-template-columns: repeat(auto-fit, minmax(var(--min-card-width), 1fr));
    gap: 24px;
    width: 100%;
    max-width: {width_px}px;
}}

/* Card Styling */
.card {{
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 16px;
    overflow: hidden;
    box-shadow: var(--shadow);
    transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1), box-shadow 0.3s ease;
    display: flex;
    flex-direction: column;
}}

.card:hover {{
    transform: translateY(-6px);
    box-shadow: var(--hover-shadow);
    border-color: var(--accent);
}}

.card-image-placeholder {{
    height: 200px;
    background: linear-gradient(135deg, var(--border), transparent);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 3rem;
    color: var(--border);
}}

.card-content {{
    padding: 20px;
    display: flex;
    flex-direction: column;
    flex-grow: 1;
}}

.card-title {{
    font-size: 1.25rem;
    font-weight: 600;
    margin-bottom: 8px;
}}

.card-subtitle {{
    color: var(--muted);
    font-size: 0.9rem;
    margin-bottom: 20px;
    flex-grow: 1;
}}

.card-footer {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: auto;
}}

.card-price {{
    font-weight: 700;
    font-size: 1.125rem;
    color: var(--accent);
}}

.btn {{
    background: var(--accent);
    color: #ffffff;
    border: none;
    padding: 8px 16px;
    border-radius: 8px;
    font-weight: 500;
    cursor: pointer;
    transition: filter 0.2s ease;
}}

.btn:hover {{
    filter: brightness(1.1);
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
    <header class="header">
        <h1 class="title">{title_text}</h1>
        <p class="body-text">{body_text}</p>
    </header>

    <!-- The Grid Container -->
    <main class="grid-container" id="grid">
        <!-- Cards will be injected here via JavaScript -->
    </main>

    <script>
        // Pass Python variables to JavaScript safely
        const CARD_COUNT = {card_count};
    </script>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Responsive Auto-Fit Grid Gallery - Population Logic
document.addEventListener('DOMContentLoaded', () => {{
    const grid = document.getElementById('grid');
    
    // Sample data generation to demonstrate the grid layout
    const generateCards = (count) => {{
        for (let i = 1; i <= count; i++) {{
            const card = document.createElement('article');
            card.className = 'card';
            
            // Using string concatenation to prevent f-string bracket issues
            card.innerHTML = 
                '<div class="card-image-placeholder">❖</div>' +
                '<div class="card-content">' +
                    '<h2 class="card-title">Product Item ' + i + '</h2>' +
                    '<p class="card-subtitle">High-quality component designed to seamlessly adapt to any viewport.</p>' +
                    '<div class="card-footer">' +
                        '<span class="card-price">$' + (19.99 + i * 5).toFixed(2) + '</span>' +
                        '<button class="btn">View</button>' +
                    '</div>' +
                '</div>';
                
            grid.appendChild(card);
        }}
    }};

    // CARD_COUNT is defined in HTML script tag
    generateCards(CARD_COUNT || 8);
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
