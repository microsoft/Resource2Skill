# CSS-Only Scroll Snapping Carousel

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: CSS-Only Scroll Snapping Carousel

* **Core Visual Mechanism**: A smooth-scrolling image carousel created entirely without JavaScript. It utilizes CSS `scroll-snap-type` to lock images into view, `overflow-x: auto` to enable horizontal scrolling, and `scroll-behavior: smooth` combined with HTML anchor links (`<a href="#slide-1">`) to trigger animated transitions between slides.
* **Why Use This Skill (Rationale)**: Native CSS scroll snapping provides a highly performant, jank-free, and accessible carousel experience that leverages the browser's built-in scrolling physics. By relying on CSS and native anchor links rather than heavy JavaScript libraries, you drastically reduce payload size and eliminate hydration or execution delays.
* **Overall Applicability**: Perfect for hero sections, image galleries, product showcases, and minimal portfolio sites where lightweight performance is prioritized over complex auto-playing logic or drag-to-swipe physics.
* **Value Addition**: Transforms a basic horizontal list of images into an interactive, app-like carousel with pagination dots. It introduces spatial organization without adding third-party dependencies.
* **Browser Compatibility**: Excellent modern browser support. `scroll-snap-type`, `scroll-snap-align`, and `scroll-behavior: smooth` are fully supported in all major browsers (Chrome, Firefox, Safari, Edge). 

### 2. Visual & Technical Breakdown

* **Step A: Core Visual Elements**
  - **HTML Constructs**: A nested set of containers (`.slider-wrapper` > `.slider` > `img`), alongside a navigation container (`.slider-nav` > `a`). Each image has a unique `id` matching the `href` of its corresponding navigation anchor.
  - **Color Logic**: Uses a dark/space-themed aesthetic. Translucent white dots (`rgba(255, 255, 255, 0.75)`) serve as navigation, transitioning to solid white (`#ffffff`) on hover. A deep shadow (`box-shadow: 0 1.5rem 3rem -0.75rem rgba(0,0,0,0.25)`) creates physical depth.
  - **CSS Properties**: `scroll-snap-type` (axis and strictness), `scroll-snap-align` (element snapping point), `scroll-behavior` (smooth anchor jumping), `object-fit` (image scaling), and `aspect-ratio` (maintaining dimensions).

* **Step B: Layout & Compositional Style**
  - **Flexbox Grid**: The main `.slider` is a flex row. Setting `flex: 1 0 100%` on the images forces them to strictly take up exactly one full width of the parent container without wrapping or shrinking.
  - **Absolute Positioning**: The navigation dots are pulled out of the document flow using `position: absolute; bottom: 1.25rem; left: 50%; transform: translateX(-50%);` to center them over the images.
  - **Dimensions**: The video specifies a max-width of `48rem` (~768px) and a `16/9` aspect ratio. Images are clipped with a `0.5rem` border radius.

* **Step C: Interactive Behavior & Animations**
  - **Snapping**: `scroll-snap-type: x mandatory` forces the browser to aggressively snap to the nearest image boundary whenever the user scrolls or stops scrolling.
  - **Smooth Anchor Jumping**: Clicking a pagination dot relies on native HTML ID linking. Adding `scroll-behavior: smooth` to the `.slider` makes the browser animate the scroll to the ID rather than instantly jumping.
  - **Hover Effects**: The navigation dots feature a `transition: opacity ease 250ms`, scaling from `0.75` opacity to `1` on hover.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| Carousel scrolling | CSS `overflow-x: auto` | Creates the native horizontal scroll container without JS. |
| Slide snapping | CSS `scroll-snap-type` | Browser-native hardware-accelerated snapping physics. |
| Smooth transitions | CSS `scroll-behavior: smooth` | Animates the native HTML anchor jumps seamlessly. |
| Pagination links | HTML `<a>` tags targeting IDs | Zero-JS way to navigate specific views within an overflow container. |
| Responsive images | Flexbox + `object-fit: cover` | Prevents aspect ratio distortion when resizing the viewport. |

> **Feasibility Assessment**: 100%. The entire visual and interactive effect demonstrated in the tutorial is purely CSS/HTML based and is fully reproduced below.

#### 3b. Complete Reproduction Code

