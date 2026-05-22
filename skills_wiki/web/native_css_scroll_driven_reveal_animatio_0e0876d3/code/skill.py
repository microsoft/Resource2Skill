def create_component(
    output_dir: str,
    title_text: str = "Native CSS Scroll Animations",
    body_text: str = "Scroll down to see the blocks animate entirely via CSS animation-timeline.",
    color_scheme: str = "light",        
    accent_color: str = "#4b7bec",     
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the pure CSS View Timeline scroll animations.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors ===
    if color_scheme == "dark":
        bg_color = "#111418"
        text_color = "#f0f0f0"
        shadow = "rgba(0, 0, 0, 0.5)"
    else:
        bg_color = "#fafafa"
        text_color = "#1a1a2e"
        shadow = "rgba(0, 0, 0, 0.12)"

    # === CSS ===
    css = f"""/* CSS Scroll-Driven Animations Component */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --text: {text_color};
    --shadow: {shadow};
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background: var(--bg);
    color: var(--text);
    overflow-x: hidden;
}}

.hero {{
    height: 80vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    padding: 2rem;
}}

.hero h1 {{
    font-size: 3rem;
    margin-bottom: 1rem;
    letter-spacing: -0.05em;
}}

.hero p {{
    font-size: 1.2rem;
    opacity: 0.8;
}}

.view-container {{
    max-width: {width_px}px;
    margin: 0 auto;
    padding: 2rem;
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 2rem;
    padding-bottom: 20vh;
}}

.block {{
    border-radius: 12px;
    box-shadow: 0 10px 30px var(--shadow);
    /* Set up the native CSS scroll animation linkage */
    animation-timeline: view();
    /* Start exactly on entry, finish when 40% into the viewport */
    animation-range: entry 0% cover 40%;
    /* linear easing feels best when scrubbing with scroll */
    animation-timing-function: linear; 
    animation-fill-mode: both;
}}

/* Fallback for browsers that don't support animation-timeline yet */
@supports not (animation-timeline: view()) {{
    .block {{
        animation: none !important;
        opacity: 1 !important;
        transform: none !important;
        clip-path: none !important;
    }}
    .warning-banner {{
        display: block !important;
        background: #ffb142;
        color: #000;
        text-align: center;
        padding: 10px;
        font-weight: bold;
    }}
}}

.warning-banner {{ display: none; }}

/* --- Animation Variations --- */

/* 1. Scale and Fade (Primary example from tutorial) */
@keyframes appear {{
    from {{
        opacity: 0;
        scale: 0.5;
    }}
    to {{
        opacity: 1;
        scale: 1;
    }}
}}
.anim-appear {{
    animation-name: appear;
}}

/* 2. Slide from side */
@keyframes slide-in {{
    from {{
        opacity: 0;
        transform: translateX(-150px);
    }}
    to {{
        opacity: 1;
        transform: translateX(0);
    }}
}}
.anim-slide {{
    animation-name: slide-in;
}}

/* 3. Clip Path reveal */
@keyframes reveal-clip {{
    from {{
        opacity: 0.2;
        clip-path: inset(100% 0 0 0);
    }}
    to {{
        opacity: 1;
        clip-path: inset(0 0 0 0);
    }}
}}
.anim-reveal {{
    animation-name: reveal-clip;
}}

/* A user-preferred motion check to be accessible */
@media (prefers-reduced-motion: reduce) {{
    .block {{
        animation: none !important;
    }}
}}
"""

    # Generate a static grid of colorful blocks
    blocks_data = [
        {"w": 300, "h": 200, "c": "#ff7979", "a": "appear"},
        {"w": 400, "h": 250, "c": "#4834d4", "a": "slide"},
        {"w": 250, "h": 350, "c": "#6ab04c", "a": "reveal"},
        {"w": 500, "h": 150, "c": "#f0932b", "a": "appear"},
        {"w": 350, "h": 350, "c": "#be2edd", "a": "slide"},
        {"w": 200, "h": 200, "c": "#22a6b3", "a": "appear"},
        {"w": 450, "h": 200, "c": "#eb4d4b", "a": "reveal"},
        {"w": 300, "h": 300, "c": "#f9ca24", "a": "slide"},
        {"w": 250, "h": 150, "c": "#686de0", "a": "appear"},
    ]
    
    blocks_html = ""
    for b in blocks_data:
        blocks_html += f'        <div class="block anim-{b["a"]}" style="width: {b["w"]}px; height: {b["h"]}px; background-color: {b["c"]};"></div>\n'

    # === HTML ===
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="warning-banner">
        Note: Your browser does not support CSS animation-timeline yet. You are seeing the static fallback. Use Chrome/Edge 115+ to see the effect.
    </div>

    <main>
        <section class="hero">
            <h1>{title_text}</h1>
            <p>{body_text}</p>
            <p style="margin-top: 2rem; font-size: 0.9rem; opacity: 0.6;">(Scroll down 👇)</p>
        </section>

        <section class="view-container">
{blocks_html}
        </section>
    </main>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    # No JS required for the core effect, kept empty to prove the CSS concept.
    js = f"""// CSS View Timeline handles the logic. 
// No JavaScript is needed for the scroll tracking or intersection observation!

document.addEventListener('DOMContentLoaded', () => {{
    console.log("Component loaded. Checking for CSS animation-timeline support...");
    if (!CSS.supports('animation-timeline: view()')) {{
        console.warn("CSS animation-timeline is not supported in this browser. Showing static fallback.");
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
