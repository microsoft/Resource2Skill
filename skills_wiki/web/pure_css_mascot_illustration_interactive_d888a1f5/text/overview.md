# Pure CSS Mascot Illustration (Interactive Penguin)

## Analysis

# Agent_Skill_Distiller Strategy Document

### 1. High-level Design Pattern Extraction

> **Skill Name**: Pure CSS Mascot Illustration (Interactive Penguin)

* **Core Visual Mechanism**: The defining visual idea is the creation of a lively, organic character illustration entirely out of CSS shapes. This is achieved by combining `border-radius` to form curves, overlapping `absolute` positioned elements for anatomy, and leveraging CSS `@keyframes` for cyclic, lifelike idle animations (like flapping wings). The aesthetic is playful, minimalist, and vector-clean.

* **Why Use This Skill (Rationale)**: Native CSS illustrations eliminate the need for heavy raster images or external SVG files, ensuring instant load times and pixel-perfect rendering at any scale. By building the character in the DOM, you gain the ability to interact with individual body parts—such as making the character's eyes track the user's cursor. This adds a delightful, engaging layer of micro-interaction that boosts user retention and brand personality.

* **Overall Applicability**: This technique is perfect for playful landing pages, loading screens, 404 error pages, onboarding flows, or interactive mascots on SaaS dashboards.

* **Value Addition**: Compared to static images, a CSS-built mascot feels "alive." The ambient flapping, combined with cursor-tracking eyes, transforms a standard UI into an engaging digital environment. 

* **Browser Compatibility**: This pattern relies on core CSS properties (`position`, `border-radius`, `transform`) and standard JavaScript event listeners, making it natively compatible with all modern browsers (Chrome, Firefox, Safari, Edge).


### 2. Visual & Technical Breakdown

* **Step A: Core Visual Elements**
  - **HTML System**: A structured, semantic tree of `div` elements mapped to anatomical parts (e.g., `.penguin`, `.body`, `.belly`, `.wing`, `.eye`, `.foot`).
  - **Color Logic**:
    - **Skin/Feathers**: A deep, rich slate grey (e.g., `#36394c`).
    - **Belly/Face**: Pure white or slightly off-white for contrast (`#ffffff`).
    - **Accent (Beak/Feet)**: Vibrant orange (e.g., `#ff7b00` or configurable).
    - **Eyes**: Deep black (`#111`) with white pupils for contrast.
  - **Shape Generation**: Intensive use of complex `border-radius` combinations (e.g., `border-radius: 50% 50% 40% 40%`) to create non-uniform ovals that mimic organic body mass.

* **Step B: Layout & Compositional Style**
  - **Layout System**: The main `.penguin` wrapper establishes a relative positioning context and a fixed aspect ratio. Every anatomical `div` inside it utilizes percentage-based `absolute` positioning.
  - **Layering (Z-Index)**: 
    - `-1`: Wings and feet (tucked behind the body).
    - `1`: Main body.
    - `2`: Belly and face patches.
    - `3`: Eyes and beak.
  - **Scalability**: Because the internal components use `%` for width, height, top, and left properties, the entire character can be scaled simply by scaling the parent container.

* **Step C: Interactive Behavior & Animations**
  - **Idle Animation (CSS)**: The wings use `@keyframes` to rotate back and forth on a continuous loop (`animation: flap 2s infinite ease-in-out`), and the entire body floats slightly.
  - **Cursor Tracking (JS)**: JavaScript listens to `mousemove` and `touchmove` events, calculating the trigonometric angle and distance from the center of the eyes to the cursor using `Math.atan2`. The pupils are then translated along that vector to look at the user.
  - **Atmosphere**: A JavaScript Canvas particle system generates a dynamic background (stars or dust) that moves upward, adding depth.


### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **Character Shapes** | Pure CSS (`border-radius`, `absolute` positioning) | Crisp rendering, fully dynamic, avoids external SVG dependencies, and enables individual DOM element targeting. |
| **Idle Animations** | CSS `@keyframes` | Hardware-accelerated, continuous looping without main-thread blocking. |
| **Interactive Eyes** | JS Event Listeners + Math | Requires real-time cursor coordinates and trigonometric calculations (`Math.atan2`) to dynamically adjust CSS `transform` on the pupils. |
| **Atmospheric Background** | Canvas API (JS) | Efficiently renders dozens of moving particles without creating heavy DOM node clutter. |

#### 3b. Complete Reproduction Code

