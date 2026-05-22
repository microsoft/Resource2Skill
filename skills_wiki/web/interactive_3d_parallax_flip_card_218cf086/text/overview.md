# Interactive 3D Parallax Flip Card

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Interactive 3D Parallax Flip Card

* **Core Visual Mechanism**: This pattern utilizes CSS 3D transforms to create a physical sense of depth. It combines `perspective` on a parent container with `transform-style: preserve-3d` on nested elements. This allows child elements to be pushed off the 2D plane using `translateZ()`, creating a layered parallax effect when the card tilts (via `rotateX` and `rotateY`). Finally, it uses `backface-visibility: hidden` paired with a 180-degree `rotateY` to create a realistic, two-sided object that flips.
* **Why Use This Skill (Rationale)**: Flat interfaces can feel static. By introducing a Z-axis, you leverage the user's spatial awareness. The parallax tilt provides immediate, satisfying tactile feedback based on cursor movement, while the flip mechanism allows you to double the information density of a specific screen area without cluttering the layout.
* **Overall Applicability**: Excellent for premium product feature highlights, interactive team member profiles, pricing tiers, or gamified reveal mechanics (e.g., flashcards, portfolio case studies).
* **Value Addition**: Transforms a standard container into a tangible object. It increases engagement metrics by encouraging users to "play" with the UI, making the digital experience feel more premium and hardware-accelerated.
* **Browser Compatibility**: Broadly supported in all modern browsers. `perspective`, `preserve-3d`, and `backface-visibility` have near 100% support on modern WebKit, Blink, and Gecko engines. (Minimum: Chrome 36, Firefox 16, Safari 9, Edge 12).

### 2. Visual & Technical Breakdown

* **Step A: Core Visual Elements**
  - **Structural Tags**: Requires a specific hierarchy: Scene (holds perspective) > Tilt Wrapper (handles mouse movement) > Flip Wrapper (handles the 180deg flip) > Faces (Front/Back with hidden backfaces) > Content (text/icons pushed out in Z-space).
  - **Color Logic**: Uses a dark or light background with semi-transparent frosted surfaces (`rgba(255, 255, 255, 0.05)`), relying on borders and glowing accents to define edges.
  - **CSS Properties**: 
    - `perspective: 1000px` sets the camera distance.
    - `transform-style: preserve-3d` ensures children render in the 3D space, not flattened.
    - `translateZ(px)` pushes elements closer to the user.
    - `backface-visibility: hidden` prevents the mirrored back of a flipped div from showing.

* **Step B: Layout & Compositional Style**
  - Layout is centered using CSS Grid/Flexbox on the body.
  - The card faces utilize `position: absolute; inset: 0;` to stack perfectly on top of each other within the wrappers.
  - Padding is generous (e.g., 40px) to give the floating inner elements room to breathe as they shift during the parallax effect.

* **Step C: Interactive Behavior & Animations**
  - **Hover/Tilt**: JavaScript listens to `mousemove` over the card, calculating the cursor's distance from the center. This maps to a `-15deg` to `15deg` rotation on the X and Y axes.
  - **Flip**: A `click` event toggles a class that applies `rotateY(180deg)`.
  - **Transitions**: The flip uses a smooth, slightly bouncy cubic-bezier transition (`transition: transform 0.8s cubic-bezier(0.175, 0.885, 0.32, 1.275)`), while the tilt tracking has no transition to ensure zero-latency mouse tracking, only snapping back to `0deg` on `mouseleave` with a quick transition.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **3D Environment** | CSS `perspective` & `preserve-3d` | Native CSS features demonstrated in the tutorial, highly performant. |
| **Card Flip** | CSS Class Toggle + `rotateY` | Cleanest way to manage the state of a two-sided object; CSS handles the interpolation. |
| **Parallax Tilt** | JavaScript Event Listeners | CSS cannot dynamically track mouse coordinates within an element's bounding box to calculate localized rotation angles. JS is required for the math. |
| **Depth / Layering** | CSS `translateZ()` | Native way to move elements toward the camera along the established 3D perspective grid. |

#### 3b. Complete Reproduction Code

