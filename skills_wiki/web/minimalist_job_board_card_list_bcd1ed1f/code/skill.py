def create_component(
    output_dir: str,
    title_text: str = "Want to Find Your Next Dev Role?",
    body_text: str = "Fantastic. You've come to the right place. Below is a curated list of dev roles.",
    color_scheme: str = "light",        # "dark" or "light"
    accent_color: str = "#e67e22",     # Toast orange
    width_px: int = 900,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Minimalist Job Board Card & List effect.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors ===
    if color_scheme == "dark":
        bg_color = "#0f1115"
        text_color = "#f1f5f9"
        text_muted = "#94a3b8"
        card_bg = "#1e293b"
        border_color = "#334155"
        dot_color = "255, 255, 255"
    else:
        bg_color = "#f8fafc"
        text_color = "#0f172a"
        text_muted = "#64748b"
        card_bg = "#ffffff"
        border_color = "#e2e8f0"
        dot_color = "0, 0, 0"

    # SVG Data URI for the dot pattern background
    bg_pattern = f"url(\"data:image/svg+xml,%3Csvg width='24' height='24' viewBox='0 0 24 24' xmlns='http://www.w3.org/2000/svg'%3E%3Ccircle cx='2' cy='2' r='1' fill='rgba({dot_color}, 0.1)'/%3E%3C/svg%3E\")"

    # === CSS ===
    css = f"""/* Minimalist Job Board List — generated component */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --bg: {bg_color};
    --text: {text_color};
    --text-muted: {text_muted};
    --accent: {accent_color};
    /* Modern CSS to create a semi-transparent background from a solid hex */
    --accent-bg: color-mix(in srgb, var(--accent) 15%, transparent);
    --card-bg: {card_bg};
    --border: {border_color};
    --width: {width_px}px;
    --height: {height_px}px;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background-color: var(--bg);
    background-image: {bg_pattern};
    color: var(--text);
    min-height: 100vh;
    display: flex;
    justify-content: center;
}}

.container {{
    width: 100%;
    max-width: var(--width);
    height: var(--height);
    padding: 3rem 2rem;
    overflow-y: auto;
}}

/* Header & Filter */
.header {{
    text-align: center;
    margin-bottom: 3rem;
}}

.title {{
    font-size: 2.25rem;
    font-weight: 700;
    margin-bottom: 0.75rem;
    letter-spacing: -0.02em;
}}

.body-text {{
    color: var(--text-muted);
    margin-bottom: 2rem;
    font-size: 1.1rem;
}}

.filter-container {{
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 1rem;
}}

.filter-container label {{
    font-weight: 600;
    color: var(--text-muted);
    font-size: 0.875rem;
}}

.select-wrapper {{
    position: relative;
}}

.select-wrapper::after {{
    content: '';
    position: absolute;
    right: 1rem;
    top: 50%;
    transform: translateY(-50%);
    width: 0; 
    height: 0; 
    border-left: 4px solid transparent;
    border-right: 4px solid transparent;
    border-top: 5px solid var(--text-muted);
    pointer-events: none;
}}

select {{
    appearance: none;
    background: var(--card-bg);
    border: 1px solid var(--border);
    color: var(--text);
    padding: 0.5rem 2.5rem 0.5rem 1.25rem;
    border-radius: 999px;
    font-family: inherit;
    font-size: 0.875rem;
    font-weight: 600;
    cursor: pointer;
    box-shadow: 0 1px 2px rgba(0,0,0,0.05);
    outline: none;
    transition: border-color 0.2s;
}}

select:focus {{
    border-color: var(--accent);
}}

/* Job List & Cards */
.job-list {{
    list-style: none;
    display: flex;
    flex-direction: column;
    gap: 1rem;
}}

.job-card {{
    display: flex;
    align-items: center;
    background: var(--card-bg);
    border: 1px solid var(--border);
    padding: 1.25rem 1.5rem;
    border-radius: 12px;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.02), 0 2px 4px -1px rgba(0, 0, 0, 0.02);
    transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
    text-decoration: none;
    color: inherit;
}}

.job-card:hover, .job-card:focus-visible {{
    transform: translateY(-2px);
    box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.08), 0 4px 6px -2px rgba(0, 0, 0, 0.04);
    border-color: var(--accent);
    outline: none;
}}

.job-logo {{
    width: 48px;
    height: 48px;
    border-radius: 8px;
    background: var(--bg);
    border: 1px solid var(--border);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.25rem;
    font-weight: 700;
    color: var(--text);
    margin-right: 1.5rem;
    flex-shrink: 0;
}}

.job-details {{
    flex-grow: 1;
    display: flex;
    flex-direction: column;
    gap: 0.25rem;
}}

.job-company {{
    font-size: 0.875rem;
    color: var(--text-muted);
    font-weight: 500;
}}

.job-title {{
    font-size: 1.125rem;
    font-weight: 600;
    color: var(--text);
}}

.job-meta {{
    display: flex;
    align-items: center;
    gap: 0.75rem;
    margin-top: 0.35rem;
}}

.job-tag {{
    font-size: 0.75rem;
    font-weight: 600;
    color: var(--accent);
    background: var(--accent-bg);
    padding: 0.2rem 0.6rem;
    border-radius: 6px;
}}

.job-separator {{
    color: var(--border);
    font-size: 1rem;
    line-height: 1;
}}

.job-date {{
    font-size: 0.8rem;
    color: var(--text-muted);
    font-weight: 500;
}}

.job-action {{
    color: var(--border);
    transition: color 0.2s, transform 0.2s;
}}

.job-card:hover .job-action {{
    color: var(--accent);
    transform: translateX(4px);
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
    <div class="container">
        <header class="header">
            <h1 class="title">{title_text}</h1>
            <p class="body-text">{body_text}</p>
            
            <div class="filter-container">
                <label for="role-filter">Jobs</label>
                <div class="select-wrapper">
                    <select id="role-filter" aria-label="Filter jobs by role">
                        <option value="all">All Roles</option>
                        <option value="frontend">Frontend</option>
                        <option value="backend">Backend</option>
                        <option value="fullstack">Full-Stack</option>
                    </select>
                </div>
            </div>
        </header>

        <main>
            <ul class="job-list" aria-label="Job listings">
                <li class="job-item" data-role="backend">
                    <a href="#" class="job-card">
                        <div class="job-logo">R</div>
                        <div class="job-details">
                            <div class="job-company">Ramp</div>
                            <h3 class="job-title">Software Engineer Internship | Backend</h3>
                            <div class="job-meta">
                                <span class="job-tag">#Backend</span>
                                <span class="job-separator">•</span>
                                <span class="job-date">February 24, 2023</span>
                            </div>
                        </div>
                        <div class="job-action">
                            <svg viewBox="0 0 24 24" width="24" height="24" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"><polyline points="9 18 15 12 9 6"></polyline></svg>
                        </div>
                    </a>
                </li>
                
                <li class="job-item" data-role="fullstack">
                    <a href="#" class="job-card">
                        <div class="job-logo">M</div>
                        <div class="job-details">
                            <div class="job-company">Moonpay</div>
                            <h3 class="job-title">Senior Full Stack Engineer</h3>
                            <div class="job-meta">
                                <span class="job-tag">#Full-Stack</span>
                                <span class="job-separator">•</span>
                                <span class="job-date">February 23, 2023</span>
                            </div>
                        </div>
                        <div class="job-action">
                            <svg viewBox="0 0 24 24" width="24" height="24" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"><polyline points="9 18 15 12 9 6"></polyline></svg>
                        </div>
                    </a>
                </li>

                <li class="job-item" data-role="frontend">
                    <a href="#" class="job-card">
                        <div class="job-logo" style="color: #fff; background: var(--text);">N</div>
                        <div class="job-details">
                            <div class="job-company">Notion</div>
                            <h3 class="job-title">Software Engineer, Frontend</h3>
                            <div class="job-meta">
                                <span class="job-tag">#Frontend</span>
                                <span class="job-separator">•</span>
                                <span class="job-date">February 22, 2023</span>
                            </div>
                        </div>
                        <div class="job-action">
                            <svg viewBox="0 0 24 24" width="24" height="24" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"><polyline points="9 18 15 12 9 6"></polyline></svg>
                        </div>
                    </a>
                </li>
                
                <li class="job-item" data-role="frontend">
                    <a href="#" class="job-card">
                        <div class="job-logo">R</div>
                        <div class="job-details">
                            <div class="job-company">Retool</div>
                            <h3 class="job-title">Frontend Engineer</h3>
                            <div class="job-meta">
                                <span class="job-tag">#Frontend</span>
                                <span class="job-separator">•</span>
                                <span class="job-date">February 21, 2023</span>
                            </div>
                        </div>
                        <div class="job-action">
                            <svg viewBox="0 0 24 24" width="24" height="24" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"><polyline points="9 18 15 12 9 6"></polyline></svg>
                        </div>
                    </a>
                </li>
            </ul>
        </main>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Minimalist Job Board List — Filtering Logic
document.addEventListener('DOMContentLoaded', () => {{
    const filterSelect = document.getElementById('role-filter');
    const jobItems = document.querySelectorAll('.job-item');

    filterSelect.addEventListener('change', (e) => {{
        const selectedRole = e.target.value;
        
        jobItems.forEach(item => {{
            // Use CSS to hide/show to maintain gap calculations in the ul
            if (selectedRole === 'all' || item.dataset.role === selectedRole) {{
                item.style.display = 'block';
                // Add a tiny animation when reappearing
                item.animate([
                    {{ opacity: 0, transform: 'translateY(10px)' }},
                    {{ opacity: 1, transform: 'translateY(0)' }}
                ], {{ duration: 300, easing: 'ease-out' }});
            }} else {{
                item.style.display = 'none';
            }}
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
