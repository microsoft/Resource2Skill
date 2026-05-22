def create_component(
    output_dir: str,
    title_text: str = "CSS Scroll Snapping",
    body_text: str = "Scroll down to see the snapping effect.",
    color_scheme: str = "dark",        
    accent_color: str = "#00bfff",     
    width_px: int = 800,
    height_px: int = 600,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Native CSS Scroll Snapping visual effect.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Base background for the page outside the container
    bg_color = "#121212" if color_scheme == "dark" else "#e2e8f0"

    # === CSS ===
    css = f"""/* Native CSS Scroll Snapping — generated component */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background: var(--bg);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden; /* Prevents whole-page scrolling, keeping focus on container */
}}

/* The parent container establishing the scrolling context */
.scroll-container {{
    width: var(--width);
    height: var(--height);
    max-width: 90vw;
    max-height: 90vh;
    overflow-y: scroll;
    
    /* THE CORE MECHANISM */
    scroll-snap-type: y mandatory;
    scroll-behavior: smooth;
    
    border-radius: 16px;
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
    background: #000;
}}

/* Subtle custom scrollbar */
.scroll-container::-webkit-scrollbar {{
    width: 8px;
}}
.scroll-container::-webkit-scrollbar-track {{
    background: rgba(255, 255, 255, 0.05);
}}
.scroll-container::-webkit-scrollbar-thumb {{
    background: rgba(255, 255, 255, 0.2);
    border-radius: 4px;
}}
.scroll-container::-webkit-scrollbar-thumb:hover {{
    background: rgba(255, 255, 255, 0.4);
}}

/* Individual snapping sections */
.scroll-area {{
    /* Match container height to ensure full-frame snapping */
    height: 100%;
    width: 100%;
    
    /* Align the top of this element with the top of the container */
    scroll-snap-align: start;
    
    /* Center the internal content */
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    
    color: #ffffff;
    text-align: center;
    padding: 2rem;
    
    /* Stop snapping to boundaries instantly on resize */
    scroll-snap-stop: always;
}}

/* Distinct section colors inspired by the tutorial */
.scroll-area:nth-child(1) {{ background-color: #0ea5e9; }} /* Light Blue */
.scroll-area:nth-child(2) {{ background-color: #ef4444; }} /* Red */
.scroll-area:nth-child(3) {{ background-color: #10b981; }} /* Emerald */
.scroll-area:nth-child(4) {{ background-color: #8b5cf6; }} /* Violet */

.number {{
    font-size: 120px;
    font-weight: 700;
    line-height: 1;
    text-shadow: 0 10px 20px rgba(0,0,0,0.15);
}}

.title {{
    font-size: 32px;
    font-weight: 600;
    margin-top: 16px;
    letter-spacing: -0.5px;
}}

.body-text {{
    font-size: 18px;
    font-weight: 400;
    margin-top: 12px;
    opacity: 0.9;
    max-width: 400px;
}}

.scroll-hint {{
    margin-top: 40px;
    animation: bounce 2s infinite;
    opacity: 0.7;
}}

@keyframes bounce {{
    0%, 20%, 50%, 80%, 100% {{ transform: translateY(0); }}
    40% {{ transform: translateY(-15px); }}
    60% {{ transform: translateY(-7px); }}
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
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="scroll-container">
        <!-- Section 1 -->
        <div class="scroll-area">
            <div class="number">1</div>
            <div class="title">{title_text}</div>
            <div class="body-text">{body_text}</div>
            <div class="scroll-hint">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 5v14M19 12l-7 7-7-7"/></svg>
            </div>
        </div>
        
        <!-- Section 2 -->
        <div class="scroll-area">
            <div class="number">2</div>
            <div class="title">Mandatory Alignment</div>
            <div class="body-text">The browser is forced to rest exactly on section boundaries.</div>
        </div>
        
        <!-- Section 3 -->
        <div class="scroll-area">
            <div class="number">3</div>
            <div class="title">Native Performance</div>
            <div class="body-text">No JS scroll-hijacking libraries required. Zero layout thrashing.</div>
        </div>
        
        <!-- Section 4 -->
        <div class="scroll-area">
            <div class="number">4</div>
            <div class="title">Perfect for Layouts</div>
            <div class="body-text">Ideal for full-screen presentations, galleries, and story-driven articles.</div>
        </div>
    </div>
    
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Native CSS Scroll Snapping — optional interactive behavior
document.addEventListener('DOMContentLoaded', () => {{
    const container = document.querySelector('.scroll-container');
    const sections = document.querySelectorAll('.scroll-area');

    // While CSS handles the snapping, JS can be used to trigger
    // animations or state changes when a section becomes active.
    const observerOptions = {{
        root: container,
        threshold: 0.6 // Trigger when 60% of the section is visible
    }};

    const observer = new IntersectionObserver((entries) => {{
        entries.forEach(entry => {{
            if (entry.isIntersecting) {{
                const sectionNumber = entry.target.querySelector('.number').textContent;
                console.log(`Snapped to section: ${{sectionNumber}}`);
                
                // Example: You could trigger entrance animations here
                // entry.target.classList.add('is-active');
            }}
        }});
    }}, observerOptions);

    sections.forEach(section => {{
        observer.observe(section);
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
