def create_slide(
    output_pptx_path: str,
    title_text: str = "Default Title", # Ignored, using phrases instead
    body_text: str = "",
    phrases: list = ["WORK\nHARD", "PLAY\nHARD"],
    bg_color: tuple = (20, 20, 22),
    colors: list = [(255, 255, 255), (255, 42, 68)],
    font_name: str = "Futura",
    font_size: int = 120,
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the Split-Block Kinetic Typography effect.
    The script perfectly aligns multiple text blocks along a central axis
    using opposing text alignments to create a seamless kinetic typography setup.

    Returns: path to the saved PPTX file.
    """
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
    from pptx.dml.color import RGBColor

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    # Use blank layout
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    # === Layer 1: Background ===
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(*bg_color)

    # === Layer 2: Kinetic Typography Layout ===
    # A small gap forces the blocks to stay slightly separated at the seam
    gap = Inches(0.2)
    center_x = prs.slide_width / 2

    # Layout calculation
    if len(phrases) == 2:
        # The dual-split kinetic layout (as seen in the tutorial):
        # Left box right-aligns text, Right box left-aligns text.
        alignments = [PP_ALIGN.RIGHT, PP_ALIGN.LEFT]
        lefts = [0, center_x + gap / 2]
        widths = [center_x - gap / 2, center_x - gap / 2]
    else:
        # Generic fallback if the user passes more than 2 phrases
        col_w = prs.slide_width / len(phrases)
        alignments = [PP_ALIGN.CENTER] * len(phrases)
        lefts = [i * col_w for i in range(len(phrases))]
        widths = [col_w] * len(phrases)

    # Generate the typography blocks
    for i, phrase in enumerate(phrases):
        # Create full-height text boxes
        txBox = slide.shapes.add_textbox(lefts[i], 0, widths[i], prs.slide_height)
        tf = txBox.text_frame
        tf.word_wrap = True
        
        # Vertically center the text within the slide height
        tf.vertical_anchor = MSO_ANCHOR.MIDDLE

        # Clear default paragraphs before adding customized lines
        tf.clear()
        
        # Split phrase by newline to ensure tight line spacing is applied uniformly
        lines = phrase.split('\n')
        for j, line in enumerate(lines):
            # Use the existing first paragraph or append new ones
            p = tf.paragraphs[0] if j == 0 else tf.add_paragraph()
            p.text = line
            p.alignment = alignments[i]
            
            # Compress line spacing to create a 'solid brick' kinetic look
            p.line_spacing = 0.85
            
            # Apply heavy font styling
            for run in p.runs:
                run.font.name = font_name
                run.font.size = Pt(font_size)
                run.font.bold = True
                
                # Alternate colors based on the text block index
                color_idx = i % len(colors)
                run.font.color.rgb = RGBColor(*colors[color_idx])

    prs.save(output_pptx_path)
    return output_pptx_path
