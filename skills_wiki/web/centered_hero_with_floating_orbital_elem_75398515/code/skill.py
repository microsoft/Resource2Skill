def create_component(
    output_dir: str,
    title_text: str = "Learn, compete and evolve together",
    body_text: str = "Join a tribe of like-minded creators building the future of the web. Connect, share, and double your income.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#6366f1",     # CSS hex color for accent (Indigo)
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the "Centered Hero with Floating Orbital Elements" visual effect.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors ===
    if color_scheme == "dark":
        bg_base = "#09090b"
        bg_glow = f"rgba({int(accent_color[1:3], 16)}, {int(accent_color[3:5], 16)}, {int(accent_color[5:7], 16)}, 0.2)"
        text_color = "#ffffff"
        text_muted = "#a1a1aa"
        surface_bg = "rgba(255, 255, 255, 0.03)"
        surface_border = "rgba(255, 255, 255, 0.08)"
        shadow_color = "rgba(0, 0, 0, 0.5)"
    else:
        bg_base = "#fafafa"
        bg_glow = f"rgba({int(accent_color[1:3], 16)}, {int(accent_color[3:5], 16)}, {int(accent_color[5:7], 16)}, 0.15)"
        text_color = "#09090b"
        text_muted = "#71717a"
        surface_bg = "rgba(255, 255, 255, 0.6)"
        surface_border = "rgba(0, 0, 0, 0.05)"
        shadow_color = "rgba(0, 0, 0, 0.05)"

    # === CSS ===
    css = f"""/* Centered Hero with Floating Orbital Elements */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg-base: {bg_base};
    --bg-glow: {bg_glow};
    --text-color: {text_color};
    --text-muted: {text_muted};
    --accent: {accent_color};
    --surface-bg: {surface_bg};
    --surface-border: {surface_border};
    --shadow: {shadow_color};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background-color: #000;
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 100vh;
}}

.hero-container {{
    width: var(--width);
    height: var(--height);
    max-width: 100vw;
    max-height: 100vh;
    background-color: var(--bg-base);
    background-image: radial-gradient(circle at 50% 40%, var(--bg-glow) 0%, transparent 50%);
    position: relative;
    overflow: hidden;
    display: flex;
    align-items: center;
    justify-content: center;
    text-align: center;
}}

/* Foreground Content */
.hero-content {{
    position: relative;
    z-index: 10;
    max-width: 800px;
    padding: 0 2rem;
    pointer-events: auto;
}}

.hero-title {{
    font-size: clamp(2.5rem, 5vw, 4.5rem);
    font-weight: 800;
    line-height: 1.1;
    letter-spacing: -0.03em;
    color: var(--text-color);
    margin-bottom: 1.5rem;
}}

.hero-subtitle {{
    font-size: clamp(1.1rem, 2vw, 1.25rem);
    line-height: 1.6;
    color: var(--text-muted);
    max-width: 600px;
    margin: 0 auto 2.5rem auto;
}}

.cta-button {{
    background-color: var(--accent);
    color: #ffffff;
    border: none;
    padding: 1rem 2.5rem;
    font-size: 1.1rem;
    font-weight: 600;
    border-radius: 50px;
    cursor: pointer;
    transition: transform 0.2s ease, filter 0.2s ease;
    box-shadow: 0 10px 25px var(--bg-glow);
}}

.cta-button:hover {{
    transform: translateY(-2px);
    filter: brightness(1.1);
}}

/* Background Orbital Elements */
.orbital-layer {{
    position: absolute;
    inset: 0;
    z-index: 1;
    pointer-events: none; /* Let clicks pass through to background */
}}

.float-wrapper {{
    position: absolute;
    /* Hardware acceleration for JS translation */
    will-change: transform; 
}}

.float-inner {{
    animation: bobbing 6s ease-in-out infinite;
    will-change: transform;
}}

/* Orbital Positions */
.el-1 {{ top: 15%; left: 12%; }}
.el-2 {{ top: 22%; right: 15%; }}
.el-3 {{ bottom: 25%; left: 18%; }}
.el-4 {{ bottom: 20%; right: 12%; }}
.el-5 {{ top: 50%; left: 5%; }}
.el-6 {{ top: 60%; right: 8%; }}

/* Stagger Animations */
.el-1 .float-inner {{ animation-delay: 0s; }}
.el-2 .float-inner {{ animation-delay: -1.2s; }}
.el-3 .float-inner {{ animation-delay: -3.5s; }}
.el-4 .float-inner {{ animation-delay: -2s; }}
.el-5 .float-inner {{ animation-delay: -4.1s; }}
.el-6 .float-inner {{ animation-delay: -0.8s; }}

/* Orbital Styles (Avatars & Badges) */
.avatar img {{
    width: 64px;
    height: 64px;
    border-radius: 50%;
    object-fit: cover;
    border: 3px solid var(--surface-border);
    box-shadow: 0 10px 20px var(--shadow);
}}

.badge {{
    background: var(--surface-bg);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border: 1px solid var(--surface-border);
    color: var(--text-color);
    padding: 0.75rem 1.5rem;
    border-radius: 30px;
    font-size: 0.9rem;
    font-weight: 500;
    box-shadow: 0 10px 30px var(--shadow);
    display: flex;
    align-items: center;
    gap: 8px;
    white-space: nowrap;
}}

@keyframes bobbing {{
    0%, 100% {{ transform: translateY(0); }}
    50% {{ transform: translateY(-18px); }}
}}

/* Responsive fallbacks for orbits */
@media (max-width: 768px) {{
    .orbital-layer {{ opacity: 0.3; filter: blur(2px); }}
    .float-wrapper {{ transform: scale(0.7) !important; }}
}}
"""

    # === HTML ===
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <main class="hero-container">
        
        <!-- Orbital Decorative Layer -->
        <div class="orbital-layer">
            <div class="float-wrapper el-1" data-speed="25">
                <div class="float-inner badge">✨ New design competition</div>
            </div>
            <div class="float-wrapper el-2" data-speed="-15">
                <div class="float-inner avatar">
                    <img src="https://i.pravatar.cc/150?img=32" alt="Community Member">
                </div>
            </div>
            <div class="float-wrapper el-3" data-speed="10">
                <div class="float-inner avatar">
                    <img src="https://i.pravatar.cc/150?img=47" alt="Community Member">
                </div>
            </div>
            <div class="float-wrapper el-4" data-speed="-30">
                <div class="float-inner badge">💡 How do I price this site?</div>
            </div>
            <div class="float-wrapper el-5" data-speed="35">
                <div class="float-inner avatar">
                    <img src="https://i.pravatar.cc/150?img=12" alt="Community Member">
                </div>
            </div>
            <div class="float-wrapper el-6" data-speed="-20">
                <div class="float-inner badge">🚀 Just landed a $10k project!</div>
            </div>
        </div>

        <!-- Main Content -->
        <div class="hero-content">
            <h1 class="hero-title">{title_text}</h1>
            <p class="hero-subtitle">{body_text}</p>
            <button class="cta-button">Join the Waitlist</button>
        </div>

    </main>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = """// Smooth Mouse Parallax for Orbital Elements
document.addEventListener('DOMContentLoaded', () => {
    const wrappers = document.querySelectorAll('.float-wrapper');
    const container = document.querySelector('.hero-container');
    
    // Target mouse coordinates (-1 to 1)
    let targetX = 0;
    let targetY = 0;
    
    // Current interpolated coordinates
    let currentX = 0;
    let currentY = 0;

    // Track mouse over the container
    container.addEventListener('mousemove', (e) => {
        const rect = container.getBoundingClientRect();
        // Calculate position relative to container center, normalized to -1 to 1
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        
        targetX = (x / rect.width - 0.5) * 2;
        targetY = (y / rect.height - 0.5) * 2;
    });

    // Reset when mouse leaves
    container.addEventListener('mouseleave', () => {
        targetX = 0;
        targetY = 0;
    });

    // Animation loop using Linear Interpolation (LERP)
    function animate() {
        // LERP factor (lower = smoother/slower)
        const ease = 0.05;
        
        currentX += (targetX - currentX) * ease;
        currentY += (targetY - currentY) * ease;

        wrappers.forEach(el => {
            // Get designated speed/direction from HTML attribute
            const speed = parseFloat(el.getAttribute('data-speed')) || 20;
            
            // Calculate pixel offset
            const xOffset = currentX * speed;
            const yOffset = currentY * speed;
            
            // Apply transform. 
            // Note: Inner div handles the CSS bobbing animation separately.
            el.style.transform = `translate(${xOffset}px, ${yOffset}px)`;
        });

        requestAnimationFrame(animate);
    }
    
    // Start loop
    animate();
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
