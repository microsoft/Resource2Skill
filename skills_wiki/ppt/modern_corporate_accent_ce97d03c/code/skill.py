import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.shapes import MSO_SHAPE
from pptx.dml.color import RGBColor

def create_slide(
    output_pptx_path: str,
    title_text: str = "ANNUAL WORK REPORT",
    subtitle_text: str = "A detailed summary of yearly performance and future outlook.",
    accent_color_1: tuple = (255, 204, 0),  # Bright Yellow
    accent_color_2: tuple = (128, 128, 128), # Medium Gray
    bg_color: tuple = (45, 45, 55), # Dark Charcoal
    **kwargs,
) -> str:
    """
    Creates a PPTX file reproducing the 'Modern Corporate Accent' visual effect.

    This style uses a dark background with bold, layered geometric shapes in the corner
    to create a professional and dynamic title slide.

    Returns:
        str: The path to the saved PPTX file.
    """
    prs = Presentation()
    # Use 16:9 aspect ratio
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    # Use a blank slide layout
    blank_slide_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(blank_slide_layout)

    # === Layer 1: Background ===
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(*bg_color)

    # === Layer 2: Geometric Accents (Top-Right Corner) ===
    # The larger, secondary color rectangle
    left_accent_2 = Inches(10.5)
    top_accent_2 = Inches(0)
    width_accent_2 = Inches(2.833)
    height_accent_2 = Inches(1.5)
    shape_2 = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left_accent_2, top_accent_2, width_accent_2, height_accent_2)
    shape_2.fill.solid()
    shape_2.fill.fore_color.rgb = RGBColor(*accent_color_2)
    shape_2.line.fill.background() # No outline

    # The smaller, primary color rectangle, layered on top
    left_accent_1 = Inches(9.5)
    top_accent_1 = Inches(0.25)
    width_accent_1 = Inches(3.0)
    height_accent_1 = Inches(1.0)
    shape_1 = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left_accent_1, top_accent_1, width_accent_1, height_accent_1)
    shape_1.fill.solid()
    shape_1.fill.fore_color.rgb = RGBColor(*accent_color_1)
    shape_1.line.fill.background() # No outline

    # === Layer 3: Text & Content ===
    # Title Text Box
    left_title = Inches(1.0)
    top_title = Inches(2.5)
    width_title = Inches(8.0)
    height_title = Inches(1.5)
    
    title_box = slide.shapes.add_textbox(left_title, top_title, width_title, height_title)
    tf_title = title_box.text_frame
    tf_title.word_wrap = True
    
    p_title = tf_title.paragraphs[0]
    p_title.text = title_text
    p_title.font.name = 'Calibri'
    p_title.font.size = Pt(44)
    p_title.font.bold = True
    p_title.font.color.rgb = RGBColor(255, 255, 255)

    # Subtitle Text Box
    left_subtitle = Inches(1.0)
    top_subtitle = Inches(3.8)
    width_subtitle = Inches(8.0)
    height_subtitle = Inches(1.0)
    
    subtitle_box = slide.shapes.add_textbox(left_subtitle, top_subtitle, width_subtitle, height_subtitle)
    tf_subtitle = subtitle_box.text_frame
    tf_subtitle.word_wrap = True
    
    p_subtitle = tf_subtitle.paragraphs[0]
    p_subtitle.text = subtitle_text
    p_subtitle.font.name = 'Calibri'
    p_subtitle.font.size = Pt(24)
    p_subtitle.font.color.rgb = RGBColor(220, 220, 220)

    # A thin decorative line to separate subtitle from potential body
    line_left = Inches(1.0)
    line_top = Inches(4.9)
    line_width = Inches(3.0)
    line_height = Inches(0) # A line is a shape with zero height
    line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, line_left, line_top, line_width, Pt(4))
    line.fill.solid()
    line.fill.fore_color.rgb = RGBColor(*accent_color_1)
    line.line.fill.background()

    # --- Save the presentation ---
    prs.save(output_pptx_path)
    return output_pptx_path

# Example usage:
if __name__ == '__main__':
    file_path = "Modern_Corporate_Accent_Slide.pptx"
    create_slide(file_path)
    # On Windows, this will open the generated file
    if os.name == 'nt':
        os.startfile(file_path)

