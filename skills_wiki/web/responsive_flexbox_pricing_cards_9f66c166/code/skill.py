def create_component(
    output_dir: str,
    title_text: str = "Choose Your Plan",
    body_text: str = "Simple, transparent pricing for everyone.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#93cb52",     # Default green from the tutorial
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Responsive Pricing Table visual effect.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Theme handling (Note: Cards are always white to match tutorial contrast style)
    if color_scheme == "dark":
        bg_color = "#333333"
        header_text_color = "#ffffff"
        card_shadow = "none"
    else:
        bg_color = "#f4f7f6"
        header_text_color = "#333333"
        card_shadow = "0 10px 30px rgba(0,0,0,0.08)"

    # === CSS ===
    css = f"""/* Responsive Pricing Table */
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600&display=swap');

*, *::before, *::after {{
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}}

:root {{
    --bg-main: {bg_color};
    --header-text: {header_text_color};
    --accent: {accent_color};
    --card-bg: #ffffff;
    --card-text: #333333;
}}

body {{
    font-family: 'Poppins', sans-serif;
    background: var(--bg-main);
    color: var(--header-text);
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 2rem;
}}

.page-header {{
    text-align: center;
    margin-bottom: 3rem;
}}

.page-header h1 {{
    font-size: 2.5rem;
    font-weight: 600;
    margin-bottom: 0.5rem;
}}

.page-header p {{
    font-size: 1.1rem;
    font-weight: 300;
    opacity: 0.8;
}}

.container {{
    width: 100%;
    max-width: {width_px}px;
    margin: 0 auto;
}}

.tbl_row {{
    display: flex;
    justify-content: center;
    align-items: stretch;
    gap: 2rem;
}}

.tbl_col {{
    flex: 1;
    background: var(--card-bg);
    color: var(--card-text);
    border-radius: 8px;
    text-align: center;
    padding: 2.5rem 0;
    box-shadow: {card_shadow};
    overflow: hidden;
    transition: transform 0.3s ease;
}}

.tbl_col:hover {{
    transform: translateY(-5px);
}}

/* Card Title */
.tbl_col > p {{
    font-size: 22px;
    font-weight: 500;
    letter-spacing: 1px;
    text-transform: uppercase;
}}

/* Price Block */
.tbl_col h3 {{
    font-size: 3rem;
    margin: 20px 0 40px;
    font-weight: 600;
    background: var(--accent);
    color: #ffffff;
    padding: 25px 0;
}}

.tbl_col h3 span {{
    font-size: 1.2rem;
    font-weight: 400;
    opacity: 0.9;
}}

/* Feature List */
.tbl_col ul {{
    text-align: left;
    margin: 0 auto;
    width: max-content;
    list-style: none;
    margin-bottom: 40px;
}}

.tbl_col ul li {{
    margin: 1.2rem 0;
    font-size: 15px;
    font-weight: 400;
    position: relative;
    padding-left: 25px;
}}

/* Custom Bullet (Checkmark) */
.tbl_col ul li::before {{
    content: "\\2714"; /* Unicode Checkmark */
    color: var(--accent);
    position: absolute;
    left: 0;
    font-size: 16px;
    font-weight: bold;
}}

/* Button */
.tbl_col button {{
    width: 75%;
    border: 2px solid var(--accent);
    background: transparent;
    color: var(--card-text);
    padding: 14px 0;
    border-radius: 5px;
    font-size: 16px;
    font-weight: 500;
    font-family: inherit;
    cursor: pointer;
    transition: all 0.4s ease;
}}

.tbl_col button:hover {{
    background: var(--accent);
    color: #ffffff;
}}

/* Responsive Breakpoint */
@media (max-width: 850px) {{
    .tbl_row {{
        flex-direction: column;
        align-items: center;
    }}
    
    .tbl_col {{
        width: 100%;
        max-width: 450px;
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
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="page-header">
        <h1>{title_text}</h1>
        <p>{body_text}</p>
    </div>

    <div class="container">
        <div class="tbl_row">
            <!-- Card 1 -->
            <div class="tbl_col">
                <p>Basic</p>
                <h3>$2.95 <span>/ Month</span></h3>
                <ul>
                    <li>Top Features</li>
                    <li>1 Website</li>
                    <li>10 GB SSD Storage</li>
                    <li>Custom Themes</li>
                    <li>24/7 Customer Support</li>
                    <li>Free Domain 1 Year</li>
                </ul>
                <button class="select-btn" data-plan="Basic">Select Now</button>
            </div>

            <!-- Card 2 -->
            <div class="tbl_col">
                <p>Plus</p>
                <h3>$5.45 <span>/ Month</span></h3>
                <ul>
                    <li>Top Features</li>
                    <li>Unlimited Websites</li>
                    <li>20 GB SSD Storage</li>
                    <li>Custom Themes</li>
                    <li>24/7 Customer Support</li>
                    <li>Free Domain 1 Year</li>
                </ul>
                <button class="select-btn" data-plan="Plus">Select Now</button>
            </div>

            <!-- Card 3 -->
            <div class="tbl_col">
                <p>Choice Plus</p>
                <h3>$13.95 <span>/ Month</span></h3>
                <ul>
                    <li>Top Features</li>
                    <li>Unlimited Websites</li>
                    <li>40 GB SSD Storage</li>
                    <li>Custom Themes</li>
                    <li>24/7 Customer Support</li>
                    <li>Free Domain 1 Year</li>
                </ul>
                <button class="select-btn" data-plan="Choice Plus">Select Now</button>
            </div>
        </div>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Responsive Pricing Table Interactions
document.addEventListener('DOMContentLoaded', () => {{
    const buttons = document.querySelectorAll('.select-btn');

    buttons.forEach(button => {{
        button.addEventListener('click', (e) => {{
            const planName = e.target.getAttribute('data-plan');
            
            // Visual feedback
            const originalText = e.target.innerText;
            e.target.innerText = 'Processing...';
            e.target.style.opacity = '0.8';
            
            // Simulate action
            setTimeout(() => {{
                alert(`You have selected the ${{planName}} plan!`);
                e.target.innerText = originalText;
                e.target.style.opacity = '1';
            }}, 400);
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
