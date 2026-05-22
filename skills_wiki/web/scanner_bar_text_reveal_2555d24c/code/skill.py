def create_component(
    output_dir: str,
    title_text: str = "REVEAL TEXT",
    body_text: str = "A cinematic scanning bar text reveal effect driven purely by CSS background clipping.",
    color_scheme: str = "dark",        
    accent_color: str = "#ffffff",     
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Scanner Bar Text Reveal visual effect.
    
    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme ===
    if color_scheme == "dark":
        bg_color = "#0a0a10"
        text_color = "#a0a0b0"
    else:
        bg_color = "#f4f4f8"
        text_color = "#4a4a50"
        # If light mode and white accent is requested, fall back to a dark accent for visibility
        if accent_color.lower() in ["#fff", "#ffffff", "white"]:
            accent_color = "#111111"

    # === CSS ===
    css = f"""/* Scanner Bar Text Reveal */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --text: {text_color};
    --accent: {accent_color};
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
    overflow-x: hidden;
}}

.container {{
    width: var(--width);
    height: var(--height);
    max-width: 100vw;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    padding: 2rem;
}}

.reveal-text {{
    font-size: clamp(3rem, 10vw, 8rem);
    font-weight: 900;
    line-height: 1.1;
    letter-spacing: -0.02em;
    text-transform: uppercase;
    color: var(--accent); /* Fallback for unsupported browsers */
    margin-bottom: 1.5rem;
}}

.body-text {{
    font-size: 1.25rem;
    line-height: 1.6;
    max-width: 600px;
    opacity: 0;
    transform: translateY(20px);
    transition: opacity 0.8s ease, transform 0.8s ease;
}}

/* Only apply complex animation if background-clip: text is supported */
@supports (-webkit-background-clip: text) or (background-clip: text) {{
    .reveal-text {{
        color: transparent;
        /* Use a solid linear gradient as a scalable background block */
        background-image: linear-gradient(var(--accent), var(--accent));
        background-repeat: no-repeat;
        
        /* Set initial state to invisible */
        background-size: 100% 0%;
        background-position-y: 0%;
        
        -webkit-background-clip: text;
        background-clip: text;
    }}
    
    .reveal-text.animate {{
        animation: reveal-background 2s ease-in-out forwards;
    }}
}}

/* Fade in the body text after the title animation completes */
.body-text.animate {{
    opacity: 1;
    transform: translateY(0);
    transition-delay: 1.5s; /* Align with the ending phase of the text reveal */
}}

/* The Core Scanning Bar Keyframes */
@keyframes reveal-background {{
    0% {{
        background-size: 100% 0%;
        background-position-y: 0%;
    }}
    10% {{
        background-size: 100% 15%; /* Expands to a 15% high horizontal bar */
        background-position-y: 0%;
    }}
    35%, 45% {{
        background-size: 100% 15%;
        background-position-y: 100%; /* Sweeps down to the bottom */
    }}
    70% {{
        background-size: 100% 15%;
        background-position-y: 0%; /* Sweeps back up to the top */
    }}
    100% {{
        background-size: 100% 100%; /* Expands to completely fill the text */
        background-position-y: 0%;
    }}
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
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;900&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        <h1 class="reveal-text">{title_text}</h1>
        <p class="body-text">{body_text}</p>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Scanner Bar Text Reveal - Orchestration
document.addEventListener('DOMContentLoaded', () => {{
    const observerOptions = {{
        root: null,
        rootMargin: '0px',
        threshold: 0.2 // Trigger when 20% of the element is visible
    }};

    const observer = new IntersectionObserver((entries) => {{
        entries.forEach(entry => {{
            if (entry.isIntersecting) {{
                // Add class to trigger CSS animation
                entry.target.classList.add('animate');
                // Stop observing once the animation has been triggered
                observer.unobserve(entry.target);
            }}
        }});
    }}, observerOptions);

    // Observe both the title and the body text
    const animatedElements = document.querySelectorAll('.reveal-text, .body-text');
    animatedElements.forEach(el => observer.observe(el));
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
