### 1. High-level Design Pattern Extraction

> **Skill Name**: High-Conversion Cinematic Hero Section

* **Core Visual Mechanism**: A full-viewport, dark-themed hero layout optimized for psychological conversion. It utilizes a striking split layout: text and primary calls-to-action (CTAs) anchored on one side, balanced by a dominant, thematic visual on the other. Key to this pattern is the integration of trust signals directly into the hero view—specifically, a social proof "avatar stack" near the primary button and a muted "authority badge" banner along the bottom.
* **Why Use This Skill (Rationale)**: This design pattern moves beyond just looking good; it employs conversion rate optimization (CRO) principles. The high contrast of a dark background with white text and a vivid accent color (like red) draws immediate attention to the value proposition. Ghost buttons for secondary actions preserve visual hierarchy, ensuring the primary CTA stands out. Adding "social proof" (avatars) reduces friction by showing others have taken the action, and authority badges (logos) establish immediate trust.
* **Overall Applicability**: Ideal for SaaS landing pages, gaming portals, event registrations, or any high-stakes campaign where driving a specific user action (like signing up or joining) is the primary goal.
* **Value Addition**: Transforms a basic informational header into an active funnel. By strategically placing trust markers and using contrast to guide the eye, it significantly increases the likelihood of user interaction compared to a standard, static hero image.
* **Browser Compatibility**: Fully supported across all modern browsers. Relies on standard CSS Flexbox, negative margins (for the avatar stack), and CSS filters (for grayscale logos).

### 2. Visual & Technical Breakdown

* **Step A: Core Visual Elements**
  - **Color Logic**: Deep cinematic dark background (e.g., `#0b0f19`), high-contrast primary text (`#ffffff`), muted secondary text (`#94a3b8`), and a highly saturated accent color for primary actions (`#e62429` - Rebel Red).
  - **Typography**: A bold, commanding sans-serif for headings (e.g., 'Inter' with `font-weight: 800`), creating a "poster-like" feel.
  - **Key CSS Properties**:
    - `filter: grayscale(100%) opacity(0.5)` for trust badges to keep them from distracting from the main CTA.
    - `border-radius: 50%` and borders matching the background color to create the overlapping avatar stack effect.

* **Step B: Layout & Compositional Style**
  - **Layout System**: CSS Flexbox handles both the macro layout (header, main hero body, footer badges) and micro layouts (nav items, avatar stacks).
  - **Spatial Feel**: Ample whitespace (padding) around the text container prevents claustrophobia despite the dark theme. The layout is weighted; the text container typically spans ~50-60% of the width, allowing the visual element room to breathe.
  - **Z-index Layering**: Avatars in the stack overlap using negative margins. The borders on the avatars visually separate them, creating depth.

* **Step C: Interactive Behavior & Animations**
  - **Hover States**: Ghost buttons gain a slight background fill on hover; primary buttons might scale up slightly or increase shadow opacity.
  - **Focus**: The design draws the eye in a Z-pattern: Logo -> Nav -> Headline -> Avatar Stack -> Primary CTA -> Trust Badges.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| Cinematic Dark Theme | CSS custom properties | Easy to theme, ensures high contrast for conversion elements. |
| Split Layout & Positioning | CSS Flexbox | Provides the most robust way to handle the text-left, image-right alignment and vertically center content. |
| Avatar Stack (Social Proof) | CSS negative margins | Cleanest, pure-CSS way to overlap circular elements while maintaining document flow. |
| Muted Trust Badges | CSS Filters | `grayscale` and `opacity` allow use of any generic logo image while forcing it to fit the background aesthetic seamlessly. |

> **Feasibility Assessment**: 100% reproduction of the layout, structural pattern, and conversion elements demonstrated in the tutorial's Figma design phase. (Note: Instead of linking to external, potentially volatile Star Wars stock photography, a purely CSS-based cinematic background and placeholder is used to ensure the generated component runs flawlessly).

#### 3b. Complete Reproduction Code

