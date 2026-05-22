def create_component(
    output_dir: str,
    title_text: str = "Hydration, Anytime, Anywhere",
    body_text: str = "Stay refreshed with our premium water bottles designed for durability, style, and sustainability.",
    color_scheme: str = "dark",
    accent_color: str = "#2b7a3e",
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Smooth Parallax Hero Animation.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Derive theme configurations
    if color_scheme == "dark":
        text_color = "#ffffff"
        bg_inverse = "#000000"
        bg_url = "https://images.unsplash.com/photo-1542273917363-3b1817f69a2d?auto=format&fit=crop&q=80&w=2000"
        overlay_start = "rgba(0,0,0,0.1)"
        overlay_end = "rgba(0,0,0,0.9)"
    else:
        text_color = "#111111"
        bg_inverse = "#ffffff"
        bg_url = "https://images.unsplash.com/photo-1445264718234-a623be589d37?auto=format&fit=crop&q=80&w=2000"
        overlay_start = "rgba(255,255,255,0.7)"
        overlay_end = "rgba(255,255,255,1)"

    # HTML
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Parallax Hero Animation</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="demo-container">
        <div class="scroll-track">
            <div class="sticky-frame">
                <!-- Background Layer -->
                <div class="bg-image"></div>
                <div class="overlay"></div>
                
                <!-- Navbar -->
                <header class="navbar">
                    <div class="hamburger"></div>
                    <button class="btn nav-btn">Order Now</button>
                </header>

                <!-- Initial Centered Text -->
                <div class="text-group initial-text">
                    <h1>{title_text}</h1>
                    <p>{body_text}</p>
                    <button class="btn">Order Now</button>
                </div>

                <!-- Secondary Left-Aligned Text -->
                <div class="text-group second-text">
                    <h2>Elevate Your<br>Hydration Game</h2>
                    <p>Meet the ultimate companion for your daily adventures. Crafted for style, durability, and a lifetime of performance. The future of hydration is here.</p>
                    <button class="btn">Learn More</button>
                </div>

                <!-- Product Layer (Pure CSS Bottle) -->
                <div class="bottle-container">
                    <div class="bottle">
                        <div class="bottle-cap">
                            <div class="bottle-ring"></div>
                        </div>
                        <div class="bottle-highlight"></div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # CSS
    css = f"""/* Base & Variables */
:root {{
    --text: {text_color};
    --bg-inverse: {bg_inverse};
    --accent: {accent_color};
    --width: {width_px}px;
    --height: {height_px}px;
}}

*, *::before, *::after {{
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background: #0d0d12;
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
}}

/* Scroll Container Setup */
.demo-container {{
    width: var(--width);
    height: var(--height);
    max-width: 100vw;
    max-height: 100vh;
    overflow-y: auto;
    position: relative;
    background: var(--bg-inverse);
    container-type: size;
    border-radius: 12px;
    box-shadow: 0 30px 80px rgba(0,0,0,0.6);
}}

.demo-container::-webkit-scrollbar {{ width: 6px; }}
.demo-container::-webkit-scrollbar-track {{ background: transparent; }}
.demo-container::-webkit-scrollbar-thumb {{ background: var(--accent); border-radius: 3px; }}

.scroll-track {{
    height: 400%; /* Creates the scrolling distance (3 additional screens) */
    width: 100%;
}}

.sticky-frame {{
    position: sticky;
    top: 0;
    width: 100cqw;
    height: 100cqh; /* Matches exact container viewport height */
    overflow: hidden;
}}

/* Environment */
.bg-image {{
    position: absolute;
    top: -15%; left: -15%;
    width: 130%; height: 130%;
    background: url('{bg_url}') center/cover no-repeat;
    transform-origin: center top;
    will-change: transform, filter;
}}

.overlay {{
    position: absolute;
    inset: 0;
    background: linear-gradient(to bottom, {overlay_start} 0%, {overlay_end} 100%);
    pointer-events: none;
}}

/* UI Elements */
.navbar {{
    position: absolute;
    top: 0; left: 0; right: 0;
    padding: clamp(20px, 4cqw, 40px) clamp(30px, 5cqw, 60px);
    display: flex;
    justify-content: space-between;
    align-items: center;
    z-index: 100;
}}

.hamburger {{
    width: 32px; height: 2px;
    background: var(--text);
    position: relative;
    cursor: pointer;
}}
.hamburger::before, .hamburger::after {{
    content: ''; position: absolute; left: 0;
    width: 100%; height: 100%; background: var(--text);
}}
.hamburger::before {{ top: -10px; }}
.hamburger::after {{ top: 10px; }}

.btn {{
    padding: 14px 32px;
    border: 1px solid rgba(150, 150, 150, 0.5);
    border-radius: 30px;
    background: transparent;
    color: var(--text);
    font-family: inherit;
    font-size: 1rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
    backdrop-filter: blur(5px);
}}
.btn:hover {{
    background: var(--text);
    color: var(--bg-inverse);
    border-color: var(--text);
}}

/* Typography Groups */
.text-group {{
    position: absolute;
    color: var(--text);
    pointer-events: none; /* Prevents hidden text blocking clicks */
}}
.text-group .btn {{
    pointer-events: auto; /* Re-enable for buttons */
    margin-top: 30px;
}}

.initial-text {{
    top: 50%; left: 50%;
    transform: translate(-50%, -50%);
    text-align: center;
    width: 90%;
    max-width: 800px;
    will-change: transform, opacity;
}}
.initial-text h1 {{
    font-size: clamp(2.5rem, 7cqw, 6rem);
    font-weight: 700;
    letter-spacing: -0.03em;
    line-height: 1.1;
    margin-bottom: 24px;
}}
.initial-text p {{
    font-size: clamp(1rem, 2cqw, 1.25rem);
    line-height: 1.6;
    opacity: 0.85;
    max-width: 600px;
    margin: 0 auto;
}}

.second-text {{
    top: 35%; left: 10%;
    max-width: 400px;
    opacity: 0;
    transform: translateY(50px);
    will-change: transform, opacity;
}}
.second-text h2 {{
    font-size: clamp(2rem, 5cqw, 4.5rem);
    font-weight: 700;
    letter-spacing: -0.02em;
    line-height: 1.1;
    margin-bottom: 20px;
}}
.second-text p {{
    font-size: clamp(0.9rem, 1.5cqw, 1.1rem);
    line-height: 1.6;
    opacity: 0.85;
}}

/* Product Layer (CSS Art) */
.bottle-container {{
    position: absolute;
    left: 50%; top: 50%;
    /* Offset centering based on intrinsic size */
    margin-left: -60px; 
    margin-top: -175px; 
    transform-origin: center center;
    will-change: transform;
    z-index: 10;
}}

.bottle {{
    width: 120px;
    height: 350px;
    background-color: var(--accent);
    border-radius: 40px 40px 15px 15px;
    position: relative;
    /* Inset shadows create the cylindrical 3D effect over a flat background */
    box-shadow: inset -22px 0 30px rgba(0,0,0,0.65),
                inset 15px 0 20px rgba(255,255,255,0.35),
                inset -5px 0 10px rgba(0,0,0,0.3),
                0 40px 60px rgba(0,0,0,0.8);
}}

.bottle-cap {{
    position: absolute;
    top: -60px; left: 25px;
    width: 70px; height: 40px;
    background: linear-gradient(to right, #111, #444, #111);
    border-radius: 8px 8px 0 0;
}}
.bottle-cap::before {{
    content: ''; position: absolute;
    bottom: -20px; left: 10px;
    width: 50px; height: 30px;
    background-color: var(--accent);
    box-shadow: inset -10px 0 15px rgba(0,0,0,0.65),
                inset 5px 0 10px rgba(255,255,255,0.35);
    z-index: -1;
}}

.bottle-ring {{
    position: absolute;
    top: -26px; left: 16px;
    width: 38px; height: 40px;
    border: 6px solid #222;
    border-radius: 50%;
    box-shadow: inset 0 2px 4px rgba(255,255,255,0.1);
    z-index: -2;
}}

.bottle-highlight {{
    position: absolute;
    top: 30px; bottom: 30px; left: 22px;
    width: 8px;
    background: linear-gradient(to bottom, rgba(255,255,255,0.5), rgba(255,255,255,0.05));
    border-radius: 10px;
    filter: blur(2px);
}}
"""

    # JS
    js = f"""document.addEventListener('DOMContentLoaded', () => {{
    const container = document.querySelector('.demo-container');
    const track = document.querySelector('.scroll-track');
    const bg = document.querySelector('.bg-image');
    const t1 = document.querySelector('.initial-text');
    const t2 = document.querySelector('.second-text');
    const bottle = document.querySelector('.bottle-container');

    let ticking = false;

    const updateAnimation = () => {{
        const scrollTop = container.scrollTop;
        const maxScroll = track.offsetHeight - container.offsetHeight;
        let progress = Math.max(0, Math.min(1, scrollTop / maxScroll));

        // 1. Background Environment (Moves slightly up to counter scroll, adding depth. Blurs late)
        let pBg = Math.min(1, progress / 0.85);
        let easeBg = pBg * pBg;
        bg.style.transform = `scale(1.1) translateY(${{easeBg * 8}}%)`;
        bg.style.filter = `blur(${{easeBg * 16}}px)`;

        // 2. Initial Text (Fades out quickly and drifts down)
        let p1 = Math.min(1, progress / 0.35);
        let easeIn1 = p1 * p1;
        t1.style.opacity = 1 - p1;
        t1.style.transform = `translate(-50%, calc(-50% + ${{easeIn1 * 120}}px))`;

        // 3. Product Parallax Focus (Starts small bottom center -> scales up, moves center-right)
        let pb = Math.min(1, Math.max(0, (progress - 0.1) / 0.7));
        let easeOutB = 1 - Math.pow(1 - pb, 3); // Cubic ease out
        
        let bScale = 0.4 + easeOutB * 0.65; // Scale from 0.4x to 1.05x
        const width = container.offsetWidth;
        const height = container.offsetHeight;
        
        const moveX = easeOutB * (width * 0.22); // Drift right by 22% of container width
        const moveY = (height * 0.35) - (easeOutB * height * 0.35); // Start low, end vertically centered
        
        bottle.style.transform = `translate(${{moveX}}px, ${{moveY}}px) scale(${{bScale}}) rotate(${{easeOutB * -5}}deg)`;

        // 4. Secondary Text (Slides in gently from the bottom at the end of the scroll)
        let p2 = Math.max(0, Math.min(1, (progress - 0.55) / 0.45));
        let easeOut2 = 1 - Math.pow(1 - p2, 3);
        t2.style.opacity = p2;
        t2.style.transform = `translateY(${{(1 - easeOut2) * 60}}px)`;

        ticking = false;
    }};

    container.addEventListener('scroll', () => {{
        if (!ticking) {{
            window.requestAnimationFrame(updateAnimation);
            ticking = true;
        }}
    }});
    
    // Trigger initial state
    updateAnimation();
}});
"""

    # Write files
    for fname, content in [("index.html", html), ("style.css", css), ("script.js", js)]:
        path = os.path.join(output_dir, fname)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)

    return {
        "html": html,
        "css": css,
        "js": js,
        "files": [os.path.join(output_dir, f) for f in ["index.html", "style.css", "script.js"]],
    }
