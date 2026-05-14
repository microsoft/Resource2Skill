def create_component(
    output_dir: str,
    title_text: str = "WELCOME<br>TO MY FIRST<br>WEBSITE",
    body_text: str = "Nam interdum felis at felis placerat, sed varius massa ultricies. Integer quis nisi non dolor scelerisque efficitur at sed turpis.",
    color_scheme: str = "dark",        
    accent_color: str = "#C13584",     
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Split-Content Parallax Hero effect.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors ===
    if color_scheme == "dark":
        bg_color = "#1A253A"
        text_color = "#FFFFFF"
        text_muted = "rgba(255, 255, 255, 0.7)"
        btn_text = "#FFFFFF"
    else:
        bg_color = "#F0F4F8"
        text_color = "#111827"
        text_muted = "rgba(17, 24, 39, 0.7)"
        btn_text = "#FFFFFF"

    # === CSS ===
    css = f"""/* Split-Content Parallax Hero */
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
    --btn-text: {btn_text};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background: var(--bg);
    color: var(--text);
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 100vh;
}}

.hero {{
    position: relative;
    width: 100%;
    min-height: var(--height);
    background-color: var(--bg);
    overflow: hidden;
    display: flex;
    align-items: center;
}}

/* Texture Layer */
.hero-pattern {{
    position: absolute;
    inset: 0;
    background-color: var(--text);
    opacity: 0.04;
    -webkit-mask-image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="40" height="40"><path d="M0 0l20 20L0 40M40 0L20 20l20 20" stroke="black" stroke-width="2" fill="none"/></svg>');
    mask-image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="40" height="40"><path d="M0 0l20 20L0 40M40 0L20 20l20 20" stroke="black" stroke-width="2" fill="none"/></svg>');
    -webkit-mask-size: 60px 60px;
    mask-size: 60px 60px;
    z-index: 0;
}}

/* Subject Layer */
.hero-subject {{
    position: absolute;
    bottom: 0;
    left: 50%;
    transform: translateX(-50%);
    height: 85vh;
    z-index: 1;
    pointer-events: none;
    will-change: transform;
    transition: transform 0.1s ease-out;
}}

.hero-subject svg {{
    height: 100%;
    width: auto;
    display: block;
}}

/* Content Layer */
.hero-wrapper {{
    position: relative;
    z-index: 2;
    width: 100%;
    max-width: var(--width);
    margin: 0 auto;
    padding: 0 5%;
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 40px;
}}

/* Left Column */
.hero-intro {{
    max-width: 480px;
}}

.title {{
    font-size: clamp(2.5rem, 5vw, 5.5rem);
    line-height: 1.1;
    text-transform: uppercase;
    font-weight: 800;
    margin-bottom: 24px;
    letter-spacing: -0.02em;
}}

.body-text {{
    font-size: 1.125rem;
    line-height: 1.6;
    color: var(--text-muted);
    margin-bottom: 32px;
}}

.cta-btn {{
    display: inline-block;
    background: var(--accent);
    color: var(--btn-text);
    padding: 14px 36px;
    text-decoration: none;
    text-transform: uppercase;
    font-weight: 600;
    font-size: 0.95rem;
    letter-spacing: 1px;
    transition: filter 0.3s ease, transform 0.2s ease;
}}

.cta-btn:hover {{
    filter: brightness(1.15);
    transform: translateY(-2px);
}}

/* Right Column */
.hero-quotes {{
    border-left: 4px solid var(--accent);
    padding-left: 32px;
    display: flex;
    flex-direction: column;
    gap: 48px;
    max-width: 380px;
}}

.quote-item {{
    font-size: 1rem;
    line-height: 1.6;
}}

.quote-text {{
    font-style: italic;
    margin-bottom: 8px;
    color: var(--text-muted);
}}

.quote-author {{
    font-weight: 600;
    color: var(--text);
}}

.quote-item.offset {{
    margin-left: 60px;
}}

/* Responsive Adaptations */
@media (max-width: 960px) {{
    .hero-wrapper {{
        flex-direction: column;
        justify-content: flex-start;
        padding-top: 10vh;
        padding-bottom: 10vh;
        gap: 60px;
    }}
    
    .hero-intro {{
        text-align: center;
    }}
    
    .hero-quotes {{
        border-left: none;
        border-top: 4px solid var(--accent);
        padding-left: 0;
        padding-top: 32px;
        margin: 0 auto;
        text-align: center;
    }}
    
    .quote-item.offset {{
        margin-left: 0;
    }}
    
    .hero-subject {{
        opacity: 0.15;
    }}
}}
"""

    # === HTML ===
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hero Section</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <main class="hero">
        
        <!-- Texture Pattern -->
        <div class="hero-pattern"></div>
        
        <!-- Central Subject (Placeholder Silhouette) -->
        <div class="hero-subject">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 500 600" preserveAspectRatio="xMidYMax meet">
                <defs>
                    <linearGradient id="subjectGrad" x1="0" y1="0" x2="0" y2="1">
                        <stop offset="0%" stop-color="var(--text)" stop-opacity="0.12"/>
                        <stop offset="100%" stop-color="var(--text)" stop-opacity="0"/>
                    </linearGradient>
                </defs>
                <circle cx="250" cy="140" r="90" fill="url(#subjectGrad)" />
                <path d="M50 600 V 450 C 50 330, 120 250, 250 250 C 380 250, 450 330, 450 450 V 600 Z" fill="url(#subjectGrad)" />
            </svg>
        </div>
        
        <!-- Foreground Content -->
        <div class="hero-wrapper">
            
            <div class="hero-intro">
                <h1 class="title">{title_text}</h1>
                <p class="body-text">{body_text}</p>
                <a href="#" class="cta-btn">MY WORK</a>
            </div>
            
            <div class="hero-quotes">
                <div class="quote-item">
                    <p class="quote-text">"The more that you read, the more things you will know. The more that you learn, the more places you'll go."</p>
                    <p class="quote-author">- Dr. Seuss</p>
                </div>
                <div class="quote-item offset">
                    <p class="quote-text">"For the best return on your money, pour your purse into your head."</p>
                    <p class="quote-author">- Benjamin Franklin</p>
                </div>
            </div>
            
        </div>
    </main>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Lightweight Parallax Effect for Central Subject
document.addEventListener('DOMContentLoaded', () => {{
    const subject = document.querySelector('.hero-subject');
    
    // Disable parallax on mobile to save performance
    if (window.innerWidth <= 960) return;

    document.addEventListener('mousemove', (e) => {{
        // Calculate normalized mouse position (-1 to 1)
        const x = (e.clientX / window.innerWidth - 0.5) * 2;
        const y = (e.clientY / window.innerHeight - 0.5) * 2;
        
        // Translate subject slightly opposite to mouse direction
        const shiftX = x * 15; 
        const shiftY = y * 10;
        
        // Use calc to maintain the existing -50% translateX centering
        subject.style.transform = `translate(calc(-50% + ${{shiftX}}px), ${{shiftY}}px)`;
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
