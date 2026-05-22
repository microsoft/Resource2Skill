def create_slide(
    output_pptx_path: str,
    title_text: str = "EMPLOYEE SPOTLIGHT",
    subtitle_text: str = "Jane Doe",
    role_text: str = "Lead Designer",
    bg_color: tuple = (75, 15, 105),       # Deep Purple
    accent_color: tuple = (255, 255, 255), # Spotlight White
    avatar_url: str = "https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=800&q=80",
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the 'Theatrical Spotlight Focus' visual effect.
    """
    import urllib.request
    from PIL import Image, ImageDraw, ImageOps
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    from pptx.enum.text import PP_ALIGN
    from pptx.oxml.xmlchemy import OxmlElement

    # --- Helper Functions ---
    def set_shape_transparency(shape, opacity_percent):
        """Injects transparency into a shape's solid fill via lxml."""
        fill = shape.fill
        fill.solid()
        fill.fore_color.rgb = RGBColor(255, 255, 255) # Force color node creation
        
        # Locate the srgbClr node and append an alpha node
        srgbClr_nodes = shape.element.xpath('.//a:srgbClr')
        if srgbClr_nodes:
            srgbClr = srgbClr_nodes[0]
            # Remove any existing alpha nodes to prevent duplicates
            for existing_alpha in srgbClr.xpath('./a:alpha'):
                srgbClr.remove(existing_alpha)
            
            alpha = OxmlElement('a:alpha')
            # 100% opacity = 100000. 30% opacity = 30000.
            alpha.set('val', str(int(opacity_percent * 1000)))
            srgbClr.append(alpha)

    def create_circular_avatar(img_url, out_path, size=(400, 400)):
        """Downloads an image and formats it as a circular avatar with a white border."""
        try:
            req = urllib.request.Request(img_url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req) as response:
                with open("temp_avatar.jpg", "wb") as f:
                    f.write(response.read())
            img = Image.open("temp_avatar.jpg").convert("RGBA")
        except Exception:
            # Fallback placeholder if download fails
            img = Image.new("RGBA", size, (100, 100, 150, 255))

        # Crop to square center
        w, h = img.size
        min_dim = min(w, h)
        left = (w - min_dim) / 2
        top = (h - min_dim) / 2
        img = img.crop((left, top, left+min_dim, top+min_dim))
        img = img.resize(size, Image.Resampling.LANCZOS)

        # Apply circular mask
        mask = Image.new("L", size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, size[0], size[1]), fill=255)
        
        output = Image.new("RGBA", size, (0, 0, 0, 0))
        output.paste(img, (0, 0), mask=mask)

        # Draw border
        draw_out = ImageDraw.Draw(output)
        border_width = 12
        draw_out.ellipse((border_width/2, border_width/2, size[0]-border_width/2, size[1]-border_width/2), 
                         outline=(255, 255, 255, 255), width=border_width)
        
        output.save(out_path)
        return out_path

    # --- Setup Presentation ---
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6]) # Blank layout

    # 1. Background
    background = slide.shapes.add_shape(
        1, 0, 0, prs.slide_width, prs.slide_height # 1 = MSO_SHAPE.RECTANGLE
    )
    background.fill.solid()
    background.fill.fore_color.rgb = RGBColor(*bg_color)
    background.line.fill.background()

    # 2. Top Truss Construction
    truss_color = RGBColor(20, 20, 20)
    # Top bar
    bar1 = slide.shapes.add_shape(1, 0, Inches(0.2), prs.slide_width, Inches(0.15))
    bar1.fill.solid(); bar1.fill.fore_color.rgb = truss_color; bar1.line.fill.background()
    # Bottom bar
    bar2 = slide.shapes.add_shape(1, 0, Inches(0.9), prs.slide_width, Inches(0.15))
    bar2.fill.solid(); bar2.fill.fore_color.rgb = truss_color; bar2.line.fill.background()
    # Truss zig-zags (simplified structural look)
    for i in range(14):
        x = i * 1.0
        line = slide.shapes.add_connector(1, Inches(x), Inches(0.35), Inches(x+0.5), Inches(0.9)) # 1 = straight
        line.line.color.rgb = truss_color; line.line.width = Pt(4)
        line2 = slide.shapes.add_connector(1, Inches(x+0.5), Inches(0.9), Inches(x+1.0), Inches(0.35))
        line2.line.color.rgb = truss_color; line2.line.width = Pt(4)

    # 3. The Stage (Bottom Ellipse)
    stage_w = Inches(7.0)
    stage_h = Inches(1.8)
    stage_x = (prs.slide_width - stage_w) / 2
    stage_y = prs.slide_height - Inches(1.5)
    
    stage = slide.shapes.add_shape(9, stage_x, stage_y, stage_w, stage_h) # 9 = MSO_SHAPE.OVAL
    stage.fill.solid()
    stage.fill.fore_color.rgb = RGBColor(*accent_color)
    stage.line.fill.background()

    # 4. Spotlights & Beams
    # We define 4 lights evenly spaced across the top
    light_positions = [Inches(2.5), Inches(5.5), Inches(7.833), Inches(10.833)]
    
    for idx, lx in enumerate(light_positions):
        # Draw the physical light fixture
        fixture = slide.shapes.add_shape(1, lx - Inches(0.3), Inches(1.05), Inches(0.6), Inches(0.8))
        fixture.fill.solid(); fixture.fill.fore_color.rgb = truss_color; fixture.line.fill.background()
        
        # Add angle rotation to fixtures pointing towards the center
        if idx == 0: fixture.rotation = -25
        elif idx == 1: fixture.rotation = -10
        elif idx == 2: fixture.rotation = 10
        elif idx == 3: fixture.rotation = 25

        # Draw the transparent beam
        builder = slide.shapes.build_freeform()
        
        # Origin at the bottom center of the light fixture
        origin_x, origin_y = lx, Inches(1.8)
        
        # The beams hit the stage oval. 
        # To make it dynamic, beams cover the inner ~80% of the stage width.
        target_left_x = stage_x + Inches(0.5)
        target_right_x = stage_x + stage_w - Inches(0.5)
        target_y = stage_y + (stage_h / 2) # Center of the oval

        # Draw Polygon: Origin -> Bottom Right -> Bottom Left -> Origin
        builder.add_line_segments([
            (origin_x - Inches(0.2), origin_y),
            (target_right_x, target_y),
            (target_left_x, target_y),
            (origin_x + Inches(0.2), origin_y)
        ], close=True)
        
        beam = builder.convert_to_shape()
        beam.line.fill.background() # No border
        
        # Apply LXML transparency (35% opacity creates a heavy additive glow where 4 beams overlap)
        set_shape_transparency(beam, 35)

    # 5. Content Injection (Text & Avatar)
    # Top Title
    tx_box = slide.shapes.add_textbox(0, Inches(2.5), prs.slide_width, Inches(1.0))
    tf = tx_box.text_frame
    p = tf.paragraphs[0]
    p.text = title_text
    p.font.size = Pt(44)
    p.font.bold = True
    p.font.name = "Arial Black"
    p.font.color.rgb = RGBColor(*accent_color)
    p.alignment = PP_ALIGN.CENTER

    # Avatar Image
    avatar_path = create_circular_avatar(avatar_url, "avatar_out.png")
    avatar_size = Inches(2.4)
    avatar_left = (prs.slide_width - avatar_size) / 2
    avatar_top = Inches(3.6)
    slide.shapes.add_picture(avatar_path, avatar_left, avatar_top, width=avatar_size, height=avatar_size)

    # Subtitle / Name
    name_box = slide.shapes.add_textbox(0, Inches(6.0), prs.slide_width, Inches(0.8))
    tf2 = name_box.text_frame
    p2 = tf2.paragraphs[0]
    p2.text = subtitle_text
    p2.font.size = Pt(36)
    p2.font.bold = True
    p2.font.color.rgb = truss_color # Black text on the white stage
    p2.alignment = PP_ALIGN.CENTER

    # Role / Description
    role_box = slide.shapes.add_textbox(0, Inches(6.5), prs.slide_width, Inches(0.5))
    tf3 = role_box.text_frame
    p3 = tf3.paragraphs[0]
    p3.text = role_text
    p3.font.size = Pt(24)
    p3.font.color.rgb = RGBColor(60, 60, 60)
    p3.alignment = PP_ALIGN.CENTER

    prs.save(output_pptx_path)
    return output_pptx_path
