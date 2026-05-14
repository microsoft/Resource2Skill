def create_slide(
    output_pptx_path: str,
    title_text: str = "INNOVATOR",
    body_text: str = "",
    bg_palette: str = "white",
    accent_color: tuple = (220, 20, 60),  # Crimson Red
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the Editorial Magazine Cover layout.
    """
    import os
    import tempfile
    import random
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    from pptx.enum.shapes import MSO_SHAPE
    from pptx.enum.text import PP_ALIGN
    from pptx.oxml import OxmlElement
    from pptx.oxml.ns import qn
    from PIL import Image, ImageDraw, ImageFilter, ImageFont

    prs = Presentation()
    
    # 1. Change slide size to Letter Portrait (8.5 x 11)
    prs.slide_width = Inches(8.5)
    prs.slide_height = Inches(11.0)
    
    # Use blank layout
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    # === Layer 1: Background ===
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
    bg.fill.solid()
    bg.fill.fore_color.rgb = RGBColor(245, 245, 245)
    bg.line.fill.background()

    # === Layer 2: Structural Border ===
    # 0.75" left margin for "binding", 0.5" elsewhere
    border = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.75), Inches(0.5), Inches(7.25), Inches(10.0))
    border.line.color.rgb = RGBColor(*accent_color)
    border.line.width = Pt(8)
    
    # Use lxml to guarantee "No Fill" so elements behind it (like the background) show through perfectly
    spPr = border.element.spPr
    for e in spPr.xpath('.//a:solidFill | .//a:gradFill | .//a:pattFill | .//a:blipFill'):
        spPr.remove(e)
    if not spPr.xpath('.//a:noFill'):
        spPr.append(OxmlElement('a:noFill'))

    # === Layer 3: Masthead & Metadata ===
    # Metadata Line
    dateline = slide.shapes.add_textbox(Inches(0.75), Inches(0.2), Inches(7.25), Inches(0.5))
    p_dl = dateline.text_frame.paragraphs[0]
    p_dl.text = "VOL. 42  •  MARCH 2025  •  $5.99"
    p_dl.alignment = PP_ALIGN.CENTER
    p_dl.font.size = Pt(10)
    p_dl.font.bold = True
    p_dl.font.color.rgb = RGBColor(100, 100, 100)

    # Masthead (Title)
    masthead = slide.shapes.add_textbox(Inches(0.75), Inches(0.5), Inches(7.25), Inches(2.0))
    tf = masthead.text_frame
    p_mh = tf.paragraphs[0]
    p_mh.text = title_text
    p_mh.alignment = PP_ALIGN.CENTER
    p_mh.font.size = Pt(76)
    p_mh.font.bold = True
    p_mh.font.name = 'Impact'
    p_mh.font.color.rgb = RGBColor(*accent_color)

    # LXML Injection: Apply WordArt Text Warp (wave1) to the masthead
    txBody = masthead.element.xpath('.//p:txBody')
    if txBody:
        bodyPr = txBody[0].xpath('.//a:bodyPr')[0]
        prstTxWarp = OxmlElement('a:prstTxWarp')
        prstTxWarp.set('prst', 'wave1')
        avLst = OxmlElement('a:avLst')
        prstTxWarp.append(avLst)
        bodyPr.append(prstTxWarp)

    # === Layer 4: Isolated Subject (Generated via PIL) ===
    # Generating a transparent, 3D floating tech-crystal to simulate an isolated subject photo
    def generate_subject(path):
        size = (600, 600)
        img = Image.new('RGBA', size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        c1 = accent_color
        c2 = (max(0, c1[0]-60), max(0, c1[1]-60), max(0, c1[2]-60), 230)
        c3 = (min(255, c1[0]+60), min(255, c1[1]+60), min(255, c1[2]+60), 240)
        c1_trans = (c1[0], c1[1], c1[2], 240)
        
        # Base shadow
        draw.ellipse((150, 480, 450, 530), fill=(0, 0, 0, 60))
        img = img.filter(ImageFilter.GaussianBlur(8))
        draw = ImageDraw.Draw(img)
        
        # Isometric geometric structure
        draw.polygon([(150, 250), (300, 350), (300, 500), (150, 400)], fill=c2)
        draw.polygon([(300, 350), (450, 250), (450, 400), (300, 500)], fill=c1_trans)
        draw.polygon([(300, 150), (450, 250), (300, 350), (150, 250)], fill=c3)
        
        # Floating top piece
        draw.polygon([(300, 50), (380, 100), (300, 150), (220, 100)], fill=c3)
        draw.polygon([(220, 100), (300, 150), (300, 200), (220, 150)], fill=c2)
        draw.polygon([(300, 150), (380, 100), (380, 150), (300, 200)], fill=c1_trans)
        img.save(path)

    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as subj_fp:
        generate_subject(subj_fp.name)
        # Centered horizontally, overlapping the masthead and border for a 3D pop effect
        slide.shapes.add_picture(subj_fp.name, Inches(1.25), Inches(2.75), width=Inches(6.0))
    os.remove(subj_fp.name)

    # === Layer 5: Teasers ===
    def add_teaser(left, top, w, h, t_title, t_sub, align):
        tb = slide.shapes.add_textbox(left, top, w, h)
        tf = tb.text_frame
        tf.word_wrap = True
        
        p1 = tf.paragraphs[0]
        p1.text = t_title
        p1.alignment = align
        p1.font.bold = True
        p1.font.size = Pt(22)
        p1.font.name = 'Arial'
        # Color every other teaser with the accent color
        if align == PP_ALIGN.RIGHT:
            p1.font.color.rgb = RGBColor(*accent_color)
        else:
            p1.font.color.rgb = RGBColor(30, 30, 30)
            
        p2 = tf.add_paragraph()
        p2.text = t_sub
        p2.alignment = align
        p2.font.size = Pt(12)
        p2.font.color.rgb = RGBColor(100, 100, 100)
        p2.font.name = 'Arial'

    add_teaser(Inches(5.25), Inches(2.5), Inches(2.5), Inches(1.5), 
               "QUANTUM\nSUPREMACY", "The race for the next era.", PP_ALIGN.RIGHT)
               
    add_teaser(Inches(0.85), Inches(4.5), Inches(2.5), Inches(1.5), 
               "AI & YOU", "How generative models change design forever.", PP_ALIGN.LEFT)
               
    add_teaser(Inches(0.85), Inches(7.5), Inches(2.5), Inches(1.5), 
               "STARTUP\nHUB 2025", "Exclusive interview with the founders.", PP_ALIGN.LEFT)
               
    add_teaser(Inches(5.25), Inches(6.5), Inches(2.5), Inches(1.5), 
               "CYBER\nSECURITY", "Protecting digital assets in the cloud.", PP_ALIGN.RIGHT)

    # === Layer 6: Authenticity Details (Barcode) ===
    def generate_barcode(path):
        img = Image.new('RGB', (180, 80), 'white')
        draw = ImageDraw.Draw(img)
        random.seed(123)
        x = 10
        while x < 170:
            w = random.randint(1, 4)
            draw.rectangle([x, 10, x+w, 60], fill='black')
            x += w + random.randint(1, 3)
        try:
            font = ImageFont.truetype("arial.ttf", 12)
        except:
            font = ImageFont.load_default()
        draw.text((20, 65), "ISSN 1234-5678", fill="black", font=font)
        img.save(path)

    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as bc_fp:
        generate_barcode(bc_fp.name)
        # Bottom right corner, sitting on the inner border
        slide.shapes.add_picture(bc_fp.name, Inches(6.0), Inches(9.6), width=Inches(1.5))
    os.remove(bc_fp.name)

    prs.save(output_pptx_path)
    return output_pptx_path
