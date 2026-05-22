import os
import urllib.request
from typing import Tuple
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN
from lxml import etree
from PIL import Image, ImageDraw

def _add_drop_shadow(shape, color="000000", blur_rad=100000, dist=30000, dir=5400000, alpha=15000):
    """
    Injects Open XML to add a subtle drop shadow to a python-pptx shape.
    Used to create UI elevation.
    """
    spPr = shape.element.find('.//p:spPr', namespaces=shape.element.nsmap)
    if spPr is not None:
        effectLst = etree.SubElement(spPr, '{http://schemas.openxmlformats.org/drawingml/2006/main}effectLst')
        outerShdw = etree.SubElement(effectLst, '{http://schemas.openxmlformats.org/drawingml/2006/main}outerShdw')
        outerShdw.set('blurRad', str(blur_rad))
        outerShdw.set('dist', str(dist))
        outerShdw.set('dir', str(dir))
        outerShdw.set('algn', 'tl')
        
        srgbClr = etree.SubElement(outerShdw, '{http://schemas.openxmlformats.org/drawingml/2006/main}srgbClr')
        srgbClr.set('val', color)
        
        alpha_node = etree.SubElement(srgbClr, '{http://schemas.openxmlformats.org/drawingml/2006/main}alpha')
        alpha_node.set('val', str(alpha))

