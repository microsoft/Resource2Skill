import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.oxml import parse_xml
from pptx.oxml.ns import nsdecls

def add_gradient_to_shape(shape, color1_hex, color2_hex, angle_degrees):
    """
    Injects OpenXML to apply a linear gradient to a python-pptx shape.
    """
    spPr = shape.element.spPr
    
    # Remove existing solid fill if it exists
    solidFill = spPr.find('{http://schemas.openxmlformats.org/drawingml/2006/main}solidFill')
    if solidFill is not None:
        spPr.remove(solidFill)

    # Angle conversion: OOXML uses 1/60000ths of a degree
    angle_ooxml = int(angle_degrees * 60000)

    # Construct gradient XML
    grad_xml = f"""
    <a:gradFill {nsdecls('a')}>
        <a:gsLst>
            <a:gs pos="0">
                <a:srgbClr val="{color1_hex}"/>
            </a:gs>
            <a:gs pos="100000">
                <a:srgbClr val="{color2_hex}"/>
            </a:gs>
        </a:gsLst>
        <a:lin ang="{angle_ooxml}" scaled="1"/>
    </a:gradFill>
    """
    gradFill = parse_xml(grad_xml)
    spPr.append(gradFill)

def set_text_format(tf, text, font_size, color_rgb, bold=False, alignment=PP_ALIGN.CENTER):
    """Helper to format text cleanly."""
    tf.text = text
    tf.alignment = alignment
    for paragraph in tf.paragraphs:
        paragraph.alignment = alignment
        for run in paragraph.runs:
            run.font.size = Pt(font_size)
            run.font.color.rgb = RGBColor(*color_rgb)
            run.font.bold = bold
            run.font.name = "Calibri"