```python
def create_component(
    output_dir: str,
    title_text: str = "CSS Only Scroll Snapping Carousel",
    body_text: str = "A smooth, lightweight image slider built entirely without JavaScript.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#ffffff",     # CSS hex color for accent
    width_px: int = 800,
    height_px: int = 450,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the CSS-Only Scroll Snapping Carousel effect.
    
    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme ===
    if color_scheme == "dark":
        bg_color = "#111418"
        text_color = "#f4f4f5"
        shadow_color = "rgba(0, 0, 0, 0.7)"
        nav_bg = accent_color
    else:
        bg_color = "#f8f9fa"
        text_color = "#1a1a2e"
        shadow_color = "rgba(0, 0, 0, 0.15)"
        nav_bg = accent_color if accent_color != "#ffffff" else "#333333"

    # === CSS ===
    css = f"""/* CSS-Only Scroll Snapping Carousel */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --text: {text_color};
    --accent: {nav_bg};
    --shadow: {shadow_color};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background-color: var(--bg);
    color: var(--text);
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 2rem;
}}

header {{
    text-align: center;
    margin-bottom: 2rem;
}}

header h1 {{
    font-size: 1.5rem;
    font-weight: 600;
    margin-bottom: 0.5rem;
}}

header p {{
    font-size: 0.95rem;
    opacity: 0.8;
}}

/* --- Carousel Container --- */
.slider-wrapper {{
    position: relative;
    width: 100%;
    max-width: var(--width);
    height: var(--height);
    margin: 0 auto;
}}

/* --- The Scrolling Area --- */
.slider {{
    display: flex;
    width: 100%;
    height: 100%;
    overflow-x: auto;
    
    /* Core Snapping Logic */
    scroll-snap-type: x mandatory;
    scroll-behavior: smooth;
    
    /* Aesthetics */
    border-radius: 0.5rem;
    box-shadow: 0 1.5rem 3rem -0.75rem var(--shadow);
    
    /* Hide scrollbar for cleaner look (optional but recommended) */
    -ms-overflow-style: none;  /* IE and Edge */
    scrollbar-width: none;     /* Firefox */
}}

.slider::-webkit-scrollbar {{
    display: none; /* Chrome, Safari and Opera */
}}

/* --- The Images --- */
.slider img {{
    /* Take up exactly one full container width, never shrink */
    flex: 1 0 100%;
    height: 100%;
    object-fit: cover;
    
    /* Tell the browser where to snap to */
    scroll-snap-align: start;
}}

/* --- Navigation Overlay --- */
.slider-nav {{
    display: flex;
    column-gap: 1rem;
    position: absolute;
    bottom: 1.25rem;
    left: 50%;
    transform: translateX(-50%);
    z-index: 1;
}}

.slider-nav a {{
    width: 0.5rem;
    height: 0.5rem;
    border-radius: 50%;
    background-color: var(--accent);
    opacity: 0.5;
    transition: opacity 250ms ease, transform 250ms ease;
    text-decoration: none;
}}

.slider-nav a:hover,
.slider-nav a:focus {{
    opacity: 1;
    transform: scale(1.2);
}}

/* Respect user preferences for reduced motion */
@media (prefers-reduced-motion: reduce) {{
    .slider {{
        scroll-behavior: auto;
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
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <header>
        <h1>{title_text}</h1>
        <p>{body_text}</p>
    </header>

    <section class="slider-wrapper" aria-label="Image Carousel">
        <div class="slider">
            <!-- 
              IDs must match the anchor tags below.
              Using Unsplash placeholder images representing space (as in tutorial).
            -->
            <img id="slide-1" src="https://images.unsplash.com/photo-1614730321146-b6fa6a46bcb4?q=80&w=1200&auto=format&fit=crop" alt="3D rendering of an imaginary orange planet in space">
            <img id="slide-2" src="https://images.unsplash.com/photo-1614729939124-03290b56c9ce?q=80&w=1200&auto=format&fit=crop" alt="3D rendering of an imaginary green planet in space">
            <img id="slide-3" src="https://images.unsplash.com/photo-1543722530-d2c3201371e7?q=80&w=1200&auto=format&fit=crop" alt="3D rendering of an imaginary blue planet in space">
        </div>
        
        <div class="slider-nav" aria-label="Carousel Navigation">
            <a href="#slide-1" aria-label="Go to slide 1"></a>
            <a href="#slide-2" aria-label="Go to slide 2"></a>
            <a href="#slide-3" aria-label="Go to slide 3"></a>
        </div>
    </section>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    # Pure CSS execution means JS is empty, but provided to fulfill structural requirements
    js = f"""// CSS Only Carousel
// No JavaScript required for core functionality!
// Scroll snapping and navigation are handled entirely by CSS and HTML Anchor tags.

document.addEventListener('DOMContentLoaded', () => {{
    console.log("Carousel initialized without JavaScript dependencies.");
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
  - **`prefers-reduced-motion`**: Added a media query to disable `scroll-behavior: smooth` if the user has requested reduced motion in their OS settings. This ensures the anchor jump happens instantly without potentially nausea-inducing animations for sensitive users.
  - **Aria Labels**: Included `aria-label` attributes on the wrapper, navigation container, and individual dot tags. Because the dots are visually empty `<a href>` tags, screen readers need aria attributes to announce what the buttons actually do ("Go to slide 1").
  - **Alt text**: Included descriptive alt text on the `img` tags as explicitly called out in the tutorial.
* **Performance**:
  - **Zero JavaScript**: Because the layout uses purely native HTML jumps (`href="#slide-1"`) and native CSS physics (`scroll-snap-type`), there are no resize-observers or scroll-event-listeners clogging up the main thread.
  - **Hidden Scrollbars**: Standard implementation hides the native horizontal scrollbar using standard vendor prefixes (`::-webkit-scrollbar` and `scrollbar-width: none`) so the component looks like a native app widget rather than a raw web container.
  - **Hardware Acceleration**: Browsers inherently optimize scrolling rendering. Using native snapping offloads calculations to the GPU compositor layer out-of-the-box.