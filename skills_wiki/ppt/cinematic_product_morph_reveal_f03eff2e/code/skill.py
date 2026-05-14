def create_slide(
    output_pptx_path: str,
    title_text: str = "PORSCHE CARRERA S",
    accent_color: tuple = (220, 180, 40),  # Yellow accent
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the Cinematic Product Morph Reveal.
    Includes dynamic background paneling and XML-injected Morph transitions.
    """
    import os
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    from pptx.enum.text import PP_ALIGN
    from pptx.oxml import parse_xml
    from PIL import Image, ImageDraw

    # --- 1. Helper: Generate Proxy Product Asset ---
    # Creates a transparent sports-car-like profile to ensure the code runs independently
    asset_path = "temp_mock_product.png"
    img = Image.new('RGBA', (800, 300), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    # Car Body
    draw.ellipse((100, 100, 700, 230), fill=(180, 185, 190, 255))  # Silver chassis
    draw.polygon([(200, 120), (350, 40), (500, 50), (620, 120)], fill=(150, 155, 160, 255))  # Cabin roof
    # Wheels & Calipers
    draw.ellipse((180, 160, 280, 260), fill=(30, 30, 30, 255)) # Rear Wheel
    draw.ellipse((520, 160, 620, 260), fill=(30, 30, 30, 255)) # Front Wheel
    draw.ellipse((210, 190, 250, 230), fill=accent_color + (255,)) # Rear Caliper
    draw.ellipse((550, 190, 590, 230), fill=accent_color + (255,)) # Front Caliper
    img.save(asset_path)

    # --- 2. Helper: Inject Morph Transition ---
    def apply_morph_transition(slide):
        """Injects PowerPoint Morph transition XML directly into the slide."""
        transition_xml = '''
        <p:transition xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" 
                      xmlns:p14="http://schemas.microsoft.com/office/powerpoint/2010/main" 
                      xmlns:p15="http://schemas.microsoft.com/office/powerpoint/2015/09/main" 
                      spd="med" p14:dur="2000">
            <p15:morph option="byObject"/>
        </p:transition>
        '''
        transition = parse_xml(transition_xml)
        slide.element.cSld.addnext(transition)

    # --- 3. Initialize Presentation ---
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    dark_grey = RGBColor(30, 30, 30)
    white = RGBColor(255, 255, 255)

    # ==========================================
    # SLIDE 1: The Hook (Full Bleed Setup)
    # ==========================================
    slide_1 = prs.slides.add_slide(blank_layout)
    
    # Background Panel (Full screen)
    bg_1 = slide_1.shapes.add_shape(
        1, 0, 0, prs.slide_width, prs.slide_height # 1 = msoShapeRectangle
    )
    bg_1.fill.solid()
    bg_1.fill.fore_color.rgb = dark_grey
    bg_1.line.fill.background()
    bg_1.name = "!!DynamicBg" # Force exact match for Morph

    # Title Text
    tx_1 = slide_1.shapes.add_textbox(Inches(0), Inches(1.5), prs.slide_width, Inches(1))
    tf_1 = tx_1.text_frame
    p_1 = tf_1.paragraphs[0]
    p_1.text = title_text.upper()
    p_1.alignment = PP_ALIGN.CENTER
    p_1.font.color.rgb = white
    p_1.font.size = Pt(48)
    p_1.font.bold = True
    tx_1.name = "!!MainTitle"

    # Product Image
    pic_1 = slide_1.shapes.add_picture(
        asset_path, 
        Inches(2.66), Inches(3.0), width=Inches(8)
    )
    pic_1.name = "!!ProductProxy"

    # ==========================================
    # SLIDE 2: The Deep Dive (Split Screen Morph)
    # ==========================================
    slide_2 = prs.slides.add_slide(blank_layout)
    apply_morph_transition(slide_2) # Apply the magic
    
    # Background Panel (Shrunk to 50% width)
    bg_2 = slide_2.shapes.add_shape(
        1, 0, 0, prs.slide_width / 2, prs.slide_height
    )
    bg_2.fill.solid()
    bg_2.fill.fore_color.rgb = dark_grey
    bg_2.line.fill.background()
    bg_2.name = "!!DynamicBg" # Matches Slide 1

    # Title Text (Moved to Right, changed to dark color)
    tx_2 = slide_2.shapes.add_textbox(Inches(7.5), Inches(1.5), Inches(5), Inches(1))
    tf_2 = tx_2.text_frame
    p_2 = tf_2.paragraphs[0]
    p_2.text = title_text.title() # Slightly softer casing
    p_2.alignment = PP_ALIGN.LEFT
    p_2.font.color.rgb = dark_grey # Inverted for white background
    p_2.font.size = Pt(40)
    p_2.font.bold = True
    tx_2.name = "!!MainTitle"

    # Detail Text (Fades in)
    detail_tx = slide_2.shapes.add_textbox(Inches(0.5), Inches(5.5), Inches(5), Inches(1.5))
    dtf = detail_tx.text_frame
    dp = dtf.paragraphs[0]
    dp.text = "D E T A I L S :\n\n379 hp             4.0s              180 mph\nMax power       0-60 mph       Top speed"
    dp.font.color.rgb = white
    dp.font.size = Pt(14)
    detail_tx.name = "DetailSpecs"

    # Product Image (Scaled down, moved to intersection)
    pic_2 = slide_2.shapes.add_picture(
        asset_path, 
        Inches(1.5), Inches(2.5), width=Inches(6.5)
    )
    pic_2.name = "!!ProductProxy" # Matches Slide 1

    # Clean up asset
    prs.save(output_pptx_path)
    if os.path.exists(asset_path):
        os.remove(asset_path)
        
    return output_pptx_path
