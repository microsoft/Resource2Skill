def create_component(
    output_dir: str,
    title_text: str = "Scroll Animation Gallery",
    body_text: str = "Scroll down to see the native CSS View Timeline reveal effect in action.",
    color_scheme: str = "dark",        
    accent_color: str = "#00E5FF",     
    width_px: int = 1000,
    height_px: int = 700,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Pure CSS 3D Glow Spinner & Scroll-Driven Reveal.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Derive theme colors
    if color_scheme == "dark":
        bg_color = "#0f172a"          # Slate 900
        text_color = "#f8fafc"        # Slate 50
        surface_color = "#1e293b"     # Slate 800
        border_color = "rgba(255, 255, 255, 0.1)"
        shadow_color = "rgba(0, 0, 0, 0.5)"
    else:
        bg_color = "#f3f4f6"          # Gray 100
        text_color = "#111827"        # Gray 900
        surface_color = "#ffffff"     # White
        border_color = "rgba(0, 0, 0, 0.08)"
        shadow_color = "rgba(0, 0, 0, 0.1)"

    # Generate 24 placeholder cards for the gallery
    cards_html = "\n        ".join([f'<div class="card">{i+1}</div>' for i in range(24)])

    # === CSS ===
    css = f"""/* Pure CSS 3D Glow Spinner & Scroll-Driven Reveal */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');

*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --text: {text_color};
    --surface: {surface_color};
    --border: {border_color};
    --accent: {accent_color};
    --shadow: {shadow_color};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Inter', system-ui, sans-serif;
    background: #000; /* Dark canvas to make the component pop */
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden; /* Lock body, scroll happens inside component */
}}

/* Main Component Scroll Container */
.container {{
    width: var(--width);
    height: var(--height);
    background: var(--bg);
    color: var(--text);
    border: 1px solid var(--border);
    border-radius: 16px;
    box-shadow: 0 25px 50px -12px var(--shadow);
    overflow-y: auto;
    scroll-behavior: smooth;
    position: relative;
}}

/* Hero Section */
.hero {{
    min-height: 80vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    padding: 2rem;
    border-bottom: 1px solid var(--border);
}}

.title {{
    font-size: 3.5rem;
    font-weight: 800;
    margin-bottom: 1rem;
    background: linear-gradient(135deg, var(--text), var(--accent));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}}

.body-text {{
    font-size: 1.25rem;
    opacity: 0.7;
    max-width: 600px;
    margin-bottom: 4rem;
    line-height: 1.6;
}}

/* 1. Pure CSS 3D Glowing Spinner */
.spinner {{
    width: 60px;
    height: 60px;
    border: 6px solid var(--accent);
    border-radius: 8px;
    box-shadow: 0 0 15px var(--accent), inset 0 0 15px var(--accent);
    /* Ease-in-out gives a nice pause at each 3D state */
    animation: spin3d 2.5s ease-in-out infinite;
}}

@keyframes spin3d {{
    0% {{ transform: rotateX(0deg) rotateY(0deg) rotateZ(0deg); }}
    33% {{ transform: rotateX(180deg) rotateY(0deg) rotateZ(0deg); }}
    67% {{ transform: rotateX(180deg) rotateY(180deg) rotateZ(0deg); }}
    100% {{ transform: rotateX(180deg) rotateY(180deg) rotateZ(180deg); }}
}}

/* 2. Scroll-Driven Reveal Gallery */
.gallery {{
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
    gap: 24px;
    padding: 60px 40px;
}}

.card {{
    background: linear-gradient(145deg, var(--surface), var(--bg));
    border: 1px solid var(--border);
    border-radius: 12px;
    height: 180px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 2.5rem;
    font-weight: 800;
    color: var(--accent);
    box-shadow: 0 10px 20px -5px var(--shadow);
    
    /* Modern View Timeline Animation */
    animation: reveal linear both;
    animation-timeline: view();
    /* Triggers between the moment it enters the screen (0%) and halfway up (50%) */
    animation-range: entry 0% cover 50%;
}}

@keyframes reveal {{
    from {{
        opacity: 0;
        scale: 0.5;
    }}
    to {{
        opacity: 1;
        scale: 1;
    }}
}}

/* 3. Progressive Enhancement / Fallback for Safari & older browsers */
@supports not (animation-timeline: view()) {{
    .card {{
        animation: none; /* Disable timeline attachment */
        opacity: 0;
        scale: 0.8; /* Softer fallback scale */
        transition: opacity 0.6s ease-out, scale 0.6s cubic-bezier(0.2, 0.8, 0.2, 1);
    }}
    
    .card.is-visible {{
        opacity: 1;
        scale: 1;
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
        
        <header class="hero">
            <h1 class="title">{title_text}</h1>
            <p class="body-text">{body_text}</p>
            <div class="spinner"></div>
        </header>

        <main class="gallery">
            {cards_html}
        </main>

    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Scroll Reveal Progressive Enhancement Fallback
document.addEventListener('DOMContentLoaded', () => {{
    // Check if the browser supports native CSS View Timelines
    const isTimelineSupported = CSS.supports('animation-timeline', 'view()');

    if (!isTimelineSupported) {{
        console.info("CSS animation-timeline not supported. Booting up IntersectionObserver fallback.");
        
        const observerOptions = {{
            root: document.querySelector('.container'), // Constrain to component scrollport
            rootMargin: '0px',
            threshold: 0.15 // Trigger when 15% visible
        }};

        const observer = new IntersectionObserver((entries) => {{
            entries.forEach(entry => {{
                if (entry.isIntersecting) {{
                    entry.target.classList.add('is-visible');
                }} else {{
                    // Remove class when scrolling out of view to re-animate on scroll up
                    entry.target.classList.remove('is-visible');
                }}
            }});
        }}, observerOptions);

        document.querySelectorAll('.card').forEach(card => {{
            observer.observe(card);
        }});
    }} else {{
        console.info("Native CSS animation-timeline is supported. Running zero-JS animations!");
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
