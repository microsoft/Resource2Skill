def create_component(
    output_dir: str,
    title_text: str = "Links & Tracking",
    body_text: str = "Manage your short links and view performance analytics.",
    color_scheme: str = "dark",        # "dark" or "light"
    accent_color: str = "#6366f1",     # CSS hex color for accent (Indigo)
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Interactive Dashboard Data List visual effect.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # === Derive theme colors from color_scheme ===
    if color_scheme == "dark":
        bg_color = "#09090b"
        surface_color = "#18181b"
        border_color = "#27272a"
        text_primary = "#fafafa"
        text_secondary = "#a1a1aa"
        hover_bg = "rgba(255, 255, 255, 0.04)"
        success_bg = "rgba(74, 222, 128, 0.1)"
        success_text = "#4ade80"
        bulk_bg = "#fafafa"
        bulk_text = "#09090b"
        toast_bg = "#18181b"
        toast_border = "#27272a"
    else:
        bg_color = "#f4f4f5"
        surface_color = "#ffffff"
        border_color = "#e4e4e7"
        text_primary = "#09090b"
        text_secondary = "#71717a"
        hover_bg = "rgba(0, 0, 0, 0.04)"
        success_bg = "rgba(22, 163, 74, 0.1)"
        success_text = "#16a34a"
        bulk_bg = "#09090b"
        bulk_text = "#fafafa"
        toast_bg = "#ffffff"
        toast_border = "#e4e4e7"

    # === CSS ===
    css = f"""/* Interactive Dashboard Data List */
:root {{
    --bg: {bg_color};
    --surface: {surface_color};
    --border: {border_color};
    --text-primary: {text_primary};
    --text-secondary: {text_secondary};
    --accent: {accent_color};
    --hover-bg: {hover_bg};
    --success-bg: {success_bg};
    --success-text: {success_text};
    --bulk-bg: {bulk_bg};
    --bulk-text: {bulk_text};
    --toast-bg: {toast_bg};
    --toast-border: {toast_border};
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
    justify-content: center;
    padding: 40px 20px;
}}

.app-container {{
    width: 100%;
    max-width: {width_px}px;
    height: {height_px}px;
    display: flex;
    flex-direction: column;
    position: relative;
}}

/* Header */
.panel-header {{
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 24px;
}}

.header-text h1 {{
    font-size: 24px;
    font-weight: 600;
    letter-spacing: -0.02em;
    margin-bottom: 4px;
}}

.header-text p {{
    font-size: 14px;
    color: var(--text-secondary);
}}

.btn-primary {{
    background: var(--accent);
    color: white;
    border: none;
    padding: 10px 16px;
    border-radius: 6px;
    font-size: 14px;
    font-weight: 500;
    display: flex;
    align-items: center;
    gap: 8px;
    cursor: pointer;
    transition: filter 0.2s;
}}

.btn-primary:hover {{
    filter: brightness(1.1);
}}

/* Data List */
.list-container {{
    border: 1px solid var(--border);
    border-radius: 8px;
    background: var(--bg);
    overflow: hidden;
}}

.list-item {{
    display: grid;
    grid-template-columns: 40px 40px 1fr auto auto 120px;
    align-items: center;
    gap: 16px;
    padding: 12px 20px;
    border-bottom: 1px solid var(--border);
    transition: background-color 0.2s ease;
}}

.list-item:last-child {{
    border-bottom: none;
}}

.list-item:hover, .list-item.selected {{
    background-color: var(--hover-bg);
}}

.checkbox-cell {{
    display: flex;
    justify-content: flex-start;
}}

input[type="checkbox"] {{
    accent-color: var(--accent);
    width: 16px;
    height: 16px;
    cursor: pointer;
    border-radius: 4px;
}}

.item-avatar {{
    width: 32px;
    height: 32px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 600;
    font-size: 14px;
    color: white;
}}

.item-details {{
    display: flex;
    flex-direction: column;
    gap: 4px;
}}

.item-title {{
    font-size: 14px;
    font-weight: 500;
    color: var(--text-primary);
}}

.item-url {{
    font-size: 13px;
    color: var(--text-secondary);
}}

.tag {{
    background: var(--hover-bg);
    color: var(--text-secondary);
    padding: 4px 8px;
    border-radius: 4px;
    font-size: 12px;
    border: 1px solid var(--border);
}}

.badge {{
    background: var(--success-bg);
    color: var(--success-text);
    padding: 4px 8px;
    border-radius: 99px;
    font-size: 12px;
    font-weight: 500;
    display: flex;
    align-items: center;
    gap: 6px;
}}

.dot {{
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: var(--success-text);
    box-shadow: 0 0 8px var(--success-text);
}}

/* Hover Actions */
.item-actions {{
    display: flex;
    gap: 8px;
    justify-content: flex-end;
    opacity: 0;
    pointer-events: none;
    transition: opacity 0.2s ease;
}}

.list-item:hover .item-actions, .list-item.selected .item-actions {{
    opacity: 1;
    pointer-events: auto;
}}

.icon-btn {{
    background: transparent;
    border: 1px solid var(--border);
    color: var(--text-secondary);
    width: 32px;
    height: 32px;
    border-radius: 6px;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    transition: all 0.2s;
}}

.icon-btn:hover {{
    background: var(--hover-bg);
    color: var(--text-primary);
}}

/* Optimistic Animation */
.new-item {{
    opacity: 0;
    transform: translateY(-10px);
    transition: opacity 0.4s ease, transform 0.4s ease;
}}
.new-item.inserted {{
    opacity: 1;
    transform: translateY(0);
}}

/* Bulk Action Bar */
.bulk-action-bar {{
    position: fixed;
    bottom: 32px;
    left: 50%;
    transform: translateX(-50%) translateY(100px);
    background: var(--bulk-bg);
    color: var(--bulk-text);
    padding: 12px 24px;
    border-radius: 99px;
    display: flex;
    align-items: center;
    gap: 24px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    opacity: 0;
    pointer-events: none;
    transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
    z-index: 1000;
}}

.bulk-action-bar.visible {{
    transform: translateX(-50%) translateY(0);
    opacity: 1;
    pointer-events: auto;
}}

.bulk-action-bar span {{
    font-size: 14px;
    font-weight: 500;
}}

.bulk-buttons {{
    display: flex;
    gap: 8px;
}}

.bulk-btn {{
    background: transparent;
    border: 1px solid rgba(128,128,128,0.3);
    color: var(--bulk-text);
    padding: 6px 12px;
    border-radius: 99px;
    font-size: 13px;
    cursor: pointer;
    transition: background 0.2s;
}}

.bulk-btn:hover {{
    background: rgba(128,128,128,0.1);
}}

/* Toast Notification */
.toast-container {{
    position: fixed;
    bottom: 32px;
    right: 32px;
    display: flex;
    flex-direction: column;
    gap: 12px;
    z-index: 1001;
}}

.toast {{
    background: var(--toast-bg);
    border: 1px solid var(--toast-border);
    color: var(--text-primary);
    padding: 16px 20px;
    border-radius: 8px;
    font-size: 14px;
    font-weight: 500;
    display: flex;
    align-items: center;
    gap: 12px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    transform: translateY(20px);
    opacity: 0;
    transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
}}

.toast.show {{
    transform: translateY(0);
    opacity: 1;
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
    <div class="app-container">
        
        <header class="panel-header">
            <div class="header-text">
                <h1>{title_text}</h1>
                <p>{body_text}</p>
            </div>
            <button id="createBtn" class="btn-primary">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 5v14m-7-7h14"/></svg>
                Create Link
            </button>
        </header>

        <div class="list-container" id="listContainer">
            <!-- Initial Dummy Item 1 -->
            <div class="list-item">
                <div class="checkbox-cell"><input type="checkbox" class="row-select"></div>
                <div class="item-avatar" style="background: linear-gradient(135deg, #f59e0b, #ea580c)">R</div>
                <div class="item-details">
                    <div class="item-title">linkd.sh/hkWhPa</div>
                    <div class="item-url">mywebsite.com/blogposts • 10d</div>
                </div>
                <div class="item-tags"><span class="tag">IG conversion</span></div>
                <div class="item-stats">
                    <span class="badge"><span class="dot"></span> 27 clicks</span>
                </div>
                <div class="item-actions">
                    <button class="icon-btn" title="Copy"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/></svg></button>
                    <button class="icon-btn" title="Edit"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 20h9M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"/></svg></button>
                </div>
            </div>

            <!-- Initial Dummy Item 2 -->
            <div class="list-item">
                <div class="checkbox-cell"><input type="checkbox" class="row-select"></div>
                <div class="item-avatar" style="background: linear-gradient(135deg, #3b82f6, #2563eb)">D</div>
                <div class="item-details">
                    <div class="item-title">linkd.sh/SnpPc</div>
                    <div class="item-url">mywebsite.com/dashboard • 2m</div>
                </div>
                <div class="item-tags"><span class="tag">App Internal</span></div>
                <div class="item-stats">
                    <span class="badge"><span class="dot"></span> 104 clicks</span>
                </div>
                <div class="item-actions">
                    <button class="icon-btn" title="Copy"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/></svg></button>
                    <button class="icon-btn" title="Edit"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 20h9M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"/></svg></button>
                </div>
            </div>
        </div>

    </div>

    <!-- Floating UI -->
    <div id="bulkActionBar" class="bulk-action-bar">
        <span id="selectedCount">0 selected</span>
        <div class="bulk-buttons">
            <button class="bulk-btn">Archive</button>
            <button class="bulk-btn" style="color: #ef4444; border-color: rgba(239, 68, 68, 0.3);">Delete</button>
        </div>
    </div>

    <div id="toastContainer" class="toast-container"></div>

    <script src="script.js"></script>
</body>
</html>"""

    # === JavaScript ===
    js = f"""// Interactive Behavior & Optimistic UI
document.addEventListener('DOMContentLoaded', () => {{
    const createBtn = document.getElementById('createBtn');
    const listContainer = document.getElementById('listContainer');
    const bulkActionBar = document.getElementById('bulkActionBar');
    const selectedCountText = document.getElementById('selectedCount');
    
    // 1. Handle Checkbox Selection & Bulk Actions Visibility
    function updateBulkActions() {{
        const checkedCount = document.querySelectorAll('.row-select:checked').length;
        if (checkedCount > 0) {{
            selectedCountText.textContent = `${{checkedCount}} selected`;
            bulkActionBar.classList.add('visible');
        }} else {{
            bulkActionBar.classList.remove('visible');
        }}
    }}

    // Event delegation for dynamically added rows
    listContainer.addEventListener('change', (e) => {{
        if (e.target.classList.contains('row-select')) {{
            const row = e.target.closest('.list-item');
            if (e.target.checked) {{
                row.classList.add('selected');
            }} else {{
                row.classList.remove('selected');
            }}
            updateBulkActions();
        }}
    }});

    // 2. Optimistic UI: Create Link
    createBtn.addEventListener('click', () => {{
        // Generate random string for demo purposes
        const randomHash = Math.random().toString(36).substring(2, 8);
        const gradientColors = ['#10b981', '#059669']; // Emerald gradient
        
        const newItem = document.createElement('div');
        newItem.className = 'list-item new-item';
        newItem.innerHTML = `
            <div class="checkbox-cell"><input type="checkbox" class="row-select"></div>
            <div class="item-avatar" style="background: linear-gradient(135deg, ${{gradientColors[0]}}, ${{gradientColors[1]}})">N</div>
            <div class="item-details">
                <div class="item-title">linkd.sh/${{randomHash}}</div>
                <div class="item-url">Optimistically created • Just now</div>
            </div>
            <div class="item-tags"><span class="tag">New</span></div>
            <div class="item-stats">
                <span class="badge"><span class="dot"></span> 0 clicks</span>
            </div>
            <div class="item-actions">
                <button class="icon-btn" title="Copy"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/></svg></button>
                <button class="icon-btn" title="Edit"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 20h9M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"/></svg></button>
            </div>
        `;
        
        // Prepend new item
        listContainer.insertBefore(newItem, listContainer.firstChild);
        
        // Trigger CSS transition in the next frame
        requestAnimationFrame(() => {{
            newItem.classList.add('inserted');
        }});

        showToast('New link created instantly.');
    }});

    // 3. Toast Notification System
    function showToast(message) {{
        const container = document.getElementById('toastContainer');
        const toast = document.createElement('div');
        toast.className = 'toast';
        toast.innerHTML = `
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="var(--success-text)" stroke-width="2"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>
            ${{message}}
        `;
        
        container.appendChild(toast);
        
        // Animate in
        requestAnimationFrame(() => toast.classList.add('show'));
        
        // Remove after delay
        setTimeout(() => {{
            toast.classList.remove('show');
            setTimeout(() => toast.remove(), 300); // wait for fade out transition
        }}, 3000);
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
