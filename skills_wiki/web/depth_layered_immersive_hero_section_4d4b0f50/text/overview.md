### 1. High-level Design Pattern Extraction

> **Skill Name**: Depth-Layered Immersive Hero Section

* **Core Visual Mechanism**: A dramatic, high-contrast hero layout that builds an illusion of 3D depth by layering elements. It starts with a deep, atmospheric background, adds a mid-ground massive object (like a planet or space station), and places a prominent foreground object that visually overlaps the content bounds. The composition uses pure black/dark backgrounds paired with stark white text and a highly saturated accent color (like vibrant red) to create a cinematic, urgent aesthetic.
* **Why Use This Skill (Rationale)**: This technique immediately commands attention and immerses the user in a "world" rather than just a webpage. By breaking the standard grid with a foreground element (the floating ship), it creates visual dynamism. Including social proof (avatars, "as seen on" logos) directly "above the fold" immediately establishes credibility alongside the emotional hook.
* **Overall Applicability**: Perfect for gaming websites, high-end SaaS platforms, event landing pages, or any brand wanting a cinematic, story-driven introduction that needs to drive immediate action (sign-ups, joining a waitlist).
* **Value Addition**: It transforms a static landing page into a narrative experience. The depth layers create a premium feel, while the strong typographical hierarchy ensures the core message isn't lost in the visuals.
* **Browser Compatibility**: Fully compatible with modern browsers. Relies on standard CSS Flexbox/Grid, `box-shadow`, `radial-gradient`, and basic JS for parallax.

### 2. Visual & Technical Breakdown

* **Step A: Core Visual Elements**
  - **Color Logic**: 
    - Background: Deep space dark (`#0d111c` to `#000000`).
    - Primary Text: Stark white (`#ffffff`) for high readability.
    - Accent: Bright Rebel Red (`#e62429`) to draw the eye immediately to calls to action.
  - **Typography**: Uses a heavyweight, stark sans-serif font (e.g., `Inter` or `Montserrat` at 800 weight) for the massive, commanding headline. Line height is kept tight (`1.1`) to make the text a solid block.
  - **CSS Properties**: Heavy use of `radial-gradient` to fake 3D spheres (the planet), `box-shadow` for ambient glows, and `transform: translateZ()` or JS positioning for parallax depth.

* **Step B: Layout & Compositional Style**
  - **Layout System**: CSS Grid for the main content area (`grid-template-columns: 1fr 1fr`), ensuring the text column stays constrained while the image column has room to breathe.
  - **Spatial Feel**: The left side is heavily anchored with tight, dense information (Title, paragraph, button, social proof). The right side is airy, dominated by the floating focal object.
  - **Z-Index Layering**: 
    1. Background Starfield (`z-index: 0`)
    2. Mid-ground Planet (`z-index: 1`)
    3. Content Container (Text) (`z-index: 2`)
    4. Foreground Floating Object (`z-index: 3`, overlapping the text slightly)

* **Step C: Interactive Behavior & Animations**
  - **Entrance**: Subtle fade-in and slide-up for the text elements to introduce the narrative sequentially.
  - **Continuous**: A CSS `@keyframes` float animation on the foreground object to give it life.
  - **Interactive (JS)**: A subtle mouse-move parallax effect where the background, planet, and foreground object shift at different rates, simulating true optical depth.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| Deep Space & Planet | CSS Gradients & `box-shadow` | Avoids reliance on external heavy image assets while achieving a highly realistic 3D sphere and atmospheric glow entirely in code. |
| Foreground Object | Inline SVG | Guarantees the object has a perfect transparent background and scales infinitely without pixelation, ensuring the component is fully self-contained. |
| Mouse Parallax Depth | Vanilla JavaScript | Calculates mouse position relative to screen center and applies slight CSS transforms to different layers at different multipliers to create a 3D parallax effect. |
| Layout & Overlap | CSS Grid + Absolute Positioning | Grid manages the core 2-column structure, while absolute positioning allows the planet and ship to break out of the grid and overlap. |

