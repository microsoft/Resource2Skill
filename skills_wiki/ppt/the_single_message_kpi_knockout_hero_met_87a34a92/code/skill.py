import os
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def create_slide(
    output_pptx_path: str,
    hero_metric: str = "$1,100,000",
    hero_label: str = "weekly sales",
    funnel_data: list = None,
    bg_color: tuple = (31, 140, 204),       # Vibrant Blue
    accent_color: tuple = (255, 192, 0),    # Golden Yellow
    text_color: tuple = (255, 255, 255),    # White
    **kwargs,
) -> str:
    """
    Creates a 2-slide presentation reproducing "The Single-Message KPI Knockout".
    Slide 1: The massive Hero Metric.
    Slide 2: The Funnel Breakdown.
    """
    if funnel_data is None:
        funnel_data = [
            ("social media engagements", "330,000"),
            ("new website visitors", "44,000"),
            ("increase in inbound leads", "323%")
        ]

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    # Helper function to set slide background using a full-screen rectangle
    def set_background(slide, r, g, b):
        bg_shape = slide.shapes.add_shape(
            MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height
        )
        bg_shape.fill.solid()
        bg_shape.fill.fore_color.rgb = RGBColor(r, g, b)
        bg_shape.line.fill.background()
        # Send to back (XML manipulation for z-order)
        slide.shapes._spTree.remove(bg_shape._element)
        slide.shapes._spTree.insert(2, bg_shape._element)
        return bg_shape

    # ==========================================
    # SLIDE 1: THE HERO METRIC
    # ==========================================
    slide_1 = prs.slides.add_slide(prs.slide_layouts[6])  # Blank layout
    set_background(slide_1, *bg_color)

    # Hero Number
    tx_box = slide_1.shapes.add_textbox(Inches(1), Inches(2.5), Inches(11.333), Inches(1.5))
    tf = tx_box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = hero_metric
    p.alignment = PP_ALIGN.CENTER
    p.font.size = Pt(110)
    p.font.bold = True
    p.font.color.rgb = RGBColor(*accent_color)
    p.font.name = "Arial"

    # Hero Label
    tx_box_label = slide_1.shapes.add_textbox(Inches(1), Inches(4.2), Inches(11.333), Inches(1))
    tf_label = tx_box_label.text_frame
    p_label = tf_label.paragraphs[0]
    p_label.text = hero_label
    p_label.alignment = PP_ALIGN.CENTER
    p_label.font.size = Pt(40)
    p_label.font.color.rgb = RGBColor(*text_color)
    p_label.font.name = "Arial"

    # ==========================================
    # SLIDE 2: THE FUNNEL BREAKDOWN
    # ==========================================
    slide_2 = prs.slides.add_slide(prs.slide_layouts[6])
    set_background(slide_2, *bg_color)

    # Title
    title_box = slide_2.shapes.add_textbox(Inches(0.5), Inches(0.5), Inches(12), Inches(1))
    tf_title = title_box.text_frame
    p_title = tf_title.paragraphs[0]
    p_title.text = f"Drivers behind the {hero_metric} {hero_label}"
    p_title.font.size = Pt(32)
    p_title.font.bold = True
    p_title.font.color.rgb = RGBColor(*text_color)

    # Funnel Construction Variables
    num_steps = len(funnel_data)
    start_y = 1.8
    step_height = 1.0
    vertical_gap = 0.6
    
    # Max width for top of funnel, decreasing sequentially
    max_bar_width = 7.0
    min_bar_width = 3.5
    width_decrement = (max_bar_width - min_bar_width) / max(1, (num_steps - 1))
    
    center_x = 9.0  # X-coordinate center for the funnel shapes

    for i, (label_text, metric_value) in enumerate(funnel_data):
        current_y = start_y + i * (step_height + vertical_gap)
        current_width = max_bar_width - (i * width_decrement)
        left_x = center_x - (current_width / 2)

        # 1. Left-aligned Label
        lbl_box = slide_2.shapes.add_textbox(Inches(0.5), Inches(current_y + 0.1), Inches(4.5), step_height)
        lbl_tf = lbl_box.text_frame
        p_lbl = lbl_tf.paragraphs[0]
        p_lbl.text = label_text
        p_lbl.alignment = PP_ALIGN.RIGHT
        p_lbl.font.size = Pt(20)
        p_lbl.font.color.rgb = RGBColor(*text_color)
        
        # Draw a subtle connecting line from label to shape
        line = slide_2.shapes.add_connector(
            MSO_SHAPE.LINE_CALLOUT_1, 
            Inches(5.2), Inches(current_y + (step_height/2)), 
            Inches(left_x), Inches(current_y + (step_height/2))
        )
        line.line.color.rgb = RGBColor(255, 255, 255)
        line.line.dash_style = 6 # Dashed line

        # 2. Funnel Bar Shape
        bar = slide_2.shapes.add_shape(
            MSO_SHAPE.RECTANGLE, Inches(left_x), Inches(current_y), Inches(current_width), Inches(step_height)
        )
        # Style the bar (Darker transparent blue to blend with background, bordered with accent)
        bar.fill.solid()
        bar.fill.fore_color.rgb = RGBColor(18, 90, 135) # Slightly darker than bg
        bar.line.color.rgb = RGBColor(*accent_color)
        bar.line.width = Pt(1.5)

        # Bar Text (The Metric)
        p_bar = bar.text_frame.paragraphs[0]
        p_bar.text = metric_value
        p_bar.alignment = PP_ALIGN.CENTER
        p_bar.font.size = Pt(32)
        p_bar.font.bold = True
        p_bar.font.color.rgb = RGBColor(*accent_color)

        # 3. Down Arrow (Connecting the steps)
        if i < num_steps - 1:
            arrow_y = current_y + step_height + 0.1
            arrow = slide_2.shapes.add_shape(
                MSO_SHAPE.DOWN_ARROW, Inches(center_x - 0.2), Inches(arrow_y), Inches(0.4), Inches(0.4)
            )
            arrow.fill.solid()
            arrow.fill.fore_color.rgb = RGBColor(*text_color)
            arrow.line.fill.background()

    prs.save(output_pptx_path)
    return output_pptx_path

# Example execution:
# create_slide("kpi_knockout.pptx")