def create_slide(
    output_pptx_path: str,
    title_text: str = "Product Comparison: Product A vs. Product B",
    prod_a_name: str = "Product A",
    prod_b_name: str = "Product B",
    metrics: list = None,
    **kwargs,
) -> str:
    """
    Creates a symmetrical divergent comparison dashboard slide.
    """
    if metrics is None:
        metrics = [
            ("Target Market Penetration", 0.50, 0.95),
            ("Market Share", 0.75, 0.65),
            ("Customer Acquisition Cost", 1.00, 0.50),
            ("Average Revenue Per User", 0.40, 0.50),
            ("Customer Lifetime Value", 0.85, 1.00)
        ]

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6])  # Blank layout

    # Colors
    BG_COLOR = (30, 30, 36)
    SPINE_COLOR = (42, 42, 50)
    TRACK_COLOR = (50, 50, 60)
    TEXT_LIGHT = (240, 240, 240)
    TEXT_MUTED = (160, 160, 170)
    
    # Brand A (Green)
    COLOR_A_BRIGHT = "8BC34A"
    COLOR_A_DARK = "4CAF50"
    COLOR_A_RGB = (139, 195, 74)
    
    # Brand B (Blue)
    COLOR_B_BRIGHT = "03A9F4"
    COLOR_B_DARK = "0288D1"
    COLOR_B_RGB = (3, 169, 244)

    # 1. Background
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
    bg.fill.solid()
    bg.fill.fore_color.rgb = RGBColor(*BG_COLOR)
    bg.line.fill.background()

    # 2. Title
    title = slide.shapes.add_textbox(Inches(1), Inches(0.4), Inches(11.33), Inches(0.8))
    set_text_format(title.text_frame, title_text, 28, TEXT_LIGHT, bold=True)

    # === Layout Coordinates ===
    center_w = Inches(2.5)
    center_x = (prs.slide_width - center_w) / 2
    
    left_bar_max_w = Inches(3.5)
    left_bar_start = center_x - Inches(0.2)
    
    right_bar_start = center_x + center_w + Inches(0.2)
    right_bar_max_w = Inches(3.5)

    # 3. Central Spine Backgrounds
    spine1 = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, center_x - Inches(0.1), Inches(1.5), center_w/2, Inches(5.5))
    spine1.fill.solid()
    spine1.fill.fore_color.rgb = RGBColor(*SPINE_COLOR)
    spine1.line.fill.background()
    
    spine2 = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, center_x + center_w/2 + Inches(0.1), Inches(1.5), center_w/2, Inches(5.5))
    spine2.fill.solid()
    spine2.fill.fore_color.rgb = RGBColor(*SPINE_COLOR)
    spine2.line.fill.background()

    # 4. Headers (Product A & B)
    # Header A
    ha = slide.shapes.add_textbox(Inches(1.5), Inches(1.2), Inches(3.5), Inches(1.0))
    ha.text_frame.word_wrap = True
    set_text_format(ha.text_frame, prod_a_name, 20, COLOR_A_RGB, bold=True, alignment=PP_ALIGN.RIGHT)
    p_desc_a = ha.text_frame.add_paragraph()
    p_desc_a.text = "Premium, high-performance product designed for professionals."
    p_desc_a.font.size = Pt(11)
    p_desc_a.font.color.rgb = RGBColor(*TEXT_MUTED)
    
    circ_a = slide.shapes.add_shape(MSO_SHAPE.OVAL, left_bar_start - Inches(0.6), Inches(1.2), Inches(0.6), Inches(0.6))
    circ_a.fill.solid()
    circ_a.fill.fore_color.rgb = RGBColor(*COLOR_A_RGB)
    circ_a.line.fill.background()
    set_text_format(circ_a.text_frame, "A", 18, (255,255,255), bold=True)

    # Header B
    circ_b = slide.shapes.add_shape(MSO_SHAPE.OVAL, right_bar_start, Inches(1.2), Inches(0.6), Inches(0.6))
    circ_b.fill.solid()
    circ_b.fill.fore_color.rgb = RGBColor(*COLOR_B_RGB)
    circ_b.line.fill.background()
    set_text_format(circ_b.text_frame, "B", 18, (255,255,255), bold=True)

    hb = slide.shapes.add_textbox(right_bar_start + Inches(0.8), Inches(1.2), Inches(3.5), Inches(1.0))
    hb.text_frame.word_wrap = True
    set_text_format(hb.text_frame, prod_b_name, 20, COLOR_B_RGB, bold=True, alignment=PP_ALIGN.LEFT)
    p_desc_b = hb.text_frame.add_paragraph()
    p_desc_b.text = "Budget-friendly option offering excellent value for everyday users."
    p_desc_b.font.size = Pt(11)
    p_desc_b.font.color.rgb = RGBColor(*TEXT_MUTED)

    # 5. Iterating through Metrics
    y_start = Inches(2.2)
    y_gap = Inches(1.0)
    bar_h = Inches(0.4)

    for i, (metric_name, val_a, val_b) in enumerate(metrics):
        curr_y = y_start + (i * y_gap)

        # Metric Text (Spine)
        lbl = slide.shapes.add_textbox(center_x, curr_y - Inches(0.15), center_w, Inches(0.7))
        lbl.text_frame.vertical_anchor = MSO_ANCHOR.MIDDLE
        lbl.text_frame.word_wrap = True
        set_text_format(lbl.text_frame, metric_name, 12, TEXT_LIGHT, bold=True)

        # --- Product A Side (Left) ---
        # Track A
        tr_a = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left_bar_start - left_bar_max_w, curr_y, left_bar_max_w, bar_h)
        tr_a.adjustments[0] = 0.5  # Pill shape
        tr_a.fill.solid()
        tr_a.fill.fore_color.rgb = RGBColor(*TRACK_COLOR)
        tr_a.line.fill.background()

        # Bar A
        actual_w_a = left_bar_max_w * val_a
        bar_a = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left_bar_start - actual_w_a, curr_y, actual_w_a, bar_h)
        bar_a.adjustments[0] = 0.5
        bar_a.line.fill.background()
        # Gradient: 180 degrees (Right to Left fade) -> Bright on outside (left), dark on inside (right)
        add_gradient_to_shape(bar_a, COLOR_A_BRIGHT, COLOR_A_DARK, 180)

        # Value Text A
        val_txt_a = slide.shapes.add_textbox(left_bar_start - actual_w_a - Inches(0.8), curr_y - Inches(0.05), Inches(0.8), bar_h)
        set_text_format(val_txt_a.text_frame, f"{int(val_a*100)}%", 14, COLOR_A_RGB, bold=True, alignment=PP_ALIGN.RIGHT)


        # --- Product B Side (Right) ---
        # Track B
        tr_b = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, right_bar_start, curr_y, right_bar_max_w, bar_h)
        tr_b.adjustments[0] = 0.5
        tr_b.fill.solid()
        tr_b.fill.fore_color.rgb = RGBColor(*TRACK_COLOR)
        tr_b.line.fill.background()

        # Bar B
        actual_w_b = right_bar_max_w * val_b
        bar_b = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, right_bar_start, curr_y, actual_w_b, bar_h)
        bar_b.adjustments[0] = 0.5
        bar_b.line.fill.background()
        # Gradient: 0 degrees (Left to Right fade) -> Dark on inside (left), bright on outside (right)
        add_gradient_to_shape(bar_b, COLOR_B_DARK, COLOR_B_BRIGHT, 0)

        # Value Text B
        val_txt_b = slide.shapes.add_textbox(right_bar_start + actual_w_b, curr_y - Inches(0.05), Inches(0.8), bar_h)
        set_text_format(val_txt_b.text_frame, f"{int(val_b*100)}%", 14, COLOR_B_RGB, bold=True, alignment=PP_ALIGN.LEFT)


    prs.save(output_pptx_path)
    return output_pptx_path

