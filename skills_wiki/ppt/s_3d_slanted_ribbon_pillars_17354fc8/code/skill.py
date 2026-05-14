def create_slide(
    output_pptx_path: str,
    title_text: str = "4 OPTIONS INFOGRAPHICS IN POWERPOINT",
    **kwargs,
) -> str:
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    from pptx.enum.shapes import MSO_SHAPE
    from lxml import etree

    # Helpers for XML Injection
    def inject_gradient(shape, color1, color2):
        spPr = shape.element.spPr
        for child in spPr:
            if child.tag.endswith('Fill'):
                spPr.remove(child)
                
        gradFill = etree.SubElement(spPr, '{http://schemas.openxmlformats.org/drawingml/2006/main}gradFill')
        lin = etree.SubElement(gradFill, '{http://schemas.openxmlformats.org/drawingml/2006/main}lin')
        lin.set('ang', '5400000') # 90 degrees (top to bottom)
        
        gsLst = etree.SubElement(gradFill, '{http://schemas.openxmlformats.org/drawingml/2006/main}gsLst')
        
        # Stop 1
        gs1 = etree.SubElement(gsLst, '{http://schemas.openxmlformats.org/drawingml/2006/main}gs')
        gs1.set('pos', '0')
        srgb1 = etree.SubElement(gs1, '{http://schemas.openxmlformats.org/drawingml/2006/main}srgbClr')
        srgb1.set('val', f"{color1[0]:02X}{color1[1]:02X}{color1[2]:02X}")
        
        # Stop 2
        gs2 = etree.SubElement(gsLst, '{http://schemas.openxmlformats.org/drawingml/2006/main}gs')
        gs2.set('pos', '100000')
        srgb2 = etree.SubElement(gs2, '{http://schemas.openxmlformats.org/drawingml/2006/main}srgbClr')
        srgb2.set('val', f"{color2[0]:02X}{color2[1]:02X}{color2[2]:02X}")

    def inject_shadow(shape):
        spPr = shape.element.spPr
        effectLst = spPr.find('{http://schemas.openxmlformats.org/drawingml/2006/main}effectLst')
        if effectLst is None:
            effectLst = etree.SubElement(spPr, '{http://schemas.openxmlformats.org/drawingml/2006/main}effectLst')
        outerShdw = etree.SubElement(effectLst, '{http://schemas.openxmlformats.org/drawingml/2006/main}outerShdw')
        outerShdw.set('blurRad', '127000') # 10pt blur
        outerShdw.set('dist', '63500')     # 5pt distance
        outerShdw.set('dir', '2700000')    # 45 degrees
        outerShdw.set('algn', 'tl')
        
        srgbClr = etree.SubElement(outerShdw, '{http://schemas.openxmlformats.org/drawingml/2006/main}srgbClr')
        srgbClr.set('val', '000000')
        alpha = etree.SubElement(srgbClr, '{http://schemas.openxmlformats.org/drawingml/2006/main}alpha')
        alpha.set('val', '25000') # 25% opacity

    def set_text_transparency(shape, alpha_percent):
        for p in shape.text_frame.paragraphs:
            for r in p.runs:
                rPr = r._r.get_or_add_rPr()
                solidFill = rPr.find('{http://schemas.openxmlformats.org/drawingml/2006/main}solidFill')
                if solidFill is None:
                    solidFill = etree.SubElement(rPr, '{http://schemas.openxmlformats.org/drawingml/2006/main}solidFill')
                srgbClr = solidFill.find('{http://schemas.openxmlformats.org/drawingml/2006/main}srgbClr')
                if srgbClr is None:
                    srgbClr = etree.SubElement(solidFill, '{http://schemas.openxmlformats.org/drawingml/2006/main}srgbClr')
                    srgbClr.set('val', 'FFFFFF')
                alpha = srgbClr.find('{http://schemas.openxmlformats.org/drawingml/2006/main}alpha')
                if alpha is None:
                    alpha = etree.SubElement(srgbClr, '{http://schemas.openxmlformats.org/drawingml/2006/main}alpha')
                alpha.set('val', str(int(alpha_percent * 1000)))

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    # 1. Base Background (Light Gray)
    bg = slide.background
    fill = bg.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(235, 235, 240)

    # Global Slide Title
    tb_main_title = slide.shapes.add_textbox(Inches(1), Inches(0.5), Inches(11.333), Inches(0.8))
    tb_main_title.text_frame.word_wrap = True
    p = tb_main_title.text_frame.paragraphs[0]
    p.text = title_text
    p.font.name = "Segoe UI"
    p.font.size = Pt(24)
    p.font.bold = True
    p.font.color.rgb = RGBColor(100, 100, 100)
    p.alignment = 2 # Center aligned

    # Pillar configuration
    banners = [
        {'num': '01', 'title': 'LOREM IPSUM', 'color1': (255, 120, 50), 'color2': (255, 50, 0), 'dark': (150, 30, 0)},
        {'num': '02', 'title': 'LOREM IPSUM', 'color1': (50, 200, 220), 'color2': (0, 150, 180), 'dark': (0, 80, 100)},
        {'num': '03', 'title': 'LOREM IPSUM', 'color1': (160, 210, 50), 'color2': (100, 170, 20), 'dark': (50, 90, 10)},
        {'num': '05', 'title': 'LOREM IPSUM', 'color1': (80, 90, 120), 'color2': (40, 50, 80), 'dark': (20, 25, 40)}
    ]

    total_width = 10.0
    w = 2.0
    spacing = (total_width - (w * 4)) / 3 
    start_x = (13.333 - total_width) / 2
    start_y = 1.6
    h = 4.2
    s = 0.8 # Downward slant amount

    for i, b in enumerate(banners):
        x = start_x + i * (w + spacing)
        y = start_y

        # Layer 1: Dark 3D Fold Triangle
        # Starts at bottom-left corner and creates a ribbon tuck behind
        ff_builder = slide.shapes.build_freeform()
        ff_builder.add_line_segments([
            (Inches(x), Inches(y + h)),
            (Inches(x + 0.5), Inches(y + h + 0.5 * (s/w))), # Match the angle slightly
            (Inches(x + 0.2), Inches(y + h + 0.4)),
            (Inches(x), Inches(y + h))
        ], close=True)
        fold = ff_builder.convert_to_shape()
        fold.fill.solid()
        fold.fill.fore_color.rgb = RGBColor(*b['dark'])
        fold.line.fill.background()

        # Layer 2: Main Slanted Body
        ff_builder = slide.shapes.build_freeform()
        ff_builder.add_line_segments([
            (Inches(x), Inches(y)),
            (Inches(x + w), Inches(y + s)),
            (Inches(x + w), Inches(y + h + s)),
            (Inches(x), Inches(y + h)),
            (Inches(x), Inches(y))
        ], close=True)
        banner = ff_builder.convert_to_shape()
        inject_gradient(banner, b['color1'], b['color2'])
        banner.line.fill.background()
        inject_shadow(banner)

        # Layer 3: Giant Semi-Transparent Number
        tb_num = slide.shapes.add_textbox(Inches(x + 0.1), Inches(y + 0.1 + (s*0.1)), Inches(w - 0.2), Inches(1))
        p = tb_num.text_frame.paragraphs[0]
        run = p.add_run()
        run.text = b['num']
        run.font.name = 'Arial Black'
        run.font.size = Pt(54)
        set_text_transparency(tb_num, 30) # 30% alpha (highly transparent)

        # Layer 4: Vertical 'OPTION' Label
        tb_opt = slide.shapes.add_textbox(Inches(x - 0.55), Inches(y + 0.6), Inches(1), Inches(0.4))
        tb_opt.rotation = -90 # Vertical reading
        p = tb_opt.text_frame.paragraphs[0]
        run = p.add_run()
        run.text = "OPTION"
        run.font.name = 'Segoe UI'
        run.font.size = Pt(9)
        run.font.bold = True
        set_text_transparency(tb_opt, 80) 

        # Layer 5: Bold Title
        tb_title = slide.shapes.add_textbox(Inches(x + 0.15), Inches(y + 1.6), Inches(w - 0.3), Inches(0.5))
        tb_title.text_frame.word_wrap = True
        p = tb_title.text_frame.paragraphs[0]
        p.text = b['title']
        p.font.name = 'Segoe UI'
        p.font.bold = True
        p.font.size = Pt(14)
        p.font.color.rgb = RGBColor(255, 255, 255)

        # Subtitle separator line
        sep_line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x + 0.2), Inches(y + 2.05), Inches(0.4), Inches(0.02))
        sep_line.fill.solid()
        sep_line.fill.fore_color.rgb = RGBColor(255, 255, 255)
        sep_line.line.fill.background()

        # Layer 6: Description Body Text
        tb_body = slide.shapes.add_textbox(Inches(x + 0.15), Inches(y + 2.15), Inches(w - 0.3), Inches(1.5))
        tb_body.text_frame.word_wrap = True
        p = tb_body.text_frame.paragraphs[0]
        p.text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Maecenas porttitor congue."
        p.font.name = 'Segoe UI'
        p.font.size = Pt(10)
        p.font.color.rgb = RGBColor(245, 245, 245)

    prs.save(output_pptx_path)
    return output_pptx_path
