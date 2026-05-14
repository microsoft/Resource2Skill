def create_component(
    output_dir: str,
    title_text: str = "Scroll-Driven Animations",
    body_text: str = "Scroll down to see the cards progressively reveal based on your viewport position.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#8b5cf6",     # CSS hex color for accent
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Scroll-Driven Viewport Reveal Cards.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors ===
    if color_scheme == "dark":
        bg_color = "#0f172a"
        text_color = "#f8fafc"
        text_muted = "#94a3b8"
        surface_color = "rgba(255, 255, 255, 0.03)"
        border_color = "rgba(255, 255, 255, 0.1)"
        shadow_color = "rgba(0, 0, 0, 0.5)"
    else:
        bg_color = "#f1f5f9"
        text_color = "#0f172a"
        text_muted = "#64748b"
        surface_color = "#ffffff"
        border_color = "rgba(0, 0, 0, 0.08)"
        shadow_color = "rgba(0, 0, 0, 0.05)"

    # === CSS ===
    css = f"""/* Scroll-Driven Viewport Reveal Cards */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --text: {text_color};
    --text-muted: {text_muted};
    --accent: {accent_color};
    --surface: {surface_color};
    --border: {border_color};
    --shadow: {shadow_color};
    --max-width: {width_px}px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background: var(--bg);
    color: var(--text);
    min-height: 100vh;
    line-height: 1.5;
    overflow-x: hidden;
}}

header {{
    height: {height_px}px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    padding: 2rem;
    max-width: 800px;
    margin: 0 auto;
}}

header h1 {{
    font-size: clamp(2.5rem, 5vw, 4rem);
    font-weight: 800;
    letter-spacing: -0.025em;
    margin-bottom: 1rem;
    background: linear-gradient(135deg, var(--text), var(--accent));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}}

header p {{
    font-size: 1.25rem;
    color: var(--text-muted);
}}

.scroll-indicator {{
    margin-top: 3rem;
    animation: bounce 2s infinite;
    opacity: 0.5;
}}

@keyframes bounce {{
    0%, 20%, 50%, 80%, 100% {{ transform: translateY(0); }}
    40% {{ transform: translateY(-15px); }}
    60% {{ transform: translateY(-7px); }}
}}

.grid-container {{
    max-width: var(--max-width);
    margin: 0 auto;
    padding: 4rem 2rem;
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
    gap: 2rem;
    padding-bottom: 10rem;
}}

.card {{
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 2.5rem 2rem;
    box-shadow: 0 10px 30px var(--shadow);
    display: flex;
    flex-direction: column;
    gap: 1rem;
    position: relative;
    overflow: hidden;
    
    /* Time-based transitions for hover state */
    transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1), 
                box-shadow 0.3s cubic-bezier(0.4, 0, 0.2, 1),
                border-color 0.3s ease;
    
    /* SCROLL-DRIVEN ANIMATION LOGIC */
    /* This connects the 'reveal' keyframes to the element's position in the viewport */
    animation: reveal linear both;
    animation-timeline: view();
    /* Starts when element enters bottom of screen, finishes when it is 25% up the screen */
    animation-range: entry 5% cover 25%;
}}

.card:hover {{
    transform: translateY(-8px);
    box-shadow: 0 20px 40px var(--shadow);
    border-color: var(--accent);
}}

.card::before {{
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 4px;
    background: var(--accent);
    transform: scaleX(0);
    transform-origin: left;
    transition: transform 0.4s ease;
}}

.card:hover::before {{
    transform: scaleX(1);
}}

.card-tag {{
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    font-weight: 700;
    color: var(--accent);
}}

.card h2 {{
    font-size: 1.5rem;
    font-weight: 600;
}}

.card p {{
    color: var(--text-muted);
}}

/* The specific keyframe animation to scrub through */
@keyframes reveal {{
    from {{
        opacity: 0;
        transform: translateY(80px) scale(0.85);
    }}
    to {{
        opacity: 1;
        transform: translateY(0) scale(1);
    }}
}}

/* Fallback for users preferring reduced motion */
@media (prefers-reduced-motion: reduce) {{
    .card {{
        animation: none !important;
        opacity: 1 !important;
        transform: none !important;
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
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
    
    <!-- Scroll-Timeline Polyfill for Safari/Firefox support -->
    <script src="https://flackr.github.io/scroll-timeline/dist/scroll-timeline.js"></script>
</head>
<body>
    <header>
        <h1>{title_text}</h1>
        <p>{body_text}</p>
        <div class="scroll-indicator">
            <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <line x1="12" y1="5" x2="12" y2="19"></line>
                <polyline points="19 12 12 19 5 12"></polyline>
            </svg>
        </div>
    </header>

    <main class="grid-container" id="grid">
        <!-- Cards will be injected via JS -->
    </main>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Generate cards dynamically to ensure page is scrollable
document.addEventListener('DOMContentLoaded', () => {{
    const grid = document.getElementById('grid');
    const cardCount = 12; // Enough to force scrolling

    const adjectives = ['Dynamic', 'Progressive', 'Silky', 'Hardware-Accelerated', 'Native', 'Smooth'];
    const nouns = ['Reveal', 'Viewport Animation', 'Scrubbing', 'Timeline', 'Intersection', 'Enhancement'];

    for (let i = 0; i < cardCount; i++) {{
        const card = document.createElement('article');
        card.className = 'card';
        
        const r1 = Math.floor(Math.random() * adjectives.length);
        const r2 = Math.floor(Math.random() * nouns.length);
        
        card.innerHTML = `
            <span class="card-tag">Item 0${{i + 1}}</span>
            <h2>${{adjectives[r1]}} ${{nouns[r2]}}</h2>
            <p>This card's entrance animation is tied directly to the scrollbar. It scales up and fades in precisely as it crosses the viewport threshold, running smoothly off the main thread.</p>
        `;
        
        grid.appendChild(card);
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
