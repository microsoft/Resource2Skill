def create_component(
    output_dir: str,
    title_text: str = "Scroll Animation Magic",
    body_text: str = "Scroll down to see the elements react to the viewport.",
    color_scheme: str = "dark",
    accent_color: str = "#ff4500",
    width_px: int = 1000,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing CSS-Only Scroll Animations.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    if color_scheme == "dark":
        bg_color = "#0f1115"
        text_color = "#ffffff"
        text_muted = "#888888"
        card_bg = "rgba(255, 255, 255, 0.03)"
        border_color = "rgba(255, 255, 255, 0.1)"
    else:
        bg_color = "#f4f4f5"
        text_color = "#000000"
        text_muted = "#666666"
        card_bg = "#ffffff"
        border_color = "rgba(0, 0, 0, 0.1)"

    css = f"""/* Native CSS Scroll Animations */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --text: {text_color};
    --muted: {text_muted};
    --accent: {accent_color};
    --card-bg: {card_bg};
    --border: {border_color};
}}

body {{
    font-family: 'Inter', system-ui, sans-serif;
    background: #000; /* Outer background to contrast widget */
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 100vh;
}}

/* The scrollable widget container */
.scroll-container {{
    width: {width_px}px;
    height: {height_px}px;
    max-width: 100vw;
    background: var(--bg);
    color: var(--text);
    overflow-y: scroll;
    overflow-x: hidden;
    position: relative;
    border-radius: 12px;
    box-shadow: 0 20px 40px rgba(0,0,0,0.4);
    scroll-behavior: smooth;
}}

/* Structural Spacing */
.hero, .section-spacer {{
    min-height: 100%; /* Relative to container height */
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 2rem;
    text-align: center;
}}

.hero h1 {{
    font-size: 3.5rem;
    margin-bottom: 1rem;
    letter-spacing: -0.05em;
}}

.hero p {{
    color: var(--muted);
    font-size: 1.25rem;
}}

.scroll-indicator {{
    position: absolute;
    bottom: 2rem;
    left: 50%;
    transform: translateX(-50%);
    animation: bounce 2s infinite ease-in-out;
    color: var(--accent);
}}

@keyframes bounce {{
    0%, 100% {{ transform: translate(-50%, 0); }}
    50% {{ transform: translate(-50%, 10px); }}
}}

/* =========================================
   TYPE 1: Continuous Rotation (Background/Abstract)
   Animates from 0% to 100% of the viewport 
   ========================================= */
.type1-visual {{
    width: 250px;
    height: 250px;
    background: conic-gradient(from 90deg at 50% 50%, var(--bg), var(--accent), var(--bg));
    border-radius: 30% 70% 70% 30% / 30% 30% 70% 70%;
    box-shadow: inset 0 0 50px var(--bg);
}}

@keyframes autoRotate {{
    from {{ transform: rotate(0deg); }}
    to {{ transform: rotate(360deg); }}
}}

/* =========================================
   TYPE 2: Reveal & Stabilize (Cards/Content)
   Enters hidden, reveals by 30-40% viewport, stays
   ========================================= */
.type2-card {{
    background: var(--card-bg);
    border: 1px solid var(--border);
    padding: 3rem;
    border-radius: 16px;
    max-width: 600px;
    text-align: left;
    backdrop-filter: blur(10px);
}}

.type2-card h3 {{
    font-size: 2rem;
    margin-bottom: 1rem;
}}

.type2-card p {{
    color: var(--muted);
    line-height: 1.6;
}}

@keyframes autoShow {{
    from {{ 
        opacity: 0; 
        transform: translateY(150px) scale(0.85); 
    }}
    to {{ 
        opacity: 1; 
        transform: translateY(0) scale(1); 
    }}
}}

/* =========================================
   TYPE 3: Focal Blur (Typography)
   Blurs in, sharp at center, blurs out
   ========================================= */
.type3-text {{
    font-size: 5rem;
    font-weight: 800;
    text-transform: uppercase;
    text-align: center;
    line-height: 1.1;
    background: linear-gradient(to bottom right, var(--text), var(--muted));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    max-width: 800px;
}}

@keyframes autoBlur {{
    0% {{ 
        filter: blur(40px); 
        opacity: 0; 
        transform: scale(0.5);
    }}
    45%, 55% {{ 
        filter: blur(0px); 
        opacity: 1; 
        transform: scale(1);
    }}
    100% {{ 
        filter: blur(40px); 
        opacity: 0; 
        transform: scale(1.5);
    }}
}}

/* =========================================
   APPLYING THE SCROLL TIMELINES
   Wrapped in @supports to ensure graceful 
   degradation in Firefox/Safari
   ========================================= */
@supports (animation-timeline: view()) {{
    .type1-visual {{
        animation: autoRotate linear both;
        animation-timeline: view();
    }}

    .type2-card {{
        animation: autoShow linear both;
        /* Start animation when element enters bottom, finish when it reaches 30% from bottom */
        animation-timeline: view(30% auto); 
    }}

    .type3-text {{
        animation: autoBlur linear both;
        animation-timeline: view();
    }}
}}
"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    
    <div class="scroll-container">
        
        <!-- Intro -->
        <section class="hero">
            <h1>{title_text}</h1>
            <p>{body_text}</p>
            <div class="scroll-indicator">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 5v14M19 12l-7 7-7-7"/></svg>
            </div>
        </section>

        <!-- TYPE 1: Continuous Rotation -->
        <section class="section-spacer">
            <p style="margin-bottom: 2rem; color: var(--muted); text-transform: uppercase; letter-spacing: 2px; font-size: 0.8rem;">Type 1: Continuous (view())</p>
            <div class="type1-visual"></div>
        </section>

        <!-- TYPE 2: Reveal & Lock -->
        <section class="section-spacer" style="min-height: 120%;">
            <p style="margin-bottom: 2rem; color: var(--muted); text-transform: uppercase; letter-spacing: 2px; font-size: 0.8rem;">Type 2: Reveal & Stabilize (view(30% auto))</p>
            <div class="type2-card">
                <h3>Design & Developer</h3>
                <p>This element scales up and fades in as it enters the viewport. Once it hits the 30% threshold from the bottom, the animation locks into its 100% keyframe state, allowing it to be easily read.</p>
            </div>
        </section>

        <!-- TYPE 3: Focal Point Blur -->
        <section class="section-spacer" style="min-height: 150%;">
            <p style="margin-bottom: 2rem; color: var(--muted); text-transform: uppercase; letter-spacing: 2px; font-size: 0.8rem;">Type 3: Focal Blur (0% → 45-55% → 100%)</p>
            <h2 class="type3-text">Pure CSS<br>Scroll Magic</h2>
        </section>

        <!-- Footer Spacer -->
        <section class="section-spacer">
            <p style="color: var(--muted);">End of scroll tracking demonstration.</p>
        </section>

    </div>

    <script src="script.js"></script>
</body>
</html>"""

    js = f"""// Component is driven entirely by CSS animation-timeline.
// This JS is included only to log browser support for demonstration purposes.

document.addEventListener('DOMContentLoaded', () => {{
    const supportsScrollTimeline = CSS.supports('animation-timeline: view()');
    
    if (!supportsScrollTimeline) {{
        console.warn("Your browser does not support 'animation-timeline: view()'. The animations have gracefully degraded to static elements.");
        
        // Optional: We could dynamically load a polyfill here, but CSS fallback is safer.
        // const script = document.createElement('script');
        // script.src = 'https://flackr.github.io/scroll-timeline/dist/scroll-timeline.js';
        // document.head.appendChild(script);
    }} else {{
        console.log("CSS Viewport Timelines supported! Enjoy the smooth animations.");
    }}
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
