import os
import io
import tempfile
import urllib.request
from PIL import Image, ImageDraw
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.oxml import OxmlElement

def create_slide(
    output_pptx_path: str,
    title_text: str = "THANK YOU",
    overlay_style: str = "diagonal",  # Choose from: 'diagonal', 'stepped', 'vertical'
    bg_image_url: str = "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?q=80&w=1920&h=1080&fit=crop",
    overlay_color: tuple = (20, 30, 50, 160),  # Deep navy tint
    line_color: tuple = (255, 255, 255, 255),  # Pure white
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the "Geometric Split-Screen Gradient Overlay" effect.
    """
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6]) # blank layout

    # 1. Fetch Background Image (with solid color fallback)
    try:
        req = urllib.request.Request(bg_image_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            bg_image = Image.open(io.BytesIO(response.read())).convert("RGBA")
            bg_image = bg_image.resize((1920, 1080))
    except Exception:
        bg_image = Image.new("RGBA", (1920, 1080), (50, 50, 60, 255))

    # 2. Generate Geometric Overlay Mask using PIL
    overlay = Image.new("RGBA", (1920, 1080), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    line_width = 8

    if overlay_style == "vertical":
        draw.rectangle([0, 0, 960, 1080], fill=overlay_color)
        draw.line([(960, 0), (960, 1080)], fill=line_color, width=line_width)
        
    elif overlay_style == "stepped":
        points = [(0, 0), (800, 0), (800, 350), (1200, 350), (1200, 750), (1920, 750), (1920, 1080), (0, 1080)]
        draw.polygon(points, fill=overlay_color)
        # Draw contiguous boundary line using curve joints for crisp corners
        boundary = [(800, 0), (800, 350), (1200, 350), (1200, 750), (1920, 750)]
        draw.line(boundary, fill=line_color, width=line_width, joint="curve")
        
    else:  # 'diagonal' (Default)
        draw.polygon([(0, 0), (0, 1080), (1920, 1080)], fill=overlay_color)
        draw.line([(0, 0), (1920, 1080)], fill=line_color, width=line_width)

    # 3. Save and Insert Images with exact z-ordering
    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp_bg:
        bg_image.save(tmp_bg.name)
        bg_path = tmp_bg.name

    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp_overlay:
        overlay.save(tmp_overlay.name)
        overlay_path = tmp_overlay.name

    slide.shapes.add_picture(bg_path, 0, 0, width=prs.slide_width, height=prs.slide_height)
    slide.shapes.add_picture(overlay_path, 0, 0, width=prs.slide_width, height=prs.slide_height)

    os.unlink(bg_path)
    os.unlink(overlay_path)

    # 4. Add Central Framed Typography (Transparent Box + White Outline)
    left = Inches(3.166)
    top = Inches(2.75)
    width = Inches(7.0)
    height = Inches(2.0)

    rect = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, width, height)
    
    # Safely inject <a:noFill> right before <a:ln> to make the shape transparent
    spPr = rect._element.spPr
    fill_idx = -1
    for i, child in enumerate(list(spPr)):
        if 'Fill' in child.tag:
            fill_idx = i
            spPr.remove(child)
            
    noFill = OxmlElement('a:noFill')
    if fill_idx != -1:
        spPr.insert(fill_idx, noFill)
    else:
        for i, child in enumerate(list(spPr)):
            if child.tag.endswith('ln'):
                spPr.insert(i, noFill)
                break
        else:
            spPr.append(noFill)

    # Outline settings
    rect.line.color.rgb = RGBColor(line_color[0], line_color[1], line_color[2])
    rect.line.width = Pt(4)

    # Text Block Configuration
    tf = rect.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tf.paragraphs[0]
    p.text = title_text.upper()
    p.alignment = PP_ALIGN.CENTER

    font = p.font
    font.name = 'Arial'
    font.size = Pt(64)
    font.bold = True
    font.color.rgb = RGBColor(255, 255, 255)

    # Typography Enhancements: Letter Spacing and Drop Shadow via XML
    rPr = font._element
    rPr.set('spc', '1500')  # 15pt wide cinematic letter spacing

    effectLst = OxmlElement('a:effectLst')
    outerShdw = OxmlElement('a:outerShdw')
    outerShdw.set('blurRad', '30000')  # 3pt blur
    outerShdw.set('dist', '30000')     # 3pt distance
    outerShdw.set('dir', '2700000')    # 45-degree angle
    srgbClr = OxmlElement('a:srgbClr')
    srgbClr.set('val', '000000')
    alpha = OxmlElement('a:alpha')
    alpha.set('val', '60000')          # 60% shadow opacity
    srgbClr.append(alpha)
    outerShdw.append(srgbClr)
    effectLst.append(outerShdw)
    rPr.append(effectLst)

    prs.save(output_pptx_path)
    return output_pptx_path
