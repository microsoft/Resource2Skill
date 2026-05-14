def create_component(
    output_dir: str,
    title_text: str = "Explore the Wild",
    body_text: str = "A curated collection of nature's most breathtaking moments, arranged in a seamless, interlocking mosaic.",
    color_scheme: str = "dark",
    accent_color: str = "#10b981",
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Responsive CSS Grid Mosaic Gallery.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme ===
    if color_scheme == "dark":
        bg_color = "#0a0a0a"
        text_color = "#f8f9fa"
        surface_color = "rgba(255, 255, 255, 0.04)"
        shadow_color = "rgba(0, 0, 0, 0.5)"
    else:
        bg_color = "#f8f9fa"
        text_color = "#111827"
        surface_color = "rgba(0, 0, 0, 0.04)"
        shadow_color = "rgba(0, 0, 0, 0.1)"

    # === CSS ===
    css = f"""/* Responsive CSS Grid Mosaic Gallery */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --text: {text_color};
    --accent: {accent_color};
    --surface: {surface_color};
    --shadow: {shadow_color};
    --max-width: {width_px}px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background-color: var(--bg);
    color: var(--text);
    min-height: 100vh;
    display: flex;
    justify-content: center;
    padding: 4rem 2rem;
    overflow-x: hidden;
}}

.wrapper {{
    width: 100%;
    max-width: var(--max-width);
}}

/* Typography Header */
.header {{
    text-align: center;
    margin-bottom: 4rem;
}}

.title {{
    font-size: clamp(2.5rem, 5vw, 4rem);
    font-weight: 700;
    letter-spacing: -0.03em;
    margin-bottom: 1rem;
}}

.title span {{
    color: var(--accent);
}}

.body-text {{
    font-size: 1.125rem;
    line-height: 1.6;
    opacity: 0.7;
    max-width: 600px;
    margin: 0 auto;
}}

/* Grid System */
.gallery {{
    display: grid;
    gap: 16px;
    grid-template-columns: repeat(1, 1fr);
    grid-auto-rows: 250px;
    grid-auto-flow: dense; /* Crucial for backfilling empty spaces */
}}

.gallery-item {{
    position: relative;
    border-radius: 16px;
    overflow: hidden;
    cursor: pointer;
    background: var(--surface);
    box-shadow: 0 10px 30px var(--shadow);
    
    /* Animation initial state */
    opacity: 0;
    transform: translateY(30px);
}}

/* Visible state toggled by JS */
.gallery-item.visible {{
    opacity: 1;
    transform: translateY(0);
    transition: opacity 0.8s cubic-bezier(0.16, 1, 0.3, 1), 
                transform 0.8s cubic-bezier(0.16, 1, 0.3, 1);
}}

/* Image Handling */
.gallery-item img {{
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    object-fit: cover;
    transition: transform 0.6s cubic-bezier(0.16, 1, 0.3, 1);
}}

/* Hover interaction */
.gallery-item:hover img {{
    transform: scale(1.08);
}}

.gallery-item::after {{
    content: '';
    position: absolute;
    inset: 0;
    background: linear-gradient(to top, rgba(0,0,0,0.6) 0%, transparent 40%);
    opacity: 0;
    transition: opacity 0.4s ease;
    pointer-events: none;
}}

.gallery-item:hover::after {{
    opacity: 1;
}}

/* Responsive Breakpoints & Mosaic Architecture */

/* Tablet */
@media (min-width: 600px) {{
    .gallery {{
        grid-template-columns: repeat(2, 1fr);
        grid-auto-rows: 220px;
        gap: 20px;
    }}
}}

/* Desktop Mosaic Layout (4 columns) */
@media (min-width: 900px) {{
    .gallery {{
        grid-template-columns: repeat(4, 1fr);
        grid-auto-rows: 180px;
        gap: 24px;
    }}
    
    /* Creating the interlocking pattern using spans.
       With 9 items, this exact sequence perfectly fills a 4x6 grid using dense flow. */
       
    .gallery-item:nth-child(1) {{
        grid-column: span 2;
        grid-row: span 2;
    }}
    
    .gallery-item:nth-child(2) {{
        grid-column: span 1;
        grid-row: span 2;
    }}
    
    /* Item 3 is 1x1 */
    
    .gallery-item:nth-child(4) {{
        grid-row: span 3;
    }}
    
    .gallery-item:nth-child(5) {{
        grid-column: span 2;
        grid-row: span 2;
    }}
    
    .gallery-item:nth-child(6) {{
        grid-column: span 2;
        grid-row: span 2;
    }}
    
    /* Item 7 is 1x1 (will backfill dense gaps) */
    
    .gallery-item:nth-child(8) {{
        grid-column: span 2;
        grid-row: span 2;
    }}
    
    /* Item 9 is 1x1 (will backfill dense gaps) */
}}
"""

    # === HTML ===
    # Using specific curated high-quality nature images from Unsplash to ensure the demo looks premium
    images = [
        "https://images.unsplash.com/photo-1682687220742-aba13b6e50ba?w=800&q=80",
        "https://images.unsplash.com/photo-1506744626753-140294b84b31?w=800&q=80",
        "https://images.unsplash.com/photo-1470071459604-3b5ec3a7fe05?w=800&q=80",
        "https://images.unsplash.com/photo-1441974231531-c6227db76b6e?w=800&q=80",
        "https://images.unsplash.com/photo-1433086966358-54859d0ed716?w=800&q=80",
        "https://images.unsplash.com/photo-1472214103451-9374bd1c798e?w=800&q=80",
        "https://images.unsplash.com/photo-1511497584788-876760111969?w=800&q=80",
        "https://images.unsplash.com/photo-1469474968028-56623f02e42e?w=800&q=80",
        "https://images.unsplash.com/photo-1426604966848-d7adac402bff?w=800&q=80"
    ]
    
    # Process title to wrap the last word in a span for the accent color
    title_words = title_text.split()
    if len(title_words) > 1:
        title_html = f"{' '.join(title_words[:-1])} <span>{title_words[-1]}</span>"
    else:
        title_html = f"<span>{title_text}</span>"

    gallery_html = "\n".join([f'            <div class="gallery-item"><img src="{src}" alt="Gallery Image {i+1}"></div>' for i, src in enumerate(images)])

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="wrapper">
        <header class="header">
            <h1 class="title">{title_html}</h1>
            <p class="body-text">{body_text}</p>
        </header>

        <main class="gallery">
{gallery_html}
        </main>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Intersection Observer for scroll-triggered staggered reveal
document.addEventListener('DOMContentLoaded', () => {{
    const galleryItems = document.querySelectorAll('.gallery-item');
    
    const observerOptions = {{
        threshold: 0.15,
        rootMargin: '0px 0px -50px 0px'
    }};

    const observer = new IntersectionObserver((entries) => {{
        entries.forEach(entry => {{
            if (entry.isIntersecting) {{
                // Add visible class to trigger CSS transition
                entry.target.classList.add('visible');
                // Stop observing once revealed
                observer.unobserve(entry.target);
            }}
        }});
    }}, observerOptions);

    // Apply staggered transition delays based on DOM order
    galleryItems.forEach((item, index) => {{
        // Create a repeating stagger pattern (0.0s, 0.1s, 0.2s, 0.3s)
        const delay = (index % 4) * 0.1;
        item.style.transitionDelay = `${{delay}}s, ${{delay}}s`;
        
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
