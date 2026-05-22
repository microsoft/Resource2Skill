def create_component(
    output_dir: str,
    title_text: str = "Scroll to Explore",
    body_text: str = "A journey through 3D space driven by your scroll.",
    color_scheme: str = "dark",
    accent_color: str = "#00bfff",
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Scroll-Driven 3D Canvas Parallax effect.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Theme Derivation ===
    if color_scheme == "dark":
        bg_color = "#0B0C10"
        text_color = "#C5C6C7"
        surface_color = "rgba(31, 40, 51, 0.6)"
        star_color = 0xffffff
        wireframe_color = 0x66fcf1
    else:
        bg_color = "#F0F0F0"
        text_color = "#121212"
        surface_color = "rgba(255, 255, 255, 0.6)"
        star_color = 0x121212
        wireframe_color = 0x444444

    # Convert to hex values for Three.js Color objects
    bg_hex = bg_color.replace("#", "0x")
    accent_hex = accent_color.replace("#", "0x")
    star_hex = hex(star_color)
    wireframe_hex = hex(wireframe_color)

    # === CSS ===
    css = f"""/* Scroll-Driven 3D Canvas Background */
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
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background: #000;
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
}}

.container {{
    width: var(--width);
    height: var(--height);
    overflow-y: auto;
    overflow-x: hidden;
    position: relative;
    background: var(--bg);
    color: var(--text);
    scroll-behavior: smooth;
    box-shadow: 0 0 50px rgba(0,0,0,0.5);
}}

.canvas-wrapper {{
    position: sticky;
    top: 0;
    left: 0;
    width: 100%;
    height: var(--height);
    z-index: 0;
}}

canvas#bg {{
    display: block;
    width: 100%;
    height: 100%;
}}

main {{
    position: relative;
    z-index: 1;
    /* Pulls the scrolling content directly over the sticky canvas wrapper */
    margin-top: calc(var(--height) * -1); 
}}

section {{
    min-height: var(--height);
    display: flex;
    align-items: center;
    padding: 0 10%;
}}

.left {{ justify-content: flex-start; }}
.right {{ justify-content: flex-end; }}
.center {{ justify-content: center; text-align: center; }}

.header-content h1 {{
    font-size: clamp(3rem, 6vw, 6rem);
    font-weight: 900;
    text-transform: uppercase;
    letter-spacing: -2px;
    margin-bottom: 1rem;
    color: var(--accent);
    text-shadow: 0 4px 20px rgba(0,0,0,0.4);
}}

.header-content p {{
    font-size: 1.5rem;
    max-width: 600px;
    margin: 0 auto;
}}

.card {{
    background: var(--surface);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    padding: 3rem;
    border-radius: 16px;
    border: 1px solid rgba(255, 255, 255, 0.1);
    box-shadow: 0 20px 40px rgba(0,0,0,0.2);
    max-width: 450px;
}}

.card h2 {{
    font-size: 2rem;
    margin-bottom: 1rem;
    color: var(--accent);
}}

.card p {{
    font-size: 1.1rem;
    line-height: 1.6;
    opacity: 0.9;
}}
"""

    # === JavaScript ===
    js = f"""import * as THREE from 'three';

document.addEventListener('DOMContentLoaded', () => {{
    const canvas = document.querySelector('#bg');
    const container = document.querySelector('.container');

    const scene = new THREE.Scene();
    scene.background = new THREE.Color({bg_hex});

    const camera = new THREE.PerspectiveCamera(75, container.clientWidth / container.clientHeight, 0.1, 1000);
    
    const renderer = new THREE.WebGLRenderer({{ canvas: canvas, antialias: true }});
    renderer.setPixelRatio(window.devicePixelRatio);
    renderer.setSize(container.clientWidth, container.clientHeight);
    
    // 1. Core Geometry: Torus
    const torusGeo = new THREE.TorusGeometry(10, 3, 16, 100);
    const torusMat = new THREE.MeshStandardMaterial({{ color: {accent_hex} }});
    const torus = new THREE.Mesh(torusGeo, torusMat);
    scene.add(torus);

    // 2. Procedural Starfield
    function addStar() {{
        const geometry = new THREE.SphereGeometry(0.25, 24, 24);
        const material = new THREE.MeshStandardMaterial({{ color: {star_hex} }});
        const star = new THREE.Mesh(geometry, material);

        const [x, y, z] = Array(3).fill().map(() => THREE.MathUtils.randFloatSpread(150));
        star.position.set(x, y, z);
        scene.add(star);
    }}
    Array(300).fill().forEach(addStar);

    // 3. Avatar Box mapped with Procedural Canvas Texture
    const avatarCanvas = document.createElement('canvas');
    avatarCanvas.width = 256;
    avatarCanvas.height = 256;
    const ctx = avatarCanvas.getContext('2d');
    ctx.fillStyle = '{accent_color}';
    ctx.fillRect(0, 0, 256, 256);
    ctx.fillStyle = '#ffffff';
    ctx.font = 'bold 120px sans-serif';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText('3D', 128, 128);
    
    const avatarTexture = new THREE.CanvasTexture(avatarCanvas);
    const avatar = new THREE.Mesh(
        new THREE.BoxGeometry(4, 4, 4),
        new THREE.MeshBasicMaterial({{ map: avatarTexture }})
    );
    avatar.position.set(8, 2, 10);
    scene.add(avatar);

    // 4. Secondary Geometry: Wireframe Sphere (Moon)
    const moon = new THREE.Mesh(
        new THREE.SphereGeometry(5, 32, 32),
        new THREE.MeshStandardMaterial({{ color: {wireframe_hex}, wireframe: true }})
    );
    moon.position.set(-10, -5, 25);
    scene.add(moon);

    // 5. Lighting Setup
    const dirLight = new THREE.DirectionalLight(0xffffff, 3);
    dirLight.position.set(10, 10, 10);
    const ambientLight = new THREE.AmbientLight(0xffffff, 1.5);
    scene.add(dirLight, ambientLight);

    // Initial Camera State
    camera.position.z = 40;

    // Scroll Logic 
    function moveCamera() {{
        // Measure scroll within our custom container
        const t = container.scrollTop * -1;
        
        moon.rotation.x += 0.05;
        moon.rotation.y += 0.075;
        moon.rotation.z += 0.05;

        avatar.rotation.y += 0.01;
        avatar.rotation.z += 0.01;

        // Camera flies forward on scroll
        camera.position.z = 40 + t * 0.015;
        camera.position.x = t * -0.0002;
        camera.rotation.y = t * -0.0002;
    }}
    
    container.addEventListener('scroll', moveCamera);
    moveCamera(); // Initialize initial offsets

    // Animation Render Loop
    function animate() {{
        requestAnimationFrame(animate);

        // Ambient animations separate from scroll
        torus.rotation.x += 0.01;
        torus.rotation.y += 0.005;
        torus.rotation.z += 0.01;

        renderer.render(scene, camera);
    }}
    animate();

    // Responsive Canvas Resize Listener
    window.addEventListener('resize', () => {{
        renderer.setSize(container.clientWidth, container.clientHeight);
        camera.aspect = container.clientWidth / container.clientHeight;
        camera.updateProjectionMatrix();
    }});
}});
"""

    # === HTML ===
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
    <!-- Unbundled Three.js loaded via native ES Module Import Map -->
    <script type="importmap">
        {{
            "imports": {{
                "three": "https://unpkg.com/three@0.160.0/build/three.module.js"
            }}
        }}
    </script>
</head>
<body>
    <div class="container">
        <!-- Sticky Wrapper holds the WebGL context in place -->
        <div class="canvas-wrapper">
            <canvas id="bg"></canvas>
        </div>
        
        <!-- Standard flow HTML slides naturally over the canvas -->
        <main>
            <section class="center">
                <div class="header-content">
                    <h1>{title_text}</h1>
                    <p>{body_text}</p>
                </div>
            </section>
            
            <section class="left">
                <div class="card">
                    <h2>Immersive Depth</h2>
                    <p>The camera glides past geometric forms as you scroll, creating a cinematic parallax effect that brings the interface to life.</p>
                </div>
            </section>

            <section class="right">
                <div class="card">
                    <h2>Dynamic Textures</h2>
                    <p>Objects are mapped with procedural canvas textures and wireframes, responding to lights and scroll positions simultaneously.</p>
                </div>
            </section>

            <section class="center">
                <div class="card">
                    <h2>Endless Space</h2>
                    <p>A procedurally generated starfield creates an expansive background layer without relying on large image assets.</p>
                </div>
            </section>
        </main>
    </div>
    
    <script type="module" src="script.js"></script>
</body>
</html>"""

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
