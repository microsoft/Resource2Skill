def create_component(
    output_dir: str,
    title_text: str = "Scroll Reveal Gallery",
    body_text: str = "Scroll down to see the elements dynamically animate into the viewport.",
    color_scheme: str = "dark",
    accent_color: str = "#00bfff",
    width_px: int = 1000,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the CSS Scroll-Driven Reveal Animation.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme and accent_color ===
    if color_scheme == "dark":
        bg_color = "#0a0a0f"
        panel_bg = "#14141e"
        text_color = "#ffffff"
        text_muted = "#8a8a9e"
        border_color = "rgba(255,255,255,0.05)"
    else:
        bg_color = "#f4f4f8"
        panel_bg = "#ffffff"
        text_color = "#111118"
        text_muted = "#666677"
        border_color = "rgba(0,0,0,0.05)"

    # Generate HTML for cards
    cards_html = ""
    for i in range(1, 16):
        # Varying heights to create a slight masonry feel
        height_class = "tall" if i % 4 == 0 else "short" if i % 3 == 0 else "normal"
        cards_html += f"""
            <div class="card {height_class}">
                <div class="card-inner">
                    <h3>Item {i:02d}</h3>
                    <p>Dynamic scroll content.</p>
                </div>
            </div>"""

    # === CSS ===
    css = f"""/* Scroll-Driven Reveal Component */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap');

*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --panel-bg: {panel_bg};
    --text: {text_color};
    --text-muted: {text_muted};
    --accent: {accent_color};
    --border: {border_color};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Inter', sans-serif;
    background: #000; /* Outer dark background */
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 100vh;
}}

/* The main component container */
.container {{
    width: var(--width);
    height: var(--height);
    background: var(--bg);
    color: var(--text);
    overflow-y: auto;
    overflow-x: hidden;
    position: relative;
    border-radius: 12px;
    box-shadow: 0 24px 48px rgba(0,0,0,0.2);
    /* Custom scrollbar for aesthetics */
    scrollbar-width: thin;
    scrollbar-color: var(--accent) var(--bg);
}}

.container::-webkit-scrollbar {{ width: 6px; }}
.container::-webkit-scrollbar-track {{ background: var(--bg); }}
.container::-webkit-scrollbar-thumb {{ background: var(--accent); border-radius: 6px; }}

.header {{
    padding: 60px 40px;
    text-align: center;
    background: linear-gradient(to bottom, var(--panel-bg), transparent);
    position: sticky;
    top: 0;
    z-index: 10;
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    border-bottom: 1px solid var(--border);
}}

.header h1 {{
    font-size: 2.5rem;
    font-weight: 600;
    margin-bottom: 10px;
}}

.header p {{
    color: var(--text-muted);
    font-size: 1.1rem;
}}

.gallery {{
    padding: 40px;
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 30px;
    max-width: 1200px;
    margin: 0 auto;
}}

/* Card Base Styles */
.card {{
    background: var(--panel-bg);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 30px;
    display: flex;
    flex-direction: column;
    justify-content: flex-end;
    transition: box-shadow 0.3s ease, border-color 0.3s ease;
}}

.card:hover {{
    box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    border-color: var(--accent);
}}

.card.normal {{ height: 250px; }}
.card.tall {{ height: 350px; grid-row: span 2; }}
.card.short {{ height: 180px; }}

/* Assigning alternating colors based on accent */
.card:nth-child(3n+1) .card-inner h3 {{ color: var(--accent); }}
.card:nth-child(3n+2) {{ border-bottom: 4px solid var(--accent); }}
.card:nth-child(3n+3) {{ background: linear-gradient(135deg, var(--panel-bg), rgba(255,255,255,0.02)); }}

.card-inner h3 {{
    font-size: 1.5rem;
    margin-bottom: 8px;
}}

.card-inner p {{
    color: var(--text-muted);
    font-size: 0.95rem;
}}

/* ========================================================
   THE CORE SKILL: Scroll-Driven Reveal Animation
   ======================================================== */

@supports (animation-timeline: view()) {{
    .card {{
        /* Bind the animation to the element's intersection with the scrollport */
        animation: scroll-reveal linear both;
        animation-timeline: view();
        
        /* Start at the bottom edge (entry 0%), finish by 25% up the screen (cover 25%) */
        animation-range: entry 10% cover 25%;
    }}

    @keyframes scroll-reveal {{
        from {{
            opacity: 0;
            transform: translateY(100px) scale(0.85);
        }}
        to {{
            opacity: 1;
            transform: translateY(0) scale(1);
        }}
    }}
}}

/* Fallback for browsers without animation-timeline support (Safari, Firefox currently) */
@supports not (animation-timeline: view()) {{
    .card {{
        opacity: 0;
        transform: translateY(60px) scale(0.9);
        transition: opacity 0.8s cubic-bezier(0.2, 0.8, 0.2, 1), 
                    transform 0.8s cubic-bezier(0.2, 0.8, 0.2, 1);
        will-change: opacity, transform;
    }}

    .card.is-visible {{
        opacity: 1;
        transform: translateY(0) scale(1);
    }}
}}
"""

    # === HTML ===
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text}</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        <header class="header">
            <h1>{title_text}</h1>
            <p>{body_text}</p>
        </header>
        
        <main class="gallery">
            {cards_html}
        </main>
    </div>
    
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Scroll Reveal Fallback Logic
document.addEventListener('DOMContentLoaded', () => {{
    
    // Check if the browser supports the modern CSS view() timeline
    if (!CSS.supports('animation-timeline: view()')) {{
        console.log("CSS animation-timeline not supported. Using IntersectionObserver fallback.");
        
        const cards = document.querySelectorAll('.card');
        
        const observerOptions = {{
            root: document.querySelector('.container'), // Observe within the component container
            rootMargin: '0px 0px -10% 0px', // Trigger slightly before it comes into full view
            threshold: 0.1
        }};

        const scrollObserver = new IntersectionObserver((entries, observer) => {{
            entries.forEach((entry) => {{
                if (entry.isIntersecting) {{
                    // Add staggered delay based on order if multiple enter at once
                    entry.target.classList.add('is-visible');
                    // Optional: Unobserve to only animate once, or keep to animate both ways
                    // observer.unobserve(entry.target); 
                }} else {{
                    // Remove class when out of view to re-animate on scroll back down
                    entry.target.classList.remove('is-visible');
                }}
            }});
        }}, observerOptions);

        cards.forEach(card => {{
            scrollObserver.observe(card);
        }});
    }} else {{
        console.log("CSS animation-timeline supported! Handled purely by CSS.");
    }}
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
