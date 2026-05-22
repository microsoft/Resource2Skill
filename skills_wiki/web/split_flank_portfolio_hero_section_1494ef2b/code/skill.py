def create_component(
    output_dir: str,
    title_text: str = "WELCOME<br>TO MY FIRST<br>WEBSITE",
    body_text: str = "I specialize in building clean, responsive, and highly interactive web experiences. Take a look around to see what I've been working on.",
    color_scheme: str = "dark",
    accent_color: str = "#c13584",
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Split-Flank Portfolio Hero Section.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Theme logic
    if color_scheme == "dark":
        bg_color = "#1A253A"
        text_color = "#ffffff"
        text_muted = "rgba(255, 255, 255, 0.7)"
        grid_color = "rgba(255, 255, 255, 0.03)"
    else:
        bg_color = "#f0f4f8"
        text_color = "#111827"
        text_muted = "rgba(17, 24, 39, 0.7)"
        grid_color = "rgba(0, 0, 0, 0.04)"

    # Hover color derivation (simple approximation for standard hex)
    # For a robust system, we just use a slight opacity shift on the accent
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hero Section Component</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <main class="hero-section">
        <!-- Center focal area simulated via absolute element for better responsive control -->
        <div class="hero-focal-point"></div>

        <div class="hero-wrapper">
            
            <!-- Left Flank: Primary Intro -->
            <div class="hero-flank hero-intro">
                <h1 class="hero-title">{title_text}</h1>
                <p class="hero-body">{body_text}</p>
                <a href="#work" class="hero-cta">MY WORK</a>
            </div>

            <!-- Right Flank: Secondary Quotes -->
            <div class="hero-flank hero-quotes">
                <div class="quote-card">
                    <p class="quote-text">"The more that you read, the more things you will know. The more that you learn, the more places you'll go."</p>
                    <p class="quote-author">- Dr. Seuss</p>
                </div>
                <div class="quote-card">
                    <p class="quote-text">"For the best return on your money, pour your purse into your head."</p>
                    <p class="quote-author">- Benjamin Franklin</p>
                </div>
            </div>

        </div>
    </main>
    <script src="script.js"></script>
</body>
</html>"""

    css = f"""/* Split-Flank Portfolio Hero Section */
:root {{
    --bg-color: {bg_color};
    --text-color: {text_color};
    --text-muted: {text_muted};
    --accent-color: {accent_color};
    --grid-color: {grid_color};
    --comp-width: {width_px}px;
    --comp-height: {height_px}px;
}}

* {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: 'Roboto', sans-serif;
    background-color: var(--bg-color);
    color: var(--text-color);
    min-height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
    overflow-x: hidden;
}}

/* Main Container */
.hero-section {{
    position: relative;
    width: 100%;
    min-height: var(--comp-height);
    display: flex;
    align-items: center;
    
    /* Layered Background: Repeating Grid */
    background-image: 
        linear-gradient(var(--grid-color) 1px, transparent 1px),
        linear-gradient(90deg, var(--grid-color) 1px, transparent 1px);
    background-size: 40px 40px;
    background-position: center;
}}

/* Simulated Portrait / Focal Point in Center Background */
.hero-focal-point {{
    position: absolute;
    bottom: 0;
    left: 50%;
    transform: translateX(-50%);
    width: 60vh;
    height: 70vh;
    border-radius: 50% 50% 0 0;
    background: radial-gradient(ellipse at bottom, var(--accent-color) 0%, transparent 60%);
    opacity: 0.15;
    z-index: 0;
    pointer-events: none;
}}

/* Layout Wrapper */
.hero-wrapper {{
    position: relative;
    z-index: 10;
    width: 100%;
    max-width: var(--comp-width);
    margin: 0 auto;
    padding: 40px 5%;
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 40px;
}}

.hero-flank {{
    flex: 1;
}}

/* Left Side Typography */
.hero-intro {{
    max-width: 500px;
    padding-bottom: 5vh; /* Slight upward lift */
}}

.hero-title {{
    font-size: clamp(40px, 6vw, 86px);
    line-height: 1.05;
    font-weight: 700;
    text-transform: uppercase;
    margin-bottom: 24px;
    letter-spacing: -0.02em;
}}

.hero-body {{
    font-size: 18px;
    line-height: 1.6;
    margin-bottom: 36px;
    color: var(--text-color);
}}

/* CTA Button */
.hero-cta {{
    display: inline-block;
    background-color: var(--accent-color);
    color: #ffffff; /* Always white text on CTA */
    text-decoration: none;
    padding: 14px 28px;
    font-size: 15px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    transition: all 0.3s ease;
    border: 1px solid transparent;
}}

.hero-cta:hover {{
    background-color: transparent;
    color: var(--accent-color);
    border-color: var(--accent-color);
}}

/* Right Side Quotes */
.hero-quotes {{
    max-width: 380px;
    display: flex;
    flex-direction: column;
    gap: 40px;
    /* Pushing quotes down slightly relative to title */
    margin-top: 8vh; 
}}

.quote-card {{
    border-left: 4px solid var(--accent-color);
    padding-left: 24px;
}}

.quote-text {{
    font-size: 18px;
    line-height: 1.6;
    margin-bottom: 12px;
    font-style: italic;
}}

.quote-author {{
    font-size: 15px;
    font-weight: 600;
    color: var(--text-muted);
}}

/* Responsive Breakpoints */
@media (max-width: 968px) {{
    .hero-wrapper {{
        flex-direction: column;
        justify-content: center;
        text-align: center;
    }}

    .hero-intro, .hero-quotes {{
        max-width: 100%;
        padding-bottom: 0;
        margin-top: 0;
    }}

    .hero-quotes {{
        align-items: center;
    }}

    .quote-card {{
        text-align: left;
    }}

    .hero-focal-point {{
        display: none; /* Hide focal point on small screens to prevent clutter */
    }}
}}
"""

    js = f"""// Hero Section Interactions
document.addEventListener('DOMContentLoaded', () => {{
    // Optional: Add simple entry animations
    const flanks = document.querySelectorAll('.hero-flank');
    
    // Apply initial state
    flanks.forEach(flank => {{
        flank.style.opacity = '0';
        flank.style.transform = 'translateY(20px)';
        flank.style.transition = 'opacity 0.8s ease, transform 0.8s cubic-bezier(0.2, 0.8, 0.2, 1)';
    }});

    // Trigger animation short delay after load
    setTimeout(() => {{
        flanks.forEach((flank, index) => {{
            setTimeout(() => {{
                flank.style.opacity = '1';
                flank.style.transform = 'translateY(0)';
            }}, index * 200); // Stagger the entry
        }});
    }}, 100);
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
