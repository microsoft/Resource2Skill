def create_component(
    output_dir: str,
    title_text: str = "Powerful Features",
    body_text: str = "Everything you need, perfectly arranged.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#6366f1",     # CSS hex color for accent (Indigo)
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Responsive Bento Grid Layout.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors ===
    if color_scheme == "dark":
        bg_color = "#090a0f"
        text_primary = "#f3f4f6"
        text_secondary = "#9ca3af"
        card_bg = "rgba(255, 255, 255, 0.03)"
        card_border = "rgba(255, 255, 255, 0.08)"
        card_hover = "rgba(255, 255, 255, 0.06)"
        shadow = "0 8px 32px rgba(0, 0, 0, 0.4)"
    else:
        bg_color = "#f9fafb"
        text_primary = "#111827"
        text_secondary = "#4b5563"
        card_bg = "#ffffff"
        card_border = "rgba(0, 0, 0, 0.08)"
        card_hover = "#f3f4f6"
        shadow = "0 8px 32px rgba(0, 0, 0, 0.06)"

    # === CSS ===
    css = f"""/* Responsive Bento Grid Layout */
:root {{
    --bg-color: {bg_color};
    --text-primary: {text_primary};
    --text-secondary: {text_secondary};
    --accent-color: {accent_color};
    --card-bg: {card_bg};
    --card-border: {card_border};
    --card-hover: {card_hover};
    --shadow: {shadow};
    --max-width: {width_px}px;
}}

* {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background-color: var(--bg-color);
    color: var(--text-primary);
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 4rem 2rem;
    line-height: 1.5;
}}

.header {{
    text-align: center;
    margin-bottom: 3rem;
    max-width: 600px;
}}

.header h1 {{
    font-size: 2.5rem;
    font-weight: 700;
    margin-bottom: 1rem;
    letter-spacing: -0.02em;
}}

.header p {{
    color: var(--text-secondary);
    font-size: 1.125rem;
}}

/* BENTO GRID CORE LOGIC */
.bento-grid {{
    display: grid;
    width: 100%;
    max-width: var(--max-width);
    /* Desktop: 4 columns, 2 rows */
    grid-template-columns: repeat(4, 1fr);
    grid-template-rows: repeat(2, 300px);
    gap: 1.5rem;
    
    /* The Magic String Array defining the layout */
    grid-template-areas: 
        "box1 box1 box2 box3"
        "box1 box1 box4 box5";
}}

/* Assigning elements to areas */
.box-1 {{ grid-area: box1; }}
.box-2 {{ grid-area: box2; }}
.box-3 {{ grid-area: box3; }}
.box-4 {{ grid-area: box4; }}
.box-5 {{ grid-area: box5; }}

/* Card Aesthetics */
.bento-card {{
    background: var(--card-bg);
    border: 1px solid var(--card-border);
    border-radius: 24px;
    padding: 2rem;
    display: flex;
    flex-direction: column;
    position: relative;
    overflow: hidden;
    transition: transform 0.3s ease, background 0.3s ease, box-shadow 0.3s ease;
    box-shadow: var(--shadow);
    
    /* Animation initial state */
    opacity: 0;
    transform: translateY(20px);
}}

.bento-card.visible {{
    opacity: 1;
    transform: translateY(0);
}}

.bento-card:hover {{
    transform: translateY(-4px);
    background: var(--card-hover);
}}

/* Card Content Styling */
.card-icon {{
    width: 48px;
    height: 48px;
    border-radius: 12px;
    background: color-mix(in srgb, var(--accent-color) 20%, transparent);
    color: var(--accent-color);
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 1.5rem;
}}

.card-icon svg {{
    width: 24px;
    height: 24px;
}}

.bento-card h3 {{
    font-size: 1.25rem;
    font-weight: 600;
    margin-bottom: 0.5rem;
}}

.bento-card p {{
    color: var(--text-secondary);
    font-size: 0.95rem;
    flex-grow: 1;
}}

/* Specialty styling for the large hero box */
.box-1 h3 {{
    font-size: 2rem;
    margin-bottom: 1rem;
}}
.box-1 p {{
    font-size: 1.1rem;
}}
.box-1 .card-icon {{
    width: 64px;
    height: 64px;
}}
.box-1 .card-icon svg {{
    width: 32px;
    height: 32px;
}}

/* Tablet Breakpoint */
@media (max-width: 992px) {{
    .bento-grid {{
        grid-template-columns: repeat(2, 1fr);
        grid-template-rows: auto;
        /* Restack for medium screens */
        grid-template-areas: 
            "box1 box1"
            "box1 box1"
            "box2 box3"
            "box4 box5";
    }}
    .bento-card {{
        min-height: 250px;
    }}
}}

/* Mobile Breakpoint */
@media (max-width: 600px) {{
    .bento-grid {{
        grid-template-columns: 1fr;
        /* Restack to a single column */
        grid-template-areas: 
            "box1"
            "box2"
            "box3"
            "box4"
            "box5";
    }}
    
    .header h1 {{ font-size: 2rem; }}
}}
"""

    # === HTML ===
    # Using inline SVGs for self-contained, immediate rendering
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text} - Bento Grid</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    
    <div class="header">
        <h1>{title_text}</h1>
        <p>{body_text}</p>
    </div>

    <div class="bento-grid">
        
        <div class="bento-card box-1">
            <div class="card-icon">
                <svg fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path></svg>
            </div>
            <h3>Lightning Fast Performance</h3>
            <p>Our completely overhauled engine processes data at the edge, reducing latency by 85% compared to traditional architectures. Experience real-time feedback with every interaction.</p>
        </div>

        <div class="bento-card box-2">
            <div class="card-icon">
                <svg fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"></path></svg>
            </div>
            <h3>Bank-Grade Security</h3>
            <p>End-to-end encryption keeping your data locked down tight.</p>
        </div>

        <div class="bento-card box-3">
            <div class="card-icon">
                <svg fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12"></path></svg>
            </div>
            <h3>Seamless Sync</h3>
            <p>Work offline, and we'll resolve conflicts automatically when you reconnect.</p>
        </div>

        <div class="bento-card box-4">
            <div class="card-icon">
                <svg fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 3.055A9.001 9.001 0 1020.945 13H11V3.055z"></path><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.488 9H15V3.512A9.025 9.025 0 0120.488 9z"></path></svg>
            </div>
            <h3>Advanced Analytics</h3>
            <p>Turn raw numbers into actionable business intelligence.</p>
        </div>

        <div class="bento-card box-5">
            <div class="card-icon">
                <svg fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"></path></svg>
            </div>
            <h3>Team Collaboration</h3>
            <p>Built-in tools to keep everyone on the exact same page.</p>
        </div>

    </div>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Staggered Entrance Animation via Intersection Observer
document.addEventListener('DOMContentLoaded', () => {{
    const cards = document.querySelectorAll('.bento-card');
    
    const observerOptions = {{
        root: null,
        rootMargin: '0px',
        threshold: 0.1
    }};

    const observer = new IntersectionObserver((entries, observer) => {{
        entries.forEach((entry, index) => {{
            if (entry.isIntersecting) {{
                // Stagger the animation delay based on element index
                setTimeout(() => {{
                    entry.target.classList.add('visible');
                }}, index * 100); // 100ms stagger between cards
                
                // Unobserve after animating once
                observer.unobserve(entry.target);
            }}
        }});
    }}, observerOptions);

    cards.forEach(card => {{
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
