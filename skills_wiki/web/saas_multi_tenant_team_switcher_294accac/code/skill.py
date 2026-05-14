def create_component(
    output_dir: str,
    title_text: str = "Dashboard",
    body_text: str = "Select a workspace to manage your resources.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#3b82f6",     # Blue accent for active states/focus rings
    width_px: int = 1000,
    height_px: int = 600,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the SaaS Multi-Tenant Team Switcher visual effect.

    Writes index.html, style.css, and script.js to output_dir.
    Returns: {"html": str, "css": str, "js": str, "files": [list of written file paths]}
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme and accent_color ===
    if color_scheme == "dark":
        bg_color = "#020817" # slate-950
        surface_color = "#0f172a" # slate-900
        surface_hover = "#1e293b" # slate-800
        border_color = "#1e293b" # slate-800
        border_hover = "#334155" # slate-700
        text_primary = "#f8fafc" # slate-50
        text_muted = "#94a3b8" # slate-400
        shadow = "0 10px 15px -3px rgba(0, 0, 0, 0.5), 0 4px 6px -4px rgba(0, 0, 0, 0.5)"
    else:
        bg_color = "#f8fafc" # slate-50
        surface_color = "#ffffff" # white
        surface_hover = "#f1f5f9" # slate-100
        border_color = "#e2e8f0" # slate-200
        border_hover = "#cbd5e1" # slate-300
        text_primary = "#0f172a" # slate-900
        text_muted = "#64748b" # slate-500
        shadow = "0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -4px rgba(0, 0, 0, 0.1)"

    # === CSS ===
    css = f"""/* SaaS Multi-Tenant Team Switcher — generated component */
:root {{
    --bg: {bg_color};
    --surface: {surface_color};
    --surface-hover: {surface_hover};
    --border: {border_color};
    --border-hover: {border_hover};
    --text-primary: {text_primary};
    --text-muted: {text_muted};
    --accent: {accent_color};
    --shadow: {shadow};
    
    --radius-lg: 0.5rem;
    --radius-md: 0.375rem;
    --radius-sm: 0.25rem;
    
    --width: {width_px}px;
    --height: {height_px}px;
}}

*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background: var(--bg);
    color: var(--text-primary);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    -webkit-font-smoothing: antialiased;
}}

.layout-wrapper {{
    width: var(--width);
    height: var(--height);
    background: var(--bg);
    border: 1px solid var(--border);
    border-radius: var(--radius-lg);
    box-shadow: var(--shadow);
    overflow: hidden;
    display: flex;
    flex-direction: column;
}}

/* Navbar Mockup */
.navbar {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 1rem 1.5rem;
    border-bottom: 1px solid var(--border);
    background: var(--surface);
}}

.nav-brand {{
    font-size: 1.25rem;
    font-weight: 600;
    letter-spacing: -0.025em;
}}

.nav-content {{
    flex: 1;
    padding: 2rem;
}}

.nav-content h1 {{
    font-size: 1.875rem;
    font-weight: 600;
    margin-bottom: 0.5rem;
    letter-spacing: -0.025em;
}}

.nav-content p {{
    color: var(--text-muted);
    font-size: 0.875rem;
}}

/* --- Team Switcher Component --- */
.team-switcher {{
    position: relative;
    font-size: 0.875rem;
}}

.switcher-trigger {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    width: 220px;
    padding: 0.375rem 0.75rem 0.375rem 0.375rem;
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    color: var(--text-primary);
    cursor: pointer;
    transition: border-color 0.2s, background-color 0.2s;
    font-family: inherit;
    outline: none;
}}

.switcher-trigger:hover, .team-switcher.is-open .switcher-trigger {{
    background: var(--surface-hover);
    border-color: var(--border-hover);
}}

.switcher-trigger:focus-visible {{
    box-shadow: 0 0 0 2px var(--bg), 0 0 0 4px var(--accent);
}}

.trigger-content {{
    display: flex;
    align-items: center;
    gap: 0.5rem;
}}

.avatar {{
    width: 24px;
    height: 24px;
    border-radius: var(--radius-sm);
    background: var(--text-primary);
    color: var(--surface);
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 600;
    font-size: 0.75rem;
    flex-shrink: 0;
}}

.avatar.muted {{
    background: var(--surface-hover);
    color: var(--text-primary);
    border: 1px dashed var(--border-hover);
}}

.team-name {{
    font-weight: 500;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    max-width: 130px;
}}

.chevron-icon {{
    width: 16px;
    height: 16px;
    color: var(--text-muted);
    transition: transform 0.2s ease;
}}

.team-switcher.is-open .chevron-icon {{
    transform: rotate(180deg);
}}

/* Dropdown Menu */
.switcher-dropdown {{
    position: absolute;
    top: calc(100% + 0.5rem);
    right: 0;
    width: 260px;
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    box-shadow: var(--shadow);
    padding: 0.25rem;
    z-index: 50;
    
    /* Animation states */
    opacity: 0;
    visibility: hidden;
    transform: translateY(-10px);
    transition: opacity 0.2s ease, transform 0.2s ease, visibility 0.2s;
}}

.team-switcher.is-open .switcher-dropdown {{
    opacity: 1;
    visibility: visible;
    transform: translateY(0);
}}

.dropdown-label {{
    padding: 0.5rem 0.5rem 0.25rem 0.5rem;
    font-size: 0.75rem;
    font-weight: 500;
    color: var(--text-muted);
}}

.team-list {{
    list-style: none;
}}

.team-item, .add-team-btn {{
    display: flex;
    align-items: center;
    width: 100%;
    padding: 0.375rem 0.5rem;
    border-radius: var(--radius-sm);
    cursor: pointer;
    background: transparent;
    border: none;
    color: var(--text-primary);
    font-family: inherit;
    font-size: 0.875rem;
    text-align: left;
    transition: background-color 0.15s, color 0.15s;
}}

.team-item:hover, .add-team-btn:hover {{
    background: var(--surface-hover);
}}

.team-item:focus-visible, .add-team-btn:focus-visible {{
    background: var(--surface-hover);
    outline: none;
}}

.item-content {{
    display: flex;
    align-items: center;
    gap: 0.5rem;
    flex: 1;
}}

.check-icon {{
    width: 16px;
    height: 16px;
    color: var(--text-primary);
    opacity: 0;
    transition: opacity 0.15s;
}}

.team-item.active .check-icon {{
    opacity: 1;
}}

.dropdown-divider {{
    height: 1px;
    background: var(--border);
    margin: 0.25rem -0.25rem;
}}

.add-team-btn {{
    color: var(--text-muted);
}}

.add-team-btn:hover {{
    color: var(--text-primary);
}}

.add-team-btn svg {{
    width: 16px;
    height: 16px;
    margin-right: 0.5rem;
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
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="layout-wrapper">
        <!-- Navbar -->
        <nav class="navbar">
            <div class="nav-brand">MarshalSaaS</div>
            
            <!-- Team Switcher Component -->
            <div class="team-switcher" id="teamSwitcher">
                <button class="switcher-trigger" id="switcherTrigger" aria-expanded="false" aria-haspopup="true">
                    <div class="trigger-content">
                        <div class="avatar" id="activeAvatar">A</div>
                        <span class="team-name" id="activeTeamName">Amazon</span>
                    </div>
                    <svg class="chevron-icon" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m7 15 5 5 5-5"/><path d="m7 9 5-5 5 5"/></svg>
                </button>
                
                <div class="switcher-dropdown" role="menu" aria-orientation="vertical" aria-labelledby="switcherTrigger">
                    <div class="dropdown-label">Teams</div>
                    <ul class="team-list" role="group">
                        <li role="menuitem" class="team-item active" tabindex="0" data-team="Amazon" data-avatar="A">
                            <div class="item-content">
                                <div class="avatar">A</div>
                                <span class="team-name">Amazon</span>
                            </div>
                            <svg class="check-icon" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>
                        </li>
                        <li role="menuitem" class="team-item" tabindex="0" data-team="Google" data-avatar="G">
                            <div class="item-content">
                                <div class="avatar">G</div>
                                <span class="team-name">Google</span>
                            </div>
                            <svg class="check-icon" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>
                        </li>
                        <li role="menuitem" class="team-item" tabindex="0" data-team="Microsoft" data-avatar="M">
                            <div class="item-content">
                                <div class="avatar">M</div>
                                <span class="team-name">Microsoft</span>
                            </div>
                            <svg class="check-icon" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>
                        </li>
                    </ul>
                    
                    <div class="dropdown-divider"></div>
                    
                    <button class="add-team-btn" role="menuitem" tabindex="0">
                        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M8 12h8"/><path d="M12 8v8"/></svg>
                        Add team
                    </button>
                </div>
            </div>
        </nav>
        
        <!-- Main Content -->
        <main class="nav-content">
            <h1>{title_text}</h1>
            <p>{body_text}</p>
        </main>
    </div>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// SaaS Multi-Tenant Team Switcher Interactive Logic
document.addEventListener('DOMContentLoaded', () => {{
    const teamSwitcher = document.getElementById('teamSwitcher');
    const trigger = document.getElementById('switcherTrigger');
    const activeAvatar = document.getElementById('activeAvatar');
    const activeTeamName = document.getElementById('activeTeamName');
    const teamItems = document.querySelectorAll('.team-item');
    
    // Toggle dropdown open/close
    trigger.addEventListener('click', (e) => {{
        e.preventDefault();
        const isOpen = teamSwitcher.classList.contains('is-open');
        toggleDropdown(!isOpen);
    }});
    
    // Close dropdown when clicking outside
    document.addEventListener('click', (e) => {{
        if (!teamSwitcher.contains(e.target)) {{
            toggleDropdown(false);
        }}
    }});
    
    // Handle keyboard navigation (Escape to close)
    teamSwitcher.addEventListener('keydown', (e) => {{
        if (e.key === 'Escape') {{
            toggleDropdown(false);
            trigger.focus();
        }}
    }});
    
    // Handle Team Selection
    teamItems.forEach(item => {{
        // Handle click
        item.addEventListener('click', () => selectTeam(item));
        
        // Handle enter key
        item.addEventListener('keydown', (e) => {{
            if (e.key === 'Enter' || e.key === ' ') {{
                e.preventDefault();
                selectTeam(item);
            }}
        }});
    }});
    
    function toggleDropdown(state) {{
        if (state) {{
            teamSwitcher.classList.add('is-open');
            trigger.setAttribute('aria-expanded', 'true');
        }} else {{
            teamSwitcher.classList.remove('is-open');
            trigger.setAttribute('aria-expanded', 'false');
        }}
    }}
    
    function selectTeam(selectedItem) {{
        // Extract data
        const teamName = selectedItem.getAttribute('data-team');
        const avatarLetter = selectedItem.getAttribute('data-avatar');
        
        // Update Trigger UI
        activeTeamName.textContent = teamName;
        activeAvatar.textContent = avatarLetter;
        
        // Update List UI (active checkmark)
        teamItems.forEach(item => item.classList.remove('active'));
        selectedItem.classList.add('active');
        
        // Close dropdown
        toggleDropdown(false);
        
        // Return focus to trigger
        trigger.focus();
        
        // Optional: Trigger a custom event for other parts of the app
        const event = new CustomEvent('teamChanged', {{ detail: {{ team: teamName }} }});
        document.dispatchEvent(event);
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
