def create_slide(
    output_pptx_path: str,
    title_text: str = "CLEAN",
    body_text: str = "P O W E R P O I N T   T E M P L A T E",
    bg_theme: str = "mountain,snow",
    accent_color: tuple = (220, 105, 95),  # Muted Coral/Red
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the Monochrome Minimalist Editorial visual effect.
    """
    import os
    import urllib.request
    from io import BytesIO
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
    from pptx.enum.shapes import MSO_SHAPE
    from pptx.oxml.ns import qn
    from pptx.oxml import OxmlElement
    from PIL import Image, ImageEnhance, ImageDraw

    # Initialize presentation
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6]) # Blank layout
    
    # Colors
    c_black = RGBColor(30, 30, 30)
    c_gray = RGBColor(120, 120, 120)
    c_accent = RGBColor(*accent_color)
    c_white = RGBColor(255, 255, 255)

    # --- Layer 1: Bottom B&W Faded Image using PIL ---
    img_path = "temp_bg_minimal.png"
    try:
        # Fetch image
        url = f"https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?ixlib=rb-4.0.3&auto=format&fit=crop&w=1600&q=80"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            img = Image.open(BytesIO(response.read())).convert("RGBA")
        
        # 1. Convert to Grayscale & Boost Contrast
        gray = img.convert('L')
        enhancer = ImageEnhance.Contrast(gray)
        gray = enhancer.enhance(1.8) # High contrast editorial look
        
        # 2. Re-merge to RGBA
        r, g, b = gray, gray, gray
        alpha = img.split()[3] if len(img.split()) == 4 else Image.new('L', img.size, 255)
        
        # 3. Create a linear gradient mask (transparent at top, opaque at bottom)
        gradient = Image.new('L', img.size)
        draw = ImageDraw.Draw(gradient)
        # Fade starts 20% from the top
        fade_start = int(img.height * 0.2)
        for y in range(img.height):
            if y < fade_start:
                a = 0
            else:
                a = int(255 * ((y - fade_start) / (img.height - fade_start)))
            draw.line([(0, y), (img.width, y)], fill=a)
        
        # Combine image alpha with gradient mask
        final_alpha = Image.new('L', img.size)
        final_alpha.paste(gradient, mask=gradient)
        
        final_img = Image.merge('RGBA', (r, g, b, final_alpha))
        final_img.save(img_path)
        
        # Insert at the bottom half of the slide
        pic = slide.shapes.add_picture(img_path, Inches(0), Inches(2.5), width=Inches(13.333))
        os.remove(img_path)
    except Exception as e:
        print(f"Failed to process image: {e}. Skipping image layer.")

    # --- Layer 2: Geometric Minimalist Frame ---
    # Center frame
    frame_w, frame_h = Inches(4.5), Inches(3.0)
    frame_l = (prs.slide_width - frame_w) / 2
    frame_t = (prs.slide_height - frame_h) / 2 - Inches(0.5)
    
    frame = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, frame_l, frame_t, frame_w, frame_h)
    frame.line.color.rgb = c_black
    frame.line.width = Pt(2)
    
    # Use lxml to completely remove the default solid fill
    spPr = frame.element.find(qn('p:spPr'))
    for child in spPr:
        if child.tag.endswith('Fill'):
            spPr.remove(child)
    spPr.insert(0, OxmlElement('a:noFill'))

    # --- Layer 3: Main Typography ---
    # Title breaking the frame (requires a white background on the text box to mask the frame line)
    title_w, title_h = Inches(6), Inches(1.5)
    title_l = (prs.slide_width - title_w) / 2
    title_t = frame_t + Inches(0.5)
    
    title_box = slide.shapes.add_textbox(title_l, title_t, title_w, title_h)
    # Add white solid fill to mask the frame line behind it
    title_box.fill.solid()
    title_box.fill.fore_color.rgb = c_white
    
    tf = title_box.text_frame
    tf.word_wrap = False
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tf.add_paragraph()
    p.text = title_text.upper()
    p.font.bold = True
    p.font.size = Pt(72)
    p.font.name = "Arial"
    p.font.color.rgb = c_black
    p.alignment = PP_ALIGN.CENTER

    # Subtitle with accent line
    sub_w, sub_h = Inches(5), Inches(0.5)
    sub_l = (prs.slide_width - sub_w) / 2
    sub_t = title_t + Inches(1.4)
    
    sub_box = slide.shapes.add_textbox(sub_l, sub_t, sub_w, sub_h)
    # White fill to cut the bottom frame line if it overlaps
    sub_box.fill.solid()
    sub_box.fill.fore_color.rgb = c_white
    
    tf_sub = sub_box.text_frame
    tf_sub.vertical_anchor = MSO_ANCHOR.MIDDLE
    p_sub = tf_sub.add_paragraph()
    p_sub.text = body_text
    p_sub.font.size = Pt(12)
    p_sub.font.name = "Arial"
    p_sub.font.color.rgb = c_gray
    p_sub.alignment = PP_ALIGN.CENTER

    # Small Accent colored line below subtitle
    acc_w, acc_h = Inches(0.3), Inches(0.05)
    acc_l = (prs.slide_width - acc_w) / 2
    acc_t = sub_t + Inches(0.5)
    acc_line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, acc_l, acc_t, acc_w, acc_h)
    acc_line.fill.solid()
    acc_line.fill.fore_color.rgb = c_accent
    acc_line.line.fill.background()

    # --- Layer 4: Perimeter Micro-Typography ---
    # Left Vertical Text
    v_text = "Y O U   C A N   W R I T E   H E R E"
    v_box = slide.shapes.add_textbox(Inches(-1.5), Inches(3.5), Inches(4), Inches(0.5))
    v_box.rotation = -90.0 # Rotate text box vertically
    tf_v = v_box.text_frame
    p_v = tf_v.add_paragraph()
    p_v.text = v_text
    p_v.font.size = Pt(9)
    p_v.font.bold = True
    p_v.font.color.rgb = c_black
    p_v.alignment = PP_ALIGN.CENTER

    # Top Right Spaced Text
    tr_text = "s i m p l e   t e x t"
    tr_box = slide.shapes.add_textbox(Inches(10.5), Inches(0.3), Inches(2.5), Inches(0.5))
    tf_tr = tr_box.text_frame
    p_tr = tf_tr.add_paragraph()
    p_tr.text = tr_text
    p_tr.font.size = Pt(10)
    p_tr.font.color.rgb = c_gray
    p_tr.alignment = PP_ALIGN.RIGHT

    # Bottom Right Page Number (Square Frame)
    sq_w = Inches(0.4)
    sq_l = prs.slide_width - Inches(0.8)
    sq_t = prs.slide_height - Inches(0.8)
    sq_box = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, sq_l, sq_t, sq_w, sq_w)
    sq_box.line.color.rgb = c_black
    sq_box.line.width = Pt(1)
    # Remove fill using lxml
    spPr_sq = sq_box.element.find(qn('p:spPr'))
    for child in spPr_sq:
        if child.tag.endswith('Fill'):
            spPr_sq.remove(child)
    spPr_sq.insert(0, OxmlElement('a:noFill'))
    
    # Add number text
    num_box = slide.shapes.add_textbox(sq_l, sq_t, sq_w, sq_w)
    tf_num = num_box.text_frame
    tf_num.vertical_anchor = MSO_ANCHOR.MIDDLE
    p_num = tf_num.add_paragraph()
    p_num.text = "01"
    p_num.font.size = Pt(10)
    p_num.font.bold = True
    p_num.font.color.rgb = c_black
    p_num.alignment = PP_ALIGN.CENTER

    # Save
    prs.save(output_pptx_path)
    return output_pptx_path
