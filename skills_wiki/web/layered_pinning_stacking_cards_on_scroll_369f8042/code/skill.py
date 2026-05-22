def create_component(
    output_dir: str,
    title_text: str = "Layered Pinning",
    body_text: str = "A smooth, scroll-driven stacking card effect built with GSAP ScrollTrigger.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#00bfff",     # CSS hex color for accent
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Layered Pinning Stacking Cards effect.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Formulate theme colors
    if color_scheme == "dark":
        body_bg = "#000000"
        grid_color = "rgba(255,255,255,0.05)"
        
        bg_color = "#020617"       # Very dark blue/black
        surface_color = "#0f172a"  # Slate 900
        mix_bg = "#1e293b"         # Slate 800
        final_bg = "#334155"       # Slate 700
        
        text_color = "#f8fafc"
        shadow_op = "0.6"
    else:
        body_bg = "#e5e7eb"
        grid_color = "rgba(0,0,0,0.05)"
        
        bg_color = "#ffffff"       # White
        surface_color = "#f1f5f9"  # Slate 50
        mix_bg = "#e2e8f0"         # Slate 200
        final_bg = "#cbd5e1"       # Slate 300
        
        text_color = "#0f172a"
        shadow_op = "0.15"

    # Style the last word of the title with the accent color
    words = title_text.split()
    if len(words) > 1:
        words[-1] = f'<span class="accent">{words[-1]}</span>'
        formatted_title = " ".join(words)
    else:
        formatted_title = f'<span class="accent">{title_text}</span>'

    css = f"""/* Layered Pinning Component */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --surface: {surface_color};
    --mix-bg: {mix_bg};
    --final-bg: {final_bg};
    --text: {text_color};
    --accent: {accent_color};
    --width: {width_px}px;
    --height: {height_px}px;
    --shadow-op: {shadow_op};
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background-color: {body_bg};
    background-image: radial-gradient({grid_color} 1px, transparent 1px);
    background-size: 24px 24px;
    color: var(--text);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
}}

.container {{
    width: var(--width);
    height: var(--height);
    max-width: 95vw;
    max-height: 95vh;
    position: relative;
    border-radius: 24px;
    background: var(--bg);
    box-shadow: 0 32px 64px rgba(0,0,0,0.4);
    overflow: hidden; 
}}

/* The scrollable wrapper */
.wrapper {{
    width: 100%;
    height: 100%;
    overflow-y: auto;
    overflow-x: hidden;
    overscroll-behavior: none;
    position: relative;
}}

/* Hide scrollbar for a cleaner aesthetic */
.wrapper::-webkit-scrollbar {{ width: 6px; }}
.wrapper::-webkit-scrollbar-track {{ background: transparent; }}
.wrapper::-webkit-scrollbar-thumb {{
    background: color-mix(in srgb, var(--text) 20%, transparent);
    border-radius: 10px;
}}

/* Individual Panels */
.panel {{
    width: 100%;
    height: 100%; /* Matches wrapper height */
    position: relative;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;
    padding: 3rem;
    border-radius: 24px;
    will-change: transform, opacity;
    overflow: hidden;
}}

/* Z-index and Colors establish the stacking hierarchy */
.panel:nth-child(1) {{ 
    background: var(--bg); 
    z-index: 1; 
}}
.panel:nth-child(2) {{ 
    background: var(--surface); 
    z-index: 2; 
    /* Upward casting shadow creates depth over the previous panel */
    box-shadow: 0 -20px 50px rgba(0,0,0,var(--shadow-op)); 
}}
.panel:nth-child(3) {{ 
    background: var(--mix-bg); 
    z-index: 3; 
    box-shadow: 0 -20px 50px rgba(0,0,0,var(--shadow-op)); 
}}
.panel:nth-child(4) {{ 
    background: var(--final-bg); 
    z-index: 4; 
    box-shadow: 0 -20px 50px rgba(0,0,0,var(--shadow-op)); 
}}

/* Typography */
.panel-content {{
    max-width: 800px;
    display: flex;
    flex-direction: column;
    gap: 1.25rem;
    align-items: center;
}}

.badge {{
    font-size: 0.875rem;
    font-weight: 700;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    padding: 0.5rem 1.25rem;
    border-radius: 100px;
    background: color-mix(in srgb, var(--accent) 15%, transparent);
    color: var(--accent);
    margin-bottom: 1rem;
}}

.title {{
    font-size: clamp(2.5rem, 6vw, 5rem);
    font-weight: 800;
    letter-spacing: -0.03em;
    line-height: 1.05;
}}

.accent {{
    color: var(--accent);
}}

h2 {{
    font-size: clamp(2rem, 4vw, 3.5rem);
    font-weight: 700;
    letter-spacing: -0.02em;
}}

.body-text, p {{
    font-size: clamp(1.1rem, 2vw, 1.35rem);
    opacity: 0.75;
    line-height: 1.6;
    font-weight: 400;
}}

/* Scroll Indicator */
.scroll-indicator {{
    position: absolute;
    bottom: 3rem;
    left: 50%;
    transform: translateX(-50%);
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0.75rem;
    opacity: 0.5;
    animation: bounce 2s cubic-bezier(0.4, 0, 0.2, 1) infinite;
    font-size: 0.875rem;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
}}

@keyframes bounce {{
    0%, 100% {{ transform: translate(-50%, 0); }}
    50% {{ transform: translate(-50%, 8px); }}
}}

.scroll-arrow {{
    width: 10px;
    height: 10px;
    border-right: 2px solid var(--text);
    border-bottom: 2px solid var(--text);
    transform: rotate(45deg);
}}

@media (max-width: 768px) {{
    .panel {{ padding: 1.5rem; }}
}}
"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Layered Pinning Component</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
    
    <!-- GSAP & ScrollTrigger Core -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/gsap.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/ScrollTrigger.min.js"></script>
</head>
<body>
    <div class="container">
        <div class="wrapper">
            
            <section class="panel">
                <div class="panel-content">
                    <div class="badge">01 Intro</div>
                    <h1 class="title">{formatted_title}</h1>
                    <p class="body-text">{body_text}</p>
                </div>
                <div class="scroll-indicator">
                    <span>Scroll</span>
                    <div class="scroll-arrow"></div>
                </div>
            </section>
            
            <section class="panel">
                <div class="panel-content">
                    <div class="badge">02 Layout</div>
                    <h2>Tactile Scrolling</h2>
                    <p>Panels stick to the top of the viewport while subsequent content smoothly slides up and layers over them.</p>
                </div>
            </section>
            
            <section class="panel">
                <div class="panel-content">
                    <div class="badge">03 Depth</div>
                    <h2>Receding Illusion</h2>
                    <p>As panels are covered, they scale down and fade, leveraging upward-cast shadows to create satisfying physical depth.</p>
                </div>
            </section>
            
            <section class="panel">
                <div class="panel-content">
                    <div class="badge">04 Engine</div>
                    <h2>Powered by <span class="accent">GSAP</span></h2>
                    <p>High-performance ScrollTrigger animations tie directly to your scrollbar. No scroll-jacking, just pure reactive motion.</p>
                </div>
            </section>

        </div>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    js = f"""// Ensure GSAP and ScrollTrigger are ready
document.addEventListener('DOMContentLoaded', () => {{
    if (typeof gsap === 'undefined' || typeof ScrollTrigger === 'undefined') {{
        console.error('GSAP or ScrollTrigger failed to load.');
        return;
    }}

    gsap.registerPlugin(ScrollTrigger);

    const panels = gsap.utils.toArray('.panel');
    const scroller = document.querySelector('.wrapper');

    panels.forEach((panel, index) => {{
        // We do not want to pin or scale the very last panel
        if (index === panels.length - 1) return;

        // Animate the current panel scaling down while the next panel scrolls over it
        gsap.to(panel, {{
            scale: 0.85,          // Recede backwards
            opacity: 0.2,         // Fade out into shadow
            transformOrigin: "top center", // Anchor to top so it pulls away from bottom/sides
            ease: "none",         // Linear animation synced exactly to scroll
            
            scrollTrigger: {{
                trigger: panel,
                scroller: scroller,
                start: "top top", // When the panel hits the top of the wrapper
                
                // End exactly when one full panel height has been scrolled past
                end: () => "+=" + panel.offsetHeight, 
                
                pin: true,        // Stick it in place
                pinSpacing: false,// Don't push following elements down; let them overlap
                
                scrub: 0.5,       // Smooth scrubbing with a 0.5s catch-up lag
                invalidateOnRefresh: true // Recalculate heights dynamically on window resize
            }}
        }});
    }});

    // Refresh ScrollTrigger calculations on window resize
    window.addEventListener('resize', () => {{
        ScrollTrigger.refresh();
    }});
}});
"""

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
