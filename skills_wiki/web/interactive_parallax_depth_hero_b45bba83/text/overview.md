# Interactive Parallax Depth Hero

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Interactive Parallax Depth Hero

* **Core Visual Mechanism**: This pattern creates a profound sense of 3D space on a 2D screen by combining two synchronized effects driven by mouse movement. First, the central content uses CSS 3D transforms (`rotateX`, `rotateY`, `translateZ`) to subtly tilt toward the user's cursor. Second, dynamically generated background particles (circles) translate across the X and Y axes at varying speeds based on their assigned "depth," creating a multi-layered parallax illusion. Heavy text shadows enhance the volumetric feel.
* **Why Use This Skill (Rationale)**: Static landing pages can feel flat and unengaging. Binding layout properties directly to user input (mouse position) transforms passive viewing into an active exploration. The differing rates of movement (parallax) mimic human binocular vision, tricking the brain into perceiving real physical depth, which makes the interface feel premium and modern.
* **Overall Applicability**: Ideal for hero sections on tech, SaaS, or creative portfolio websites. It excels in environments where grabbing user attention within the first 3 seconds is critical.
* **Value Addition**: Transforms a standard text-over-background layout into an immersive, interactive diorama. It proves technical polish without requiring heavy WebGL/Three.js payloads.
* **Browser Compatibility**: Relies on CSS `transform-style: preserve-3d`, `perspective`, and basic JS event listeners. Supported in all modern browsers (Chrome, Firefox, Safari, Edge).

### 2. Visual & Technical Breakdown

* **Step A: Core Visual Elements**
  - **Typography**: Bold, sans-serif fonts (like *Inter* or *Montserrat*) ensure the text remains legible even when rotated in 3D space.
  - **Colors**: High contrast is required. The background uses a linear gradient to give environmental lighting, while the floating particles use low-opacity colors (e.g., `rgba(255, 255, 255, 0.15)`) to act as soft, out-of-focus light blockers or dust motes.
  - **Shadows**: A heavy, slightly offset `text-shadow` (e.g., `0 20px 40px rgba(0,0,0,0.4)`) is crucial; it acts as the anchor point that makes the `translateZ` pop-out effect believable.

* **Step B: Layout & Compositional Style**
  - **Container**: Positioned relatively with `overflow: hidden` and a CSS `perspective` of around `1000px`.
  - **Content Wrapper**: Centered using Flexbox or absolute positioning, given `transform-style: preserve-3d` to allow its children to exist in 3D space.
  - **Z-Index Layering**: Background gradient -> Parallax Particles (`z-index: 1`) -> Content Wrapper (`z-index: 10`).

* **Step C: Interactive Behavior & Animations**
  - A JavaScript `mousemove` listener captures cursor coordinates, normalizing them to a `-0.5` to `0.5` range relative to the container.
  - The content wrapper is rotated (max ~15 degrees) inversely to the mouse position to make it "look" at the cursor.
  - Background particles are translated. Particles assigned a higher "depth" multiplier move further and faster, simulating proximity to the camera.
  - CSS `transition: transform 0.1s ease-out` is applied to elements to smooth out the tracking frame rate and prevent jitter.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **Responsive Container** | CSS Flexbox | Centers the 3D content easily while conforming to provided dimensions. |
| **3D Tilt Effect** | CSS `perspective` & `transform` | Native GPU-accelerated 3D transforms (`rotateX`, `rotateY`, `translateZ`) create perfect planar rotation. |
| **Parallax Particles** | JS DOM Injection + `transform` | Generating `div`s via JS allows random sizing, positioning, and individualized depth multipliers for the parallax math. |
| **Interaction Tracking** | JS `mousemove` Event | Captures real-time pointer coordinates to feed the CSS transforms dynamically. |

> **Feasibility Assessment**: 100%. The exact interactive parallax and 3D tilt mechanisms demonstrated in the tutorial are fully reproducible using plain CSS and standard DOM JavaScript without any external libraries.

#### 3b. Complete Reproduction Code

