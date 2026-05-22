def create_component(
    output_dir: str,
    title_text: str = "Parallax Depth",
    body_text: str = "A cinematic 2.5D WebGL experience.",
    color_scheme: str = "dark",
    accent_color: str = "#00bfff",
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the 2.5D Parallax Depth Slicing effect.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme ===
    if color_scheme == "dark":
        bg_color = "#050510"
        text_color = "#ffffff"
        overlay_grad = "linear-gradient(to top, rgba(5, 5, 16, 0.9) 0%, rgba(5, 5, 16, 0.1) 100%)"
        sky_color = "#0a0a2a"
        mid_color = "#1f1f45"
        fore_color = "#0d0d1c"
    else:
        bg_color = "#e0e5ec"
        text_color = "#1a1a2e"
        overlay_grad = "linear-gradient(to top, rgba(224, 229, 236, 0.9) 0%, rgba(224, 229, 236, 0.1) 100%)"
        sky_color = "#b8c6db"
        mid_color = "#889cbd"
        fore_color = "#4a5d7c"

    # === CSS ===
    css = f"""/* 2.5D Parallax Depth Slicing - CSS */
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
    --overlay: {overlay_grad};
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background: var(--bg);
    color: var(--text);
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 100vh;
    overflow: hidden;
}}

.viewport-container {{
    width: var(--width);
    height: var(--height);
    position: relative;
    overflow: hidden;
    background: var(--bg);
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
    border-radius: 12px;
}}

/* The WebGL Canvas container */
#webgl-container {{
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    z-index: 1;
}}

/* UI Overlay */
.content-overlay {{
    position: absolute;
    bottom: 0;
    left: 0;
    width: 100%;
    height: 50%;
    z-index: 10;
    display: flex;
    flex-direction: column;
    justify-content: flex-end;
    padding: 40px;
    background: var(--overlay);
    pointer-events: none; /* Let mouse events pass through to canvas */
}}

.title {{
    font-size: 3.5rem;
    font-weight: 700;
    letter-spacing: -0.02em;
    margin-bottom: 12px;
    line-height: 1.1;
    text-shadow: 0 4px 12px rgba(0,0,0,0.3);
}}

.title span {{
    color: var(--accent);
}}

.body-text {{
    font-size: 1.25rem;
    font-weight: 300;
    max-width: 600px;
    line-height: 1.6;
    opacity: 0.9;
    text-shadow: 0 2px 8px rgba(0,0,0,0.3);
}}

.controls {{
    position: absolute;
    top: 20px;
    right: 20px;
    z-index: 10;
    pointer-events: auto;
}}

.btn {{
    background: transparent;
    border: 1px solid var(--accent);
    color: var(--accent);
    padding: 8px 16px;
    border-radius: 20px;
    font-family: inherit;
    font-size: 0.9rem;
    cursor: pointer;
    backdrop-filter: blur(4px);
    transition: all 0.3s ease;
}}

.btn:hover {{
    background: var(--accent);
    color: var(--bg);
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
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
    <!-- Load Three.js -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
</head>
<body>
    <div class="viewport-container">
        <div id="webgl-container"></div>
        
        <div class="content-overlay">
            <h1 class="title"><span>{title_text.split()[0] if " " in title_text else title_text}</span> {" ".join(title_text.split()[1:]) if " " in title_text else ""}</h1>
            <p class="body-text">{body_text}</p>
        </div>

        <div class="controls">
            <button class="btn" id="replay-btn">Replay Animation</button>
        </div>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// 2.5D Parallax WebGL logic
document.addEventListener('DOMContentLoaded', () => {{
    const container = document.getElementById('webgl-container');
    const width = container.clientWidth;
    const height = container.clientHeight;

    // 1. Setup Scene, Camera, Renderer
    const scene = new THREE.Scene();
    
    // Field of View, Aspect Ratio, Near, Far
    const camera = new THREE.PerspectiveCamera(75, width / height, 0.1, 10000);
    
    const renderer = new THREE.WebGLRenderer({{ antialias: true, alpha: true }});
    renderer.setSize(width, height);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    container.appendChild(renderer.domElement);

    // 2. Generate Procedural Textures via Canvas (Ensures 100% reproducibility without external images)
    function createLayerTexture(type) {{
        const canvas = document.createElement('canvas');
        canvas.width = 2048;
        canvas.height = 1024;
        const ctx = canvas.getContext('2d');

        if (type === 'bg') {{
            // Background: Sky and distant atmosphere
            ctx.fillStyle = '{sky_color}';
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            
            // Add some "stars" or atmosphere dust
            for(let i=0; i<300; i++) {{
                ctx.fillStyle = 'rgba(255,255,255,' + Math.random()*0.5 + ')';
                ctx.beginPath();
                ctx.arc(Math.random()*canvas.width, Math.random()*(canvas.height/1.5), Math.random()*2, 0, Math.PI*2);
                ctx.fill();
            }}
        }} else if (type === 'mid') {{
            // Midground: Mountains with transparent sky
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            ctx.fillStyle = '{mid_color}';
            ctx.beginPath();
            ctx.moveTo(0, canvas.height);
            ctx.lineTo(0, canvas.height * 0.6);
            
            // Generate jagged mountain peaks
            let points = 15;
            for (let i = 1; i <= points; i++) {{
                let x = (canvas.width / points) * i;
                let y = canvas.height * (0.3 + Math.random() * 0.4);
                ctx.lineTo(x, y);
            }}
            ctx.lineTo(canvas.width, canvas.height);
            ctx.fill();
            
            // Fog at bottom
            let grad = ctx.createLinearGradient(0, canvas.height*0.8, 0, canvas.height);
            grad.addColorStop(0, 'transparent');
            grad.addColorStop(1, '{bg_color}');
            ctx.fillStyle = grad;
            ctx.fillRect(0, canvas.height*0.8, canvas.width, canvas.height*0.2);

        }} else if (type === 'fore') {{
            // Foreground: Silhouettes/Hills
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            ctx.fillStyle = '{fore_color}';
            ctx.beginPath();
            ctx.moveTo(0, canvas.height);
            ctx.lineTo(0, canvas.height * 0.8);
            
            ctx.quadraticCurveTo(canvas.width * 0.2, canvas.height * 0.6, canvas.width * 0.5, canvas.height * 0.85);
            ctx.quadraticCurveTo(canvas.width * 0.8, canvas.height * 0.7, canvas.width, canvas.height * 0.9);
            
            ctx.lineTo(canvas.width, canvas.height);
            ctx.fill();
        }}

        const texture = new THREE.CanvasTexture(canvas);
        texture.minFilter = THREE.LinearFilter;
        return texture;
    }}

    // 3. Create Meshes & Apply Depth Scaling
    // In Parallax stacking, layers further back must be scaled UP so they look correct from the starting camera position.
    
    // Standard sizes
    const planeWidth = 1600;
    const planeHeight = 800;

    const layers = [];
    
    const layerConfigs = [
        {{ tex: 'bg', z: -2000, scale: 3.5 }},
        {{ tex: 'mid', z: -1000, scale: 2.2 }},
        {{ tex: 'fore', z: 0, scale: 1.1 }}
    ];

    layerConfigs.forEach(config => {{
        const geometry = new THREE.PlaneGeometry(planeWidth, planeHeight);
        const material = new THREE.MeshBasicMaterial({{ 
            map: createLayerTexture(config.tex),
            transparent: true,
            depthWrite: false // Prevents transparency sorting glitches
        }});
        const mesh = new THREE.Mesh(geometry, material);
        
        mesh.position.z = config.z;
        mesh.scale.set(config.scale, config.scale, 1);
        
        scene.add(mesh);
        layers.push(mesh);
    }});

    // 4. Animation Settings
    let initialCameraZ = 800;
    let targetCameraZ = 150; // How close it gets to the foreground plane
    
    let currentAnimZ = initialCameraZ;
    let mouseX = 0;
    let mouseY = 0;
    let targetX = 0;
    let targetY = 0;

    camera.position.z = initialCameraZ;

    // Track mouse for subtle parallax pan
    container.addEventListener('mousemove', (e) => {{
        const rect = container.getBoundingClientRect();
        // Normalize from -1 to 1
        mouseX = ((e.clientX - rect.left) / width) * 2 - 1;
        mouseY = -((e.clientY - rect.top) / height) * 2 + 1;
    }});

    // 5. Render Loop
    let isAnimating = true;

    function animate() {{
        requestAnimationFrame(animate);

        // Auto fly-through zooming logic
        if (isAnimating) {{
            // Ease camera forward
            currentAnimZ += (targetCameraZ - currentAnimZ) * 0.015;
            
            // Stop auto-animation if we are very close to target
            if (Math.abs(currentAnimZ - targetCameraZ) < 1) {{
                isAnimating = false;
            }}
        }}

        // Mouse pan interpolation (easing)
        targetX = mouseX * 100;
        targetY = mouseY * 50;
        
        camera.position.x += (targetX - camera.position.x) * 0.05;
        // Combine auto-pan (slight downward dip) with mouse pan
        let baseDip = isAnimating ? (initialCameraZ - currentAnimZ) * -0.05 : -32.5;
        camera.position.y += ((targetY + baseDip) - camera.position.y) * 0.05;
        
        // Apply Z
        camera.position.z = currentAnimZ;

        renderer.render(scene, camera);
    }}

    animate();

    // 6. Replay Button
    document.getElementById('replay-btn').addEventListener('click', () => {{
        currentAnimZ = initialCameraZ;
        camera.position.set(0, 0, initialCameraZ);
        isAnimating = true;
    }});

    // Handle Resize
    window.addEventListener('resize', () => {{
        const newWidth = container.clientWidth;
        const newHeight = container.clientHeight;
        renderer.setSize(newWidth, newHeight);
        camera.aspect = newWidth / newHeight;
        camera.updateProjectionMatrix();
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
