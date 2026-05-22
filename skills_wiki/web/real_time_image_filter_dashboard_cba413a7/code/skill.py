def create_component(
    output_dir: str,
    title_text: str = "Image Filter Dashboard",
    body_text: str = "Select a filter category and adjust the sliders for real-time effects.",
    color_scheme: str = "dark",
    accent_color: str = "#00bfff",
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Real-time Image Filter Dashboard.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    if color_scheme == "dark":
        bg_main = "#121212"
        bg_sidebar = "#1e1e1e"
        bg_accordion = "#2a2a2a"
        text_primary = "#eeeeee"
        text_secondary = "#aaaaaa"
        border_color = "#333333"
    else:
        bg_main = "#e5e5e5"
        bg_sidebar = "#f4f4f4"
        bg_accordion = "#ffffff"
        text_primary = "#222222"
        text_secondary = "#555555"
        border_color = "#dddddd"

    css = f"""/* Image Filter Dashboard — generated component */
:root {{
    --bg-main: {bg_main};
    --bg-sidebar: {bg_sidebar};
    --bg-accordion: {bg_accordion};
    --text-primary: {text_primary};
    --text-secondary: {text_secondary};
    --border-color: {border_color};
    --accent: {accent_color};
    --width: {width_px}px;
    --height: {height_px}px;
}}

*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background: var(--bg-main);
    color: var(--text-primary);
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 100vh;
    overflow: hidden;
}}

.app-container {{
    width: var(--width);
    height: var(--height);
    display: flex;
    flex-direction: row;
    background: var(--bg-main);
    border: 1px solid var(--border-color);
    box-shadow: 0 20px 50px rgba(0,0,0,0.5);
    overflow: hidden;
}}

/* === Sidebar Styles === */
.sidebar {{
    width: 280px;
    background: var(--bg-sidebar);
    border-right: 1px solid var(--border-color);
    display: flex;
    flex-direction: column;
    overflow-y: auto;
}}

.sidebar-header {{
    padding: 16px;
    border-bottom: 1px solid var(--border-color);
    background: var(--bg-sidebar);
    position: sticky;
    top: 0;
    z-index: 10;
}}

.sidebar-header h2 {{
    font-size: 14px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-bottom: 4px;
}}

.sidebar-header p {{
    font-size: 11px;
    color: var(--text-secondary);
}}

/* === Accordion Filter Groups === */
.filter-group {{
    border-bottom: 1px solid var(--border-color);
}}

.filter-header {{
    padding: 14px 16px;
    font-size: 13px;
    font-weight: 600;
    cursor: pointer;
    user-select: none;
    transition: background 0.2s, color 0.2s;
    display: flex;
    justify-content: space-between;
    align-items: center;
}}

.filter-header:hover {{
    background: rgba(255, 255, 255, 0.05);
}}

.filter-header::after {{
    content: '+';
    color: var(--text-secondary);
    font-size: 16px;
    transition: transform 0.3s;
}}

.filter-group.active .filter-header {{
    background: var(--bg-accordion);
    color: var(--accent);
}}

.filter-group.active .filter-header::after {{
    content: '−';
    color: var(--accent);
}}

.filter-controls {{
    display: none;
    padding: 16px;
    background: var(--bg-accordion);
}}

.filter-group.active .filter-controls {{
    display: block;
}}

/* === Control Elements === */
.control-row {{
    margin-bottom: 16px;
}}

.control-row:last-child {{
    margin-bottom: 0;
}}

.control-label {{
    display: flex;
    justify-content: space-between;
    font-size: 11px;
    color: var(--text-secondary);
    margin-bottom: 8px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}}

.val-display {{
    color: var(--text-primary);
    font-variant-numeric: tabular-nums;
}}

/* Custom Range Slider */
input[type=range] {{
    -webkit-appearance: none;
    width: 100%;
    background: transparent;
}}

input[type=range]:focus {{
    outline: none;
}}

input[type=range]::-webkit-slider-runnable-track {{
    width: 100%;
    height: 4px;
    cursor: pointer;
    background: var(--border-color);
    border-radius: 2px;
}}

input[type=range]::-webkit-slider-thumb {{
    height: 14px;
    width: 14px;
    border-radius: 50%;
    background: var(--text-primary);
    cursor: pointer;
    -webkit-appearance: none;
    margin-top: -5px;
    transition: background 0.2s, transform 0.1s;
}}

input[type=range]:active::-webkit-slider-thumb {{
    background: var(--accent);
    transform: scale(1.2);
}}

/* Action Buttons */
.action-buttons {{
    display: flex;
    gap: 8px;
    margin-top: 20px;
}}

.btn {{
    flex: 1;
    padding: 6px 0;
    font-size: 11px;
    font-weight: 600;
    text-transform: uppercase;
    background: transparent;
    border: 1px solid var(--border-color);
    color: var(--text-primary);
    cursor: pointer;
    border-radius: 4px;
    transition: all 0.2s;
}}

.btn:hover {{
    background: rgba(255, 255, 255, 0.1);
}}

.btn.accept {{
    background: var(--accent);
    border-color: var(--accent);
    color: #fff;
}}

.btn.accept:hover {{
    filter: brightness(1.1);
}}

/* === Main Canvas Area === */
.canvas-area {{
    flex-grow: 1;
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 40px;
    background-image: 
        linear-gradient(45deg, rgba(255,255,255,0.02) 25%, transparent 25%), 
        linear-gradient(-45deg, rgba(255,255,255,0.02) 25%, transparent 25%), 
        linear-gradient(45deg, transparent 75%, rgba(255,255,255,0.02) 75%), 
        linear-gradient(-45deg, transparent 75%, rgba(255,255,255,0.02) 75%);
    background-size: 20px 20px;
    background-position: 0 0, 0 10px, 10px -10px, -10px 0px;
}}

#target-image {{
    max-width: 100%;
    max-height: 100%;
    object-fit: contain;
    box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    /* Transition for smooth sliding updates */
    transition: filter 0.1s ease-out;
}}

/* Custom Scrollbar */
::-webkit-scrollbar {{
    width: 8px;
}}
::-webkit-scrollbar-track {{
    background: var(--bg-sidebar);
}}
::-webkit-scrollbar-thumb {{
    background: var(--border-color);
    border-radius: 4px;
}}
::-webkit-scrollbar-thumb:hover {{
    background: #555;
}}
"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="app-container">
        <aside class="sidebar">
            <div class="sidebar-header">
                <h2>{title_text}</h2>
                <p>{body_text}</p>
            </div>

            <!-- Group 1: Brightness & Contrast -->
            <div class="filter-group active">
                <div class="filter-header">Brightness / Contrast</div>
                <div class="filter-controls">
                    <div class="control-row">
                        <div class="control-label">
                            <span>Brightness</span>
                            <span class="val-display" id="val-brightness">100%</span>
                        </div>
                        <input type="range" id="brightness" data-filter="brightness" data-unit="%" min="0" max="200" value="100">
                    </div>
                    <div class="control-row">
                        <div class="control-label">
                            <span>Contrast</span>
                            <span class="val-display" id="val-contrast">100%</span>
                        </div>
                        <input type="range" id="contrast" data-filter="contrast" data-unit="%" min="0" max="200" value="100">
                    </div>
                    <div class="action-buttons">
                        <button class="btn accept" onclick="alert('Changes Applied!')">Accept</button>
                        <button class="btn reset" data-group="bc">Reset</button>
                    </div>
                </div>
            </div>

            <!-- Group 2: Color Adjustment -->
            <div class="filter-group">
                <div class="filter-header">Hue / Saturation</div>
                <div class="filter-controls">
                    <div class="control-row">
                        <div class="control-label">
                            <span>Hue Rotate</span>
                            <span class="val-display" id="val-hue">0deg</span>
                        </div>
                        <input type="range" id="hue" data-filter="hue-rotate" data-unit="deg" min="0" max="360" value="0">
                    </div>
                    <div class="control-row">
                        <div class="control-label">
                            <span>Saturation</span>
                            <span class="val-display" id="val-saturate">100%</span>
                        </div>
                        <input type="range" id="saturate" data-filter="saturate" data-unit="%" min="0" max="300" value="100">
                    </div>
                    <div class="action-buttons">
                        <button class="btn accept" onclick="alert('Changes Applied!')">Accept</button>
                        <button class="btn reset" data-group="hs">Reset</button>
                    </div>
                </div>
            </div>

            <!-- Group 3: Blur Effects -->
            <div class="filter-group">
                <div class="filter-header">Lens Blur</div>
                <div class="filter-controls">
                    <div class="control-row">
                        <div class="control-label">
                            <span>Strength</span>
                            <span class="val-display" id="val-blur">0px</span>
                        </div>
                        <input type="range" id="blur" data-filter="blur" data-unit="px" min="0" max="20" value="0" step="0.5">
                    </div>
                    <div class="action-buttons">
                        <button class="btn accept" onclick="alert('Changes Applied!')">Accept</button>
                        <button class="btn reset" data-group="blur">Reset</button>
                    </div>
                </div>
            </div>

        </aside>
        
        <main class="canvas-area">
            <!-- Sample high-res image -->
            <img src="https://images.unsplash.com/photo-1506744626753-eda8151a74a0?ixlib=rb-4.0.3&auto=format&fit=crop&w=1200&q=80" id="target-image" alt="Landscape to edit">
        </main>
    </div>

    <script src="script.js"></script>
</body>
</html>"""

    js = """document.addEventListener('DOMContentLoaded', () => {
    // === Accordion Logic ===
    const headers = document.querySelectorAll('.filter-header');
    
    headers.forEach(header => {
        header.addEventListener('click', () => {
            const group = header.parentElement;
            
            // If already active, close it
            if (group.classList.contains('active')) {
                group.classList.remove('active');
                return;
            }
            
            // Close all others
            document.querySelectorAll('.filter-group').forEach(g => g.classList.remove('active'));
            
            // Open clicked
            group.classList.add('active');
        });
    });

    // === Filter Logic ===
    const targetImage = document.getElementById('target-image');
    const ranges = document.querySelectorAll('input[type="range"]');
    
    // Default state map
    const defaultValues = {
        brightness: 100,
        contrast: 100,
        hue: 0,
        saturate: 100,
        blur: 0
    };

    // Current state map
    const currentValues = { ...defaultValues };

    function applyFilters() {
        // Construct the CSS filter string
        const filterString = `
            brightness(${currentValues.brightness}%)
            contrast(${currentValues.contrast}%)
            hue-rotate(${currentValues.hue}deg)
            saturate(${currentValues.saturate}%)
            blur(${currentValues.blur}px)
        `;
        targetImage.style.filter = filterString;
    }

    function updateControlDisplay(inputObj) {
        const id = inputObj.id;
        const displaySpan = document.getElementById(`val-${id}`);
        const unit = inputObj.getAttribute('data-unit');
        if(displaySpan) {
            displaySpan.textContent = inputObj.value + unit;
        }
    }

    // Attach Input Event Listeners
    ranges.forEach(range => {
        range.addEventListener('input', (e) => {
            const id = e.target.id;
            currentValues[id] = e.target.value;
            updateControlDisplay(e.target);
            applyFilters();
        });
    });

    // === Reset Button Logic ===
    const resetButtons = document.querySelectorAll('.btn.reset');
    
    resetButtons.forEach(btn => {
        btn.addEventListener('click', (e) => {
            const groupType = e.target.getAttribute('data-group');
            let idsToReset = [];
            
            if (groupType === 'bc') idsToReset = ['brightness', 'contrast'];
            if (groupType === 'hs') idsToReset = ['hue', 'saturate'];
            if (groupType === 'blur') idsToReset = ['blur'];

            idsToReset.forEach(id => {
                const input = document.getElementById(id);
                input.value = defaultValues[id];
                currentValues[id] = defaultValues[id];
                updateControlDisplay(input);
            });
            
            applyFilters();
        });
    });
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
