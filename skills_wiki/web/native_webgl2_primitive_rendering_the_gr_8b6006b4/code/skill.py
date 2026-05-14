def create_component(
    output_dir: str,
    title_text: str = "WebGL2: Hello Triangle",
    body_text: str = "A foundational demonstration of the GPU graphics pipeline.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#4B0082",     # CSS hex color for the triangle (Indigo default)
    width_px: int = 600,
    height_px: int = 600,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Native WebGL2 Triangle rendering.
    
    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Helper: Convert Hex to Normalized RGB Floats for WebGL ===
    def hex_to_rgb_float(hex_str):
        hex_str = hex_str.lstrip('#')
        if len(hex_str) == 3:
            hex_str = ''.join([c*2 for c in hex_str])
        return tuple(int(hex_str[i:i+2], 16) / 255.0 for i in (0, 2, 4))

    # Derive theme colors
    tri_r, tri_g, tri_b = hex_to_rgb_float(accent_color)
    
    if color_scheme == "dark":
        bg_color = "#121212"
        text_color = "#f0f0f0"
        clear_r, clear_g, clear_b = (0.12, 0.12, 0.12) # Canvas background
    else:
        bg_color = "#f8f9fa"
        text_color = "#1a1a2e"
        clear_r, clear_g, clear_b = (0.9, 0.9, 0.9) # Canvas background

    # === CSS ===
    # Doubling braces {{ }} to escape them in Python f-string
    css = f"""/* Native WebGL2 Setup */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --text: {text_color};
    --accent: {accent_color};
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background: var(--bg);
    color: var(--text);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 2rem;
}}

.container {{
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 1.5rem;
    max-width: 800px;
    text-align: center;
}}

.title {{
    font-size: 2rem;
    font-weight: 700;
}}

.body-text {{
    font-size: 1.1rem;
    opacity: 0.8;
}}

/* The Canvas Element */
#webgl-canvas {{
    width: {width_px}px;
    height: {height_px}px;
    /* A bright fallback color to immediately show if WebGL fails to render */
    background-color: #FA8072; 
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
    border-radius: 4px;
}}

/* Error Reporting Box */
#error-box {{
    width: {width_px}px;
    min-height: 50px;
    background-color: #2a0808;
    color: #ff6b6b;
    border-left: 4px solid #ff4757;
    padding: 1rem;
    font-family: monospace;
    font-size: 0.9rem;
    text-align: left;
    display: none; /* Hidden by default */
    white-space: pre-wrap;
    word-break: break-word;
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
    <div class="container">
        <div>
            <h1 class="title">{title_text}</h1>
            <p class="body-text">{body_text}</p>
        </div>
        
        <!-- WebGL Drawing Surface -->
        <canvas id="webgl-canvas"></canvas>
        
        <!-- Dev Error Output -->
        <div id="error-box"></div>
    </div>
    
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    # Utilizing double braces {{ }} where JS needs single braces.
    js = f"""// WebGL2 Initializer and Graphics Pipeline

// Helper to show errors on screen instead of just console
function showError(errorText) {{
    const errorBox = document.getElementById('error-box');
    errorBox.style.display = 'block';
    const p = document.createElement('p');
    p.innerText = errorText;
    errorBox.appendChild(p);
    console.error(errorText);
}}

function initWebGL() {{
    const canvas = document.getElementById('webgl-canvas');
    if (!canvas) {{
        showError("Cannot find canvas element.");
        return;
    }}

    // Ensure internal resolution matches CSS display size to prevent stretching
    canvas.width = canvas.clientWidth;
    canvas.height = canvas.clientHeight;

    // Get WebGL2 Context
    const gl = canvas.getContext('webgl2');
    if (!gl) {{
        showError("This browser does not support WebGL 2. The demo will not work.");
        return;
    }}

    // --- 1. CLEAR THE CANVAS ---
    // Set the clear color using parameters from Python
    gl.clearColor({clear_r:.3f}, {clear_g:.3f}, {clear_b:.3f}, 1.0);
    // Execute the clear command
    gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);

    // --- 2. DEFINE GEOMETRY (VERTICES) ---
    // X, Y coordinates for a triangle
    const triangleVertices = [
         0.0,  0.5,  // Top middle
        -0.5, -0.5,  // Bottom left
         0.5, -0.5   // Bottom right
    ];

    // Convert standard JS array to a Float32Array (required by WebGL)
    const triangleVerticesCpuBuffer = new Float32Array(triangleVertices);

    // --- 3. CREATE & BIND GPU BUFFER ---
    const triangleGeoBuffer = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, triangleGeoBuffer);
    
    // Send the CPU data over to the GPU buffer
    gl.bufferData(gl.ARRAY_BUFFER, triangleVerticesCpuBuffer, gl.STATIC_DRAW);

    // --- 4. SHADERS ---
    
    // Vertex Shader: Determines geometry positions on screen
    const vertexShaderSourceCode = `#version 300 es
    precision mediump float;
    
    in vec2 vertexPosition;
    
    void main() {{
        // Convert 2D x,y coordinate into 4D coordinate (x, y, z, w) required by WebGL
        gl_Position = vec4(vertexPosition, 0.0, 1.0);
    }}`;

    // Fragment Shader: Determines exact pixel colors
    const fragmentShaderSourceCode = `#version 300 es
    precision mediump float;
    
    out vec4 outputColor;
    
    void main() {{
        // RGBA color formatted via Python injection
        outputColor = vec4({tri_r:.3f}, {tri_g:.3f}, {tri_b:.3f}, 1.0);
    }}`;

    // Helper function to compile shaders
    function compileShader(type, source) {{
        const shader = gl.createShader(type);
        gl.shaderSource(shader, source);
        gl.compileShader(shader);
        
        if (!gl.getShaderParameter(shader, gl.COMPILE_STATUS)) {{
            showError("Failed to compile shader: " + gl.getShaderInfoLog(shader));
            return null;
        }}
        return shader;
    }}

    const vertexShader = compileShader(gl.VERTEX_SHADER, vertexShaderSourceCode);
    const fragmentShader = compileShader(gl.FRAGMENT_SHADER, fragmentShaderSourceCode);
    
    if (!vertexShader || !fragmentShader) return;

    // --- 5. CREATE PROGRAM ---
    // Combine shaders into a usable program
    const triangleShaderProgram = gl.createProgram();
    gl.attachShader(triangleShaderProgram, vertexShader);
    gl.attachShader(triangleShaderProgram, fragmentShader);
    gl.linkProgram(triangleShaderProgram);

    if (!gl.getProgramParameter(triangleShaderProgram, gl.LINK_STATUS)) {{
        showError("Failed to link program: " + gl.getProgramInfoLog(triangleShaderProgram));
        return;
    }}

    gl.useProgram(triangleShaderProgram);

    // --- 6. LINK BUFFER DATA TO SHADER ATTRIBUTES ---
    // Find where 'vertexPosition' lives in the compiled shader
    const vertexPositionAttributeLocation = gl.getAttribLocation(triangleShaderProgram, 'vertexPosition');
    if (vertexPositionAttributeLocation < 0) {{
        showError("Failed to get attribute location for vertexPosition");
        return;
    }}

    // Enable the attribute
    gl.enableVertexAttribArray(vertexPositionAttributeLocation);

    // Tell WebGL how to read the currently bound buffer (triangleGeoBuffer)
    gl.vertexAttribPointer(
        vertexPositionAttributeLocation, 
        2,          // size: number of components per vertex (x, y)
        gl.FLOAT,   // type: the data is 32bit floats
        false,      // normalized: don't normalize
        0,          // stride: 0 = move forward size * sizeof(type) each iteration
        0           // offset: start at the beginning of the buffer
    );

    // --- 7. DRAW ---
    // Tell WebGL what part of the canvas to render to
    gl.viewport(0, 0, canvas.width, canvas.height);
    
    // Execute the draw command
    // mode: TRIANGLES, first: 0, count: 3 vertices
    gl.drawArrays(gl.TRIANGLES, 0, 3);
}}

// Run the application
try {{
    initWebGL();
}} catch (e) {{
    showError("Uncaught JavaScript Exception: " + e.message);
}}
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
