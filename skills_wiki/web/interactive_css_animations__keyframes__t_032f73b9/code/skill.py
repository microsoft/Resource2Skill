import os

def create_component(
    output_dir: str,
    title_text: str = "CSS Animation Guide",
    body_text: str = "Unlock the power of CSS animations with keyframes, transforms, and transitions.",
    color_scheme: str = "dark",  # "dark" or "light"
    accent_color: str = "#E74C3C",  # CSS hex color for accent (e.g., Red)
    width_px: int = 1200,
    height_px: int = 800, # This height will be minimal, content will make it scrollable
    **kwargs,
) -> dict:
    """
    Create a web component demonstrating CSS animations (keyframes, transforms, transitions, scroll-animations).

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme and accent_color ===
    if color_scheme == "dark":
        bg_color = "#131217" # Dark background from video
        text_color = "#f0f0f0"
        surface_color = "rgba(255, 255, 255, 0.1)"
        spinner_border_color = "white"
        hover_bg_color = "#C0392B" # Darker accent for hover
        complex_bg_color_25 = "#E67E22" # Orange
        complex_bg_color_50 = "#F1C40F" # Yellow
        complex_bg_color_75 = "#2ECC71" # Green
    else: # Light scheme
        bg_color = "#f8f9fa"
        text_color = "#1a1a2e"
        surface_color = "rgba(0, 0, 0, 0.1)"
        spinner_border_color = "#333"
        hover_bg_color = "#CB4335" # Slightly darker red
        complex_bg_color_25 = "#FF8C00" # Dark orange
        complex_bg_color_50 = "#FFD700" # Gold
        complex_bg_color_75 = "#32CD32" # Lime Green

    # === CSS ===
    css = f"""/* CSS Animation Guide — generated component */
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
    --spinner-border: {spinner_border_color};
    --hover-bg: {hover_bg_color};
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
    padding: 40px;
    gap: 80px;
    overflow-x: hidden; /* Prevent horizontal scroll from transforms */
    max-width: {width_px}px; /* Constrain overall width */
    margin: 0 auto;
}}

h1, h2 {{
    text-align: center;
    margin-bottom: 20px;
}}

p {{
    text-align: center;
    max-width: 800px;
    line-height: 1.6;
}}

.section {{
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 20px;
    width: 100%;
    padding: 40px 0;
    border-bottom: 1px dashed var(--surface);
}}

.section:last-child {{
    border-bottom: none;
}}

/* === Keyframes & Spinner Animation === */
.spinner-container {{
    display: grid;
    place-content: center;
    height: 200px;
    width: 200px;
    /* background-color: transparent; */ /* Removed to ensure visibility */
    border-radius: 50%;
    margin-bottom: 40px;
}}

.spinner {{
    width: 100px;
    height: 100px;
    border: 10px solid var(--spinner-border);
    border-bottom-color: transparent; /* Makes it a C-shape */
    border-radius: 50%;
    animation: spin 3s linear infinite;
}}

@keyframes spin {{
    0% {{
        transform: rotate(0deg);
        border-color: var(--spinner-border) transparent transparent transparent;
    }}
    25% {{ /* Example from video changing border colors */
        border-color: {accent_color} var(--spinner-border) transparent transparent;
    }}
    50% {{
        border-color: transparent {accent_color} var(--spinner-border) transparent;
    }}
    75% {{
        border-color: transparent transparent {accent_color} var(--spinner-border);
    }}
    100% {{
        transform: rotate(360deg);
        border-color: var(--spinner-border) transparent transparent transparent;
    }}
}}

/* === Transform Property Demonstration === */
.transform-box {{
    width: 150px;
    height: 150px;
    background-color: var(--accent);
    display: grid;
    place-content: center;
    font-weight: bold;
    color: var(--text);
    transition: transform 0.4s ease-in-out, background-color 0.4s ease-in-out;
    will-change: transform, background-color;
}}

.transform-box.scaled:hover {{
    transform: scale(1.2);
}}

.transform-box.rotated:hover {{
    transform: rotate(135deg);
}}

.transform-box.translated:hover {{
    transform: translate(50px, 50px);
}}

.transform-box.skewed:hover {{
    transform: skew(20deg, 10deg);
}}

.transform-box.complex {{
    animation: complexTransform 4s infinite alternate ease-in-out;
}}

