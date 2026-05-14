def create_component(
    output_dir: str,
    title_text: str = "GSAP ScrollTrigger Magic",
    body_text: str = "Keep scrolling down to pin the container and scrub the timeline.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#ff9900",     # CSS hex color for active state
    width_px: int = 1000,
    height_px: int = 700,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the GSAP Scroll-Scrubbed Pinned Animation.
    
    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme and accent_color ===
    if color_scheme == "dark":
        bg_color = "#121212"
        text_color = "#ffffff"
        surface_color = "#1e1e1e"
        box_color = "#f0f0f0"
        box_text = "#121212"
    else:
        bg_color = "#f5f5f7"
        text_color = "#1d1d1f"
        surface_color = "#ffffff"
        box_color = "#1d1d1f"
        box_text = "#ffffff"

    # === CSS ===
    css = f"""/* GSAP Scroll-Scrubbed Pinned Animation */
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
    --box-bg: {box_color};
    --box-text: {box_text};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background: var(--bg);
    color: var(--text);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    /* We handle scrolling inside .container to keep the component isolated */
    overflow: hidden; 
}}

/* The main scrollable viewport for our component */
.container {{
    width: var(--width);
    height: var(--height);
    overflow-y: auto;
    overflow-x: hidden;
    position: relative;
    border-radius: 16px;
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
    background: var(--bg);
    border: 1px solid rgba(128, 128, 128, 0.1);
}}

/* Spacer sections to give us room to scroll */
.space {{
    min-height: 120%; /* 1.2x container height to force scrolling */
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    padding: 2rem;
}}

.title {{
    font-size: 2.5rem;
    font-weight: 700;
    letter-spacing: -0.02em;
    margin-bottom: 1rem;
}}

.body-text {{
    font-size: 1.125rem;
    opacity: 0.7;
    max-width: 500px;
    line-height: 1.6;
}}

.scroll-indicator {{
    margin-top: 3rem;
    font-size: 2rem;
    color: var(--accent);
    animation: bounce 2s infinite ease-in-out;
}}

@keyframes bounce {{
    0%, 20%, 50%, 80%, 100% {{ transform: translateY(0); }}
    40% {{ transform: translateY(-20px); }}
    60% {{ transform: translateY(-10px); }}
}}

/* The section that will be pinned */
.stack {{
    height: 100%; /* Matches container height so it fits perfectly when pinned */
    display: flex;
    align-items: center;
    justify-content: center;
    background: var(--surface);
    position: relative;
    border-top: 1px solid rgba(128, 128, 128, 0.1);
    border-bottom: 1px solid rgba(128, 128, 128, 0.1);
}}

/* The animated element */
.box {{
    width: 120px;
    height: 120px;
    background: var(--box-bg);
    color: var(--box-text);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 3rem;
    font-weight: 800;
    border-radius: 20px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.15);
    
    /* Native CSS transition for the toggleClass color shift */
    transition: background-color 0.4s ease, color 0.4s ease, box-shadow 0.4s ease;
    will-change: transform;
    z-index: 10;
}}

/* The state triggered by GSAP ScrollTrigger toggleClass */
.box.active {{
    background-color: var(--accent);
    color: #ffffff;
    box-shadow: 0 0 40px var(--accent);
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
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    
    <!-- Isolated Scrolling Context -->
    <div class="container">
        
        <!-- Entry space -->
        <section class="space">
            <h1 class="title">{title_text}</h1>
            <p class="body-text">{body_text}</p>
            <div class="scroll-indicator">↓</div>
        </section>
        
        <!-- The Pinned Section -->
        <section class="stack">
            <div class="box" aria-hidden="true">A</div>
        </section>
        
        <!-- Exit space -->
        <section class="space">
            <h2 class="title">Animation Complete</h2>
            <p class="body-text">Scroll back up to automatically reverse the timeline smoothly.</p>
        </section>
        
    </div>

    <!-- GSAP Core & ScrollTrigger Plugin CDN -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/gsap.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/ScrollTrigger.min.js"></script>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Register the plugin before using it
gsap.registerPlugin(ScrollTrigger);

document.addEventListener('DOMContentLoaded', () => {{
    
    // We target our specific container as the scroller instead of the window
    const scrollerSelector = ".container";
    
    // Create a GSAP Timeline hooked to the scroll position
    const mainTimeline = gsap.timeline({{
        scrollTrigger: {{
            trigger: ".stack",             // The element that dictates the start/end points
            scroller: scrollerSelector,    // The element with overflow-y: auto
            pin: true,                     // Locks the trigger element in place
            start: "center center",        // Starts when trigger center hits viewport center
            end: "+=200%",                 // Keeps it pinned for a scroll distance = 2x container height
            scrub: 1,                      // Smooth scrubbing (takes 1 sec to catch up to scroll bar)
            toggleClass: {{                // Dynamically applies class when between start and end
                targets: ".box", 
                className: "active"
            }},
            markers: false                 // Set to true for debugging lines
        }}
    }});

    // Build the sequential animation
    // Each step gets an equal fraction of the scroll distance automatically
    const moveDist = 150; 
    
    mainTimeline
        .to(".box", {{ rotation: 90, x: moveDist, duration: 1 }})       // Move Right & Turn
        .to(".box", {{ rotation: 180, y: moveDist, duration: 1 }})      // Move Down & Turn
        .to(".box", {{ rotation: 270, x: -moveDist, duration: 1 }})     // Move Left & Turn
        .to(".box", {{ rotation: 360, x: 0, y: 0, duration: 1 }});      // Move Up (Back to origin) & Turn

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
