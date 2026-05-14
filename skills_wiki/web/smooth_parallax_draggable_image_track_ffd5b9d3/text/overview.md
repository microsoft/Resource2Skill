# Smooth Parallax Draggable Image Track

## Analysis

# Skill Strategy Document

### 1. High-level Design Pattern Extraction

> **Skill Name**: Smooth Parallax Draggable Image Track

* **Core Visual Mechanism**: A horizontally scrolling flexbox gallery that operates via direct mouse/touch drag rather than standard scrollbars. As the user drags the track left or right, the track translates physically, but the images inside counter-animate their `object-position`. This creates a buttery-smooth "window" parallax effect, where the images appear to pan inside their frames in the opposite direction of the drag. The movement is heavily smoothed using the Web Animations API with a 1.2s duration.
* **Why Use This Skill (Rationale)**: Standard horizontal scroll containers can feel rigid or completely tied to system scrolling physics. This pattern breaks out of native scrolling constraints to create a cinematic, highly tactile experience. The parallax effect creates an illusion of depth, making the flat images feel like physical viewports. The long animation duration (1200ms) gives the interaction a feeling of weight and inertia.
* **Overall Applicability**: Perfect for immersive portfolio galleries, premium e-commerce product showcases, photography websites, and hero sections where establishing a distinct, high-end mood is more important than rapid information density. 
* **Value Addition**: Transforms a basic list of images into a memorable interactive toy. It encourages users to physically engage with the page and increases the perceived production value of the site through its custom physics and fluid interpolation.
* **Browser Compatibility**: Requires modern browsers supporting the Web Animations API (`Element.animate()`) and CSS `object-fit`/`object-position`. Fully supported in all modern versions of Chrome, Safari, Firefox, and Edge.

### 2. Visual & Technical Breakdown

* **Step A: Core Visual Elements**
  - **Containers**: A wrapper (`.container`), a draggable track (`.image-track`), and a series of images (`.image`).
  - **Color Logic**: High contrast. Typically a stark black or dark background to make the images pop.
  - **Images**: Must use `object-fit: cover` to ensure they fill their frames regardless of aspect ratio, which is crucial for the parallax `object-position` math to work visually.
  - **Attributes**: Images must have `draggable="false"` to prevent the browser's native ghost-image drag behavior from interfering with the custom JS pointer tracking.

* **Step B: Layout & Compositional Style**
  - **Layout System**: The track is positioned using `position: absolute`, starting at `left: 50%` and `top: 50%` with a Y-translation of `-50%` to perfectly center it vertically.
  - **Display**: The track uses `display: flex` with a substantial `gap` to separate the frames.
  - **Sizing**: Images use viewport-relative or container-relative sizing (e.g., `max-width`, aspect ratios) so they scale consistently.

* **Step C: Interactive Behavior & Animations**
  - **State Tracking**: The component tracks the mouse down position (`mousedown at`), the delta (current position minus down position), and the previous total percentage moved.
  - **Math**: The `percentage` of movement is calculated relative to half the container's width (`maxDelta = width / 2`). This percentage is clamped between `0%` and `-100%`.
  - **Track Animation**: The track's translation maps directly to the percentage (e.g., moving to `translate(-45%, -50%)`).
  - **Parallax Animation**: The `object-position` of the images is calculated as `100 + nextPercentage`. At `0%` track translation, images are focused at `100% 50%` (right-aligned). At `-100%` track translation, images are focused at `0% 50%` (left-aligned).
  - **Smoothing**: Instead of updating CSS directly on `mousemove`, it triggers `.animate()` with a `duration` of `1200ms` and `fill: "forwards"`. The Web Animations API handles the complex interpolation, overriding the previous animation frame automatically and resulting in a liquid-smooth decay effect.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **Draggable Track** | JS Event Listeners | Requires tracking pointer down/move/up events to calculate deltas independently of native scroll. |
