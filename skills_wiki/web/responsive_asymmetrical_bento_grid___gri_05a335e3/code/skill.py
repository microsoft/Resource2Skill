def create_component(
    output_dir: str,
    title_text: str = "Unleash Your Productivity",
    body_text: str = "Streamline your workflow with our advanced grid-based tools designed for modern teams.",
    color_scheme: str = "dark",        
    accent_color: str = "#8B5CF6",     
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Responsive Bento Grid & Grid Stacking effect.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors ===
    if color_scheme == "dark":
        bg_color = "#090a0f"
        card_bg = "#141720"
        text_color = "#F9FAFB"
        text_muted = "#9CA3AF"
        border_color = "#2E323A"
        shadow_hover = "rgba(0, 0, 0, 0.4)"
    else:
        bg_color = "#F3F4F6"
        card_bg = "#FFFFFF"
        text_color = "#111827"
        text_muted = "#6B7280"
        border_color = "#E5E7EB"
        shadow_hover = "rgba(0, 0, 0, 0.1)"

    # === CSS ===
    css = f"""/* Responsive Bento Grid — generated component */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --card-bg: {card_bg};
    --text: {text_color};
    --text-muted: {text_muted};
    --accent: {accent_color};
    --border: {border_color};
    --shadow-hover: {shadow_hover};
    --max-width: {width_px}px;
    --min-height: {height_px}px;
}}

body {{
    font-family: 'Inter', system-ui, sans-serif;
    background: var(--bg);
    color: var(--text);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 2rem;
}}

.bento-container {{
    width: 100%;
    max-width: var(--max-width);
    min-height: var(--min-height);
    display: grid;
    /* 4 Column layout for Desktop */
    grid-template-columns: repeat(4, 1fr);
    grid-auto-rows: minmax(220px, 1fr);
    gap: 1.25rem;
    grid-template-areas:
        "hero hero item2 item3"
        "hero hero item4 item5";
}}

/* -- Individual Card Styles -- */
.bento-card {{
    background: var(--card-bg);
    border: 1px solid var(--border);
    border-radius: 24px;
    padding: 1.5rem;
    display: flex;
    flex-direction: column;
    position: relative;
    overflow: hidden;
    
    /* Animation initial state */
    opacity: 0;
    transform: translateY(30px);
    transition: opacity 0.6s cubic-bezier(0.2, 0.8, 0.2, 1), 
                transform 0.6s cubic-bezier(0.2, 0.8, 0.2, 1),
                box-shadow 0.3s ease,
                scale 0.3s ease;
}}

.bento-card.visible {{
    opacity: 1;
    transform: translateY(0);
}}

.bento-card:hover {{
    scale: 1.02;
    box-shadow: 0 20px 40px var(--shadow-hover);
    border-color: color-mix(in srgb, var(--accent) 50%, var(--border));
}}

/* -- Grid Area Assignments -- */
.card-hero {{ grid-area: hero; padding: 0; }}
.card-2 {{ grid-area: item2; }}
.card-3 {{ grid-area: item3; }}
.card-4 {{ grid-area: item4; }}
.card-5 {{ grid-area: item5; }}

/* -- Grid Stacking Technique (Hero Card) -- */
.card-hero {{
    display: grid;
    /* Both children will occupy row 1, column 1 natively overlapping */
}}

.hero-bg {{
    grid-area: 1 / 1 / -1 / -1;
    width: 100%;
    height: 100%;
    object-fit: cover;
    filter: brightness(0.4) saturate(1.2);
    transition: filter 0.5s ease, transform 0.5s ease;
}}

.card-hero:hover .hero-bg {{
    filter: brightness(0.5) saturate(1.3);
    transform: scale(1.05);
}}

.hero-content {{
    grid-area: 1 / 1 / -1 / -1;
    align-self: end;
    padding: 2.5rem;
    z-index: 10;
    display: flex;
    flex-direction: column;
    gap: 1rem;
    color: #ffffff; /* Forced white against dark image */
}}

.hero-title {{
    font-size: 2.5rem;
    font-weight: 700;
    line-height: 1.1;
    letter-spacing: -0.02em;
}}

.hero-desc {{
    font-size: 1.1rem;
    opacity: 0.9;
    max-width: 80%;
    line-height: 1.5;
}}

.hero-cta {{
    align-self: flex-start;
    padding: 0.75rem 1.5rem;
    background: var(--accent);
    color: #fff;
    border: none;
    border-radius: 8px;
    font-weight: 600;
    font-size: 1rem;
    cursor: pointer;
    margin-top: 0.5rem;
    transition: background 0.2s ease;
}}

.hero-cta:hover {{
    background: color-mix(in srgb, var(--accent) 80%, #fff);
}}

/* -- Standard Card Content -- */
.icon-box {{
    width: 48px;
    height: 48px;
    border-radius: 12px;
    background: color-mix(in srgb, var(--accent) 15%, transparent);
    color: var(--accent);
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: auto; /* Pushes content below to bottom */
}}

.icon-box svg {{
    width: 24px;
    height: 24px;
    stroke-width: 2;
}}

.card-title {{
    font-size: 1.25rem;
    font-weight: 600;
    margin-bottom: 0.5rem;
    margin-top: 1.5rem;
}}

.card-desc {{
    font-size: 0.95rem;
    color: var(--text-muted);
    line-height: 1.5;
}}

/* === Responsive Breakpoints === */

/* Tablet Configuration */
@media (max-width: 1024px) {{
    .bento-container {{
        grid-template-columns: repeat(3, 1fr);
        grid-auto-rows: minmax(200px, 1fr);
        grid-template-areas:
            "hero hero item2"
            "hero hero item3"
            "item4 item5 item5";
    }}
    .hero-title {{ font-size: 2rem; }}
}}

/* Mobile Configuration */
@media (max-width: 640px) {{
    .bento-container {{
        grid-template-columns: 1fr;
        grid-auto-rows: minmax(200px, auto);
        grid-template-areas:
            "hero"
            "item2"
            "item3"
            "item4"
            "item5";
    }}
    .card-hero {{ min-height: 400px; }}
    .hero-desc {{ max-width: 100%; }}
}}
"""

    # === HTML ===
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Responsive Bento Grid</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>

    <main class="bento-container">
        
        <!-- Hero Card with Grid Stacking -->
        <article class="bento-card card-hero">
            <img src="https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?q=80&w=1000&auto=format&fit=crop" alt="Abstract Background" class="hero-bg">
            <div class="hero-content">
                <h1 class="hero-title">{title_text}</h1>
                <p class="hero-desc">{body_text}</p>
                <button class="hero-cta">Get Started</button>
            </div>
        </article>

        <!-- Secondary Cards -->
        <article class="bento-card card-2">
            <div class="icon-box">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M3 3v18h18M18 9l-5 5-4-4-4 4"/></svg>
            </div>
            <h2 class="card-title">Real-time Analytics</h2>
            <p class="card-desc">Monitor your traffic and engagement seamlessly with live updates.</p>
        </article>

        <article class="bento-card card-3">
            <div class="icon-box">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
            </div>
            <h2 class="card-title">Enterprise Security</h2>
            <p class="card-desc">Bank-grade encryption ensures your data is locked down tight.</p>
        </article>

        <article class="bento-card card-4">
            <div class="icon-box">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"/></svg>
            </div>
            <h2 class="card-title">Lightning Fast</h2>
            <p class="card-desc">Optimized edge-routing delivers content in milliseconds globally.</p>
        </article>

        <article class="bento-card card-5">
            <div class="icon-box">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M19.428 15.428A2 2 0 0021 14h-2a2 2 0 11-4 0h-2v2a2 2 0 110 4v2h2a2 2 0 002-1.428zM4 15.428A2 2 0 002.572 14H4v1.428zM15.428 4A2 2 0 0014 2.572V4h1.428z"/></svg>
            </div>
            <h2 class="card-title">Seamless Integrations</h2>
            <p class="card-desc">Connect with over 100+ native apps and webhooks out of the box.</p>
        </article>

    </main>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Staggered Entry Animation using Intersection Observer
document.addEventListener('DOMContentLoaded', () => {{
    const cards = document.querySelectorAll('.bento-card');
    
    const observerOptions = {{
        root: null,
        rootMargin: '0px',
        threshold: 0.15
    }};

    const observer = new IntersectionObserver((entries, obs) => {{
        entries.forEach(entry => {{
            if (entry.isIntersecting) {{
                // Determine index for stagger delay based on DOM order
                const index = Array.from(cards).indexOf(entry.target);
                
                setTimeout(() => {{
                    entry.target.classList.add('visible');
                }}, index * 100); // 100ms stagger between cards
                
                // Stop observing once revealed
                obs.unobserve(entry.target);
            }}
        }});
    }}, observerOptions);

    cards.forEach(card => observer.observe(card));
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
