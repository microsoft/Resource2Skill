def create_slide(
    output_pptx_path: str,
    title_text: str = "N A T U R E",
    bg_color_top: tuple = (50, 150, 220),     # Sky blue
    bg_color_bottom: tuple = (240, 248, 255), # Alice blue / White
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the 3D Out-of-Bounds Pop-out Effect.
    
    Returns: path to the saved PPTX file.
    """
    import os
    import urllib.request
    from io import BytesIO
    from pptx import Presentation
    from pptx.util import Inches, Pt, Emu
    from pptx.dml.color import RGBColor
    from pptx.enum.text import PP_ALIGN
    from PIL import Image, ImageDraw

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6]) # Blank layout

    # ==========================================
    # Helper: Download or Generate Assets
    # ==========================================
    def get_image(url, fallback_color, size, is_transparent=False):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=5) as response:
                img = Image.open(BytesIO(response.read())).convert("RGBA")
                return img
        except Exception as e:
            # Fallback generation if download fails
            print(f"Download failed, using fallback. Error: {e}")
            img = Image.new('RGBA', size, (0,0,0,0) if is_transparent else fallback_color)
            if is_transparent:
                draw = ImageDraw.Draw(img)
                draw.ellipse([size[0]*0.2, size[1]*0.1, size[0]*0.8, size[1]*0.9], fill=fallback_color)
            return img

    # Use stable Wikimedia Commons images (Transparent Elephant & Jungle Background)
    subject_url = "https://upload.wikimedia.org/wikipedia/commons/png/3/37/African_Elephant_Transparent.png"
    bg_texture_url = "https://images.unsplash.com/photo-1542273917363-3b1817f69a2d?q=80&w=1200&auto=format&fit=crop"

    print("Fetching assets...")
    subject_img = get_image(subject_url, (100, 100, 100, 255), (800, 600), True)
    # Resize subject to a manageable internal resolution
    subject_img.thumbnail((800, 800), Image.Resampling.LANCZOS)
    
    bg_img = get_image(bg_texture_url, (34, 45, 34, 255), (1200, 800), False)
    
    # ==========================================
    # Image Processing: Create Perspective Floor
    # ==========================================
    print("Generating perspective floor...")
    # 1. Crop the bottom 25% of the background to act as the "ground"
    w, h = bg_img.size
    crop_h = int(h * 0.25)
    floor_base = bg_img.crop((0, h - crop_h, w, h))
    
    # 2. Programmatically warp into a trapezoid (Perspective logic)
    fw, fh = floor_base.size
    top_shrink_ratio = 0.4 # Shrink the top width by 40% to create depth
    
    floor_trapezoid = Image.new('RGBA', (fw, fh), (0,0,0,0))
    for y in range(fh):
        progress = y / fh
        # Width goes from (fw * (1 - top_shrink_ratio)) at top, to fw at bottom
        current_w = int(fw * (1 - top_shrink_ratio) + (fw * top_shrink_ratio * progress))
        if current_w <= 0: continue
        
        row = floor_base.crop((0, y, fw, y+1))
        row = row.resize((current_w, 1), Image.Resampling.LANCZOS)
        x_offset = (fw - current_w) // 2
        floor_trapezoid.paste(row, (x_offset, y))

    floor_path = "temp_floor.png"
    floor_trapezoid.save(floor_path)
    
    subject_path = "temp_subject.png"
    subject_img.save(subject_path)

    # ==========================================
    # Layer 1: Background Gradient (Sky)
    # ==========================================
    bg_shape = slide.shapes.add_shape(
        1, # msoShapeRectangle
        0, 0, prs.slide_width, prs.slide_height
    )
    bg_shape.line.fill.background()
    
    # Apply gradient via lxml OOXML injection
    fill = bg_shape.fill
    fill.solid() # Init fill
    fill_xml = f"""
    <a:gradFill xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" rotWithShape="1">
        <a:gsLst>
            <a:gs pos="0">
                <a:srgbClr val="{bg_color_top[0]:02X}{bg_color_top[1]:02X}{bg_color_top[2]:02X}"/>
            </a:gs>
            <a:gs pos="100000">
                <a:srgbClr val="{bg_color_bottom[0]:02X}{bg_color_bottom[1]:02X}{bg_color_bottom[2]:02X}"/>
            </a:gs>
        </a:gsLst>
        <a:lin ang="5400000" scaled="1"/>
    </a:gradFill>
    """
    bg_shape.element.spPr.replace(bg_shape.element.spPr.find('{http://schemas.openxmlformats.org/drawingml/2006/main}solidFill'), 
                                  fromstring(fill_xml))

    # ==========================================
    # Layer 2: Atmospheric Text Backdrop
    # ==========================================
    # Add large text behind the main subject
    tb = slide.shapes.add_textbox(Inches(1), Inches(1.5), Inches(11.33), Inches(3))
    tf = tb.text_frame
    tf.text = title_text
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    p.font.size = Pt(140)
    p.font.name = 'Arial Black'
    p.font.bold = True
    # Semi-transparent white to blend with sky
    p.font.color.rgb = RGBColor(255, 255, 255)
    
    # Inject transparency to text color (approx 60% transparent)
    for run in p.runs:
        rPr = run._r.get_or_add_rPr()
        solidFill = rPr.get_or_add_solidFill()
        srgbClr = solidFill.get_or_add_srgbClr()
        srgbClr.val = "FFFFFF"
        alpha = OxmlElement('a:alpha')
        alpha.set('val', '40000') # 40% opacity
        srgbClr.append(alpha)

    # ==========================================
    # Layer 3: The Perspective Floor
    # ==========================================
    floor_width = Inches(10)
    floor_height = floor_width * (fh / fw)
    floor_left = (prs.slide_width - floor_width) / 2
    floor_top = prs.slide_height - floor_height - Inches(0.5)
    
    slide.shapes.add_picture(floor_path, floor_left, floor_top, floor_width, floor_height)

    # ==========================================
    # Layer 4: The Cutout Subject
    # ==========================================
    # Calculate subject placement to align with the floor
    # We want the bottom of the subject to rest slightly above the bottom of the floor
    sub_w, sub_h = subject_img.size
    
    # Scale subject height to overlap the top boundary while fitting on slide
    target_sub_height = Inches(5.5)
    target_sub_width = target_sub_height * (sub_w / sub_h)
    
    sub_left = (prs.slide_width - target_sub_width) / 2
    # Align bottom of subject with bottom 10% of the floor
    sub_top = (floor_top + floor_height) - target_sub_height - Inches(0.2)
    
    slide.shapes.add_picture(subject_path, sub_left, sub_top, target_sub_width, target_sub_height)

    # Cleanup temp files
    try:
        os.remove(floor_path)
        os.remove(subject_path)
    except:
        pass

    prs.save(output_pptx_path)
    return output_pptx_path

# Helper import for XML injection
from pptx.oxml import parse_xml
from pptx.oxml.ns import nsdecls
from lxml.etree import fromstring
from pptx.oxml.xmlchemy import OxmlElement
