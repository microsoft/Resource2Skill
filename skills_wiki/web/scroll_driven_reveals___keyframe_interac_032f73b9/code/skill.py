def create_component(
    output_dir: str,
    title_text: str = "Welcome to tomorrow",
    body_text: str = "Tomorrow isn't just a company, it's a revolution in the world of digital experiences.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#cc3f4e",     # CSS hex color for accent (defaulting to the red from the video)
    width_px: int = 1000,
    height_px: int = 700,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Scroll-Driven Reveals & Keyframe Interactive Hero.
    
    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme ===
    if color_scheme == "dark":
        bg_color = "#131217"
        text_color = "#ffffff"
        sub_text_color = "#a0a0a5"
        surface_color = "#1e1d24"
        btn_text_hover = "#ffffff"
    else:
        bg_color = "#ffffff"
        text_color = "#131217"
        sub_text_color = "#555555"
        surface_color = "#f0f0f0"
        btn_text_hover = "#ffffff"

    # === CSS ===
    css = f"""/* Scroll-Driven Reveals & Keyframes Component */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --text: {text_color};
    --sub-text: {sub_text_color};
    --accent: {accent_color};
    --surface: {surface_color};
    --btn-text-hover: {btn_text_hover};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background: #000; /* Outer background to contrast component container */
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 100vh;
}}

.container {{
    width: var(--width);
    height: var(--height);
    background: var(--bg);
    color: var(--text);
    position: relative;
    overflow-y: auto;
    overflow-x: hidden;
    scroll-behavior: smooth;
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
}}

/* =========================================
   HERO SECTION & KEYFRAMES
   ========================================= */
.hero {{
    min-height: 80%;
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    justify-content: center;
    padding: 0 10%;
}}

.hero-title {{
    font-size: 4rem;
    font-weight: 800;
    line-height: 1.1;
    margin-bottom: 1.5rem;
    max-width: 800px;
    /* Keyframe Animation */
    opacity: 0;
    animation: slideFadeIn 0.8s cubic-bezier(0.2, 0.8, 0.2, 1) 0.2s forwards;
}}

.highlight {{
    position: relative;
    display: inline-block;
    color: var(--accent);
    z-index: 1;
}}

.highlight::after {{
    content: '';
    position: absolute;
    bottom: 5px;
    left: -2%;
    width: 104%;
    height: 30%;
    background-color: var(--accent);
    opacity: 0.2;
    z-index: -1;
    transform: skewX(-15deg);
    border-radius: 4px;
}}

.hero-subtitle {{
    font-size: 1.25rem;
    color: var(--sub-text);
    margin-bottom: 2.5rem;
    max-width: 600px;
    opacity: 0;
    animation: slideFadeIn 0.8s cubic-bezier(0.2, 0.8, 0.2, 1) 0.4s forwards;
}}

@keyframes slideFadeIn {{
    from {{
        opacity: 0;
        transform: translateX(-40px);
    }}
    to {{
        opacity: 1;
        transform: translateX(0);
    }}
}}

/* =========================================
   BUTTON TRANSITIONS (HOVER Fill)
   ========================================= */
.cta-button {{
    position: relative;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    padding: 16px 36px;
    font-size: 1.1rem;
    font-weight: 600;
    color: var(--text);
    text-decoration: none;
    background: transparent;
    border: 2px solid var(--accent);
    border-radius: 4px;
    cursor: pointer;
    overflow: hidden;
    z-index: 1;
    transition: color 0.3s ease;
    /* Hero load animation */
    opacity: 0;
    animation: slideFadeIn 0.8s cubic-bezier(0.2, 0.8, 0.2, 1) 0.6s forwards;
}}

.cta-button::after {{
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    bottom: 0;
    width: 0%;
    background-color: var(--accent);
    z-index: -1;
    transition: width 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}}

.cta-button:hover {{
    color: var(--btn-text-hover);
}}

.cta-button:hover::after {{
    width: 100%;
}}

/* =========================================
   SCROLL ANIMATIONS SECTION
   ========================================= */
.content-section {{
    padding: 10% 10%;
    display: flex;
    gap: 4rem;
    align-items: center;
}}

.content-section:nth-child(even) {{
    flex-direction: row-reverse;
    background: var(--surface);
}}

.block-text {{
    flex: 1;
}}

.block-text h2 {{
    font-size: 2.5rem;
    margin-bottom: 1rem;
}}

.block-text p {{
    color: var(--sub-text);
    font-size: 1.1rem;
    line-height: 1.6;
}}

.block-image {{
    flex: 1;
    height: 300px;
    background: linear-gradient(135deg, var(--surface), var(--accent));
    border-radius: 12px;
    box-shadow: 0 10px 30px -10px rgba(0,0,0,0.3);
}}

/* Scroll Reveal Classes */
.reveal {{
    opacity: 0;
    transform: translateY(50px);
    transition: all 0.8s cubic-bezier(0.2, 0.8, 0.2, 1);
}}

.reveal.visible {{
    opacity: 1;
    transform: translateY(0);
}}

/* Delays for staggered revealing */
.delay-1 {{ transition-delay: 0.1s; }}
.delay-2 {{ transition-delay: 0.3s; }}
"""

    # === HTML ===
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Scroll Animations & Transitions</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        <!-- Hero Section -->
        <section class="hero">
            <h1 class="hero-title">
                {title_text.split()[0]} 
                <span class="highlight">{" ".join(title_text.split()[1:])}</span>
            </h1>
            <p class="hero-subtitle">{body_text}</p>
            <a href="#" class="cta-button">Order now!</a>
        </section>

        <!-- Scroll Section 1 -->
        <section class="content-section">
            <div class="block-text reveal">
                <h2>Innovation at its <span class="highlight">Core</span></h2>
                <p>We believe in pushing boundaries. Watch how seamlessly elements transition into view, guiding your focus down the page without overwhelming your senses.</p>
            </div>
            <div class="block-image reveal delay-1"></div>
        </section>

        <!-- Scroll Section 2 -->
        <section class="content-section">
            <div class="block-text reveal">
                <h2>Custom <span class="highlight">Experiences</span></h2>
                <p>Every micro-interaction matters. From the way our buttons fill with color, to the precise easing curves of our typography sliding into place.</p>
                <br>
                <a href="#" class="cta-button reveal delay-2">Discover more</a>
            </div>
            <div class="block-image reveal delay-1" style="background: linear-gradient(135deg, var(--accent), #2a2a35);"></div>
        </section>
        
        <!-- Bottom padding for scrolling -->
        <div style="height: 100px;"></div>
    </div>
    
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Scroll Animations via Intersection Observer
document.addEventListener('DOMContentLoaded', () => {{
    
    // Select all elements that should animate on scroll
    const revealElements = document.querySelectorAll('.reveal');
    
    // Configuration options for the observer
    const observerOptions = {{
        root: document.querySelector('.container'), // Observe scrolling within the specific container
        rootMargin: '0px',
        threshold: 0.15 // Trigger when 15% of the element is visible
    }};
    
    // Callback function when intersecting occurs
    const observerCallback = (entries, observer) => {{
        entries.forEach(entry => {{
            if (entry.isIntersecting) {{
                // Add the class that triggers the CSS transition
                entry.target.classList.add('visible');
                
                // Optional: Stop observing once revealed so it doesn't animate out and in repeatedly
                observer.unobserve(entry.target);
            }}
        }});
    }};
    
    // Initialize Observer
    const observer = new IntersectionObserver(observerCallback, observerOptions);
    
    // Attach observer to all target elements
    revealElements.forEach(element => {{
        observer.observe(element);
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
