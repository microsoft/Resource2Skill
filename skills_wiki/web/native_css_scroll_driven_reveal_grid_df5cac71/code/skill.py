def create_component(
    output_dir: str,
    title_text: str = "Scroll-Driven Reveal",
    body_text: str = "Scroll down to see the elements dynamically animate into view based on your scroll position.",
    color_scheme: str = "dark",
    accent_color: str = "#00bfff",
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the CSS Scroll-Driven Reveal Gallery effect.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors ===
    if color_scheme == "dark":
        bg_color = "#0a0a0f"
        text_color = "#ffffff"
        text_muted = "#a1a1aa"
        surface_color = "rgba(255, 255, 255, 0.05)"
        surface_hover = "rgba(255, 255, 255, 0.08)"
        border_color = "rgba(255, 255, 255, 0.1)"
    else:
        bg_color = "#f4f4f5"
        text_color = "#18181b"
        text_muted = "#52525b"
        surface_color = "rgba(0, 0, 0, 0.03)"
        surface_hover = "rgba(0, 0, 0, 0.06)"
        border_color = "rgba(0, 0, 0, 0.08)"

    # Derive semi-transparent accent for glow effects
    hex_c = accent_color.lstrip('#')
    if len(hex_c) == 6:
        r, g, b = tuple(int(hex_c[i:i+2], 16) for i in (0, 2, 4))
        accent_alpha = f"rgba({r}, {g}, {b}, 0.25)"
    else:
        accent_alpha = "rgba(0, 191, 255, 0.25)"

    # Generate Card HTML
    cards_html = ""
    for i in range(1, 13):
        cards_html += f"""
            <div class="card">
                <div class="card-icon" style="background: {accent_alpha}; color: {accent_color};">0{i}</div>
                <h3 class="card-title">Feature Block</h3>
                <p class="card-text">Smooth animations driven purely by CSS timelines.</p>
            </div>"""

    # === CSS ===
    css = f"""/* CSS Scroll-Driven Reveal Component */
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
    --accent-alpha: {accent_alpha};
    --surface: {surface_color};
    --surface-hover: {surface_hover};
    --border: {border_color};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background: #000; /* Dark outer background to frame the component */
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
}}

.viewport-container {{
    width: var(--width);
    height: var(--height);
    background: var(--bg);
    color: var(--text);
    overflow-y: auto;
    overflow-x: hidden;
    position: relative;
    scroll-behavior: smooth;
    box-shadow: 0 0 50px rgba(0,0,0,0.5);
}}

/* Custom Scrollbar for container */
.viewport-container::-webkit-scrollbar {{
    width: 10px;
}}
.viewport-container::-webkit-scrollbar-track {{
    background: var(--bg);
}}
.viewport-container::-webkit-scrollbar-thumb {{
    background: var(--border);
    border-radius: 5px;
}}

.hero {{
    min-height: 85%;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    padding: 2rem;
}}

.hero h1 {{
    font-size: 3.5rem;
    font-weight: 700;
    letter-spacing: -0.05em;
    margin-bottom: 1rem;
    background: linear-gradient(135deg, var(--text), var(--text-muted));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}}

.hero p {{
    font-size: 1.125rem;
    color: var(--text-muted);
    max-width: 500px;
    line-height: 1.6;
    margin-bottom: 3rem;
}}

.scroll-indicator {{
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0.5rem;
    color: var(--accent);
    font-weight: 500;
    font-size: 0.875rem;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    animation: bounce 2s infinite ease-in-out;
}}

@keyframes bounce {{
    0%, 100% {{ transform: translateY(0); }}
    50% {{ transform: translateY(10px); }}
}}

.grid {{
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 32px;
    padding: 32px 48px 96px 48px;
    max-width: 1200px;
    margin: 0 auto;
}}

/* --- Card Base Styles --- */
.card {{
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 32px 24px;
    display: flex;
    flex-direction: column;
    gap: 16px;
    cursor: pointer;
    
    /* 1. Base state for JS Fallback */
    opacity: 0;
    transform: translateY(60px) scale(0.85);
    /* Transition is applied here for the JS fallback toggle */
    transition: opacity 0.8s cubic-bezier(0.16, 1, 0.3, 1), 
                transform 0.8s cubic-bezier(0.16, 1, 0.3, 1),
                background 0.3s ease, border-color 0.3s ease, box-shadow 0.3s ease;
}}

.card-icon {{
    width: 48px;
    height: 48px;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 700;
    font-size: 1.2rem;
}}

.card-title {{
    font-size: 1.25rem;
    font-weight: 600;
}}

.card-text {{
    color: var(--text-muted);
    font-size: 0.95rem;
    line-height: 1.5;
}}

/* Hover interaction */
.card:hover {{
    background: var(--surface-hover);
    border-color: var(--accent);
    box-shadow: 0 10px 40px -10px var(--accent-alpha);
}}

/* --- Modern CSS Scroll Timeline Execution --- */
@supports (animation-timeline: view()) {{
    .card {{
        /* Reset initial state so keyframes take full control */
        opacity: 0; 
        transform: none; 
        
        /* Apply scroll-driven animation */
        animation: scroll-reveal linear both;
        animation-timeline: view();
        /* Start animating slightly after entering viewport, finish when 30% visible */
        animation-range: entry 5% cover 30%;
        
        /* Remove opacity/transform from standard transitions to avoid fighting the timeline */
        transition: background 0.3s ease, border-color 0.3s ease, box-shadow 0.3s ease;
    }}
}}

/* Keyframes mapped linearly to scroll position */
@keyframes scroll-reveal {{
    0% {{
        opacity: 0;
        transform: translateY(80px) scale(0.85);
    }}
    100% {{
        opacity: 1;
        transform: translateY(0) scale(1);
    }}
}}

/* --- JS Fallback Execution State --- */
.card.is-visible {{
    opacity: 1;
    transform: translateY(0) scale(1);
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
    <div class="viewport-container" id="scroll-root">
        <div class="hero">
            <h1>{title_text}</h1>
            <p>{body_text}</p>
            <div class="scroll-indicator">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M12 5v14M19 12l-7 7-7-7"/>
                </svg>
            </div>
        </div>
        <div class="grid">
            {cards_html}
        </div>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = """// CSS Scroll-Driven Reveal Fallback Logic
document.addEventListener('DOMContentLoaded', () => {
    // 1. Check if the browser supports the modern CSS animation-timeline
    const supportsScrollTimeline = CSS.supports('animation-timeline: view()');

    // 2. If it is NOT supported (e.g., Safari, older Firefox), initialize the JS fallback
    if (!supportsScrollTimeline) {
        console.info('animation-timeline not supported. Initializing IntersectionObserver fallback.');
        
        const scrollRoot = document.getElementById('scroll-root');
        const cards = document.querySelectorAll('.card');

        // Observer options: Use the specific container as root, trigger when 15% visible
        const observerOptions = {
            root: scrollRoot,
            rootMargin: '0px',
            threshold: 0.15 
        };

        const observer = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    // Add visibility class to trigger standard CSS transition
                    entry.target.classList.add('is-visible');
                    // Stop observing once revealed to match CSS 'both' fill-mode behavior
                    observer.unobserve(entry.target);
                }
            });
        }, observerOptions);

        cards.forEach(card => observer.observe(card));
    } else {
        console.info('Native CSS animation-timeline supported. Running purely on GPU.');
    }
});
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
