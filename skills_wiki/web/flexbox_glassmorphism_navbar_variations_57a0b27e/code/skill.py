def create_component(
    output_dir: str,
    title_text: str = "Flexbox Navbar Variations",
    body_text: str = "A comprehensive collection of glassmorphism navigation layouts.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#38bdf8",     # CSS hex color for accent
    width_px: int = 1200,
    height_px: int = 1000,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Flexbox Glassmorphism Navbar Variations.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Helper to convert hex to rgba for glow effects
    def hex_to_rgba(hex_color, alpha):
        hex_color = hex_color.lstrip('#')
        if len(hex_color) == 3:
            hex_color = ''.join([c*2 for c in hex_color])
        try:
            r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
            return f"rgba({r}, {g}, {b}, {alpha})"
        except:
            return f"rgba(56, 189, 248, {alpha})" # Fallback cyan

    accent_glow_strong = hex_to_rgba(accent_color, 0.6)
    accent_glow_soft = hex_to_rgba(accent_color, 0.3)

    if color_scheme == "dark":
        bg_color = "#0a0d14"
        text_color = "#f0f0f0"
        text_dim = "#94a3b8"
        surface_color = "rgba(255, 255, 255, 0.05)"
        border_color = "rgba(255, 255, 255, 0.1)"
        blob_color_2 = "#8b5cf6" # purple secondary
    else:
        bg_color = "#f8fafc"
        text_color = "#0f172a"
        text_dim = "#64748b"
        surface_color = "rgba(255, 255, 255, 0.4)"
        border_color = "rgba(0, 0, 0, 0.08)"
        blob_color_2 = "#fb923c" # orange secondary

    css = f"""/* Flexbox Glassmorphism Navbars */
:root {{
    --bg: {bg_color};
    --text: {text_color};
    --text-dim: {text_dim};
    --accent: {accent_color};
    --surface: {surface_color};
    --border: {border_color};
    --accent-glow: {accent_glow_strong};
    --accent-glow-soft: {accent_glow_soft};
    --blob-2: {blob_color_2};
}}

*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: 'Inter', system-ui, sans-serif;
    background-color: var(--bg);
    color: var(--text);
    min-height: 100vh;
    overflow-x: hidden;
    position: relative;
}}

/* Background decorative blobs to highlight the glass effect */
.bg-blob {{
    position: absolute;
    border-radius: 50%;
    filter: blur(80px);
    z-index: -1;
    opacity: 0.5;
}}
.blob-1 {{
    top: 10%;
    left: 15%;
    width: 350px;
    height: 350px;
    background: var(--accent);
}}
.blob-2 {{
    bottom: 10%;
    right: 15%;
    width: 400px;
    height: 400px;
    background: var(--blob-2);
}}

.preview-container {{
    width: 100%;
    max-width: {width_px}px;
    margin: 0 auto;
    padding: 3rem 1rem;
    display: flex;
    flex-direction: column;
    gap: 4rem;
}}

.header {{
    text-align: center;
    margin-bottom: 2rem;
}}
.header h1 {{ font-weight: 700; margin-bottom: 0.5rem; }}
.header p {{ color: var(--text-dim); }}

.nav-wrapper {{
    display: flex;
    flex-direction: column;
    gap: 0.8rem;
}}

.nav-label {{
    font-size: 0.85rem;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: var(--text-dim);
    font-weight: 600;
    padding-left: 1rem;
}}

/* =========================================
   Base Navbar Styles (Shared)
   ========================================= */
.navbar {{
    width: 100%;
    padding: 1rem 5%;
    background: var(--surface);
    border-bottom: 1px solid var(--border);
    border-radius: 12px;
    backdrop-filter: blur(15px);
    -webkit-backdrop-filter: blur(15px);
    display: flex;
    align-items: center;
    box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
}}

.logo {{
    font-size: 1.5rem;
    font-weight: 700;
    color: var(--accent);
    letter-spacing: 1px;
    cursor: pointer;
}}

.nav-links {{
    list-style: none;
    display: flex;
    gap: 2rem;
}}

.nav-links a {{
    text-decoration: none;
    color: var(--text-dim);
    font-weight: 500;
    transition: all 0.3s ease;
    position: relative;
}}

.nav-links a:hover,
.nav-links a:focus {{
    color: var(--accent);
    text-shadow: 0 0 10px var(--accent-glow);
    outline: none;
}}

.btn {{
    padding: 0.6rem 1.6rem;
    border-radius: 30px;
    font-weight: 600;
    font-size: 0.95rem;
    font-family: inherit;
    background: var(--accent);
    color: #fff; /* Enforce readable contrast for button text */
    border: none;
    cursor: pointer;
    box-shadow: 0 0 15px var(--accent-glow-soft);
    transition: all 0.3s ease;
}}

.btn:hover,
.btn:focus {{
    filter: brightness(0.9);
    box-shadow: 0 0 25px var(--accent-glow);
    transform: translateY(-1px);
    outline: none;
}}

/* =========================================
   Variation 1: Space Between
   ========================================= */
.type-1 {{
    justify-content: space-between;
}}

/* =========================================
   Variation 2: Flex End + Push Left
   ========================================= */
.type-2 {{
    justify-content: flex-end;
}}
.type-2 .logo {{
    margin-right: auto;
}}
.type-2 .nav-links {{
    margin-right: 2.5rem;
}}

/* =========================================
   Variation 3: Grouped Wrap
   ========================================= */
.type-3 {{
    justify-content: space-between;
}}
.type-3 .nav-group {{
    display: flex;
    align-items: center;
    gap: 2.5rem;
}}

/* =========================================
   Variation 4: Absolute Centering
   ========================================= */
.type-4 {{
    justify-content: space-between;
    position: relative;
}}
.type-4 .logo {{
    position: absolute;
    left: 50%;
    transform: translateX(-50%);
}}

/* =========================================
   Variation 5: Split Clusters
   ========================================= */
.type-5 {{
    justify-content: center;
    gap: 3rem;
}}

/* Responsive fallbacks */
@media (max-width: 850px) {{
    .nav-links, .btn {{ display: none; }}
    .navbar {{ justify-content: center !important; }}
    .type-4 .logo {{ position: static; transform: none; }}
    .type-3 .nav-group {{ justify-content: center; width: 100%; }}
    .navbar::after {{
        content: "☰";
        position: absolute;
        right: 5%;
        font-size: 1.5rem;
        color: var(--text);
        cursor: pointer;
    }}
}}
"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <!-- Decorative background elements -->
    <div class="bg-blob blob-1"></div>
    <div class="bg-blob blob-2"></div>

    <main class="preview-container">
        <header class="header">
            <h1>{title_text}</h1>
            <p>{body_text}</p>
        </header>

        <!-- Layout 1 -->
        <div class="nav-wrapper">
            <span class="nav-label">Layout 1: Space Between (Logo Left, Links Center, CTA Right)</span>
            <nav class="navbar type-1">
                <div class="logo">BRAND</div>
                <ul class="nav-links">
                    <li><a href="#">Home</a></li>
                    <li><a href="#">Features</a></li>
                    <li><a href="#">Pricing</a></li>
                    <li><a href="#">About</a></li>
                </ul>
                <button class="btn">Get Started</button>
            </nav>
        </div>

        <!-- Layout 2 -->
        <div class="nav-wrapper">
            <span class="nav-label">Layout 2: Flex End (Logo Left, Links & CTA Grouped Right)</span>
            <nav class="navbar type-2">
                <div class="logo">BRAND</div>
                <ul class="nav-links">
                    <li><a href="#">Home</a></li>
                    <li><a href="#">Features</a></li>
                    <li><a href="#">Pricing</a></li>
                    <li><a href="#">About</a></li>
                </ul>
                <button class="btn">Get Started</button>
            </nav>
        </div>

        <!-- Layout 3 -->
        <div class="nav-wrapper">
            <span class="nav-label">Layout 3: Grouped (Logo & Links Left, CTA Right)</span>
            <nav class="navbar type-3">
                <div class="nav-group">
                    <div class="logo">BRAND</div>
                    <ul class="nav-links">
                        <li><a href="#">Home</a></li>
                        <li><a href="#">Features</a></li>
                        <li><a href="#">Pricing</a></li>
                        <li><a href="#">About</a></li>
                    </ul>
                </div>
                <button class="btn">Get Started</button>
            </nav>
        </div>

        <!-- Layout 4 -->
        <div class="nav-wrapper">
            <span class="nav-label">Layout 4: Absolute Center (Links Left, Logo Center, CTA Right)</span>
            <nav class="navbar type-4">
                <ul class="nav-links">
                    <li><a href="#">Home</a></li>
                    <li><a href="#">Features</a></li>
                </ul>
                <div class="logo">BRAND</div>
                <button class="btn">Get Started</button>
            </nav>
        </div>

        <!-- Layout 5 -->
        <div class="nav-wrapper">
            <span class="nav-label">Layout 5: Split Center (Links Left, Logo Center, Links Right)</span>
            <nav class="navbar type-5">
                <ul class="nav-links">
                    <li><a href="#">Home</a></li>
                    <li><a href="#">Features</a></li>
                </ul>
                <div class="logo">BRAND</div>
                <ul class="nav-links">
                    <li><a href="#">Pricing</a></li>
                    <li><a href="#">Contact</a></li>
                </ul>
            </nav>
        </div>

    </main>
    <script src="script.js"></script>
</body>
</html>"""

    js = f"""// Flexbox Glassmorphism Navbars
document.addEventListener('DOMContentLoaded', () => {{
    // Add subtle entrance animation
    const wrappers = document.querySelectorAll('.nav-wrapper');
    wrappers.forEach((wrapper, index) => {{
        wrapper.style.opacity = '0';
        wrapper.style.transform = 'translateY(20px)';
        wrapper.style.transition = 'all 0.6s cubic-bezier(0.16, 1, 0.3, 1)';
        
        setTimeout(() => {{
            wrapper.style.opacity = '1';
            wrapper.style.transform = 'translateY(0)';
        }}, 100 + (index * 100));
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
