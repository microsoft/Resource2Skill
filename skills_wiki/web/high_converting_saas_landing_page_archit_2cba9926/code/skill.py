def create_component(
    output_dir: str,
    title_text: str = "Spend 10x less time on product management",
    body_text: str = "The easy-to-use platform for busy Engineering, DevOps, and Tech teams. Wave goodbye to unexpected bottlenecks and scale with confidence.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#4F46E5",     # CSS hex color for accent
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the High-Converting SaaS Landing Page architecture.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Helper to convert hex to comma-separated RGB values for CSS variables
    def hex_to_rgb_str(hex_str):
        hex_str = hex_str.lstrip('#')
        if len(hex_str) == 3:
            hex_str = ''.join(c + c for c in hex_str)
        return f"{int(hex_str[0:2], 16)}, {int(hex_str[2:4], 16)}, {int(hex_str[4:6], 16)}"

    accent_rgb = hex_to_rgb_str(accent_color)

    if color_scheme == "dark":
        bg_rgb = "13, 17, 28"          # #0d111c
        surface_rgb = "26, 30, 43"     # #1a1e2b
        border_rgb = "42, 47, 62"      # #2a2f3e
        text_rgb = "255, 255, 255"     # #ffffff
        text_muted_rgb = "148, 163, 184" # #94a3b8
    else:
        bg_rgb = "255, 255, 255"       # #ffffff
        surface_rgb = "248, 250, 252"  # #f8fafc
        border_rgb = "226, 232, 240"   # #e2e8f0
        text_rgb = "15, 23, 42"        # #0f172a
        text_muted_rgb = "100, 116, 139" # #64748b

    # === CSS ===
    css = f"""/* SaaS Landing Page Component */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

:root {{
    --bg-rgb: {bg_rgb};
    --surface-rgb: {surface_rgb};
    --border-rgb: {border_rgb};
    --text-rgb: {text_rgb};
    --text-muted-rgb: {text_muted_rgb};
    --accent-rgb: {accent_rgb};

    --bg: rgb(var(--bg-rgb));
    --surface: rgb(var(--surface-rgb));
    --border: rgb(var(--border-rgb));
    --text: rgb(var(--text-rgb));
    --text-muted: rgb(var(--text-muted-rgb));
    --accent: rgb(var(--accent-rgb));

    --width: {width_px}px;
    --height: {height_px}px;
}}

*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    background-color: #000; /* Outer canvas frame */
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
    font-family: 'Inter', system-ui, sans-serif;
}}

.container {{
    width: var(--width);
    height: var(--height);
    background-color: var(--bg);
    color: var(--text);
    overflow-y: auto;
    overflow-x: hidden;
    position: relative;
    scroll-behavior: smooth;
    /* Hide scrollbar for presentation */
    scrollbar-width: none;
}}
.container::-webkit-scrollbar {{ display: none; }}

/* Glow Effect */
.bg-glow {{
    position: absolute;
    top: 200px;
    left: 50%;
    transform: translateX(-50%);
    width: 800px;
    height: 600px;
    background: radial-gradient(circle, rgba(var(--accent-rgb), 0.15) 0%, rgba(var(--accent-rgb), 0) 70%);
    z-index: 0;
    pointer-events: none;
}}

/* Navbar (Links to Pricing as per SaaS best practices) */
.navbar {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1.5rem 3rem;
    position: relative;
    z-index: 10;
}}

.nav-logo {{
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-weight: 700;
    font-size: 1.25rem;
    letter-spacing: -0.02em;
}}

.nav-links {{
    display: flex;
    gap: 2rem;
    align-items: center;
}}

.nav-links a {{
    color: var(--text-muted);
    text-decoration: none;
    font-size: 0.9rem;
    font-weight: 500;
    transition: color 0.2s ease;
}}

.nav-links a:hover {{ color: var(--text); }}
.nav-links a.highlight {{ color: var(--text); font-weight: 600; }}

.nav-links a.login-btn {{
    padding: 0.5rem 1rem;
    background: rgba(var(--surface-rgb), 0.5);
    border: 1px solid var(--border);
    border-radius: 0.375rem;
    color: var(--text);
}}
.nav-links a.login-btn:hover {{ border-color: var(--text-muted); }}

/* Hero Section */
.hero {{
    text-align: center;
    padding: 6rem 2rem 2rem;
    position: relative;
    z-index: 10;
    max-width: 800px;
    margin: 0 auto;
}}

.hero-title {{
    font-size: 3.5rem;
    font-weight: 800;
    letter-spacing: -0.025em;
    line-height: 1.1;
    margin-bottom: 1.5rem;
    color: var(--text);
}}

.hero-subtitle {{
    font-size: 1.25rem;
    font-weight: 400;
    color: var(--text-muted);
    line-height: 1.6;
    margin-bottom: 2.5rem;
    max-width: 640px;
    margin-left: auto;
    margin-right: auto;
}}

.cta-group {{
    display: flex;
    gap: 0.75rem;
    justify-content: center;
    margin-bottom: 1rem;
}}

.email-input {{
    padding: 0.875rem 1.25rem;
    border-radius: 0.5rem;
    border: 1px solid var(--border);
    background: rgba(var(--surface-rgb), 0.8);
    color: var(--text);
    font-size: 1rem;
    width: 320px;
    outline: none;
    transition: border-color 0.2s, box-shadow 0.2s;
}}
.email-input::placeholder {{ color: var(--text-muted); opacity: 0.7; }}
.email-input:focus {{
    border-color: var(--accent);
    box-shadow: 0 0 0 3px rgba(var(--accent-rgb), 0.2);
}}

.cta-button {{
    background: var(--accent);
    color: #ffffff;
    border: none;
    border-radius: 0.5rem;
    padding: 0.875rem 1.75rem;
    font-size: 1rem;
    font-weight: 600;
    cursor: pointer;
    transition: transform 0.2s, opacity 0.2s, box-shadow 0.2s;
    box-shadow: 0 4px 14px 0 rgba(var(--accent-rgb), 0.39);
}}
.cta-button:hover {{
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(var(--accent-rgb), 0.39);
}}

.cta-subtext {{
    font-size: 0.875rem;
    color: var(--text-muted);
    margin-bottom: 4rem;
}}

/* Abstract UI Mockup */
.mockup-wrapper {{
    max-width: 900px;
    width: 90%;
    margin: 0 auto 5rem auto;
    position: relative;
    z-index: 10;
}}

.mockup {{
    background: rgba(var(--surface-rgb), 0.6);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    border: 1px solid rgba(var(--border-rgb), 0.8);
    border-radius: 0.75rem;
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
    overflow: hidden;
}}

.mockup-topbar {{
    display: flex;
    gap: 0.5rem;
    padding: 1rem;
    border-bottom: 1px solid var(--border);
    background: rgba(var(--bg-rgb), 0.4);
}}

.dot {{ width: 10px; height: 10px; border-radius: 50%; }}
.dot.close {{ background: #ff5f56; }}
.dot.minimize {{ background: #ffbd2e; }}
.dot.expand {{ background: #27c93f; }}

.mockup-content {{
    display: flex;
    height: 400px;
}}

.mockup-sidebar {{
    width: 220px;
    border-right: 1px solid var(--border);
    padding: 1.5rem;
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
}}

.skeleton-line {{
    height: 10px;
    border-radius: 5px;
    background: var(--border);
    opacity: 0.5;
}}
.nav-item {{ height: 1.5rem; border-radius: 0.25rem; margin-bottom: 0.25rem; }}
.nav-item.active {{ background: rgba(var(--accent-rgb), 0.2); opacity: 1; }}
.nav-item.active .skeleton-line {{ background: var(--accent); opacity: 0.8; }}

.mockup-main {{
    flex: 1;
    padding: 2rem;
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
}}

.mockup-header-bar {{
    height: 2.5rem;
    border-radius: 0.375rem;
    background: rgba(var(--border-rgb), 0.3);
    width: 60%;
}}

.mockup-cards {{ display: flex; gap: 1rem; }}
.mockup-card {{
    flex: 1;
    height: 100px;
    background: rgba(var(--bg-rgb), 0.5);
    border: 1px solid var(--border);
    border-radius: 0.5rem;
    padding: 1rem;
}}

.mockup-chart {{
    flex: 1;
    background: rgba(var(--bg-rgb), 0.5);
    border: 1px solid var(--border);
    border-radius: 0.5rem;
    padding: 1rem;
    display: flex;
    align-items: flex-end;
    gap: 10px;
}}
.chart-bar {{
    flex: 1;
    background: var(--border);
    border-radius: 2px 2px 0 0;
    opacity: 0.5;
}}
.chart-bar:nth-child(1) {{ height: 40%; }}
.chart-bar:nth-child(2) {{ height: 70%; }}
.chart-bar:nth-child(3) {{ height: 50%; background: var(--accent); opacity: 0.8; }}
.chart-bar:nth-child(4) {{ height: 90%; }}
.chart-bar:nth-child(5) {{ height: 60%; }}

/* Social Proof */
.social-proof {{
    text-align: center;
    padding: 0 2rem 4rem;
    position: relative;
    z-index: 10;
}}

.social-text {{
    font-size: 0.875rem;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: var(--text-muted);
    margin-bottom: 2rem;
}}

.logo-strip {{
    display: flex;
    gap: 4rem;
    justify-content: center;
    align-items: center;
    flex-wrap: wrap;
    color: var(--text-muted);
}}

.company-logo {{
    font-size: 1.5rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
    opacity: 0.6;
    transition: opacity 0.3s;
}}
.company-logo:hover {{ opacity: 1; }}

/* Feature List (Section 7 from video) */
.feature-list {{
    padding: 5rem 3rem;
    background: var(--surface);
    border-top: 1px solid var(--border);
    position: relative;
    z-index: 10;
}}

.feature-grid {{
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 2.5rem;
    max-width: 1000px;
    margin: 0 auto;
}}

.feature-card {{
    background: var(--bg);
    border: 1px solid var(--border);
    border-radius: 0.75rem;
    padding: 2rem;
    transition: transform 0.3s, box-shadow 0.3s;
}}
.feature-card:hover {{
    transform: translateY(-4px);
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
}}

.feature-icon {{
    width: 48px;
    height: 48px;
    border-radius: 0.5rem;
    background: rgba(var(--accent-rgb), 0.1);
    color: var(--accent);
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 1.5rem;
}}

.feature-title {{
    font-size: 1.25rem;
    font-weight: 600;
    margin-bottom: 0.75rem;
}}

.feature-desc {{
    font-size: 0.95rem;
    color: var(--text-muted);
    line-height: 1.6;
}}

/* JS Animation Classes */
.animate-on-scroll {{
    opacity: 0;
    transform: translateY(24px);
    transition: opacity 0.7s cubic-bezier(0.16, 1, 0.3, 1), transform 0.7s cubic-bezier(0.16, 1, 0.3, 1);
}}
.animate-on-scroll.visible {{
    opacity: 1;
    transform: translateY(0);
}}

.delay-1 {{ transition-delay: 0.1s; }}
.delay-2 {{ transition-delay: 0.2s; }}
.delay-3 {{ transition-delay: 0.3s; }}
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
    <div class="container">
        <div class="bg-glow"></div>
        
        <nav class="navbar animate-on-scroll">
            <div class="nav-logo">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="var(--accent)" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polygon points="12 2 2 7 12 12 22 7 12 2"></polygon><polyline points="2 17 12 22 22 17"></polyline><polyline points="2 12 12 17 22 12"></polyline></svg>
                <span>SaaSify</span>
            </div>
            <div class="nav-links">
                <a href="#">Features</a>
                <a href="#">Case Studies</a>
                <a href="#" class="highlight">Pricing</a>
                <a href="#" class="login-btn">Log in</a>
            </div>
        </nav>

        <main class="hero">
            <h1 class="hero-title animate-on-scroll">{title_text}</h1>
            <h2 class="hero-subtitle animate-on-scroll delay-1">{body_text}</h2>
            
            <div class="cta-group animate-on-scroll delay-2">
                <input type="email" placeholder="Enter your work email" class="email-input">
                <button class="cta-button">Start Free Trial</button>
            </div>
            <p class="cta-subtext animate-on-scroll delay-2">No credit card required. 14-day free trial.</p>
        </main>

        <div class="mockup-wrapper animate-on-scroll delay-3">
            <div class="mockup">
                <div class="mockup-topbar">
                    <div class="dot close"></div>
                    <div class="dot minimize"></div>
                    <div class="dot expand"></div>
                </div>
                <div class="mockup-content">
                    <div class="mockup-sidebar">
                        <div class="nav-item active"><div class="skeleton-line" style="width: 60%; margin: 7px 10px"></div></div>
                        <div class="nav-item"><div class="skeleton-line" style="width: 80%; margin: 7px 10px"></div></div>
                        <div class="nav-item"><div class="skeleton-line" style="width: 50%; margin: 7px 10px"></div></div>
                    </div>
                    <div class="mockup-main">
                        <div class="mockup-header-bar"></div>
                        <div class="mockup-cards">
                            <div class="mockup-card">
                                <div class="skeleton-line" style="width: 40%"></div>
                                <div class="skeleton-line" style="width: 70%; margin-top: 15px; height: 20px; background: var(--text); opacity: 0.8"></div>
                            </div>
                            <div class="mockup-card">
                                <div class="skeleton-line" style="width: 30%"></div>
                                <div class="skeleton-line" style="width: 50%; margin-top: 15px; height: 20px; background: var(--text); opacity: 0.8"></div>
                            </div>
                            <div class="mockup-card">
                                <div class="skeleton-line" style="width: 50%"></div>
                                <div class="skeleton-line" style="width: 80%; margin-top: 15px; height: 20px; background: var(--text); opacity: 0.8"></div>
                            </div>
                        </div>
                        <div class="mockup-chart">
                            <div class="chart-bar"></div>
                            <div class="chart-bar"></div>
                            <div class="chart-bar"></div>
                            <div class="chart-bar"></div>
                            <div class="chart-bar"></div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <div class="social-proof animate-on-scroll">
            <p class="social-text">Trusted by innovative teams worldwide</p>
            <div class="logo-strip">
                <div class="company-logo" style="font-weight: 800; font-family: sans-serif;">
                    <svg width="24" height="24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/></svg> Globex
                </div>
                <div class="company-logo" style="font-weight: 900; font-style: italic;">
                    <svg width="24" height="24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg> Acme Corp
                </div>
                <div class="company-logo" style="font-family: serif; font-weight: 700;">
                    <svg width="24" height="24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg> Initech
                </div>
                <div class="company-logo" style="font-family: monospace; font-size: 1.75rem; font-weight: 600;">
                    <svg width="24" height="24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="3" width="20" height="14" rx="2" ry="2"/><line x1="8" y1="21" x2="16" y2="21"/><line x1="12" y1="17" x2="12" y2="21"/></svg> Soylent
                </div>
            </div>
        </div>

        <div class="feature-list">
            <div class="feature-grid">
                <div class="feature-card animate-on-scroll">
                    <div class="feature-icon">
                        <svg width="24" height="24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"/></svg>
                    </div>
                    <h3 class="feature-title">Lightning Fast</h3>
                    <p class="feature-desc">Built for speed and performance to save your team hours every single week without lag.</p>
                </div>
                <div class="feature-card animate-on-scroll delay-1">
                    <div class="feature-icon">
                        <svg width="24" height="24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
                    </div>
                    <h3 class="feature-title">Enterprise Security</h3>
                    <p class="feature-desc">Bank-grade encryption and granular role-based access controls keep your data safe.</p>
                </div>
                <div class="feature-card animate-on-scroll delay-2">
                    <div class="feature-icon">
                        <svg width="24" height="24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 20V10M12 20V4M6 20v-6"/></svg>
                    </div>
                    <h3 class="feature-title">Deep Analytics</h3>
                    <p class="feature-desc">Uncover hidden trends with our AI-powered dashboards and automated reporting.</p>
                </div>
            </div>
        </div>
    </div>
    
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// SaaS Landing Page Interaction Logic
document.addEventListener('DOMContentLoaded', () => {{
    const container = document.querySelector('.container');

    // Setup Intersection Observer for smooth scroll-reveal animations
    const observerOptions = {{
        root: container, // Observe relative to the custom scrolling container
        rootMargin: '0px',
        threshold: 0.15 // Trigger when 15% of the element is visible
    }};

    const observer = new IntersectionObserver((entries, observer) => {{
        entries.forEach(entry => {{
            if (entry.isIntersecting) {{
                // Add class to trigger CSS transition
                entry.target.classList.add('visible');
                // Unobserve so it only animates once
                observer.unobserve(entry.target);
            }}
        }});
    }}, observerOptions);

    // Attach observer to all elements with the animate-on-scroll class
    const animatedElements = document.querySelectorAll('.animate-on-scroll');
    animatedElements.forEach(el => observer.observe(el));
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
