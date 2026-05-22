def create_component(
    output_dir: str,
    title_text: str = "Bento Grid System",
    body_text: str = "A highly responsive, asymmetrical grid layout using modern CSS Grid Area matrices and Grid Stacking for effortless layering.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#8b5cf6",     # CSS hex color for accent (e.g., Violet)
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Bento Grid and Grid Stacking visual effects.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors ===
    if color_scheme == "dark":
        bg_color = "#09090b"
        text_color = "#fafafa"
        text_muted = "#a1a1aa"
        surface_color = "#18181b"
        border_color = "rgba(255, 255, 255, 0.08)"
        shadow = "0 10px 30px -10px rgba(0,0,0,0.5)"
    else:
        bg_color = "#f4f4f5"
        text_color = "#09090b"
        text_muted = "#52525b"
        surface_color = "#ffffff"
        border_color = "rgba(0, 0, 0, 0.08)"
        shadow = "0 10px 30px -10px rgba(0,0,0,0.05)"

    # === CSS ===
    css = f"""/* Responsive Bento Grid & Grid Stacking — generated component */
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

*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background: var(--bg);
    color: var(--text);
    min-height: var(--min-height);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 4rem 2rem;
    overflow-x: hidden;
}}

.header {{
    text-align: center;
    max-width: 600px;
    margin-bottom: 3rem;
}}

.header h1 {{
    font-size: 2.5rem;
    font-weight: 700;
    letter-spacing: -0.02em;
    margin-bottom: 1rem;
}}

.header p {{
    font-size: 1.125rem;
    color: var(--text-muted);
    line-height: 1.6;
}}

/* --- Bento Grid Layout System --- */
.bento-container {{
    width: 100%;
    max-width: var(--max-width);
    display: grid;
    /* Desktop layout: 4 columns, auto rows */
    grid-template-columns: repeat(4, 1fr);
    grid-auto-rows: minmax(220px, auto);
    gap: 1.5rem;
    
    /* The Magic String Matrix */
    grid-template-areas: 
        "box-1 box-1 box-2 box-3"
        "box-1 box-1 box-4 box-5";
}}

/* Grid Item Base Styling */
.bento-item {{
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 24px;
    padding: 2rem;
    display: flex;
    flex-direction: column;
    justify-content: flex-end;
    align-items: flex-start;
    position: relative;
    overflow: hidden;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
    transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1), box-shadow 0.3s ease;
    opacity: 0;
    transform: translateY(20px);
}}

.bento-item.visible {{
    opacity: 1;
    transform: translateY(0);
}}

.bento-item:hover {{
    transform: translateY(-6px);
    box-shadow: var(--shadow);
}}

/* Map elements to grid areas */
.box-1 {{ grid-area: box-1; min-height: 400px; }}
.box-2 {{ grid-area: box-2; }}
.box-3 {{ grid-area: box-3; }}
.box-4 {{ grid-area: box-4; }}
.box-5 {{ grid-area: box-5; }}

/* --- Grid Stacking Technique (Hero Card) --- */
/* Overlapping elements without position:absolute */
.grid-stack {{
    display: grid;
    padding: 0; /* Let children handle padding to reach edges */
}}

.grid-stack > * {{
    /* Put all children into row 1, column 1 so they stack perfectly */
    grid-area: 1 / 1;
}}

.grid-stack .background-layer {{
    width: 100%;
    height: 100%;
    background: linear-gradient(135deg, var(--accent), #ec4899);
    opacity: 0.15;
    transition: opacity 0.4s ease;
}}

.grid-stack:hover .background-layer {{
    opacity: 0.3;
}}

.grid-stack .content-layer {{
    padding: 2.5rem;
    display: flex;
    flex-direction: column;
    justify-content: flex-end;
    z-index: 1; /* Ensure text stays on top */
}}

/* Typography inside cards */
.icon-wrapper {{
    width: 48px;
    height: 48px;
    border-radius: 12px;
    background: rgba(139, 92, 246, 0.15);
    color: var(--accent);
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: auto; /* Pushes content down */
}}

.icon-wrapper svg {{
    width: 24px;
    height: 24px;
}}

.bento-item h3 {{
    font-size: 1.25rem;
    font-weight: 600;
    margin-bottom: 0.5rem;
    letter-spacing: -0.01em;
}}

.box-1 h3 {{
    font-size: 2rem;
    margin-bottom: 1rem;
}}

.bento-item p {{
    color: var(--text-muted);
    font-size: 0.95rem;
    line-height: 1.5;
}}

/* --- Responsive Media Queries --- */
/* Tablet */
@media (max-width: 968px) {{
    .bento-container {{
        grid-template-columns: repeat(3, 1fr);
        grid-template-areas: 
            "box-1 box-1 box-2"
            "box-1 box-1 box-3"
            "box-4 box-5 box-5";
    }}
    .box-1 {{ min-height: 350px; }}
}}

/* Mobile Large */
@media (max-width: 768px) {{
    .bento-container {{
        grid-template-columns: repeat(2, 1fr);
        grid-template-areas: 
            "box-1 box-1"
            "box-1 box-1"
            "box-2 box-3"
            "box-4 box-4"
            "box-5 box-5";
    }}
}}

/* Mobile Small */
@media (max-width: 480px) {{
    .bento-container {{
        grid-template-columns: 1fr;
        grid-template-areas: 
            "box-1"
            "box-2"
            "box-3"
            "box-4"
            "box-5";
    }}
    .box-1 {{ min-height: 300px; }}
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
    
    <div class="header">
        <h1>{title_text}</h1>
        <p>{body_text}</p>
    </div>

    <div class="bento-container" id="bentoGrid">
        
        <!-- Box 1: Hero Card showcasing Grid Stacking -->
        <article class="bento-item box-1 grid-stack">
            <div class="background-layer"></div>
            <div class="content-layer">
                <div class="icon-wrapper">
                    <svg fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 5a1 1 0 011-1h14a1 1 0 011 1v2a1 1 0 01-1 1H5a1 1 0 01-1-1V5zM4 13a1 1 0 011-1h6a1 1 0 011 1v6a1 1 0 01-1 1H5a1 1 0 01-1-1v-6zM16 13a1 1 0 011-1h2a1 1 0 011 1v6a1 1 0 01-1 1h-2a1 1 0 01-1-1v-6z"></path></svg>
                </div>
                <h3>Grid Stacking Technique</h3>
                <p>By applying <code>display: grid</code> to a container and setting its children to <code>grid-area: 1 / 1</code>, we overlay elements natively without the structural collapse of absolute positioning. This background gradient and text are stacked in the same cell.</p>
            </div>
        </article>

        <!-- Box 2 -->
        <article class="bento-item box-2">
            <div class="icon-wrapper">
                <svg fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 18h.01M8 21h8a2 2 0 002-2V5a2 2 0 00-2-2H8a2 2 0 00-2 2v14a2 2 0 002 2z"></path></svg>
            </div>
            <h3>Responsive</h3>
            <p>Adapts fluidly. Resize the window to see template areas shift seamlessly.</p>
        </article>

        <!-- Box 3 -->
        <article class="bento-item box-3">
            <div class="icon-wrapper">
                <svg fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path></svg>
            </div>
            <h3>Performance</h3>
            <p>Utilizes raw CSS layout engines. Zero reflow lag via JS window measuring.</p>
        </article>

        <!-- Box 4 -->
        <article class="bento-item box-4">
            <div class="icon-wrapper">
                <svg fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2V6zM14 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V6zM4 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2v-2zM14 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z"></path></svg>
            </div>
            <h3>Template Matrices</h3>
            <p>The power of ASCII art in CSS. Visual strings define complex 2D spatial relationships.</p>
        </article>

        <!-- Box 5 -->
        <article class="bento-item box-5">
            <div class="icon-wrapper">
                <svg fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 21a4 4 0 01-4-4V5a2 2 0 012-2h4a2 2 0 012 2v12a4 4 0 01-4 4zm0 0h12a2 2 0 002-2v-4a2 2 0 00-2-2h-2.343M11 7.343l1.657-1.657a2 2 0 012.828 0l2.829 2.829a2 2 0 010 2.828l-8.486 8.485M7 17h.01"></path></svg>
            </div>
            <h3>Visual Hierarchy</h3>
            <p>Naturally draws the user's eye across varying box weights and proportions.</p>
        </article>

    </div>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Staggered Reveal Animation for Bento Grid Items
document.addEventListener('DOMContentLoaded', () => {{
    const bentoItems = document.querySelectorAll('.bento-item');
    
    // Intersection Observer to detect when items enter the viewport
    const observerOptions = {{
        root: null,
        rootMargin: '0px',
        threshold: 0.15
    }};
    
    const observer = new IntersectionObserver((entries, observer) => {{
        entries.forEach((entry, index) => {{
            if (entry.isIntersecting) {{
                // Apply a staggered delay based on the index
                // Wait a small amount of time per element to create a cascade effect
                setTimeout(() => {{
                    entry.target.classList.add('visible');
                }}, index * 100);
                
                // Unobserve once revealed
                observer.unobserve(entry.target);
            }}
        }});
    }}, observerOptions);
    
    bentoItems.forEach(item => {{
        observer.observe(item);
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
