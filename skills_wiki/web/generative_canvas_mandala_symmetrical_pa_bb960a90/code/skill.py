def create_component(
    output_dir: str,
    title_text: str = "Canvas Magic",
    body_text: str = "Generative mathematical animation using polar coordinates and symmetry.",
    color_scheme: str = "dark",        
    accent_color: str = "#00bfff",     
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    import os
    import html as html_lib

    os.makedirs(output_dir, exist_ok=True)

    # Escape HTML texts
    title_text_escaped = html_lib.escape(title_text)
    body_text_escaped = html_lib.escape(body_text)

    # Theme colors
    if color_scheme == "dark":
        bg_color = "#0d111c"
        text_color = "#f0f0f0"
        surface_color = "rgba(255, 255, 255, 0.08)"
        border_color = "rgba(255, 255, 255, 0.15)"
        is_dark_str = "true"
    else:
        bg_color = "#f8f9fa"
        text_color = "#1a1a2e"
        surface_color = "rgba(255, 255, 255, 0.6)"
        border_color = "rgba(0, 0, 0, 0.1)"
        is_dark_str = "false"

    css = f"""/* Generative Canvas Mandala Component */
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
    --border: {border_color};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background: #000; /* Outer page bg */
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
}}

.container {{
    width: var(--width);
    height: var(--height);
    background: var(--bg);
    position: relative;
    border-radius: 16px;
    overflow: hidden;
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
    display: flex;
    align-items: center;
    justify-content: center;
}}

#bg-canvas {{
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    z-index: 1;
    /* Prevent cursor interaction from breaking glass card */
    pointer-events: none; 
}}

.content-card {{
    position: relative;
    z-index: 2;
    background: var(--surface);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    padding: 3rem 4rem;
    border-radius: 20px;
    text-align: center;
    max-width: 80%;
    border: 1px solid var(--border);
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
    color: var(--text);
    /* Subtle pulsing glow around the card */
    animation: cardGlow 6s ease-in-out infinite alternate;
}}

@keyframes cardGlow {{
    0% {{ box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2), 0 0 0px var(--accent); }}
    100% {{ box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2), 0 0 40px var(--accent); }}
}}

.title {{
    font-size: 3rem;
    font-weight: 700;
    margin-bottom: 1rem;
    letter-spacing: -0.03em;
    background: linear-gradient(135deg, var(--text) 30%, var(--accent) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}}

.body-text {{
    font-size: 1.125rem;
    font-weight: 400;
    line-height: 1.6;
    opacity: 0.9;
    max-width: 500px;
    margin: 0 auto;
}}
"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text_escaped}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        <canvas id="bg-canvas"></canvas>
        <div class="content-card">
            <h1 class="title">{title_text_escaped}</h1>
            <p class="body-text">{body_text_escaped}</p>
        </div>
    </div>
    
    <!-- Config injected for JS -->
    <script>
        window.COMPONENT_CONFIG = {{
            accentHex: "{accent_color}",
            isDark: {is_dark_str}
        }};
    </script>
    <script src="script.js"></script>
</body>
</html>"""

    js = """// Generative Canvas Mandala Logic
document.addEventListener('DOMContentLoaded', () => {
    const canvas = document.getElementById('bg-canvas');
    const ctx = canvas.getContext('2d');
    const container = document.querySelector('.container');
    const config = window.COMPONENT_CONFIG;

    let width, height, cx, cy;
    const symmetry = 8; // Number of rotational copies (mandala effect)
    const particles = [];
    const numParticles = 80;

    // --- Helper: Convert Hex to HSL Hue ---
    function hexToHue(hex) {
        if(!hex) return 200;
        hex = hex.replace('#', '');
        if (hex.length === 3) hex = hex.split('').map(c => c+c).join('');
        let r = parseInt(hex.substring(0,2), 16) / 255 || 0;
        let g = parseInt(hex.substring(2,4), 16) / 255 || 0;
        let b = parseInt(hex.substring(4,6), 16) / 255 || 0;
        
        let max = Math.max(r, g, b), min = Math.min(r, g, b);
        let h = 0;
        if (max !== min) {
            let d = max - min;
            switch(max) {
                case r: h = (g - b) / d + (g < b ? 6 : 0); break;
                case g: h = (b - r) / d + 2; break;
                case b: h = (r - g) / d + 4; break;
            }
            h /= 6;
        }
        return h * 360;
    }

    const baseHue = hexToHue(config.accentHex);
    const particleLightness = config.isDark ? '60%' : '45%';
    const nodeLightness = config.isDark ? '75%' : '35%';
    
    // Determine fade color based on theme (0.12 opacity creates the trail length)
    const fadeColor = config.isDark 
        ? 'rgba(13, 17, 28, 0.12)' 
        : 'rgba(248, 249, 250, 0.12)';

    // --- Resize Logic ---
    function resize() {
        width = container.clientWidth;
        height = container.clientHeight;
        canvas.width = width;
        canvas.height = height;
        cx = width / 2;
        cy = height / 2;
    }
    window.addEventListener('resize', resize);
    resize();

    // --- Particle Class ---
    class Particle {
        constructor() {
            this.reset();
            // Stagger initial spawn times
            this.life = Math.random() * this.maxLife;
        }
        
        reset() {
            this.r = Math.random() * 30 + 10; // Start near center
            this.baseAngle = Math.random() * Math.PI * 2;
            this.speed = Math.random() * 1.5 + 0.5;
            this.freq = Math.random() * 0.04 + 0.01; // Wiggle frequency
            this.amp = Math.random() * 0.6;          // Wiggle amplitude
            this.size = Math.random() * 2.5 + 0.5;   // Line thickness
            this.hueOffset = Math.random() * 80 - 40; // Color variance
            this.life = 0;
            this.maxLife = Math.random() * 120 + 60;
            
            this.prevR = this.r;
            this.prevAngle = this.baseAngle;
            this.currentAngle = this.baseAngle;
        }
        
        update() {
            this.prevR = this.r;
            this.prevAngle = this.currentAngle;
            
            // Outward movement with slight acceleration
            this.r += this.speed;
            this.speed *= 1.015; 
            
            // Sine-wave wiggle on the angle
            this.currentAngle = this.baseAngle + Math.sin(this.life * this.freq) * this.amp;
            
            this.size *= 0.99; // Shrink as it travels
            this.life++;
            
            if (this.life >= this.maxLife || this.size < 0.1) {
                this.reset();
            }
        }
    }

    // Initialize particles
    for (let i = 0; i < numParticles; i++) {
        particles.push(new Particle());
    }

    // --- Animation Loop ---
    function draw() {
        // 1. Draw semi-transparent background to create motion trails
        ctx.fillStyle = fadeColor;
        ctx.fillRect(0, 0, width, height);
        
        // 2. Draw Particles (Symmetrical Burst)
        ctx.lineCap = 'round';
        particles.forEach(p => {
            p.update();
            
            ctx.strokeStyle = `hsl(${baseHue + p.hueOffset}, 85%, ${particleLightness})`;
            ctx.lineWidth = p.size;
            
            // Draw 'symmetry' number of copies rotated around center
            for(let i = 0; i < symmetry; i++) {
                const symOffset = (i * Math.PI * 2) / symmetry;
                
                const symAngle = p.currentAngle + symOffset;
                const prevSymAngle = p.prevAngle + symOffset;
                
                const x = cx + Math.cos(symAngle) * p.r;
                const y = cy + Math.sin(symAngle) * p.r;
                const px = cx + Math.cos(prevSymAngle) * p.prevR;
                const py = cy + Math.sin(prevSymAngle) * p.prevR;
                
                ctx.beginPath();
                ctx.moveTo(px, py);
                ctx.lineTo(x, y);
                ctx.stroke();
            }
        });
        
        // 3. Draw Inner Rotating Geometric Nodes
        const time = Date.now() * 0.0008;
        for(let ring = 1; ring <= 2; ring++) {
            const ringNodes = symmetry * ring;
            // Radius pulses slightly with time
            const ringRadius = 40 * ring + Math.sin(time * 2 + ring) * 8;
            
            ctx.fillStyle = `hsl(${baseHue + ring * 20}, 90%, ${nodeLightness})`;
            
            for(let i = 0; i < ringNodes; i++) {
                // Alternate rotation direction per ring
                const dir = ring % 2 === 0 ? 1 : -1;
                const angle = (time * dir) + (i * Math.PI * 2 / ringNodes);
                
                const x = cx + Math.cos(angle) * ringRadius;
                const y = cy + Math.sin(angle) * ringRadius;
                
                ctx.beginPath();
                ctx.arc(x, y, 3, 0, Math.PI * 2);
                ctx.fill();
            }
        }
        
        requestAnimationFrame(draw);
    }
    
    // Start animation
    draw();
});
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
