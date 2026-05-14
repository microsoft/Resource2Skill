def create_component(
    output_dir: str,
    title_text: str = "CSS Animation Toolkit",
    body_text: str = "Hover over cards to trigger effects. Click any card to pause/resume its animation.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#00bfff",     # CSS hex color for accent
    width_px: int = 1000,
    height_px: int = 700,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the CSS Keyframe Animations visual effects.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme and accent_color ===
    if color_scheme == "dark":
        bg_color = "#1e1e24"
        text_color = "#f8f9fa"
        surface_color = "#2b2b36"
        border_color = "#3a3a48"
    else:
        bg_color = "#f0f2f5"
        text_color = "#1a1a2e"
        surface_color = "#ffffff"
        border_color = "#e1e4e8"

    # === CSS ===
    css = f"""/* CSS Keyframe Animation Toolkit */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --text: {text_color};
    --accent: {accent_color};
    --surface: {surface_color};
    --border: {border_color};
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
    overflow: hidden;
}}

.container {{
    width: var(--width);
    max-width: 90vw;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 40px;
}}

header {{
    text-align: center;
}}

h1 {{
    font-size: 2.5rem;
    margin-bottom: 10px;
    letter-spacing: -0.02em;
}}

p.subtitle {{
    color: var(--text);
    opacity: 0.7;
    font-size: 1.1rem;
}}

.grid {{
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 30px;
    width: 100%;
}}

.card {{
    aspect-ratio: 1 / 1;
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 16px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    cursor: pointer;
    user-select: none;
    box-shadow: 0 4px 15px rgba(0,0,0,0.05);
    transition: box-shadow 0.3s ease;
    padding: 20px;
}}

.card:focus-visible {{
    outline: 2px solid var(--accent);
    outline-offset: 4px;
}}

.card-icon {{
    font-size: 3rem;
    margin-bottom: 15px;
    pointer-events: none;
}}

.card-title {{
    font-weight: 600;
    font-size: 1.2rem;
    pointer-events: none;
    margin-bottom: 4px;
}}

.card-desc {{
    font-size: 0.85rem;
    opacity: 0.6;
    pointer-events: none;
}}

/* =========================================
   ANIMATION DEFINITIONS (FROM TUTORIAL)
   ========================================= */

/* 1. Slide (Translate, Alternate Direction) */
@keyframes slideRight {{
    0% {{ transform: translateX(-20px); }}
    100% {{ transform: translateX(20px); }}
}}
.card.slide:hover {{
    animation-name: slideRight;
    animation-duration: 0.8s;
    animation-timing-function: ease-in-out;
    animation-iteration-count: infinite;
    animation-direction: alternate; /* Moves back and forth smoothly */
}}

/* 2. Rotate (Linear Timing) */
@keyframes rotate {{
    from {{ transform: rotateZ(0deg); }}
    to {{ transform: rotateZ(360deg); }}
}}
.card.rotate {{
    animation: rotate 5s linear infinite; /* Constant speed */
}}

/* 3. Grow (Scale & Cubic Bezier) */
@keyframes grow {{
    0% {{ transform: scale(1); }}
    100% {{ transform: scale(1.15); }}
}}
.card.grow:hover {{
    /* Custom spring-like bounce using cubic-bezier */
    animation: grow 0.6s cubic-bezier(0.28, -0.5, 0.54, 2.21) infinite alternate;
}}

/* 4. Fade (Opacity Transition) */
@keyframes fade {{
    0% {{ opacity: 1; }}
    100% {{ opacity: 0.2; }}
}}
.card.fade {{
    animation: fade 1.5s ease-in-out infinite alternate;
}}

/* 5. Glow (Box-Shadow & Color Shift) */
@keyframes glow {{
    0% {{ 
        box-shadow: 0 0 0px var(--accent); 
        border-color: var(--border);
    }}
    100% {{ 
        box-shadow: 0 0 30px var(--accent), inset 0 0 10px var(--accent); 
        border-color: var(--accent);
    }}
}}
.card.glow:hover {{
    animation: glow 0.8s ease-in-out infinite alternate;
}}

/* 6. Stepped Motion (Ticking Clock Effect) */
.card.steps {{
    /* Breaks a smooth rotation into 8 discrete frames */
    animation: rotate 4s steps(8) infinite;
}}

/* =========================================
   PLAY STATE CONTROL (JS TOGGLED)
   ========================================= */
.card.paused {{
    animation-play-state: paused !important;
}}
.card.paused .card-desc::after {{
    content: " (Paused)";
    color: var(--accent);
    font-weight: 700;
    opacity: 1;
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
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        <header>
            <h1>{title_text}</h1>
            <p class="subtitle">{body_text}</p>
        </header>
        
        <div class="grid">
            <!-- Animation 1: Slide -->
            <div class="card slide" tabindex="0">
                <div class="card-icon">↔️</div>
                <div class="card-title">Slide</div>
                <div class="card-desc">Hover • Alternate</div>
            </div>

            <!-- Animation 2: Rotate -->
            <div class="card rotate" tabindex="0">
                <div class="card-icon">🔄</div>
                <div class="card-title">Rotate</div>
                <div class="card-desc">Infinite • Linear</div>
            </div>

            <!-- Animation 3: Grow -->
            <div class="card grow" tabindex="0">
                <div class="card-icon">🗜️</div>
                <div class="card-title">Grow</div>
                <div class="card-desc">Hover • Cubic Bezier</div>
            </div>

            <!-- Animation 4: Fade -->
            <div class="card fade" tabindex="0">
                <div class="card-icon">👻</div>
                <div class="card-title">Fade</div>
                <div class="card-desc">Infinite • Ease</div>
            </div>

            <!-- Animation 5: Glow -->
            <div class="card glow" tabindex="0">
                <div class="card-icon">🌟</div>
                <div class="card-title">Glow</div>
                <div class="card-desc">Hover • Box Shadow</div>
            </div>

            <!-- Animation 6: Stepped -->
            <div class="card steps" tabindex="0">
                <div class="card-icon">⏱️</div>
                <div class="card-title">Steps</div>
                <div class="card-desc">Infinite • steps(8)</div>
            </div>
        </div>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// CSS Animation Toolkit Interactive Behavior
document.addEventListener('DOMContentLoaded', () => {{
    const cards = document.querySelectorAll('.card');

    cards.forEach(card => {{
        // Toggle animation play state on click
        card.addEventListener('click', () => {{
            card.classList.toggle('paused');
        }});

        // Accessibility: Allow keyboard toggle
        card.addEventListener('keydown', (e) => {{
            if (e.key === 'Enter' || e.key === ' ') {{
                e.preventDefault();
                card.classList.toggle('paused');
            }}
        }});
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
