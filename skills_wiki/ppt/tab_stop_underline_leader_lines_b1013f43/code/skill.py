from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import MSO_TAB_ALIGN, MSO_UNDERLINE, PP_ALIGN

def create_slide(
    output_pptx_path: str,
    title_text: str = "TABLE OF CONTENTS",
    toc_data: list = None,
    title_color: tuple = (29, 87, 114),
    **kwargs,
) -> str:
    """
    Creates a PPTX slide with a professionally formatted Table of Contents.

    This function uses the "Tab-Stop Underline" technique to create perfectly
    aligned leader lines between section titles and page numbers.

    Args:
        output_pptx_path (str): The path to save the generated PPTX file.
        title_text (str): The main title for the slide.
        toc_data (list): A list of dictionaries, where each dictionary represents
                         a line in the TOC. Example keys:
                         {'text': str, 'page': str, 'level': int, 'bold': bool}
        title_color (tuple): RGB tuple for the main title's color.

    Returns:
        str: The path to the saved PPTX file.
    """
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    # === Default TOC Data (from the tutorial) ===
    if toc_data is None:
        toc_data = [
            {'text': 'Executive Summary', 'page': '1', 'level': 0, 'bold': True},
            {'text': 'Introduction', 'page': '3', 'level': 0, 'bold': True},
            {'text': '  Purpose Statement', 'page': '4', 'level': 0, 'bold': False},
            {'text': '  Literature Review', 'page': '5', 'level': 0, 'bold': False},
            {'text': '  Evaluation Questions', 'page': '6', 'level': 0, 'bold': False},
            {'text': 'Results', 'page': '7-8', 'level': 0, 'bold': True},
            {'text': 'Discussion', 'page': '9', 'level': 0, 'bold': True},
            {'text': 'Recommendations', 'page': '10', 'level': 0, 'bold': True},
            {'text': 'Appendix', 'page': '11', 'level': 0, 'bold': True},
        ]
        
    # === Layer 1: Slide Background (optional, simple white) ===
    # You can add a background here if desired. Default is white.

    # === Layer 2: Text & Content ===

    # Add the main title
    title_shape = slide.shapes.add_textbox(Inches(1), Inches(0.5), Inches(11.33), Inches(1.0))
    title_tf = title_shape.text_frame
    p_title = title_tf.paragraphs[0]
    p_title.text = title_text
    p_title.font.name = 'Aptos'
    p_title.font.size = Pt(36)
    p_title.font.bold = True
    p_title.font.color.rgb = RGBColor(*title_color)

    # Add the Table of Contents text box
    # Positioned below the title
    toc_shape = slide.shapes.add_textbox(Inches(1), Inches(1.75), Inches(11.33), Inches(5.0))
    tf = toc_shape.text_frame
    tf.word_wrap = False

    # CRITICAL STEP: Define the right-aligned tab stop
    # This is where all the page numbers will align to.
    # We set it slightly less than the width of the textbox.
    tab_stop_pos = Inches(11.0)
    tf.tab_stops.add_tab_stop(tab_stop_pos, MSO_TAB_ALIGN.RIGHT)

    # Populate the Table of Contents
    for entry in toc_data:
        p = tf.add_paragraph()
        p.font.name = 'Aptos'
        p.font.size = Pt(22)
        p.level = entry.get('level', 0)

        # Run 1: The section title
        title_run = p.add_run()
        title_run.text = entry['text']
        title_run.font.bold = entry.get('bold', False)

        # Run 2: The tab character with the special underline style
        tab_run = p.add_run()
        tab_run.text = '\t'
        # This is the core trick: apply a dashed underline to the tab.
        tab_run.font.underline = MSO_UNDERLINE.DASH_HEAVY
        tab_run.font.color.rgb = RGBColor(128, 128, 128) # Softer gray for leader line

        # Run 3: The page number
        page_run = p.add_run()
        page_run.text = entry['page']
        page_run.font.bold = entry.get('bold', False) # Match boldness of title

    prs.save(output_pptx_path)
    return output_pptx_path

# Example of how to run the function
if __name__ == '__main__':
    file_path = "table_of_contents_slide.pptx"
    # The video has manual spacing for indentation, so we'll add it to the text.
    custom_toc = [
        {'text': 'Executive Summary', 'page': '1', 'level': 0, 'bold': True},
        {'text': 'Introduction', 'page': '3', 'level': 0, 'bold': True},
        {'text': '    Purpose Statement', 'page': '4', 'level': 0, 'bold': False},
        {'text': '    Literature Review', 'page': '5', 'level': 0, 'bold': False},
        {'text': '    Evaluation Questions', 'page': '6', 'level': 0, 'bold': False},
        {'text': 'Results', 'page': '7-8', 'level': 0, 'bold': True},
        {'text': 'Discussion', 'page': '9', 'level': 0, 'bold': True},
        {'text': 'Recommendations', 'page': '10', 'level': 0, 'bold': True},
        {'text': 'Appendix', 'page': '11', 'level': 0, 'bold': True},
    ]
    create_slide(file_path, toc_data=custom_toc)
    print(f"Presentation saved to {file_path}")

