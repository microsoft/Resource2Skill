def create_component(
    output_dir: str,
    title_text: str = "Welcome to tomorrow",
    body_text: str = "Innovation at its core. Tomorrow isn't just a company, it's a revolution in digital experience.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#cc3f4e",     # The vibrant red from the tutorial
    width_px: int = 1000,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Dynamic Landing Page Interactions pattern.
    Features keyframe text reveals, offset expanding hover blocks, and scroll-triggered animations.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors ===
    if color_scheme == "dark":
        bg_color = "#131217"
        text_color = "#ffffff"
        surface_color = "#1e1d24"
        sub_text_color = "#a0a0a0"
    else:
        bg_color = "#f4f4f5"
        text_color = "#18181b"
        surface_color = "#ffffff"
        sub_text_color = "#71717a"

    # Split title to apply highlight to the last word
    words = title_text.split()
    if len(words) > 1:
        highlighted_title = " ".join(words[:-1]) + f' <span class="highlight">{words[-1]}</span>'
    else:
        highlighted_title = f'<span class="highlight">{title_text}</span>'

    # === CSS ===
    css = f"""/* Dynamic Landing Page Interactions */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');

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
}}

body {{
    font-family: 'Inter', sans-serif;
    background: #000; /* Outer canvas */
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 100vh;
    overflow: hidden; /* Prevent full page scroll, rely on viewport */
}}

/* Simulated Browser Viewport */
.viewport {{
    width: {width_px}px;
    height: {height_px}px;
    background: var(--bg);
    color: var(--text);
    overflow-y: auto;
    overflow-x: hidden;
    position: relative;
    scroll-behavior: smooth;
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
    border-radius: 12px;
}}

/* --- Hero Section --- */
.hero {{
    min-height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: center;
    padding: 0 10%;
    position: relative;
}}

.hero-title {{
    font-size: clamp(3rem, 6vw, 5rem);
    font-weight: 800;
    line-height: 1.1;
    letter-spacing: -0.03em;
    max-width: 800px;
    z-index: 2;
}}

.hero-subtitle {{
    font-size: 1.5rem;
    color: var(--sub-text);
    margin-top: 1.5rem;
    font-weight: 400;
    max-width: 600px;
    opacity: 0;
    animation: simpleFadeIn 1s ease-out 0.4s forwards;
}}

/* 1. Entrance Keyframe Reveal */
.highlight {{
    color: var(--accent);
    display: inline-block;
    opacity: 0;
    animation: slideFadeIn 0.8s cubic-bezier(0.25, 1, 0.5, 1) forwards;
}}

@keyframes slideFadeIn {{
    0% {{
        opacity: 0;
        transform: translateX(-50px) scale(0.95);
    }}
    100% {{
        opacity: 1;
        transform: translateX(0) scale(1);
    }}
}}

@keyframes simpleFadeIn {{
    from {{ opacity: 0; transform: translateY(20px); }}
    to {{ opacity: 1; transform: translateY(0); }}
}}

/* 2. Edgy Offset Block Hover Button */
.cta-wrapper {{
    margin-top: 3rem;
    opacity: 0;
    animation: simpleFadeIn 1s ease-out 0.6s forwards;
}}

.cta-button {{
    background: transparent;
    color: var(--text);
    border: none;
    font-size: 1.25rem;
    font-weight: 800;
    font-family: inherit;
    position: relative;
    padding: 16px 24px;
    cursor: pointer;
    z-index: 1;
    outline: none;
}}

.cta-button::after {{
    content: '';
    position: absolute;
    background-color: var(--accent);
    height: calc(100% + 20px);
    width: 60px;
    top: -10px;
    right: -20px;
    z-index: -1;
    transition: width 0.35s cubic-bezier(0.4, 0, 0.2, 1), right 0.35s cubic-bezier(0.4, 0, 0.2, 1);
}}

.cta-button:hover::after {{
    width: calc(100% + 40px);
    right: -20px;
}}

/* --- Scroll Content Section --- */
.content-section {{
    padding: 100px 10%;
    min-height: 100%;
}}

.section-header {{
    font-size: 2.5rem;
    font-weight: 800;
    margin-bottom: 3rem;
}}

.features-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 30px;
}}

/* 3. Scroll-Triggered Reveal Classes */
.scroll-reveal {{
    background: var(--surface);
    padding: 40px 30px;
    border-radius: 16px;
    border: 1px solid rgba(255, 255, 255, 0.05);
    opacity: 0;
    transform: translateY(60px);
    transition: opacity 0.8s ease-out, transform 0.8s cubic-bezier(0.25, 1, 0.5, 1);
}}

.scroll-reveal.visible {{
    opacity: 1;
    transform: translateY(0);
}}

/* Staggered delays based on structural order */
.scroll-reveal:nth-child(2) {{ transition-delay: 0.15s; }}
.scroll-reveal:nth-child(3) {{ transition-delay: 0.30s; }}

.feature-title {{
    font-size: 1.25rem;
    font-weight: 600;
    margin-bottom: 1rem;
    color: var(--text);
}}

.feature-text {{
    color: var(--sub-text);
    line-height: 1.6;
}}
"""

    # === HTML ===
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dynamic Landing Page Interactions</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="viewport">
        
        <!-- Hero Section -->
        <section class="hero">
            <h1 class="hero-title">
                {highlighted_title}
            </h1>
            <p class="hero-subtitle">{body_text}</p>
            
            <div class="cta-wrapper">
                <button class="cta-button">Order now!</button>
            </div>
        </section>

        <!-- Scroll Reveal Section -->
        <section class="content-section">
            <h2 class="section-header scroll-reveal">Why Choose Us?</h2>
            
            <div class="features-grid">
                <div class="scroll-reveal">
                    <h3 class="feature-title">Custom Crafting</h3>
                    <p class="feature-text">Every detail is meticulously constructed to provide an unmatched user experience that scales with your ambition.</p>
                </div>
                <div class="scroll-reveal">
                    <h3 class="feature-title">Lightning Fast</h3>
                    <p class="feature-text">Optimized performance ensuring that your interactions are smooth, seamless, and completely jank-free.</p>
                </div>
                <div class="scroll-reveal">
                    <h3 class="feature-title">Future Proof</h3>
                    <p class="feature-text">Built on modern web standards utilizing the latest native APIs to ensure longevity and minimal technical debt.</p>
                </div>
            </div>
        </section>
        
        <!-- Spacer to allow scrolling past the features -->
        <div style="height: 200px;"></div>

    </div>
    
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = """// Dynamic Landing Page Interactions - Scroll Logic
document.addEventListener('DOMContentLoaded', () => {
    
    // Configure the Intersection Observer
    const observerOptions = {
        root: document.querySelector('.viewport'), // Observe relative to our custom scrolling container
        rootMargin: '0px 0px -10% 0px',            // Trigger slightly before element enters fully
        threshold: 0.1                             // Trigger when 10% of the element is visible
    };

    const revealObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                // Add the class that triggers the CSS transition
                entry.target.classList.add('visible');
                
                // Optional: Stop observing once revealed if you only want it to animate once
                // observer.unobserve(entry.target);
            } else {
                // Remove class when scrolling back up to allow re-animation (optional)
                entry.target.classList.remove('visible');
            }
        });
    }, observerOptions);

    // Find all elements with the scroll-reveal class and observe them
    const revealElements = document.querySelectorAll('.scroll-reveal');
    revealElements.forEach(el => revealObserver.observe(el));
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
