# Scroll-Driven Isometric Exploded View

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Scroll-Driven Isometric Exploded View

* **Core Visual Mechanism**: A layered, isometric 2D image (constructed via SVG) that creates an illusion of 3D depth. As the user scrolls, the outer layers of the "building" or "object" are translated along specific X and Y axes while fading out. This "disassembles" the object, revealing a detailed interior layer. The viewport is pinned during this scroll process to keep the object centered.
* **Why Use This Skill (Rationale)**: This technique bridges the gap between static imagery and heavy 3D WebGL rendering. By slicing a 2D isometric illustration into SVG layers and animating them, you achieve a highly engaging, interactive narrative experience (like unboxing or exploring internal architecture) with a fraction of the performance cost of a real 3D engine. 
* **Overall Applicability**: Perfect for high-end landing page hero sections, hardware product showcases (showing the chips inside a phone or computer), software architecture diagrams, or storytelling websites where "looking beneath the surface" is a core theme.
* **Value Addition**: Transforms passive scrolling into active exploration. It creates a "wow" factor by manipulating perspective and rewards the user's scroll input with a physics-defying structural breakdown.
* **Browser Compatibility**: Excellent. Relies on standard SVG DOM manipulation and GSAP (GreenSock Animation Platform). Works on all modern browsers (Chrome, Firefox, Safari, Edge). Minimum requirements correspond to basic ES6 JavaScript and CSS Grid/Flexbox support.

### 2. Visual & Technical Breakdown

* **Step A: Core Visual Elements**
  - **SVG Composition**: The heart of this is a single `<svg>` element containing multiple grouped layers (`<g id="...">`). Elements lower in the DOM order render on top (Z-index logic for SVG).
  - **Layer Hierarchy (Back to Front)**:
    1. Background/Back walls
    2. Interior details (the "revealed" content)
    3. Outer walls (Left/Right)
    4. Roof/Top cover
    5. A solid "Full Object" overlay used for the initial zoomed-out state.
  - **Color Logic**: Uses monochromatic or dual-tone isometric shading. Top faces are lightest, left faces mid-tone, right faces darkest. (e.g., Top: `#1e293b`, Left: `#0f172a`, Right: `#020617`, Interior Accent: `#00bfff`).
  - **CSS Attributes**: `overflow: hidden` on the container, `preserveAspectRatio="xMidYMid slice"` on the SVG to ensure it acts like `object-fit: cover`.

* **Step B: Layout & Compositional Style**
  - The container is set to `width: 100vw` and `height: 100vh`.
  - GSAP's `ScrollTrigger` uses `pin: true` to lock this container in the viewport while the scrollbar keeps moving, mapping the scroll distance to the animation timeline.
  - Elements are centered dynamically by the SVG's `viewBox` and `preserveAspectRatio`.

* **Step C: Interactive Behavior & Animations**
  - **Scroll Scrubbing**: The animation doesn't play automatically; its playback head is locked to the user's scroll position (`scrub: true` or `scrub: 1` for slight smoothing).
  - **Timeline Synchronization**: GSAP's `timeline.add('label')` is used to group animations. For example, the left wall moving left and the right wall moving right happen simultaneously.
  - **Vector Movement**: To maintain the isometric illusion during the "explosion", elements aren't just moved up or down. They move along the isometric grid lines (e.g., `x: -200, y: -100` moves an element up and to the left).

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **Layered Image Structure** | Inline SVG | Allows individual addressing of paths via DOM IDs (`#roof`, `#wall`). *Note: The tutorial used JS `fetch()` to load the SVG, but for a self-contained, CORS-safe local file execution, inlining the SVG is mathematically identical and much more robust.* |
| **Scroll-Triggered Pinning** | GSAP ScrollTrigger | Industry standard for complex, scrubbable scroll animations. Handles viewport pinning seamlessly without CSS `position: sticky` jumping. |
| **Animation Choreography** | GSAP Timeline | Allows precise grouping of animations (e.g., outer overlay fading exactly as the zoom happens) using timeline labels. |
| **Isometric Movement** | GSAP `x` and `y` transforms | Animating `transform: translate()` on SVG nodes provides hardware-accelerated movement. |

> **Feasibility Assessment**: 100% reproduction of the *technical* and *visual interaction* pattern. Note that the tutorial uses a highly complex custom illustration of a Hong Kong building. To ensure the code runs independently, the Python script mathematically generates a sleek, isometric "Sci-Fi Server/Building" SVG that behaves exactly the same way (roof lifts off, walls slide outward to reveal a glowing interior core).

#### 3b. Complete Reproduction Code

