def create_component(
    output_dir: str,
    title_text: str = "Exclusive Course Discounts",
    body_text: str = "Be the first to know when our new courses drop! Join the mailing list to receive exclusive updates.",
    color_scheme: str = "light",
    accent_color: str = "#0f172a",     # Primary Dark Color (Top Header)
    secondary_color: str = "#3b82f6",  # Vibrant Blue (Form Header)
    width_px: int = 1200,
    height_px: int = 1000,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Asymmetric Grid Layout with Curved Section Dividers.
    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Base Colors determined by the scheme mapping to the body background
    if color_scheme == "dark":
        bg_color = "#020617"
        text_color = "#f8fafc"
        card_bg = "#1e293b"
        text_muted = "#94a3b8"
    else:
        bg_color = "#ffffff"
        text_color = "#0f172a"
        card_bg = "#f1f5f9"
        text_muted = "#475569"

    css = f"""/* Asymmetric Grid Layout with Curved Section Dividers */
:root {{
    --accent: {accent_color};
    --secondary: {secondary_color};
    --bg: {bg_color};
    --text: {text_color};
    --card-bg: {card_bg};
    --text-muted: {text_muted};
    --width: {width_px}px;
    --height: {height_px}px;
}}

*, *::before, *::after {{
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background-color: var(--bg);
    color: var(--text);
    width: var(--width);
    height: var(--height);
    overflow-x: hidden;
    overflow-y: auto;
    -webkit-font-smoothing: antialiased;
}}

h1, h2, h3, .brand {{
    font-family: 'Quicksand', sans-serif;
}}

/* Base Structural Classes */
.container {{
    max-width: 1100px;
    margin: 0 auto;
    padding: 0 24px;
    width: 100%;
}}

.grid {{
    display: grid;
    grid-template-columns: repeat(6, 1fr);
    gap: 24px;
}}

.content-span {{
    grid-column: 2 / 6;
    text-align: center;
}}

/* Header Sections */
.header-section {{
    position: relative;
}}

.header-section.dark {{
    background-color: var(--accent);
    color: #ffffff;
    padding: 60px 0 0;
}}

.header-section.light {{
    background-color: var(--secondary);
    color: #ffffff;
    padding: 20px 0 0;
}}

.brand {{
    font-size: 1.5rem;
    font-weight: 700;
    margin-bottom: 24px;
    display: inline-flex;
    align-items: center;
    gap: 10px;
}}

.brand i {{
    color: var(--secondary);
}}

.title {{
    font-size: clamp(2.5rem, 5vw, 3.5rem);
    line-height: 1.1;
    margin-bottom: 16px;
    letter-spacing: -0.02em;
}}

.subtitle {{
    font-size: clamp(1.1rem, 2vw, 1.25rem);
    opacity: 0.9;
    font-weight: 400;
    line-height: 1.6;
}}

/* Wave Dividers */
.wave-container {{
    width: 100%;
    /* Pulling margin up slightly prevents subpixel rendering gaps between divs */
    margin-top: -1px; 
}}

.wave {{
    display: block;
    width: 100%;
    height: clamp(60px, 10vw, 120px);
}}

/* Email Form */
.email-form {{
    display: flex;
    gap: 12px;
    background: rgba(255, 255, 255, 0.15);
    padding: 8px;
    border-radius: 12px;
    backdrop-filter: blur(12px);
    max-width: 600px;
    margin: 0 auto;
}}

.email-form input {{
    flex: 1;
    padding: 16px 24px;
    border-radius: 8px;
    border: 2px solid transparent;
    font-size: 1rem;
    outline: none;
    font-family: inherit;
    transition: all 0.3s ease;
}}

.email-form input:focus {{
    border-color: var(--accent);
    box-shadow: 0 0 0 4px rgba(255, 255, 255, 0.3);
}}

.email-form button {{
    padding: 16px 32px;
    background: var(--accent);
    color: #ffffff;
    border: none;
    border-radius: 8px;
    font-size: 1.05rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s ease;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    min-width: 140px;
}}

.email-form button:hover {{
    transform: translateY(-2px);
    box-shadow: 0 6px 16px rgba(0, 0, 0, 0.2);
    filter: brightness(1.1);
}}

/* Main Grid Content */
.main-content {{
    padding-top: 60px;
    padding-bottom: 100px;
}}

.split-grid {{
    display: grid;
    grid-template-columns: repeat(6, 1fr);
    gap: 64px;
    align-items: center;
}}

.video-section {{
    grid-column: 1 / 4;
}}

.video-placeholder {{
    width: 100%;
    aspect-ratio: 16 / 9;
    background: linear-gradient(135deg, var(--secondary), var(--accent));
    border-radius: 16px;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15);
    position: relative;
    overflow: hidden;
    cursor: pointer;
    transition: transform 0.3s cubic-bezier(0.34, 1.56, 0.64, 1), box-shadow 0.3s ease;
}}

.video-placeholder:hover {{
    transform: translateY(-8px);
    box-shadow: 0 30px 60px rgba(0, 0, 0, 0.25);
}}

.video-placeholder i {{
    font-size: 4rem;
    color: rgba(255, 255, 255, 0.9);
    filter: drop-shadow(0 4px 8px rgba(0,0,0,0.3));
    transition: transform 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
}}

.video-placeholder:hover i {{
    transform: scale(1.15);
    color: #ffffff;
}}

.video-badge {{
    position: absolute;
    bottom: 16px;
    left: 16px;
    background: rgba(0, 0, 0, 0.6);
    color: white;
    padding: 6px 12px;
    border-radius: 6px;
    font-size: 0.85rem;
    font-weight: 500;
    backdrop-filter: blur(4px);
}}

.benefits-section {{
    grid-column: 4 / 7;
    display: flex;
    flex-direction: column;
    gap: 36px;
}}

.benefit-item {{
    display: flex;
    gap: 20px;
    align-items: flex-start;
}}

.icon-wrapper {{
    font-size: 1.25rem;
    color: var(--secondary);
    background: var(--card-bg);
    width: 56px;
    height: 56px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 14px;
    flex-shrink: 0;
    box-shadow: inset 0 2px 4px rgba(255,255,255,0.05), 0 4px 12px rgba(0,0,0,0.05);
}}

.benefit-text h3 {{
    font-size: 1.35rem;
    margin-bottom: 8px;
    color: var(--text);
    line-height: 1.2;
}}

.benefit-text p {{
    font-size: 1rem;
    color: var(--text-muted);
    line-height: 1.6;
}}

/* Responsive Breakpoints */
@media (max-width: 900px) {{
    .grid, .split-grid {{
        grid-template-columns: 1fr;
    }}
    
    .content-span, .video-section, .benefits-section {{
        grid-column: 1 / -1;
    }}
    
    .email-form {{
        flex-direction: column;
        background: transparent;
        padding: 0;
        backdrop-filter: none;
    }}
    
    .email-form input, .email-form button {{
        width: 100%;
    }}
}}
"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text}</title>
    <!-- Typography -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Quicksand:wght@600;700&display=swap" rel="stylesheet">
    <!-- Iconography -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    
    <link rel="stylesheet" href="style.css">
</head>
<body>

    <!-- Hero Dark Section -->
    <header class="header-section dark">
        <div class="container grid">
            <div class="content-span">
                <div class="brand">
                    <i class="fa-solid fa-layer-group"></i> WebDev Simplified
                </div>
                <h1 class="title">{title_text}</h1>
                <p class="subtitle">{body_text}</p>
            </div>
        </div>
    </header>
    
    <!-- Top Wave (Transition: Dark -> Light) -->
    <div class="wave-container" style="background-color: var(--accent);">
        <svg class="wave" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1440 320" preserveAspectRatio="none">
            <path fill="var(--secondary)" d="M0,160L48,170.7C96,181,192,203,288,213.3C384,224,480,224,576,202.7C672,181,768,139,864,117.3C960,96,1056,96,1152,117.3C1248,139,1344,181,1392,202.7L1440,224L1440,320L1392,320C1344,320,1248,320,1152,320C1056,320,960,320,864,320C768,320,672,320,576,320C480,320,384,320,288,320C192,320,96,320,48,320L0,320Z"></path>
        </svg>
    </div>
    
    <!-- Form Light Section -->
    <section class="header-section light">
        <div class="container grid">
            <div class="content-span">
                <form class="email-form" id="signupForm">
                    <input type="email" placeholder="Enter your best email address" required autocomplete="email">
                    <button type="submit"><span>Join Now!</span></button>
                </form>
            </div>
        </div>
    </section>
    
    <!-- Bottom Wave (Transition: Light -> Body Background) -->
    <div class="wave-container" style="background-color: var(--secondary);">
        <!-- Using a slightly different path for variation -->
        <svg class="wave" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1440 320" preserveAspectRatio="none">
            <path fill="var(--bg)" d="M0,224L48,202.7C96,181,192,139,288,149.3C384,160,480,224,576,245.3C672,267,768,245,864,208C960,171,1056,117,1152,117.3C1248,117,1344,171,1392,197.3L1440,224L1440,320L1392,320C1344,320,1248,320,1152,320C1056,320,960,320,864,320C768,320,672,320,576,320C480,320,384,320,288,320C192,320,96,320,48,320L0,320Z"></path>
        </svg>
    </div>
    
    <!-- Main Content (Video & Benefits) -->
    <main class="container main-content">
        <div class="split-grid">
            
            <div class="video-section">
                <div class="video-placeholder">
                    <i class="fa-solid fa-circle-play"></i>
                    <div class="video-badge">Watch Intro (2:14)</div>
                </div>
            </div>
            
            <div class="benefits-section">
                <div class="benefit-item">
                    <div class="icon-wrapper"><i class="fa-regular fa-envelope"></i></div>
                    <div class="benefit-text">
                        <h3>Instant Email Updates</h3>
                        <p>All members of the mailing list will receive notifications the minute a new course module drops.</p>
                    </div>
                </div>
                <div class="benefit-item">
                    <div class="icon-wrapper"><i class="fa-solid fa-tags"></i></div>
                    <div class="benefit-text">
                        <h3>Special Discounts</h3>
                        <p>Get exclusive early-bird discounts and bundle offers available only to our subscriber base.</p>
                    </div>
                </div>
                <div class="benefit-item">
                    <div class="icon-wrapper"><i class="fa-solid fa-wand-magic-sparkles"></i></div>
                    <div class="benefit-text">
                        <h3>Exclusive Content</h3>
                        <p>Gain access to behind-the-scenes content, raw code snippets, and unlisted architecture reviews.</p>
                    </div>
                </div>
            </div>

        </div>
    </main>

    <script src="script.js"></script>
</body>
</html>"""

    js = f"""// Asymmetric Grid Layout - Interactive Enhancements
document.addEventListener('DOMContentLoaded', () => {{
    const form = document.getElementById('signupForm');
    
    if (form) {{
        form.addEventListener('submit', (e) => {{
            e.preventDefault();
            
            const btn = form.querySelector('button');
            const span = btn.querySelector('span');
            const originalText = span.textContent;
            
            // Loading state
            span.innerHTML = '<i class="fa-solid fa-circle-notch fa-spin"></i> Processing';
            btn.style.opacity = '0.8';
            btn.disabled = true;
            
            // Simulate network request
            setTimeout(() => {{
                span.innerHTML = '<i class="fa-solid fa-check"></i> Subscribed!';
                btn.style.backgroundColor = '#10b981'; // Success green
                btn.style.opacity = '1';
                
                // Reset form state
                setTimeout(() => {{
                    span.textContent = originalText;
                    btn.style.backgroundColor = '';
                    btn.disabled = false;
                    form.reset();
                }}, 3000);
                
            }}, 1200);
        }});
    }}
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
