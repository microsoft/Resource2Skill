import os
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from PIL import Image, ImageDraw
from lxml import etree

def add_native_drop_shadow(shape):
    """
    Injects OOXML into a python-pptx shape to add a native PowerPoint drop shadow.
    This creates the "layered paper" depth effect.
    """
    spPr = shape.element.spPr
    # Create the effectLst element
    effectLst = etree.SubElement(spPr, '{http://schemas.openxmlformats.org/drawingml/2006/main}effectLst')
    
    # Create the outerShdw element
    outerShdw = etree.SubElement(effectLst, '{http://schemas.openxmlformats.org/drawingml/2006/main}outerShdw')
    outerShdw.set('blurRad', '200000') # Blur radius (20pt)
    outerShdw.set('dist', '100000')    # Distance (10pt)
    outerShdw.set('dir', '2700000')    # Direction (90 degrees / down)
    outerShdw.set('algn', 'tl')
    outerShdw.set('rotWithShape', '0')
    
    # Set shadow color and transparency
    srgbClr = etree.SubElement(outerShdw, '{http://schemas.openxmlformats.org/drawingml/2006/main}srgbClr')
    srgbClr.set('val', '000000') # Black shadow
    alpha = etree.SubElement(srgbClr, '{http://schemas.openxmlformats.org/drawingml/2006/main}alpha')
    alpha.set('val', '15000') # 15% opacity

def generate_cutout_placeholder(output_path: str, accent_color: tuple):
    """
    Generates a stylized transparent PNG representing the isolated person/cutout.
    Using PIL to ensure the script runs flawlessly without relying on external URLs.
    """
    width, height = 800, 1000
    # Create an image with transparent background (RGBA)
    img = Image.new('RGBA', (width, height), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)
    
    # Draw a dynamic stylized silhouette to represent the athlete
    # Body
    draw.polygon([(200, 1000), (300, 400), (500, 400), (700, 1000)], fill=(40, 40, 40, 255))
    # Head
    draw.ellipse([(320, 150), (480, 310)], fill=(40, 40, 40, 255))
    # Arm showing action/power
    draw.polygon([(500, 450), (750, 250), (700, 200), (480, 400)], fill=accent_color + (255,))
    
    # Add some placeholder text to the shirt
    draw.text((380, 500), "POWER", fill=(255, 255, 255, 255), font=None)
    
    img.save(output_path)
    return output_path

def create_slide(
    output_pptx_path: str,
    title_text: str = "飞人归来",
    subtitle_text: str = "苏炳添 晋级百米半决赛",
    body_text: str = "北京时间16日上午，2022俄勒冈田径世锦赛展开男子100米预赛的争夺。亚洲纪录保持者、中国选手苏炳添跑出10秒15的成绩排名小组第五，凭借递补前三名之外的第三好成绩惊险晋级17日上午的半决赛。",
    accent_color: tuple = (220, 38, 38),  # Red accent
    **kwargs,
) -> str:
    """
    Creates a PPTX file reproducing the Editorial Magazine Cutout Profile effect.
    """
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    # Use blank layout
    slide_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(slide_layout)
    
    # --- Layer 1: Canvas Background ---
    # A slightly off-white/gray background makes the white card pop
    bg = slide.shapes.add_shape(
        1, # msoShapeRectangle
        0, 0, prs.slide_width, prs.slide_height
    )
    bg.fill.solid()
    bg.fill.fore_color.rgb = RGBColor(240, 240, 242)
    bg.line.fill.background() # No line
    
    # --- Layer 2: The Magazine Content Card ---
    # Placed on the right side
    card_left = Inches(3.5)
    card_top = Inches(0.8)
    card_width = Inches(9.0)
    card_height = Inches(5.9)
    
    card = slide.shapes.add_shape(
        1, card_left, card_top, card_width, card_height
    )
    card.fill.solid()
    card.fill.fore_color.rgb = RGBColor(255, 255, 255) # Pure white
    card.line.fill.background()
    
    # Add OOXML drop shadow for depth (Layered effect)
    add_native_drop_shadow(card)
    
    # --- Layer 3: Typography on the Card ---
    # Decorative Top Left Text
    decor_tb = slide.shapes.add_textbox(Inches(4.0), Inches(1.2), Inches(3), Inches(0.5))
    dtf = decor_tb.text_frame
    dp = dtf.paragraphs[0]
    dp.text = "NO LIMITS / BREAK THE RECORD"
    dp.font.size = Pt(10)
    dp.font.color.rgb = RGBColor(150, 150, 150)
    dp.font.bold = True
    
    # Main Headline (Theme)
    title_tb = slide.shapes.add_textbox(Inches(4.0), Inches(1.8), Inches(7.5), Inches(1.2))
    ttf = title_tb.text_frame
    tp = ttf.paragraphs[0]
    tp.text = title_text
    tp.font.size = Pt(54)
    tp.font.bold = True
    tp.font.color.rgb = RGBColor(30, 30, 30)
    
    # Subtitle / Name (Accent Color)
    sub_tb = slide.shapes.add_textbox(Inches(4.0), Inches(3.0), Inches(7.5), Inches(0.8))
    stf = sub_tb.text_frame
    sp = stf.paragraphs[0]
    sp.text = subtitle_text
    sp.font.size = Pt(28)
    sp.font.bold = True
    sp.font.color.rgb = RGBColor(*accent_color)
    
    # Decorative Accent Line
    line = slide.shapes.add_shape(
        1, Inches(4.0), Inches(3.8), Inches(0.8), Inches(0.06)
    )
    line.fill.solid()
    line.fill.fore_color.rgb = RGBColor(*accent_color)
    line.line.fill.background()
    
    # Body Text
    body_tb = slide.shapes.add_textbox(Inches(4.0), Inches(4.2), Inches(6.0), Inches(2.0))
    btf = body_tb.text_frame
    btf.word_wrap = True
    bp = btf.paragraphs[0]
    bp.text = body_text
    bp.font.size = Pt(14)
    bp.font.color.rgb = RGBColor(100, 100, 100)
    bp.line_spacing = 1.5
    
    # Bottom Left Decorative ID
    id_tb = slide.shapes.add_textbox(Inches(4.0), Inches(6.0), Inches(3), Inches(0.5))
    idf = id_tb.text_frame
    idp = idf.paragraphs[0]
    idp.text = "NO. 123456789"
    idp.font.size = Pt(10)
    idp.font.color.rgb = RGBColor(*accent_color)
    idp.font.bold = True
    
    # --- Layer 4: The Cutout Character (Foreground Overlapping) ---
    # Generate the placeholder cutout
    cutout_path = "temp_cutout.png"
    generate_cutout_placeholder(cutout_path, accent_color)
    
    # Insert the transparent PNG. 
    # Notice it starts at Left: 0.5, overlapping the card at Left: 3.5
    pic = slide.shapes.add_picture(
        cutout_path, 
        Inches(0.2),  # Left
        Inches(1.5),  # Top
        height=Inches(6.0) # Height
    )
    
    # Cleanup temp file
    if os.path.exists(cutout_path):
        os.remove(cutout_path)
    
    # Save Presentation
    prs.save(output_pptx_path)
    return output_pptx_path

# Example usage:
# create_slide("editorial_profile.pptx")
