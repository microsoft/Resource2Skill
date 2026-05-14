def create_component(
    output_dir: str,
    title_text: str = "CSS Animation Mastery",
    body_text: str = "Scroll down to see timeline-driven animations in action.",
    color_scheme: str = "dark",
    accent_color: str = "#00ffff", # Cyan accent matching tutorial
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the 3D Loader and Scroll Reveal animations.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    if color_scheme == "dark":
        bg_color = "#0a0a0a"
        text_color = "#ffffff"
        surface_color = "rgba(255, 255, 255, 0.05)"
        surface_border = "rgba(255, 255, 255, 0.1)"
    else:
        bg_color = "#f0f2f5"
        text_color = "#111111"
        surface_color = "rgba(0, 0, 0, 0.05)"
        surface_border = "rgba(0, 0, 0, 0.1)"

    css = f"""/* CSS Animation Showcase */
:root {{
    --bg: {bg_color};
    --text: {text_color};
    --accent: {accent_color};
    --surface: {surface_color};
    --border: {surface_border};
}}

* {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: 'Inter', system-ui, sans-serif;
    background-color: var(--bg);
    color: var(--text);
    overflow-x: hidden;
}}

/* --- Hero Section & Loader --- */
.hero {{
    height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    padding: 2rem;
}}

.loader-container {{
    margin-bottom: 3rem;
    perspective: 800px; /* Gives depth to the 3D rotation */
}}

.loader {{
    height: 60px;
    width: 60px;
    border: 6px solid var(--accent);
    border-radius: 6px;
    box-shadow: 0 0 15px var(--accent), inset 0 0 15px var(--accent);
    /* 
      animation shorthand: 
      name | duration | timing-function | iteration-count 
    */
    animation: loading 2.5s ease-in-out infinite;
}}

@keyframes loading {{
    0% {{
        transform: rotateX(0deg) rotateY(0deg) rotateZ(0deg);
    }}
    33% {{
        transform: rotateX(180deg) rotateY(0deg) rotateZ(0deg);
    }}
    67% {{
        transform: rotateX(180deg) rotateY(180deg) rotateZ(0deg);
    }}
    100% {{
        transform: rotateX(180deg) rotateY(180deg) rotateZ(180deg);
    }}
}}

h1 {{
    font-size: 3rem;
    margin-bottom: 1rem;
    letter-spacing: -0.05em;
}}

p {{
    font-size: 1.2rem;
    opacity: 0.7;
}}

.scroll-indicator {{
    margin-top: 4rem;
    animation: bounce 2s infinite;
    opacity: 0.5;
}}

@keyframes bounce {{
    0%, 20%, 50%, 80%, 100% {{ transform: translateY(0); }}
    40% {{ transform: translateY(-20px); }}
    60% {{ transform: translateY(-10px); }}
}}

/* --- Scroll Grid Section --- */
.grid-section {{
    max-width: {width_px}px;
    margin: 0 auto;
    padding: 4rem 2rem 10rem 2rem;
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 2rem;
}}

.card {{
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    height: 250px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 2rem;
    font-weight: 700;
    color: var(--accent);
    box-shadow: 0 10px 30px rgba(0,0,0,0.1);
}}

/* 
  FALLBACK: For browsers that don't support animation-timeline.
  We set initial states and use a class added by IntersectionObserver.
*/
.card {{
    opacity: 0;
    transform: scale(0.8) translateY(50px);
    transition: opacity 0.6s ease-out, transform 0.6s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}}

.card.is-visible {{
    opacity: 1;
    transform: scale(1) translateY(0);
}}

/* 
  MODERN CSS ENHANCEMENT: 
  If animation-timeline is supported, override the fallback and use pure CSS scroll sync.
*/
@supports (animation-timeline: view()) {{
    .card {{
        /* Reset fallback transition states */
        transition: none;
        opacity: 1;
        transform: none;
        
        /* Apply scroll-driven animation */
        animation: reveal linear both;
        animation-timeline: view();
        /* Start animating when element enters 10% from bottom, finish when 30% up */
        animation-range: entry 10% cover 30%; 
    }}
}}

@keyframes reveal {{
    from {{
        opacity: 0;
        transform: scale(0.5) translateY(100px);
    }}
    to {{
        opacity: 1;
        transform: scale(1) translateY(0);
    }}
}}
"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    
    <main class="hero">
        <div class="loader-container">
            <div class="loader"></div>
        </div>
        <h1>{title_text}</h1>
        <p>{body_text}</p>
        <div class="scroll-indicator">↓</div>
    </main>

    <section class="grid-section">
        <!-- Generating multiple cards to enable scrolling -->
        <div class="card">1</div>
        <div class="card">2</div>
        <div class="card">3</div>
        <div class="card">4</div>
        <div class="card">5</div>
        <div class="card">6</div>
        <div class="card">7</div>
        <div class="card">8</div>
        <div class="card">9</div>
        <div class="card">10</div>
        <div class="card">11</div>
        <div class="card">12</div>
    </section>

    <script src="script.js"></script>
</body>
</html>"""

    js = f"""// CSS Animation Showcase Script

document.addEventListener('DOMContentLoaded', () => {{
    // Check if the browser supports animation-timeline
    const supportsScrollTimeline = CSS.supports('animation-timeline: view()');

    // If it doesn't, we use an IntersectionObserver to mimic the reveal effect
    if (!supportsScrollTimeline) {{
        console.log("animation-timeline not supported, using IntersectionObserver fallback.");
        
        const cards = document.querySelectorAll('.card');
        
        const observerOptions = {{
            root: null,
            rootMargin: '0px',
            threshold: 0.15 // Trigger when 15% of the card is visible
        }};

        const observer = new IntersectionObserver((entries, observer) => {{
            entries.forEach(entry => {{
                if (entry.isIntersecting) {{
                    entry.target.classList.add('is-visible');
                    // Optional: stop observing once revealed
                    // observer.unobserve(entry.target); 
                }} else {{
                    // Remove class when scrolling back up to reset animation
                    entry.target.classList.remove('is-visible');
                }}
            }});
        }}, observerOptions);

        cards.forEach(card => {{
            observer.observe(card);
        }});
    }} else {{
        console.log("Using native pure CSS animation-timeline.");
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
