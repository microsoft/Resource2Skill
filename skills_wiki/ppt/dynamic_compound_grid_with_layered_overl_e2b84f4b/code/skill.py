import os
import urllib.request
from io import BytesIO
from lxml import etree
from PIL import Image, ImageDraw
from pptx import Presentation
from pptx.util import Pt, Inches, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.oxml.ns import qn

def create_slide(
    output_pptx_path: str,
    title_text: str = "DYNAMIC\nGRID\nSYSTEMS",
    body_text: str = "Combining column and modular grids with strategic overlapping creates visual interest, breaking monotony while maintaining organized structure.",
    bg_palette: str = "architecture",  
    accent_color: tuple = (229, 57, 53),  # Vibrant Editorial Red
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the "Dynamic Compound Grid with Layered Overlap" effect.
    """
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6]) # Blank layout

    # Canvas and Grid Setup (12 Column Grid)
    margin = Inches(0.666)
    usable_width = prs.slide_width - (margin * 2)
    col_width = usable_width / 12
    gutter = Inches(0.15)

    # Background Fill
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(245, 245, 245)

    # ==========================================
    # Layer 1: Image (Spans Cols 1 to 7)
    # ==========================================
    img_width = int((7 * col_width) - gutter)
    img_height = int(Inches(5.5))
    img_left = margin
    img_top = Inches(0.666)
    
    img_path = "temp_grid_hero.jpg"
    
    # Attempt to download image, fallback to PIL generation
    try:
        url = f"https://picsum.photos/seed/{bg_palette}/{int(img_width/914400*150)}/{int(img_height/914400*150)}"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=5) as response:
            img_data = response.read()
            img = Image.open(BytesIO(img_data)).convert("RGB")
            img.save(img_path)
    except Exception:
        # Fallback PIL geometric pattern
        img = Image.new('RGB', (800, 600), color=(30, 30, 30))
        draw = ImageDraw.Draw(img)
        for i in range(0, 800, 40):
            draw.line([(i, 0), (0, i)], fill=(60, 60, 60), width=2)
            draw.line([(i, 600), (800, i-200)], fill=(60, 60, 60), width=2)
        img.save(img_path)

    pic = slide.shapes.add_picture(img_path, img_left, img_top, width=img_width, height=img_height)
    if os.path.exists(img_path):
        os.remove(img_path)

    # ==========================================
    # Layer 2: Overlapping Text Block (Cols 6 to 11)
    # Creates depth by overlapping the image by 2 columns
    # ==========================================
    overlap_cols = 5
    box_width = (overlap_cols * col_width)
    box_height = Inches(4.5)
    box_left = margin + (6 * col_width) # Starts at col 7
    box_top = Inches(2.2) # Shifted down to break vertical symmetry

    # Create Shape
    shape = slide.shapes.add_shape(
        1, # msoShapeRectangle
        box_left, box_top, box_width, box_height
    )
    shape.fill.solid()
    shape.fill.fore_color.rgb = RGBColor(*accent_color)
    shape.line.fill.background() # No line

    # --- XML INJECTION: Add Drop Shadow to Overlap Box ---
    spPr = shape.element.spPr
    effectLst = etree.SubElement(spPr, qn('a:effectLst'))
    outerShdw = etree.SubElement(effectLst, qn('a:outerShdw'))
    outerShdw.set('blurRad', str(Emu(Inches(0.2)))) # Blur
    outerShdw.set('dist', str(Emu(Inches(0.08))))   # Distance
    outerShdw.set('dir', '2700000')                 # Angle (45 deg)
    
    srgbClr = etree.SubElement(outerShdw, qn('a:srgbClr'))
    srgbClr.set('val', '000000') # Black shadow
    alpha = etree.SubElement(srgbClr, qn('a:alpha'))
    alpha.set('val', '25000') # 25% opacity

    # ==========================================
    # Layer 3: Typography inside Overlap Box
    # ==========================================
    text_frame = shape.text_frame
    text_frame.margin_left = Inches(0.4)
    text_frame.margin_top = Inches(0.4)
    
    p = text_frame.paragraphs[0]
    p.text = title_text.upper()
    p.font.name = "Arial" # Standard bold sans-serif
    p.font.size = Pt(54)
    p.font.bold = True
    p.font.color.rgb = RGBColor(255, 255, 255)
    p.line_spacing = 0.9

    # ==========================================
    # Layer 4: Secondary Body Text (Modular Grid Alignment)
    # Aligned to Cols 8 to 11, below the main title
    # ==========================================
    body_width = (4 * col_width)
    body_height = Inches(1.5)
    body_left = box_left + Inches(0.4)
    body_top = box_top + box_height - Inches(1.2) # Anchored to bottom of red box

    # Create a separate text box for body so it overlays the red box bottom 
    # but could extend if needed (creates dynamic tension)
    body_box = slide.shapes.add_textbox(body_left, body_top, body_width, body_height)
    body_frame = body_box.text_frame
    body_frame.word_wrap = True
    
    p2 = body_frame.paragraphs[0]
    p2.text = body_text
    p2.font.name = "Calibri"
    p2.font.size = Pt(14)
    p2.font.color.rgb = RGBColor(255, 255, 255) # White text for contrast on accent color

    # Save Presentation
    prs.save(output_pptx_path)
    return output_pptx_path

