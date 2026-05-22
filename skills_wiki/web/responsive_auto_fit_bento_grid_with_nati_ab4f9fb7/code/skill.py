def create_component(
    output_dir: str,
    title_text: str = "Explore Our Features",
    body_text: str = "A fully responsive, auto-fitting bento grid utilizing native CSS grid stacking.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#00bfff",     # CSS hex color for accent
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Responsive Auto-Fit Bento Grid visual effect.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme and accent_color ===
    if color_scheme == "dark":
        bg_color = "#0a0a0f"
        text_color = "#ffffff"
        text_muted = "#a0a0ab"
        card_bg = "#1a1a24"
        card_border = "rgba(255, 255, 255, 0.08)"
        shadow = "rgba(0, 0, 0, 0.4)"
    else:
        bg_color = "#f4f4f8"
        text_color = "#111118"
        text_muted = "#50505a"
        card_bg = "#ffffff"
        card_border = "rgba(0, 0, 0, 0.08)"
        shadow = "rgba(0, 0, 0, 0.05)"

    # Escape HTML safely
    import html as html_lib
    safe_title = html_lib.escape(title_text)
    safe_body = html_lib.escape(body_text)

    # === CSS ===
    css = f"""/* Responsive Auto-Fit Bento Grid */
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
    --card-bg: {card_bg};
    --card-border: {card_border};
    --shadow: {shadow};
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background: var(--bg);
    color: var(--text);
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 4rem 2rem;
}}

.wrapper {{
    width: 100%;
    max-width: {width_px}px;
}}

.header {{
    text-align: center;
    margin-bottom: 4rem;
}}

.header h1 {{
    font-size: 2.5rem;
    font-weight: 700;
    margin-bottom: 1rem;
    letter-spacing: -0.02em;
}}

.header p {{
    font-size: 1.125rem;
    color: var(--text-muted);
    max-width: 600px;
    margin: 0 auto;
    line-height: 1.6;
}}

/* MACRO LAYOUT: The Auto-Fitting Grid */
.bento-grid {{
    display: grid;
    /* This is the magic formula for responsive wrapping without media queries */
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 1.5rem;
}}

/* MICRO LAYOUT: The Grid Stacked Card */
.bento-card {{
    position: relative;
    display: grid;
    /* Create a single cell named 'stack' */
    grid-template-areas: "stack";
    border-radius: 1.25rem;
    overflow: hidden;
    background: var(--card-bg);
    border: 1px solid var(--card-border);
    box-shadow: 0 10px 30px var(--shadow);
    text-decoration: none;
    aspect-ratio: 4/5;
    transition: transform 0.3s cubic-bezier(0.2, 0.8, 0.2, 1), 
                box-shadow 0.3s cubic-bezier(0.2, 0.8, 0.2, 1),
                border-color 0.3s ease;
    
    /* Animation initial state */
    opacity: 0;
    transform: translateY(20px);
}}

/* Assign ALL direct children to the 'stack' area */
.bento-card > * {{
    grid-area: stack;
}}

.bento-image {{
    width: 100%;
    height: 100%;
    object-fit: cover;
    transition: transform 0.7s ease;
}}

.bento-overlay {{
    /* Push content to the bottom and stretch horizontally */
    align-self: end;
    display: flex;
    flex-direction: column;
    justify-content: flex-end;
    padding: 2rem 1.5rem;
    height: 60%;
    background: linear-gradient(to top, rgba(0,0,0,0.9) 0%, rgba(0,0,0,0) 100%);
    color: #ffffff; /* Always white due to dark gradient */
    z-index: 10;
}}

.bento-tag {{
    align-self: flex-start;
    background: var(--accent);
    color: #fff;
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    padding: 0.35rem 0.75rem;
    border-radius: 100px;
    margin-bottom: 0.75rem;
}}

.bento-title {{
    font-size: 1.5rem;
    font-weight: 600;
    margin-bottom: 0.5rem;
    line-height: 1.2;
}}

.bento-desc {{
    font-size: 0.95rem;
    color: rgba(255,255,255,0.7);
    line-height: 1.5;
}}

/* Interactive States */
.bento-card:hover {{
    transform: translateY(-8px);
    box-shadow: 0 20px 40px var(--shadow);
    border-color: var(--accent);
}}

.bento-card:hover .bento-image {{
    transform: scale(1.05);
}}

/* JS Animation Class */
.bento-card.is-visible {{
    opacity: 1;
    transform: translateY(0);
}}

/* Accessibility: Reduce Motion */
@media (prefers-reduced-motion: reduce) {{
    .bento-card {{
        transition: none;
        opacity: 1;
        transform: none;
    }}
    .bento-image {{ transition: none; }}
}}
"""

    # === Generate Sample Cards ===
    cards_html = ""
    sample_data = [
        ("Architecture", "Modern Paradigms", "Building scalable layouts with native CSS properties.", "1018"),
        ("Analytics", "Real-time Metrics", "Visualize data efficiently using fluid grid systems.", "1035"),
        ("Workflow", "Streamlined Processes", "Reduce media query dependency and write cleaner code.", "1040"),
        ("Integration", "Seamless Stacking", "Layer elements flawlessly without absolute positioning.", "1048"),
        ("Performance", "Hardware Accelerated", "Utilize browser optimizations for buttery smooth UX.", "1055"),
        ("Design", "Adaptive Aesthetics", "Bento-style containers that naturally fit any viewport.", "1062")
    ]

    for i, (tag, title, desc, img_id) in enumerate(sample_data):
        # Calculate transition delay for staggered effect (only used if JS fails, otherwise handled by JS)
        delay = i * 0.1
        cards_html += f"""
            <a href="#" class="bento-card" aria-label="{title}">
                <img src="https://picsum.photos/id/{img_id}/600/800" alt="Abstract background for {title}" class="bento-image" loading="lazy">
                <div class="bento-overlay">
                    <span class="bento-tag">{tag}</span>
                    <h2 class="bento-title">{title}</h2>
                    <p class="bento-desc">{desc}</p>
                </div>
            </a>"""

    # === HTML ===
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{safe_title}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <main class="wrapper">
        <header class="header">
            <h1>{safe_title}</h1>
            <p>{safe_body}</p>
        </header>

        <section class="bento-grid">
            {cards_html}
        </section>
    </main>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Staggered Entrance Animation using Intersection Observer
document.addEventListener('DOMContentLoaded', () => {{
    const cards = document.querySelectorAll('.bento-card');
    
    // Check for reduced motion preference
    const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    
    if (prefersReducedMotion) {{
        // If reduced motion is requested, show all immediately
        cards.forEach(card => card.classList.add('is-visible'));
        return;
    }}

    const observerOptions = {{
        root: null,
        rootMargin: '0px 0px -50px 0px',
        threshold: 0.1
    }};

    const cardObserver = new IntersectionObserver((entries, observer) => {{
        entries.forEach((entry, index) => {{
            if (entry.isIntersecting) {{
                // Add a staggered delay based on the element's position in the DOM
                setTimeout(() => {{
                    entry.target.classList.add('is-visible');
                }}, index * 100); // 100ms stagger
                
                // Stop observing once visible
                observer.unobserve(entry.target);
            }}
        }});
    }}, observerOptions);

    cards.forEach(card => {{
        cardObserver.observe(card);
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
