def create_slide(
    output_pptx_path: str,
    title_text: str = "Rotating Carousel Morph",
    bg_palette: str = "restaurant",
    accent_color: tuple = (212, 175, 55),  # Gold
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the 'Off-Center Radial Carousel Morph' visual effect.
    Generates 3 slides. Applying the 'Morph' transition in PPTX will animate them.
    """
    import math
    import io
    import urllib.request
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    from pptx.enum.text import PP_ALIGN
    from PIL import Image, ImageDraw, ImageFont

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    # Carousel Configuration
    items_data = [
        {"title": "Signature Ramen", "subtitle": "Rich pork broth with chashu", "color": (200, 80, 50)},
        {"title": "Spicy Pumpkin Soup", "subtitle": "Warm and creamy autumn delight", "color": (220, 130, 30)},
        {"title": "Roasted Potatoes", "subtitle": "Herb-infused baby potatoes", "color": (180, 160, 80)},
    ]
    
    cx = Inches(-2.0)          # Center X of the wheel (off-screen left)
    cy = prs.slide_height / 2  # Center Y of the wheel (middle vertical)
    radius = Inches(5.5)       # Radius of the wheel
    angle_step = 40            # Degrees between each item

    # --- Helper: Generate Background Image ---
    bg_stream = io.BytesIO()
    try:
        url = "https://images.unsplash.com/photo-1577219491135-ce391730fb2c?q=80&w=1920&auto=format&fit=crop"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            img = Image.open(response).convert("RGB")
            # Darken background slightly for contrast
            dark_layer = Image.new("RGBA", img.size, (0, 0, 0, 128))
            img.paste(dark_layer, (0,0), dark_layer)
            img.save(bg_stream, format="JPEG")
    except Exception:
        # Fallback background
        img = Image.new("RGB", (1920, 1080), (30, 30, 35))
        img.save(bg_stream, format="JPEG")
    bg_stream.seek(0)

    # --- Helper: Generate Semi-Transparent Guide Arc ---
    # We create a slide-sized transparent PNG and draw the arc on it
    arc_stream = io.BytesIO()
    arc_img = Image.new("RGBA", (int(prs.slide_width), int(prs.slide_height)), (0, 0, 0, 0))
    draw = ImageDraw.Draw(arc_img)
    
    # Calculate bounding box for the arc in EMU/Pixels (1 Inch = 914400 EMU. We use approx 96 DPI for PIL)
    dpi = 96
    pil_cx = -2.0 * dpi
    pil_cy = 7.5 / 2 * dpi
    pil_r = 5.5 * dpi
    line_width = int(0.2 * dpi)
    
    bbox = [pil_cx - pil_r, pil_cy - pil_r, pil_cx + pil_r, pil_cy + pil_r]
    draw.arc(bbox, start=-90, end=90, fill=(255, 255, 255, 80), width=line_width) # 30% opacity white arc
    arc_img.save(arc_stream, format="PNG")
    arc_stream.seek(0)

    # --- Helper: Generate Item "Plates" ---
    plate_streams = []
    plate_size = int(2.5 * dpi)
    for item in items_data:
        p_stream = io.BytesIO()
        p_img = Image.new("RGBA", (plate_size, plate_size), (0, 0, 0, 0))
        p_draw = ImageDraw.Draw(p_img)
        # Draw outer plate (white)
        p_draw.ellipse([0, 0, plate_size, plate_size], fill=(240, 240, 240, 255))
        # Draw inner food color
        padding = int(0.15 * dpi)
        p_draw.ellipse([padding, padding, plate_size-padding, plate_size-padding], fill=item["color"])
        p_img.save(p_stream, format="PNG")
        p_stream.seek(0)
        plate_streams.append(p_stream)

    # --- Loop: Generate 3 Slides (Animation States) ---
    for slide_idx in range(len(items_data)):
        slide = prs.slides.add_slide(prs.slide_layouts[6])
        
        # 1. Background
        slide.shapes.add_picture(bg_stream, 0, 0, prs.slide_width, prs.slide_height)
        
        # 2. Guide Arc
        slide.shapes.add_picture(arc_stream, 0, 0, prs.slide_width, prs.slide_height)
        
        # 3. Place Items based on math
        for item_idx, item in enumerate(items_data):
            # Calculate dynamic angle: 
            # When item_idx == slide_idx, angle is 0 (focal point, horizontal right)
            # When item_idx > slide_idx, angle is positive (lower down the arc)
            # When item_idx < slide_idx, angle is negative (higher up the arc)
            relative_position = item_idx - slide_idx
            angle_deg = relative_position * angle_step
            angle_rad = math.radians(angle_deg)
            
            # Position Math (Y is positive downwards in screen coords)
            x = cx + radius * math.cos(angle_rad)
            y = cy + radius * math.sin(angle_rad)
            
            # Adjust size based on focus
            is_focus = (relative_position == 0)
            current_size = Inches(2.8) if is_focus else Inches(2.0)
            
            # Center the image on the calculated coordinate
            img_x = x - (current_size / 2)
            img_y = y - (current_size / 2)
            
            # Insert plate image
            plate_streams[item_idx].seek(0)
            pic = slide.shapes.add_picture(plate_streams[item_idx], img_x, img_y, current_size, current_size)
            # Give consistent name so PPTX Morph knows they are the same object across slides
            pic.name = f"Carousel_Item_{item_idx}"
            
            # 4. Add Text for the in-focus item
            if is_focus:
                tx_left = x + (current_size / 2) + Inches(0.5)
                tx_top = y - Inches(0.5)
                tx_width = Inches(5)
                tx_height = Inches(2)
                
                tb = slide.shapes.add_textbox(tx_left, tx_top, tx_width, tx_height)
                tf = tb.text_frame
                tf.word_wrap = True
                
                p = tf.add_paragraph()
                p.text = item["title"]
                p.font.size = Pt(36)
                p.font.bold = True
                p.font.color.rgb = RGBColor(*accent_color)
                
                p2 = tf.add_paragraph()
                p2.text = item["subtitle"]
                p2.font.size = Pt(20)
                p2.font.color.rgb = RGBColor(255, 255, 255)

    prs.save(output_pptx_path)
    return output_pptx_path
