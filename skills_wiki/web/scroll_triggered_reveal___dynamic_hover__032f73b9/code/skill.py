def create_component(
    output_dir: str,
    title_text: str = "Welcome to tomorrow",
    body_text: str = "Scroll down to experience smooth, performant reveal animations driven by modern web APIs.",
    color_scheme: str = "dark",
    accent_color: str = "#e63946",
    width_px: int = 1000,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing Scroll-Triggered Reveals and Dynamic Button Hovers.
    
    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Color definitions based on scheme
    if color_scheme == "dark":
        bg_color = "#121212"
        surface_color = "#1e1e1e"
        text_primary = "#ffffff"
        text_secondary = "#a0a0a0"
        border_color = "#333333"
    else:
        bg_color = "#f8f9fa"
        surface_color = "#ffffff"
        text_primary = "#121212"
        text_secondary = "#555555"
        border_color = "#dddddd"

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Scroll Animation Showcase</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <!-- Viewport Container strictly respects the requested dimensions -->
    <div class="viewport-container" id="scroll-root">
        
        <!-- Hero Section -->
        <section class="section hero">
            <h1 class="hero-title">
                <span class="animate-on-load">Innovation</span><br>
                {title_text}
            </h1>
            <p class="hero-subtitle reveal-elem fade-up" style="transition-delay: 0.3s;">
                {body_text}
            </p>
            <div class="reveal-elem fade-up" style="transition-delay: 0.5s;">
                <button class="dynamic-btn">Order now!</button>
            </div>
            
            <div class="scroll-indicator animate-bounce">↓</div>
        </section>

        <!-- Feature Section 1 (Staggered Grid) -->
        <section class="section features">
            <h2 class="section-title reveal-elem fade-right">Custom features tailored for you.</h2>
            <div class="card-grid">
                <div class="card reveal-elem fade-up" style="transition-delay: 0.1s;">
                    <h3>Speed</h3>
                    <p>Optimized with Intersection Observer for 60fps performance.</p>
                </div>
                <div class="card reveal-elem fade-up" style="transition-delay: 0.2s;">
                    <h3>Design</h3>
                    <p>Hardware accelerated CSS transforms eliminate layout thrashing.</p>
                </div>
                <div class="card reveal-elem fade-up" style="transition-delay: 0.3s;">
                    <h3>Scalability</h3>
                    <p>Easily add classes to any element to make them react to the viewport.</p>
                </div>
            </div>
        </section>

        <!-- Feature Section 2 (Scale Reveal) -->
        <section class="section split">
            <div class="split-content reveal-elem fade-right">
                <h2 class="section-title">A revolution in web design.</h2>
                <p class="hero-subtitle">We believe in the power of fluid interfaces to tell a better story.</p>
                <button class="dynamic-btn">Learn More</button>
            </div>
            <div class="split-image reveal-elem scale-in">
                <!-- Abstract geometric shapes representing image -->
                <div class="cube"></div>
                <div class="cube" style="top: -20px; left: 40px; transform: scale(0.8)"></div>
            </div>
        </section>
        
        <!-- Footer Spacer -->
        <section class="section" style="min-height: 30vh; display: flex; align-items: center; justify-content: center;">
            <p class="hero-subtitle reveal-elem fade-up">End of demonstration.</p>
        </section>

    </div>
    <script src="script.js"></script>
</body>
</html>"""

    css = f"""/* Base Component Resets */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg-color: {bg_color};
    --surface-color: {surface_color};
    --text-primary: {text_primary};
    --text-secondary: {text_secondary};
    --accent: {accent_color};
    --border: {border_color};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background-color: #000; /* Dark outside backdrop */
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--text-primary);
}}

/* Isolated Container */
.viewport-container {{
    width: var(--width);
    height: var(--height);
    background-color: var(--bg-color);
    overflow-y: auto;
    overflow-x: hidden;
    position: relative;
    box-shadow: 0 20px 50px rgba(0,0,0,0.5);
    scroll-behavior: smooth;
}}

/* Layout Utilities */
.section {{
    min-height: 100vh;
    padding: 100px 8%;
    display: flex;
    flex-direction: column;
    justify-content: center;
    position: relative;
}}

.hero-title {{
    font-size: 4.5rem;
    line-height: 1.1;
    font-weight: 800;
    letter-spacing: -0.03em;
    margin-bottom: 24px;
}}

.hero-subtitle {{
    font-size: 1.25rem;
    color: var(--text-secondary);
    max-width: 600px;
    line-height: 1.6;
    margin-bottom: 40px;
}}

.section-title {{
    font-size: 3rem;
    font-weight: 800;
    margin-bottom: 40px;
    letter-spacing: -0.02em;
}}

