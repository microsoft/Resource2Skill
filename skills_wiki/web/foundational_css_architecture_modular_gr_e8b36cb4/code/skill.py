def create_component(
    output_dir: str,
    title_text: str = "Foundational CSS Architecture",
    body_text: str = "This interface is built on the six pillars of CSS: Inheritance, The Cascade, Specificity management, the Box Model, Modern Grid Layouts, and Strict Separation of Concerns.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#8b5cf6",     # CSS hex color for accent (Purple)
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the modular, principle-driven CSS architecture.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme ===
    if color_scheme == "dark":
        bg_color = "#0f172a"
        text_color = "#f1f5f9"
        text_muted = "#94a3b8"
        surface_color = "#1e293b"
        border_color = "#334155"
        shadow = "rgba(0, 0, 0, 0.4)"
    else:
        bg_color = "#f8fafc"
        text_color = "#0f172a"
        text_muted = "#64748b"
        surface_color = "#ffffff"
        border_color = "#e2e8f0"
        shadow = "rgba(0, 0, 0, 0.08)"

    # === CSS ===
    css = f"""/* Foundational CSS Architecture */

/* 1. The Box Model Reset */
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
    --width: {width_px}px;
    --height: {height_px}px;
}}

/* 2. Inheritance: Setting base styles to cascade downwards */
body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background-color: var(--bg);
    color: var(--text);
    line-height: 1.6;
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 2rem;
}}

/* Forcing form elements to inherit typography (they resist by default) */
button, input, textarea, select {{
    font: inherit;
}}

.header {{
    text-align: center;
    max-width: 800px;
    margin-bottom: 3rem;
}}

.header h1 {{
    font-size: 2.5rem;
    margin-bottom: 1rem;
    color: var(--accent);
    line-height: 1.2;
}}

.header p {{
    font-size: 1.125rem;
    color: var(--text-muted);
}}

/* 3. Creating Layouts & 4. Separation of Concerns */
/* LAYOUT CLASSES (Prefixed with l- ) - Strictly for structure */
.l-grid {{
    display: grid;
    /* Inherent responsiveness without media queries */
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 2rem;
    width: 100%;
    max-width: var(--width);
}}

/* COMPONENT CLASSES (Prefixed with c- ) - Strictly for visuals */
.c-card {{
    background-color: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 2rem;
    display: flex;
    flex-direction: column;
    box-shadow: 0 4px 6px var(--shadow);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}}

/* 5. Specificity & The Cascade */
/* Keeping specificity low and flat so overrides are easy */
.c-card:hover {{
    transform: translateY(-5px);
    box-shadow: 0 12px 20px var(--shadow);
}}

.c-card h2 {{
    color: var(--text);
    margin-bottom: 0.75rem;
    font-size: 1.25rem;
}}

.c-card p {{
    color: var(--text-muted);
    font-size: 0.95rem;
    margin-bottom: 1.5rem;
    flex-grow: 1; /* Pushes button to bottom */
}}

.c-button {{
    background-color: var(--accent);
    color: #ffffff;
    border: none;
    padding: 0.75rem 1.5rem;
    border-radius: 6px;
    cursor: pointer;
    font-weight: 500;
    transition: filter 0.2s ease;
    align-self: flex-start;
}}

.c-button:hover {{
    filter: brightness(1.15);
}}

/* Utility Class (Highest intent, but low specificity) */
.u-text-accent {{
    color: var(--accent);
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
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    
    <header class="header">
        <h1>{title_text}</h1>
        <p>{body_text}</p>
    </header>

    <!-- Strict separation: .l-grid handles position, children handle their own cosmetics -->
    <main class="l-grid">
        
        <article class="c-card">
            <h2>Inheritance & Box Model</h2>
            <p>Typography naturally flows down from the body element. A universal <code>box-sizing: border-box</code> reset ensures padding mathematically behaves intuitively, never breaking grid boundaries.</p>
            <button class="c-button">Inherited Font</button>
        </article>

        <article class="c-card">
            <h2>Specificity & Cascade</h2>
            <p>We avoid IDs and deep nesting. By keeping CSS selector specificity flat and relying on the source order (cascade), styling conflicts are virtually eliminated.</p>
            <button class="c-button">Flat Hierarchy</button>
        </article>

        <article class="c-card">
            <h2>Layout Separation</h2>
            <p>Layout logic (CSS Grid) is completely isolated from visual styling (backgrounds, borders). This modularity allows structural reuse without visual contamination.</p>
            <button class="c-button">Modular Design</button>
        </article>

    </main>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = """// Foundational CSS Architecture
document.addEventListener('DOMContentLoaded', () => {
    // JavaScript is intentionally kept minimal.
    // The core architecture relies on robust CSS principles (Grid, Box-sizing, Inheritance)
    // rather than JS-driven layout calculations or hardcoded dimensions.
    console.log('CSS Principles Architecture Loaded Successfully.');
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
