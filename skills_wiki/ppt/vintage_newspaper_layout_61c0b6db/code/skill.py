def create_slide(
    output_pptx_path: str,
    title_text: str = "THE DAILY CHRONICLE",
    body_text: str = "",
    bg_palette: str = "vintage", 
    accent_color: tuple = (0, 0, 0), 
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the 'Vintage Newspaper Layout' visual effect.
    """
    import os
    import urllib.request
    import io
    from PIL import Image, ImageDraw, ImageFilter, ImageEnhance
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    from pptx.enum.shapes import MSO_CONNECTOR
    from pptx.enum.text import PP_ALIGN

    # ==========================================
    # Helper Functions
    # ==========================================
    def create_vintage_paper_bg(filename="vintage_bg.jpg"):
        bg_width, bg_height = 1920, 1080
        # Base aged paper color
        bg_img = Image.new('RGB', (bg_width, bg_height), (244, 238, 227))
        
        # Create vignette mask
        mask = Image.new('L', (bg_width, bg_height), 255)
        draw = ImageDraw.Draw(mask)
        draw.rectangle([150, 150, bg_width-150, bg_height-150], fill=0)
        mask = mask.filter(ImageFilter.GaussianBlur(150))
        
        # Darker edge color
        dark_edge = Image.new('RGB', (bg_width, bg_height), (200, 185, 160))
        
        # Composite
        final_bg = Image.composite(bg_img, dark_edge, mask)
        final_bg.save(filename, quality=90)
        return filename

    def get_grayscale_image(url="https://picsum.photos/400/300", filename="news_img.jpg"):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=5) as response:
                img_data = response.read()
            img = Image.open(io.BytesIO(img_data)).convert('L') # Convert to grayscale
            # Boost contrast to simulate newsprint
            enhancer = ImageEnhance.Contrast(img)
            img = enhancer.enhance(1.3)
            img.save(filename)
            return filename
        except Exception as e:
            # Fallback: Create a placeholder graphic
            img = Image.new('L', (400, 300), color=220)
            draw = ImageDraw.Draw(img)
            draw.line((0,0, 400,300), fill=100, width=3)
            draw.line((0,300, 400,0), fill=100, width=3)
            img.save(filename)
            return filename

    def add_horizontal_line(slide, x, y, width, thickness=Pt(1)):
        line = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, x, y, x + width, y)
        line.line.color.rgb = RGBColor(0, 0, 0)
        line.line.width = thickness

    def add_vertical_line(slide, x, y, height, thickness=Pt(1)):
        line = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, x, y, x, y + height)
        line.line.color.rgb = RGBColor(0, 0, 0)
        line.line.width = thickness

    def add_border(slide, x, y, w, h, thickness=Pt(1.5)):
        add_horizontal_line(slide, x, y, w, thickness)
        add_horizontal_line(slide, x, y+h, w, thickness)
        add_vertical_line(slide, x, y, h, thickness)
        add_vertical_line(slide, x+w, y, h, thickness)

    def add_text_block(slide, x, y, w, h, text, font_name='Georgia', font_size=11, bold=False, align=PP_ALIGN.JUSTIFY):
        txBox = slide.shapes.add_textbox(x, y, w, h)
        tf = txBox.text_frame
        tf.word_wrap = True
        tf.margin_top = Pt(2)
        tf.margin_bottom = Pt(2)
        tf.margin_left = Pt(5)
        tf.margin_right = Pt(5)
        
        # Split by double newlines for paragraphs
        paragraphs = text.split('\n\n')
        for i, para_text in enumerate(paragraphs):
            if i == 0:
                p = tf.paragraphs[0]
            else:
                p = tf.add_paragraph()
            p.text = para_text
            p.alignment = align
            p.font.name = font_name
            p.font.size = Pt(font_size)
            p.font.bold = bold
            p.font.color.rgb = RGBColor(0, 0, 0)
            p.space_after = Pt(6)
        return txBox

    # ==========================================
    # Presentation Setup
    # ==========================================
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    # Constants for Layout
    SLIDE_W = prs.slide_width
    SLIDE_H = prs.slide_height
    MARGIN_X = Inches(0.8)
    MARGIN_Y = Inches(0.5)
    COL_WIDTH = Inches(3.64)
    GAP = Inches(0.4)

    default_body = (
        "In a startling turn of events late yesterday evening, authorities reported unprecedented "
        "developments in the downtown sector. Witnesses described a flurry of activity as officials "
        "scrambled to address the rapidly evolving situation. 'We have never seen anything quite like "
        "this in the history of our great city,' remarked one bystander, visibly shaken.\n\n"
        "Experts are already debating the long-term implications of these events. While some predict "
        "a swift return to normalcy, others warn that this may be the dawn of a new era. "
        "Citizens are advised to remain calm and await further instructions from authorities."
    )
    if not body_text:
        body_text = default_body

    # ==========================================
    # Layer 1: Background & Page Borders
    # ==========================================
    bg_path = create_vintage_paper_bg("temp_bg.jpg")
    slide.shapes.add_picture(bg_path, 0, 0, width=SLIDE_W, height=SLIDE_H)
    
    # Outer thick border
    add_border(slide, Inches(0.4), Inches(0.4), SLIDE_W - Inches(0.8), SLIDE_H - Inches(0.8), Pt(2.5))
    # Inner thin border
    add_border(slide, Inches(0.46), Inches(0.46), SLIDE_W - Inches(0.92), SLIDE_H - Inches(0.92), Pt(0.75))

    # ==========================================
    # Layer 2: Header Section (Masthead & Dateline)
    # ==========================================
    masthead = add_text_block(slide, MARGIN_X, MARGIN_Y, SLIDE_W - 2*MARGIN_X, Inches(1.0), 
                              title_text, font_name='Times New Roman', font_size=54, bold=True, align=PP_ALIGN.CENTER)
    
    y_line1 = MARGIN_Y + Inches(1.1)
    add_horizontal_line(slide, MARGIN_X, y_line1, SLIDE_W - 2*MARGIN_X, Pt(2))

    dateline_text = "VOL. CXLI .... NO. 49,000      |      MONDAY, OCTOBER 24      |      PRICE: 5 CENTS"
    add_text_block(slide, MARGIN_X, y_line1 + Inches(0.02), SLIDE_W - 2*MARGIN_X, Inches(0.3), 
                   dateline_text, font_size=9, bold=True, align=PP_ALIGN.CENTER)

    y_line2 = y_line1 + Inches(0.35)
    add_horizontal_line(slide, MARGIN_X, y_line2, SLIDE_W - 2*MARGIN_X, Pt(1))

    # ==========================================
    # Layer 3: Columns & Content
    # ==========================================
    col_y = y_line2 + Inches(0.2)
    col_h = SLIDE_H - col_y - Inches(0.6) # Leave margin at bottom

    # --- Column 1 ---
    c1_x = MARGIN_X
    add_text_block(slide, c1_x, col_y, COL_WIDTH, Inches(0.8), 
                   "MARKET CRASHES;\nPANIC IN STREETS", font_size=24, bold=True, align=PP_ALIGN.LEFT)
    add_text_block(slide, c1_x, col_y + Inches(1.0), COL_WIDTH, col_h - Inches(1.0), 
                   body_text + "\n\n" + body_text[:200] + "...", font_size=11, align=PP_ALIGN.JUSTIFY)

    # Divider 1
    add_vertical_line(slide, c1_x + COL_WIDTH + GAP/2, col_y, col_h, Pt(0.5))

    # --- Column 2 (Image + Text) ---
    c2_x = c1_x + COL_WIDTH + GAP
    img_path = get_grayscale_image(filename="temp_img.jpg")
    img_h = Inches(2.2)
    slide.shapes.add_picture(img_path, c2_x, col_y, width=COL_WIDTH, height=img_h)
    
    add_text_block(slide, c2_x, col_y + img_h + Inches(0.05), COL_WIDTH, Inches(0.3), 
                   "Above: A scene from downtown yesterday as crowds gathered.", font_size=8, align=PP_ALIGN.LEFT)
    
    add_text_block(slide, c2_x, col_y + img_h + Inches(0.4), COL_WIDTH, col_h - img_h - Inches(0.4), 
                   body_text, font_size=11, align=PP_ALIGN.JUSTIFY)

    # Divider 2
    add_vertical_line(slide, c2_x + COL_WIDTH + GAP/2, col_y, col_h, Pt(0.5))

    # --- Column 3 ---
    c3_x = c2_x + COL_WIDTH + GAP
    add_text_block(slide, c3_x, col_y, COL_WIDTH, Inches(0.8), 
                   "MAYOR PROMISES\nSWIFT RECOVERY", font_size=18, bold=True, align=PP_ALIGN.LEFT)
    add_text_block(slide, c3_x, col_y + Inches(0.8), COL_WIDTH, col_h - Inches(0.8), 
                   body_text + "\n\n" + body_text[:150], font_size=11, align=PP_ALIGN.JUSTIFY)

    # Clean up temp files
    prs.save(output_pptx_path)
    if os.path.exists("temp_bg.jpg"): os.remove("temp_bg.jpg")
    if os.path.exists("temp_img.jpg"): os.remove("temp_img.jpg")

    return output_pptx_path
