def create_component(
    output_dir: str,
    title_text: str = "Master Web Development",
    body_text: str = "Get our complete freelancing bundle to quit your job and earn a side-income.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#0d6efd",     # CSS hex color for accent (Bootstrap blue)
    width_px: int = 1200,
    height_px: int = 600,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Fading Focussed Hero Carousel.
    
    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme ===
    if color_scheme == "dark":
        slide_bg = "#000000"
        text_color = "#ffffff"
        overlay_opacity = "0.55"
        carousel_variant_class = ""
    else:
        slide_bg = "#ffffff"
        text_color = "#212529"
        overlay_opacity = "0.8" # Wash out the image heavily to let dark text read clearly
        carousel_variant_class = "carousel-dark"

    # === CSS ===
    css = f"""/* Fading Focussed Hero Carousel — generated component */
:root {{
    --slide-bg: {slide_bg};
    --text-color: {text_color};
    --accent: {accent_color};
    --overlay-opacity: {overlay_opacity};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    margin: 0;
    padding: 0;
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background-color: #e9ecef;
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 100vh;
}}

/* Component Wrapper Enforcing Dimensions */
.carousel-wrapper {{
    width: 100%;
    max-width: var(--width);
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
    background: var(--slide-bg);
}}

/* Slide Base Styling */
.carousel-item {{
    height: var(--height);
    background-color: var(--slide-bg);
    color: var(--text-color);
    position: relative;
}}

/* The image overlay trick for guaranteed contrast */
.overlay-image {{
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-position: center;
    background-size: cover;
    opacity: var(--overlay-opacity);
    z-index: 1;
    transition: transform 10s ease-out; /* subtle zoom effect */
}}

/* Optional subtle zoom animation on active slide */
.carousel-item.active .overlay-image {{
    transform: scale(1.05);
}}

/* Content Container Positioned at the Bottom */
.carousel-item .content-container {{
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    padding-bottom: 60px;
    padding-left: 10%;
    padding-right: 10%;
    z-index: 10;
    text-align: center;
}}

/* Typography Adjustments */
.content-container h1 {{
    font-weight: 700;
    font-size: clamp(2rem, 4vw, 3.5rem);
    margin-bottom: 1rem;
    text-shadow: 0 2px 10px rgba(0,0,0,0.1);
}}

.content-container .lead {{
    font-size: clamp(1rem, 2vw, 1.25rem);
    font-weight: 400;
    margin-bottom: 2rem;
    max-width: 800px;
    margin-left: auto;
    margin-right: auto;
}}

/* Custom Call to Action Button */
.custom-btn {{
    background-color: var(--accent);
    border-color: var(--accent);
    color: #ffffff;
    padding: 0.75rem 2rem;
    font-weight: 600;
    border-radius: 8px;
    transition: all 0.2s ease-in-out;
    text-decoration: none;
    display: inline-block;
}}

.custom-btn:hover {{
    background-color: var(--text-color);
    border-color: var(--text-color);
    color: var(--slide-bg);
    transform: translateY(-2px);
}}

/* Customizing Bootstrap Indicators */
.carousel-indicators {{
    margin-bottom: 1.5rem;
    z-index: 15;
}}

.carousel-indicators [data-bs-target] {{
    width: 30px;
    height: 4px;
    border-radius: 2px;
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
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
    <!-- Bootstrap 5 CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>

    <div class="carousel-wrapper">
        <!-- Carousel Container -->
        <div id="heroCarousel" class="carousel slide carousel-fade {carousel_variant_class}" data-bs-ride="carousel">
            
            <!-- Indicators -->
            <div class="carousel-indicators">
                <button type="button" data-bs-target="#heroCarousel" data-bs-slide-to="0" class="active" aria-current="true" aria-label="Slide 1"></button>
                <button type="button" data-bs-target="#heroCarousel" data-bs-slide-to="1" aria-label="Slide 2"></button>
                <button type="button" data-bs-target="#heroCarousel" data-bs-slide-to="2" aria-label="Slide 3"></button>
            </div>

            <!-- Slides -->
            <div class="carousel-inner">
                
                <!-- Slide 1: Fast interval, User inputs -->
                <div class="carousel-item active" data-bs-interval="4000">
                    <div class="overlay-image" style="background-image: url('https://images.unsplash.com/photo-1498050108023-c5249f4df085?auto=format&fit=crop&w=1920&q=80');"></div>
                    <div class="content-container">
                        <h1>{title_text}</h1>
                        <p class="lead">{body_text}</p>
                        <a class="custom-btn" href="#">Start Learning Today</a>
                    </div>
                </div>

                <!-- Slide 2: Medium interval -->
                <div class="carousel-item" data-bs-interval="5000">
                    <div class="overlay-image" style="background-image: url('https://images.unsplash.com/photo-1555066931-4365d14bab8c?auto=format&fit=crop&w=1920&q=80');"></div>
                    <div class="content-container">
                        <h1>Design Responsive Interfaces</h1>
                        <p class="lead">Learn to write clean, modular CSS and JavaScript that scales perfectly across every device dimension.</p>
                        <a class="custom-btn" href="#">View Curriculum</a>
                    </div>
                </div>

                <!-- Slide 3: Longer interval -->
                <div class="carousel-item" data-bs-interval="6000">
                    <div class="overlay-image" style="background-image: url('https://images.unsplash.com/photo-1522071820081-009f0129c71c?auto=format&fit=crop&w=1920&q=80');"></div>
                    <div class="content-container">
                        <h1>Join 3,100+ Developers</h1>
                        <p class="lead">Step out of your comfort zone and figure out things the hard way. Build a freelance business you can rely on.</p>
                        <a class="custom-btn" href="#">Read Success Stories</a>
                    </div>
                </div>

            </div>

            <!-- Controls -->
            <button class="carousel-control-prev" type="button" data-bs-target="#heroCarousel" data-bs-slide="prev">
                <span class="carousel-control-prev-icon" aria-hidden="true"></span>
                <span class="visually-hidden">Previous</span>
            </button>
            <button class="carousel-control-next" type="button" data-bs-target="#heroCarousel" data-bs-slide="next">
                <span class="carousel-control-next-icon" aria-hidden="true"></span>
                <span class="visually-hidden">Next</span>
            </button>

        </div>
    </div>

    <!-- Bootstrap 5 JS Bundle (includes Popper) -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Component initialization and behavior tracking
document.addEventListener('DOMContentLoaded', () => {{
    // The carousel is automatically initialized by Bootstrap's data-bs-* attributes.
    // However, we can listen to its native events to log behavior or add custom logic.
    
    const myCarouselElement = document.querySelector('#heroCarousel');
    
    myCarouselElement.addEventListener('slide.bs.carousel', event => {{
        // Fires immediately when the slide transition begins
        console.log(`Transitioning to slide ${{event.to}}`);
    }});

    myCarouselElement.addEventListener('slid.bs.carousel', event => {{
        // Fires when the slide transition has finished
        console.log(`Finished transition to slide ${{event.to}}`);
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
