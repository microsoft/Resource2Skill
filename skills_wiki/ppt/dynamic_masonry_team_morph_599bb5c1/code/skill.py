import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN
from pptx.oxml.xmlchemy import OxmlElement
from PIL import Image, ImageDraw, ImageFont

def _create_placeholder_portrait(color_rgb, initials, filename):
    """Generates a stylish solid-color portrait placeholder using PIL."""
    w, h = 600, 600
    img = Image.new('RGB', (w, h), color_rgb)
    draw = ImageDraw.Draw(img)
    
    # Add a subtle dark gradient at the bottom for depth
    for y in range(h):
        alpha = int(255 * (y / h) * 0.3)
        overlay = Image.new('RGBA', (w, 1), (0, 0, 0, alpha))
        img.paste(overlay, (0, y), overlay)
        
    # Draw initials as a logo/face replacement
    try:
        font = ImageFont.truetype("arialbd.ttf", 200)
    except IOError:
        font = ImageFont.load_default()
    
    # Center text roughly
    draw.text((w/2 - 100, h/2 - 100), initials, font=font, fill=(255, 255, 255, 180))
    img.save(filename)
    return filename

def _set_text_outline(run, hex_color="E0E0E0", width_pt=2):
    """Uses lxml to inject stroke/outline properties into a text run, removing solid fill."""
    rPr = run._r.get_or_add_rPr()
    
    # Create Line element
    ln = OxmlElement('a:ln')
    ln.set('w', str(int(width_pt * 12700))) # convert pt to EMUs
    solidFill = OxmlElement('a:solidFill')
    srgbClr = OxmlElement('a:srgbClr')
    srgbClr.set('val', hex_color)
    solidFill.append(srgbClr)
    ln.append(solidFill)
    
    # Create NoFill element
    noFill = OxmlElement('a:noFill')
    
    rPr.append(ln)
    rPr.append(noFill)

def _add_morph_transition(slide):
    """Injects the Morph transition into the slide XML."""
    transition = OxmlElement('p:transition')
    transition.set('spd', 'slow')
    morph = OxmlElement('p:morph')
    morph.set('option', 'byObject')
    transition.append(morph)
    slide.element.append(transition)

