# Documentary-Style Speaker Overlay

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Documentary-Style Speaker Overlay

* **Core Visual Mechanism**: A solid, full-height, dark-toned rectangular panel anchored to the left edge of the screen, acting as a high-contrast matte for elegant typography. It juxtaposes large, classic Serif fonts (for the human element/name) against heavily tracked (letter-spaced) Sans-Serif fonts (for corporate/brand entities), layered over a real-world video feed or photographic background.
* **Why Use This Skill (Rationale)**: This layout provides critical context (who is speaking, their affiliation) without cluttering or obscuring the main subject. The use of dark, desaturated navy paired with white typography conveys authority, tradition, and premium value. The vertical layout feels cinematic, echoing high-end documentary interviews.
* **Overall Applicability**: Ideal for video overlays, speaker introductions, webinar title cards, executive summaries, or any presentation slide where a prominent photograph of a person or product occupies the right 2/3 of the canvas.
* **Value Addition**: Compared to standard lower-thirds or bullet points, this full-height sidebar establishes a strict visual hierarchy. The integration of advanced typographic tracking (letter spacing) elevates the design from "basic PowerPoint" to a polished, professional broadcast aesthetic.

### 2. Visual Breakdown

* **Step A: Core Visual Elements**
  - **Color Logic**:
    - **Panel Background**: Deep, desaturated Navy Blue `(16, 21, 34, 255)`. It is nearly black but retains a cool undertone to feel modern.
    - **Primary Text**: Pure White `(255, 255, 255, 255)`.
    - **Secondary/Dimmed Text**: Light Slate Grey `(170, 180, 190, 255)` for less important connecting words.
  - **Text Hierarchy**:
    - *Top Logo/Brand*: Small, Sans-Serif (e.g., Arial), All-Caps, heavily letter-spaced (tracked).
    - *Subject Name*: Very large, classic Serif (e.g., Georgia or Times New Roman), regular weight, split across two lines.
    - *Footer Info*: Small italicized Serif for transition words, followed by tracked bold Sans-Serif for the partner brand.

* **Step B: Compositional Style**
  - **Proportions**: The dark overlay panel occupies exactly ~33% (1/3) of the slide width.
  - **Margins**: Generous internal padding within the panel. Elements are strictly left-aligned, starting roughly 0.8 inches from the left edge to breathe.
  - **Vertical Pacing**: Elements are anchored to the top (10% down), center (40% down), and bottom (85% down) to balance the column.

* **Step C: Dynamic Effects & Transitions**
  - In video editing, this panel slides in smoothly from the left edge (`Fly In` animation from left). The text fades in shortly after.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| Layout & Flat Shapes | `python-pptx` native | Native shapes provide the crispest rendering for solid geometric overlays and keep the text fully editable for the user. |
| Typographic Tracking | `lxml` XML injection | `python-pptx` natively lacks an API to adjust letter spacing (tracking). We must manipulate the OOXML `<a:rPr spc="...">` directly to achieve the premium brand aesthetic. |
| Contextual Background | `urllib` + native picture | Downloads a simulated "interview video feed" background to accurately demonstrate how the overlay interacts with underlying imagery. |

> **Feasibility Assessment**: 95% — The code perfectly reproduces the static layout, typography, proportions, and colors of the broadcast overlay. The only missing element is the video motion (sliding in), which can be easily added via PowerPoint's native animation pane.

#### 3b. Complete Reproduction Code

