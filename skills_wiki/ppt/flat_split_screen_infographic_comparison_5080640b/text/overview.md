# Flat Split-Screen Infographic Comparison

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Flat Split-Screen Infographic Comparison

* **Core Visual Mechanism**: This design relies on **stark color blocking** and **macro-typography**. The slide is split cleanly into two contrasting vertical zones (a vibrant accent color vs. a deep neutral background). Large, oversized numeric percentages dominate the visual hierarchy, paired with flat, borderless vector illustrations. A dark, full-width footer anchors the bottom, containing secondary micro-statistics.
* **Why Use This Skill (Rationale)**: The split-screen layout forces a direct visual comparison between two primary data points (e.g., A/B testing results, demographic splits, "Us vs. Them"). The removal of 3D effects, shadows, and gradients reduces cognitive load, allowing the giant numbers to act as the primary visual anchors.
* **Overall Applicability**: Ideal for data summary slides, survey results, demographic comparisons, A/B testing readouts, and high-level dashboard presentations. 
* **Value Addition**: It transforms dry, bulleted statistics into an instantly readable poster-style infographic. The combination of macro (huge top numbers) and micro (small footer numbers) creates a structured narrative flow.

### 2. Visual Breakdown

* **Step A: Core Visual Elements**
  - **Color Logic**:
    - Left Panel Fill: Vibrant Yellow/Orange `RGBA(255, 184, 0, 255)`
    - Right Panel Fill: Dark Navy/Slate `RGBA(31, 38, 46, 255)`
    - Footer Banner Fill: Near Black `RGBA(38, 38, 38, 255)`
    - Text Color: Pure White `RGBA(255, 255, 255, 255)`
  - **Text Hierarchy**:
    - **Macro Value**: 76pt Century Gothic (e.g., "98%")
    - **Header/Title**: 28pt Century Gothic
    - **Sub-label**: 24pt Century Gothic
    - **Footer Value**: 36pt Century Gothic
    - **Footer Label**: 16pt Century Gothic
  - **Graphics**: Flat, geometric vector-style illustrations inside circular base plates.

* **Step B: Compositional Style**
  - **Spatial Division**: Top 75% of the slide is split exactly 50/50 vertically. The bottom 25% is a unified horizontal footer.
  - **Grid**: Within each half, text is heavily left-aligned, occupying the left 60% of the block, while the illustration anchors the right 40% of the block.

* **Step C: Dynamic Effects & Transitions**
  - Best animated using simple "Fade" or "Wipe from Left/Right" on the text elements, bringing in the background blocks first, then the macro values, then the footer stats. (Achieved manually in PPT).

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **Color Blocking & Layout** | `python-pptx` shapes | Perfect for exact geometric placement, background rectangles, and clean text rendering. |
| **Flat Vector Illustrations** | `PIL` (Pillow) | We don't have the external chef assets from the video. PIL allows us to programmatically generate clean, flat-design geometric icons (bar charts/pie charts) with alpha transparency, mimicking the infographic style without needing external files. |
| **Macro Typography** | `python-pptx` text frames | Direct control over font sizes, weights, and word-wrap for crisp data presentation. |

*Feasibility Assessment*: **95%**. The code perfectly recreates the split layout, the stark color logic, the typographic hierarchy, and the footer grid. Instead of specific character illustrations, it generates high-quality flat geometric data graphics that fit the infographic theme perfectly and make the code fully self-contained.

#### 3b. Complete Reproduction Code

