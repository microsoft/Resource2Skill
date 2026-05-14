def create_component(
    output_dir: str,
    title_text: str = "Meet Your<br>Creative Tribe.",
    body_text: str = "The community and training platform built to help you double your impact, learn new skills, and connect with peers.",
    cta_text: str = "Join the Waitlist",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#6366f1",     # Indigo accent
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the "Centered Hero with Floating Parallax Elements" visual effect.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    def hex_to_rgb(hex_color):
        hex_color = hex_color.lstrip('#')
        if len(hex_color) == 3:
            hex_color = ''.join([c*2 for c in hex_color])
        return f"{int(hex_color[0:2], 16)}, {int(hex_color[2:4], 16)}, {int(hex_color[4:6], 16)}"

    accent_rgb = hex_to_rgb(accent_color)

    if color_scheme == "dark":
        bg_color = "#0f172a"
        text_color = "#f8fafc"
        text_rgb = hex_to_rgb(text_color)
        surface_color = "rgba(30, 41, 59, 0.6)"
        border_color = "rgba(255, 255, 255, 0.1)"
    else:
        bg_color = "#f8fafc"
        text_color = "#0f172a"
        text_rgb = hex_to_rgb(text_color)
        surface_color = "rgba(255, 255, 255, 0.6)"
        border_color = "rgba(0, 0, 0, 0.05)"

    css = f"""/* Centered Hero with Floating Parallax Elements */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --text: {text_color};
    --text-rgb: {text_rgb};
    --accent: {accent_color};
    --accent-rgb: {accent_rgb};
    --surface: {surface_color};
    --border: {border_color};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background-color: #000; /* Outer canvas */
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 100vh;
    overflow: hidden;
}}

.hero-container {{
    width: var(--width);
    height: var(--height);
    max-width: 100vw;
    background-color: var(--bg);
    color: var(--text);
    position: relative;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    overflow: hidden;
}}

/* Ambient Background Glow */
.hero-container::before {{
    content: '';
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: 60%;
    height: 60%;
    background: radial-gradient(circle, rgba(var(--accent-rgb), 0.15) 0%, rgba(var(--accent-rgb), 0) 70%);
    z-index: 0;
    pointer-events: none;
}}

/* Central Content */
.hero-content {{
    position: relative;
    z-index: 10;
    text-align: center;
    max-width: 720px;
    padding: 0 24px;
}}

.hero-title {{
    font-size: clamp(2.5rem, 6vw, 4.5rem);
    font-weight: 800;
    line-height: 1.05;
    letter-spacing: -0.03em;
    margin-bottom: 24px;
}}

.hero-subtitle {{
    font-size: clamp(1rem, 2vw, 1.125rem);
    line-height: 1.6;
    color: rgba(var(--text-rgb), 0.75);
    margin-bottom: 40px;
    max-width: 600px;
    margin-inline: auto;
}}

.btn-primary {{
    background-color: var(--accent);
    color: #ffffff;
    font-size: 1.125rem;
    font-weight: 600;
    padding: 16px 36px;
    border-radius: 9999px;
    border: none;
    cursor: pointer;
    box-shadow: 0 10px 25px -5px rgba(var(--accent-rgb), 0.5);
    transition: all 0.3s cubic-bezier(0.2, 0.8, 0.2, 1);
}}

.btn-primary:hover {{
    transform: translateY(-3px) scale(1.02);
    box-shadow: 0 15px 35px -5px rgba(var(--accent-rgb), 0.6);
}}

/* Floating Elements */
.floating-layer {{
    position: absolute;
    inset: 0;
    z-index: 5;
    pointer-events: none; /* Let clicks pass through */
}}

.float-wrapper {{
    position: absolute;
    /* Smooths out the JS mousemove parallax */
    transition: transform 0.4s ease-out;
    will-change: transform;
}}

.anim-float {{
    animation: levitate 6s ease-in-out infinite;
}}

.float-avatar {{
    border-radius: 50%;
    object-fit: cover;
    border: 3px solid var(--surface);
    box-shadow: 0 10px 25px rgba(0,0,0,0.15);
}}

.float-badge {{
    background: var(--surface);
    color: var(--text);
    padding: 12px 20px;
    border-radius: 24px;
    font-size: 0.875rem;
    font-weight: 600;
    display: flex;
    align-items: center;
    gap: 8px;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border: 1px solid var(--border);
    white-space: nowrap;
}}

/* Specific Sizes and Positions */
.avatar-sm {{ width: 50px; height: 50px; }}
.avatar-md {{ width: 70px; height: 70px; }}
.avatar-lg {{ width: 90px; height: 90px; }}

.item-1 {{ top: 15%; left: 10%; }}
.item-2 {{ top: 45%; left: 5%; }}
.item-3 {{ bottom: 18%; left: 15%; }}
.item-4 {{ top: 20%; right: 10%; }}
.item-5 {{ top: 55%; right: 8%; }}
.item-6 {{ bottom: 25%; right: 15%; }}

/* Animation offsets to randomize bobbing */
.delay-1 {{ animation-delay: 0s; }}
.delay-2 {{ animation-delay: -1.5s; animation-duration: 5s; }}
.delay-3 {{ animation-delay: -3s; animation-duration: 7s; }}
.delay-4 {{ animation-delay: -0.5s; animation-duration: 6.5s; }}
.delay-5 {{ animation-delay: -2s; animation-duration: 5.5s; }}
.delay-6 {{ animation-delay: -4s; animation-duration: 6s; }}

@keyframes levitate {{
    0%, 100% {{ transform: translateY(0px); }}
    50% {{ transform: translateY(-15px); }}
}}

/* Responsive hiding for very small screens */
@media (max-width: 768px) {{
    .float-wrapper {{ display: none; }}
    .hero-container::before {{ width: 100%; height: 100%; }}
}}
"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Centered Hero Layout</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <section class="hero-container">
        
        <!-- Peripheral Floating Layer -->
        <div class="floating-layer" aria-hidden="true">
            <div class="float-wrapper item-1" data-depth="1.2">
                <div class="anim-float delay-1">
                    <img src="https://i.pravatar.cc/150?img=68" alt="" class="float-avatar avatar-sm">
                </div>
            </div>
            <div class="float-wrapper item-2" data-depth="2.5">
                <div class="anim-float delay-2">
                    <div class="float-badge">🎨 New design competition</div>
                </div>
            </div>
            <div class="float-wrapper item-3" data-depth="0.8">
                <div class="anim-float delay-3">
                    <img src="https://i.pravatar.cc/150?img=47" alt="" class="float-avatar avatar-lg">
                </div>
            </div>
            <div class="float-wrapper item-4" data-depth="1.8">
                <div class="anim-float delay-4">
                    <div class="float-badge">💬 Just landed a $10k project!</div>
                </div>
            </div>
            <div class="float-wrapper item-5" data-depth="1.1">
                <div class="anim-float delay-5">
                    <img src="https://i.pravatar.cc/150?img=33" alt="" class="float-avatar avatar-md">
                </div>
            </div>
            <div class="float-wrapper item-6" data-depth="2.2">
                <div class="anim-float delay-6">
                    <div class="float-badge">💡 How do I price this site?</div>
                </div>
            </div>
        </div>

        <!-- Core Content -->
        <div class="hero-content">
            <h1 class="hero-title">{title_text}</h1>
            <p class="hero-subtitle">{body_text}</p>
            <button class="btn-primary" aria-label="{cta_text}">{cta_text}</button>
        </div>

    </section>
    <script src="script.js"></script>
</body>
</html>"""

    js = f"""// Parallax Mouse tracking for floating elements
document.addEventListener('DOMContentLoaded', () => {{
    const container = document.querySelector('.hero-container');
    const wrappers = document.querySelectorAll('.float-wrapper');

    // Only apply parallax on desktop dimensions where elements are visible
    if (window.innerWidth <= 768) return;

    container.addEventListener('mousemove', (e) => {{
        const rect = container.getBoundingClientRect();
        
        // Normalize mouse coordinates to range [-0.5, 0.5]
        const x = (e.clientX - rect.left) / rect.width - 0.5;
        const y = (e.clientY - rect.top) / rect.height - 0.5;

        wrappers.forEach(wrapper => {{
            const depth = parseFloat(wrapper.getAttribute('data-depth')) || 1;
            // The deeper the depth multiplier, the more the element moves
            const moveX = x * -50 * depth; 
            const moveY = y * -50 * depth;
            
            wrapper.style.transform = `translate(${{moveX}}px, ${{moveY}}px)`;
        }});
    }});

    // Gracefully reset elements to center origin when mouse leaves hero
    container.addEventListener('mouseleave', () => {{
        wrappers.forEach(wrapper => {{
            wrapper.style.transform = `translate(0px, 0px)`;
        }});
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