def _create_rounded_image(image_url: str, output_path: str, width_px: int, height_px: int, corner_radius: int = 40):
    """
    Downloads an image and uses PIL to crop it to a specific size with rounded corners and transparent background.
    """
    try:
        req = urllib.request.Request(image_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            img = Image.open(response).convert("RGBA")
    except Exception:
        # Fallback to a solid color block if download fails
        img = Image.new("RGBA", (width_px, height_px), (200, 200, 210, 255))
        
    # Resize and crop to fill
    img_ratio = img.width / img.height
    target_ratio = width_px / height_px
    
    if img_ratio > target_ratio:
        # Image is wider, crop width
        new_width = int(img.height * target_ratio)
        offset = (img.width - new_width) // 2
        img = img.crop((offset, 0, offset + new_width, img.height))
    else:
        # Image is taller, crop height
        new_height = int(img.width / target_ratio)
        offset = (img.height - new_height) // 2
        img = img.crop((0, offset, img.width, offset + new_height))
        
    img = img.resize((width_px, height_px), Image.Resampling.LANCZOS)
    
    # Create mask for rounded corners
    mask = Image.new("L", (width_px, height_px), 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle((0, 0, width_px, height_px), radius=corner_radius, fill=255)
    
    # Apply mask
    rounded_img = Image.new("RGBA", (width_px, height_px), (0, 0, 0, 0))
    rounded_img.paste(img, (0, 0), mask=mask)
    rounded_img.save(output_path, "PNG")
    return output_path

def create_slide(
    output_pptx_path: str,
    title_text: str = "Museum Art App",
    body_text: str = "Explore contemporary collections and upcoming exhibitions.",
    bg_palette: str = "art,museum", 
    accent_color: tuple = (255, 59, 48), # Default iOS Red accent
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the Modern App UI Showcase effect.
    """
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6]) # Blank slide
    
    # Colors
    bg_color = RGBColor(245, 245, 247)
    text_primary = RGBColor(29, 29, 31)
    text_secondary = RGBColor(134, 134, 139)
    accent_rgb = RGBColor(*accent_color)
    
    # === 1. Slide Background ===
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
    bg.fill.solid()
    bg.fill.fore_color.rgb = bg_color
    bg.line.fill.background()
    
    # === 2. Horizontal Gallery (Simulated Horizontal Scroll) ===
    gallery_y = Inches(1.5)
    card_width = Inches(3.8)
    card_height = Inches(2.2)
    gap = Inches(0.4)
    start_x = Inches(0.6)
    
    # Gallery Title
    tb = slide.shapes.add_textbox(start_x, gallery_y - Inches(0.5), Inches(5), Inches(0.5))
    p = tb.text_frame.add_paragraph()
    p.text = "Featured Exhibitions"
    p.font.size = Pt(20)
    p.font.bold = True
    p.font.color.rgb = text_primary
    
    gallery_images = [
        f"https://source.unsplash.com/random/800x600/?{bg_palette},1",
        f"https://source.unsplash.com/random/800x600/?{bg_palette},2",
        f"https://source.unsplash.com/random/800x600/?{bg_palette},3"
    ]
    
    for i, img_url in enumerate(gallery_images):
        x = start_x + i * (card_width + gap)
        # Create rounded image using PIL
        tmp_img = f"temp_gallery_{i}.png"
        _create_rounded_image(img_url, tmp_img, width_px=800, height_px=460, corner_radius=30)
        
        pic = slide.shapes.add_picture(tmp_img, x, gallery_y, width=card_width, height=card_height)
        _add_drop_shadow(pic, blur_rad=120000, dist=40000, alpha=15000) # Subtle UI shadow
        os.remove(tmp_img)
        
    # === 3. Vertical Components List (Auto Layout Simulation) ===
    list_y_start = gallery_y + card_height + Inches(0.8)
    
    # List Title
    tb = slide.shapes.add_textbox(start_x, list_y_start - Inches(0.5), Inches(5), Inches(0.5))
    p = tb.text_frame.add_paragraph()
    p.text = "Upcoming Events"
    p.font.size = Pt(20)
    p.font.bold = True
    p.font.color.rgb = text_primary
    
    events = [
        ("Modern Sculpture Workshop", "Tomorrow, 10:00 AM • Studio B"),
        ("Abstract Art Tour", "Oct 15, 2:00 PM • Main Gallery"),
        ("Curator Talk: Post-War Era", "Oct 18, 6:00 PM • Auditorium")
    ]
    
    for i, (ev_title, ev_sub) in enumerate(events):
        y = list_y_start + i * Inches(0.9)
        
        # Component Background Card
        row_card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, start_x, y, Inches(12.1), Inches(0.8))
        row_card.fill.solid()
        row_card.fill.fore_color.rgb = RGBColor(255, 255, 255)
        row_card.line.fill.background()
        # Adjust corner radius for the PPTX shape (native)
        adj = row_card.adjustments
        adj[0] = 0.15 
        _add_drop_shadow(row_card, blur_rad=80000, dist=20000, alpha=8000)
        
        # Thumbnail (Small rounded square)
        tmp_img = f"temp_thumb_{i}.png"
        thumb_url = f"https://source.unsplash.com/random/200x200/?{bg_palette},event,{i}"
        _create_rounded_image(thumb_url, tmp_img, width_px=150, height_px=150, corner_radius=20)
        slide.shapes.add_picture(tmp_img, start_x + Inches(0.15), y + Inches(0.15), width=Inches(0.5), height=Inches(0.5))
        os.remove(tmp_img)
        
        # Text Component
        tb = slide.shapes.add_textbox(start_x + Inches(0.8), y + Inches(0.1), Inches(10), Inches(0.6))
        
        # Title
        p1 = tb.text_frame.paragraphs[0]
        p1.text = ev_title
        p1.font.size = Pt(14)
        p1.font.bold = True
        p1.font.color.rgb = text_primary
        
        # Subtitle
        p2 = tb.text_frame.add_paragraph()
        p2.text = ev_sub
        p2.font.size = Pt(11)
        p2.font.color.rgb = text_secondary
        
        # Action button (simulated)
        btn = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, start_x + Inches(11.0), y + Inches(0.2), Inches(0.9), Inches(0.4))
        btn.fill.solid()
        btn.fill.fore_color.rgb = RGBColor(240, 240, 245)
        btn.line.fill.background()
        btn_text = btn.text_frame.paragraphs[0]
        btn_text.text = "View"
        btn_text.font.size = Pt(11)
        btn_text.font.bold = True
        btn_text.font.color.rgb = accent_rgb
        btn_text.alignment = PP_ALIGN.CENTER
        
    # === 4. Sticky Glassmorphism Header (Z-Index Top) ===
    # Using a rectangle with transparency and a subtle bottom border
    header = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, Inches(1.0))
    header.fill.solid()
    header.fill.fore_color.rgb = RGBColor(255, 255, 255)
    header.fill.transparency = 0.15 # 85% opacity creates frosted look over light bg
    
    header.line.color.rgb = RGBColor(230, 230, 235)
    header.line.width = Pt(1)
    _add_drop_shadow(header, blur_rad=100000, dist=10000, alpha=10000)
    
    # App Header Title
    tb = slide.shapes.add_textbox(Inches(0.4), Inches(0.25), Inches(5), Inches(0.5))
    p = tb.text_frame.paragraphs[0]
    p.text = title_text
    p.font.size = Pt(24)
    p.font.bold = True
    p.font.color.rgb = text_primary
    
    # Subtitle / Body in header
    tb2 = slide.shapes.add_textbox(Inches(5.0), Inches(0.35), Inches(8), Inches(0.5))
    p_body = tb2.text_frame.paragraphs[0]
    p_body.text = body_text
    p_body.font.size = Pt(12)
    p_body.font.color.rgb = text_secondary
    p_body.alignment = PP_ALIGN.RIGHT
    
    prs.save(output_pptx_path)
    return output_pptx_path
