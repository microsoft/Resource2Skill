def create_component(
    output_dir: str,
    title_text: str = "Fluid Noise Gradient",
    body_text: str = "Immersive WebGL fragment shaders create organic, swirly background animations that elevate the visual language of modern web interfaces. Stacked mathematical functions create the illusion of fluid dynamics.",
    color_scheme: str = "dark",
    accent_color: str = "#4f46e5",
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the WebGL Fluid Noise Gradient.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os
    import colorsys

    os.makedirs(output_dir, exist_ok=True)

    # --- Color Palette Generation ---
    def hex_to_rgb_norm(hex_color):
        hex_color = hex_color.lstrip('#')
        if len(hex_color) == 3:
            hex_color = ''.join([c*2 for c in hex_color])
        return tuple(int(hex_color[i:i+2], 16)/255.0 for i in (0, 2, 4))
        
    def rgb_norm_to_hex(r, g, b):
        return '#{:02x}{:02x}{:02x}'.format(int(r*255), int(g*255), int(b*255))
        
    def generate_palette(base_hex, is_dark):
        try:
            r, g, b = hex_to_rgb_norm(base_hex)
            h, l, s = colorsys.rgb_to_hls(r, g, b)
        except:
            h, l, s = (0.6, 0.5, 0.8) # Default if parsing fails
            
        # Ensure optimal lightness for gradients
        if is_dark:
            l = min(max(l, 0.3), 0.6)
        else:
            l = min(max(l, 0.6), 0.85)
            
        s = min(s + 0.2, 1.0) # Boost saturation
        
        # Generate analogous/split palette
        c1 = rgb_norm_to_hex(*colorsys.hls_to_rgb((h + 0.05) % 1.0, l * 0.7, s))
        c2 = rgb_norm_to_hex(*colorsys.hls_to_rgb(h, l, s))
        c3 = rgb_norm_to_hex(*colorsys.hls_to_rgb((h - 0.15) % 1.0, l * 0.9, s))
        c4 = rgb_norm_to_hex(*colorsys.hls_to_rgb((h + 0.3) % 1.0, l * 1.1, s))
        return c1, c2, c3, c4
        
    is_dark = (color_scheme == "dark")
    c1, c2, c3, c4 = generate_palette(accent_color, is_dark)

    # --- Theme Variables ---
    if is_dark:
        bg_color = "#000000"
        text_color = "#ffffff"
        card_bg = "rgba(20, 20, 25, 0.4)"
        card_border = "rgba(255, 255, 255, 0.1)"
        shadow = "rgba(0, 0, 0, 0.4)"
        badge_bg = "rgba(255, 255, 255, 0.1)"
        badge_text = "#ffffff"
        btn_text = "#000000"
    else:
        bg_color = "#ffffff"
        text_color = "#111827"
        card_bg = "rgba(255, 255, 255, 0.6)"
        card_border = "rgba(255, 255, 255, 0.4)"
        shadow = "rgba(0, 0, 0, 0.1)"
        badge_bg = "rgba(0, 0, 0, 0.06)"
        badge_text = "#374151"
        btn_text = "#ffffff"

    # === CSS ===
    css = f"""/* WebGL Fluid Gradient Styles */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Inter', system-ui, sans-serif;
    background-color: {bg_color};
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
    padding: 2rem;
}}

.viewport-container {{
    width: 100%;
    max-width: var(--width);
    height: var(--height);
    position: relative;
    border-radius: 24px;
    overflow: hidden;
    box-shadow: 0 25px 50px -12px {shadow};
}}

.canvas-container {{
    position: absolute;
    inset: 0;
    width: 100%;
    height: 100%;
    z-index: 0;
}}

canvas {{
    width: 100%;
    height: 100%;
    display: block;
}}

.content-overlay {{
    position: relative;
    z-index: 10;
    width: 100%;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 2rem;
}}

.glass-card {{
    background: {card_bg};
    backdrop-filter: blur(24px);
    -webkit-backdrop-filter: blur(24px);
    border: 1px solid {card_border};
    border-radius: 20px;
    padding: 3rem;
    max-width: 540px;
    box-shadow: 0 24px 48px {shadow};
    color: {text_color};
    animation: fadeUp 1s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    opacity: 0;
    transform: translateY(20px);
}}

@keyframes fadeUp {{
    to {{
        opacity: 1;
        transform: translateY(0);
    }}
}}

.badge {{
    display: inline-block;
    padding: 0.35rem 0.85rem;
    border-radius: 9999px;
    font-size: 0.75rem;
    font-weight: 600;
    background: {badge_bg};
    color: {badge_text};
    margin-bottom: 1.5rem;
    letter-spacing: 0.05em;
    text-transform: uppercase;
}}

.title {{
    font-size: 2.75rem;
    line-height: 1.1;
    margin-bottom: 1.25rem;
    font-weight: 700;
    letter-spacing: -0.03em;
}}

.body-text {{
    font-size: 1.125rem;
    line-height: 1.6;
    margin-bottom: 2.5rem;
    opacity: 0.85;
}}

.actions {{
    display: flex;
    gap: 1rem;
    flex-wrap: wrap;
}}

.cta-button {{
    padding: 0.875rem 1.75rem;
    border-radius: 9999px;
    font-size: 1rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s ease;
    border: none;
}}

.cta-button.primary {{
    background: {text_color};
    color: {btn_text};
}}

.cta-button.primary:hover {{
    transform: translateY(-2px);
    box-shadow: 0 10px 20px {shadow};
}}

.cta-button.secondary {{
    background: transparent;
    border: 1px solid {card_border};
    color: {text_color};
}}

.cta-button.secondary:hover {{
    background: {badge_bg};
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
    <div class="viewport-container">
        <div class="canvas-container">
            <canvas id="gradient-canvas"></canvas>
        </div>
        
        <div class="content-overlay">
            <div class="glass-card">
                <span class="badge">Procedural WebGL</span>
                <h1 class="title">{title_text}</h1>
                <p class="body-text">{body_text}</p>
                <div class="actions">
                    <button class="cta-button primary">Explore Render</button>
                    <button class="cta-button secondary">View Source</button>
                </div>
            </div>
        </div>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript (WebGL Boilerplate & Shaders) ===
    js = f"""document.addEventListener('DOMContentLoaded', () => {{
    const canvas = document.getElementById('gradient-canvas');
    const gl = canvas.getContext('webgl') || canvas.getContext('experimental-webgl');

    // Graceful fallback if WebGL fails
    if (!gl) {{
        canvas.style.display = 'none';
        document.querySelector('.canvas-container').style.background = 'linear-gradient(135deg, {c1}, {c4})';
        return;
    }}

    // Vertex Shader (Full-screen quad)
    const vsSource = `
        attribute vec2 position;
        void main() {{
            gl_Position = vec4(position, 0.0, 1.0);
        }}
    `;

    // Fragment Shader (Fluid Noise Logic)
    const fsSource = `
        precision highp float;
        uniform vec2 u_resolution;
        uniform float u_time;
        uniform vec3 u_color1;
        uniform vec3 u_color2;
        uniform vec3 u_color3;
        uniform vec3 u_color4;

        void main() {{
            // Normalize coordinates
            vec2 st = gl_FragCoord.xy / u_resolution.xy;
            // Adjust for aspect ratio to prevent stretching
            st.x *= u_resolution.x / u_resolution.y;

            // Animate the coordinate space using stacked sines (fBm variation)
            vec2 q = vec2(0.0);
            q.x = sin(st.y * 2.5 + u_time * 0.3) + cos(st.x * 2.0 + u_time * 0.2);
            q.y = cos(st.x * 3.0 + u_time * 0.25) + sin(st.y * 2.5 + u_time * 0.35);

            // Distort original coordinates
            vec2 p = st + 0.15 * q;

            // Generate mixing weights based on distorted space
            float w1 = sin(p.x * 3.0 + u_time * 0.4) * 0.5 + 0.5;
            float w2 = cos(p.y * 3.5 - u_time * 0.3) * 0.5 + 0.5;
            float w3 = sin((p.x + p.y) * 2.0 + u_time * 0.5) * 0.5 + 0.5;

            // Progressively mix the 4 palette colors
            vec3 color = mix(u_color1, u_color2, w1);
            color = mix(color, u_color3, w2);
            color = mix(color, u_color4, w3);

            // Add a subtle vignette for depth
            vec2 center = vec2(0.5 * u_resolution.x / u_resolution.y, 0.5);
            float dist = length(st - center);
            color -= dist * 0.25;

            gl_FragColor = vec4(color, 1.0);
        }}
    `;

    // WebGL Helper Functions
    function createShader(type, source) {{
        const shader = gl.createShader(type);
        gl.shaderSource(shader, source);
        gl.compileShader(shader);
        if (!gl.getShaderParameter(shader, gl.COMPILE_STATUS)) {{
            console.error('Shader error:', gl.getShaderInfoLog(shader));
            gl.deleteShader(shader);
            return null;
        }}
        return shader;
    }}

    const vertexShader = createShader(gl.VERTEX_SHADER, vsSource);
    const fragmentShader = createShader(gl.FRAGMENT_SHADER, fsSource);

    const program = gl.createProgram();
    gl.attachShader(program, vertexShader);
    gl.attachShader(program, fragmentShader);
    gl.linkProgram(program);
    gl.useProgram(program);

    // Geometry definition
    const positionBuffer = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, positionBuffer);
    gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([
        -1.0, -1.0,  1.0, -1.0,  -1.0,  1.0,
        -1.0,  1.0,  1.0, -1.0,   1.0,  1.0
    ]), gl.STATIC_DRAW);

    const positionLocation = gl.getAttribLocation(program, "position");
    gl.enableVertexAttribArray(positionLocation);
    gl.vertexAttribPointer(positionLocation, 2, gl.FLOAT, false, 0, 0);

    // Uniform mapping
    const locRes = gl.getUniformLocation(program, "u_resolution");
    const locTime = gl.getUniformLocation(program, "u_time");
    const locC1 = gl.getUniformLocation(program, "u_color1");
    const locC2 = gl.getUniformLocation(program, "u_color2");
    const locC3 = gl.getUniformLocation(program, "u_color3");
    const locC4 = gl.getUniformLocation(program, "u_color4");

    function hexToRgb(hex) {{
        let bigint = parseInt(hex.replace('#', ''), 16);
        return [
            ((bigint >> 16) & 255) / 255,
            ((bigint >> 8) & 255) / 255,
            (bigint & 255) / 255
        ];
    }}

    // Inject generated colors from Python
    gl.uniform3fv(locC1, hexToRgb('{c1}'));
    gl.uniform3fv(locC2, hexToRgb('{c2}'));
    gl.uniform3fv(locC3, hexToRgb('{c3}'));
    gl.uniform3fv(locC4, hexToRgb('{c4}'));

    function resize() {{
        const rect = canvas.parentElement.getBoundingClientRect();
        // Avoid constant subpixel resizing checks
        if (canvas.width !== Math.floor(rect.width) || canvas.height !== Math.floor(rect.height)) {{
            canvas.width = Math.floor(rect.width);
            canvas.height = Math.floor(rect.height);
            gl.viewport(0, 0, canvas.width, canvas.height);
            gl.uniform2f(locRes, canvas.width, canvas.height);
        }}
    }}
    window.addEventListener('resize', resize);
    resize();

    // Render loop
    let startTime = Date.now();
    function render() {{
        const time = (Date.now() - startTime) * 0.001;
        resize(); // Check size changes
        gl.uniform1f(locTime, time);
        gl.drawArrays(gl.TRIANGLES, 0, 6);
        requestAnimationFrame(render);
    }}
    requestAnimationFrame(render);
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
