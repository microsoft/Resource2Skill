def create_slide(
    output_pptx_path: str,
    title_text: str = "Sales of Apple Products in India",
    body_text: str = "", # Not strictly used in this layout
    bg_palette: str = "iphone,technology", 
    accent_color: tuple = (230, 230, 230),  # Light grey for blocks
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the "Vertical Icon-Block Agenda" visual effect.
    """
    import os
    import urllib.request
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    from pptx.enum.shapes import MSO_SHAPE
    from pptx.enum.text import PP_ALIGN
    from PIL import Image, ImageDraw

    # === Presentation Setup ===
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6])  # Blank slide

    # === Helper Functions ===
    def hex_to_rgb(hex_code):
        hex_code = hex_code.lstrip('#')
        return tuple(int(hex_code[i:i+2], 16) for i in (0, 2, 4))

    # --- Generate Local Icons using PIL ---
    # To replicate downloading icons from Noun Project, we generate minimalist icons dynamically.
    icon_color = (60, 60, 60, 255) # Dark Grey
    
    def create_globe_icon(path):
        img = Image.new('RGBA', (200, 200), (255, 255, 255, 0))
        draw = ImageDraw.Draw(img)
        draw.ellipse([20, 20, 180, 180], outline=icon_color, width=12)
        draw.ellipse([60, 20, 140, 180], outline=icon_color, width=12)
        draw.line([20, 100, 180, 100], fill=icon_color, width=12)
        img.save(path)
        
    def create_device_icon(path):
        img = Image.new('RGBA', (200, 200), (255, 255, 255, 0))
        draw = ImageDraw.Draw(img)
        draw.rounded_rectangle([50, 10, 150, 190], radius=15, outline=icon_color, width=12)
        draw.ellipse([90, 160, 110, 180], outline=icon_color, width=8) # Home button
        img.save(path)
        
    def create_chart_icon(path):
        img = Image.new('RGBA', (200, 200), (255, 255, 255, 0))
        draw = ImageDraw.Draw(img)
        # Axes
        draw.line([20, 20, 20, 180], fill=icon_color, width=12)
        draw.line([20, 180, 180, 180], fill=icon_color, width=12)
        # Bars
        draw.rectangle([40, 120, 70, 180], fill=icon_color)
        draw.rectangle([90, 80, 120, 180], fill=icon_color)
        draw.rectangle([140, 40, 170, 180], fill=icon_color)
        img.save(path)

    globe_path = "temp_icon_globe.png"
    device_path = "temp_icon_device.png"
    chart_path = "temp_icon_chart.png"
    create_globe_icon(globe_path)
    create_device_icon(device_path)
    create_chart_icon(chart_path)

    # === Layer 1: Background Elements ===
    bg_img_path = "temp_bg.jpg"
    try:
        # Fetch an aesthetic tech/phone background
        url = f"https://source.unsplash.com/featured/1600x900/?{bg_palette}"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            with open(bg_img_path, 'wb') as f:
                f.write(response.read())
        
        # Apply fading effect to image via PIL to make text readable
        img = Image.open(bg_img_path).convert("RGBA")
        overlay = Image.new('RGBA', img.size, (255, 255, 255, 120)) # White tint
        img = Image.alpha_composite(img, overlay)
        img.convert("RGB").save(bg_img_path)
        
        slide.shapes.add_picture(bg_img_path, 0, 0, width=Inches(13.333), height=Inches(7.5))
    except Exception as e:
        # Fallback background
        bg_shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
        bg_shape.fill.solid()
        bg_shape.fill.fore_color.rgb = RGBColor(240, 240, 245)
        bg_shape.line.fill.background()

    # === Layer 2: Main Title ===
    # Add floating title label similar to the transcript setup
    title_box = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1), Inches(0.8), Inches(6), Inches(0.8)
    )
    title_box.fill.solid()
    title_box.fill.fore_color.rgb = RGBColor(255, 255, 255)
    title_box.line.fill.background()
    
    # Text for Title
    tf = title_box.text_frame
    tf.clear()
    p = tf.paragraphs[0]
    p.text = title_text
    p.font.size = Pt(24)
    p.font.bold = True
    p.font.color.rgb = RGBColor(60, 60, 60)
    p.alignment = PP_ALIGN.CENTER

    # === Layer 3: Separator Agenda Blocks ===
    # Configuration for blocks
    block_width = Inches(5.5)
    block_height = Inches(1.3)
    start_x = Inches(7.0)
    start_y = Inches(2.2)
    spacing = Inches(1.6) # Distance from top of one block to top of next

    menu_items = [
        {"title": "Geography", "icon": globe_path},
        {"title": "Products", "icon": device_path},
        {"title": "Sales (Online vs Store)", "icon": chart_path}
    ]

    for index, item in enumerate(menu_items):
        current_y = start_y + (index * spacing)
        
        # 1. The Block (Grey Background)
        block = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE, start_x, current_y, block_width, block_height
        )
        block.fill.solid()
        block.fill.fore_color.rgb = RGBColor(*accent_color)
        block.line.fill.background() # No border
        
        # 2. The Icon
        # Place icon inside the block on the left side
        icon_size = Inches(0.8)
        icon_x = start_x + Inches(0.3)
        icon_y = current_y + Inches(0.25)
        slide.shapes.add_picture(item["icon"], icon_x, icon_y, width=icon_size, height=icon_size)
        
        # 3. The Text
        # Place text next to the icon
        tx_box = slide.shapes.add_textbox(
            icon_x + icon_size + Inches(0.2), 
            current_y + Inches(0.25), 
            block_width - icon_size - Inches(0.7), 
            Inches(0.8)
        )
        tf = tx_box.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = item["title"]
        p.font.size = Pt(28)
        p.font.color.rgb = RGBColor(*icon_color) # Match icon color
        # Vertical centering within text frame
        tx_box.text_frame.vertical_anchor = MSO_SHAPE.RECTANGLE 

    # === Cleanup ===
    prs.save(output_pptx_path)
    for path in [globe_path, device_path, chart_path, bg_img_path]:
        if os.path.exists(path):
            os.remove(path)
            
    return output_pptx_path
