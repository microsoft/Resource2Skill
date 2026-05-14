def create_slide(
    output_pptx_path: str,
    title_text: str = "Chief Financial Officers KPI Dashboard",
    **kwargs,
) -> str:
    """
    Creates a PPTX slide reproducing the "Modern KPI Card Dashboard" style,
    inspired by the CFO dashboard at 00:59 in the source video.

    Returns: path to the saved PPTX file.
    """
    import io
    import math
    from pptx import Presentation
    from pptx.util import Inches, Pt, Emu
    from pptx.dml.color import RGBColor
    from pptx.enum.text import PP_ALIGN
    from pptx.oxml.xmlchemy import OxmlElement
    from PIL import Image, ImageDraw, ImageFont

    # --- Helper Functions ---

    def add_shadow_to_shape(shape):
        """Adds a subtle outer shadow to a shape."""
        shape_element = shape.element
        spPr = shape_element.spPr
        
        effect_list = OxmlElement('a:effectLst')
        
        outer_shadow = OxmlElement('a:outerShdw')
        outer_shadow.set('blurRad', '63500')  # 5pt blur
        outer_shadow.set('dist', '25400')   # 2pt dist
        outer_shadow.set('dir', '2700000')  # 45 degrees
        outer_shadow.set('algn', 'bl')      # Bottom-right
        outer_shadow.set('rotWithShape', '0')
        
        srgb_color = OxmlElement('a:srgbClr')
        srgb_color.set('val', '000000')
        
        alpha = OxmlElement('a:alpha')
        alpha.set('val', '25000')  # 25% transparent
        srgb_color.append(alpha)
        
        outer_shadow.append(srgb_color)
        effect_list.append(outer_shadow)
        spPr.append(effect_list)

    def create_gauge_image(size=(120, 120), percentage=75, color=(46, 179, 120), bg_color=(240, 240, 240)):
        """Creates a circular gauge/progress ring image."""
        img = Image.new("RGBA", size, (255, 255, 255, 0))
        draw = ImageDraw.Draw(img)
        bbox = [(10, 10), (size[0] - 10, size[1] - 10)]
        thickness = 12
        
        # Background ring
        draw.arc(bbox, start=-90, end=270, fill=bg_color, width=thickness)
        
        # Foreground arc
        end_angle = -90 + (percentage * 3.6)
        if percentage > 0:
            draw.arc(bbox, start=-90, end=end_angle, fill=color, width=thickness)
            
        return img
    
    def create_donut_chart_image(size=(200, 200), segments=[(50, (55, 126, 184)), (30, (77, 175, 74)), (20, (255, 255, 51))]):
        """Creates a donut chart image."""
        img = Image.new("RGBA", size, (255, 255, 255, 0))
        draw = ImageDraw.Draw(img)
        bbox = [(10, 10), (size[0] - 10, size[1] - 10)]
        start_angle = -90
        
        for value, color in segments:
            angle = value * 3.6
            draw.pieslice(bbox, start=start_angle, end=start_angle + angle, fill=color)
            start_angle += angle
            
        hole_bbox = [(50, 50), (size[0] - 50, size[1] - 50)]
        draw.ellipse(hole_bbox, fill=(255, 255, 255, 255))
        return img

    def create_kpi_card(slide, left, top, width, height, title, value, sub_text, percentage, status='positive'):
        """Creates a complete KPI card widget."""
        card_shape = slide.shapes.add_shape(1, left, top, width, height) # 1 is rect
        card_shape.fill.solid()
        card_shape.fill.fore_color.rgb = RGBColor(255, 255, 255)
        card_shape.line.fill.solid()
        card_shape.line.fill.fore_color.rgb = RGBColor(230, 230, 230)
        add_shadow_to_shape(card_shape)
        
        # Title
        tb = slide.shapes.add_textbox(left + Inches(0.2), top + Inches(0.15), width - Inches(0.4), Inches(0.3))
        p = tb.text_frame.paragraphs[0]
        p.text = title
        p.font.size = Pt(11)
        p.font.color.rgb = RGBColor(89, 89, 89)

        # Main Value
        tb_val = slide.shapes.add_textbox(left + Inches(0.2), top + Inches(0.5), width - Inches(1.4), Inches(0.5))
        p_val = tb_val.text_frame.paragraphs[0]
        p_val.text = value
        p_val.font.size = Pt(22)
        p_val.font.bold = True
        p_val.font.color.rgb = RGBColor(0, 0, 0)

        # Sub Text
        if status == 'positive':
            color = (46, 179, 120)
            icon = "▲"
        elif status == 'negative':
            color = (230, 83, 83)
            icon = "▼"
        else:
            color = (89, 89, 89)
            icon = ""
        
        tb_sub = slide.shapes.add_textbox(left + Inches(0.2), top + Inches(0.85), width - Inches(1.4), Inches(0.3))
        p_sub = tb_sub.text_frame.paragraphs[0]
        run = p_sub.add_run()
        run.text = f"{icon} {sub_text}"
        run.font.size = Pt(9)
        run.font.color.rgb = RGBColor(*color)
        
        # Gauge Image
        gauge_img = create_gauge_image(percentage=percentage, color=color)
        img_stream = io.BytesIO()
        gauge_img.save(img_stream, format="PNG")
        slide.shapes.add_picture(img_stream, left + width - Inches(1.1), top + Inches(0.3), height=Inches(0.9))

    # --- Presentation Setup ---
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide_layout = prs.slide_layouts[6]  # Blank layout
    slide = prs.slides.add_slide(slide_layout)

    # Set background color
    background = slide.background
    background.fill.solid()
    background.fill.fore_color.rgb = RGBColor(248, 249, 250)

    # --- Slide Content ---
    # Title
    title_shape = slide.shapes.add_textbox(Inches(0.5), Inches(0.2), Inches(12), Inches(0.75))
    title_shape.text_frame.paragraphs[0].text = title_text
    title_shape.text_frame.paragraphs[0].font.size = Pt(32)
    title_shape.text_frame.paragraphs[0].font.bold = True
    
    # KPI Card Data
    kpis = [
        {'title': 'Revenue', 'value': '$10,088,844', 'sub': '(+2%)', 'perc': 84, 'status': 'positive'},
        {'title': 'Gross Profit', 'value': '$6,588,844', 'sub': '(+2%)', 'perc': 65, 'status': 'positive'},
        {'title': 'EBIT', 'value': '$3,588,844', 'sub': '(+4%)', 'perc': 70, 'status': 'positive'},
        {'title': 'EBIT %', 'value': '35.6%', 'sub': '(+0.4%)', 'perc': 36, 'status': 'positive'},
        {'title': 'Operating Expenses', 'value': '$2,988,844', 'sub': '(-3%)', 'perc': 45, 'status': 'negative'},
        {'title': 'Net Income', 'value': '$2,988,844', 'sub': '(-5%)', 'perc': 30, 'status': 'negative'},
    ]

    # Layout dimensions
    card_w, card_h = Inches(3.8), Inches(1.5)
    gutter_x, gutter_y = Inches(0.3), Inches(0.3)
    start_x, start_y = Inches(0.5), Inches(1.2)
    
    # Create KPI Cards
    for i, kpi in enumerate(kpis):
        col = i % 2
        row = i // 2
        left = start_x + col * (card_w + gutter_x)
        top = start_y + row * (card_h + gutter_y)
        create_kpi_card(slide, left, top, card_w, card_h, kpi['title'], kpi['value'], kpi['sub'], kpi['perc'], kpi['status'])

    # --- Right Column: Donut Charts ---
    right_col_x = start_x + 2 * (card_w + gutter_x)

    # Costs Breakdown Card
    card_shape = slide.shapes.add_shape(1, right_col_x, start_y, card_w, Inches(2.4))
    card_shape.fill.solid()
    card_shape.fill.fore_color.rgb = RGBColor(255, 255, 255)
    card_shape.line.fill.solid()
    card_shape.line.fill.fore_color.rgb = RGBColor(230, 230, 230)
    add_shadow_to_shape(card_shape)
    tb = slide.shapes.add_textbox(right_col_x + Inches(0.2), start_y + Inches(0.15), card_w - Inches(0.4), Inches(0.3))
    tb.text_frame.paragraphs[0].text = "Breakdowns Costs"
    tb.text_frame.paragraphs[0].font.size = Pt(11)

    donut_img = create_donut_chart_image(segments=[(50, (55, 126, 184)), (25, (77, 175, 74)), (15, (255, 127, 0)), (10, (255, 255, 51))])
    img_stream = io.BytesIO()
    donut_img.save(img_stream, format="PNG")
    slide.shapes.add_picture(img_stream, right_col_x + Inches(0.7), start_y + Inches(0.5), height=Inches(1.8))
    
    # Revenue Breakdown Card
    rev_card_top = start_y + Inches(2.4) + gutter_y
    card_shape = slide.shapes.add_shape(1, right_col_x, rev_card_top, card_w, Inches(2.4))
    card_shape.fill.solid()
    card_shape.fill.fore_color.rgb = RGBColor(255, 255, 255)
    card_shape.line.fill.solid()
    card_shape.line.fill.fore_color.rgb = RGBColor(230, 230, 230)
    add_shadow_to_shape(card_shape)
    tb = slide.shapes.add_textbox(right_col_x + Inches(0.2), rev_card_top + Inches(0.15), card_w - Inches(0.4), Inches(0.3))
    tb.text_frame.paragraphs[0].text = "Revenue"
    tb.text_frame.paragraphs[0].font.size = Pt(11)
    
    donut_img_2 = create_donut_chart_image(segments=[(70, (46, 179, 120)), (20, (55, 126, 184)), (10, (152, 78, 163))])
    img_stream = io.BytesIO()
    donut_img_2.save(img_stream, format="PNG")
    slide.shapes.add_picture(img_stream, right_col_x + Inches(0.7), rev_card_top + Inches(0.5), height=Inches(1.8))


    # --- Save Presentation ---
    prs.save(output_pptx_path)
    return output_pptx_path
