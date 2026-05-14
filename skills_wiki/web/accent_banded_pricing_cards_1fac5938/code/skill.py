def create_component(
    output_dir: str,
    title_text: str = "PRICING FOR YOU",
    body_text: str = "Choose the plan that best fits your goals.",
    color_scheme: str = "dark",
    accent_color: str = "#fd3c4d",
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the 'Accent-Banded Pricing Cards' visual effect.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Theme colors configuration
    if color_scheme == "dark":
        bg_color = "#191a1f"
        card_bg = "#24272e"
        text_color = "#ffffff"
        text_muted = "rgba(255, 255, 255, 0.7)"
        shadow_base = "rgba(0, 0, 0, 0.2)"
        shadow_hover = "rgba(0, 0, 0, 0.4)"
    else:
        bg_color = "#f0f2f5"
        card_bg = "#ffffff"
        text_color = "#1a1a2e"
        text_muted = "rgba(0, 0, 0, 0.6)"
        shadow_base = "rgba(0, 0, 0, 0.05)"
        shadow_hover = "rgba(0, 0, 0, 0.15)"

    # Format title to highlight the first word
    words = title_text.split()
    if len(words) > 0:
        first_word = words[0]
        rest_of_title = " ".join(words[1:])
        formatted_title = f"<span>{first_word}</span> {rest_of_title}"
    else:
        formatted_title = f"<span>{title_text}</span>"

    # Static data for cards
    plans = [
        {
            "name": "Beginner Plan",
            "price": "$50",
            "contract": "1 Month Contract",
            "features": ["Classes 2 Weeks", "Open Gym Monday-Friday", "Yoga Relax classes", "Free drinking package"]
        },
        {
            "name": "Advanced Plan",
            "price": "$150",
            "contract": "6 Month Contract",
            "features": ["Classes 6 Weeks", "Open Gym Monday-Friday", "Yoga Relax classes", "Free drinking package"]
        },
        {
            "name": "Pro Plan",
            "price": "$250",
            "contract": "12 Month Contract",
            "features": ["Classes 9 Weeks", "Open Gym Monday-Friday", "Yoga Relax classes", "Free drinking package"]
        }
    ]

    cards_html = ""
    for plan in plans:
        features_html = "".join([f"<li><span class=\"check\">&#10003;</span> {f}</li>" for f in plan['features']])
        cards_html += f"""
            <div class="pricing-card">
                <h4>{plan['name']}</h4>
                <div class="head">
                    <h3>{plan['price']}</h3>
                    <p>{plan['contract']}</p>
                </div>
                <div class="line"></div>
                <ul class="feature">
                    {features_html}
                </ul>
                <div class="btn-container">
                    <a href="#" class="btn">Get Started</a>
                </div>
            </div>
        """

    # === CSS ===
    css = f"""/* Accent-Banded Pricing Cards — generated component */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg-main: {bg_color};
    --bg-card: {card_bg};
    --text-main: {text_color};
    --text-muted: {text_muted};
    --accent: {accent_color};
    --shadow-base: {shadow_base};
    --shadow-hover: {shadow_hover};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background-color: var(--bg-main);
    color: var(--text-main);
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    overflow-x: hidden;
}}

.pricing-section {{
    width: 100%;
    max-width: var(--width);
    padding: 60px 20px;
}}

.header-container {{
    text-align: center;
    margin-bottom: 50px;
}}

.pricing-title {{
    font-size: 2.2rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 10px;
}}

.pricing-title span {{
    color: var(--accent);
}}

.pricing-subtitle {{
    color: var(--text-muted);
    font-size: 1.1rem;
}}

.pricing-table {{
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 30px;
    max-width: 1100px;
    margin: 0 auto;
}}

.pricing-card {{
    background-color: var(--bg-card);
    flex: 1 1 300px;
    max-width: 340px;
    text-align: center;
    border-radius: 8px;
    overflow: hidden;
    box-shadow: 0 10px 30px var(--shadow-base);
    
    /* Animation defaults */
    opacity: 0;
    transform: translateY(30px);
    transition: opacity 0.6s ease, transform 0.6s cubic-bezier(0.2, 0.8, 0.2, 1);
}}

/* JS Triggers this class */
.pricing-card.visible {{
    opacity: 1;
    transform: translateY(0);
}}

.pricing-card.visible:hover {{
    transform: translateY(-10px);
    box-shadow: 0 15px 40px var(--shadow-hover);
    /* Transition specifically for the hover state, maintaining opacity */
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}}

.pricing-card h4 {{
    color: var(--text-main);
    text-transform: uppercase;
    padding: 25px 0;
    font-size: 1.1rem;
    letter-spacing: 1px;
}}

.pricing-card .head {{
    background-color: var(--accent);
    color: #ffffff; /* Always white text on accent backgrounds */
    padding: 20px 0;
}}

.pricing-card .head h3 {{
    font-size: 2.5rem;
    font-weight: 700;
    margin-bottom: 5px;
}}

.pricing-card .head p {{
    font-size: 0.95rem;
    font-weight: 500;
    opacity: 0.95;
}}

.pricing-card .line {{
    background-color: var(--accent);
    width: 70%;
    height: 2px;
    margin: 25px auto;
    opacity: 0.4;
}}

.pricing-card ul {{
    list-style: none;
    padding: 0 20px;
    margin-bottom: 25px;
}}

.pricing-card li {{
    color: var(--text-main);
    margin-bottom: 15px;
    font-size: 0.95rem;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 10px;
}}

.pricing-card li .check {{
    color: var(--accent);
    font-weight: bold;
    font-size: 1.1rem;
}}

.pricing-card .btn-container {{
    padding: 0 20px 30px;
}}

.pricing-card .btn {{
    display: inline-block;
    background-color: var(--accent);
    color: #ffffff;
    text-decoration: none;
    width: 85%;
    padding: 14px 0;
    border-radius: 30px;
    text-transform: uppercase;
    font-weight: 600;
    font-size: 0.9rem;
    letter-spacing: 1px;
    transition: background-color 0.3s ease, transform 0.2s ease;
}}

.pricing-card .btn:hover {{
    filter: brightness(1.15);
    transform: scale(1.05);
}}
"""

    # === HTML ===
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <section class="pricing-section">
        <div class="header-container">
            <h2 class="pricing-title">{formatted_title}</h2>
            <p class="pricing-subtitle">{body_text}</p>
        </div>
        
        <div class="pricing-table">
{cards_html}
        </div>
    </section>
    
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Accent-Banded Pricing Cards — interactive behavior
document.addEventListener('DOMContentLoaded', () => {{
    const cards = document.querySelectorAll('.pricing-card');
    
    // Sequential fade-in and slide-up animation on load
    cards.forEach((card, index) => {{
        setTimeout(() => {{
            card.classList.add('visible');
        }}, 150 * (index + 1)); // Stagger by 150ms
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
