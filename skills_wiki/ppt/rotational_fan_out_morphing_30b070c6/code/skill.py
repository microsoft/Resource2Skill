import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from lxml import etree

# Helper function to inject XML for arbitrary rotation
def set_rotation(shape, angle):
    """
    Set the rotation of a shape by a specified angle in degrees.
    """
    chp = shape._element
    xfrm = chp.xpath('.//a:xfrm', namespaces={'a': 'http://schemas.openxmlformats.org/drawingml/2006/main'})[0]
    # Rotation is in 60,000ths of a degree
    rot_val = int(angle * 60000)
    xfrm.set('rot', str(rot_val))

# Helper function to add the Morph transition via XML
def set_morph_transition(slide):
    """
    Applies a Morph transition to the given slide.
    """
    slide_xml = slide._element
    # Find or create the transition element
    transition_elm = slide_xml.find('{http://schemas.openxmlformats.org/presentationml/2006/main}transition')
    if transition_elm is None:
        transition_elm = etree.SubElement(slide_xml, '{http://schemas.openxmlformats.org/presentationml/2006/main}transition')

    # Add morph-specific tags
    # Ensure p14 namespace is registered
    ns_map = {
        'p14': 'http://schemas.microsoft.com/office/powerpoint/2010/main',
        'p': 'http://schemas.openxmlformats.org/presentationml/2006/main'
    }
    
    # Set duration
    transition_elm.set('{http://schemas.microsoft.com/office/powerpoint/2010/main}dur', "800")
    
    # Add morph element
    morph_elm = etree.SubElement(transition_elm, '{http://schemas.microsoft.com/office/powerpoint/2010/main}morph')
    morph_elm.set('option', 'byObject')