```python
def create_slide(
    output_pptx_path: str,
    speaker_name: str = "Mike\nVernal",
    main_brand: str = "SEQUOIA",
    partner_brand: str = "NFX",
    bg_image_url: str = "https://images.unsplash.com/photo-1556761175-5973dc0f32e7?q=80&w=1920&auto=format&fit=crop",
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the 'Documentary-Style Speaker Overlay' visual effect.
    
    Returns: path to the saved PPTX file.
    """
    import os
    import urllib.request
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    from pptx.enum.shapes import MSO_SHAPE
    
    # Helper function to inject letter spacing (tracking) via lxml
    def apply_tracking(run, pt_spacing: float):
        """Injects letter spacing into a text run. pt_spacing is converted to 1/100ths of a point."""
        rPr = run._r.get_or_add_rPr()
        # The 'spc' attribute in OOXML DrawingML represents spacing in 1/100ths of a point.
        spacing_val = int(pt_spacing * 100)
        rPr.set('spc', str(spacing_val))

    # Initialize presentation (16:9 aspect ratio)
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    # Use blank layout
    blank_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(blank_layout)

    # === Layer 1: Simulated Video Background ===
    bg_img_path = "temp_bg.jpg"
    try:
        req = urllib.request.Request(bg_image_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response, open(bg_img_path, 'wb') as out_file:
            out_file.write(response.read())
        slide.shapes.add_picture(bg_img_path, 0, 0, width=prs.slide_width, height=prs.slide_height)
    except Exception as e:
        print(f"Image download failed, using fallback background. Error: {e}")
        # Fallback background
        bg_shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
        bg_shape.fill.solid()
        bg_shape.fill.fore_color.rgb = RGBColor(50, 50, 50)
        bg_shape.line.fill.background()

    # === Layer 2: The Dark Overlay Panel ===
    # Covers left ~33% of the screen
    panel_width = Inches(4.5)
    panel = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, panel_width, prs.slide_height)
    panel.fill.solid()
    panel.fill.fore_color.rgb = RGBColor(16, 21, 34)  # Deep desaturated Navy
    panel.line.fill.background() # Remove outline

    # === Layer 3: Typography & Content ===
    left_margin = Inches(0.8)

    # 1. Top Brand Logo (Small, Sans-Serif, Highly Tracked)
    top_box = slide.shapes.add_textbox(left_margin, Inches(0.8), panel_width - left_margin, Inches(0.5))
    tf_top = top_box.text_frame
    p_top = tf_top.paragraphs[0]
    run_top = p_top.add_run()
    run_top.text = main_brand.upper()
    run_top.font.name = "Arial"
    run_top.font.size = Pt(14)
    run_top.font.bold = True
    run_top.font.color.rgb = RGBColor(255, 255, 255)
    apply_tracking(run_top, 5.0) # Add 5pt letter spacing for premium look

    # 2. Main Subject Name (Large, Serif)
    mid_box = slide.shapes.add_textbox(left_margin, Inches(2.8), panel_width - left_margin, Inches(2.0))
    tf_mid = mid_box.text_frame
    tf_mid.word_wrap = True
    p_mid = tf_mid.paragraphs[0]
    run_mid = p_mid.add_run()
    run_mid.text = speaker_name
    run_mid.font.name = "Georgia"
    run_mid.font.size = Pt(54)
    run_mid.font.color.rgb = RGBColor(255, 255, 255)

    # 3. Footer Context (Mix of Serif Italic and Tracked Sans-Serif)
    bot_box = slide.shapes.add_textbox(left_margin, Inches(6.0), panel_width - left_margin, Inches(1.0))
    tf_bot = bot_box.text_frame
    
    p_bot1 = tf_bot.paragraphs[0]
    run_bot1 = p_bot1.add_run()
    run_bot1.text = "in partnership with"
    run_bot1.font.name = "Georgia"
    run_bot1.font.italic = True
    run_bot1.font.size = Pt(14)
    run_bot1.font.color.rgb = RGBColor(170, 180, 190)

    p_bot2 = tf_bot.add_paragraph()
    run_bot2 = p_bot2.add_run()
    run_bot2.text = partner_brand.upper()
    run_bot2.font.name = "Arial"
    run_bot2.font.bold = True
    run_bot2.font.size = Pt(22)
    run_bot2.font.color.rgb = RGBColor(255, 255, 255)
    apply_tracking(run_bot2, 4.0) # Add 4pt letter spacing

    # Save and cleanup
    prs.save(output_pptx_path)
    if os.path.exists(bg_img_path):
        os.remove(bg_img_path)
        
    return output_pptx_path
```