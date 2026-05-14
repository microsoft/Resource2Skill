def create_component(
    output_dir: str,
    title_text: str = "It's your universe, it's time to save it",
    body_text: str = "The Rebel alliance is fighting to get rid of the evil empire. Join the resistance to create a better future for your children.",
    color_scheme: str = "dark",        
    accent_color: str = "#E63946",     
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the High-Conversion Optimized Hero Section.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Derive theme colors based on the requested scheme
    if color_scheme == "dark":
        bg_color = "#0a0b10"
        text_color = "#ffffff"
        text_muted = "rgba(255, 255, 255, 0.7)"
        border_color = "rgba(255, 255, 255, 0.1)"
        bg_image = "https://images.unsplash.com/photo-1462331940025-496dfbfc7564?q=80&w=2000&auto=format&fit=crop" # Space background
    else:
        bg_color = "#f8f9fa"
        text_color = "#111827"
        text_muted = "rgba(0, 0, 0, 0.6)"
        border_color = "rgba(0, 0, 0, 0.1)"
        bg_image = "https://images.unsplash.com/photo-1557683311-eac922347aa1?q=80&w=2000&auto=format&fit=crop" # Bright abstract background

    # CSS Content
    css = f"""/* High-Conversion Optimized Hero Section */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700;800;900&display=swap');

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
    --border: {border_color};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Inter', sans-serif;
    background-color: var(--bg);
    color: var(--text);
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 100vh;
    overflow-x: hidden;
}}

/* Container sizing to match requirements */
.hero-wrapper {{
    width: var(--width);
    height: var(--height);
    position: relative;
    overflow: hidden;
    display: flex;
    flex-direction: column;
    background-image: linear-gradient(to bottom, rgba(0,0,0,0.3), var(--bg) 90%), url('{bg_image}');
    background-size: cover;
    background-position: center;
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
}}

/* Navbar */
.top-nav {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 2rem 4rem;
    z-index: 10;
}}

.logo {{
    font-weight: 900;
    font-size: 1.5rem;
    letter-spacing: -0.05em;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}}

.logo-icon {{
    color: var(--accent);
}}

.nav-links {{
    display: flex;
    gap: 2.5rem;
    list-style: none;
}}

.nav-links li {{
    font-weight: 500;
    font-size: 0.95rem;
    color: var(--text-muted);
    cursor: pointer;
    transition: color 0.2s ease;
}}

.nav-links li:hover {{
    color: var(--text);
}}

/* Buttons */
.btn {{
    padding: 0.8rem 1.8rem;
    border-radius: 4px;
    font-weight: 700;
    font-size: 0.9rem;
    cursor: pointer;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    text-transform: uppercase;
    letter-spacing: 0.05em;
}}

.btn-primary {{
    background-color: var(--accent);
    color: #fff;
    border: none;
    box-shadow: 0 4px 14px 0 rgba(0, 0, 0, 0.2);
}}

.btn-primary:hover {{
    transform: translateY(-2px) scale(1.02);
    box-shadow: 0 6px 20px 0 rgba(0, 0, 0, 0.3);
    filter: brightness(1.1);
}}

.btn-ghost {{
    background-color: transparent;
    color: var(--text);
    border: 2px solid var(--border);
}}

.btn-ghost:hover {{
    border-color: var(--text);
    background-color: rgba(255, 255, 255, 0.05);
}}

/* Main Hero Layout */
.hero-content {{
    display: flex;
    flex: 1;
    align-items: center;
    padding: 0 4rem;
    gap: 4rem;
    z-index: 10;
}}

.text-column {{
    flex: 1;
    max-width: 550px;
    animation: fadeUp 1s ease-out forwards;
}}

.image-column {{
    flex: 1;
    display: flex;
    justify-content: center;
    align-items: center;
    animation: fadeUp 1s ease-out 0.2s forwards;
    opacity: 0;
}}

/* Typography */
.title {{
    font-size: 4rem;
    font-weight: 800;
    line-height: 1.1;
    margin-bottom: 1.5rem;
    letter-spacing: -0.03em;
}}

.body-text {{
    font-size: 1.15rem;
    line-height: 1.6;
    color: var(--text-muted);
    margin-bottom: 2.5rem;
}}

/* Social Proof Section */
.social-proof {{
    display: flex;
    align-items: center;
    gap: 1rem;
    margin-top: 2rem;
    padding-top: 2rem;
    border-top: 1px solid var(--border);
}}

.avatars {{
    display: flex;
}}

.avatars img {{
    width: 38px;
    height: 38px;
    border-radius: 50%;
    border: 2px solid var(--bg);
    margin-left: -12px;
    position: relative;
    object-fit: cover;
}}

.avatars img:nth-child(1) {{ z-index: 3; margin-left: 0; }}
.avatars img:nth-child(2) {{ z-index: 2; }}
.avatars img:nth-child(3) {{ z-index: 1; }}

.proof-text {{
    font-size: 0.9rem;
    color: var(--text-muted);
    font-weight: 500;
}}

/* Floating Featured Image */
.featured-graphic {{
    width: 100%;
    max-width: 500px;
    filter: drop-shadow(0 20px 30px rgba(0,0,0,0.5));
    animation: float 6s ease-in-out infinite;
}}

/* Trust Banner */
.trust-banner {{
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 2rem;
    padding: 2rem;
    color: var(--text-muted);
    font-size: 0.9rem;
    font-weight: 500;
    z-index: 10;
    animation: fadeUp 1s ease-out 0.4s forwards;
    opacity: 0;
}}

.logos {{
    display: flex;
    gap: 2.5rem;
    align-items: center;
    opacity: 0.7;
}}

/* Faking logos with typography for the demo */
.logo-sim {{
    font-size: 1.2rem;
    filter: grayscale(100%);
}}
.logo-sim.abc {{ font-weight: 800; letter-spacing: -1px; }}
.logo-sim.news {{ font-family: serif; font-weight: bold; font-style: italic; }}
.logo-sim.cnn {{ border: 1px solid currentColor; padding: 2px 6px; border-radius: 4px; font-weight: bold; }}
.logo-sim.fox {{ font-weight: 900; letter-spacing: 1px; }}

/* Animations */
@keyframes fadeUp {{
    from {{
        opacity: 0;
        transform: translateY(30px);
    }}
    to {{
        opacity: 1;
        transform: translateY(0);
    }}
}}

@keyframes float {{
    0% {{ transform: translateY(0px); }}
    50% {{ transform: translateY(-20px); }}
    100% {{ transform: translateY(0px); }}
}}
"""

    # HTML Content
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text}</title>
    <link rel="stylesheet" href="style.css">
    <!-- FontAwesome for Logo Icon -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
