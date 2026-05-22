def create_component(
    output_dir: str,
    title_text: str = "Step Up Your Style",
    body_text: str = "Explore top-notch sneakers blending style, comfort, and quality for every step ahead!",
    color_scheme: str = "dark",        
    accent_color: str = "#adff2f",     
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Dynamic Floating Product Hero Carousel.
    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Derive theme colors and select appropriate placeholder images for blend modes
    if color_scheme == "dark":
        bg_color = "#0b0c10"
        text_color = "#ffffff"
        text_muted = "#9ca3af"
        surface_color = "rgba(255, 255, 255, 0.1)"
        blend_mode = "screen" # Removes black background from images
        wave_color_2 = "rgba(255,255,255,0.4)"
        images = [
            "https://images.unsplash.com/photo-1542291026-7eec264c27ff?auto=format&fit=crop&w=800&q=80", # Red
            "https://images.unsplash.com/photo-1551107696-a4b0a5f621ce?auto=format&fit=crop&w=800&q=80", # White
            "https://images.unsplash.com/photo-1600185365483-26d7a4cc7519?auto=format&fit=crop&w=800&q=80"  # Orange/Black
        ]
    else:
        bg_color = "#ffffff"
        text_color = "#111827"
        text_muted = "#4b5563"
        surface_color = "rgba(0, 0, 0, 0.08)"
        blend_mode = "multiply" # Removes white background from images
        wave_color_2 = "rgba(0,0,0,0.4)"
        images = [
            "https://images.unsplash.com/photo-1608231387042-66d1773070a5?auto=format&fit=crop&w=800&q=80", # Green
            "https://images.unsplash.com/photo-1595950653106-6c9ebd614d3a?auto=format&fit=crop&w=800&q=80", # Colorful
            "https://images.unsplash.com/photo-1515955656352-a1fa3ffcd111?auto=format&fit=crop&w=800&q=80"  # Blue
        ]

    # === CSS ===
    css = f"""/* Dynamic Floating Product Hero Carousel */
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;800&display=swap');

*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --text: {text_color};
    --text-muted: {text_muted};
    --accent: {accent_color};
    --surface: {surface_color};
    --wave-color-2: {wave_color_2};
    --blend-mode: {blend_mode};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Montserrat', sans-serif;
    background: #111; /* Outer page bg */
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 100vh;
}}

.container {{
    width: var(--width);
    height: var(--height);
    background: var(--bg);
    color: var(--text);
    position: relative;
    display: flex;
    flex-direction: column;
    overflow: hidden;
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
}}

/* Header */
header {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 2rem 3rem;
    z-index: 20;
}}

.logo {{
    font-size: 1.8rem;
    font-weight: 800;
    letter-spacing: -1px;
}}

.logo span {{
    color: var(--accent);
}}

nav {{
    display: flex;
    gap: 2.5rem;
}}

nav a {{
    color: var(--text);
    text-decoration: none;
    font-weight: 500;
    font-size: 1rem;
    transition: color 0.3s ease;
}}

nav a:hover {{
    color: var(--accent);
}}

.cart {{
    font-size: 1.4rem;
    cursor: pointer;
    transition: color 0.3s ease;
}}

.cart:hover {{
    color: var(--accent);
}}

/* Decorative Background */
.bg-lines {{
    position: absolute;
    top: 55%;
    left: 0;
    width: 100%;
    height: 60%;
    transform: translateY(-50%);
    z-index: 1;
    pointer-events: none;
}}

.glow {{
    position: absolute;
    top: 60%;
    left: 50%;
    width: 600px;
    height: 600px;
    background: radial-gradient(circle, var(--accent) 0%, transparent 60%);
    opacity: 0.15;
    transform: translate(-50%, -50%);
    z-index: 0;
    pointer-events: none;
    border-radius: 50%;
}}

/* Hero Section */
.hero {{
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: flex-start;
    position: relative;
    padding-top: 2rem;
}}

.hero-text {{
    text-align: center;
    z-index: 10;
    max-width: 800px;
}}

.hero-text h1 {{
    font-size: 3.5rem;
    font-weight: 800;
    margin-bottom: 1rem;
    letter-spacing: -1px;
}}

.hero-text p {{
    font-size: 1.1rem;
    color: var(--text-muted);
    max-width: 600px;
    margin: 0 auto 2rem;
    line-height: 1.6;
}}

.buttons {{
    display: flex;
    gap: 1.5rem;
    justify-content: center;
}}

.btn {{
    padding: 0.8rem 2.5rem;
    border-radius: 50px;
    font-weight: 600;
    font-size: 1rem;
    cursor: pointer;
    transition: all 0.3s ease;
    text-decoration: none;
    display: inline-flex;
    align-items: center;
    justify-content: center;
}}

.btn-primary {{
    background: var(--accent);
    color: #000; /* Always dark for primary contrast */
    border: 2px solid var(--accent);
    box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2);
}}

.btn-primary:hover {{
    transform: translateY(-3px);
    box-shadow: 0 15px 25px rgba(0, 0, 0, 0.3);
}}

.btn-secondary {{
    background: transparent;
    color: var(--accent);
    border: 2px solid var(--accent);
}}

.btn-secondary:hover {{
    background: var(--accent);
    color: #000;
}}

/* Slider System */
.slider-area {{
    display: flex;
    align-items: center;
    justify-content: center;
    width: 100%;
    max-width: 1000px;
    z-index: 10;
    position: relative;
    margin-top: 2rem;
    flex: 1;
}}

.nav-btn {{
    background: var(--surface);
    color: var(--text);
    border: none;
    width: 50px;
    height: 50px;
    border-radius: 50%;
    font-size: 1.2rem;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    flex-shrink: 0;
}}

.nav-btn:hover {{
    background: var(--accent);
    color: #000;
    transform: scale(1.1);
}}

.slider-container {{
    flex: 1;
    overflow: hidden;
    margin: 0 20px;
    position: relative;
    height: 100%;
    display: flex;
    align-items: center;
}}

.slider-track {{
    display: flex;
    width: 100%;
    transition: transform 0.6s cubic-bezier(0.25, 1, 0.5, 1);
    will-change: transform;
}}

.slide {{
    flex: 0 0 100%;
    display: flex;
    justify-content: center;
    align-items: center;
}}

.slide img {{
    max-width: 90%;
    max-height: 380px;
    object-fit: contain;
    mix-blend-mode: var(--blend-mode);
    filter: drop-shadow(0 20px 30px rgba(0,0,0,0.4));
    transition: transform 0.6s cubic-bezier(0.25, 1, 0.5, 1), opacity 0.6s ease;
    opacity: 0.3;
    transform: scale(0.85) rotate(-5deg);
}}

.slide.active img {{
    opacity: 1;
    transform: scale(1) rotate(0deg);
}}

.slider-dots {{
    display: flex;
    gap: 12px;
    margin-bottom: 3rem;
    z-index: 10;
    position: relative;
}}

.dot {{
    width: 10px;
    height: 10px;
    border-radius: 50%;
    background: var(--surface);
    cursor: pointer;
    transition: all 0.3s ease;
}}

.dot.active {{
    background: var(--accent);
    transform: scale(1.4);
    box-shadow: 0 0 10px var(--accent);
}}
"""

    # === HTML ===
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text}</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        <header>
            <div class="logo">Sneaker<span>X</span></div>
            <nav>
                <a href="#">Home</a>
                <a href="#">Store</a>
                <a href="#">Men</a>
                <a href="#">Women</a>
                <a href="#">Contacts</a>
            </nav>
            <div class="cart">
                <i class="fas fa-shopping-cart"></i>
            </div>
        </header>

        <!-- Decorative Background Elements -->
        <div class="glow"></div>
        <svg class="bg-lines" viewBox="0 0 100 100" preserveAspectRatio="none">
            <path d="M -10 50 C 20 20, 40 80, 60 50 C 80 20, 110 80, 110 50" fill="none" stroke="var(--accent)" stroke-width="4" vector-effect="non-scaling-stroke" />
            <path d="M -10 60 C 30 90, 40 10, 70 50 C 90 80, 110 30, 110 60" fill="none" stroke="var(--wave-color-2)" stroke-width="2" vector-effect="non-scaling-stroke" />
        </svg>

        <main class="hero">
            <div class="hero-text">
                <h1>{title_text}</h1>
                <p>{body_text}</p>
                <div class="buttons">
                    <a href="#" class="btn btn-primary">Open Store</a>
                    <a href="#" class="btn btn-secondary">Explore Now</a>
                </div>
            </div>

            <div class="slider-area">
                <button class="nav-btn prev"><i class="fas fa-chevron-left"></i></button>
                <div class="slider-container">
                    <div class="slider-track">
                        <div class="slide"><img src="{images[0]}" alt="Featured Sneaker 1"></div>
                        <div class="slide"><img src="{images[1]}" alt="Featured Sneaker 2"></div>
                        <div class="slide"><img src="{images[2]}" alt="Featured Sneaker 3"></div>
                    </div>
                </div>
                <button class="nav-btn next"><i class="fas fa-chevron-right"></i></button>
            </div>

            <div class="slider-dots">
                <div class="dot"></div>
                <div class="dot"></div>
                <div class="dot"></div>
            </div>
        </main>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Dynamic Slider Logic
