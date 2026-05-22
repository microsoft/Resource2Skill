def create_component(
    output_dir: str,
    title_text: str = "One unified workspace",
    body_text: str = "Build, test, and ship faster.",
    color_scheme: str = "dark",
    accent_color: str = "#ffffff",
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Creates a Scroll-Driven Canvas Image Sequence component.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    if color_scheme == "dark":
        bg_color = "#0d111c"
        text_color = "#f0f0f0"
        nav_bg = "rgba(13, 17, 28, 0.8)"
    else:
        bg_color = "#f8f9fa"
        text_color = "#1a1a2e"
        nav_bg = "rgba(248, 249, 250, 0.8)"

    css = f"""/* Base Resets */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --text: {text_color};
    --accent: {accent_color};
    --nav-bg: {nav_bg};
}}

body {{
    font-family: 'Inter', system-ui, sans-serif;
    background-color: var(--bg);
    color: var(--text);
    overflow-x: hidden;
    -webkit-font-smoothing: antialiased;
}}

/* Navigation */
nav {{
    position: fixed;
    top: 0;
    width: 100%;
    padding: 1.5rem 2rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    z-index: 100;
    background: var(--nav-bg);
    backdrop-filter: blur(10px);
    will-change: opacity, transform;
}}

.nav-logo {{
    font-weight: 700;
    letter-spacing: 1px;
    font-size: 1.2rem;
}}

/* Hero Section */
.hero {{
    position: relative;
    width: 100vw;
    height: 100vh;
    overflow: hidden;
}}

/* The Canvas */
canvas {{
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    z-index: 1;
}}

/* Overlay 3D Content */
.hero-content {{
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    z-index: 2;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    /* Crucial for 3D receding effect */
    perspective: 1000px;
    transform-style: preserve-3d;
    pointer-events: none;
}}

.header-container {{
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
    will-change: transform, opacity;
}}

.header-container h1 {{
    font-size: clamp(3rem, 5vw, 5rem);
    font-weight: 400;
    line-height: 1.1;
    max-width: 800px;
    margin-bottom: 1rem;
}}

.header-container p {{
    font-size: 1rem;
    text-transform: uppercase;
    letter-spacing: 2px;
    opacity: 0.6;
    font-weight: 500;
}}

/* Outro Section for scrolling space */
.outro {{
    height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    background: var(--bg);
    position: relative;
    z-index: 10;
}}

.outro h2 {{
    font-size: 3rem;
    font-weight: 300;
}}

/* Preloader Overlay */
#preloader {{
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    background: var(--bg);
    color: var(--text);
    z-index: 9999;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.5rem;
    transition: opacity 0.5s ease;
}}
"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text}</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
    
    <!-- Dependencies -->
    <script src="https://unpkg.com/@studio-freight/lenis@1.0.34/dist/lenis.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/gsap.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/ScrollTrigger.min.js"></script>
</head>
<body>
    <div id="preloader">Generating sequence frames... 0%</div>

    <nav class="navbar">
        <div class="nav-logo">SYSTEM</div>
        <div>Overview | Specs</div>
    </nav>

    <section class="hero">
        <canvas id="sequence-canvas"></canvas>
        <div class="hero-content">
            <div class="header-container">
                <h1>{title_text}</h1>
                <p>{body_text}</p>
            </div>
        </div>
    </section>

    <section class="outro">
        <h2>Keep Exploring</h2>
    </section>

    <script src="script.js"></script>
</body>
</html>"""

    js = """// Register GSAP Plugin
gsap.registerPlugin(ScrollTrigger);

// 1. Setup Smooth Scrolling (Lenis)
const lenis = new Lenis({
    duration: 1.2,
    easing: (t) => Math.min(1, 1.001 - Math.pow(2, -10 * t)),
    smooth: true,
});

function raf(time) {
    lenis.raf(time);
    requestAnimationFrame(raf);
}
requestAnimationFrame(raf);

// Connect Lenis to GSAP ScrollTrigger
lenis.on('scroll', ScrollTrigger.update);
gsap.ticker.add((time) => { lenis.raf(time * 1000); });
gsap.ticker.lagSmoothing(0);

// 2. DOM Elements
const canvas = document.getElementById('sequence-canvas');
const context = canvas.getContext('2d');
const preloader = document.getElementById('preloader');
const heroSection = document.querySelector('.hero');
const headerContainer = document.querySelector('.header-container');
const navbar = document.querySelector('.navbar');

// 3. Frame Generation (Simulating a downloaded image sequence)
// In a real project, you would load URLs. Here, we generate them to be self-contained.
const frameCount = 120;
const images = [];
let loadedCount = 0;

function generateFrames() {
    const tempCanvas = document.createElement('canvas');
    tempCanvas.width = 1280;
    tempCanvas.height = 720;
    const ctx = tempCanvas.getContext('2d');

    for (let i = 0; i < frameCount; i++) {
        // Draw a simulated 3D terrain/gradient landscape moving
        ctx.fillStyle = '#0d111c';
        ctx.fillRect(0, 0, tempCanvas.width, tempCanvas.height);
        
        const progress = i / frameCount;
        
        // Dynamic "Sun" or light source
        const grad = ctx.createRadialGradient(
            tempCanvas.width * 0.5, tempCanvas.height * (0.8 + progress * 0.5), 50,
            tempCanvas.width * 0.5, tempCanvas.height * (0.8 + progress * 0.5), 800
        );
        grad.addColorStop(0, '#ff6a00');
        grad.addColorStop(1, 'transparent');
        ctx.fillStyle = grad;
        ctx.fillRect(0, 0, tempCanvas.width, tempCanvas.height);

        // Simulated grid/terrain moving towards camera
        ctx.strokeStyle = `rgba(255, 255, 255, ${0.1 + progress * 0.2})`;
        ctx.lineWidth = 2;
        ctx.beginPath();
        for(let x = -500; x <= tempCanvas.width + 500; x += 100) {
            ctx.moveTo(tempCanvas.width / 2, tempCanvas.height * 0.4);
            // shift perspective based on progress
            ctx.lineTo(x + (progress * 200), tempCanvas.height); 
        }
        for(let y = tempCanvas.height * 0.4; y <= tempCanvas.height; y += Math.pow(y * 0.05, 1.2)) {
            // Move horizontal lines down based on progress to simulate forward motion
            let offset = (progress * 100) % 50; 
            ctx.moveTo(0, y + offset);
            ctx.lineTo(tempCanvas.width, y + offset);
        }
        ctx.stroke();

        // Save frame to image object
        const img = new Image();
        img.src = tempCanvas.toDataURL('image/jpeg', 0.6);
        img.onload = () => {
            loadedCount++;
            preloader.innerText = `Loading sequence... Math.round((loadedCount / frameCount) * 100)%`;
            if (loadedCount === frameCount) {
                initAnimation();
            }
        };
        images.push(img);
    }
}

// 4. Canvas Resizing and "Object-Fit: Cover" Logic
function resizeCanvas() {
    const pixelRatio = window.devicePixelRatio || 1;
    canvas.width = window.innerWidth * pixelRatio;
    canvas.height = window.innerHeight * pixelRatio;
    canvas.style.width = `${window.innerWidth}px`;
    canvas.style.height = `${window.innerHeight}px`;
    context.scale(pixelRatio, pixelRatio);
    renderFrame(state.frame);
}

const state = { frame: 0 };

function renderFrame(index) {
    if (!images[index]) return;
    const img = images[index];
    
    // Clear canvas
    context.clearRect(0, 0, canvas.width, canvas.height);
    
    // Object-fit: cover math
    const canvasAspect = window.innerWidth / window.innerHeight;
    const imgAspect = img.width / img.height;
    
    let drawWidth, drawHeight, drawX, drawY;
    
    if (imgAspect > canvasAspect) {
        // Image is wider than canvas
        drawHeight = window.innerHeight;
        drawWidth = drawHeight * imgAspect;
        drawX = (window.innerWidth - drawWidth) / 2;
        drawY = 0;
    } else {
        // Image is taller than canvas
        drawWidth = window.innerWidth;
        drawHeight = drawWidth / imgAspect;
        drawX = 0;
        drawY = (window.innerHeight - drawHeight) / 2;
    }
    
    context.drawImage(img, drawX, drawY, drawWidth, drawHeight);
}

// 5. GSAP Animation Initialization
function initAnimation() {
    // Hide preloader
    preloader.style.opacity = '0';
    setTimeout(() => preloader.remove(), 500);

    window.addEventListener('resize', resizeCanvas);
    resizeCanvas(); // initial draw

    // The core scroll sequence
    ScrollTrigger.create({
        trigger: heroSection,
        start: "top top",
        end: "+=500%", // Pin for 5x window height
        pin: true,
        scrub: 0.5,    // Smooth scrubbing
        onUpdate: (self) => {
            // 1. Map scroll progress to frame array
            const progress = self.progress;
            const targetFrame = Math.floor(progress * (frameCount - 1));
            
            // Draw corresponding frame
            if (state.frame !== targetFrame) {
                state.frame = targetFrame;
                renderFrame(state.frame);
            }

            // 2. Animate 3D Text (Fading and moving backwards)
            // Push it back up to 800px on the Z axis
            const zMovement = -progress * 800; 
            const textOpacity = 1 - (progress * 2); // Fade out twice as fast
            
            gsap.set(headerContainer, {
                transform: `translateZ(${zMovement}px)`,
                opacity: Math.max(0, textOpacity)
            });

            // 3. Fade out Nav bar slightly later
            const navOpacity = 1 - (progress * 4);
            gsap.set(navbar, {
                transform: `translateY(${-progress * 100}px)`,
                opacity: Math.max(0, navOpacity)
            });
        }
    });
}

// Start generating the fake video sequence
generateFrames();
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
