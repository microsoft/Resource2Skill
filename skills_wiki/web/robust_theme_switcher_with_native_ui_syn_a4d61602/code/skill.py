def create_component(
    output_dir: str,
    title_text: str = "Theme Sync Demo",
    body_text: str = "Change the theme using the dropdown. Notice how the native scrollbar and input fields instantly adapt to match the selected theme, thanks to the CSS color-scheme property.",
    color_scheme: str = "dark",        # "dark" or "light" (initial explicit theme)
    accent_color: str = "#3b82f6",     # CSS hex color for accent highlights
    width_px: int = 800,
    height_px: int = 600,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Robust Theme Switcher with Native UI Syncing.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Initial HTML attribute configuration based on default parameter
    html_theme_attr = f'data-theme="{color_scheme}"' if color_scheme in ["light", "dark"] else ''

    # === CSS ===
    css = f"""/* Robust Theme Switcher with Native UI Syncing */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    /* Light Mode Tokens */
    --bg-light: #ffffff;
    --text-light: #1a1a2e;
    --surface-light: #f3f4f6;
    --border-light: #e5e7eb;

    /* Dark Mode Tokens */
    --bg-dark: #0f172a;
    --text-dark: #f8fafc;
    --surface-dark: #1e293b;
    --border-dark: #334155;

    /* Universal Tokens */
    --accent: {accent_color};
    --width: {width_px}px;
    --height: {height_px}px;

    /* System Default Fallback (Assumes light, overridden by media query below) */
    --bg: var(--bg-light);
    --text: var(--text-light);
    --surface: var(--surface-light);
    --border: var(--border-light);
}}

/* System Preference override */
@media (prefers-color-scheme: dark) {{
    :root {{
        --bg: var(--bg-dark);
        --text: var(--text-dark);
        --surface: var(--surface-dark);
        --border: var(--border-dark);
    }}
}}

/* Base browser theme behavior */
html {{
    /* Tells the browser this page supports both, defaulting to system preference */
    color-scheme: light dark;
}}

/* Explicit User Choice: Light Mode */
html[data-theme="light"] {{
    --bg: var(--bg-light);
    --text: var(--text-light);
    --surface: var(--surface-light);
    --border: var(--border-light);
    /* Forces native UI (scrollbars, inputs) to light mode, ignoring system settings */
    color-scheme: light;
}}

/* Explicit User Choice: Dark Mode */
html[data-theme="dark"] {{
    --bg: var(--bg-dark);
    --text: var(--text-dark);
    --surface: var(--surface-dark);
    --border: var(--border-dark);
    /* Forces native UI (scrollbars, inputs) to dark mode, ignoring system settings */
    color-scheme: dark;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background-color: var(--bg);
    color: var(--text);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: background-color 0.3s ease, color 0.3s ease;
}}

.container {{
    width: var(--width);
    max-width: 90vw;
    height: var(--height);
    max-height: 90vh;
    background-color: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 32px;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15);
    display: flex;
    flex-direction: column;
    gap: 24px;
    transition: background-color 0.3s ease, border-color 0.3s ease;
}}

.header {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid var(--border);
    padding-bottom: 16px;
    transition: border-color 0.3s ease;
}}

.title {{
    font-size: 1.5rem;
    font-weight: 600;
}}

.theme-controls {{
    display: flex;
    align-items: center;
    gap: 12px;
    font-size: 0.95rem;
}}

select {{
    padding: 8px 12px;
    border-radius: 6px;
    border: 1px solid var(--border);
    background-color: var(--bg);
    color: var(--text);
    font-family: inherit;
    font-size: 0.95rem;
    cursor: pointer;
    transition: border-color 0.2s ease, outline 0.2s ease;
}}

select:focus {{
    outline: 2px solid var(--accent);
    outline-offset: 1px;
    border-color: transparent;
}}

.content-area {{
    display: flex;
    flex-direction: column;
    gap: 20px;
    flex-grow: 1;
}}

.body-text {{
    line-height: 1.6;
    color: var(--text);
    opacity: 0.9;
}}

.demo-box {{
    background-color: var(--bg);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 20px;
    display: flex;
    flex-direction: column;
    gap: 16px;
    transition: background-color 0.3s ease, border-color 0.3s ease;
}}

/* We deliberately DO NOT set background-color or color on these native form elements.
   This allows us to prove that CSS `color-scheme` styles them natively. */
input, textarea {{
    width: 100%;
    padding: 12px;
    border-radius: 6px;
    border: 1px solid var(--border);
    font-family: inherit;
    font-size: 1rem;
}}

textarea {{
    resize: vertical;
}}

/* Custom scrollbar fallback styling ONLY for aesthetics on webkit. 
   Notice we don't define colors here, we let `color-scheme` define the base contrast. */
::-webkit-scrollbar {{
    width: 12px;
    height: 12px;
}}
"""

    # === HTML ===
    html = f"""<!DOCTYPE html>
<html lang="en" {html_theme_attr}>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        <header class="header">
            <h1 class="title">{title_text}</h1>
            <div class="theme-controls">
                <label for="theme-switcher">Theme:</label>
                <select id="theme-switcher">
                    <option value="system">System Preference</option>
                    <option value="light">Light Mode</option>
                    <option value="dark">Dark Mode</option>
                </select>
            </div>
        </header>

        <main class="content-area">
            <p class="body-text">{body_text}</p>
            
            <div class="demo-box">
                <input type="text" placeholder="Type here... native background syncs automatically">
                <textarea rows="6">Native Textarea Scrollbar Demo.

Scroll down to see the scrollbar.
When you change the theme using the dropdown, notice how the scrollbar's color natively adapts to the light or dark setting. 

This happens because we are overriding the CSS `color-scheme` property on the HTML element!
Line 9
Line 10
Line 11
Line 12</textarea>
            </div>
        </main>
    </div>
    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Robust Theme Switcher Logic
document.addEventListener('DOMContentLoaded', () => {{
    const themeSwitcher = document.getElementById('theme-switcher');
    const rootElement = document.documentElement;

    // 1. Initialize dropdown value based on the rendered HTML data attribute
    const currentTheme = rootElement.getAttribute('data-theme');
    if (currentTheme === 'light' || currentTheme === 'dark') {{
        themeSwitcher.value = currentTheme;
    }} else {{
        themeSwitcher.value = 'system';
    }}

    // 2. Listen for user interaction
    themeSwitcher.addEventListener('change', (e) => {{
        const selectedTheme = e.target.value;

        if (selectedTheme === 'system') {{
            // Removing the attribute lets CSS fallback to @media (prefers-color-scheme)
            rootElement.removeAttribute('data-theme');
        }} else {{
            // Explicitly set light or dark
            rootElement.setAttribute('data-theme', selectedTheme);
        }}
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
