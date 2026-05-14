def create_component(
    output_dir: str,
    title_text: str = "Infinite Skies",
    body_text: str = "Look up. The universe is waiting.",
    color_scheme: str = "dark",
    accent_color: str = "#00bfff",
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Astrophotography Time-Lapse effect.
    
    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os
    import json

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors ===
    if color_scheme == "dark":
        sky_center = "#0b1021"
        sky_edge = "#050814"
        silhouette_color = "#020305"
        text_color = "#ffffff"
        text_shadow = "rgba(0,0,0,0.8)"
    else:
        # "Light" theme in this context acts as a twilight/sunset aesthetic
        sky_center = "#394168"
        sky_edge = "#1a1d2b"
        silhouette_color = "#0b0c10"
        text_color = "#f4f6ff"
        text_shadow = "rgba(0,0,0,0.5)"

    # Inject colors into JS config safely
    js_config = {
        "accent": accent_color,
        "silhouette": silhouette_color
    }

    # === CSS ===
    css = f"""/* Astrophotography Time-lapse — generated component */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --sky-center: {sky_center};
    --sky-edge: {sky_edge};
    --text: {text_color};
    --accent: {accent_color};
    --shadow: {text_shadow};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background: #000;
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 100vh;
}}

.time-lapse-container {{
    width: var(--width);
    height: var(--height);
    position: relative;
    overflow: hidden;
    background: radial-gradient(circle at center, var(--sky-center) 0%, var(--sky-edge) 100%);
    box-shadow: 0 24px 48px rgba(0,0,0,0.4);
    /* Soften the edges of the container for aesthetic presentation */
    border-radius: 12px; 
}}

/* Rotating Sky Layer */
.rotating-sky {{
    position: absolute;
    top: 50%;
    left: 50%;
    /* Width and height are dynamically set by JS to the diagonal length */
    transform: translate(-50%, -50%) rotate(0deg);
    animation: rotateSky 300s linear infinite;
    pointer-events: none;
    z-index: 2;
}}

@keyframes rotateSky {{
    0% {{ transform: translate(-50%, -50%) rotate(0deg); }}
    100% {{ transform: translate(-50%, -50%) rotate(360deg); }}
}}

/* Twinkling Layer Pulse */
.twinkle-layer {{
    animation: pulseTwinkle 5s ease-in-out infinite alternate;
}}

@keyframes pulseTwinkle {{
    0% {{ opacity: 0.2; }}
    100% {{ opacity: 0.9; }}
}}

/* Canvas stack */
canvas {{
    position: absolute;
    top: 0;
    left: 0;
    pointer-events: none;
}}

.layer-meteors {{
    z-index: 3;
}}

.layer-silhouettes {{
    z-index: 4;
}}

/* Content Overlay */
.content-overlay {{
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    z-index: 10;
    padding: 2rem;
    pointer-events: auto;
}}

.title {{
    font-size: 4rem;
    font-weight: 700;
    letter-spacing: -0.02em;
    color: var(--text);
    text-shadow: 0 4px 16px var(--shadow);
    margin-bottom: 1rem;
}}

.title span {{
    color: var(--accent);
    /* Subtle glow on the accent color */
    text-shadow: 0 0 20px var(--accent), 0 4px 16px var(--shadow);
}}

.body-text {{
    font-size: 1.25rem;
    font-weight: 400;
    color: rgba(255, 255, 255, 0.85);
    max-width: 600px;
    line-height: 1.6;
    text-shadow: 0 2px 8px var(--shadow);
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
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="time-lapse-container" id="tl-container">
        
        <!-- Rotating background: Nebulas and static stars -->
        <div class="rotating-sky" id="rotating-sky">
            <canvas id="cvs-milky-way"></canvas>
            <canvas id="cvs-stars-base"></canvas>
            <canvas id="cvs-stars-twinkle" class="twinkle-layer"></canvas>
        </div>

        <!-- High-speed overlay: Meteors -->
        <canvas id="cvs-meteors" class="layer-meteors"></canvas>

        <!-- Static foreground: Pine Trees -->
        <canvas id="cvs-silhouettes" class="layer-silhouettes"></canvas>

        <!-- Text Overlay -->
        <div class="content-overlay">
            <h1 class="title">{title_text.replace(title_text.split()[-1], f"<span>{title_text.split()[-1]}</span>") if " " in title_text else title_text}</h1>
            <p class="body-text">{body_text}</p>
        </div>

    </div>

    <!-- Pass configuration to JS -->
    <script id="config" type="application/json">
        {json.dumps(js_config)}
    </script>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = """// Astrophotography Time-Lapse Logic

document.addEventListener('DOMContentLoaded', () => {
    const config = JSON.parse(document.getElementById('config').textContent);
    
    const container = document.getElementById('tl-container');
    const rotatingSky = document.getElementById('rotating-sky');
    
    // Canvases
    const cvsMilkyWay = document.getElementById('cvs-milky-way');
    const cvsStarsBase = document.getElementById('cvs-stars-base');
    const cvsStarsTwinkle = document.getElementById('cvs-stars-twinkle');
    const cvsMeteors = document.getElementById('cvs-meteors');
    const cvsSilhouettes = document.getElementById('cvs-silhouettes');
    
    // Contexts
    const ctxMilkyWay = cvsMilkyWay.getContext('2d');
    const ctxStarsBase = cvsStarsBase.getContext('2d');
    const ctxStarsTwinkle = cvsStarsTwinkle.getContext('2d');
    const ctxMeteors = cvsMeteors.getContext('2d');
    const ctxSilhouettes = cvsSilhouettes.getContext('2d');

    let cw, ch, diagonal;
    let meteors = [];

    function initCanvases() {
        const rect = container.getBoundingClientRect();
        cw = rect.width;
        ch = rect.height;
        diagonal = Math.ceil(Math.sqrt(cw * cw + ch * ch));

        // Size rotating container and its canvases to the diagonal
        rotatingSky.style.width = `${diagonal}px`;
        rotatingSky.style.height = `${diagonal}px`;
        
        [cvsMilkyWay, cvsStarsBase, cvsStarsTwinkle].forEach(cvs => {
            cvs.width = diagonal;
            cvs.height = diagonal;
        });

        // Size static overlay canvases exactly to container
        [cvsMeteors, cvsSilhouettes].forEach(cvs => {
            cvs.width = cw;
            cvs.height = ch;
        });

        renderMilkyWay(ctxMilkyWay, diagonal, diagonal);
        renderStars(ctxStarsBase, diagonal, diagonal, 3000, 1.5, 0.1, 0.8);
        renderStars(ctxStarsTwinkle, diagonal, diagonal, 800, 2.5, 0.5, 1.0);
        renderSilhouettes(ctxSilhouettes, cw, ch);
    }

    // === Render Functions (One-time draws) ===

    function renderMilkyWay(ctx, w, h) {
        ctx.clearRect(0, 0, w, h);
        ctx.globalCompositeOperation = 'screen';
        
        const cx = w / 2;
        const cy = h / 2;
        
        // Draw sweeping elliptical gradient clouds
        const drawCloud = (x, y, r, colorStart, colorEnd) => {
            const grad = ctx.createRadialGradient(x, y, 0, x, y, r);
            grad.addColorStop(0, colorStart);
            grad.addColorStop(1, colorEnd);
            ctx.fillStyle = grad;
            ctx.beginPath();
            ctx.arc(x, y, r, 0, Math.PI * 2);
            ctx.fill();
        };

        // Create a loose band across the canvas
        for (let i = 0; i < 15; i++) {
            const offsetX = (Math.random() - 0.5) * (w * 0.8);
            const offsetY = (Math.random() - 0.5) * (h * 0.3); // Compressed y to form a band
            const radius = Math.random() * 300 + 150;
            
            // Mix of deep purples and blues
            const isPurple = Math.random() > 0.5;
            const cStart = isPurple ? 'rgba(62, 29, 74, 0.25)' : 'rgba(28, 40, 89, 0.25)';
            const cEnd = isPurple ? 'rgba(62, 29, 74, 0)' : 'rgba(28, 40, 89, 0)';
            
            drawCloud(cx + offsetX, cy + offsetY, radius, cStart, cEnd);
        }
    }

    function renderStars(ctx, w, h, count, maxRadius, minAlpha, maxAlpha) {
        ctx.clearRect(0, 0, w, h);
        for (let i = 0; i < count; i++) {
            const x = Math.random() * w;
            const y = Math.random() * h;
            const r = Math.random() * maxRadius;
            const alpha = minAlpha + Math.random() * (maxAlpha - minAlpha);
            
            ctx.beginPath();
            ctx.fillStyle = `rgba(255, 255, 255, ${alpha})`;
            ctx.arc(x, y, r, 0, Math.PI * 2);
            ctx.fill();
        }
    }

    function renderSilhouettes(ctx, w, h) {
        ctx.clearRect(0, 0, w, h);
        ctx.fillStyle = config.silhouette;

        // Function to draw a jagged pine tree shape pointing UP
        // Origin is at bottom center of the tree
        const drawPine = (x, y, width, height) => {
            ctx.save();
            ctx.translate(x, y);
            ctx.beginPath();
            ctx.moveTo(0, -height); // tip
            ctx.lineTo(-width/3, -height * 0.6);
            ctx.lineTo(-width/5, -height * 0.65);
            ctx.lineTo(-width/2, -height * 0.2);
            ctx.lineTo(-width/4, -height * 0.25);
            ctx.lineTo(-width/1.8, 0); // bottom left base
            ctx.lineTo(width/1.8, 0);  // bottom right base
            ctx.lineTo(width/4, -height * 0.25);
            ctx.lineTo(width/2, -height * 0.2);
            ctx.lineTo(width/5, -height * 0.65);
            ctx.lineTo(width/3, -height * 0.6);
            ctx.closePath();
            ctx.fill();
            ctx.restore();
        };

        const drawEdge = (length, depth, angle, originX, originY) => {
            ctx.save();
            ctx.translate(originX, originY);
            ctx.rotate(angle);
            
            // Draw a base rect to ensure no gaps at the edge
            ctx.fillRect(0, 0, length, depth * 0.3);
            
            // Populate trees along the edge
            const treeCount = Math.floor(length / 20);
            for (let i = 0; i < treeCount; i++) {
                const x = (i * 20) + (Math.random() * 15 - 7.5);
                const treeW = 30 + Math.random() * 40;
                const treeH = depth * 0.5 + Math.random() * (depth * 0.8);
                // Draw pointing inwards (y goes negative relative to rotated edge)
                drawPine(x, depth * 0.2, treeW, treeH);
            }
            ctx.restore();
        };

        const depth = Math.min(w, h) * 0.25; // How far trees reach into the screen

        // Bottom edge (trees point up, so angle 0, origin bottom left)
        drawEdge(w, depth, 0, 0, h - depth*0.2);
        
        // Top edge (trees point down, angle PI, origin top right)
        drawEdge(w, depth, Math.PI, w, depth*0.2);
        
        // Left edge (trees point right, angle Math.PI/2, origin top left)
        drawEdge(h, depth, Math.PI / 2, depth*0.2, 0);
        
        // Right edge (trees point left, angle -Math.PI/2, origin bottom right)
        drawEdge(h, depth, -Math.PI / 2, w - depth*0.2, h);
    }

    // === Animation Loop (Meteors) ===

    class Meteor {
        constructor(w, h) {
            this.w = w;
            this.h = h;
            this.reset();
        }
        
        reset() {
            // Start somewhere in the top half
            this.x = Math.random() * this.w * 1.5;
            this.y = Math.random() * this.h * 0.5 - this.h * 0.2;
            
            this.length = 50 + Math.random() * 150;
            this.speed = 15 + Math.random() * 20;
            // Angle moving down and left
            this.angle = Math.PI * 0.2 + Math.random() * 0.1; 
            
            this.opacity = 0;
            this.state = 'fade_in'; // fade_in, active, fade_out
            this.life = 0;
            this.maxLife = 20 + Math.random() * 40;
        }

        update() {
            this.x -= Math.cos(this.angle) * this.speed;
            this.y += Math.sin(this.angle) * this.speed;
            
            this.life++;
            
            if (this.state === 'fade_in') {
                this.opacity += 0.1;
                if (this.opacity >= 1) this.state = 'active';
            } else if (this.state === 'active') {
                if (this.life > this.maxLife * 0.6) this.state = 'fade_out';
            } else if (this.state === 'fade_out') {
                this.opacity -= 0.05;
            }
            
            if (this.opacity <= 0 || this.y > this.h || this.x < 0) {
                return false; // dead
            }
            return true; // alive
        }

        draw(ctx) {
            const tailX = this.x + Math.cos(this.angle) * this.length;
            const tailY = this.y - Math.sin(this.angle) * this.length;
            
            const grad = ctx.createLinearGradient(this.x, this.y, tailX, tailY);
            grad.addColorStop(0, `rgba(255, 255, 255, ${this.opacity})`);
            grad.addColorStop(0.1, `rgba(180, 220, 255, ${this.opacity * 0.8})`);
            grad.addColorStop(1, `rgba(255, 255, 255, 0)`);
            
            ctx.beginPath();
            ctx.strokeStyle = grad;
            ctx.lineWidth = 2;
            ctx.lineCap = 'round';
            ctx.moveTo(this.x, this.y);
            ctx.lineTo(tailX, tailY);
            ctx.stroke();
            
            // Tiny glow at the head
            ctx.beginPath();
            ctx.fillStyle = `rgba(255, 255, 255, ${this.opacity})`;
            ctx.arc(this.x, this.y, 1.5, 0, Math.PI*2);
            ctx.fill();
        }
    }

    function animateMeteors() {
        ctxMeteors.clearRect(0, 0, cw, ch);
        
        // Randomly spawn a meteor
        if (Math.random() < 0.015 && meteors.length < 3) {
            meteors.push(new Meteor(cw, ch));
        }
        
        for (let i = meteors.length - 1; i >= 0; i--) {
            const isAlive = meteors[i].update();
            if (isAlive) {
                meteors[i].draw(ctxMeteors);
            } else {
                meteors.splice(i, 1);
            }
        }
        
        requestAnimationFrame(animateMeteors);
    }

    // Initialize
    initCanvases();
    animateMeteors();

    // Resize handler (debounce recommended for production, kept simple here)
    window.addEventListener('resize', () => {
        initCanvases();
    });
});
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
