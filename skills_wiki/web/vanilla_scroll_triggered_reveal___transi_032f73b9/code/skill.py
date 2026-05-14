def create_component(
    output_dir: str,
    title_text: str = "Welcome to tomorrow",
    body_text: str = "Tomorrow isn't just a company, it's a revolution in design.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#e63946",     # Red accent from the tutorial
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Vanilla Scroll-Triggered Reveal Animations effect.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme and accent_color ===
    if color_scheme == "dark":
        bg_color = "#131217"
        text_color = "#ffffff"
        surface_color = "rgba(255, 255, 255, 0.05)"
        subtext_color = "#a0a0a5"
    else:
        bg_color = "#f4f4f6"
        text_color = "#131217"
        surface_color = "rgba(0, 0, 0, 0.05)"
        subtext_color = "#55555c"

    # === CSS ===
    css = f"""/* Vanilla Scroll-Triggered UI Engine */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --text: {text_color};
    --subtext: {subtext_color};
    --accent: {accent_color};
    --surface: {surface_color};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background: var(--bg);
    color: var(--text);
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 100vh;
    overflow: hidden; /* Prevent body scroll, container will handle it */
}}

/* Container respects requested dimensions and enables localized scrolling */
.container {{
    width: var(--width);
    height: var(--height);
    position: relative;
    overflow-y: auto;
    overflow-x: hidden;
    background: var(--bg);
    border: 1px solid var(--surface);
    scroll-behavior: smooth;
}}

/* --- Core Layout Modules --- */
.section {{
    min-height: 80vh;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    padding: 4rem 2rem;
    text-align: center;
}}

.hero-title {{
    font-size: 4rem;
    font-weight: 700;
    line-height: 1.1;
    margin-bottom: 1.5rem;
}}

.hero-title .highlight {{
    color: var(--accent);
    display: inline-block;
    /* Hero Load Animation */
    animation: slideInFade 0.8s cubic-bezier(0.2, 0.8, 0.2, 1) forwards;
    opacity: 0;
    transform: translateX(-60%);
}}

.hero-body {{
    font-size: 1.5rem;
    color: var(--subtext);
    max-width: 600px;
    margin-bottom: 3rem;
}}

/* --- Interactive CTA Button (Transitions) --- */
.cta-button {{
    position: relative;
    padding: 16px 40px;
    font-size: 1.25rem;
    font-weight: 700;
    color: var(--text);
    background: transparent;
    border: 2px solid var(--surface);
    cursor: pointer;
    overflow: hidden;
    z-index: 1;
    transition: color 0.3s ease;
}}

.cta-button::after {{
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    height: 100%;
    width: 0%;
    background-color: var(--accent);
    z-index: -1;
    transition: all 0.3s ease-in-out;
}}

.cta-button:hover::after {{
    width: 100%;
}}

/* --- Scroll Animation Engine Base Classes --- */
.scroll-element {{
    opacity: 0;
    transition: all 0.6s cubic-bezier(0.16, 1, 0.3, 1);
}}

/* Modifiers for different entry directions */
.fade-up {{
    transform: translateY(100px);
}}

.fade-left {{
    transform: translateX(-100px);
}}

.fade-scale {{
    transform: scale(0.8);
}}

/* The active state assigned by JS */
.scroll-element.visible {{
    opacity: 1;
    transform: translate(0) scale(1);
}}

/* Staggered delays for grouped items */
.delay-1 {{ transition-delay: 0.1s; }}
.delay-2 {{ transition-delay: 0.2s; }}
.delay-3 {{ transition-delay: 0.3s; }}

/* --- Keyframes --- */
@keyframes slideInFade {{
    from {{
        opacity: 0;
        transform: translateX(-60%);
    }}
    to {{
        opacity: 1;
        transform: translateX(0);
    }}
}}

/* Content Blocks for Scroll Testing */
.content-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 2rem;
    width: 100%;
    max-width: 900px;
}}

.card {{
    background: var(--surface);
    padding: 3rem 2rem;
    border-radius: 8px;
    text-align: left;
    border-top: 4px solid var(--accent);
}}
.card h3 {{ margin-bottom: 1rem; font-size: 1.5rem; }}
.card p {{ color: var(--subtext); line-height: 1.6; }}
"""

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
    <div class="container" id="scroll-container">
        
        <!-- Hero Section (Keyframes) -->
        <div class="section">
            <h1 class="hero-title">
                {title_text.split()[0] if title_text else "Welcome"} 
                <span class="highlight">{" ".join(title_text.split()[1:]) if len(title_text.split()) > 1 else "Tomorrow"}</span>
            </h1>
            <p class="hero-body">{body_text}</p>
            <button class="cta-button">Order now!</button>
        </div>

        <!-- Scroll Section 1 (Fade Up) -->
        <div class="section">
            <h2 class="hero-title scroll-element fade-up">Innovation at its Core</h2>
            <p class="hero-body scroll-element fade-up delay-1">Scroll down to see the elements reveal themselves seamlessly.</p>
        </div>

        <!-- Scroll Section 2 (Fade Left & Staggered Cards) -->
        <div class="section">
            <div class="content-grid">
                <div class="card scroll-element fade-left">
                    <h3>CSS Transitions</h3>
                    <p>Smoothly interpolate property changes over time, triggered by state changes like hover.</p>
                </div>
                <div class="card scroll-element fade-up delay-1">
                    <h3>Keyframes</h3>
                    <p>Complex, multi-step animations executed instantly on page load or via specific class triggers.</p>
                </div>
                <div class="card scroll-element fade-scale delay-2">
                    <h3>Scroll Triggers</h3>
                    <p>Calculate element bounds in JS to add classes, shifting the animation workload to the GPU.</p>
                </div>
            </div>
        </div>

        <!-- Final CTA Section -->
        <div class="section">
            <h2 class="hero-title scroll-element fade-scale">Ready to build?</h2>
            <div class="scroll-element fade-up delay-1">
                <button class="cta-button">Get Started</button>
            </div>
        </div>

    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Vanilla JS Scroll Animation Engine
document.addEventListener('DOMContentLoaded', () => {{
    // Since we forced the body to not scroll and placed overflow on .container,
    // we attach the scroll event listener to the container.
    const scrollContainer = document.getElementById('scroll-container');
    const scrollElements = document.querySelectorAll('.scroll-element');

    function checkVisibility() {{
        // Use container's bounding rect as the viewport reference
        const containerRect = scrollContainer.getBoundingClientRect();
        const containerHeight = containerRect.height;
        const containerTop = containerRect.top;

        scrollElements.forEach(el => {{
            const elementRect = el.getBoundingClientRect();
            
            // Calculate position relative to the visual container
            // The logic: if the element's top is above the bottom of the container 
            // AND the element's bottom is below the top of the container
            if (
                (elementRect.top - containerTop) < containerHeight - 50 && // 50px offset for nicer reveal timing
                (elementRect.bottom - containerTop) >= 0
            ) {{
                el.classList.add('visible');
            }} 
            // Optional: Remove else block if you only want animations to happen once.
            // Leaving it in creates repeatable scrolling animations (like the tutorial).
            else {{
                el.classList.remove('visible');
            }}
        }});
    }}

    // Listen to container scroll instead of window
    scrollContainer.addEventListener('scroll', checkVisibility);
    
    // Trigger once on load to catch elements already in viewport
    checkVisibility();
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
