def create_component(
    output_dir: str,
    title_text: str = "Flexbox Playground",
    body_text: str = "Use the controls below to dynamically manipulate the CSS Flexbox properties of the container.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#0ea5e9",     # CSS hex color for accent
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Interactive Flexbox Playground visual effect.
    
    Kwargs:
        num_boxes (int): The number of colored boxes to generate (default: 8).
    """
    import os

    os.makedirs(output_dir, exist_ok=True)
    
    num_boxes = kwargs.get("num_boxes", 8)

    # === Derive theme colors ===
    if color_scheme == "dark":
        bg_color = "#0f172a"
        text_color = "#f8fafc"
        border_color = "#334155"
        surface_color = "#1e293b"
        surface_light = "#020617" 
    else:
        bg_color = "#f8fafc"
        text_color = "#0f172a"
        border_color = "#cbd5e1"
        surface_color = "#ffffff"
        surface_light = "#e2e8f0"

    # Generate the boxes HTML with a rainbow HSL spread
    boxes_html = ""
    for i in range(1, num_boxes + 1):
        hue = int((i - 1) * (360 / num_boxes))
        bg_color_box = f"hsl({hue}, 85%, 65%)"
        boxes_html += f'            <div class="box" style="background-color: {bg_color_box};">{i}</div>\n'

    # === CSS ===
    css = f"""/* Flexbox Playground — generated component */
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
    --surface-light: {surface_light};
    --border: {border_color};
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
    padding: 24px;
}}

.app-container {{
    width: 100%;
    max-width: var(--width);
    height: var(--height);
    display: flex;
    flex-direction: column;
    gap: 20px;
}}

.header h1 {{
    font-size: 2rem;
    margin-bottom: 8px;
    color: var(--text);
}}

.header p {{
    color: var(--text);
    opacity: 0.8;
    line-height: 1.5;
}}

/* Controls Panel */
.controls {{
    display: flex;
    flex-wrap: wrap;
    gap: 16px;
    padding: 24px;
    background: var(--surface);
    border-radius: 12px;
    border: 1px solid var(--border);
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}}

.control-group {{
    display: flex;
    flex-direction: column;
    gap: 8px;
    flex-grow: 1;
    min-width: 140px;
}}

.control-group label {{
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: var(--accent);
    font-weight: 700;
}}

select {{
    padding: 10px 12px;
    border-radius: 8px;
    background: var(--bg);
    color: var(--text);
    border: 1px solid var(--border);
    font-family: inherit;
    font-size: 0.95rem;
    cursor: pointer;
    outline: none;
    transition: border-color 0.2s ease;
    appearance: none;
    background-image: url("data:image/svg+xml;charset=US-ASCII,%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20width%3D%22292.4%22%20height%3D%22292.4%22%3E%3Cpath%20fill%3D%22%23{accent_color.replace('#', '')}%22%20d%3D%22M287%2069.4a17.6%2017.6%200%200%200-13-5.4H18.4c-5%200-9.3%201.8-12.9%205.4A17.6%2017.6%200%200%200%200%2082.2c0%205%201.8%209.3%205.4%2012.9l128%20127.9c3.6%203.6%207.8%205.4%2012.8%205.4s9.2-1.8%2012.8-5.4L287%2095c3.5-3.5%205.4-7.8%205.4-12.8%200-5-1.9-9.2-5.5-12.8z%22%2F%3E%3C%2Fsvg%3E");
    background-repeat: no-repeat;
    background-position: right 12px top 50%;
    background-size: 10px auto;
}}

select:focus {{
    border-color: var(--accent);
}}

/* The Flexbox Target Container */
.playground-container {{
    display: flex;
    flex-grow: 1;
    border: 6px solid var(--text);
    border-radius: 16px;
    padding: 16px;
    background-color: var(--surface-light);
    overflow: auto;
    
    /* Default Flex properties applied initially */
    flex-direction: row;
    justify-content: flex-start;
    align-items: flex-start;
    flex-wrap: nowrap;
    align-content: stretch;
    gap: 16px;
}}