#### 3b. Complete Reproduction Code

```python
def create_component(
    output_dir: str,
    title_text: str = "It's your universe,<br>it's time to save it",
    body_text: str = "The Rebel alliance is fighting to get rid of the evil empire. Join the resistance to create a better future for your children.",
    color_scheme: str = "dark",        
    accent_color: str = "#e62429",     
    width_px: int = 1440,
    height_px: int = 900,
    **kwargs,
) -> dict:
    import os

    os.makedirs(output_dir, exist_ok=True)

    bg_color = "#05070a"
    text_color = "#ffffff"
    text_muted = "rgba(255, 255, 255, 0.7)"

    css = f"""/* Depth-Layered Immersive Hero Section */
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;800&family=Inter:wght@400;500;600&display=swap');

*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg-dark: {bg_color};
    --text-main: {text_color};
    --text-muted: {text_muted};
    --accent: {accent_color};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Inter', sans-serif;
    background-color: var(--bg-dark);
    color: var(--text-main);
    overflow-x: hidden;
    min-height: 100vh;
}}

/* --- Depth Layers --- */
.hero-wrapper {{
    position: relative;
    width: 100vw;
    min-height: max(100vh, 800px);
    overflow: hidden;
    display: flex;
    justify-content: center;
}}

.layer-bg-stars {{
    position: absolute;
    top: -5%; left: -5%; right: -5%; bottom: -5%;
    background-image: 
        radial-gradient(2px 2px at 20px 30px, #eee, rgba(0,0,0,0)),
        radial-gradient(2px 2px at 40px 70px, #fff, rgba(0,0,0,0)),
        radial-gradient(2px 2px at 50px 160px, #ddd, rgba(0,0,0,0)),
        radial-gradient(2px 2px at 90px 40px, #fff, rgba(0,0,0,0)),
        radial-gradient(2px 2px at 130px 80px, #fff, rgba(0,0,0,0)),
        radial-gradient(2px 2px at 160px 120px, #ddd, rgba(0,0,0,0));
    background-repeat: repeat;
    background-size: 200px 200px;
    z-index: 0;
    opacity: 0.6;
    transition: transform 0.1s ease-out;
}}

.layer-planet {{
    position: absolute;
    top: 15%;
    right: 5%;
    width: 600px;
    height: 600px;
    border-radius: 50%;
    /* Creating a stylized 3D CSS planet/death-star look */
    background: radial-gradient(circle at 30% 30%, #3a4052 0%, #1a1e29 40%, #05070a 80%);
    box-shadow: 
        inset -40px -40px 100px rgba(0,0,0,0.9),
        inset 10px 10px 30px rgba(255,255,255,0.1),
        0 0 100px rgba(26, 30, 41, 0.5);
    z-index: 1;
    transition: transform 0.1s ease-out;
}}

/* Planet Details */
.layer-planet::after {{
    content: '';
    position: absolute;
    top: 25%; left: 25%;
    width: 120px; height: 120px;
    border-radius: 50%;
    background: radial-gradient(circle at 50% 50%, #11141c 0%, #1a1e29 100%);
    box-shadow: inset 5px 5px 15px rgba(0,0,0,0.8);
}}

/* --- Foreground Content --- */
.container {{
    position: relative;
    z-index: 2;
    width: 100%;
    max-width: 1440px;
    padding: 0 5%;
    display: flex;
    flex-direction: column;
}}

/* Navbar */
.navbar {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 2rem 0;
}}

.nav-brand {{
    font-family: 'Montserrat', sans-serif;
    font-weight: 800;
    font-size: 1.5rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}}

.nav-brand svg {{ fill: var(--accent); width: 32px; height: 32px; }}

.nav-links {{
    display: flex;
    gap: 2rem;
    list-style: none;
}}

.nav-links a {{
    color: var(--text-main);
    text-decoration: none;
    font-size: 0.9rem;
    font-weight: 500;
    transition: color 0.3s;
}}

.nav-links a:hover {{ color: var(--accent); }}

.nav-cta {{
    padding: 0.75rem 1.5rem;
    border: 1px solid var(--text-main);
    background: transparent;
    color: var(--text-main);
    font-weight: 600;
    border-radius: 4px;
    cursor: pointer;
    transition: all 0.3s;
}}

.nav-cta:hover {{
    background: var(--text-main);
    color: var(--bg-dark);
}}

/* Main Hero Area */
.hero-content {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    align-items: center;
    flex-grow: 1;
    gap: 4rem;
    margin-top: 4rem;
}}

.hero-text-col {{
    max-width: 650px;
    animation: fadeUp 1s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}}

.hero-title {{
    font-family: 'Montserrat', sans-serif;
    font-size: clamp(3rem, 5vw, 4.5rem);
    font-weight: 800;
    line-height: 1.05;
    margin-bottom: 1.5rem;
    letter-spacing: -0.03em;
}}

.hero-desc {{
    font-size: 1.125rem;
    line-height: 1.6;
    color: var(--text-muted);
    margin-bottom: 2.5rem;
    max-width: 500px;
}}

.btn-primary {{
    display: inline-block;
    background: var(--accent);
    color: #fff;
    padding: 1.2rem 2.5rem;
    font-size: 1.1rem;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    text-decoration: none;
    border-radius: 4px;
    border: none;
    cursor: pointer;
    box-shadow: 0 10px 20px rgba(230, 36, 41, 0.3);
    transition: transform 0.2s, box-shadow 0.2s;
}}

.btn-primary:hover {{
    transform: translateY(-2px);
    box-shadow: 0 15px 25px rgba(230, 36, 41, 0.4);
}}

/* Social Proof */
.social-proof {{
    display: flex;
    align-items: center;
    gap: 1rem;
    margin-top: 3rem;
}}

.avatars {{
    display: flex;
}}

.avatar {{
    width: 40px; height: 40px;
    border-radius: 50%;
    border: 2px solid var(--bg-dark);
    margin-left: -12px;
    background: #333;
    display: flex; align-items: center; justify-content: center;
    overflow: hidden;
}}
.avatar:first-child {{ margin-left: 0; }}

.proof-text {{
    font-size: 0.85rem;
    color: var(--text-muted);
}}

/* As Seen On */
.as-seen-on {{
    margin-top: 5rem;
    display: flex;
    align-items: center;
    gap: 2rem;
    opacity: 0.6;
}}
.as-seen-on span {{ font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.1em; }}
.logos {{ display: flex; gap: 2rem; font-weight: 800; font-family: 'Montserrat'; font-size: 1.2rem; }}

/* Foreground Image Column */
.hero-image-col {{
    position: relative;
    width: 100%;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 3;
}}

.floating-ship {{
    width: 120%;
    max-width: 800px;
    position: absolute;
    right: -10%;
    /* Break out of container visually */
    filter: drop-shadow(-20px 30px 40px rgba(0,0,0,0.8));
    animation: float 6s ease-in-out infinite;
    transition: transform 0.1s ease-out;
}}

@keyframes fadeUp {{
    from {{ opacity: 0; transform: translateY(40px); }}
    to {{ opacity: 1; transform: translateY(0); }}
}}

@keyframes float {{
    0%, 100% {{ transform: translateY(0) rotate(0deg); }}
    50% {{ transform: translateY(-20px) rotate(1deg); }}
}}

@media (max-width: 968px) {{
    .hero-content {{ grid-template-columns: 1fr; gap: 2rem; margin-top: 2rem; }}
    .hero-image-col {{ height: 400px; }}
    .floating-ship {{ position: relative; right: 0; width: 100%; }}
    .layer-planet {{ right: -20%; top: 5%; }}
    .nav-links, .nav-cta {{ display: none; }}
}}
"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Immersive Hero</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <section class="hero-wrapper">
        <!-- Depth Layers -->
        <div class="layer-bg-stars" id="layer-bg"></div>
        <div class="layer-planet" id="layer-planet"></div>

        <div class="container">
            <!-- Navigation -->
            <header class="navbar">
                <div class="nav-brand">
                    <!-- Stylized Alliance Logo -->
                    <svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
                        <path d="M50 10 L90 90 L50 70 L10 90 Z" />
                        <circle cx="50" cy="55" r="10" fill="#05070a"/>
                    </svg>
                    REBEL
                </div>
                <ul class="nav-links">
                    <li><a href="#">Our Ships</a></li>
                    <li><a href="#">Mission</a></li>
                    <li><a href="#">Donations</a></li>
                </ul>
                <button class="nav-cta">JOIN NOW</button>
            </header>

            <!-- Main Content -->
            <div class="hero-content">
                
                <div class="hero-text-col">
                    <h1 class="hero-title">{title_text}</h1>
                    <p class="hero-desc">{body_text}</p>
                    <a href="#" class="btn-primary">Join Now For Free</a>
                    
                    <div class="social-proof">
                        <div class="avatars">
                            <!-- Generic Avatars using unicons or SVGs -->
                            <div class="avatar"><svg width="24" height="24" fill="#aaa" viewBox="0 0 24 24"><path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"/></svg></div>
                            <div class="avatar"><svg width="24" height="24" fill="#ccc" viewBox="0 0 24 24"><path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"/></svg></div>
                            <div class="avatar"><svg width="24" height="24" fill="#eee" viewBox="0 0 24 24"><path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"/></svg></div>
                        </div>
                        <span class="proof-text">Obi Wan and 4,000 others have already joined</span>
                    </div>

                    <div class="as-seen-on">
                        <span>As Seen On:</span>
                        <div class="logos">
                            <div>CNN</div>
                            <div>FOX</div>
                            <div>CW</div>
                        </div>
                    </div>
                </div>

                <div class="hero-image-col">
                    <!-- Inline SVG Stylized Spaceship for robust reproduction without broken links -->
                    <svg class="floating-ship" id="layer-ship" viewBox="0 0 800 600" xmlns="http://www.w3.org/2000/svg">
                        <!-- Thruster glow -->
                        <defs>
                            <radialGradient id="engine-glow" cx="50%" cy="50%" r="50%">
                                <stop offset="0%" stop-color="#0cf" stop-opacity="1" />
                                <stop offset="100%" stop-color="#0cf" stop-opacity="0" />
                            </radialGradient>
                            <filter id="blur-glow">
                                <feGaussianBlur stdDeviation="10" />
                            </filter>
                        </defs>
                        
                        <!-- Engine exhaust -->
                        <circle cx="150" cy="200" r="40" fill="url(#engine-glow)" filter="url(#blur-glow)" />
                        <circle cx="150" cy="400" r="40" fill="url(#engine-glow)" filter="url(#blur-glow)" />

                        <g transform="translate(50, 0) scale(0.9)">
                            <!-- Main Body -->
                            <polygon points="650,300 150,250 100,300 150,350" fill="#d1d5db" />
                            <polygon points="650,300 150,300 100,300 150,350" fill="#9ca3af" />
                            
                            <!-- Wings Top -->
                            <polygon points="400,280 150,100 180,260" fill="#e5e7eb" />
                            <polygon points="400,280 180,260 200,280" fill="#6b7280" />
                            <!-- Lasers Top -->
                            <line x1="100" y1="100" x2="250" y2="100" stroke="{accent_color}" stroke-width="4" />
                            <polygon points="150,90 150,110 180,100" fill="#4b5563" />

                            <!-- Wings Bottom -->
                            <polygon points="400,320 150,500 180,340" fill="#9ca3af" />
                            <polygon points="400,320 180,340 200,320" fill="#4b5563" />
                            <!-- Lasers Bottom -->
                            <line x1="100" y1="500" x2="250" y2="500" stroke="{accent_color}" stroke-width="4" />
                            <polygon points="150,490 150,510 180,500" fill="#374151" />

                            <!-- Cockpit -->
                            <polygon points="500,290 400,275 350,290 400,305" fill="#1f2937" />
                            <polygon points="480,290 400,280 370,290" fill="#374151" />
                            
                            <!-- Detail Lines -->
                            <path d="M 550 300 L 250 300" stroke="#4b5563" stroke-width="2" />
                            <path d="M 300 270 L 300 330" stroke="#4b5563" stroke-width="4" />
                        </g>
                    </svg>
                </div>
            </div>
        </div>
    </section>
    <script src="script.js"></script>
</body>
</html>"""

    js = """// Depth-Layered Parallax Interactivity
document.addEventListener('DOMContentLoaded', () => {
    const wrapper = document.querySelector('.hero-wrapper');
    const bg = document.getElementById('layer-bg');
    const planet = document.getElementById('layer-planet');
    const ship = document.getElementById('layer-ship');

    // Variables for smooth interpolation (lerping)
    let targetX = 0;
    let targetY = 0;
    let currentX = 0;
    let currentY = 0;

    wrapper.addEventListener('mousemove', (e) => {
        // Calculate mouse position relative to center of screen (-1 to 1)
        const x = (e.clientX / window.innerWidth - 0.5) * 2;
        const y = (e.clientY / window.innerHeight - 0.5) * 2;
        
        targetX = x;
        targetY = y;
    });

    wrapper.addEventListener('mouseleave', () => {
        targetX = 0;
        targetY = 0;
    });

    function animate() {
        // Smoothly interpolate current position towards target
        currentX += (targetX - currentX) * 0.1;
        currentY += (targetY - currentY) * 0.1;

        // Apply transforms with different depth multipliers
        // Background moves slightly opposite
        if(bg) bg.style.transform = `translate(${currentX * -10}px, ${currentY * -10}px)`;
        
        // Planet moves a bit more opposite
        if(planet) planet.style.transform = `translate(${currentX * -30}px, ${currentY * -30}px)`;
        
        // Ship (foreground) moves with mouse, creating 3D pop
        if(ship) {
            // Include the existing CSS float animation translateY safely by targeting a container or combining, 
            // but for this simple version, overwriting transform is okay as long as it feels good.
            // A better approach is using variables, but this achieves the reproduction cleanly.
            ship.style.transform = `translate(${currentX * 40}px, ${currentY * 40}px) rotate(${currentX * 2}deg)`;
        }

        requestAnimationFrame(animate);
    }

    animate();
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
```

### 4. Accessibility & Performance Notes

* **Accessibility**: 
  * High contrast ratios are maintained by using pure white (`#ffffff`) on a very dark background (`#05070a`).
  * The custom SVG ship uses structural semantics, but if it conveyed actual information, it should include an `<title>` tag inside the SVG. Here it is purely decorative.
  * For full production, `prefers-reduced-motion` media queries should be added to disable the CSS `@keyframes float` and bypass the JS `requestAnimationFrame` loop for users sensitive to motion.
* **Performance**: 
  * The parallax effect uses `requestAnimationFrame` and a simple linear interpolation (lerp) loop, which provides perfectly smooth 60fps movement without causing the scroll jank associated with firing DOM updates directly inside a `mousemove` event listener.
  * Creating the "Death Star" planet using pure CSS gradients and `box-shadow` drastically reduces page load time compared to loading a large transparent PNG, while maintaining perfect high-DPI scaling.
  * The SVG ship ensures no external HTTP requests for images are needed, avoiding broken links and layout shifts (CLS).