def create_component(
    output_dir: str,
    title_text: str = "Build Your Dream Website Easily & Quickly",
    body_text: str = "Unlock the Power of Creativity with Our design and tools. Don't wait. Try Now!",
    color_scheme: str = "dark",        # "dark" produces deep vibrant colors, "light" softer vibrant colors
    accent_color: str = "#facc15",     # CSS hex color for accent (Tailwind yellow-400)
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Responsive Gradient Hero Section.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors based on scheme ===
    if color_scheme == "dark":
        grad_start = "#3b82f6" # blue-500
        grad_mid = "#9333ea"   # purple-600
        grad_end = "#4338ca"   # indigo-700
        text_color = "#ffffff"
        text_muted = "#e5e7eb" # gray-200
        btn_text_dark = "#111827" # gray-900
    else:
        # A softer, brighter gradient for a "light" theme interpretation,
        # but maintaining white text for the classic hero look.
        grad_start = "#60a5fa" # blue-400
        grad_mid = "#c084fc"   # purple-400
        grad_end = "#818cf8"   # indigo-400
        text_color = "#ffffff"
        text_muted = "#f3f4f6"
        btn_text_dark = "#111827"

    # === CSS ===
    css = f"""/* Responsive Gradient Hero Section */
:root {{
    --grad-start: {grad_start};
    --grad-mid: {grad_mid};
    --grad-end: {grad_end};
    --text-primary: {text_color};
    --text-muted: {text_muted};
    --accent: {accent_color};
    --btn-text-dark: {btn_text_dark};
    --container-width: {width_px}px;
    --container-height: {height_px}px;
}}

* {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background-color: #000; /* Fallback */
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 100vh;
}}

.hero-container {{
    width: 100%;
    max-width: var(--container-width);
    height: var(--container-height);
    background: linear-gradient(to right, var(--grad-start), var(--grad-mid), var(--grad-end));
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    padding: 2rem 1.5rem;
    position: relative;
    overflow: hidden;
}}

.hero-content {{
    max-width: 800px;
    z-index: 10;
}}

.hero-title {{
    color: var(--text-primary);
    font-size: clamp(2.5rem, 5vw, 4rem);
    font-weight: 800;
    line-height: 1.1;
    margin-bottom: 1.5rem;
    letter-spacing: -0.02em;
}}

.hero-title .highlight {{
    color: var(--accent);
    display: inline-block;
    margin-top: 0.25rem;
}}

.hero-description {{
    color: var(--text-muted);
    font-size: clamp(1rem, 2vw, 1.25rem);
    font-weight: 400;
    max-width: 600px;
    margin: 0 auto 2.5rem auto;
    line-height: 1.6;
}}

.hero-actions {{
    display: flex;
    gap: 1rem;
    justify-content: center;
    flex-wrap: wrap;
}}

.btn {{
    display: inline-flex;
    align-items: center;
    justify-content: center;
    padding: 0.75rem 2rem;
    border-radius: 9999px; /* Fully rounded */
    font-size: 1.125rem;
    font-weight: 600;
    text-decoration: none;
    transition: all 0.2s ease-in-out;
    cursor: pointer;
}}

.btn-primary {{
    background-color: var(--accent);
    color: var(--btn-text-dark);
    border: 2px solid var(--accent);
}}

.btn-primary:hover {{
    filter: brightness(0.9);
    transform: translateY(-2px);
}}

.btn-secondary {{
    background-color: transparent;
    color: var(--text-primary);
    border: 2px solid var(--text-primary);
}}

.btn-secondary:hover {{
    background-color: var(--text-primary);
    color: var(--btn-text-dark);
    transform: translateY(-2px);
}}

@media (max-width: 640px) {{
    .hero-actions {{
        flex-direction: column;
        width: 100%;
        max-width: 300px;
        margin: 0 auto;
    }}
    .btn {{
        width: 100%;
    }}
}}
"""

    # === HTML ===
    # Using JS to safely inject text and handle the highlight logic
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Responsive Hero Section</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="hero-container">
        <div class="hero-content">
            <!-- Title populated by JS to apply highlight styling -->
            <h1 class="hero-title" id="dynamic-title" data-raw-title="{title_text}"></h1>
            
            <p class="hero-description">{body_text}</p>
            
            <div class="hero-actions">
                <a href="#" class="btn btn-primary">Get Started</a>
                <a href="#" class="btn btn-secondary">Learn More</a>
            </div>
        </div>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Dynamic text highlighting logic
document.addEventListener('DOMContentLoaded', () => {{
    const titleEl = document.getElementById('dynamic-title');
    const rawText = titleEl.getAttribute('data-raw-title');
    
    if (rawText) {{
        // Split words to highlight the last two, mimicking the tutorial's visual structure
        const words = rawText.trim().split(' ');
        
        if (words.length >= 3) {{
            const highlightWords = words.splice(-2).join(' '); // Take last 2 words
            const mainWords = words.join(' ');
            
            // Reconstruct HTML with a line break and span
            titleEl.innerHTML = `${{mainWords}}<br/><span class="highlight">${{highlightWords}}</span>`;
        }} else {{
            // Fallback if title is very short
            titleEl.textContent = rawText;
        }}
    }}
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
