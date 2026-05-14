def create_component(
    output_dir: str,
    title_text: str = "Scroll-Driven Reveal",
    body_text: str = "Scroll down inside this frame. The cards below are animated entirely by CSS scroll timelines, requiring zero JavaScript to calculate intersection.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#00e5ff",     # CSS hex color for accent
    width_px: int = 1000,
    height_px: int = 700,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Pure CSS Scroll-Driven Reveal Cards effect.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Derive theme colors
    if color_scheme == "dark":
        bg_color = "#0f172a"          # Slate 900
        text_color = "#f8fafc"        # Slate 50
        text_muted = "#94a3b8"        # Slate 400
        surface_color = "rgba(255, 255, 255, 0.04)"
        border_color = "rgba(255, 255, 255, 0.1)"
        shadow = "none"
    else:
        bg_color = "#f8fafc"          # Slate 50
        text_color = "#0f172a"        # Slate 900
        text_muted = "#64748b"        # Slate 500
        surface_color = "#ffffff"
        border_color = "rgba(0, 0, 0, 0.08)"
        shadow = "0 10px 15px -3px rgba(0, 0, 0, 0.05), 0 4px 6px -2px rgba(0, 0, 0, 0.02)"

    # Generate Card HTML dynamically
    cards_html = ""
    for i in range(1, 15):
        cards_html += f"""
            <div class="card">
                <div class="icon-placeholder"></div>
                <h3 class="card-title">Feature Block {i}</h3>
                <p class="card-text">This element's opacity, scale, and translation are natively linked to your scroll position.</p>
            </div>"""

    # === CSS ===
    css = f"""/* Pure CSS Scroll-Driven Reveal — generated component */
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
    --shadow: {shadow};
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background: #000; /* Dark backdrop for the isolated component view */
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
}}

/* The scrollable component frame */
.component-frame {{
    width: {width_px}px;
    height: {height_px}px;
    max-width: 100vw;
    max-height: 100vh;
    background: var(--bg);
    overflow-y: auto; /* Acts as the scroll timeline root */
    position: relative;
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
    border: 1px solid rgba(255, 255, 255, 0.1);
}}

.content-wrapper {{
    padding: 6rem 3rem;
    max-width: 900px;
    margin: 0 auto;
}}

.header {{
    text-align: center;
    margin-bottom: 5rem;
}}

.title {{
    font-size: 3rem;
    font-weight: 700;
    color: var(--text);
    margin-bottom: 1rem;
    letter-spacing: -0.02em;
}}

.subtitle {{
    font-size: 1.125rem;
    color: var(--text-muted);
    max-width: 600px;
    margin: 0 auto;
    line-height: 1.6;
}}

/* Warning banner for unsupported browsers */
.support-warning {{
    display: none;
    background: rgba(255, 170, 0, 0.1);
    color: #ffaa00;
    padding: 1rem;
    border-radius: 8px;
    margin-top: 2rem;
    font-size: 0.9rem;
    border: 1px solid rgba(255, 170, 0, 0.2);
}}

.card-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
    gap: 1.5rem;
}}

.card {{
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 2rem;
    box-shadow: var(--shadow);
    display: flex;
    flex-direction: column;
    gap: 1rem;
    /* Base styles (fallback for browsers without animation-timeline) */
    opacity: 1;
    scale: 1;
    translate: 0 0;
}}

.icon-placeholder {{
    width: 48px;
    height: 48px;
    border-radius: 12px;
    background: var(--accent);
    opacity: 0.9;
    margin-bottom: 0.5rem;
    box-shadow: 0 0 20px var(--accent);
    filter: brightness(1.2);
}}

.card-title {{
    font-size: 1.25rem;
    font-weight: 600;
    color: var(--text);
}}

.card-text {{
    font-size: 0.95rem;
    color: var(--text-muted);
    line-height: 1.5;
}}

/* =========================================================
   THE MAGIC: CSS Scroll-Driven Animation
   ========================================================= */

@supports (animation-timeline: view()) {{
    @media (prefers-reduced-motion: no-preference) {{
        .card {{
            /* 1. Apply the animation */
            animation: card-reveal linear both;
            
            /* 2. Bind the animation to the element's intersection with the scrollport */
            animation-timeline: view();
            
            /* 3. Define the start and end range. 
               entry 5%: starts when element is 5% past the bottom edge.
               cover 25%: finishes when element has traveled 25% up the screen. */
            animation-range: entry 5% cover 25%;
        }}
    }}
}}

/* Independent transform properties (scale, translate) prevent conflict with standard transforms */
@keyframes card-reveal {{
    from {{
        opacity: 0;
        scale: 0.8;
        translate: 0 60px;
    }}
    to {{
        opacity: 1;
        scale: 1;
        translate: 0 0;
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
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="component-frame">
        <div class="content-wrapper">
            <header class="header">
                <h1 class="title">{title_text}</h1>
                <p class="subtitle">
                    {body_text}
                </p>
                <div class="support-warning" id="warning">
                    <strong>Note:</strong> Your browser does not currently support CSS Scroll Timelines. You are seeing the static fallback layout. Try viewing in Chrome or Edge 115+.
                </div>
            </header>
            
            <div class="card-grid">
                {cards_html}
            </div>
        </div>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Scroll-Driven Reveal — logic
document.addEventListener('DOMContentLoaded', () => {{
    // The core animation is 100% CSS. 
    // We only use JS here to detect support and inform the user if their browser lacks the feature.
    
    if (!CSS.supports('animation-timeline: view()')) {{
        const warning = document.getElementById('warning');
        if (warning) {{
            warning.style.display = 'block';
        }}
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
