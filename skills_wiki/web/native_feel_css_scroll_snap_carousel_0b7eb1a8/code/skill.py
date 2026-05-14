def create_component(
    output_dir: str,
    title_text: str = "Discover Horizons",
    body_text: str = "Swipe through the cards to experience smooth, hardware-accelerated CSS snapping.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#00bfff",     # CSS hex color for accent
    width_px: int = 1000,
    height_px: int = 650,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Native-Feel CSS Scroll-Snap Carousel.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme ===
    if color_scheme == "dark":
        bg_color = "#121212"
        text_color = "#ffffff"
        surface_color = "#1e1e1e"
        border_color = "#333333"
        hover_bg = "#2a2a2a"
    else:
        bg_color = "#f8f9fa"
        text_color = "#1a1a2e"
        surface_color = "#ffffff"
        border_color = "#e0e0e0"
        hover_bg = "#f0f0f0"

    # === CSS ===
    css = f"""/* Native-Feel CSS Scroll-Snap Carousel */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --text: {text_color};
    --accent: {accent_color};
    --surface: {surface_color};
    --border: {border_color};
    --hover-bg: {hover_bg};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background: var(--bg);
    color: var(--text);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow-x: hidden;
}}

.carousel-section {{
    width: min(var(--width), 95vw);
    display: flex;
    flex-direction: column;
    gap: 2rem;
}}

.carousel-header {{
    text-align: center;
}}

.carousel-header h1 {{
    font-size: 2.5rem;
    font-weight: 700;
    margin-bottom: 0.5rem;
}}

.carousel-header p {{
    font-size: 1.1rem;
    opacity: 0.8;
}}

.carousel-container {{
    position: relative;
    display: flex;
    align-items: center;
    width: 100%;
    border-radius: 12px;
}}

/* The magic scroll track */
.carousel-track {{
    display: grid;
    grid-auto-flow: column;
    grid-auto-columns: clamp(260px, 40%, 350px);
    gap: 1.5rem;
    overflow-x: auto;
    scroll-snap-type: x mandatory;
    overscroll-behavior-x: contain;
    padding: 1rem 0; /* Vertical padding for shadows */
    width: 100%;
    
    /* Center the first and last items visually */
    padding-inline: calc(50% - (clamp(260px, 40%, 350px) / 2));
    
    /* Hide scrollbar for clean look */
    scrollbar-width: none; /* Firefox */
}}

.carousel-track::-webkit-scrollbar {{
    display: none; /* Safari/Chrome */
}}

/* Individual Slide Cards */
.carousel-slide {{
    scroll-snap-align: center;
    background: var(--surface);
    border: 2px solid var(--border);
    border-radius: 16px;
    padding: 2rem;
    display: flex;
    flex-direction: column;
    gap: 1rem;
    transition: border-color 0.3s, transform 0.3s;
    user-select: none;
}}

.carousel-slide:hover {{
    border-color: var(--accent);
    transform: translateY(-4px);
}}

.slide-number {{
    font-size: 0.875rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: var(--accent);
}}

.slide-title {{
    font-size: 1.5rem;
    font-weight: 600;
}}

.slide-desc {{
    font-size: 1rem;
    line-height: 1.5;
    opacity: 0.8;
}}

/* Floating Action Buttons */
.scroll-btn {{
    position: absolute;
    z-index: 10;
    width: 48px;
    height: 48px;
    border-radius: 50%;
    background: var(--surface);
    border: 2px solid var(--border);
    color: var(--text);
    font-size: 1.25rem;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: background 0.2s, transform 0.2s, border-color 0.2s;
    box-shadow: 0 4px 12px rgba(0,0,0,0.2);
}}

.scroll-btn:hover {{
    background: var(--hover-bg);
    border-color: var(--accent);
    transform: scale(1.1);
}}

.scroll-btn:active {{
    transform: scale(0.95);
}}

.prev-btn {{
    left: 1rem;
}}

.next-btn {{
    right: 1rem;
}}

/* Dot Markers */
.carousel-markers {{
    display: flex;
    justify-content: center;
    gap: 0.75rem;
    margin-top: 1rem;
}}

.marker {{
    width: 12px;
    height: 12px;
    border-radius: 50%;
    border: 2px solid var(--border);
    background: transparent;
    cursor: pointer;
    padding: 0;
    transition: background 0.3s, border-color 0.3s, transform 0.3s;
}}

.marker:hover {{
    border-color: var(--accent);
    transform: scale(1.2);
}}

.marker.active {{
    background: var(--accent);
    border-color: var(--accent);
    transform: scale(1.2);
}}

@media (max-width: 768px) {{
    .carousel-track {{
        grid-auto-columns: 80%;
        padding-inline: calc(50% - 40%);
    }}
    .scroll-btn {{
        display: none; /* Hide buttons on small touch screens */
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
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <section class="carousel-section">
        <header class="carousel-header">
            <h1 class="title">{title_text}</h1>
            <p class="body-text">{body_text}</p>
        </header>
        
        <div class="carousel-container">
            <button class="scroll-btn prev-btn" aria-label="Scroll Left">&#10094;</button>
            
            <div class="carousel-track">
                <!-- Slides -->
                <div class="carousel-slide">
                    <span class="slide-number">Card 01</span>
                    <h2 class="slide-title">Responsive Grid</h2>
                    <p class="slide-desc">Utilizing grid-auto-flow to automatically stack items horizontally without complex wrapping logic.</p>
                </div>
                <div class="carousel-slide">
                    <span class="slide-number">Card 02</span>
                    <h2 class="slide-title">Hardware Snapping</h2>
                    <p class="slide-desc">Scroll-snap-type shifts the physics engine to the native browser, ensuring zero JS jank.</p>
                </div>
                <div class="carousel-slide">
                    <span class="slide-number">Card 03</span>
                    <h2 class="slide-title">Center Aligned</h2>
                    <p class="slide-desc">By using scroll-snap-align: center, the focused card immediately commands user attention.</p>
                </div>
                <div class="carousel-slide">
                    <span class="slide-number">Card 04</span>
                    <h2 class="slide-title">Spatial Padding</h2>
                    <p class="slide-desc">CSS padding-inline math ensures the first and last cards can naturally reach the center of the track.</p>
                </div>
                <div class="carousel-slide">
                    <span class="slide-number">Card 05</span>
                    <h2 class="slide-title">Future Ready</h2>
                    <p class="slide-desc">Prepares the visual DOM structure for CSS Overflow 5 features like scroll-markers and target-current.</p>
                </div>
                <div class="carousel-slide">
                    <span class="slide-number">Card 06</span>
                    <h2 class="slide-title">Accessible Design</h2>
                    <p class="slide-desc">Maintains standard tab-indexing, keyboard control, and Aria labeling for inclusive experiences.</p>
                </div>
            </div>
            
            <button class="scroll-btn next-btn" aria-label="Scroll Right">&#10095;</button>
        </div>
        
        <!-- Markers dynamically injected by JS -->
        <div class="carousel-markers" role="tablist"></div>
    </section>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Native-Feel CSS Scroll-Snap Carousel Logic
document.addEventListener('DOMContentLoaded', () => {{
    const track = document.querySelector('.carousel-track');
    const slides = document.querySelectorAll('.carousel-slide');
    const markersContainer = document.querySelector('.carousel-markers');
    const prevBtn = document.querySelector('.prev-btn');
    const nextBtn = document.querySelector('.next-btn');

    // 1. Generate Markers based on slide count
    slides.forEach((slide, index) => {{
        slide.dataset.index = index; // Tag slide for observer
        
        const marker = document.createElement('button');
        marker.classList.add('marker');
        marker.setAttribute('role', 'tab');
        marker.setAttribute('aria-label', `Go to slide ${{index + 1}}`);
        
        // Marker Click Event
        marker.addEventListener('click', () => {{
            slide.scrollIntoView({{ behavior: 'smooth', inline: 'center', block: 'nearest' }});
        }});
        
        markersContainer.appendChild(marker);
    }});

    const markers = document.querySelectorAll('.marker');

    // 2. Intersection Observer to handle Active State
    // rootMargin -50% ensures the intersection line is exactly in the middle of the track
    const observerOptions = {{
        root: track,
        rootMargin: '0px -50% 0px -50%', 
        threshold: 0
    }};

    const observer = new IntersectionObserver((entries) => {{
        entries.forEach(entry => {{
            if (entry.isIntersecting) {{
                const index = entry.target.dataset.index;
                
                // Update marker styles
                markers.forEach(m => m.classList.remove('active'));
                if (markers[index]) {{
                    markers[index].classList.add('active');
                }}
            }}
        }});
    }}, observerOptions);

    slides.forEach(slide => observer.observe(slide));

    // 3. Navigation Buttons Logic
    // Nudges the track by 85% of its visible width (mimicking CSS ::scroll-button default)
    const scrollAmount = () => track.clientWidth * 0.85;

    prevBtn.addEventListener('click', () => {{
        track.scrollBy({{ left: -scrollAmount(), behavior: 'smooth' }});
    }});

    nextBtn.addEventListener('click', () => {{
        track.scrollBy({{ left: scrollAmount(), behavior: 'smooth' }});
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
