def create_component(
    output_dir: str,
    title_text: str = "Welcome to tomorrow",
    body_text: str = "We craft innovative digital solutions for a brighter future. Scroll down to see the magic unfold.",
    color_scheme: str = "dark",        
    accent_color: str = "#cc3f4e",     
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Scroll & Hover Reveal landing page effect.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme and accent_color ===
    if color_scheme == "dark":
        bg_color = "#131217"
        text_color = "#ffffff"
        surface_color = "#1e1d24"
    else:
        bg_color = "#f4f4f5"
        text_color = "#111827"
        surface_color = "#ffffff"
        
    # Isolate the last word of the title for the special animation
    words = title_text.split()
    if len(words) > 1:
        normal_title = " ".join(words[:-1])
        highlight_word = words[-1]
    else:
        normal_title = ""
        highlight_word = title_text

    # Squiggly SVG encoded for CSS background
    svg_squiggle = f"%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 20' preserveAspectRatio='none'%3E%3Cpath d='M0,10 Q25,20 50,10 T100,10' fill='none' stroke='{accent_color.replace('#', '%23')}' stroke-width='4' stroke-linecap='round'/%3E%3C/svg%3E"

    # === CSS ===
    css = f"""/* Dynamic Scroll & Hover Reveal — generated component */
:root {{
    --bg: {bg_color};
    --text: {text_color};
    --accent: {accent_color};
    --surface: {surface_color};
    --width: {width_px}px;
    --height: {height_px}px;
}}

*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

html {{
    scroll-behavior: smooth;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background: var(--bg);
    color: var(--text);
    overflow-x: hidden;
    line-height: 1.6;
}}

.app-container {{
    max-width: var(--width);
    margin: 0 auto;
    position: relative;
}}

/* -- Hero Section -- */
.hero {{
    min-height: var(--height);
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: flex-start;
    padding: 0 5%;
}}

h1 {{
    font-size: clamp(3rem, 6vw, 5rem);
    font-weight: 700;
    line-height: 1.1;
    margin-bottom: 1.5rem;
    max-width: 800px;
}}

.highlight-container {{
    display: inline-block;
    position: relative;
}}

.highlight {{
    color: var(--accent);
    display: inline-block;
    position: relative;
    opacity: 0; /* Starting state for keyframe */
    animation: slideInFade 0.6s cubic-bezier(0.2, 0.8, 0.2, 1) 0.2s forwards;
}}

.highlight::after {{
    content: '';
    position: absolute;
    bottom: -5px;
    left: 0;
    width: 100%;
    height: 15px;
    background-image: url("data:image/svg+xml,{svg_squiggle}");
    background-repeat: no-repeat;
    background-size: 100% 100%;
    background-position: bottom;
    z-index: -1;
}}

.hero p {{
    font-size: 1.25rem;
    max-width: 600px;
    margin-bottom: 2.5rem;
    opacity: 0.8;
}}

/* -- CTA Button (Hover Transition) -- */
.cta-button {{
    position: relative;
    padding: 15px 30px;
    background: transparent;
    color: var(--text);
    border: none;
    font-size: 1.125rem;
    font-weight: 700;
    cursor: pointer;
    z-index: 1; /* Keep text above the pseudo-element */
    outline: none;
}}

.cta-button::after {{
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 50px; /* Small block initially */
    height: 100%;
    background-color: var(--accent);
    z-index: -1;
    transition: width 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}}

.cta-button:hover::after,
.cta-button:focus-visible::after {{
    width: 100%; /* Expand to cover entire button */
}}

/* -- Scroll Sections (Intersection Observer Targets) -- */
.content-section {{
    min-height: 80vh;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 100px 5%;
}}

.content-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 3rem;
    width: 100%;
}}

.card {{
    background: var(--surface);
    padding: 3rem 2rem;
    border-radius: 12px;
    box-shadow: 0 20px 40px rgba(0,0,0,0.1);
}}

.card h2 {{
    font-size: 2rem;
    margin-bottom: 1rem;
}}

.card p {{
    opacity: 0.8;
}}

/* -- Scroll Animation Classes -- */
.scroll-element {{
    opacity: 0;
    transform: translateY(60px);
    transition: opacity 0.8s ease-out, transform 0.8s ease-out;
    will-change: opacity, transform;
}}

.scroll-element.delay-1 {{ transition-delay: 0.1s; }}
.scroll-element.delay-2 {{ transition-delay: 0.2s; }}

/* This class is appended via JS */
.scroll-element.visible {{
    opacity: 1;
    transform: translateY(0);
}}

/* Keyframes */
@keyframes slideInFade {{
    from {{
        opacity: 0;
        transform: translateX(-30%);
    }}
    to {{
        opacity: 1;
        transform: translateX(0);
    }}
}}

/* Accessibility / Preferences */
@media (prefers-reduced-motion: reduce) {{
    .highlight {{
        animation: none;
        opacity: 1;
        transform: none;
    }}
    
    .cta-button::after {{
        transition: none;
    }}
    
    .scroll-element {{
        transition: none;
        opacity: 1;
        transform: none;
    }}
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
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="app-container">
        
        <!-- Hero with Keyframe Animation and Hover Button -->
        <section class="hero">
            <h1>
                {normal_title} 
                <span class="highlight-container">
                    <span class="highlight">{highlight_word}</span>
                </span>
            </h1>
            <p>{body_text}</p>
            <button class="cta-button">Order now!</button>
        </section>

        <!-- Scroll Reveal Content -->
        <section class="content-section">
            <div class="content-grid">
                <div class="card scroll-element">
                    <h2>Innovation at Its Core</h2>
                    <p>Tomorrow isn't just a promise, it's a revolution in the world of experiences. We build with the future in mind.</p>
                </div>
                
                <div class="card scroll-element delay-1">
                    <h2>Custom Experiences</h2>
                    <p>Make your own today. Everything we design is tailored to map perfectly to your unique needs.</p>
                </div>
                
                <div class="card scroll-element delay-2">
                    <h2>Seamless Interfaces</h2>
                    <p>Through robust animations and logical structures, we make interactions that feel entirely natural.</p>
                </div>
            </div>
        </section>
        
        <section class="content-section" style="text-align: center; display: block;">
            <h2 class="scroll-element" style="font-size: 3rem; margin-bottom: 2rem;">Ready to begin?</h2>
            <div class="scroll-element delay-1">
                <button class="cta-button">Start Project</button>
            </div>
        </section>

    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Scroll-Triggered Animation Logic
document.addEventListener('DOMContentLoaded', () => {{
    
    // Select all elements that need to be animated on scroll
    const scrollElements = document.querySelectorAll('.scroll-element');
    
    // Check if browser supports IntersectionObserver
    if ('IntersectionObserver' in window) {{
        
        // Setup observer options
        const observerOptions = {{
            root: null, // use the viewport
            rootMargin: '0px',
            threshold: 0.15 // Trigger when 15% of the element is visible
        }};
        
        // Callback for when element visibility changes
        const observerCallback = (entries, observer) => {{
            entries.forEach(entry => {{
                if (entry.isIntersecting) {{
                    // Add the class that triggers the CSS transition
                    entry.target.classList.add('visible');
                    
                    // Stop observing once animated (runs only once)
                    observer.unobserve(entry.target);
                }}
            }});
        }};
        
        // Initialize the observer
        const scrollObserver = new IntersectionObserver(observerCallback, observerOptions);
        
        // Attach observer to all elements
        scrollElements.forEach(el => scrollObserver.observe(el));
        
    }} else {{
        // Fallback for extremely old browsers: just make them visible immediately
        scrollElements.forEach(el => el.classList.add('visible'));
    }}
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
