def create_component(
    output_dir: str,
    title_text: str = "Latest Arrivals",
    body_text: str = "Explore our dynamically adjusting, auto-wrapping product gallery.",
    color_scheme: str = "dark",
    accent_color: str = "#6366f1",
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Auto-Wrapping Grid with Stacked Overlays.
    
    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os
    import json

    os.makedirs(output_dir, exist_ok=True)

    # Derive theme colors
    if color_scheme == "dark":
        bg_color = "#0d111c"
        text_color = "#f0f0f0"
        surface_color = "#1e2433"
        gradient_base = "rgba(13, 17, 28, 0.95)"
        glass_bg = "rgba(255, 255, 255, 0.1)"
    else:
        bg_color = "#f4f6f8"
        text_color = "#111827"
        surface_color = "#ffffff"
        gradient_base = "rgba(0, 0, 0, 0.85)"
        glass_bg = "rgba(0, 0, 0, 0.4)"

    # JSON data for the dynamic grid items
    cards_data = [
        {"title": "Lunar Stride X", "price": "$120.00", "badge": "New", "img": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?auto=format&fit=crop&w=600&q=80"},
        {"title": "Aero Glide Pro", "price": "$145.00", "badge": "", "img": "https://images.unsplash.com/photo-1608231387042-66d1773070a5?auto=format&fit=crop&w=600&q=80"},
        {"title": "Nova Dash 3", "price": "$95.00", "badge": "Sale", "img": "https://images.unsplash.com/photo-1595950653106-6c9ebd614d3a?auto=format&fit=crop&w=600&q=80"},
        {"title": "Velocity React", "price": "$180.00", "badge": "Popular", "img": "https://images.unsplash.com/photo-1605348532760-6753d2c43329?auto=format&fit=crop&w=600&q=80"},
        {"title": "Apex Trainer", "price": "$110.00", "badge": "", "img": "https://images.unsplash.com/photo-1511556532299-8f662fc26c06?auto=format&fit=crop&w=600&q=80"},
        {"title": "Quantum Shift", "price": "$200.00", "badge": "Limited", "img": "https://images.unsplash.com/photo-1579338559194-a162d19bf842?auto=format&fit=crop&w=600&q=80"}
    ]

    css = f"""/* Auto-Wrapping Grid Component */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --text: {text_color};
    --surface: {surface_color};
    --accent: {accent_color};
    --gradient-base: {gradient_base};
    --glass-bg: {glass_bg};
    --max-width: {width_px}px;
    --min-height: {height_px}px;
}}

body {{
    font-family: 'Inter', sans-serif;
    background-color: var(--bg);
    color: var(--text);
    display: flex;
    justify-content: center;
    min-height: 100vh;
    padding: 2rem;
    -webkit-font-smoothing: antialiased;
}}

.app-wrapper {{
    width: 100%;
    max-width: var(--max-width);
    min-height: var(--min-height);
    display: flex;
    flex-direction: column;
    gap: 2.5rem;
}}

.header {{
    text-align: center;
    margin-bottom: 1rem;
}}

.header h1 {{
    font-size: 2.5rem;
    font-weight: 700;
    margin-bottom: 0.75rem;
    letter-spacing: -0.02em;
}}

.header p {{
    font-size: 1.125rem;
    opacity: 0.8;
    max-width: 600px;
    margin: 0 auto;
}}

/* MACRO LAYOUT: The Auto-Wrapping Grid */
.product-grid {{
    display: grid;
    /* The Magic Line: Fluid wrapping without media queries */
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 2rem;
    width: 100%;
}}

/* MICRO LAYOUT: Grid Stacking */
.card {{
    display: grid;
    /* Single area defining the stack */
    grid-template-areas: "stack";
    background-color: var(--surface);
    border-radius: 16px;
    overflow: hidden;
    cursor: pointer;
    box-shadow: 0 10px 20px rgba(0,0,0,0.05);
    transition: transform 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94),
                box-shadow 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94);
    
    /* For entrance animation */
    opacity: 0;
    transform: translateY(30px);
}}

.card.visible {{
    opacity: 1;
    transform: translateY(0);
}}

.card:hover {{
    transform: translateY(-8px);
    box-shadow: 0 20px 40px rgba(0,0,0,0.12);
}}

/* All direct children share the same grid area to overlap */
.card > * {{
    grid-area: stack;
}}

/* Image Layer */
.card-img {{
    width: 100%;
    height: 380px;
    object-fit: cover;
    transition: transform 0.6s cubic-bezier(0.25, 0.46, 0.45, 0.94);
}}

.card:hover .card-img {{
    transform: scale(1.08);
}}

/* Gradient Overlay Layer */
.card-gradient {{
    background: linear-gradient(to top, var(--gradient-base) 0%, transparent 60%);
    width: 100%;
    height: 100%;
    z-index: 1;
}}

/* Content Layer (Aligned Bottom-Left) */
.card-content {{
    place-self: end start;
    padding: 1.5rem;
    z-index: 2;
    color: #ffffff; /* Forcing white for contrast over gradient */
    width: 100%;
}}

.card-title {{
    font-size: 1.25rem;
    font-weight: 600;
    margin-bottom: 0.25rem;
}}

.card-price {{
    font-size: 1rem;
    font-weight: 500;
    color: var(--accent);
    filter: brightness(1.2);
}}

/* Badge Layer (Aligned Top-Right) */
.card-badge {{
    place-self: start end;
    margin: 1.25rem;
    padding: 0.35rem 0.85rem;
    background: var(--glass-bg);
    backdrop-filter: blur(8px);
    -webkit-backdrop-filter: blur(8px);
    color: #ffffff;
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    border-radius: 999px;
    z-index: 3;
    border: 1px solid rgba(255,255,255,0.2);
}}
"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text}</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <main class="app-wrapper">
        <header class="header">
            <h1>{title_text}</h1>
            <p>{body_text}</p>
        </header>

        <div class="product-grid" id="grid">
            <!-- Cards injected via JavaScript -->
        </div>
    </main>

    <script id="card-data" type="application/json">
        {json.dumps(cards_data)}
    </script>
    <script src="script.js"></script>
</body>
</html>"""

    js = f"""// Grid Auto-Wrapping & Intersection Observer logic
document.addEventListener('DOMContentLoaded', () => {{
    const gridContainer = document.getElementById('grid');
    const cardData = JSON.parse(document.getElementById('card-data').textContent);

    // 1. Render Cards using Grid Stacking Pattern
    cardData.forEach((item, index) => {{
        const card = document.createElement('article');
        card.className = 'card';
        card.style.transitionDelay = `${{(index % 3) * 0.1}}s`; // Staggered delay logic
        
        let badgeHTML = item.badge 
            ? `<div class="card-badge">${{item.badge}}</div>` 
            : '';

        card.innerHTML = `
            <img class="card-img" src="${{item.img}}" alt="${{item.title}}" loading="lazy">
            <div class="card-gradient"></div>
            <div class="card-content">
                <h3 class="card-title">${{item.title}}</h3>
                <p class="card-price">${{item.price}}</p>
            </div>
            ${{badgeHTML}}
        `;
        gridContainer.appendChild(card);
    }});

    // 2. Intersection Observer for Scroll Animations
    const observerOptions = {{
        root: null,
        rootMargin: '0px',
        threshold: 0.1
    }};

    const observer = new IntersectionObserver((entries, obs) => {{
        entries.forEach(entry => {{
            if (entry.isIntersecting) {{
                // Request animation frame ensures the transition triggers smoothly
                requestAnimationFrame(() => {{
                    entry.target.classList.add('visible');
                    // Remove transition delay after entrance so hover effects are instant
                    setTimeout(() => {{
                        entry.target.style.transitionDelay = '0s';
                    }}, 600);
                }});
                obs.unobserve(entry.target);
            }}
        }});
    }}, observerOptions);

    // Observe all generated cards
    document.querySelectorAll('.card').forEach(card => {{
        observer.observe(card);
    }});
}});
"""

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
