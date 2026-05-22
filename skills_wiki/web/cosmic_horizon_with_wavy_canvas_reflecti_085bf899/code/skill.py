def create_component(
    output_dir: str,
    title_text: str = "Cosmic Horizon",
    body_text: str = "A procedural canvas reflection experiment",
    color_scheme: str = "dark",
    accent_color: str = "#ff7f00",
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Cosmic Horizon with Wavy Canvas Reflections.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Base styling values
    bg_color = "#000000"
    text_color = "#ffffff" if color_scheme == "dark" else "#f0f0f0"

    # === CSS ===
    css = f"""/* Cosmic Horizon — generated component */
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
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background: #000;
    color: var(--text);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
}}

.canvas-container {{
    width: var(--width);
    height: var(--height);
    position: relative;
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 32px 64px rgba(0, 0, 0, 0.8), 0 0 0 1px rgba(255, 255, 255, 0.05);
    background: var(--bg);
}}

canvas {{
    display: block;
    width: 100%;
    height: 100%;
}}

.overlay-content {{
    position: absolute;
    inset: 0;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding-top: 12%;
    z-index: 10;
    pointer-events: none; /* Let clicks pass through to canvas if interactive */
    text-align: center;
}}

.title {{
    font-size: 3.5rem;
    font-weight: 700;
    letter-spacing: -0.02em;
    background: linear-gradient(to bottom, #ffffff, rgba(255,255,255,0.6));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    filter: drop-shadow(0 4px 16px rgba(0, 0, 0, 0.8));
    margin-bottom: 1rem;
}}

.body-text {{
    font-size: 1.125rem;
    font-weight: 400;
    color: rgba(255, 255, 255, 0.8);
    max-width: 600px;
    line-height: 1.6;
    filter: drop-shadow(0 2px 8px rgba(0, 0, 0, 0.8));
}}

@media (max-width: 768px) {{
    .title {{ font-size: 2.5rem; }}
    .body-text {{ font-size: 1rem; padding: 0 20px; }}
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
    <div class="canvas-container">
        <div class="overlay-content">
            <h1 class="title">{title_text}</h1>
            <p class="body-text">{body_text}</p>
        </div>
        <canvas id="cosmic-scene" aria-hidden="true"></canvas>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Cosmic Horizon Render Engine
document.addEventListener('DOMContentLoaded', () => {{
    const canvas = document.getElementById('cosmic-scene');
    const ctx = canvas.getContext('2d', {{ alpha: false }}); // Optimize by disabling alpha channel on root
    const container = document.querySelector('.canvas-container');

    let width, height, horizon;
    let stars = [];
    let meteors = [];

    // Configuration
    const accentColor = "{accent_color}";
    
    function resize() {{
        // Lock internal resolution to container size for 1:1 pixel slice mapping
        width = container.clientWidth;
        height = container.clientHeight;
        canvas.width = width;
        canvas.height = height;
        horizon = Math.floor(height / 2);
        initStars();
    }}

    function initStars() {{
        stars = [];
        const numStars = Math.floor((width * horizon) / 2500); // Scale stars based on screen real estate
        for (let i = 0; i < numStars; i++) {{
            stars.push({{
                x: Math.random() * width,
                y: Math.random() * horizon,
                r: Math.random() * 1.2 + 0.3,
                phase: Math.random() * Math.PI * 2,
                speed: Math.random() * 0.02 + 0.005,
                baseAlpha: Math.random() * 0.5 + 0.3
            }});
        }}
    }}

    function spawnMeteor() {{
        meteors.push({{
            x: Math.random() * width * 1.5, // Can spawn offscreen right
            y: -50,
            vx: -Math.random() * 12 - 6,   // Moving left and fast
            vy: Math.random() * 6 + 4,     // Moving down
            len: Math.random() * 60 + 40,
            life: 1,
            decay: Math.random() * 0.02 + 0.01
        }});
    }}

    function draw(time) {{
        // --- 1. Draw Base Sky ---
        const skyGrad = ctx.createLinearGradient(0, 0, 0, horizon);
        skyGrad.addColorStop(0, '#020204');
        skyGrad.addColorStop(1, '#1a1025');
        ctx.fillStyle = skyGrad;
        ctx.fillRect(0, 0, width, horizon);

        // --- 2. Draw Stars ---
        ctx.fillStyle = '#ffffff';
        stars.forEach(star => {{
            const alpha = star.baseAlpha + (0.5 * Math.sin(time * star.speed + star.phase));
            ctx.globalAlpha = Math.max(0.1, alpha);
            ctx.beginPath();
            ctx.arc(star.x, star.y, star.r, 0, Math.PI * 2);
            ctx.fill();
        }});
        ctx.globalAlpha = 1.0;

        // --- 3. Draw Meteors ---
        if (Math.random() < 0.03) spawnMeteor(); // Spawn chance
        
        for (let i = meteors.length - 1; i >= 0; i--) {{
            let m = meteors[i];
            m.x += m.vx;
            m.y += m.vy;
            m.life -= m.decay;

            if (m.life <= 0 || m.y > horizon) {{
                meteors.splice(i, 1);
                continue;
            }}

            let dx = m.vx * (m.len / 10);
            let dy = m.vy * (m.len / 10);
            
            let mGrad = ctx.createLinearGradient(m.x, m.y, m.x - dx, m.y - dy);
            mGrad.addColorStop(0, `rgba(255, 230, 180, ${{m.life}})`);
            mGrad.addColorStop(1, `rgba(255, 200, 100, 0)`);
            
            ctx.strokeStyle = mGrad;
            ctx.lineWidth = 2;
            ctx.lineCap = 'round';
            ctx.beginPath();
            ctx.moveTo(m.x, m.y);
            ctx.lineTo(m.x - dx, m.y - dy);
            ctx.stroke();
        }}

        // --- 4. Draw Rainbow ---
        ctx.save();
        ctx.globalCompositeOperation = 'screen';
        const rbRadius = width * 0.22;
        const rbThick = width * 0.04;
        const rainbowColors = [
            [255, 0, 0], [255, 127, 0], [255, 255, 0],
            [0, 255, 0], [0, 0, 255], [75, 0, 130], [139, 0, 255]
        ];
        const bandSize = rbThick / rainbowColors.length;
        
        ctx.shadowBlur = 12;
        ctx.lineWidth = bandSize + 0.5;

        rainbowColors.forEach((c, i) => {{
            ctx.strokeStyle = `rgba(${{c[0]}}, ${{c[1]}}, ${{c[2]}}, 0.35)`;
            ctx.shadowColor = `rgba(${{c[0]}}, ${{c[1]}}, ${{c[2]}}, 0.6)`;
            ctx.beginPath();
            // Draw arc in the sky (top half only)
            ctx.arc(width/2, horizon, rbRadius - i * bandSize, Math.PI, 0);
            ctx.stroke();
        }});
        ctx.restore();

        // --- 5. Draw Central Sun / Light Source ---
        ctx.save();
        ctx.globalCompositeOperation = 'screen';
        const sunR = width * 0.12;
        const sunGrad = ctx.createRadialGradient(width/2, horizon, 0, width/2, horizon, sunR);
        sunGrad.addColorStop(0, 'rgba(255, 255, 255, 1)');
        sunGrad.addColorStop(0.08, 'rgba(255, 220, 150, 0.9)');
        sunGrad.addColorStop(0.3, `rgba(255, 120, 30, 0.4)`);
        sunGrad.addColorStop(1, 'rgba(0, 0, 0, 0)');
        
        ctx.fillStyle = sunGrad;
        ctx.beginPath();
        ctx.arc(width/2, horizon, sunR, Math.PI, 0); // Semi-circle above horizon
        ctx.fill();

        // Lens Flare Line
        const hLine = ctx.createLinearGradient(width/2 - sunR*1.8, horizon, width/2 + sunR*1.8, horizon);
        hLine.addColorStop(0, 'rgba(255,200,100,0)');
        hLine.addColorStop(0.5, 'rgba(255,255,255,0.7)');
        hLine.addColorStop(1, 'rgba(255,200,100,0)');
        ctx.fillStyle = hLine;
        ctx.fillRect(width/2 - sunR*1.8, horizon - 1, sunR*3.6, 2);
        ctx.restore();


        // --- 6. Simulate Water Reflection ---
        // Fill lower half with deep water base color
        ctx.fillStyle = '#010103';
        ctx.fillRect(0, horizon, width, height - horizon);

        // Feedback loop: Read rendered sky and draw it onto the water with sine wave distortion
        const stripH = 3; // Height of horizontal slices. 3px balances quality & CPU load.
        let t = time * 0.001; // Time in seconds

        for (let y = horizon; y < height; y += stripH) {{
            let depth = y - horizon;
            let sourceY = horizon - depth;
            
            // Prevent reading outside canvas bounds
            let safeSourceY = Math.max(0, Math.floor(sourceY - stripH));
            
            // Calculate ripple displacement
            let amplitude = 1 + depth * 0.015; // Waves get wider closer to the camera
            let frequency = 0.035;
            let dx = Math.sin((depth * frequency) - (t * 2)) * amplitude;
            dx += Math.sin((depth * 0.08) - (t * 3.5)) * (amplitude * 0.3); // Secondary turbulence

            try {{
                // Draw slice flipped and horizontally shifted
                ctx.drawImage(
                    canvas,
                    0, safeSourceY, width, stripH, // Source rectangle
                    Math.floor(dx), Math.floor(y), width, stripH // Destination rectangle
                );
            }} catch(e) {{}} // Failsafe for bounds edge cases
        }}

        // --- 7. Water Depth Gradient Tint ---
        // Darkens the water as it approaches the bottom of the screen
        const waterTint = ctx.createLinearGradient(0, horizon, 0, height);
        waterTint.addColorStop(0, 'rgba(5, 5, 10, 0.2)');
        waterTint.addColorStop(1, 'rgba(0, 0, 5, 0.85)');
        ctx.fillStyle = waterTint;
        ctx.fillRect(0, horizon, width, height - horizon);

        // --- 8. Specular Highlight (Sun glints on water) ---
        ctx.save();
        ctx.globalCompositeOperation = 'screen';
        for (let y = horizon; y < height; y += 4) {{
            let depth = y - horizon;
            let depthNorm = depth / (height - horizon);
            
            // Re-calculate primary wave to align sparkles to wave crests
            let dx = Math.sin((depth * 0.035) - (t * 2)) * (1 + depth * 0.015);
            
            let intensity = Math.max(0, 1 - (depthNorm * 1.5));
            if (Math.random() < 0.4 * intensity) {{
                let w = Math.random() * 40 * (1 - depthNorm) + 10;
                ctx.fillStyle = `rgba(255, 200, 100, ${{intensity * 0.6}})`;
                // Add noise to horizontal position
                let noiseX = (Math.random() - 0.5) * 30 * depthNorm;
                ctx.fillRect(width/2 + dx + noiseX - w/2, y, w, 1.5);
            }}
        }}
        ctx.restore();

        // Loop
        requestAnimationFrame(draw);
    }}

    // Init and start
    window.addEventListener('resize', resize);
    resize();
    requestAnimationFrame(draw);
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
