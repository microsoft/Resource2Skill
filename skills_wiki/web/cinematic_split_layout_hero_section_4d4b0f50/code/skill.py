def create_component(
    output_dir: str,
    title_text: str = "It's your universe, it's time to save it",
    body_text: str = "The Alliance is fighting to get rid of the evil empire. Join the resistance to create a better future for your children.",
    color_scheme: str = "dark",
    accent_color: str = "#E62429", # A cinematic, rebel red
    width_px: int = 1280,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Cinematic Split-Layout Hero Section.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Derive theme colors
    if color_scheme == "light":
        bg_color = "#ffffff"
        bg_gradient = "radial-gradient(circle at 75% 50%, #f3f4f6 0%, #ffffff 60%)"
        text_primary = "#111827"
        text_secondary = "#4b5563"
        nav_border = "rgba(0, 0, 0, 0.2)"
        social_text = "#6b7280"
        logo_bg = "#f3f4f6"
    else:
        bg_color = "#0b0f19"
        bg_gradient = "radial-gradient(circle at 75% 50%, #1e293b 0%, #0b0f19 60%)"
        text_primary = "#ffffff"
        text_secondary = "#94a3b8"
        nav_border = "rgba(255, 255, 255, 0.2)"
        social_text = "#94a3b8"
        logo_bg = "rgba(255, 255, 255, 0.05)"

    css = f"""/* Cinematic Split-Layout Hero Section */
:root {{
    --bg-color: {bg_color};
    --bg-gradient: {bg_gradient};
    --text-primary: {text_primary};
    --text-secondary: {text_secondary};
    --accent-color: {accent_color};
    --nav-border: {nav_border};
    --social-text: {social_text};
    --logo-bg: {logo_bg};
}}

* {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background-color: var(--bg-color);
    background-image: var(--bg-gradient);
    color: var(--text-primary);
    min-height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
    overflow-x: hidden;
}}

.hero-wrapper {{
    width: 100%;
    max-width: {width_px}px;
    height: {height_px}px;
    max-height: 100vh;
    display: flex;
    flex-direction: column;
    position: relative;
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
    background-color: var(--bg-color);
    background-image: var(--bg-gradient);
    overflow: hidden;
}}

/* Navbar Styles */
.navbar {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 2rem 5%;
    z-index: 10;
}}

.logo {{
    font-size: 1.5rem;
    font-weight: 800;
    letter-spacing: -0.05em;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}}

.logo-icon {{
    width: 24px;
    height: 24px;
    background-color: var(--accent-color);
    border-radius: 50%;
}}

.nav-links {{
    display: flex;
    gap: 2.5rem;
}}

.nav-links a {{
    color: var(--text-primary);
    text-decoration: none;
    font-size: 0.95rem;
    font-weight: 500;
    transition: opacity 0.2s;
}}

.nav-links a:hover {{
    opacity: 0.7;
}}

/* Button Styles */
.btn {{
    padding: 0.875rem 2rem;
    border-radius: 4px;
    font-weight: 700;
    font-size: 0.95rem;
    cursor: pointer;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    transition: all 0.3s ease;
    border: none;
}}

.btn-ghost {{
    background: transparent;
    color: var(--text-primary);
    border: 1px solid var(--nav-border);
}}

.btn-ghost:hover {{
    background: var(--nav-border);
}}

.btn-primary {{
    background-color: var(--accent-color);
    color: #ffffff;
    box-shadow: 0 10px 20px -10px var(--accent-color);
}}

.btn-primary:hover {{
    transform: translateY(-2px);
    box-shadow: 0 15px 25px -10px var(--accent-color);
    filter: brightness(1.1);
}}

/* Main Hero Area */
.hero-main {{
    flex: 1;
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 4rem;
    padding: 0 5% 4rem 5%;
    align-items: center;
    z-index: 5;
}}

/* Left Column: Content */
.hero-content {{
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    gap: 1.5rem;
}}

.hero-title {{
    font-size: clamp(2.5rem, 5vw, 4.5rem);
    line-height: 1.1;
    font-weight: 800;
    letter-spacing: -0.02em;
    /* Entrance Animation Prep */
    opacity: 0;
    transform: translateY(20px);
    animation: fadeUp 0.8s ease forwards 0.2s;
}}

.hero-subtitle {{
    font-size: 1.125rem;
    line-height: 1.6;
    color: var(--text-secondary);
    max-width: 90%;
    /* Entrance Animation Prep */
    opacity: 0;
    transform: translateY(20px);
    animation: fadeUp 0.8s ease forwards 0.4s;
}}

.hero-cta-group {{
    margin-top: 1rem;
    /* Entrance Animation Prep */
    opacity: 0;
    transform: translateY(20px);
    animation: fadeUp 0.8s ease forwards 0.6s;
}}

/* Social Proof */
.social-proof {{
    margin-top: 3rem;
    display: flex;
    flex-direction: column;
    gap: 1rem;
    /* Entrance Animation Prep */
    opacity: 0;
    transform: translateY(20px);
    animation: fadeUp 0.8s ease forwards 0.8s;
}}

.social-proof-label {{
    font-size: 0.875rem;
    color: var(--social-text);
    text-transform: uppercase;
    letter-spacing: 0.1em;
    font-weight: 600;
}}

.social-logos {{
    display: flex;
    gap: 1.5rem;
    align-items: center;
}}

.mock-logo {{
    font-family: serif;
    font-weight: 900;
    font-size: 1.25rem;
    color: var(--text-primary);
    opacity: 0.5;
    background: var(--logo-bg);
    padding: 0.5rem 1rem;
    border-radius: 4px;
    letter-spacing: 1px;
    transition: opacity 0.3s;
    user-select: none;
}}

.mock-logo:hover {{
    opacity: 1;
}}

/* Right Column: Visual */
.hero-visual {{
    width: 100%;
    height: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
    position: relative;
    /* Entrance Animation Prep */
    opacity: 0;
    transform: scale(0.95);
    animation: fadeInScale 1s cubic-bezier(0.2, 0.8, 0.2, 1) forwards 0.4s;
}}

.hero-image-wrapper {{
    width: 100%;
    max-width: 600px;
    aspect-ratio: 1 / 1;
    position: relative;
    animation: float 6s ease-in-out infinite;
}}

.hero-image {{
    width: 100%;
    height: 100%;
    object-fit: cover;
    border-radius: 20px;
    box-shadow: 0 25px 50px -12px rgba(0,0,0,0.5);
    /* Subtle border to separate from dark background */
    border: 1px solid rgba(255,255,255,0.05);
}}

/* Dynamic Glow behind image */
.hero-image-wrapper::before {{
    content: '';
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: 80%;
    height: 80%;
    background: var(--accent-color);
    filter: blur(100px);
    opacity: 0.15;
    z-index: -1;
    border-radius: 50%;
}}

/* Animations */
@keyframes fadeUp {{
    to {{
        opacity: 1;
        transform: translateY(0);
    }}
}}

@keyframes fadeInScale {{
    to {{
        opacity: 1;
        transform: scale(1);
    }}
}}

@keyframes float {{
    0% {{ transform: translateY(0px); }}
    50% {{ transform: translateY(-20px); }}
    100% {{ transform: translateY(0px); }}
}}

/* Responsive Design */
@media (max-width: 900px) {{
    .hero-main {{
        grid-template-columns: 1fr;
        text-align: center;
        gap: 2rem;
    }}
    
    .hero-content {{
        align-items: center;
    }}
    
    .hero-subtitle {{
        margin: 0 auto;
    }}
    
    .social-logos {{
        justify-content: center;
    }}
    
    .nav-links {{
        display: none; /* Hide links on mobile for simplicity in this demo */
    }}
}}
"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cinematic Hero Section</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="hero-wrapper">
        
        <!-- Header / Navigation -->
        <header class="navbar">
            <div class="logo">
                <div class="logo-icon"></div>
                ALLIANCE
            </div>
            <nav class="nav-links">
                <a href="#ships">Our Ships</a>
                <a href="#mission">Mission</a>
                <a href="#donations">Donations</a>
            </nav>
            <button class="btn btn-ghost">JOIN NOW</button>
        </header>

        <!-- Main Hero Section -->
        <main class="hero-main">
            
            <!-- Left Side: Copy & CTA -->
            <div class="hero-content">
                <h1 class="hero-title">{title_text}</h1>
                <p class="hero-subtitle">{body_text}</p>
                
                <div class="hero-cta-group">
                    <button class="btn btn-primary">JOIN NOW FOR FREE</button>
                </div>

                <!-- Optimization/Social Proof -->
                <div class="social-proof">
                    <span class="social-proof-label">Trusted By Over 4,000 Recruits & Seen On:</span>
                    <div class="social-logos">
                        <span class="mock-logo">GNN</span>
                        <span class="mock-logo">HoloNet</span>
                        <span class="mock-logo">Tribune</span>
                    </div>
                </div>
            </div>

            <!-- Right Side: Visual focal point -->
            <div class="hero-visual">
                <div class="hero-image-wrapper">
                    <!-- Using a high-quality abstract/space placeholder to mimic the complex composite -->
                    <img src="https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?q=80&w=1000&auto=format&fit=crop" alt="Abstract Hero Visual" class="hero-image">
                </div>
            </div>

        </main>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    js = """// No complex JS required for this component.
// Animations are handled via performant CSS keyframes.
// Interactive behaviors (parallax, advanced tracking) could be initialized here if needed.

document.addEventListener('DOMContentLoaded', () => {
    console.log("Cinematic Hero Section Loaded Successfully.");
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
