def create_component(
    output_dir: str,
    title_text: str = "Latest Collections",
    body_text: str = "Explore our responsive grid-stacked gallery. Resize the window to see the magic.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#6366f1",     # CSS hex color for accent
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Responsive Grid-Stacked Card Gallery effect.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Derive theme colors
    if color_scheme == "dark":
        bg_color = "#0f172a"
        text_color = "#f8fafc"
        subtext_color = "#94a3b8"
    else:
        bg_color = "#f8fafc"
        text_color = "#0f172a"
        subtext_color = "#64748b"

    # Generate 6 mock cards
    cards_html = ""
    for i in range(1, 7):
        cards_html += f"""
            <article class="grid-card">
                <img src="https://picsum.photos/seed/grid{i*12}/600/800" alt="Gallery Image {i}" class="card-bg">
                <div class="card-overlay"></div>
                <div class="card-content">
                    <span class="card-badge">Category {i}</span>
                    <h2 class="card-title">Immersive Experience {i}</h2>
                    <p class="card-desc">Seamlessly layered using CSS Grid stacking. No absolute positioning required.</p>
                    <a href="#" class="card-btn">Explore Concept</a>
                </div>
            </article>"""

    # === CSS ===
    css = f"""/* Responsive Grid-Stacked Card Gallery */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --text: {text_color};
    --subtext: {subtext_color};
    --accent: {accent_color};
    --card-min-width: 320px;
}}

body {{
    font-family: 'Inter', system-ui, sans-serif;
    background: var(--bg);
    color: var(--text);
    min-height: 100vh;
    padding: 3rem 1.5rem;
    display: flex;
    flex-direction: column;
    align-items: center;
}}

/* Header Styles */
.header {{
    text-align: center;
    margin-bottom: 3rem;
    max-width: 600px;
}}

.header h1 {{
    font-size: 2.5rem;
    font-weight: 700;
    margin-bottom: 1rem;
    letter-spacing: -0.02em;
}}

.header p {{
    color: var(--subtext);
    line-height: 1.6;
    font-size: 1.1rem;
}}

/* Macro Layout: Auto-wrapping Grid Container */
.gallery-container {{
    display: grid;
    /* The magic line: fluidly adds/removes columns based on available width */
    grid-template-columns: repeat(auto-fit, minmax(var(--card-min-width), 1fr));
    gap: 2rem;
    width: 100%;
    max-width: {width_px}px;
}}

/* Micro Layout: 1x1 Grid Stacking */
.grid-card {{
    display: grid;
    grid-template-areas: "stack"; /* Create a single named cell */
    border-radius: 16px;
    overflow: hidden;
    min-height: 420px;
    cursor: pointer;
    box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1), 0 8px 10px -6px rgba(0, 0, 0, 0.1);
    transition: transform 0.4s cubic-bezier(0.16, 1, 0.3, 1), box-shadow 0.4s ease;
}}

.grid-card:hover {{
    transform: translateY(-8px);
    box-shadow: 0 20px 35px -5px rgba(0, 0, 0, 0.2), 0 10px 15px -6px rgba(0, 0, 0, 0.1);
}}

/* Stack Layer 1: Background Image */
.card-bg {{
    grid-area: stack;
    width: 100%;
    height: 100%;
    object-fit: cover;
    z-index: 1;
    transition: transform 0.6s cubic-bezier(0.16, 1, 0.3, 1);
}}

.grid-card:hover .card-bg {{
    transform: scale(1.06);
}}

/* Stack Layer 2: Gradient Overlay for readability */
.card-overlay {{
    grid-area: stack;
    background: linear-gradient(
        to bottom,
        rgba(0, 0, 0, 0) 20%,
        rgba(0, 0, 0, 0.4) 60%,
        rgba(0, 0, 0, 0.9) 100%
    );
    z-index: 2;
    pointer-events: none;
}}

/* Stack Layer 3: Content Container */
.card-content {{
    grid-area: stack;
    z-index: 3;
    /* Grid/Flex alignments to push content to bottom */
    display: flex;
    flex-direction: column;
    justify-content: flex-end;
    align-items: flex-start;
    padding: 2.5rem 2rem;
    color: #ffffff; /* Explicitly white due to dark overlay */
}}

.card-badge {{
    background: var(--accent);
    color: white;
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    font-weight: 700;
    padding: 0.35rem 0.75rem;
    border-radius: 100px;
    margin-bottom: 1rem;
}}

.card-title {{
    font-size: 1.5rem;
    font-weight: 600;
    line-height: 1.2;
    margin-bottom: 0.75rem;
}}

.card-desc {{
    font-size: 0.95rem;
    line-height: 1.5;
    color: rgba(255, 255, 255, 0.8);
    margin-bottom: 1.5rem;
}}

.card-btn {{
    display: inline-block;
    color: #ffffff;
    text-decoration: none;
    font-size: 0.95rem;
    font-weight: 500;
    padding-bottom: 0.25rem;
    border-bottom: 2px solid var(--accent);
    transition: color 0.3s ease, border-color 0.3s ease;
}}

.card-btn:hover {{
    color: var(--accent);
}}
"""

    # === HTML ===
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text}</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <header class="header">
        <h1>{title_text}</h1>
        <p>{body_text}</p>
    </header>

    <main class="gallery-container">
        {cards_html}
    </main>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Responsive Grid-Stacked Card Gallery
// The core layout logic is driven entirely by CSS Grid.
// JS is included here for extensibility (e.g., dynamically fetching more cards or adding scroll animations).

document.addEventListener('DOMContentLoaded', () => {{
    console.log('Grid gallery initialized. Try resizing the window to see the auto-wrapping behavior.');
    
    // Example: Optional smooth entrance animation for cards
    const cards = document.querySelectorAll('.grid-card');
    cards.forEach((card, index) => {{
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        card.style.transition = 'opacity 0.6s ease, transform 0.6s ease, box-shadow 0.4s ease';
        
        setTimeout(() => {{
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
            
            // Remove transform transition after entrance to not conflict with hover effect
            setTimeout(() => {{
                card.style.transition = 'transform 0.4s cubic-bezier(0.16, 1, 0.3, 1), box-shadow 0.4s ease';
            }}, 600);
        }}, 100 * index);
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
