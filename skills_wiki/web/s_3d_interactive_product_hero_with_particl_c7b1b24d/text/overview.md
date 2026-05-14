# 3D Interactive Product Hero with Particle Environment

## Analysis

# Skill Strategy Document

### 1. High-level Design Pattern Extraction

> **Skill Name**: 3D Interactive Product Hero with Particle Environment

* **Core Visual Mechanism**: The core visual is an interactive WebGL scene embedded directly beneath a standard UI layer. It features a central 3D focal object resting above a mathematically animated, color-cycling geometric base (a torus ring). The background is a spatial void filled with a floating particle system, giving a sense of depth and environment. 
* **Why Use This Skill (Rationale)**: This technique bridges standard web typography with immersive 3D experiences. It immediately captures user attention by offering interaction (drag to rotate) rather than passive viewing. The color-cycling ring directs the eye to the focal object, while the particle background prevents the dark space from feeling flat.
* **Overall Applicability**: Ideal for high-end product landing pages (cars, electronics, luxury goods), Web3/crypto platforms, digital portfolio hero sections, or interactive educational academies where a futuristic or technical aesthetic is desired.
* **Value Addition**: Transforms a static image or standard video background into a tangible, interactive object. It significantly increases time-on-page as users naturally want to "play" with the object, creating a memorable, premium brand impression.
* **Browser Compatibility**: Requires WebGL support (standard in all modern browsers). Minimal performance impact on modern devices due to hardware acceleration, though highly complex 3D models (unlike the simplified fallback provided here) require careful optimization.

### 2. Visual & Technical Breakdown

* **Step A: Core Visual Elements**
  - **Layers**: Two distinct layers — a `<canvas>` element managed by Three.js (z-index 1) and an HTML UI overlay (`pointer-events: none` on the container, re-enabled on buttons) (z-index 2).
  - **Color Logic**: A deep space gradient background (`linear-gradient(to bottom, #000000, #081028, #000000)`), stark white futuristic typography, and a dynamically shifting RGB base ring.
  - **Typography**: Uses `Orbitron` (a geometric sans-serif) to establish a sci-fi/technical tone.
  - **3D Elements**: An ambient light, a directional light for highlights, a stylized 3D object (a procedural placeholder is used in the code to ensure immediate execution without external assets), a geometric `Torus`, and a `BufferGeometry` point cloud for stars.

* **Step B: Layout & Compositional Style**
  - **Layout**: Absolute positioning overlays the UI directly on top of the full-bleed canvas.
  - **Flexbox**: The UI layer uses Flexbox (`flex-direction: column`, `justify-content: space-between`) to anchor the title to the top and the CTA button to the bottom, leaving the center unobstructed for the 3D interaction.
  - **Proportions**: The 3D camera is positioned at `(0, 2.5, 8)` to provide a slight downward isometric perspective, grounding the floating object.

* **Step C: Interactive Behavior & Animations**
  - **Auto-rotation**: The camera (or scene) automatically rotates on the Y-axis to display all angles of the product without requiring user input.
  - **Manual Override**: OrbitControls allow the user to click and drag to orbit the object. Pan and zoom are disabled to maintain layout integrity.
  - **Mathematical Animation**: The pulsing ring scales via a sine wave function `1 + Math.sin(time * 2) * 0.1` and its colors cycle smoothly using offset sine waves for R, G, and B channels.
  - **UI Interaction**: The entry button features a scale transition and glowing box-shadow on hover.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **3D Rendering** | Three.js (via CDN) | Necessary for WebGL abstraction to handle cameras, lights, and geometry without writing raw GLSL/WebGL. |
| **User Interaction** | Three.js OrbitControls | Provides robust, pre-built logic for camera orbiting via mouse/touch drag. |
| **Pulsing Ring / Colors** | JS Animation Loop + Math.sin() | Directly reproduces the mathematical color and scale cycling seen in the original React `useFrame` hook. |
| **Particle Background** | Three.js Points + BufferGeometry | Much more performant to render hundreds of particles in WebGL than manipulating DOM elements. |
| **UI Overlay** | CSS Absolute Positioning | Simplest way to float HTML typography cleanly over a WebGL canvas. |

> **Feasibility Assessment**: 90%. The structural, interactive, and environmental effects (particles, pulsing ring, camera controls, typography, colors) are fully reproduced. The specific 3D car model from the video requires an external `.glb` file, which is prone to link rot. To guarantee the code runs perfectly upon generation, a stylized procedural 3D model (built from primitives) is used as a stand-in, with clear instructions on where to swap in a `GLTFLoader` for a custom model.

#### 3b. Complete Reproduction Code

