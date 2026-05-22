def create_component(
    output_dir: str,
    title_text: str = "System Architecture",
    body_text: str = "Real-time data synchronization across all edge devices and core processing nodes.",
    color_scheme: str = "dark",
    accent_color: str = "#00e5ff",
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    import os

    os.makedirs(output_dir, exist_ok=True)

    # --- Theme Configuration ---
    if color_scheme == "dark":
        bg_color = "#0b0d13"
        text_color = "#ffffff"
        text_muted = "#8b949e"
        grid_color = "#1f242f"
        d_colors = {
            'top': '#2d3342',
            'side_right': '#212631',
            'side_left': '#161a22',
            'screen_edge': '#3a4150',
            'screen_front': '#000000',
            'screen_ui_bg': '#1f242f',
            'keyboard': '#1c202a'
        }
    else:
        bg_color = "#f8f9fa"
        text_color = "#111827"
        text_muted = "#6b7280"
        grid_color = "#e5e7eb"
        d_colors = {
            'top': '#ffffff',
            'side_right': '#e5e7eb',
            'side_left': '#d1d5db',
            'screen_edge': '#f3f4f6',
            'screen_front': '#111827',
            'screen_ui_bg': '#374151',
            'keyboard': '#f3f4f6'
        }

    chart_colors = [accent_color, '#ff3366', '#ffcc00', '#00ff66']

    # --- Isometric Math Helpers ---
    # These map standard 2D coordinates to isometric planes
    COS30 = 0.866025
    SIN30 = 0.5
    cx, cy = width_px / 2, height_px / 2

    def iso_top(x, y, z):
        tx = cx + (x - y) * COS30
        ty = cy + (x + y) * SIN30 - z
        return f"matrix({COS30:.6f}, {SIN30:.6f}, {-COS30:.6f}, {SIN30:.6f}, {tx:.2f}, {ty:.2f})"

    def iso_left(x, y, z):
        tx = cx + (x - y) * COS30
        ty = cy + (x + y) * SIN30 - z
        return f"matrix({-COS30:.6f}, {SIN30:.6f}, 0, 1, {tx:.2f}, {ty:.2f})"

    def iso_right(x, y, z):
        tx = cx + (x - y) * COS30
        ty = cy + (x + y) * SIN30 - z
        return f"matrix({COS30:.6f}, {SIN30:.6f}, 0, 1, {tx:.2f}, {ty:.2f})"

    # --- Device Generators ---
    def draw_laptop(x, y, z, w, d, h, screen_h, ui_content):
        t = 4 # thickness
        return f"""
        <g class="device">
            <!-- Base Sides -->
            <g transform="{iso_left(x+w, y, z+h)}"><rect width="{d}" height="{h}" fill="{d_colors['side_left']}"/></g>
            <g transform="{iso_right(x, y+d, z+h)}"><rect width="{w}" height="{h}" fill="{d_colors['side_right']}"/></g>
            <!-- Base Top (Keyboard area) -->
            <g transform="{iso_top(x, y, z+h)}">
                <rect width="{w}" height="{d}" fill="{d_colors['top']}" rx="2"/>
                <rect x="{w*0.1}" y="{d*0.4}" width="{w*0.8}" height="{d*0.45}" fill="{d_colors['keyboard']}" rx="2"/>
                <rect x="{(w - w*0.25)/2}" y="{d*0.4 + d*0.45 + 4}" width="{w*0.25}" height="{d*0.1}" fill="{d_colors['side_left']}" rx="1"/>
            </g>
            <!-- Screen Sides -->
            <g transform="{iso_left(x+w, y, z+h+screen_h)}"><rect width="{t}" height="{screen_h}" fill="{d_colors['side_left']}"/></g>
            <g transform="{iso_top(x, y, z+h+screen_h)}"><rect width="{w}" height="{t}" fill="{d_colors['screen_edge']}"/></g>
            <!-- Screen Front (UI) -->
            <g transform="{iso_right(x, y+t, z+h+screen_h)}">
                <rect width="{w}" height="{screen_h}" fill="{d_colors['screen_front']}" stroke="{d_colors['side_right']}" stroke-width="1"/>
                {ui_content}
            </g>
        </g>
        """

    def draw_flat_device(x, y, z, w, d, h, ui_content):
        return f"""
        <g class="device">
            <g transform="{iso_left(x+w, y, z+h)}"><rect width="{d}" height="{h}" fill="{d_colors['side_left']}"/></g>
            <g transform="{iso_right(x, y+d, z+h)}"><rect width="{w}" height="{h}" fill="{d_colors['side_right']}"/></g>
            <g transform="{iso_top(x, y, z+h)}">
                <rect width="{w}" height="{d}" fill="{d_colors['top']}" rx="4"/>
                {ui_content}
            </g>
        </g>
        """

    # --- UI Snippets ---
    ui_main_laptop = f"""
        <rect x="10" y="10" width="180" height="12" rx="2" fill="{d_colors['screen_ui_bg']}"/>
        <rect x="15" y="14" width="30" height="4" rx="2" fill="{chart_colors[0]}"/>
        <!-- Bar Chart -->
        <g transform="translate(15, 120) scale(1, -1)">
            <rect class="bar b1" x="0" y="0" width="12" height="60" fill="{chart_colors[0]}"/>
            <rect class="bar b2" x="18" y="0" width="12" height="80" fill="{chart_colors[1]}"/>
            <rect class="bar b3" x="36" y="0" width="12" height="40" fill="{chart_colors[2]}"/>
            <rect class="bar b4" x="54" y="0" width="12" height="90" fill="{chart_colors[3]}"/>
            <rect class="bar b5" x="72" y="0" width="12" height="50" fill="{chart_colors[0]}"/>
        </g>
        <!-- Line Chart -->
        <g transform="translate(105, 30)">
            <path d="M 0 20 L 80 20 M 0 40 L 80 40 M 0 60 L 80 60 M 0 80 L 80 80" stroke="{d_colors['screen_ui_bg']}" stroke-width="1"/>
            <path class="trend-line" d="M 0 80 L 20 45 L 40 60 L 60 15 L 80 25" fill="none" stroke="{chart_colors[1]}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
        </g>
    """

    ui_small_laptop = f"""
        <rect x="10" y="10" width="120" height="8" rx="2" fill="{d_colors['screen_ui_bg']}"/>
        <rect x="10" y="25" width="40" height="40" rx="4" fill="{d_colors['screen_ui_bg']}"/>
        <rect x="60" y="25" width="70" height="40" rx="4" fill="{d_colors['screen_ui_bg']}"/>
        <g transform="translate(60, 65) scale(1, -1)">
            <path class="trend-line-2" d="M 5 5 L 25 25 L 45 15 L 65 35" fill="none" stroke="{chart_colors[3]}" stroke-width="2" stroke-linecap="round"/>
        </g>
    """

    ui_tablet = f"""
        <rect x="8" y="8" width="74" height="114" fill="{d_colors['screen_front']}" rx="2"/>
        <circle cx="45" cy="55" r="25" fill="none" stroke="{d_colors['screen_ui_bg']}" stroke-width="8"/>
        <circle class="donut-anim" cx="45" cy="55" r="25" fill="none" stroke="{chart_colors[2]}" stroke-width="8" stroke-dasharray="157" stroke-dashoffset="157" transform="rotate(-90 45 55)"/>
        <rect x="15" y="105" width="60" height="6" rx="3" fill="{d_colors['screen_ui_bg']}"/>
    """

    ui_phone = f"""
        <rect x="4" y="4" width="42" height="92" fill="{d_colors['screen_front']}" rx="2"/>
        <g transform="translate(10, 15)">
            <rect class="notif n1" x="0" y="0" width="30" height="6" rx="2" fill="{chart_colors[0]}"/>
            <rect class="notif n2" x="0" y="12" width="20" height="6" rx="2" fill="{chart_colors[1]}"/>
            <rect class="notif n3" x="0" y="24" width="25" height="6" rx="2" fill="{chart_colors[3]}"/>
            <rect class="notif n4" x="0" y="36" width="28" height="6" rx="2" fill="{d_colors['screen_ui_bg']}"/>
            <rect class="notif n5" x="0" y="48" width="15" height="6" rx="2" fill="{d_colors['screen_ui_bg']}"/>
        </g>
    """

    # --- Scene Assembly ---
    # Background Grid
    grid_svg = f'<g transform="{iso_top(0,0,0)}">\n'
    for i in range(-12, 13):
        val = i * 60
        grid_svg += f'<line x1="{val}" y1="-720" x2="{val}" y2="720" stroke="{grid_color}" stroke-width="1"/>\n'
        grid_svg += f'<line x1="-720" y1="{val}" x2="720" y2="{val}" stroke="{grid_color}" stroke-width="1"/>\n'
    grid_svg += '</g>'

    # Network Lines on Floor
    paths = [
        "M -130 100 L -130 -80 L 150 -80",  # Small Laptop to Main Laptop
        "M 150 -80 L 195 -80 L 195 215",    # Main Laptop to Tablet
        "M -75 250 L -130 250 L -130 100",  # Phone to Small Laptop
    ]
    lines_svg = f'<g class="network-layer" transform="{iso_top(0,0,0)}">\n'
    for p in paths:
        lines_svg += f'<path class="conn-base" d="{p}" />\n'
        lines_svg += f'<path class="conn-glow" d="{p}" />\n'
    lines_svg += '</g>'

    # Devices (Rendered back to front based on Y-axis projection)
    scene_svg = "\n".join([
        grid_svg,
        lines_svg,
        draw_laptop(-200, 50, 0, 140, 100, 8, 100, ui_small_laptop), # Small Laptop
        draw_laptop(50, -150, 0, 200, 140, 12, 140, ui_main_laptop), # Main Laptop
        draw_flat_device(-100, 200, 0, 50, 100, 4, ui_phone),        # Phone
        draw_flat_device(150, 150, 0, 90, 130, 6, ui_tablet),        # Tablet
    ])


    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="overlay">
        <h1 class="title">{title_text}</h1>
        <p class="body-text">{body_text}</p>
    </div>
    
    <svg class="isometric-scene" viewBox="0 0 {width_px} {height_px}" preserveAspectRatio="xMidYMid slice">
        {scene_svg}
    </svg>

    <script src="script.js"></script>
</body>
</html>"""

    css = f"""/* Isometric Device Network Styles */
:root {{
    --bg: {bg_color};
    --text: {text_color};
    --text-muted: {text_muted};
    --accent: {accent_color};
}}

* {{ margin: 0; padding: 0; box-sizing: border-box; }}

body {{
    font-family: 'Inter', system-ui, sans-serif;
    background-color: var(--bg);
    color: var(--text);
    width: 100vw;
    height: 100vh;
    overflow: hidden;
    position: relative;
}}

/* Typography Overlay */
.overlay {{
    position: absolute;
    top: 60px;
    left: 60px;
    max-width: 480px;
    z-index: 10;
    pointer-events: none;
}}

.title {{
    font-size: 3rem;
    font-weight: 700;
    line-height: 1.1;
    letter-spacing: -0.03em;
    margin-bottom: 1rem;
}}

.body-text {{
    font-size: 1.125rem;
    line-height: 1.6;
    color: var(--text-muted);
}}

/* SVG Container */
.isometric-scene {{
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
}}

/* Network Line Animations */
.conn-base {{
    fill: none;
    stroke: {grid_color};
    stroke-width: 3;
    stroke-linejoin: round;
}}

.conn-glow {{
    fill: none;
    stroke: var(--accent);
    stroke-width: 3;
    stroke-linecap: round;
    stroke-linejoin: round;
    stroke-dasharray: 40 400;
    stroke-dashoffset: 440;
    animation: data-flow 4s linear infinite;
    filter: drop-shadow(0 0 6px var(--accent));
}}

.network-layer path:nth-child(2) {{ animation-delay: 0s; }}
.network-layer path:nth-child(4) {{ animation-delay: -1.5s; }}
.network-layer path:nth-child(6) {{ animation-delay: -3s; }}

@keyframes data-flow {{
    to {{ stroke-dashoffset: 0; }}
}}

/* UI Micro-Animations */
.bar {{
    transform: scaleY(0);
    animation: bar-grow 1.2s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}}
.b1 {{ animation-delay: 0.5s; }}
.b2 {{ animation-delay: 0.7s; }}
.b3 {{ animation-delay: 0.9s; }}
.b4 {{ animation-delay: 1.1s; }}
.b5 {{ animation-delay: 1.3s; }}

@keyframes bar-grow {{
    to {{ transform: scaleY(1); }}
}}

.trend-line {{
    stroke-dasharray: 200;
    stroke-dashoffset: 200;
    animation: line-draw 1.5s ease-out forwards 1.2s;
}}

.trend-line-2 {{
    stroke-dasharray: 120;
    stroke-dashoffset: 120;
    animation: line-draw 1.2s ease-out forwards 1.6s;
}}

@keyframes line-draw {{
    to {{ stroke-dashoffset: 0; }}
}}

.donut-anim {{
    animation: donut-fill 1.5s cubic-bezier(0.16, 1, 0.3, 1) forwards 1.8s;
}}

@keyframes donut-fill {{
    to {{ stroke-dashoffset: 40; }}
}}

.notif {{
    opacity: 0;
    transform: translateX(-10px);
    animation: slide-in 0.6s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}}
.n1 {{ animation-delay: 2.2s; }}
.n2 {{ animation-delay: 2.4s; }}
.n3 {{ animation-delay: 2.6s; }}
.n4 {{ animation-delay: 2.8s; }}
.n5 {{ animation-delay: 3.0s; }}

@keyframes slide-in {{
    to {{ opacity: 1; transform: translateX(0); }}
}}
"""

    js = """// Animations are handled entirely by CSS.
// The SVG structural generation creates perfect 2D representations of 3D objects.
document.addEventListener('DOMContentLoaded', () => {
    console.log("Isometric network scene initialized.");
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
