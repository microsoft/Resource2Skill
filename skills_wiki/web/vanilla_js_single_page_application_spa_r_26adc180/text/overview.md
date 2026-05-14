# Vanilla JS Single Page Application (SPA) Router

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Vanilla JS Single Page Application (SPA) Router

* **Core Visual Mechanism**: A fluid, persistent layout (typically a sidebar navigation and a main content area) where content dynamically swaps out instantly upon navigation. By manipulating the browser's History API, the application avoids full page reloads, resulting in a flicker-free, seamless transition between distinct "views" or "pages."
* **Why Use This Skill (Rationale)**: Native browser navigation triggers a full document teardown and rebuild, resulting in a blank screen flash and lost application state. A client-side router intercepts navigation intents, fetches or renders only the necessary internal content, and artificially updates the URL. This drastically improves perceived performance and makes a web application feel like a responsive, native desktop/mobile app.
* **Overall Applicability**: Ideal for lightweight dashboards, administrative panels, portfolio sites, and interactive web tools where the overhead of a heavy framework (like React or Angular) is unnecessary, but the user experience of an SPA is desired.
* **Browser Compatibility**: Requires modern browser features including the History API (`history.pushState`), Promises/Async/Await, and modern DOM methods (`closest()`). Supported in all modern evergreen browsers (Chrome, Firefox, Safari, Edge).

### 2. Visual & Technical Breakdown

* **Step A: Core Visual Elements**
  * **Application Shell**: A rigid bounding container establishing the application window.
  * **Navigation Sidebar (`nav`)**: A static area containing internal anchor links decorated with a specific identifier (e.g., `data-link`).
  * **Dynamic Content Node (`div#app`)**: The designated injection target where view-specific HTML is rendered.
  * **Color Logic**: Uses a split-surface design. The sidebar often utilizes a slightly contrasting surface color to establish hierarchy.
  * **Typography**: Clean, sans-serif fonts with clear hierarchy (distinct heading weights and muted body copy) to simulate a software interface.

* **Step B: Layout & Compositional Style**
  * **Layout System**: CSS Flexbox is utilized on the main wrapper (`display: flex`). The sidebar receives a fixed width (`width: 250px; flex-shrink: 0`), while the main content area expands to fill the remaining space (`flex: 1`).
  * **Layering**: The sidebar and main content sit adjacent. Box shadows and borders separate the application shell from the document body, giving it a "software window" aesthetic.

* **Step C: Interactive Behavior & Animations**
  * **Link Interception**: A delegated event listener on the `document.body` watches for `click` events. If the target resides within a `[data-link]` element, the default browser navigation is prevented (`e.preventDefault()`).
  * **History Manipulation**: The router invokes `history.pushState()` to update the URL without triggering a network request.
  * **Route Resolution**: An array of route configurations maps path strings to View classes. The router evaluates the current URL, finds the matching View, instantiates it, and awaits its HTML output.
  * **History Traversal**: A `popstate` event listener ensures that clicking the browser's back/forward buttons triggers the router to evaluate the new URL and render the correct view.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **Client-Side Routing** | JS History API | Core to the tutorial; enables URL updates without page reloads. |
| **Route Matching** | JS Array mapping | Allows declarative definition of paths to View components. |
| **File:// Compatibility** | URL Query Parameters | Standard absolute paths (`/posts`) fail when executed directly from local files (`file://`). By converting the routing path to a query parameter (`?route=/posts`), we maintain the exact `pushState` architecture from the tutorial while ensuring the generated component runs flawlessly offline. |
| **Application Shell** | CSS Flexbox | Provides the simplest, most robust method for creating a resilient sidebar/content split. |

#### 3b. Complete Reproduction Code

