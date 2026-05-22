# Neon Vertical Timeline System

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Neon Vertical Timeline System

* **Core Visual Mechanism**: A dual-column structural timeline layout that uses pseudo-elements (`::before`) and CSS borders to create a connected "node-and-path" visualization. It embraces a bold cyber/neon aesthetic, pairing dark background surfaces with high-contrast, glowing accent borders. Scroll-triggered animations slide elements into place chronologically.
* **Why Use This Skill (Rationale)**: Timelines are universally understood metaphors for displaying sequential data (resumes, project roadmaps, changelogs). By wrapping the content in distinct, high-contrast cards and connecting them visually, you make scanning easy while maintaining a modern, premium feel. The scroll-reveals provide a satisfying sense of progression and reward the user for scrolling.
* **Overall Applicability**: Ideal for "Education" or "Experience" sections in personal portfolios, "How it Works" steps in SaaS landing pages, or "Version History" changelogs.
* **Value Addition**: Transforms a flat list of text into a narrative journey. The connected line guides the eye vertically, while the boxed cards contain and structure distinct chunks of information.
* **Browser Compatibility**: Fully supported in modern browsers. Uses `color-mix()` for transparent glowing shadows (supported in Chrome 111+, Safari 111+, Firefox 111+, Safari iOS 16.4+). Fallbacks are naturally handled if shadows don't render.

### 2. Visual & Technical Breakdown

* **Step A: Core Visual Elements**
  - **Color Logic**: Utilizes a deep dark theme (`#080808` background, `#111111` card surfaces) to let a vibrant accent color (e.g., `#00e5ff` cyan or `#ff004f` red) pop. The accent color is applied to the structural borders, icons, and glowing nodes.
  - **Typography**: Clean sans-serif (`Inter`), with highly legible contrasting hierarchies. Years/Dates are small but colored with the accent; titles are bold and white; descriptions are subdued gray (`#a0a0a0`).
  - **Structural Nodes**: The timeline "dots" are constructed purely in CSS using `::before` pseudo-elements on the cards, mathematically positioned using negative `left` values to sit perfectly over the wrapper's left border.

* **Step B: Layout & Compositional Style**
  - **CSS Grid layout**: The main wrapper uses a 2-column CSS Grid (`1fr 1fr`) on desktop, collapsing to a single column on mobile (`max-width: 768px`).
  - **Spacing**: The layout relies on exact padding and negative positioning. The timeline wrapper has a thick left border and significant left padding. The cards sit inside the padding, and their pseudo-nodes are pulled back negatively to overlap the border.

* **Step C: Interactive Behavior & Animations**
  - **Scroll-triggered Reveals**: Uses the `IntersectionObserver` API to detect when cards enter the viewport.
  - **Cascading Delays**: JavaScript dynamically calculates an `animation-delay` based on the item's index, creating a staggered "waterfall" slide-in effect (`translateX(-40px)` to `0`, `opacity: 0` to `1`).
  - **Hover States**: Cards subtly lift (`transform: translateY(-5px)`) and increase their glowing drop-shadow on hover using CSS `color-mix()` for perfect semi-transparent accent shadows.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| Structural Timeline Line | CSS `border-left` | The simplest, most responsive way to create a continuous vertical path that automatically scales with content height. |
| Timeline Nodes (Dots) | CSS `::before` pseudo-elements | Keeps the HTML semantic and clean without requiring empty `<div>` tags just for decoration. Easy to position relatively. |
| Glowing Shadows | CSS `color-mix()` + `box-shadow` | Allows dynamically mixing the hex accent color with transparency for elegant, non-harsh glowing effects without needing explicit RGB variables. |
| Staggered Reveal Animation | JS `IntersectionObserver` | Provides a highly performant way to trigger CSS keyframes natively as the user scrolls, avoiding clunky scroll event listeners. |

#### 3b. Complete Reproduction Code

