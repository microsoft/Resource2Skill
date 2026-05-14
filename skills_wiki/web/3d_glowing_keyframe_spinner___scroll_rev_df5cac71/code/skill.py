def create_component(
    output_dir: str,
    title_text: str = "CSS Keyframe Mastery",
    body_text: str = "Scroll down to witness the grid reveal effect.",
    color_scheme: str = "dark",
    accent_color: str = "#00ffff",  # Cyan neon
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the 3D Glowing Spinner & Scroll-Reveal Grid.
    
    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors ===
    if color_scheme == "dark":
        bg_color = "#0a0a0f"
        text_color = "#ffffff"
        text_muted = "#888899"
    else:
        bg_color = "#f4f4f6"
        text_color = "#111118"
        text_muted = "#666677"
        
    # Varied grid colors mimicking the tutorial's colorful blocks
    grid_colors = [
        "#ff4757", "#2ed573", "#1e90ff", "#ffa502", "#a4b0be", 
        "#ff6348", "#7bed9f", "#70a1ff", "#eccc68", "#57606f",
        "#ff7f50", "#2f3542", "#3742fa", "#ff6b81", "#16a085"
    ]

    # === CSS ===
    css = f"""/* Cinematc CSS Animation Suite — generated component */
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
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background-color: var(--bg);
    color: var(--text);
    overflow-x: hidden;
    line-height: 1.6;
}}

.app-container {{
    max-width: {width_px}px;
    margin: 0 auto;
}}

/* --- Hero Section & Spinner --- */
.hero {{
    height: {height_px}px;
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    padding: 2rem;
}}

.hero h1 {{
    font-size: 3.5rem;
    font-weight: 800;
    margin-top: 3rem;
    margin-bottom: 1rem;
    letter-spacing: -0.03em;
}}

.hero p {{
    font-size: 1.25rem;
    color: var(--text-muted);
}}

/* The 3D Glowing Loading Spinner */
.spinner {{
    width: 60px;
    height: 60px;
    border: 5px solid var(--accent);
    border-radius: 6px;
    box-shadow: 
        0 0 15px var(--accent), 
        inset 0 0 15px var(--accent);
    /* 2s duration, easing for snap, infinite loop */
    animation: loading-tumble 2.4s ease-in-out infinite;
}}

/* Multi-axis keyframe sequence extracted from tutorial */
@keyframes loading-tumble {{
    0% {{
        transform: perspective(400px) rotateX(0deg) rotateY(0deg) rotateZ(0deg);
    }}
    33% {{
        transform: perspective(400px) rotateX(180deg) rotateY(0deg) rotateZ(0deg);
    }}
    67% {{
        transform: perspective(400px) rotateX(180deg) rotateY(180deg) rotateZ(0deg);
    }}
    100% {{
        transform: perspective(400px) rotateX(180deg) rotateY(180deg) rotateZ(180deg);
    }}
}}

/* --- Scroll Reveal Grid --- */
.grid-section {{
    padding: 4rem 2rem 8rem;
}}

.grid-container {{
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    grid-auto-rows: 200px;
    gap: 24px;
}}

/* Card base state (hidden/shrunk) */
.card {{
    border-radius: 12px;
    opacity: 0;
    transform: scale(0.5) translateY(40px);
    transition: opacity 0.8s cubic-bezier(0.16, 1, 0.3, 1), 
                transform 0.8s cubic-bezier(0.16, 1, 0.3, 1);
}}

/* Card revealed state (triggered by JS IntersectionObserver) */
.card.visible {{
    opacity: 1;
    transform: scale(1) translateY(0);
}}

/* Modifying grid spans to look like the tutorial's varied masonry */
.card:nth-child(3n) {{ grid-column: span 2; }}
.card:nth-child(7n) {{ grid-row: span 2; }}

@media (max-width: 768px) {{
    .hero h1 {{ font-size: 2.5rem; }}
    .card:nth-child(3n) {{ grid-column: span 1; }}
}}
"""

    # === HTML ===
    cards_html = ""
    for i in range(15):
        color = grid_colors[i % len(grid_colors)]
        cards_html += f'            <div class="card" style="background-color: {color};"></div>\n'

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
    <div class="app-container">
        <!-- Hero Section with 3D Keyframe Spinner -->
        <header class="hero">
            <div class="spinner"></div>
            <h1>{title_text}</h1>
            <p>{body_text}</p>
        </header>

        <!-- Grid Section with Scroll Reveals -->
        <section class="grid-section">
            <div class="grid-container">
{cards_html}
            </div>
        </section>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Scroll Reveal logic using IntersectionObserver
// This replicates CSS `animation-timeline: view()` but works in all modern browsers.

document.addEventListener('DOMContentLoaded', () => {{
    const cards = document.querySelectorAll('.card');

    // Configure the observer to trigger when elements come 10% into the viewport
    const observerOptions = {{
        root: null,
        rootMargin: '0px 0px -10% 0px',
        threshold: 0.1
    }};

    const revealObserver = new IntersectionObserver((entries, observer) => {{
        entries.forEach(entry => {{
            if (entry.isIntersecting) {{
                // Add class to trigger CSS transition
                entry.target.classList.add('visible');
                
                // Optional: Stop observing once revealed if you only want it to happen once
                // observer.unobserve(entry.target); 
            }} else {{
                // Remove class when scrolling back up to repeat the animation (mimics CSS view timeline)
                entry.target.classList.remove('visible');
            }}
        }});
    }}, observerOptions);

    // Attach observer to all grid cards
    cards.forEach(card => {{
        revealObserver.observe(card);
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
