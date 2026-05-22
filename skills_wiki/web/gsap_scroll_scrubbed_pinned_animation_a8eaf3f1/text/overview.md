# GSAP Scroll-Scrubbed Pinned Animation

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: GSAP Scroll-Scrubbed Pinned Animation

* **Core Visual Mechanism**: This pattern uses **scroll-driven animation pinning** combined with **timeline scrubbing**. When a specific container scrolls into the center of the viewport, it is "pinned" (locked in place). Further scrolling no longer moves the page down, but instead advances (or reverses) the playhead of a complex CSS transform timeline applied to an element inside the container. Additionally, state-based classes are toggled during the pinned duration to change colors.
* **Why Use This Skill (Rationale)**: Tying an animation directly to the user's scroll position creates an immersive, tactile narrative experience. The user feels as though they are physically turning a gear or dragging an object. Pinning the container ensures the subject remains in the focal center while the complex animation (which might normally take too long to watch passively) unfolds at the exact speed the user desires.
* **Overall Applicability**: This technique is highly effective for storytelling sections, product feature deep-dives, step-by-step process explanations, and engaging hero sections on modern SaaS or portfolio websites.
* **Value Addition**: It transforms a passive vertical scroll into a multi-dimensional interactive interaction, increasing user dwell time and making abstract concepts (like a multi-step timeline) feel concrete and playful.
* **Browser Compatibility**: GSAP and ScrollTrigger are highly compatible across all modern browsers (Chrome, Firefox, Safari, Edge). The CSS properties being animated (`transform`, `background-color`) are fully GPU-accelerated and natively supported everywhere.

### 2. Visual & Technical Breakdown

* **Step A: Core Visual Elements**
  - **Colors**: Relies on a high-contrast background (`#0d111c` or `#f8f9fa`) with a visually distinct, muted surface color (`rgba(255, 255, 255, 0.06)`) for the pinned section. 
  - **Accent Logic**: A bright accent color (e.g., `#ff9900` orange) is applied via a dynamically injected `.active` class when the element enters the trigger zone.
  - **Typography**: Bold, clean sans-serif (Inter) ensures legibility during motion.
  - **CSS Properties**: `transform` (rotation, translate X/Y) for layout shifting, `transition` for the color toggling (allowing a smooth fade into the active orange state), and `will-change: transform` to optimize rendering.

* **Step B: Layout & Compositional Style**
  - **Layout System**: Flexbox is used to perfectly center the animated target (the box) within the pinned `.stack` section.
  - **Spatial Feel**: Enormous vertical whitespace (spacer `<div>`s set to `120%` of the container height) exists above and below the pinned section to give the user plenty of physical "scroll track" to play with.
  - **Layering**: GSAP automatically handles z-indexing and wrapping the pinned element in a "pin-spacer" div to prevent layout collapse.

* **Step C: Interactive Behavior & Animations**
  - **Scrubbing**: The `scrub: 1` parameter applies a 1-second smoothing delay to the animation, meaning if the user scrolls very fast, the box catches up smoothly with a buttery easing, rather than jumping instantly.
  - **Motion Arc**: The timeline moves the box in a continuous square pattern (`x`, then `y`, then `-x`, then `-y`) while simultaneously rotating it 90 degrees at each step.
  - **State Toggle**: `toggleClass` handles the color change independently of the timeline progress, applying the class immediately on entry and removing it precisely on exit.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **Scroll Tracking & Pinning** | GSAP ScrollTrigger | The industry standard for complex scroll logic. It natively calculates viewport intersections, handles the complex DOM wrapping required for pinning, and normalizes scroll behavior across devices. |
| **Sequential Animation** | GSAP Timeline (`gsap.timeline`) | Allows chaining multiple animations (moving right, then down, then left) easily, which then maps perfectly to the scroll progress (0% to 100%). |
| **Active Color State** | ScrollTrigger `toggleClass` | Cleaner than animating colors in the timeline; it acts as a boolean state (in trigger zone vs. out of trigger zone) using native CSS transitions for the fade. |

> **Feasibility Assessment**: 100% reproduction. The code below encapsulates all the core concepts from the tutorial (pinning, scrubbing, timelines, and toggle classes) into a single, clean, self-contained interactive component.

#### 3b. Complete Reproduction Code

