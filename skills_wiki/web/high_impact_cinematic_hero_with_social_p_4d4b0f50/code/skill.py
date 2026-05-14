def create_component(
    output_dir: str,
    title_text: str = "It's your universe, it's time to save it",
    body_text: str = "The resistance is fighting to get rid of the evil empire. Join the alliance to create a better future for your system.",
    color_scheme: str = "dark",
    accent_color: str = "#e62429",
    width_px: int = 1440,
    height_px: int = 900,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the High-Impact Cinematic Hero with Social Proof.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Note: This design pattern relies heavily on the dark cinematic look.
    # The light theme fallback is provided but the visual impact is native to dark mode.
    if color_scheme == "dark":
        bg_base = "#050814"
        text_main = "#ffffff"
        text_muted = "rgba(255, 255, 255, 0.7)"
        card_bg = "rgba(255, 255, 255, 0.05)"
        border_color = "rgba(255, 255, 255, 0.1)"
    else:
        bg_base = "#f0f2f5"
        text_main = "#0d111c"
        text_muted = "rgba(0, 0, 0, 0.6)"
        card_bg = "rgba(0, 0, 0, 0.03)"
        border_color = "rgba(0, 0, 0, 0.1)"

    # Using high-quality Unsplash placeholders that fit the space/cinematic vibe
    bg_image_url = "https://images.unsplash.com/photo-1462331940025-496dfbfc7564?q=80&w=2048&auto=format&fit=crop"
    hero_image_url = "https://images.unsplash.com/photo-1614730321146-b6fa6a46bcb4?q=80&w=1000&auto=format&fit=crop"

    css = f"""/* High-Impact Cinematic Hero */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Montserrat:wght@700;800;900&display=swap');

:root {{
    --bg-base: {bg_base};
    --text-main: {text_main};
    --text-muted: {text_muted};
    --accent: {accent_color};
    --card-bg: {card_bg};
    --border-color: {border_color};
    
    --font-head: 'Montserrat', sans-serif;
    --font-body: 'Inter', sans-serif;
}}

*, *::before, *::after {{
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}}

body {{
    font-family: var(--font-body);
    background-color: var(--bg-base);
    color: var(--text-main);
    line-height: 1.6;
    overflow-x: hidden;
}}

/* Main wrapper constraining to requested dimensions for preview */
.preview-container {{
    width: {width_px}px;
    height: {height_px}px;
    max-width: 100vw;
    margin: 0 auto;
    position: relative;
    overflow-y: auto;
    overflow-x: hidden;
    background-color: var(--bg-base);
    /* Cinematic Background setup */
    background-image: 
        linear-gradient(to right, {bg_base} 0%, rgba(5,8,20,0.6) 50%, rgba(5,8,20,0.2) 100%),
        linear-gradient(to bottom, rgba(5,8,20,0.8) 0%, rgba(5,8,20,0) 20%, {bg_base} 100%),
        url('{bg_image_url}');
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
    display: flex;
    flex-direction: column;
}}

/* Header / Nav */
header {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 2rem 5%;
    position: relative;
    z-index: 10;
}}

.logo {{
    font-family: var(--font-head);
    font-weight: 900;
    font-size: 1.5rem;
    letter-spacing: 2px;
    text-transform: uppercase;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}}

.logo-icon {{
    width: 24px;
    height: 24px;
    background-color: var(--accent);
    mask: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M12 2L2 22h20L12 2zm0 4.5l6.5 13.5H5.5L12 6.5z"/></svg>') no-repeat center;
    -webkit-mask: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M12 2L2 22h20L12 2zm0 4.5l6.5 13.5H5.5L12 6.5z"/></svg>') no-repeat center;
}}

.nav-links {{
    display: flex;
    gap: 2.5rem;
}}

.nav-links a {{
    color: var(--text-main);
    text-decoration: none;
    font-weight: 500;
    font-size: 0.95rem;
    transition: opacity 0.3s;
}}

.nav-links a:hover {{
    opacity: 0.7;
    color: var(--accent);
}}

/* Buttons */
.btn {{
    padding: 0.8rem 2rem;
    border-radius: 4px;
    font-family: var(--font-head);
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1px;
    font-size: 0.9rem;
    cursor: pointer;
    transition: all 0.3s ease;
    text-decoration: none;
    display: inline-flex;
    align-items: center;
    justify-content: center;
}}

.btn-ghost {{
    background: transparent;
    color: var(--text-main);
    border: 2px solid var(--border-color);
}}

.btn-ghost:hover {{
    border-color: var(--accent);
    color: var(--accent);
}}

.btn-primary {{
    background: var(--accent);
    color: #fff;
    border: 2px solid var(--accent);
    padding: 1rem 2.5rem;
    font-size: 1rem;
    box-shadow: 0 4px 15px rgba(230, 36, 41, 0.3);
}}

.btn-primary:hover {{
    background: transparent;
    color: var(--accent);
    box-shadow: 0 0 20px rgba(230, 36, 41, 0.5);
}}

/* Hero Section */
.hero {{
    flex: 1;
    display: grid;
    grid-template-columns: 1.2fr 0.8fr;
    gap: 4rem;
    align-items: center;
    padding: 2rem 5% 4rem;
    position: relative;
    z-index: 5;
}}

.hero-content {{
    max-width: 650px;
}}

.hero h1 {{
    font-family: var(--font-head);
    font-size: clamp(3rem, 5vw, 4.5rem);
    line-height: 1.05;
    font-weight: 900;
    margin-bottom: 1.5rem;
    letter-spacing: -1px;
    text-transform: uppercase;
}}

.hero h1 span {{
    color: var(--accent);
}}

.hero p.lead {{
    font-size: 1.2rem;
    color: var(--text-muted);
    margin-bottom: 2.5rem;
    max-width: 90%;
}}

.cta-group {{
    display: flex;
    flex-wrap: wrap;
    gap: 1.5rem;
    align-items: center;
    margin-bottom: 2rem;
}}

/* Social Proof Block */
.social-proof {{
    display: flex;
    align-items: center;
    gap: 1rem;
    padding-top: 1.5rem;
    border-top: 1px solid var(--border-color);
}}

.avatars {{
    display: flex;
}}

.avatar {{
    width: 40px;
    height: 40px;
    border-radius: 50%;
    border: 3px solid var(--bg-base);
    background-color: var(--card-bg);
    background-size: cover;
    margin-left: -12px;
}}
.avatar:first-child {{ margin-left: 0; }}

.proof-text {{
    font-size: 0.9rem;
    color: var(--text-muted);
}}
.proof-text strong {{
    color: var(--text-main);
}}

/* Hero Visual */
.hero-visual {{
    position: relative;
    height: 100%;
    min-height: 400px;
    display: flex;
    justify-content: center;
    align-items: center;
}}

.hero-image-wrapper {{
    position: relative;
    width: 100%;
    padding-bottom: 100%; /* 1:1 Aspect Ratio */
    border-radius: 50%;
    overflow: hidden;
    box-shadow: 0 20px 50px rgba(0,0,0,0.5), inset 0 0 40px rgba(255,255,255,0.1);
    animation: float 6s ease-in-out infinite;
}}

.hero-image-wrapper img {{
    position: absolute;
    top: 0; left: 0;
    width: 100%; height: 100%;
    object-fit: cover;
    /* Optional: blend mode to fit it into space better */
    mix-blend-mode: screen; 
    filter: contrast(1.2) brightness(1.1);
}}

/* Trust Banner */
.trust-banner {{
    background-color: var(--card-bg);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    border-top: 1px solid var(--border-color);
    padding: 1.5rem 5%;
    display: flex;
    align-items: center;
    gap: 2rem;
    position: relative;
    z-index: 10;
}}

.trust-banner p {{
    font-size: 0.8rem;
    text-transform: uppercase;
    letter-spacing: 2px;
    color: var(--text-muted);
    white-space: nowrap;
}}

.trust-logos {{
    display: flex;
    gap: 3rem;
    flex-wrap: wrap;
    opacity: 0.5;
    filter: grayscale(100%) contrast(200%);
}}

.trust-logos svg {{
    height: 24px;
    fill: var(--text-main);
}}

/* Animations */
@keyframes float {{
    0% {{ transform: translateY(0px); }}
    50% {{ transform: translateY(-20px); }}
    100% {{ transform: translateY(0px); }}
}}

.reveal {{
    opacity: 0;
    transform: translateY(30px);
    transition: opacity 0.8s ease-out, transform 0.8s cubic-bezier(0.16, 1, 0.3, 1);
}}

.reveal.active {{
    opacity: 1;
    transform: translateY(0);
}}

.delay-1 {{ transition-delay: 0.1s; }}
.delay-2 {{ transition-delay: 0.2s; }}
.delay-3 {{ transition-delay: 0.3s; }}
.delay-4 {{ transition-delay: 0.4s; }}

/* Responsive */
@media (max-width: 992px) {{
    .hero {{
        grid-template-columns: 1fr;
        text-align: center;
    }}
    .hero-content {{
        margin: 0 auto;
    }}
    .cta-group {{
        justify-content: center;
    }}
    .social-proof {{
        justify-content: center;
    }}
    .nav-links {{ display: none; }} /* simplified for mobile preview */
    .trust-banner {{
        flex-direction: column;
        text-align: center;
        gap: 1rem;
    }}
    .trust-logos {{
        justify-content: center;
    }}
}}
"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text}</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="preview-container">
        
        <header class="reveal">
            <div class="logo">
                <div class="logo-icon"></div>
                REBEL
            </div>
            <nav class="nav-links">
                <a href="#">Our Fleet</a>
                <a href="#">Mission</a>
                <a href="#">Intel</a>
            </nav>
            <a href="#" class="btn btn-ghost">Comm Link</a>
        </header>

        <main class="hero">
            <div class="hero-content">
                <h1 class="reveal delay-1">It's your <span>universe</span>,<br>it's time to save it.</h1>
                <p class="lead reveal delay-2">{body_text}</p>
                
                <div class="cta-group reveal delay-3">
                    <a href="#" class="btn btn-primary">Join Now For Free</a>
                </div>

                <div class="social-proof reveal delay-4">
                    <div class="avatars">
                        <!-- Placeholder avatars via UI Faces API simulation -->
                        <div class="avatar" style="background-image: url('https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?fit=crop&w=100&h=100');"></div>
                        <div class="avatar" style="background-image: url('https://images.unsplash.com/photo-1494790108377-be9c29b29330?fit=crop&w=100&h=100');"></div>
                        <div class="avatar" style="background-image: url('https://images.unsplash.com/photo-1534528741775-53994a69daeb?fit=crop&w=100&h=100');"></div>
                        <div class="avatar" style="background-image: url('https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?fit=crop&w=100&h=100');"></div>
                    </div>
                    <div class="proof-text">
                        <strong>Luke</strong> and 4,000+ others<br>have already joined.
                    </div>
                </div>
            </div>

            <div class="hero-visual reveal delay-2">
                <div class="hero-image-wrapper">
                    <!-- Abstract space/tech object acting as the floating hero element -->
                    <img src="{hero_image_url}" alt="Space Tech">
                </div>
            </div>
        </main>

        <footer class="trust-banner reveal delay-4">
            <p>Transmission Detected On</p>
            <div class="trust-logos">
                <!-- Generic SVG logos simulating media outlets -->
                <svg viewBox="0 0 100 30"><text x="0" y="20" font-family="Montserrat" font-weight="900" font-size="20">HOLO-NET</text></svg>
                <svg viewBox="0 0 100 30"><text x="0" y="20" font-family="Montserrat" font-weight="900" font-size="20">CORUSCANT TV</text></svg>
                <svg viewBox="0 0 100 30"><text x="0" y="20" font-family="Montserrat" font-weight="900" font-size="20">OUTER RIM NEWS</text></svg>
            </div>
        </footer>

    </div>
    <script src="script.js"></script>
</body>
</html>"""

    js = f"""// High-Impact Cinematic Hero - Interaction Logic

document.addEventListener('DOMContentLoaded', () => {{
    // Intersection Observer for smooth entrance animations
    const revealElements = document.querySelectorAll('.reveal');
    
    const revealOptions = {{
        threshold: 0.1,
        rootMargin: "0px 0px -50px 0px"
    }};

    const revealOnScroll = new IntersectionObserver(function(entries, observer) {{
        entries.forEach(entry => {{
            if (!entry.isIntersecting) {{
                return;
            }} else {{
                entry.target.classList.add('active');
                observer.unobserve(entry.target); // Only animate once
            }}
        }});
    }}, revealOptions);

    revealElements.forEach(el => {{
        revealOnScroll.observe(el);
    }});
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