```python
def create_component(
    output_dir: str,
    title_text: str = "Interactive Depth",
    body_text: str = "Move your cursor to explore the parallax dimension.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#ff4757",     # Used for gradient accents
    width_px: int = 1000,
    height_px: int = 600,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Interactive Parallax Depth Hero effect.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors ===
    if color_scheme == "dark":
        bg_start = "#1a1a2e"
        bg_end = "#16213e"
        text_color = "#ffffff"
        particle_bg = "rgba(255, 255, 255, 0.08)"
        shadow_color = "rgba(0, 0, 0, 0.6)"
    else:
        bg_start = "#f8f9fa"
        bg_end = "#e9ecef"
        text_color = "#2d3436"
        particle_bg = "rgba(0, 0, 0, 0.05)"
        shadow_color = "rgba(0, 0, 0, 0.15)"

    # === CSS ===
    css = f"""/* Interactive Parallax Depth Hero */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    background-color: #000;
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 100vh;
    font-family: 'Inter', system-ui, sans-serif;
}}

.interactive-container {{
    width: {width_px}px;
    height: {height_px}px;
    max-width: 100vw;
    position: relative;
    overflow: hidden;
    border-radius: 24px;
    background: linear-gradient(135deg, {bg_start}, {bg_end});
    box-shadow: 0 30px 60px rgba(0,0,0,0.3);
    
    /* Crucial for the 3D effect */
    perspective: 1200px;
    
    display: flex;
    align-items: center;
    justify-content: center;
}}

/* Decorative gradient orb based on accent color */
.interactive-container::before {{
    content: '';
    position: absolute;
    width: 60%;
    height: 60%;
    background: {accent_color};
    border-radius: 50%;
    filter: blur(120px);
    opacity: 0.3;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    z-index: 0;
    pointer-events: none;
}}

#particle-canvas {{
    position: absolute;
    inset: 0;
    z-index: 1;
    pointer-events: none;
}}

.parallax-particle {{
    position: absolute;
    border-radius: 50%;
    background: {particle_bg};
    backdrop-filter: blur(4px);
    -webkit-backdrop-filter: blur(4px);
    /* Soft transition to smooth out mouse movement */
    transition: transform 0.15s cubic-bezier(0.2, 0, 0.2, 1);
    will-change: transform;
}}

.content-wrapper {{
    position: relative;
    z-index: 10;
    text-align: center;
    padding: 40px;
    pointer-events: none; /* Let mouse events pass through to container */
    
    /* Allows children to pop out in Z-space */
    transform-style: preserve-3d;
    transition: transform 0.15s cubic-bezier(0.2, 0, 0.2, 1);
    will-change: transform;
}}

.title {{
    color: {text_color};
    font-size: 4.5rem;
    font-weight: 800;
    letter-spacing: -0.03em;
    line-height: 1.1;
    margin-bottom: 20px;
    
    /* Pop out from the screen */
    transform: translateZ(80px);
    text-shadow: 0 25px 50px {shadow_color};
}}

.subtitle {{
    color: {text_color};
    font-size: 1.5rem;
    font-weight: 400;
    opacity: 0.9;
    
    /* Pop out slightly less than the title */
    transform: translateZ(40px);
    text-shadow: 0 15px 30px {shadow_color};
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
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="interactive-container" id="hero-container">
        <div id="particle-canvas"></div>
        <div class="content-wrapper" id="hero-content">
            <h1 class="title">{title_text}</h1>
            <p class="subtitle">{body_text}</p>
        </div>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""document.addEventListener('DOMContentLoaded', () => {{
    const container = document.getElementById('hero-container');
    const content = document.getElementById('hero-content');
    const canvas = document.getElementById('particle-canvas');
    
    const PARTICLE_COUNT = 35;
    const particles = [];

    // Generate random parallax particles
    for (let i = 0; i < PARTICLE_COUNT; i++) {{
        const p = document.createElement('div');
        p.className = 'parallax-particle';
        
        // Randomize size between 20px and 120px
        const size = Math.random() * 100 + 20;
        p.style.width = `${{size}}px`;
        p.style.height = `${{size}}px`;
        
        // Randomize initial position
        p.style.left = `${{Math.random() * 100}}%`;
        p.style.top = `${{Math.random() * 100}}%`;
        
        // Assign a random depth multiplier (parallax speed)
        // Higher value = moves faster/feels closer
        const depth = Math.random() * 2 + 0.2;
        p.dataset.depth = depth;
        
        canvas.appendChild(p);
        particles.push(p);
    }}

    // Handle mouse movement for 3D tilt and parallax
    container.addEventListener('mousemove', (e) => {{
        const rect = container.getBoundingClientRect();
        
        // Calculate normalized mouse position relative to container (-0.5 to 0.5)
        const x = (e.clientX - rect.left) / rect.width - 0.5;
        const y = (e.clientY - rect.top) / rect.height - 0.5;

        // 1. Tilt the content wrapper
        // Multiplying by negative values reverses the tilt direction for a natural feel
        const tiltMaxDegrees = 20;
        const rotateX = y * -tiltMaxDegrees; 
        const rotateY = x * tiltMaxDegrees;
        content.style.transform = `rotateX(${{rotateX}}deg) rotateY(${{rotateY}}deg)`;

        // 2. Translate the background particles
        // Particles move in opposition to the mouse to create parallax depth
        particles.forEach(p => {{
            const depth = parseFloat(p.dataset.depth);
            const moveMaxPx = 80;
            const moveX = x * -moveMaxPx * depth;
            const moveY = y * -moveMaxPx * depth;
            p.style.transform = `translate(${{moveX}}px, ${{moveY}}px)`;
        }});
    }});

    // Reset transforms when mouse leaves the container
    container.addEventListener('mouseleave', () => {{
        content.style.transform = `rotateX(0deg) rotateY(0deg)`;
        particles.forEach(p => {{
            p.style.transform = `translate(0px, 0px)`;
        }});
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
  - The heavy text shadows ensure high contrast against the shifting background.
  - **Motion Sensitivity**: Users with vestibular disorders may experience dizziness from continuous 3D rotation and parallax movement. For production environments, it is highly recommended to wrap the JavaScript logic in a `window.matchMedia('(prefers-reduced-motion: reduce)').matches` check to disable the `mousemove` listener if the user has requested reduced motion.
* **Performance**:
  - The code uses CSS `will-change: transform` and applies movement strictly via `transform` (translations and rotations) rather than `top`/`left` properties. This ensures all animations are offloaded to the GPU and do not trigger browser layout reflows.
  - A CSS `transition` is used on the transformed elements to act as a native interpolation/smoothing mechanism, preventing the need for a complex JavaScript `requestAnimationFrame` loop just to smooth out raw mouse coordinate updates.