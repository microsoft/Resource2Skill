def create_component(
    output_dir: str,
    title_text: str = "Background Animation",
    body_text: str = "",
    color_scheme: str = "dark",
    accent_color: str = "#ffffff",
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Prime-Distributed DOM Particle Field effect.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Theme colors based on selection
    if color_scheme == "dark":
        bg_color = "#141516"
        text_color = "#ffffff"
        palette = ["#ff9800", "#ffeb3b", "#2196f3", "#f44336", "#4caf50", "#9c27b0"]
    else:
        bg_color = "#f0f2f5"
        text_color = "#1a1a2e"
        palette = ["#fb8c00", "#fdd835", "#1e88e5", "#e53935", "#43a047", "#8e24aa"]

    css = f"""/* Prime-Distributed DOM Particle Field */
@import url('https://fonts.googleapis.com/css2?family=Concert+One&family=Inter:wght@400;500&display=swap');

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
    background: var(--bg);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    font-family: 'Inter', sans-serif;
}}

.container {{
    width: var(--width);
    height: var(--height);
    position: relative;
    background: var(--bg);
    overflow: hidden;
    border-radius: 12px;
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
}}

.circles-container {{
    position: absolute;
    inset: 0;
    z-index: 1;
    pointer-events: none;
}}

/* Particle Base Styles */
.circles-container span {{
    position: absolute;
    top: 0;
    left: 0;
    width: 35px;
    aspect-ratio: 1 / 1;
    border-radius: 50%;
    opacity: 0.6;
    background-color: {palette[0]}; /* Fallback */
    will-change: transform;
}}

/* The Magic: Prime-Number Color Distribution */
.circles-container span:nth-child(2n)  {{ background-color: {palette[0]}; }}
.circles-container span:nth-child(3n)  {{ background-color: {palette[1]}; }}
.circles-container span:nth-child(5n)  {{ background-color: {palette[2]}; }}
.circles-container span:nth-child(7n)  {{ background-color: {palette[3]}; }}
.circles-container span:nth-child(11n) {{ background-color: {palette[4]}; }}
.circles-container span:nth-child(13n) {{ background-color: {palette[5]}; }}

/* Typography Overlay */
.content-overlay {{
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    z-index: 2;
    text-align: center;
    width: 100%;
    padding: 0 20px;
    pointer-events: none;
}}

h1.title {{
    font-family: 'Concert One', sans-serif;
    font-size: clamp(3rem, 6vw, 5rem);
    letter-spacing: 3px;
    color: transparent;
    -webkit-text-stroke: 2px var(--accent);
    text-stroke: 2px var(--accent);
    margin-bottom: 1rem;
    user-select: none;
}}

p.body-text {{
    font-size: 1.25rem;
    color: var(--text);
    opacity: 0.8;
    max-width: 600px;
    margin: 0 auto;
}}
"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text}</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        <!-- Particle Container -->
        <div class="circles-container"></div>
        
        <!-- Content Layer -->
        <div class="content-overlay">
            <h1 class="title">{title_text}</h1>
            <p class="body-text">{body_text}</p>
        </div>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    js = """document.addEventListener('DOMContentLoaded', () => {
    const container = document.querySelector('.container');
    const circlesContainer = document.querySelector('.circles-container');
    
    const NUM_PARTICLES = 200;
    const SPEED_MULTIPLIER = 1;
    const PARTICLE_SIZE = 35; // Matches CSS width
    const particles = [];

    class Particle {
        constructor() {
            this.span = document.createElement('span');
            
            // Random initial placement within container bounds
            this.x = Math.random() * (container.clientWidth - PARTICLE_SIZE);
            this.y = Math.random() * (container.clientHeight - PARTICLE_SIZE);
            
            // Random velocity vectors
            this.speedX = (Math.random() - 0.5) * 2 * SPEED_MULTIPLIER;
            this.speedY = (Math.random() - 0.5) * 2 * SPEED_MULTIPLIER;
            
            // Set initial position
            this.span.style.transform = `translate(${this.x}px, ${this.y}px)`;
            circlesContainer.appendChild(this.span);
        }

        update() {
            this.x += this.speedX;
            this.y += this.speedY;

            // Bounding box collision detection
            if (this.x <= 0 || this.x >= container.clientWidth - PARTICLE_SIZE) {
                this.speedX *= -1;
                // Clamp to prevent getting stuck
                this.x = Math.max(0, Math.min(this.x, container.clientWidth - PARTICLE_SIZE));
            }
            if (this.y <= 0 || this.y >= container.clientHeight - PARTICLE_SIZE) {
                this.speedY *= -1;
                // Clamp to prevent getting stuck
                this.y = Math.max(0, Math.min(this.y, container.clientHeight - PARTICLE_SIZE));
            }

            // Using translate instead of top/left for GPU acceleration
            this.span.style.transform = `translate(${this.x}px, ${this.y}px)`;
        }
        
        handleResize() {
            // Keep particles inside if container shrinks
            if (this.x > container.clientWidth - PARTICLE_SIZE) {
                this.x = container.clientWidth - PARTICLE_SIZE;
            }
            if (this.y > container.clientHeight - PARTICLE_SIZE) {
                this.y = container.clientHeight - PARTICLE_SIZE;
            }
        }
    }

    // Initialize particles
    function init() {
        for (let i = 0; i < NUM_PARTICLES; i++) {
            particles.push(new Particle());
        }
    }

    // Main animation loop
    function animate() {
        particles.forEach(particle => particle.update());
        requestAnimationFrame(animate);
    }

    // Handle container/window resizes
    window.addEventListener('resize', () => {
        particles.forEach(particle => particle.handleResize());
    });

    init();
    animate();
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