document.addEventListener('DOMContentLoaded', () => {{
    const track = document.querySelector('.slider-track');
    const slides = document.querySelectorAll('.slide');
    const dots = document.querySelectorAll('.dot');
    const prevBtn = document.querySelector('.prev');
    const nextBtn = document.querySelector('.next');

    let currentIndex = 0;
    const totalSlides = slides.length;

    function updateSlider() {{
        // Move track
        track.style.transform = `translateX(-${{currentIndex * 100}}%)`;
        
        // Update slide classes for scaling animation
        slides.forEach((slide, index) => {{
            if (index === currentIndex) {{
                slide.classList.add('active');
            }} else {{
                slide.classList.remove('active');
            }}
        }});

        // Update dot indicators
        dots.forEach((dot, index) => {{
            dot.classList.toggle('active', index === currentIndex);
        }});
    }}

    // Event Listeners for controls
    nextBtn.addEventListener('click', () => {{
        currentIndex = (currentIndex + 1) % totalSlides;
        updateSlider();
        resetAutoPlay();
    }});

    prevBtn.addEventListener('click', () => {{
        currentIndex = (currentIndex - 1 + totalSlides) % totalSlides;
        updateSlider();
        resetAutoPlay();
    }});

    dots.forEach((dot, index) => {{
        dot.addEventListener('click', () => {{
            currentIndex = index;
            updateSlider();
            resetAutoPlay();
        }});
    }});

    // Auto-play functionality
    let autoPlayInterval;
    
    function startAutoPlay() {{
        autoPlayInterval = setInterval(() => {{
            currentIndex = (currentIndex + 1) % totalSlides;
            updateSlider();
        }}, 4000);
    }}

    function resetAutoPlay() {{
        clearInterval(autoPlayInterval);
        startAutoPlay();
    }}

    // Initialization
    updateSlider();
    startAutoPlay();
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
