# Bilateral Layered Comparison Card

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Bilateral Layered Comparison Card

* **Core Visual Mechanism**: This pattern leverages a highly symmetrical, dual-pane layout split down the middle. Its defining feature is the **depth stacking**—base panels sit in the background, out of which colorful "tab" items and oversized circular hubs appear to float or protrude. By relying heavily on soft drop shadows and clean geometric overlap (rather than literal cutouts), it achieves a sleek, modern "Neumorphic" or Material Design card aesthetic.
* **Why Use This Skill (Rationale)**: The symmetry immediately communicates an A/B choice, while the color-coding distinctly separates the two conceptual groups. The stacked pill tabs intuitively suggest hierarchical lists or features belonging to the primary central nodes, pulling the viewer’s eye outward from the hub.
* **Overall Applicability**: Perfect for "Us vs. Them" competitive analysis, A/B testing results, pros/cons evaluations, or contrasting two distinct product tiers (e.g., Free vs. Pro).
* **Value Addition**: Transforms a boring bullet-point list into an engaging, interactive-feeling dashboard interface. The depth and shadows make the slide feel like a piece of crafted software UI rather than a flat document.

### 2. Visual Breakdown

* **Step A: Core Visual Elements**
  - **Base Canvas**: A very subtle, cool light gray background `(240, 245, 245)` ensures the white cards pop.
  - **Panels**: Two pure white `(255, 255, 255)` rounded rectangles with wide, soft drop shadows.
  - **Hubs**: Large overlapping circles featuring a dark outer ring and a bright, gradient-filled inner circle.
  - **Color Logic**:
    - *Side A (Blue)*: Ranges from deep navy `(21, 67, 96)` to vibrant sky blue `(52, 152, 219)`.
    - *Side B (Pink/Red)*: Ranges from deep crimson `(100, 30, 22)` to bright salmon `(231, 76, 60)`.
  - **Text Hierarchy**: Large colored titles (`32pt+`), prominent numeric indicators inside the tabs, and smaller subtle gray body text (`12-14pt`).

* **Step B: Compositional Style**
  - **Symmetrical Balance**: Mirrored directly around the absolute vertical center.
  - **Overlap & Z-Index Logic**: The base card is drawn first, then the horizontal tabs, and finally the circular hub on top. This hides the inner edge of the tabs, making them look seamlessly anchored behind the circle.
  - **Proportions**: Each side occupies roughly 40% of the canvas width, leaving a 20% negative space channel down the center for the primary "V/S" pivot text.

* **Step C: Dynamic Effects & Transitions**
  - The drop shadows simulate physical layers. If animated, the optimal setup is for the base cards to fade in first, followed by the circle hubs "zooming" in, and finally the horizontal tabs "wiping" out from behind the circles to the left/right.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **Base layout & Shapes** | `python-pptx` native | Standard rounded rectangles and ovals handle 90% of the geometry perfectly and remain fully editable. |
| **Drop Shadows** | `lxml` XML injection | `python-pptx` cannot natively apply shadows. Injecting `<a:outerShdw>` achieves the critical layered depth effect. |
| **Circular Hub Gradients** | `lxml` XML injection | Injecting `<a:gradFill>` provides the polished, multi-stop gradient look seen in the tutorial, making the hubs pop. |

> **Feasibility Assessment**: 95% reproduction. We bypass complex boolean shape subtraction by utilizing intelligent Z-order stacking and shadows, producing an identical visual result that is much safer and cleaner to generate via code.

#### 3b. Complete Reproduction Code

