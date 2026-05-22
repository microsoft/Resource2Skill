def create_component(
    output_dir: str,
    title_text: str = "Ask anything",
    body_text: str = "Trying to wrap your head around a new topic? Looking for specific recommendations? We'll help you decode it.",
    color_scheme: str = "dark",        
    accent_color: str = "#8a2be2",     
    width_px: int = 420,
    height_px: int = 280,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Glassmorphism Card with Masked Gradient Border effect.
    
    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors ===
    if color_scheme == "dark":
        page_bg = "#0d1117"
        card_bg = "rgba(255, 255, 255, 0.02)"
        border_light = "rgba(255, 255, 255, 0.3)"
        border_dark = "rgba(255, 255, 255, 0.05)"
        text_color = "#f0f6fc"
        text_muted = "#8b949e"
        icon_bg = "rgba(255, 255, 255, 0.05)"
        icon_border = "rgba(255, 255, 255, 0.1)"
    else:
        page_bg = "#f3f4f6"
        card_bg = "rgba(255, 255, 255, 0.4)"
        border_light = "rgba(255, 255, 255, 0.8)"
        border_dark = "rgba(255, 255, 255, 0.2)"
        text_color = "#111827"
        text_muted = "#4b5563"
        icon_bg = "rgba(255, 255, 255, 0.5)"
        icon_border = "rgba(255, 255, 255, 0.4)"

    # === CSS ===
    css = f"""/* Glassmorphism Card with Masked Gradient Border */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --page-bg: {page_bg};
    --card-bg: {card_bg};
    --text-color: {text_color};
    --text-muted: {text_muted};
    --accent: {accent_color};
    --border-light: {border_light};
    --border-dark: {border_dark};
    --icon-bg: {icon_bg};
    --icon-border: {icon_border};
    
    /* Using color-mix to create dynamic translucent variations of the accent color */
    --accent-glow: color-mix(in srgb, var(--accent) 30%, transparent);
    --orb-1: color-mix(in srgb, var(--accent) 25%, transparent);
    --orb-2: color-mix(in srgb, #4169e1 20%, transparent);
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background-color: var(--page-bg);
    /* Abstract background to show off the glass blur effect */
    background-image: 
        radial-gradient(circle at 15% 20%, var(--orb-1) 0%, transparent 40%),
        radial-gradient(circle at 85% 80%, var(--orb-2) 0%, transparent 40%);
    color: var(--text-color);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
    padding: 2rem;
}}

.card {{
    width: {width_px}px;
    max-width: 100%;
    min-height: {height_px}px;
    position: relative;
    border-radius: 20px;
    padding: 32px;
    display: flex;
    flex-direction: column;
    gap: 16px;
    
    /* True Glass Background */
    background: 
        radial-gradient(circle at 50% 150%, var(--accent-glow), transparent 60%),
        var(--card-bg);
    
    /* The Blur */
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    
    /* Ambient Shadow */
    box-shadow: 0 12px 32px 0 rgba(0, 0, 0, 0.2);
    
    transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1), box-shadow 0.3s ease;
    cursor: pointer;
}}

.card:hover {{
    transform: translateY(-4px);
    box-shadow: 0 16px 40px 0 rgba(0, 0, 0, 0.3), 0 0 40px 0 var(--accent-glow);
}}

/* THE MASKED GRADIENT BORDER TRICK */
.card::before {{
    content: "";
    position: absolute;
    inset: 0; /* Cover the whole card */
    border-radius: inherit; /* Match card radius exactly */
    z-index: -1;
    pointer-events: none;
    
    /* Set border width using a transparent border */
    border: 1px solid transparent; 
    
    /* The actual gradient that will act as the border */
    background: linear-gradient(180deg, var(--border-light), var(--border-dark)) border-box;
    
    /* The Masking logic to cut out the center */
    -webkit-mask: 
        linear-gradient(#fff 0 0) padding-box, 
        linear-gradient(#fff 0 0);
    -webkit-mask-composite: xor;
    
    /* Standard CSS Masking */
    mask: 
        linear-gradient(#fff 0 0) padding-box, 
        linear-gradient(#fff 0 0);
    mask-composite: exclude;
    
    transition: opacity 0.3s ease;
}}

.card:hover::before {{
    background: linear-gradient(180deg, var(--accent), var(--border-dark)) border-box;
    opacity: 1;
}}

/* Inner Content Styling */
.card-icon {{
    width: 48px;
    height: 48px;
    border-radius: 12px;
    background: var(--icon-bg);
    border: 1px solid var(--icon-border);
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 8px;
    color: var(--accent);
}}

.card-title {{
    font-size: 1.5rem;
    font-weight: 600;
    letter-spacing: -0.02em;
    line-height: 1.2;
}}

.card-body {{
    font-size: 0.95rem;
    line-height: 1.6;
    color: var(--text-muted);
}}

.card-button {{
    align-self: flex-start;
    margin-top: auto;
    background: transparent;
    border: none;
    color: var(--accent);
    font-weight: 600;
    font-size: 0.95rem;
    display: flex;
    align-items: center;
    gap: 8px;
    cursor: pointer;
    transition: opacity 0.2s ease;
}}

.card-button:hover {{
    opacity: 0.7;
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
    <div class="card">
        <div class="card-icon">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/>
            </svg>
        </div>
        <h2 class="card-title">{title_text}</h2>
        <p class="card-body">{body_text}</p>
        <button class="card-button">
            Learn more
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <line x1="5" y1="12" x2="19" y2="12"></line>
                <polyline points="12 5 19 12 12 19"></polyline>
            </svg>
        </button>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Pure CSS is handling the visual complexity (masks, blurs, and hover states).
// Minimal JS included to handle potential data interactions.
document.addEventListener('DOMContentLoaded', () => {{
    const card = document.querySelector('.card');
    const button = document.querySelector('.card-button');
    
    button.addEventListener('click', (e) => {{
        e.stopPropagation(); // Prevent card click event if button is clicked
        console.log('Action initiated');
    }});

    card.addEventListener('click', () => {{
        console.log('Card clicked');
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
