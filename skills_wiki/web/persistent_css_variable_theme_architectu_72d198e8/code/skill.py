def create_component(
    output_dir: str,
    title_text: str = "Frontend Developer",
    body_text: str = "Building responsive, accessible, and user-centric web applications with modern technologies.",
    color_scheme: str = "light",       # Default initial load state if no localStorage exists
    accent_color: str = "#3b82f6",     # Primary accent color (blue by default)
    width_px: int = 800,
    height_px: int = 600,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Persistent CSS Variable Theme Architecture.
    Includes a realistic profile card layout to demonstrate the theme switching.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === CSS ===
    css = f"""/* Base & Theme Variables */
:root {{
    /* Light Mode Variables (Default) */
    --bg-color: #f8f9fa;
    --surface-color: #ffffff;
    --text-primary: #0f172a;
    --text-secondary: #64748b;
    --border-color: #e2e8f0;
    --accent-color: {accent_color};
    --shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    --icon-hover-bg: #f1f5f9;
}}

/* Dark Mode Overrides */
[data-theme="dark"] {{
    --bg-color: #0f172a;
    --surface-color: #1e293b;
    --text-primary: #f8fafc;
    --text-secondary: #94a3b8;
    --border-color: #334155;
    --shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.5), 0 4px 6px -2px rgba(0, 0, 0, 0.3);
    --icon-hover-bg: #334155;
}}

/* Global Styles with Transitions */
*, *::before, *::after {{
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background-color: var(--bg-color);
    color: var(--text-primary);
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    /* Smooth transition for theme switching */
    transition: background-color 0.4s ease, color 0.4s ease;
}}

/* Navbar & Toggle Button */
.navbar {{
    position: absolute;
    top: 0;
    width: 100%;
    padding: 1.5rem 2rem;
    display: flex;
    justify-content: flex-end;
}}

.theme-toggle {{
    background: transparent;
    border: none;
    cursor: pointer;
    width: 44px;
    height: 44px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--text-primary);
    transition: background-color 0.2s ease, color 0.4s ease, transform 0.2s ease;
}}

.theme-toggle:hover {{
    background-color: var(--icon-hover-bg);
}}

.theme-toggle:active {{
    transform: scale(0.92);
}}

/* Icon swapping logic via CSS */
.theme-toggle .sun-icon {{ display: none; }}
.theme-toggle .moon-icon {{ display: block; }}

[data-theme="dark"] .theme-toggle .sun-icon {{ display: block; }}
[data-theme="dark"] .theme-toggle .moon-icon {{ display: none; }}

.theme-toggle svg {{
    width: 24px;
    height: 24px;
    fill: currentColor;
}}

/* Demo Profile Card */
.profile-card {{
    background-color: var(--surface-color);
    border: 1px solid var(--border-color);
    border-radius: 16px;
    padding: 3rem 2rem;
    max-width: {width_px}px;
    width: 90%;
    text-align: center;
    box-shadow: var(--shadow);
    /* Surface transition */
    transition: background-color 0.4s ease, border-color 0.4s ease, box-shadow 0.4s ease;
}}

.avatar {{
    width: 120px;
    height: 120px;
    border-radius: 50%;
    background: linear-gradient(135deg, var(--accent-color), #8b5cf6);
    margin: 0 auto 1.5rem;
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    font-size: 3rem;
    font-weight: 700;
    box-shadow: 0 4px 14px rgba(59, 130, 246, 0.3);
}}

.title {{
    font-size: 2rem;
    font-weight: 700;
    margin-bottom: 0.5rem;
    letter-spacing: -0.025em;
}}

.subtitle {{
    font-size: 1.1rem;
    color: var(--accent-color);
    font-weight: 500;
    margin-bottom: 1.5rem;
}}

.description {{
    color: var(--text-secondary);
    line-height: 1.6;
    margin-bottom: 2rem;
    font-size: 1.05rem;
    transition: color 0.4s ease;
}}

.actions {{
    display: flex;
    gap: 1rem;
    justify-content: center;
}}

.btn {{
    padding: 0.75rem 1.5rem;
    border-radius: 8px;
    font-weight: 600;
    cursor: pointer;
    text-decoration: none;
    transition: all 0.2s ease;
    font-family: inherit;
}}

.btn-primary {{
    background-color: var(--accent-color);
    color: white;
    border: none;
}}

.btn-primary:hover {{
    filter: brightness(1.1);
    transform: translateY(-2px);
}}

.btn-outline {{
    background-color: transparent;
    color: var(--text-primary);
    border: 1px solid var(--border-color);
}}

.btn-outline:hover {{
    background-color: var(--icon-hover-bg);
}}
"""

    # === HTML ===
    # Note the inline script in <head> to prevent FOUC (Flash of Unstyled Content)
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Theme Architecture Demo</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
    
    <!-- FOUC Prevention Script: Runs before CSS/DOM is fully parsed -->
    <script>
        (function() {{
            const savedTheme = localStorage.getItem('site-theme');
            // If saved theme exists, use it. Otherwise, fallback to OS preference, then default parameter.
            if (savedTheme) {{
                document.documentElement.setAttribute('data-theme', savedTheme);
            }} else if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {{
                document.documentElement.setAttribute('data-theme', 'dark');
            }} else {{
                document.documentElement.setAttribute('data-theme', '{color_scheme}');
            }}
        }})();
    </script>
</head>
<body>
    <nav class="navbar">
        <button id="theme-toggle" class="theme-toggle" aria-label="Toggle dark mode">
            <!-- Moon Icon (shows in Light mode) -->
            <svg class="moon-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
                <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path>
            </svg>
            <!-- Sun Icon (shows in Dark mode) -->
            <svg class="sun-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
                <circle cx="12" cy="12" r="5"></circle>
                <line x1="12" y1="1" x2="12" y2="3"></line>
                <line x1="12" y1="21" x2="12" y2="23"></line>
                <line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line>
                <line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line>
                <line x1="1" y1="12" x2="3" y2="12"></line>
                <line x1="21" y1="12" x2="23" y2="12"></line>
                <line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line>
                <line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line>
            </svg>
        </button>
    </nav>

    <main class="profile-card">
        <div class="avatar">JD</div>
        <h1 class="title">John Doe</h1>
        <h2 class="subtitle">{title_text}</h2>
        <p class="description">{body_text}</p>
        
        <div class="actions">
            <button class="btn btn-primary">Download CV</button>
            <button class="btn btn-outline">Contact Info</button>
        </div>
    </main>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Script for handling interactive behavior after DOM loads
document.addEventListener('DOMContentLoaded', () => {{
    const themeToggleBtn = document.getElementById('theme-toggle');
    const htmlElement = document.documentElement;

    themeToggleBtn.addEventListener('click', () => {{
        // Determine current theme
        const currentTheme = htmlElement.getAttribute('data-theme');
        
        // Toggle logic
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
        
        // Apply new theme to DOM
        htmlElement.setAttribute('data-theme', newTheme);
        
        // Persist user preference to localStorage
        localStorage.setItem('site-theme', newTheme);
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
