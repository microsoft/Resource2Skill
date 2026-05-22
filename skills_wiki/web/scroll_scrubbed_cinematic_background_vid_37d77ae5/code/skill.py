def create_component(
    output_dir: str,
    title_text: str = "Cinematic Flow",
    body_text: str = "Scroll down to control time.",
    color_scheme: str = "dark",
    accent_color: str = "#ff2a5f",
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Scroll-Scrubbed Cinematic Background Video effect.
    Uses GSAP ScrollTrigger to tie video playback to scroll position.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    if color_scheme == "dark":
        text_color = "#ffffff"
        ui_bg = "rgba(0, 0, 0, 0.3)"
    else:
        text_color = "#111111"
        ui_bg = "rgba(255, 255, 255, 0.4)"

    # Using a reliable public domain sample video suitable for demonstrating the effect
    video_url = "https://storage.googleapis.com/gtv-videos-bucket/sample/ForBiggerBlazes.mp4"

    css = f"""/* Scroll-Scrubbed Background Video */
:root {{
    --text-color: {text_color};
    --accent: {accent_color};
    --ui-bg: {ui_bg};
}}

* {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body, html {{
    font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    background-color: #000;
    color: var(--text-color);
    /* Prevent horizontal scrolling */
    overflow-x: hidden; 
}}

/* The hidden spacer that creates the scrollable area */
.scroll-spacer {{
    /* The height determines how long the user has to scroll to finish the video */
    height: 400vh; 
    width: 100%;
    position: absolute;
    top: 0;
    left: 0;
    z-index: 0;
}}

/* Fixed container holding all visual elements */
.fixed-viewport {{
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    z-index: 1;
    overflow: hidden;
}}

/* The video itself */
.bg-video {{
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    object-fit: cover;
    z-index: -1;
    /* Optional: add a slight dimming filter if needed for text contrast */
    filter: brightness(0.8);
}}

/* UI Overlay styling */
header {{
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    padding: 2rem 4rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    z-index: 10;
}}

.logo {{
    font-size: 1.5rem;
    font-weight: bold;
    letter-spacing: 2px;
}}

nav ul {{
    list-style: none;
    display: flex;
    gap: 2rem;
}}

nav a {{
    color: var(--text-color);
    text-decoration: none;
    font-size: 0.9rem;
    text-transform: uppercase;
    letter-spacing: 1px;
    transition: color 0.3s ease;
}}

nav a:hover {{
    color: var(--accent);
}}

.hero {{
    position: absolute;
    top: 50%;
    left: 0;
    width: 100%;
    transform: translateY(-50%);
    display: flex;
    justify-content: space-between;
    padding: 0 5vw;
    z-index: 10;
    pointer-events: none; /* Let clicks pass through to video if needed */
}}

.hero-left, .hero-right {{
    width: 45%;
}}

.hero-right {{
    text-align: right;
    display: flex;
    flex-direction: column;
    align-items: flex-end;
    justify-content: center;
}}

h1 {{
    font-size: clamp(3rem, 6vw, 6rem);
    line-height: 1.1;
    font-weight: 800;
    margin-bottom: 1rem;
}}

p {{
    font-size: clamp(1rem, 1.5vw, 1.5rem);
    font-weight: 400;
    opacity: 0.9;
    max-width: 400px;
}}

.scroll-indicator {{
    position: absolute;
    bottom: 3rem;
    left: 4rem;
    display: flex;
    align-items: center;
    gap: 1rem;
    z-index: 10;
}}

.scroll-text {{
    font-size: 0.8rem;
    text-transform: uppercase;
    letter-spacing: 4px;
    writing-mode: vertical-rl;
    transform: rotate(180deg);
    opacity: 0.7;
}}

.scroll-line {{
    width: 1px;
    height: 60px;
    background-color: var(--text-color);
    opacity: 0.5;
}}

/* Loader for when video is buffering metadata */
.loader {{
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    font-size: 1.2rem;
    letter-spacing: 2px;
    z-index: 100;
    color: var(--text-color);
    transition: opacity 0.5s ease;
}}
"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text}</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>

    <!-- Loading state indicator -->
    <div class="loader" id="loader">Loading Video...</div>

    <!-- The tall element that creates scrollable space -->
    <div class="scroll-spacer"></div>

    <!-- The fixed viewport holding the UI and Video -->
    <div class="fixed-viewport">
        <!-- Video element: muted and playsinline are critical for programmatic control -->
        <video 
            id="bg-video" 
            class="bg-video" 
            src="{video_url}" 
            muted 
            playsinline 
            preload="auto"
        ></video>

        <header>
            <div class="logo">BRAND</div>
            <nav>
                <ul>
                    <li><a href="#">Home</a></li>
                    <li><a href="#">Showcase</a></li>
                    <li><a href="#">Specs</a></li>
                    <li><a href="#">Buy</a></li>
                </ul>
            </nav>
        </header>

        <section class="hero">
            <div class="hero-left">
                <h1>{title_text}</h1>
            </div>
            <div class="hero-right">
                <p>{body_text}</p>
            </div>
        </section>

        <div class="scroll-indicator">
            <div class="scroll-line"></div>
            <div class="scroll-text">SCROLL</div>
        </div>
    </div>

    <!-- GSAP Core -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/gsap.min.js"></script>
    <!-- GSAP ScrollTrigger -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/ScrollTrigger.min.js"></script>
    <script src="script.js"></script>
</body>
</html>"""

    js = f"""// Register GSAP Plugin
gsap.registerPlugin(ScrollTrigger);

document.addEventListener('DOMContentLoaded', () => {{
    const video = document.getElementById('bg-video');
    const loader = document.getElementById('loader');

    // It is crucial to wait for the video metadata to load so we know its duration
    video.addEventListener('loadedmetadata', () => {{
        
        // Hide loader once video is ready
        loader.style.opacity = '0';
        setTimeout(() => loader.style.display = 'none', 500);

        // Map scroll position to video time
        gsap.to(video, {{
            currentTime: video.duration, // Animate from 0 to full duration
            ease: "none",                // Linear progression, tied strictly to scroll
            scrollTrigger: {{
                trigger: ".scroll-spacer", // The element determining scroll length
                start: "top top",          // Start animation when top of spacer hits top of viewport
                end: "bottom bottom",      // End animation when bottom of spacer hits bottom of viewport
                scrub: 1,                  // Smooth scrubbing effect (1 second lag)
                markers: false             // Set to true for debugging
            }}
        }});
    }});

    // Fallback: If video is cached, loadedmetadata might have already fired before the event listener was attached
    if (video.readyState >= 1) {{
        // Manually dispatch event to trigger setup
        video.dispatchEvent(new Event('loadedmetadata'));
    }}
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
