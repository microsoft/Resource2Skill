def create_component(
    output_dir: str,
    title_text: str = "Cinematic Animations",
    body_text: str = "Scroll down inside the container to see the scroll-driven reveals.",
    color_scheme: str = "dark",
    accent_color: str = "#00ffff", 
    width_px: int = 1000,
    height_px: int = 700,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the 3D loader and Scroll-Driven Reveal animations.
    """
    import os
    import random

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors ===
    if color_scheme == "dark":
        bg_color = "#080b12"
        surface_color = "#121826"
        text_color = "#f0f0f0"
        text_muted = "#a0aabf"
    else:
        bg_color = "#e0e5ec"
        surface_color = "#ffffff"
        text_color = "#1a1a2e"
        text_muted = "#6b7280"

    # Deterministic color palette for blocks to match tutorial aesthetics
    block_colors = ["#E27D60", "#85DCBA", "#E8A87C", "#C38D9E", "#41B3A3", "#F23460", "#2A363B", "#99B898", "#FECEAB", "#FF847C"]
    
    # Generate gallery blocks HTML
    random.seed(42)
    blocks_html = ""
    for _ in range(30):
        bg = random.choice(block_colors)
        blocks_html += f'            <div class="block" style="background-color: {bg};"></div>\n'

    # === CSS ===
    css = f"""/* CSS Cinematic Animations — generated component */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --surface: {surface_color};
    --text: {text_color};
    --text-muted: {text_muted};
    --accent: {accent_color};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background: var(--bg);
    color: var(--text);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
}}

/* Scrollable Component Wrapper */
.container {{
    width: var(--width);
    height: var(--height);
    max-width: 95vw;
    max-height: 95vh;
    background: var(--surface);
    border-radius: 16px;
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
    overflow-y: auto;
    overflow-x: hidden;
    position: relative;
    scroll-behavior: smooth;
}}

/* Header & Typography */
.header {{
    padding: 60px 40px;
    text-align: center;
    border-bottom: 1px solid rgba(255, 255, 255, 0.05);
}}

.title {{
    font-size: 2.5rem;
    font-weight: 700;
    letter-spacing: -0.02em;
    margin-bottom: 12px;
}}

.body-text {{
    font-size: 1.1rem;
    color: var(--text-muted);
    max-width: 500px;
    margin: 0 auto 40px auto;
    line-height: 1.5;
}}

/* 1. Glowing 3D Loader Animation */
.loader {{
    width: 50px;
    height: 50px;
    margin: 0 auto;
    border: 5px solid var(--accent);
    border-radius: 4px;
    box-shadow: 0 0 12px var(--accent), inset 0 0 12px var(--accent);
    animation: loader-spin 2s ease-in-out infinite both;
}}

@keyframes loader-spin {{
    0%   {{ transform: rotateX(0deg) rotateY(0deg) rotateZ(0deg); }}
    33%  {{ transform: rotateX(180deg) rotateY(0deg) rotateZ(0deg); }}
    67%  {{ transform: rotateX(180deg) rotateY(180deg) rotateZ(0deg); }}
    100% {{ transform: rotateX(180deg) rotateY(180deg) rotateZ(180deg); }}
}}

/* Gallery Layout */
.gallery {{
    display: flex;
    flex-wrap: wrap;
    gap: 20px;
    padding: 40px;
    justify-content: center;
}}

/* 2. Scroll Reveal Block Base */
.block {{
    height: 140px;
    border-radius: 8px;
    flex-grow: 1;
    min-width: 150px;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    
    /* Fallback styles for JS Intersection Observer */
    opacity: 0;
    transform: scale(0.5);
    transition: opacity 0.6s cubic-bezier(0.16, 1, 0.3, 1), transform 0.6s cubic-bezier(0.16, 1, 0.3, 1);
}}

/* Sizing variations to simulate masonry organic feel */
.block:nth-child(3n) {{ flex-basis: 280px; }}
.block:nth-child(5n) {{ flex-basis: 220px; }}
.block:nth-child(7n) {{ flex-basis: 350px; }}

/* JS Fallback Active State */
.block.visible {{
    opacity: 1;
    transform: scale(1);
}}

/* Native CSS Scroll-Driven Animation (Chrome/Edge 115+) */
@supports (animation-timeline: view()) {{
    .block {{
        /* Reset JS fallback manual transitions */
        opacity: 1; 
        transform: none;
        transition: none;
        
        /* Apply native scroll timeline */
        animation: block-reveal linear both;
        animation-timeline: view();
        /* Animation starts entering viewport, finishes when it covers 30% */
        animation-range: entry 0% cover 30%;
    }}
}}

@keyframes block-reveal {{
    from {{
        opacity: 0;
        scale: 0.5;
    }}
    to {{
        opacity: 1;
        scale: 1;
    }}
}}

/* Accessibility: Respect user motion preferences */
@media (prefers-reduced-motion: reduce) {{
    .loader {{
        animation: none;
        transform: none;
    }}
    .block {{
        animation: none !important;
        transition: none !important;
        opacity: 1 !important;
        transform: none !important;
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
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        <header class="header">
            <h1 class="title">{title_text}</h1>
            <p class="body-text">{body_text}</p>
            <div class="loader"></div>
        </header>
        <div class="gallery">
{blocks_html}
        </div>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Intersection Observer Fallback for Scroll Reveals
// This ensures the animation works in Firefox and Safari which do not yet natively support 'animation-timeline: view()'

document.addEventListener('DOMContentLoaded', () => {{
    // Only apply JS fallback if native CSS feature is NOT supported
    if (!CSS.supports('animation-timeline: view()')) {{
        const blocks = document.querySelectorAll('.block');
        
        const observerOptions = {{
            root: document.querySelector('.container'), // Observe scrolling within the specific container
            rootMargin: '0px',
            threshold: 0.15 // Trigger when 15% of the block is visible
        }};

        const observer = new IntersectionObserver((entries) => {{
            entries.forEach(entry => {{
                if (entry.isIntersecting) {{
                    entry.target.classList.add('visible');
                }} else {{
                    // Optional: remove class to animate out when scrolling away
                    // entry.target.classList.remove('visible'); 
                }}
            }});
        }}, observerOptions);

        blocks.forEach(block => observer.observe(block));
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
