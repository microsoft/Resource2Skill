def create_component(
    output_dir: str,
    title_text: str = "It's your universe, it's time to save it.",
    body_text: str = "The Alliance is fighting to get rid of the evil empire. Join the resistance to create a better future for your children.",
    color_scheme: str = "dark",
    accent_color: str = "#E62429", # Rebel Red
    width_px: int = 1440,
    height_px: int = 900,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Cinematic Parallax Hero visual effect.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === CSS ===
    css = f"""/* Cinematic Parallax Hero */
:root {{
    --bg-dark: #07090F;
    --bg-light: #1A1A2E;
    --text-main: #FFFFFF;
    --text-muted: #A0AEC0;
    --accent: {accent_color};
    --nav-height: 80px;
}}

* {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: 'Inter', system-ui, sans-serif;
    background: radial-gradient(circle at center, var(--bg-light) 0%, var(--bg-dark) 100%);
    color: var(--text-main);
    overflow-x: hidden;
    min-height: 100vh;
}}

/* Canvas Starfield */
#starfield {{
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    z-index: 0;
    pointer-events: none;
}}

.hero-wrapper {{
    position: relative;
    width: 100%;
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    z-index: 1;
    overflow: hidden;
}}

/* Navigation */
.navbar {{
    height: var(--nav-height);
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0 5%;
    position: relative;
    z-index: 10;
}}

.logo {{
    font-size: 1.25rem;
    font-weight: 800;
    letter-spacing: 1px;
    display: flex;
    align-items: center;
    gap: 10px;
    text-transform: uppercase;
}}

.logo-icon {{
    width: 24px;
    height: 24px;
    fill: var(--accent);
}}

.nav-links {{
    display: flex;
    gap: 32px;
}}

.nav-links a {{
    color: var(--text-main);
    text-decoration: none;
    font-size: 0.9rem;
    font-weight: 500;
    transition: color 0.3s ease;
}}

.nav-links a:hover {{
    color: var(--accent);
}}

.btn-ghost {{
    border: 1px solid rgba(255,255,255,0.3);
    background: transparent;
    color: var(--text-main);
    padding: 10px 24px;
    border-radius: 4px;
    font-weight: 600;
    font-size: 0.9rem;
    cursor: pointer;
    transition: all 0.3s ease;
    text-transform: uppercase;
}}

.btn-ghost:hover {{
    border-color: var(--text-main);
    background: rgba(255,255,255,0.1);
}}

/* Main Hero Content */
.hero-content {{
    flex: 1;
    display: flex;
    align-items: center;
    padding: 0 5%;
    position: relative;
    z-index: 2;
}}

.text-column {{
    max-width: 650px;
    position: relative;
    z-index: 3;
}}

.title {{
    font-size: clamp(3rem, 5vw, 4.5rem);
    font-weight: 900;
    line-height: 1.05;
    margin-bottom: 1.5rem;
    letter-spacing: -1px;
    text-wrap: balance;
}}

.body-text {{
    font-size: clamp(1.1rem, 2vw, 1.25rem);
    color: var(--text-muted);
    line-height: 1.6;
    margin-bottom: 2.5rem;
    max-width: 550px;
}}

/* Call to Action Area */
.cta-group {{
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
    align-items: flex-start;
}}

.btn-primary {{
    background: var(--accent);
    color: #fff;
    border: none;
    padding: 16px 36px;
    font-size: 1rem;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 1px;
    cursor: pointer;
    border-radius: 4px;
    transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
    box-shadow: 0 4px 15px rgba(230, 36, 41, 0.3);
}}

.btn-primary:hover {{
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(230, 36, 41, 0.5);
}}

/* Social Proof */
.social-proof {{
    display: flex;
    align-items: center;
    gap: 16px;
}}

.avatars {{
    display: flex;
}}

.avatar {{
    width: 36px;
    height: 36px;
    border-radius: 50%;
    border: 2px solid var(--bg-dark);
    margin-left: -12px;
    background-color: #333;
    background-size: cover;
    background-position: center;
    box-shadow: 0 2px 5px rgba(0,0,0,0.5);
}}

.avatar:nth-child(1) {{ margin-left: 0; background-image: url('https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?w=100&h=100&fit=crop'); }}
.avatar:nth-child(2) {{ background-image: url('https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=100&h=100&fit=crop'); }}
.avatar:nth-child(3) {{ background-image: url('https://images.unsplash.com/photo-1599566150163-29194dcaad36?w=100&h=100&fit=crop'); }}
.avatar:nth-child(4) {{ background-image: url('https://images.unsplash.com/photo-1527980965255-d3b416303d12?w=100&h=100&fit=crop'); }}

.social-text {{
    font-size: 0.85rem;
    color: var(--text-muted);
    font-weight: 500;
}}

.social-text strong {{
    color: var(--text-main);
}}

/* Floating Depth Elements */
.parallax-layer {{
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    pointer-events: none;
}}

/* Background Planet/Moon */
.bg-planet {{
    position: absolute;
    right: 15%;
    top: 15%;
    width: 300px;
    height: 300px;
    background: radial-gradient(circle at 30% 30%, #4A5568, #1A202C, #000);
    border-radius: 50%;
    box-shadow: inset -20px -20px 50px rgba(0,0,0,0.9), 0 0 40px rgba(255,255,255,0.05);
    z-index: 1;
    filter: blur(1px);
}}

/* Foreground Grid-Breaking Ship (SVG Container) */
.fg-ship {{
    position: absolute;
    right: 5%;
    top: 50%;
    transform: translateY(-50%);
    width: 600px;
    z-index: 4;
    filter: drop-shadow(-20px 30px 40px rgba(0,0,0,0.6));
}}

/* As Seen On Footer */
.as-seen-on {{
    padding: 2rem 5%;
    display: flex;
    align-items: center;
    gap: 2rem;
    position: relative;
    z-index: 2;
    border-top: 1px solid rgba(255,255,255,0.05);
    background: linear-gradient(to top, rgba(0,0,0,0.5), transparent);
}}

.as-seen-text {{
    font-size: 0.8rem;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 1px;
    font-weight: 600;
}}

.logos-container {{
    display: flex;
    gap: 3rem;
    align-items: center;
}}

.partner-logo {{
    height: 24px;
    fill: #fff;
    opacity: 0.4;
    filter: grayscale(100%);
    transition: all 0.3s ease;
}}

.partner-logo:hover {{
    opacity: 1;
    filter: grayscale(0%);
}}

@media (max-width: 1024px) {{
    .fg-ship {{ width: 450px; right: -5%; opacity: 0.8; }}
    .title {{ font-size: 3.5rem; }}
}}

@media (max-width: 768px) {{
    .nav-links {{ display: none; }}
    .fg-ship {{ display: none; /* Hide complex graphic on small screens for readability */ }}
    .text-column {{ max-width: 100%; text-align: center; display: flex; flex-direction: column; align-items: center; }}
    .body-text {{ text-align: center; }}
    .cta-group {{ align-items: center; }}
    .bg-planet {{ right: 50%; transform: translateX(50%); top: 10%; opacity: 0.3; }}
    .logos-container {{ flex-wrap: wrap; gap: 1.5rem; justify-content: center; }}
    .as-seen-on {{ flex-direction: column; text-align: center; gap: 1rem; }}
}}
"""

    # === HTML ===
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Rebel Alliance Hero</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;800;900&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <canvas id="starfield"></canvas>

    <div class="hero-wrapper">
        <!-- Parallax Background Elements -->
        <div class="parallax-layer" data-speed="0.05">
            <div class="bg-planet"></div>
        </div>

        <nav class="navbar">
            <div class="logo">
                <svg class="logo-icon" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                    <path d="M12 2L2 22L12 17L22 22L12 2Z"/>
                </svg>
                Rebel Alliance
            </div>
            <div class="nav-links">
                <a href="#">Our Ships</a>
                <a href="#">Mission</a>
                <a href="#">Donations</a>
            </div>
            <button class="btn-ghost">Sign In</button>
        </nav>

        <main class="hero-content">
            <div class="text-column">
                <h1 class="title">{title_text}</h1>
                <p class="body-text">{body_text}</p>
                
                <div class="cta-group">
                    <button class="btn-primary">Join Now For Free</button>
                    
                    <div class="social-proof">
                        <div class="avatars">
                            <div class="avatar"></div>
                            <div class="avatar"></div>
                            <div class="avatar"></div>
                            <div class="avatar"></div>
                        </div>
                        <span class="social-text"><strong>Obi Wan</strong> and 4,000 others have already joined</span>
                    </div>
                </div>
            </div>

            <!-- Parallax Foreground Element (Grid Breaking) -->
            <div class="parallax-layer fg-ship" data-speed="-0.08">
                <!-- Abstract glowing spacecraft SVG -->
                <svg viewBox="0 0 600 400" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <defs>
                        <linearGradient id="ship-body" x1="0%" y1="0%" x2="100%" y2="100%">
                            <stop offset="0%" stop-color="#E2E8F0" />
                            <stop offset="100%" stop-color="#718096" />
                        </linearGradient>
                        <linearGradient id="engine-glow" x1="0%" y1="50%" x2="100%" y2="50%">
                            <stop offset="0%" stop-color="{accent_color}" stop-opacity="0" />
                            <stop offset="100%" stop-color="{accent_color}" stop-opacity="0.8" />
                        </linearGradient>
                        <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">
                            <feGaussianBlur stdDeviation="8" result="blur" />
                            <feComposite in="SourceGraphic" in2="blur" operator="over" />
                        </filter>
                    </defs>
                    
                    <!-- Engine Trails -->
                    <path d="M50,150 L200,150" stroke="url(#engine-glow)" stroke-width="8" stroke-linecap="round" filter="url(#glow)"/>
                    <path d="M30,250 L180,250" stroke="url(#engine-glow)" stroke-width="8" stroke-linecap="round" filter="url(#glow)"/>
                    
                    <!-- Left Wing -->
                    <path d="M150,150 L450,200 L250,50 Z" fill="url(#ship-body)"/>
                    <!-- Right Wing -->
                    <path d="M130,250 L430,200 L230,350 Z" fill="#4A5568"/>
                    <!-- Central Fuselage -->
                    <path d="M100,200 L550,200 L150,220 Z" fill="#CBD5E0"/>
                    <path d="M100,200 L550,200 L150,180 Z" fill="#EDF2F7"/>
                    <!-- Cockpit -->
                    <path d="M350,195 L420,200 L350,205 Z" fill="#1A202C"/>
                    
                    <!-- Accent Lines -->
                    <path d="M200,170 L300,190" stroke="{accent_color}" stroke-width="3"/>
                    <path d="M180,230 L280,210" stroke="{accent_color}" stroke-width="3"/>
                </svg>
            </div>
        </main>

        <footer class="as-seen-on">
            <span class="as-seen-text">As seen on:</span>
            <div class="logos-container">
                <!-- Generic placeholders for TV logos using SVG shapes and text -->
                <svg class="partner-logo" viewBox="0 0 100 30" xmlns="http://www.w3.org/2000/svg">
                    <text x="0" y="22" font-family="Arial" font-weight="900" font-size="24">NEWS<tspan fill="{accent_color}">X</tspan></text>
                </svg>
                <svg class="partner-logo" viewBox="0 0 100 30" xmlns="http://www.w3.org/2000/svg">
                    <circle cx="15" cy="15" r="10" stroke="white" stroke-width="3" fill="none"/>
                    <text x="35" y="22" font-family="Arial" font-weight="bold" font-size="20">GLOBAL</text>
                </svg>
                <svg class="partner-logo" viewBox="0 0 100 30" xmlns="http://www.w3.org/2000/svg">
                    <rect x="0" y="5" width="20" height="20" fill="white"/>
                    <text x="28" y="22" font-family="Arial" font-style="italic" font-weight="bold" font-size="20">TECH</text>
                </svg>
            </div>
        </footer>
    </div>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Parallax and Starfield logic
document.addEventListener('DOMContentLoaded', () => {{
    
    // --- 1. Mouse Parallax Effect ---
    const parallaxLayers = document.querySelectorAll('.parallax-layer');
    const heroWrapper = document.querySelector('.hero-wrapper');
    
    // Only apply parallax on non-touch devices
    if (window.matchMedia("(pointer: fine)").matches) {{
        heroWrapper.addEventListener('mousemove', (e) => {{
            const x = e.clientX;
            const y = e.clientY;
            const centerX = window.innerWidth / 2;
            const centerY = window.innerHeight / 2;

            parallaxLayers.forEach(layer => {{
                const speed = parseFloat(layer.getAttribute('data-speed'));
                // Calculate movement based on distance from center
                const moveX = (x - centerX) * speed;
                const moveY = (y - centerY) * speed;
                
                // Using transform3d for hardware acceleration
                layer.style.transform = `translate3d(${{moveX}}px, ${{moveY}}px, 0)`;
            }});
        }});
        
        // Reset on mouse leave
        heroWrapper.addEventListener('mouseleave', () => {{
            parallaxLayers.forEach(layer => {{
                layer.style.transform = `translate3d(0px, 0px, 0)`;
                layer.style.transition = 'transform 0.5s ease-out';
            }});
        }});
        
        // Remove transition when moving to prevent lag
        heroWrapper.addEventListener('mouseenter', () => {{
            parallaxLayers.forEach(layer => {{
                layer.style.transition = 'none';
            }});
        }});
    }}

    // --- 2. Canvas Starfield ---
    const canvas = document.getElementById('starfield');
    const ctx = canvas.getContext('2d');
    
    let width, height;
    let stars = [];
    const numStars = 200; // Adjust for density

    function resizeCanvas() {{
        width = window.innerWidth;
        height = window.innerHeight;
        canvas.width = width;
        canvas.height = height;
    }}

    class Star {{
        constructor() {{
            this.reset();
        }}

        reset() {{
            this.x = Math.random() * width;
            this.y = Math.random() * height;
            this.size = Math.random() * 1.5;
            // Stars closer appear to move faster
            this.speed = (Math.random() * 0.5) + 0.1;
            this.alpha = Math.random();
            this.alphaChange = (Math.random() * 0.02) - 0.01;
        }}

        update() {{
            // Move star to the right (simulating forward motion if we pan left)
            this.x += this.speed;
            
            // Twinkle effect
            this.alpha += this.alphaChange;
            if (this.alpha <= 0.1 || this.alpha >= 1) {{
                this.alphaChange = -this.alphaChange;
            }}

            // Loop around
            if (this.x > width) {{
                this.x = 0;
                this.y = Math.random() * height;
            }}
        }}

        draw() {{
            ctx.beginPath();
            ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
            ctx.fillStyle = `rgba(255, 255, 255, ${{this.alpha}})`;
            ctx.fill();
        }}
    }}

    function initStars() {{
        stars = [];
        for (let i = 0; i < numStars; i++) {{
            stars.push(new Star());
        }}
    }}

    function animateStars() {{
        ctx.clearRect(0, 0, width, height);
        stars.forEach(star => {{
            star.update();
            star.draw();
        }});
        requestAnimationFrame(animateStars);
    }}

    // Initialize
    window.addEventListener('resize', () => {{
        resizeCanvas();
        initStars();
    }});
    
    resizeCanvas();
    initStars();
    animateStars();
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
