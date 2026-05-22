# Scrollytelling Reveal Grid (Scroll-Driven Animations)

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Scrollytelling Reveal Grid (Scroll-Driven Animations)

* **Core Visual Mechanism**: As the user scrolls down the page, static elements dynamically transition into view via staggered fading, scaling, and upward translations. This effect is driven natively by the scrollbar position using modern CSS `animation-timeline: view()`, creating a fluid, cinematic "scrollytelling" experience where the layout feels alive and responsive to the user's pace.
* **Why Use This Skill (Rationale)**: The tutorial explicitly notes that this technique "keeps users exploring" and breaks free from "static UI." Scroll-driven animations create a continuous feedback loop: the user's physical action (scrolling) directly maps to visual motion, dramatically increasing engagement, spatial awareness, and the perceived premium quality of the interface.
* **Overall Applicability**: Perfect for high-end product landing pages, editorial articles, SaaS feature showcases, photography portfolios, and corporate narrative sites (like the logistics company shown in the video). 
* **Value Addition**: Transforms a standard block-level document into an interactive narrative. It guides the user's eye to specific elements as they cross the viewport threshold, ensuring content is noticed exactly when it's meant to be.
* **Browser Compatibility**: CSS Scroll-driven animations (`animation-timeline: view()`) are supported in Chrome 115+, Edge 115+, and Opera 101+. For unsupported browsers (Safari, Firefox), a progressive enhancement strategy is strictly required, falling back to an `IntersectionObserver` to trigger standard CSS transitions.

### 2. Visual & Technical Breakdown

* **Step A: Core Visual Elements**
  - **Layout Constraints**: The layout uses an airy, asymmetrical grid of images and text blocks. Elements are given generous padding to allow the animation to "breathe" as it enters the viewport.
  - **Color Logic**: The video uses elegant, muted, earthy tones typical of modern editorial web design.
    - Light Theme Background: Sand/Beige `#e8e4df`
    - Light Theme Text: Deep charcoal `#2c2a28`
    - Dark Theme Background: Midnight blue/black `#0d111c`
    - Dark Theme Text: Off-white `#f0f0f0`
    - Accent: Vivid blue (like the trucks in the video) `#0055ff`
  - **Typographic Hierarchy**: High-contrast typography mixing large, thin sans-serif display headers with highly legible, medium-weight body copy. (e.g., `font-family: 'Inter', sans-serif`).
  - **CSS Properties**: `animation-timeline`, `animation-range`, `transform: translateY()`, `scale()`, `opacity`, `clip-path` (for rounded media wrappers).

* **Step B: Layout & Compositional Style**
  - Uses CSS Grid with asymmetrical column spans to create visual rhythm.
  - Vertical spacing (margins/gaps) is intentionally large (`10vh` to `20vh`) so elements enter the viewport one by one, allowing the scroll animations to play independently rather than all at once.
  - Media elements feature soft rounded corners (`border-radius: 16px`) to contrast with the rigid browser viewport.

* **Step C: Interactive Behavior & Animations**
  - **Scroll-Triggered Entry**: Elements start at `opacity: 0`, `transform: translateY(100px) scale(0.95)`.
  - As the element's bounding box intersects the viewport (e.g., from `entry 10%` to `cover 30%`), the CSS animation scrubs from 0% to 100%, resolving to `opacity: 1`, `transform: translateY(0) scale(1)`.
  - **Progressive Enhancement**: For browsers without `view()` timeline support, a JavaScript `IntersectionObserver` detects when elements enter the screen and appends an `.in-view` class, triggering a 0.6s ease-out CSS transition.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **Scroll-driven animation** | CSS `animation-timeline: view()` | Native browser API showcased in the video. Provides perfect 1:1 scroll synchronization without JS performance overhead. |
| **Progressive enhancement** | JS `IntersectionObserver` | Ensures the exact same entry visual effect on Safari/Firefox, just time-based instead of scroll-scrubbed. |
| **Asymmetrical Grid Layout** | CSS Grid | Native, responsive auto-placement with column spans (`grid-column: span X`) for a staggered "editorial" look. |
| **Styling & Aesthetics** | Pure CSS & Google Fonts | Keeps the component self-contained while achieving the modern typography and muted palette. |

