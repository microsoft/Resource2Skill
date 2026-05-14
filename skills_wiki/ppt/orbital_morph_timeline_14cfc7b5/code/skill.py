def create_slide(
    output_pptx_path: str,
    title_text: str = "GoTech 发展历程",
    body_text: str = "The History of GoTech",
    bg_palette: str = "technology",
    accent_color: tuple = (242, 192, 86),  # Golden accent
    **kwargs,
) -> str:
    """
    Creates an "Orbital Morph Timeline" presentation.
    Generates procedural starry backgrounds and planet images, 
    calculates orbital paths for text nodes, and injects Morph transitions.
    """
    import math
    import random
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    from pptx.enum.text import PP_ALIGN
    from pptx.oxml import OxmlElement
    from PIL import Image, ImageDraw, ImageFilter
    import os

    # ---------------------------------------------------------
    # Helper 1: Generate Procedural Assets (No network required)
    # ---------------------------------------------------------
    def generate_assets():
        bg_path = "temp_space_bg.png"
        planet_path = "temp_planet.png"
        
        # 1. Starry Space Background
        bg_img = Image.new('RGB', (1920, 1080), (10, 14, 25))
        draw_bg = ImageDraw.Draw(bg_img)
        # Add a subtle nebula glow
        glow = Image.new('RGB', (1920, 1080), (0, 0, 0))
        glow_draw = ImageDraw.Draw(glow)
        glow_draw.ellipse((400, 200, 1500, 800), fill=(20, 40, 80))
        glow = glow.filter(ImageFilter.GaussianBlur(150))
        bg_img = Image.blend(bg_img, glow, 0.5)
        # Add stars
        for _ in range(300):
            x, y = random.randint(0, 1920), random.randint(0, 1080)
            r = random.randint(1, 3)
            draw_bg.ellipse((x, y, x+r, y+r), fill=(255, 255, 255))
        bg_img.save(bg_path)

        # 2. Planet Image (Blue gradient circle with transparent background)
        p_size = 1000
        p_img = Image.new('RGBA', (p_size, p_size), (0, 0, 0, 0))
        p_draw = ImageDraw.Draw(p_img)
        # Base sphere
        p_draw.ellipse((10, 10, p_size-10, p_size-10), fill=(30, 80, 160, 255))
        # Highlight/Shadow for 3D effect
        shadow = Image.new('RGBA', (p_size, p_size), (0, 0, 0, 0))
        s_draw = ImageDraw.Draw(shadow)
        s_draw.ellipse((10, 10, p_size-10, p_size-10), fill=(0, 0, 0, 200))
        s_draw.ellipse((50, 50, p_size+200, p_size+200), fill=(0, 0, 0, 0)) # subtract
        shadow = shadow.filter(ImageFilter.GaussianBlur(30))
        p_img.alpha_composite(shadow)
        p_img.save(planet_path)
        
        return bg_path, planet_path

    # ---------------------------------------------------------
    # Helper 2: Inject Morph Transition via lxml
    # ---------------------------------------------------------
    def apply_morph_transition(slide):
        # Insert <p:transition><p15:morph/></p:transition> into slide XML
        transition = OxmlElement('p:transition')
        transition.set('spd', 'slow')
        morph = OxmlElement('p15:morph')
        morph.set('xmlns:p15', 'http://schemas.microsoft.com/office/powerpoint/2012/main')
        morph.set('prst', 'morph')
        transition.append(morph)
        # Insert right after slide properties
        slide.element.insert(2, transition)

    # ---------------------------------------------------------
    # Main Presentation Logic
    # ---------------------------------------------------------
    bg_path, planet_path = generate_assets()

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    # Timeline Data
    nodes = [
        {"year": "1995年", "title": f"{title_text} 成立", "desc": "公司成立，发布首个互联网产品，开始探索未知领域。"},
        {"year": "2001年", "title": "推出电子商务平台", "desc": "允许用户在线购买各种商品和服务，平台获得了巨大的成功。"},
        {"year": "2008年", "title": "推出移动应用", "desc": "随着移动设备的普及，推出了一系列移动端社交与游戏应用。"},
        {"year": "2015年", "title": "进军人工智能领域", "desc": "开始大力投资AI技术研发，推出智能语音助手与家居设备。"}
    ]

    # Orbital Geometry Settings
    pivot_x = Inches(11.5)  # Planet center X (bottom right)
    pivot_y = Inches(6.5)   # Planet center Y 
    planet_radius = Inches(4.5)
    orbit_radius = Inches(6.0) # Distance from center to text box
    rotation_step = 60         # Degrees to rotate between slides
    
    # Create a slide for each node to act as the "active" frame
    for slide_idx in range(len(nodes)):
        slide_layout = prs.slide_layouts[6] # Blank
        slide = prs.slides.add_slide(slide_layout)
        
        # Apply morph to all slides except the first
        if slide_idx > 0:
            apply_morph_transition(slide)

        # 1. Add Background
        slide.shapes.add_picture(bg_path, 0, 0, prs.slide_width, prs.slide_height)

        # 2. Add Planet
        # The planet itself needs to rotate physically across slides
        planet_shape = slide.shapes.add_picture(
            planet_path, 
            pivot_x - planet_radius, 
            pivot_y - planet_radius, 
            planet_radius * 2, 
            planet_radius * 2
        )
        planet_shape.name = "!!Planet" # '!!' forces strict morph tracking
        # Planet rotates counter-clockwise as we progress
        planet_shape.rotation = slide_idx * -rotation_step 

        # 3. Add Orbiting Text Nodes
        for node_idx, node_data in enumerate(nodes):
            # Calculate angle relative to the active slide
            # If node_idx == slide_idx, angle is 0 (placed directly to the left)
            # If node_idx > slide_idx, angle is positive (placed higher up)
            angle_deg = (node_idx - slide_idx) * rotation_step
            angle_rad = math.radians(angle_deg)
            
            # Box dimensions
            box_w = Inches(3.5)
            box_h = Inches(1.5)
            
            # Calculate center position of the text box on the orbit
            # cos(0) = 1 (Left of pivot), sin(0) = 0 (Same Y as pivot)
            ctx = pivot_x - orbit_radius * math.cos(angle_rad)
            cty = pivot_y - orbit_radius * math.sin(angle_rad)
            
            # Top-Left corner for PPTX placement
            left = ctx - box_w / 2
            top = cty - box_h / 2
            
            # Add text box
            tb = slide.shapes.add_textbox(left, top, box_w, box_h)
            tb.name = f"!!Node_{node_idx}"
            # Rotate text box so its right edge points toward the planet
            tb.rotation = -angle_deg 
            
            tf = tb.text_frame
            tf.clear()
            
            # Formatting based on whether it is the active node
            is_active = (node_idx == slide_idx)
            
            # Paragraph 1: Year & Title
            p1 = tf.paragraphs[0]
            p1.alignment = PP_ALIGN.RIGHT
            run_year = p1.add_run()
            run_year.text = node_data["year"] + "  "
            run_year.font.name = 'Arial'
            run_year.font.size = Pt(28 if is_active else 20)
            run_year.font.bold = True
            run_year.font.color.rgb = RGBColor(*accent_color) if is_active else RGBColor(150, 150, 150)
            
            run_title = p1.add_run()
            run_title.text = node_data["title"]
            run_title.font.name = 'Microsoft YaHei'
            run_title.font.size = Pt(18 if is_active else 14)
            run_title.font.bold = True
            run_title.font.color.rgb = RGBColor(255, 255, 255) if is_active else RGBColor(120, 120, 120)
            
            # Paragraph 2: Description (Only show clearly if active)
            p2 = tf.add_paragraph()
            p2.alignment = PP_ALIGN.RIGHT
            run_desc = p2.add_run()
            run_desc.text = "\n" + node_data["desc"]
            run_desc.font.name = 'Microsoft YaHei'
            run_desc.font.size = Pt(12)
            # Fade out description if not active
            run_desc.font.color.rgb = RGBColor(200, 200, 200) if is_active else RGBColor(50, 50, 50)

    prs.save(output_pptx_path)
    
    # Cleanup temporary assets
    if os.path.exists(bg_path): os.remove(bg_path)
    if os.path.exists(planet_path): os.remove(planet_path)
    
    return output_pptx_path
