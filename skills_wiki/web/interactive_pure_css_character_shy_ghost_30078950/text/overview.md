# Interactive Pure CSS Character (Shy Ghost)

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Interactive Pure CSS Character (Shy Ghost)

* **Core Visual Mechanism**: This pattern relies on **Pure CSS Illustration**—using fundamental CSS shapes (`border-radius`), custom masks (`clip-path: polygon`), and absolute positioning to draw a character without any external SVGs or image assets. This is enhanced with state-driven CSS transitions (the "shy" hiding mechanic) and vanilla JavaScript cursor tracking to breathe life into the component. 
* **Why Use This Skill (Rationale)**: Native CSS characters are incredibly lightweight, scale infinitely without blurring, and their individual body parts can be manipulated independently via the DOM. The interaction mechanic (hiding when hovered, tracking the mouse otherwise) creates micro-delight and engages the user's attention playfully.
* **Overall Applicability**: This technique is perfect for "Easter egg" interactions, interactive 404 error pages, loading state mascots, or onboarding flows where a friendly UI character adds personality to the brand.
* **Value Addition**: Compared to static PNGs or even animated GIFs, a pure CSS character can natively react to user states (`:hover`, `:active`) and precise cursor coordinates. It bridges the gap between static illustration and dynamic UI.
* **Browser Compatibility**: Excellent. Uses standard `clip-path`, `transform`, and `border-radius`. Fully supported in all modern browsers (Chrome 24+, Firefox 3.5+, Safari 9+).

---

### 2. Visual & Technical Breakdown

* **Step A: Core Visual Elements**
  - **Color Logic**:
    - Ghost Body: `#ffffff` (White) to ensure it acts as a central focal point.
    - Mouth/Features: Dark Red (`#800000`) inner mouth, Pink (`#ff6688`) tongue, Black (`#111111`) eyes and eyebrows.
    - Ambient Glow: Tied to the dynamic `accent_color`, utilizing a `radial-gradient` that shifts to red when hovered to simulate "blushing".
  - **Typographic Hierarchy**: Clean, sans-serif font (Inter) to contrast the playful illustration, placing the character firmly in a modern UI context.
  - **CSS Properties at Play**: `border-radius: 50% 50% 45% 55%` is used to create organic, non-rigid body curves. `clip-path` creates sharp teeth triangles.

* **Step B: Layout & Compositional Style**
  - **Layout System**: The character is constructed inside a localized stacking context (`.boo`), utilizing `position: absolute` for all distinct body parts.
  - **Z-Index Layering**: The most critical CSS logic. The arms sit at `z-index: 1` (behind the body) by default. On hover, they jump to `z-index: 4` instantly, then swing across the `z-index: 3` face elements.

* **Step C: Interactive Behavior & Animations**
  - **Continuous Motion**: A CSS `@keyframes` animation translates the wrapper up and down over 4 seconds, paired with a scaling floor shadow.
  - **Hover Mechanics**: Triggers a rapid CSS transition where the arms swing upwards (using precise `transform-origin` pivots), the mouth squashes into a line, and the eyes flatten.
  - **Mouse Tracking**: JavaScript dynamically calculates the cursor's vector relative to the character's center, applying a subtle `translate()` to the face layer and an inverse translation to the tail layer.

---

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| Character Geometry | CSS `border-radius` / `clip-path` | Exact recreation of the tutorial's technique, keeping it lightweight and DOM-manipulatable. |
| The "Shy" Swing | CSS `transform-origin` & `rotate` | Rotating from edge-anchored origins creates a natural arm sweep covering the face without altering top/left. |
| Z-Index Swapping | CSS `transition-delay` | Using `transition: z-index 0s 0.4s` allows arms to finish their swing before popping behind the back. |
| Cursor Tracking | JavaScript DOM `mousemove` | Real-time coordinate math is required to shift the `.face` towards the user's cursor dynamically. |

#### 3b. Complete Reproduction Code

