import os
import urllib.request
from io import BytesIO
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from PIL import Image, ImageDraw, ImageFilter

def _create_avatar_image(image_url_or_color, size=300, border_w=12, shadow_blur=15):
    """
    Generates a circular avatar with a white border and a soft drop shadow.
    Returns an Image object.
    """
    pad = 40
    img_size = size + pad * 2
    
    # Base shadow layer
    shadow_layer = Image.new('RGBA', (img_size, img_size), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow_layer)
    shadow_bbox = [pad, pad, pad + size, pad + size]
    sd.ellipse(shadow_bbox, fill=(0, 0, 0, 120))
    shadow_layer = shadow_layer.filter(ImageFilter.GaussianBlur(shadow_blur))
    
    # Avatar image
    try:
        req = urllib.request.Request(image_url_or_color, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            avatar = Image.open(BytesIO(response.read())).convert('RGBA')
            # Crop to square first
            w, h = avatar.size
            min_side = min(w, h)
            avatar = avatar.crop(((w - min_side) // 2, (h - min_side) // 2, 
                                  (w + min_side) // 2, (h + min_side) // 2))
            avatar = avatar.resize((size, size), Image.Resampling.LANCZOS)
    except Exception:
        # Fallback to solid color if URL fails
        avatar = Image.new('RGBA', (size, size), image_url_or_color)
        
    # Create circular mask for avatar
    mask = Image.new('L', (size, size), 0)
    ImageDraw.Draw(mask).ellipse([0, 0, size, size], fill=255)
    
    # Composite avatar into a transparent layer
    avatar_layer = Image.new('RGBA', (img_size, img_size), (0, 0, 0, 0))
    avatar_layer.paste(avatar, (pad, pad), mask=mask)
    
    # Draw white border
    bd = ImageDraw.Draw(avatar_layer)
    bd.ellipse(shadow_bbox, outline=(255, 255, 255, 255), width=border_w)
    
    # Combine
    out = Image.new('RGBA', (img_size, img_size), (0, 0, 0, 0))
    out.paste(shadow_layer, (0, 0))
    out.paste(avatar_layer, (0, 0), mask=avatar_layer)
    
    return out

def _create_tooltip_ribbon(w_px=300, h_px=80, ptr_w=40, ptr_h=25, corner_r=20, shadow_blur=15):
    """
    Generates a tooltip-shaped ribbon with a vertical gradient and drop shadow.
    """
    pad = 40
    img_w = w_px + pad * 2
    img_h = h_px + ptr_h + pad * 2
    
    # Shadow layer
    shadow = Image.new('RGBA', (img_w, img_h), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    
    shape_rect = [pad, pad + ptr_h, pad + w_px, pad + ptr_h + h_px]
    ptr_poly = [
        (img_w // 2 - ptr_w // 2, pad + ptr_h),
        (img_w // 2, pad),
        (img_w // 2 + ptr_w // 2, pad + ptr_h)
    ]
    
    sd.rounded_rectangle(shape_rect, radius=corner_r, fill=(0, 0, 0, 100))
    sd.polygon(ptr_poly, fill=(0, 0, 0, 100))
    shadow = shadow.filter(ImageFilter.GaussianBlur(shadow_blur))
    
    # Mask for gradient
    mask = Image.new('L', (img_w, img_h), 0)
    md = ImageDraw.Draw(mask)
    md.rounded_rectangle(shape_rect, radius=corner_r, fill=255)
    md.polygon(ptr_poly, fill=255)
    
    # Gradient layer (dark purple)
    grad = Image.new('RGBA', (img_w, img_h))
    c1, c2 = (45, 10, 89, 255), (80, 25, 140, 255)
    
    for y in range(img_h):
        ratio = y / img_h
        r = int(c1[0] + (c2[0] - c1[0]) * ratio)
        g = int(c1[1] + (c2[1] - c1[1]) * ratio)
        b = int(c1[2] + (c2[2] - c1[2]) * ratio)
        ImageDraw.Draw(grad).line([(0, y), (img_w, y)], fill=(r, g, b, 255))
        
    # Composite
    out = Image.new('RGBA', (img_w, img_h), (0, 0, 0, 0))
    out.paste(shadow, (0, 0))
    out.paste(grad, (0, 0), mask=mask)
    
    return out

def create_slide(
    output_pptx_path: str,
    title_text: str = "Our Team",
    **kwargs,
) -> str:
    """
    Creates a PPTX file reproducing the 'Straddling Profile Tooltips' design style.
    """
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6]) # blank layout
    
    # --- Background ---
    # Top dark purple header
    bg_top = slide.shapes.add_shape(
        1, # rectangle
        0, 0, prs.slide_width, Inches(3.2)
    )
    bg_top.fill.solid()
    bg_top.fill.fore_color.rgb = RGBColor(45, 10, 89)
    bg_top.line.fill.background()
    
    # --- Slide Title ---
    title_box = slide.shapes.add_textbox(Inches(4), Inches(0.4), Inches(5.33), Inches(0.8))
    tf = title_box.text_frame
    p = tf.paragraphs[0]
    p.text = title_text
    p.alignment = PP_ALIGN.CENTER
    p.font.size = Pt(44)
    p.font.bold = True
    p.font.name = "Georgia"
    p.font.color.rgb = RGBColor(255, 255, 255)
    
    # Flanking accent lines for title
    line_y = Inches(0.8)
    line_left = slide.shapes.add_shape(9, Inches(3.5), line_y, Inches(1.5), Pt(1))
    line_left.fill.solid()
    line_left.fill.fore_color.rgb = RGBColor(255, 255, 255)
    line_left.line.color.rgb = RGBColor(255, 255, 255)
    
    line_right = slide.shapes.add_shape(9, Inches(8.33), line_y, Inches(1.5), Pt(1))
    line_right.fill.solid()
    line_right.fill.fore_color.rgb = RGBColor(255, 255, 255)
    line_right.line.color.rgb = RGBColor(255, 255, 255)
    
    # --- Team Members Data ---
    members = [
        {"name": "James Doe", "role": "CEO", "url": "https://images.unsplash.com/photo-1560250097-0b93528c311a?auto=format&fit=crop&w=400&q=80", "color": (100, 150, 200)},
        {"name": "Robert Smith", "role": "CTO", "url": "https://images.unsplash.com/photo-1519085360753-af0119f7cbe7?auto=format&fit=crop&w=400&q=80", "color": (200, 100, 150)},
        {"name": "Jane Adams", "role": "CFO", "url": "https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?auto=format&fit=crop&w=400&q=80", "color": (150, 200, 100)}
    ]
    
    # Positioning logic
    num_members = len(members)
    col_width = prs.slide_width / num_members
    
    avatar_w_inches = 2.4
    ribbon_w_inches = 2.4
    ribbon_h_inches = 0.95
    
    for i, member in enumerate(members):
        center_x = (i * col_width) + (col_width / 2)
        
        # 1. Generate & Insert Circular Avatar
        # We straddle the intersection (y = 3.2). So top is 3.2 - (avatar_h/2)
        avatar_img = _create_avatar_image(member['url'])
        avatar_path = f"tmp_avatar_{i}.png"
        avatar_img.save(avatar_path)
        
        # The image has padding (40px on all sides of a 300px circle -> 380px total)
        # So visual width = avatar_w_inches * (300/380)
        actual_img_w = avatar_w_inches * (380/300)
        slide.shapes.add_picture(
            avatar_path, 
            center_x - actual_img_w/2, 
            Inches(3.2) - actual_img_w/2, 
            width=actual_img_w
        )
        os.remove(avatar_path)
        
        # 2. Generate & Insert Tooltip Ribbon
        ribbon_img = _create_tooltip_ribbon()
        ribbon_path = f"tmp_ribbon_{i}.png"
        ribbon_img.save(ribbon_path)
        
        # Similar padding logic for the ribbon (width=300, pad=40 -> 380)
        actual_rib_w = ribbon_w_inches * (380/300)
        actual_rib_h = ribbon_h_inches * (205/105) # approx heights with padding
        
        ribbon_y = Inches(3.2) + (avatar_w_inches / 2.1) # snug just under the circle
        
        slide.shapes.add_picture(
            ribbon_path, 
            center_x - actual_rib_w/2, 
            ribbon_y, 
            width=actual_rib_w
        )
        os.remove(ribbon_path)
        
        # 3. Add Editable Name Text overlaying the ribbon
        name_box = slide.shapes.add_textbox(
            center_x - Inches(1.2), 
            ribbon_y + Inches(0.55), # Offset past the shadow and pointer
            Inches(2.4), 
            Inches(0.4)
        )
        tf_name = name_box.text_frame
        p_name = tf_name.paragraphs[0]
        p_name.text = member['name'].upper()
        p_name.alignment = PP_ALIGN.CENTER
        p_name.font.size = Pt(14)
        p_name.font.bold = True
        p_name.font.color.rgb = RGBColor(255, 255, 255)
        
        # 4. Add Description Text below
        desc_box = slide.shapes.add_textbox(
            center_x - Inches(1.5), 
            ribbon_y + Inches(1.3), 
            Inches(3.0), 
            Inches(0.8)
        )
        tf_desc = desc_box.text_frame
        tf_desc.word_wrap = True
        p_desc = tf_desc.paragraphs[0]
        p_desc.text = "Lorem ipsum dolor sit amet\nLorem ipsum dolor sit amet"
        p_desc.alignment = PP_ALIGN.CENTER
        p_desc.font.size = Pt(11)
        p_desc.font.color.rgb = RGBColor(80, 80, 80)
        
        # 5. Add decorative dots
        dot_spacing = 0.15
        dot_y = ribbon_y + Inches(2.0)
        for d in range(-1, 2):
            dot = slide.shapes.add_shape(
                9, # oval
                center_x + (d * Inches(dot_spacing)) - Inches(0.04), 
                dot_y, 
                Inches(0.08), 
                Inches(0.08)
            )
            dot.fill.background() # transparent interior
            dot.line.color.rgb = RGBColor(100, 100, 100)
            dot.line.width = Pt(1)

    prs.save(output_pptx_path)
    return output_pptx_path
