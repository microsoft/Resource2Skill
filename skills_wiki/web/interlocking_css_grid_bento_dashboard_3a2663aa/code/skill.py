def create_component(
    output_dir: str,
    title_text: str = "Live Analytics Dashboard",
    body_text: str = "Real-time metrics and system performance overview.",
    color_scheme: str = "dark",
    accent_color: str = "#e91e63",
    width_px: int = 1200,
    height_px: int = 850,
    **kwargs,
) -> dict:
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Theme definitions
    if color_scheme == "dark":
        bg_color = "#0b0f19"
        text_color = "#ffffff"
        text_muted = "#8b949e"
        surface_color = "rgba(255, 255, 255, 0.03)"
        surface_border = "rgba(255, 255, 255, 0.08)"
        overlap_bg = "rgba(11, 15, 25, 0.65)"
    else:
        bg_color = "#f3f4f6"
        text_color = "#111827"
        text_muted = "#6b7280"
        surface_color = "#ffffff"
        surface_border = "rgba(0, 0, 0, 0.05)"
        overlap_bg = "rgba(255, 255, 255, 0.75)"

    body_html = f"<p>{body_text}</p>" if body_text else ""

    css = f"""/* Interlocking CSS Grid Bento Dashboard */
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
    --border: {surface_border};
    --overlap-bg: {overlap_bg};
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
    padding: 2rem;
    overflow-x: hidden;
}}

.dashboard-wrapper {{
    width: 100%;
    max-width: var(--width);
}}

.dashboard-header {{
    text-align: center;
    margin-bottom: 2.5rem;
}}

.dashboard-header h1 {{
    font-size: 2.5rem;
    font-weight: 700;
    margin-bottom: 0.5rem;
    letter-spacing: -0.02em;
}}

.dashboard-header p {{
    font-size: 1.1rem;
    color: var(--text-muted);
}}

/* == The Core Bento Grid == */
.bento-grid {{
    display: grid;
    /* 4 Columns, flexible but equal */
    grid-template-columns: repeat(4, 1fr);
    /* 3 Rows, minimum 140px, expanding to fill available height */
    grid-template-rows: repeat(3, minmax(140px, 1fr));
    min-height: calc(var(--height) - 150px);
    gap: 1.5rem;
}}

.bento-item {{
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 24px;
    padding: 2rem;
    display: flex;
    flex-direction: column;
    position: relative;
    transition: transform 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275), box-shadow 0.4s ease;
}}

.bento-item:hover {{
    transform: translateY(-6px);
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15);
}}

/* == Grid Explicit Positioning == */
/* syntax: grid-area: row-start / col-start / row-end / col-end */

.item-hero {{
    grid-area: 1 / 1 / 3 / 3;
    background: linear-gradient(135deg, var(--accent), #7b2cbf);
    color: #ffffff;
    box-shadow: 0 10px 30px rgba(233, 30, 99, 0.2);
}}

.item-stat-1 {{
    grid-area: 1 / 3 / 2 / 5;
}}

.item-overlap {{
    grid-area: 2 / 2 / 4 / 4;
    z-index: 10;
    background: var(--overlap-bg);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border: 1px solid rgba(255, 255, 255, 0.15);
    box-shadow: 0 30px 60px rgba(0, 0, 0, 0.25);
}}

.item-stat-2 {{
    grid-area: 2 / 4 / 4 / 5;
    background: linear-gradient(135deg, #03a9f4, #00d2ff);
    color: #ffffff;
}}

.item-mini {{
    grid-area: 3 / 1 / 4 / 2;
    align-items: center;
    justify-content: center;
}}

/* == Internal Typography & Layout == */
.icon-wrap {{
    margin-bottom: auto;
}}

h3 {{
    font-size: 1.1rem;
    font-weight: 500;
    margin-bottom: 0.5rem;
}}

.item-hero h3, .item-stat-2 h3 {{
    color: rgba(255, 255, 255, 0.9);
}}

.value {{
    font-size: 3rem;
    font-weight: 700;
    line-height: 1;
    margin-bottom: 0.75rem;
    letter-spacing: -0.03em;
}}

.trend {{
    display: inline-flex;
    align-items: center;
    gap: 8px;
    font-size: 0.9rem;
    font-weight: 600;
    background: rgba(255, 255, 255, 0.2);
    padding: 6px 14px;
    border-radius: 50px;
    backdrop-filter: blur(4px);
    width: max-content;
}}

.text-muted {{ color: var(--text-muted); }}
.sub-text {{ font-size: 0.9rem; color: var(--text-muted); }}

/* == Specific Card Adjustments == */
.item-stat-2 {{
    justify-content: flex-end;
}}
.item-stat-2 .status-optimal {{
    margin-top: auto;
    font-weight: 500;
    background: rgba(255, 255, 255, 0.25);
    padding: 6px 12px;
    border-radius: 8px;
    display: inline-block;
    width: max-content;
}}

/* == Animations (Chart & Badge) == */
.badge-live {{
    position: absolute;
    top: 1.5rem;
    right: 1.5rem;
    background: #ff0055;
    color: white;
    font-size: 0.75rem;
    font-weight: 800;
    padding: 4px 12px;
    border-radius: 20px;
    letter-spacing: 1px;
    animation: pulse-red 2s infinite;
}}

@keyframes pulse-red {{
    0% {{ box-shadow: 0 0 0 0 rgba(255, 0, 85, 0.6); }}
    70% {{ box-shadow: 0 0 0 10px rgba(255, 0, 85, 0); }}
    100% {{ box-shadow: 0 0 0 0 rgba(255, 0, 85, 0); }}
}}

.chart-mockup {{
    display: flex;
    align-items: flex-end;
    gap: 8px;
    height: 100px;
    margin-top: auto;
}}

.chart-bar {{
    flex: 1;
    background: var(--accent);
    border-radius: 4px 4px 0 0;
    transform-origin: bottom;
    opacity: 0;
    animation: rise 1s cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards;
}}

.chart-bar:nth-child(1) {{ height: 40%; animation-delay: 0.1s; }}
.chart-bar:nth-child(2) {{ height: 75%; animation-delay: 0.2s; }}
.chart-bar:nth-child(3) {{ height: 50%; animation-delay: 0.3s; }}
.chart-bar:nth-child(4) {{ height: 95%; animation-delay: 0.4s; background: #ff0055; }}
.chart-bar:nth-child(5) {{ height: 60%; animation-delay: 0.5s; }}
.chart-bar:nth-child(6) {{ height: 85%; animation-delay: 0.6s; }}

@keyframes rise {{
    0% {{ transform: scaleY(0); opacity: 0; }}
    100% {{ transform: scaleY(1); opacity: 1; }}
}}

/* == Responsive Grid Fallback == */
@media (max-width: 900px) {{
    .bento-grid {{
        grid-template-columns: repeat(2, 1fr);
        grid-template-rows: auto;
    }}
    .item-hero {{ grid-area: 1 / 1 / 3 / 3; }}
    .item-stat-1 {{ grid-area: 3 / 1 / 4 / 3; }}
    .item-overlap {{ 
        grid-area: 4 / 1 / 6 / 3; 
        backdrop-filter: none;
        background: var(--surface);
    }}
    .item-stat-2 {{ grid-area: 6 / 1 / 7 / 2; }}
    .item-mini {{ grid-area: 6 / 2 / 7 / 3; }}
}}

@media (max-width: 600px) {{
    .bento-grid {{
        grid-template-columns: 1fr;
    }}
    .bento-item {{
        grid-area: auto !important;
    }}
}}

@media (prefers-reduced-motion: reduce) {{
    .chart-bar, .badge-live {{
        animation: none;
        transform: scaleY(1);
        opacity: 1;
    }}
    .bento-item {{ transition: none; }}
}}
"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="dashboard-wrapper">
        <header class="dashboard-header">
            <h1>{title_text}</h1>
            {body_html}
        </header>

        <div class="bento-grid">
            
            <!-- 1. Span 2x2 Hero -->
            <div class="bento-item item-hero">
                <div class="icon-wrap"><i class="fa-solid fa-chart-pie fa-2x"></i></div>
                <div>
                    <h3>Total Revenue</h3>
                    <div class="value counter" data-target="124500">$0</div>
                    <div class="trend"><i class="fa-solid fa-arrow-trend-up"></i> +14.5% this month</div>
                </div>
            </div>

            <!-- 2. Top Right Row -->
            <div class="bento-item item-stat-1">
                <h3 class="text-muted">Active Users</h3>
                <div class="value">8,234</div>
                <div class="sub-text">Currently online</div>
            </div>

            <!-- 3. Glassmorphism Overlap -->
            <div class="bento-item item-overlap">
                <div class="badge-live">LIVE</div>
                <h3>Traffic Spikes</h3>
                <div class="chart-mockup">
                    <div class="chart-bar"></div>
                    <div class="chart-bar"></div>
                    <div class="chart-bar"></div>
                    <div class="chart-bar"></div>
                    <div class="chart-bar"></div>
                    <div class="chart-bar"></div>
                </div>
            </div>

            <!-- 4. Right Column Span -->
            <div class="bento-item item-stat-2">
                <i class="fa-solid fa-bolt fa-2x mb-3"></i>
                <h3>Server Load</h3>
                <div class="value">24%</div>
                <div class="status-optimal">Optimal Performance</div>
            </div>

            <!-- 5. Bottom Left Mini -->
            <div class="bento-item item-mini">
                <i class="fa-solid fa-sliders fa-2x text-muted"></i>
            </div>

        </div>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    js = """// Smooth Counter Animation for Dashboard Integrity
document.addEventListener('DOMContentLoaded', () => {
    const counterEl = document.querySelector('.counter');
    if (!counterEl) return;

    const endValue = parseInt(counterEl.getAttribute('data-target'), 10);
    const startValue = Math.floor(endValue * 0.85); // Start at 85% for quick tick
    const duration = 2000; // ms
    const startTime = performance.now();

    function updateCounter(currentTime) {
        const elapsed = currentTime - startTime;
        const progress = Math.min(elapsed / duration, 1);
        
        // Easing function: easeOutQuart
        const ease = 1 - Math.pow(1 - progress, 4);
        const currentVal = Math.floor(startValue + (endValue - startValue) * ease);
        
        // Format with commas and prefix
        counterEl.textContent = '$' + currentVal.toLocaleString();

        if (progress < 1) {
            requestAnimationFrame(updateCounter);
        } else {
            counterEl.textContent = '$' + endValue.toLocaleString();
        }
    }
    
    // Start animation loop
    requestAnimationFrame(updateCounter);
});
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
