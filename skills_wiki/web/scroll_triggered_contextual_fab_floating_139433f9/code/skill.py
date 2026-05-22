def create_component(
    output_dir: str,
    title_text: str = "Scroll Triggered FAB Transition",
    body_text: str = "Scroll down to see the inline action button detach and morph into a floating action button as it leaves the viewport. Scroll back up to see it return.",
    color_scheme: str = "dark",        
    accent_color: str = "#f6b93b",     
    width_px: int = 1000,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Scroll-Triggered Contextual FAB Morph effect.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Derive theme colors
    if color_scheme == "dark":
        bg_color = "#1a1e29"
        text_color = "#e2e8f0"
        text_muted = "#94a3b8"
        surface_color = "#272d3d"
    else:
        bg_color = "#f8fafc"
        text_color = "#0f172a"
        text_muted = "#64748b"
        surface_color = "#ffffff"

    # === CSS ===
    css = f"""/* Scroll-Triggered FAB Morph */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --text: {text_color};
    --text-muted: {text_muted};
    --surface: {surface_color};
    --accent: {accent_color};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background: var(--bg);
    color: var(--text);
    min-height: 100vh;
    display: flex;
    justify-content: center;
    /* Custom scrollbar for aesthetics */
    scrollbar-width: thin;
    scrollbar-color: var(--accent) var(--bg);
}}

.app-frame {{
    width: 100%;
    max-width: var(--width);
    min-height: 200vh; /* Force scrolling */
    padding: 4rem 2rem;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 4rem;
}}

.header {{
    text-align: center;
    max-width: 600px;
    margin-bottom: 2rem;
}}

.header h1 {{
    font-size: 2.5rem;
    font-weight: 700;
    margin-bottom: 1rem;
    color: var(--text);
    line-height: 1.2;
}}

.header p {{
    font-size: 1.125rem;
    color: var(--text-muted);
    line-height: 1.6;
}}

/* Dummy Content Blocks */
.content-block {{
    width: 100%;
    max-width: 650px;
    background: var(--surface);
    padding: 2.5rem;
    border-radius: 16px;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    color: var(--text-muted);
    line-height: 1.7;
}}

.content-block p {{ margin-bottom: 1.5rem; }}
.content-block p:last-child {{ margin-bottom: 0; }}

/* === The Core UI Pattern === */

.action-container {{
    display: flex;
    justify-content: center;
    align-items: center;
    width: 100%;
    padding: 2rem 0;
}}

.btn-static {{
    background: var(--accent);
    color: #111;
    font-family: inherit;
    font-size: 1.125rem;
    font-weight: 600;
    padding: 1rem 2.5rem;
    border: none;
    border-radius: 50px;
    cursor: pointer;
    box-shadow: 0 10px 25px color-mix(in srgb, var(--accent) 40%, transparent);
    transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
}}

.btn-static:hover {{
    transform: translateY(-4px) scale(1.02);
    box-shadow: 0 14px 30px color-mix(in srgb, var(--accent) 50%, transparent);
}}

.btn-fixed {{
    position: fixed;
    bottom: 2.5rem;
    right: 2.5rem;
    width: 64px;
    height: 64px;
    border-radius: 50%;
    background: var(--accent);
    color: #111;
    border: none;
    cursor: pointer;
    display: flex;
    justify-content: center;
    align-items: center;
    box-shadow: 0 10px 25px color-mix(in srgb, var(--accent) 40%, transparent);
    z-index: 100;
    
    /* Initial Hidden State */
    opacity: 0;
    transform: scale(0) translateY(20px);
    pointer-events: none;
    
    transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
}}

.btn-fixed svg {{
    width: 28px;
    height: 28px;
    fill: currentColor;
    transition: transform 0.3s ease;
}}

.btn-fixed:hover {{
    transform: scale(1.1) !important; /* Override the default scale(1) */
}}

.btn-fixed:hover svg {{
    transform: rotate(90deg);
}}

/* === Intersection Observer State Logic === */

/* When the static button has scrolled ABOVE the viewport (scroll-pos = -1) */
html[data-scroll-pos="-1"] .btn-static {{
    opacity: 0;
    transform: scale(0.8) translateY(-20px);
    pointer-events: none;
}}

html[data-scroll-pos="-1"] .btn-fixed {{
    opacity: 1;
    transform: scale(1) translateY(0);
    pointer-events: auto;
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
    <div class="app-frame">
        <header class="header">
            <h1>{title_text}</h1>
            <p>{body_text}</p>
        </header>

        <div class="content-block">
            <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.</p>
            <p>Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.</p>
        </div>

        <div class="content-block">
            <p>Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo.</p>
        </div>

        <!-- The Target Container tracked by JS -->
        <div class="action-container" id="action-trigger">
            <button class="btn-static">Subscribe Now</button>
        </div>

        <div class="content-block">
            <p>Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt. Neque porro quisquam est, qui dolorem ipsum quia dolor sit amet.</p>
            <p>Ut enim ad minima veniam, quis nostrum exercitationem ullam corporis suscipit laboriosam, nisi ut aliquid ex ea commodi consequatur? Quis autem vel eum iure reprehenderit qui in ea voluptate velit esse quam nihil molestiae consequatur.</p>
        </div>
        
        <div class="content-block">
            <p>Keep scrolling... Notice how the button has morphed into the bottom right corner?</p>
            <br/><br/><br/><br/><br/><br/><br/><br/>
            <p>End of article.</p>
        </div>
    </div>

    <!-- The Fixed FAB (Always in DOM, controlled by CSS state) -->
    <button class="btn-fixed" aria-label="Subscribe Now">
        <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
            <path d="M19 11H13V5C13 4.45 12.55 4 12 4C11.45 4 11 4.45 11 5V11H5C4.45 11 4 11.45 4 12C4 12.55 4.45 13 5 13H11V19C11 19.55 11.45 20 12 20C12.55 20 13 19.55 13 19V13H19C19.55 13 20 12.55 20 12C20 11.45 19.55 11 19 11Z"/>
        </svg>
    </button>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Scroll-Triggered Action Button logic using IntersectionObserver
document.addEventListener('DOMContentLoaded', () => {{
    const triggerEl = document.getElementById('action-trigger');
    
    // Set up the IntersectionObserver
    const observer = new IntersectionObserver((entries) => {{
        const entry = entries[0];
        let scrollPosition = 0;
        
        // entry.isIntersecting is true when the element is partially or fully visible
        if (entry.isIntersecting) {{
            scrollPosition = 0; // In viewport
        }} else if (entry.boundingClientRect.y < 0) {{
            scrollPosition = -1; // Scrolled past it (above viewport)
        }} else {{
            scrollPosition = 1; // Hasn't reached it yet (below viewport)
        }}
        
        // Apply state to the HTML tag to drive CSS transitions
        document.documentElement.setAttribute('data-scroll-pos', scrollPosition);
        
    }}, {{
        // Fire when 0% of the element is visible (crossing the threshold entirely)
        threshold: 0,
        // Optional: offset the trigger point slightly so the FAB morphs exactly as the container clips
        rootMargin: "-20px 0px 0px 0px"
    }});

    if (triggerEl) {{
        observer.observe(triggerEl);
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
