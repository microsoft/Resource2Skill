def create_slide(
    output_pptx_path: str,
    title_text: str = "HOW TO MAKE\nYOUR QBR MORE\nINTERESTING",
    band_colors: list = [(142, 202, 201), (103, 156, 155), (74, 118, 117)],
    text_color: tuple = (255, 255, 255),
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the 'Bold Split-Background Typographic Transition' visual effect.
    
    Returns: path to the saved PPTX file.
    """
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
    from pptx.enum.shapes import MSO_SHAPE
    
    # Initialize presentation with 16:9 aspect ratio
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    # Add a blank slide
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    
    # === Layer 1: Banded Background ===
    num_bands = len(band_colors)
    band_height = prs.slide_height / num_bands
    
    for i, color in enumerate(band_colors):
        top = i * band_height
        rect = slide.shapes.add_shape(
            MSO_SHAPE.RECTANGLE,
            0, top, prs.slide_width, band_height
        )
        # Apply flat solid color
        rect.fill.solid()
        rect.fill.fore_color.rgb = RGBColor(*color)
        # Match line color to fill to remove default borders seamlessly
        rect.line.color.rgb = RGBColor(*color)
        
    # === Layer 2: Massive Bold Typography ===
    left_margin = Inches(1.0)
    width = prs.slide_width - Inches(2.0)
    # Give the text box full height so MSO_ANCHOR.MIDDLE centers it perfectly
    txBox = slide.shapes.add_textbox(left_margin, 0, width, prs.slide_height)
    text_frame = txBox.text_frame
    text_frame.word_wrap = True
    
    # Vertically center the text block across the color bands
    text_frame.vertical_anchor = MSO_ANCHOR.MIDDLE 
    text_frame.clear() # Clear the default empty paragraph
    
    # Split text by newlines to apply specific tight line spacing to each line
    lines = title_text.upper().split('\n')
    
    for line in lines:
        p = text_frame.add_paragraph()
        p.text = line
        p.alignment = PP_ALIGN.LEFT
        
        # Tighten line spacing to create a cohesive 'block' of text
        p.line_spacing = 0.85 
        
        if p.runs:
            run = p.runs[0]
            # Use a universally available heavy font
            run.font.name = 'Arial Black' 
            run.font.size = Pt(95)
            run.font.bold = True
            run.font.color.rgb = RGBColor(*text_color)
            
    prs.save(output_pptx_path)
    return output_pptx_path
