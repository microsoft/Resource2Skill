def create_component(
    output_dir: str,
    title_text: str = "Our Impact in Numbers",
    body_text: str = "See how we're making a difference every single day.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#18f98f",     # CSS hex color for accent
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Animated Number Counter Cards.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme ===
    if color_scheme == "dark":
        bg_color = "#121317"
        surface_color = "#21242b"
        text_primary = "#ffffff"
        text_secondary = "#e0e0e0"
        shadow = "rgba(0, 0, 0, 0.4)"
    else:
        bg_color = "#f3f4f6"
        surface_color = "#ffffff"
        text_primary = "#111827"
        text_secondary = "#4b5563"
        shadow = "rgba(0, 0, 0, 0.08)"

    # === CSS ===
    css = f"""/* Animated Number Counter Cards */
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap');

*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg-color: {bg_color};
    --surface-color: {surface_color};
    --text-primary: {text_primary};
    --text-secondary: {text_secondary};
    --accent-color: {accent_color};
    --shadow: {shadow};
}}

body {{
    font-family: 'Poppins', sans-serif;
    background-color: var(--bg-color);
    color: var(--text-primary);
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 2rem;
}}

.section-container {{
    max-width: {width_px}px;
    width: 100%;
    text-align: center;
}}

.header {{
    margin-bottom: 3rem;
}}

.header h1 {{
    font-size: 2.5rem;
    font-weight: 600;
    margin-bottom: 0.5rem;
}}

.header p {{
    font-size: 1.1rem;
    color: var(--text-secondary);
}}

.stats-wrapper {{
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 2rem;
    width: 100%;
}}

.stat-card {{
    background-color: var(--surface-color);
    flex: 1;
    min-width: 240px;
    max-width: 300px;
    padding: 2.5rem 1.5rem;
    border-radius: 12px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    border-bottom: 8px solid var(--accent-color);
    box-shadow: 0 10px 30px var(--shadow);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}}

.stat-card:hover {{
    transform: translateY(-8px);
    box-shadow: 0 15px 40px var(--shadow);
}}

.stat-icon {{
    font-size: 2.8rem;
    color: var(--accent-color);
    margin-bottom: 1rem;
}}

.stat-num {{
    font-size: 3rem;
    font-weight: 600;
    color: var(--text-primary);
    line-height: 1.2;
    margin-bottom: 0.25rem;
}}

.stat-text {{
    font-size: 1.05rem;
    color: var(--text-secondary);
    font-weight: 400;
}}

/* Responsive Adjustments */
@media screen and (max-width: 768px) {{
    .stats-wrapper {{
        gap: 1.5rem;
    }}
    .stat-card {{
        min-width: calc(50% - 1.5rem);
    }}
}}

@media screen and (max-width: 480px) {{
    .stat-card {{
        min-width: 100%;
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
    <!-- Font Awesome for Icons -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="section-container">
        <div class="header">
            <h1>{title_text}</h1>
            <p>{body_text}</p>
        </div>

        <div class="stats-wrapper">
            <!-- Card 1 -->
            <div class="stat-card">
                <i class="fas fa-utensils stat-icon"></i>
                <span class="stat-num" data-val="400">0</span>
                <span class="stat-text">Meals Delivered</span>
            </div>
            
            <!-- Card 2 -->
            <div class="stat-card">
                <i class="fas fa-smile-beam stat-icon"></i>
                <span class="stat-num" data-val="340">0</span>
                <span class="stat-text">Happy Customers</span>
            </div>
            
            <!-- Card 3 -->
            <div class="stat-card">
                <i class="fas fa-list stat-icon"></i>
                <span class="stat-num" data-val="225">0</span>
                <span class="stat-text">Menu Items</span>
            </div>
            
            <!-- Card 4 -->
            <div class="stat-card">
                <i class="fas fa-star stat-icon"></i>
                <span class="stat-num" data-val="280">0</span>
                <span class="stat-text">Five Stars</span>
            </div>
        </div>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Animated Number Counter Logic
document.addEventListener('DOMContentLoaded', () => {{
    const valueDisplays = document.querySelectorAll('.stat-num');
    const animationDuration = 2500; // Total animation time in ms

    // Easing function for smoother deceleration at the end
    // easeOutQuart
    const easeOut = (t) => 1 - Math.pow(1 - t, 4);

    const animateValue = (el) => {{
        const endValue = parseInt(el.getAttribute('data-val'), 10);
        let startTimestamp = null;

        const step = (timestamp) => {{
            if (!startTimestamp) startTimestamp = timestamp;
            
            // Calculate progress between 0 and 1
            const progress = Math.min((timestamp - startTimestamp) / animationDuration, 1);
            
            // Apply easing
            const easedProgress = easeOut(progress);
            
            // Calculate current value and update DOM
            const currentValue = Math.floor(easedProgress * endValue);
            el.textContent = currentValue;
            
            // Continue animation if not reached 100%
            if (progress < 1) {{
                window.requestAnimationFrame(step);
            }} else {{
                el.textContent = endValue; // Ensure exact final value is set
            }}
        }};
        
        window.requestAnimationFrame(step);
    }};

    // Use Intersection Observer to only start animations when cards scroll into view
    const observerOptions = {{
        root: null,
        rootMargin: '0px',
        threshold: 0.3 // Trigger when 30% of the card is visible
    }};

    const observer = new IntersectionObserver((entries, observer) => {{
        entries.forEach(entry => {{
            if (entry.isIntersecting) {{
                animateValue(entry.target);
                // Unobserve so it only animates once per page load
                observer.unobserve(entry.target);
            }}
        }});
    }}, observerOptions);

    // Attach observer to all number elements
    valueDisplays.forEach(display => {{
        observer.observe(display);
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
