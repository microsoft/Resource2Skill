def create_component(
    output_dir: str,
    title_text: str = "Welcome to Tomorrow",
    body_text: str = "Discover an interactive experience built with modern CSS animations, seamless transitions, and performant scroll-triggered reveals.",
    color_scheme: str = "dark",        
    accent_color: str = "#e63946",     
    width_px: int = 1000,
    height_px: int = 700,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Dynamic Scroll Reveal & Keyframe Accents visual effect.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Theme definitions
    if color_scheme == "dark":
        bg_color = "#11131a"
        text_color = "#f8f9fa"
        surface_color = "rgba(255, 255, 255, 0.04)"
        surface_border = "rgba(255, 255, 255, 0.08)"
        mute_text = "#a0a4b8"
    else:
        bg_color = "#ffffff"
        text_color = "#11131a"
        surface_color = "rgba(0, 0, 0, 0.03)"
        surface_border = "rgba(0, 0, 0, 0.08)"
        mute_text = "#5c6070"

    css = f"""/* Dynamic Scroll Reveal & Keyframe Accents */
:root {{
    --bg: {bg_color};
    --text: {text_color};
    --text-mute: {mute_text};
    --accent: {accent_color};
    --surface: {surface_color};
    --border: {surface_border};
    --width: {width_px}px;
    --height: {height_px}px;
}}

* {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background: #000; /* Outer canvas */
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 100vh;
}}

/* The specific dimensional container representing the tutorial viewport */
.viewport {{
    width: var(--width);
    height: var(--height);
    background: var(--bg);
    color: var(--text);
    overflow-y: auto;
    overflow-x: hidden;
    position: relative;
    scroll-behavior: smooth;
    box-shadow: 0 24px 48px rgba(0,0,0,0.4);
}}

/* === Hero Section === */
.hero {{
    height: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    padding: 2rem;
}}

.hero h1 {{
    font-size: 3.5rem;
    font-weight: 800;
    line-height: 1.1;
    letter-spacing: -0.03em;
    margin-bottom: 1.5rem;
    position: relative;
}}

/* The Animated Keyframe Accent on Text */
.accent-word {{
    position: relative;
    display: inline-block;
    color: var(--text);
    z-index: 1;
}}

.accent-word::after {{
    content: '';
    position: absolute;
    bottom: 5px;
    left: -5%;
    width: 110%;
    height: 12px;
    background: var(--accent);
    z-index: -1;
    transform-origin: left center;
    border-radius: 6px;
    /* Keyframe execution */
    animation: slideAccent 0.7s cubic-bezier(0.22, 1, 0.36, 1) forwards;
    animation-delay: 0.3s;
    transform: scaleX(0);
}}

@keyframes slideAccent {{
    0% {{ transform: scaleX(0); opacity: 0; }}
    100% {{ transform: scaleX(1); opacity: 1; }}
}}

.hero p {{
    font-size: 1.125rem;
    color: var(--text-mute);
    max-width: 600px;
    margin-bottom: 2.5rem;
    line-height: 1.6;
}}

/* Hover Transitions */
.cta-button {{
    display: inline-flex;
    align-items: center;
    justify-content: center;
    padding: 1rem 2rem;
    font-size: 1rem;
    font-weight: 600;
    text-decoration: none;
    color: #fff;
    background-color: var(--accent);
    border: none;
    border-radius: 50px;
    cursor: pointer;
    /* Transition declaration */
    transition: transform 0.3s ease, background-color 0.3s ease, box-shadow 0.3s ease;
}}

.cta-button:hover {{
    transform: translateY(-4px) scale(1.03);
    box-shadow: 0 12px 24px rgba(0, 0, 0, 0.15);
    filter: brightness(1.1);
}}

.scroll-indicator {{
    position: absolute;
    bottom: 2rem;
    left: 50%;
    transform: translateX(-50%);
    animation: bounce 2s infinite ease-in-out;
    color: var(--text-mute);
}}

@keyframes bounce {{
    0%, 100% {{ transform: translate(-50%, 0); }}
    50% {{ transform: translate(-50%, 10px); }}
}}

/* === Content Section & Scroll Animations === */
.content-section {{
    padding: 6rem 3rem;
    min-height: 100%;
}}

.section-title {{
    font-size: 2.5rem;
    margin-bottom: 3rem;
    text-align: center;
}}

.grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 2rem;
}}

.card {{
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 2rem;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}}

.card:hover {{
    transform: translateY(-8px);
    box-shadow: 0 12px 32px rgba(0,0,0,0.1);
    border-color: var(--accent);
}}

.card h3 {{
    font-size: 1.25rem;
    margin-bottom: 1rem;
}}

.card p {{
    color: var(--text-mute);
    line-height: 1.6;
    font-size: 0.95rem;
}}

/* THE SCROLL REVEAL UTILITY CLASSES */
.scroll-reveal {{
    opacity: 0;
    transform: translateY(40px) scale(0.95);
    transition: opacity 0.8s cubic-bezier(0.16, 1, 0.3, 1), 
                transform 0.8s cubic-bezier(0.16, 1, 0.3, 1);
}}

.scroll-reveal.visible {{
    opacity: 1;
    transform: translateY(0) scale(1);
}}
"""

    # Processing the title to inject the animated span class automatically
    words = title_text.split()
    if len(words) > 1:
        # Wrap the last word in the accent class
        last_word = words.pop()
        processed_title = " ".join(words) + f' <span class="accent-word">{last_word}</span>'
    else:
        processed_title = f'<span class="accent-word">{title_text}</span>'

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <!-- Viewport represents the component boundaries -->
    <div class="viewport">
        
        <!-- Hero Section -->
        <section class="hero">
            <h1>{processed_title}</h1>
            <p>{body_text}</p>
            <a href="#explore" class="cta-button">Explore Features</a>
            
            <div class="scroll-indicator">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M12 5v14M19 12l-7 7-7-7"/>
                </svg>
            </div>
        </section>

        <!-- Dynamic Content Section -->
        <section id="explore" class="content-section">
            <h2 class="section-title scroll-reveal">Innovation at its Core</h2>
            
            <div class="grid">
                <!-- Staggered delay applied inline -->
                <div class="card scroll-reveal" style="transition-delay: 0.1s;">
                    <h3>Interactive `@keyframes`</h3>
                    <p>Continuous or timeline-based animations that breathe life into the page automatically on load.</p>
                </div>
                <div class="card scroll-reveal" style="transition-delay: 0.2s;">
                    <h3>Slick Transitions</h3>
                    <p>Feedback-driven style changes when interacting with buttons, links, or cards to enhance UX.</p>
                </div>
                <div class="card scroll-reveal" style="transition-delay: 0.3s;">
                    <h3>Scroll Intersection</h3>
                    <p>Performant revealing of content only when it enters the viewport using the Intersection Observer API.</p>
                </div>
                <div class="card scroll-reveal" style="transition-delay: 0.4s;">
                    <h3>Layered Depth</h3>
                    <p>Using structural offsets and z-index to create a 3D aesthetic even within flat 2D designs.</p>
                </div>
            </div>
        </section>
        
        <section class="hero" style="min-height: 60%;">
            <h1 class="scroll-reveal">Ready to build?</h1>
            <p class="scroll-reveal" style="transition-delay: 0.1s;">Combine these properties for engaging digital experiences.</p>
            <a href="#" class="cta-button scroll-reveal" style="transition-delay: 0.2s;">Get Started</a>
        </section>

    </div>

    <script src="script.js"></script>
</body>
</html>"""

    js = f"""// Intersection Observer for Scroll Animations
document.addEventListener('DOMContentLoaded', () => {{
    // 1. Setup the Intersection Observer options
    const observerOptions = {{
        root: document.querySelector('.viewport'), // Observe relative to the custom viewport
        rootMargin: '0px',
        threshold: 0.15 // Trigger when 15% of the element is visible
    }};

    // 2. Create the observer callback
    const observerCallback = (entries, observer) => {{
        entries.forEach(entry => {{
            if (entry.isIntersecting) {{
                // Add the 'visible' class to trigger CSS transition
                entry.target.classList.add('visible');
                
                // Optional: Stop observing once revealed so it doesn't animate out and back in
                // observer.unobserve(entry.target);
            }} else {{
                // Remove class if you want the animation to reset when scrolled out of view
                entry.target.classList.remove('visible');
            }}
        }});
    }};

    const observer = new IntersectionObserver(observerCallback, observerOptions);

    // 3. Target all elements with the .scroll-reveal class
    const hiddenElements = document.querySelectorAll('.scroll-reveal');
    hiddenElements.forEach(el => observer.observe(el));
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