def create_rotational_fan_out_morph_slide(
    output_pptx_path: str,
    cover_title: str = "PROJECT SUMMARY REPORT",
    items: list = None,
    **kwargs,
) -> str:
    """
    Creates a PPTX file with a two-slide rotational fan-out morphing effect
    for a table of contents.

    Args:
        output_pptx_path: The path to save the generated PPTX file.
        cover_title: The main title for the first slide.
        items: A list of strings for the content items.

    Returns:
        The path to the saved PPTX file.
    """
    if items is None:
        items = [
            "Project Introduction",
            "Goal Planning",
            "Results Showcase",
            "Existing Deficiencies",
            "Future Planning"
        ]

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # --- Define visual parameters ---
    colors = [
        RGBColor(244, 107, 69),  # Orange
        RGBColor(112, 48, 160), # Purple
        RGBColor(255, 192, 0),   # Yellow
        RGBColor(0, 176, 240),   # Bright Blue
        RGBColor(244, 107, 69),  # Orange (can be different)
    ]
    background_color = RGBColor(47, 182, 218) # Main background blue
    
    # Rotations for the final state (Slide 2)
    angles = [40, 30, 20, 10, 0]

    # Positions for the final state (Slide 2) - Found by trial and error
    end_positions = [
        (Inches(4.5), Inches(-8)),
        (Inches(5.5), Inches(-6)),
        (Inches(6.5), Inches(-4)),
        (Inches(7.5), Inches(-2)),
        (Inches(8.5), Inches(0)),
    ]
    
    # Large shape size to ensure coverage
    shape_width = Inches(20)
    shape_height = Inches(20)

    # =================================================
    # SLIDE 1: The Initial State (Collapsed)
    # =================================================
    slide1 = prs.slides.add_slide(blank_layout)

    # Create the background shape that will cover the slide
    bg_shape_s1 = slide1.shapes.add_shape(1, Inches(0), Inches(0), prs.slide_width, prs.slide_height)
    bg_shape_s1.name = "!!BackgroundPanel"
    bg_shape_s1.fill.solid()
    bg_shape_s1.fill.fore_color.rgb = background_color
    bg_shape_s1.line.fill.background()

    # Create other shapes off-screen with 0 rotation
    for i in range(len(items)):
        shape = slide1.shapes.add_shape(1, prs.slide_width, Inches(i), shape_width, shape_height)
        shape.name = f"!!FanShape_{i}"
        shape.fill.solid()
        shape.fill.fore_color.rgb = colors[i % len(colors)]
        shape.line.fill.background()
        set_rotation(shape, 0)
        
        # Add text boxes, also off-screen
        tx_box = slide1.shapes.add_textbox(prs.slide_width, Inches(i), Inches(5), Inches(1))
        tx_box.name = f"!!FanText_{i}"
        p = tx_box.text_frame.paragraphs[0]
        p.text = f"{i+1:02d} {items[i]}"
        p.font.color.rgb = RGBColor(255, 255, 255)
        p.font.bold = True
        p.font.size = Pt(24)
        set_rotation(tx_box, 0)

    # Add the main title on Slide 1
    title_box = slide1.shapes.add_textbox(Inches(1), Inches(3), Inches(11.333), Inches(1.5))
    p = title_box.text_frame.paragraphs[0]
    p.text = cover_title
    p.font.size = Pt(44)
    p.font.bold = True
    p.font.color.rgb = RGBColor(255, 255, 255)
    p.alignment = PP_ALIGN.CENTER
    
    # =================================================
    # SLIDE 2: The Final State (Fanned Out)
    # =================================================
    slide2 = prs.slides.add_slide(blank_layout)

    # Create the background shape in its final position
    bg_shape_s2 = slide2.shapes.add_shape(1, prs.slide_width * 0.6, 0, prs.slide_width * 0.4, prs.slide_height)
    bg_shape_s2.name = "!!BackgroundPanel"
    bg_shape_s2.fill.solid()
    bg_shape_s2.fill.fore_color.rgb = background_color
    bg_shape_s2.line.fill.background()
    
    # Add "CONTENTS" text
    contents_box = slide2.shapes.add_textbox(Inches(11.5), Inches(1.5), Inches(1), Inches(4))
    contents_box.text_frame.text = "CONTENTS"
    contents_box.text_frame.paragraphs[0].font.size = Pt(28)
    contents_box.text_frame.paragraphs[0].font.bold = True
    contents_box.text_frame.paragraphs[0].font.color.rgb = RGBColor(255, 255, 255)
    contents_box.text_frame.word_wrap = False
    contents_box.text_frame.vertical_anchor = MSO_ANCHOR.MIDDLE
    set_rotation(contents_box, 90)

    # Create the fanned shapes in their final positions and rotations
    for i in range(len(items)):
        left, top = end_positions[i]
        angle = angles[i]

        # Add shape
        shape = slide2.shapes.add_shape(1, left, top, shape_width, shape_height)
        shape.name = f"!!FanShape_{i}"
        shape.fill.solid()
        shape.fill.fore_color.rgb = colors[i % len(colors)]
        shape.line.fill.background()
        set_rotation(shape, angle)
        
        # Add text
        tx_box = slide2.shapes.add_textbox(left + Inches(1), top + Inches(8), Inches(7), Inches(1))
        tx_box.name = f"!!FanText_{i}"
        p = tx_box.text_frame.paragraphs[0]
        p.text = f"{i+1:02d} {items[i]}"
        p.font.color.rgb = RGBColor(255, 255, 255)
        p.font.bold = True
        p.font.size = Pt(24)
        tx_box.text_frame.vertical_anchor = MSO_ANCHOR.MIDDLE
        set_rotation(tx_box, angle)

    # Apply the morph transition to the second slide
    set_morph_transition(slide2)

    prs.save(output_pptx_path)
    return output_pptx_path


# # Example Usage:
# if __name__ == '__main__':
#     file_path = "rotational_fan_out_morph.pptx"
#     create_rotational_fan_out_morph_slide(
#         output_pptx_path=file_path,
#         cover_title="项目总结汇报\nPROJECT SUMMARY REPORT",
#         items=[
#             "项目介绍",
#             "目标规划",
#             "成果展示",
#             "存在不足",
#             "未来规划"
#         ]
#     )
#     # Open the file to see the result
#     os.startfile(file_path)

