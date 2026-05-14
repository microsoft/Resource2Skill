import os
import urllib.request
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN
from pptx.oxml import parse_xml

# Required by Agent_Skill_Distiller contract for ambient motion effects
AMBIENT_CAPABLE = True
from _shell_helpers import add_infinite_rotation

def apply_gradient_line(shape, color1="FFFFFF", alpha1=100000, color2="FFFFFF", alpha2=0, angle=2700000):
    """
    Injects OpenXML to replace a standard shape outline with a gradient line.
    alpha values: 100000 = 100%, 0 = 0%.
    angle: 0 = Left to Right, 2700000 (45 degrees), 5400000 (90 degrees).
    """
    ln = shape.line._linePr
    # Remove existing fill elements (solidFill, noFill, etc.)
    for child in list(ln):
        if child.tag.endswith('Fill'):
            ln.remove(child)
            
    # Construct the gradFill XML element
    gradFill_xml = f"""
    <a:gradFill rotWithShape="1" xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">
        <a:gsLst>
            <a:gs pos="0">
                <a:srgbClr val="{color1}">
                    <a:alpha val="{alpha1}"/>
                </a:srgbClr>
            </a:gs>
            <a:gs pos="100000">
                <a:srgbClr val="{color2}">
                    <a:alpha val="{alpha2}"/>
                </a:srgbClr>
            </a:gs>
        </a:gsLst>
        <a:lin ang="{angle}" scaled="0"/>
    </a:gradFill>
    """
    gradFill = parse_xml(gradFill_xml)
    ln.append(gradFill)

def create_slide(
    output_pptx_path: str,
    title_text: str = '"ONE SMALL STEP FOR A MAN,\nA GIANT LEAP FOR MANKIND."',
    body_text: str = "NEIL ARMSTRONG",
    bg_palette: str = "space,moon", 
    accent_color: tuple = (255, 69, 0),  # Orange/Red accent for divider
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the 'Cinematic Orbital Quote Reveal' effect.
    Returns: path to the saved PPTX file.
    """
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6]) # Blank layout

    # === Layer 1: Background Image ===
    img_path = "bg_temp.jpg"
    try:
        # Fetch an image matching the theme
        url = f"https://source.unsplash.com/1920x1080/?{bg_palette.replace(' ', ',')}"
        urllib.request.urlretrieve(url, img_path)
        slide.shapes.add_picture(img_path, 0, 0, prs.slide_width, prs.slide_height)
    except Exception:
        # Fallback to dark gray background if download fails
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
        bg.fill.solid()
        bg.fill.fore_color.rgb = RGBColor(20, 20, 25)
        bg.line.fill.background()

    # Clean up temp image
    if os.path.exists(img_path):
        os.remove(img_path)

    # === Layer 2: Dimming Overlay ===
    # A black rectangle with transparency to make text readable against busy backgrounds
    overlay = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
    overlay.fill.solid()
    overlay.fill.fore_color.rgb = RGBColor(0, 0, 0)
    overlay.fill.transparency = 0.65
    overlay.line.fill.background()

    # === Layer 3: Rotating Gradient Arcs ===
    arc_size = Inches(6.5)
    center_x = (prs.slide_width - arc_size) / 2
    center_y = (prs.slide_height - arc_size) / 2

    # Arc 1 (Top/Right side)
    arc1 = slide.shapes.add_shape(MSO_SHAPE.ARC, center_x, center_y, arc_size, arc_size)
    arc1.adjustments[0] = 0.0    # Start angle
    arc1.adjustments[1] = 160.0  # End angle (leaves a 20 deg gap)
    arc1.line.width = Pt(4)
    apply_gradient_line(arc1, color1="FFFFFF", alpha1=100000, color2="FFFFFF", alpha2=0, angle=2700000)
    
    # Arc 2 (Bottom/Left side)
    arc2 = slide.shapes.add_shape(MSO_SHAPE.ARC, center_x, center_y, arc_size, arc_size)
    arc2.adjustments[0] = 180.0
    arc2.adjustments[1] = 340.0
    arc2.line.width = Pt(4)
    apply_gradient_line(arc2, color1="FFFFFF", alpha1=0, color2="FFFFFF", alpha2=100000, angle=2700000)

    # Apply ambient infinite rotation from _shell_helpers
    # Since they share the exact same bounding box, rotating them individually achieves the "orbit" effect
    add_infinite_rotation(slide, arc1, duration_ms=12000, direction="cw")
    add_infinite_rotation(slide, arc2, duration_ms=12000, direction="cw")

    # === Layer 4: Typography & Content ===
    # Text container restricted to the inner radius of the arcs
    text_width = Inches(5.5)
    text_height = Inches(3.0)
    tx_x = (prs.slide_width - text_width) / 2
    tx_y = (prs.slide_height - text_height) / 2

    textbox = slide.shapes.add_textbox(tx_x, tx_y, text_width, text_height)
    tf = textbox.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = 3 # Middle

    # Quote Paragraph
    p_quote = tf.paragraphs[0]
    p_quote.text = title_text
    p_quote.alignment = PP_ALIGN.CENTER
    p_quote.font.name = "Arial Black"
    p_quote.font.size = Pt(28)
    p_quote.font.color.rgb = RGBColor(255, 255, 255)
    p_quote.font.bold = True

    # Author Paragraph
    p_author = tf.add_paragraph()
    p_author.text = f"\n{body_text}"
    p_author.alignment = PP_ALIGN.CENTER
    p_author.font.name = "Arial"
    p_author.font.size = Pt(14)
    p_author.font.color.rgb = RGBColor(200, 200, 200)
    p_author.font.bold = True

    # Divider Line
    line_w = Inches(1.5)
    line_h = Pt(2)
    line_x = (prs.slide_width - line_w) / 2
    
    # Calculate a rough Y position for the divider (between quote and author)
    line_y = center_y + Inches(1.2)
    
    divider = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, line_x, line_y, line_w, line_h)
    divider.fill.solid()
    divider.fill.fore_color.rgb = RGBColor(*accent_color)
    divider.line.fill.background()

    prs.save(output_pptx_path)
    return output_pptx_path
