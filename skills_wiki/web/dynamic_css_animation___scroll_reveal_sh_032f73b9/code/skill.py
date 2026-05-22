def create_component(
    output_dir: str,
    title_text: str = "CSS Animation Showcase",
    body_text: str = "Explore key CSS animation and transition techniques, plus scroll-triggered effects.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#cc3f4e",     # CSS hex color for accent (red from video example)
    width_px: int = 1200,              # Max width for main content
    height_px: int = 800,              # Minimum viewport height (content will scroll)
    **kwargs,
) -> dict:
    """
    Create a web component demonstrating CSS animations, transforms, transitions,
    and scroll-triggered effects as shown in the video tutorial.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme and accent_color ===
    if color_scheme == "dark":
        bg_color = "#131217" # Dark grey from spinner example in video
        text_color = "#ffffff"
        surface_color = "rgba(255, 255, 255, 0.1)"
    else:
        bg_color = "#f8f9fa"
        text_color = "#1a1a2e"
        surface_color = "rgba(0, 0, 0, 0.1)"

    # === CSS ===
    css = f"""
/* CSS Animation Showcase – generated component */
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
    --component-size: 150px; /* Unified size for spinner and transform box */
    --main-content-width: {width_px}px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background: var(--bg);
    color: var(--text);
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: flex-start;
    padding: 40px 20px;
    line-height: 1.6;
    overflow-x: hidden; /* Prevent horizontal scroll from transforms */
}}

h1 {{
    font-size: 2.8em;
    margin-bottom: 20px;
    text-align: center;
    max-width: var(--main-content-width);
}}

p {{
    font-size: 1.1em;
    margin-bottom: 40px;
    text-align: center;
    max-width: 800px;
}}

.section-title {{
    font-size: 2em;
    margin-top: 80px;
    margin-bottom: 30px;
    color: var(--accent);
    text-align: center;
    width: 100%;
    max-width: var(--main-content-width);
}}

/* --- Spinner Animation Section --- */
.spinner-container {{
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 300px; /* Space for the spinner */
    margin-bottom: 80px;
    width: 100%;
    max-width: var(--main-content-width);
}}

.spinner {{
    width: var(--component-size);
    height: var(--component-size);
    border: 15px solid var(--surface); /* Thinner border for cleaner look */
    border-top: 15px solid var(--accent);
    border-radius: 50%;
    animation: spin-color 3s linear infinite; /* 3s duration, linear, infinite */
}}

@keyframes spin-color {{
    0% {{ transform: rotate(0deg); border-top-color: var(--accent); }}
    25% {{ border-top-color: #ff0000; /* Red */ }}
    50% {{ border-top-color: #ffff00; /* Yellow */ }}
    75% {{ border-top-color: #00ff00; /* Green */ }}
    100% {{ transform: rotate(360deg); border-top-color: var(--accent); }}
}}

/* --- Transform & Transition Section --- */
.transform-box-container {{
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 300px;
    margin-bottom: 80px;
    width: 100%;
    max-width: var(--main-content-width);
}}

.transform-box {{
    width: var(--component-size);
    height: var(--component-size);
    background-color: var(--accent);
    transition: transform 0.4s ease-in-out, background-color 0.4s ease-in-out;
}}

.transform-box:hover {{
    transform: scale(1.2) rotate(45deg);
    background-color: #5aa469; /* A different color on hover */
}}

/* --- Scroll Reveal Section --- */
.scroll-reveal-container {{
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 50px 0;
    margin-bottom: 100vh; /* Ensure enough scroll space */
    width: 100%;
    max-width: var(--main-content-width);
}}

.scroll-reveal-item {{
    opacity: 0;
    transform: translateY(50px);
    transition: opacity 0.8s cubic-bezier(0.25, 0.46, 0.45, 0.94), transform 0.8s cubic-bezier(0.25, 0.46, 0.45, 0.94);
    margin: 20px 0;
    text-align: center;
    max-width: 800px; /* Constrain width of content items */
}}

.scroll-reveal-item.visible {{
    opacity: 1;
    transform: translateY(0);
}}

.scroll-reveal-item h2 {{
    font-size: 2.2em;
    margin-bottom: 15px;
    color: var(--text);
}}

.scroll-reveal-item p {{
    font-size: 1em;
    color: var(--text);
    margin-bottom: 0; /* Override default p margin-bottom */
}}

.scroll-reveal-image {{
    width: 300px;
    height: auto;
    max-width: 100%;
    border-radius: 8px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.2);
}}

/* Just for making more scrollable content */
.placeholder-space {{
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 2em;
    color: var(--surface);
    margin: 100px 0;
    max-width: var(--main-content-width);
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
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <h1>{title_text}</h1>
    <p>{body_text}</p>

    <h2 class="section-title">CSS Keyframe Animation (Spinner)</h2>
    <div class="spinner-container">
        <div class="spinner"></div>
    </div>

    <h2 class="section-title">CSS Transform & Transition (Hover Effect)</h2>
    <div class="transform-box-container">
        <div class="transform-box"></div>
    </div>

    <div class="placeholder-space">Scroll down to reveal content!</div>

    <h2 class="section-title">Scroll-Triggered Reveal (JS + CSS)</h2>
    <div class="scroll-reveal-container">
        <div class="scroll-reveal-item">
            <h2>Dynamic Content Loading</h2>
            <p>This content block elegantly fades in and slides up as it enters the viewport, enhancing the user experience with a subtle yet impactful visual effect. It makes the page feel alive and responsive to user interaction.</p>
        </div>
        <div class="scroll-reveal-item">
            <img src="https://via.placeholder.com/300/CCCCCC/FFFFFF?text=Scroll+Image" alt="Placeholder image" class="scroll-reveal-image">
        </div>
        <div class="scroll-reveal-item">
            <h2>Engaging Visuals</h2>
            <p>Pairing text with images that animate on scroll creates a narrative flow, guiding the user's attention through your story or product features seamlessly. Try it out!</p>
        </div>
    </div>

    <div class="placeholder-space">The end of the showcase.</div>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""
// CSS Animation Showcase – interactive behavior
document.addEventListener('DOMContentLoaded', () => {{
    const scrollRevealItems = document.querySelectorAll('.scroll-reveal-item');

    const observerOptions = {{
        root: null, // Use the viewport as the root
        rootMargin: '0px',
        threshold: 0.2 // Trigger when 20% of the item is visible
    }};

    const observer = new IntersectionObserver((entries, observer) => {{
        entries.forEach(entry => {{
            if (entry.isIntersecting) {{
                entry.target.classList.add('visible');
                // Optional: Stop observing once the animation has played
                // observer.unobserve(entry.target);
            }} else {{
                // Optional: Remove 'visible' class if item scrolls out of view
                // entry.target.classList.remove('visible');
            }}
        }});
    }}, observerOptions);

    scrollRevealItems.forEach(item => {{
        observer.observe(item);
    }});
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

