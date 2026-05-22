def create_component(
    output_dir: str,
    title_text: str = "Powerful Features",
    body_text: str = "Everything you need to scale your workflows, beautifully organized in one platform.",
    color_scheme: str = "dark",
    accent_color: str = "#00bfff",
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the SaaS Bento Box Feature Grid visual effect.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Theme setup ===
    if color_scheme == "dark":
        bg_color = "#030712"
        text_color = "#f9fafb"
        text_muted = "#9ca3af"
        surface_color = "#111827"
        border_color = "#1f2937"
        shadow_color = "rgba(0, 0, 0, 0.4)"
        hover_shadow = "rgba(0, 0, 0, 0.6)"
    else:
        bg_color = "#f3f4f6"
        text_color = "#111827"
        text_muted = "#6b7280"
        surface_color = "#ffffff"
        border_color = "#e5e7eb"
        shadow_color = "rgba(0, 0, 0, 0.05)"
        hover_shadow = "rgba(0, 0, 0, 0.12)"

    # === CSS ===
    css = f"""/* SaaS Bento Box Feature Grid — generated component */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --text: {text_color};
    --text-muted: {text_muted};
    --surface: {surface_color};
    --border: {border_color};
    --accent: {accent_color};
    --shadow-color: {shadow_color};
    --hover-shadow: {hover_shadow};
    --max-width: {width_px}px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background: var(--bg);
    color: var(--text);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 2rem;
    overflow-x: hidden;
}}

.container {{
    width: 100%;
    max-width: var(--max-width);
    display: flex;
    flex-direction: column;
    gap: 4rem;
}}

.section-header {{
    text-align: center;
    max-width: 600px;
    margin: 0 auto;
}}

.title {{
    font-size: 2.5rem;
    font-weight: 700;
    margin-bottom: 1rem;
    letter-spacing: -0.025em;
}}

.body-text {{
    font-size: 1.125rem;
    color: var(--text-muted);
    line-height: 1.6;
}}

/* Grid Layout */
.bento-grid {{
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    grid-auto-rows: 280px;
    gap: 1.5rem;
    width: 100%;
}}

/* Entrance Animation Wrapper */
.bento-card {{
    opacity: 0;
    transform: translateY(30px);
    transition: opacity 0.6s cubic-bezier(0.16, 1, 0.3, 1), transform 0.6s cubic-bezier(0.16, 1, 0.3, 1);
}}

.bento-card.visible {{
    opacity: 1;
    transform: translateY(0);
}}

/* Spans */
.span-2x2 {{ grid-column: span 2; grid-row: span 2; }}
.span-2x1 {{ grid-column: span 2; grid-row: span 1; }}
.span-1x1 {{ grid-column: span 1; grid-row: span 1; }}

/* Inner Hover Container */
.bento-inner {{
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 24px;
    padding: 2rem;
    height: 100%;
    display: flex;
    flex-direction: column;
    position: relative;
    overflow: hidden;
    transition: transform 0.4s cubic-bezier(0.4, 0, 0.2, 1), box-shadow 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    box-shadow: 0 4px 6px -1px var(--shadow-color), 0 2px 4px -2px var(--shadow-color);
}}

.bento-inner:hover {{
    transform: translateY(-8px);
    box-shadow: 0 25px 30px -5px var(--hover-shadow), 0 10px 15px -6px var(--shadow-color);
    border-color: var(--accent);
}}

/* Typography inside cards */
.card-content {{
    display: flex;
    flex-direction: column;
    z-index: 10;
}}
.card-content h3 {{
    font-size: 1.25rem;
    font-weight: 600;
    margin-bottom: 0.5rem;
    color: var(--text);
}}
.card-content p {{
    font-size: 0.875rem;
    color: var(--text-muted);
    line-height: 1.6;
}}

/* Specific Card Layouts */
.span-2x1 .bento-inner {{
    flex-direction: row;
    align-items: center;
    gap: 2rem;
}}
.span-2x1 .card-content {{ flex: 1; }}
.span-2x1 .card-visual {{ flex: 1; height: 100%; }}

.span-1x1 .bento-inner {{
    align-items: center;
    justify-content: center;
    text-align: center;
    gap: 1.5rem;
}}

/* Visual Containers */
.card-visual {{
    display: flex;
    align-items: center;
    justify-content: center;
    width: 100%;
}}
.span-2x2 .card-visual {{
    flex: 1;
    margin-top: 2rem;
    align-items: flex-start;
}}

/* --- MOCK UI: 2x2 Feature --- */
.mock-window {{
    width: 100%;
    height: 200px;
    background: var(--bg);
    border-radius: 12px;
    border: 1px solid var(--border);
    display: flex;
    flex-direction: column;
    overflow: hidden;
    mask-image: linear-gradient(to bottom, black 40%, transparent 100%);
    -webkit-mask-image: linear-gradient(to bottom, black 40%, transparent 100%);
    transform: rotate(-3deg) translateY(10px) scale(1.05);
    transition: transform 0.5s cubic-bezier(0.4, 0, 0.2, 1);
    box-shadow: 0 10px 15px -3px var(--shadow-color);
}}
.bento-inner:hover .mock-window {{
    transform: rotate(0) translateY(0) scale(1);
}}
.mock-header {{
    height: 32px;
    border-bottom: 1px solid var(--border);
    display: flex;
    align-items: center;
    padding: 0 12px;
    gap: 6px;
    background: rgba(255,255,255,0.02);
}}
.mock-dot {{ width: 10px; height: 10px; border-radius: 50%; }}
.mock-body {{ padding: 16px; display: flex; flex-direction: column; gap: 16px; }}
.mock-title {{ height: 16px; width: 40%; background: var(--border); border-radius: 4px; }}
.mock-row {{ display: flex; gap: 12px; align-items: center; }}
.mock-box {{ width: 32px; height: 32px; border-radius: 8px; background: var(--border); }}
.mock-box.accent {{ background: var(--accent); opacity: 0.8; }}
.mock-lines {{ flex: 1; display: flex; flex-direction: column; gap: 6px; }}
.mock-lines .line {{ height: 8px; background: var(--border); border-radius: 4px; width: 100%; }}
.mock-lines .line.short {{ width: 60%; }}
.mock-lines .line.shorter {{ width: 40%; }}

/* --- MOCK UI: Chart (2x1) --- */
.chart-container {{
    display: flex;
    align-items: flex-end;
    gap: 8px;
    width: 100%;
    height: 120px;
}}
.chart-bar {{
    flex: 1;
    background: var(--border);
    border-radius: 4px 4px 0 0;
    transition: height 1s cubic-bezier(0.16, 1, 0.3, 1), background-color 0.3s, box-shadow 0.3s;
}}
.bento-inner:hover .chart-bar {{ opacity: 0.7; }}
.bento-inner:hover .chart-bar.accent {{
    background: var(--accent);
    opacity: 1;
    box-shadow: 0 0 15px var(--accent);
}}

/* --- MOCK UI: Toggle (1x1) --- */
.toggle-wrapper {{
    background: var(--bg);
    padding: 16px;
    border-radius: 24px;
    border: 1px solid var(--border);
}}
.toggle-track {{
    width: 56px;
    height: 32px;
    background: var(--border);
    border-radius: 16px;
    padding: 4px;
    transition: background 0.3s;
}}
.toggle-thumb {{
    width: 24px;
    height: 24px;
    background: #fff;
    border-radius: 50%;
    transition: transform 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    box-shadow: 0 2px 4px rgba(0,0,0,0.2);
}}
.bento-inner:hover .toggle-track {{ background: var(--accent); }}
.bento-inner:hover .toggle-thumb {{ transform: translateX(24px); }}

/* --- MOCK UI: Avatars (1x1) --- */
.avatar-stack {{ display: flex; align-items: center; }}
.avatar {{
    width: 48px;
    height: 48px;
    border-radius: 50%;
    background: var(--border);
    border: 3px solid var(--surface);
    margin-left: -16px;
    transition: transform 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}}
.avatar:first-child {{ margin-left: 0; }}
.avatar.accent {{
    background: var(--accent);
    color: #fff;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 600;
    font-size: 0.875rem;
}}
.bento-inner:hover .avatar:nth-child(2) {{ transform: translateX(8px); }}
.bento-inner:hover .avatar:nth-child(3) {{ transform: translateX(16px); }}

/* Responsive Defaults */
@media (max-width: 1024px) {{
    .bento-grid {{ grid-template-columns: repeat(2, 1fr); }}
    .span-2x1 {{ grid-column: span 2; }}
}}
@media (max-width: 640px) {{
    .bento-grid {{ grid-template-columns: 1fr; }}
    .span-2x2, .span-2x1, .span-1x1 {{ grid-column: span 1; }}
    .span-2x1 .bento-inner {{ flex-direction: column; align-items: flex-start; }}
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
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        <div class="section-header">
            <h2 class="title">{title_text}</h2>
            <p class="body-text">{body_text}</p>
        </div>

        <div class="bento-grid">
            <!-- Large Feature (2x2) -->
            <div class="bento-card span-2x2">
                <div class="bento-inner">
                    <div class="card-content">
                        <h3>Automated Workflows</h3>
                        <p>Set up intricate processes once, and let our engine handle the execution autonomously in the background.</p>
                    </div>
                    <div class="card-visual">
                        <div class="mock-window">
                            <div class="mock-header">
                                <div class="mock-dot" style="background: #ef4444"></div>
                                <div class="mock-dot" style="background: #f59e0b"></div>
                                <div class="mock-dot" style="background: #10b981"></div>
                            </div>
                            <div class="mock-body">
                                <div class="mock-title"></div>
                                <div class="mock-row">
                                    <div class="mock-box"></div>
                                    <div class="mock-lines">
                                        <div class="line"></div>
                                        <div class="line short"></div>
                                    </div>
                                </div>
                                <div class="mock-row">
                                    <div class="mock-box accent"></div>
                                    <div class="mock-lines">
                                        <div class="line"></div>
                                        <div class="line shorter"></div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Wide Feature (2x1) -->
            <div class="bento-card span-2x1">
                <div class="bento-inner">
                    <div class="card-content">
                        <h3>Real-time Analytics</h3>
                        <p>Monitor your performance with live data streams and instant visual reporting.</p>
                    </div>
                    <div class="card-visual">
                        <div class="chart-container">
                            <div class="chart-bar" style="height: 30%"></div>
                            <div class="chart-bar" style="height: 50%"></div>
                            <div class="chart-bar" style="height: 40%"></div>
                            <div class="chart-bar" style="height: 80%"></div>
                            <div class="chart-bar" style="height: 60%"></div>
                            <div class="chart-bar accent" style="height: 95%"></div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Small Feature 1 (1x1) -->
            <div class="bento-card span-1x1">
                <div class="bento-inner">
                    <div class="card-visual">
                        <div class="toggle-wrapper">
                            <div class="toggle-track">
                                <div class="toggle-thumb"></div>
                            </div>
                        </div>
                    </div>
                    <div class="card-content">
                        <h3>1-Click Setup</h3>
                        <p>Deploy instantly without configuration.</p>
                    </div>
                </div>
            </div>

            <!-- Small Feature 2 (1x1) -->
            <div class="bento-card span-1x1">
                <div class="bento-inner">
                    <div class="card-visual">
                        <div class="avatar-stack">
                            <div class="avatar" style="z-index: 3"></div>
                            <div class="avatar" style="z-index: 2"></div>
                            <div class="avatar accent" style="z-index: 1">+5</div>
                        </div>
                    </div>
                    <div class="card-content">
                        <h3>Team Ready</h3>
                        <p>Invite your entire team seamlessly.</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// SaaS Bento Box Feature Grid — entrance animations
document.addEventListener('DOMContentLoaded', () => {{
    // Set up intersection observer for scroll reveal
    const observerOptions = {{
        root: null,
        rootMargin: '0px',
        threshold: 0.1
    }};

    const observer = new IntersectionObserver((entries, observer) => {{
        entries.forEach(entry => {{
            if (entry.isIntersecting) {{
                entry.target.classList.add('visible');
                // Unobserve after animating in
                observer.unobserve(entry.target);
            }}
        }});
    }}, observerOptions);

    // Apply staggered delays and observe
    const cards = document.querySelectorAll('.bento-card');
    cards.forEach((card, index) => {{
        // Stagger the entrance animation by 100ms per card
        card.style.transitionDelay = `${{index * 100}}ms`;
        observer.observe(card);
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