```python
def create_component(
    output_dir: str,
    title_text: str = "ISOMETRIC EXPLORATION",
    body_text: str = "Scroll down to disassemble the structure and reveal the core.",
    color_scheme: str = "dark",
    accent_color: str = "#00eafe",
    width_px: int = 1920,
    height_px: int = 1080,
    **kwargs,
) -> dict:
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Base theme definitions
    if color_scheme == "dark":
        bg_color = "#020617"
        text_color = "#ffffff"
        roof_color = "#1e293b"
        wall_l_color = "#0f172a"
        wall_r_color = "#0b1120"
        interior_base = "#334155"
    else:
        bg_color = "#f8fafc"
        text_color = "#0f172a"
        roof_color = "#cbd5e1"
        wall_l_color = "#94a3b8"
        wall_r_color = "#64748b"
        interior_base = "#e2e8f0"

    # CSS Code
    css = f"""/* Isometric Exploded View generated component */
* {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg-color: {bg_color};
    --text-color: {text_color};
    --accent-color: {accent_color};
}}

body {{
    font-family: 'Inter', system-ui, sans-serif;
    background-color: var(--bg-color);
    color: var(--text-color);
    overflow-x: hidden;
}}

/* Typography */
.overlay-content {{
    position: absolute;
    top: 50px;
    left: 0;
    width: 100%;
    text-align: center;
    z-index: 100;
    pointer-events: none;
}}

h1 {{
    font-size: 3rem;
    letter-spacing: 0.2em;
    font-weight: 700;
    text-transform: uppercase;
    text-shadow: 0 4px 20px rgba(0,0,0,0.5);
}}

p {{
    font-size: 1.2rem;
    margin-top: 10px;
    opacity: 0.8;
}}

/* Animation Container */
.scene-container {{
    width: 100vw;
    height: 100vh;
    position: relative;
    overflow: hidden;
    background: radial-gradient(circle at center, rgba(255,255,255,0.05) 0%, transparent 70%);
}}

.svg-container {{
    width: 100%;
    height: 100%;
    position: absolute;
    top: 0;
    left: 0;
    display: flex;
    justify-content: center;
    align-items: center;
}}

svg {{
    width: 100%;
    height: 100%;
    object-fit: cover;
}}

/* Dummy space to allow scrolling */
.scroll-space {{
    height: 150vh;
    display: flex;
    align-items: center;
    justify-content: center;
    background-color: {bg_color};
    border-top: 1px solid rgba(255,255,255,0.1);
}}

.scroll-space h2 {{
    opacity: 0.3;
    font-weight: 300;
}}
"""

    # HTML with Embedded generated SVG
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text}</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
    
    <!-- GSAP Core & ScrollTrigger -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/gsap.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/ScrollTrigger.min.js"></script>
</head>
<body>

    <div class="scene-container" id="pinned-scene">
        <div class="overlay-content">
            <h1>{title_text}</h1>
            <p>{body_text}</p>
        </div>
        
        <div class="svg-container">
            <!-- 
                Using preserveAspectRatio="xMidYMid slice" to mimic object-fit: cover 
                The viewBox is 1000x1000, centered around (500,500)
            -->
            <svg id="iso-svg" viewBox="0 0 1000 1000" preserveAspectRatio="xMidYMid slice">
                
                <!-- LAYER 1: Background shadows/pedestal -->
                <g id="pedestal">
                    <polygon points="500,800 200,650 500,500 800,650" fill="rgba(0,0,0,0.4)" />
                </g>

                <!-- LAYER 2: INTERIOR (The Reveal) -->
                <g id="interior">
                    <!-- Base grid/floor -->
                    <polygon points="500,700 300,600 500,500 700,600" fill="{interior_base}" stroke="rgba(255,255,255,0.1)" />
                    <!-- Inner glowing core -->
                    <polygon points="500,450 450,475 500,500 550,475" fill="#ffffff" />
                    <polygon points="450,475 500,500 500,600 450,575" fill="{accent_color}" />
                    <polygon points="500,500 550,475 550,575 500,600" fill="{accent_color}" style="filter: brightness(0.7);" />
                    <!-- Floating Data Rings (Decorative) -->
                    <path d="M 500,420 L 400,470 L 500,520 L 600,470 Z" fill="none" stroke="{accent_color}" stroke-width="2" opacity="0.5" />
                    <path d="M 500,400 L 350,475 L 500,550 L 650,475 Z" fill="none" stroke="{accent_color}" stroke-width="1" opacity="0.3" stroke-dasharray="10, 5" />
                </g>

                <!-- LAYER 3: OUTER SHELL (These will explode outward) -->
                <!-- Right Wall -->
                <g id="wall_right">
                    <polygon points="500,500 800,350 800,650 500,800" fill="{wall_r_color}" stroke="#000" stroke-width="2" />
                    <!-- Window/Detail -->
                    <polygon points="550,550 750,450 750,500 550,600" fill="{accent_color}" opacity="0.1" />
                    <line x1="650" y1="500" x2="650" y2="650" stroke="{accent_color}" stroke-width="2" opacity="0.3"/>
                </g>

                <!-- Left Wall -->
                <g id="wall_left">
                    <polygon points="200,350 500,500 500,800 200,650" fill="{wall_l_color}" stroke="#000" stroke-width="2" />
                    <!-- Window/Detail -->
                    <polygon points="250,450 450,550 450,600 250,500" fill="{accent_color}" opacity="0.1" />
                    <line x1="350" y1="500" x2="350" y2="650" stroke="{accent_color}" stroke-width="2" opacity="0.3"/>
                </g>

                <!-- Top Roof -->
                <g id="building_top">
                    <polygon points="500,200 800,350 500,500 200,350" fill="{roof_color}" stroke="#000" stroke-width="2" />
                    <!-- Roof details -->
                    <polygon points="500,250 700,350 500,450 300,350" fill="none" stroke="rgba(255,255,255,0.1)" stroke-width="4" />
                    <circle cx="500" cy="350" r="20" fill="{accent_color}" opacity="0.5" />
                </g>

                <!-- LAYER 4: FULL COVER (Used for the initial zoomed-out state) -->
                <!-- In a real scenario, this is an un-cut rendering. Here we use an overlaying group -->
                <g id="full_city">
                    <!-- Replicate outer shell identically -->
                    <polygon points="500,200 800,350 500,500 200,350" fill="{roof_color}" />
                    <polygon points="200,350 500,500 500,800 200,650" fill="{wall_l_color}" />
                    <polygon points="500,500 800,350 800,650 500,800" fill="{wall_r_color}" />
                    <!-- Edges -->
                    <path d="M 200,350 L 500,200 L 800,350 L 500,500 Z" fill="none" stroke="#fff" opacity="0.1" stroke-width="2"/>
                    <path d="M 200,350 L 500,500 L 500,800" fill="none" stroke="#fff" opacity="0.1" stroke-width="2"/>
                    <path d="M 500,800 L 500,500 L 800,350" fill="none" stroke="#fff" opacity="0.1" stroke-width="2"/>
                </g>

            </svg>
        </div>
    </div>

    <div class="scroll-space">
        <h2>Data Core Reached. Continue scrolling...</h2>
    </div>

    <script src="script.js"></script>
</body>
</html>"""

    # JS Code using GSAP
    js = """// Isometric Exploded View GSAP Animation
document.addEventListener("DOMContentLoaded", () => {
    // 1. Register ScrollTrigger Plugin
    gsap.registerPlugin(ScrollTrigger);

    // 2. Setup the Timeline
    // This timeline maps to the scroll progress over the pinned container
    const tl = gsap.timeline({
        scrollTrigger: {
            trigger: "#pinned-scene", // The container to pin
            start: "top top",         // Start when container hits top of viewport
            end: "+=1500",            // Scroll distance for the animation (1500px)
            scrub: 1,                 // Smooth scrubbing (1 sec lag)
            pin: true                 // Pin the container in place
        }
    });

    // 3. Define the Animation Choreography

    // Phase 1: Zoom in on the whole SVG & fade out the solid "full_city" cover
    // The 'start' label ensures these two animations happen simultaneously
    tl.add('start')
      .to("#iso-svg", { scale: 1.5, transformOrigin: "50% 50%", duration: 2 }, 'start')
      .to("#full_city", { opacity: 0, duration: 2 }, 'start');

    // Phase 2: Disassemble the building
    // Using isometric math logic: 
    // Moving along the Y axis is pure vertical.
    // Moving along an isometric 30-degree line involves ratio shifts in X and Y.
    
    tl.add('explode')
      // Move Roof straight UP
      .to("#building_top", { y: -200, opacity: 0, duration: 3 }, 'explode')
      
      // Move Left Wall DOWN and LEFT
      .to("#wall_left", { x: -200, y: 100, opacity: 0, duration: 3 }, 'explode')
      
      // Move Right Wall DOWN and RIGHT
      .to("#wall_right", { x: 200, y: 100, opacity: 0, duration: 3 }, 'explode');

    // By the end of 'explode', the #interior group is fully visible!
    
    // Optional: Add a slight rotation or pulse to the interior after opening
    tl.to("#interior", { scale: 1.05, transformOrigin: "50% 50%", duration: 1 });
});
"""

    # Write files
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
  - Scroll-jacking (pinning elements while the user scrolls) can be disorienting for some users. To make this production-ready, consider wrapping the GSAP timeline creation in a `matchMedia("(prefers-reduced-motion: no-preference)")` block. If reduced motion is requested, simply hide the outer shells immediately and don't pin the container.
  - Ensure the text overlay has a high contrast against the background (handled by the dark/light variables in the component logic).
* **Performance**:
  - Animating SVG elements via `x`, `y`, `scale`, and `opacity` is ideal as GSAP can push these to hardware-accelerated CSS transforms.
  - **Avoid animating SVG attributes like `d` (paths) or `points` on scroll**, as this requires the CPU to recalculate the rasterized vector geometry every frame. Translating whole `<g>` groups, as demonstrated here, avoids this layout thrashing.
  - The `scrub: 1` setting in `ScrollTrigger` adds a 1-second lerp/smoothing to the scroll tracking. This makes the animation feel buttery smooth even if the user is scrolling on a jerky, rigid mouse wheel.