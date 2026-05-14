def create_slide(
    output_pptx_path: str,
    title_text: str = "MAGAZINE",
    subtitle_text: str = "CUT-OUT STYLE",
    bg_color: tuple = (244, 208, 63), # Warm Mustard Yellow
    **kwargs,
) -> str:
    """
    Creates a PPTX file reproducing the 'Magazine Cut-out Collage Effect'.
    If no subject image is provided, it generates an abstract graphic to demonstrate the technique.
    """
    import io
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    from pptx.enum.shapes import MSO_SHAPE
    from PIL import Image, ImageDraw, ImageFilter
    from lxml import etree
    from pptx.oxml.ns import qn

    # --- Helper 1: Generate a transparent dummy subject ---
    def create_abstract_subject_png():
        # Creates a transparent image with stylized geometric shapes to simulate a subject
        img = Image.new("RGBA", (400, 500), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        # Draw some overlapping "cut-out" abstract shapes
        draw.ellipse([50, 50, 350, 350], fill=(255, 99, 71, 255))   # Coral
        draw.polygon([(200, 150), (20, 480), (380, 480)], fill=(65, 105, 225, 255)) # Royal Blue
        draw.rectangle([120, 200, 280, 400], fill=(255, 215, 0, 255)) # Gold
        return img

    # --- Helper 2: Generate the padded cut-out assets using PIL ---
    def create_collage_assets(img, border_width=15):
        # Add padding so the expanded border doesn't get cut off at the canvas edge
        padding = border_width * 3
        new_size = (img.width + padding*2, img.height + padding*2)

        # 1. Pad the original subject
        subject_padded = Image.new("RGBA", new_size, (0, 0, 0, 0))
        subject_padded.paste(img, (padding, padding))

        # 2. Create the expanded white paper backing mask
        alpha = subject_padded.split()[-1]
        
        # Blur expands the area, threshold hardens it into a slightly rounded, organic shape
        blurred_alpha = alpha.filter(ImageFilter.GaussianBlur(border_width))
        threshold = 30 # Lower threshold = thicker border
        expanded_alpha = blurred_alpha.point(lambda p: 255 if p > threshold else 0)
        
        # Tiny blur to soften the jagged aliasing caused by thresholding
        final_alpha = expanded_alpha.filter(ImageFilter.GaussianBlur(1))

        paper_padded = Image.new("RGBA", new_size, (255, 255, 255, 255))
        paper_padded.putalpha(final_alpha)

        return subject_padded, paper_padded

    # --- Helper 3: Inject shadow via lxml ---
    def add_shadow_to_shape(shape):
        spPr = shape._element.spPr
        effectLst = etree.SubElement(spPr, qn('a:effectLst'))
        # blurRad 100000 = ~8pt, dist 60000 = ~5pt, dir 2700000 = bottom-right
        outerShdw = etree.SubElement(effectLst, qn('a:outerShdw'),
                                     blurRad="100000", dist="60000", dir="2700000", algn="tl", rotWithShape="0")
        srgbClr = etree.SubElement(outerShdw, qn('a:srgbClr'), val="000000")
        etree.SubElement(srgbClr, qn('a:alpha'), val="30000") # 30% opacity

    def pil_to_bytes(img):
        img_bytes = io.BytesIO()
        img.save(img_bytes, format='PNG')
        img_bytes.seek(0)
        return img_bytes

    # ==========================================
    # Presentation Construction
    # ==========================================
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6]) # Blank slide

    # 1. Set solid background
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(*bg_color)

    # 2. Generate Assets
    base_subject_img = create_abstract_subject_png()
    subject_img, paper_img = create_collage_assets(base_subject_img, border_width=18)

    # 3. Insert Images into PPTX
    # Both images have the exact same dimensions thanks to the padding logic,
    # so placing them at the identical coordinates ensures perfect registration.
    img_width = Inches(5.5)
    img_height = Inches(5.5 * (subject_img.height / subject_img.width))
    left = Inches(7.0) # Right side of slide
    top = Inches(7.5/2) - (img_height/2)

    # Note: Insert paper backing FIRST so it sits behind the subject
    paper_pic = slide.shapes.add_picture(pil_to_bytes(paper_img), left, top, width=img_width, height=img_height)
    add_shadow_to_shape(paper_pic)
    
    subject_pic = slide.shapes.add_picture(pil_to_bytes(subject_img), left, top, width=img_width, height=img_height)
    
    # Rotate both by the exact same amount to create the "tossed" collage look
    rotation_angle = -6.0 
    paper_pic.rotation = rotation_angle
    subject_pic.rotation = rotation_angle

    # 4. Add "Magazine" style typography
    txBox = slide.shapes.add_textbox(Inches(1), Inches(2.2), Inches(5), Inches(1.5))
    tf = txBox.text_frame
    p = tf.add_paragraph()
    p.text = title_text
    p.font.name = "Arial Black"
    p.font.size = Pt(65)
    p.font.color.rgb = RGBColor(30, 30, 30)

    txBox2 = slide.shapes.add_textbox(Inches(1.2), Inches(3.5), Inches(5), Inches(1.5))
    tf2 = txBox2.text_frame
    p2 = tf2.add_paragraph()
    p2.text = subtitle_text
    p2.font.name = "Courier New"
    p2.font.bold = True
    p2.font.size = Pt(45)
    p2.font.color.rgb = RGBColor(255, 255, 255)

    # 5. Add a decorative "Washi Tape" element pinning the text
    tape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(1.0), Inches(2.0), Inches(1.8), Inches(0.4))
    tape.fill.solid()
    tape.fill.fore_color.rgb = RGBColor(255, 255, 255)
    tape.fill.transparency = 0.5 # Semi-transparent
    tape.line.fill.background() # No border
    tape.rotation = -12.0

    prs.save(output_pptx_path)
    return output_pptx_path
