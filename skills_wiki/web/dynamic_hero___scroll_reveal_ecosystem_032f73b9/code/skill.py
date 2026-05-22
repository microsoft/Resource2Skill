def create_component(
    output_dir: str,
    title_text: str = "Welcome to tomorrow",
    body_text: str = "Tomorrow isn't just a cookie company, it's a revolution in the world of sweets. Experience the ultimate digital experience.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#e63946",     # Red accent from tutorial
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Dynamic Hero & Scroll-Reveal Ecosystem.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme and accent_color ===
    if color_scheme == "dark":
        bg_color = "#121212"
        text_color = "#ffffff"
        surface_color = "#1e1e1e"
        text_muted = "#a0a0a0"
    else:
        bg_color = "#f8f9fa"
        text_color = "#212529"
        surface_color = "#ffffff"
        text_muted = "#6c757d"

    # === CSS ===
    css = f"""/* Dynamic Hero & Scroll-Reveal — generated component */
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
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background-color: var(--bg);
    color: var(--text);
    line-height: 1.6;
    overflow-x: hidden;
}}

/* =========================================
   HERO SECTION & KEYFRAME ANIMATIONS
   ========================================= */
.hero {{
    min-height: 100vh; /* Full viewport height to force scrolling later */
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    padding: 2rem;
}}

.hero-title {{
    font-size: clamp(2.5rem, 5vw, 5rem);
    font-weight: 800;
    letter-spacing: -0.02em;
    margin-bottom: 1.5rem;
    
    /* Setup for keyframe animation */
    opacity: 0;
    animation: slideInFade 0.8s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    animation-delay: 0.2s; /* Slight delay on load */
}}

.highlight {{
    color: var(--accent);
    /* Mimicking the squiggly SVG with pure CSS */
    text-decoration: underline wavy var(--accent);
    text-underline-offset: 8px;
}}

.hero-subtitle {{
    font-size: clamp(1rem, 2vw, 1.25rem);
    color: var(--text-muted);
    max-width: 600px;
    margin-bottom: 2.5rem;
    
    opacity: 0;
    animation: slideInFade 0.8s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    animation-delay: 0.4s;
}}

/* Keyframe Definition */
@keyframes slideInFade {{
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
   CTA BUTTON & CSS TRANSITIONS
   ========================================= */
.cta-button {{
    display: inline-block;
    background-color: transparent;
    color: var(--text);
    font-size: 1.125rem;
    font-weight: 600;
    text-decoration: none;
    padding: 1rem 2.5rem;
    border: 2px solid var(--accent);
    border-radius: 4px;
    cursor: pointer;
    position: relative;
    overflow: hidden;
    z-index: 1;
    
    /* The Transition */
    transition: all 0.3s ease-in-out;
    
    opacity: 0;
    animation: fadeIn 1s ease forwards;
    animation-delay: 0.6s;
}}

/* Button Hover State */
.cta-button:hover {{
    color: #fff; /* Ensure contrast on hover */
    transform: translateY(-3px) scale(1.02);
    box-shadow: 0 10px 20px rgba(0,0,0,0.2);
}}

/* Pseudo-element for background fill effect */
.cta-button::after {{
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: var(--accent);
    z-index: -1;
    transform: scaleX(0);
    transform-origin: right;
    transition: transform 0.3s cubic-bezier(0.16, 1, 0.3, 1);
}}

.cta-button:hover::after {{
    transform: scaleX(1);
    transform-origin: left;
}}

@keyframes fadeIn {{
    from {{ opacity: 0; }}
    to {{ opacity: 1; }}
}}

/* =========================================
   SCROLL REVEAL SECTION
   ========================================= */
.content-section {{
    padding: 8rem 2rem;
    max-width: {width_px}px;
    margin: 0 auto;
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 3rem;
}}

.card {{
    background-color: var(--surface);
    padding: 2.5rem;
    border-radius: 8px;
    box-shadow: 0 4px 6px rgba(0,0,0,0.05);
}}

.card h3 {{
    font-size: 1.5rem;
    margin-bottom: 1rem;
    color: var(--accent);
}}

/* The initial hidden state for scroll elements */
.scroll-reveal {{
    opacity: 0;
    transform: translateY(50px);
    /* Transition applied to ALL properties when class changes */
    transition: opacity 0.8s cubic-bezier(0.16, 1, 0.3, 1), 
                transform 0.8s cubic-bezier(0.16, 1, 0.3, 1);
}}

/* Optional: Stagger delays via CSS */
.scroll-delay-1 {{ transition-delay: 0.1s; }}
.scroll-delay-2 {{ transition-delay: 0.3s; }}
.scroll-delay-3 {{ transition-delay: 0.5s; }}

/* The visible state triggered by JS */
.scroll-reveal.visible {{
    opacity: 1;
    transform: translateY(0);
}}

/* Accessibility: Respect user motion preferences */
@media (prefers-reduced-motion: reduce) {{
    *, *::before, *::after {{
        animation-duration: 0.01ms !important;
        animation-iteration-count: 1 !important;
        transition-duration: 0.01ms !important;
        scroll-behavior: auto !important;
    }}
    .scroll-reveal {{
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
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    
    <main>
        <!-- Initial Load Animations (@keyframes) -->
        <section class="hero">
            <h1 class="hero-title">
                {title_text.replace('tomorrow', '<span class="highlight">tomorrow</span>')}
            </h1>
            <p class="hero-subtitle">
                {body_text}
            </p>
            <a href="#explore" class="cta-button">Order now!</a>
        </section>

        <!-- Scroll Reveal Content (JS + CSS Transitions) -->
        <section id="explore" class="content-section">
            <div class="card scroll-reveal scroll-delay-1">
                <h3>Innovation at its Core</h3>
                <p>We blend design and technology to create memorable digital footprints. Scroll down to see the magic happen.</p>
            </div>
            <div class="card scroll-reveal scroll-delay-2">
                <h3>Custom Cookies</h3>
                <p>Experience tailored solutions that fit your exact needs, animating into view precisely when you need them to.</p>
            </div>
            <div class="card scroll-reveal scroll-delay-3">
                <h3>Future Proof</h3>
                <p>Built with performant CSS and modern JavaScript APIs to ensure smooth 60fps animations across all devices.</p>
            </div>
        </section>
    </main>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Dynamic Hero & Scroll-Reveal Logic

document.addEventListener('DOMContentLoaded', () => {{
    
    // 1. Setup Intersection Observer for Scroll Animations
    // This is the modern replacement for window.addEventListener('scroll') + getBoundingClientRect()
    // It's vastly more performant as it doesn't run on the main thread during scroll.
    
    const observerOptions = {{
        root: null,           // Use the viewport as the root
        rootMargin: '0px',    
        threshold: 0.15       // Trigger when 15% of the element is visible
    }};

    const observer = new IntersectionObserver((entries, observer) => {{
        entries.forEach(entry => {{
            // When the element intersects (enters viewport)
            if (entry.isIntersecting) {{
                // Add the visible class to trigger CSS transition
                entry.target.classList.add('visible');
                
                // Optional: Stop observing once revealed so it doesn't animate out and back in
                observer.unobserve(entry.target);
            }}
        }});
    }}, observerOptions);

    // 2. Select all elements to be animated on scroll and observe them
    const scrollElements = document.querySelectorAll('.scroll-reveal');
    
    scrollElements.forEach(el => {{
        observer.observe(el);
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
