def create_component(
    output_dir: str,
    title_text: str = "Glossy Gradients",
    body_text: str = "Interactive fluid dynamics powered by WebGL",
    color_scheme: str = "dark",
    accent_color: str = "#00f0ff",
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Interactive WebGL Fluid Gradient effect.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Derive palette based on color_scheme
    if color_scheme == "dark":
        c1 = accent_color
        c2 = "#1d1135"  # Deep violet
        c3 = "#0c1631"  # Deep navy
        c4 = "#2e0f27"  # Deep plum
        text_color = "#ffffff"
        bg_color = "#050505"
    else:
        c1 = accent_color
        c2 = "#f3e8ff"  # Soft purple
        c3 = "#e0f2fe"  # Soft sky
        c4 = "#fae8ff"  # Soft fuchsia
        text_color = "#0f172a"
        bg_color = "#f8fafc"

    css = f"""/* Interactive WebGL Fluid Gradient */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');

*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --text: {text_color};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Inter', sans-serif;
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
    max-width: 100vw;
    max-height: 100vh;
    position: relative;
    overflow: hidden;
    border-radius: 16px;
    box-shadow: 0 24px 64px rgba(0,0,0,0.4);
    background: var(--bg);
}}

#gradient-canvas {{
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    z-index: 0;
}}

.content-overlay {{
    position: relative;
    z-index: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100%;
    text-align: center;
    pointer-events: none; /* Allows mouse events to reach the canvas interaction */
    padding: 2rem;
}}

.navbar {{
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    padding: 2rem 3rem;
    display: flex;
    justify-content: space-between;
    font-weight: 600;
    font-size: 0.9rem;
    letter-spacing: 0.05em;
    text-transform: uppercase;
}}

.logo {{
    font-size: 1.25rem;
    font-weight: 800;
    letter-spacing: -0.05em;
}}

.nav-links span {{
    margin-left: 2rem;
    opacity: 0.7;
}}

h1 {{
    font-size: clamp(3rem, 6vw, 6rem);
    font-weight: 800;
    letter-spacing: -0.04em;
    line-height: 1.1;
    margin-bottom: 1.5rem;
    text-shadow: 0 12px 32px rgba(0,0,0,0.3);
}}

p {{
    font-size: clamp(1rem, 1.5vw, 1.25rem);
    opacity: 0.9;
    max-width: 600px;
    text-shadow: 0 4px 12px rgba(0,0,0,0.3);
}}
"""

    vert_shader = """
varying vec2 vUv;
void main() {
    vUv = uv;
    gl_Position = vec4(position, 1.0);
}
"""

    fluid_frag = """
varying vec2 vUv;
uniform sampler2D uPreviousFrame;
uniform vec2 uResolution;
uniform vec4 uMouse;
uniform float uBrushSize;
uniform float uBrushStrength;
uniform float uFluidDecay;

void main() {
    vec2 offset = texture2D(uPreviousFrame, vUv).xy;
    vec2 velocity = uMouse.xy - uMouse.zw;
    
    float aspect = uResolution.x / uResolution.y;
    vec2 p = vUv * vec2(aspect, 1.0);
    vec2 m = uMouse.xy * vec2(aspect, 1.0);
    
    float dist = length(p - m);
    float influence = smoothstep(uBrushSize, 0.0, dist);
    
    offset += velocity * influence * uBrushStrength;
    offset *= uFluidDecay;
    offset = clamp(offset, -1.0, 1.0);
    
    gl_FragColor = vec4(offset, 0.0, 1.0);
}
"""

    display_frag = """
varying vec2 vUv;
uniform sampler2D uFluid;
uniform float uTime;
uniform vec3 uColor1;
uniform vec3 uColor2;
uniform vec3 uColor3;
uniform vec3 uColor4;
uniform float uDistortionAmount;

void main() {
    vec2 offset = texture2D(uFluid, vUv).xy;
    vec2 p = vUv + offset * uDistortionAmount;

    // Time driver
    float t = uTime * 0.4;
    
    // Procedural wavy distortion
    vec2 q = vec2(
        sin(p.y * 3.0 + t) * 0.5 + p.x,
        cos(p.x * 3.0 - t) * 0.5 + p.y
    );
    
    // Overlapping waves for glossy lighting
    float n1 = sin(q.x * 2.5 + t);
    float n2 = cos(q.y * 2.0 - t * 0.8);
    float n3 = sin((q.x + q.y) * 1.5 + t * 1.2);
    
    // Calculate color blending weights
    float w1 = max(0.0, n1 + n2);
    float w2 = max(0.0, n2 - n3);
    float w3 = max(0.0, n3 - n1);
    float w4 = max(0.0, -(n1 + n2 + n3));
    
    // Normalize weights to avoid blowouts
    float sum = w1 + w2 + w3 + w4 + 0.01;
    w1 /= sum; w2 /= sum; w3 /= sum; w4 /= sum;
    
    vec3 col = uColor1 * w1 + uColor2 * w2 + uColor3 * w3 + uColor4 * w4;
    
    // Subtle vignette to center focus
    float dist = distance(vUv, vec2(0.5));
    col *= smoothstep(1.2, 0.2, dist * 0.6 + 0.2);

    gl_FragColor = vec4(col, 1.0);
}
"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text}</title>
    <link rel="stylesheet" href="style.css">
    
    <!-- Three.js CDN -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>

    <!-- Shaders -->
    <script id="vertShader" type="x-shader/x-vertex">{vert_shader}</script>
    <script id="fluidFragShader" type="x-shader/x-fragment">{fluid_frag}</script>
    <script id="displayFragShader" type="x-shader/x-fragment">{display_frag}</script>
    
    <script src="script.js" defer></script>
</head>
<body>
    <div class="container" id="main-container">
        <!-- WebGL Canvas Layer -->
        <div id="gradient-canvas"></div>
        
        <!-- UI Overlay Layer -->
        <div class="content-overlay">
            <nav class="navbar">
                <div class="logo">WWW.</div>
                <div class="nav-links">
                    <span>Work</span>
                    <span>Studio</span>
                </div>
            </nav>
            <h1>{title_text}</h1>
            <p>{body_text}</p>
        </div>
    </div>
</body>
</html>"""

    js = f"""
document.addEventListener('DOMContentLoaded', () => {{
    const container = document.getElementById('main-container');
    const canvasContainer = document.getElementById('gradient-canvas');
    
    let width = container.clientWidth;
    let height = container.clientHeight;

    // Palette injected from Python generator
    const COLORS = {{
        c1: "{c1}",
        c2: "{c2}",
        c3: "{c3}",
        c4: "{c4}"
    }};

    // 1. Scene Setup
    const scene = new THREE.Scene();
    const camera = new THREE.OrthographicCamera(-1, 1, 1, -1, 0, 1);
    const geometry = new THREE.PlaneGeometry(2, 2);

    const renderer = new THREE.WebGLRenderer({{ antialias: false, alpha: true }});
    renderer.setSize(width, height);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    canvasContainer.appendChild(renderer.domElement);

    // 2. Ping-Pong Render Targets
    const rtParams = {{
        minFilter: THREE.LinearFilter,
        magFilter: THREE.LinearFilter,
        format: THREE.RGBAFormat,
        type: THREE.HalfFloatType, // Best precision/performance balance for mobile/desktop
        depthBuffer: false,
        stencilBuffer: false
    }};
    let rtA = new THREE.WebGLRenderTarget(width, height, rtParams);
    let rtB = new THREE.WebGLRenderTarget(width, height, rtParams);

    // 3. Materials
    const fluidMaterial = new THREE.ShaderMaterial({{
        vertexShader: document.getElementById('vertShader').textContent,
        fragmentShader: document.getElementById('fluidFragShader').textContent,
        uniforms: {{
            uPreviousFrame: {{ value: null }},
            uResolution: {{ value: new THREE.Vector2(width, height) }},
            uMouse: {{ value: new THREE.Vector4(0, 0, 0, 0) }},
            uBrushSize: {{ value: 0.15 }},
            uBrushStrength: {{ value: 2.5 }},
            uFluidDecay: {{ value: 0.96 }} // Value < 1 ensures trails fade
        }}
    }});

    const displayMaterial = new THREE.ShaderMaterial({{
        vertexShader: document.getElementById('vertShader').textContent,
        fragmentShader: document.getElementById('displayFragShader').textContent,
        uniforms: {{
            uFluid: {{ value: null }},
            uTime: {{ value: 0.0 }},
            uColor1: {{ value: new THREE.Color(COLORS.c1) }},
            uColor2: {{ value: new THREE.Color(COLORS.c2) }},
            uColor3: {{ value: new THREE.Color(COLORS.c3) }},
            uColor4: {{ value: new THREE.Color(COLORS.c4) }},
            uDistortionAmount: {{ value: 1.0 }}
        }}
    }});

    const mesh = new THREE.Mesh(geometry, fluidMaterial);
    scene.add(mesh);

    // 4. Interaction Logic
    let targetMouse = {{ x: 0.5, y: 0.5 }};
    let mouse = {{ x: 0.5, y: 0.5, prevX: 0.5, prevY: 0.5 }};

    window.addEventListener('pointermove', (e) => {{
        const rect = container.getBoundingClientRect();
        targetMouse.x = (e.clientX - rect.left) / width;
        targetMouse.y = 1.0 - ((e.clientY - rect.top) / height); // WebGL Y is flipped
    }});

    window.addEventListener('resize', () => {{
        width = container.clientWidth;
        height = container.clientHeight;
        renderer.setSize(width, height);
        rtA.setSize(width, height);
        rtB.setSize(width, height);
        fluidMaterial.uniforms.uResolution.value.set(width, height);
    }});

    // 5. Render Loop
    const clock = new THREE.Clock();

    function animate() {{
        requestAnimationFrame(animate);
        const time = clock.getElapsedTime();

        // Interpolate mouse for smooth velocity vectors
        const vx = targetMouse.x - mouse.x;
        const vy = targetMouse.y - mouse.y;
        mouse.prevX = mouse.x;
        mouse.prevY = mouse.y;
        mouse.x += vx * 0.2; 
        mouse.y += vy * 0.2;

        // Pass 1: Render Fluid Buffer
        fluidMaterial.uniforms.uPreviousFrame.value = rtA.texture;
        fluidMaterial.uniforms.uMouse.value.set(mouse.x, mouse.y, mouse.prevX, mouse.prevY);
        
        mesh.material = fluidMaterial;
        renderer.setRenderTarget(rtB);
        renderer.render(scene, camera);

        // Pass 2: Render Display to Canvas
        displayMaterial.uniforms.uFluid.value = rtB.texture;
        displayMaterial.uniforms.uTime.value = time;
        
        mesh.material = displayMaterial;
        renderer.setRenderTarget(null); // Render to screen
        renderer.render(scene, camera);

        // Pass 3: Swap Buffers (Ping-Pong)
        const temp = rtA;
        rtA = rtB;
        rtB = temp;
    }}
    
    animate();
}});
"""

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
