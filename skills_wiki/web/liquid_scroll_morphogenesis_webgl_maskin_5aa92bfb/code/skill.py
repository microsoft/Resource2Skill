def create_component(
    output_dir: str,
    title_text: str = "MORPHOGENESIS",
    body_text: str = "Solid form gives way to liquid movement. An underlying field of motion pushes and pulls the image across its surface, redistributing pixels in a way that feels organic and constantly in flux.",
    color_scheme: str = "light",
    accent_color: str = "#d4af37", # Gold accent
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Liquid Scroll Morphogenesis effect.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Derive theme colors
    if color_scheme == "dark":
        bg_color = "#111418"  # The color the image dissolves INTO
        text_color = "#f4f4f5"
        shader_color_glsl = "vec3(0.066, 0.078, 0.094)" # normalized #111418
    else:
        bg_color = "#f4f4f2"  # The color the image dissolves INTO
        text_color = "#1a1a1a"
        shader_color_glsl = "vec3(0.956, 0.956, 0.949)" # normalized #f4f4f2
        
    # Standard placeholder nature image suitable for the effect
    bg_image_url = "https://images.unsplash.com/photo-1542273917363-3b1817f69a2d?q=80&w=2500&auto=format&fit=crop"

    css = f"""/* Morphogenesis WebGL Transition */
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;1,400&family=Inter:wght@300;400&display=swap');

:root {{
    --bg: {bg_color};
    --text: {text_color};
    --accent: {accent_color};
}}

* {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: 'Inter', sans-serif;
    background-color: var(--bg);
    color: var(--text);
    overflow-x: hidden;
    /* Lenis smooth scrolling requirement */
    overscroll-behavior: none; 
}}

/* The scroll track container */
.hero-track {{
    position: relative;
    width: 100%;
    height: 300vh; /* Determines how long the scroll transition takes */
}}

/* The sticky container that holds the visuals */
.hero-visuals {{
    position: sticky;
    top: 0;
    left: 0;
    width: 100%;
    height: 100vh;
    overflow: hidden;
}}

/* 1. Deepest Layer: Image */
.hero-img {{
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    object-fit: cover;
    z-index: 1;
}}

/* 2. Middle Layer: WebGL Mask */
#glcanvas {{
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    z-index: 2;
    pointer-events: none;
}}

/* 3. Top Layer: Text Overlay */
.hero-content {{
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    z-index: 3;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    padding: 2rem;
    pointer-events: none;
}}

.hero-title {{
    font-family: 'Playfair Display', serif;
    font-size: clamp(3rem, 8vw, 8rem);
    font-weight: 400;
    letter-spacing: -0.02em;
    color: var(--accent);
    margin-bottom: 1.5rem;
}}

.hero-body {{
    font-size: clamp(1rem, 2vw, 1.25rem);
    max-width: 600px;
    line-height: 1.6;
    font-weight: 300;
}}

/* Word splitting utility classes */
.word {{
    display: inline-block;
    white-space: pre;
    will-change: transform, opacity;
}}

/* Subsequent content to prove scrolling works */
.next-section {{
    height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    background-color: var(--bg);
    padding: 2rem;
}}
.next-section h2 {{
    font-family: 'Playfair Display', serif;
    font-size: 3rem;
    font-weight: 400;
}}
"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text}</title>
    <link rel="stylesheet" href="style.css">
    
    <!-- Dependencies -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/gsap.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/ScrollTrigger.min.js"></script>
    <script src="https://cdn.jsdelivr.net/gh/studio-freight/lenis@1.0.29/bundled/lenis.min.js"></script>
</head>
<body>

    <div class="hero-track">
        <div class="hero-visuals">
            <img class="hero-img" src="{bg_image_url}" alt="Hero Background">
            <canvas id="glcanvas"></canvas>
            
            <div class="hero-content">
                <h1 class="hero-title">{title_text}</h1>
                <p class="hero-body">{body_text}</p>
            </div>
        </div>
    </div>
    
    <div class="next-section">
        <h2>The Journey Continues</h2>
    </div>

    <script src="script.js"></script>
</body>
</html>"""

    js = f"""// Morphogenesis Implementation
gsap.registerPlugin(ScrollTrigger);

// 1. Setup Smooth Scrolling (Lenis)
const lenis = new Lenis({{
    duration: 1.2,
    easing: (t) => Math.min(1, 1.001 - Math.pow(2, -10 * t)),
    smooth: true,
}});

function raf(time) {{
    lenis.raf(time);
    requestAnimationFrame(raf);
}}
requestAnimationFrame(raf);

// 2. Text Splitting Utility (Replaces premium SplitText)
function splitTextIntoWords(selector) {{
    const elements = document.querySelectorAll(selector);
    elements.forEach(el => {{
        const text = el.innerText;
        const words = text.split(' ');
        el.innerHTML = '';
        words.forEach(word => {{
            const span = document.createElement('span');
            span.className = 'word';
            span.innerText = word + ' ';
            el.appendChild(span);
        }});
    }});
}}

// Apply splitting
splitTextIntoWords('.hero-title');
splitTextIntoWords('.hero-body');

// Initially hide all words for the scroll reveal
gsap.set('.word', {{ opacity: 0, y: 30 }});

// 3. WebGL Setup
const canvas = document.getElementById('glcanvas');
const scene = new THREE.Scene();
const camera = new THREE.OrthographicCamera(-1, 1, 1, -1, 0, 1);
const renderer = new THREE.WebGLRenderer({{ canvas: canvas, alpha: true, antialias: false }});

function resize() {{
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
}}
window.addEventListener('resize', resize);
resize();

// Shader Configuration
const vertexShader = `
    varying vec2 vUv;
    void main() {{
        vUv = uv;
        gl_Position = vec4(position, 1.0);
    }}
`;

const fragmentShader = `
    varying vec2 vUv;
    uniform float uProgress;
    uniform vec3 uColor;

    // Pseudo-random noise functions
    float hash(vec2 p) {{
        p = fract(p * vec2(123.34, 456.21));
        p += dot(p, p + 45.32);
        return fract(p.x * p.y);
    }}

    float noise(vec2 p) {{
        vec2 i = floor(p);
        vec2 f = fract(p);
        vec2 u = f * f * (3.0 - 2.0 * f);
        return mix(mix(hash(i + vec2(0.0, 0.0)), hash(i + vec2(1.0, 0.0)), u.x),
                   mix(hash(i + vec2(0.0, 1.0)), hash(i + vec2(1.0, 1.0)), u.x), u.y);
    }}

    float fbm(vec2 p) {{
        float value = 0.0;
        float amplitude = 0.5;
        for(int i = 0; i < 4; i++) {{
            value += amplitude * noise(p);
            p *= 2.0;
            amplitude *= 0.5;
        }}
        return value;
    }}

    void main() {{
        vec2 uv = vUv * 2.0 - 1.0;
        
        // Generate fractal noise
        // Adding a subtle offset based on progress gives it a flowing feeling
        float n = fbm(uv * 2.5 + vec2(0.0, uProgress * -0.5));
        
        // Combine noise with vertical gradient (uv.y goes -1 to 1)
        // This causes the dissolve to naturally rise from the bottom to the top
        float d = (n * 0.5) + (uv.y * 0.5 + 0.5); 
        
        // Map scroll progress to a sweeping threshold
        float threshold = uProgress * 2.5 - 0.5;
        
        // Calculate final alpha with smooth edges
        float alpha = 1.0 - smoothstep(threshold - 0.4, threshold + 0.4, d);
        
        gl_FragColor = vec4(uColor, alpha);
    }}
`;

const material = new THREE.ShaderMaterial({{
    vertexShader,
    fragmentShader,
    transparent: true,
    uniforms: {{
        uProgress: {{ value: 0.0 }},
        uColor: {{ value: new THREE.Vector3({shader_color_glsl}) }}
    }}
}});

const geometry = new THREE.PlaneGeometry(2, 2);
const mesh = new THREE.Mesh(geometry, material);
scene.add(mesh);

// 4. Render Loop hooked into Lenis
function animate() {{
    renderer.render(scene, camera);
    requestAnimationFrame(animate);
}}
animate();

// 5. ScrollTrigger Animation Logic
// Drive the Shader
ScrollTrigger.create({{
    trigger: ".hero-track",
    start: "top top",
    end: "bottom bottom",
    scrub: 1, // Smoothly link progress
    onUpdate: (self) => {{
        // Apply a slight easing to the shader uniform
        gsap.to(material.uniforms.uProgress, {{
            value: self.progress,
            duration: 0.1,
            overwrite: true
        }});
    }}
}});

// Drive the Typography
gsap.to('.hero-title .word', {{
    opacity: 1,
    y: 0,
    stagger: 0.03,
    scrollTrigger: {{
        trigger: ".hero-track",
        start: "top top",
        end: "center center",
        scrub: 1.5,
    }}
}});

gsap.to('.hero-body .word', {{
    opacity: 1,
    y: 0,
    stagger: 0.015,
    scrollTrigger: {{
        trigger: ".hero-track",
        start: "20% top", // Start reading body a bit later
        end: "70% center",
        scrub: 1.5,
    }}
}});
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
