# Interactive 3D Hero Canvas (Three.js WebGL)

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Interactive 3D Hero Canvas (Three.js WebGL)

* **Core Visual Mechanism**: The defining visual idea is rendering hardware-accelerated 3D graphics directly within an HTML layout. It breaks the traditional flat 2D plane of the DOM by introducing depth, complex geometry, dynamic lighting, and real-time physical materials (like gloss and metalness) using a `<canvas>` element powered by WebGL. 
* **Why Use This Skill (Rationale)**: As highlighted in the video, raw WebGL requires complex shader logic and matrix math. By leveraging a 3D library (like Three.js), we abstract this complexity to easily create high-impact, memorable landing pages. It captures user attention immediately through ambient motion and cursor-responsive interactions (parallax), creating a premium, modern aesthetic often associated with bleeding-edge tech, gaming, or high-end design agencies.
* **Overall Applicability**: Perfect for hero sections on SaaS landing pages, digital portfolio showcases, "Web3" or crypto sites, product landing pages (rendering the physical product in 3D), or interactive data visualizations.
* **Value Addition**: Transforms a static page into an immersive experience. Instead of a static image or a heavy video file, a WebGL canvas provides a lightweight (code-based), infinitely scalable, and inherently interactive element that responds in real-time to the user's environment and input.
* **Browser Compatibility**: Broadly supported. WebGL 1.0 is supported in 99% of browsers; WebGL 2.0 is supported in >96% of browsers. The Three.js library abstracts compatibility layers. Hardware acceleration requires a functional client GPU.

### 2. Visual & Technical Breakdown

* **Step A: Core Visual Elements**
  - **HTML/CSS Constructs**: A full-bleed or precisely sized container using `position: relative`. The 3D element lives inside a `<canvas>` tag styled with `position: absolute` and `z-index: -1` to act as an interactive background, allowing standard HTML text to overlay it.
  - **Color Logic**: High-contrast. Usually a dark void (`#0d111c`) to make 3D lighting pop. The 3D object uses an accent color (e.g., `#00bfff`) applied to a PBR (Physically Based Rendering) material, illuminated by contrasting directional and ambient lights.
  - **Typographic Hierarchy**: Clean, bold sans-serif fonts (like Inter) placed in the foreground with high contrast (white/light gray) so they remain legible over the moving 3D background.
  - **WebGL Properties (via Three.js)**: `MeshStandardMaterial` (for physical lighting), `DirectionalLight` (for shadows/highlights), `PerspectiveCamera` (for realistic depth foreshortening).

* **Step B: Layout & Compositional Style**
  - **Layout system**: CSS Flexbox or Grid for the overlaid text container. The WebGL canvas breaks out of the standard flow using absolute positioning.
  - **Spatial feel**: Vast and deep. By positioning the camera back on the Z-axis and allowing the object to float in empty space, it creates breathing room.
  - **Z-index layering**: 
    1. Background Base (`body` or `.container` background)
    2. WebGL Canvas (`z-index: 0` or `-1`)
    3. Foreground Text/UI (`z-index: 10`, `position: relative`)

* **Step C: Interactive Behavior & Animations**
  - **Ambient Animation**: The 3D object rotates slowly on its X and Y axes inside the `requestAnimationFrame` render loop, providing continuous visual interest without user input.
  - **Cursor Interaction**: The camera or object subtly shifts position/rotation based on the user's normalized mouse coordinates (X/Y mapped to -1 to +1), creating a faux-parallax effect that ties the 3D space to the user's physical input.
  - **Performance/Scaling**: A `resize` event listener ensures the camera's aspect ratio and the renderer's pixel density update dynamically, keeping the geometry crisp without stretching.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **3D Rendering context** | HTML5 `<canvas>` | Native browser element required for WebGL context, as explained in the video. |
| **Graphics pipeline** | Three.js (CDN) | Raw WebGL requires hundreds of lines of boilerplate and custom GLSL shaders (as the video states, "This looks hard"). Three.js simplifies scene graph, camera, and lighting management. |
| **Layout integration** | CSS Absolute Positioning | Allows standard HTML (title, body text) to sit effortlessly on top of the interactive 3D canvas. |
| **Continuous Motion** | `requestAnimationFrame` (JS) | The standard browser API for syncing visual updates (rendering the 3D scene) with the display's refresh rate (usually 60+ FPS). |

*Feasibility Assessment*: 95%. The code fully reproduces the 3D WebGL paradigm discussed in the video, rendering a high-quality, interactive 3D shape (a Torus Knot, similar to the abstract shapes shown at 0:21) with dynamic lighting. It relies on Three.js as explicitly recommended in the video.

