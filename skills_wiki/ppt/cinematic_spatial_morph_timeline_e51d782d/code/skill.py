def create_slide(
    output_pptx_path: str,
    title_text: str = "THE ROMAN EMPIRE",
    events: list = None,
    bg_image_url: str = "https://images.unsplash.com/photo-1549886314-2579b29150b0?w=1600&q=80",
    **kwargs,
) -> str:
    """
    Creates a cinematic, morphing spatial timeline presentation.
    
    Args:
        output_pptx_path: Path to save the PPTX.
        title_text: Text for the hero slide.
        events: List of dicts [{'date': '753 BCE', 'title': 'Rome is Founded', 'desc': 'Legendary event...'}].
        bg_image_url: URL for the title slide background.
    """
    import os
    import urllib.request
    from io import BytesIO
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.enum.text import PP_ALIGN
    from pptx.enum.shapes import MSO_SHAPE
    from pptx.dml.color import RGBColor
    from PIL import Image, ImageEnhance
    from lxml import etree

    # Default data if none provided
    if not events:
        events = [
            {"date": "753 BCE", "title": "Rome is founded", "desc": "Rome was believed to have been founded by Romulus and Remus."},
            {"date": "509 BCE", "title": "Rome becomes a republic", "desc": "The Roman Republic was characterized by a system of government where power was held by elected officials."},
            {"date": "27 BCE", "title": "The Roman Empire begins", "desc": "Augustus Caesar becomes the first emperor of Rome."}
        ]

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # --- HELPER: Inject Morph Transition ---
    def apply_morph_transition(slide):
        """Injects PowerPoint Morph transition XML into the slide."""
        transition_xml = '''
        <p:transition xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" 
                      xmlns:p14="http://schemas.microsoft.com/office/powerpoint/2010/main" 
                      spd="slow">
            <p14:morph option="byObject"/>
        </p:transition>
        '''
        morph_el = etree.fromstring(transition_xml)
        slide._element.append(morph_el)

    # --- HELPER: Set Solid Black Background ---
    def set_black_background(slide):
        bg_xml = '''
        <p:bg xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" 
              xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">
            <p:bgPr>
                <a:solidFill><a:srgbClr val="000000"/></a:solidFill>
                <a:effectLst/>
            </p:bgPr>
        </p:bg>
        '''
        bg_el = etree.fromstring(bg_xml)
        slide._element.insert(1, bg_el)

    # --- LAYER 1: TITLE SLIDE (PIL Compositing) ---
    slide_title = prs.slides.add_slide(blank_layout)
    set_black_background(slide_title)
    
    bg_img_path = "temp_bg.png"
    try:
        # Download and process image to make it dark and cinematic
        req = urllib.request.Request(bg_image_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            img = Image.open(BytesIO(response.read())).convert("RGBA")
            
            # Crop to 16:9
            target_ratio = 16 / 9
            w, h = img.size
            if w / h > target_ratio:
                new_w = int(h * target_ratio)
                img = img.crop(((w - new_w) // 2, 0, (w + new_w) // 2, h))
            else:
                new_h = int(w / target_ratio)
                img = img.crop((0, (h - new_h) // 2, w, (h + new_h) // 2))
            
            # Apply 70% dark overlay
            overlay = Image.new("RGBA", img.size, (0, 0, 0, int(255 * 0.75)))
            img = Image.alpha_composite(img, overlay)
            
            # Warm tint
            enhancer = ImageEnhance.Color(img)
            img = enhancer.enhance(0.5)
            
            img.save(bg_img_path)
            slide_title.shapes.add_picture(bg_img_path, 0, 0, prs.slide_width, prs.slide_height)
    except Exception as e:
        print(f"Image download failed: {e}. Proceeding with black background.")

    # Add Title Text
    tb = slide_title.shapes.add_textbox(Inches(1), Inches(2.5), Inches(11.333), Inches(2))
    p = tb.text_frame.paragraphs[0]
    p.text = title_text
    p.alignment = PP_ALIGN.CENTER
    font = p.font
    font.name = "Georgia"  # Standard serif alternative
    font.size = Pt(64)
    font.color.rgb = RGBColor(255, 255, 255)

    # --- LAYER 2: TIMELINE SLIDES (Spatial Math & Morph) ---
    
    # Coordinates and sizing
    slide_w = 13.333
    center_y = 3.0
    center_x = slide_w / 2.0
    node_size = 0.15

    for slide_index in range(len(events)):
        slide = prs.slides.add_slide(blank_layout)
        set_black_background(slide)
        
        # Apply Morph to all timeline slides except the first one (from the title)
        if slide_index > 0:
            apply_morph_transition(slide)

        # Draw elements for all events to maintain spatial continuity
        # We render the current event, the previous one, and the next one (off-screen)
        for event_index, event in enumerate(events):
            
            # Calculate where this event belongs on THIS slide
            # If event_index == slide_index, it's at center_x.
            # If event_index > slide_index, it's pushed to the right by multiples of slide width.
            relative_offset = event_index - slide_index
            x_pos = center_x + (relative_offset * slide_w)
            
            # Only draw if it's within 1 slide width off-screen (optimization)
            if -slide_w <= x_pos <= 2 * slide_w:
                
                # 1. Timeline Line (Connects current node to the next)
                line = slide.shapes.add_connector(
                    1, # straight connector
                    Inches(x_pos), Inches(center_y),
                    Inches(x_pos + slide_w), Inches(center_y)
                )
                line.line.color.rgb = RGBColor(255, 255, 255)
                line.line.width = Pt(1.5)

                # 2. Node Circle
                node = slide.shapes.add_shape(
                    MSO_SHAPE.OVAL,
                    Inches(x_pos - (node_size/2)), Inches(center_y - (node_size/2)),
                    Inches(node_size), Inches(node_size)
                )
                node.fill.solid()
                node.fill.fore_color.rgb = RGBColor(255, 255, 255)
                node.line.fill.background() # No outline

                # 3. Date Text (Above Node)
                date_tb = slide.shapes.add_textbox(Inches(x_pos - 2), Inches(center_y - 0.8), Inches(4), Inches(0.5))
                dp = date_tb.text_frame.paragraphs[0]
                dp.text = event["date"]
                dp.alignment = PP_ALIGN.CENTER
                dp.font.name = "Georgia"
                dp.font.size = Pt(20)
                dp.font.color.rgb = RGBColor(222, 208, 185) # Sand/Gold color

                # 4. Title Text (Below Node)
                title_tb = slide.shapes.add_textbox(Inches(x_pos - 3), Inches(center_y + 0.3), Inches(6), Inches(0.8))
                tp = title_tb.text_frame.paragraphs[0]
                tp.text = event["title"]
                tp.alignment = PP_ALIGN.CENTER
                tp.font.name = "Georgia"
                tp.font.size = Pt(36)
                tp.font.color.rgb = RGBColor(255, 255, 255)

                # 5. Description Text
                desc_tb = slide.shapes.add_textbox(Inches(x_pos - 3), Inches(center_y + 1.2), Inches(6), Inches(1.5))
                desc_tb.text_frame.word_wrap = True
                dcp = desc_tb.text_frame.paragraphs[0]
                dcp.text = event["desc"]
                dcp.alignment = PP_ALIGN.CENTER
                dcp.font.name = "Arial"
                dcp.font.size = Pt(14)
                dcp.font.color.rgb = RGBColor(180, 180, 180)

    prs.save(output_pptx_path)
    
    # Cleanup temporary files
    if os.path.exists(bg_img_path):
        os.remove(bg_img_path)
        
    return output_pptx_path
