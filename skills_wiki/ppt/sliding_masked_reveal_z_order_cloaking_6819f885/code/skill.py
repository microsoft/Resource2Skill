def create_slide(
    output_pptx_path: str,
    title_text: str = "SUBSCRIBE",
    body_text: str = "TO OUR CHANNEL",
    bg_palette: str = "dark",  
    accent_color: tuple = (255, 50, 80),  # RGB accent color (Neon Pink/Red)
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the 'Sliding Masked Reveal' visual effect.
    This generates a static slide in the "mid-reveal" state to showcase the masked text illusion.
    
    Returns: path to the saved PPTX file.
    """
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    from pptx.enum.shapes import MSO_SHAPE
    from pptx.oxml import OxmlElement

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6]) # Blank layout

    # === Helper Functions for Advanced XML Manipulation ===
    ns = 'http://schemas.openxmlformats.org/drawingml/2006/main'

    def remove_line(shape):
        """Removes the outline from a shape to ensure seamless masking."""
        spPr = shape.element.spPr
        ln = spPr.find(f'{{{ns}}}ln')
        if ln is not None:
            for child in ln:
                ln.remove(child)
            ln.append(OxmlElement('a:noFill'))

    def apply_bg_fill(shape):
        """Applies Slide Background Fill to act as a cloaking device."""
        spPr = shape.element.spPr
        # Remove any existing standard fills
        for fill_type in ['noFill', 'solidFill', 'gradFill', 'blipFill', 'pattFill', 'grpFill', 'bgFill']:
            el = spPr.find(f'{{{ns}}}{fill_type}')
            if el is not None:
                spPr.remove(el)
        
        # Inject the <a:bgFill> element
        bgFill = OxmlElement('a:bgFill')
        insert_after = None
        for tag in ['xfrm', 'prstGeom', 'custGeom']:
            el = spPr.find(f'{{{ns}}}{tag}')
            if el is not None:
                insert_after = el
        
        if insert_after is not None:
            insert_after.addnext(bgFill)
        else:
            spPr.insert(0, bgFill)
        remove_line(shape)

    def apply_glow(shape, color_rgb, radius_pt=10):
        """Adds a vibrant neon glow effect around the shape."""
        spPr = shape.element.spPr
        effectLst = spPr.find(f'{{{ns}}}effectLst')
        if effectLst is None:
            effectLst = OxmlElement('a:effectLst')
            extLst = spPr.find(f'{{{ns}}}extLst')
            if extLst is not None:
                extLst.addprevious(effectLst)
            else:
                spPr.append(effectLst)
        
        glow = OxmlElement('a:glow')
        glow.set('rad', str(int(radius_pt * 12700))) # Convert Pt to EMUs
        srgbClr = OxmlElement('a:srgbClr')
        srgbClr.set('val', f'{color_rgb[0]:02X}{color_rgb[1]:02X}{color_rgb[2]:02X}')
        alpha = OxmlElement('a:alpha')
        alpha.set('val', '60000') # 60% opacity for the glow
        srgbClr.append(alpha)
        glow.append(srgbClr)
        effectLst.append(glow)

    # === Layer 0: Slide Background ===
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(20, 22, 28) # Deep Tech Navy

    # === Layer 1: Text Boxes (Placed behind the Mask) ===
    # These text boxes are intentionally positioned to intersect the mask boundary
    tx1 = slide.shapes.add_textbox(Inches(1.5), Inches(2.5), Inches(8.0), Inches(1.5))
    tf1 = tx1.text_frame
    tf1.text = title_text.upper()
    p1 = tf1.paragraphs[0]
    p1.font.name = 'Arial Black'
    p1.font.size = Pt(76)
    p1.font.color.rgb = RGBColor(255, 255, 255)

    tx2 = slide.shapes.add_textbox(Inches(2.5), Inches(4.0), Inches(6.0), Inches(1.0))
    tf2 = tx2.text_frame
    tf2.text = body_text.upper()
    p2 = tf2.paragraphs[0]
    p2.font.name = 'Arial'
    p2.font.size = Pt(32)
    p2.font.color.rgb = RGBColor(180, 180, 190)

    # === Layer 2: The Cloaking Mask ===
    # A rectangle covering the left side of the slide.
    # Because of `a:bgFill`, it perfectly mirrors the slide background, hiding the left half of the text.
    mask = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE,
        Inches(0), Inches(0), Inches(4.5), Inches(7.5)
    )
    apply_bg_fill(mask)

    # === Layer 3: The Divider Line (Placed in front of the mask) ===
    # Placed exactly on the seam of the mask to create the emergence point
    divider = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE,
        Inches(4.45), Inches(2.0), Inches(0.1), Inches(3.5)
    )
    divider.fill.solid()
    divider.fill.fore_color.rgb = RGBColor(*accent_color)
    remove_line(divider)
    apply_glow(divider, accent_color, radius_pt=15)

    # === Layer 4: Accent Element (Play/Action Arrow) ===
    arrow = slide.shapes.add_shape(
        MSO_SHAPE.ISOSCELES_TRIANGLE,
        Inches(10.0), Inches(4.1), Inches(0.3), Inches(0.4)
    )
    arrow.rotation = 90
    arrow.fill.solid()
    arrow.fill.fore_color.rgb = RGBColor(*accent_color)
    remove_line(arrow)
    apply_glow(arrow, accent_color, radius_pt=8)

    prs.save(output_pptx_path)
    return output_pptx_path
