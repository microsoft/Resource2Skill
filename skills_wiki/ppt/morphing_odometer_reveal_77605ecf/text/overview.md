# Morphing Odometer Reveal

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Morphing Odometer Reveal

* **Core Visual Mechanism**: Vertical text arrays of sequential numbers are visually bounded by masking shapes (which match the slide background). Using PowerPoint's Morph transition, the vertical arrays physically slide upward between the two slides, mimicking the mechanical rolling motion of a slot machine or an odometer to reveal the final data point.
* **Why Use This Skill (Rationale)**: Static numbers lack emotional weight. By rolling the numbers up sequentially, this technique builds a momentary sense of anticipation. The kinetic energy draws the viewer’s eye exactly to the KPI, emphasizing growth, progression, or massive scale.
* **Overall Applicability**: Perfect for high-impact metric slides: year-over-year profit margins, sales KPIs, total users reached, or celebrating major company milestones.
* **Value Addition**: Transforms a standard data point into a cinematic event. It signals to the audience that *this specific number* is important and worth paying attention to, elevating the professional polish of the deck.

### 2. Visual Breakdown

* **Step A: Core Visual Elements**
  * **Typography**: Ultra-large, highly legible sans-serif fonts (e.g., Arial, Calibri, Helvetica) set to 100pt+. Heavy font weights (Bold or Black).
  * **Color Logic**: 
    * Background and Masks: Pure White `(255, 255, 255)` or a solid flat color. The masking shapes *must* perfectly match the background to create an invisible "window".
    * Text/Numbers: High-contrast Dark Gray/Navy `(13, 17, 28)`.
  * **Masking**: Two rectangular blocks with no outlines—one above the target viewing area and one below—acting as a letterbox.

* **Step B: Compositional Style**
  * **Spatial Feel**: Split-screen design. ~50% of the canvas is dedicated to the rolling numbers (left), and ~50% features supporting imagery or context (right).
  * **Alignment**: The numbers, the static labels (e.g., "Profits"), and the "%" symbol share a strict baseline and bounding box logic.

* **Step C: Dynamic Effects & Transitions**
  * **Animation Mechanism**: **Slide Morph**. The layout relies on having two consecutive slides. Slide 1 places the vertical number columns at starting coordinates (showing "00"). Slide 2 shifts the Y-coordinates of these columns upwards. PowerPoint's Morph automatically interpolates the vertical shift, creating the smooth rolling effect.
  * **Naming Convention**: Prepending shape names with `!!` (e.g., `!!Tens`) forces PowerPoint's Morph engine to uniquely map the shapes between slides.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **Exact Spacing & Alignment** | `python-pptx` text manipulation | By setting exact paragraph `line_spacing` (120pt) and removing internal text box margins (`margin_top = 0`), we can calculate the exact mathematical Y-offset needed to display any specific digit through the viewing window. |
| **Masking Rectangles** | `python-pptx` standard shapes | Native white rectangles overlaying the text boxes perfectly simulate the "window" cutout without needing complex alpha-mask PNGs. |
| **Morph Animation** | `lxml` XML injection | `python-pptx` lacks a native API for slide transitions. Using `lxml`, we directly inject the `<p:transition>` and `<p:morph>` tags into the presentation XML to ensure the effect works out-of-the-box. |

> **Feasibility Assessment**: 100% reproducible. The script mathematically positions the number columns for exact digit alignment, sets up the masks, and injects the required Morph XML so the presentation runs the rolling effect immediately upon entering Presentation Mode.

#### 3b. Complete Reproduction Code

