import os
import io
import urllib.request
from PIL import Image, ImageDraw, ImageOps
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml import parse_xml

def create_slide(
    output_pptx_path: str,
    title_text: str = "TITLE",
    subtitle_text: str = "subtitle",
    body_text: str = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam.",
    img_url: str = "https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?q=80&w=1920&auto=format&fit=crop"
) -> str:
    """
    Create a PPTX file reproducing the 'Geometric Glass-Shard Reveal' visual effect.
    """
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    # ==========================================
    # 1. Background Layer (LXML Gradient)
    # ==========================================
    bg_rect = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
    bg_rect.line.fill.background()
    
    # Remove default solid fill and apply gradient
    for elem in list(bg_rect.element.spPr):
        if elem.tag.endswith('Fill'):
            bg_rect.element.spPr.remove(elem)
            
    grad_xml = """
    <a:gradFill rotWithShape="1" xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">
      <a:gsLst>
        <a:gs pos="0"><a:srgbClr val="1A2130"/></a:gs>
        <a:gs pos="100000"><a:srgbClr val="0B0E14"/></a:gs>
      </a:gsLst>
      <a:lin ang="5400000" scaled="0"/>
    </a:gradFill>
    """
    bg_rect.element.spPr.append(parse_xml(grad_xml))

    # ==========================================
    # 2. Giant Watermark Icon (LXML Opacity)
    # ==========================================
    icon_box = slide.shapes.add_textbox(Inches(0), Inches(0), Inches(6), Inches(6))
    icon_box.rotation = -20
    icon_run = icon_box.text_frame.paragraphs[0].add_run()
    icon_run.text = "✈"
    icon_run.font.size = Pt(350)
    
    # Inject 8% opacity white fill
    rPr = icon_run._r.get_or_add_rPr()
    for child in list(rPr):
        if child.tag.endswith('Fill'):
            rPr.remove(child)
    opacity_xml = """
    <a:solidFill xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">
        <a:srgbClr val="FFFFFF"><a:alpha val="8000"/></a:srgbClr>
    </a:solidFill>
    """
    rPr.append(parse_xml(opacity_xml))

    # ==========================================
    # 3. Geometric Glass-Shard Mask (PIL)
    # ==========================================
    try:
        req = urllib.request.Request(img_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            img = Image.open(io.BytesIO(response.read())).convert("RGBA")
            img = ImageOps.fit(img, (1920, 1080), Image.Resampling.LANCZOS)
    except Exception:
        # Fallback if download fails
        img = Image.new('RGBA', (1920, 1080), (30, 80, 120, 255))

    # Create Alpha Mask for the exact triangle cutouts
    mask = Image.new('L', (1920, 1080), 0)
    draw = ImageDraw.Draw(mask)
    draw.polygon([(1100, -10), (1800, -10), (1450, 900)], fill=255)       # Top triangle
    draw.polygon([(1300, 1090), (1920, 1090), (1610, 200)], fill=255)     # Bottom triangle
    draw.polygon([(1930, 100), (1930, 1000), (1200, 550)], fill=255)      # Right triangle
    
    img.putalpha(mask)

    # Create semi-transparent glass layer
    glass = Image.new('RGBA', (1920, 1080), (0, 0, 0, 0))
    g_draw = ImageDraw.Draw(glass)
    g_draw.polygon([(1150, -10), (1500, -10), (1325, 450)], fill=(255, 255, 255, 40))
    g_draw.polygon([(1930, 300), (1930, 800), (1400, 550)], fill=(255, 255, 255, 40))

    # Composite layers
    final_img = Image.alpha_composite(img, glass)
    temp_img_path = "temp_shard_overlay.png"
    final_img.save(temp_img_path)

    # Insert into slide
    slide.shapes.add_picture(temp_img_path, 0, 0, prs.slide_width, prs.slide_height)

    # ==========================================
    # 4. Typography & Drop Shadows
    # ==========================================
    def add_run_shadow(run, angle_deg, dist_pt=4, blur_pt=5, opacity=60):
        rPr = run._r.get_or_add_rPr()
        for child in list(rPr):
            if child.tag.endswith('effectLst'):
                rPr.remove(child)
        
        angle_val = int(angle_deg * 60000)
        dist_emu = int(dist_pt * 12700)
        blur_emu = int(blur_pt * 12700)
        alpha_val = int(opacity * 1000)
        
        shadow_xml = f"""
        <a:effectLst xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">
            <a:outerShdw blurRad="{blur_emu}" dist="{dist_emu}" dir="{angle_val}">
                <a:srgbClr val="000000"><a:alpha val="{alpha_val}"/></a:srgbClr>
            </a:outerShdw>
        </a:effectLst>
        """
        rPr.append(parse_xml(shadow_xml))

    # Title
    title_box = slide.shapes.add_textbox(Inches(0.8), Inches(2.3), Inches(6), Inches(2))
    title_run = title_box.text_frame.paragraphs[0].add_run()
    title_run.text = title_text.upper()
    title_run.font.name = "Arial Black"
    title_run.font.size = Pt(100)
    title_run.font.color.rgb = RGBColor(255, 255, 255)
    add_run_shadow(title_run, angle_deg=90)  # Shadow goes DOWN

    # Subtitle (Overlaps title)
    sub_box = slide.shapes.add_textbox(Inches(2.5), Inches(3.6), Inches(5), Inches(1.5))
    sub_box.rotation = -3  # Slight stylistic tilt
    sub_run = sub_box.text_frame.paragraphs[0].add_run()
    sub_run.text = subtitle_text
    sub_run.font.name = "Segoe Script"
    sub_run.font.size = Pt(65)
    sub_run.font.color.rgb = RGBColor(255, 204, 0)
    add_run_shadow(sub_run, angle_deg=270, dist_pt=3, blur_pt=4)  # Shadow goes UP

    # Body Text
    body_box = slide.shapes.add_textbox(Inches(0.9), Inches(5.2), Inches(5.5), Inches(1.5))
    body_run = body_box.text_frame.paragraphs[0].add_run()
    body_run.text = body_text
    body_run.font.name = "Calibri"
    body_run.font.size = Pt(12)
    body_run.font.color.rgb = RGBColor(220, 225, 230)
    body_box.text_frame.paragraphs[0].alignment = 3  # Justify

    # Cleanup and Save
    prs.save(output_pptx_path)
    if os.path.exists(temp_img_path):
        os.remove(temp_img_path)
        
    return output_pptx_path
