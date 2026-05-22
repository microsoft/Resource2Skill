def create_component(
    output_dir: str,
    title_text: str = "Responsive CSS Grid",
    body_text: str = "This grid automatically adjusts its columns based on available width without using media queries.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#00bfff",     # CSS hex color for accent
    width_px: int = 1200,              # Max width of the container
    height_px: int = 800,              # Min height for demo presentation
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Auto-Fit CSS Grid layout.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme ===
    if color_scheme == "dark":
        bg_color = "#0d0d14"          # Body background from tutorial
        surface_color = "#222429"     # Card background from tutorial
        text_color = "#ffffff"
        text_muted = "#a0aab2"
        border_color = "#4b525c"
    else:
        bg_color = "#f0f2f5"
        surface_color = "#ffffff"
        text_color = "#1a1a1a"
        text_muted = "#666666"
        border_color = "#e1e4e8"

    # === CSS ===
    css = f"""/* Responsive Auto-Fit CSS Grid */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --surface: {surface_color};
    --text: {text_color};
    --text-muted: {text_muted};
    --border: {border_color};
    --accent: {accent_color};
    --max-width: {width_px}px;
    --min-height: {height_px}px;
}}

body {{
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background-color: var(--bg);
    color: var(--text);
    min-height: var(--min-height);
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 40px 20px;
}}

.page-header {{
    text-align: center;
    margin-bottom: 40px;
    max-width: 800px;
}}

.page-header h1 {{
    font-size: 2.5rem;
    margin-bottom: 10px;
}}

.page-header p {{
    color: var(--text-muted);
    font-size: 1.1rem;
    line-height: 1.6;
}}

/* === The Core Grid Layout === */
.grid-container {{
    display: grid;
    /* 
      auto-fit: create as many columns as fit
      minmax(300px, 1fr): columns must be at least 300px, but grow to share remaining space
    */
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 20px; /* Space between cards */
    justify-content: center; /* Center items if max container width is reached */
    
    width: 100%;
    max-width: var(--max-width);
}}

/* === Card Styling === */
.card {{
    background-color: var(--surface);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 2.5em 2em;
    text-align: center;
    
    /* Interactive enhancements */
    transition: transform 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275), 
                border-color 0.3s ease,
                box-shadow 0.3s ease;
}}

.card:hover {{
    transform: translateY(-8px);
    border-color: var(--accent);
    box-shadow: 0 10px 20px rgba(0,0,0,0.2);
}}

.card h2 {{
    font-size: 1.4rem;
    margin-bottom: 15px;
    color: var(--text);
}}

.card p {{
    color: var(--text-muted);
    line-height: 1.5;
    font-size: 0.95rem;
}}
"""

    # === HTML ===
    # Escaping parameters
    import html as html_lib
    safe_title = html_lib.escape(title_text)
    safe_body = html_lib.escape(body_text)

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{safe_title}</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <header class="page-header">
        <h1>{safe_title}</h1>
        <p>{safe_body}</p>
    </header>

    <!-- The grid container -->
    <main class="grid-container" id="grid">
        <!-- Cards will be injected by JavaScript for demonstration purposes -->
    </main>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Generates dummy cards to demonstrate the grid layout
document.addEventListener('DOMContentLoaded', () => {{
    const gridContainer = document.getElementById('grid');
    const numCards = 8; // Number of cards to generate

    const dummyText = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Distinctio placeat iure aliquid eaque sed aliquam dicta maiores cupiditate earum quasi.";

    for (let i = 1; i <= numCards; i++) {{
        const card = document.createElement('div');
        card.className = 'card';
        
        const title = document.createElement('h2');
        title.textContent = `Lorem Ipsum ${{i}}`;
        
        const text = document.createElement('p');
        text.textContent = dummyText;
        
        card.appendChild(title);
        card.appendChild(text);
        gridContainer.appendChild(card);
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