#### 3b. Complete Reproduction Code

```python
def create_component(
    output_dir: str,
    title_text: str = "WebGL Experience",
    body_text: str = "Interactive 3D graphics rendered directly in the browser using the GPU.",
    color_scheme: str = "dark",        
    accent_color: str = "#ff0055",     
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing an interactive 3D WebGL Hero section.
    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme and accent_color ===
    if color_scheme == "dark":
        bg_color = "#0a0a0f"
        text_color = "#ffffff"
        text_muted = "rgba(255, 255, 255, 0.7)"
    else:
        bg_color = "#f0f2f5"
        text_color = "#111111"
        text_muted = "rgba(0, 0, 0, 0.6)"

    # Convert accent hex to a 0x hex string for Three.js
    accent_hex_three = accent_color.replace('#', '0x')

    # === CSS ===
    css = f"""/* WebGL 3D Hero — generated component */
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
    /* Optional: hide scrollbars for embedded components */
    overflow: hidden; 
}}

.hero-container {{
    width: var(--width);
    max-width: 100vw;
    height: var(--height);
    max-height: 100vh;
    position: relative;
    display: flex;
    align-items: center;
    justify-content: flex-start;
    padding: 4rem;
    overflow: hidden;
    border-radius: 12px;
    box-shadow: 0 24px 48px rgba(0, 0, 0, 0.2);
    background: var(--bg);
}}

/* The WebGL Canvas behind the text */
#webgl-canvas {{
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    z-index: 0;
    pointer-events: none; /* Let clicks pass through if needed */
}}

.content {{
    position: relative;
    z-index: 10;
    max-width: 500px;
    pointer-events: auto;
}}

.badge {{
    display: inline-block;
    padding: 0.4rem 1rem;
    background: rgba(128, 128, 128, 0.15);
    border: 1px solid rgba(128, 128, 128, 0.3);
    border-radius: 50px;
    font-size: 0.85rem;
    font-weight: 600;
    letter-spacing: 1px;
    text-transform: uppercase;
    margin-bottom: 1.5rem;
    backdrop-filter: blur(4px);
    color: var(--accent);
}}

.title {{
    font-size: 3.5rem;
    font-weight: 800;
    line-height: 1.1;
    margin-bottom: 1rem;
    letter-spacing: -1px;
}}

.body-text {{
    font-size: 1.2rem;
    line-height: 1.6;
    color: var(--text-muted);
    margin-bottom: 2rem;
}}

.cta-button {{
    display: inline-block;
    padding: 1rem 2rem;
    background: var(--text);
    color: var(--bg);
    text-decoration: none;
    font-weight: 600;
    border-radius: 6px;
    transition: transform 0.2s ease, opacity 0.2s ease;
}}

.cta-button:hover {{
    transform: translateY(-2px);
    opacity: 0.9;
}}

@media (max-width: 768px) {{
    .hero-container {{
        padding: 2rem;
        justify-content: center;
        text-align: center;
    }}
    .title {{ font-size: 2.5rem; }}
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
    
    <!-- Load Three.js core library via CDN -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
</head>
<body>
    <div class="hero-container" id="container">
        <!-- 3D Context -->
        <canvas id="webgl-canvas"></canvas>
        
        <!-- UI Overlay -->
        <div class="content">
            <div class="badge">Powered by GPU</div>
            <h1 class="title">{title_text}</h1>
            <p class="body-text">{body_text}</p>
            <a href="#" class="cta-button">Explore Experience</a>
        </div>
    </div>
    
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Three.js Interactive WebGL Setup
document.addEventListener('DOMContentLoaded', () => {{
    const container = document.getElementById('container');
    const canvas = document.getElementById('webgl-canvas');
    
    // 1. Scene setup
    const scene = new THREE.Scene();
    
    // 2. Camera setup
    // PerspectiveCamera(fov, aspect ratio, near clip, far clip)
    const camera = new THREE.PerspectiveCamera(
        45, 
        container.clientWidth / container.clientHeight, 
        0.1, 
        1000
    );
    // Move camera back to see the object
    camera.position.z = 12;
    // Shift camera slightly to the left so object appears on the right
    camera.position.x = 2;

    // 3. Renderer setup
    const renderer = new THREE.WebGLRenderer({{
        canvas: canvas,
        alpha: true,         // Transparent background to see CSS behind it
        antialias: true      // Smooth edges
    }});
    renderer.setSize(container.clientWidth, container.clientHeight);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2)); // Cap at 2 for performance

    // 4. Create Geometry (Torus Knot)
    const geometry = new THREE.TorusKnotGeometry(2.5, 0.8, 128, 32);
    
    // 5. Create Material (Physically based)
    const material = new THREE.MeshStandardMaterial({{
        color: {accent_hex_three},
        roughness: 0.2,      // Makes it glossy
        metalness: 0.8,      // Makes it look metallic
        wireframe: false
    }});
    
    // 6. Create Mesh and add to scene
    const torusKnot = new THREE.Mesh(geometry, material);
    
    // Position object to the right side of the container (desktop layout)
    if (window.innerWidth > 768) {{
        torusKnot.position.x = 3;
    }}
    
    scene.add(torusKnot);

    // 7. Lighting setup
    // Ambient light (base illumination)
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.5);
    scene.add(ambientLight);
    
    // Directional light (main light source casting "shadows")
    const dirLight = new THREE.DirectionalLight(0xffffff, 1);
    dirLight.position.set(5, 5, 5);
    scene.add(dirLight);

    // Add a subtle colored point light for aesthetic depth
    const pointLight = new THREE.PointLight(0xffffff, 2, 50);
    pointLight.position.set(-5, -5, 2);
    scene.add(pointLight);

    // 8. Interaction: Mouse movement parallax tracking
    let mouseX = 0;
    let mouseY = 0;
    let targetX = 0;
    let targetY = 0;
    
    const windowHalfX = window.innerWidth / 2;
    const windowHalfY = window.innerHeight / 2;

    container.addEventListener('mousemove', (event) => {{
        // Normalize mouse coordinates to range [-1, 1]
        mouseX = (event.clientX - windowHalfX) * 0.001;
        mouseY = (event.clientY - windowHalfY) * 0.001;
    }});

    // 9. Animation Loop
    const clock = new THREE.Clock();

    function animate() {{
        requestAnimationFrame(animate);
        
        const elapsedTime = clock.getElapsedTime();

        // Constant ambient rotation
        torusKnot.rotation.y = 0.2 * elapsedTime;
        torusKnot.rotation.x = 0.1 * elapsedTime;

        // Smoothly interpolate current rotation towards target based on mouse
        targetX = mouseX * 2;
        targetY = mouseY * 2;
        
        // Add mouse offset to the rotation
        torusKnot.rotation.y += 0.05 * (targetX - torusKnot.rotation.y);
        torusKnot.rotation.x += 0.05 * (targetY - torusKnot.rotation.x);
        
        // Slight floating effect on the Y axis
        torusKnot.position.y = Math.sin(elapsedTime * 1.5) * 0.2;

        renderer.render(scene, camera);
    }}
    
    animate();

    // 10. Handle window resizing
    window.addEventListener('resize', () => {{
        // Re-evaluate container size
        const width = container.clientWidth;
        const height = container.clientHeight;
        
        // Update camera aspect ratio
        camera.aspect = width / height;
        camera.updateProjectionMatrix();
        
        // Update renderer dimensions
        renderer.setSize(width, height);
        
        // Update layout based on breakpoint
        if (window.innerWidth <= 768) {{
            torusKnot.position.x = 0;
            camera.position.x = 0;
        }} else {{
            torusKnot.position.x = 3;
            camera.position.x = 2;
        }}
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
  - A `<canvas>` element is treated as a single bitmap image by screen readers. Since the 3D graphic is purely decorative here, it should technically have an `aria-hidden="true"` attribute or `role="presentation"` applied to the canvas so screen readers skip it and focus on the readable `.content` div overlay.
  - Adding `prefers-reduced-motion: reduce` logic in JavaScript would be highly advisable for production. If detected (`window.matchMedia('(prefers-reduced-motion: reduce)').matches`), you should disable the ambient rotation (`torusKnot.rotation.y = 0`) and the mouse parallax interpolation to prevent causing motion sickness or vestibular discomfort.
* **Performance**: 
  - **Pixel Ratio**: The code uses `Math.min(window.devicePixelRatio, 2)` to cap the resolution multiplier at 2. High-DPI screens (like 4K mobile phones) will try to render at 3x or 4x pixel density, which will crush GPU performance without visible benefit.
  - **Geometry Complexity**: The `TorusKnotGeometry` parameters are kept balanced (128 tubular segments, 32 radial segments) to ensure smooth curves without overloading the vertex count.
  - **Memory Leaks**: If this component were embedded in a Single Page Application (React/Vue), it would be critical to call `renderer.dispose()`, `geometry.dispose()`, and `material.dispose()` when the component unmounts to prevent memory leaks in the GPU context. The current code is optimized for static HTML deployment.