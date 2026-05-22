def create_component(
    output_dir: str,
    title_text: str = "Selected Case Studies",
    body_text: str = "Explore our latest projects showcasing staggered animations, fluid layouts, and engaging scroll interactions.",
    color_scheme: str = "dark",        
    accent_color: str = "#ff4500",     
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the GSAP Staggered Scroll Reveals effect.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme and accent_color ===
    if color_scheme == "dark":
        bg_color = "#0a0a0a"
        text_color = "#ffffff"
        text_muted = "#a0a0a0"
        surface_color = "rgba(255, 255, 255, 0.05)"
        border_color = "rgba(255, 255, 255, 0.1)"
    else:
        bg_color = "#ffffff"
        text_color = "#0a0a0a"
        text_muted = "#666666"
        surface_color = "rgba(0, 0, 0, 0.03)"
        border_color = "rgba(0, 0, 0, 0.1)"

    # Helper to wrap words in spans for GSAP targeting without external SplitText library
    words = title_text.split(" ")
    split_title_html = " ".join([f'<span class="title-word"><span class="title-word-inner">{word}</span></span>' for word in words])

    # === CSS ===
    css = f"""/* GSAP Staggered Scroll Reveals */
:root {{
    --bg: {bg_color};
    --text: {text_color};
    --text-muted: {text_muted};
    --accent: {accent_color};
    --surface: {surface_color};
    --border: {border_color};
}}

* {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background-color: var(--bg);
    color: var(--text);
    overflow-x: hidden;
}}

/* Spacer to allow scrolling to the component */
.scroll-spacer {{
    height: 80vh;
    display: flex;
    align-items: center;
    justify-content: center;
    border-bottom: 1px solid var(--border);
}}

.scroll-spacer p {{
    color: var(--text-muted);
    font-size: 1.2rem;
    text-transform: uppercase;
    letter-spacing: 0.1em;
}}

/* Main Component Container */
.container {{
    max-width: {width_px}px;
    margin: 0 auto;
    padding: 120px 24px;
    min-height: {height_px}px;
}}

/* Title Section */
.section-header {{
    margin-bottom: 80px;
    max-width: 800px;
}}

.reveal-title {{
    font-size: clamp(3rem, 6vw, 5rem);
    font-weight: 800;
    line-height: 1.1;
    letter-spacing: -0.02em;
    margin-bottom: 24px;
    display: flex;
    flex-wrap: wrap;
    gap: 0.25em;
}}

/* Required setup for text reveal (masking effect) */
.title-word {{
    display: inline-block;
    overflow: hidden; /* Masks the inner word as it slides up */
    vertical-align: top;
}}

.title-word-inner {{
    display: inline-block;
    /* Initial state set by GSAP, but good practice to ensure it behaves like a block for transforms */
}}

.reveal-desc {{
    font-size: 1.25rem;
    color: var(--text-muted);
    line-height: 1.6;
    max-width: 600px;
}}

/* Card Grid */
.card-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 32px;
}}

.card {{
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 40px 32px;
    display: flex;
    flex-direction: column;
    gap: 16px;
    position: relative;
    overflow: hidden;
    transition: background 0.3s ease, border-color 0.3s ease;
}}

.card:hover {{
    background: rgba(255, 255, 255, 0.08);
    border-color: var(--accent);
}}

.card-number {{
    font-size: 0.875rem;
    font-weight: 600;
    color: var(--accent);
    margin-bottom: auto;
}}

.card-title {{
    font-size: 1.5rem;
    font-weight: 600;
}}

.card-tags {{
    display: flex;
    gap: 8px;
    margin-top: 16px;
}}

.tag {{
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    padding: 4px 12px;
    border-radius: 100px;
    border: 1px solid var(--border);
    color: var(--text-muted);
}}
"""

    # === HTML ===
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text} - Animation Demo</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
    <!-- Load GSAP and ScrollTrigger from CDN -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/gsap.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/ScrollTrigger.min.js"></script>
</head>
<body>
    
    <!-- Spacer to demonstrate scrolling -->
    <div class="scroll-spacer">
        <p>Scroll down to reveal</p>
    </div>

    <main class="container" id="reveal-section">
        <header class="section-header">
            <h2 class="reveal-title">
                {split_title_html}
            </h2>
            <p class="reveal-desc">{body_text}</p>
        </header>

        <div class="card-grid">
            <article class="card">
                <span class="card-number">01</span>
                <h3 class="card-title">Brand Identity</h3>
                <div class="card-tags">
                    <span class="tag">Design</span>
                    <span class="tag">Strategy</span>
                </div>
            </article>
            <article class="card">
                <span class="card-number">02</span>
                <h3 class="card-title">Digital Platforms</h3>
                <div class="card-tags">
                    <span class="tag">Web</span>
                    <span class="tag">Mobile</span>
                </div>
            </article>
            <article class="card">
                <span class="card-number">03</span>
                <h3 class="card-title">Campaign Creation</h3>
                <div class="card-tags">
                    <span class="tag">Marketing</span>
                    <span class="tag">Social</span>
                </div>
            </article>
        </div>
    </main>

    <!-- Spacer to allow scrolling past -->
    <div class="scroll-spacer" style="height: 50vh; border: none;"></div>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// GSAP Staggered Scroll Reveals Implementation

document.addEventListener('DOMContentLoaded', () => {{
    // Register the ScrollTrigger plugin with GSAP
    gsap.registerPlugin(ScrollTrigger);

    // 1. Text Reveal Animation
    // Targets the inner spans of the title words, sliding them up from behind the hidden overflow of their parent
    gsap.from(".title-word-inner", {{
        scrollTrigger: {{
            trigger: ".section-header",
            start: "top 80%", // Triggers when the top of the header hits 80% down the viewport
        }},
        yPercent: 100, // Start pushed down 100% of its height
        opacity: 0,
        duration: 0.8,
        ease: "power4.out", // Smooth, natural deceleration
        stagger: 0.05 // Delay between each word animating
    }});

    // Fade in the description slightly after the title starts
    gsap.from(".reveal-desc", {{
        scrollTrigger: {{
            trigger: ".section-header",
            start: "top 75%",
        }},
        y: 20,
        opacity: 0,
        duration: 0.8,
        delay: 0.3,
        ease: "power2.out"
    }});

    // 2. Card Grid Staggered Reveal
    // Animates the cards sliding up, rotating slightly, and fading in sequentially
    gsap.from(".card", {{
        scrollTrigger: {{
            trigger: ".card-grid",
            start: "top 85%", // Trigger slightly lower down
        }},
        y: 80, // Start 80px down
        rotation: 4, // Start with a slight rotation
        opacity: 0,
        duration: 0.8,
        ease: "back.out(1.5)", // Gives a slight "bounce" or overshoot at the end of the animation
        stagger: {{
            amount: 0.4 // Distributes the start times of all cards across a total of 0.4 seconds
        }}
    }});
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
