# Native CSS Scroll-Snap Carousel

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Native CSS Scroll-Snap Carousel

* **Core Visual Mechanism**: A horizontally scrolling gallery that fluidly glides and "snaps" to perfectly align individual cards upon resting. The layout utilizes a hidden scrollbar, replacing it with floating, translucent navigation arrows and interactive pagination dots.
* **Why Use This Skill (Rationale)**: Historically, carousels required heavy JavaScript libraries (like Slick or Swiper) to handle drag events, momentum, and positioning. Relying on CSS `scroll-snap` offloads the physics and momentum calculations to the browser's native rendering engine. This guarantees a butter-smooth, touch-native swiping experience on mobile, while requiring significantly less code.
* **Overall Applicability**: Perfect for image galleries, product feature highlights, pricing tiers, and testimonial sliders where horizontal space is constrained but content needs to be easily browsable.
* **Value Addition**: By hiding the default scrollbar and delegating the layout to CSS Flexbox + Scroll Snapping, you transform a mundane scrolling `div` into an app-like, premium component.
* **Browser Compatibility**: `scroll-snap-type` and smooth scrolling are universally supported in modern browsers. *Note:* The original tutorial showcases highly experimental CSS features (`::scroll-button`, `scroll-marker-group`, and `anchor-name`) which are currently only available in Chrome Canary behind flags. To guarantee reproducibility in stable browsers today, the provided code retains the pure CSS snapping core but implements the buttons and markers using minimal standard JavaScript.

### 2. Visual & Technical Breakdown

* **Step A: Core Visual Elements**
  - **Cards**: Vibrant, fixed-aspect-ratio containers (5:3) that utilize linear gradients to create a rich visual rhythm.
  - **Color Logic**: Dark, modern background (`#0a0a0e`) contrasted with vibrant accent controls (`#6f2aff`) and gradient overlays.
  - **Typography**: Clean, sans-serif font centered within the cards for maximum readability.
  - **Key CSS Properties**: `scroll-snap-type: x mandatory`, `scroll-snap-align: start`, `aspect-ratio: 5 / 3`, `scrollbar-width: none`.

* **Step B: Layout & Compositional Style**
  - **Layout System**: A CSS Flexbox container with `overflow-x: auto` dictates the scrolling track. Cards are sized with `flex: 0 0 20em` to prevent shrinking.
  - **Spacing**: A standardized `1rem` gap between cards ensures the snapping points feel consistent.
  - **Z-Index Layering**: Navigation arrows are positioned absolutely with `z-index: 10` to hover halfway outside the carousel wrapper, framing the content without obscuring it.

* **Step C: Interactive Behavior & Animations**
  - **Scroll Snapping**: As the user scrolls (or clicks a button), the browser naturally decelerates and forces the nearest card to align with the left edge (`scroll-snap-align: start`).
  - **Button State**: The navigation arrows gracefully fade to 50% opacity when the user reaches the boundaries of the scroll container.
  - **Pagination Sync**: Small dot markers highlight the currently visible card via an active state, dynamically calculated based on scroll position.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **Layout & Physics** | CSS `scroll-snap` & `flexbox` | Delivers native, hardware-accelerated momentum scrolling and perfectly aligned resting states without JS physics libraries. |
| **Hidden Scrollbar** | `::-webkit-scrollbar` / `scrollbar-width` | Maintains scroll functionality while removing the ugly OS-default scrollbar UI. |
| **Buttons & Markers** | JS Intersection Math + DOM | The tutorial's `::scroll-button` and anchor positioning are experimental and fail in current stable browsers. JS guarantees 100% functional reproducibility today. |
| **Button Action** | `element.scrollBy()` | Pairs seamlessly with native CSS `scroll-behavior: smooth` for elegant transitions. |

#### 3b. Complete Reproduction Code

```python
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
```

### 4. Accessibility & Performance Notes

* **Performance**: The core scrolling mechanism is fully delegated to the browser via CSS `scroll-snap-type`, ensuring GPU-accelerated framerates and natural momentum swiping on mobile devices. The JavaScript scroll listener is throttled using `window.requestAnimationFrame` to prevent layout thrashing and maintain 60 FPS during fast scrolls.
* **Accessibility (a11y)**: 
  - Although the visual scrollbar is hidden (`scrollbar-width: none`), the container retains its native scrollability. Users navigating via `Tab` key will automatically snap cards into view as focus moves inside them.
  - Buttons include `aria-label` tags (`"Previous slide"` / `"Next slide"`).
  - The pagination markers are built using semantic `<button>` elements (rather than divs) and include dynamically generated `aria-label` tags (`"Go to slide 1"`, etc.), allowing screen reader users to jump directly to specific content.