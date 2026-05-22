def create_component(
    output_dir: str,
    title_text: str = "Scroll Animation Article",
    body_text: str = "Scroll down to see native CSS animations in action. No JavaScript is required for these effects.",
    color_scheme: str = "dark",
    accent_color: str = "#00bfff",
    width_px: int = 800,
    height_px: int = 1000,
    **kwargs,
) -> dict:
    import os

    os.makedirs(output_dir, exist_ok=True)

    if color_scheme == "dark":
        bg_color = "#121212"
        text_color = "#e0e0e0"
        surface_color = "#1e1e1e"
    else:
        bg_color = "#ffffff"
        text_color = "#333333"
        surface_color = "#f5f5f5"

    css = f"""/* Native CSS Scroll Animations */
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
}}

body {{
    font-family: 'Inter', system-ui, sans-serif;
    background-color: var(--bg);
    color: var(--text);
    line-height: 1.8;
}}

/* Set up the root scroll timeline for the progress bar */
html {{
    scroll-timeline-name: --page-scroll;
    scroll-timeline-axis: y;
}}

.progress-bar {{
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 6px;
    background-color: var(--accent);
    transform-origin: 0 50%;
    z-index: 100;
    /* Connect to the page scroll timeline */
    animation: progress-anim linear;
    animation-timeline: --page-scroll;
}}

@keyframes progress-anim {{
    from {{ transform: scaleX(0); }}
    to {{ transform: scaleX(1); }}
}}

main {{
    max-width: {width_px}px;
    margin: 0 auto;
    padding: 60px 20px 100vh 20px; /* Extra padding at bottom to allow scrolling */
}}

h1 {{
    font-size: 3rem;
    margin-bottom: 0.5em;
    color: var(--text);
}}

h2 {{
    font-size: 2rem;
    margin: 2em 0 1em;
    border-bottom: 2px solid var(--surface);
    padding-bottom: 0.5em;
}}

p {{
    font-size: 1.125rem;
    margin-bottom: 1.5em;
    color: var(--text);
    opacity: 0.9;
}}

.placeholder-text {{
    margin-bottom: 300px; /* Force scrolling space */
}}

.image-container {{
    width: 100%;
    height: 400px;
    background: var(--surface);
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 40px 0;
    overflow: hidden;
    position: relative;
    border: 1px solid rgba(255, 255, 255, 0.1);
}}

.image-container::after {{
    content: 'Image Placeholder';
    color: var(--text);
    opacity: 0.5;
    font-size: 1.5rem;
    font-weight: 600;
}}

ul {{
    list-style: none;
    padding-left: 1rem;
}}

li {{
    font-size: 1.25rem;
    margin-bottom: 1rem;
    padding-left: 1.5rem;
    position: relative;
}}

li::before {{
    content: '•';
    color: var(--accent);
    font-weight: bold;
    font-size: 1.5rem;
    position: absolute;
    left: 0;
    top: -4px;
}}

/* === VIEW TIMELINE ANIMATIONS === */

/* Feature detection: Only apply starting hidden states if the browser supports view-timeline */
@supports (animation-timeline: view()) {{
    .reveal-img {{
        opacity: 0;
        view-timeline-name: --revealing-image;
        view-timeline-axis: y;
        animation: appear linear forwards;
        animation-timeline: --revealing-image;
        animation-range: entry 10% cover 40%;
    }}

    .slide-list li {{
        opacity: 0;
        /* Using the shorthand view() function instead of named timelines for the list items */
        animation: fadeLeft linear forwards;
        animation-timeline: view();
        animation-range: entry 10% cover 30%;
    }}
}}

@keyframes appear {{
    from {{
        opacity: 0;
        transform: scale(0.5);
    }}
    to {{
        opacity: 1;
        transform: scale(1);
    }}
}}

@keyframes fadeLeft {{
    from {{
        opacity: 0;
        transform: translateX(-100px);
    }}
    to {{
        opacity: 1;
        transform: translateX(0);
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
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="progress-bar"></div>

    <main>
        <h1>{title_text}</h1>
        <p><strong>Note:</strong> To see these effects, use Chrome/Edge 115+ or a compatible browser. In unsupported browsers, content will degrade gracefully and remain visible.</p>
        <p>{body_text}</p>
        
        <p class="placeholder-text">
            Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.
            <br><br>
            Keep scrolling down...
        </p>

        <h2>Scale Reveal Effect</h2>
        <p>This image container will scale up and fade in as it enters the viewport based on its own view timeline.</p>
        
        <div class="image-container reveal-img"></div>

        <p class="placeholder-text">
            Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum. Curabitur pretium tincidunt lacus. Nulla gravida orci a odio.
            <br><br>
            Keep scrolling down...
        </p>

        <h2>Sequential Slide Reveal</h2>
        <p>Each list item is linked to its own view timeline, causing them to slide in individually as they cross the threshold.</p>
        
        <ul class="slide-list">
            <li>First item sliding in from the left</li>
            <li>Second item follows as you scroll</li>
            <li>Third item appearing smoothly</li>
            <li>Fourth item completing the list</li>
            <li>Fifth item just to be sure</li>
        </ul>
        
        <p style="margin-top: 100px; text-align: center; opacity: 0.5;">End of Demo</p>
    </main>

    <script src="script.js"></script>
</body>
</html>"""

    js = """// No JavaScript required for these scroll animations!
// The effects are handled entirely by CSS animation-timeline properties.
console.log('Scroll animations initialized via CSS.');
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