```python
def create_component(
    output_dir: str,
    title_text: str = "SPA Dashboard",
    body_text: str = "Welcome to the custom Vanilla JS Single Page Application.",
    color_scheme: str = "dark",
    accent_color: str = "#3b82f6",
    width_px: int = 1000,
    height_px: int = 650,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Vanilla JS SPA Router pattern.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os
    import re

    os.makedirs(output_dir, exist_ok=True)

    # Calculate transparent accent for active states
    def hex_to_rgba(hex_color, alpha):
        hex_color = hex_color.lstrip('#')
        if len(hex_color) == 3:
            hex_color = ''.join([c*2 for c in hex_color])
        try:
            r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
            return f"rgba({r}, {g}, {b}, {alpha})"
        except ValueError:
            return f"rgba(59, 130, 246, {alpha})"

    accent_transparent = hex_to_rgba(accent_color, 0.1)

    if color_scheme == "dark":
        bg_body = "#0f172a"
        bg_surface = "#1e293b"
        bg_content = "#0f172a"
        text_main = "#f8fafc"
        text_muted = "#94a3b8"
        border_color = "#334155"
    else:
        bg_body = "#cbd5e1"
        bg_surface = "#ffffff"
        bg_content = "#f8fafc"
        text_main = "#0f172a"
        text_muted = "#64748b"
        border_color = "#e2e8f0"

    css = f"""/* Vanilla JS SPA Router — Style */
:root {{
    --bg-body: {bg_body};
    --bg-surface: {bg_surface};
    --bg-content: {bg_content};
    --text-main: {text_main};
    --text-muted: {text_muted};
    --border: {border_color};
    --accent: {accent_color};
    --accent-trans: {accent_transparent};
    --width: {width_px}px;
    --height: {height_px}px;
}}

* {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: 'Inter', system-ui, sans-serif;
    background-color: var(--bg-body);
    color: var(--text-main);
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 100vh;
    padding: 2rem;
}}

.app-container {{
    display: flex;
    width: var(--width);
    max-width: 100%;
    height: var(--height);
    background-color: var(--bg-content);
    border-radius: 16px;
    overflow: hidden;
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.3);
    border: 1px solid var(--border);
}}

/* Sidebar Navigation */
.sidebar {{
    width: 260px;
    flex-shrink: 0;
    background-color: var(--bg-surface);
    display: flex;
    flex-direction: column;
    border-right: 1px solid var(--border);
}}

.sidebar-header {{
    padding: 2rem;
    font-size: 1.25rem;
    font-weight: 700;
    letter-spacing: -0.025em;
    color: var(--text-main);
    border-bottom: 1px solid var(--border);
}}

.nav-links {{
    display: flex;
    flex-direction: column;
    padding: 1.5rem 0;
}}

.nav-link {{
    display: flex;
    align-items: center;
    padding: 1rem 2rem;
    color: var(--text-muted);
    text-decoration: none;
    font-weight: 500;
    transition: all 0.2s ease;
    border-left: 4px solid transparent;
}}

.nav-link:hover {{
    color: var(--text-main);
    background-color: rgba(150, 150, 150, 0.05);
}}

.nav-link.active {{
    color: var(--accent);
    background-color: var(--accent-trans);
    border-left-color: var(--accent);
}}

/* Main Content Injection Area */
.main-content {{
    flex: 1;
    overflow-y: auto;
    padding: 3rem;
    position: relative;
}}

/* View Specific Styles */
.view-header {{
    font-size: 2.25rem;
    font-weight: 700;
    letter-spacing: -0.025em;
    margin-bottom: 1rem;
}}

.view-description {{
    font-size: 1.125rem;
    line-height: 1.6;
    color: var(--text-muted);
    margin-bottom: 2.5rem;
}}

.dashboard-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
    gap: 1.5rem;
}}

.stat-card {{
    background-color: var(--bg-surface);
    border: 1px solid var(--border);
    padding: 1.5rem;
    border-radius: 12px;
}}

.stat-card h3 {{
    font-size: 0.875rem;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-bottom: 0.5rem;
}}

.stat-card .value {{
    font-size: 2rem;
    font-weight: 700;
    color: var(--text-main);
}}

.list-container {{
    list-style: none;
}}

.list-item {{
    padding: 1.5rem;
    border: 1px solid var(--border);
    border-radius: 12px;
    margin-bottom: 1rem;
    background-color: var(--bg-surface);
    transition: transform 0.2s ease;
}}

.list-item:hover {{
    transform: translateY(-2px);
    border-color: var(--accent);
}}

.list-item strong {{ display: block; font-size: 1.125rem; margin-bottom: 0.25rem; }}
.list-item span {{ color: var(--text-muted); font-size: 0.9rem; }}
"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="app-container">
        <nav class="sidebar">
            <div class="sidebar-header">{title_text}</div>
            <div class="nav-links">
                <!-- Using ?route= enables file:// protocol compatibility while maintaining History API mechanics -->
                <a href="?route=/" class="nav-link" data-link>Dashboard</a>
                <a href="?route=/posts" class="nav-link" data-link>Posts</a>
                <a href="?route=/settings" class="nav-link" data-link>Settings</a>
            </div>
        </nav>
        
        <main id="app" class="main-content">
            <!-- Dynamic Content Injected Here -->
        </main>
    </div>

    <script src="script.js"></script>
</body>
</html>"""

    js = f"""// Vanilla JS SPA Router Implementation

// --- 1. View Classes ---
class AbstractView {{
    constructor(params) {{
        this.params = params;
    }}
    setTitle(title) {{
        document.title = title;
    }}
    async getHtml() {{
        return "";
    }}
}}

class Dashboard extends AbstractView {{
    constructor(params) {{
        super(params);
        this.setTitle("Dashboard | {title_text}");
    }}
    async getHtml() {{
        return `
            <h1 class="view-header">Dashboard</h1>
            <p class="view-description">{body_text}</p>
            
            <div class="dashboard-grid">
                <div class="stat-card">
                    <h3>Total Views</h3>
                    <div class="value">45.2K</div>
                </div>
                <div class="stat-card">
                    <h3>Engagement</h3>
                    <div class="value">24%</div>
                </div>
                <div class="stat-card">
                    <h3>Active Sessions</h3>
                    <div class="value">1,204</div>
                </div>
            </div>
        `;
    }}
}}

class Posts extends AbstractView {{
    constructor(params) {{
        super(params);
        this.setTitle("Posts | {title_text}");
    }}
    async getHtml() {{
        return `
            <h1 class="view-header">Recent Posts</h1>
            <p class="view-description">Manage and view your published content.</p>
            
            <ul class="list-container">
                <li class="list-item">
                    <strong>Building a Vanilla JS Router</strong>
                    <span>Published 2 days ago • 1.2k reads</span>
                </li>
                <li class="list-item">
                    <strong>Understanding the History API</strong>
                    <span>Published 1 week ago • 3.4k reads</span>
                </li>
                <li class="list-item">
                    <strong>Web Components vs SPAs</strong>
                    <span>Published 2 weeks ago • 5.1k reads</span>
                </li>
            </ul>
        `;
    }}
}}

class Settings extends AbstractView {{
    constructor(params) {{
        super(params);
        this.setTitle("Settings | {title_text}");
    }}
    async getHtml() {{
        return `
            <h1 class="view-header">Settings</h1>
            <p class="view-description">Configure your application preferences.</p>
            
            <div class="stat-card">
                <h3>System Configuration</h3>
                <p style="margin-top: 1rem; color: var(--text-muted)">
                    This view is dynamically loaded via JavaScript without a page refresh. 
                    Observe the URL changing while the application shell remains intact.
                </p>
            </div>
        `;
    }}
}}

// --- 2. Router Logic ---

// Wrapper for history.pushState
const navigateTo = url => {{
    history.pushState(null, null, url);
    router();
}};

const router = async () => {{
    const routes = [
        {{ path: "/", view: Dashboard }},
        {{ path: "/posts", view: Posts }},
        {{ path: "/settings", view: Settings }}
    ];

    // Read the intended route from the URL parameters to ensure file:// compatibility
    const params = new URLSearchParams(window.location.search);
    const currentPath = params.get('route') || "/";

    // Match current path to routes array
    const potentialMatches = routes.map(route => {{
        return {{
            route: route,
            isMatch: currentPath === route.path
        }};
    }});

    let match = potentialMatches.find(potentialMatch => potentialMatch.isMatch);

    // 404 Fallback to Dashboard
    if (!match) {{
        match = {{
            route: routes[0],
            isMatch: true
        }};
    }}

    // Instantiate the matched view and inject HTML
    const view = new match.route.view();
    document.querySelector("#app").innerHTML = await view.getHtml();

    // Update active state on Navigation Links
    document.querySelectorAll('.nav-link').forEach(link => {{
        const linkUrl = new URL(link.href, window.location.origin);
        const linkRoute = new URLSearchParams(linkUrl.search).get('route') || "/";
        
        if (linkRoute === currentPath) {{
            link.classList.add('active');
        }} else {{
            link.classList.remove('active');
        }}
    }});
}};

// --- 3. Event Listeners ---

// Handle browser Back/Forward buttons
window.addEventListener("popstate", router);

document.addEventListener("DOMContentLoaded", () => {{
    // Delegate click events on the body to intercept internal link clicks
    document.body.addEventListener("click", e => {{
        // Use closest() to handle clicks on elements nested inside the anchor
        const link = e.target.closest("[data-link]");
        
        if (link) {{
            e.preventDefault(); // Stop browser from reloading
            navigateTo(link.href);
        }}
    }});

    // Initialize initial route
    router();
}});
"""

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
```

### 4. Accessibility & Performance Notes

* **Accessibility (a11y)**:
  * By overriding native link behavior (`e.preventDefault()`), screen readers and assistive technologies are not automatically notified that a new page has loaded. A robust SPA router should update the `<title>` (which the code handles) and ideally shift keyboard focus to the newly injected container or its primary heading (`<h1>`) so users navigating via keyboard aren't left stranded on the navigation link.
  * The `nav` element and semantic anchor tags (`<a>`) are used properly to ensure the layout remains understandable in the accessibility tree.
* **Performance**:
  * **Event Delegation**: Instead of binding event listeners to every single navigation link, a single listener is bound to `document.body` and filters by `closest("[data-link]")`. This is a highly performant pattern that scales flawlessly even if thousands of links are dynamically injected into the DOM later.
  * **File Protocol Compatibility**: Utilizing URL query parameters (`?route=`) allows the History API mechanics to operate completely locally (`file://`) without triggering filesystem access errors, maintaining 100% architectural fidelity to the tutorial while solving its reliance on an active Node/Express server.