def create_component(
    output_dir: str,
    title_text: str = "THE ARTIFACT",
    body_text: str = "Interactive 3D model with studio lighting, soft shadows, and damped orbit physics.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#00bfff",     # CSS hex color for accent
    width_px: int = 1000,
    height_px: int = 600,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Interactive 3D Artifact Showcase.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors ===
    if color_scheme == "dark":
        bg_color = "#050505"
        text_color = "#ffffff"
        surface_color = "#151515"  # Ground plane color
        ambient_intensity = "0.5"
        spot_intensity = "800"
    else:
        bg_color = "#e5e5e5"
        text_color = "#111111"
        surface_color = "#c0c0c0"
        ambient_intensity = "1.0"
        spot_intensity = "600"

    # === CSS ===
    css = f"""/* Interactive 3D Showcase */
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
    background-color: #000; /* Outer page background */
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
}}

.viewer-container {{
    width: var(--width);
    height: var(--height);
    max-width: 100vw;
    position: relative;
    overflow: hidden;
    background: var(--bg);
    border-radius: 8px;
    box-shadow: 0 24px 48px rgba(0,0,0,0.4);
}}

.ui-layer {{
    position: absolute;
    top: 32px;
    left: 40px;
    z-index: 10;
    pointer-events: none; /* Let clicks pass through to the 3D canvas */
    max-width: 400px;
}}

.title {{
    font-weight: 300;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    font-size: 22px;
    color: var(--text);
    margin-bottom: 8px;
    text-shadow: 0 2px 10px rgba(0,0,0,0.2);
}}

.body-text {{
    font-weight: 400;
    font-size: 13px;
    line-height: 1.5;
    color: var(--text);
    opacity: 0.6;
}}

.canvas-container {{
    width: 100%;
    height: 100%;
    cursor: grab;
}}

.canvas-container:active {{
    cursor: grabbing;
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
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
    
    <!-- ES Module Import Map for Three.js -->
    <script type="importmap">
      {{
        "imports": {{
          "three": "https://unpkg.com/three@0.153.0/build/three.module.js",
          "three/addons/": "https://unpkg.com/three@0.153.0/examples/jsm/"
        }}
      }}
    </script>
</head>
<body>
    <div class="viewer-container">
        <div class="ui-layer">
            <h1 class="title">{title_text}</h1>
            <p class="body-text">{body_text}</p>
        </div>
        <div class="canvas-container"></div>
    </div>
    <script type="module" src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// 3D Scene Setup and Interaction
import * as THREE from 'three';
import {{ OrbitControls }} from 'three/addons/controls/OrbitControls.js';
// import {{ GLTFLoader }} from 'three/addons/loaders/GLTFLoader.js';

document.addEventListener('DOMContentLoaded', () => {{
    const container = document.querySelector('.canvas-container');
    let width = container.clientWidth;
    let height = container.clientHeight;

    // 1. Renderer Setup (Enable Shadows & Anti-aliasing)
    const renderer = new THREE.WebGLRenderer({{ antialias: true, alpha: true }});
    renderer.outputColorSpace = THREE.SRGBColorSpace;
    renderer.setSize(width, height);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2)); // Cap pixel ratio for performance
    renderer.setClearColor(new THREE.Color('{bg_color}'));
    
    // Enable and configure shadow mapping
    renderer.shadowMap.enabled = true;
    renderer.shadowMap.type = THREE.PCFSoftShadowMap;
    container.appendChild(renderer.domElement);

    // 2. Scene & Camera Setup
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(45, width / height, 0.1, 100);
    camera.position.set(4, 5, 11);
    camera.lookAt(0, 0, 0);

    // 3. Ground Plane (Receives Shadows)
    const groundGeometry = new THREE.PlaneGeometry(50, 50, 32, 32);
    groundGeometry.rotateX(-Math.PI / 2);
    const groundMaterial = new THREE.MeshStandardMaterial({{
        color: new THREE.Color('{surface_color}'),
        roughness: 0.9,
        metalness: 0.1,
        side: THREE.DoubleSide
    }});
    const groundMesh = new THREE.Mesh(groundGeometry, groundMaterial);
    groundMesh.receiveShadow = true;
    scene.add(groundMesh);

    // 4. Lighting Setup
    // Soft ambient fill light
    const ambientLight = new THREE.AmbientLight(0xffffff, {ambient_intensity});
    scene.add(ambientLight);

    // Dramatic spot light casting shadows
    const spotLight = new THREE.SpotLight(0xffffff, {spot_intensity}, 50, Math.PI / 6, 0.5, 1);
    spotLight.position.set(0, 15, 0);
    spotLight.castShadow = true;
    
    // Shadow refinement to prevent artifacts
    spotLight.shadow.bias = -0.0001; 
    spotLight.shadow.mapSize.width = 2048;
    spotLight.shadow.mapSize.height = 2048;
    scene.add(spotLight);

    // 5. Artifact Model
    /* 
    // TO LOAD AN EXTERNAL GLTF/GLB MODEL, REPLACE THE PROCEDURAL MESH WITH THIS:
    const loader = new GLTFLoader();
    loader.load('YOUR_MODEL_PATH.glb', (gltf) => {{
        const model = gltf.scene;
        model.traverse((child) => {{
            if (child.isMesh) {{
                child.castShadow = true;
                child.receiveShadow = true;
            }}
        }});
        scene.add(model);
    }});
    */

    // For demonstration (avoiding CORS/local file loading errors), we generate a complex metallic artifact
    const artifactGeometry = new THREE.TorusKnotGeometry(1.5, 0.45, 256, 32);
    const artifactMaterial = new THREE.MeshStandardMaterial({{ 
        color: 0xa0a0a0, 
        metalness: 0.85, 
        roughness: 0.25 
    }});
    const artifactMesh = new THREE.Mesh(artifactGeometry, artifactMaterial);
    artifactMesh.position.set(0, 2.2, 0);
    artifactMesh.castShadow = true;
    artifactMesh.receiveShadow = true;
    scene.add(artifactMesh);

    // 6. Interactive Controls
    const controls = new OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true; // Smooth physics
    controls.dampingFactor = 0.05;
    controls.enablePan = false;    // Keep artifact centered
    controls.minDistance = 4;
    controls.maxDistance = 15;
    controls.minPolarAngle = 0.1;
    controls.maxPolarAngle = 1.45; // Prevent camera from going under the ground
    controls.target.set(0, 1.5, 0);

    // 7. Render Loop
    function animate() {{
        requestAnimationFrame(animate);
        
        // Slight idle rotation to show off lighting if user isn't interacting
        if(!controls.state && artifactMesh) {{
            artifactMesh.rotation.y += 0.002;
        }}

        controls.update(); // Required for damping
        renderer.render(scene, camera);
    }}
    animate();

    // 8. Handle Resizing
    window.addEventListener('resize', () => {{
        width = container.clientWidth;
        height = container.clientHeight;
        camera.aspect = width / height;
        camera.updateProjectionMatrix();
        renderer.setSize(width, height);
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