```python
def create_component(
    output_dir: str,
    title_text: str = "Journey & Milestones",
    body_text: str = "A timeline of academic achievements and professional growth.",
    color_scheme: str = "dark",
    accent_color: str = "#00e5ff",
    width_px: int = 1200,
    height_px: int = 800,
    **kwargs,
) -> dict:
    """
    Create a web component reproducing the Neon Vertical Timeline System.
    Writes index.html, style.css, and script.js to output_dir.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    if color_scheme == "dark":
        bg_color = "#080808"
        surface_color = "#151515"
        text_color = "#f4f4f5"
        text_muted = "#a1a1aa"
        border_light = "#27272a"
    else:
        bg_color = "#f8fafc"
        surface_color = "#ffffff"
        text_color = "#0f172a"
        text_muted = "#64748b"
        border_light = "#e2e8f0"

    css = f"""/* Neon Vertical Timeline System */
:root {{
    --bg: {bg_color};
    --surface: {surface_color};
    --text: {text_color};
    --text-muted: {text_muted};
    --accent: {accent_color};
    --border-light: {border_light};
    --width: {width_px}px;
    --min-height: {height_px}px;
}}

* {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background-color: var(--bg);
    color: var(--text);
    min-height: var(--min-height);
    display: flex;
    justify-content: center;
    padding: 80px 20px;
    overflow-x: hidden;
}}

.container {{
    width: 100%;
    max-width: var(--width);
}}

/* Section Header */
.section-header {{
    text-align: center;
    margin-bottom: 60px;
}}

.section-header h1 {{
    font-size: 2.8rem;
    font-weight: 800;
    margin-bottom: 16px;
    letter-spacing: -0.02em;
}}

/* Glowing accent text */
.section-header h1 span {{
    color: var(--accent);
    text-shadow: 0 0 15px color-mix(in srgb, var(--accent) 40%, transparent);
}}

.section-header p {{
    color: var(--text-muted);
    font-size: 1.1rem;
    max-width: 600px;
    margin: 0 auto;
    line-height: 1.6;
}}

/* Timeline Grid */
.timeline-grid {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 50px;
}}

.timeline-column {{
    display: flex;
    flex-direction: column;
}}

.column-title {{
    font-size: 1.8rem;
    font-weight: 700;
    margin-bottom: 30px;
    padding-left: 15px;
    color: var(--text);
}}

/* The structural line */
.timeline-wrapper {{
    border-left: 3px solid var(--accent);
    padding-left: 25px; /* Distance from line to cards */
    margin-left: 15px;  /* Margin to allow nodes to overlap nicely without clipping */
}}

/* Timeline Cards */
.timeline-card {{
    position: relative;
    background: var(--surface);
    border: 2px solid var(--border-light);
    border-radius: 12px;
    padding: 30px;
    margin-bottom: 30px;
    transition: transform 0.3s ease, border-color 0.3s ease, box-shadow 0.3s ease;
    
    /* Animation initial state */
    opacity: 0;
    transform: translateX(-40px);
}}

/* Ensure last card doesn't push wrapper down excessively */
.timeline-card:last-child {{
    margin-bottom: 0;
}}

/* The Timeline Node (Dot) */
.timeline-card::before {{
    content: '';
    position: absolute;
    top: 28px; 
    /* Perfect centering math: 
       Wrapper padding (25px) + wrapper border radius/width adjustments 
       => move left 25px + 1.5px (half border) + 10px (half dot) = 36.5px */
    left: -36.5px;
    width: 20px;
    height: 20px;
    background: var(--bg);
    border: 4px solid var(--accent);
    border-radius: 50%;
    box-shadow: 0 0 10px var(--accent);
    transition: background 0.3s ease, transform 0.3s ease, box-shadow 0.3s ease;
}}

/* Hover Effects */
.timeline-card:hover {{
    transform: translateY(-5px);
    border-color: var(--accent);
    box-shadow: 0 10px 30px color-mix(in srgb, var(--accent) 15%, transparent);
}}

.timeline-card:hover::before {{
    background: var(--accent);
    box-shadow: 0 0 20px var(--accent);
}}

/* Card Content Typography */
.card-year {{
    display: inline-flex;
    align-items: center;
    gap: 8px;
    font-size: 0.9rem;
    font-weight: 600;
    color: var(--accent);
    margin-bottom: 12px;
    background: color-mix(in srgb, var(--accent) 10%, transparent);
    padding: 6px 12px;
    border-radius: 20px;
}}

.card-year i {{
    font-size: 1.1rem;
}}

.card-title {{
    font-size: 1.4rem;
    font-weight: 700;
    margin-bottom: 12px;
    line-height: 1.3;
}}

.card-desc {{
    color: var(--text-muted);
    font-size: 1rem;
    line-height: 1.7;
}}

/* Animation Classes */
.timeline-card.in-view {{
    animation: slideIn 0.7s cubic-bezier(0.165, 0.84, 0.44, 1) forwards;
}}

@keyframes slideIn {{
    0% {{
        opacity: 0;
        transform: translateX(-40px);
    }}
    100% {{
        opacity: 1;
        transform: translateX(0);
    }}
}}

/* Responsive Design */
@media (max-width: 900px) {{
    .timeline-grid {{
        grid-template-columns: 1fr;
        gap: 60px;
    }}
    
    .section-header h1 {{
        font-size: 2.2rem;
    }}
}}
"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap" rel="stylesheet">
    <!-- Boxicons for the calendar icon -->
    <link href='https://unpkg.com/boxicons@2.1.4/css/boxicons.min.css' rel='stylesheet'>
    <link rel="stylesheet" href="style.css">
</head>
<body>

<div class="container">
    <div class="section-header">
        <h1>{title_text.split()[0]} <span>{' '.join(title_text.split()[1:]) if len(title_text.split()) > 1 else 'Timeline'}</span></h1>
        <p>{body_text}</p>
    </div>

    <div class="timeline-grid">
        <!-- Column 1: Education -->
        <div class="timeline-column" data-col="0">
            <h2 class="column-title">Education</h2>
            <div class="timeline-wrapper">
                
                <div class="timeline-card">
                    <div class="card-year"><i class='bx bxs-calendar'></i> 2021 - 2023</div>
                    <h3 class="card-title">Master's in Computer Science</h3>
                    <p class="card-desc">Advanced studies focusing on machine learning, distributed systems, and modern web architectures. Graduated with honors.</p>
                </div>
                
                <div class="timeline-card">
                    <div class="card-year"><i class='bx bxs-calendar'></i> 2017 - 2021</div>
                    <h3 class="card-title">Bachelor of Engineering</h3>
                    <p class="card-desc">Foundational knowledge in software engineering, data structures, algorithms, and database management systems.</p>
                </div>

                <div class="timeline-card">
                    <div class="card-year"><i class='bx bxs-calendar'></i> 2015 - 2017</div>
                    <h3 class="card-title">High School Diploma</h3>
                    <p class="card-desc">Specialized in mathematics and physics. Participated in regional coding competitions and robotics clubs.</p>
                </div>

            </div>
        </div>

        <!-- Column 2: Experience -->
        <div class="timeline-column" data-col="1">
            <h2 class="column-title">Experience</h2>
            <div class="timeline-wrapper">
                
                <div class="timeline-card">
                    <div class="card-year"><i class='bx bxs-briefcase'></i> 2023 - Present</div>
                    <h3 class="card-title">Senior Frontend Engineer</h3>
                    <p class="card-desc">Leading a team of 4 developers to build high-performance React applications. Decreased initial load times by 45% through code splitting.</p>
                </div>
                
                <div class="timeline-card">
                    <div class="card-year"><i class='bx bxs-briefcase'></i> 2021 - 2023</div>
                    <h3 class="card-title">UI/UX Developer</h3>
                    <p class="card-desc">Bridged the gap between design and engineering. Created a comprehensive design system utilized across 3 core product lines.</p>
                </div>

                <div class="timeline-card">
                    <div class="card-year"><i class='bx bxs-briefcase'></i> 2019 - 2021</div>
                    <h3 class="card-title">Web Development Intern</h3>
                    <p class="card-desc">Assisted in maintaining legacy PHP applications and spearheaded the migration to modern modular JavaScript frameworks.</p>
                </div>

            </div>
        </div>
    </div>
</div>

<script src="script.js"></script>
</body>
</html>
"""

    js = """// Neon Vertical Timeline Animation System
document.addEventListener('DOMContentLoaded', () => {
    
    // Configure Intersection Observer
    const observerOptions = {
        root: null,
        rootMargin: '0px 0px -50px 0px', // Trigger slightly before the item enters the viewport fully
        threshold: 0.1
    };

    const observer = new IntersectionObserver((entries, observer) => {
        entries.forEach((entry) => {
            if (entry.isIntersecting) {
                // Read the dynamic delay assigned during setup
                const delay = entry.target.getAttribute('data-delay') || '0s';
                entry.target.style.animationDelay = delay;
                
                // Trigger the CSS animation
                entry.target.classList.add('in-view');
                
                // Stop observing once animated to prevent repeating
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    // Prepare and observe all timeline cards
    const cards = document.querySelectorAll('.timeline-card');
    
    cards.forEach((card) => {
        // Find out which column and row this card is in for staggered cascading delays
        const column = card.closest('.timeline-column');
        const colIndex = parseInt(column.getAttribute('data-col') || '0');
        
        // Find index of the card within its wrapper
        const wrapper = card.parentElement;
        const siblings = Array.from(wrapper.children);
        const rowIndex = siblings.indexOf(card);
        
        // Calculate delay: rows cascade down (+0.2s per row), 
        // secondary column slightly delayed (+0.15s) relative to the first
        const delay = (rowIndex * 0.2) + (colIndex * 0.15);
        
        // Assign delay and observe
        card.setAttribute('data-delay', `${delay}s`);
        observer.observe(card);
    });
});
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

* **Accessibility**: 
  - Semantic HTML tags (`<h1>`, `<h2>`, `<h3>`, `<p>`) are utilized to maintain proper screen reader hierarchy instead of using un-styled `<div>` elements.
  - Contrast ratios for the placeholder dark theme (Light gray text against dark surface) comfortably pass WCAG AA standards.
  - The decorative icons from Boxicons should ideally have `aria-hidden="true"` applied to them in production so screen readers do not attempt to parse them.
* **Performance**:
  - The scrolling reveal effect uses the `IntersectionObserver` API rather than bounding box calculations inside a `scroll` event listener. This offloads the tracking to the browser's native API, eliminating main-thread jank and scroll lagging.
  - Animations target `transform` and `opacity`, which can be hardware-accelerated by the GPU, ensuring consistent 60fps motion. Avoid animating properties like `margin-left` or `width` which trigger expensive layout reflows.