```python
def create_slide(
    output_pptx_path: str,
    left_title: str = "Total Respondents",
    left_label: str = "Respondents",
    left_val: str = "98%",
    right_title: str = "Favorite Food Type",
    right_label: str = "Pizza & Burger",
    right_val: str = "54%",
    footer_stats: list = None
) -> str:
    """
    Create a PPTX file reproducing the Flat Split-Screen Infographic Comparison effect.
    """
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    from pptx.enum.text import PP_ALIGN
    from pptx.enum.shapes import MSO_SHAPE
    from PIL import Image, ImageDraw
    import os

    if footer_stats is None:
        footer_stats = [
            {"val": "55%", "label": "Male Respondent"},
            {"val": "45%", "label": "Female Respondent"},
            {"val": "20%", "label": "Kabab & Grills"},
            {"val": "14%", "label": "Rice & Curries"}
        ]

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6]) # Blank layout

    # --- Colors ---
    c_left = RGBColor(255, 184, 0)
    c_right = RGBColor(31, 38, 46)
    c_footer = RGBColor(38, 38, 38)
    c_white = RGBColor(255, 255, 255)

    # --- Helper: Add Shape ---
    def add_rect(left, top, width, height, color):
        rect = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, width, height)
        rect.fill.solid()
        rect.fill.fore_color.rgb = color
        rect.line.fill.background()
        return rect

    # --- Helper: Add Text ---
    def add_text(left, top, width, height, text, font_size, bold=True, color=c_white):
        txBox = slide.shapes.add_textbox(left, top, width, height)
        tf = txBox.text_frame
        tf.word_wrap = False
        p = tf.paragraphs[0]
        p.text = text
        p.alignment = PP_ALIGN.LEFT
        p.font.size = Pt(font_size)
        p.font.name = 'Century Gothic'
        p.font.bold = bold
        p.font.color.rgb = color
        return txBox

    # --- Layer 1: Background Blocks ---
    # Left Block
    add_rect(0, 0, Inches(6.666), Inches(5.5), c_left)
    # Right Block
    add_rect(Inches(6.666), 0, Inches(6.667), Inches(5.5), c_right)
    # Footer Banner
    add_rect(0, Inches(5.5), Inches(13.333), Inches(2.0), c_footer)

    # --- Layer 2: Generate PIL Infographic Assets ---
    tmp_files = []
    
    # Left Main Graphic (Bar Chart)
    f_left_img = "tmp_left.png"
    img_l = Image.new('RGBA', (400, 400), (255, 255, 255, 0))
    draw_l = ImageDraw.Draw(img_l)
    draw_l.ellipse([20, 20, 380, 380], fill=(230, 160, 0, 255)) # Darker yellow circle
    draw_l.rectangle([100, 200, 150, 320], fill=(255, 255, 255, 255))
    draw_l.rectangle([175, 120, 225, 320], fill=(255, 255, 255, 255))
    draw_l.rectangle([250, 260, 300, 320], fill=(255, 255, 255, 255))
    img_l.save(f_left_img)
    tmp_files.append(f_left_img)

    # Right Main Graphic (Pie Chart)
    f_right_img = "tmp_right.png"
    img_r = Image.new('RGBA', (400, 400), (255, 255, 255, 0))
    draw_r = ImageDraw.Draw(img_r)
    draw_r.ellipse([20, 20, 380, 380], fill=(45, 55, 68, 255)) # Lighter navy circle
    draw_r.pieslice([80, 80, 320, 320], 0, 240, fill=(255, 255, 255, 255))
    draw_r.pieslice([90, 70, 330, 310], 240, 360, fill=(255, 184, 0, 255)) # Pop accent
    img_r.save(f_right_img)
    tmp_files.append(f_right_img)

    # Small Footer Icons
    symbols = ['circle', 'square', 'triangle', 'diamond']
    footer_icons = []
    for i, sym in enumerate(symbols):
        f_name = f"tmp_icon_{i}.png"
        img_i = Image.new('RGBA', (100, 100), (255, 255, 255, 0))
        draw_i = ImageDraw.Draw(img_i)
        # Left side gets yellow backgrounds, Right side gets navy backgrounds
        bg_c = (255, 184, 0, 255) if i < 2 else (45, 55, 68, 255)
        draw_i.ellipse([5, 5, 95, 95], fill=bg_c)
        if sym == 'circle':
            draw_i.ellipse([35, 35, 65, 65], fill=(255, 255, 255, 255))
        elif sym == 'square':
            draw_i.rectangle([35, 35, 65, 65], fill=(255, 255, 255, 255))
        elif sym == 'triangle':
            draw_i.polygon([(50, 30), (70, 70), (30, 70)], fill=(255, 255, 255, 255))
        elif sym == 'diamond':
            draw_i.polygon([(50, 25), (75, 50), (50, 75), (25, 50)], fill=(255, 255, 255, 255))
        img_i.save(f_name)
        footer_icons.append(f_name)
        tmp_files.append(f_name)

    # --- Layer 3: Typography & Content Placement ---

    # Left Top Data
    add_text(Inches(0.5), Inches(0.5), Inches(4.0), Inches(0.5), left_title, 28)
    add_text(Inches(0.5), Inches(2.2), Inches(3.0), Inches(0.5), left_label, 24)
    add_text(Inches(0.4), Inches(2.6), Inches(3.0), Inches(1.5), left_val, 76)
    slide.shapes.add_picture(f_left_img, Inches(3.3), Inches(1.8), Inches(3.0), Inches(3.0))

    # Right Top Data
    add_text(Inches(7.166), Inches(0.5), Inches(4.0), Inches(0.5), right_title, 28)
    add_text(Inches(7.166), Inches(2.2), Inches(3.0), Inches(0.5), right_label, 24)
    add_text(Inches(7.066), Inches(2.6), Inches(3.0), Inches(1.5), right_val, 76)
    slide.shapes.add_picture(f_right_img, Inches(9.966), Inches(1.8), Inches(3.0), Inches(3.0))

    # Footer Row Data
    anchors = [0.8, 3.8, 7.5, 10.5] # Left X positions for the 4 footer items
    for i in range(4):
        if i < len(footer_stats):
            x_base = anchors[i]
            slide.shapes.add_picture(footer_icons[i], Inches(x_base), Inches(5.8), Inches(0.7), Inches(0.7))
            add_text(Inches(x_base + 0.8), Inches(5.75), Inches(1.5), Inches(0.8), footer_stats[i]['val'], 36)
            add_text(Inches(x_base), Inches(6.6), Inches(2.5), Inches(0.4), footer_stats[i]['label'], 16)

    # Save Presentation
    prs.save(output_pptx_path)

    # Cleanup temp images
    for f in tmp_files:
        if os.path.exists(f):
            os.remove(f)

    return output_pptx_path
```