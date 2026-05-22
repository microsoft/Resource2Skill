def create_component(
    output_dir: str,
    title_text: str = "It's your universe, it's time to save it",
    body_text: str = "The Rebel alliance is fighting to get rid of the evil empire. Join the resistance to create a better future for your children.",
    color_scheme: str = "dark",        
    accent_color: str = "#E52E2E",     
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Conversion-Optimized Cinematic Hero Section.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Derive theme colors from color_scheme
    if color_scheme == "dark":
        bg_color = "#050914"
        bg_rgb = "5, 9, 20"
        text_main = "#ffffff"
        text_muted = "rgba(255, 255, 255, 0.7)"
        bg_image = "https://images.unsplash.com/photo-1462331940025-496dfbfc7564?auto=format&fit=crop&q=80&w=2000"
        border_color = "rgba(255, 255, 255, 0.2)"
    else:
        bg_color = "#f4f7f6"
        bg_rgb = "244, 247, 246"
        text_main = "#1a1a1a"
        text_muted = "rgba(0, 0, 0, 0.6)"
        bg_image = "https://images.unsplash.com/photo-1495344517868-8ebaf0a2044a?auto=format&fit=crop&q=80&w=2000"
        border_color = "rgba(0, 0, 0, 0.1)"

    css = f"""/* Conversion-Optimized Cinematic Hero */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg-color: {bg_color};
    --text-main: {text_main};
    --text-muted: {text_muted};
    --accent: {accent_color};
    --border: {border_color};
    --width: {width_px}px;
    --height: {height_px}px;
    --font-sans: 'Inter', system-ui, sans-serif;
}}

body {{
    font-family: var(--font-sans);
    background: #000; /* Outer canvas background */
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 100vh;
}}

.hero-wrapper {{
    width: var(--width);
    height: var(--height);
    position: relative;
    overflow: hidden;
    background-color: var(--bg-color);
    background-image: url('{bg_image}');
    background-size: cover;
    background-position: calc(100% + 0px) calc(50% + 0px);
    color: var(--text-main);
    
    /* Establish container for responsive queries */
    container-type: inline-size;
    container-name: hero;
}}

/* The gradient overlay ensures text readability regardless of the image */
.overlay {{
    position: absolute;
    inset: 0;
    background: linear-gradient(90deg, rgba({bg_rgb}, 0.95) 0%, rgba({bg_rgb}, 0.8) 45%, rgba({bg_rgb}, 0) 100%);
    z-index: 1;
    pointer-events: none;
}}

.container {{
    position: relative;
    z-index: 2;
    width: 100%;
    height: 100%;
    display: flex;
    flex-direction: column;
    padding: 2.5rem 4rem;
}}

/* --- Header & Nav --- */
.header {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding-bottom: 2rem;
}}

.brand {{
    display: flex;
    align-items: center;
    gap: 0.75rem;
    font-weight: 800;
    font-size: 1.25rem;
    text-transform: uppercase;
    letter-spacing: 1px;
}}

.logo-icon {{
    width: 32px;
    height: 32px;
    fill: var(--accent);
}}

.nav {{
    display: flex;
    gap: 2.5rem;
}}

.nav a {{
    color: var(--text-main);
    text-decoration: none;
    font-size: 0.85rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    transition: color 0.3s ease;
}}

.nav a:hover {{
    color: var(--accent);
}}

/* --- Buttons --- */
.btn {{
    display: inline-block;
    padding: 0.75rem 1.5rem;
    border-radius: 4px;
    text-decoration: none;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1px;
    font-size: 0.85rem;
    transition: all 0.3s ease;
    cursor: pointer;
}}

.btn-outline {{
    border: 2px solid var(--text-main);
    color: var(--text-main);
}}

.btn-outline:hover {{
    background: var(--text-main);
    color: var(--bg-color);
}}

.btn-primary {{
    background: var(--accent);
    color: #fff;
    padding: 1.25rem 2.5rem;
    font-size: 1.1rem;
    border-radius: 6px;
    border: 2px solid var(--accent);
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
    margin-top: 0.5rem;
}}

.btn-primary:hover {{
    filter: brightness(1.1);
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.4);
    transform: translateY(-2px);
}}

/* --- Main Content --- */
.main-content {{
    flex: 1;
    display: flex;
    align-items: center;
}}

.text-content {{
    max-width: 55%;
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    gap: 1.5rem;
}}

.headline {{
    font-size: 4rem;
    font-weight: 800;
    line-height: 1.05;
    margin: 0;
    letter-spacing: -1.5px;
}}

.subheadline {{
    font-size: 1.25rem;
    line-height: 1.6;
    color: var(--text-muted);
    margin: 0;
    max-width: 90%;
    font-weight: 400;
}}

/* --- Social Proof --- */
.social-proof {{
    display: flex;
    align-items: center;
    gap: 1rem;
    margin-top: 1rem;
}}

.avatars {{
    display: flex;
}}

.avatar {{
    width: 36px;
    height: 36px;
    border-radius: 50%;
    border: 2px solid var(--bg-color);
    background-color: #333;
    background-size: cover;
    background-position: center;
    margin-left: -12px;
}}

.avatar:first-child {{ margin-left: 0; }}
.avatar:nth-child(1) {{ background-image: url('https://i.pravatar.cc/100?img=11'); }}
.avatar:nth-child(2) {{ background-image: url('https://i.pravatar.cc/100?img=12'); }}
.avatar:nth-child(3) {{ background-image: url('https://i.pravatar.cc/100?img=33'); }}

.proof-text {{
    font-size: 0.85rem;
    color: var(--text-muted);
    font-weight: 500;
}}

/* --- Trust Badges --- */
.trust-badges {{
    margin-top: 2rem;
    display: flex;
    align-items: center;
    gap: 1.5rem;
    border-top: 1px solid var(--border);
    padding-top: 1.5rem;
    width: 100%;
}}

.trust-label {{
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: var(--text-muted);
    font-weight: 600;
}}

.trust-logos {{
    display: flex;
    gap: 1.5rem;
    align-items: center;
    opacity: 0.5;
    /* Keeps colored logos cohesive with the theme */
    filter: grayscale(100%) brightness(2); 
}}

.logo-txt {{
    font-size: 1.25rem;
    line-height: 1;
}}

/* --- Animations --- */
@keyframes fadeInUp {{
    from {{ opacity: 0; transform: translateY(20px); }}
    to {{ opacity: 1; transform: translateY(0); }}
}}

.headline {{ animation: fadeInUp 0.8s ease-out forwards; }}
.subheadline {{ animation: fadeInUp 0.8s ease-out 0.15s forwards; opacity: 0; }}
.btn-primary {{ animation: fadeInUp 0.8s ease-out 0.3s forwards; opacity: 0; }}
.social-proof {{ animation: fadeInUp 0.8s ease-out 0.45s forwards; opacity: 0; }}
.trust-badges {{ animation: fadeInUp 0.8s ease-out 0.6s forwards; opacity: 0; }}

/* --- Container Queries for Component Responsiveness --- */
@container hero (max-width: 900px) {{
    .text-content {{
        max-width: 75%;
    }}
    .overlay {{
        /* Push gradient further right to cover more text area */
        background: linear-gradient(90deg, rgba({bg_rgb}, 0.95) 0%, rgba({bg_rgb}, 0.85) 60%, rgba({bg_rgb}, 0.2) 100%);
    }}
    .headline {{ font-size: 3.25rem; }}
}}

@container hero (max-width: 650px) {{
    .container {{
        padding: 2rem;
    }}
    .text-content {{
        max-width: 100%;
        text-align: left;
    }}
    .overlay {{
        background: rgba({bg_rgb}, 0.85); /* Solid overlay for smaller widths to guarantee legibility */
    }}
    .headline {{ font-size: 2.5rem; }}
    .subheadline {{ font-size: 1.1rem; }}
    .nav {{ display: none; }} /* Collapse nav on small sizes */
}}
"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hero Section Component</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="hero-wrapper">
        <div class="overlay"></div>
        <div class="container">
            <header class="header">
                <div class="brand">
                    <svg class="logo-icon" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                        <path d="M12 2L15 9L22 10L17 15L18 22L12 18L6 22L7 15L2 10L9 9L12 2Z"/>
                    </svg>
                    <span class="logo-text">Rebel Alliance</span>
                </div>
                <nav class="nav">
                    <a href="#">Our Ships</a>
                    <a href="#">Mission</a>
                    <a href="#">Donations</a>
                </nav>
                <a href="#" class="btn btn-outline">JOIN NOW</a>
            </header>

            <main class="main-content">
                <div class="text-content">
                    <h1 class="headline">{title_text}</h1>
                    <p class="subheadline">{body_text}</p>

                    <a href="#" class="btn btn-primary">JOIN NOW FOR FREE</a>

                    <div class="social-proof">
                        <div class="avatars">
                            <div class="avatar"></div>
                            <div class="avatar"></div>
                            <div class="avatar"></div>
                        </div>
                        <span class="proof-text">Obi Wan and 4,000 others have already joined</span>
                    </div>

                    <div class="trust-badges">
                        <span class="trust-label">As Seen On:</span>
                        <div class="trust-logos">
                            <span class="logo-txt" style="font-weight: 900; font-family: Arial;">CNN</span>
                            <span class="logo-txt" style="font-weight: 700; font-family: Times New Roman;">NBC</span>
                            <span class="logo-txt" style="font-weight: 800; font-family: Impact; letter-spacing: 1px;">FOX</span>
                        </div>
                    </div>
                </div>
            </main>
        </div>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    js = """// Cinematic Parallax Background Effect
document.addEventListener('DOMContentLoaded', () => {
    const hero = document.querySelector('.hero-wrapper');
    
    // Only apply parallax if user doesn't prefer reduced motion
    const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    
    if (!prefersReducedMotion && hero) {
        hero.addEventListener('mousemove', (e) => {
            // Calculate mouse position relative to container
            const rect = hero.getBoundingClientRect();
            const x = (e.clientX - rect.left) / rect.width;
            const y = (e.clientY - rect.top) / rect.height;
            
            // Move background slightly opposite to cursor (max 15px shift)
            const bgX = -(x - 0.5) * 30; 
            const bgY = -(y - 0.5) * 30;
            
            // 100% horizontally locks it to the right edge roughly, plus offset
            hero.style.backgroundPosition = `calc(100% + ${bgX}px) calc(50% + ${bgY}px)`;
        });
        
        // Reset position when mouse leaves
        hero.addEventListener('mouseleave', () => {
            hero.style.backgroundPosition = `calc(100% + 0px) calc(50% + 0px)`;
            hero.style.transition = 'background-position 0.5s ease-out';
            
            setTimeout(() => {
                hero.style.transition = '';
            }, 500);
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
