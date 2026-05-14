import os
import io
import urllib.request
from typing import List, Tuple
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from PIL import Image, ImageDraw, ImageFilter, ImageFont

def create_slide(
    output_pptx_path: str,
    title_text: str = "Table of Contents",
    menu_items: List[str] = None,
    bg_image_url: str = "https://images.unsplash.com/photo-1600607688969-a5bfcd646154?q=80&w=1920&auto=format&fit=crop", # Beautiful interior
    **kwargs,
) -> str:
    """
    Creates a PPTX file reproducing the Glassmorphic "Lens Bubble" Menu overlay.
    """
    if menu_items is None:
        menu_items = [
            "Our Mission", "Problem", "Solution", 
            "Market Potential", "Business Model", "Our Team"
        ]

    # --- 1. PPTX Setup ---
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6]) # Blank layout
    
    canvas_w, canvas_h = 1920, 1080 # 16:9 equivalent for PIL
    
    # --- 2. Acquire and Prepare Background Image ---
    try:
        req = urllib.request.Request(bg_image_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as url:
            bg_data = io.BytesIO(url.read())
        bg_image = Image.open(bg_data).convert("RGBA")
        
        # Crop and resize to exactly 1920x1080
        bg_ratio = bg_image.width / bg_image.height
        target_ratio = canvas_w / canvas_h
        if bg_ratio > target_ratio:
            new_w = int(bg_image.height * target_ratio)
            left = (bg_image.width - new_w) // 2
            bg_image = bg_image.crop((left, 0, left + new_w, bg_image.height))
        else:
            new_h = int(bg_image.width / target_ratio)
            top = (bg_image.height - new_h) // 2
            bg_image = bg_image.crop((0, top, bg_image.width, top + new_h))
        bg_image = bg_image.resize((canvas_w, canvas_h), Image.Resampling.LANCZOS)
    except Exception as e:
        print(f"Failed to download image, using fallback gradient. Error: {e}")
        bg_image = Image.new("RGBA", (canvas_w, canvas_h))
        draw = ImageDraw.Draw(bg_image)
        for y in range(canvas_h):
            r = int(20 + (y / canvas_h) * 40)
            g = int(30 + (y / canvas_h) * 50)
            b = int(20 + (y / canvas_h) * 20)
            draw.line([(0, y), (canvas_w, y)], fill=(r, g, b, 255))

    # --- 3. Create the Blurred "Glass" Base ---
    # Heavy blur for the glassmorphism effect
    bg_blurred = bg_image.filter(ImageFilter.GaussianBlur(radius=25))
    
    # --- 4. Define Bubble Geometry ---
    radius = 160
    centers = []
    # Calculate grid for bubbles (2 rows)
    num_items = len(menu_items)
    cols = (num_items + 1) // 2  # Up to 3 per row for 6 items
    
    y_start_row1 = 450
    y_start_row2 = 800
    
    row1_items = menu_items[:cols]
    row2_items = menu_items[cols:]
    
    def calculate_x_centers(num_in_row):
        spacing = canvas_w / (num_in_row + 1)
        return [int(spacing * (i + 1)) for i in range(num_in_row)]
        
    for cx in calculate_x_centers(len(row1_items)):
        centers.append((cx, y_start_row1))
    for cx in calculate_x_centers(len(row2_items)):
        centers.append((cx, y_start_row2))

    # --- 5. Generate Glassmorphism Overlay (Using PIL Alpha Compositing) ---
    # Create an empty transparent canvas
    overlay = Image.new("RGBA", (canvas_w, canvas_h), (0, 0, 0, 0))
    
    for cx, cy in centers:
        # Bounding box for the circle
        bbox = [cx - radius, cy - radius, cx + radius, cy + radius]
        
        # A. Create a circular mask
        mask = Image.new("L", (canvas_w, canvas_h), 0)
        ImageDraw.Draw(mask).ellipse(bbox, fill=255)
        
        # B. Paste the blurred background into the transparent overlay using the mask
        overlay.paste(bg_blurred, (0, 0), mask)
        
        # C. Add Frosted Tint and Stroke
        tint_layer = Image.new("RGBA", (canvas_w, canvas_h), (0, 0, 0, 0))
        tint_draw = ImageDraw.Draw(tint_layer)
        # White overlay with 15% opacity to brighten the frosted glass
        tint_draw.ellipse(bbox, fill=(255, 255, 255, 40))
        # Crisp white border (1px)
        tint_draw.ellipse(bbox, outline=(255, 255, 255, 200), width=2)
        
        # Composite tint over the bubble
        overlay = Image.alpha_composite(overlay, tint_layer)

    # Save layers to disk temporarily
    bg_path = "temp_sharp_bg.png"
    overlay_path = "temp_glass_overlay.png"
    bg_image.save(bg_path)
    overlay.save(overlay_path)

    # --- 6. Assemble PPTX Layers ---
    # Layer 1: Sharp background
    slide.shapes.add_picture(bg_path, 0, 0, width=Inches(13.333), height=Inches(7.5))
    
    # Layer 2: Frosted glass circles
    slide.shapes.add_picture(overlay_path, 0, 0, width=Inches(13.333), height=Inches(7.5))

    # --- 7. Add Text Layout (`python-pptx`) ---
    
    # Main Title
    title_box = slide.shapes.add_textbox(Inches(0), Inches(0.5), Inches(13.333), Inches(1.5))
    tf = title_box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    p.text = title_text
    p.font.size = Pt(64)
    p.font.color.rgb = RGBColor(255, 255, 255)
    p.font.name = "Arial"
    p.font.bold = True

    # Section Bubbles Text
    for i, (cx, cy) in enumerate(centers):
        # Convert pixel coordinates to inches
        x_inch = (cx / canvas_w) * 13.333
        y_inch = (cy / canvas_h) * 7.5
        
        # Textbox dimensions
        tb_w, tb_h = Inches(2.5), Inches(1.0)
        tb_x = x_inch - (tb_w / 2)
        tb_y = y_inch - (tb_h / 2)
        
        txt_box = slide.shapes.add_textbox(tb_x, tb_y, tb_w, tb_h)
        tf = txt_box.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        p.text = menu_items[i]
        p.font.size = Pt(22)
        p.font.color.rgb = RGBColor(255, 255, 255)
        p.font.name = "Arial"
        p.font.bold = True

    # --- Cleanup & Save ---
    prs.save(output_pptx_path)
    if os.path.exists(bg_path): os.remove(bg_path)
    if os.path.exists(overlay_path): os.remove(overlay_path)
    
    return output_pptx_path
