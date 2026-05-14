def create_component(
    output_dir: str,
    title_text: str = "Building Brands for the Digital World",
    body_text: str = "We help brands grow through innovative design, cutting-edge development, and strategic digital marketing. Experience the future of web interaction.",
    color_scheme: str = "light",       # "dark" or "light"
    accent_color: str = "#A855F7",     # CSS hex color for accent
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Interactive 3D Particle Landing Page.
    
    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme and accent_color ===
    if color_scheme == "dark":
        bg_color = "#0f1015"
        text_color = "#ffffff"
        text_muted = "#9ca3af"
        surface_color = "rgba(255, 255, 255, 0.05)"
        surface_border = "rgba(255, 255, 255, 0.1)"
    else:
        bg_color = "#f4f4f9"
        text_color = "#111827"
        text_muted = "#4b5563"
        surface_color = "rgba(255, 255, 255, 0.6)"
        surface_border = "rgba(0, 0, 0, 0.05)"

    # === CSS ===
    css = f"""/* Interactive 3D Particle Landing Page */
:root {{
    --bg-color: {bg_color};
    --text-color: {text_color};
    --text-muted: {text_muted};
    --accent-color: {accent_color};
    --surface-color: {surface_color};
    --surface-border: {surface_border};
    --max-width: {width_px}px;
}}

*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background-color: var(--bg-color);
    color: var(--text-color);
    line-height: 1.6;
    overflow-x: hidden;
}}

/* WebGL Background Container */
#webgl-container {{
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    z-index: -1;
    pointer-events: none;
}}

/* Layout & Typography */
.container {{
    max-width: var(--max-width);
    margin: 0 auto;
    padding: 0 2rem;
    position: relative;
    z-index: 10;
}}

nav {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 2rem 0;
}}

.logo {{
    font-size: 1.5rem;
    font-weight: 800;
    letter-spacing: -1px;
}}

.nav-links {{
    display: flex;
    gap: 2rem;
    list-style: none;
}}

.nav-links a {{
    text-decoration: none;
    color: var(--text-color);
    font-weight: 500;
    font-size: 0.9rem;
    transition: color 0.3s ease;
}}

.nav-links a:hover {{
    color: var(--accent-color);
}}

.btn {{
    background: var(--text-color);
    color: var(--bg-color);
    padding: 0.75rem 1.5rem;
    border-radius: 50px;
    text-decoration: none;
    font-weight: 600;
    font-size: 0.9rem;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    display: inline-block;
    border: none;
    cursor: pointer;
}}

.btn:hover {{
    transform: translateY(-2px);
    box-shadow: 0 10px 20px rgba(0,0,0,0.1);
}}

.btn-outline {{
    background: transparent;
    color: var(--text-color);
    border: 2px solid var(--text-color);
}}

/* Hero Section */
.hero {{
    min-height: calc({height_px}px - 100px);
    display: flex;
    align-items: center;
    padding: 4rem 0;
}}

.hero-grid {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 4rem;
    align-items: center;
}}

.hero-content h1 {{
    font-size: clamp(3rem, 5vw, 4.5rem);
    font-weight: 800;
    line-height: 1.1;
    letter-spacing: -2px;
    margin-bottom: 1.5rem;
}}

.gradient-text {{
    background: linear-gradient(135deg, var(--accent-color), #f43f5e);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    color: transparent;
    display: inline-block;
}}

.hero-content p {{
    font-size: 1.1rem;
    color: var(--text-muted);
    margin-bottom: 2.5rem;
    max-width: 480px;
}}

.hero-actions {{
    display: flex;
    gap: 1rem;
}}

/* Right side visual & badge */
.hero-visual {{
    position: relative;
    height: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
}}

.glass-card {{
    background: var(--surface-color);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border: 1px solid var(--surface-border);
    border-radius: 24px;
    padding: 2rem;
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.1);
    position: relative;
    z-index: 2;
}}

.glass-card img {{
    width: 100%;
    border-radius: 16px;
    display: block;
}}

/* Spinning Badge */
.spinning-badge {{
    position: absolute;
    top: -30px;
    left: -30px;
    width: 120px;
    height: 120px;
    background: var(--text-color);
    color: var(--bg-color);
    border-radius: 50%;
    display: flex;
    justify-content: center;
    align-items: center;
    font-size: 0.75rem;
    font-weight: bold;
    text-transform: uppercase;
    letter-spacing: 2px;
    z-index: 3;
    animation: spin 10s linear infinite;
    text-align: center;
    padding: 1rem;
    box-shadow: 0 10px 20px rgba(0,0,0,0.15);
}}

@keyframes spin {{
    0% {{ transform: rotate(0deg); }}
    100% {{ transform: rotate(360deg); }}
}}

/* Responsive */
@media (max-width: 900px) {{
    .hero-grid {{
        grid-template-columns: 1fr;
        text-align: center;
    }}
    .hero-content p {{
        margin: 0 auto 2.5rem auto;
    }}
    .hero-actions {{
        justify-content: center;
    }}
    .nav-links {{
        display: none; /* Hide on mobile for simplicity */
    }}
}}
"""

    # === HTML ===
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Interactive 3D Particle Landing Page</title>
    
    <!-- Google Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;800&display=swap" rel="stylesheet">
    
    <!-- AOS CSS for scroll animations -->
    <link href="https://unpkg.com/aos@2.3.1/dist/aos.css" rel="stylesheet">
    
    <link rel="stylesheet" href="style.css">
</head>
<body>

    <!-- WebGL Background -->
    <div id="webgl-container"></div>

    <div class="container">
        <!-- Navigation -->
        <nav data-aos="fade-down" data-aos-duration="1000">
            <div class="logo">BRAND.</div>
            <ul class="nav-links">
                <li><a href="#">Home</a></li>
                <li><a href="#">Services</a></li>
                <li><a href="#">Features</a></li>
                <li><a href="#">About</a></li>
            </ul>
            <a href="#" class="btn">Login</a>
        </nav>

        <!-- Hero Section -->
        <section class="hero">
            <div class="hero-grid">
                
                <div class="hero-content">
                    <h1 data-aos="fade-up" data-aos-duration="1000" data-aos-delay="100">
                        {title_text.replace('Digital', '<span class="gradient-text">Digital</span>')}
                    </h1>
                    <p data-aos="fade-up" data-aos-duration="1000" data-aos-delay="200">
                        {body_text}
                    </p>
                    <div class="hero-actions" data-aos="fade-up" data-aos-duration="1000" data-aos-delay="300">
                        <a href="#" class="btn">Get Started</a>
                        <a href="#" class="btn btn-outline">More Details</a>
                    </div>
                </div>

                <div class="hero-visual" data-aos="zoom-in-up" data-aos-duration="1200" data-aos-delay="400">
                    <div class="spinning-badge">
                        Discover<br>The Magic<br>Of WebGL
                    </div>
                    <div class="glass-card">
                        <!-- Placeholder block for a visually pleasing image/graphic -->
                        <div style="width: 100%; height: 300px; background: linear-gradient(45deg, rgba({int(accent_color[1:3], 16)},{int(accent_color[3:5], 16)},{int(accent_color[5:7], 16)},0.2), transparent); border-radius: 16px; display:flex; align-items:center; justify-content:center;">
                             <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="var(--accent-color)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="3 11 22 2 13 21 11 13 3 11"></polygon></svg>
                        </div>
                    </div>
                </div>

            </div>
        </section>
    </div>

    <!-- Three.js Library -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <!-- AOS Library -->
    <script src="https://unpkg.com/aos@2.3.1/dist/aos.js"></script>
    
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Initialize AOS Animations
AOS.init({{
    once: true,
    offset: 50,
}});

// --- WebGL 3D Particle System Setup ---
const container = document.getElementById('webgl-container');

// Scene, Camera, Renderer
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
const renderer = new THREE.WebGLRenderer({{ alpha: true, antialias: true }}); // Alpha true for transparent bg

renderer.setSize(window.innerWidth, window.innerHeight);
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2)); // Performance optimization
container.appendChild(renderer.domElement);

