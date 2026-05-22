import collections.abc
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

def create_slide(
    output_pptx_path: str,
    title_text: str = "Table of Contents",
    toc_data: list = None,
    **kwargs,
) -> str:
    """
    Creates a PowerPoint presentation with an interactive, hyperlinked Table of Contents slide.

    Args:
        output_pptx_path: The path to save the generated .pptx file.
        title_text: The title for the Table of Contents slide.
        toc_data: A list of dictionaries representing the ToC structure.
                  Each dict should have 'text' and 'level' (0 for main, 1 for sub).
                  Example: [{'text': 'About Us', 'level': 0}, {'text': 'Who We Are', 'level': 1}]

    Returns:
        The path to the saved PPTX file.
    """
    # --- Default Data if not provided, mimicking the tutorial ---
    if toc_data is None:
        toc_data = [
            {'text': 'About Us', 'level': 0, 'bold': True},
            {'text': 'Who We Are', 'level': 1, 'bold': False},
            {'text': 'Our Vision', 'level': 1, 'bold': False},
            {'text': 'Our Service', 'level': 0, 'bold': True},
            {'text': 'Meet the Team', 'level': 0, 'bold': True},
            {'text': 'Leadership', 'level': 1, 'bold': False},
            {'text': 'Design', 'level': 1, 'bold': False},
            {'text': 'Operations', 'level': 1, 'bold': False},
            {'text': 'Q&A', 'level': 0, 'bold': True},
        ]

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_slide_layout = prs.slide_layouts[6]

    # --- 1. Create Slides in Order: Title, ToC, then Content ---
    # This order ensures slide indices are predictable for linking.
    
    # Slide 1: Title Slide
    title_slide = prs.slides.add_slide(prs.slide_layouts[0])
    title_slide.shapes.title.text = "Company Presentation"
    title_slide.placeholders[1].text = "An Interactive Overview"
    
    # Slide 2: Table of Contents (will be populated later)
    toc_slide = prs.slides.add_slide(blank_slide_layout)
    
    # Create the actual content slides that the ToC will link to
    content_slides = []
    for item in toc_data:
        slide = prs.slides.add_slide(prs.slide_layouts[1])
        slide.shapes.title.text = item['text']
        # Add some placeholder body text
        body_shape = slide.placeholders[1]
        tf = body_shape.text_frame
        tf.text = f"This slide contains details about {item['text'].lower()}."
        
        content_slides.append(slide)
        
    # --- 2. Populate the Table of Contents Slide with Hyperlinks ---
    
    # Add ToC Title
    title_shape = toc_slide.shapes.add_textbox(Inches(1), Inches(0.5), Inches(8), Inches(1))
    title_tf = title_shape.text_frame
    p_title = title_tf.paragraphs[0]
    p_title.text = title_text
    p_title.font.bold = True
    p_title.font.size = Pt(44)
    p_title.font.color.rgb = RGBColor(0, 112, 192)

    # Add ToC List Text Box
    toc_box = toc_slide.shapes.add_textbox(Inches(1), Inches(1.5), Inches(8), Inches(5.5))
    tf = toc_box.text_frame
    tf.word_wrap = False # Prevent wrapping for clean list
    tf.clear() # Clear default paragraph
    
    # Iterate through data to create and link each ToC item
    for i, item in enumerate(toc_data):
        p = tf.add_paragraph()
        p.text = item['text']
        p.level = item['level']
        p.font.size = Pt(24)
        p.font.color.rgb = RGBColor(64, 64, 64)
        
        if item.get('bold', False):
            p.font.bold = True

        # The hyperlink is applied to the first (and only) run of text in the paragraph
        run = p.runs[0]
        run.hyperlink.target_slide = content_slides[i]
        run.font.underline = True
        run.font.color.rgb = RGBColor(64, 64, 64) # Override default blue link color
    
    # --- 3. Add Decorative Accent Shape ---
    circle = toc_slide.shapes.add_shape(
        MSO_SHAPE.OVAL, Inches(11.5), Inches(3.0), Inches(1.5), Inches(1.5)
    )
    circle.fill.solid()
    circle.fill.fore_color.rgb = RGBColor(0, 176, 240)
    circle.line.fill.background() # No outline

    prs.save(output_pptx_path)
    return output_pptx_path
