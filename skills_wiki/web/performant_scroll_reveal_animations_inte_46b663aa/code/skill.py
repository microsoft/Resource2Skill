def create_component(
    output_dir: str,
    title_text: str = "Scroll Reveal Magic",
    body_text: str = "Scroll down to see the Intersection Observer in action. Elements fade, slide, and scale as they enter the viewport.",
    color_scheme: str = "dark",
    accent_color: str = "#8a2be2",
    width_px: int = 1000,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Performant Scroll-Reveal Animations visual effect.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Derived theme colors
    if color_scheme == "dark":
        bg_color = "#0f172a"
        text_color = "#f8fafc"
        surface_color = "rgba(255, 255, 255, 0.05)"
        border_color = "rgba(255, 255, 255, 0.1)"
        text_muted = "#94a3b8"
    else:
        bg_color = "#f1f5f9"
        text_color = "#0f172a"
        surface_color = "#ffffff"
        border_color = "rgba(0, 0, 0, 0.08)"
        text_muted = "#64748b"

    # Generate grid items HTML programmatically to ensure we have enough to scroll
    cards_html = ""
    effects = ["fade-up", "fade-left", "fade-right", "zoom-in"]
    for i in range(1, 21):
        # Rotate through the different animation classes
        effect = effects[i % len(effects)]
        cards_html += f"""
        <div class="card hidden {effect}">
            <div class="card-icon" style="background: {accent_color}22; color: {accent_color};">
                {i}
            </div>
            <h3>Module Item {i}</h3>
            <p>Animated via IntersectionObserver using the <code>{effect}</code> CSS transition class.</p>
        </div>
        """

    css = f"""/* Performant Scroll-Reveal Animations */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --text: {text_color};
    --text-muted: {text_muted};
    --accent: {accent_color};
    --surface: {surface_color};
    --border: {border_color};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background: #000; /* Darker backdrop to frame the component */
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 100vh;
}}

/* The main bounded container to emulate a specific resolution/window */
.component-wrapper {{
    width: 100%;
    max-width: var(--width);
    height: var(--height);
    background: var(--bg);
    color: var(--text);
    overflow-y: auto; /* Required to allow scrolling within the defined height */
    overflow-x: hidden;
    position: relative;
    border-radius: 12px;
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
    scroll-behavior: smooth;
}}

.hero {{
    text-align: center;
    padding: 100px 20px;
    min-height: 60vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    border-bottom: 1px solid var(--border);
}}

.hero h1 {{
    font-size: 3.5rem;
    font-weight: 800;
    margin-bottom: 1rem;
    letter-spacing: -0.05em;
    background: linear-gradient(135deg, var(--text), var(--accent));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}}

.hero p {{
    font-size: 1.25rem;
    color: var(--text-muted);
    max-width: 600px;
    line-height: 1.6;
}}

.hero .scroll-indicator {{
    margin-top: 3rem;
    width: 30px;
    height: 50px;
    border: 2px solid var(--text-muted);
    border-radius: 20px;
    position: relative;
    opacity: 0.7;
}}

.hero .scroll-indicator::before {{
    content: '';
    position: absolute;
    top: 8px;
    left: 50%;
    transform: translateX(-50%);
    width: 6px;
    height: 6px;
    background: var(--accent);
    border-radius: 50%;
    animation: scroll-bob 2s infinite cubic-bezier(0.4, 0, 0.2, 1);
}}

@keyframes scroll-bob {{
    0% {{ transform: translate(-50%, 0); opacity: 1; }}
    100% {{ transform: translate(-50%, 20px); opacity: 0; }}
}}

.grid-container {{
    padding: 80px 40px;
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 2rem;
    max-width: 1200px;
    margin: 0 auto;
}}

/* === The Card Style === */
.card {{
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 30px;
    display: flex;
    flex-direction: column;
    gap: 1rem;
}}

.card-icon {{
    width: 48px;
    height: 48px;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.25rem;
    font-weight: 700;
    margin-bottom: 0.5rem;
}}

.card h3 {{
    font-size: 1.5rem;
    font-weight: 600;
}}

.card p {{
    color: var(--text-muted);
    line-height: 1.5;
    font-size: 0.95rem;
}}

/* ========================================================= */
/* === INTERSECTION OBSERVER ANIMATION CLASSES (THE SKILL) === */
/* ========================================================= */

/* Base hidden state and transition definitions */
.hidden {{
    opacity: 0;
    transition: all 0.8s cubic-bezier(0.25, 0.46, 0.45, 0.94);
}}

/* Hardware acceleration hint */
.hidden {{
    will-change: opacity, transform;
}}

/* Different types of starting positions */
.fade-up {{
    transform: translateY(50px);
}}

.fade-left {{
    transform: translateX(-50px);
}}

.fade-right {{
    transform: translateX(50px);
}}

.zoom-in {{
    transform: scale(0.85);
}}

/* The active state applied by JavaScript */
.show {{
    opacity: 1;
    transform: translate(0) scale(1);
}}

/* Respect user's system preferences for reduced motion */
@media (prefers-reduced-motion: reduce) {{
    .hidden {{
        transition: none;
        opacity: 1;
        transform: none;
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
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="component-wrapper" id="scroll-root">
        <header class="hero hidden fade-up">
            <h1>{title_text}</h1>
            <p>{body_text}</p>
            <div class="scroll-indicator"></div>
        </header>

        <main class="grid-container">
            {cards_html}
        </main>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    js = f"""// Performant Scroll-Reveal Animations using IntersectionObserver

document.addEventListener('DOMContentLoaded', () => {{
    
    // We observe elements against our custom scrolling container
    // If observing against the whole window, 'root' would just be null.
    const scrollContainer = document.getElementById('scroll-root');

    // Options for the observer
    const observerOptions = {{
        root: scrollContainer,
        rootMargin: '0px',
        // threshold: 0.1 means the callback fires when 10% of the element is visible
        threshold: 0.1 
    }};

    // Create the IntersectionObserver instance
    const observer = new IntersectionObserver((entries) => {{
        // The callback receives an array of entries (elements being observed)
        entries.forEach(entry => {{
            
            // Check if the element has entered the viewport
            if (entry.isIntersecting) {{
                // Add the CSS class that triggers the transition
                entry.target.classList.add('show');
            }} else {{
                // Optional: Remove the class when it leaves the viewport
                // This allows the animation to replay if the user scrolls back up
                entry.target.classList.remove('show');
            }}
        }});
    }}, observerOptions);

    // Grab all elements with the 'hidden' class and tell the observer to watch them
    const hiddenElements = document.querySelectorAll('.hidden');
    
    hiddenElements.forEach((el) => {{
        observer.observe(el);
    }});
}});
"""

    # Write files
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