/* Flex Items */
.box {{
    width: 140px;
    height: 140px;
    border-radius: 16px;
    display: flex;
    justify-content: center;
    align-items: center;
    font-size: 3.5rem;
    font-weight: 800;
    color: rgba(0, 0, 0, 0.7);
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    transition: transform 0.2s cubic-bezier(0.4, 0, 0.2, 1), box-shadow 0.2s ease;
    flex-shrink: 0; /* Match the tutorial's rigid boxes initially */
}}

.box:hover {{
    transform: translateY(-6px) scale(1.02);
    box-shadow: 0 12px 24px rgba(0,0,0,0.3);
    z-index: 10;
}}

/* Specific overrides to natively demonstrate 'align-items: baseline' */
.box:nth-child(2) {{ font-size: 2rem; }}
.box:nth-child(4) {{ font-size: 5rem; }}
.box:nth-child(6) {{ font-size: 1.5rem; }}
"""

    # === HTML ===
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="app-container">
        <div class="header">
            <h1>{title_text}</h1>
            <p>{body_text}</p>
        </div>

        <div class="controls">
            <div class="control-group">
                <label>flex-direction</label>
                <select class="control-select" data-prop="flexDirection">
                    <option value="row">row</option>
                    <option value="row-reverse">row-reverse</option>
                    <option value="column">column</option>
                    <option value="column-reverse">column-reverse</option>
                </select>
            </div>
            
            <div class="control-group">
                <label>justify-content</label>
                <select class="control-select" data-prop="justifyContent">
                    <option value="flex-start">flex-start</option>
                    <option value="flex-end">flex-end</option>
                    <option value="center">center</option>
                    <option value="space-between">space-between</option>
                    <option value="space-around">space-around</option>
                    <option value="space-evenly">space-evenly</option>
                </select>
            </div>

            <div class="control-group">
                <label>align-items</label>
                <select class="control-select" data-prop="alignItems">
                    <option value="flex-start">flex-start</option>
                    <option value="flex-end">flex-end</option>
                    <option value="center">center</option>
                    <option value="baseline">baseline</option>
                    <option value="stretch">stretch</option>
                </select>
            </div>

            <div class="control-group">
                <label>flex-wrap</label>
                <select class="control-select" data-prop="flexWrap">
                    <option value="nowrap">nowrap</option>
                    <option value="wrap">wrap</option>
                    <option value="wrap-reverse">wrap-reverse</option>
                </select>
            </div>

            <div class="control-group">
                <label>align-content</label>
                <select class="control-select" data-prop="alignContent">
                    <option value="stretch">stretch</option>
                    <option value="flex-start">flex-start</option>
                    <option value="flex-end">flex-end</option>
                    <option value="center">center</option>
                    <option value="space-between">space-between</option>
                    <option value="space-around">space-around</option>
                </select>
            </div>

            <div class="control-group">
                <label>gap</label>
                <select class="control-select" data-prop="gap">
                    <option value="16px">16px</option>
                    <option value="0px">0px</option>
                    <option value="8px">8px</option>
                    <option value="32px">32px</option>
                    <option value="64px">64px</option>
                </select>
            </div>
        </div>

        <div class="playground-container" id="playground">
{boxes_html}
        </div>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Interactive Flexbox Playground — logic
document.addEventListener('DOMContentLoaded', () => {{
    const container = document.getElementById('playground');
    const selects = document.querySelectorAll('.control-select');

    // Attach event listeners to all dropdowns
    selects.forEach(select => {{
        select.addEventListener('change', (e) => {{
            const propertyToUpdate = e.target.dataset.prop;
            const newValue = e.target.value;
            
            // Directly apply the selected value to the container's inline style
            container.style[propertyToUpdate] = newValue;
        }});
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
