import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.oxml import parse_xml
from PIL import Image, ImageDraw

def create_slide(
    output_pptx_path: str,
    title_text: str = "State A",
    body_text: str = "State B",
    **kwargs,
) -> str:
    """
    Create a 2-slide PPTX demonstrating the Dynamic Morph Continuity Sequence.
    Objects explicitly tagged with roles will fluidly animate their position,
    scale, and color from Slide 1 to Slide 2.
    """
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    # 1. Generate Static PIL Background (Deep Navy Radial Gradient)
    bg_img_path = "morph_bg_radial.png"
    width, height = int(13.333 * 100), int(7.5 * 100)
    bg_img = Image.new('RGBA', (width, height), (13, 17, 28, 255))
    draw = ImageDraw.Draw(bg_img)
    for radius in range(height, 0, -5):
        alpha = int(255 * (1 - (radius / height)))
        color = (25, 35, 55, alpha)
        bbox = [width/2 - radius, height/2 - radius, width/2 + radius, height/2 + radius]
        draw.ellipse(bbox, fill=color)
    bg_img.save(bg_img_path)

    # Helper: Set Morph Anchor Role
    def set_morph_anchor(shape, role: str):
        """
        Enforces the !! naming convention so PowerPoint connects the objects
        across slides during a Morph transition.
        """
        try:
            # Check for standard shell_helpers interface
            from _shell_helpers import set_morph_anchor as ext_anchor
            ext_anchor(shape, role)
        except ImportError:
            # Fallback to direct lxml manipulation
            nv_props = shape._element.xpath('.//*[@name]')
            if nv_props:
                nv_props[0].set('name', f"!!{role}")

    # Helper: Inject Morph Transition
    def enable_morph_transition(slide):
        """Injects PowerPoint Morph transition XML into the slide."""
        morph_xml = '''
        <p:transition xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" spd="slow">
            <p14:morph xmlns:p14="http://schemas.microsoft.com/office/powerpoint/2010/main" option="byObject"/>
        </p:transition>
        '''
        trans_el = parse_xml(morph_xml)
        slide_xml = slide._element
        
        # Remove existing transitions
        for trans in slide_xml.xpath('./p:transition'):
            slide_xml.remove(trans)
            
        # Determine correct insertion point (after cSld and clrMapOvr)
        insert_idx = 0
        for i, child in enumerate(slide_xml):
            if child.tag in [
                '{http://schemas.openxmlformats.org/presentationml/2006/main}cSld',
                '{http://schemas.openxmlformats.org/presentationml/2006/main}clrMapOvr'
            ]:
                insert_idx = i + 1
        slide_xml.insert(insert_idx, trans_el)

    blank_layout = prs.slide_layouts[6]

    # ==========================================
    # SLIDE 1: The Status Quo (Clustered / Base)
    # ==========================================
    slide1 = prs.slides.add_slide(blank_layout)
    slide1.shapes.add_picture(bg_img_path, 0, 0, prs.slide_width, prs.slide_height)

    # Element 1: Hero Number (Large, Left)
    num1 = slide1.shapes.add_textbox(Inches(0.5), Inches(2.5), Inches(3), Inches(2))
    tf1 = num1.text_frame
    p = tf1.paragraphs[0]
    p.text = "01"
    p.font.size = Pt(120)
    p.font.bold = True
    p.font.color.rgb = RGBColor(60, 70, 90)
    set_morph_anchor(num1, "hero_number")

    # Element 2: Hero Headline (Center, prominent)
    head1 = slide1.shapes.add_textbox(Inches(4), Inches(3), Inches(5.333), Inches(1))
    tf2 = head1.text_frame
    tf2.text = title_text
    tf2.paragraphs[0].font.size = Pt(48)
    tf2.paragraphs[0].font.bold = True
    tf2.paragraphs[0].font.color.rgb = RGBColor(255, 255, 255)
    tf2.paragraphs[0].alignment = PP_ALIGN.CENTER
    set_morph_anchor(head1, "hero_headline")

    # Element 3: Accent Orb (Small, Cyan, Top Right)
    orb1 = slide1.shapes.add_shape(9, Inches(10), Inches(1), Inches(1.5), Inches(1.5)) # 9 is msoShapeOval
    orb1.fill.solid()
    orb1.fill.fore_color.rgb = RGBColor(0, 191, 255)
    orb1.line.fill.background()
    set_morph_anchor(orb1, "accent_orb")

    # Element 4: Section Chip (Small rect, Bottom Center)
    chip1 = slide1.shapes.add_shape(1, Inches(5.666), Inches(6), Inches(2), Inches(0.5)) # 1 is msoShapeRectangle
    chip1.fill.solid()
    chip1.fill.fore_color.rgb = RGBColor(75, 0, 130)
    chip1.line.fill.background()
    set_morph_anchor(chip1, "section_chip")


    # ==========================================
    # SLIDE 2: The Evolution (Expanded / Changed)
    # ==========================================
    slide2 = prs.slides.add_slide(blank_layout)
    slide2.shapes.add_picture(bg_img_path, 0, 0, prs.slide_width, prs.slide_height)
    enable_morph_transition(slide2)

    # Element 1: Hero Number (Moves Right, Gets Darker)
    num2 = slide2.shapes.add_textbox(Inches(10), Inches(2.5), Inches(3), Inches(2))
    tf1_2 = num2.text_frame
    p_2 = tf1_2.paragraphs[0]
    p_2.text = "02"
    p_2.font.size = Pt(120)
    p_2.font.bold = True
    p_2.font.color.rgb = RGBColor(30, 40, 60)
    set_morph_anchor(num2, "hero_number")

    # Element 2: Hero Headline (Moves Bottom Left, Shrinks)
    head2 = slide2.shapes.add_textbox(Inches(0.5), Inches(6), Inches(4), Inches(1))
    tf2_2 = head2.text_frame
    tf2_2.text = body_text
    tf2_2.paragraphs[0].font.size = Pt(32)
    tf2_2.paragraphs[0].font.bold = True
    tf2_2.paragraphs[0].font.color.rgb = RGBColor(200, 200, 200)
    tf2_2.paragraphs[0].alignment = PP_ALIGN.LEFT
    set_morph_anchor(head2, "hero_headline")

    # Element 3: Accent Orb (Moves Center, Expands Massively, Changes to Coral)
    orb2 = slide2.shapes.add_shape(9, Inches(3.666), Inches(0.75), Inches(6), Inches(6))
    orb2.fill.solid()
    orb2.fill.fore_color.rgb = RGBColor(255, 127, 80)
    orb2.line.fill.background()
    set_morph_anchor(orb2, "accent_orb")

    # Element 4: Section Chip (Moves Top, Spans full width, Changes to Gold)
    chip2 = slide2.shapes.add_shape(1, Inches(0), Inches(0), Inches(13.333), Inches(0.25))
    chip2.fill.solid()
    chip2.fill.fore_color.rgb = RGBColor(255, 215, 0)
    chip2.line.fill.background()
    set_morph_anchor(chip2, "section_chip")

    # Cleanup temp image
    if os.path.exists(bg_img_path):
        os.remove(bg_img_path)

    prs.save(output_pptx_path)
    return output_pptx_path
