import os
from PIL import Image, ImageDraw
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.dml import MSO_LINE_DASH_STYLE
from pptx.oxml.xmlchemy import OxmlElement

def create_slide(
    output_pptx_path: str,
    title_text: str = "X",       # Main Concept (e.g., Base)
    body_text: str = "3",        # Exponent or secondary label
    **kwargs,
) -> str:
    """
    Create a 2-slide sequence that visually splits a concept into parts using Morph.
    """
    # Extract dynamic concepts
    main_concept = kwargs.get("main_concept", title_text)
    main_exponent = kwargs.get("main_exponent", body_text)
    sub_concepts = kwargs.get("sub_concepts", ["X", "X", "X"])

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    # === Helper 1: Generate Cinematic Radial Background ===
    bg_path = "radial_bg_split.png"
    def create_background():
        width, height = 1920, 1080
        img = Image.new('RGB', (width, height))
        draw = ImageDraw.Draw(img)
        center_color = (30, 36, 50)
        edge_color = (10, 12, 18)
        max_radius = ((width/2)**2 + (height/2)**2)**0.5
        for i in range(int(max_radius), 0, -5):
            ratio = i / max_radius
            r = int(edge_color[0] * ratio + center_color[0] * (1 - ratio))
            g = int(edge_color[1] * ratio + center_color[1] * (1 - ratio))
            b = int(edge_color[2] * ratio + center_color[2] * (1 - ratio))
            draw.ellipse(
                (width/2 - i, height/2 - i, width/2 + i, height/2 + i),
                fill=(r, g, b)
            )
        img.save(bg_path)
    
    create_background()

    # === Helper 2: Draw Main Title with XML Superscript ===
    def draw_main_title(slide):
        tb = slide.shapes.add_textbox(Inches(4), Inches(0.5), Inches(5.333), Inches(1.5))
        tb.name = "!!MainTitle" # Force Morph match
        p = tb.text_frame.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        
        run_main = p.add_run()
        run_main.text = main_concept
        run_main.font.size = Pt(72)
        run_main.font.bold = True
        run_main.font.name = "Arial"
        run_main.font.color.rgb = RGBColor(255, 255, 255)
        
        if main_exponent:
            run_exp = p.add_run()
            run_exp.text = main_exponent
            run_exp.font.size = Pt(44)
            run_exp.font.bold = True
            run_exp.font.name = "Arial"
            run_exp.font.color.rgb = RGBColor(0, 255, 150)
            
            # Inject baseline offset for superscript via lxml
            rPr = run_exp._r.get_or_add_rPr()
            baseline = OxmlElement('a:baseline')
            baseline.set('val', '40000') # 40% raised
            rPr.append(baseline)

    # Coordinates for the "Split" animation
    center_x = (prs.slide_width / 2) - Inches(1)
    center_y = Inches(3.25)
    target_y = Inches(5.5)

    # ==========================================
    # SLIDE 1: Start State (Stacked in center)
    # ==========================================
    slide1 = prs.slides.add_slide(prs.slide_layouts[6])
    slide1.shapes.add_picture(bg_path, 0, 0, prs.slide_width, prs.slide_height)
    draw_main_title(slide1)

    # Stack the sub-elements perfectly on top of each other
    for i, text in enumerate(sub_concepts):
        box = slide1.shapes.add_textbox(center_x, center_y, Inches(2), Inches(1))
        box.name = f"!!SubNode_{i}" # Critical for Morph mapping
        p = box.text_frame.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        run = p.add_run()
        run.text = text
        run.font.size = Pt(54)
        run.font.bold = True
        run.font.color.rgb = RGBColor(0, 255, 150)

    # ==========================================
    # SLIDE 2: End State (Divergent Spread)
    # ==========================================
    slide2 = prs.slides.add_slide(prs.slide_layouts[6])
    slide2.shapes.add_picture(bg_path, 0, 0, prs.slide_width, prs.slide_height)
    
    n_subs = len(sub_concepts)
    spacing = prs.slide_width / (n_subs + 1)

    # Draw trajectory lines FIRST (so they stay behind text)
    for i in range(n_subs):
        target_x = spacing * (i + 1) - Inches(1)
        line = slide2.shapes.add_connector(
            MSO_SHAPE.LINE, 
            center_x + Inches(1), center_y + Inches(0.5), 
            target_x + Inches(1), target_y
        )
        line.line.color.rgb = RGBColor(0, 255, 150)
        line.line.dash_style = MSO_LINE_DASH_STYLE.DASH
        line.line.width = Pt(2)
        # Add a subtle transparency/shadow effect conceptually (darker line)
        line.line.color.rgb = RGBColor(0, 150, 100)

    # Draw ghost anchor at center
    anchor = slide2.shapes.add_shape(
        MSO_SHAPE.OVAL, 
        center_x + Inches(0.85), center_y + Inches(0.35), 
        Inches(0.3), Inches(0.3)
    )
    anchor.fill.background()
    anchor.line.color.rgb = RGBColor(100, 120, 150)
    anchor.line.dash_style = MSO_LINE_DASH_STYLE.DASH

    # Draw diverged elements
    for i, text in enumerate(sub_concepts):
        target_x = spacing * (i + 1) - Inches(1)
        box = slide2.shapes.add_textbox(target_x, target_y, Inches(2), Inches(1))
        box.name = f"!!SubNode_{i}" # Matches Slide 1 exactly
        p = box.text_frame.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        run = p.add_run()
        run.text = text
        run.font.size = Pt(54)
        run.font.bold = True
        run.font.color.rgb = RGBColor(0, 255, 150)

    draw_main_title(slide2)

    # === Helper 3: Inject Morph Transition ===
    def inject_morph(slide):
        sld = slide.element
        transition = OxmlElement('p:transition')
        transition.set('spd', 'slow')
        morph = OxmlElement('p14:morph')
        morph.set('xmlns:p14', 'http://schemas.microsoft.com/office/powerpoint/2010/main')
        morph.set('option', 'byObject')
        transition.append(morph)

        cSld = sld.find('{http://schemas.openxmlformats.org/presentationml/2006/main}cSld')
        if cSld is not None:
            cSld.addnext(transition)

    inject_morph(slide2)

    prs.save(output_pptx_path)
    
    # Clean up temp bg
    if os.path.exists(bg_path):
        os.remove(bg_path)
        
    return output_pptx_path
