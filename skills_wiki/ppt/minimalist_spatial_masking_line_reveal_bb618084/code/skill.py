import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def create_slide(
    output_pptx_path: str,
    title_text: str = "THIS IS THE TITLE",
    bg_color: tuple = (255, 255, 255),       # White background
    accent_color: tuple = (210, 105, 30),    # Terracotta orange
    text_color: tuple = (38, 38, 38),        # Dark Charcoal
    **kwargs,
) -> str:
    """
    Creates a PPTX file demonstrating the "Minimalist Masking Reveal" setup.
    It builds the text, the masking block (slightly transparent to show the technique), 
    and the accent line, layered correctly for animation.
    """
    
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    # Use blank layout
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    # === Layer 0: Background ===
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(*bg_color)

    # Calculate center positions
    center_y = prs.slide_height / 2
    center_x = prs.slide_width / 2

    # === Layer 1: Text Block (Bottom Layer) ===
    # Positioned slightly to the right of center to accommodate the line
    text_width = Inches(6.0)
    text_height = Inches(1.5)
    text_left = center_x - Inches(2.0)
    text_top = center_y - (text_height / 2)

    txBox = slide.shapes.add_textbox(text_left, text_top, text_width, text_height)
    tf = txBox.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = PP_ALIGN.CENTER
    
    p = tf.paragraphs[0]
    p.text = title_text
    p.alignment = PP_ALIGN.LEFT
    
    font = p.font
    font.name = 'Arial'
    font.size = Pt(44)
    font.bold = True
    font.color.rgb = RGBColor(*text_color)

    # === Layer 2: The Masking Block (Middle Layer) ===
    # This block is meant to cover the text. 
    # For demonstration purposes in the generated file, we place it halfway across the text 
    # and give it a slight transparency so the user can see how the trick works.
    mask_width = Inches(4.5)
    mask_height = text_height + Inches(0.5)
    mask_left = text_left + Inches(1.5) # Offset to reveal part of the text
    mask_top = text_top - Inches(0.25)

    mask_shape = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, mask_left, mask_top, mask_width, mask_height
    )
    mask_shape.fill.solid()
    mask_shape.fill.fore_color.rgb = RGBColor(*bg_color)
    # Set slight transparency so the technique is visible. Set to 0.0 for actual use.
    mask_shape.fill.transparency = 0.15 
    mask_shape.line.fill.background() # No border

    # === Layer 3: The Accent Line (Top Layer) ===
    # This acts as the visual barrier between the revealed text and the mask
    line_width = Inches(0.08)
    line_height = mask_height - Inches(0.1)
    # Placed exactly at the left edge of the mask
    line_left = mask_left - (line_width / 2) 
    line_top = mask_top + Inches(0.05)

    line_shape = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, line_left, line_top, line_width, line_height
    )
    line_shape.fill.solid()
    line_shape.fill.fore_color.rgb = RGBColor(*accent_color)
    line_shape.line.fill.background() # No border

    # Save presentation
    prs.save(output_pptx_path)
    return output_pptx_path

# Example usage:
# create_slide("reveal_animation_setup.pptx")
