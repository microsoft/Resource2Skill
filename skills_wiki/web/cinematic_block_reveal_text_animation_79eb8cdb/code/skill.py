def create_component(
    output_dir: str,
    title_text: str = "FRAMED IN TUNGSTEN",
    body_text: str = "This is cinematography in its raw form. The camera settles into long takes and patient movement. Colors stay unrefined and shadows turn into texture.",
    color_scheme: str = "dark",
    accent_color: str = "#ff0100",
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    import os

    os.makedirs(output_dir, exist_ok=True)

    if color_scheme == "dark":
        bg_color = "#0a0a0a"
        text_color = "#f4f4f4"
        secondary_bg = "#111111"
    else:
        bg_color = "#f4f4f4"
        text_color = "#0a0a0a"
        secondary_bg = "#e0e0e0"

    css = f"""/* Cinematic Block Reveal — generated component */
@import url('https://fonts.googleapis.com/css2?family=Anton&family=Inter:wght@400;600&display=swap');

*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --text: {text_color};
    --accent: {accent_color};
    --secondary-bg: {secondary_bg};
}}

html.lenis {{
  height: auto;
}}
.lenis.lenis-smooth {{
  scroll-behavior: auto;
}}
.lenis.lenis-smooth [data-lenis-prevent] {{
  overscroll-behavior: contain;
}}
.lenis.lenis-stopped {{
  overflow: hidden;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background: var(--bg);
    color: var(--text);
    min-height: 200vh; /* Allow scrolling */
    overflow-x: hidden;
    -webkit-font-smoothing: antialiased;
}}

/* Navigation mock */
nav {{
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    padding: 2rem 4rem;
    display: flex;
    justify-content: space-between;
    z-index: 100;
    mix-blend-mode: difference;
    color: #fff;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1px;
    pointer-events: none;
}}

/* Layout */
.section {{
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    justify-content: center;
    padding: 4rem;
    position: relative;
}}

.section.intro {{
    align-items: center;
    text-align: center;
    background: var(--secondary-bg);
}}

.section.content {{
    align-items: flex-start;
    max-width: {width_px}px;
    margin: 0 auto;
}}

/* Typography */
.reveal-heading {{
    font-family: 'Anton', sans-serif;
    text-transform: uppercase;
    font-size: clamp(4rem, 8vw, 8rem);
    line-height: 1.05;
    letter-spacing: 0.02em;
    margin-bottom: 2rem;
    max-width: 900px;
}}

.reveal-body {{
    font-family: 'Inter', sans-serif;
    text-transform: uppercase;
    font-weight: 600;
    font-size: clamp(1.5rem, 3vw, 2.5rem);
    line-height: 1.3;
    max-width: 800px;
}}

/* Utility for the generated structure */
.line {{
    position: relative;
    display: inline-block;
    vertical-align: top;
}}
"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cinematic Block Reveal</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <nav>
        <span>Index</span>
        <span>Menu</span>
    </nav>

    <!-- First section pushes content down to demo scroll trigger -->
    <section class="section intro">
        <p style="font-family: 'Anton', sans-serif; font-size: 2rem; letter-spacing: 2px; color: var(--accent);">
            Scroll Down
        </p>
    </section>

    <!-- Content section with reveal elements -->
    <section class="section content">
        <h1 class="reveal-heading" data-block-color="var(--accent)">{title_text}</h1>
        <p class="reveal-body" data-block-color="var(--text)">{body_text}</p>
    </section>
    
    <section class="section intro">
        <p style="font-family: 'Anton', sans-serif; font-size: 2rem; letter-spacing: 2px;">
            End of Reel
        </p>
    </section>

    <!-- Dependencies -->
    <script src="https://unpkg.com/@studio-freight/lenis@1.0.42/dist/lenis.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/ScrollTrigger.min.js"></script>
    <script src="https://unpkg.com/split-type"></script>
    <script src="script.js"></script>
</body>
</html>"""

    js = f"""// Cinematic Block Reveal — interactive behavior

document.addEventListener('DOMContentLoaded', () => {{
    // 1. Initialize Lenis Smooth Scroll
    const lenis = new Lenis({{
        duration: 1.2,
        easing: (t) => Math.min(1, 1.001 - Math.pow(2, -10 * t)),
        orientation: 'vertical',
        gestureOrientation: 'vertical',
        smoothWheel: true,
    }});

    lenis.on('scroll', ScrollTrigger.update);

    gsap.ticker.add((time) => {{
        lenis.raf(time * 1000);
    }});
    gsap.ticker.lagSmoothing(0);

    // 2. Setup Reveal Animations
    const revealElements = document.querySelectorAll('.reveal-heading, .reveal-body');

    revealElements.forEach(el => {{
        // Split text into lines
        const splitText = new SplitType(el, {{ types: 'lines' }});
        const blockColor = el.getAttribute('data-block-color') || 'var(--accent)';

        // Setup GSAP ScrollTrigger timeline for this block of text
        const tl = gsap.timeline({{
            scrollTrigger: {{
                trigger: el,
                start: "top 85%", // Trigger when top of element hits 85% of viewport height
                toggleActions: "play none none none" 
            }}
        }});

        // Process each line to create the overlay block and text span
        splitText.lines.forEach((line, index) => {{
            // Ensure line container acts as a positioning context
            line.style.position = 'relative';

            // Wrap original text in a span so we can hide/show it independently
            const originalHTML = line.innerHTML;
            line.innerHTML = ''; // Clear line

            const textSpan = document.createElement('span');
            textSpan.innerHTML = originalHTML;
            textSpan.style.opacity = '0'; // Hide initially
            textSpan.style.position = 'relative';
            textSpan.style.zIndex = '0';
            line.appendChild(textSpan);

            // Create the wiping block overlay
            const block = document.createElement('div');
            block.style.position = 'absolute';
            block.style.top = '0';
            block.style.left = '0';
            block.style.width = '100%';
            block.style.height = '100%';
            block.style.backgroundColor = blockColor;
            block.style.transformOrigin = 'left center';
            block.style.transform = 'scaleX(0)';
            block.style.zIndex = '1';
            block.style.pointerEvents = 'none';
            line.appendChild(block);

            // Calculate staggered timing
            const staggerDelay = index * 0.15;
            const animDuration = 0.45;

            // Step 1: Block scales in from the left
            tl.to(block, {{
                scaleX: 1,
                duration: animDuration,
                ease: "power3.inOut"
            }}, staggerDelay)
            
            // Step 2: Make text visible exactly when block is fully covering it
            .set(textSpan, {{
                opacity: 1
            }}, staggerDelay + animDuration)
            
            // Step 3: Shift block's transform origin to the right
            .set(block, {{
                transformOrigin: "right center"
            }}, staggerDelay + animDuration)
            
            // Step 4: Block scales out to the right, revealing text
            .to(block, {{
                scaleX: 0,
                duration: animDuration,
                ease: "power3.inOut"
            }}, staggerDelay + animDuration);
        }});
    }});
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
