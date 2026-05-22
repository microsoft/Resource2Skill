def create_component(
    output_dir: str,
    title_text: str = "Procedural Entity",
    body_text: str = "Rendered via 15,000 mathematically positioned particles per frame.",
    color_scheme: str = "dark",
    accent_color: str = "#0ea5e9",
    width_px: int = 1000,
    height_px: int = 700,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Procedural Particle Entity Animation.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Theme definitions
    if color_scheme == "dark":
        bg_gradient = "linear-gradient(135deg, #0f1322, #1f253d)"
        surface = "rgba(15, 23, 42, 0.4)"
        border = "rgba(255, 255, 255, 0.08)"
        text_primary = "#f8fafc"
        text_secondary = "#94a3b8"
        btn_bg = "rgba(255, 255, 255, 0.05)"
        btn_hover = "rgba(255, 255, 255, 0.15)"
        badge_bg = "rgba(0, 0, 0, 0.6)"
    else:
        bg_gradient = "linear-gradient(135deg, #f8fafc, #e2e8f0)"
        surface = "rgba(255, 255, 255, 0.6)"
        border = "rgba(0, 0, 0, 0.08)"
        text_primary = "#0f172a"
        text_secondary = "#64748b"
        btn_bg = "rgba(0, 0, 0, 0.03)"
        btn_hover = "rgba(0, 0, 0, 0.08)"
        badge_bg = "rgba(255, 255, 255, 0.8)"

    # === CSS ===
    css = f"""/* Procedural Particle Entity Component */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg-gradient: {bg_gradient};
    --surface: {surface};
    --border: {border};
    --text-primary: {text_primary};
    --text-secondary: {text_secondary};
    --accent: {accent_color};
    --btn-bg: {btn_bg};
    --btn-hover: {btn_hover};
    --badge-bg: {badge_bg};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background: var(--bg-gradient);
    color: var(--text-primary);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 20px;
}}

.app-container {{
    width: 100%;
    max-width: var(--width);
    height: var(--height);
    max-height: 90vh;
    display: flex;
    flex-direction: column;
    gap: 20px;
}}

.header {{
    text-align: center;
}}

.title {{
    font-size: 2.25rem;
    font-weight: 700;
    letter-spacing: -0.5px;
    margin-bottom: 0.5rem;
}}

.subtitle {{
    font-size: 1rem;
    color: var(--text-secondary);
    font-weight: 400;
}}

.controls {{
    display: flex;
    gap: 12px;
    justify-content: center;
    margin-top: 16px;
}}

button {{
    background: var(--btn-bg);
    border: 1px solid var(--border);
    color: var(--text-primary);
    padding: 10px 24px;
    border-radius: 8px;
    cursor: pointer;
    font-size: 0.95rem;
    font-weight: 500;
    transition: all 0.2s ease;
    backdrop-filter: blur(4px);
}}

button:hover {{
    background: var(--btn-hover);
    border-color: var(--accent);
    transform: translateY(-1px);
}}

.canvas-wrapper {{
    flex-grow: 1;
    position: relative;
    border-radius: 20px;
    background: var(--surface);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    border: 1px solid var(--border);
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
    overflow: hidden;
}}

canvas {{
    display: block;
    width: 100%;
    height: 100%;
}}

.stats-badge {{
    position: absolute;
    bottom: 20px;
    left: 20px;
    background: var(--badge-bg);
    color: var(--text-primary);
    padding: 8px 16px;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 0.5px;
    border: 1px solid var(--border);
    pointer-events: none;
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
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="app-container">
        <header class="header">
            <h1 class="title">{title_text}</h1>
            <p class="subtitle">{body_text}</p>
            <div class="controls">
                <button id="pauseBtn">Pause Animation</button>
                <button id="resetBtn">Reset Position</button>
            </div>
        </header>
        
        <main class="canvas-wrapper">
            <canvas id="entityCanvas"></canvas>
            <div class="stats-badge">15,000 Particles / Frame</div>
        </main>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = """// Procedural Shape Rendering System
class ParticleEntity {
    constructor(canvas, accentColor) {
        this.canvas = canvas;
        this.ctx = canvas.getContext('2d', { alpha: true });
        this.accentColor = accentColor;
        this.particlesPerFrame = 15000;
        
        // State
        this.x = -200;
        this.y = 0; // Updated on resize
        this.wingAngle = 0;
        this.isPaused = false;
        
        // Parse themes
        this.initColors();
        this.resize();
    }

    initColors() {
        // Generate a palette derived from the accent color
        this.colors = {
            body: this.adjustColor(this.accentColor, 0),
            head: this.adjustColor(this.accentColor, 0.15), // lighter
            tail: this.adjustColor(this.accentColor, -0.2), // darker
            wingFront: this.adjustColor(this.accentColor, -0.1),
            wingBack: this.adjustColor(this.accentColor, -0.3), // deepest
            beak: [255, 140, 0], // Fixed orange
            eye: [26, 26, 26]    // Fixed near-black
        };
    }

    adjustColor(hex, percent) {
        // Expand shorthand if needed
        if (hex.length === 4) {
            hex = '#' + hex[1]+hex[1] + hex[2]+hex[2] + hex[3]+hex[3];
        }
        let r = parseInt(hex.slice(1, 3), 16);
        let g = parseInt(hex.slice(3, 5), 16);
        let b = parseInt(hex.slice(5, 7), 16);

        // Mix with white (>0) or black (<0)
        if (percent > 0) {
            r += (255 - r) * percent;
            g += (255 - g) * percent;
            b += (255 - b) * percent;
        } else if (percent < 0) {
            r += r * percent;
            g += g * percent;
            b += b * percent;
        }
        return [Math.round(r), Math.round(g), Math.round(b)];
    }

    resize() {
        // Handle high-DPI displays for crisp rendering
        const dpr = window.devicePixelRatio || 1;
        const rect = this.canvas.parentElement.getBoundingClientRect();
        
        this.w = rect.width;
        this.h = rect.height;
        
        this.canvas.width = this.w * dpr;
        this.canvas.height = this.h * dpr;
        
        this.ctx.scale(dpr, dpr);
        this.y = this.h / 2;
    }

    // Mathematical bounding functions
    inCircle(x, y, cx, cy, r) { 
        return (x - cx) ** 2 + (y - cy) ** 2 <= r ** 2; 
    }
    
    inEllipse(x, y, cx, cy, rx, ry) { 
        if (rx === 0 || ry === 0) return false;
        return ((x - cx) ** 2) / (rx ** 2) + ((y - cy) ** 2) / (ry ** 2) <= 1; 
    }
    
    sign(p1x, p1y, p2x, p2y, p3x, p3y) {
        return (p1x - p3x) * (p2y - p3y) - (p2x - p3x) * (p1y - p3y);
    }
    
    inTriangle(px, py, x1, y1, x2, y2, x3, y3) {
        let d1 = this.sign(px, py, x1, y1, x2, y2);
        let d2 = this.sign(px, py, x2, y2, x3, y3);
        let d3 = this.sign(px, py, x3, y3, x1, y1);
        let hasNeg = (d1 < 0) || (d2 < 0) || (d3 < 0);
        let hasPos = (d1 > 0) || (d2 > 0) || (d3 > 0);
        return !(hasNeg && hasPos);
    }

    drawFrame() {
        if (this.isPaused) return;

        // 1. Trail Effect (Fade existing pixels instead of full clear)
        this.ctx.globalCompositeOperation = 'destination-out';
        this.ctx.fillStyle = 'rgba(255, 255, 255, 0.15)'; // 15% fade per frame
        this.ctx.fillRect(0, 0, this.w, this.h);

        // 2. State Updates
        this.ctx.globalCompositeOperation = 'source-over';
        this.x += 2.5; // Flight speed
        if (this.x > this.w + 200) {
            this.x = -200;
            this.y = 100 + Math.random() * (this.h - 200);
        }
        this.wingAngle += 0.12; // Flap speed

        // Dynamic wing parameters (creates fake 3D flap)
        const w1ry = 10 + 65 * Math.abs(Math.sin(this.wingAngle));
        const w2ry = 10 + 65 * Math.abs(Math.sin(this.wingAngle + Math.PI / 2));

        let drawn = 0;
        let attempts = 0;
        const maxAttempts = this.particlesPerFrame * 4;

        // 3. Monte Carlo Particle Rendering
        while (drawn < this.particlesPerFrame && attempts < maxAttempts) {
            attempts++;
            
            // Random point within local bounding box
            const lx = (Math.random() - 0.5) * 400; 
            const ly = (Math.random() - 0.5) * 300; 

            let part = null;

            // Z-Order Hit Testing (Top to Bottom visually)
            if (this.inCircle(lx, ly, 115, -40, 6)) part = 'eye';
            else if (this.inTriangle(lx, ly, 130, -35, 130, -15, 170, -25)) part = 'beak';
            else if (this.inCircle(lx, ly, 100, -30, 45)) part = 'head';
            else if (this.inEllipse(lx, ly, -10, 0, 80, w1ry)) part = 'wingFront';
            else if (this.inEllipse(lx, ly, 0, 0, 120, 70)) part = 'body';
            else if (this.inTriangle(lx, ly, -100, 0, -170, -30, -170, 30)) part = 'tail';
            else if (this.inEllipse(lx, ly, -10, 0, 80, w2ry)) part = 'wingBack';

            if (part) {
                const baseCol = this.colors[part];
                
                // Add texture noise
                const variation = (Math.random() - 0.5) * 20;
                const r = Math.min(255, Math.max(0, baseCol[0] + variation)) | 0;
                const g = Math.min(255, Math.max(0, baseCol[1] + variation)) | 0;
                const b = Math.min(255, Math.max(0, baseCol[2] + variation)) | 0;

                const size = Math.random() * 1.5 + 0.5;

                this.ctx.fillStyle = `rgba(${r}, ${g}, ${b}, 0.85)`;
                this.ctx.beginPath();
                this.ctx.arc(this.x + lx, this.y + ly, size, 0, 6.28);
                this.ctx.fill();
                drawn++;
            }
        }
    }
}

// App Initialization
document.addEventListener('DOMContentLoaded', () => {
    const canvas = document.getElementById('entityCanvas');
    const pauseBtn = document.getElementById('pauseBtn');
    const resetBtn = document.getElementById('resetBtn');

    // Initialize with injected python variable
    const entity = new ParticleEntity(canvas, 'ACCENT_COLOR_VAR');

    // Animation Loop
    function animate() {
        entity.drawFrame();
        requestAnimationFrame(animate);
    }
    requestAnimationFrame(animate);

    // Event Listeners
    pauseBtn.addEventListener('click', () => {
        entity.isPaused = !entity.isPaused;
        pauseBtn.textContent = entity.isPaused ? 'Resume Animation' : 'Pause Animation';
    });

    resetBtn.addEventListener('click', () => {
        entity.x = -200;
        entity.y = entity.h / 2;
        entity.wingAngle = 0;
        entity.ctx.clearRect(0, 0, entity.w, entity.h);
        if (entity.isPaused) entity.drawFrame();
    });

    window.addEventListener('resize', () => {
        entity.resize();
    });
});
""".replace('ACCENT_COLOR_VAR', accent_color)

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