</head>
<body>
    <div class="hero-wrapper">
        
        <nav class="top-nav">
            <div class="logo">
                <i class="fa-solid fa-meteor logo-icon"></i> Rebel
            </div>
            <ul class="nav-links">
                <li>Our Ships</li>
                <li>Mission</li>
                <li>Donations</li>
            </ul>
            <button class="btn btn-ghost">Join Now</button>
        </nav>

        <main class="hero-content">
            <div class="text-column">
                <h1 class="title">{title_text}</h1>
                <p class="body-text">{body_text}</p>
                <button class="btn btn-primary">JOIN NOW FOR FREE</button>
                
                <div class="social-proof">
                    <div class="avatars">
                        <!-- Unsplash placeholder faces -->
                        <img src="https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?q=80&w=100&auto=format&fit=crop" alt="User">
                        <img src="https://images.unsplash.com/photo-1527980965255-d3b416303d12?q=80&w=100&auto=format&fit=crop" alt="User">
                        <img src="https://images.unsplash.com/photo-1438761681033-6461ffad8d80?q=80&w=100&auto=format&fit=crop" alt="User">
                    </div>
                    <span class="proof-text">Obi Wan and 4,000 others have already joined</span>
                </div>
            </div>

            <div class="image-column">
                <!-- Placeholder for the main featured graphic (e.g. composited ship) -->
                <!-- Using a transparent tech/space object from Unsplash source or a generic shaped image -->
                <img class="featured-graphic" src="https://images.unsplash.com/photo-1614729939124-032f0b56c9ce?q=80&w=600&auto=format&fit=crop&bg=transparent" alt="Spacecraft" style="border-radius: 50%; mix-blend-mode: screen;">
            </div>
        </main>

        <footer class="trust-banner">
            <span>As Seen On:</span>
            <div class="logos">
                <span class="logo-sim abc">abc</span>
                <span class="logo-sim news">NEWS</span>
                <span class="logo-sim cnn">CNN</span>
                <span class="logo-sim fox">FOX</span>
            </div>
        </footer>

    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # JS Content
    js = f"""// Interactive behaviors for the Hero Section
document.addEventListener('DOMContentLoaded', () => {{
    const primaryBtn = document.querySelector('.btn-primary');
    
    // Add an interactive ripple or slight scale effect via JS if desired, 
    // though CSS handles the primary hover state well.
    primaryBtn.addEventListener('click', function(e) {{
        // Simple visual feedback on click
        this.style.transform = 'scale(0.95)';
        setTimeout(() => {{
            this.style.transform = '';
        }}, 150);
        
        console.log("Conversion action triggered!");
    }});
}});
"""

    # Write files
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
