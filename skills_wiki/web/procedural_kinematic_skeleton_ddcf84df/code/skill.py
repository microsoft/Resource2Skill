def create_component(
    output_dir: str,
    title_text: str = "",
    body_text: str = "",
    color_scheme: str = "dark",
    accent_color: str = "#00ffcc",
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    import os

    os.makedirs(output_dir, exist_ok=True)

    if color_scheme == "dark":
        bg_color = "#0a0b10"
        line_color = "#ffffff"
        glow_color = accent_color
    else:
        bg_color = "#f4f4f5"
        line_color = "#111111"
        glow_color = accent_color

    css = f"""/* Procedural Kinematic Skeleton */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    background-color: var(--bg);
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 100vh;
    overflow: hidden;
    font-family: sans-serif;
}}

.canvas-container {{
    width: var(--width);
    height: var(--height);
    max-width: 100vw;
    max-height: 100vh;
    position: relative;
    background: var(--bg);
    box-shadow: 0 0 50px rgba(0,0,0,0.5);
    border-radius: 8px;
    overflow: hidden;
    cursor: crosshair;
}}

canvas {{
    display: block;
    width: 100%;
    height: 100%;
}}

.overlay {{
    position: absolute;
    top: 2rem;
    left: 2rem;
    color: {line_color};
    pointer-events: none;
    opacity: 0.7;
}}
"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Procedural Skeleton</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="canvas-container">
        <canvas id="creatureCanvas"></canvas>
        <div class="overlay">
            <h1 style="font-size: 1.5rem; letter-spacing: 2px;">{title_text}</h1>
            <p style="font-size: 0.9rem; margin-top: 0.5rem;">{body_text}</p>
        </div>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    js = f"""// Kinematic Procedural Skeleton Logic
document.addEventListener('DOMContentLoaded', () => {{
    const canvas = document.getElementById('creatureCanvas');
    const ctx = canvas.getContext('2d');
    const container = canvas.parentElement;

    // Configuration
    const ACCENT_COLOR = "{glow_color}";
    const LINE_COLOR = "{line_color}";
    
    let width, height;
    let mouseX = window.innerWidth / 2;
    let mouseY = window.innerHeight / 2;
    let targetX = mouseX;
    let targetY = mouseY;

    // --- Core Kinematic Logic ---

    class Segment {{
        constructor(x, y, length) {{
            this.x = x;
            this.y = y;
            this.length = length;
            this.angle = 0;
        }}

        // Make this segment follow a target x,y
        follow(tx, ty) {{
            const dx = tx - this.x;
            const dy = ty - this.y;
            this.angle = Math.atan2(dy, dx);
            this.x = tx - Math.cos(this.angle) * this.length;
            this.y = ty - Math.sin(this.angle) * this.length;
        }}
    }}

    class Leg {{
        constructor(attachIndex, side, reach) {{
            this.attachIndex = attachIndex; // which spine segment it connects to
            this.side = side;               // 1 for right, -1 for left
            this.reach = reach;             // max distance before stepping
            
            this.foot = {{ x: 0, y: 0 }};
            this.startFoot = {{ x: 0, y: 0 }};
            this.isStepping = false;
            this.stepRatio = 0;
            this.stepSpeed = 0.15;
        }}

        update(spine) {{
            const node = spine[this.attachIndex];
            if (!node) return;

            // Calculate ideal target position relative to spine segment
            const targetAngle = node.angle + (Math.PI / 2.5) * this.side;
            const idealX = node.x + Math.cos(targetAngle) * this.reach;
            const idealY = node.y + Math.sin(targetAngle) * this.reach;

            const dist = Math.hypot(this.foot.x - idealX, this.foot.y - idealY);

            // Trigger step if foot drags too far from ideal position
            if (!this.isStepping && dist > this.reach * 1.2) {{
                this.isStepping = true;
                this.stepRatio = 0;
                this.startFoot = {{ x: this.foot.x, y: this.foot.y }};
            }}

            // Animate step
            if (this.isStepping) {{
                this.stepRatio += this.stepSpeed;
                if (this.stepRatio >= 1) {{
                    this.stepRatio = 1;
                    this.isStepping = false;
                }}
                
                // Interpolate position
                this.foot.x = this.startFoot.x + (idealX - this.startFoot.x) * this.stepRatio;
                this.foot.y = this.startFoot.y + (idealY - this.startFoot.y) * this.stepRatio;
            }}

            // Draw Leg (2-bone IK simplified)
            const midX = (node.x + this.foot.x) / 2;
            const midY = (node.y + this.foot.y) / 2;
            const dX = this.foot.x - node.x;
            const dY = this.foot.y - node.y;
            const legAngle = Math.atan2(dY, dX);
            
            // Push the knee joint outward
            const kneeDist = 25 * this.side;
            const kneeX = midX + Math.cos(legAngle + Math.PI/2) * kneeDist;
            const kneeY = midY + Math.sin(legAngle + Math.PI/2) * kneeDist;

            ctx.moveTo(node.x, node.y);
            ctx.lineTo(kneeX, kneeY);
            ctx.lineTo(this.foot.x, this.foot.y);
            
            // Draw foot indicator
            ctx.moveTo(this.foot.x + 3, this.foot.y);
            ctx.arc(this.foot.x, this.foot.y, 3, 0, Math.PI*2);
        }}
    }}

    class Creature {{
        constructor(x, y) {{
            this.spine = [];
            this.numSegments = 45;
            this.segmentLength = 12;
            
            // Initialize spine
            for (let i = 0; i < this.numSegments; i++) {{
                this.spine.push(new Segment(x - i * this.segmentLength, y, this.segmentLength));
            }}

            // Initialize legs
            this.legs = [];
            const legPlacements = [8, 16, 24, 32]; // Attach legs to these spine indices
            legPlacements.forEach(index => {{
                this.legs.push(new Leg(index, 1, 60));  // Right leg
                this.legs.push(new Leg(index, -1, 60)); // Left leg
            }});
        }}

        update(tx, ty) {{
            // Smoothly ease head toward target
            let head = this.spine[0];
            let easeX = head.x + (tx - head.x) * 0.1;
            let easeY = head.y + (ty - head.y) * 0.1;
            
            // Head follows target
            head.follow(easeX, easeY);

            // Rest of the spine follows the segment in front of it
            for (let i = 1; i < this.numSegments; i++) {{
                this.spine[i].follow(this.spine[i-1].x, this.spine[i-1].y);
            }}
        }}

        draw() {{
            ctx.beginPath();
            ctx.strokeStyle = LINE_COLOR;
            ctx.lineWidth = 1.5;
            ctx.lineCap = 'round';
            ctx.lineJoin = 'round';

            // Glow effect
            ctx.shadowBlur = 10;
            ctx.shadowColor = ACCENT_COLOR;

            // Draw Spine
            ctx.moveTo(this.spine[0].x, this.spine[0].y);
            for (let i = 1; i < this.numSegments; i++) {{
                ctx.lineTo(this.spine[i].x, this.spine[i].y);
            }}

            // Draw Ribs (perpendicular offsets)
            for (let i = 1; i < this.numSegments; i++) {{
                const node = this.spine[i];
                // Math.sin creates a taper profile: narrow at head/tail, wide in middle
                const thickness = Math.sin((i / this.numSegments) * Math.PI) * 20;
                
                const rX1 = node.x + Math.cos(node.angle + Math.PI/2) * thickness;
                const rY1 = node.y + Math.sin(node.angle + Math.PI/2) * thickness;
                const rX2 = node.x + Math.cos(node.angle - Math.PI/2) * thickness;
                const rY2 = node.y + Math.sin(node.angle - Math.PI/2) * thickness;

                ctx.moveTo(rX1, rY1);
                ctx.lineTo(rX2, rY2);
            }}

            // Update and draw Legs
            this.legs.forEach(leg => leg.update(this.spine));

            ctx.stroke();
            
            // Reset shadow to avoid trailing artifacts on clear
            ctx.shadowBlur = 0; 
        }}
    }}

    let creature;

    function init() {{
        width = container.clientWidth;
        height = container.clientHeight;
        
        // Handle high DPI displays
        const dpr = window.devicePixelRatio || 1;
        canvas.width = width * dpr;
        canvas.height = height * dpr;
        ctx.scale(dpr, dpr);

        targetX = width / 2;
        targetY = height / 2;
        creature = new Creature(width / 2, height / 2);
    }}

    function animate() {{
        ctx.clearRect(0, 0, width, height);
        
        creature.update(targetX, targetY);
        creature.draw();

        requestAnimationFrame(animate);
    }}

    // Event Listeners
    window.addEventListener('resize', init);
    
    container.addEventListener('mousemove', (e) => {{
        const rect = container.getBoundingClientRect();
        targetX = e.clientX - rect.left;
        targetY = e.clientY - rect.top;
    }});

    container.addEventListener('touchmove', (e) => {{
        const rect = container.getBoundingClientRect();
        targetX = e.touches[0].clientX - rect.left;
        targetY = e.touches[0].clientY - rect.top;
    }}, {{ passive: true }});

    // Start
    init();
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
