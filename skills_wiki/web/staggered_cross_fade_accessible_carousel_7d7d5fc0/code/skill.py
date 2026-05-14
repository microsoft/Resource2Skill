def create_component(
    output_dir: str,
    title_text: str = "Modern CSS Carousel",
    body_text: str = "A fully accessible, staggered cross-fade image slider built with CSS transitions and data-attribute state management.",
    color_scheme: str = "dark",
    accent_color: str = "#0ea5e9",
    width_px: int = 1000,
    height_px: int = 600,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Staggered Cross-Fade Carousel visual effect.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    if color_scheme == "dark":
        bg_color = "#0f172a"
        text_color = "#f8fafc"
        surface_color = "rgba(15, 23, 42, 0.7)"
    else:
        bg_color = "#f8fafc"
        text_color = "#0f172a"
        surface_color = "rgba(255, 255, 255, 0.85)"

    css = f"""/* Accessible Staggered Cross-Fade Carousel */
*, *::before, *::after {{
    box-sizing: border-box;
}}

body {{
    margin: 0;
    font-family: 'Inter', system-ui, sans-serif;
    background-color: {bg_color};
    color: {text_color};
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
}}

.carousel {{
    width: {width_px}px;
    height: {height_px}px;
    max-width: 100vw;
    position: relative;
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
}}

.carousel > ul {{
    margin: 0;
    padding: 0;
    list-style: none;
}}

.slide {{
    position: absolute;
    inset: 0;
    opacity: 0;
    /* 
      CORE TRICK: The outgoing slide waits 250ms before fading out.
      This ensures it stays fully opaque while the new slide fades in on top of it.
    */
    transition: 250ms opacity ease-in-out;
    transition-delay: 250ms;
}}

.slide > img {{
    display: block;
    width: 100%;
    height: 100%;
    object-fit: cover;
    object-position: center;
}}

.slide[data-active] {{
    opacity: 1;
    z-index: 1;
    /* The incoming slide fades in immediately */
    transition-delay: 0ms;
}}

.carousel-button {{
    position: absolute;
    z-index: 2;
    background: none;
    border: none;
    font-size: 3rem;
    top: 50%;
    transform: translateY(-50%);
    color: rgba(255, 255, 255, 0.6);
    cursor: pointer;
    border-radius: 0.25rem;
    padding: 0 0.5rem;
    background-color: rgba(0, 0, 0, 0.15);
    transition: all 0.2s ease;
}}

.carousel-button:hover,
.carousel-button:focus {{
    color: white;
    background-color: rgba(0, 0, 0, 0.4);
}}

.carousel-button:focus {{
    outline: 2px solid {accent_color};
    outline-offset: 2px;
}}

.carousel-button.prev {{
    left: 1rem;
}}

.carousel-button.next {{
    right: 1rem;
}}

/* Added to showcase the parameters requested */
.carousel-overlay {{
    position: absolute;
    bottom: 2rem;
    left: 2rem;
    z-index: 3;
    background: {surface_color};
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    padding: 1.5rem 2rem;
    border-radius: 8px;
    max-width: 450px;
    border: 1px solid rgba(255, 255, 255, 0.1);
}}

.carousel-overlay h1 {{
    margin: 0 0 0.5rem 0;
    font-size: 1.5rem;
    color: {accent_color};
}}

.carousel-overlay p {{
    margin: 0;
    line-height: 1.5;
    font-size: 0.95rem;
}}
"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>

    <section aria-label="Featured Photography">
        <div class="carousel" data-carousel>
            <button class="carousel-button prev" data-carousel-button="prev" aria-label="Previous slide">&#8656;</button>
            <button class="carousel-button next" data-carousel-button="next" aria-label="Next slide">&#8658;</button>

            <!-- Overlay injected to satisfy component parameters -->
            <div class="carousel-overlay">
                <h1>{title_text}</h1>
                <p>{body_text}</p>
            </div>

            <ul data-slides>
                <li class="slide" data-active>
                    <img src="https://images.unsplash.com/photo-1469474968028-56623f02e42e?auto=format&fit=crop&w=1200&q=80" alt="Lush mountain valley">
                </li>
                <li class="slide">
                    <img src="https://images.unsplash.com/photo-1447752875215-b2761acb3c5d?auto=format&fit=crop&w=1200&q=80" alt="Sunlight breaking through forest canopy">
                </li>
                <li class="slide">
                    <img src="https://images.unsplash.com/photo-1472214103451-9374bd1c798e?auto=format&fit=crop&w=1200&q=80" alt="Vast green mountain landscape">
                </li>
            </ul>
        </div>
    </section>

    <script src="script.js"></script>
</body>
</html>"""

    js = """document.addEventListener('DOMContentLoaded', () => {
    // Select all elements acting as carousel navigation buttons
    const buttons = document.querySelectorAll('[data-carousel-button]');

    buttons.forEach(button => {
        button.addEventListener('click', () => {
            // Determine direction based on the data attribute value
            const offset = button.dataset.carouselButton === 'next' ? 1 : -1;
            
            // Scope the selector to the specific carousel the button belongs to
            const slides = button.closest('[data-carousel]').querySelector('[data-slides]');
            const activeSlide = slides.querySelector('[data-active]');
            
            // Calculate new index
            let newIndex = [...slides.children].indexOf(activeSlide) + offset;

            // Handle wrap-around constraints
            if (newIndex < 0) newIndex = slides.children.length - 1;
            if (newIndex >= slides.children.length) newIndex = 0;

            // Update the dataset attributes to trigger CSS state changes
            slides.children[newIndex].dataset.active = true;
            delete activeSlide.dataset.active;
        });
    });
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
