def create_slide(
    output_pptx_path: str,
    title_text: str = "Introduction",
    body_text: str = "Fusce tristique massa eget finibus iaculis. Vestibulum convallis, tortor ac dictum tincidunt.\n\nEt venenatis tortor justo et sem. Etiam in pellentesque massa.",
    **kwargs,
) -> str:
    """
    Creates a 2-slide PPTX demonstrating the Dynamic Glassmorphic Dial morph transition.
    Returns the path to the generated PPTX file.
    """
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    from pptx.enum.shapes import MSO_SHAPE
    from pptx.enum.text import PP_ALIGN
    from pptx.oxml import parse_xml
    from pptx.oxml.ns import qn
    from PIL import Image, ImageDraw
    import urllib.request
    import os
    import math

    # === Helper 1: Download Image ===
    def download_image(url, filename):
        if os.path.exists(filename):
            return filename
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req) as response:
                with open(filename, 'wb') as f:
                    f.write(response.read())
        except Exception:
            # Fallback graphic if download fails
            img = Image.new('RGB', (1920, 1080), color=(30, 40, 50))
            img.save(filename)
        return filename

    # === Helper 2: Create Gradient Overlay via PIL ===
    def create_gradient_overlay(filepath):
        img = Image.new('RGBA', (1920, 1080))
        draw = ImageDraw.Draw(img)
        for x in range(1920):
            # Alpha scales from 0 to 220 (transparent to dark)
            alpha = int((x / 1920) * 220)
            draw.line([(x, 0), (x, 1080)], fill=(10, 15, 25, alpha))
        img.save(filepath)
        return filepath

    # === Helper 3: Inject True Slide Picture Background ===
    def set_slide_background_picture(slide, image_path, prs):
        # Insert temporarily to get Relationship ID
        pic = slide.shapes.add_picture(image_path, 0, 0, prs.slide_width, prs.slide_height)
        blip = pic.element.xpath('.//a:blip')[0]
        rId = blip.get(qn('r:embed'))
        
        # Inject <p:bg> XML
        bg_xml = f"""
        <p:bg xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"
              xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"
              xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
            <p:bgPr>
                <a:blipFill>
                    <a:blip r:embed="{rId}"/>
                    <a:stretch><a:fillRect/></a:stretch>
                </a:blipFill>
            </p:bgPr>
        </p:bg>
        """
        bg = parse_xml(bg_xml)
        existing_bg = slide.element.cSld.find(qn('p:bg'))
        if existing_bg is not None:
            slide.element.cSld.remove(existing_bg)
        slide.element.cSld.insert(0, bg)
        # Remove temp shape
        slide.shapes._spTree.remove(pic.element)

    # === Helper 4: Apply Slide Background Fill & Shadow ===
    def apply_bg_fill_and_shadow(shape):
        spPr = shape.element.spPr
        
        # Remove standard fills
        for elem in spPr.xpath('./a:solidFill | ./a:noFill | ./a:blipFill | ./a:gradFill'):
            spPr.remove(elem)
            
        bg_fill = parse_xml('<a:bgFill xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"/>')
        
        # Insert strictly after geometry definitions
        geom = spPr.xpath('./a:prstGeom | ./a:custGeom')
        if geom:
            geom[0].addnext(bg_fill)
        else:
            spPr.insert(0, bg_fill)

        # White Outline
        shape.line.color.rgb = RGBColor(255, 255, 255)
        shape.line.width = Pt(1.5)

        # Drop Shadow
        for elem in spPr.xpath('./a:effectLst'):
            spPr.remove(elem)
        effect_xml = """
        <a:effectLst xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">
            <a:outerShdw blurRad="152400" dist="139700" dir="0" algn="b" rotWithShape="0">
                <a:srgbClr val="000000"><a:alpha val="40000"/></a:srgbClr>
            </a:outerShdw>
        </a:effectLst>
        """
        spPr.append(parse_xml(effect_xml))

    # === Helper 5: Place Rotated Tangential Text ===
    def place_rotated_text(slide, cx_in, cy_in, radius_in, angle_deg, text):
        angle_rad = math.radians(angle_deg)
        w_in, h_in = 1.8, 0.5
        tx_in = cx_in + radius_in * math.cos(angle_rad)
        ty_in = cy_in + radius_in * math.sin(angle_rad)
        
        txBox = slide.shapes.add_textbox(
            Inches(tx_in - w_in/2), Inches(ty_in - h_in/2), Inches(w_in), Inches(h_in)
        )
        txBox.text_frame.text = text
        txBox.text_frame.paragraphs[0].alignment = PP_ALIGN.CENTER
        
        font = txBox.text_frame.paragraphs[0].runs[0].font
        font.bold = True
        font.size = Pt(16)
        font.color.rgb = RGBColor(255, 255, 255)
        
        # Tangential rotation
        txBox.rotation = (angle_deg + 90) % 360
        return txBox

    # === Setup Presentation ===
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Prepare assets
    bg1_path = download_image("https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?w=1920&q=80", "mountain_bg.jpg")
    bg2_path = download_image("https://images.unsplash.com/photo-1518730518541-d0843268c287?w=1920&q=80", "ice_bg.jpg")
    grad_path = create_gradient_overlay("gradient_overlay.png")

    titles = [title_text, "Lorem Ipsum"]
    
    # Generate 2 Slides to demonstrate Morph rotation
    for i in range(2):
        slide = prs.slides.add_slide(blank_layout)
        
        # 1. Image Background
        img_path = bg1_path if i == 0 else bg2_path
        set_slide_background_picture(slide, img_path, prs)
        
        # 2. Gradient Overlay
        slide.shapes.add_picture(grad_path, 0, 0, prs.slide_width, prs.slide_height)
        
        # 3. Rotating Dial Elements (Left side, centered at X=3.5, Y=3.75)
        cx, cy = 3.5, 3.75
        
        # Outer Portal
        outer_r = 3.0
        large_circle = slide.shapes.add_shape(
            MSO_SHAPE.OVAL, Inches(cx - outer_r), Inches(cy - outer_r), Inches(outer_r*2), Inches(outer_r*2)
        )
        apply_bg_fill_and_shadow(large_circle)
        large_circle.name = "!!MorphDialOuter"  # '!!' enforces strict morph mapping

        # Inner Portal
        inner_r = 1.2
        inner_circle = slide.shapes.add_shape(
            MSO_SHAPE.OVAL, Inches(cx - inner_r), Inches(cy - inner_r), Inches(inner_r*2), Inches(inner_r*2)
        )
        apply_bg_fill_and_shadow(inner_circle)
        inner_circle.name = "!!MorphDialInner"

        # Text Node Elements (Rotate counter-clockwise by 90 deg on slide 2)
        offset = -90 if i == 1 else 0
        nodes = ["PART 01", "PART 02", "PART 03", "PART 04"]
        base_angles = [0, 90, 180, 270]  # Right, Bottom, Left, Top
        
        for j, txt in enumerate(nodes):
            angle = base_angles[j] + offset
            tb = place_rotated_text(slide, cx, cy, 2.3, angle, txt)
            tb.name = f"!!MorphNode{j}"
            
        # 4. Main Content (Right Side)
        title_box = slide.shapes.add_textbox(Inches(6.5), Inches(2.2), Inches(6), Inches(1))
        title_box.text_frame.text = titles[i]
        t_font = title_box.text_frame.paragraphs[0].runs[0].font
        t_font.size = Pt(54)
        t_font.bold = True
        t_font.color.rgb = RGBColor(255, 255, 255)
        
        body_box = slide.shapes.add_textbox(Inches(6.5), Inches(3.5), Inches(5.5), Inches(2))
        body_box.text_frame.word_wrap = True
        body_box.text_frame.text = body_text
        b_font = body_box.text_frame.paragraphs[0].runs[0].font
        b_font.size = Pt(18)
        b_font.color.rgb = RGBColor(230, 230, 230)

        # 5. Inject Morph Transition on the 2nd Slide
        if i == 1:
            morph_xml = (
                '<p:transition xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" '
                'xmlns:p14="http://schemas.microsoft.com/office/powerpoint/2010/main" '
                'spd="slow" p14:dur="1500">'
                '<p14:morph option="byObject"/>'
                '</p:transition>'
            )
            transition = parse_xml(morph_xml)
            sld = slide.element
            timing = sld.find(qn('p:timing'))
            if timing is not None:
                timing.addprevious(transition)
            else:
                sld.append(transition)

    prs.save(output_pptx_path)
    
    # Cleanup local assets
    for f in ["mountain_bg.jpg", "ice_bg.jpg", "gradient_overlay.png"]:
        if os.path.exists(f):
            os.remove(f)
            
    return output_pptx_path
