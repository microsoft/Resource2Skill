import os
import urllib.request
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.text import MSO_ANCHOR
from pptx.oxml import parse_xml
from pptx.oxml.ns import nsdecls
from PIL import Image, ImageDraw

def create_slide(
    output_pptx_path: str,
    title_text: str = "Our Team",
    body_text: str = "",
    bg_palette: str = "business",
    accent_color: tuple = (255, 204, 0),
    **kwargs,
) -> str:
    """
    Creates an Accordion Image Slider slide. 
    This generates a single state of the accordion (e.g., the 3rd person is active).
    """
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6]) # Blank layout

    # Inject Morph Transition XML
    morph_xml = f'<p:transition {nsdecls("p")} spd="slow"><p:morph/></p:transition>'
    slide.element.insert(-1, parse_xml(morph_xml))

    # --- Data Definition ---
    team_members = [
        {"name": "EVA", "role": "Finance", "seed": "11"},
        {"name": "JACOB", "role": "Admin", "seed": "12"},
        {"name": "EMILY", "role": "Operations", "seed": "13"},
        {"name": "SARAH", "role": "Manager", "seed": "14"}, # Active
        {"name": "LAUREN", "role": "Design", "seed": "15"},
        {"name": "MIKE", "role": "Developer", "seed": "16"},
        {"name": "ANGIE", "role": "HR", "seed": "17"},
    ]
    active_index = 3 # Sarah is expanded

    # --- Background Generation ---
    bg_path = "temp_bg_gradient.png"
    bg_img = Image.new('RGB', (1920, 1080))
    draw = ImageDraw.Draw(bg_img)
    # Light subtle blue/grey gradient
    color_top = (245, 247, 250)
    color_bottom = (220, 225, 230)
    for y in range(1080):
        r = int(color_top[0] + (color_bottom[0] - color_top[0]) * (y / 1080))
        g = int(color_top[1] + (color_bottom[1] - color_top[1]) * (y / 1080))
        b = int(color_top[2] + (color_bottom[2] - color_top[2]) * (y / 1080))
        draw.line([(0, y), (1920, y)], fill=(r, g, b))
    bg_img.save(bg_path)
    slide.shapes.add_picture(bg_path, 0, 0, prs.slide_width, prs.slide_height)

    # --- Add Slide Title ---
    title_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.3), Inches(5), Inches(1))
    tf = title_box.text_frame
    p = tf.paragraphs[0]
    p.text = title_text
    p.font.size = Pt(44)
    p.font.bold = True
    p.font.color.rgb = RGBColor(40, 40, 40)

    # --- Layout Math ---
    slide_w = 13.333
    slide_h = 7.5
    
    # Dimensions in inches
    active_w = 4.5
    active_h = 5.5
    inactive_w = 0.8
    inactive_h = 4.8
    
    y_center = slide_h / 2
    
    total_items = len(team_members)
    total_content_w = active_w + ((total_items - 1) * inactive_w)
    
    # Available space for gaps and margins
    available_space = slide_w - total_content_w
    gap = available_space / (total_items + 1)
    
    current_x = gap

    # --- Helper: Download, Crop, and Add Shadow Overlay ---
    def process_image(seed, target_w_inch, target_h_inch, dpi=150):
        url = f"https://picsum.photos/seed/{seed}/800/800"
        temp_path = f"temp_img_{seed}.png"
        
        target_w_px = int(target_w_inch * dpi)
        target_h_px = int(target_h_inch * dpi)
        
        try:
            urllib.request.urlretrieve(url, temp_path)
            img = Image.open(temp_path).convert("RGBA")
        except Exception:
            # Fallback to solid color block
            img = Image.new("RGBA", (800, 800), (100, 120, 150, 255))
            
        # Center crop
        img_ratio = img.width / img.height
        target_ratio = target_w_px / target_h_px
        if img_ratio > target_ratio:
            new_w = int(target_ratio * img.height)
            left = (img.width - new_w) // 2
            img = img.crop((left, 0, left + new_w, img.height))
        else:
            new_h = int(img.width / target_ratio)
            top = (img.height - new_h) // 2
            img = img.crop((0, top, img.width, top + new_h))
            
        img = img.resize((target_w_px, target_h_px), Image.Resampling.LANCZOS)
        
        # Add gradient overlay at bottom for text readability
        overlay = Image.new('RGBA', img.size, (0,0,0,0))
        draw_ov = ImageDraw.Draw(overlay)
        start_y = int(target_h_px * 0.5) # start fading from 50% down
        for y in range(start_y, target_h_px):
            alpha = int(255 * 0.85 * ((y - start_y) / (target_h_px - start_y)))
            draw_ov.line([(0, y), (target_w_px, y)], fill=(0, 0, 0, alpha))
            
        final_img = Image.alpha_composite(img, overlay)
        final_img.save(temp_path, "PNG")
        return temp_path

    # --- Render Accordion Elements ---
    for i, member in enumerate(team_members):
        is_active = (i == active_index)
        
        w = active_w if is_active else inactive_w
        h = active_h if is_active else inactive_h
        y = y_center - (h / 2)
        
        # Process and insert image
        img_path = process_image(member['seed'], w, h)
        slide.shapes.add_picture(img_path, Inches(current_x), Inches(y), Inches(w), Inches(h))
        
        if is_active:
            # Horizontal Text Box for Active Member
            text_x = current_x + 0.2
            text_y = y + h - 1.0
            tb = slide.shapes.add_textbox(Inches(text_x), Inches(text_y), Inches(w - 0.4), Inches(1))
            tf = tb.text_frame
            
            p1 = tf.paragraphs[0]
            p1.text = member['name']
            p1.font.size = Pt(28)
            p1.font.bold = True
            p1.font.color.rgb = RGBColor(255, 255, 255)
            
            p2 = tf.add_paragraph()
            p2.text = member['role']
            p2.font.size = Pt(14)
            p2.font.color.rgb = RGBColor(220, 220, 220)
            
        else:
            # Vertical Rotated Text Box for Inactive Member
            # We create a box where Width = strip Height, Height = strip Width
            # Center it exactly over the strip, then rotate -90 degrees
            cx = current_x + (w / 2)
            cy = y + (h / 2)
            
            tb_w = h
            tb_h = w
            tb_x = cx - (tb_w / 2)
            tb_y = cy - (tb_h / 2)
            
            tb = slide.shapes.add_textbox(Inches(tb_x), Inches(tb_y), Inches(tb_w), Inches(tb_h))
            tb.rotation = -90.0
            
            tf = tb.text_frame
            tf.vertical_anchor = MSO_ANCHOR.MIDDLE
            tf.margin_left = Inches(0.2) # Adds padding from the bottom of the strip due to rotation
            
            p = tf.paragraphs[0]
            p.text = member['name']
            p.alignment = PP_ALIGN.LEFT # Aligns to the "bottom" of the unrotated box
            p.font.size = Pt(16)
            p.font.bold = True
            p.font.color.rgb = RGBColor(255, 255, 255)
            
        current_x += w + gap

    # Cleanup temp images
    if os.path.exists(bg_path): os.remove(bg_path)
    for m in team_members:
        tmp = f"temp_img_{m['seed']}.png"
        if os.path.exists(tmp): os.remove(tmp)

    prs.save(output_pptx_path)
    return output_pptx_path
