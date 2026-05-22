def create_component(
    output_dir: str,
    title_text: str = "Refer and Earn",
    body_text: str = "Refer Friends, Earn Points and Fees",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#8b5cf6",     # Violet accent
    width_px: int = 1000,
    height_px: int = 600,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Glassmorphism Masked Gradient Border effect.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme and accent_color ===
    if color_scheme == "dark":
        bg_color = "#0f1117"
        text_color = "#f8fafc"
        text_muted = "#94a3b8"
        surface_color = "rgba(255, 255, 255, 0.03)"
        surface_inner = "rgba(0, 0, 0, 0.2)"
        glass_border_fade = "rgba(255, 255, 255, 0.06)"
        blob_opacity = "0.25"
    else:
        bg_color = "#f8fafc"
        text_color = "#0f172a"
        text_muted = "#64748b"
        surface_color = "rgba(255, 255, 255, 0.6)"
        surface_inner = "rgba(255, 255, 255, 0.8)"
        glass_border_fade = "rgba(0, 0, 0, 0.08)"
        blob_opacity = "0.15"

    # === CSS ===
    css = f"""/* Glassmorphism Masked Gradient Border Component */
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
    --surface: {surface_color};
    --surface-inner: {surface_inner};
    --border-fade: {glass_border_fade};
    --blob-opacity: {blob_opacity};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background: var(--bg);
    color: var(--text);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
}}

.container {{
    width: var(--width);
    height: var(--height);
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
    background: var(--bg);
    overflow: hidden;
}}

/* Ambient glowing blob in the background to emphasize the glass blur */
.ambient-blob {{
    position: absolute;
    width: 600px;
    height: 600px;
    background: radial-gradient(circle, var(--accent) 0%, transparent 60%);
    filter: blur(60px);
    opacity: var(--blob-opacity);
    top: 50%;
    left: 40%;
    transform: translate(-50%, -50%);
    z-index: 0;
    pointer-events: none;
}}

/* --- Core Card Layout & Glassmorphism --- */
.card {{
    position: relative;
    width: min(100% - 48px, 420px);
    padding: 32px;
    border-radius: 24px;
    
    /* 1. Setup the transparent border to make physical room for the pseudo-element glow */
    border: 1px solid transparent;
    /* 2. Clip the card's background to the padding so it doesn't bleed into the border area */
    background-clip: padding-box;
    /* 3. Establish strict stacking context */
    isolation: isolate;

    /* Interactive hover glow combined with static surface */
    background-image: 
        radial-gradient(
            600px circle at var(--mouse-x, -1000px) var(--mouse-y, -1000px), 
            color-mix(in srgb, var(--accent) 15%, transparent),
            transparent 40%
        ),
        linear-gradient(var(--surface), var(--surface));
        
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    
    display: flex;
    flex-direction: column;
    gap: 28px;
    box-shadow: 0 12px 40px -12px rgba(0, 0, 0, 0.2);
    transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    z-index: 1;
}}

.card:hover {{
    transform: translateY(-4px);
    box-shadow: 0 16px 50px -12px color-mix(in srgb, var(--accent) 30%, transparent);
}}

/* --- Masked Gradient Border --- */
@keyframes shimmer {{
    0% {{ background-position: 0% 50%; }}
    50% {{ background-position: 100% 50%; }}
    100% {{ background-position: 0% 50%; }}
}}

.card::before {{
    content: "";
    position: absolute;
    /* Stretch over the transparent border */
    inset: -1px; 
    border-radius: inherit;
    /* The padding determines the border stroke width */
    padding: 1px; 
    
    background: linear-gradient(
        115deg, 
        var(--border-fade) 0%, 
        var(--accent) 50%, 
        var(--border-fade) 100%
    );
    background-size: 200% 100%;
    animation: shimmer 4s infinite linear;
    
    /* MASK MAGIC: Subtract content-box from border-box to leave only the 1px stroke */
    -webkit-mask: 
        linear-gradient(#fff 0 0) content-box, 
        linear-gradient(#fff 0 0);
    -webkit-mask-composite: xor;
    
    mask: 
        linear-gradient(#fff 0 0) content-box, 
        linear-gradient(#fff 0 0);
    mask-composite: exclude;
    
    z-index: -1;
    pointer-events: none;
}}

/* --- Inner Typography and Styling --- */
.card-header {{
    display: flex;
    flex-direction: column;
    gap: 6px;
}}
.title {{
    font-size: 1.25rem;
    font-weight: 600;
    letter-spacing: -0.02em;
    color: var(--text);
}}
.body-text {{
    font-size: 0.875rem;
    color: var(--text-muted);
    line-height: 1.5;
}}

.stats-row {{
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
    padding-bottom: 8px;
    border-bottom: 1px solid var(--border-fade);
}}
.stat-block {{
    display: flex;
    flex-direction: column;
    gap: 8px;
}}
.right-align {{
    align-items: flex-end;
}}
.stat-label {{
    font-size: 0.75rem;
    color: var(--text-muted);
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}}
.stat-value {{
    font-size: 1.125rem;
    font-weight: 500;
    color: var(--text);
}}
.code {{
    font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
    background: var(--surface-inner);
    padding: 4px 10px;
    border-radius: 6px;
    letter-spacing: 0.05em;
    font-size: 0.875rem;
    border: 1px solid var(--border-fade);
}}

.rewards-pill {{
    background: var(--surface-inner);
    border-radius: 12px;
    padding: 16px;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 6px;
    border: 1px solid var(--border-fade);
}}
.rewards-label {{
    font-size: 0.75rem;
    color: var(--text-muted);
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}}
.rewards-val {{
    font-size: 0.875rem;
    font-weight: 500;
    color: var(--text);
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
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        <!-- Abstract blur background to demonstrate glassmorphism -->
        <div class="ambient-blob"></div>
        
        <div class="card">
            <div class="card-header">
                <h2 class="title">{title_text}</h2>
                <p class="body-text">{body_text}</p>
            </div>
            
            <div class="stats-row">
                <div class="stat-block">
                    <span class="stat-label">Referral Code</span>
                    <span class="stat-value code">7D45564JK355</span>
                </div>
                <div class="stat-block right-align">
                    <span class="stat-label">Referred Users</span>
                    <span class="stat-value">4</span>
                </div>
            </div>
            
            <div class="rewards-pill">
                <span class="rewards-label">Rewards</span>
                <span class="rewards-val">20% Platform Fees + 10% Extra points</span>
            </div>
        </div>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Interactive Mouse Tracking for Card Ambient Glow
document.addEventListener('DOMContentLoaded', () => {{
    const card = document.querySelector('.card');
    
    // Set initial position off-screen so the glow isn't visible until hover
    card.style.setProperty('--mouse-x', `-1000px`);
    card.style.setProperty('--mouse-y', `-1000px`);
    
    card.addEventListener('mousemove', (e) => {{
        const rect = card.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        
        // Pass local cursor coordinates to CSS variables
        card.style.setProperty('--mouse-x', `${{x}}px`);
        card.style.setProperty('--mouse-y', `${{y}}px`);
    }});
    
    // Optional: Hide the cursor glow gracefully when leaving the card
    card.addEventListener('mouseleave', () => {{
        card.style.setProperty('--mouse-x', `-1000px`);
        card.style.setProperty('--mouse-y', `-1000px`);
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
