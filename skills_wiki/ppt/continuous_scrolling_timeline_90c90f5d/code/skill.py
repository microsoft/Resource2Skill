from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN
from pptx.enum.dml import MSO_THEME_COLOR

def create_horizontal_push_timeline(output_pptx_path: str, theme_name: str = "Company Timeline") -> str:
    """
    Creates a two-slide PowerPoint presentation designed for a seamless horizontal
    "Push" transition, simulating a continuous timeline.

    **Manual Step Required After Generation**:
    1. Open the generated .pptx file.
    2. Select the second slide.
    3. Go to the "Transitions" tab.
    4. Select the "Push" transition.
    5. In "Effect Options," choose "From Right."

    Args:
        output_pptx_path: The path to save the generated .pptx file.
        theme_name: The main title for the timeline.

    Returns:
        The path to the saved .pptx file.
    """
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    # --- Define Styles ---
    BG_COLOR = RGBColor(242, 242, 242)
    TEXT_COLOR = RGBColor(51, 51, 51)
    ACCENT_COLOR = RGBColor(255, 192, 0)
    FONT_FAMILY = "Avenir Next"

    # --- Data for Timeline ---
    steps_data = [
        {"num": "1", "title": "LOREM IPSUM", "text": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt."},
        {"num": "2", "title": "LOREM IPSUM", "text": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt."},
        {"num": "3", "title": "LOREM IPSUM", "text": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt."},
        {"num": "4", "title": "LOREM IPSUM", "text": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt."},
        {"num": "5", "title": "LOREM IPSUM", "text": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt."},
        {"num": "6", "title": "LOREM IPSUM", "text": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt."},
    ]

    # --- Helper function to draw a single milestone ---
    def draw_milestone(slide, x_pos, data, is_staggered_down):
        circle_size = Inches(0.7)
        y_center = prs.slide_height / 2

        # Draw circle
        circle = slide.shapes.add_shape(MSO_SHAPE.OVAL, x_pos - circle_size / 2, y_center - circle_size / 2, circle_size, circle_size)
        circle.fill.solid()
        circle.fill.fore_color.rgb = ACCENT_COLOR
        circle.line.fill.solid()
        circle.line.fill.fore_color.rgb = TEXT_COLOR
        circle.line.width = Pt(2)

        # Add number to circle
        text_box = slide.shapes.add_textbox(x_pos - circle_size / 2, y_center - circle_size / 2, circle_size, circle_size)
        p = text_box.text_frame.paragraphs[0]
        p.text = data["num"]
        p.font.name = FONT_FAMILY
        p.font.size = Pt(24)
        p.font.bold = True
        p.font.color.rgb = TEXT_COLOR
        p.alignment = PP_ALIGN.CENTER
        text_box.text_frame.vertical_anchor = 'middle'

        # Add text blocks
        text_y_offset = Inches(0.6)
        if is_staggered_down:
            title_y = y_center + text_y_offset
            body_y = title_y + Inches(0.3)
        else:
            title_y = y_center - text_y_offset - Inches(0.6) # Adjust for height
            body_y = title_y + Inches(0.3)
            
        # Title
        title_box = slide.shapes.add_textbox(x_pos - Inches(1.5), title_y, Inches(3), Inches(0.5))
        p_title = title_box.text_frame.paragraphs[0]
        p_title.text = data["title"]
        p_title.font.name = FONT_FAMILY
        p_title.font.size = Pt(18)
        p_title.font.bold = True
        p_title.font.color.rgb = TEXT_COLOR
        p_title.alignment = PP_ALIGN.CENTER

        # Body
        body_box = slide.shapes.add_textbox(x_pos - Inches(1.5), body_y, Inches(3), Inches(1))
        p_body = body_box.text_frame.paragraphs[0]
        p_body.text = data["text"]
        p_body.font.name = FONT_FAMILY
        p_body.font.size = Pt(11)
        p_body.font.color.rgb = TEXT_COLOR
        p_body.alignment = PP_ALIGN.CENTER

    # --- Create Slides ---
    for i in range(2): # Create two slides
        slide = prs.slides.add_slide(prs.slide_layouts[6])

        # Set background
        background = slide.background
        fill = background.fill
        fill.solid()
        fill.fore_color.rgb = BG_COLOR

        # Draw timeline axis
        line = slide.shapes.add_shape(MSO_SHAPE.LINE_INVERSE, 0, prs.slide_height / 2, prs.slide_width, 0)
        line_format = line.line
        line_format.fill.solid()
        line_format.fill.fore_color.rgb = TEXT_COLOR
        line_format.width = Pt(2)

        # Draw milestones
        start_offset = Inches(2.5)
        spacing = Inches(4.25)
        
        data_index_offset = i * 3
        for j in range(3):
            step_data = steps_data[j + data_index_offset]
            x_position = start_offset + (j * spacing)
            is_down = (j % 2 != 0) # Stagger logic: 0-up, 1-down, 2-up
            draw_milestone(slide, x_position, step_data, is_down)

    # --- Add Title to the First Slide ---
    first_slide = prs.slides[0]
    title_box = first_slide.shapes.add_textbox(Inches(1), Inches(0.5), prs.slide_width - Inches(2), Inches(1))
    p_title = title_box.text_frame.paragraphs[0]
    p_title.text = theme_name.upper()
    p_title.font.name = FONT_FAMILY
    p_title.font.size = Pt(44)
    p_title.font.bold = True
    p_title.font.color.rgb = TEXT_COLOR
    p_title.alignment = PP_ALIGN.CENTER

    subtitle_box = first_slide.shapes.add_textbox(Inches(1), Inches(1.2), prs.slide_width - Inches(2), Inches(0.5))
    p_subtitle = subtitle_box.text_frame.paragraphs[0]
    p_subtitle.text = "EASY TO EDIT"
    p_subtitle.font.name = FONT_FAMILY
    p_subtitle.font.size = Pt(14)
    p_subtitle.font.color.rgb = TEXT_COLOR
    p_subtitle.alignment = PP_ALIGN.CENTER
    
    # Add highlight behind subtitle
    # Get coordinates from the text runs to be precise
    p_subtitle.font.bold = True # Make it bold to better measure
    subtitle_width = Emu(sum(run.font._element.get_or_add_rPr().sz * 0.75 * len(run.text) for run in p_subtitle.runs) * 1000) # Approximate width
    highlight_width = subtitle_width + Inches(0.2)
    highlight_height = Inches(0.3)
    highlight_left = (prs.slide_width / 2) - (highlight_width / 2)
    highlight_top = Inches(1.15)
    
    highlight = first_slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, highlight_left, highlight_top, highlight_width, highlight_height)
    highlight.fill.solid()
    highlight.fill.fore_color.rgb = ACCENT_COLOR
    highlight.line.fill.background()
    # Send highlight behind text
    sp = highlight.element
    sp.getparent().remove(sp)
    subtitle_box.element.getparent().insert(subtitle_box.element.getparent().index(subtitle_box.element), sp)


    prs.save(output_pptx_path)
    return output_pptx_path

# Example usage:
# create_horizontal_push_timeline("timeline_presentation.pptx")
