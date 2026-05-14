def create_component(
    output_dir: str,
    title_text: str = "Unpredictable Weather Ready",
    body_text: str = "Scroll down to experience GSAP-style staggered reveals, 3D interactive product cards, and a dynamic tracking cursor.",
    color_scheme: str = "light",        
    accent_color: str = "#eab308",     
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the GSAP-Style Interactive Showcase.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Theme derivation
    if color_scheme == "dark":
        bg_color = "#0d111c"
        text_color = "#ffffff"
        surface_color = "rgba(255, 255, 255, 0.05)"
        cursor_bg_default = "#ffffff"
        cursor_text_default = "#0d111c"
    else:
        bg_color = "#f8f9fa"
        text_color = "#111827"
        surface_color = "#ffffff"
        cursor_bg_default = "#111827"
        cursor_text_default = "#ffffff"

    # === CSS ===
    css = f"""/* GSAP-Style Interactive Showcase */
:root {{
    --bg: {bg_color};
    --text: {text_color};
    --accent: {accent_color};
    --surface: {surface_color};
    --cursor-bg: {cursor_bg_default};
    --cursor-text: {cursor_text_default};
    --width: {width_px}px;
    --height: {height_px}px;
}}

*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: 'Inter', system-ui, sans-serif;
    background: #000;
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 100vh;
    overflow: hidden;
}}

.container {{
    width: var(--width);
    height: var(--height);
    max-width: 100vw;
    max-height: 100vh;
    background: var(--bg);
    color: var(--text);
    position: relative;
    overflow-y: auto;
    overflow-x: hidden;
    border-radius: 12px;
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
    scrollbar-width: none; /* Clean aesthetic */
}}
.container::-webkit-scrollbar {{ display: none; }}

/* === Layout Sections === */
.hero {{
    min-height: 80vh;
    display: flex;
    flex-direction: column;
    justify-content: center;
    padding: 10% 8%;
}}

.subtitle {{
    color: var(--accent);
    font-weight: 700;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 1rem;
}}

.title {{
    font-size: clamp(3rem, 6vw, 5rem);
    line-height: 1.1;
    margin-bottom: 1.5rem;
    font-weight: 800;
}}

.body-text {{
    font-size: 1.25rem;
    max-width: 600px;
    opacity: 0.8;
    line-height: 1.6;
}}

.scroll-indicator {{
    margin-top: 4rem;
    font-weight: 600;
    font-size: 0.9rem;
    letter-spacing: 1px;
    text-transform: uppercase;
    opacity: 0.5;
    animation: bounce 2s infinite;
}}

@keyframes bounce {{
    0%, 20%, 50%, 80%, 100% {{ transform: translateY(0); }}
    40% {{ transform: translateY(-10px); }}
    60% {{ transform: translateY(-5px); }}
}}

.content-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 2.5rem;
    padding: 5% 8% 15% 8%;
}}

/* === 3D Interactive Cards === */
.card {{
    height: 420px;
    perspective: 1000px; /* Required for 3D tilt */
}}

.card-inner {{
    background: var(--surface);
    border-radius: 16px;
    overflow: hidden;
    box-shadow: 0 20px 40px rgba(0,0,0,0.06);
    display: flex;
    flex-direction: column;
    height: 100%;
    /* Transition applied via JS for smoothing */
}}

.card-image {{
    height: 55%;
    width: 100%;
}}

.card-info {{
    padding: 2rem;
    display: flex;
    flex-direction: column;
    justify-content: center;
    height: 45%;
}}

.card-info h3 {{
    font-size: 1.5rem;
    margin-bottom: 0.5rem;
}}

.card-info p {{
    opacity: 0.7;
    line-height: 1.5;
}}

/* === Core Animations (GSAP Mimicry) === */
.split-text span {{
    display: inline-block;
    opacity: 0;
    transform: translateY(40px) scale(0.95);
    /* Spring-like easing */
    transition: opacity 0.6s ease, transform 0.8s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}}
.split-text.is-visible span {{
    opacity: 1;
    transform: translateY(0) scale(1);
}}

.reveal-on-scroll {{
    opacity: 0;
    transform: translateY(60px);
    transition: opacity 0.8s ease, transform 1s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}}
.reveal-on-scroll.is-visible {{
    opacity: 1;
    transform: translateY(0);
}}

.delay-1 {{ transition-delay: 0.1s; }}
.delay-2 {{ transition-delay: 0.2s; }}
.delay-3 {{ transition-delay: 0.3s; }}
.delay-4 {{ transition-delay: 0.4s; }}

/* === Dynamic Custom Cursor === */
.has-cursor {{
    cursor: none !important;
}}

.custom-cursor {{
    position: fixed;
    top: 0; left: 0;
    width: 90px;
    height: 90px;
    border-radius: 50%;
    background: var(--cursor-bg);
    color: var(--cursor-text);
    font-size: 0.85rem;
    font-weight: 600;
    letter-spacing: 0.5px;
    text-transform: uppercase;
    display: flex;
    align-items: center;
    justify-content: center;
    pointer-events: none;
    z-index: 9999;
    /* Scale logic */
    transform: translate(-50%, -50%) scale(0);
    opacity: 0;
    /* Transition scale and color, but NOT top/left (JS handles that smoothly) */
    transition: transform 0.4s cubic-bezier(0.34, 1.56, 0.64, 1), 
                opacity 0.3s ease, 
                background-color 0.3s ease,
                color 0.3s ease;
    will-change: transform, top, left;
}}

.custom-cursor.active {{
    transform: translate(-50%, -50%) scale(1);
    opacity: 1;
}}
"""

    # === HTML ===
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Interactive Showcase</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        <!-- Hero Section -->
        <section class="hero">
            <h4 class="reveal-on-scroll subtitle">Featured Collection</h4>
            <h1 class="split-text title">{title_text}</h1>
            <p class="reveal-on-scroll delay-1 body-text">{body_text}</p>
            <div class="scroll-indicator reveal-on-scroll delay-2">↓ Scroll to explore</div>
        </section>
        
        <!-- Interactive Grid -->
        <section class="content-grid">
            <div class="card reveal-on-scroll delay-1 has-cursor" data-cursor-text="Explore" data-cursor-bg="var(--accent)" data-cursor-color="#000">
                <div class="card-inner">
                    <div class="card-image" style="background: linear-gradient(135deg, #11998e, #38ef7d);"></div>
                    <div class="card-info">
                        <h3>Spring Collection</h3>
                        <p>Breathable fabrics engineered for changing seasons.</p>
                    </div>
                </div>
            </div>
            
            <div class="card reveal-on-scroll delay-2 has-cursor" data-cursor-text="Shop Now">
                <div class="card-inner">
                    <div class="card-image" style="background: linear-gradient(135deg, #FF416C, #FF4B2B);"></div>
                    <div class="card-info">
                        <h3>Summer Essentials</h3>
                        <p>Lightweight, vibrant styles that breathe naturally.</p>
                    </div>
                </div>
            </div>
            
            <div class="card reveal-on-scroll delay-1 has-cursor" data-cursor-text="View" data-cursor-bg="#000" data-cursor-color="#fff">
                <div class="card-inner">
                    <div class="card-image" style="background: linear-gradient(135deg, #8E2DE2, #4A00E0);"></div>
                    <div class="card-info">
                        <h3>Autumn Fashion</h3>
                        <p>Stay warm and stylish with premium layering.</p>
                    </div>
                </div>
            </div>
            
            <div class="card reveal-on-scroll delay-2 has-cursor" data-cursor-text="Pre-order" data-cursor-bg="var(--accent)" data-cursor-color="#000">
                <div class="card-inner">
                    <div class="card-image" style="background: linear-gradient(135deg, #2980B9, #6DD5FA);"></div>
                    <div class="card-info">
                        <h3>Winter Wear</h3>
                        <p>Total insulation. Unpredictable weather ready.</p>
                    </div>
                </div>
            </div>
        </section>

        <!-- Dynamic Tracking Cursor -->
        <div class="custom-cursor">
            <span class="cursor-text"></span>
        </div>
    </div>
    
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = """document.addEventListener('DOMContentLoaded', () => {
    const container = document.querySelector('.container');

    // --- 1. Dynamic Text Splitting ---
    // Wraps individual words in spans to allow staggered CSS animations
    const splitTextElements = document.querySelectorAll('.split-text');
    splitTextElements.forEach(el => {
        const text = el.innerText.trim();
        el.innerHTML = '';
        const words = text.split(/\s+/);
        words.forEach((word, i) => {
            const span = document.createElement('span');
            span.innerText = word;
            span.style.transitionDelay = `${i * 0.06}s`;
            el.appendChild(span);
            el.appendChild(document.createTextNode(' ')); // preserve spacing
        });
    });

    // --- 2. Scroll-Triggered Reveal (Intersection Observer) ---
    const observerOptions = {
        root: container,
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('is-visible');
                observer.unobserve(entry.target); // Trigger only once
            }
        });
    }, observerOptions);

    document.querySelectorAll('.reveal-on-scroll, .split-text').forEach(el => observer.observe(el));

    // --- 3. Dynamic Tracking Cursor (LERP smoothing) ---
    const cursor = document.querySelector('.custom-cursor');
    const cursorText = document.querySelector('.cursor-text');
    
    let mouseX = window.innerWidth / 2;
    let mouseY = window.innerHeight / 2;
    let cursorX = mouseX;
    let cursorY = mouseY;

    // Track mouse coordinates (relative to viewport)
    container.addEventListener('mousemove', (e) => {
        mouseX = e.clientX;
        mouseY = e.clientY;
    });

    // RequestAnimationFrame loop for silky smooth physics drag
    function renderCursor() {
        cursorX += (mouseX - cursorX) * 0.15; // LERP factor
        cursorY += (mouseY - cursorY) * 0.15;
        cursor.style.left = `${cursorX}px`;
        cursor.style.top = `${cursorY}px`;
        requestAnimationFrame(renderCursor);
    }
    renderCursor();

    // Contextual Hover Logic
    document.querySelectorAll('.has-cursor').forEach(el => {
        el.addEventListener('mouseenter', () => {
            cursorText.innerText = el.getAttribute('data-cursor-text') || 'View';
            
            // Dynamic thematic coloring
            cursor.style.backgroundColor = el.dataset.cursorBg || 'var(--cursor-bg)';
            cursor.style.color = el.dataset.cursorColor || 'var(--cursor-text)';
            
            cursor.classList.add('active');
        });
        
        el.addEventListener('mouseleave', () => {
            cursor.classList.remove('active');
        });
    });

    // --- 4. 3D Hover Tilt Effect ---
    const cards = document.querySelectorAll('.card');
    cards.forEach(card => {
        const inner = card.querySelector('.card-inner');
        
        card.addEventListener('mouseenter', () => {
            // Remove smoothing temporarily to prevent math jitter on entry
            inner.style.transition = 'transform 0.1s ease-out';
        });
        
        card.addEventListener('mousemove', (e) => {
            const rect = card.getBoundingClientRect();
            const x = e.clientX - rect.left; // x position within element
            const y = e.clientY - rect.top;  // y position within element
            
            const centerX = rect.width / 2;
            const centerY = rect.height / 2;
            
            // Calculate rotation degrees (max 8 degrees tilt)
            const rotateX = ((y - centerY) / centerY) * -8;
            const rotateY = ((x - centerX) / centerX) * 8;
            
            inner.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) scale3d(1.02, 1.02, 1.02)`;
        });
        
        card.addEventListener('mouseleave', () => {
            // Restore smooth transition for the snap-back to origin
            inner.style.transition = 'transform 0.6s cubic-bezier(0.25, 0.46, 0.45, 0.94)';
            inner.style.transform = `perspective(1000px) rotateX(0deg) rotateY(0deg) scale3d(1, 1, 1)`;
        });
    });
});
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
