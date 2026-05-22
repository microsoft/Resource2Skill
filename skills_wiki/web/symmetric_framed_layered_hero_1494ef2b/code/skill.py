def create_component(
    output_dir: str,
    title_text: str = "WELCOME TO MY FIRST WEBSITE",
    body_text: str = "Nam interdum felis at felis placerat, sed varius massa ultricies. Integer quis nisi non dolor scelerisque efficitur at sed turpis.",
    color_scheme: str = "dark",
    accent_color: str = "#C13584",
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Symmetric Framed Layered Hero.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Derive colors based on scheme
    if color_scheme == "dark":
        bg_color = "#1A253A"
        text_color = "#FFFFFF"
        surface_dot = "rgba(255, 255, 255, 0.06)"
        subject_end = "#0D1320"
        quote_text = "rgba(255, 255, 255, 0.8)"
    else:
        bg_color = "#F8FAFC"
        text_color = "#0F172A"
        surface_dot = "rgba(0, 0, 0, 0.06)"
        subject_end = "#CBD5E1"
        quote_text = "rgba(15, 23, 42, 0.8)"

    css = f"""/* Symmetric Framed Layered Hero */
:root {{
    --bg-color: {bg_color};
    --text-color: {text_color};
    --quote-color: {quote_text};
    --accent-color: {accent_color};
    --surface-dot: {surface_dot};
    --subject-end: {subject_end};
    --width: {width_px}px;
    --height: {height_px}px;
}}

* {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: 'Inter', system-ui, sans-serif;
    background-color: #000; /* Outer wrapper dark fallback */
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
    overflow-x: hidden;
}}

/* Main Component Container */
.hero-container {{
    width: var(--width);
    height: var(--height);
    max-width: 100%;
    position: relative;
    background-color: var(--bg-color);
    background-image: radial-gradient(var(--surface-dot) 2px, transparent 2px);
    background-size: 32px 32px;
    background-position: center center;
    display: flex;
    overflow: hidden;
}}

/* The Centered Subject (Replaces Portrait Image) */
.subject-placeholder {{
    position: absolute;
    bottom: 0;
    left: 50%;
    transform: translateX(-50%);
    width: 32vw;
    max-width: 420px;
    height: 75%;
    background: linear-gradient(155deg, var(--accent-color) 0%, var(--subject-end) 100%);
    border-radius: 200px 200px 0 0;
    z-index: 1;
    box-shadow: 
        inset -15px -15px 40px rgba(0, 0, 0, 0.4),
        inset 15px 15px 40px rgba(255, 255, 255, 0.15),
        0 -10px 60px rgba(0, 0, 0, 0.2);
    border-top: 1px solid rgba(255, 255, 255, 0.2);
    border-left: 1px solid rgba(255, 255, 255, 0.2);
    opacity: 0;
    animation: riseUp 1s cubic-bezier(0.2, 0.8, 0.2, 1) 0.2s forwards;
    will-change: transform;
}}

/* Left and Right Columns */
.hero-left, .hero-right {{
    flex: 1;
    display: flex;
    flex-direction: column;
    justify-content: center;
    z-index: 2; /* Sits above the subject */
    padding-bottom: 8%; /* Visual lift matching tutorial */
}}

.hero-left {{
    align-items: flex-end;
    padding-right: 5vw;
}}

.hero-right {{
    align-items: flex-start;
    padding-left: 5vw;
}}

/* Content Wrappers for max-width constraints */
.intro-content {{
    max-width: 480px;
    opacity: 0;
    animation: slideInLeft 0.8s cubic-bezier(0.2, 0.8, 0.2, 1) forwards;
}}

.quotes-content {{
    max-width: 380px;
    opacity: 0;
    animation: slideInRight 0.8s cubic-bezier(0.2, 0.8, 0.2, 1) 0.1s forwards;
}}

/* Typography */
h1 {{
    color: var(--text-color);
    font-size: clamp(40px, 4.5vw, 84px);
    line-height: 1.05;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: -0.02em;
    margin-bottom: 24px;
}}

.intro-text {{
    color: var(--text-color);
    font-size: 18px;
    line-height: 1.6;
    margin-bottom: 32px;
    opacity: 0.9;
}}

.btn {{
    display: inline-block;
    background-color: var(--accent-color);
    color: #FFFFFF;
    text-decoration: none;
    font-weight: 600;
    font-size: 16px;
    padding: 14px 32px;
    border-radius: 4px;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    transition: filter 0.3s ease, transform 0.2s ease;
}}

.btn:hover {{
    filter: brightness(1.1);
    transform: translateY(-2px);
}}

/* Quotes Styling */
.quote-block {{
    border-left: 4px solid var(--accent-color);
    padding-left: 24px;
    margin-bottom: 48px;
}}

.quote-block:last-child {{
    margin-bottom: 0;
}}

.quote-text {{
    color: var(--quote-color);
    font-size: 18px;
    line-height: 1.6;
    font-style: normal;
}}

.quote-author {{
    display: block;
    margin-top: 12px;
    color: var(--text-color);
    font-weight: 600;
    font-size: 16px;
}}

/* Animations */
@keyframes slideInLeft {{
    from {{ opacity: 0; transform: translateX(-40px); }}
    to {{ opacity: 1; transform: translateX(0); }}
}}

@keyframes slideInRight {{
    from {{ opacity: 0; transform: translateX(40px); }}
    to {{ opacity: 1; transform: translateX(0); }}
}}

@keyframes riseUp {{
    from {{ opacity: 0; transform: translate(-50%, 80px); }}
    to {{ opacity: 1; transform: translate(-50%, 0); }}
}}

/* Responsive Graceful Degradation */
@media (max-width: 900px) {{
    .hero-container {{
        flex-direction: column;
        height: auto;
        min-height: var(--height);
        justify-content: flex-start;
        padding-top: 10%;
    }}
    
    .hero-left, .hero-right {{
        align-items: center;
        padding: 0 6vw;
        text-align: center;
        padding-bottom: 40px;
    }}
    
    .quote-block {{
        text-align: left; /* Keep quotes readable */
    }}
    
    .subject-placeholder {{
        height: 50%;
        width: 70vw;
        opacity: 0.15 !important; /* Fade heavily to allow reading overlaid text */
        z-index: 0;
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
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <main class="hero-container">
        
        <!-- The Central Framed Subject -->
        <div class="subject-placeholder"></div>

        <!-- Left Framing Content -->
        <div class="hero-left">
            <div class="intro-content">
                <h1>{title_text}</h1>
                <p class="intro-text">{body_text}</p>
                <a href="#" class="btn">MY WORK</a>
            </div>
        </div>

        <!-- Right Framing Content -->
        <div class="hero-right">
            <div class="quotes-content">
                <div class="quote-block">
                    <p class="quote-text">"The more that you read, the more things you will know. The more that you learn, the more places you'll go."</p>
                    <span class="quote-author">- Dr. Seuss</span>
                </div>
                <div class="quote-block">
                    <p class="quote-text">"For the best return on your money, pour your purse into your head."</p>
                    <span class="quote-author">- Benjamin Franklin</span>
                </div>
            </div>
        </div>

    </main>
    <script src="script.js"></script>
</body>
</html>"""

    js = """// Layered depth mouse-parallax effect
document.addEventListener('DOMContentLoaded', () => {
    const container = document.querySelector('.hero-container');
    const subject = document.querySelector('.subject-placeholder');
    const intro = document.querySelector('.intro-content');
    const quotes = document.querySelector('.quotes-content');

    // Only apply hover parallax on desktop devices
    if (window.matchMedia("(min-width: 901px)").matches) {
        container.addEventListener('mousemove', (e) => {
            const rect = container.getBoundingClientRect();
            
            // Calculate mouse position relative to container center (-1 to 1)
            const x = ((e.clientX - rect.left) / rect.width - 0.5) * 2;
            const y = ((e.clientY - rect.top) / rect.height - 0.5) * 2;

            // Apply different translation multipliers to create depth layers
            // Subject moves opposite to mouse
            if(subject) subject.style.transform = `translate(calc(-50% + ${x * -15}px), ${y * -10}px)`;
            
            // Text moves with mouse, seemingly floating above
            if(intro) intro.style.transform = `translate(${x * 12}px, ${y * 8}px)`;
            if(quotes) quotes.style.transform = `translate(${x * 12}px, ${y * 8}px)`;
        });

        // Reset positions on leave
        container.addEventListener('mouseleave', () => {
            if(subject) subject.style.transform = `translate(-50%, 0)`;
            if(intro) intro.style.transform = `translate(0, 0)`;
            if(quotes) quotes.style.transform = `translate(0, 0)`;
        });
    }
});
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
