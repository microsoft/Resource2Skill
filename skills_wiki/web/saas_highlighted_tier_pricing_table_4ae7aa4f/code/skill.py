def create_component(
    output_dir: str,
    title_text: str = "Choose Your Plan",
    body_text: str = "Simple, transparent pricing for teams of all sizes.",
    color_scheme: str = "light",
    accent_color: str = "#fed000", # The classic SaaS Yellow/Gold
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the SaaS Highlighted Tier Pricing Table.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors ===
    if color_scheme == "dark":
        bg_color = "#0f172a"
        card_bg = "#1e293b"
        text_primary = "#f8fafc"
        text_secondary = "#94a3b8"
        border_color = "#334155"
        popular_text = "#0f172a" # Dark text on bright accent
    else:
        bg_color = "#f8f9fa"
        card_bg = "#ffffff"
        text_primary = "#1e293b"
        text_secondary = "#64748b"
        border_color = "#e2e8f0"
        popular_text = "#0f172a" # Dark text on bright accent

    # === CSS ===
    css = f"""/* SaaS Pricing Table Styles */
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg-color: {bg_color};
    --card-bg: {card_bg};
    --text-primary: {text_primary};
    --text-secondary: {text_secondary};
    --border-color: {border_color};
    --accent-color: {accent_color};
    --popular-text: {popular_text};
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
    padding: 40px 20px;
}}

.header {{
    text-align: center;
    margin-bottom: 50px;
}}

.header h1 {{
    font-size: 2.5rem;
    font-weight: 700;
    margin-bottom: 10px;
}}

.header p {{
    color: var(--text-secondary);
    font-size: 1.1rem;
}}

/* Toggle Switch */
.toggle-container {{
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 15px;
    margin-top: 25px;
    font-weight: 500;
}}

.switch {{
    position: relative;
    display: inline-block;
    width: 60px;
    height: 34px;
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
    background-color: var(--border-color);
    transition: .4s;
    border-radius: 34px;
}}

.slider:before {{
    position: absolute;
    content: "";
    height: 26px;
    width: 26px;
    left: 4px;
    bottom: 4px;
    background-color: var(--card-bg);
    transition: .4s;
    border-radius: 50%;
}}

input:checked + .slider {{
    background-color: var(--accent-color);
}}

input:checked + .slider:before {{
    transform: translateX(26px);
}}

/* Pricing Cards Container */
.pricing-wrapper {{
    display: flex;
    justify-content: center;
    align-items: center;
    flex-wrap: wrap;
    gap: 30px;
    width: 100%;
    max-width: 1100px;
}}

/* Individual Card */
.price-box {{
    background: var(--card-bg);
    border: 1px solid var(--border-color);
    border-radius: 16px;
    width: 320px;
    padding: 40px 30px;
    text-align: center;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    display: flex;
    flex-direction: column;
}}

.price-box:hover {{
    transform: translateY(-5px);
    box-shadow: 0 20px 40px rgba(0,0,0,0.08);
}}

/* Popular/Highlighted Card Override */
.price-box.popular {{
    background: var(--accent-color);
    color: var(--popular-text);
    border: none;
    transform: scale(1.05);
    box-shadow: 0 20px 40px rgba(0,0,0,0.15);
    position: relative;
}}

.price-box.popular:hover {{
    transform: scale(1.05) translateY(-5px);
}}

.popular-badge {{
    position: absolute;
    top: -15px;
    left: 50%;
    transform: translateX(-50%);
    background: var(--popular-text);
    color: var(--accent-color);
    padding: 5px 15px;
    border-radius: 20px;
    font-size: 0.8rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1px;
}}

/* Card Content */
.plan-icon {{
    font-size: 3rem;
    margin-bottom: 20px;
    color: var(--text-primary);
}}

.popular .plan-icon {{
    color: var(--popular-text);
}}

.plan-name {{
    font-size: 1.5rem;
    font-weight: 600;
    margin-bottom: 5px;
}}

.plan-desc {{
    font-size: 0.9rem;
    color: var(--text-secondary);
    margin-bottom: 25px;
}}

.popular .plan-desc {{
    color: rgba(0,0,0,0.7);
}}

.price-container {{
    display: flex;
    justify-content: center;
    align-items: baseline;
    margin-bottom: 30px;
}}

.currency {{
    font-size: 1.5rem;
    font-weight: 600;
    align-self: flex-start;
    margin-top: 5px;
}}

.price {{
    font-size: 4rem;
    font-weight: 700;
    line-height: 1;
}}

.billing-cycle {{
    font-size: 1rem;
    color: var(--text-secondary);
    margin-left: 5px;
}}

.popular .billing-cycle {{
    color: rgba(0,0,0,0.7);
}}

/* Features List */
.features {{
    list-style: none;
    text-align: left;
    margin-bottom: 40px;
    flex-grow: 1;
}}

.features li {{
    margin-bottom: 15px;
    font-size: 0.95rem;
    display: flex;
    align-items: center;
    gap: 10px;
}}

.features li i {{
    color: var(--accent-color);
    font-size: 1.1rem;
}}

.popular .features li i {{
    color: var(--popular-text);
}}

/* Buttons */
.btn {{
    display: inline-block;
    padding: 15px 0;
    width: 100%;
    border-radius: 8px;
    text-decoration: none;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    transition: all 0.3s ease;
    border: 2px solid var(--border-color);
    color: var(--text-primary);
    background: transparent;
}}

.btn:hover {{
    background: var(--text-primary);
    color: var(--card-bg);
    border-color: var(--text-primary);
}}

.popular .btn {{
    background: var(--popular-text);
    color: var(--accent-color);
    border-color: var(--popular-text);
}}

.popular .btn:hover {{
    background: transparent;
    color: var(--popular-text);
}}

/* Responsive */
@media (max-width: 1024px) {{
    .price-box.popular {{
        transform: scale(1);
    }}
    .price-box.popular:hover {{
        transform: translateY(-5px);
    }}
}}

@media (max-width: 768px) {{
    .pricing-wrapper {{
        flex-direction: column;
    }}
    .price-box {{
        width: 100%;
        max-width: 400px;
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
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    
    <div class="header">
        <h1>{title_text}</h1>
        <p>{body_text}</p>
        
        <div class="toggle-container">
            <span>Monthly</span>
            <label class="switch">
                <input type="checkbox" id="billing-toggle">
                <span class="slider"></span>
            </label>
            <span>Annually <span style="color: var(--accent-color); font-size: 0.8rem;">(Save 20%)</span></span>
        </div>
    </div>

    <div class="pricing-wrapper">
        
        <!-- Starter Plan -->
        <div class="price-box">
            <i class="fa-regular fa-paper-plane plan-icon"></i>
            <div class="plan-name">Starter</div>
            <div class="plan-desc">Perfect for small projects.</div>
            <div class="price-container">
                <span class="currency">$</span>
                <span class="price" data-monthly="16" data-yearly="12">16</span>
                <span class="billing-cycle">/mo</span>
            </div>
            <ul class="features">
                <li><i class="fa-solid fa-check"></i> 60-day chat history</li>
                <li><i class="fa-solid fa-check"></i> Basic widget customization</li>
                <li><i class="fa-solid fa-check"></i> Ticketing system</li>
                <li><i class="fa-solid fa-check"></i> Data security</li>
            </ul>
            <a href="#" class="btn">Choose Plan <i class="fa-solid fa-chevron-right" style="font-size: 0.8em; margin-left: 5px;"></i></a>
        </div>

        <!-- Popular Plan -->
        <div class="price-box popular">
            <div class="popular-badge">Popular</div>
            <i class="fa-solid fa-rocket plan-icon"></i>
            <div class="plan-name">Business</div>
            <div class="plan-desc">For growing teams & agencies.</div>
            <div class="price-container">
                <span class="currency">$</span>
                <span class="price" data-monthly="50" data-yearly="40">50</span>
                <span class="billing-cycle">/mo</span>
            </div>
            <ul class="features">
                <li><i class="fa-solid fa-check"></i> Unlimited chat history</li>
                <li><i class="fa-solid fa-check"></i> Advanced customization</li>
                <li><i class="fa-solid fa-check"></i> Ticketing system</li>
                <li><i class="fa-solid fa-check"></i> Data security</li>
                <li><i class="fa-solid fa-check"></i> Multiple brandings</li>
                <li><i class="fa-solid fa-check"></i> Basic reporting</li>
            </ul>
            <a href="#" class="btn">Choose Plan <i class="fa-solid fa-chevron-right" style="font-size: 0.8em; margin-left: 5px;"></i></a>
        </div>

        <!-- Enterprise Plan -->
        <div class="price-box">
            <i class="fa-solid fa-building plan-icon"></i>
            <div class="plan-name">Enterprise</div>
            <div class="plan-desc">Advanced security & support.</div>
            <div class="price-container">
                <span class="currency">$</span>
                <span class="price" data-monthly="80" data-yearly="64">80</span>
                <span class="billing-cycle">/mo</span>
            </div>
            <ul class="features">
                <li><i class="fa-solid fa-check"></i> Everything in Business</li>
                <li><i class="fa-solid fa-check"></i> Dedicated acc. manager</li>
                <li><i class="fa-solid fa-check"></i> Single Sign-On (SSO)</li>
                <li><i class="fa-solid fa-check"></i> HIPAA Compliance</li>
                <li><i class="fa-solid fa-check"></i> Staffing prediction</li>
            </ul>
            <a href="#" class="btn">Choose Plan <i class="fa-solid fa-chevron-right" style="font-size: 0.8em; margin-left: 5px;"></i></a>
        </div>

    </div>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Pricing Toggle Logic
document.addEventListener('DOMContentLoaded', () => {{
    const toggle = document.getElementById('billing-toggle');
    const priceElements = document.querySelectorAll('.price');

    if(toggle) {{
        toggle.addEventListener('change', (e) => {{
            const isYearly = e.target.checked;
            
            priceElements.forEach(el => {{
                // Fade out effect
                el.style.opacity = 0;
                
                setTimeout(() => {{
                    // Update value based on toggle state
                    if(isYearly) {{
                        el.textContent = el.getAttribute('data-yearly');
                    }} else {{
                        el.textContent = el.getAttribute('data-monthly');
                    }}
                    // Fade in effect
                    el.style.opacity = 1;
                }}, 200);
            }});
        }});
    }}
}});

// Add smooth transitions for opacity changes handled by JS
const style = document.createElement('style');
style.innerHTML = `
    .price {{
        transition: opacity 0.2s ease-in-out;
    }}
`;
document.head.appendChild(style);
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