// Create Particles
const particlesGeometry = new THREE.BufferGeometry();
const particlesCount = 2500; // Adjust for density
const posArray = new Float32Array(particlesCount * 3);

// Generate random positions spread across a wide area
for(let i = 0; i < particlesCount * 3; i++) {{
    posArray[i] = (Math.random() - 0.5) * 15; // Spread multiplier
}}

particlesGeometry.setAttribute('position', new THREE.BufferAttribute(posArray, 3));

// Material setup using the dynamic accent color
const particlesMaterial = new THREE.PointsMaterial({{
    size: 0.03,
    color: '{accent_color}', // Matches the accent color from Python
    transparent: true,
    opacity: 0.8,
    blending: THREE.AdditiveBlending // Gives a nice glowing effect when particles overlap
}});

// Mesh
const particlesMesh = new THREE.Points(particlesGeometry, particlesMaterial);
scene.add(particlesMesh);

camera.position.z = 3;

// Mouse Interaction Logic
let mouseX = 0;
let mouseY = 0;
let targetX = 0;
let targetY = 0;

const windowHalfX = window.innerWidth / 2;
const windowHalfY = window.innerHeight / 2;

document.addEventListener('mousemove', (event) => {{
    mouseX = (event.clientX - windowHalfX);
    mouseY = (event.clientY - windowHalfY);
}});

// Animation Loop
const clock = new THREE.Clock();

function animate() {{
    requestAnimationFrame(animate);
    const elapsedTime = clock.getElapsedTime();

    // Constant slow rotation
    particlesMesh.rotation.y = elapsedTime * 0.05;
    particlesMesh.rotation.x = elapsedTime * 0.02;

    // Mouse interactive rotation (Lerp towards mouse position)
    targetX = mouseX * 0.001;
    targetY = mouseY * 0.001;
    
    particlesMesh.rotation.y += 0.5 * (targetX - particlesMesh.rotation.y);
    particlesMesh.rotation.x += 0.5 * (targetY - particlesMesh.rotation.x);

    // Subtle wave/breathing effect on Z axis
    particlesMesh.position.z = Math.sin(elapsedTime * 0.5) * 0.2;

    renderer.render(scene, camera);
}}

animate();

// Handle Window Resize
window.addEventListener('resize', () => {{
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
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
