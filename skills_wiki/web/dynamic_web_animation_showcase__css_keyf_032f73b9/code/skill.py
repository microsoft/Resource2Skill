import os

def create_component(
    output_dir: str,
    main_title: str = "Welcome to tomorrow we got cookies",
    highlight_word: str = "tomorrow",
    call_to_action_text: str = "Order now!",
    section2_title: str = "Innovation at Its Core",
    section2_subtitle: str = "Tomorrow isn't just a cookie company, it's a revolution in the world of sweets.",
    section3_title: str = "Custom Cookies",
    section3_button_text: str = "Make your own today!",
    color_scheme: str = "dark",  # "dark" or "light"
    accent_color: str = "#CC3F4E", # Red for underlines and buttons (from video)
    width_px: int = 1200, # Main content max width for desktop view
    height_px: int = 1000, # This will be minimum body height to ensure scrollability
    **kwargs,
) -> dict:
    """
    Create a web component reproducing key CSS animation, transition, and scroll animation effects from the tutorial.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme and accent_color ===
    if color_scheme == "dark":
        bg_color = "#131217" # From video
        text_color = "#FFFFFF"
        secondary_text_color = "#A0A0A0"
    else:
        bg_color = "#FFFFFF"
        text_color = "#131217"
        secondary_text_color = "#555555"

    # SVG for squiggly line (dynamically colored)
    squiggly_svg = f"""<svg width="100%" height="10px" viewBox="0 0 100 10" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M0 5C10 2 20 8 30 5C40 2 50 8 60 5C70 2 80 8 90 5C100 2 100 5 100 5" stroke="{accent_color}" stroke-width="2" stroke-linecap="round"/>
</svg>"""
    squiggly_encoded = f"data:image/svg+xml;utf8,{squiggly_svg.replace('#', '%23').replace('\\n', '')}"

    # SVG for cubes (section 2 image, dynamically colored outline)
    cubes_svg = f"""<svg width="400" height="400" viewBox="0 0 400 400" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M100 50L200 100L200 200L100 150L100 50Z" stroke="{text_color}" stroke-width="4" stroke-linejoin="round" fill="rgba(255,255,255,0.1)"/>
    <path d="M200 100L300 50L300 150L200 200L200 100Z" stroke="{text_color}" stroke-width="4" stroke-linejoin="round" fill="rgba(255,255,255,0.1)"/>
    <path d="M100 150L200 200L200 300L100 250L100 150Z" stroke="{text_color}" stroke-width="4" stroke-linejoin="round" fill="rgba(255,255,255,0.1)"/>
    <path d="M200 200L300 150L300 250L200 300L200 200Z" stroke="{text_color}" stroke-width="4" stroke-linejoin="round" fill="rgba(255,255,255,0.1)"/>
