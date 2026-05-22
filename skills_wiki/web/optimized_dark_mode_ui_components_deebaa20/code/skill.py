def create_component(
    output_dir: str,
    title_text: str = "Pumpkin Mead",
    body_text: str = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam.",
    color_scheme: str = "dark",
    accent_color: str = "#14b8a6",
    width_px: int = 1000,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Optimized Dark Mode UI card effect.
    Includes a theme toggle to demonstrate the 'Provide Options' tip.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Base HTML structure
    html = f"""<!DOCTYPE html>
<html lang="en" data-theme="{color_scheme}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Optimized Dark Mode UI</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="layout-container">
        
        <!-- Tip 5: Provide Options (Theme Toggle) -->
        <div class="theme-controls">
            <span class="theme-label">Dark Mode</span>
            <label class="switch">
                <input type="checkbox" id="theme-toggle" {"checked" if color_scheme == "light" else ""}>
                <span class="slider round"></span>
            </label>
            <span class="theme-label">Light Mode</span>
        </div>

        <div class="card">
            <div class="card-image-area">
                <svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg" class="placeholder-icon">
                    <circle cx="50" cy="50" r="30" stroke="currentColor" stroke-width="4" fill="none" opacity="0.3" />
                    <path d="M 40 60 L 50 40 L 60 60" stroke="currentColor" stroke-width="4" stroke-linecap="round" stroke-linejoin="round" fill="none" opacity="0.5" />
                </svg>
            </div>
            
            <div class="card-content">
                <!-- Header Tabs area simulating the video UI -->
                <div class="details-header">
                    <div class="tab active">Details:</div>
                    <div class="tab">Specifications:</div>
                </div>

                <!-- Tip 3: Softer Colours (Body Text) -->
                <p class="description">{body_text}</p>
                
                <!-- Tip 1 & 4: Accent Colour used sparingly as a CTA -->
                <button class="buy-button">Buy Now</button>
            </div>
        </div>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # CSS Structure implementing all dark mode tips
    css = f"""/* Optimized Dark Mode Tips Implementation */

*, *::before, *::after {{
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}}

/* --- THEME VARIABLES --- */
:root[data-theme="dark"] {{
    /* Tip 6: Tinted dark backgrounds (Slate), not pure #000000 */
    --page-bg: #0f172a; 
    --card-bg: #1e293b;
    --image-bg: linear-gradient(145deg, #334155, #1e293b);
    
    /* Tip 3: Softer Colours (No pure white) */
    --text-primary: #f8fafc; /* Very light grey/blue */
    --text-secondary: #94a3b8; /* Mid-grey */
    --text-icon: #cbd5e1;
    
    /* Tip 1 & 4: Vibrant Colours (Controlled accent) */
    --accent: {accent_color};
    --btn-text: #042f2e; /* High contrast dark text on vibrant button */
    
    /* Tip 2: Better Shadows (Pure black with high blur) */
    --shadow-color: rgba(0, 0, 0, 0.6);
    --shadow-border: rgba(255, 255, 255, 0.05);
}}

:root[data-theme="light"] {{
    --page-bg: #f1f5f9;
    --card-bg: #ffffff;
    --image-bg: linear-gradient(145deg, #e2e8f0, #f8fafc);
    
    --text-primary: #0f172a;
    --text-secondary: #475569;
    --text-icon: #64748b;
    
    --accent: {accent_color};
    --btn-text: #ffffff;
    
    --shadow-color: rgba(0, 0, 0, 0.08);
    --shadow-border: rgba(0, 0, 0, 0.05);
}}

body {{
    font-family: 'Inter', sans-serif;
    background-color: var(--page-bg);
    color: var(--text-primary);
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
    transition: background-color 0.3s ease, color 0.3s ease;
    overflow-x: hidden;
}}

.layout-container {{
    width: {width_px}px;
    height: {height_px}px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 40px;
}}

/* --- THEME TOGGLE STYLES --- */
.theme-controls {{
    display: flex;
    align-items: center;
    gap: 12px;
    font-size: 0.9rem;
    color: var(--text-secondary);
    font-weight: 500;
}}

.switch {{
    position: relative;
    display: inline-block;
    width: 50px;
    height: 26px;
}}
.switch input {{
    opacity: 0;
    width: 0;
    height: 0;
}}
.slider {{
    position: absolute;
    cursor: pointer;
    top: 0; left: 0; right: 0; bottom: 0;
    background-color: var(--card-bg);
    border: 1px solid var(--shadow-border);
    transition: .4s;
}}
.slider:before {{
    position: absolute;
    content: "";
    height: 18px;
    width: 18px;
    left: 3px;
    bottom: 3px;
    background-color: var(--accent);
    transition: .4s;
}}
input:checked + .slider:before {{
    transform: translateX(24px);
}}
.slider.round {{
    border-radius: 34px;
}}
.slider.round:before {{
    border-radius: 50%;
}}

/* --- CARD COMPONENT --- */
.card {{
    width: 360px;
    background-color: var(--card-bg);
    border-radius: 12px;
    overflow: hidden;
    /* Tip 2: Implementing the pure black soft shadow */
    box-shadow: 0 20px 40px var(--shadow-color);
    border: 1px solid var(--shadow-border);
    transition: transform 0.3s ease, background-color 0.3s ease, box-shadow 0.3s ease;
}}

.card:hover {{
    transform: translateY(-5px);
}}

.card-image-area {{
    height: 240px;
    background: var(--image-bg);
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--text-icon);
}}

.placeholder-icon {{
    width: 80px;
    height: 80px;
}}

.card-content {{
    padding: 30px;
}}

.details-header {{
    display: flex;
    gap: 24px;
    margin-bottom: 20px;
    font-size: 0.95rem;
    font-weight: 600;
}}

.tab {{
    color: var(--text-secondary);
    padding-bottom: 8px;
    position: relative;
    cursor: pointer;
}}

.tab.active {{
    color: var(--text-primary);
}}

/* Tip 1: Accent color used for small detail hierarchy */
.tab.active::after {{
    content: '';
    position: absolute;
    bottom: 0;
    left: 0;
    width: 100%;
    height: 2px;
    background-color: var(--accent);
    border-radius: 2px;
}}

.description {{
    /* Tip 3: Softer color for body copy to prevent halation */
    color: var(--text-secondary);
    font-size: 0.9rem;
    line-height: 1.6;
    margin-bottom: 30px;
}}

.buy-button {{
    width: 100%;
    padding: 14px;
    border: none;
    border-radius: 6px;
    /* Tip 1: Accent color used for primary action block */
    background-color: var(--accent);
    color: var(--btn-text);
    font-size: 1rem;
    font-weight: 600;
    cursor: pointer;
    transition: filter 0.2s ease, transform 0.1s ease;
}}

.buy-button:hover {{
    filter: brightness(1.15);
}}
.buy-button:active {{
    transform: scale(0.98);
}}
"""

    # JavaScript to handle theme toggling
    js = """// Handle Theme Toggling
document.addEventListener('DOMContentLoaded', () => {
    const themeToggle = document.getElementById('theme-toggle');
    const root = document.documentElement;

    themeToggle.addEventListener('change', (e) => {
        if (e.target.checked) {
            root.setAttribute('data-theme', 'light');
        } else {
            root.setAttribute('data-theme', 'dark');
        }
    });
});
"""

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