```python
def create_component(
    output_dir: str,
    title_text: str = "It's your universe, it's time to save it.",
    body_text: str = "The Rebel alliance is fighting to get rid of the evil empire. Join the resistance to create a better future for your children.",
    color_scheme: str = "dark",
    accent_color: str = "#e62429", # Rebel Red
    width_px: int = 1440,
    height_px: int = 900,
    **kwargs,
) -> dict:
    """
    Creates a high-converting, cinematic dark hero component with social proof.
    """
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Force dark scheme for this specific cinematic aesthetic, but allow fallback
    bg_color = "#0b0f19" if color_scheme == "dark" else "#f8f9fa"
    text_color = "#ffffff" if color_scheme == "dark" else "#111827"
    text_muted = "#94a3b8" if color_scheme == "dark" else "#6b7280"
    surface_bg = "rgba(255, 255, 255, 0.05)" if color_scheme == "dark" else "rgba(0, 0, 0, 0.05)"

    css = f"""/* High-Conversion Cinematic Hero */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700;800&display=swap');

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
    --surface: {surface_bg};
    --font-main: 'Inter', sans-serif;
}}

body {{
    font-family: var(--font-main);
    background-color: var(--bg);
    /* Cinematic radial gradient background */
    background-image: radial-gradient(circle at 70% 50%, rgba(230, 36, 41, 0.08) 0%, transparent 50%), 
                      radial-gradient(circle at 20% 80%, rgba(255, 255, 255, 0.03) 0%, transparent 40%);
    color: var(--text);
    min-height: 100vh;
    display: flex;
    justify-content: center;
}}

.hero-wrapper {{
    width: 100%;
    max-width: {width_px}px;
    min-height: {height_px}px;
    display: flex;
    flex-direction: column;
    position: relative;
    overflow: hidden;
}}

/* Header / Nav */
.header {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 2rem 5%;
    z-index: 10;
}}

.logo {{
    font-size: 1.5rem;
    font-weight: 800;
    letter-spacing: -0.05em;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}}

.logo-icon {{
    color: var(--accent);
}}

.nav-links {{
    display: flex;
    gap: 2.5rem;
}}

.nav-links a {{
    color: var(--text-muted);
    text-decoration: none;
    font-weight: 500;
    font-size: 0.95rem;
    transition: color 0.2s ease;
}}

.nav-links a:hover {{
    color: var(--text);
}}

.btn {{
    padding: 0.75rem 1.5rem;
    border-radius: 4px;
    font-weight: 700;
    font-size: 0.9rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    cursor: pointer;
    transition: all 0.2s ease;
    text-decoration: none;
    display: inline-flex;
    align-items: center;
    justify-content: center;
}}

.btn-ghost {{
    background: transparent;
    border: 2px solid var(--surface);
    color: var(--text);
}}

.btn-ghost:hover {{
    border-color: var(--text);
    background: var(--surface);
}}

.btn-primary {{
    background: var(--accent);
    border: 2px solid var(--accent);
    color: #fff;
    box-shadow: 0 4px 14px rgba(230, 36, 41, 0.4);
}}

.btn-primary:hover {{
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(230, 36, 41, 0.6);
}}

/* Main Hero Area */
.hero-main {{
    flex: 1;
    display: flex;
    align-items: center;
    padding: 0 5%;
    gap: 4rem;
    z-index: 2;
}}

.hero-content {{
    flex: 1;
    max-width: 650px;
}}

.hero-title {{
    font-size: clamp(3rem, 5vw, 4.5rem);
    font-weight: 800;
    line-height: 1.1;
    margin-bottom: 1.5rem;
    letter-spacing: -0.03em;
}}

.hero-body {{
    font-size: 1.25rem;
    color: var(--text-muted);
    line-height: 1.6;
    margin-bottom: 2.5rem;
    max-width: 550px;
}}

.hero-actions {{
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
}}

/* Social Proof Stack */
.social-proof {{
    display: flex;
    align-items: center;
    gap: 1rem;
}}

.avatar-stack {{
    display: flex;
}}

.avatar {{
    width: 36px;
    height: 36px;
    border-radius: 50%;
    border: 2px solid var(--bg);
    background-color: var(--surface);
    object-fit: cover;
}}

.avatar:not(:first-child) {{
    margin-left: -12px;
}}

.proof-text {{
    font-size: 0.9rem;
    color: var(--text-muted);
    font-weight: 500;
}}

.proof-highlight {{
    color: var(--text);
    font-weight: 700;
}}

/* Visual Side Placeholder */
.hero-visual {{
    flex: 1;
    display: flex;
    justify-content: center;
    align-items: center;
    position: relative;
}}

.visual-placeholder {{
    width: 80%;
    aspect-ratio: 1;
    background: var(--surface);
    border-radius: 50%;
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--text-muted);
    font-size: 0.8rem;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    border: 1px dashed rgba(255,255,255,0.1);
}}

/* Trust Badges */
.trust-bar {{
    padding: 2rem 5% 3rem;
    display: flex;
    align-items: center;
    gap: 2rem;
    z-index: 2;
}}

.trust-label {{
    font-size: 0.85rem;
    color: var(--text-muted);
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}}

.trust-logos {{
    display: flex;
    gap: 3rem;
    align-items: center;
    opacity: 0.4;
    filter: grayscale(100%) contrast(200%);
    transition: opacity 0.3s ease;
}}

.trust-logos:hover {{
    opacity: 0.8;
}}

.trust-logo-placeholder {{
    font-weight: 800;
    font-size: 1.2rem;
    letter-spacing: -0.05em;
}}

@media (max-width: 968px) {{
    .hero-main {{
        flex-direction: column;
        justify-content: center;
        text-align: center;
        padding-top: 2rem;
    }}
    .hero-content {{
        display: flex;
        flex-direction: column;
        align-items: center;
    }}
    .hero-visual {{
        display: none; /* Hide placeholder on mobile for tighter layout */
    }}
    .nav-links {{
        display: none;
    }}
    .trust-bar {{
        flex-direction: column;
        gap: 1.5rem;
    }}
}}
"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>High-Conversion Hero</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="hero-wrapper">
        
        <!-- Navigation -->
        <header class="header">
            <div class="logo">
                <span class="logo-icon">★</span> REBEL
            </div>
            <nav class="nav-links">
                <a href="#ships">Our Ships</a>
                <a href="#mission">Mission</a>
                <a href="#donations">Donations</a>
            </nav>
            <a href="#" class="btn btn-ghost">Join Now</a>
        </header>

        <!-- Main Content -->
        <main class="hero-main">
            <div class="hero-content">
                <h1 class="hero-title">{title_text}</h1>
                <p class="hero-body">{body_text}</p>
                
                <div class="hero-actions">
                    <div>
                        <a href="#" class="btn btn-primary">Join Now For Free</a>
                    </div>
                    
                    <!-- Social Proof Mechanism -->
                    <div class="social-proof">
                        <div class="avatar-stack">
                            <img src="https://i.pravatar.cc/100?img=11" alt="Member" class="avatar">
                            <img src="https://i.pravatar.cc/100?img=33" alt="Member" class="avatar">
                            <img src="https://i.pravatar.cc/100?img=12" alt="Member" class="avatar">
                            <img src="https://i.pravatar.cc/100?img=68" alt="Member" class="avatar">
                        </div>
                        <div class="proof-text">
                            <span class="proof-highlight">Obi Wan</span> and 4,000 others have already joined
                        </div>
                    </div>
                </div>
            </div>

            <!-- Visual Space -->
            <div class="hero-visual">
                <div class="visual-placeholder">
                    [ Epic Ship Image Here ]
                </div>
            </div>
        </main>

        <!-- Trust Badges Mechanism -->
        <footer class="trust-bar">
            <div class="trust-label">As Seen On:</div>
            <div class="trust-logos">
                <div class="trust-logo-placeholder">NEWS CORP</div>
                <div class="trust-logo-placeholder">GLOBAL MEDIA</div>
                <div class="trust-logo-placeholder">TECH INSIDER</div>
                <div class="trust-logo-placeholder">THE DAILY</div>
            </div>
        </footer>

    </div>
    <script src="script.js"></script>
</body>
</html>
"""

    js = """// High-Conversion Hero Interactions
document.addEventListener('DOMContentLoaded', () => {
    // Add subtle hover effects or entry animations here if desired.
    // The core pattern relies heavily on layout and pure CSS for conversion cues.
    
    console.log("Hero component loaded. Ready for conversion tracking.");
});
"""

    # Write files
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