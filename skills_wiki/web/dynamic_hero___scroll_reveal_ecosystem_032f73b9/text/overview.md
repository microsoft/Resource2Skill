### 1. High-level Design Pattern Extraction

> **Skill Name**: Dynamic Hero & Scroll-Reveal Ecosystem

* **Core Visual Mechanism**: A cohesive orchestration of three web animation pillars: 
  1. **Initial Load Animations**: Using CSS `@keyframes` and `transform` to slide and fade elements into place when the page loads (establishing spatial relationships).
  2. **Micro-interactions**: Using CSS `transition` properties to create fluid hover states on interactive elements (e.g., buttons expanding or shifting color).
  3. **Scroll-Driven Reveals**: Using JavaScript to detect when elements enter the viewport and applying CSS classes to trigger smooth `transform` and `opacity` transitions, making the page feel "alive" as the user consumes content.

* **Why Use This Skill (Rationale)**: Static pages feel lifeless. By introducing elements gradually (slide-ins, fade-ups), you guide the user's eye to the most important information sequentially. Hover transitions provide immediate tactile feedback, enhancing user confidence. Scroll reveals reward the user for scrolling, creating a rhythm of discovery that keeps them engaged.

* **Overall Applicability**: This is the gold standard for modern landing pages, SaaS marketing sites, portfolios, and editorial articles. Any page that aims to tell a sequential story benefits from scroll reveals and hero animations.

* **Value Addition**: Transforms a static document into an interactive experience. It adds a perception of premium quality, guides narrative flow, and prevents cognitive overload by only showing elements when they become relevant in the viewport.

* **Browser Compatibility**: Very high. CSS `@keyframes`, `transitions`, and `transforms` are universally supported. The `IntersectionObserver` API (the modern, performant replacement for the bounding-box scroll listener shown in the tutorial) is supported in all modern browsers (Chrome 51+, Safari 12.2+, Firefox 55+).

### 2. Visual & Technical Breakdown

* **Step A: Core Visual Elements**
  - **Color Logic**: A high-contrast background (e.g., dark `#121212` or stark white `#ffffff`) paired with a bold, saturated accent color (`#e63946` red from the tutorial). The accent color is used for targeted emphasis (underlines, buttons, key text).
  - **Typography**: Clean, geometric sans-serif fonts (like `Inter`) to maintain legibility while elements are in motion. Heavy font weights (700+) for headings to maximize the impact of spatial movements.
  - **CSS Constructs**: `transform: translate()` for sliding, `transform: scale()` for expanding, `opacity` for fading. The `transition` shorthand is used for hovers and reveals, while `animation` and `@keyframes` are used for autonomous on-load effects.

* **Step B: Layout & Compositional Style**
  - **Spatial Feel**: Sections are typically full-height (`100vh`) to allow distinct stages of the animation narrative. Ample whitespace (`padding: 5rem 2rem`) ensures animating elements have room to breathe and don't clash.
  - **Z-index Layering**: Text and interactive buttons sit above background shapes or images.
  - **Proportions**: Large hero headings (e.g., `4rem`), moderately sized CTA buttons (`padding: 1rem 2rem`), and content blocks staggered vertically to create a scrolling runway.

* **Step C: Interactive Behavior & Animations**
  - **Hero Load (`@keyframes`)**: The main heading enters using an `ease-out` timing function, starting off-screen (e.g., `translateX(-60%)`) and transparent, settling at `translateX(0)` over 0.6 seconds with `animation-fill-mode: forwards`.
  - **Hover Effects (`transition`)**: Buttons scale slightly (`scale(1.05)`) and change background color smoothly over 0.25 seconds.
  - **Scroll Reveal (JS + `transition`)**: Elements below the fold start with `opacity: 0` and `translateY(40px)`. When JavaScript detects they are in view, a `.visible` class is added, triggering a CSS transition to `opacity: 1` and `translateY(0)` over `0.6s ease-out`.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| Initial Load Animation | Pure CSS `@keyframes` | Best performance for autonomous on-load animations, running on the compositor thread. |
| Button Hover States | CSS `transition` | Simple, native interpolation between two states without JS overhead. |
| Text Accent (Squiggly line) | CSS `text-decoration` | Replaces the external SVG from the video with native CSS `text-decoration: underline wavy` for a zero-dependency, highly scalable equivalent. |
| Scroll Reveal Detection | JS `IntersectionObserver` | The tutorial used a `scroll` event listener with `getBoundingClientRect()`. `IntersectionObserver` is the modern, vastly more performant standard that avoids scroll-jank by moving calculations off the main thread. |
| Scroll Reveal Execution | CSS `.visible` Class | CSS handles the actual interpolation (opacity, transform) for hardware acceleration; JS only acts as the trigger. |

#### 3b. Complete Reproduction Code

```python
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
```

### 4. Accessibility & Performance Notes

* **Accessibility**: 
  - Crucially, a `@media (prefers-reduced-motion: reduce)` query is included in the CSS. If a user has disabled system-level animations (due to vestibular disorders or motion sickness), all transition and animation durations are set to near-zero, and scroll-hidden elements default to visible.
  - The HTML retains a semantic structure (`<main>`, `<section>`, `<h1>`, `<h3>`) regardless of the applied visual effects. Color contrast is ensured by mapping the theme strictly to high-contrast variables.
* **Performance**: 
  - Instead of binding a function to the `scroll` event and continuously calculating `getBoundingClientRect()` (which triggers expensive browser reflows/repaints as shown in the tutorial), this implementation uses the **Intersection Observer API**. This offloads visibility calculations to the browser's native engine, preventing jank and keeping the main thread free.
  - The CSS transitions strictly animate `transform` and `opacity`. These properties are hardware-accelerated (handled by the GPU compositor), preventing expensive layout recalculations during motion.