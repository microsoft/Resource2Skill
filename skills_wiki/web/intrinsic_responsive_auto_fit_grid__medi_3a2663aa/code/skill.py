def create_component(
    output_dir: str,
    title_text: str = "Responsive Auto-Fit Grid",
    body_text: str = "Resize the window to see the cards automatically wrap and resize without media queries.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#00bfff",     # CSS hex color for accent
    width_px: int = 1200,              # Max width of the container
    height_px: int = 800,              # Min height
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the intrinsic responsive auto-fit grid.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors ===
    if color_scheme == "dark":
        bg_color = "#0a0c10"
        text_color = "#f0f6fc"
        text_muted = "#8b949e"
        surface_color = "rgba(255, 255, 255, 0.03)"
        border_color = "rgba(255, 255, 255, 0.08)"
        shadow = "0 8px 24px rgba(0,0,0,0.4)"
    else:
        bg_color = "#f6f8fa"
        text_color = "#1F2328"
        text_muted = "#656d76"
        surface_color = "#ffffff"
        border_color = "rgba(31, 35, 40, 0.15)"
        shadow = "0 4px 12px rgba(0,0,0,0.05)"

    # Generate Card HTML dynamically
    cards_html = ""
    for i in range(1, 9):
        cards_html += f"""
        <div class="grid-card">
            <div class="card-icon" style="color: var(--accent);">0{i}</div>
            <h3 class="card-title">Grid Item {i}</h3>
            <p class="card-desc">This is a flexible card. It will automatically stretch to fill 1 fraction of the available space, but will never shrink below 280px.</p>
        </div>"""

    # === CSS ===
    css = f"""/* Intrinsic Responsive Auto-Fit Grid */
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
    --border: {border_color};
    --shadow: {shadow};
    --max-width: {width_px}px;
    --min-height: {height_px}px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background: var(--bg);
    color: var(--text);
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 3rem 1.5rem;
}}

.header {{
    text-align: center;
    max-width: 600px;
    margin-bottom: 3rem;
}}

.header h1 {{
    font-size: 2.5rem;
    font-weight: 700;
    letter-spacing: -0.03em;
    margin-bottom: 1rem;
}}

.header p {{
    color: var(--text-muted);
    line-height: 1.6;
    font-size: 1.1rem;
}}

/* --- THE CORE SKILL: AUTO-FIT GRID --- */
.auto-grid {{
    width: 100%;
    max-width: var(--max-width);
    
    /* Enable Grid */
    display: grid;
    
    /* Standardize spacing between rows and columns */
    gap: 1.5rem;
    
    /* 
       THE MAGIC FORMULA:
       repeat()   - Repeat the following pattern
       auto-fit   - Create as many tracks as will fit in the container
       minmax()   - Cards must be >= 280px wide, and stretch up to 1fr (1 fraction of remaining space)
    */
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
}}

/* Card Styling */
.grid-card {{
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 2rem;
    display: flex;
    flex-direction: column;
    gap: 1rem;
    transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1), 
                box-shadow 0.3s cubic-bezier(0.4, 0, 0.2, 1),
                border-color 0.3s ease;
    box-shadow: var(--shadow);
    
    /* Initial state for JS animation */
    opacity: 0;
    transform: translateY(20px);
}}

.grid-card:hover {{
    transform: translateY(-6px);
    box-shadow: 0 12px 32px rgba(0,0,0,0.15);
    border-color: var(--accent);
}}

.card-icon {{
    font-size: 1.5rem;
    font-weight: 700;
    background: color-mix(in srgb, var(--accent) 15%, transparent);
    width: 48px;
    height: 48px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 12px;
}}

.card-title {{
    font-size: 1.25rem;
    font-weight: 600;
}}

.card-desc {{
    color: var(--text-muted);
    line-height: 1.6;
    font-size: 0.95rem;
}}

/* Animation classes applied by JS */
.grid-card.is-visible {{
    opacity: 1;
    transform: translateY(0);
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
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <header class="header">
        <h1>{title_text}</h1>
        <p>{body_text}</p>
    </header>

    <main class="auto-grid">
        {cards_html}
    </main>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Staggered Entrance Animation for Grid Items
document.addEventListener('DOMContentLoaded', () => {{
    const cards = document.querySelectorAll('.grid-card');
    
    // Create an intersection observer to detect when cards enter the viewport
    const observer = new IntersectionObserver((entries) => {{
        entries.forEach(entry => {{
            if (entry.isIntersecting) {{
                // Add the visible class to trigger the CSS transition
                entry.target.classList.add('is-visible');
                // Unobserve once animated in
                observer.unobserve(entry.target);
            }}
        }});
    }}, {{
        threshold: 0.1, // Trigger when 10% of the card is visible
        rootMargin: "0px 0px -50px 0px" // Trigger slightly before it hits the bottom
    }});

    // Apply staggered transition delays based on index, then observe
    cards.forEach((card, index) => {{
        // Calculate a staggered delay (max out at 500ms so it doesn't take too long)
        const delay = Math.min(index * 75, 500); 
        card.style.transitionDelay = `${{delay}}ms`;
        
        observer.observe(card);
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