| **Smooth Interpolation** | Web Animations API | `element.animate()` handles overlapping animation frames gracefully, providing the "buttery" easing without needing a heavy library like GSAP or complex `requestAnimationFrame` math. |
| **Parallax Inner Images** | CSS `object-position` + JS | Modifying `object-position` via JS synchronously with the track's movement creates the panning window effect. |
| **Responsiveness** | CSS Flexbox + Clamp | Keeps the gallery frames looking correct without explicit JS resize handlers. |

> **Feasibility Assessment**: 100% reproducible. The logic maps perfectly to standard Web APIs and CSS features, packaged into a standalone component. Touch event listeners have been added alongside the original mouse listeners to ensure mobile functionality, which is essential for a modern component.

#### 3b. Complete Reproduction Code

```python
def create_component(
    output_dir: str,
    title_text: str = "Drag to Explore",
    body_text: str = "Interactive parallax image track",
    color_scheme: str = "dark",
    accent_color: str = "#ffffff",
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Parallax Draggable Image Track visual effect.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    if color_scheme == "dark":
        bg_color = "#0a0a0a"
        text_color = "#ffffff"
        hint_color = "rgba(255, 255, 255, 0.5)"
    else:
        bg_color = "#f4f4f5"
        text_color = "#18181b"
        hint_color = "rgba(0, 0, 0, 0.5)"

    css = f"""/* Smooth Parallax Draggable Image Track */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --text: {text_color};
    --accent: {accent_color};
    --hint: {hint_color};
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
    /* Prevent pull-to-refresh on mobile */
    overscroll-behavior-y: none; 
}}

.app-wrapper {{
    width: 100%;
    max-width: var(--width);
    height: var(--height);
    position: relative;
    overflow: hidden;
    background: var(--bg);
    box-shadow: 0 0 0 1px rgba(128,128,128,0.1);
}}

.header {{
    position: absolute;
    top: 40px;
    left: 40px;
    z-index: 10;
    pointer-events: none;
}}

.title {{
    font-size: 2rem;
    font-weight: 500;
    letter-spacing: -0.02em;
    margin-bottom: 8px;
}}

.body-text {{
    font-size: 1rem;
    color: var(--hint);
    font-weight: 400;
}}

#image-track {{
    display: flex;
    gap: 4vmin;
    position: absolute;
    left: 50%;
    top: 50%;
    transform: translate(0%, -50%);
    /* Prevent text/image selection during drag */
    user-select: none;
    -webkit-user-select: none;
    touch-action: pan-y;
}}

.image {{
    width: 40vmin;
    height: 56vmin;
    min-width: 250px;
    min-height: 350px;
    object-fit: cover;
    object-position: 100% 50%;
    border-radius: 8px;
    pointer-events: none; /* Let the track handle drag events */
    box-shadow: 0 20px 40px rgba(0,0,0,0.3);
}}

/* Interactive cursor states */
.app-wrapper:active #image-track {{
    cursor: grabbing;
}}

#image-track {{
    cursor: grab;
}}
"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="app-wrapper" id="wrapper">
        <div class="header">
            <h1 class="title">{title_text}</h1>
            <p class="body-text">{body_text}</p>
        </div>
        
        <div id="image-track" data-mouse-down-at="0" data-prev-percentage="0">
            <img class="image" src="https://images.unsplash.com/photo-1524781289445-e18c36281b31?q=80&w=1000&auto=format&fit=crop" draggable="false" alt="Gallery image 1" />
            <img class="image" src="https://images.unsplash.com/photo-1610194352361-4c81a6a8967e?q=80&w=1000&auto=format&fit=crop" draggable="false" alt="Gallery image 2" />
            <img class="image" src="https://images.unsplash.com/photo-1618202133208-280718d7bd3e?q=80&w=1000&auto=format&fit=crop" draggable="false" alt="Gallery image 3" />
            <img class="image" src="https://images.unsplash.com/photo-1495805442109-8b2138f6c41b?q=80&w=1000&auto=format&fit=crop" draggable="false" alt="Gallery image 4" />
            <img class="image" src="https://images.unsplash.com/photo-1548021682-27208e9e0e20?q=80&w=1000&auto=format&fit=crop" draggable="false" alt="Gallery image 5" />
            <img class="image" src="https://images.unsplash.com/photo-1496753480864-3e588e0269b3?q=80&w=1000&auto=format&fit=crop" draggable="false" alt="Gallery image 6" />
            <img class="image" src="https://images.unsplash.com/photo-1613346945084-35cccc812dd5?q=80&w=1000&auto=format&fit=crop" draggable="false" alt="Gallery image 7" />
            <img class="image" src="https://images.unsplash.com/photo-1516681100942-77d8e7f9dd97?q=80&w=1000&auto=format&fit=crop" draggable="false" alt="Gallery image 8" />
        </div>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    js = f"""document.addEventListener('DOMContentLoaded', () => {{
    const track = document.getElementById("image-track");
    const wrapper = document.getElementById("wrapper");

    const handleOnDown = e => {{
        // Unified coordinate extraction for mouse and touch
        const clientX = e.type.includes('mouse') ? e.clientX : e.touches[0].clientX;
        track.dataset.mouseDownAt = clientX;
    }};

    const handleOnUp = () => {{
        track.dataset.mouseDownAt = "0";
        track.dataset.prevPercentage = track.dataset.percentage || "0";
    }};

    const handleOnMove = e => {{
        if(track.dataset.mouseDownAt === "0") return;

        const clientX = e.type.includes('mouse') ? e.clientX : e.touches[0].clientX;
        const mouseDelta = parseFloat(track.dataset.mouseDownAt) - clientX;
        
        // The distance required to slide the entire track (half the container width)
        const maxDelta = wrapper.clientWidth / 2;
        
        const percentage = (mouseDelta / maxDelta) * -100;
        const nextPercentageUnconstrained = parseFloat(track.dataset.prevPercentage) + percentage;
        
        // Clamp between 0% and -100%
        const nextPercentage = Math.max(Math.min(nextPercentageUnconstrained, 0), -100);
        
        track.dataset.percentage = nextPercentage;
        
        // Animate the track container moving horizontally
        track.animate({{
            transform: `translate(${{nextPercentage}}%, -50%)`
        }}, {{ duration: 1200, fill: "forwards" }});
        
        // Animate the object-position of each image for the counter-parallax effect
        for(const image of track.getElementsByClassName("image")) {{
            image.animate({{
                objectPosition: `${{100 + nextPercentage}}% center`
            }}, {{ duration: 1200, fill: "forwards" }});
        }}
    }};

    // Mouse Events
    wrapper.addEventListener("mousedown", handleOnDown);
    window.addEventListener("mouseup", handleOnUp);
    window.addEventListener("mousemove", handleOnMove);

    // Touch Events (mobile support)
    wrapper.addEventListener("touchstart", handleOnDown, {{ passive: true }});
    window.addEventListener("touchend", handleOnUp);
    window.addEventListener("touchmove", handleOnMove, {{ passive: true }});
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

* **Accessibility**: This is a heavily custom, pointer-driven interaction. To make it accessible, the images contain `alt` tags, but screen-reader users and keyboard navigators would normally be left out. In a true production environment, keyboard event listeners (arrow keys) should be added to decrement/increment the percentage, and `aria-live` regions could announce the currently focused image.
* **Performance**: 
  - Using the Web Animations API (`.animate()`) combined with CSS `transform` is highly performant as it offloads the animation calculations to the browser's compositor thread (GPU acceleration).
  - The JS correctly skips calculations if `mouseDownAt` is `"0"`, saving unnecessary cycles during regular mouse movement.
  - Using `passive: true` on touch event listeners is implemented to ensure the browser doesn't delay scrolling, though we explicitly set `touch-action: pan-y` in CSS to allow native vertical scrolling but capture horizontal gestures for the slider.
  - Animating `object-position` can occasionally trigger repaints depending on the browser. While usually smooth, avoiding massive, uncompressed original images is recommended to keep decoding and rendering fast. The provided unsplash links use `&q=80&w=1000` to load reasonably sized assets.