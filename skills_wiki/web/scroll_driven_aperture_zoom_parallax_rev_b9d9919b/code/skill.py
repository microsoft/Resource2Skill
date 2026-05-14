def create_component(
    output_dir: str,
    title_text: str = "An aperture into stillness",
    body_text: str = "A sustained moment where scale dissolves and perception lingers.",
    color_scheme: str = "dark",
    accent_color: str = "#00bfff",
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Aperture Zoom Parallax visual effect.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme ===
    if color_scheme == "dark":
        bg_outer = "#050505"
        surface_color = "#11131a"
        border_color = "#2a2d35"
        text_primary = "#f8f9fa"
        text_secondary = "#8e93a0"
    else:
        bg_outer = "#e0e0e0"
        surface_color = "#f4f5f7"
        border_color = "#e2e4e8"
        text_primary = "#1a1a24"
        text_secondary = "#5a5e69"

    # Background image URL (High quality sky/clouds)
    sky_bg_url = "https://images.unsplash.com/photo-1579033461380-adb47c3eb938?q=80&w=2000&auto=format&fit=crop"

    # === CSS ===
    css = f"""/* Scroll-Driven Aperture Zoom - Generated Component */
@import url('https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Inter:wght@300;400;500&display=swap');

*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --surface: {surface_color};
    --border: {border_color};
    --text-primary: {text_primary};
    --text-secondary: {text_secondary};
    --accent: {accent_color};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    background: {bg_outer};
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 100vh;
    font-family: 'Inter', sans-serif;
}}

/* Sandbox Wrapper to constrain the component to requested dimensions */
.sandbox-wrapper {{
    width: var(--width);
    height: var(--height);
    max-width: 100vw;
    max-height: 100vh;
    background: var(--surface);
    position: relative;
    overflow-y: auto;
    overflow-x: hidden;
    box-shadow: 0 20px 40px rgba(0,0,0,0.4);
}}

/* Inner content area */
.sandbox-content {{
    position: relative;
    width: 100%;
}}

/* Intro and Outro sections just for scroll real estate */
.spacer-section {{
    height: 50vh;
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--text-secondary);
    text-transform: uppercase;
    letter-spacing: 2px;
    font-size: 0.85rem;
    background: var(--surface);
    position: relative;
    z-index: 10;
}}

/* The Core Hero Section */
.hero {{
    position: relative;
    width: 100%;
    height: var(--height);
    overflow: hidden;
    background: #000; /* Behind everything */
}}

/* Layer 1: Parallax Sky Background */
.sky-container {{
    position: absolute;
    top: -10%; 
    left: 0;
    width: 100%;
    height: 120%; /* Extra height for parallax travel */
    z-index: 1;
    will-change: transform;
}}

.sky-container img {{
    width: 100%;
    height: 100%;
    object-fit: cover;
}}

/* Layer 2: Final Hero Copy (Revealed at the end) */
.hero-copy-container {{
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    z-index: 2;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 10%;
    pointer-events: none;
}}

.hero-copy {{
    font-family: 'Instrument Serif', serif;
    font-size: clamp(2rem, 5cqw, 4.5rem);
    line-height: 1.1;
    color: #ffffff; /* Always white against the sky */
    text-align: center;
    text-shadow: 0 10px 30px rgba(0,0,0,0.3);
    max-width: 800px;
    will-change: transform, opacity;
}}

/* Layer 3: The Window Masking Frame */
.window-container {{
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    z-index: 3;
    display: flex;
    align-items: center;
    justify-content: center;
    will-change: transform;
    pointer-events: none;
}}

.window-frame {{
    width: 320px;
    height: 480px;
    border-radius: 160px; /* Pill shape */
    /* The magic trick: A 4000px solid shadow that forms the wall */
    box-shadow: 0 0 0 4000px var(--surface), inset 0 0 40px rgba(0,0,0,0.6);
    border: 12px solid var(--border);
    position: relative;
}}

/* Subtle glare/reflection on the glass */
.window-frame::after {{
    content: '';
    position: absolute;
    top: 0; left: 0; width: 100%; height: 100%;
    border-radius: inherit;
    background: linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0) 50%);
    z-index: 10;
}}

/* Layer 4: Foreground Header Text */
.hero-header {{
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    z-index: 4;
    display: flex;
    justify-content: space-between;
    padding: 3rem 4rem;
    pointer-events: none;
    will-change: transform, opacity;
}}

.col {{
    display: flex;
    flex-direction: column;
    justify-content: center;
    max-width: 250px;
}}

.col.right {{
    text-align: right;
}}

.hero-header h1 {{
    font-family: 'Instrument Serif', serif;
    font-size: 3rem;
    line-height: 1.1;
    color: var(--text-primary);
    margin-bottom: 1rem;
}}

.hero-header p {{
    font-size: 1rem;
    line-height: 1.5;
    color: var(--text-secondary);
}}

/* Scrollbar styling for sandbox */
.sandbox-wrapper::-webkit-scrollbar {{
    width: 8px;
}}
.sandbox-wrapper::-webkit-scrollbar-track {{
    background: var(--surface);
}}
.sandbox-wrapper::-webkit-scrollbar-thumb {{
    background: var(--border);
    border-radius: 4px;
}}
"""

    # === HTML ===
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Aperture Scroll Parallax</title>
    <link rel="stylesheet" href="style.css">
    <!-- Lenis for smooth scrolling -->
    <script src="https://cdn.jsdelivr.net/npm/@studio-freight/lenis@1.0.29/dist/lenis.min.js"></script>
    <!-- GSAP Core & ScrollTrigger -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/gsap.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/ScrollTrigger.min.js"></script>
</head>
<body>

    <div class="sandbox-wrapper">
        <div class="sandbox-content">
            
            <section class="hero">
                <!-- Parallax Background -->
                <div class="sky-container">
                    <img src="{sky_bg_url}" alt="Sky clouds">
                </div>
                
                <!-- Final Revealed Text -->
                <div class="hero-copy-container">
                    <div class="hero-copy">
                        {body_text}
                    </div>
                </div>

                <!-- Scaling Mask Frame -->
                <div class="window-container">
                    <div class="window-frame"></div>
                </div>

                <!-- Foreground Overlay Text -->
                <div class="hero-header">
                    <div class="col left">
                        <h1>{title_text}</h1>
                    </div>
                    <div class="col right">
                        <p>Where distance becomes a presence.</p>
                    </div>
                </div>
            </section>
            
            <!-- Outro space to allow scrolling past the pinned hero -->
            <section class="spacer-section">
                <span>End of View</span>
            </section>

        </div>
    </div>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Scroll-Driven Aperture Zoom Initialization

document.addEventListener('DOMContentLoaded', () => {{
    
    // 1. Initialize Lenis Smooth Scrolling on the specific wrapper
    const wrapper = document.querySelector('.sandbox-wrapper');
    const content = document.querySelector('.sandbox-content');
    
    const lenis = new Lenis({{
        wrapper: wrapper,
        content: content,
        lerp: 0.08,
        smoothWheel: true
    }});

    function raf(time) {{
        lenis.raf(time);
        requestAnimationFrame(raf);
    }}
    requestAnimationFrame(raf);

    // 2. Register GSAP ScrollTrigger
    gsap.registerPlugin(ScrollTrigger);

    // Inform ScrollTrigger to attach to our custom sandbox container instead of the window
    ScrollTrigger.defaults({{
        scroller: wrapper
    }});

    // Update ScrollTrigger on Lenis scroll
    lenis.on('scroll', ScrollTrigger.update);
    gsap.ticker.add((time) => {{
        lenis.raf(time * 1000);
    }});
    gsap.ticker.lagSmoothing(0);

    // 3. Create the Cinematic Animation Timeline
    const tl = gsap.timeline({{
        scrollTrigger: {{
            trigger: ".hero",
            start: "top top",
            end: "+=350%", // Pins for 3.5x the height of the container
            pin: true,
            scrub: 1, // 1 second smoothing on the scrub
            anticipatePin: 1
        }}
    }});

    // Phase A: The Zoom & Background Drift
    // Scale the window up exponentially so the "hole" covers the screen
    tl.to(".window-container", {{
        scale: 9, // Adjust based on max viewport size relative to window size
        ease: "power2.inOut",
        duration: 2
    }}, 0);

    // Scale the foreground text and fade it out so it feels like it flies past the camera
    tl.to(".hero-header", {{
        scale: 2.5,
        opacity: 0,
        ease: "power1.in",
        duration: 1.2
    }}, 0);

    // Slowly drift the sky background upwards throughout the entire scroll interaction
    tl.to(".sky-container", {{
        yPercent: -15, // Moves up by 15% of its height
        ease: "none",
        duration: 3
    }}, 0);

    // Phase B: Bring in the final copy
    // Starts hidden below, reveals upward smoothly
    tl.fromTo(".hero-copy", 
        {{ yPercent: 40, opacity: 0 }},
        {{ yPercent: 0, opacity: 1, ease: "power3.out", duration: 1.5 }},
        1.2 // Overlaps with the zoom effect slightly
    );
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