```python
def create_slide(
    output_pptx_path: str,
    title_text: str = "V/S\nCOMPARISON",
    option_a_title: str = "OPTION A",
    option_b_title: str = "OPTION B",
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the Bilateral Layered Comparison visual effect.
    """
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    from pptx.enum.shapes import MSO_SHAPE
    from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
    from lxml import etree

    # --- Helper Functions for XML Effects ---
    def add_shadow(shape, blur_rad=100000, dist=50000, dir_angle=2700000, alpha=30000):
        spPr = shape.element.spPr
        effectLst = spPr.find('{http://schemas.openxmlformats.org/drawingml/2006/main}effectLst')
        if effectLst is None:
            effectLst = etree.SubElement(spPr, '{http://schemas.openxmlformats.org/drawingml/2006/main}effectLst')
        for shadow in effectLst.findall('{http://schemas.openxmlformats.org/drawingml/2006/main}outerShdw'):
            effectLst.remove(shadow)
            
        outerShdw = etree.SubElement(effectLst, '{http://schemas.openxmlformats.org/drawingml/2006/main}outerShdw', 
                                     blurRad=str(blur_rad), dist=str(dist), dir=str(dir_angle), algn="tl", rotWithShape="0")
        srgbClr = etree.SubElement(outerShdw, '{http://schemas.openxmlformats.org/drawingml/2006/main}srgbClr', val="000000")
        etree.SubElement(srgbClr, '{http://schemas.openxmlformats.org/drawingml/2006/main}alpha', val=str(alpha))

    def set_shape_gradient(shape, color1_hex, color2_hex, angle=2700000):
        spPr = shape.element.spPr
        for fill in ['solidFill', 'noFill', 'blipFill', 'pattFill', 'gradFill']:
            fill_element = spPr.find(f'{{http://schemas.openxmlformats.org/drawingml/2006/main}}{fill}')
            if fill_element is not None:
                spPr.remove(fill_element)
                
        gradFill = etree.SubElement(spPr, '{http://schemas.openxmlformats.org/drawingml/2006/main}gradFill', rotWithShape="1")
        gsLst = etree.SubElement(gradFill, '{http://schemas.openxmlformats.org/drawingml/2006/main}gsLst')
        
        gs1 = etree.SubElement(gsLst, '{http://schemas.openxmlformats.org/drawingml/2006/main}gs', pos="0")
        etree.SubElement(gs1, '{http://schemas.openxmlformats.org/drawingml/2006/main}srgbClr', val=color1_hex)
        
        gs2 = etree.SubElement(gsLst, '{http://schemas.openxmlformats.org/drawingml/2006/main}gs', pos="100000")
        etree.SubElement(gs2, '{http://schemas.openxmlformats.org/drawingml/2006/main}srgbClr', val=color2_hex)
        etree.SubElement(gradFill, '{http://schemas.openxmlformats.org/drawingml/2006/main}lin', ang=str(angle), scaled="1")

    # --- Setup Presentation ---
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    
    # Background
    slide.background.fill.solid()
    slide.background.fill.fore_color.rgb = RGBColor(240, 245, 245)

    # --- Color Palettes ---
    blue_tabs = [RGBColor(93, 173, 226), RGBColor(52, 152, 219), RGBColor(41, 128, 185), RGBColor(36, 113, 163)]
    pink_tabs = [RGBColor(241, 148, 138), RGBColor(236, 112, 99), RGBColor(217, 30, 24), RGBColor(192, 57, 43)]

    # ==============================
    # LEFT COLUMN (Blue Theme)
    # ==============================
    
    # 1. Base Panel
    panel_l = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), Inches(1.0), Inches(5.0), Inches(6.0))
    panel_l.fill.solid()
    panel_l.fill.fore_color.rgb = RGBColor(255, 255, 255)
    panel_l.line.fill.background()
    panel_l.adjustments[0] = 0.05
    add_shadow(panel_l, blur_rad=150000, dist=50000, alpha=12000)

    # 2. Tabs (Drawn before circle so they sit underneath)
    for i in range(4):
        tab = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(2.0), Inches(4.05 + i*0.5), Inches(3.5), Inches(0.4))
        tab.fill.solid()
        tab.fill.fore_color.rgb = blue_tabs[i]
        tab.line.fill.background()
        tab.adjustments[0] = 0.5
        add_shadow(tab, blur_rad=50000, dist=20000, alpha=25000)
        
        tf = tab.text_frame
        tf.word_wrap = False
        p = tf.paragraphs[0]
        p.text = f"0{i+1}   Insert detailed feature here"
        p.font.color.rgb = RGBColor(255, 255, 255)
        p.font.size = Pt(12)
        p.alignment = PP_ALIGN.LEFT
        tf.margin_left = Inches(1.1) # Prevents text from hiding under circle

    # 3. Circular Hub
    outer_cl = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(1.0), Inches(4.0), Inches(2.0), Inches(2.0))
    outer_cl.fill.solid()
    outer_cl.fill.fore_color.rgb = RGBColor(21, 67, 96)
    outer_cl.line.fill.background()
    add_shadow(outer_cl, blur_rad=80000, dist=30000, alpha=30000)

    inner_cl = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(1.1), Inches(4.1), Inches(1.8), Inches(1.8))
    set_shape_gradient(inner_cl, "5DADE2", "2874A6") # Light to Dark Blue
    inner_cl.line.fill.background()
    
    tf_cl = inner_cl.text_frame
    tf_cl.vertical_anchor = MSO_ANCHOR.MIDDLE
    p_cl = tf_cl.paragraphs[0]
    p_cl.text = "A"
    p_cl.font.size = Pt(44)
    p_cl.font.bold = True
    p_cl.font.color.rgb = RGBColor(255, 255, 255)
    p_cl.alignment = PP_ALIGN.CENTER

    # 4. Text Blocks
    tb_title_l = slide.shapes.add_textbox(Inches(1.5), Inches(1.3), Inches(4.0), Inches(0.8))
    p = tb_title_l.text_frame.add_paragraph()
    p.text = option_a_title
    p.font.size = Pt(32)
    p.font.bold = True
    p.font.color.rgb = RGBColor(41, 128, 185)
    p.alignment = PP_ALIGN.CENTER

    tb_body_l = slide.shapes.add_textbox(Inches(1.5), Inches(2.1), Inches(4.0), Inches(1.5))
    tb_body_l.text_frame.word_wrap = True
    p = tb_body_l.text_frame.add_paragraph()
    p.text = "Analyze the fundamental strengths and structural advantages of the first option. This area provides high-level context before diving into the specific tabs below."
    p.font.size = Pt(13)
    p.font.color.rgb = RGBColor(120, 120, 120)
    p.alignment = PP_ALIGN.CENTER

    # ==============================
    # RIGHT COLUMN (Pink Theme)
    # ==============================
    
    # 1. Base Panel
    panel_r = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(7.333), Inches(1.0), Inches(5.0), Inches(6.0))
    panel_r.fill.solid()
    panel_r.fill.fore_color.rgb = RGBColor(255, 255, 255)
    panel_r.line.fill.background()
    panel_r.adjustments[0] = 0.05
    add_shadow(panel_r, blur_rad=150000, dist=50000, alpha=12000)

    # 2. Tabs
    for i in range(4):
        tab = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(7.833), Inches(4.05 + i*0.5), Inches(3.5), Inches(0.4))
        tab.fill.solid()
        tab.fill.fore_color.rgb = pink_tabs[i]
        tab.line.fill.background()
        tab.adjustments[0] = 0.5
        add_shadow(tab, blur_rad=50000, dist=20000, alpha=25000)
        
        tf = tab.text_frame
        tf.word_wrap = False
        p = tf.paragraphs[0]
        p.text = f"Insert detailed feature here   0{i+1}"
        p.font.color.rgb = RGBColor(255, 255, 255)
        p.font.size = Pt(12)
        p.alignment = PP_ALIGN.RIGHT
        tf.margin_right = Inches(1.1)

    # 3. Circular Hub
    outer_cr = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(10.333), Inches(4.0), Inches(2.0), Inches(2.0))
    outer_cr.fill.solid()
    outer_cr.fill.fore_color.rgb = RGBColor(100, 30, 22)
    outer_cr.line.fill.background()
    add_shadow(outer_cr, blur_rad=80000, dist=30000, alpha=30000)

    inner_cr = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(10.433), Inches(4.1), Inches(1.8), Inches(1.8))
    set_shape_gradient(inner_cr, "F5B7B1", "C0392B") # Light to Dark Pink/Red
    inner_cr.line.fill.background()
    
    tf_cr = inner_cr.text_frame
    tf_cr.vertical_anchor = MSO_ANCHOR.MIDDLE
    p_cr = tf_cr.paragraphs[0]
    p_cr.text = "B"
    p_cr.font.size = Pt(44)
    p_cr.font.bold = True
    p_cr.font.color.rgb = RGBColor(255, 255, 255)
    p_cr.alignment = PP_ALIGN.CENTER

    # 4. Text Blocks
    tb_title_r = slide.shapes.add_textbox(Inches(7.833), Inches(1.3), Inches(4.0), Inches(0.8))
    p = tb_title_r.text_frame.add_paragraph()
    p.text = option_b_title
    p.font.size = Pt(32)
    p.font.bold = True
    p.font.color.rgb = RGBColor(192, 57, 43)
    p.alignment = PP_ALIGN.CENTER

    tb_body_r = slide.shapes.add_textbox(Inches(7.833), Inches(2.1), Inches(4.0), Inches(1.5))
    tb_body_r.text_frame.word_wrap = True
    p = tb_body_r.text_frame.add_paragraph()
    p.text = "Review the corresponding strengths and unique features of the alternative option. Clearly map out how these items directly compare to the counterpart."
    p.font.size = Pt(13)
    p.font.color.rgb = RGBColor(120, 120, 120)
    p.alignment = PP_ALIGN.CENTER

    # ==============================
    # CENTER COMPARISON LABEL
    # ==============================
    tb_center = slide.shapes.add_textbox(Inches(5.666), Inches(0.5), Inches(2.0), Inches(1.2))
    tf_center = tb_center.text_frame
    
    # Split text if it contains newline
    parts = title_text.split("\n")
    
    p1 = tf_center.add_paragraph()
    p1.text = parts[0] if len(parts) > 0 else "V/S"
    p1.font.size = Pt(44)
    p1.font.bold = True
    p1.font.color.rgb = RGBColor(50, 50, 50)
    p1.alignment = PP_ALIGN.CENTER

    if len(parts) > 1:
        p2 = tf_center.add_paragraph()
        p2.text = parts[1]
        p2.font.size = Pt(14)
        p2.font.bold = True
        p2.font.color.rgb = RGBColor(150, 150, 150)
        p2.alignment = PP_ALIGN.CENTER

    prs.save(output_pptx_path)
    return output_pptx_path
```