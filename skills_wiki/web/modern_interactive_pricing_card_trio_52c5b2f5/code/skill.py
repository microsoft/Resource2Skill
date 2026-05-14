def create_component(
    output_dir: str,
    title_text: str = "Choose Your Plan",
    body_text: str = "Simple, transparent pricing for teams of all sizes.",
    color_scheme: str = "light",       # "dark" or "light"
    accent_color: str = "#5222d0",     # Primary accent (Purple in video)
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Modern Interactive Pricing Card Trio.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors ===
    # The original video uses a vibrant gradient background and white cards.
    # We adapt it cleanly for the requested color_scheme.
    if color_scheme == "dark":
        bg_gradient = "linear-gradient(45deg, #1a1a2e 0%, #16213e 100%)"
        card_bg = "#0f3460"
        text_primary = "#f0f0f0"
        text_secondary = "#a0a0a0"
        card_shadow = "rgba(0, 0, 0, 0.5)"
    else:
        # Replicating the video's vibrant gradient
        bg_gradient = f"linear-gradient(45deg, {accent_color} 0%, #ec615b 100%)"
        card_bg = "#ffffff"
        text_primary = "#333333"
        text_secondary = "#777777"
        card_shadow = "rgba(0, 0, 0, 0.22)"

    # Pricing Data Structure to generate HTML dynamically
    plans = [
        {
            "name": "STARTER",
            "icon": "fa-paper-plane",
            "price": "10",
            "features": [
                {"text": "1 full user", "inc": True},
                {"text": "5 contacts per client", "inc": True},
                {"text": "Advanced analytics", "inc": False},
                {"text": "24/7 Priority Support", "inc": False}
            ]
        },
        {
            "name": "PROFESSIONAL",
            "icon": "fa-rocket",
            "price": "25",
            "features": [
                {"text": "5 full users", "inc": True},
                {"text": "20 contacts per client", "inc": True},
                {"text": "Advanced analytics", "inc": True},
                {"text": "24/7 Priority Support", "inc": False}
            ]
        },
        {
            "name": "BUSINESS",
            "icon": "fa-user-astronaut",
            "price": "45",
            "features": [
                {"text": "20 full users", "inc": True},
                {"text": "Unlimited contacts", "inc": True},
                {"text": "Advanced analytics", "inc": True},
                {"text": "24/7 Priority Support", "inc": True}
            ]
        }
    ]

    cards_html = ""
    for plan in plans:
        features_html = ""
        for f in plan['features']:
            if f['inc']:
                features_html += f'<li class="inc"><i class="fas fa-check"></i> {f["text"]}</li>\n'
            else:
                features_html += f'<li class="exc"><i class="fas fa-times"></i> {f["text"]}</li>\n'

        cards_html += f"""
        <div class="card-wrapper">
            <div class="card-header">
                <i class="fas {plan['icon']} fa-4x header-icon"></i>
                <h2>{plan['name']}</h2>
            </div>
            <div class="card-detail">
                <ul>
                    {features_html}
                </ul>
            </div>
            <div class="card-price">
                <p><sup>$</sup>{plan['price']}<sub>/month</sub></p>
            </div>
            <button class="card-button">I WANT IT</button>
        </div>
        """

    # === CSS ===
    css = f"""/* Modern Interactive Pricing Card Trio */
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;800&display=swap');

*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --accent: {accent_color};
    --bg-gradient: {bg_gradient};
    --card-bg: {card_bg};
    --text-primary: {text_primary};
    --text-secondary: {text_secondary};
    --shadow: {card_shadow};
    --color-success: #28a745;
    --color-error: #ec615b;
}}

body {{
    font-family: 'Poppins', sans-serif;
    background-image: var(--bg-gradient);
    background-attachment: fixed;
    color: var(--text-primary);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
}}

.page-container {{
    width: 100%;
    max-width: {width_px}px;
    min-height: {height_px}px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 3rem 1rem;
}}

.page-header {{
    text-align: center;
    margin-bottom: 3rem;
    color: #fff;
    text-shadow: 0 2px 4px rgba(0,0,0,0.2);
}}

.page-header h1 {{
    font-size: 2.5rem;
    font-weight: 800;
    margin-bottom: 0.5rem;
}}

.page-header p {{
    font-size: 1.1rem;
    font-weight: 300;
    opacity: 0.9;
}}

.pricing-grid {{
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 2rem;
    width: 100%;
}}

/* Card Container */
.card-wrapper {{
    background-color: var(--card-bg);
    width: 320px;
    border-radius: 20px;
    box-shadow: 0 5px 14px var(--shadow);
    padding: 2rem 1.5rem;
    display: flex;
    flex-direction: column;
    align-items: center;
    transition: transform 0.3s ease-in-out, box-shadow 0.3s ease-in-out;
}}

.card-wrapper:hover {{
    transform: scale(1.08);
    box-shadow: 0 15px 30px var(--shadow);
}}

/* Card Header */
.card-header {{
    text-align: center;
    margin-bottom: 1.5rem;
    width: 100%;
}}

.header-icon {{
    color: var(--text-primary);
    margin-bottom: 1.5rem;
    opacity: 0.8;
    transition: color 0.3s ease;
}}

.card-wrapper:hover .header-icon {{
    color: var(--accent);
}}

.card-header h2 {{
    font-size: 1.3rem;
    letter-spacing: 2px;
    transition: color 0.3s ease-in-out;
}}

.card-wrapper:hover .card-header h2 {{
    color: var(--accent);
}}

/* Features List */
.card-detail {{
    width: 100%;
    margin-bottom: 1.5rem;
    border-bottom: 1px solid rgba(128, 128, 128, 0.2);
    padding-bottom: 1.5rem;
}}

.card-detail ul {{
    list-style: none;
    display: flex;
    flex-direction: column;
    gap: 0.8rem;
}}

.card-detail li {{
    font-size: 0.9rem;
    color: var(--text-secondary);
    display: flex;
    align-items: center;
    gap: 10px;
}}

.card-detail li i {{
    width: 16px;
    text-align: center;
}}

.card-detail li.inc i {{ color: var(--color-success); }}
.card-detail li.exc i {{ color: var(--color-error); }}

/* Pricing */
.card-price {{
    margin-bottom: 1.5rem;
    text-align: center;
}}

.card-price p {{
    font-size: 3.5rem;
    font-weight: 800;
    line-height: 1;
    display: flex;
    align-items: flex-start;
    justify-content: center;
}}

.card-price sup {{
    font-size: 1.5rem;
    font-weight: 600;
    margin-top: 0.5rem;
    margin-right: 0.2rem;
}}

.card-price sub {{
    font-size: 1rem;
    font-weight: 400;
    align-self: flex-end;
    margin-bottom: 0.5rem;
    margin-left: 0.2rem;
    color: var(--text-secondary);
}}

/* Button */
.card-button {{
    width: 100%;
    padding: 0.8rem 0;
    border-radius: 30px;
    border: 2px solid var(--accent);
    background-color: var(--accent);
    color: #ffffff;
    font-size: 1rem;
    font-weight: 600;
    font-family: inherit;
    cursor: pointer;
    transition: all 0.3s ease-in-out;
}}

.card-wrapper:hover .card-button {{
    background-color: transparent;
    color: var(--accent);
}}
"""

    # === HTML ===
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text}</title>
    <!-- FontAwesome CDN for Icons -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="page-container">
        <header class="page-header">
            <h1>{title_text}</h1>
            <p>{body_text}</p>
        </header>

        <section class="pricing-grid">
            {cards_html}
        </section>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    # While the core effect is pure CSS, we add a simple interaction script to make the buttons functional.
    js = f"""// Pricing Table Interactivity
document.addEventListener('DOMContentLoaded', () => {{
    const buttons = document.querySelectorAll('.card-button');

    buttons.forEach(button => {{
        button.addEventListener('click', (e) => {{
            // Find the tier name relative to the clicked button
            const card = e.target.closest('.card-wrapper');
            const tierName = card.querySelector('h2').innerText;

            // Visual feedback on click
            const originalText = e.target.innerText;
            e.target.innerText = "Processing...";
            e.target.style.opacity = "0.7";
            
            setTimeout(() => {{
                alert(`You selected the ${{tierName}} plan!`);
                e.target.innerText = originalText;
                e.target.style.opacity = "1";
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
