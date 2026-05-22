def create_component(
    output_dir: str,
    title_text: str = "Every idea begins as a single image.",
    body_text: str = "Three pillars with one purpose",
    color_scheme: str = "dark",        
    accent_color: str = "#d32f2f",     
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Split Image 3D Card Flip scroll animation.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    if color_scheme == "dark":
        bg_color = "#0a0a0a"
        text_color = "#f4f4f5"
        card_bg_1 = "#18181b"
        card_bg_2 = accent_color
        card_bg_3 = "#27272a"
        subtext_color = "#a1a1aa"
    else:
        bg_color = "#f4f4f5"
        text_color = "#0a0a0a"
        card_bg_1 = "#ffffff"
        card_bg_2 = accent_color
        card_bg_3 = "#e4e4e7"
        subtext_color = "#52525b"

    # Ensure contrast on the accent card
    accent_text_color = "#ffffff" if color_scheme == "light" else "#ffffff"

    # Sample Unsplash image - landscape abstract/nature to split
    sample_image = "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?q=80&w=2564&auto=format&fit=crop"

    css = f"""/* Split-Card Scroll Animation */
:root {{
    --bg-color: {bg_color};
    --text-color: {text_color};
    --accent: {accent_color};
    --subtext: {subtext_color};
    --card-bg-1: {card_bg_1};
    --card-bg-2: {card_bg_2};
    --card-bg-3: {card_bg_3};
    --accent-text: {accent_text_color};
}}

* {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: 'Inter', system-ui, sans-serif;
    background: var(--bg-color);
    color: var(--text-color);
    overflow-x: hidden;
}}

h1, h2, h3, .serif {{
    font-family: 'Instrument Serif', serif;
    font-weight: 400;
}}

/* Sections */
.intro, .outro {{
    height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    padding: 2rem;
}}

.intro h1, .outro h1 {{
    font-size: clamp(3rem, 6vw, 6rem);
    max-width: 800px;
    line-height: 1.1;
}}

.sticky-section {{
    position: relative;
    height: 300vh; /* Gives room to scroll */
}}

.sticky-content {{
    position: sticky;
    top: 0;
    height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    overflow: hidden;
}}

.sticky-header {{
    position: absolute;
    top: 15%;
    font-size: 2.5rem;
    color: var(--text-color);
    opacity: 0; /* Animated via JS */
    transform: translateY(30px);
}}

/* Card Container & Illusion Setup */
.card-container {{
    display: flex;
    gap: 0px; /* Starts at 0 to form single image */
    perspective: 1500px; /* Depth for 3D flip */
    z-index: 10;
}}

.card {{
    width: clamp(200px, 25vw, 320px);
    aspect-ratio: 0.7;
    position: relative;
    transform-style: preserve-3d;
    /* Initial border radius makes the outer edges rounded, inner flat */
}}

.card:nth-child(1) {{ border-radius: 24px 0 0 24px; }}
.card:nth-child(2) {{ border-radius: 0px; }}
.card:nth-child(3) {{ border-radius: 0 24px 24px 0; }}

/* Faces */
.card-face {{
    position: absolute;
    inset: 0;
    backface-visibility: hidden;
    border-radius: inherit;
    overflow: hidden;
    -webkit-backface-visibility: hidden; /* Safari */
}}

.card-front {{
    background-image: url('{sample_image}');
    background-size: 300% 100%;
    background-repeat: no-repeat;
}}

/* The Magic: Aligning the background to make 3 cards look like 1 image */
.card:nth-child(1) .card-front {{ background-position: 0% center; }}
.card:nth-child(2) .card-front {{ background-position: 50% center; }}
.card:nth-child(3) .card-front {{ background-position: 100% center; }}

.card-back {{
    transform: rotateY(180deg);
    padding: 2rem;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}}

.card:nth-child(1) .card-back {{ background: var(--card-bg-1); color: var(--text-color); }}
.card:nth-child(2) .card-back {{ background: var(--card-bg-2); color: var(--accent-text); }}
.card:nth-child(3) .card-back {{ background: var(--card-bg-3); color: var(--text-color); }}

.card-index {{
    font-size: 0.875rem;
    font-weight: 500;
    opacity: 0.7;
}}

.card-title {{
    font-size: 2rem;
    line-height: 1.1;
    margin-top: auto;
}}

/* Mobile Fallback */
@media (max-width: 768px) {{
    .sticky-section {{ height: auto; padding: 4rem 1rem; }}
    .sticky-content {{ position: relative; height: auto; }}
    .sticky-header {{ position: relative; top: 0; opacity: 1; transform: none; margin-bottom: 2rem; text-align: center; }}
    .card-container {{ flex-direction: column; gap: 2rem !important; }}
    .card {{ width: 100%; border-radius: 24px !important; transform: none !important; }}
    .card-front {{ display: none; }} /* Skip the split trick on mobile */
    .card-back {{ transform: none; position: relative; min-height: 300px; }}
}}
"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Split Card Scroll Animation</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Inter:wght@400;500&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>

    <section class="intro">
        <h1>{title_text}</h1>
    </section>

    <section class="sticky-section">
        <div class="sticky-content">
            <h2 class="sticky-header serif">{body_text}</h2>
            
            <div class="card-container">
                <!-- Card 1 -->
                <div class="card">
                    <div class="card-face card-front"></div>
                    <div class="card-face card-back">
                        <span class="card-index">(01)</span>
                        <h3 class="card-title serif">Interactive Web<br>Experiences</h3>
                    </div>
                </div>

                <!-- Card 2 -->
                <div class="card">
                    <div class="card-face card-front"></div>
                    <div class="card-face card-back">
                        <span class="card-index">(02)</span>
                        <h3 class="card-title serif">Thoughtful Design<br>Language</h3>
                    </div>
                </div>

                <!-- Card 3 -->
                <div class="card">
                    <div class="card-face card-front"></div>
                    <div class="card-face card-back">
                        <span class="card-index">(03)</span>
                        <h3 class="card-title serif">Visual Design<br>Systems</h3>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <section class="outro">
        <h1>Every transition leaves a trace.</h1>
    </section>

    <!-- GSAP & Lenis -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/gsap.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/ScrollTrigger.min.js"></script>
    <script src="https://cdn.jsdelivr.net/gh/studio-freight/lenis@1.0.29/bundled/lenis.min.js"></script>
    <script src="script.js"></script>
</body>
</html>"""

    js = f"""document.addEventListener("DOMContentLoaded", () => {{
    gsap.registerPlugin(ScrollTrigger);

    // Initialize smooth scrolling
    const lenis = new Lenis({{
        duration: 1.2,
        easing: (t) => Math.min(1, 1.001 - Math.pow(2, -10 * t)),
        direction: 'vertical',
        gestureDirection: 'vertical',
        smooth: true,
    }});

    lenis.on('scroll', ScrollTrigger.update);

    gsap.ticker.add((time) => {{
        lenis.raf(time * 1000);
    }});
    gsap.ticker.lagSmoothing(0);

    // Desktop Animation Logic (Responsive fallback handled via MatchMedia)
    let mm = gsap.matchMedia();

    mm.add("(min-width: 769px)", () => {{
        
        const tl = gsap.timeline({{
            scrollTrigger: {{
                trigger: ".sticky-section",
                start: "top top",
                end: "bottom bottom", // Scrubs through the 300vh height
                scrub: 1,
            }}
        }});

        // Phase 1: Reveal Header, Add Gap, Round Borders (Splitting the image)
        tl.to(".sticky-header", {{
            opacity: 1,
            y: 0,
            duration: 1,
            ease: "power2.out"
        }}, 0);

        tl.to(".card-container", {{
            gap: "2rem",
            duration: 1.5,
            ease: "power2.inOut"
        }}, 0.5);

        tl.to(".card", {{
            borderRadius: "24px",
            duration: 1.5,
            ease: "power2.inOut"
        }}, 0.5);

        // Phase 2: The Staggered 3D Flip
        tl.to(".card", {{
            rotateY: 180,
            y: (index) => index % 2 === 0 ? -20 : 20, // Add physical sway
            rotateZ: (index) => index === 0 ? -4 : (index === 2 ? 4 : 0), // Outer cards tilt slightly
            stagger: 0.2,
            duration: 1.5,
            ease: "power3.inOut"
        }}, 2.5);

        // Phase 3: Settle Back down
        tl.to(".card", {{
            y: 0,
            rotateZ: 0,
            stagger: 0.1,
            duration: 0.8,
            ease: "power2.out"
        }}, 4);

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
