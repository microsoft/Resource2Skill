# Cinematic Scroll-Driven Parallax Engine

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Cinematic Scroll-Driven Parallax Engine

* **Core Visual Mechanism**: A layered 2.5D optical illusion achieved by translating DOM elements at different rates relative to the user's scroll position. Elements further away (backgrounds) move slower, while closer elements (foregrounds) move faster, mimicking real-world depth and perspective. A central "sticky" subject (the parachuting cat) maintains its focal point through specific scroll windows before landing.
* **Why Use This Skill (Rationale)**: This technique transforms a standard vertical scrolling layout into a cinematic, narrative experience. By decoupling the scrollbar from a 1:1 pixel mapping, the page becomes a timeline. The sticky subject provides a narrative anchor, making the user feel like they are "driving" an animation rather than just reading a document.
* **Overall Applicability**: Perfect for immersive landing pages, storytelling/scrollytelling editorials, product unveilings (like Apple's hardware pages), and gamified portfolios. 
* **Value Addition**: Replaces static, flat reading with a spatial journey. It hooks user attention by rewarding scrolling with dynamic micro-interactions, significantly increasing time-on-page and engagement metrics.
* **Browser Compatibility**: Fully supported across all modern browsers. Uses hardware-accelerated 3D transforms (`translate3d`) and `requestAnimationFrame` for buttery smooth 60fps rendering without jank. No external dependencies required.

### 2. Visual & Technical Breakdown

* **Step A: Core Visual Elements**
  - **Layers**: Composed of distinct depth tiers—a deep sky gradient, a starfield, a celestial body (moon/sun), distant mountains, midground slopes, and a foreground ground plane.
  - **Color Logic**: Driven by a cohesive atmospheric theme. The dark theme utilizes deep purples (`#20124d`) transitioning to blacks (`#0f0814`) with a bright cyan/white accent. The light theme uses soft blues and earthy teals.
  - **Typography**: Oversized, heavy-weight sans-serif (`font-family: 'Inter', system-ui`) with aggressive text strokes and shadows to separate the text from the complex visual background.
  - **Subject**: An emoji composition (🪂🐈) acts as the high-contrast focal point, utilizing a CSS keyframe sway for ambient liveliness.

* **Step B: Layout & Compositional Style**
  - **Encapsulated Viewport**: The component wraps the entire effect in a bounded container (`overflow-y: auto`), meaning the parallax effect is cleanly contained and doesn't hijack the host page's body scroll.
  - **The "Proxy" Hack**: A transparent `.scroll-spacer` div is set to `300%` height, forcing a scrollbar. The actual visible content `.parallax-scene` uses `position: sticky; top: 0` to stay locked in frame.
  - **Layer Positioning**: Elements are positioned using percentages (`top: 130%`, `top: 350%`) so they exist "off-screen" in the timeline and are pulled into the viewport by the scroll engine.

* **Step C: Interactive Behavior & Animations**
  - **The Lerped Scroll Engine**: Vanilla JavaScript listens to the container's scroll event but applies the transform via a linear interpolation (Lerp) inside a `requestAnimationFrame` loop. This gives the scroll a "springy", fluid feeling entirely independent of the user's trackpad/mouse wheel harshness.
  - **Layer Speeds**: Backgrounds have speed multipliers (`0.1`, `0.5`), while the foreground maps `1.0` (moving exactly inversely to scroll).
  - **The "Sticky" Subject**: The cat falls through three distinct mathematical states: 
    1. Base falling (0 to 1x viewport scrolled)
    2. Sticky suspension (1x to 2.8x viewport scrolled)
    3. Landing sequence (2.8x to max scroll)

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **Layer Depth Physics** | Vanilla JS + Lerp | Simulates `react-spring/parallax` natively without a 30kb library. Uses `translate3d` for GPU acceleration. |
| **Scroll Encapsulation** | CSS `position: sticky` | Keeps the parallax scene framed correctly inside a fixed-size component container while allowing an invisible proxy to create the scrollbar. |
| **Mountains & Ground** | CSS `clip-path: polygon()` | Draws crisp, responsive geometric landscape layers without needing heavy external SVG/PNG assets. |
| **Parachute Sway** | CSS `@keyframes` | Ambient looping motion (swaying) is best handled by pure CSS, keeping the JS render loop focused purely on scroll physics. |

#### 3b. Complete Reproduction Code

```python
def create_component(
    output_dir: str,
    title_text: str = "WELCOME TO MY WEBSITE",
    body_text: str = "WEB DEVELOPMENT IS FUN!",
    color_scheme: str = "dark",
    accent_color: str = "#00ffff",
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    import os

    os.makedirs(output_dir, exist_ok=True)
    
    # Use fallback body_text if empty
    if not body_text:
        body_text = "WEB DEVELOPMENT IS FUN!"

    # Theme logic
    if color_scheme == "dark":
        sky_gradient = "linear-gradient(to bottom, #020111 0%, #20124d 30%, #543159 60%, #1a1225 100%)"
        mtn_far = "#2a1b38"
        mtn_mid = "#1d1124"
        ground = "#0f0814"
        celestial_bg = "radial-gradient(circle at 30% 30%, #fff, #ddd 60%, #aaa 100%)"
        celestial_shadow = f"0 0 50px {accent_color}"
        text_color = "#fff"
        text_stroke = "2px #000"
        stars_opacity = "1"
    else:
        sky_gradient = "linear-gradient(to bottom, #87CEEB 0%, #aae0fa 30%, #ffdcb3 60%, #ffcda5 100%)"
        mtn_far = "#8db5a6"
        mtn_mid = "#5b9e83"
        ground = "#2f7a5b"
        celestial_bg = "radial-gradient(circle at 30% 30%, #fffde7, #ffeb3b 60%, #fbc02d 100%)" # Sun
        celestial_shadow = f"0 0 70px {accent_color}"
        text_color = "#fff"
        text_stroke = "2px #222"
        stars_opacity = "0.2"

    css = f"""/* Cinematic Parallax Engine */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --width: {width_px}px;
    --height: {height_px}px;
    --sky: {sky_gradient};
    --mtn-far: {mtn_far};
    --mtn-mid: {mtn_mid};
    --ground: {ground};
    --celestial-bg: {celestial_bg};
    --celestial-shadow: {celestial_shadow};
    --text-color: {text_color};
    --text-stroke: {text_stroke};
    --stars-opacity: {stars_opacity};
    --accent: {accent_color};
}}

body {{
    font-family: 'Inter', system-ui, sans-serif;
    background: #000;
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 100vh;
}}

.component-wrapper {{
    width: var(--width);
    height: var(--height);
    max-width: 100vw;
    max-height: 100vh;
    border-radius: 12px;
    box-shadow: 0 25px 50px rgba(0,0,0,0.5), 0 0 0 1px rgba(255,255,255,0.1);
    overflow: hidden;
    position: relative;
    background: #000;
}}

.parallax-viewport {{
    width: 100%;
    height: 100%;
    overflow-y: auto;
    overflow-x: hidden;
    /* Smooth scroll behavior disabled natively because JS handles the Lerp */
    scroll-behavior: auto; 
}}

/* Custom scrollbar for the viewport */
.parallax-viewport::-webkit-scrollbar {{ width: 8px; }}
.parallax-viewport::-webkit-scrollbar-track {{ background: rgba(0,0,0,0.2); }}
.parallax-viewport::-webkit-scrollbar-thumb {{ background: var(--accent); border-radius: 4px; }}

.parallax-scene {{
    position: sticky;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    overflow: hidden;
    background: var(--sky);
}}

.scroll-spacer {{
    height: 300%; /* Creates a total scrollable space of 400% */
    width: 100%;
    pointer-events: none;
}}

.layer {{
    position: absolute;
    width: 100%;
    left: 0;
    will-change: transform;
}}

.stars {{
    top: 0; 
    height: 150%;
    background-image: 
      radial-gradient(2px 2px at 10% 20%, rgba(255,255,255,0.9), rgba(0,0,0,0)),
      radial-gradient(2px 2px at 30% 60%, rgba(255,255,255,0.8), rgba(0,0,0,0)),
      radial-gradient(3px 3px at 50% 10%, rgba(255,255,255,1), rgba(0,0,0,0)),
      radial-gradient(2px 2px at 70% 80%, rgba(255,255,255,0.6), rgba(0,0,0,0)),
      radial-gradient(2px 2px at 90% 40%, rgba(255,255,255,0.8), rgba(0,0,0,0));
    background-repeat: repeat;
    background-size: 250px 250px;
    opacity: var(--stars-opacity);
}}

.celestial {{
    top: 10%;
    right: 15%;
    width: 25%;
    aspect-ratio: 1;
    border-radius: 50%;
    background: var(--celestial-bg);
    box-shadow: var(--celestial-shadow);
}}

/* Mountain geometry using CSS clip-path */
.mtn-far {{
    top: 130%;
    height: 150%;
    background: var(--mtn-far);
    clip-path: polygon(0 100%, 0 35%, 10% 25%, 20% 40%, 35% 15%, 50% 30%, 65% 10%, 80% 35%, 90% 20%, 100% 40%, 100% 100%);
}}

.mtn-mid {{
    top: 240%;
    height: 150%;
    background: var(--mtn-mid);
    clip-path: polygon(0 100%, 0 45%, 25% 20%, 50% 50%, 75% 15%, 100% 40%, 100% 100%);
}}

.ground {{
    top: 350%;
    height: 150%;
    background: var(--ground);
    clip-path: polygon(0 100%, 0 15%, 40% 5%, 70% 10%, 100% 0%, 100% 100%);
    box-shadow: inset 0 20px 50px rgba(0,0,0,0.5);
}}

.text-layer {{
    text-align: center;
    padding: 0 5%;
    display: flex;
    justify-content: center;
    align-items: center;
}}

.text-layer h2 {{
    font-size: calc(var(--width) * 0.08);
    font-weight: 800;
    color: var(--text-color);
    -webkit-text-stroke: var(--text-stroke);
    text-shadow: 0 10px 40px var(--accent), 0 0 5px #000;
    text-transform: uppercase;
    line-height: 1.1;
    margin: 0;
}}

.text-1 {{ top: 30%; }}
.text-2 {{ top: 220%; }}
.text-3 {{ top: 320%; }}

/* The Subject */
.cat-container {{
    position: absolute;
    left: 50%;
    top: 0;
    z-index: 100;
    will-change: transform;
}}

.cat {{
    display: flex;
    flex-direction: column;
    align-items: center;
    font-size: calc(var(--width) * 0.08);
    animation: sway 3s ease-in-out infinite;
    transform-origin: top center;
    filter: drop-shadow(0 15px 15px rgba(0,0,0,0.6));
}}

.parachute {{ margin-bottom: -0.25em; z-index: 2; }}
.kitty {{ font-size: 0.8em; z-index: 1; }}

@keyframes sway {{
    0%, 100% {{ transform: rotate(-8deg); }}
    50% {{ transform: rotate(8deg); }}
}}

.scroll-hint {{
    position: absolute;
    bottom: 5%;
    left: 50%;
    transform: translateX(-50%);
    text-align: center;
    color: #fff;
    font-weight: 600;
    font-size: calc(var(--width) * 0.025);
    transition: opacity 0.3s;
    text-shadow: 0 2px 10px #000;
}}

.scroll-hint .arrow {{
    margin-top: 5px;
    animation: bounce 1.5s infinite;
}}

@keyframes bounce {{
    0%, 100% {{ transform: translateY(0); }}
    50% {{ transform: translateY(10px); }}
}}
"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cinematic Parallax Component</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="component-wrapper">
        <div class="parallax-viewport" id="viewport">
            <div class="parallax-scene">
                <!-- Parallax Layers -->
                <div class="layer stars" data-speed="0.1"></div>
                <div class="layer celestial" data-speed="0.25"></div>
                <div class="layer mtn-far" data-speed="0.5"></div>
                <div class="layer mtn-mid" data-speed="0.7"></div>
                
                <div class="layer text-layer text-1" data-speed="0.8">
                    <h2>{title_text}</h2>
                </div>
                
                <div class="layer text-layer text-2" data-speed="1.2">
                    <h2>{body_text}</h2>
                </div>

                <div class="layer ground" data-speed="1.0"></div>

                <div class="layer text-layer text-3" data-speed="1.0">
                    <h2>HI MOM!</h2>
                </div>

                <!-- Sticky Subject -->
                <div class="cat-container" id="cat-rig">
                    <div class="cat">
                        <div class="parachute">🪂</div>
                        <div class="kitty">🐈</div>
                    </div>
                </div>
                
                <div class="scroll-hint" id="scroll-hint">
                    <div>Scroll Down</div>
                    <div class="arrow">↓</div>
                </div>
            </div>
            
            <!-- Proxy to force the scrollbar without pushing content -->
            <div class="scroll-spacer"></div>
        </div>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    js = f"""// Parallax Physics Engine
document.addEventListener('DOMContentLoaded', () => {{
    const viewport = document.getElementById('viewport');
    const layers = document.querySelectorAll('.layer');
    const catRig = document.getElementById('cat-rig');
    const scrollHint = document.getElementById('scroll-hint');
    
    // Lerp state variables
    let currentY = 0;
    let targetY = 0;
    
    // Capture scroll events from the encapsulated viewport
    viewport.addEventListener('scroll', () => {{
        targetY = viewport.scrollTop;
    }});

    function renderEngine() {{
        // Linear interpolation for buttery smooth movement
        currentY += (targetY - currentY) * 0.08; 
        
        const vh = viewport.clientHeight;
        const scrollProgress = currentY / vh; // 0.0 to 3.0
        
        // Hide scroll hint automatically
        if (currentY > vh * 0.1) {{
            scrollHint.style.opacity = '0';
        }} else {{
            scrollHint.style.opacity = '1';
        }}
        
        // Update generic backgrounds and texts
        layers.forEach(layer => {{
            const speed = parseFloat(layer.getAttribute('data-speed'));
            const yPos = -(currentY * speed);
            layer.style.transform = `translate3d(0, ${{yPos}}px, 0)`;
        }});
        
        // Scripted narrative logic for the Parachuting Subject
        let catYPercent;
        
        if (scrollProgress < 1.0) {{
            // Phase 1: Descending slowly into view
            catYPercent = 20 + (scrollProgress * 30); 
        }} else if (scrollProgress < 2.8) {{
            // Phase 2: Sticky focal point (holds at 50% screen height)
            catYPercent = 50;
        }} else {{
            // Phase 3: Landing firmly on the ground
            // Ground layer is moving up at 1.0x speed, so the cat must move up matching it
            catYPercent = 50 - ((scrollProgress - 2.8) * 100); 
        }}
        
        // Convert percentage height to pixels relative to the container
        const catPx = (catYPercent / 100) * vh;
        
        // Apply transform. Note the -50% centers the rigid body horizontally.
        catRig.style.transform = `translate3d(-50%, ${{catPx}}px, 0)`;
        
        requestAnimationFrame(renderEngine);
    }}
    
    // Initialize loop
    renderEngine();
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
```