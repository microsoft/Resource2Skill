def create_component(
    output_dir: str,
    title_text: str = "Award-Winning Digital Experience",
    body_text: str = "We craft immersive web experiences using advanced motion design, typography, and interactive physics.",
    color_scheme: str = "dark",
    accent_color: str = "#ccff00",
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Interactive Agency Showcase.
    Utilizes Text Splitting, Sticky Position, Viewport Detection, Easing, Map Functions, and Lerp.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    if color_scheme == "dark":
        bg_color = "#0a0a0c"
        text_color = "#f4f4f5"
        surface_color = "rgba(255, 255, 255, 0.03)"
        glass_border = "rgba(255, 255, 255, 0.08)"
    else:
        bg_color = "#f4f4f5"
        text_color = "#0a0a0c"
        surface_color = "rgba(0, 0, 0, 0.03)"
        glass_border = "rgba(0, 0, 0, 0.08)"

    css = f"""/* Typography & Reset */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&display=swap');

*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --text: {text_color};
    --accent: {accent_color};
    --surface: {surface_color};
    --glass-border: {glass_border};
}}

body {{
    font-family: 'Inter', sans-serif;
    background-color: var(--bg);
    color: var(--text);
    overflow-x: hidden;
    /* Subtle radial gradient to enhance glass effect */
    background-image: radial-gradient(circle at 50% 0%, rgba(255,255,255,0.03) 0%, transparent 70%);
}}

/* Spacer to allow scrolling to reach the component */
.scroll-spacer {{
    height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.2rem;
    opacity: 0.4;
    text-transform: uppercase;
    letter-spacing: 2px;
}}

/* Technique 3: Sticky Position */
.award-showcase-wrapper {{
    height: 400vh; /* Determines how long the animation lasts */
    position: relative;
}}

.sticky-container {{
    position: sticky;
    top: 0;
    height: 100vh;
    width: 100%;
    overflow: hidden;
    display: flex;
    align-items: center;
    justify-content: center;
}}

/* Content Lockup */
.text-content {{
    position: relative;
    z-index: 10;
    text-align: center;
    max-width: 1000px;
    padding: 0 2rem;
    pointer-events: none;
}}

.title {{
    font-size: clamp(3rem, 8vw, 7rem);
    font-weight: 900;
    line-height: 1.05;
    letter-spacing: -0.03em;
    margin-bottom: 1.5rem;
    text-transform: uppercase;
}}

.body-text {{
    font-size: clamp(1.1rem, 2vw, 1.5rem);
    font-weight: 400;
    opacity: 0;
    transform: translateY(20px);
    transition: opacity 1s ease, transform 1s ease;
    max-width: 600px;
    margin: 0 auto;
}}

.text-content.is-visible .body-text {{
    opacity: 0.7;
    transform: translateY(0);
}}

/* Technique 5: Text Splitting CSS */
.word {{
    display: inline-block;
    overflow: hidden;
    vertical-align: top;
}}

.word-inner {{
    display: inline-block;
    transform: translateY(110%);
    opacity: 0;
    /* Technique 4: Easing (Snappy easeOutExpo equivalent) */
    transition: transform 1.2s cubic-bezier(0.19, 1, 0.22, 1), opacity 1.2s cubic-bezier(0.19, 1, 0.22, 1);
}}

.text-content.is-visible .word-inner {{
    transform: translateY(0);
    opacity: 1;
}}

/* Abstract Geometric Cards (Parallax Elements) */
.card {{
    position: absolute;
    will-change: transform;
    border-radius: 32px;
}}

.card-1 {{
    width: 280px;
    height: 380px;
    background-color: var(--accent);
    top: 50%;
    left: 50%;
    /* Initial offset handled by JS mapRange, but we set starting center */
    margin-top: -190px;
    margin-left: -140px;
    z-index: 5;
    box-shadow: 0 24px 48px rgba(0,0,0,0.2);
}}

.card-2 {{
    width: 450px;
    height: 280px;
    background-color: var(--surface);
    backdrop-filter: blur(24px);
    -webkit-backdrop-filter: blur(24px);
    border: 1px solid var(--glass-border);
    top: 50%;
    left: 50%;
    margin-top: -140px;
    margin-left: -225px;
    z-index: 15;
    border-radius: 40px;
}}

.card-3 {{
    width: 200px;
    height: 200px;
    border: 2px dashed var(--text);
    opacity: 0.2;
    border-radius: 50%;
    top: 50%;
    left: 50%;
    margin-top: -100px;
    margin-left: -100px;
    z-index: 2;
}}
"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Agency Animation Showcase</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>

    <div class="scroll-spacer">
        <span>Scroll Down ↓</span>
    </div>

    <!-- Wrapper dictates scroll duration -->
    <div class="award-showcase-wrapper">
        <!-- Sticky container holds the viewport -->
        <div class="sticky-container">
            
            <!-- Floating Parallax Cards -->
            <div class="card card-1"></div>
            <div class="card card-2"></div>
            <div class="card card-3"></div>

            <!-- Typography Lockup -->
            <div class="text-content">
                <h1 class="title split-target">{title_text}</h1>
                <p class="body-text">{body_text}</p>
            </div>

        </div>
    </div>

    <div class="scroll-spacer">
        <span>End of Sequence</span>
    </div>

    <script src="script.js"></script>
</body>
</html>"""

    js = f"""document.addEventListener('DOMContentLoaded', () => {{
    
    // --- Technique 5: Text Splitting ---
    const splitTarget = document.querySelector('.split-target');
    const text = splitTarget.innerText;
    const words = text.split(' ');
    splitTarget.innerHTML = '';
    
    words.forEach((word, index) => {{
        const outer = document.createElement('span');
        outer.className = 'word';
        
        const inner = document.createElement('span');
        inner.className = 'word-inner';
        inner.innerText = word;
        // Stagger the animation delay for each word
        inner.style.transitionDelay = `${{index * 0.05}}s`;
        
        outer.appendChild(inner);
        splitTarget.appendChild(outer);
        
        // Add space after word
        splitTarget.appendChild(document.createTextNode(' '));
    }});

    const bodyText = document.querySelector('.body-text');
    // Delay body text fade until title is mostly done
    bodyText.style.transitionDelay = `${{words.length * 0.05 + 0.2}}s`;


    // --- Technique 2: Viewport Detection ---
    const textContainer = document.querySelector('.text-content');
    const observer = new IntersectionObserver((entries) => {{
        entries.forEach(entry => {{
            if (entry.isIntersecting) {{
                // Add class to trigger CSS transitions
                textContainer.classList.add('is-visible');
            }}
        }});
    }}, {{ threshold: 0.5 }});
    
    observer.observe(document.querySelector('.sticky-container'));


    // --- Math Utilities ---
    // Bonus 2: Lerp (Linear Interpolation)
    const lerp = (start, end, t) => start * (1 - t) + end * t;
    
    // Bonus 1: Map Function
    const mapRange = (inMin, inMax, outMin, outMax, value) => {{
        return ((value - inMin) * (outMax - outMin)) / (inMax - inMin) + outMin;
    }};


    // --- Technique 1: Scroll Tracking & Animation Loop ---
    const wrapper = document.querySelector('.award-showcase-wrapper');
    const card1 = document.querySelector('.card-1');
    const card2 = document.querySelector('.card-2');
    const card3 = document.querySelector('.card-3');
    
    let targetProgress = 0;
    let currentProgress = 0;

    // Calculate normalized scroll progress (0 to 1) relative to the wrapper
    const calculateScroll = () => {{
        const rect = wrapper.getBoundingClientRect();
        const windowHeight = window.innerHeight;
        const scrollableDistance = rect.height - windowHeight;
        
        // Distance from top of viewport
        let progress = -rect.top / scrollableDistance;
        
        // Clamp between 0 and 1
        targetProgress = Math.max(0, Math.min(1, progress));
    }};

    window.addEventListener('scroll', calculateScroll, {{ passive: true }});
    window.addEventListener('resize', calculateScroll);
    calculateScroll(); // Init

    // Render Loop
    const render = () => {{
        // Apply Lerp to smooth out mouse wheel ticks
        currentProgress = lerp(currentProgress, targetProgress, 0.06);

        const wh = window.innerHeight;
        const ww = window.innerWidth;

        // Map progress to transformations for Card 1 (Solid Accent)
        // Moves from bottom-left to top-right
        const y1 = mapRange(0, 1, wh * 0.4, -wh * 0.4, currentProgress);
        const x1 = mapRange(0, 1, -ww * 0.2, ww * 0.2, currentProgress);
        const r1 = mapRange(0, 1, -15, 35, currentProgress);

        // Map progress for Card 2 (Glassmorphism)
        // Moves from top-right to bottom-left (crosses paths)
        const y2 = mapRange(0, 1, -wh * 0.3, wh * 0.3, currentProgress);
        const x2 = mapRange(0, 1, ww * 0.15, -ww * 0.15, currentProgress);
        const r2 = mapRange(0, 1, 15, -15, currentProgress);

        // Map progress for Card 3 (Dashed Circle)
        // Scales up and rotates
        const y3 = mapRange(0, 1, wh * 0.1, -wh * 0.5, currentProgress);
        const s3 = mapRange(0, 1, 0.8, 2, currentProgress);
        const r3 = mapRange(0, 1, 0, 180, currentProgress);

        // Apply transformations using translate3d for GPU acceleration
        card1.style.transform = `translate3d(${{x1}}px, ${{y1}}px, 0) rotate(${{r1}}deg)`;
        card2.style.transform = `translate3d(${{x2}}px, ${{y2}}px, 0) rotate(${{r2}}deg)`;
        card3.style.transform = `translate3d(0, ${{y3}}px, 0) scale(${{s3}}) rotate(${{r3}}deg)`;

        requestAnimationFrame(render);
    }};

    // Start loop
    requestAnimationFrame(render);
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
