def create_gradient_doughnut_charts(
    output_pptx_path: str,
    title_text: str = "DOUGHNUT CHARTS",
    bg_color: tuple = (22, 22, 24), # Dark charcoal background
) -> str:
    """
    Create a PPTX file reproducing the elegant, glowing gradient doughnut charts.
    """
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    from pptx.enum.text import PP_ALIGN
    from pptx.enum.shapes import MSO_SHAPE
    from lxml import etree
    from pptx.oxml.ns import qn

    # Define chart data: (percentage, title, desc, start_hex, end_hex)
    charts_data = [
        (0.60, "CHART 1", "Insert some awesome text right here. Just remember keep it short and sweet.", "00BFFF", "0000FF"),
        (0.75, "CHART 2", "Insert some awesome text right here. Just remember keep it short and sweet.", "FF00FF", "800080"),
        (0.90, "CHART 3", "Insert some awesome text right here. Just remember keep it short and sweet.", "FF1493", "FF8C00")
    ]

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6]) # Blank layout

    # Set background
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(*bg_color)

    # Helper 1: Transparent fill injection
    def make_transparent_fill(shape):
        spPr = shape.element.spPr
        for tag in ['a:solidFill', 'a:gradFill', 'a:pattFill', 'a:blipFill']:
            fill_el = spPr.find(qn(tag))
            if fill_el is not None:
                spPr.remove(fill_el)
        geom = spPr.find(qn('a:prstGeom'))
        if geom is not None and spPr.find(qn('a:noFill')) is None:
            noFill = etree.Element(qn('a:noFill'))
            geom.addnext(noFill)

    # Helper 2: Inject Gradient Line and Rounded Cap
    def apply_gradient_stroke(shape, hex_start, hex_end, width_pt=35):
        # Trigger native line creation to establish strict XML order
        shape.line.width = Pt(width_pt)
        shape.line.color.rgb = RGBColor(255, 255, 255) 
        
        spPr = shape.element.spPr
        ln = spPr.find(qn('a:ln'))
        ln.set('cap', 'rnd') # Rounded cap

        # Remove solid line fill
        solid = ln.find(qn('a:solidFill'))
        if solid is not None:
            ln.remove(solid)

        # Build gradient fill
        gradFill = etree.SubElement(ln, qn('a:gradFill'))
        gsLst = etree.SubElement(gradFill, qn('a:gsLst'))
        
        gs1 = etree.SubElement(gsLst, qn('a:gs'))
        gs1.set('pos', '0')
        clr1 = etree.SubElement(gs1, qn('a:srgbClr'))
        clr1.set('val', hex_start.replace('#', ''))
        
        gs2 = etree.SubElement(gsLst, qn('a:gs'))
        gs2.set('pos', '100000') # 100%
        clr2 = etree.SubElement(gs2, qn('a:srgbClr'))
        clr2.set('val', hex_end.replace('#', ''))
        
        lin = etree.SubElement(gradFill, qn('a:lin'))
        lin.set('ang', '2700000') # 45 degree gradient sweep
        lin.set('scaled', '1')

    # Helper 3: Inject Exact Sweep Adjustments
    def apply_arc_sweep(shape, pct):
        geom = shape.element.spPr.find(qn('a:prstGeom'))
        avLst = geom.find(qn('a:avLst'))
        if avLst is None:
            avLst = etree.SubElement(geom, qn('a:avLst'))
        for gd in list(avLst):
            avLst.remove(gd)
        
        # PPT angles: 270 is Top (12 o'clock). 60000 units per degree.
        start_angle = 270
        sweep_angle = pct * 360
        end_angle = start_angle + sweep_angle
        
        gd1 = etree.SubElement(avLst, qn('a:gd'))
        gd1.set('name', 'adj1')
        gd1.set('fmla', f'val {int(start_angle * 60000)}')
        
        gd2 = etree.SubElement(avLst, qn('a:gd'))
        gd2.set('name', 'adj2')
        gd2.set('fmla', f'val {int(end_angle * 60000)}')

    # Main Title
    tx_box = slide.shapes.add_textbox(Inches(0), Inches(0.5), Inches(13.333), Inches(1))
    tf = tx_box.text_frame
    tf.text = title_text
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    p.font.name = 'Arial'
    p.font.size = Pt(36)
    p.font.bold = True
    p.font.color.rgb = RGBColor(230, 230, 230)

    # Calculate layout parameters
    chart_size = Inches(2.8)
    spacing = Inches(13.333) / (len(charts_data) + 1)
    y_center = Inches(3.2)
    top_pos = y_center - chart_size/2

    for i, data in enumerate(charts_data):
        pct, title, desc, hex_start, hex_end = data
        x_center = spacing * (i + 1)
        left_pos = x_center - chart_size/2

        # 1. Doughnut Track (Underlay)
        track = slide.shapes.add_shape(MSO_SHAPE.OVAL, left_pos, top_pos, chart_size, chart_size)
        make_transparent_fill(track)
        track.line.width = Pt(35)
        track.line.color.rgb = RGBColor(40, 40, 42) # Subtle track color

        # 2. Doughnut Arc (Overlay Gradient)
        arc = slide.shapes.add_shape(MSO_SHAPE.ARC, left_pos, top_pos, chart_size, chart_size)
        make_transparent_fill(arc)
        apply_gradient_stroke(arc, hex_start, hex_end, width_pt=35)
        apply_arc_sweep(arc, pct)

        # 3. Center Percentage Text
        pct_box = slide.shapes.add_textbox(left_pos, y_center - Inches(0.4), chart_size, Inches(0.8))
        tf = pct_box.text_frame
        tf.text = f"{int(pct*100)}%"
        p = tf.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        p.font.name = 'Arial'
        p.font.size = Pt(44)
        p.font.bold = True
        p.font.color.rgb = RGBColor(255, 255, 255)

        # 4. Label & Description
        label_box = slide.shapes.add_textbox(x_center - Inches(1.5), top_pos + chart_size + Inches(0.3), Inches(3), Inches(0.5))
        tf_lbl = label_box.text_frame
        tf_lbl.text = title
        p_lbl = tf_lbl.paragraphs[0]
        p_lbl.alignment = PP_ALIGN.CENTER
        p_lbl.font.name = 'Arial'
        p_lbl.font.size = Pt(22)
        p_lbl.font.bold = True
        p_lbl.font.color.rgb = RGBColor(220, 220, 220)

        desc_box = slide.shapes.add_textbox(x_center - Inches(1.5), top_pos + chart_size + Inches(0.8), Inches(3), Inches(0.8))
        tf_desc = desc_box.text_frame
        tf_desc.word_wrap = True
        tf_desc.text = desc
        p_desc = tf_desc.paragraphs[0]
        p_desc.alignment = PP_ALIGN.CENTER
        p_desc.font.name = 'Arial'
        p_desc.font.size = Pt(12)
        p_desc.font.color.rgb = RGBColor(150, 150, 150)

    prs.save(output_pptx_path)
    return output_pptx_path
