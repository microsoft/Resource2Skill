def create_slide(
    output_pptx_path: str,
    card_width_in: float = 2.2,
    card_height_in: float = 3.3,
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the Interactive 3D Card Flip setup.
    Slide 1: Three cards face down.
    Slide 2: The middle card flips to reveal a gift.
    (Apply 'Morph' transition to Slide 2 in PowerPoint to see the flip).
    """
    import os
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.oxml import parse_xml
    from pptx.oxml.ns import nsdecls
    from PIL import Image, ImageDraw, ImageFont

    # --- Helper 1: Generate Assets via PIL ---
    def generate_card_back(filename="card_back.png"):
        img = Image.new('RGBA', (400, 600), (255, 255, 255, 255))
        draw = ImageDraw.Draw(img)
        # Green border
        draw.rounded_rectangle([10, 10, 390, 590], radius=20, fill=(34, 139, 34, 255))
        # Inner pattern (simplified grid for card back)
        for x in range(30, 370, 40):
            for y in range(30, 570, 40):
                draw.ellipse([x, y, x+30, y+30], outline=(0, 100, 0, 255), width=3)
        img.save(filename)
        return filename

    def generate_card_front(filename="card_front.png", text="GIFT", color=(220, 20, 60, 255)):
        img = Image.new('RGBA', (400, 600), (255, 255, 255, 255))
        draw = ImageDraw.Draw(img)
        # White card with thin gray border
        draw.rounded_rectangle([5, 5, 395, 595], radius=20, outline=(200, 200, 200, 255), width=3)
        # Try to load a standard font, fallback to default
        try:
            font = ImageFont.truetype("arialbd.ttf", 60)
            font_small = ImageFont.truetype("arialbd.ttf", 30)
        except:
            font = ImageFont.load_default()
            font_small = font
        
        # Draw central text/icon placeholder
        draw.text((200, 300), text, fill=color, font=font, anchor="mm")
        # Draw corner indices
        draw.text((40, 50), text[0], fill=color, font=font_small, anchor="mm")
        draw.text((360, 550), text[0], fill=color, font=font_small, anchor="mm")
        img.save(filename)
        return filename

    def generate_bg(filename="bg.png"):
        img = Image.new('RGB', (1280, 720), (20, 90, 20))
        draw = ImageDraw.Draw(img)
        # Simple radial-ish gradient simulation via expanding ellipses
        for i in range(200, 0, -5):
            color = (max(10, 34 - int((200-i)/10)), max(50, 139 - int((200-i)/2)), max(10, 34 - int((200-i)/10)))
            draw.ellipse([640 - i*4, 360 - i*3, 640 + i*4, 360 + i*3], fill=color)
        img.save(filename)
        return filename

    card_back_img = generate_card_back()
    card_front_joker = generate_card_front("card_joker.png", "JOKER", (0, 0, 128, 255))
    card_front_gift = generate_card_front("card_gift.png", "GIFT", (220, 20, 60, 255))
    bg_img = generate_bg()

    # --- Helper 2: LXML Injection for 3D Rotation & Shadow ---
    def apply_3d_and_shadow(shape, rx_degrees=0):
        """Injects 3D rotation (X-axis) and a drop shadow into shape XML."""
        spPr = shape.element.find('.//p:spPr', namespaces=shape.element.nsmap)
        if spPr is None:
            return

        # 1. Outer Shadow XML
        shadow_xml = f"""
        <a:effectLst {nsdecls('a')}>
            <a:outerShdw blurRad="200000" dist="250000" dir="2700000" algn="bl" rotWithShape="0">
                <a:srgbClr val="000000">
                    <a:alpha val="40000"/>
                </a:srgbClr>
            </a:outerShdw>
        </a:effectLst>
        """
        spPr.append(parse_xml(shadow_xml))

        # 2. 3D Scene and Rotation XML (60,000 units per degree)
        rx_units = int(rx_degrees * 60000)
        scene_xml = f"""
        <a:scene3d {nsdecls('a')}>
            <a:camera prst="orthographicFront"/>
            <a:lightRig rig="threePt" dir="t"/>
        </a:scene3d>
        """
        sp3d_xml = f"""
        <a:sp3d {nsdecls('a')}>
            <a:rot rx="{rx_units}" ry="0" rz="0"/>
        </a:sp3d>
        """
        spPr.append(parse_xml(scene_xml))
        spPr.append(parse_xml(sp3d_xml))

    # --- Presentation Setup ---
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Function to build a slide state
    def build_slide(is_flipped=False):
        slide = prs.slides.add_slide(blank_layout)
        
        # Set background
        slide.shapes.add_picture(bg_img, 0, 0, prs.slide_width, prs.slide_height)

        # Card positions
        positions = [
            (Inches(2.5), Inches(2.1)),  # Left
            (Inches(5.5), Inches(2.1)),  # Center
            (Inches(8.5), Inches(2.1))   # Right
        ]
        
        fronts = [card_front_joker, card_front_gift, card_front_joker]

        for i, (x, y) in enumerate(positions):
            # If we are building the flipped slide, and this is the center card (index 1)
            flip_this_card = is_flipped and i == 1

            if flip_this_card:
                # Z-Order Bottom: Card Back (rotated 180)
                back_shape = slide.shapes.add_picture(card_back_img, x, y, width=Inches(card_width_in), height=Inches(card_height_in))
                apply_3d_and_shadow(back_shape, rx_degrees=180)
                
                # Z-Order Top: Card Front (rotated 0)
                front_shape = slide.shapes.add_picture(fronts[i], x, y, width=Inches(card_width_in), height=Inches(card_height_in))
                apply_3d_and_shadow(front_shape, rx_degrees=0)
            else:
                # Z-Order Bottom: Card Front (rotated 180)
                front_shape = slide.shapes.add_picture(fronts[i], x, y, width=Inches(card_width_in), height=Inches(card_height_in))
                apply_3d_and_shadow(front_shape, rx_degrees=180)
                
                # Z-Order Top: Card Back (rotated 0)
                back_shape = slide.shapes.add_picture(card_back_img, x, y, width=Inches(card_width_in), height=Inches(card_height_in))
                apply_3d_and_shadow(back_shape, rx_degrees=0)

        # Add text to the flipped slide
        if is_flipped:
            txBox = slide.shapes.add_textbox(Inches(0), Inches(6), prs.slide_width, Inches(1))
            tf = txBox.text_frame
            tf.text = "Congratulations! You found the Gift!"
            tf.paragraphs[0].alignment = 2  # PP_ALIGN.CENTER
            tf.paragraphs[0].font.size = Pt(40)
            tf.paragraphs[0].font.color.rgb = from_hex("FFFFFF") # Requires a small helper or pptx native
            tf.paragraphs[0].font.bold = True

    # Simple hex to RGB color helper
    def from_hex(hexstr):
        from pptx.dml.color import RGBColor
        return RGBColor(int(hexstr[:2], 16), int(hexstr[2:4], 16), int(hexstr[4:], 16))

    # --- Generate Slides ---
    build_slide(is_flipped=False) # Slide 1: All face down
    build_slide(is_flipped=True)  # Slide 2: Middle card face up

    # Cleanup temp files
    for f in [card_back_img, card_front_joker, card_front_gift, bg_img]:
        if os.path.exists(f):
            os.remove(f)

    prs.save(output_pptx_path)
    return output_pptx_path