@keyframes complexTransform {{
    0% {{
        transform: translate(0, 0) rotate(0deg) scale(1);
        background-color: {accent_color};
    }}
    25% {{
        transform: translate(50px, -20px) rotate(45deg) scale(1.1);
        background-color: {complex_bg_color_25};
    }}
    50% {{
        transform: translate(0, 50px) rotate(90deg) scale(0.9);
        background-color: {complex_bg_color_50};
    }}
    75% {{
        transform: translate(-50px, -20px) rotate(135deg) scale(1.1);
        background-color: {complex_bg_color_75};
    }}
    100% {{
        transform: translate(0, 0) rotate(180deg) scale(1);
        background-color: {accent_color};
    }}
}}

/* === Transition Property Demonstration === */
.transition-button {{
    padding: 12px 24px;
    font-size: 1.1rem;
    font-weight: 600;
    background-color: var(--accent);
    color: var(--text);
    border: none;
    border-radius: 8px;
    cursor: pointer;
    transition: background-color 0.3s ease-in-out, transform 0.3s ease-in-out, box-shadow 0.3s ease-in-out;
    will-change: background-color, transform, box-shadow; /* Performance hint */
}}

.transition-button:hover {{
    background-color: var(--hover-bg); /* Darker accent */
    transform: translateY(-3px) scale(1.05);
    box-shadow: 0 8px 16px rgba(0, 0, 0, 0.3);
}}

/* === Scroll Animation === */
.scroll-element {{
    width: 250px;
    height: 250px;
    background-color: var(--accent);
    border-radius: 12px;
    opacity: 0;
    transform: translateY(50px); /* Start slightly below */
    transition: opacity 0.6s cubic-bezier(0.25, 0.46, 0.45, 0.94), transform 0.6s cubic-bezier(0.25, 0.46, 0.45, 0.94); /* ease-out-quad */
    will-change: opacity, transform;
}}

.scroll-element.visible {{
    opacity: 1;
    transform: translateY(0);
}}

/* Utility for spacing in the demo */
.spacer {{
    height: 400px; /* To allow scrolling */
    background: repeating-linear-gradient(
        45deg,
        var(--bg),
        var(--bg) 10px,
        rgba(255, 255, 255, 0.05) 10px,
        rgba(255, 255, 255, 0.05) 20px
    );
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--text);
    font-weight: bold;
    font-size: 1.5rem;
    margin: 60px 0;
    border-radius: 8px;
}}

/* For scroll demo elements below the fold */
.scroll-container {{
    min-height: 120vh; /* Ensure enough height for scrolling */
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 40px;
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
    <div class="section">
        <h1>{title_text}</h1>
        <p>{body_text}</p>
        <h2>Keyframes & Spinner Animation</h2>
        <p>Using <code>@keyframes</code> to define complex animations with multiple intermediate steps, like this color-changing spinner that rotates and changes border colors over 3 seconds, looping infinitely.</p>
        <div class="spinner-container">
            <div class="spinner"></div>
        </div>
    </div>

    <div class="section">
        <h2>Transform Property</h2>
        <p>The <code>transform</code> property allows moving, scaling, rotating, and skewing elements in 2D or 3D space. Hover over the boxes to see individual transforms, or observe the complex animated box combining multiple transforms.</p>
        <div style="display: flex; gap: 20px; flex-wrap: wrap; justify-content: center;">
            <div class="transform-box scaled">Scale</div>
            <div class="transform-box rotated">Rotate</div>
            <div class="transform-box translated">Translate</div>
            <div class="transform-box skewed">Skew</div>
            <div class="transform-box complex">Complex</div>
        </div>
    </div>

    <div class="section">
        <h2>Transition Property</h2>
        <p>CSS transitions provide a way to control animation speed when changing CSS properties. They are perfect for simpler, state-based animations, like changing a button's appearance on hover.</p>
        <button class="transition-button">Hover Me!</button>
    </div>

    <div class="section scroll-container">
        <h2>Scroll-Triggered Animation</h2>
        <p>Elements appear with a smooth fade-in and slide-up effect as they enter the viewport, creating a more engaging and dynamic scrolling experience.</p>
        <div class="spacer">Scroll Down</div>
        <div class="scroll-element"></div>
        <div class="spacer">Keep Scrolling</div>
        <div class="scroll-element"></div>
        <div class="spacer">Almost There</div>
        <div class="scroll-element"></div>
    </div>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = """// Scroll Animation Logic using IntersectionObserver
document.addEventListener('DOMContentLoaded', () => {
    const scrollElements = document.querySelectorAll('.scroll-element');

    const observerOptions = {
        root: null, // viewport
        rootMargin: '0px',
        threshold: 0.4 // Trigger when 40% of the element is visible
    };

    const observer = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
            } else {
                // Optionally remove 'visible' class if element scrolls out of view
                // entry.target.classList.remove('visible');
            }
        });
    }, observerOptions);

    scrollElements.forEach(el => {
        observer.observe(el);
    });
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
