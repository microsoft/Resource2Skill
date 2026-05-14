def create_component(
    output_dir: str,
    title_text: str = "Artisan Roasts",
    body_text: str = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Id laborum iste doloremque ab facere unde alias sit commodi accusamus. Eius ut molestiae nemo perspiciatis, pariatur numquam accusamus voluptatem libero sint.",
    color_scheme: str = "dark",
    accent_color: str = "#d4a373",
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Scroll-Triggered Clip-Path Reveal & Image Zoom effect.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Derive theme colors
    if color_scheme == "dark":
        bg_gradient = "linear-gradient(178deg, #3e2723, #1b110f)"
        text_color = "#f5f5f5"
        heading_color = "#ffffff"
    else:
        bg_gradient = "linear-gradient(178deg, #f5f0e6, #e3d5c8)"
        text_color = "#4a3b32"
        heading_color = "#2d201c"

    # Images for the grid layout
    img1 = "https://images.unsplash.com/photo-1497935586351-b67a49e012bf?auto=format&fit=crop&w=1200&q=80"
    img2 = "https://images.unsplash.com/photo-1511920170033-f8396924c348?auto=format&fit=crop&w=1200&q=80"

    css = f"""/* Scroll-Triggered Clip-Path Reveal & Image Zoom */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background: {bg_gradient};
    color: {text_color};
    overflow-x: hidden;
    /* Added min-height to allow scrolling to see the effect */
    min-height: 200vh; 
}}

/* Spacer to push content down so scroll is required */
.scroll-prompt {{
    height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    font-size: 1.5rem;
    letter-spacing: 2px;
    text-transform: uppercase;
    opacity: 0.7;
}}

.section {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    align-items: center;
    max-width: {width_px}px;
    margin: 0 auto;
}}

/* --- Image Boxes --- */
.image-box {{
    height: {height_px}px;
    overflow: hidden;
    position: relative;
}}

.image-box img {{
    width: 100%;
    height: 100%;
    object-fit: cover;
    transform: scale(1.5);
    /* Transition scale when revealed. Adding 300ms delay to sync with clip-path animation delay */
    transition: transform 1.2s cubic-bezier(0.17, 0.97, 0.38, 1) 0.3s;
}}

.image-box.revealed img {{
    transform: scale(1);
}}

/* --- Content Boxes --- */
.content-box {{
    padding-inline: 4em;
}}

.title {{
    font-size: 4em;
    color: {heading_color};
    margin-bottom: 0.25em;
    line-height: 1.1;
}}

.text {{
    font-size: 1.1em;
    line-height: 1.8;
    opacity: 0.85;
}}

/* --- Reveal Animation Mechanics --- */

/* Initial hidden states using clip-path inset */
[data-reveal="left"] {{
    clip-path: inset(0 100% 0 0);
}}

[data-reveal="right"] {{
    clip-path: inset(0 0 0 100%);
}}

/* The animation application */
[data-reveal="left"].revealed {{
    animation: reveal-left 1.2s cubic-bezier(0.17, 0.97, 0.38, 1) forwards 300ms;
}}

[data-reveal="right"].revealed {{
    animation: reveal-right 1.2s cubic-bezier(0.17, 0.97, 0.38, 1) forwards 300ms;
}}

/* Keyframes for sliding open the clip-path */
@keyframes reveal-left {{
    0% {{ clip-path: inset(0 100% 0 0); }}
    100% {{ clip-path: inset(0 0 0 0); }}
}}

@keyframes reveal-right {{
    0% {{ clip-path: inset(0 0 0 100%); }}
    100% {{ clip-path: inset(0 0 0 0); }}
}}

/* Responsive adjustments */
@media (max-width: 900px) {{
    .section {{
        grid-template-columns: 1fr;
    }}
    .image-box {{
        height: 50vh;
    }}
    .content-box {{
        padding: 3em 2em;
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
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    
    <div class="scroll-prompt">
        <p>Scroll Down</p>
        <p>↓</p>
    </div>

    <!-- Main Grid Section -->
    <section class="section">
        
        <!-- Row 1: Image Left, Text Right -->
        <div class="image-box" data-reveal="left">
            <img src="{img1}" alt="Coffee Beans">
        </div>
        <div class="content-box">
            <h2 class="title" data-reveal="right">{title_text}</h2>
            <p class="text" data-reveal="right">{body_text}</p>
        </div>

        <!-- Row 2: Text Left, Image Right (Checkerboard) -->
        <div class="content-box">
            <h2 class="title" data-reveal="left">Rich Aroma</h2>
            <p class="text" data-reveal="left">{body_text}</p>
        </div>
        <div class="image-box" data-reveal="right">
            <img src="{img2}" alt="Coffee Cup">
        </div>

    </section>
    
    <div class="scroll-prompt">
        <p>Scroll Up to re-trigger</p>
        <p>↑</p>
    </div>

    <script src="script.js"></script>
</body>
</html>"""

    js = f"""// Scroll-Triggered Clip-Path Reveal Logic
document.addEventListener('DOMContentLoaded', () => {{
    
    // Select all elements that have a data-reveal attribute
    const revealElements = document.querySelectorAll('[data-reveal]');

    // Set up the Intersection Observer
    const observerOptions = {{
        root: null, // use the viewport
        rootMargin: '0px',
        threshold: 0.15 // trigger when 15% of the element is visible
    }};

    const revealCallback = (entries, observer) => {{
        entries.forEach(entry => {{
            if (entry.isIntersecting) {{
                // Element has scrolled into view
                entry.target.classList.add('revealed');
            }} else {{
                // Element has scrolled out of view - remove class to allow re-animation
                // Remove this else block if you only want the animation to play once
                entry.target.classList.remove('revealed');
            }}
        }});
    }};

    const observer = new IntersectionObserver(revealCallback, observerOptions);

    // Observe each element
    revealElements.forEach(el => observer.observe(el));
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
