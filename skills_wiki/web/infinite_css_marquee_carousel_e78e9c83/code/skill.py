def create_component(
    output_dir: str,
    title_text: str = "Platform Capabilities",
    body_text: str = "Explore the robust features powering our ecosystem.",
    color_scheme: str = "dark",
    accent_color: str = "#4361ee",
    width_px: int = 1000,
    height_px: int = 600,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Infinite CSS Marquee Carousel visual effect.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Theme handling
    if color_scheme == "dark":
        bg_color = "#0a0a16"
        text_color = "#f8f9fa"
        muted_text = "#8b8d9b"
        card_bg = "rgba(255, 255, 255, 0.03)"
        card_border = "rgba(255, 255, 255, 0.08)"
        card_hover_bg = "rgba(255, 255, 255, 0.06)"
    else:
        bg_color = "#f4f5f7"
        text_color = "#111118"
        muted_text = "#5a5c69"
        card_bg = "#ffffff"
        card_border = "rgba(0, 0, 0, 0.08)"
        card_hover_bg = "#fdfdfd"

    # CSS
    css = f"""/* Infinite CSS Marquee Carousel */
:root {{
    --bg: {bg_color};
    --text: {text_color};
    --muted: {muted_text};
    --accent: {accent_color};
    --card-bg: {card_bg};
    --card-border: {card_border};
    --card-hover: {card_hover_bg};
    --max-width: {width_px}px;
    --height: {height_px}px;
    --gap: 1.5rem;
}}

*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background-color: var(--bg);
    color: var(--text);
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 100vh;
    overflow-x: hidden;
}}

.viewport {{
    width: 100%;
    max-width: var(--max-width);
    padding: 2rem;
    display: flex;
    flex-direction: column;
    gap: 3rem;
}}

.header {{
    text-align: center;
}}

.header h1 {{
    font-size: 2.5rem;
    font-weight: 700;
    margin-bottom: 0.5rem;
    letter-spacing: -0.02em;
}}

.header p {{
    color: var(--muted);
    font-size: 1.125rem;
}}

/* =========================================
   CAROUSEL CORE STYLES
   ========================================= */

.carousel-container {{
    position: relative;
    width: 100%;
    /* Optional: Fade edges for a smoother entrance/exit */
    mask-image: linear-gradient(to right, transparent, black 10%, black 90%, transparent);
    -webkit-mask-image: linear-gradient(to right, transparent, black 10%, black 90%, transparent);
}}

.carousel {{
    display: flex;
    overflow: hidden; /* Replaces overflow-x: auto and hides scrollbar */
    width: 100%;
}}

.carousel-track {{
    display: flex;
    gap: var(--gap);
    /* 
      CRITICAL: Add padding-right equal to the gap. 
      This ensures the 100% translation width encompasses the spacing 
      needed before the next track starts.
    */
    padding-right: var(--gap);
    animation: marquee 25s linear infinite;
}}

/* Pause animation on hover for readability */
.carousel:hover .carousel-track {{
    animation-play-state: paused;
}}

@keyframes marquee {{
    from {{ translate: 0; }}
    to {{ translate: -100%; }}
}}

/* =========================================
   CARD STYLES
   ========================================= */

.card {{
    /* Prevent cards from shrinking to fit container */
    flex: 0 0 280px; 
    
    background: var(--card-bg);
    border: 1px solid var(--card-border);
    border-radius: 16px;
    padding: 2rem 1.5rem;
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
    gap: 1rem;
    transition: background 0.3s ease, transform 0.3s ease;
    cursor: default;
}}

.card:hover {{
    background: var(--card-hover);
    transform: translateY(-4px);
    box-shadow: 0 10px 30px -10px rgba(0,0,0,0.2);
}}

.card-icon-wrap {{
    width: 64px;
    height: 64px;
    border-radius: 50%;
    background: color-mix(in srgb, var(--accent) 15%, transparent);
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--accent);
    font-size: 1.5rem;
    box-shadow: inset 0 0 20px color-mix(in srgb, var(--accent) 10%, transparent);
}}

.card h3 {{
    font-size: 1.25rem;
    font-weight: 600;
}}

.card p {{
    font-size: 0.9rem;
    line-height: 1.5;
    color: var(--muted);
}}
"""

    # HTML
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
    <div class="viewport">
        <header class="header">
            <h1>{title_text}</h1>
            <p>{body_text}</p>
        </header>

        <div class="carousel-container">
            <div class="carousel">
                <!-- Group 1: Author content here -->
                <div class="carousel-track" id="primary-track">
                    <div class="card">
                        <div class="card-icon-wrap">☁️</div>
                        <h3>Cloud Storage</h3>
                        <p>Securely store and retrieve your files from anywhere in the world.</p>
                    </div>
                    <div class="card">
                        <div class="card-icon-wrap">🔒</div>
                        <h3>Reliable & Safe</h3>
                        <p>Enterprise-grade encryption keeps your data protected around the clock.</p>
                    </div>
                    <div class="card">
                        <div class="card-icon-wrap">🤖</div>
                        <h3>Automated Insights</h3>
                        <p>Leverage AI to automatically extract meaningful trends from your data.</p>
                    </div>
                    <div class="card">
                        <div class="card-icon-wrap">💎</div>
                        <h3>Premium Support</h3>
                        <p>Get 24/7 access to our dedicated success team for immediate resolution.</p>
                    </div>
                    <div class="card">
                        <div class="card-icon-wrap">⚡</div>
                        <h3>Optimization</h3>
                        <p>Lightning-fast delivery networks ensure zero latency globally.</p>
                    </div>
                </div>
                <!-- Group 2 will be injected via JS to ensure DRY HTML & accessibility -->
            </div>
        </div>
    </div>
    
    <script src="script.js"></script>
</body>
</html>"""

    # JavaScript
    js = f"""// Infinite Marquee JS Logic
document.addEventListener('DOMContentLoaded', () => {{
    const carousel = document.querySelector('.carousel');
    const primaryTrack = document.getElementById('primary-track');
    
    if (carousel && primaryTrack) {{
        // 1. Clone the primary track
        const cloneTrack = primaryTrack.cloneNode(true);
        
        // 2. Remove the ID to prevent duplicates
        cloneTrack.removeAttribute('id');
        
        // 3. Add aria-hidden so screen readers don't read the duplicated content
        cloneTrack.setAttribute('aria-hidden', 'true');
        
        // 4. Append the cloned track directly behind the original
        carousel.appendChild(cloneTrack);
    }}
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