</svg>"""
    cubes_encoded = f"data:image/svg+xml;utf8,{cubes_svg.replace('#', '%23').replace('\\n', '')}"


    # === CSS ===
    css = f"""
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    :root {{
        --bg-color: {bg_color};
        --text-color: {text_color};
        --secondary-text-color: {secondary_text_color};
        --accent-color: {accent_color};
        --desktop-max-width: {width_px}px;
    }}

    * {{
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }}

    body {{
        font-family: 'Inter', sans-serif;
        background-color: var(--bg-color);
        color: var(--text-color);
        min-height: {height_px}px; /* Ensure enough height for scroll animations */
        line-height: 1.6;
        overflow-x: hidden; /* Prevent horizontal scroll from transform effects */
        display: flex;
        flex-direction: column;
        align-items: center; /* Center content horizontally on the page */
    }}

    h1, h2, h3, p {{
        text-align: center;
        margin-bottom: 20px;
    }}

    .section {{
        min-height: 100vh; /* Each section fills at least the viewport height */
        width: 100%;
        max-width: var(--desktop-max-width);
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        padding: 40px 20px;
        box-sizing: border-box;
        position: relative; /* For containing absolute elements like buttons */
    }}

    /* --- Header Section (Always visible) --- */
    .header-section {{
        padding-top: 100px; /* Offset for aesthetic */
        min-height: 50vh; /* Shorter for top section */
    }}
    .header-title {{
        font-size: 3.5rem;
        font-weight: 700;
        margin-bottom: 30px;
        position: relative; /* For containing the highlight-word span */
    }}
    .highlight-word {{
        position: relative;
        display: inline-block;
        color: var(--text-color); /* Original text color */
        overflow: hidden; /* Hide the ::after content until it slides in */
    }}
    .highlight-word::after {{
        content: '{highlight_word}'; /* The animated text */
        position: absolute;
        bottom: 0;
        left: 0;
        width: 100%;
        height: 110%; /* To cover text vertically for sliding */
        background-image: url('{squiggly_encoded}');
        background-repeat: no-repeat;
        background-position: bottom;
        background-size: contain;
        color: var(--accent-color); /* Highlight color */
        opacity: 0;
        transform: translateY(110%); /* Start off-screen below */
        animation: slideInSquiggle 0.5s ease-out 0.5s forwards; /* 0.5s delay after page load */
    }}
    @keyframes slideInSquiggle {{
        from {{ opacity: 0; transform: translateY(110%); }}
        to {{ opacity: 1; transform: translateY(0%); }}
    }}

    .cta-button {{
        background-color: transparent;
        color: var(--text-color);
        border: none;
        padding: 15px 30px;
        font-size: 1.2rem;
        font-weight: 600;
        cursor: pointer;
        position: relative;
        overflow: hidden;
        z-index: 1;
        transition: color 0.3s ease;
        margin-top: 50px;
    }}
    .cta-button::after {{
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 0; /* Start with zero width */
        height: 100%;
        background-color: var(--accent-color);
        z-index: -1;
        transition: width 0.3s ease-out; /* Animate width */
    }}
    .cta-button:hover::after {{
        width: 100%; /* Expand to full width on hover */
    }}
    .cta-button:hover {{
        color: var(--bg-color); /* Change text color for contrast */
    }}

    /* --- Section 2 (Scroll-animated) --- */
    .section-2 {{
        flex-direction: row;
        gap: 50px;
        opacity: 0;
        transform: translateY(50px);
        transition: opacity 0.8s ease-out, transform 0.8s ease-out;
    }}
    .section-2.visible {{
        opacity: 1;
        transform: translateY(0);
    }}
    .section-2-content, .section-2-image {{
        flex: 1;
        max-width: 500px;
        text-align: left;
    }}
    .section-2-image {{
        text-align: center;
    }}
    .section-2-image img {{
        max-width: 100%;
        height: auto;
    }}
    .section-2 h2 {{
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 20px;
        color: var(--text-color);
    }}
    .section-2 h2 .red-text {{
        color: var(--accent-color);
    }}
    .section-2 p {{
        font-size: 1.1rem;
        color: var(--secondary-text-color);
        line-height: 1.8;
    }}

    /* --- Section 3 (Scroll-animated with button hover) --- */
    .section-3 {{
        opacity: 0;
        transform: translateY(50px);
        transition: opacity 0.8s ease-out, transform 0.8s ease-out;
    }}
    .section-3.visible {{
        opacity: 1;
        transform: translateY(0);
    }}
    .section-3 h2 {{
        font-size: 3rem;
        font-weight: 700;
        margin-bottom: 30px;
    }}

    /* Responsive adjustments */
    @media (max-width: 768px) {{
        .header-title {{
            font-size: 2.5rem;
        }}
        .section-2 {{
            flex-direction: column;
            gap: 30px;
        }}
        .section-2-content, .section-2-image {{
             max-width: 100%;
        }}
        .section-2 h2 {{
            font-size: 2rem;
        }}
        .section-3 h2 {{
            font-size: 2.2rem;
        }}
        .cta-button {{
            padding: 12px 25px;
            font-size: 1rem;
        }}
    }}
    """

    # HTML structure to include all sections
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Animation Showcase</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <section class="section header-section">
        <h1 class="header-title">{main_title.replace(highlight_word, f'<span class="highlight-word">{highlight_word}</span>')}</h1>
        <button class="cta-button">{call_to_action_text}</button>
    </section>

    <section class="section section-2">
        <div class="section-2-image">
            <img src="{cubes_encoded}" alt="Innovation Cubes">
        </div>
        <div class="section-2-content">
            <h2>{section2_title.replace('Core', '<span class="red-text">Core</span>')}</h2>
            <p>{section2_subtitle}</p>
        </div>
    </section>

    <section class="section section-3">
        <h2>{section3_title}</h2>
        <button class="cta-button">{section3_button_text}</button>
    </section>

    <script src="script.js"></script>
</body>
</html>"""

    # JavaScript to handle scroll animations using IntersectionObserver
    js = f"""
    document.addEventListener('DOMContentLoaded', () => {{
        const scrollAnimatedElements = document.querySelectorAll('.section-2, .section-3');

        const observerOptions = {{
            root: null, // viewport
            rootMargin: '0px',
            threshold: 0.3 // Trigger when 30% of the element is visible
        }};

        const observer = new IntersectionObserver((entries, observer) => {{
            entries.forEach(entry => {{
                if (entry.isIntersecting) {{
                    entry.target.classList.add('visible');
                    // Optionally stop observing once visible if animation only plays once
                    // observer.unobserve(entry.target);
                }} else {{
                    // Optionally remove 'visible' class if you want animation to re-trigger on scroll back
                    // entry.target.classList.remove('visible');
                }}
            }});
        }}, observerOptions);

        scrollAnimatedElements.forEach(element => {{
            observer.observe(element);
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