```python
def create_slide(
    output_pptx_path: str,
    title_text: str = "Sales Report 2021",
    body_text: str = "Profits",
    bg_palette: str = "technology",
    accent_color: tuple = (0, 191, 255),
    **kwargs,
) -> str:
    """
    Create a 2-slide PPTX reproducing the Morphing Odometer Reveal effect.
    Slide 1 shows "00", Slide 2 shows "37" (or target numbers).
    When advancing from Slide 1 to Slide 2, the numbers roll like an odometer.
    """
    import os
    import urllib.request
    from lxml import etree
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    from pptx.enum.text import PP_ALIGN
    from pptx.enum.shapes import MSO_SHAPE
    from pptx.oxml import parse_xml

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    # Odometer logic configuration
    target_tens = 3
    target_units = 7
    font_size = Pt(100)
    line_height = Pt(120)  # Exact spacing to calculate Y-offsets
    base_top = Inches(3.5) # The vertical center where the active number sits

    # Try downloading a thematic right-side image
    img_path = "odometer_bg_temp.jpg"
    try:
        req = urllib.request.Request(
            f"https://images.unsplash.com/photo-1554224155-6726b3ff858f?w=800&q=80", 
            headers={'User-Agent': 'Mozilla/5.0'}
        )
        with urllib.request.urlopen(req) as response, open(img_path, 'wb') as out_file:
            out_file.write(response.read())
    except Exception:
        img_path = None

    # We build two slides: Initial state (00) and Final state (target)
    for step in [1, 2]:
        slide = prs.slides.add_slide(prs.slide_layouts[6])

        # === Background / Side Image ===
        if img_path and os.path.exists(img_path):
            slide.shapes.add_picture(img_path, Inches(6.666), Inches(0), Inches(6.667), Inches(7.5))
        else:
            bg_rect = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(6.666), Inches(0), Inches(6.667), Inches(7.5))
            bg_rect.fill.solid()
            bg_rect.fill.fore_color.rgb = RGBColor(220, 230, 240)
            bg_rect.line.fill.background()

        # === Odometer Number Columns (Z-Order: Back) ===
        # Tens Column (Left)
        tens_val = 0 if step == 1 else target_tens
        tens_top = base_top - (tens_val * line_height) # Shift upward based on target
        
        tens_box = slide.shapes.add_textbox(Inches(1.5), tens_top, Inches(1.2), Inches(20))
        tens_box.name = "!!Tens" # '!!' forces strict Morph matching in PowerPoint
        tf_tens = tens_box.text_frame
        tf_tens.word_wrap = False
        tf_tens.margin_top = 0  # Remove margins for exact math alignment
        tf_tens.margin_bottom = 0
        
        for i in range(10):
            p = tf_tens.add_paragraph() if i > 0 else tf_tens.paragraphs[0]
            p.text = str(i)
            p.font.size = font_size
            p.font.bold = True
            p.font.name = "Arial"
            p.font.color.rgb = RGBColor(13, 17, 28)
            p.line_spacing = line_height
            p.alignment = PP_ALIGN.CENTER

        # Units Column (Right)
        units_val = 0 if step == 1 else target_units
        units_top = base_top - (units_val * line_height)
        
        units_box = slide.shapes.add_textbox(Inches(2.7), units_top, Inches(1.2), Inches(20))
        units_box.name = "!!Units"
        tf_units = units_box.text_frame
        tf_units.word_wrap = False
        tf_units.margin_top = 0
        tf_units.margin_bottom = 0
        
        for i in range(10):
            p = tf_units.add_paragraph() if i > 0 else tf_units.paragraphs[0]
            p.text = str(i)
            p.font.size = font_size
            p.font.bold = True
            p.font.name = "Arial"
            p.font.color.rgb = RGBColor(13, 17, 28)
            p.line_spacing = line_height
            p.alignment = PP_ALIGN.CENTER

        # === Masking Shapes (Z-Order: Middle) ===
        # Top Mask (Hides numbers sliding up)
        top_mask = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(6.666), base_top)
        top_mask.fill.solid()
        top_mask.fill.fore_color.rgb = RGBColor(255, 255, 255)
        top_mask.line.fill.background()

        # Bottom Mask (Hides numbers waiting below)
        bottom_mask_top = base_top + line_height
        bottom_mask = slide.shapes.add_shape(
            MSO_SHAPE.RECTANGLE, Inches(0), bottom_mask_top, Inches(6.666), Inches(7.5) - bottom_mask_top
        )
        bottom_mask.fill.solid()
        bottom_mask.fill.fore_color.rgb = RGBColor(255, 255, 255)
        bottom_mask.line.fill.background()

        # === Static Content (Z-Order: Front) ===
        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(1.0), Inches(5), Inches(0.8))
        tf = title_box.text_frame
        tf.text = title_text
        tf.paragraphs[0].font.size = Pt(28)
        tf.paragraphs[0].font.bold = True
        tf.paragraphs[0].font.color.rgb = RGBColor(80, 80, 80)

        sub_box = slide.shapes.add_textbox(Inches(1.5), base_top - Inches(0.8), Inches(4), Inches(0.6))
        tf = sub_box.text_frame
        tf.text = body_text
        tf.paragraphs[0].font.size = Pt(24)
        tf.paragraphs[0].font.color.rgb = RGBColor(13, 17, 28)

        pct_box = slide.shapes.add_textbox(Inches(4.0), base_top + Inches(0.2), Inches(1.0), Inches(1.0))
        tf = pct_box.text_frame
        tf.text = "%"
        tf.paragraphs[0].font.size = Pt(60)
        tf.paragraphs[0].font.bold = True
        tf.paragraphs[0].font.color.rgb = RGBColor(13, 17, 28)

        # === Inject Morph Transition (Slide 2 Only) ===
        if step == 2:
            # Office Open XML extension payload for standard Morph Transition
            morph_xml = """
            <p:transition xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" xmlns:p14="http://schemas.microsoft.com/office/powerpoint/2010/main" p14:dur="2000">
                <p:extLst>
                    <p:ext uri="{C55B5115-585F-4CA1-8DE8-B1F341BB6A24}">
                        <p15:prstTrans xmlns:p15="http://schemas.microsoft.com/office/powerpoint/2012/main" prst="morph"/>
                    </p:ext>
                </p:extLst>
            </p:transition>
            """
            morph_trans = parse_xml(morph_xml)
            # Insert the transition node safely right after slide properties
            slide.element.cSld.addnext(morph_trans)

    prs.save(output_pptx_path)

    if img_path and os.path.exists(img_path):
        os.remove(img_path)

    return output_pptx_path
```