```python
def create_component(
    output_dir: str,
    title_text: str = "Drive & Thrive Academy",
    body_text: str = "",
    color_scheme: str = "dark",
    accent_color: str = "#00bfff",
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the 3D Interactive Product Hero visual effect.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Theme logic
    if color_scheme == "dark":
        bg_gradient = "linear-gradient(to bottom, #000000, #081028, #000000)"
        text_color = "#ffffff"
        btn_bg = "#ffffff"
        btn_text = "#081028"
        mesh_color = "#f0f0f0"
    else:
        bg_gradient = "linear-gradient(to bottom, #e2e8f0, #ffffff, #e2e8f0)"
        text_color = "#0f172a"
        btn_bg = "#0f172a"
        btn_text = "#ffffff"
        mesh_color = "#334155"

    # CSS Code
    css = f"""/* Base styles */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --accent: {accent_color};
    --text: {text_color};
    --btn-bg: {btn_bg};
    --btn-text: {btn_text};
    --mesh-color: {mesh_color};
}}

body {{
    font-family: 'Orbitron', monospace;
    background-color: #111;
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
}}

.hero-container {{
    width: {width_px}px;
    height: {height_px}px;
    max-width: 100%;
    position: relative;
    background: {bg_gradient};
    overflow: hidden;
    box-shadow: 0 20px 50px rgba(0,0,0,0.5);
}}

/* The 3D Canvas Layer */
#canvas-container {{
    position: absolute;
    inset: 0;
    z-index: 1;
}}

/* The HTML UI Layer */
.ui-layer {{
    position: absolute;
    inset: 0;
    z-index: 2;
    pointer-events: none; /* Allows clicks to pass through to the 3D canvas */
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: space-between;
    padding: 3rem 2rem;
}}

.title-wrapper {{
    text-align: center;
}}

.main-title {{
    color: var(--text);
    font-size: 3rem;
    font-weight: 700;
    letter-spacing: 0.05em;
    text-shadow: 0 4px 15px rgba(0,0,0,0.4);
}}

.subtitle {{
    color: var(--text);
    font-size: 1.2rem;
    margin-top: 0.5rem;
    opacity: 0.8;
    font-family: sans-serif;
}}

.cta-button {{
    pointer-events: auto; /* Re-enable clicks for the button */
    background-color: var(--btn-bg);
    color: var(--btn-text);
    text-decoration: none;
    font-size: 1.25rem;
    font-weight: 600;
    padding: 1rem 3rem;
    border-radius: 50px;
    transition: all 0.3s ease;
    box-shadow: 0 4px 10px rgba(0,0,0,0.2);
}}

.cta-button:hover {{
    transform: scale(1.05);
    background-color: var(--accent);
    color: #fff;
    box-shadow: 0 0 25px var(--accent);
}}
"""

    # HTML Code
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text}</title>
    <!-- External Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;600;700&display=swap" rel="stylesheet">
    
    <link rel="stylesheet" href="style.css">
</head>
<body>

    <div class="hero-container">
        <!-- WebGL Canvas Anchor -->
        <div id="canvas-container"></div>

        <!-- UI Overlay -->
        <div class="ui-layer">
            <div class="title-wrapper">
                <h1 class="main-title">{title_text}</h1>
                <p class="subtitle">{body_text}</p>
            </div>
            
            <a href="#" class="cta-button">Enter Here</a>
        </div>
    </div>

    <!-- Three.js Dependencies via CDN (Global Script tags to avoid local file CORS issues) -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>
    
    <!-- Main Application Logic -->
    <script src="script.js"></script>
</body>
</html>"""

    # JavaScript Code
    js = """// 3D Scene Initialization
const container = document.getElementById('canvas-container');
const styles = getComputedStyle(document.documentElement);
const meshColor = styles.getPropertyValue('--mesh-color').trim() || '#f0f0f0';

// Setup Scene, Camera, Renderer
const scene = new THREE.Scene();
// Scene background is transparent to show CSS gradient
const camera = new THREE.PerspectiveCamera(50, container.clientWidth / container.clientHeight, 0.1, 1000);
camera.position.set(0, 2.5, 8);

const renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true });
renderer.setSize(container.clientWidth, container.clientHeight);
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2)); // optimize for high DPI
container.appendChild(renderer.domElement);

// Lighting
const ambientLight = new THREE.AmbientLight(0xffffff, 0.8);
scene.add(ambientLight);

const dirLight = new THREE.DirectionalLight(0xffffff, 1.0);
dirLight.position.set(10, 10, 5);
scene.add(dirLight);

const pointLight = new THREE.PointLight(0xffffff, 0.8);
pointLight.position.set(-10, -10, -5);
scene.add(pointLight);

// ==========================================
// Central 3D Object
// Using a stylized procedural geometric composition as a robust fallback.
// To use a real 3D model (like the car), replace this block with GLTFLoader logic:
// const loader = new THREE.GLTFLoader();
// loader.load('path/to/model.glb', (gltf) => { scene.add(gltf.scene); });
// ==========================================
const objectGroup = new THREE.Group();

// Stylized "Chassis"
const chassisGeo = new THREE.BoxGeometry(1.8, 0.4, 4);
const materialOptions = { color: meshColor, roughness: 0.2, metalness: 0.8 };
const mainMat = new THREE.MeshStandardMaterial(materialOptions);
const chassis = new THREE.Mesh(chassisGeo, mainMat);
chassis.position.y = 0.5;
objectGroup.add(chassis);

// Stylized "Cabin"
const cabinGeo = new THREE.BoxGeometry(1.4, 0.5, 2);
const glassMat = new THREE.MeshStandardMaterial({ color: 0x111111, roughness: 0.1, metalness: 0.9 });
const cabin = new THREE.Mesh(cabinGeo, glassMat);
cabin.position.set(0, 0.95, -0.2);
objectGroup.add(cabin);

// Abstract "Wheels"
const wheelGeo = new THREE.CylinderGeometry(0.35, 0.35, 0.2, 32);
wheelGeo.rotateZ(Math.PI / 2);
const wheelMat = new THREE.MeshStandardMaterial({ color: 0x222222, roughness: 0.9 });

const wheelPositions = [
    [-1.0, 0.35, 1.2], [1.0, 0.35, 1.2],
    [-1.0, 0.35, -1.2], [1.0, 0.35, -1.2]
];

wheelPositions.forEach(pos => {
    const w = new THREE.Mesh(wheelGeo, wheelMat);
    w.position.set(...pos);
    objectGroup.add(w);
});

scene.add(objectGroup);


// ==========================================
// Pulsing Ring (Torus)
// ==========================================
const ringGeo = new THREE.TorusGeometry(3.5, 0.08, 32, 100);
const ringMat = new THREE.MeshBasicMaterial({ color: 0xffffff, side: THREE.DoubleSide });
const ring = new THREE.Mesh(ringGeo, ringMat);
ring.rotation.x = Math.PI / 2;
scene.add(ring);


// ==========================================
// Particle Background (Stars)
// ==========================================
const particleCount = 200;
const posArray = new Float32Array(particleCount * 3);
const initialY = new Float32Array(particleCount);

for(let i = 0; i < particleCount; i++) {
    posArray[i*3] = (Math.random() - 0.5) * 50;     // x
    posArray[i*3+1] = (Math.random() - 0.5) * 20;   // y
    posArray[i*3+2] = (Math.random() - 0.5) * 30 - 10; // z (push slightly back)
    initialY[i] = posArray[i*3+1];
}

const particlesGeo = new THREE.BufferGeometry();
particlesGeo.setAttribute('position', new THREE.BufferAttribute(posArray, 3));
const particlesMat = new THREE.PointsMaterial({ 
    size: 0.1, 
    color: 0xffffff, 
    transparent: true, 
    opacity: 0.6 
});
const particles = new THREE.Points(particlesGeo, particlesMat);
scene.add(particles);


// ==========================================
// Controls
// ==========================================
const controls = new THREE.OrbitControls(camera, renderer.domElement);
controls.enableZoom = false; // Prevent breaking the layout scale
controls.enablePan = false;
controls.autoRotate = true;
controls.autoRotateSpeed = 1.5;


// ==========================================
// Animation Loop
// ==========================================
const clock = new THREE.Clock();

function animate() {
    requestAnimationFrame(animate);
    const time = clock.getElapsedTime();

    // 1. Math-driven Ring Pulsing (Scale & Color)
    const scale = 1 + Math.sin(time * 2) * 0.05;
    ring.scale.set(scale, scale, scale);

    // RGB Color Cycling logic extracted from video
    const r = (Math.sin(time * 0.5) + 1) / 2;
    const g = (Math.sin(time * 0.5 + 2) + 1) / 2;
    const b = (Math.sin(time * 0.5 + 4) + 1) / 2;
    ring.material.color.setRGB(r, g, b);

    // 2. Particle subtle movement
    const positions = particles.geometry.attributes.position.array;
    for(let i = 0; i < particleCount; i++) {
        // Subtle vertical drift
        positions[i*3+1] = initialY[i] + Math.sin(time + i) * 0.2;
    }
    particles.geometry.attributes.position.needsUpdate = true;
    
    // Slight slow rotation of the whole particle field
    particles.rotation.y = time * 0.02;

    controls.update();
    renderer.render(scene, camera);
}

animate();

// Handle Resize smoothly
window.addEventListener('resize', () => {
    camera.aspect = container.clientWidth / container.clientHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(container.clientWidth, container.clientHeight);
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