```python
def create_component(
    output_dir: str,
    title_text: str = "3D Transform",
    body_text: str = "Hover to experience perspective parallax. Click the card to flip it around and see the backface.",
    color_scheme: str = "dark",        
    accent_color: str = "#10b981",     
    width_px: int = 340,
    height_px: int = 460,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Interactive 3D Parallax Flip Card effect.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Derive theme colors
    if color_scheme == "dark":
        bg_color = "#0b0f19"
        text_color = "#f3f4f6"
        text_muted = "#9ca3af"
        surface_color = "rgba(255, 255, 255, 0.03)"
        border_color = "rgba(255, 255, 255, 0.1)"
    else:
        bg_color = "#f3f4f6"
        text_color = "#111827"
        text_muted = "#4b5563"
        surface_color = "rgba(0, 0, 0, 0.03)"
        border_color = "rgba(0, 0, 0, 0.1)"

    # === CSS ===
    css = f"""/* Interactive 3D Parallax Flip Card */
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
    --border: {border_color};
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
    overflow: hidden;
    perspective: 1200px; /* Establishes the 3D viewport for the body */
}}

/* 1. SCENE: Creates the 3D space */
.scene {{
    width: var(--width);
    height: var(--height);
    perspective: 1000px; 
    cursor: pointer;
}}

/* 2. TILT WRAPPER: Managed by JS for mouse tracking */
.tilt-wrapper {{
    width: 100%;
    height: 100%;
    transform-style: preserve-3d;
    will-change: transform;
}}

/* Add a transition only when mouse leaves to snap back smoothly */
.tilt-wrapper.reset {{
    transition: transform 0.5s cubic-bezier(0.25, 1, 0.5, 1);
}}

/* 3. FLIP WRAPPER: Handles the 180deg CSS animation */
.flip-wrapper {{
    position: relative;
    width: 100%;
    height: 100%;
    transform-style: preserve-3d;
    transition: transform 0.8s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}}

.flip-wrapper.is-flipped {{
    transform: rotateY(180deg);
}}

/* 4. FACES: The actual front and back surfaces */
.card-face {{
    position: absolute;
    inset: 0;
    border-radius: 24px;
    padding: 40px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;
    background: var(--surface);
    border: 1px solid var(--border);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    backface-visibility: hidden; /* Hides the mirrored back side */
    -webkit-backface-visibility: hidden;
    transform-style: preserve-3d; /* Crucial: Allows content to pop out in Z */
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
}}

/* Back face is pre-rotated 180deg */
.card-back {{
    transform: rotateY(180deg);
    background: linear-gradient(135deg, var(--surface), rgba(0,0,0,0.2));
    border-color: var(--accent);
}}

/* 5. PARALLAX CONTENT: Pushed toward the viewer */
.icon-wrapper {{
    width: 64px;
    height: 64px;
    border-radius: 50%;
    background: var(--accent);
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 24px;
    transform: translateZ(80px); /* Extreme pop out */
    box-shadow: 0 10px 30px -10px var(--accent);
}}

.title {{
    font-size: 1.5rem;
    font-weight: 700;
    margin-bottom: 12px;
    transform: translateZ(50px); /* Medium pop out */
}}

.body-text {{
    font-size: 0.95rem;
    color: var(--text-muted);
    line-height: 1.6;
    transform: translateZ(30px); /* Subtle pop out */
}}

.back-text {{
    font-size: 1.25rem;
    font-weight: 600;
    transform: translateZ(60px);
    color: var(--accent);
}}

/* Floating decorative elements */
.decor-circle {{
    position: absolute;
    width: 150px;
    height: 150px;
    border-radius: 50%;
    background: var(--accent);
    filter: blur(80px);
    opacity: 0.15;
    z-index: -1;
    top: -50px;
    right: -50px;
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
    <div class="decor-circle"></div>
    
    <!-- 3D Scene Container -->
    <div class="scene" id="card-scene">
        
        <!-- Tilt Wrapper handles mouse parallax -->
        <div class="tilt-wrapper" id="tilt-wrapper">
            
            <!-- Flip Wrapper handles click rotation -->
            <div class="flip-wrapper" id="flip-wrapper">
                
                <!-- FRONT FACE -->
                <div class="card-face card-front">
                    <div class="icon-wrapper">
                        <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="{bg_color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                            <path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"></path>
                            <polyline points="3.27 6.96 12 12.01 20.73 6.96"></polyline>
                            <line x1="12" y1="22.08" x2="12" y2="12"></line>
                        </svg>
                    </div>
                    <h2 class="title">{title_text}</h2>
                    <p class="body-text">{body_text}</p>
                </div>
                
                <!-- BACK FACE -->
                <div class="card-face card-back">
                    <div class="icon-wrapper" style="background: transparent; border: 2px solid var(--accent);">
                        <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="var(--accent)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                            <polyline points="20 6 9 17 4 12"></polyline>
                        </svg>
                    </div>
                    <p class="back-text">backface-visibility: hidden</p>
                    <p class="body-text" style="margin-top: 10px;">The backside is revealed.</p>
                </div>

            </div>
        </div>
    </div>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Interactive 3D Parallax logic
document.addEventListener('DOMContentLoaded', () => {{
    const scene = document.getElementById('card-scene');
    const tiltWrapper = document.getElementById('tilt-wrapper');
    const flipWrapper = document.getElementById('flip-wrapper');

    // Configurable tilt limit (in degrees)
    const maxTilt = 15; 

    // Handle Parallax Tilt
    scene.addEventListener('mousemove', (e) => {{
        // Remove reset transition for instantaneous tracking
        tiltWrapper.classList.remove('reset');

        // Get bounding box of the scene
        const rect = scene.getBoundingClientRect();
        
        // Calculate mouse position relative to the center of the card
        const centerX = rect.left + rect.width / 2;
        const centerY = rect.top + rect.height / 2;
        
        const mouseX = e.clientX - centerX;
        const mouseY = e.clientY - centerY;

        // Convert position to a percentage (-1 to 1) and multiply by max degrees
        // Note: Moving mouse right (positive X) should rotate Y-axis positively.
        // Moving mouse down (positive Y) should rotate X-axis negatively (tilt back).
        const rotateY = (mouseX / (rect.width / 2)) * maxTilt;
        const rotateX = -(mouseY / (rect.height / 2)) * maxTilt;

        // Apply dynamic rotation to the tilt wrapper
        tiltWrapper.style.transform = `rotateX(${{rotateX}}deg) rotateY(${{rotateY}}deg)`;
    }});

    // Reset rotation smoothly when mouse leaves
    scene.addEventListener('mouseleave', () => {{
        tiltWrapper.classList.add('reset');
        tiltWrapper.style.transform = `rotateX(0deg) rotateY(0deg)`;
    }});

    // Handle Card Flip
    scene.addEventListener('click', () => {{
        flipWrapper.classList.toggle('is-flipped');
    }});
}});
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