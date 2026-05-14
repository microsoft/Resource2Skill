def create_component(
    output_dir: str,
    title_text: str = "Get our<br><span class='highlight'>Lottie animations</span>",
    body_text: str = "They're the best!",
    color_scheme: str = "dark",
    accent_color: str = "#a855f7",
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Interactive Lottie Animation Integration effect.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors ===
    if color_scheme == "dark":
        bg_color = "#111827"
        text_color = "#f9fafb"
        muted_text = "#9ca3af"
        input_bg = "#374151"
        glow_color = f"rgba(168, 85, 247, 0.15)"
    else:
        bg_color = "#f3f4f6"
        text_color = "#111827"
        muted_text = "#4b5563"
        input_bg = "#ffffff"
        glow_color = f"rgba(168, 85, 247, 0.1)"

    # Using public Lottie URLs representing the ones used in the video
    hero_lottie_url = "https://assets7.lottiefiles.com/packages/lf20_70nDCE.json"
    twitter_lottie_url = "https://assets8.lottiefiles.com/packages/lf20_th1bypwb.json"
    facebook_lottie_url = "https://assets5.lottiefiles.com/packages/lf20_nnlareso.json"

    # === CSS ===
    css = f"""/* Interactive Lottie Integration — generated component */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --text: {text_color};
    --muted: {muted_text};
    --accent: {accent_color};
    --input-bg: {input_bg};
    --glow: {glow_color};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background-color: var(--bg);
    color: var(--text);
    min-height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
    overflow-x: hidden;
    position: relative;
}}

/* Background aesthetic glow simulating the video's dark mode design */
body::before {{
    content: '';
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: 80%;
    height: 80%;
    background: radial-gradient(circle, var(--glow) 0%, transparent 70%);
    z-index: 0;
    pointer-events: none;
}}

.container {{
    width: var(--width);
    height: var(--height);
    max-width: 100vw;
    position: relative;
    z-index: 1;
    display: flex;
    flex-direction: column;
    padding: 2rem 4rem;
}}

/* Top Navigation with Animated Icons */
nav {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding-bottom: 2rem;
}}

.logo {{
    font-size: 1.5rem;
    font-weight: 800;
    letter-spacing: -0.05em;
}}

.social-links {{
    display: flex;
    gap: 1rem;
}}

/* Social Icon Container - scaling transform matches the video behavior */
.social-icon {{
    width: 32px;
    height: 32px;
    cursor: pointer;
    transition: transform 0.2s ease;
    border-radius: 50%;
}}

.social-icon:hover {{
    transform: scale(1.1);
}}

/* Hero Section */
.hero {{
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 4rem;
}}

.hero-content {{
    flex: 1;
    max-width: 500px;
}}

.title {{
    font-size: 4rem;
    line-height: 1.1;
    font-weight: 800;
    margin-bottom: 1rem;
    letter-spacing: -0.02em;
}}

.highlight {{
    background: linear-gradient(to right, var(--accent), #ec4899);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}}

.body-text {{
    font-size: 1.5rem;
    color: var(--muted);
    font-weight: 500;
    margin-bottom: 2.5rem;
}}

.newsletter-form {{
    background: rgba(255, 255, 255, 0.05);
    padding: 1.5rem;
    border-radius: 0.5rem;
    border: 1px solid rgba(255,255,255,0.1);
}}

.newsletter-form label {{
    display: block;
    font-size: 0.875rem;
    font-weight: 600;
    margin-bottom: 0.5rem;
}}

.input-group {{
    display: flex;
    flex-direction: column;
    gap: 1rem;
}}

input[type="email"] {{
    padding: 0.75rem 1rem;
    border-radius: 0.25rem;
    border: none;
    background: var(--input-bg);
    color: var(--text);
    font-size: 1rem;
    width: 100%;
    outline: none;
}}

button {{
    padding: 0.75rem 1.5rem;
    border-radius: 0.25rem;
    border: none;
    background: linear-gradient(to right, var(--accent), #d946ef);
    color: white;
    font-weight: 700;
    font-size: 1rem;
    cursor: pointer;
    transition: filter 0.2s;
    align-self: flex-start;
}}

button:hover {{
    filter: brightness(1.1);
}}

/* Hero Graphic Stage */
.hero-graphic {{
    flex: 1;
    display: flex;
    justify-content: center;
    align-items: center;
}}

.lottie-hero-wrapper {{
    width: 100%;
    max-width: 500px;
    filter: drop-shadow(0 20px 30px rgba(0,0,0,0.3));
}}
"""

    # === HTML ===
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Interactive Lottie Component</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
    
    <!-- Lottie Player Script (Dependency) -->
    <script src="https://unpkg.com/@lottiefiles/lottie-player@latest/dist/lottie-player.js"></script>
</head>
<body>
    <div class="container">
        
        <nav>
            <div class="logo">Lottie</div>
            <div class="social-links">
                <!-- Interactive Hover Animation: Twitter -->
                <div class="social-icon">
                    <lottie-player 
                        src="{twitter_lottie_url}" 
                        background="transparent" 
                        speed="1" 
                        hover
                        style="width: 100%; height: 100%;">
                    </lottie-player>
                </div>
                <!-- Interactive Hover Animation: Facebook -->
                <div class="social-icon">
                    <lottie-player 
                        src="{facebook_lottie_url}" 
                        background="transparent" 
                        speed="1" 
                        hover
                        style="width: 100%; height: 100%;">
                    </lottie-player>
                </div>
            </div>
        </nav>

        <main class="hero">
            <div class="hero-content">
                <h1 class="title">{title_text}</h1>
                <p class="body-text">{body_text}</p>
                
                <div class="newsletter-form">
                    <label>Sign up for our newsletter</label>
                    <div class="input-group">
                        <input type="email" placeholder="you@somewhere.com">
                        <button type="button">Sign Up</button>
                    </div>
                </div>
            </div>

            <div class="hero-graphic">
                <!-- Autoplaying Looping Hero Animation -->
                <div class="lottie-hero-wrapper">
                    <lottie-player 
                        src="{hero_lottie_url}" 
                        background="transparent" 
                        speed="2" 
                        loop 
                        autoplay
                        style="width: 100%; height: auto;">
                    </lottie-player>
                </div>
            </div>
        </main>
        
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = """// Lottie animations in this component are handled declaratively via HTML attributes.
// The @lottiefiles/lottie-player web component handles Intersection Observers, 
// hover event listeners, and animation loop execution natively.

document.addEventListener('DOMContentLoaded', () => {
    // If you need programmatic control over the Lottie player later:
    // const player = document.querySelector('.lottie-hero-wrapper lottie-player');
    // player.play();
    // player.pause();
    // player.setSpeed(1.5);
    console.log("Lottie Web Player component loaded and active.");
});
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
