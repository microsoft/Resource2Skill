def create_component(
    output_dir: str,
    title_text: str = "CSS-Snap Carousel",
    body_text: str = "Swipe or use the arrows to explore. Driven by native CSS scroll snapping.",
    color_scheme: str = "dark",
    accent_color: str = "#6f2aff",
    width_px: int = 1000,
    height_px: int = 600,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Native CSS Scroll-Snap Carousel.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    if color_scheme == "dark":
        bg_color = "#0a0a0e"
        text_color = "#ffffff"
        surface_color = "#1e1e24"
        body_text_color = "#a0a0a5"
    else:
        bg_color = "#f4f4f8"
        text_color = "#111111"
        surface_color = "#e2e2e8"
        body_text_color = "#555555"

    css = f"""/* Native CSS Scroll-Snap Carousel */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --text: {text_color};
    --text-muted: {body_text_color};
    --accent: {accent_color};
    --surface: {surface_color};
}}

body {{
    font-family: 'Inter', system-ui, sans-serif;
    background: var(--bg);
    color: var(--text);
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    overflow-x: hidden;
}}

.header {{
    text-align: center;
    margin-bottom: 2rem;
    padding: 0 1rem;
}}

.header h1 {{
    font-size: 2.5rem;
    margin-bottom: 0.5rem;
    font-weight: 700;
    letter-spacing: -0.02em;
}}

.header p {{
    color: var(--text-muted);
    font-size: 1.1rem;
    max-width: 500px;
    margin: 0 auto;
}}

.carousel-wrapper {{
    position: relative;
    width: calc(100% - 80px);
    max-width: {width_px}px;
    margin: 0 auto;
}}

.carousel {{
    display: flex;
    overflow-x: auto;
    scroll-snap-type: x mandatory;
    scroll-behavior: smooth;
    gap: 1.5rem;
    padding-bottom: 1rem;
    position: relative;
    
    /* Hide standard scrollbars */
    scrollbar-width: none; /* Firefox */
    -ms-overflow-style: none; /* IE/Edge */
}}

.carousel::-webkit-scrollbar {{
    display: none; /* Chrome/Safari */
}}

.card {{
    flex: 0 0 20rem;
    aspect-ratio: 5 / 3;
    background-color: var(--surface);
    border-radius: 1rem;
    display: flex;
    align-items: center;
    justify-content: center;
    scroll-snap-align: start;
    font-size: 1.5rem;
    font-weight: 600;
    color: #ffffff; /* Always white for gradients */
    box-shadow: 0 10px 20px rgba(0,0,0,0.1);
    transition: transform 0.3s ease;
}}

/* Generate vibrant gradients for cards based on accent color */
.card:nth-child(1) {{ background: linear-gradient(135deg, var(--accent), #ff6b6b); }}
.card:nth-child(2) {{ background: linear-gradient(135deg, #4ecdc4, var(--accent)); }}
.card:nth-child(3) {{ background: linear-gradient(135deg, #ffe66d, #ff6b6b); }}
.card:nth-child(4) {{ background: linear-gradient(135deg, var(--accent), #a8e6cf); }}
.card:nth-child(5) {{ background: linear-gradient(135deg, #d4a5a5, var(--accent)); }}
.card:nth-child(6) {{ background: linear-gradient(135deg, #9b5de5, var(--accent)); }}

@media (max-width: 600px) {{
    .card {{
        flex: 0 0 100%;
    }}
    .carousel-wrapper {{
        width: 100%;
        padding: 0 1rem;
    }}
    .scroll-btn {{
        display: none !important; /* Rely on touch swiping on mobile */
    }}
}}

/* Navigation Controls */
.scroll-btn {{
    position: absolute;
    top: calc(50% - 0.5rem);
    transform: translateY(-50%);
    width: 50px;
    height: 50px;
    border-radius: 50%;
    background-color: var(--accent);
    color: white;
    border: none;
    font-size: 1.5rem;
    cursor: pointer;
    z-index: 10;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: opacity 0.3s, background-color 0.2s;
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}}

.scroll-btn:hover:not(:disabled) {{
    filter: brightness(1.1);
}}

.scroll-btn.left {{
    left: -25px;
}}

.scroll-btn.right {{
    right: -25px;
}}

.scroll-btn:disabled {{
    opacity: 0.4;
    cursor: auto;
    box-shadow: none;
}}

.markers {{
    display: flex;
    justify-content: center;
    gap: 0.6rem;
    margin-top: 1.5rem;
}}

.marker {{
    width: 10px;
    height: 10px;
    border-radius: 50%;
    background-color: var(--surface);
    border: none;
    cursor: pointer;
    transition: background-color 0.3s, transform 0.2s;
}}

.marker.active {{
    background-color: var(--accent);
    transform: scale(1.3);
}}
"""

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
    <div class="header">
        <h1>{title_text}</h1>
        <p>{body_text}</p>
    </div>

    <div class="carousel-wrapper">
        <button class="scroll-btn left" aria-label="Previous slide" disabled>&#8592;</button>
        
        <div class="carousel">
            <div class="card">Card 1</div>
            <div class="card">Card 2</div>
            <div class="card">Card 3</div>
            <div class="card">Card 4</div>
            <div class="card">Card 5</div>
            <div class="card">Card 6</div>
        </div>
        
        <button class="scroll-btn right" aria-label="Next slide">&#8594;</button>
        
        <div class="markers">
            <!-- Markers generated by JS -->
        </div>
    </div>

    <script src="script.js"></script>
</body>
</html>"""

    js = f"""document.addEventListener('DOMContentLoaded', () => {{
    const carousel = document.querySelector('.carousel');
    const cards = document.querySelectorAll('.card');
    const markersContainer = document.querySelector('.markers');
    const btnLeft = document.querySelector('.scroll-btn.left');
    const btnRight = document.querySelector('.scroll-btn.right');

    if (!carousel || cards.length === 0) return;

    // 1. Generate Interactive Markers
    cards.forEach((_, i) => {{
        const marker = document.createElement('button');
        marker.classList.add('marker');
        if (i === 0) marker.classList.add('active');
        marker.setAttribute('aria-label', `Go to slide ${{i + 1}}`);
        
        marker.addEventListener('click', () => {{
            const scrollTarget = cards[i].offsetLeft - carousel.offsetLeft;
            carousel.scrollTo({{ left: scrollTarget, behavior: 'smooth' }});
        }});
        
        markersContainer.appendChild(marker);
    }});

    const markers = document.querySelectorAll('.marker');

    // 2. Synchronize UI State with Scroll Position
    const updateState = () => {{
        const scrollPos = carousel.scrollLeft;
        const maxScroll = carousel.scrollWidth - carousel.clientWidth;
        
        // Disable buttons at bounds
        btnLeft.disabled = scrollPos <= 5;
        btnRight.disabled = scrollPos >= maxScroll - 5;

        // Determine which card is currently closest to the left edge
        let activeIndex = 0;
        let minDiff = Infinity;
        
        cards.forEach((card, index) => {{
            // Calculate distance between current scroll view and the card's position
            const diff = Math.abs((card.offsetLeft - carousel.offsetLeft) - scrollPos);
            if (diff < minDiff) {{
                minDiff = diff;
                activeIndex = index;
            }}
        }});

        // Update dot highlights
        markers.forEach((m, i) => m.classList.toggle('active', i === activeIndex));
    }};

    // Use requestAnimationFrame to throttle scroll events for performance
    let isScrolling;
    carousel.addEventListener('scroll', () => {{
        window.cancelAnimationFrame(isScrolling);
        isScrolling = window.requestAnimationFrame(updateState);
    }});
    
    window.addEventListener('resize', updateState);

    // 3. Arrow Button Listeners
    const getScrollAmount = () => {{
        // Get width of a card plus the flex gap
        const gapStr = window.getComputedStyle(carousel).gap;
        const gap = gapStr === 'normal' ? 0 : parseFloat(gapStr) || 16;
        return cards[0].offsetWidth + gap;
    }};

    btnLeft.addEventListener('click', () => {{
        carousel.scrollBy({{ left: -getScrollAmount(), behavior: 'smooth' }});
    }});

    btnRight.addEventListener('click', () => {{
        carousel.scrollBy({{ left: getScrollAmount(), behavior: 'smooth' }});
    }});
}});
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