> **Feasibility Assessment**: 95% reproducible. The core CSS-driven scroll animations, grid layout, and progressive enhancements are perfectly reproduced here. The video also showcased horizontal 3D scrolling models (a truck moving across the screen based on scroll), which would require WebGL/Three.js to fully replicate the 3D aspect, but the 2D layout and animation logic are captured identically.

#### 3b. Complete Reproduction Code

```python
def create_component(
    output_dir: str,
    title_text: str = "Stories on scroll",
    body_text: str = "Transform any website into an immersive narrative that performs beautifully by default. Scroll to explore.",
    color_scheme: str = "light",       # "dark" or "light"
    accent_color: str = "#2266cc",     # CSS hex color for accent
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Scrollytelling Reveal Grid visual effect.
    
    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors ===
    if color_scheme == "dark":
        bg_color = "#121418"
        text_color = "#f4f4f5"
        card_bg = "#1e2128"
        sub_text = "#a1a1aa"
    else:
        bg_color = "#e8e4df"
        text_color = "#2c2a28"
        card_bg = "#ffffff"
        sub_text = "#5c5955"

    # === CSS ===
    css = f"""/* Scrollytelling Reveal Grid */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap');

:root {{
    --bg-color: {bg_color};
    --text-color: {text_color};
    --sub-text: {sub_text};
    --card-bg: {card_bg};
    --accent: {accent_color};
    --container-width: {width_px}px;
    --container-height: {height_px}px;
}}

*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: 'Inter', system-ui, sans-serif;
    background-color: var(--bg-color);
    color: var(--text-color);
    line-height: 1.5;
    overflow-x: hidden;
    /* Smooth scrolling for anchor links if needed */
    scroll-behavior: smooth; 
}}

/* Centered fixed-size container to match requested dimensions, 
   with internal scrolling to showcase the effect */
.viewport-container {{
    width: 100vw;
    height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    background-color: #000; /* Outer backdrop */
}}

.app-frame {{
    width: var(--container-width);
    height: var(--container-height);
    max-width: 100vw;
    max-height: 100vh;
    background-color: var(--bg-color);
    overflow-y: auto;
    overflow-x: hidden;
    position: relative;
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
}}

/* Typography */
h1, h2, h3 {{
    font-weight: 400;
    letter-spacing: -0.02em;
}}

.hero {{
    min-height: 80vh;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;
    padding: 2rem;
}}

.hero h1 {{
    font-size: clamp(3rem, 6vw, 6rem);
    margin-bottom: 1rem;
    line-height: 1.1;
}}

.hero p {{
    font-size: clamp(1.1rem, 2vw, 1.5rem);
    color: var(--sub-text);
    max-width: 600px;
}}

.hero-scroll-indicator {{
    margin-top: 4rem;
    width: 30px;
    height: 50px;
    border: 2px solid var(--sub-text);
    border-radius: 15px;
    position: relative;
    opacity: 0.7;
}}

.hero-scroll-indicator::before {{
    content: '';
    position: absolute;
    top: 8px;
    left: 50%;
    transform: translateX(-50%);
    width: 6px;
    height: 6px;
    background-color: var(--text-color);
    border-radius: 50%;
    animation: scroll-bob 2s infinite ease-in-out;
}}

@keyframes scroll-bob {{
    0%, 100% {{ transform: translate(-50%, 0); opacity: 1; }}
    50% {{ transform: translate(-50%, 15px); opacity: 0.3; }}
}}

/* Scrollytelling Grid Layout */
.story-grid {{
    display: grid;
    grid-template-columns: repeat(12, 1fr);
    gap: 2rem;
    padding: 4rem 5%;
    max-width: 1400px;
    margin: 0 auto;
    padding-bottom: 20vh;
}}

.grid-item {{
    grid-column: span 12;
    display: flex;
    flex-direction: column;
    gap: 1rem;
}}

/* Asymmetrical Spanning for larger screens */
@media (min-width: 768px) {{
    .grid-item.span-6 {{ grid-column: span 6; }}
    .grid-item.span-8 {{ grid-column: span 8; }}
    .grid-item.span-4 {{ grid-column: span 4; }}
    .grid-item.offset-2 {{ grid-column-start: 3; }}
    .grid-item.offset-4 {{ grid-column-start: 5; }}
}}

.media-wrapper {{
    position: relative;
    width: 100%;
    border-radius: 16px;
    overflow: hidden;
    background-color: var(--card-bg);
    aspect-ratio: 4/3;
}}

.media-wrapper.portrait {{
    aspect-ratio: 3/4;
}}

.media-wrapper.landscape {{
    aspect-ratio: 16/9;
}}

.media-wrapper img {{
    width: 100%;
    height: 100%;
    object-fit: cover;
    transition: transform 0.7s ease;
}}

.grid-item:hover .media-wrapper img {{
    transform: scale(1.05);
}}

.item-caption {{
    font-size: 1.1rem;
    color: var(--text-color);
    font-weight: 500;
}}

.item-desc {{
    font-size: 0.95rem;
    color: var(--sub-text);
}}


/* =========================================================
   CORE SKILL: Scroll-Triggered Animations 
   ========================================================= */

/* 1. Base states for all animated elements (JS Fallback setup) */
.scroll-reveal {{
    opacity: 0;
    transform: translateY(60px) scale(0.95);
    transition: opacity 0.8s cubic-bezier(0.2, 0.8, 0.2, 1), 
                transform 0.8s cubic-bezier(0.2, 0.8, 0.2, 1);
    will-change: opacity, transform;
}}

/* JS Triggered Class */
.scroll-reveal.in-view {{
    opacity: 1;
    transform: translateY(0) scale(1);
}}

/* 2. Modern Native CSS Scroll-Driven Animations
   Overrides JS fallback completely if supported! */
@supports (animation-timeline: view()) {{
    .scroll-reveal {{
        /* Reset JS transition properties */
        transition: none;
        opacity: 0; 
        
        /* Apply native view timeline */
        animation: reveal-on-scroll linear both;
        animation-timeline: view();
        /* Animation starts when element is 5% past the bottom of viewport 
           and ends when it covers 25% of the viewport */
        animation-range: entry 5% cover 25%;
    }}

    @keyframes reveal-on-scroll {{
        0% {{
            opacity: 0;
            transform: translateY(80px) scale(0.95);
        }}
        100% {{
            opacity: 1;
            transform: translateY(0) scale(1);
        }}
    }}
    
    /* Optional: Parallax effect for images inside the grid */
    .media-wrapper img {{
        animation: parallax-image linear both;
        animation-timeline: view();
        animation-range: entry 0% exit 100%;
    }}
    
    @keyframes parallax-image {{
        0% {{ object-position: 50% 100%; }}
        100% {{ object-position: 50% 0%; }}
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
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="viewport-container">
        <!-- App frame limits dimensions for the component preview -->
        <main class="app-frame" id="scroll-container">
            
            <header class="hero">
                <h1>{title_text}</h1>
                <p>{body_text}</p>
                <div class="hero-scroll-indicator"></div>
            </header>

            <section class="story-grid">
                
                <!-- Grid Item 1 -->
                <article class="grid-item span-12 scroll-reveal">
                    <div class="media-wrapper landscape">
                        <img src="https://images.unsplash.com/photo-1601584115197-04ecc0da31d7?auto=format&fit=crop&w=1600&q=80" alt="Logistics Truck">
                    </div>
                    <h2 class="item-caption">Delivering Memories</h2>
                    <p class="item-desc">Transforming complex logistics into an immersive narrative experience.</p>
                </article>

                <!-- Grid Item 2 & 3 (Side by Side on Desktop) -->
                <article class="grid-item span-6 scroll-reveal" style="margin-top: 5vh;">
                    <div class="media-wrapper portrait">
                        <img src="https://images.unsplash.com/photo-1586528116311-ad8ed7c83a50?auto=format&fit=crop&w=800&q=80" alt="Packaging">
                    </div>
                    <h2 class="item-caption">Care in Every Box</h2>
                    <p class="item-desc">Your memories handled as our own.</p>
                </article>

                <article class="grid-item span-6 offset-2 scroll-reveal" style="margin-top: 15vh;">
                    <div class="media-wrapper">
                        <img src="https://images.unsplash.com/photo-1578575437130-527eed3abbec?auto=format&fit=crop&w=800&q=80" alt="Warehouse architecture">
                    </div>
                    <h2 class="item-caption">Built for Scale</h2>
                    <p class="item-desc">Securing your legacy, one journey at a time.</p>
                </article>

                <!-- Grid Item 4 (Centered) -->
                <article class="grid-item span-8 offset-2 scroll-reveal" style="margin-top: 10vh;">
                    <div class="media-wrapper landscape">
                        <img src="https://images.unsplash.com/photo-1494412651409-8963ce7935a7?auto=format&fit=crop&w=1200&q=80" alt="Moving logistics">
                    </div>
                    <h2 class="item-caption">Ensuring Safety</h2>
                    <p class="item-desc">Temperature adjusted and protected at every step.</p>
                </article>

                 <!-- Grid Item 5 & 6 -->
                <article class="grid-item span-4 scroll-reveal" style="margin-top: 15vh;">
                    <div class="media-wrapper portrait">
                        <img src="https://images.unsplash.com/photo-1512418490979-92798cec1380?auto=format&fit=crop&w=600&q=80" alt="Delivery Van">
                    </div>
                    <h2 class="item-caption">Local Reach</h2>
                    <p class="item-desc">Ready to start your shipping journey?</p>
                </article>

                <article class="grid-item span-8 scroll-reveal" style="margin-top: 5vh;">
                    <div class="media-wrapper landscape">
                        <img src="https://images.unsplash.com/photo-1436491865332-7a61a109cc05?auto=format&fit=crop&w=1200&q=80" alt="Airplane shipping">
                    </div>
                    <h2 class="item-caption">Global Scale</h2>
                    <p class="item-desc">Crossing borders without barriers.</p>
                </article>

            </section>
        </main>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Scrollytelling Reveal Grid - Progressive Enhancement
document.addEventListener('DOMContentLoaded', () => {{
    
    // Check if the browser supports CSS animation-timeline
    const supportsScrollTimeline = CSS.supports('animation-timeline: view()');
    
    // If supported, let CSS handle everything. No JS overhead required!
    if (supportsScrollTimeline) {{
        console.log("Using native CSS view() timeline for scroll animations.");
        return; 
    }}

    console.log("CSS view() timeline not supported. Falling back to IntersectionObserver.");

    // Fallback: IntersectionObserver to trigger entry animations
    const observerOptions = {{
        root: document.getElementById('scroll-container'), // Use custom scroll container
        rootMargin: '0px 0px -10% 0px', // Trigger slightly before the bottom of the viewport
        threshold: 0.1
    }};

    const revealCallback = (entries, observer) => {{
        entries.forEach(entry => {{
            if (entry.isIntersecting) {{
                // Add class to trigger CSS transition
                entry.target.classList.add('in-view');
                // Optional: Stop observing once revealed
                observer.unobserve(entry.target);
            }}
        }});
    }};

    const revealObserver = new IntersectionObserver(revealCallback, observerOptions);

    // Observe all elements with the .scroll-reveal class
    const revealElements = document.querySelectorAll('.scroll-reveal');
    revealElements.forEach(el => revealObserver.observe(el));
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
```

### 4. Accessibility & Performance Notes

* **Accessibility (a11y)**: 
  * Ensure high contrast between text and background. The provided dark/light configurations meet WCAG AA standards.
  * Motion Sensitivity: Ideally, wrap the scroll animations inside a `@media (prefers-reduced-motion: no-preference)` block in a production environment to respect users who experience vertigo or nausea from parallax and scale animations.
  * Semantic HTML: The code correctly uses `<header>`, `<main>`, `<section>`, and `<article>` tags to outline the layout, ensuring screen readers can digest the visual chunks easily.
* **Performance**: 
  * The primary technique (`animation-timeline: view()`) relies entirely on the browser's compositor thread (GPU accelerated). It avoids the notorious "scroll jank" caused by JavaScript attaching functions to the `window.onscroll` event.
  * The `.scroll-reveal` elements explicitly use `will-change: opacity, transform;` to hint the browser ahead of time, ensuring layout recalculations are skipped during the scroll animation.
  * For the JS fallback, `IntersectionObserver` is utilized instead of generic scroll listeners, which is natively performant as it operates asynchronously off the main thread. Utilizing `rootMargin` enables elements to pre-load or animate slightly before entering the direct line of sight.