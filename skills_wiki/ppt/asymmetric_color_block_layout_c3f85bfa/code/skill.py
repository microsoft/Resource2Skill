import os
import urllib.request
from io import BytesIO
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def create_asymmetric_color_block_presentation(
    output_pptx_path: str,
    title_slide_content: dict = None,
    content_slide_content: dict = None,
    accent_color_rgb: tuple = (79, 230, 222),
    **kwargs
) -> str:
    """
    Creates a complete PPTX file with two slides reproducing the "Asymmetric Color Block" style.

    Args:
        output_pptx_path: Path to save the generated .pptx file.
        title_slide_content: Dictionary with content for the title slide.
        content_slide_content: Dictionary with content for the content slide.
        accent_color_rgb: The (R, G, B) tuple for the accent color.

    Returns:
        The path to the saved PPTX file.
    """
    # --- Default Content ---
    if title_slide_content is None:
        title_slide_content = {
            "title": "NETWORK TOPOLOGY",
            "subtitle": "TOPKHANA, TRIPURESHWOR, NEPAL",
            "author": "Abhiyan Jung Khadka",
            "date": "7 JULY 2021",
            "image_url": "https://images.unsplash.com/photo-1544256718-3bcf237f3974?w=800&q=80&auto=format&fit=crop"
        }
    if content_slide_content is None:
        content_slide_content = {
            "main_title": "ADVANTAGES OF STAR TOPOLOGY",
            "sections": [
                {'title': 'SINGLE HUB', 'points': ['Allows to manage entire network from single location', 'Independent nodes allows network to continue if one node is down']},
                {'title': 'LAYOUT', 'points': ['More stable and secure', 'Allows addition, modification without going offline']},
                {'title': 'COST', 'points': ['Low startup cost', 'Requires less cable']}
            ]
        }

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # --- Helper Functions for Slide Creation ---
    def _add_title_slide(prs, layout, content):
        slide = prs.slides.add_slide(layout)
        slide.background.fill.solid().fore_color.rgb = RGBColor(255, 255, 255)
        accent_color = RGBColor.from_rgb(*accent_color_rgb)

        # Image on the right
        img_left, img_width = Inches(7.0), Inches(6.333)
        try:
            with urllib.request.urlopen(content['image_url']) as url:
                slide.shapes.add_picture(BytesIO(url.read()), img_left, Inches(0), width=img_width)
        except Exception:
            slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, img_left, Inches(0), img_width, prs.slide_height).fill.solid().fore_color.rgb = RGBColor(220, 220, 220)

        # Bottom banner
        banner_height, banner_top = Inches(2.0), prs.slide_height - Inches(2.0)
        slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), banner_top, prs.slide_width, banner_height).fill.solid().fore_color.rgb = accent_color

        # Text elements
        sub_box = slide.shapes.add_textbox(Inches(1), Inches(1), Inches(5), Inches(0.5))
        sub_box.text_frame.paragraphs[0].text = content['subtitle']
        sub_box.text_frame.paragraphs[0].font.name = "Arial Black"
        sub_box.text_frame.paragraphs[0].font.size = Pt(12)

        title_box = slide.shapes.add_textbox(Inches(1), Inches(3), Inches(6), Inches(2))
        p = title_box.text_frame.paragraphs[0]
        p.text = content['title']
        p.font.name = "Times New Roman"
        p.font.size = Pt(60)
        p.font.bold = True

        author_box = slide.shapes.add_textbox(Inches(1), banner_top + Inches(0.5), Inches(5), Inches(1))
        author_box.text_frame.paragraphs[0].text = content['author']
        author_box.text_frame.paragraphs[0].font.name = "Calibri"
        author_box.text_frame.paragraphs[0].font.size = Pt(18)

        # Rotated date (lxml injection)
        date_box = slide.shapes.add_textbox(Inches(12.5), Inches(1), Inches(2), Inches(0.5))
        tf = date_box.text_frame
        tf.text = content['date']
        tf.paragraphs[0].font.name = "Calibri"
        tf.paragraphs[0].font.size = Pt(11)
        tf.paragraphs[0].font.color.rgb = RGBColor(128, 128, 128)
        date_box.element.attrib['rot'] = '5400000'

    def _add_content_slide(prs, layout, content):
        slide = prs.slides.add_slide(layout)
        slide.background.fill.solid().fore_color.rgb = RGBColor(255, 255, 255)
        accent_color = RGBColor.from_rgb(*accent_color_rgb)

        # Main title
        title_box = slide.shapes.add_textbox(Inches(7.0), Inches(1.5), Inches(5.5), Inches(1.5))
        p = title_box.text_frame.paragraphs[0]
        p.text = content['main_title']
        p.font.name = "Arial Black"
        p.font.size = Pt(36)
        p.font.bold = True

        # Content sections
        current_top = Inches(1.5)
        for section in content['sections']:
            slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(1.0), current_top + Pt(10), Inches(0.2), Inches(0.2)).fill.solid().fore_color.rgb = accent_color
            
            sec_title_box = slide.shapes.add_textbox(Inches(1.35), current_top, Inches(4.5), Inches(0.5))
            sec_p = sec_title_box.text_frame.paragraphs[0]
            sec_p.text = section.get('title', 'SECTION TITLE')
            sec_p.font.name = "Arial Black"
            sec_p.font.size = Pt(16)

            current_top += Inches(0.5)
            points_text = '\n'.join([f"•  {point}" for point in section.get('points', [])])
            points_box = slide.shapes.add_textbox(Inches(1.35), current_top, Inches(5.0), Inches(1.5))
            points_p = points_box.text_frame
            points_p.word_wrap = True
            points_p.text = points_text
            points_p.paragraphs[0].font.name = "Calibri"
            points_p.paragraphs[0].font.size = Pt(14)
            points_p.paragraphs[0].line_spacing = 1.5
            
            current_top += Inches(0.3 * len(section.get('points', []))) + Inches(0.8)

        # Bottom accent banner piece
        slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, prs.slide_width - Inches(5), prs.slide_height - Inches(1.5), Inches(5), Inches(1.5)).fill.solid().fore_color.rgb = accent_color

    # --- Generate Slides ---
    _add_title_slide(prs, blank_layout, title_slide_content)
    _add_content_slide(prs, blank_layout, content_slide_content)

    # --- Save Presentation ---
    if not os.path.exists(os.path.dirname(output_pptx_path)) and os.path.dirname(output_pptx_path):
        os.makedirs(os.path.dirname(output_pptx_path))
    prs.save(output_pptx_path)
    return output_pptx_path

