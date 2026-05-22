def create_slide(
    output_pptx_path: str,
    title_text: str = "STUNNING TITLES",
    body_text: str = "USING POWERPOINT ANIMATION FUN FAST EASY EFFECT",
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the 'Kinetic Typography Morph Sequence' visual effect.
    Generates a 4-slide sequence that utilizes XML-injected Morph transitions.
    
    Returns: path to the saved PPTX file.
    """
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    from pptx.enum.text import PP_ALIGN
    from pptx.enum.shapes import MSO_SHAPE
    from pptx.oxml import parse_xml

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    # --- Helper Functions ---
    def apply_morph_transition(slide):
        """Injects the native Morph transition into the slide's XML"""
        xml = '''
        <p:transition spd="slow" xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" xmlns:p14="http://schemas.microsoft.com/office/powerpoint/2010/main">
            <p14:morph option="byObject"/>
        </p:transition>
        '''
        transition_elm = parse_xml(xml)
        slide._element.append(transition_elm)

    def add_tracked_text(slide, word, x, y, w, h, size, rgb_color, rotation=0):
        """Creates a text box with forced Morph tracking via the '!!' naming convention"""
        txBox = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
        # Prefixing name with '!!' forces strict Morph object matching in PowerPoint
        txBox.name = f"!!{word}"  
        txBox.rotation = rotation
        
        tf = txBox.text_frame
        tf.word_wrap = False
        p = tf.paragraphs[0]
        p.alignment = PP_ALIGN.LEFT
        run = p.add_run()
        run.text = word
        run.font.name = "Impact"  # Heavy, blocky font
        run.font.size = Pt(size)
        run.font.color.rgb = rgb_color
        return txBox

    def add_shutters(slide, state="open"):
        """Adds cinematic black shutters that close at the end of the sequence"""
        top_y = -3.75 if state == "open" else 0.0
        bot_y = 7.50 if state == "open" else 3.75
        color = RGBColor(33, 43, 54) # Dark Navy
        
        top = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(top_y), Inches(13.333), Inches(3.75))
        top.fill.solid()
        top.fill.fore_color.rgb = color
        top.line.fill.background()
        top.name = "!!TopShutter"
        
        bot = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(bot_y), Inches(13.333), Inches(3.75))
        bot.fill.solid()
        bot.fill.fore_color.rgb = color
        bot.line.fill.background()
        bot.name = "!!BotShutter"

    # Split text into elements (fallback to default sequence if not enough words)
    words = (title_text + " " + body_text).split()
    if len(words) < 9:
        words = ["STUNNING", "TITLES", "USING", "POWERPOINT", "ANIMATION", "FUN", "FAST", "EASY", "EFFECT"]

    w1, w2, w3, w4, w5, w6, w7, w8, w9 = words[:9]

    # --- Colors ---
    c_orange = RGBColor(244, 114, 43)
    c_teal = RGBColor(0, 150, 136)
    c_navy = RGBColor(33, 43, 54)
    c_green = RGBColor(139, 195, 74)
    c_purple = RGBColor(156, 39, 176)
    c_cyan = RGBColor(3, 169, 244)
    c_pink = RGBColor(233, 30, 99)

    # ==========================================
    # SLIDE 1: Intro (Just the title words)
    # ==========================================
    s1 = prs.slides.add_slide(prs.slide_layouts[6])
    add_tracked_text(s1, w1, 4.5, 3.0, 4.0, 1.0, 64, c_orange, 0)
    add_tracked_text(s1, w2, 4.5, 4.0, 4.0, 1.0, 64, c_orange, 0)
    add_shutters(s1, "open")

    # ==========================================
    # SLIDE 2: Morph to left + Reveal Vertical text
    # ==========================================
    s2 = prs.slides.add_slide(prs.slide_layouts[6])
    apply_morph_transition(s2)
    # Move titles to bottom left
    add_tracked_text(s2, w1, 2.5, 5.2, 3.0, 0.8, 44, c_orange, 0)
    add_tracked_text(s2, w2, 2.5, 6.0, 3.0, 0.8, 44, c_orange, 0)
    # Inject verticals
    add_tracked_text(s2, w3, 1.5, 2.5, 3.0, 1.0, 48, c_teal, -90)
    add_tracked_text(s2, w4, 1.5, 2.5, 5.0, 1.0, 56, c_navy, -90)
    add_tracked_text(s2, w5, 3.0, 2.5, 4.0, 1.0, 48, c_teal, -90)
    add_shutters(s2, "open")

    # ==========================================
    # SLIDE 3: The Complete Kinetic Poster
    # ==========================================
    s3 = prs.slides.add_slide(prs.slide_layouts[6])
    apply_morph_transition(s3)
    # Persist left block
    add_tracked_text(s3, w1, 2.5, 5.2, 3.0, 0.8, 44, c_orange, 0)
    add_tracked_text(s3, w2, 2.5, 6.0, 3.0, 0.8, 44, c_orange, 0)
    add_tracked_text(s3, w3, 1.5, 2.5, 3.0, 1.0, 48, c_teal, -90)
    add_tracked_text(s3, w4, 1.5, 2.5, 5.0, 1.0, 56, c_navy, -90)
    add_tracked_text(s3, w5, 3.0, 2.5, 4.0, 1.0, 48, c_teal, -90)
    # Add massive right block
    add_tracked_text(s3, w6, 5.8, 0.5, 4.0, 1.5, 100, c_green, 0)
    add_tracked_text(s3, w7, 5.8, 2.0, 4.0, 1.5, 100, c_purple, 0)
    add_tracked_text(s3, w8, 5.8, 3.5, 4.0, 1.5, 100, c_cyan, 0)
    add_tracked_text(s3, w9, 5.8, 5.0, 4.0, 1.5, 100, c_pink, 0)
    add_shutters(s3, "open")

    # ==========================================
    # SLIDE 4: Shutters Close
    # ==========================================
    s4 = prs.slides.add_slide(prs.slide_layouts[6])
    apply_morph_transition(s4)
    # Persist all text underneath
    add_tracked_text(s4, w1, 2.5, 5.2, 3.0, 0.8, 44, c_orange, 0)
    add_tracked_text(s4, w2, 2.5, 6.0, 3.0, 0.8, 44, c_orange, 0)
    add_tracked_text(s4, w3, 1.5, 2.5, 3.0, 1.0, 48, c_teal, -90)
    add_tracked_text(s4, w4, 1.5, 2.5, 5.0, 1.0, 56, c_navy, -90)
    add_tracked_text(s4, w5, 3.0, 2.5, 4.0, 1.0, 48, c_teal, -90)
    add_tracked_text(s4, w6, 5.8, 0.5, 4.0, 1.5, 100, c_green, 0)
    add_tracked_text(s4, w7, 5.8, 2.0, 4.0, 1.5, 100, c_purple, 0)
    add_tracked_text(s4, w8, 5.8, 3.5, 4.0, 1.5, 100, c_cyan, 0)
    add_tracked_text(s4, w9, 5.8, 5.0, 4.0, 1.5, 100, c_pink, 0)
    # Morph shutters to closed state
    add_shutters(s4, "closed")

    prs.save(output_pptx_path)
    return output_pptx_path
