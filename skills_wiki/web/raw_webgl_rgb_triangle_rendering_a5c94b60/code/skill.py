def create_component(
    output_dir: str,
    title_text: str = "WebGL Tutorial 01: Boring Triangle",
    body_text: str = "The demo is right above this text.",
    color_scheme: str = "dark",        
    accent_color: str = "#00bfff",     
    width_px: int = 800,
    height_px: int = 600,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Raw WebGL RGB Triangle Rendering.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Base page colors
    if color_scheme == "dark":
        bg_color = "#121212"
        text_color = "#f0f0f0"
        canvas_border = "#333"
    else:
        bg_color = "#ffffff"
        text_color = "#1a1a2e"
        canvas_border = "#ddd"

    # === CSS ===
    css = f"""/* WebGL Triangle — generated component */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background: {bg_color};
    color: {text_color};
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 2rem;
}}

.container {{
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 1.5rem;
}}

canvas {{
    border: 1px solid {canvas_border};
    background-color: #000; /* Fallback before WebGL kicks in */
    box-shadow: 0 10px 30px rgba(0,0,0,0.1);
}}

h1 {{
    font-weight: 600;
    font-size: 1.5rem;
}}

p {{
    font-style: italic;
    color: {accent_color};
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
    <link href="https://fonts.googleapis.com/css2?family=Inter:ital,wght@0,400;0,600;1,400&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        <h1>{title_text}</h1>
        <!-- WebGL Canvas -->
        <canvas id="game-surface" width="{width_px}" height="{height_px}">
            Your browser does not support HTML5 Canvas.
        </canvas>
        <p>{body_text}</p>
    </div>
    
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript (WebGL Pipeline) ===
    js = """// WebGL Initialization and Rendering Pipeline
const vertexShaderText = `
precision mediump float;
attribute vec2 vertPosition;
attribute vec3 vertColor;
varying vec3 fragColor;

void main() {
    fragColor = vertColor;
    gl_Position = vec4(vertPosition, 0.0, 1.0);
}
`;

const fragmentShaderText = `
precision mediump float;
varying vec3 fragColor;

void main() {
    gl_FragColor = vec4(fragColor, 1.0);
}
`;

function InitDemo() {
    console.log('This is working');

    const canvas = document.getElementById('game-surface');
    let gl = canvas.getContext('webgl');

    if (!gl) {
        console.log('WebGL not supported, falling back on experimental-webgl');
        gl = canvas.getContext('experimental-webgl');
    }

    if (!gl) {
        alert('Your browser does not support WebGL');
        return;
    }

    // Set clear color (Pale green from the tutorial)
    gl.clearColor(0.75, 0.85, 0.8, 1.0);
    gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);

    // ==================
    // Create Shaders
    // ==================
    const vertexShader = gl.createShader(gl.VERTEX_SHADER);
    const fragmentShader = gl.createShader(gl.FRAGMENT_SHADER);

    gl.shaderSource(vertexShader, vertexShaderText);
    gl.shaderSource(fragmentShader, fragmentShaderText);

    // Compile Vertex Shader
    gl.compileShader(vertexShader);
    if (!gl.getShaderParameter(vertexShader, gl.COMPILE_STATUS)) {
        console.error('ERROR compiling vertex shader!', gl.getShaderInfoLog(vertexShader));
        return;
    }

    // Compile Fragment Shader
    gl.compileShader(fragmentShader);
    if (!gl.getShaderParameter(fragmentShader, gl.COMPILE_STATUS)) {
        console.error('ERROR compiling fragment shader!', gl.getShaderInfoLog(fragmentShader));
        return;
    }

    // ==================
    // Create Program
    // ==================
    const program = gl.createProgram();
    gl.attachShader(program, vertexShader);
    gl.attachShader(program, fragmentShader);

    gl.linkProgram(program);
    if (!gl.getProgramParameter(program, gl.LINK_STATUS)) {
        console.error('ERROR linking program!', gl.getProgramInfoLog(program));
        return;
    }

    gl.validateProgram(program);
    if (!gl.getProgramParameter(program, gl.VALIDATE_STATUS)) {
        console.error('ERROR validating program!', gl.getProgramInfoLog(program));
        return;
    }

    // ==================
    // Create Buffer
    // ==================
    // Interleaved data: X, Y, R, G, B
    const triangleVertices = [
         0.0,  0.5,     1.0, 1.0, 0.0, // Top (Yellow)
        -0.5, -0.5,     0.7, 0.0, 1.0, // Bottom Left (Purple)
         0.5, -0.5,     0.1, 1.0, 0.6  // Bottom Right (Cyan)
    ];

    const triangleVertexBufferObject = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, triangleVertexBufferObject);
    gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(triangleVertices), gl.STATIC_DRAW);

    // ==================
    // Set Attributes
    // ==================
    const positionAttribLocation = gl.getAttribLocation(program, 'vertPosition');
    const colorAttribLocation = gl.getAttribLocation(program, 'vertColor');

    // Layout configuration
    // 5 elements total per vertex (2 for pos, 3 for color) * 4 bytes per float
    gl.vertexAttribPointer(
        positionAttribLocation, // Attribute location
        2, // Number of elements per attribute (X, Y)
        gl.FLOAT, // Type of elements
        gl.FALSE, // Normalized?
        5 * Float32Array.BYTES_PER_ELEMENT, // Size of an individual vertex (stride)
        0 // Offset from beginning of single vertex
    );

    gl.vertexAttribPointer(
        colorAttribLocation, 
        3, // (R, G, B)
        gl.FLOAT, 
        gl.FALSE, 
        5 * Float32Array.BYTES_PER_ELEMENT, 
        2 * Float32Array.BYTES_PER_ELEMENT // Offset (skip X, Y)
    );

    gl.enableVertexAttribArray(positionAttribLocation);
    gl.enableVertexAttribArray(colorAttribLocation);

    // ==================
    // Render Loop (Static)
    // ==================
    gl.useProgram(program);
    gl.drawArrays(gl.TRIANGLES, 0, 3);
}

// Ensure the code runs after the DOM is fully loaded
document.addEventListener('DOMContentLoaded', InitDemo);
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
