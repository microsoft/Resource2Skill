def create_component(
    output_dir: str,
    title_text: str = "Unleash the Power",
    body_text: str = "Our new mobile device combines cutting-edge performance with an E Ink display and a phone-sized design, allowing you to effortlessly slip it into your pocket and carry it on the go.",
    color_scheme: str = "dark",
    accent_color: str = "#ffffff",
    width_px: int = 1000,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Scroll-Driven Text Reveal effect.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    if color_scheme == "dark":
        bg_color = "#0a0a0a"
        text_color = "#ffffff"
        mute_color = "rgba(255, 255, 255, 0.15)"
    else:
        bg_color = "#f4f4f5"
        text_color = "#09090b"
        mute_color = "rgba(9, 9, 11, 0.15)"

    css = f"""/* Scroll-Driven Text Reveal */
:root {{
    --bg: {bg_color};
    --text: {text_color};
    --accent: {accent_color};
    --mute: {mute_color};
    --width: {width_px}px;
}}

* {{
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}}

body {{
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    background-color: var(--bg);
    color: var(--text);
    overflow-x: hidden;
}}

/* Spacer classes just to enable scrolling for the demo */
.spacer {{
    height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    opacity: 0.3;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    font-size: 0.875rem;
}}

.container {{
    max-width: var(--width);
    margin: 0 auto;
    padding: 4rem 2rem;
    min-height: 80vh;
    display: flex;
    flex-direction: column;
    justify-content: center;
}}

.scroll-reveal {{
    display: flex;
    flex-direction: column;
    gap: 2rem;
}}

.scroll-reveal h2 {{
    font-size: clamp(3rem, 6vw, 5rem);
    line-height: 1.1;
    letter-spacing: -0.02em;
}}

.scroll-reveal p {{
    font-size: clamp(1.25rem, 3vw, 2.25rem);
    line-height: 1.4;
    max-width: 45ch;
}}

/* --- Core Technique --- */
.scroll-reveal span {{
    /* Base faded color */
    color: var(--mute);
    /* Modern fallback using color-mix if supported to perfectly match theme */
    color: color-mix(in srgb, var(--text) 20%, transparent);
    
    /* The gradient that will "fill" the text */
    background-image: linear-gradient(90deg, var(--accent), var(--accent));
    background-repeat: no-repeat;
    background-size: 0% 100%;
    
    /* Clip background to text shape */
    -webkit-background-clip: text;
    background-clip: text;
    
    /* Native CSS Scroll-driven Animation */
    animation: text-reveal-anim linear forwards;
    animation-timeline: view();
    /* Starts filling at 15% from bottom of screen, finishes at 50% from bottom */
    animation-range: cover 15% cover 50%;
}}

@keyframes text-reveal-anim {{
    0% {{
        background-size: 0% 100%;
    }}
    100% {{
        background-size: 100% 100%;
    }}
}}

/* Accessibility: Disable animation for users who prefer reduced motion */
@media (prefers-reduced-motion: reduce) {{
    .scroll-reveal span {{
        animation: none;
        background-size: 100% 100%;
    }}
}}
"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Scroll-Driven Text Reveal</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="spacer">Scroll Down &darr;</div>
    
    <main class="container">
        <section class="scroll-reveal">
            <!-- Text must be wrapped in inline spans for the bounding-box fill effect -->
            <h2><span>{title_text}</span></h2>
            <p><span>{body_text}</span></p>
        </section>
    </main>

    <div class="spacer">&uarr; Scroll Up</div>
    
    <script src="script.js"></script>
</body>
</html>"""

    js = f"""// Scroll-Driven Text Reveal — Polyfill / Fallback
document.addEventListener('DOMContentLoaded', () => {{
    const spans = document.querySelectorAll('.scroll-reveal span');
    
    // Respect user accessibility preferences
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {{
        spans.forEach(span => span.style.backgroundSize = '100% 100%');
        return;
    }}

    // Fallback logic for Safari / Browsers lacking CSS animation-timeline support
    if (!CSS.supports('animation-timeline: view()')) {{
        const updateScrollProgress = () => {{
            const windowHeight = window.innerHeight;
            
            spans.forEach(span => {{
                const rect = span.getBoundingClientRect();
                
                // Map the element's position mathematically to the 'cover 15% cover 50%' range
                const start = windowHeight * 0.85; // 15% from the bottom
                const end = windowHeight * 0.50;   // 50% from the bottom
                const current = rect.top;
                
                // Calculate percentage between start and end
                let progress = (start - current) / (start - end);
                
                // Clamp between 0 and 1
                progress = Math.max(0, Math.min(1, progress));
                
                // Apply inline style representing animation progress
                span.style.backgroundSize = `${{progress * 100}}% 100%`;
            }});
        }};
        
        // Listen to scroll events (passive for performance)
        window.addEventListener('scroll', updateScrollProgress, {{ passive: true }});
        
        // Trigger calculation once on load to establish initial state
        updateScrollProgress();
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