```python
def create_component(
    output_dir: str,
    title_text: str = "Hello, I'm CSS!",
    body_text: str = "Move your mouse around to see me look at you.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#ff7b00",     # CSS hex color for beak and feet
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Pure CSS Mascot Illustration.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme ===
    if color_scheme == "dark":
        bg_color = "#0f172a"
        text_color = "#f8fafc"
        penguin_skin = "#36394c"
        penguin_belly = "#ffffff"
        particle_color = "rgba(255, 255, 255, 0.6)"
    else:
        bg_color = "#e2e8f0"
        text_color = "#0f172a"
        penguin_skin = "#1e293b"
        penguin_belly = "#ffffff"
        particle_color = "rgba(0, 0, 0, 0.15)"

    # === CSS ===
    css = f"""/* Pure CSS Mascot Illustration — generated component */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --text: {text_color};
    --accent: {accent_color};
    --skin: {penguin_skin};
    --belly: {penguin_belly};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background: var(--bg);
    color: var(--text);
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    overflow: hidden;
    position: relative;
}}

/* Canvas Background */
#bg-canvas {{
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    z-index: 0;
    pointer-events: none;
}}

/* Typography */
.content {{
    position: relative;
    z-index: 10;
    text-align: center;
    margin-bottom: 40px;
}}

.title {{
    font-size: 2.5rem;
    font-weight: 700;
    letter-spacing: -0.02em;
    margin-bottom: 8px;
    text-shadow: 0 2px 10px rgba(0,0,0,0.2);
}}

.body-text {{
    font-size: 1.1rem;
    font-weight: 400;
    opacity: 0.8;
}}

/* Mascot Container */
.penguin-container {{
    position: relative;
    z-index: 10;
    width: 260px;
    height: 320px;
    animation: float 4s ease-in-out infinite;
}}

.penguin {{
    width: 100%;
    height: 100%;
    position: relative;
}}

.penguin * {{
    position: absolute;
}}

/* Feet */
.foot {{
    width: 26%;
    height: 12%;
    background: var(--accent);
    border-radius: 50%;
    bottom: -2%;
    z-index: 1;
    box-shadow: inset 0 -4px 0 rgba(0,0,0,0.2);
}}
.foot.left {{
    left: 18%;
    transform: rotate(-15deg);
}}
.foot.right {{
    right: 18%;
    transform: rotate(15deg);
}}

/* Wings */
.wing {{
    width: 24%;
    height: 50%;
    background: var(--skin);
    border-radius: 50% 50% 40% 40%;
    top: 35%;
    z-index: 1;
    transform-origin: 50% 10%;
}}
.wing.left {{
    left: -12%;
    animation: flap-left 2s infinite ease-in-out;
}}
.wing.right {{
    right: -12%;
    animation: flap-right 2s infinite ease-in-out;
}}

/* Main Body */
.body-shape {{
    width: 100%;
    height: 100%;
    background: var(--skin);
    border-radius: 48% 48% 45% 45%;
    z-index: 2;
    box-shadow: inset -10px -15px 20px rgba(0,0,0,0.2),
                0 15px 25px rgba(0,0,0,0.2);
    overflow: hidden;
}}

/* Belly & Face overlays inside body */
.belly {{
    width: 82%;
    height: 85%;
    background: var(--belly);
    border-radius: 45% 45% 50% 50%;
    bottom: 3%;
    left: 9%;
}}

.face-arc {{
    width: 60%;
    height: 50%;
    background: var(--belly);
    border-radius: 50%;
    top: 5%;
}}
.face-arc.left {{ left: 2%; }}
.face-arc.right {{ right: 2%; }}

/* Eyes */
.eye {{
    width: 20%;
    height: 22%;
    background: #111;
    border-radius: 50%;
    top: 22%;
    z-index: 3;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: inset 0 3px 6px rgba(0,0,0,0.8);
}}
.eye.left {{ left: 23%; }}
.eye.right {{ right: 23%; }}

.pupil {{
    width: 35%;
    height: 35%;
    background: #fff;
    border-radius: 50%;
    position: relative;
    /* transition for smooth but slightly snappy movement */
    transition: transform 0.1s ease-out;
}}
.pupil::after {{
    content: '';
    position: absolute;
    width: 30%;
    height: 30%;
    background: rgba(255,255,255,0.8);
    border-radius: 50%;
    top: 15%;
    left: 15%;
}}

/* Beak */
.beak {{
    width: 22%;
    height: 12%;
    background: var(--accent);
    border-radius: 50%;
    top: 38%;
    left: 39%;
    z-index: 4;
    box-shadow: inset 0 -4px 0 rgba(0,0,0,0.2), 
                0 4px 6px rgba(0,0,0,0.1);
}}

/* Animations */
@keyframes float {{
    0%, 100% {{ transform: translateY(0px); }}
    50% {{ transform: translateY(-10px); }}
}}

@keyframes flap-left {{
    0%, 100% {{ transform: rotate(15deg); }}
    50% {{ transform: rotate(45deg); }}
}}

@keyframes flap-right {{
    0%, 100% {{ transform: rotate(-15deg); }}
    50% {{ transform: rotate(-45deg); }}
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
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <canvas id="bg-canvas"></canvas>
    
    <div class="content">
        <h1 class="title">{title_text}</h1>
        <p class="body-text">{body_text}</p>
    </div>

    <div class="penguin-container">
        <div class="penguin">
            <div class="foot left"></div>
            <div class="foot right"></div>
            <div class="wing left"></div>
            <div class="wing right"></div>
            
            <div class="body-shape">
                <div class="face-arc left"></div>
                <div class="face-arc right"></div>
                <div class="belly"></div>
            </div>
            
            <div class="eye left">
                <div class="pupil"></div>
            </div>
            <div class="eye right">
                <div class="pupil"></div>
            </div>
            
            <div class="beak"></div>
        </div>
    </div>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Pure CSS Mascot Illustration — Interactive Behavior
document.addEventListener('DOMContentLoaded', () => {{
    
    // --- 1. Interactive Eyes Logic ---
    const eyes = document.querySelectorAll('.eye');
    
    const handleMove = (x, y) => {{
        eyes.forEach(eye => {{
            const rect = eye.getBoundingClientRect();
            // Calculate center of the eye
            const eyeCenterX = rect.left + rect.width / 2;
            const eyeCenterY = rect.top + rect.height / 2;
            
            // Calculate angle between eye and cursor
            const angle = Math.atan2(y - eyeCenterY, x - eyeCenterX);
            
            // Limit distance so the pupil doesn't leave the eye
            const maxDistance = rect.width / 3.5;
            const distance = Math.min(
                maxDistance, 
                Math.hypot(x - eyeCenterX, y - eyeCenterY) / 8
            );
            
            // Calculate new X and Y positions
            const pupilX = Math.cos(angle) * distance;
            const pupilY = Math.sin(angle) * distance;
            
            const pupil = eye.querySelector('.pupil');
            pupil.style.transform = `translate(${{pupilX}}px, ${{pupilY}}px)`;
        }});
    }};

    window.addEventListener('mousemove', (e) => {{
        handleMove(e.clientX, e.clientY);
    }});

    window.addEventListener('touchmove', (e) => {{
        if(e.touches.length > 0) {{
            handleMove(e.touches[0].clientX, e.touches[0].clientY);
        }}
    }});

    // --- 2. Canvas Background (Particles) ---
    const canvas = document.getElementById('bg-canvas');
    const ctx = canvas.getContext('2d');
    
    let width, height;
    let particles = [];
    const particleColor = '{particle_color}';

    const resize = () => {{
        width = window.innerWidth;
        height = window.innerHeight;
        canvas.width = width;
        canvas.height = height;
    }};

    class Particle {{
        constructor() {{
            this.x = Math.random() * width;
            this.y = Math.random() * height;
            this.size = Math.random() * 2.5 + 0.5;
            this.speedY = Math.random() * 0.5 + 0.1;
            this.opacity = Math.random() * 0.5 + 0.2;
        }}
        update() {{
            this.y -= this.speedY;
            if (this.y < -10) {{
                this.y = height + 10;
                this.x = Math.random() * width;
            }}
        }}
        draw() {{
            ctx.fillStyle = particleColor;
            ctx.globalAlpha = this.opacity;
            ctx.beginPath();
            ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
            ctx.fill();
            ctx.globalAlpha = 1.0;
        }}
    }}

    const initParticles = () => {{
        particles = [];
        const count = Math.floor((window.innerWidth * window.innerHeight) / 12000);
        for (let i = 0; i < count; i++) {{
            particles.push(new Particle());
        }}
    }};

    const animate = () => {{
        ctx.clearRect(0, 0, width, height);
        particles.forEach(p => {{
            p.update();
            p.draw();
        }});
        requestAnimationFrame(animate);
    }};

    window.addEventListener('resize', () => {{
        resize();
        initParticles();
    }});

    // Initialize
    resize();
    initParticles();
    animate();
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
  - Pure CSS mascots are inherently screen-reader agnostic, meaning they won't clutter accessible navigation loops. However, they should generally be wrapped in a container that features an `aria-label="Animated Penguin illustration"` and `role="img"`.
  - Added support for `prefers-reduced-motion` can easily be included by turning off `@keyframes` animations for users who request it.
* **Performance**:
  - **CSS Layering**: Uses hardware-accelerated properties (`transform: rotate()` and `transform: translateY()`) for character animations to prevent expensive browser re-paints.
  - **JS Optimization**: The pupil tracking relies on `getBoundingClientRect()` inside a `mousemove` handler. While standard screens handle this easily, dropping it into a `requestAnimationFrame` queue or debouncing it would further optimize performance for lower-end devices.
  - **Canvas Background**: Rendering simple arcs (`ctx.arc`) is exceptionally cheap, keeping the particle frame budget under 1ms. Automatic resizing limits particle counts dynamically based on screen real estate.