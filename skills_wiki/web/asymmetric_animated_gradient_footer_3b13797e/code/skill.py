def create_component(
    output_dir: str,
    title_text: str = "xTyle",
    body_text: str = "Subscribe to our channel to watch more videos on website development and press the bell icon to get immediate notification of latest videos.",
    color_scheme: str = "dark",        
    accent_color: str = "#00bfff",     
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Asymmetric Animated Gradient Footer.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme ===
    if color_scheme == "dark":
        bg_gradient = "linear-gradient(to right, #00093c, #2d0b00)"
        text_color = "#ffffff"
        line_bg = "#767676"
        icon_bg = "#ffffff"
        icon_color = "#000000"
    else:
        bg_gradient = "linear-gradient(to right, #eef8ff, #d0e8f2)"
        text_color = "#1a1a2e"
        line_bg = "#b0c4de"
        icon_bg = "#1a1a2e"
        icon_color = "#ffffff"

    # === CSS ===
    css = f"""/* Asymmetric Animated Gradient Footer */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg-gradient: {bg_gradient};
    --text-color: {text_color};
    --line-bg: {line_bg};
    --icon-bg: {icon_bg};
    --icon-color: {icon_color};
    --accent: {accent_color};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background: #f4f7f6;
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
}}

.container {{
    width: 100%;
    max-width: var(--width);
    min-height: var(--height);
    position: relative;
    background: #ffffff;
    overflow: hidden;
    box-shadow: 0 20px 40px rgba(0,0,0,0.1);
    display: flex;
    flex-direction: column;
}}

.content-placeholder {{
    flex: 1;
    padding: 60px;
    font-size: 24px;
    color: #a0a0a0;
    text-align: center;
}}

/* Footer Core Styles */
footer {{
    width: 100%;
    position: absolute;
    bottom: 0;
    background: var(--bg-gradient);
    color: var(--text-color);
    padding: 80px 0 30px;
    border-top-left-radius: 125px;
    font-size: 13px;
    line-height: 22px;
}}

.row {{
    width: 85%;
    margin: auto;
    display: flex;
    flex-wrap: wrap;
    align-items: flex-start;
    justify-content: space-between;
}}

.col {{
    flex-basis: 25%;
    padding: 10px;
}}

.col:nth-child(2), .col:nth-child(3) {{
    flex-basis: 15%;
}}

.logo {{
    width: auto;
    margin-bottom: 30px;
    font-size: 32px;
    font-weight: 700;
    letter-spacing: -1px;
}}

.col h3 {{
    width: fit-content;
    margin-bottom: 40px;
    position: relative;
    font-size: 16px;
    font-weight: 600;
}}

.email-id {{
    width: fit-content;
    border-bottom: 1px solid var(--line-bg);
    margin: 20px 0;
    padding-bottom: 5px;
}}

/* List Links */
ul li {{
    list-style: none;
    margin-bottom: 12px;
}}

ul li a {{
    text-decoration: none;
    color: var(--text-color);
    transition: color 0.3s ease;
}}

ul li a:hover {{
    color: var(--accent);
}}

/* Newsletter Form */
form {{
    padding-bottom: 15px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    border-bottom: 1px solid var(--line-bg);
    margin-bottom: 40px;
}}

form .fa-envelope {{
    font-size: 18px;
    margin-right: 15px;
}}

form input {{
    width: 100%;
    background: transparent;
    color: var(--text-color);
    border: 0;
    outline: none;
    font-family: inherit;
}}

form input::placeholder {{
    color: var(--line-bg);
    opacity: 0.8;
}}

form button {{
    background: transparent;
    border: 0;
    outline: none;
    cursor: pointer;
}}

form button .fa-arrow-right {{
    font-size: 16px;
    color: var(--text-color);
    transition: transform 0.3s ease, color 0.3s ease;
}}

form button:hover .fa-arrow-right {{
    color: var(--accent);
    transform: translateX(4px);
}}

/* Social Icons */
.social-icons .fab {{
    width: 36px;
    height: 36px;
    border-radius: 50%;
    text-align: center;
    line-height: 36px;
    font-size: 16px;
    color: var(--icon-color);
    background: var(--icon-bg);
    margin-right: 12px;
    cursor: pointer;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}}

.social-icons .fab:hover {{
    background: var(--accent);
    color: #fff;
    transform: translateY(-4px);
    box-shadow: 0 5px 15px rgba(0,0,0,0.2);
}}

hr {{
    width: 90%;
    border: 0;
    border-bottom: 1px solid var(--line-bg);
    margin: 30px auto 20px;
    opacity: 0.3;
}}

.copyright {{
    text-align: center;
    opacity: 0.8;
}}

/* Animated Scanning Underline */
.underline {{
    width: 100%;
    height: 4px;
    background: var(--line-bg);
    border-radius: 2px;
    position: absolute;
    top: 28px;
    left: 0;
    overflow: hidden;
    opacity: 0.5;
}}

.underline span {{
    width: 15px;
    height: 100%;
    background: var(--accent);
    border-radius: 2px;
    position: absolute;
    top: 0;
    left: 10px;
    animation: scanner 2s linear infinite;
}}

@keyframes scanner {{
    0% {{ left: -20px; }}
    100% {{ left: 100%; }}
}}

/* Responsive Design */
@media (max-width: 768px) {{
    footer {{
        position: relative;
        border-top-left-radius: 80px;
        padding-top: 60px;
    }}
    .col {{
        flex-basis: 100%;
        margin-bottom: 30px;
    }}
    .col:nth-child(2), .col:nth-child(3) {{
        flex-basis: 100%;
    }}
    .container {{
        height: auto;
    }}
}}
"""

    # === HTML ===
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text} - Footer</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        <!-- Main Content Area Placeholder -->
        <div class="content-placeholder">
            Scroll down to view footer
        </div>

        <!-- Footer Component -->
        <footer>
            <div class="row">
                <div class="col">
                    <h2 class="logo">{title_text}</h2>
                    <p>{body_text}</p>
                </div>
                <div class="col">
                    <h3>Office <div class="underline"><span></span></div></h3>
                    <p>ITPL Road</p>
                    <p>Whitefield, Bangalore</p>
                    <p>Karnataka, PIN 560066, India</p>
                    <p class="email-id">hello@example.com</p>
                    <h4>+91 - 0123456789</h4>
                </div>
                <div class="col">
                    <h3>Links <div class="underline"><span></span></div></h3>
                    <ul>
                        <li><a href="#">Home</a></li>
                        <li><a href="#">Services</a></li>
                        <li><a href="#">About Us</a></li>
                        <li><a href="#">Features</a></li>
                        <li><a href="#">Contacts</a></li>
                    </ul>
                </div>
                <div class="col">
                    <h3>Newsletter <div class="underline"><span></span></div></h3>
                    <form id="newsletter-form">
                        <i class="far fa-envelope"></i>
                        <input type="email" placeholder="Enter your email id" required>
                        <button type="submit" aria-label="Subscribe"><i class="fas fa-arrow-right"></i></button>
                    </form>
                    <div class="social-icons">
                        <i class="fab fa-facebook-f" aria-hidden="true"></i>
                        <i class="fab fa-twitter" aria-hidden="true"></i>
                        <i class="fab fa-whatsapp" aria-hidden="true"></i>
                        <i class="fab fa-pinterest" aria-hidden="true"></i>
                    </div>
                </div>
            </div>
            <hr>
            <p class="copyright">{title_text} © 2024 - All Rights Reserved.</p>
        </footer>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Footer Interactive Behavior
document.addEventListener('DOMContentLoaded', () => {{
    const form = document.getElementById('newsletter-form');
    
    if(form) {{
        form.addEventListener('submit', (e) => {{
            e.preventDefault();
            const input = form.querySelector('input[type="email"]');
            
            if(input && input.value) {{
                // Provide visual feedback instead of page reload
                const btn = form.querySelector('button');
                const originalIcon = btn.innerHTML;
                
                btn.innerHTML = '<i class="fas fa-check" style="color: var(--accent);"></i>';
                
                setTimeout(() => {{
                    alert(`Thank you for subscribing with ${{input.value}}!`);
                    input.value = '';
                    btn.innerHTML = originalIcon;
                }}, 300);
            }}
        }});
    }}
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
