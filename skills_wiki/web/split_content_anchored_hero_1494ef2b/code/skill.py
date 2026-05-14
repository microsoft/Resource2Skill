def create_component(
    output_dir: str,
    title_text: str = "WELCOME\nTO MY FIRST\nWEBSITE",
    body_text: str = "A clean, modern approach to web layout focusing on typography, negative space, and a strong central visual anchor.",
    color_scheme: str = "dark",
    accent_color: str = "#c13584",
    width_px: int = 1440,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the 'Split-Content Anchored Hero' effect.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Convert newline characters to <br> for the title
    formatted_title = title_text.replace('\n', '<br>')

    # Theme definitions
    if color_scheme == "dark":
        bg_base = "#1a253a"
        bg_pattern = "rgba(255,255,255,0.03)"
        text_primary = "#ffffff"
        text_secondary = "#a0abbf"
        accent_hover = "#9e2f6e"  # Darker magenta
    else:
        bg_base = "#f0f4f8"
        bg_pattern = "rgba(0,0,0,0.03)"
        text_primary = "#111827"
        text_secondary = "#4b5563"
        accent_hover = "#a1266b"

    css = f"""/* Split-Content Anchored Hero - Style */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg-base: {bg_base};
    --bg-pattern: {bg_pattern};
    --text-primary: {text_primary};
    --text-secondary: {text_secondary};
    --accent: {accent_color};
    --accent-hover: {accent_hover};
    --comp-width: {width_px}px;
    --comp-height: {height_px}px;
}}

body {{
    font-family: 'Roboto', -apple-system, sans-serif;
    background-color: #000;
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 100vh;
}}

/* Component Container constraints */
.hero-wrapper {{
    width: var(--comp-width);
    height: var(--comp-height);
    max-width: 100vw;
    position: relative;
    background-color: var(--bg-base);
    /* Simulated patterned background */
    background-image: 
        radial-gradient(circle at 20% 30%, var(--bg-pattern) 0%, transparent 50%),
        radial-gradient(circle at 80% 70%, var(--bg-pattern) 0%, transparent 50%);
    overflow: hidden;
    display: flex;
    justify-content: center;
    align-items: center;
}}

/* Main Flex Layout */
.hero-content {{
    position: relative;
    z-index: 10;
    display: flex;
    justify-content: space-between;
    align-items: center;
    width: 100%;
    max-width: 1200px;
    padding: 0 40px;
    /* Create a wide gap for the central image */
    gap: clamp(40px, 20vw, 400px); 
}}

/* Left Column: Intro */
.main-intro {{
    flex: 1;
    max-width: 400px;
    position: relative;
}}

.main-intro h1 {{
    color: var(--text-primary);
    font-size: clamp(32px, 4vw, 56px);
    font-weight: 700;
    text-transform: uppercase;
    line-height: 1.1;
    margin-bottom: 24px;
}}

.main-intro p {{
    color: var(--text-secondary);
    font-size: 16px;
    line-height: 1.6;
    margin-bottom: 32px;
}}

.btn {{
    display: inline-block;
    background-color: var(--accent);
    color: #ffffff;
    padding: 14px 32px;
    text-decoration: none;
    text-transform: uppercase;
    font-size: 14px;
    font-weight: 700;
    letter-spacing: 1px;
    transition: background-color 0.3s ease, transform 0.2s ease;
}}

.btn:hover {{
    background-color: var(--accent-hover);
    transform: translateY(-2px);
}}

/* Right Column: Quotes/Secondary Content */
.main-quotes {{
    flex: 1;
    max-width: 400px;
    border-left: 4px solid var(--accent);
    padding-left: 24px;
    display: flex;
    flex-direction: column;
    gap: 40px;
}}

.quote-block {{
    color: var(--text-secondary);
    font-size: 15px;
    line-height: 1.8;
}}

.quote-block span {{
    display: block;
    margin-top: 12px;
    color: var(--text-primary);
    font-weight: 600;
}}

/* The Stagger Effect */
.main-quotes .quote-block:nth-child(2) {{
    margin-left: 40px; /* Pushes the second block outwards */
}}

/* Central Anchored Graphic (Simulating the Portrait) */
.hero-anchor-graphic {{
    position: absolute;
    bottom: 0;
    left: 50%;
    transform: translateX(-50%);
    width: clamp(250px, 30vw, 450px);
    height: 75%;
    /* Abstract silhouette using a gradient and border-radius */
    background: linear-gradient(to top, var(--accent) 0%, rgba(193, 53, 132, 0) 100%);
    border-radius: 200px 200px 0 0;
    z-index: 1;
    opacity: 0.8;
    filter: blur(1px);
}}

/* Simple Responsive Pass */
@media (max-width: 900px) {{
    .hero-content {{
        flex-direction: column;
        gap: 60px;
        text-align: center;
        justify-content: center;
    }}
    .main-quotes {{
        border-left: none;
        border-top: 4px solid var(--accent);
        padding-left: 0;
        padding-top: 24px;
    }}
    .main-quotes .quote-block:nth-child(2) {{
        margin-left: 0;
    }}
    .hero-anchor-graphic {{
        opacity: 0.15; /* Push to background on small screens */
        height: 100%;
        border-radius: 0;
    }}
}}
"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Split-Content Anchored Hero</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="hero-wrapper">
        <!-- Central Visual Anchor -->
        <div class="hero-anchor-graphic"></div>

        <!-- Content Columns -->
        <main class="hero-content">
            
            <div class="main-intro">
                <h1>{formatted_title}</h1>
                <p>{body_text}</p>
                <a href="#" class="btn">My Work</a>
            </div>

            <div class="main-quotes">
                <div class="quote-block">
                    "The more that you read, the more things you will know. The more that you learn, the more places you'll go."
                    <span>- Dr. Seuss</span>
                </div>
                <div class="quote-block">
                    "An investment in knowledge always pays the best interest."
                    <span>- Benjamin Franklin</span>
                </div>
            </div>

        </main>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    js = """// Interaction logic for the Hero Section
document.addEventListener('DOMContentLoaded', () => {
    const btn = document.querySelector('.btn');
    
    // Optional: Subtle parallax effect on the central graphic based on mouse movement
    const graphic = document.querySelector('.hero-anchor-graphic');
    const wrapper = document.querySelector('.hero-wrapper');

    wrapper.addEventListener('mousemove', (e) => {
        if (window.innerWidth > 900) {
            const x = (e.clientX / window.innerWidth - 0.5) * 20; // 20px max movement
            const y = (e.clientY / window.innerHeight - 0.5) * 10;
            
            // Use requestAnimationFrame in production for smoother performance
            graphic.style.transform = `translateX(calc(-50% + ${x}px)) translateY(${y}px)`;
        }
    });

    wrapper.addEventListener('mouseleave', () => {
        graphic.style.transform = `translateX(-50%) translateY(0)`;
    });
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
