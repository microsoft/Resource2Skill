def create_component(
    output_dir: str,
    title_text: str = "Connected Ecosystem",
    body_text: str = "Seamlessly integrate our dynamic animation APIs into your entire tech stack. High performance, beautifully scalable, and always synchronized.",
    color_scheme: str = "dark",
    accent_color: str = "#00E676",
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Neon Orbital Ecosystem visual effect.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Convert hex accent to rgb triplet for CSS rgba() injection
    hex_clean = accent_color.lstrip('#')
    if len(hex_clean) == 3:
        hex_clean = ''.join([c*2 for c in hex_clean])
    r, g, b = tuple(int(hex_clean[i:i+2], 16) for i in (0, 2, 4))
    accent_rgb = f"{r}, {g}, {b}"

    if color_scheme == "dark":
        bg_color = "#050508"
        bg_light = "#1a1a24"
        text_color = "#ffffff"
        text_muted = "#9ca3af"
        surface_color = "rgba(255, 255, 255, 0.08)"
        grid_color = "rgba(255, 255, 255, 0.03)"
    else:
        bg_color = "#f4f5f7"
        bg_light = "#ffffff"
        text_color = "#0f172a"
        text_muted = "#475569"
        surface_color = "rgba(0, 0, 0, 0.08)"
        grid_color = "rgba(0, 0, 0, 0.03)"

    css = f"""/* Neon Orbital Ecosystem */
:root {{
    --bg: {bg_color};
    --bg-light: {bg_light};
    --text: {text_color};
    --text-muted: {text_muted};
    --accent: {accent_color};
    --accent-rgb: {accent_rgb};
    --surface: {surface_color};
    --grid: {grid_color};
    --width: {width_px}px;
    --height: {height_px}px;
}}

* {{ margin: 0; padding: 0; box-sizing: border-box; }}

body {{
    font-family: 'Inter', system-ui, sans-serif;
    background: var(--bg);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
}}

.component-wrapper {{
    width: var(--width);
    height: var(--height);
    position: relative;
    background: radial-gradient(circle at 50% 50%, var(--bg-light) 0%, var(--bg) 100%);
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 60px;
    border-radius: 24px;
    overflow: hidden;
}}

/* Subtle Background Grid */
.component-wrapper::before {{
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; bottom: 0;
    background-image: radial-gradient(var(--grid) 1px, transparent 1px);
    background-size: 40px 40px;
    z-index: 0;
    pointer-events: none;
}}

.text-panel {{
    position: relative;
    z-index: 10;
    flex: 1;
    max-width: 480px;
}}

.badge {{
    display: inline-block;
    padding: 6px 14px;
    background: rgba(var(--accent-rgb), 0.1);
    color: var(--accent);
    border-radius: 20px;
    font-size: 0.85rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-bottom: 24px;
    border: 1px solid rgba(var(--accent-rgb), 0.2);
}}

.title {{
    font-size: 3.5rem;
    font-weight: 700;
    line-height: 1.1;
    letter-spacing: -0.03em;
    margin-bottom: 24px;
    background: linear-gradient(135deg, var(--text) 30%, var(--accent) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}}

.body-text {{
    font-size: 1.15rem;
    color: var(--text-muted);
    line-height: 1.6;
    margin-bottom: 40px;
}}

.cta-button {{
    padding: 16px 32px;
    background: var(--accent);
    color: #fff;
    border: none;
    border-radius: 12px;
    font-size: 1rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
    box-shadow: 0 8px 20px rgba(var(--accent-rgb), 0.3);
}}

.cta-button:hover {{
    transform: translateY(-2px);
    box-shadow: 0 12px 25px rgba(var(--accent-rgb), 0.5);
}}

.graphic-panel {{
    flex: 1.2;
    height: 100%;
    position: relative;
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 5;
}}

.graphic-anchor {{
    position: relative;
    width: 100%;
    height: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
}}

/* Absolute container strictly scaled by JS */
.graphic-scalable {{
    position: absolute;
    width: 650px;
    height: 650px;
}}

/* --- ORBITAL ANIMATIONS --- */

.center-core {{
    position: absolute;
    top: 50%; left: 50%;
    transform: translate(-50%, -50%);
    width: 80px; height: 80px;
    z-index: 100;
    display: flex;
    justify-content: center;
    align-items: center;
}}

.core-solid {{
    position: absolute;
    width: 100%; height: 100%;
    border-radius: 50%;
    background: var(--accent);
    box-shadow: 0 0 40px rgba(var(--accent-rgb), 0.6), inset -6px -6px 15px rgba(0,0,0,0.2);
}}

.core-solid::after {{
    content: '';
    position: absolute;
    top: 15%; left: 15%;
    width: 30%; height: 30%;
    background: #fff;
    border-radius: 50%;
    opacity: 0.7;
    filter: blur(2px);
}}

.pulse-ring {{
    position: absolute;
    width: 100%; height: 100%;
    border-radius: 50%;
    border: 2px solid var(--accent);
    animation: pulse-out 4.5s cubic-bezier(0.215, 0.61, 0.355, 1) infinite;
}}

@keyframes pulse-out {{
    0% {{ transform: scale(1); opacity: 0.8; }}
    100% {{ transform: scale(3.5); opacity: 0; }}
}}

.ring-wrapper {{
    position: absolute;
    top: 50%; left: 50%;
    transform: translate(-50%, -50%);
    border-radius: 50%;
}}

.ring-border {{
    position: absolute;
    top: 0; left: 0; right: 0; bottom: 0;
    border: 1px solid var(--surface);
    border-radius: 50%;
}}

.orbit-arm {{
    position: absolute;
    top: 0; left: 0; right: 0; bottom: 0;
    border-radius: 50%;
    animation-name: spin;
    animation-timing-function: linear;
    animation-iteration-count: infinite;
}}

.orbit-tail {{
    position: absolute;
    top: 0; left: 0; right: 0; bottom: 0;
    border-radius: 50%;
    -webkit-mask: radial-gradient(circle closest-side at 50% 50%, transparent calc(100% - 4px), black calc(100% - 2px), black 100%, transparent 100%);
    mask: radial-gradient(circle closest-side at 50% 50%, transparent calc(100% - 4px), black calc(100% - 2px), black 100%, transparent 100%);
    z-index: 1;
}}

.node-container {{
    position: absolute;
    top: 0;
    left: 50%;
    transform: translate(-50%, -50%);
    z-index: 2;
}}

.orbit-node {{
    position: relative;
    border-radius: 50%;
    box-shadow: inset -5px -5px 12px rgba(0,0,0,0.3);
    animation-timing-function: linear;
    animation-iteration-count: infinite;
}}

/* Specular highlight fixed to top-left via counter-spin */
.orbit-node::after {{
    content: '';
    position: absolute;
    top: 15%; left: 15%;
    width: 35%; height: 35%;
    background: #fff;
    border-radius: 50%;
    opacity: 0.75;
    filter: blur(1px);
}}

@keyframes spin {{
    0% {{ transform: rotate(0deg); }}
    100% {{ transform: rotate(360deg); }}
}}

@keyframes counter-spin {{
    0% {{ transform: rotate(360deg); }}
    100% {{ transform: rotate(0deg); }}
}}

@media (max-width: 950px) {{
    .component-wrapper {{ flex-direction: column; padding: 40px; text-align: center; }}
    .text-panel {{ max-width: 100%; margin-bottom: 20px; }}
    .title {{ font-size: 2.8rem; }}
}}
"""

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
    <div class="component-wrapper">
        <div class="text-panel">
            <div class="badge">Integration Ecosystem</div>
            <h1 class="title">{title_text}</h1>
            <p class="body-text">{body_text}</p>
            <button class="cta-button">Explore Network</button>
        </div>
        
        <div class="graphic-panel">
            <div class="graphic-anchor" id="graphic-anchor">
                <div class="graphic-scalable" id="ecosystem-graphic">
                    
                    <div class="center-core">
                        <div class="pulse-ring" style="animation-delay: 0s;"></div>
                        <div class="pulse-ring" style="animation-delay: 1.5s;"></div>
                        <div class="pulse-ring" style="animation-delay: 3s;"></div>
                        <div class="core-solid"></div>
                    </div>
                    
                </div>
            </div>
        </div>
    </div>
    
    <script src="script.js"></script>
</body>
</html>"""

    js = """document.addEventListener('DOMContentLoaded', () => {
    const graphicPanel = document.getElementById('ecosystem-graphic');
    const centerCore = graphicPanel.querySelector('.center-core');

    // Ring Configuration Data
    const rings = [
        { size: 280, speed: 14, reverse: false, dashed: false, nodes: [
            { color: 'linear-gradient(135deg, #ff0844 0%, #ffb199 100%)', tailColor: '#ff0844', tailTrans: 'rgba(255,8,68,0)', size: 28, delay: 0 },
            { color: 'linear-gradient(135deg, #f83600 0%, #f9d423 100%)', tailColor: '#f83600', tailTrans: 'rgba(248,54,0,0)', size: 18, delay: -7 }
        ]},
        { size: 440, speed: 22, reverse: true, dashed: true, nodes: [
            { color: 'linear-gradient(135deg, #1e3c72 0%, #2a5298 100%)', tailColor: '#2a5298', tailTrans: 'rgba(42,82,152,0)', size: 36, delay: 0 },
            { color: 'linear-gradient(135deg, #0ed2f7 0%, #b2ff05 100%)', tailColor: '#0ed2f7', tailTrans: 'rgba(14,210,247,0)', size: 22, delay: -9 },
            { color: 'linear-gradient(135deg, #8e2de2 0%, #4a00e0 100%)', tailColor: '#8e2de2', tailTrans: 'rgba(142,45,226,0)', size: 30, delay: -15 }
        ]},
        { size: 620, speed: 32, reverse: false, dashed: false, nodes: [
            { color: 'var(--accent)', tailColor: 'var(--accent)', tailTrans: 'rgba(var(--accent-rgb), 0)', size: 40, delay: 0 },
            { color: 'linear-gradient(135deg, #ff0844 0%, #ffb199 100%)', tailColor: '#ff0844', tailTrans: 'rgba(255,8,68,0)', size: 20, delay: -16 }
        ]}
    ];

    // Generate rings via DOM manipulation
    rings.forEach((ringConfig, index) => {
        const wrapper = document.createElement('div');
        wrapper.className = 'ring-wrapper';
        wrapper.style.width = `${ringConfig.size}px`;
        wrapper.style.height = `${ringConfig.size}px`;
        wrapper.style.zIndex = index + 1;

        const border = document.createElement('div');
        border.className = 'ring-border';
        if (ringConfig.dashed) {
            border.style.borderStyle = 'dashed';
            border.style.animation = `spin ${ringConfig.speed * 2}s linear infinite`;
            if (ringConfig.reverse) border.style.animationDirection = 'reverse';
        }
        wrapper.appendChild(border);

        ringConfig.nodes.forEach(nodeConfig => {
            const arm = document.createElement('div');
            arm.className = 'orbit-arm';
            arm.style.animationDuration = `${ringConfig.speed}s`;
            arm.style.animationDelay = `${nodeConfig.delay}s`;
            arm.style.animationName = 'spin';
            
            const nodeContainer = document.createElement('div');
            nodeContainer.className = 'node-container';

            const node = document.createElement('div');
            node.className = 'orbit-node';
            node.style.width = `${nodeConfig.size}px`;
            node.style.height = `${nodeConfig.size}px`;
            node.style.background = nodeConfig.color;
            node.style.animationDuration = `${ringConfig.speed}s`;
            node.style.animationDelay = `${nodeConfig.delay}s`;

            // Comet Tail Rendering
            const tail = document.createElement('div');
            tail.className = 'orbit-tail';
            
            if (ringConfig.reverse) {
                // Reverse rotation logic
                arm.style.animationDirection = 'reverse';
                node.style.animationName = 'spin'; // Counter-spins against the reverse arm
                // Tail draws behind node moving left
                tail.style.background = `conic-gradient(from 0deg, ${nodeConfig.tailColor} 0deg, ${nodeConfig.tailTrans} 100deg, ${nodeConfig.tailTrans} 360deg)`;
            } else {
                // Normal rotation logic
                node.style.animationName = 'counter-spin';
                // Tail draws behind node moving right
                tail.style.background = `conic-gradient(from 0deg, ${nodeConfig.tailTrans} 0deg, ${nodeConfig.tailTrans} 260deg, ${nodeConfig.tailColor} 360deg)`;
            }

            nodeContainer.appendChild(node);
            arm.appendChild(tail);
            arm.appendChild(nodeContainer);
            wrapper.appendChild(arm);
        });

        graphicPanel.insertBefore(wrapper, centerCore);
    });

    // Responsive Scaling Logic
    const anchor = document.getElementById('graphic-anchor');
    const scalable = document.getElementById('ecosystem-graphic');
    
    const resizeObserver = new ResizeObserver(entries => {
        for (let entry of entries) {
            const rect = entry.contentRect;
            const size = Math.min(rect.width, rect.height);
            let scale = size / 650;
            scale = scale * 0.95; // Add margin padding
            if (scale > 1) scale = 1; 
            scalable.style.transform = `scale(${scale})`;
        }
    });
    resizeObserver.observe(anchor);
});"""

    # Write files
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
