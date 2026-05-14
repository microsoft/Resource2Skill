import os
from PIL import Image, ImageDraw
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.shapes import MSO_SHAPE
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.oxml import OxmlElement

def create_slide(
    output_pptx_path: str = "Morphing_Panels.pptx",
    main_title_text: str = "CHOOSING THE BEST",
    **kwargs,
) -> str:
    """
    Creates a PPTX file reproducing the Dynamic Morphing Split-Panels effect.
    Returns the path to the saved presentation.
    """
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    # ---------------------------------------------------------
    # Helper 1: Generate Mockup Device Images using PIL
    # ---------------------------------------------------------
    def create_mockup_phone(filename, body_color, grad_start, grad_end):
        """Draws a sleek phone graphic to act as our product imagery."""
        img = Image.new('RGBA', (400, 800), (0,0,0,0))
        draw = ImageDraw.Draw(img)
        # Phone body
        draw.rounded_rectangle([20, 20, 380, 780], radius=45, fill=body_color)
        
        # Screen gradient
        screen_img = Image.new('RGBA', (320, 720))
        draw_scr = ImageDraw.Draw(screen_img)
        for y in range(720):
            r = int(grad_start[0] + (grad_end[0] - grad_start[0]) * y / 720)
            g = int(grad_start[1] + (grad_end[1] - grad_start[1]) * y / 720)
            b = int(grad_start[2] + (grad_end[2] - grad_start[2]) * y / 720)
            draw_scr.line([(0, y), (320, y)], fill=(r, g, b, 255))
            
        # Screen Mask for rounded corners
        mask = Image.new('L', (320, 720), 0)
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.rounded_rectangle([0, 0, 320, 720], radius=25, fill=255)
        img.paste(screen_img, (40, 40), mask)
        
        # Camera punch-hole
        draw.ellipse([185, 55, 215, 85], fill=(30, 30, 30, 255))
        img.save(filename)

    # Generate 3 distinct product images
    img1_path, img2_path, img3_path = "phone1.png", "phone2.png", "phone3.png"
    create_mockup_phone(img1_path, (200, 200, 200), (255, 100, 100), (100, 100, 255)) # Silver/Purple
    create_mockup_phone(img2_path, (80, 80, 80), (100, 255, 100), (20, 100, 100))     # Dark Grey/Green
    create_mockup_phone(img3_path, (240, 240, 240), (255, 200, 100), (255, 100, 100)) # White/Orange

    # ---------------------------------------------------------
    # Helper 2: PPTX Element Generators
    # ---------------------------------------------------------
    def add_panel(slide, x, y, w, h, rgb_col):
        shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
        shape.fill.solid()
        shape.fill.fore_color.rgb = RGBColor(*rgb_col)
        shape.line.fill.solid()
        shape.line.fill.fore_color.rgb = RGBColor(*rgb_col) # Invisible border
        return shape

    def add_text(slide, x, y, w, h, text, size, rgb_col, bold=False, center=False):
        txBox = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
        tf = txBox.text_frame
        tf.word_wrap = True
        for i, line in enumerate(text.split('\n')):
            p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
            p.text = line
            p.font.size = Pt(size)
            p.font.color.rgb = RGBColor(*rgb_col)
            p.font.bold = bold
            p.font.name = 'Arial'
            if center:
                p.alignment = PP_ALIGN.CENTER
        return txBox

    # ---------------------------------------------------------
    # Global Palette
    # ---------------------------------------------------------
    C_NAVY = (41, 48, 63)
    C_BLUE = (147, 155, 172)
    C_GREY = (198, 203, 212)
    C_WHITE = (255, 255, 255)

    detail_text = (
        "• Design: Premium build, iconic look\n"
        "• Performance: Next-gen Bionic chip\n"
        "• Camera: 48MP Super Res System\n"
        "• Battery: All-day life, fast charging\n"
        "• Price: Starting at $999"
    )

    # MUST strictly order object creation for Morph to map shapes automatically
    def build_layout(slide, data):
        # 1. Panels
        add_panel(slide, *data['p1'])
        add_panel(slide, *data['p2'])
        add_panel(slide, *data['p3'])
        
        # 2. Main Title
        add_text(slide, *data['title'])
        
        # 3. Product 1 (Focus item)
        slide.shapes.add_picture(*data['img1'])
        add_text(slide, *data['sub1'])
        add_text(slide, *data['det1'])
        
        # 4. Product 2
        slide.shapes.add_picture(*data['img2'])
        add_text(slide, *data['sub2'])
        
        # 5. Product 3
        slide.shapes.add_picture(*data['img3'])
        add_text(slide, *data['sub3'])

    # ---------------------------------------------------------
    # Slide 1: Overview State (Equally divided)
    # ---------------------------------------------------------
    slide1 = prs.slides.add_slide(prs.slide_layouts[6])
    
    data_s1 = {
        'p1': (0, 0, 4.444, 7.5, C_NAVY),
        'p2': (4.444, 0, 4.444, 7.5, C_BLUE),
        'p3': (8.888, 0, 4.444, 7.5, C_GREY),
        
        'title': (0, 0.5, 13.333, 1.0, main_title_text, 48, C_WHITE, True, True),
        
        'img1': (img1_path, Inches(0.97), Inches(2.5), Inches(2.5)), 
        'sub1': (0.72, 1.5, 3.0, 0.5, "Phone Alpha", 28, C_WHITE, True, True),
        # Detail text exists but matches background color to be invisible
        'det1': (0.72, 5.5, 3.0, 0.5, detail_text, 16, C_NAVY, False, True), 
        
        'img2': (img2_path, Inches(5.41), Inches(2.5), Inches(2.5)),
        'sub2': (5.16, 1.5, 3.0, 0.5, "Galaxy Beta", 28, C_WHITE, True, True),
        
        'img3': (img3_path, Inches(9.86), Inches(2.5), Inches(2.5)),
        'sub3': (9.61, 1.5, 3.0, 0.5, "Pixel Gamma", 28, C_NAVY, True, True),
    }
    build_layout(slide1, data_s1)

    # ---------------------------------------------------------
    # Slide 2: Focused State (Panel 1 Expands)
    # ---------------------------------------------------------
    slide2 = prs.slides.add_slide(prs.slide_layouts[6])
    
    data_s2 = {
        'p1': (0, 0, 7.333, 7.5, C_NAVY),     # Expanded
        'p2': (7.333, 0, 3.0, 7.5, C_BLUE),   # Collapsed
        'p3': (10.333, 0, 3.0, 7.5, C_GREY),  # Collapsed
        
        'title': (0, 0.5, 13.333, 1.0, main_title_text, 48, C_WHITE, True, True),
        
        'img1': (img1_path, Inches(0.5), Inches(3.0), Inches(3.0)), # Shifted and Scaled
        'sub1': (0.5, 2.0, 3.0, 0.5, "Phone Alpha", 36, C_WHITE, True, True),
        'det1': (3.8, 3.0, 3.2, 3.0, detail_text, 16, C_WHITE, False, False), # Text turns White to Fade-in
        
        'img2': (img2_path, Inches(8.08), Inches(4.0), Inches(1.5)), # Shrunk
        'sub2': (7.83, 6.0, 2.0, 0.5, "Galaxy Beta", 18, C_WHITE, True, True),
        
        'img3': (img3_path, Inches(11.08), Inches(4.0), Inches(1.5)), # Shrunk
        'sub3': (10.83, 6.0, 2.0, 0.5, "Pixel Gamma", 18, C_NAVY, True, True),
    }
    build_layout(slide2, data_s2)

    # Inject OpenXML for Morph Transition on Slide 2
    transition = OxmlElement('p:transition')
    transition.set('spd', 'slow')
    morph = OxmlElement('p:morph')
    morph.set('option', 'byObject')
    transition.append(morph)
    slide2.element.append(transition)

    # Save and cleanup
    prs.save(output_pptx_path)
    
    for tmp_img in [img1_path, img2_path, img3_path]:
        if os.path.exists(tmp_img):
            os.remove(tmp_img)

    return output_pptx_path