```python
def create_component(
    output_dir: str,
    title_text: str = "404 - Not Found",
    body_text: str = "Oops! You scared our server ghost. Try moving your cursor slowly...",
    color_scheme: str = "dark",
    accent_color: str = "#00bfff",
    width_px: int = 800,
    height_px: int = 600,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Pure CSS Interactive Ghost pattern.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os
    os.makedirs(output_dir, exist_ok=True)

    if color_scheme == "dark":
        bg_color = "#0f172a"
        text_color = "#f8fafc"
    else:
        bg_color = "#f1f5f9"
        text_color = "#0f172a"

    # HTML string generation
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
    <div class="container">
        <div class="header">
            <h1 class="title">{title_text}</h1>
            {f'<p class="body-text">{body_text}</p>' if body_text else ''}
        </div>
        
        <div class="scene">
            <div class="boo-wrapper">
                <div class="boo">
                    <div class="tail"></div>
                    <div class="arm arm-left"></div>
                    <div class="arm arm-right"></div>
                    
                    <div class="body">
                        <div class="blush blush-left"></div>
                        <div class="blush blush-right"></div>
                        
                        <div class="face">
                            <div class="eyebrow eyebrow-left"></div>
                            <div class="eyebrow eyebrow-right"></div>
                            <div class="eye eye-left"></div>
                            <div class="eye eye-right"></div>
                            
                            <div class="mouth">
                                <div class="tooth tooth-1"></div>
                                <div class="tooth tooth-2"></div>
                                <div class="tooth tooth-3"></div>
                                <div class="tooth tooth-4"></div>
                                <div class="tongue"></div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="shadow"></div>
        </div>
    </div>
    
    <script src="script.js"></script>
</body>
</html>"""

    # CSS string generation
    css = f"""/* Interactive Pure CSS Character (Shy Ghost) */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --text: {text_color};
    --accent: {accent_color};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Inter', system-ui, sans-serif;
    background: var(--bg);
    color: var(--text);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
}}

.container {{
    width: var(--width);
    height: var(--height);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 60px;
}}

.header {{
    text-align: center;
    max-width: 600px;
    z-index: 10;
}}

.title {{
    font-size: 2.5rem;
    font-weight: 700;
    letter-spacing: -0.02em;
    margin-bottom: 0.5rem;
}}

.body-text {{
    font-size: 1.1rem;
    opacity: 0.7;
    line-height: 1.5;
}}

.scene {{
    position: relative;
    display: flex;
    flex-direction: column;
    align-items: center;
}}

/* Ghost Core Animation Wrapper */
.boo-wrapper {{
    position: relative;
    width: 250px;
    height: 250px;
    animation: float 4s ease-in-out infinite;
}}

@keyframes float {{
    0%, 100% {{ transform: translateY(0px); }}
    50% {{ transform: translateY(-20px); }}
}}

/* Interactive Ghost Entity */
.boo {{
    position: absolute;
    top: 0; left: 0; width: 100%; height: 100%;
    transition: transform 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    filter: drop-shadow(0 20px 30px rgba(0,0,0,0.15));
    z-index: 10;
}}

/* Ambient Glow */
.boo::before {{
    content: '';
    position: absolute;
    top: 50%; left: 50%;
    width: 450px; height: 450px;
    transform: translate(-50%, -50%);
    background: radial-gradient(circle, var(--accent) 0%, transparent 60%);
    opacity: 0.15;
    z-index: -1;
    pointer-events: none;
    transition: all 0.4s;
}}

/* Hover States (The "Shy" Interaction) */
.container:hover .boo-wrapper {{
    animation-play-state: paused;
}}

.container:hover .boo {{
    transform: scale(0.95);
}}

.container:hover .boo::before {{
    background: radial-gradient(circle, #ff6688 0%, transparent 60%);
    opacity: 0.25;
}}

/* Body Anatomy */
.body {{
    position: absolute;
    top: 0; left: 0; right: 0; bottom: 0;
    background: #ffffff;
    border-radius: 45% 55% 45% 50%;
    box-shadow: inset -15px -15px 30px rgba(0,0,0,0.08);
    z-index: 2; /* Stacking context boundary */
}}

.tail {{
    position: absolute;
    width: 80px; height: 80px;
    background: #ffffff;
    border-radius: 0 50% 50% 50%;
    bottom: 20px; left: -20px;
    transform: rotate(-30deg);
    z-index: 1;
    box-shadow: inset 10px -10px 20px rgba(0,0,0,0.05);
}}

/* Tracking Face Wrapper */
.face {{
    position: absolute;
    top: 0; left: 0; width: 100%; height: 100%;
    z-index: 3;
    transition: transform 0.1s ease-out;
}}

.container:hover .face {{
    transform: translate(0, 0) !important;
}}
.container:hover .tail {{
    transform: translate(0, 0) rotate(-30deg) !important;
}}

/* Facial Features */
.eye {{
    position: absolute;
    width: 24px; height: 36px;
    background: #111;
    border-radius: 50%;
    top: 60px;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}}
.eye-left {{ left: 70px; transform: rotate(15deg); }}
.eye-right {{ right: 70px; transform: rotate(-15deg); }}

.eyebrow {{
    position: absolute;
    width: 36px; height: 16px;
    border-top: 6px solid #111;
    border-radius: 50%;
    top: 45px;
    transition: all 0.3s;
}}
.eyebrow-left {{ left: 60px; transform: rotate(20deg); }}
.eyebrow-right {{ right: 60px; transform: rotate(-20deg); }}

.mouth {{
    position: absolute;
    width: 80px; height: 60px;
    background: #800000;
    bottom: 50px; left: 85px;
    border-radius: 10px 10px 60px 60px;
    overflow: hidden;
    box-shadow: inset 0 10px 20px rgba(0,0,0,0.4);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}}

.tooth {{
    position: absolute;
    width: 20px; height: 25px;
    background: #ffffff;
    -webkit-clip-path: polygon(50% 100%, 0 0, 100% 0);
    clip-path: polygon(50% 100%, 0 0, 100% 0);
    top: 0px;
    transition: opacity 0.2s;
}}
.tooth-1 {{ left: 4px; height: 30px; }}
.tooth-2 {{ left: 28px; }}
.tooth-3 {{ right: 28px; }}
.tooth-4 {{ right: 4px; height: 30px; }}

.tongue {{
    position: absolute;
    width: 50px; height: 40px;
    background: #ff6688;
    bottom: -10px; left: 15px;
    border-radius: 50%;
    box-shadow: inset -5px -5px 10px rgba(0,0,0,0.2);
    transition: opacity 0.2s;
}}

.blush {{
    position: absolute;
    width: 40px; height: 20px;
    background: #ff6688;
    border-radius: 50%;
    top: 90px;
    opacity: 0;
    filter: blur(8px);
    transition: all 0.4s;
    z-index: 3;
}}
.blush-left {{ left: 45px; }}
.blush-right {{ right: 45px; }}

/* Face Squashing on Hover */
.container:hover .eye {{
    height: 6px;
    top: 75px;
    border-radius: 6px;
}}
.container:hover .eye-left {{ transform: rotate(10deg); }}
.container:hover .eye-right {{ transform: rotate(-10deg); }}
.container:hover .eyebrow {{ opacity: 0; transform: translateY(-10px); }}
.container:hover .tooth, .container:hover .tongue {{ opacity: 0; }}
.container:hover .mouth {{
    height: 8px; width: 30px;
    left: 110px; bottom: 80px;
    border-radius: 10px;
    background: #111;
    box-shadow: none;
}}
.container:hover .blush {{ opacity: 0.8; }}

/* The Arms (Z-Index Logic Core) */
.arm {{
    position: absolute;
    width: 80px; height: 50px;
    background: #ffffff;
    top: 120px;
    z-index: 1; /* Rests behind the body */
    box-shadow: inset -5px -5px 10px rgba(0,0,0,0.1);
    /* Waits 0.4s before dropping behind body on hover out */
    transition: transform 0.4s cubic-bezier(0.4, 0, 0.2, 1), z-index 0s 0.4s;
}}
.arm-left {{
    left: -30px;
    border-radius: 50px;
    transform-origin: 90% 50%;
    transform: rotate(-30deg); /* points down-left */
}}
.arm-right {{
    right: -30px;
    border-radius: 50px;
    transform-origin: 10% 50%;
    transform: rotate(30deg); /* points down-right */
}}

.container:hover .arm {{
    z-index: 4; /* Jumps in front immediately */
    transition: transform 0.4s cubic-bezier(0.4, 0, 0.2, 1), z-index 0s 0s;
}}
.container:hover .arm-left {{
    transform: rotate(150deg); /* Swings OUT and UP across the face */
}}
.container:hover .arm-right {{
    transform: rotate(-150deg);
}}

/* Ground Shadow */
.shadow {{
    width: 140px; height: 16px;
    background: var(--text);
    border-radius: 50%;
    margin-top: 40px;
    animation: float-shadow 4s ease-in-out infinite;
}}
@keyframes float-shadow {{
    0%, 100% {{ transform: scale(1); opacity: 0.1; }}
    50% {{ transform: scale(0.8); opacity: 0.05; }}
}}

@media (prefers-reduced-motion: reduce) {{
    .boo-wrapper, .shadow {{ animation: none; }}
    .arm, .mouth, .eye, .face, .tail, .blush, .boo {{ transition: none; }}
}}
"""

    # JS string generation (Escaping '{' with '{{' for python f-strings where JS brackets are needed)
    js = f"""// Real-time cursor tracking logic
document.addEventListener('DOMContentLoaded', () => {{
    const container = document.querySelector('.container');
    const boo = document.querySelector('.boo');
    const face = document.querySelector('.face');
    const tail = document.querySelector('.tail');

    document.addEventListener('mousemove', (e) => {{
        if (!face || !boo) return;
        
        // Disable tracking when shy/hidden
        if (container.matches(':hover')) return;

        const rect = boo.getBoundingClientRect();
        const centerX = rect.left + rect.width / 2;
        const centerY = rect.top + rect.height / 2;

        const deltaX = (e.clientX - centerX) / window.innerWidth;
        const deltaY = (e.clientY - centerY) / window.innerHeight;

        // Multiply by 60 for an expressive but contained tracking distance
        const moveX = deltaX * 60; 
        const moveY = deltaY * 60;

        face.style.transform = `translate(${{moveX}}px, ${{moveY}}px)`;
        // Tail moves inversely to simulate physical inertia
        tail.style.transform = `translate(${{-moveX * 0.5}}px, ${{-moveY * 0.5}}px) rotate(-30deg)`;
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

### 4. Accessibility & Performance Notes

* **Accessibility**: Implements standard `prefers-reduced-motion` media queries which instantly disable the CSS infinite floating animations and the CSS transition durations, yielding a static character experience for sensitive users.
* **Performance**: 
  - The Javascript `mousemove` listener does cause localized style recalculations (`transform`), but is strictly limited to translating two DOM elements (`.face` and `.tail`), skipping layout thrashing.
  - The complex Z-index crossing effect (arms swinging to cover face) is achieved cleanly with `transition-delay: 0.4s` entirely in the CSS GPU layer without resorting to JavaScript `setTimeout` mutations.
  - Elements rely on non-paint-blocking animations (`transform`, `opacity`, `clip-path`) maximizing 60fps performance across the interaction.