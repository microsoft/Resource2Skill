import os
import urllib.request
from io import BytesIO
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from lxml import etree
from PIL import Image, ImageOps

def create_slide(
    output_pptx_path: str,
    title_text: str = "FUNCTIONAL",
    subtitle_text: str = "DESIGN SYSTEM",
    cta_text: str = "JOIN NOW",
    image_url: str = "https://images.unsplash.com/photo-1549490349-8643362247b5?q=80&w=1000&auto=format&fit=crop",
    neutral_color: tuple = (246, 244, 241),       # Off-White (Canvas)
    communicator_color: tuple = (18, 38, 56),     # Navy (Text/Shadows)
    action_color: tuple = (235, 94, 40),          # Orange (CTA)
    support_color: tuple = (119, 186, 173),       # Teal (Secondary blocks)
    anchor_color: tuple = (180, 180, 180),        # Gray (Grid lines)
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the Functional Color Mapping (Swiss Brutalist Grid) effect.
    """
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6]) # Blank slide
    
    # Helper functions for coloring and OOXML injection
    def apply_color(element, rgb_tuple):
        element.color.rgb = RGBColor(*rgb_tuple)
        
    def draw_line(slide, x, y, w, h, rgb_tuple):
        # Using a 1pt rectangle as a strict, clean grid line
        line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, y, w, h)
        line.fill.solid()
        line.fill.fore_color.rgb = RGBColor(*rgb_tuple)
        line.line.fill.background() # No border
        return line

    def add_hard_shadow(shape, rgb_tuple):
        # Inject custom OOXML for a 0-blur brutalist hard shadow
        hex_color = '%02X%02X%02X' % rgb_tuple
        spPr = shape.element.spPr
        effectLst = etree.SubElement(spPr, '{http://schemas.openxmlformats.org/drawingml/2006/main}effectLst')
        outerShdw = etree.SubElement(
            effectLst, '{http://schemas.openxmlformats.org/drawingml/2006/main}outerShdw',
            blurRad="0", dist="63500", dir="2700000", algn="tl", rotWithShape="0"
        ) # dist=63500 is ~5pt, dir=2700000 is 45 deg down/right
        etree.SubElement(
            outerShdw, '{http://schemas.openxmlformats.org/drawingml/2006/main}srgbClr', val=hex_color
        )

    # === Layer 1: The Neutral Canvas ===
    bg = slide.background
    bg.fill.solid()
    bg.fill.fore_color.rgb = RGBColor(*neutral_color)

    # === Layer 2: The Anchor Grid (Structural Lines) ===
    # Top Nav Separator
    draw_line(slide, 0, Inches(0.8), Inches(13.333), Pt(1), anchor_color)
    # Center Vertical Separator
    draw_line(slide, Inches(6.666), Inches(0.8), Pt(1), Inches(4.7), anchor_color)
    # Bottom Row Separator
    draw_line(slide, 0, Inches(5.5), Inches(13.333), Pt(1), anchor_color)

    # === Layer 3: Top Navigation ===
    tx_box = slide.shapes.add_textbox(Inches(0.4), Inches(0.2), Inches(3), Inches(0.5))
    tf = tx_box.text_frame
    p = tf.paragraphs[0]
    p.text = "SATORI SYSTEM"
    p.font.bold = True
    p.font.size = Pt(14)
    p.font.name = "Arial"
    apply_color(p.font, communicator_color)

    # === Layer 4: Quadrant 1 - Communicator & Action Hero ===
    # Huge Typography
    tx_box = slide.shapes.add_textbox(Inches(0.4), Inches(1.3), Inches(5.8), Inches(2.5))
    tf = tx_box.text_frame
    tf.word_wrap = True
    
    p1 = tf.paragraphs[0]
    p1.text = title_text
    p1.font.bold = True
    p1.font.size = Pt(64)
    p1.font.name = "Arial Black"
    apply_color(p1.font, communicator_color)
    
    p2 = tf.add_paragraph()
    p2.text = subtitle_text
    p2.font.bold = True
    p2.font.size = Pt(64)
    p2.font.name = "Arial Black"
    apply_color(p2.font, communicator_color)

    p3 = tf.add_paragraph()
    p3.text = "\nStop picking colors based on taste. Start assigning them specific functional roles for a smarter, high-conversion visual hierarchy."
    p3.font.size = Pt(14)
    p3.font.name = "Arial"
    apply_color(p3.font, communicator_color)

    # The Action CTA Button
    btn = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.5), Inches(4.2), Inches(2.2), Inches(0.6))
    btn.fill.solid()
    btn.fill.fore_color.rgb = RGBColor(*action_color)
    btn.line.fill.background()
    # Inject brutalist hard shadow using the Communicator color
    add_hard_shadow(btn, communicator_color)
    
    btn_tf = btn.text_frame
    btn_tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    btn_p = btn_tf.paragraphs[0]
    btn_p.text = cta_text
    btn_p.font.bold = True
    btn_p.font.size = Pt(14)
    btn_p.font.name = "Arial"
    apply_color(btn_p.font, neutral_color)
    btn_p.alignment = PP_ALIGN.CENTER

    # === Layer 5: Quadrant 2 - The System Integrated Image (Duotone via PIL) ===
    img_path = "temp_duotone.png"
    target_size = (1200, 846) # Approximate ratio for 6.666 x 4.7 inches
    
    try:
        req = urllib.request.Request(image_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            img = Image.open(BytesIO(response.read())).convert("RGB")
            # Fit and crop
            img = ImageOps.fit(img, target_size, method=Image.Resampling.LANCZOS)
            # Convert to Grayscale
            img_l = img.convert("L")
            # Apply Duotone mapping: Shadows -> Navy, Highlights -> Off-White
            duotone = ImageOps.colorize(img_l, black=communicator_color, white=neutral_color)
            duotone.save(img_path, format="PNG")
    except Exception as e:
        # Fallback if image download fails: Create a solid Support Color block with a pattern
        img = Image.new("RGB", target_size, support_color)
        img.save(img_path, format="PNG")

    # Insert Image filling the entire right quadrant flawlessly
    slide.shapes.add_picture(img_path, Inches(6.666), Inches(0.8), Inches(6.666), Inches(4.7))

    # === Layer 6: Quadrant 3 - The Support Role Block ===
    # A block specifically demonstrating the Support Color
    sup_block = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, Inches(5.5), Inches(6.666), Inches(2.0))
    sup_block.fill.solid()
    sup_block.fill.fore_color.rgb = RGBColor(*support_color)
    sup_block.line.fill.background()

    tx_box = slide.shapes.add_textbox(Inches(0.4), Inches(5.8), Inches(5.8), Inches(1.5))
    tf = tx_box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "SUPPORT ROLE"
    p.font.bold = True
    p.font.size = Pt(18)
    apply_color(p.font, communicator_color)
    
    p_sub = tf.add_paragraph()
    p_sub.text = "Guiding the eye's flow between sections without stealing focus from the primary action."
    p_sub.font.size = Pt(12)
    apply_color(p_sub.font, communicator_color)

    # === Layer 7: Quadrant 4 - Data / Extra Info ===
    tx_box = slide.shapes.add_textbox(Inches(7.0), Inches(5.8), Inches(5.8), Inches(1.5))
    tf = tx_box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "ANCHOR ROLE"
    p.font.bold = True
    p.font.size = Pt(18)
    apply_color(p.font, communicator_color)
    
    p_sub = tf.add_paragraph()
    p_sub.text = "Providing structural grid lines and stability. Notice the subtle gray 1pt lines dividing this entire canvas."
    p_sub.font.size = Pt(12)
    apply_color(p_sub.font, communicator_color)

    # Cleanup temp image
    if os.path.exists(img_path):
        os.remove(img_path)

    prs.save(output_pptx_path)
    return output_pptx_path