```python
def create_component(
    output_dir: str,
    title_text: str = "GSAP ScrollTrigger Magic",
    body_text: str = "Keep scrolling down to pin the container and scrub the timeline.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#ff9900",     # CSS hex color for active state
    width_px: int = 1000,
    height_px: int = 700,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the GSAP Scroll-Scrubbed Pinned Animation.
    
    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme and accent_color ===
    if color_scheme == "dark":
        bg_color = "#121212"
        text_color = "#ffffff"
        surface_color = "#1e1e1e"
        box_color = "#f0f0f0"
        box_text = "#121212"
    else:
        bg_color = "#f5f5f7"
        text_color = "#1d1d1f"
        surface_color = "#ffffff"
        box_color = "#1d1d1f"
        box_text = "#ffffff"

    # === CSS ===
    css = f"""/* GSAP Scroll-Scrubbed Pinned Animation */
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
    --box-bg: {box_color};
    --box-text: {box_text};
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
    /* We handle scrolling inside .container to keep the component isolated */
    overflow: hidden; 
}}

/* The main scrollable viewport for our component */
.container {{
    width: var(--width);
    height: var(--height);
    overflow-y: auto;
    overflow-x: hidden;
    position: relative;
    border-radius: 16px;
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
    background: var(--bg);
    border: 1px solid rgba(128, 128, 128, 0.1);
}}

/* Spacer sections to give us room to scroll */
.space {{
    min-height: 120%; /* 1.2x container height to force scrolling */
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    padding: 2rem;
}}

.title {{
    font-size: 2.5rem;
    font-weight: 700;
    letter-spacing: -0.02em;
    margin-bottom: 1rem;
}}

.body-text {{
    font-size: 1.125rem;
    opacity: 0.7;
    max-width: 500px;
    line-height: 1.6;
}}

.scroll-indicator {{
    margin-top: 3rem;
    font-size: 2rem;
    color: var(--accent);
    animation: bounce 2s infinite ease-in-out;
}}

@keyframes bounce {{
    0%, 20%, 50%, 80%, 100% {{ transform: translateY(0); }}
    40% {{ transform: translateY(-20px); }}
    60% {{ transform: translateY(-10px); }}
}}

/* The section that will be pinned */
.stack {{
    height: 100%; /* Matches container height so it fits perfectly when pinned */
    display: flex;
    align-items: center;
    justify-content: center;
    background: var(--surface);
    position: relative;
    border-top: 1px solid rgba(128, 128, 128, 0.1);
    border-bottom: 1px solid rgba(128, 128, 128, 0.1);
}}

/* The animated element */
.box {{
    width: 120px;
    height: 120px;
    background: var(--box-bg);
    color: var(--box-text);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 3rem;
    font-weight: 800;
    border-radius: 20px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.15);
    
    /* Native CSS transition for the toggleClass color shift */
    transition: background-color 0.4s ease, color 0.4s ease, box-shadow 0.4s ease;
    will-change: transform;
    z-index: 10;
}}

/* The state triggered by GSAP ScrollTrigger toggleClass */
.box.active {{
    background-color: var(--accent);
    color: #ffffff;
    box-shadow: 0 0 40px var(--accent);
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
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    
    <!-- Isolated Scrolling Context -->
    <div class="container">
        
        <!-- Entry space -->
        <section class="space">
            <h1 class="title">{title_text}</h1>
            <p class="body-text">{body_text}</p>
            <div class="scroll-indicator">↓</div>
        </section>
        
        <!-- The Pinned Section -->
        <section class="stack">
            <div class="box" aria-hidden="true">A</div>
        </section>
        
        <!-- Exit space -->
        <section class="space">
            <h2 class="title">Animation Complete</h2>
            <p class="body-text">Scroll back up to automatically reverse the timeline smoothly.</p>
        </section>
        
    </div>

    <!-- GSAP Core & ScrollTrigger Plugin CDN -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/gsap.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/ScrollTrigger.min.js"></script>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Register the plugin before using it
gsap.registerPlugin(ScrollTrigger);

document.addEventListener('DOMContentLoaded', () => {{
    
    // We target our specific container as the scroller instead of the window
    const scrollerSelector = ".container";
    
    // Create a GSAP Timeline hooked to the scroll position
    const mainTimeline = gsap.timeline({{
        scrollTrigger: {{
            trigger: ".stack",             // The element that dictates the start/end points
            scroller: scrollerSelector,    // The element with overflow-y: auto
            pin: true,                     // Locks the trigger element in place
            start: "center center",        // Starts when trigger center hits viewport center
            end: "+=200%",                 // Keeps it pinned for a scroll distance = 2x container height
            scrub: 1,                      // Smooth scrubbing (takes 1 sec to catch up to scroll bar)
            toggleClass: {{                // Dynamically applies class when between start and end
                targets: ".box", 
                className: "active"
            }},
            markers: false                 // Set to true for debugging lines
        }}
    }});

    // Build the sequential animation
    // Each step gets an equal fraction of the scroll distance automatically
    const moveDist = 150; 
    
    mainTimeline
        .to(".box", {{ rotation: 90, x: moveDist, duration: 1 }})       // Move Right & Turn
        .to(".box", {{ rotation: 180, y: moveDist, duration: 1 }})      // Move Down & Turn
        .to(".box", {{ rotation: 270, x: -moveDist, duration: 1 }})     // Move Left & Turn
        .to(".box", {{ rotation: 360, x: 0, y: 0, duration: 1 }});      // Move Up (Back to origin) & Turn

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
  - The animating `.box` element uses `aria-hidden="true"` as it contains a decorative letter ("A") that does not provide structural context to a screen reader. 
  - All textual elements utilize high-contrast hex variables depending on the `color_scheme` selection.
  - To respect user preferences for reduced motion, you could wrap the JS initialization in a media query check (`window.matchMedia('(prefers-reduced-motion: no-preference)').matches`), allowing the page to scroll normally without pinning/animations for sensitive users.
* **Performance**: 
  - The animation exclusively alters `transform` properties (`rotation`, `x`, `y`), keeping all recalculations on the GPU and avoiding expensive layout repaints. 
  - `will-change: transform` is applied to the `.box` to notify the browser to optimize for this specific alteration ahead of time.
  - The `scrub: 1` parameter uses `requestAnimationFrame` inherently within GSAP, smoothing out varying scroll wheel hardware event rates (e.g., detent vs. smooth trackpad scrolling).