def create_slide(output_pptx_path: str, **kwargs) -> str:
    """
    Creates a 2-slide presentation showcasing the dynamic masonry team morph.
    """
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    # Define Team Members & Generate Images
    team = [
        {"id": "1", "name": "Sophia\nWhite", "title": "Brand Strategist", "color": (32, 178, 170), "init": "SW"},
        {"id": "2", "name": "Eva\nRodriguez", "title": "PR Executive", "color": (235, 87, 142), "init": "ER"},
        {"id": "3", "name": "Ethan\nTurner", "title": "Video Maestro", "color": (253, 203, 88), "init": "ET"},
        {"id": "4", "name": "Jackson\nSmith", "title": "Lead Copywriter", "color": (146, 102, 204), "init": "JS"},
        {"id": "5", "name": "Caleb\nDavis", "title": "Social Media Wizard", "color": (255, 140, 0), "init": "CD"},
        {"id": "6", "name": "Emily\nLewis", "title": "Events Genius", "color": (67, 181, 129), "init": "EL"},
    ]
    
    for member in team:
        filename = f"temp_portrait_{member['id']}.jpg"
        _create_placeholder_portrait(member["color"], member["init"], filename)
        member["img"] = filename

    # Define the 6 masonry slots (Left, Top, Width, Height)
    slots = [
        (6.0, 1.5, 3.5, 4.5), # Slot 0: HERO (Center Right)
        (9.8, 1.2, 1.8, 2.0), # Slot 1: Top Right
        (9.8, 3.5, 2.0, 2.0), # Slot 2: Mid Right
        (12.1, 2.0, 1.0, 1.5),# Slot 3: Far Right Edge
        (4.5, 0.8, 1.2, 1.2), # Slot 4: Top Left (Peeking)
        (4.2, 5.0, 1.5, 1.5), # Slot 5: Bottom Left
    ]

    # Slide 1 mapping (Member index -> Slot index)
    mapping_slide_1 = [0, 1, 2, 3, 4, 5]
    # Slide 2 mapping (Rotate so Member 1 becomes Hero, Member 0 moves to background)
    mapping_slide_2 = [1, 0, 5, 2, 3, 4]
    
    mappings = [mapping_slide_1, mapping_slide_2]
    
    for slide_idx, mapping in enumerate(mappings):
        slide = prs.slides.add_slide(prs.slide_layouts[6]) # Blank slide
        hero_member = team[mapping.index(0)] # Find who is in Slot 0
        
        # --- LAYER 1: Background Outlined Text ---
        bg_text = slide.shapes.add_textbox(Inches(6.0), Inches(5.5), Inches(7.0), Inches(1.5))
        bg_tf = bg_text.text_frame
        bg_tf.word_wrap = False
        p = bg_tf.add_paragraph()
        run = p.add_run()
        run.text = "OUR TEAM"
        run.font.size = Pt(110)
        run.font.name = "Arial Black"
        _set_text_outline(run, hex_color="EAEAEA", width_pt=2)
        
        # --- LAYER 2: Image Collage ---
        for member_idx, slot_idx in enumerate(mapping):
            member = team[member_idx]
            x, y, w, h = slots[slot_idx]
            
            # Create rounded rectangle
            shape = slide.shapes.add_shape(
                MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h)
            )
            # EXTREMELY IMPORTANT: Naming shapes with "!!" forces Morph to connect them across slides
            shape.name = f"!!Portrait_{member['id']}" 
            
            # Fill with picture and remove border
            shape.fill.user_picture(member["img"])
            shape.line.fill.background()
            
            # Adjust rounding radius via XML injection for a modern look (~10%)
            for adj in shape.element.xpath('.//a:adjLst/a:adj'):
                adj.set('idx', '2')
                adj.set('val', '10000') 

        # --- LAYER 3: Text Content (Left Side) ---
        # Main Title
        tx_box = slide.shapes.add_textbox(Inches(0.8), Inches(2.0), Inches(4.0), Inches(2.0))
        tf = tx_box.text_frame
        
        lines = hero_member["name"].split('\n')
        p1 = tf.add_paragraph()
        r1 = p1.add_run()
        r1.text = lines[0]
        r1.font.size = Pt(54)
        r1.font.color.rgb = RGBColor(*hero_member["color"])
        
        p2 = tf.add_paragraph()
        r2 = p2.add_run()
        r2.text = lines[1]
        r2.font.size = Pt(54)
        r2.font.bold = True
        r2.font.color.rgb = RGBColor(*hero_member["color"])
        
        # Accent Line
        line = slide.shapes.add_connector(
            MSO_SHAPE.LINE_INVERSE, Inches(0.8), Inches(4.2), Inches(3.0), Inches(4.2)
        )
        line.line.color.rgb = RGBColor(200, 200, 200)
        line.line.width = Pt(1.5)
        
        # Role & Bio
        bio_box = slide.shapes.add_textbox(Inches(0.8), Inches(4.5), Inches(3.5), Inches(1.5))
        bio_tf = bio_box.text_frame
        bio_tf.word_wrap = True
        bp = bio_tf.add_paragraph()
        bp.text = f"{hero_member['title']} with a golden touch. Transforms startups into household names with unparalleled creative direction."
        bp.font.size = Pt(14)
        bp.font.color.rgb = RGBColor(100, 100, 100)
        
        # Add Transition
        if slide_idx > 0:
            _add_morph_transition(slide)

    prs.save(output_pptx_path)
    
    # Cleanup temporary images
    for member in team:
        if os.path.exists(member["img"]):
            os.remove(member["img"])
            
    return output_pptx_path
