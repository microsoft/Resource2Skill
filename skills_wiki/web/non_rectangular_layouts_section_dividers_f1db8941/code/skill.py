def create_component(
    output_dir: str,
    title_text: str = "Break the Box",
    body_text: str = "Explore non-rectangular layouts using modern CSS shapes, skewed pseudo-elements, and clip-paths.",
    color_scheme: str = "light",
    accent_color: str = "#FFC145",
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Non-Rectangular Layouts visual effect.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Determine contrasting theme colors
    if color_scheme == "dark":
        text_color = "#ffffff"
        sec2_color = kwargs.get("secondary_color", "#2a2a40")
        sec3_color = kwargs.get("tertiary_color", "#12121c")
        text_shadow = "0 2px 4px rgba(0,0,0,0.5)"
    else:
        text_color = "#1a1a2e"
        sec2_color = kwargs.get("secondary_color", "#FF6B6C")
        sec3_color = kwargs.get("tertiary_color", "#5B5F97")
        text_shadow = "none"

    # === CSS ===
    css = f"""/* Non-Rectangular Layouts - Generated CSS */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg1: {accent_color};
    --bg2: {sec2_color};
    --bg3: {sec3_color};
    --text: {text_color};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background: #e9ecef;
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
}}

.container {{
    width: var(--width);
    max-width: 100%;
    height: var(--height);
    overflow-y: auto;
    overflow-x: hidden;
    background: var(--bg3);
    position: relative;
    border-radius: 12px;
    box-shadow: 0 25px 50px -12px rgba(0,0,0,0.25);
    scroll-behavior: smooth;
}}

.section {{
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    padding: 80px 20px;
    position: relative;
    color: var(--text);
}}

.title {{
    font-size: clamp(2.5rem, 5vw, 4rem);
    font-weight: 800;
    margin-bottom: 16px;
    letter-spacing: -0.03em;
    text-shadow: {text_shadow};
}}

.subtitle {{
    font-size: 1.25rem;
    opacity: 0.85;
    max-width: 600px;
    line-height: 1.6;
    text-shadow: {text_shadow};
}}

/* --- SECTION ONE: Chevron Down --- */
.one {{
    background: var(--bg1);
    z-index: 10;
    min-height: 60%;
    color: #1a1a2e; /* Force dark text for bright accent */
}}
.one .title, .one .subtitle {{ text-shadow: none; }}

.circle-icon {{
    width: 80px;
    height: 80px;
    background: rgba(0, 0, 0, 0.1);
    border-radius: 50%;
    display: grid;
    place-items: center;
    font-size: 2rem;
    font-weight: 800;
    margin-top: 40px;
    color: rgba(0,0,0,0.6);
    transition: transform 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
    cursor: pointer;
}}

.circle-icon:hover {{
    transform: scale(1.15) rotate(15deg);
    background: rgba(0, 0, 0, 0.15);
}}

/* The Chevron Pseudo-elements 
   Sized relatively to the container width using calc() to maintain angles */
.one::before, .one::after {{
    content: '';
    position: absolute;
    bottom: calc(var(--width) * -0.03);
    width: 50%;
    height: calc(var(--width) * 0.08); /* Tall enough to hide gap behind section */
    background: var(--bg1);
    z-index: -1;
}}

.one::before {{
    left: 0;
    transform-origin: bottom left;
    transform: skewY(4deg);
}}

.one::after {{
    right: 0;
    transform-origin: bottom right;
    transform: skewY(-4deg);
}}

/* --- SECTION TWO: Clip-path Angle --- */
.two {{
    background: var(--bg2);
    z-index: 5;
    padding-top: calc(80px + var(--width) * 0.03); 
    padding-bottom: calc(100px + var(--width) * 0.06);
    
    /* Cuts the bottom right corner higher than the bottom left */
    clip-path: polygon(0 0, 100% 0, 100% calc(100% - calc(var(--width) * 0.06)), 0 100%);
    
    /* Physically pull the next section up to hide behind the cut */
    margin-bottom: calc(var(--width) * -0.06);
}}

.image-wrapper {{
    margin-top: 50px;
    /* Drop shadow applied to wrapper because clip-path on child truncates box-shadow */
    filter: drop-shadow(0 20px 30px rgba(0,0,0,0.4));
}}

.angled-img {{
    width: 300px;
    height: 380px;
    object-fit: cover;
    /* Parallelogram cutout */
    clip-path: polygon(15% 0, 100% 0, 85% 100%, 0 100%);
    transition: clip-path 0.5s cubic-bezier(0.4, 0, 0.2, 1);
    cursor: pointer;
}}

.angled-img:hover {{
    /* Reverts to square on hover */
    clip-path: polygon(0 0, 100% 0, 100% 100%, 0 100%);
}}

/* --- SECTION THREE: Base Layer --- */
.three {{
    background: var(--bg3);
    color: #ffffff; /* Assumes tertiary is dark */
    z-index: 1;
    min-height: 40%;
    /* Push content down so it isn't hidden behind Section Two's overlap */
    padding-top: calc(80px + var(--width) * 0.08);
}}
.three .title, .three .subtitle {{ text-shadow: 0 2px 4px rgba(0,0,0,0.5); }}

/* Scroll Animation Classes */
.reveal {{
    opacity: 0;
    transform: translateY(30px);
    transition: all 0.8s cubic-bezier(0.2, 0.8, 0.2, 1);
}}

.reveal.active {{
    opacity: 1;
    transform: translateY(0);
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
    <div class="container">
        <!-- Section 1: Skewed Chevron Base -->
        <section class="section one">
            <h1 class="title">{title_text}</h1>
            <p class="subtitle">{body_text}</p>
            <div class="circle-icon">;)</div>
        </section>

        <!-- Section 2: Polygon Clip-Path Background -->
        <section class="section two">
            <h2 class="title reveal">Clipped Perspectives</h2>
            <p class="subtitle reveal">Using clip-path on both images and layout blocks creates sharp, architectural intersections.</p>
            <div class="image-wrapper reveal">
                <img class="angled-img" src="https://images.unsplash.com/photo-1550684848-fac1c5b4e853?auto=format&fit=crop&w=600&q=80" alt="Architecture">
            </div>
        </section>

        <!-- Section 3: Deep Overlap -->
        <section class="section three">
            <h2 class="title reveal">Seamless Overlap</h2>
            <p class="subtitle reveal">Negative margins physically pull this layer upward, nestling it comfortably behind the clipped edge of the section above.</p>
        </section>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Non-Rectangular Layouts - Scroll Interactions
document.addEventListener('DOMContentLoaded', () => {{
    const container = document.querySelector('.container');
    const revealElements = document.querySelectorAll('.reveal');

    // Setup Intersection Observer tied to the internal scrolling container
    const observer = new IntersectionObserver((entries) => {{
        entries.forEach(entry => {{
            if (entry.isIntersecting) {{
                // Add active class with a slight delay for nested elements
                setTimeout(() => {{
                    entry.target.classList.add('active');
                }}, 100);
            }}
        }});
    }}, {{ 
        root: container,
        threshold: 0.15,
        rootMargin: "0px 0px -50px 0px"
    }});

    // Observe all targeted elements
    revealElements.forEach(el => observer.observe(el));
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
