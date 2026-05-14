def create_component(
    output_dir: str,
    title_text: str = "ORGANIC JUICE",
    body_text: str = "Scroll down to control time and explore the perfect blend.",
    color_scheme: str = "dark",
    accent_color: str = "#ff4757",
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Scroll-Driven Video Scrubber effect.
    
    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors ===
    if color_scheme == "dark":
        bg_color = "#0a0a0a"
        text_color = "#ffffff"
        tint_color = "rgba(0, 0, 0, 0.5)"
        section_bg = "#111111"
    else:
        bg_color = "#ffffff"
        text_color = "#0a0a0a"
        tint_color = "rgba(255, 255, 255, 0.4)"
        section_bg = "#f8f9fa"

    # === CSS ===
    css = f"""/* Scroll-Driven Video Scrubber */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --text: {text_color};
    --accent: {accent_color};
    --tint: {tint_color};
    --section-bg: {section_bg};
}}

body {{
    font-family: 'Inter', system-ui, sans-serif;
    background: var(--bg);
    color: var(--text);
    overflow-x: hidden;
}}

/* Intro section just to show scroll context */
.intro-section {{
    height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    background: var(--bg);
    padding: 2rem;
    text-align: center;
}}

.intro-section h1 {{
    font-size: clamp(2.5rem, 5vw, 5rem);
    text-transform: uppercase;
    letter-spacing: -0.03em;
    font-weight: 800;
}}

/* The main scroll track containing the video */
.scroll-track {{
    /* 400vh gives us 3 viewport heights worth of scrollable scrubbing space */
    height: 400vh; 
    position: relative;
    width: 100%;
}}

/* The sticky container locks the video to the viewport while inside the track */
.video-container {{
    position: sticky;
    top: 0;
    width: 100%;
    height: 100vh;
    overflow: hidden;
    z-index: 0;
}}

.scrub-video {{
    width: 100%;
    height: 100%;
    object-fit: cover;
    /* Optional: scale slightly to prevent edge artifacts */
    transform: scale(1.02);
}}

.video-tint {{
    position: absolute;
    inset: 0;
    background: var(--tint);
    z-index: 1;
}}

/* Content layered on top of the video */
.content-overlay {{
    position: relative;
    z-index: 2;
    /* Pull the content up over the sticky container */
    margin-top: -100vh;
    pointer-events: none; /* Let clicks pass through if needed */
}}

.screen {{
    height: 100vh;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;
    padding: 2rem;
}}

.screen-content {{
    max-width: 800px;
    background: rgba(0, 0, 0, 0.01);
    backdrop-filter: blur(4px);
    -webkit-backdrop-filter: blur(4px);
    padding: 3rem;
    border-radius: 24px;
    border: 1px solid rgba(255,255,255,0.1);
}}

.title {{
    font-size: clamp(3rem, 6vw, 6rem);
    text-transform: uppercase;
    letter-spacing: -0.02em;
    font-weight: 800;
    margin-bottom: 1rem;
    color: var(--text);
}}

.body-text {{
    font-size: clamp(1.1rem, 2vw, 1.5rem);
    line-height: 1.6;
    color: var(--text);
    opacity: 0.9;
}}

.highlight {{
    color: var(--accent);
}}

/* Normal content block below the track */
.normal-section {{
    min-height: 100vh;
    background: var(--section-bg);
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    position: relative;
    z-index: 3;
    padding: 4rem 2rem;
    text-align: center;
}}

/* Graceful degradation for users who prefer reduced motion */
@media (prefers-reduced-motion: reduce) {{
    .scroll-track {{ height: auto; }}
    .video-container {{ position: relative; height: 60vh; }}
    .content-overlay {{ margin-top: 0; }}
    .screen {{ height: auto; padding: 4rem 2rem; }}
    .scrub-video {{ display: none; }} /* Fallback applied via JS or poster */
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
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>

    <header class="intro-section">
        <div>
            <h1>Scroll Down</h1>
            <p style="opacity: 0.6; margin-top: 1rem;">Begin the experience</p>
        </div>
    </header>

    <main class="scroll-track">
        <div class="video-container">
            <!-- Using a widely available GSAP demo Codepen asset known for good keyframing -->
            <video class="scrub-video" 
                   src="https://assets.codepen.io/39255/output_960.mp4" 
                   muted 
                   playsinline 
                   preload="auto"></video>
            <div class="video-tint"></div>
        </div>
        
        <div class="content-overlay">
            <section class="screen">
                <div class="screen-content">
                    <h2 class="title">{title_text}</h2>
                    <p class="body-text">{body_text}</p>
                </div>
            </section>
            <section class="screen">
                <div class="screen-content">
                    <h2 class="title" style="font-size: clamp(2rem, 4vw, 4rem);">Perfectly <span class="highlight">Synced</span></h2>
                    <p class="body-text">The video is scrubbed forward and backward precisely to your scrollbar.</p>
                </div>
            </section>
            <section class="screen">
                <!-- Empty screen to let the user focus purely on the end of the video animation -->
            </section>
        </div>
    </main>

    <section class="normal-section">
        <h2 class="title" style="font-size: 3rem;">Normal Flow Resumes</h2>
        <p class="body-text" style="max-width: 600px; margin-top: 1rem;">
            Once the scroll track is completed, standard web flow takes over seamlessly.
        </p>
    </section>

    <!-- GSAP & ScrollTrigger CDNs -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/gsap.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/ScrollTrigger.min.js"></script>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = """// Initialize Scroll-Driven Video Scrubber
document.addEventListener('DOMContentLoaded', () => {
    // Respect user motion preferences
    const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    if (prefersReducedMotion) return;

    gsap.registerPlugin(ScrollTrigger);
    
    const video = document.querySelector('.scrub-video');
    const track = document.querySelector('.scroll-track');

    // Function to set up the GSAP tween
    function setupScrub() {
        gsap.to(video, {
            // Animate the currentTime of the video to its total duration
            currentTime: video.duration || 1, 
            ease: "none",
            scrollTrigger: {
                trigger: track,
                start: "top top",     // When the top of track hits top of viewport
                end: "bottom bottom", // When bottom of track hits bottom of viewport
                scrub: 0.5,           // Slight smoothing for mouse wheel clicks
                // markers: true      // Uncomment for debugging
            }
        });
    }

    // We must ensure the browser has loaded the video metadata to know the duration
    if (video.readyState >= 1) { // HAVE_METADATA
        setupScrub();
    } else {
        video.addEventListener('loadedmetadata', setupScrub);
    }
    
    // Attempt to warm up the video decoder to prevent initial stuttering
    // Note: Autoplay policies might catch this, so we swallow the promise error
    video.play().then(() => {
        video.pause();
    }).catch((e) => {
        // Autoplay blocked, no action needed, scrubbing will still work
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
