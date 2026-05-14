def create_component(
    output_dir: str,
    title_text: str = "IT'S YOUR UNIVERSE,<br>IT'S TIME TO SAVE IT",
    body_text: str = "The Rebel alliance is fighting to get rid of the evil empire. Join the resistance to create a better future for your children.",
    color_scheme: str = "dark",
    accent_color: str = "#e62429", # Rebel Red
    width_px: int = 1440,
    height_px: int = 900,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Cinematic Immersive Hero Section.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Force dark theme base as this design pattern inherently relies on it for the "cinematic" space effect
    # The color_scheme parameter is accepted but overrides are minimal to preserve the intended aesthetic
    bg_color = "#050914"
    text_primary = "#ffffff"
    text_secondary = "#a0aab2"
    
    # Placeholder high-quality space image from Unsplash
    bg_image_url = "https://images.unsplash.com/photo-1462331940025-496dfbfc7564?q=80&w=2048&auto=format&fit=crop"

    # === CSS ===
    css = f"""/* Cinematic Immersive Hero Section */
:root {{
    --color-accent: {accent_color};
    --color-bg-base: {bg_color};
    --color-text-primary: {text_primary};
    --color-text-secondary: {text_secondary};
    --hero-width: {width_px}px;
    --hero-height: {height_px}px;
    
    --font-heading: 'Oswald', sans-serif;
    --font-body: 'Inter', sans-serif;
}}

*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: var(--font-body);
    background-color: var(--color-bg-base);
    color: var(--color-text-primary);
    -webkit-font-smoothing: antialiased;
    /* Center the component for demo purposes */
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
    margin: 0;
}}

.hero-container {{
    width: 100%;
    max-width: var(--hero-width);
    height: 100vh;
    max-height: var(--hero-height);
    position: relative;
    overflow: hidden;
    display: flex;
    flex-direction: column;
    
    /* Background setup with darkening overlay for legibility */
    background-image: linear-gradient(
        to right, 
        rgba(5, 9, 20, 0.9) 0%, 
        rgba(5, 9, 20, 0.6) 40%, 
        rgba(5, 9, 20, 0.1) 100%
    ), url('{bg_image_url}');
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
}}

/* Navigation Bar */
.navbar {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 2.5rem 5%;
    z-index: 10;
}}

.nav-brand {{
    font-family: var(--font-heading);
    font-size: 1.5rem;
    font-weight: 700;
    letter-spacing: 1px;
    text-transform: uppercase;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}}

.nav-brand-icon {{
    color: var(--color-accent);
    font-size: 1.8rem;
}}

.nav-links {{
    display: flex;
    list-style: none;
    gap: 2.5rem;
}}

.nav-links a {{
    color: var(--color-text-primary);
    text-decoration: none;
    font-size: 0.9rem;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    transition: color 0.3s ease;
}}

.nav-links a:hover {{
    color: var(--color-accent);
}}

/* Main Hero Content */
.hero-content {{
    flex: 1;
    display: flex;
    flex-direction: column;
    justify-content: center;
    padding: 0 5%;
    max-width: 650px;
    z-index: 10;
    
    /* Entrance Animation */
    animation: fadeUp 1s ease-out forwards;
    opacity: 0;
    transform: translateY(20px);
}}

.hero-title {{
    font-family: var(--font-heading);
    font-size: clamp(3rem, 5vw, 5.5rem);
    font-weight: 700;
    line-height: 1.1;
    text-transform: uppercase;
    margin-bottom: 1.5rem;
    letter-spacing: -1px;
    text-shadow: 0 4px 12px rgba(0,0,0,0.5);
}}

.hero-desc {{
    font-size: 1.125rem;
    line-height: 1.6;
    color: var(--color-text-secondary);
    margin-bottom: 2.5rem;
    max-width: 90%;
}}

/* Buttons */
.btn {{
    display: inline-flex;
    align-items: center;
    justify-content: center;
    padding: 1rem 2rem;
    font-family: var(--font-heading);
    font-size: 1.1rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1px;
    text-decoration: none;
    border: none;
    cursor: pointer;
    transition: all 0.3s ease;
}}

.btn-primary {{
    background-color: var(--color-accent);
    color: #ffffff;
}}

.btn-primary:hover {{
    background-color: #ff3338; /* Slightly lighter on hover */
    transform: translateY(-2px);
    box-shadow: 0 4px 15px rgba(230, 36, 41, 0.4);
}}

/* Footer elements (Social Proof) */
.hero-footer {{
    display: flex;
    align-items: center;
    gap: 1rem;
    margin-top: 2rem;
}}

.avatar-group {{
    display: flex;
}}

.avatar {{
    width: 32px;
    height: 32px;
    border-radius: 50%;
    border: 2px solid var(--color-bg-base);
    background-color: #333;
    margin-left: -10px;
}}
.avatar:first-child {{ margin-left: 0; }}

.social-proof-text {{
    font-size: 0.85rem;
    color: var(--color-text-secondary);
}}

/* Animations */
@keyframes fadeUp {{
    to {{
        opacity: 1;
        transform: translateY(0);
    }}
}}

/* Responsive adjustments */
@media (max-width: 768px) {{
    .nav-links {{ display: none; }} /* Hide links on mobile for simplicity in this demo */
    .hero-content {{ max-width: 100%; text-align: center; align-items: center; }}
    .hero-container {{ background-image: linear-gradient(to bottom, rgba(5,9,20,0.7), rgba(5,9,20,0.9)), url('{bg_image_url}'); }}
    .hero-title {{ font-size: 2.5rem; }}
}}
"""

    # === HTML ===
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cinematic Hero Section</title>
    <!-- Preconnect to Google Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <!-- Import Oswald for Headings and Inter for Body -->
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500&family=Oswald:wght@600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>

    <div class="hero-container">
        <!-- Navigation -->
        <nav class="navbar">
            <div class="nav-brand">
                <!-- Using a text character to represent a logo icon -->
                <span class="nav-brand-icon">✧</span> 
                Rebel Alliance
            </div>
            <ul class="nav-links">
                <li><a href="#">Our Ships</a></li>
                <li><a href="#">Mission</a></li>
                <li><a href="#">Donations</a></li>
            </ul>
            <a href="#" class="btn btn-primary nav-btn">Join Now</a>
        </nav>

        <!-- Main Content -->
        <main class="hero-content">
            <h1 class="hero-title">{title_text}</h1>
            <p class="hero-desc">{body_text}</p>
            
            <div class="hero-actions">
                <a href="#" class="btn btn-primary">Join Now For Free</a>
            </div>

            <!-- Implied Social Proof Element -->
            <div class="hero-footer">
                <div class="avatar-group">
                    <div class="avatar" style="background-image: url('https://i.pravatar.cc/100?img=11'); background-size: cover;"></div>
                    <div class="avatar" style="background-image: url('https://i.pravatar.cc/100?img=12'); background-size: cover;"></div>
                    <div class="avatar" style="background-image: url('https://i.pravatar.cc/100?img=13'); background-size: cover;"></div>
                </div>
                <span class="social-proof-text">Obi Wan and 4,000 others have already joined</span>
            </div>
        </main>
    </div>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = """// Cinematic Immersive Hero Section
document.addEventListener('DOMContentLoaded', () => {
    // Basic interaction to prove JS execution and add minor polish
    const primaryBtns = document.querySelectorAll('.btn-primary');
    
    primaryBtns.forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.preventDefault();
            // Create a simple click ripple or console log
            console.log('Action initiated: Joining the resistance.');
            
            // Visual feedback
            const originalText = btn.innerText;
            btn.innerText = 'Transmitting...';
            btn.style.opacity = '0.8';
            
            setTimeout(() => {
                btn.innerText = originalText;
                btn.style.opacity = '1';
            }, 1000);
        });
    });
});
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
