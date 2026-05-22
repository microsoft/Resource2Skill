from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN

def _create_column(slide, x, width, title, icon, color, border_color, text_color, items):
    """
    Helper function to create a single column for pros or cons. This function is
    intended to be called by create_balanced_decision_matrix.
    """
    # --- Column Header ---
    header_y = Inches(1.2)
    header_height = Inches(0.5)

    # Icon
    icon_box = slide.shapes.add_textbox(x, header_y, Inches(0.6), header_height)
    icon_tf = icon_box.text_frame
    icon_tf.margin_left = icon_tf.margin_right = icon_tf.margin_top = icon_tf.margin_bottom = 0
    p_icon = icon_tf.paragraphs[0]
    run_icon = p_icon.add_run()
    run_icon.text = icon
    # Segoe UI Emoji is widely available on Windows and supports these glyphs.
    # A fallback font will be used on other systems.
    run_icon.font.name = 'Segoe UI Emoji'
    run_icon.font.size = Pt(24)
    run_icon.font.color.rgb = color
    p_icon.alignment = PP_ALIGN.CENTER

    # Title
    title_box = slide.shapes.add_textbox(x + Inches(0.6), header_y, width - Inches(0.6), header_height)
    title_tf = title_box.text_frame
    title_tf.margin_left = title_tf.margin_right = title_tf.margin_top = title_tf.margin_bottom = 0
    p_title = title_tf.paragraphs[0]
    p_title.text = title
    p_title.font.name = 'Calibri'
    p_title.font.bold = True
    p_title.font.size = Pt(20)
    p_title.font.color.rgb = text_color

    # --- Content Box ---
    content_y = header_y + header_height + Inches(0.2)
    content_height = Inches(4.5)
    
    box = slide.shapes.add_shape(1, x, content_y, width, content_height) # MSO_SHAPE.RECTANGLE
    box.fill.solid()
    box.fill.fore_color.rgb = RGBColor(248, 249, 250)
    box.line.color.rgb = border_color
    box.line.width = Pt(1.5)

    # Text Frame for list
    tf = box.text_frame
    tf.clear()
    tf.margin_left = Inches(0.3)
    tf.margin_right = Inches(0.2)
    tf.margin_top = Inches(0.2)
    tf.margin_bottom = Inches(0.2)
    tf.word_wrap = True

    for i, item_text in enumerate(items):
        if i == 0:
            p = tf.paragraphs[0]
        else:
            p = tf.add_paragraph()
        
        p.text = item_text
        p.font.name = 'Calibri'
        p.font.size = Pt(16)
        p.font.color.rgb = text_color
        p.level = 0
        p.space_after = Pt(12)

def create_slide(
    output_pptx_path: str,
    slide_title: str = "Analysis of the Proposed Initiative",
    pros_list: list = None,
    cons_list: list = None,
    **kwargs,
) -> str:
    """
    Creates a PPTX slide with a balanced Pros and Cons layout, perfect for
    decision-making and strategic analysis.

    Returns: Path to the saved PPTX file.
    """
    # Default content if none is provided
    if pros_list is None:
        pros_list = [
            "Focuses on what is important",
            "Shared vision communicated",
            "Involves and engages the organization",
            "Progress is monitored"
        ]
    if cons_list is None:
        cons_list = [
            "Rigid implementation system",
            "Requires long-term commitment",
            "Objective must be static over 3-5 years",
            "Potential resistance to change"
        ]

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    # --- Set background color ---
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(255, 255, 255)

    # --- Slide Title ---
    title_shape = slide.shapes.add_textbox(Inches(0.5), Inches(0.2), Inches(12.33), Inches(0.75))
    title_tf = title_shape.text_frame
    title_p = title_tf.paragraphs[0]
    title_p.text = slide_title
    title_p.font.name = 'Calibri'
    title_p.font.size = Pt(28)
    title_p.font.bold = True
    title_p.font.color.rgb = RGBColor(64, 64, 64)
    title_p.alignment = PP_ALIGN.CENTER

    # --- Define Colors and Layout ---
    PROS_COLOR = RGBColor(108, 194, 74)
    CONS_COLOR = RGBColor(220, 53, 69)
    TEXT_COLOR = RGBColor(73, 80, 87)
    BORDER_COLOR = RGBColor(222, 226, 230)
    
    margin_x = Inches(0.75)
    gutter = Inches(0.5)
    col_width = (prs.slide_width - 2 * margin_x - gutter) / 2

    # --- PROS COLUMN ---
    pros_x = margin_x
    _create_column(slide, pros_x, col_width, "Pros", "👍", PROS_COLOR, BORDER_COLOR, TEXT_COLOR, pros_list)

    # --- CONS COLUMN ---
    cons_x = margin_x + col_width + gutter
    _create_column(slide, cons_x, col_width, "Cons", "👎", CONS_COLOR, BORDER_COLOR, TEXT_COLOR, cons_list)


    prs.save(output_pptx_path)
    return output_pptx_path