/* ========================================= */
/* ANIMATION PATTERN 1: The Dynamic Button   */
/* ========================================= */
.dynamic-btn {{
    position: relative;
    background: transparent;
    color: var(--text-primary);
    border: none;
    font-family: inherit;
    font-size: 1.1rem;
    font-weight: 600;
    padding: 16px 32px;
    cursor: pointer;
    overflow: hidden;
    z-index: 1;
    transition: color 0.3s ease;
}}

/* The expanding block */
.dynamic-btn::after {{
    content: '';
    position: absolute;
    top: 0;
    right: -20px;
    width: 60px;
    height: 100%;
    background-color: var(--accent);
    z-index: -1;
    transition: all 0.4s cubic-bezier(0.25, 1, 0.5, 1);
    transform: skewX(-15deg);
}}

.dynamic-btn:hover {{
    color: #ffffff; /* Ensure text is visible over accent */
}}

.dynamic-btn:hover::after {{
    width: 150%;
    right: -10px;
    transform: skewX(0deg);
}}

/* ========================================= */
/* ANIMATION PATTERN 2: On-Load Keyframes    */
/* ========================================= */
.animate-on-load {{
    display: inline-block;
    color: var(--accent);
    opacity: 0;
    animation: slideInLeft 0.8s cubic-bezier(0.165, 0.84, 0.44, 1) forwards;
}}

@keyframes slideInLeft {{
    from {{
        opacity: 0;
        transform: translateX(-100px);
    }}
    to {{
        opacity: 1;
        transform: translateX(0);
    }}
}}

.scroll-indicator {{
    position: absolute;
    bottom: 40px;
    left: 50%;
    transform: translateX(-50%);
    color: var(--text-secondary);
    font-size: 1.5rem;
}}

.animate-bounce {{
    animation: bounce 2s infinite ease-in-out;
}}

@keyframes bounce {{
    0%, 100% {{ transform: translate(-50%, 0); }}
    50% {{ transform: translate(-50%, 15px); }}
}}

/* ========================================= */
/* ANIMATION PATTERN 3: Scroll Reveals       */
/* ========================================= */
/* Base state for all revealing elements */
.reveal-elem {{
    opacity: 0;
    will-change: transform, opacity;
    /* The core smoothing engine */
    transition: all 0.8s cubic-bezier(0.25, 1, 0.5, 1);
}}

/* Specific off-screen states */
.reveal-elem.fade-up {{
    transform: translateY(40px);
}}

.reveal-elem.fade-right {{
    transform: translateX(-40px);
}}

.reveal-elem.scale-in {{
    transform: scale(0.85);
}}

/* The active state appended by JS */
.reveal-elem.is-visible {{
    opacity: 1;
    transform: translate(0) scale(1);
}}

/* Section Specific Layouts */
.card-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 30px;
}}

.card {{
    background: var(--surface-color);
    padding: 40px;
    border-radius: 12px;
    border: 1px solid var(--border);
}}

.card h3 {{
    font-size: 1.5rem;
    margin-bottom: 16px;
    color: var(--accent);
}}

.card p {{
    color: var(--text-secondary);
    line-height: 1.6;
}}

.split {{
    flex-direction: row;
    align-items: center;
    gap: 60px;
}}

.split-content {{
    flex: 1;
}}

.split-image {{
    flex: 1;
    height: 400px;
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
}}

.cube {{
    width: 150px;
    height: 150px;
    border: 4px solid var(--accent);
    position: absolute;
    box-shadow: inset 0 0 40px rgba(0,0,0,0.5);
}}
"""

    js = """// Scroll-Triggered Reveal Logic
document.addEventListener('DOMContentLoaded', () => {
    // Select all elements that have the base reveal class
    const revealElements = document.querySelectorAll('.reveal-elem');
    const scrollRoot = document.getElementById('scroll-root');

    // Configure the Intersection Observer
    const observerOptions = {
        // Use our custom container as the viewport, not the main browser window
        root: scrollRoot,
        rootMargin: '0px',
        // Trigger when 15% of the element is visible
        threshold: 0.15 
    };

    const revealCallback = (entries, observer) => {
        entries.forEach(entry => {
            // Check if the element has crossed the threshold into view
            if (entry.isIntersecting) {
                // Add the active class to trigger CSS transition
                entry.target.classList.add('is-visible');
                
                // Optional: Stop observing once revealed so it doesn't animate out when scrolling up
                // observer.unobserve(entry.target); 
            } else {
                // Remove class when scrolling out of view to allow re-animation (Playful feel)
                // Remove the `else` block if you only want animations to play once.
                entry.target.classList.remove('is-visible');
            }
        });
    };

    const observer = new IntersectionObserver(revealCallback, observerOptions);

    // Attach observer to every element
    revealElements.forEach(el => observer.observe(el));
});
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
