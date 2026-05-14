def create_component(
    output_dir: str,
    title_text: str = "Discover The Details",
    body_text: str = "This card's position is physically bound to your scroll position. Scroll up and down to scrub the timeline.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#8a2be2",     # CSS hex color for accent
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the GSAP ScrollTrigger + Lenis smooth scroll reveal.
    
    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os
    import html

    os.makedirs(output_dir, exist_ok=True)
    
    safe_title = html.escape(title_text)
    safe_body = html.escape(body_text)

    # === Derive theme colors from color_scheme ===
    if color_scheme == "dark":
        bg_color = "#0f1016"
        grid_color = "rgba(255, 255, 255, 0.05)"
        text_color = "#f0f0f0"
        text_muted = "#a0a0b0"
        surface_color = "rgba(255, 255, 255, 0.03)"
        border_color = "rgba(255, 255, 255, 0.1)"
        shadow = "0 20px 40px rgba(0,0,0,0.4)"
    else:
        bg_color = "#f4f6f8"
        grid_color = "rgba(0, 0, 0, 0.05)"
        text_color = "#111111"
        text_muted = "#555566"
        surface_color = "#ffffff"
        border_color = "rgba(0, 0, 0, 0.1)"
        shadow = "0 20px 40px rgba(0,0,0,0.08)"

    # === CSS ===
    css = f"""/* Smooth Scroll-Linked Content Reveal — generated component */
:root {{
    --bg: {bg_color};
    --grid: {grid_color};
    --text: {text_color};
    --text-muted: {text_muted};
    --accent: {accent_color};
    --surface: {surface_color};
    --border: {border_color};
    --shadow: {shadow};
    --max-width: {width_px}px;
}}

/* Lenis recommended base styles */
html.lenis {{ height: auto; }}
.lenis.lenis-smooth {{ scroll-behavior: auto !important; }}
.lenis.lenis-smooth [data-lenis-prevent] {{ overscroll-behavior: contain; }}
.lenis.lenis-stopped {{ overflow: hidden; }}
.lenis.lenis-scrolling iframe {{ pointer-events: none; }}

*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: 'Inter', system-ui, sans-serif;
    background-color: var(--bg);
    color: var(--text);
    /* Subtle grid to make smooth scrolling visually apparent */
    background-image: 
        linear-gradient(to right, var(--grid) 1px, transparent 1px),
        linear-gradient(to bottom, var(--grid) 1px, transparent 1px);
    background-size: 40px 40px;
    overflow-x: hidden;
}}

.spacer {{
    height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-direction: column;
    text-align: center;
    padding: 2rem;
}}

.spacer-text {{
    font-size: 1rem;
    color: var(--text-muted);
    letter-spacing: 2px;
    text-transform: uppercase;
    animation: pulse 2s infinite;
}}

@keyframes pulse {{
    0%, 100% {{ opacity: 0.5; transform: translateY(0); }}
    50% {{ opacity: 1; transform: translateY(5px); }}
}}

.trigger-section {{
    height: 150vh; /* Extra height to allow a long scroll track for the animation */
    display: flex;
    align-items: center;
    justify-content: center;
    position: relative;
    border-top: 1px dashed var(--border);
    border-bottom: 1px dashed var(--border);
    background: radial-gradient(circle at center, var(--surface) 0%, transparent 70%);
}}

.animated-card {{
    background: var(--surface);
    border: 1px solid var(--border);
    border-left: 4px solid var(--accent);
    padding: 3rem;
    border-radius: 12px;
    width: 90%;
    max-width: 450px;
    box-shadow: var(--shadow);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    
    /* Performance optimization */
    will-change: transform, opacity;
    
    /* Initial state (hidden and pushed left) */
    opacity: 0;
    transform: translateX(-150px);
}}

.card-title {{
    font-size: 1.75rem;
    font-weight: 700;
    margin-bottom: 1rem;
    line-height: 1.2;
}}

.card-title span {{
    color: var(--accent);
}}

.card-body {{
    font-size: 1rem;
    line-height: 1.6;
    color: var(--text-muted);
}}
"""

    # === HTML ===
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Scroll-Linked Animation</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>

    <section class="spacer">
        <h2 style="font-size: 3rem; margin-bottom: 1rem;">Keep Scrolling</h2>
        <div class="spacer-text">↓ Scroll Down ↓</div>
    </section>

    <!-- The trigger section dictates the start and end of the timeline -->
    <section class="trigger-section">
        
        <!-- The element that actually animates -->
        <div class="animated-card">
            <h3 class="card-title"><span>#</span> {safe_title}</h3>
            <p class="card-body">{safe_body}</p>
        </div>

    </section>

    <section class="spacer">
        <h2 style="font-size: 2rem;">End of Timeline</h2>
        <div class="spacer-text" style="margin-top: 1rem; animation: none;">Scroll back up to reverse</div>
    </section>

    <!-- Lenis Smooth Scroll -->
    <script src="https://cdn.jsdelivr.net/gh/studio-freight/lenis@1.0.29/bundled/lenis.min.js"></script>
    
    <!-- GSAP Core & ScrollTrigger -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/gsap.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/ScrollTrigger.min.js"></script>
    
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""document.addEventListener('DOMContentLoaded', () => {{
    
    // 1. Initialize Lenis for Smooth Scrolling
    const lenis = new Lenis({{
        duration: 1.2, // smoothness modifier
        easing: (t) => Math.min(1, 1.001 - Math.pow(2, -10 * t)), 
        direction: 'vertical', 
        gestureDirection: 'vertical',
        smooth: true,
        mouseMultiplier: 1,
        smoothTouch: false,
        touchMultiplier: 2,
    }});

    // Tie Lenis rAF to GSAP ticker so they stay perfectly in sync
    lenis.on('scroll', ScrollTrigger.update);

    gsap.ticker.add((time) => {{
        lenis.raf(time * 1000);
    }});
    gsap.ticker.lagSmoothing(0);

    // 2. Register GSAP ScrollTrigger
    gsap.registerPlugin(ScrollTrigger);

    // 3. Create the Scroll Animation
    // We animate from the CSS default (-150px, opacity 0) TO (0px, opacity 1)
    gsap.to('.animated-card', {{
        x: 0,
        opacity: 1,
        ease: "none", // Avoid adding ease to scrubbed animations for 1:1 scroll feel
        scrollTrigger: {{
            trigger: '.trigger-section',
            
            // "top center" -> Start animation when the TOP of the trigger-section hits the CENTER of viewport
            start: 'top center',
            
            // "bottom center" -> End animation when the BOTTOM of the trigger-section hits the CENTER of viewport
            end: 'bottom center',
            
            // Link animation progress directly to scrollbar (scrubbing)
            scrub: true,
            
            // Uncomment to see the visual markers debugging tools
            // markers: true 
        }}
    }});
}});
"""

    # === Write files ===
    files = []
    for fname, content in [("index.html", html_content), ("style.css", css), ("script.js", js)]:
        path = os.path.join(output_dir, fname)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        files.append(path)

    return {
        "html": html_content,
        "css": css,
        "js": js,
        "files": files,
    }
