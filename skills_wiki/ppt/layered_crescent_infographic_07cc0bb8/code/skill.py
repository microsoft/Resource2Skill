import os
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml.ns import qn
from lxml import etree
import urllib.request
from io import BytesIO

def _get_shape_tree(slide):
    """Helper to access the shape tree of a slide."""
    return slide.shapes._spTree

def _add_shadow_effect(spPr, blur_rad, dist, direction, alpha=23):
    """
    Applies an <a:outerShdw> effect to a shape's properties.
    All distance/blur values should be in EMUs.
    Alpha is a percentage (0-100).
    """
    effect_list = spPr.get_or_add_effectLst()
    shadow = etree.SubElement(effect_list, qn('a:outerShdw'))
    shadow.set('blurRad', str(blur_rad))
    shadow.set('dist', str(dist))
    shadow.set('dir', str(direction))
    shadow.set('algn', 'bl')
    shadow.set('rotWithShape', '0')
    
    srgb_color = etree.SubElement(shadow, qn('a:srgbClr'))
    srgb_color.set('val', '000000')
    etree.SubElement(srgb_color, qn('a:alpha')).set('val', str(alpha * 1000))

def _create_layered_arc_with_shadow(slide, x, y, width, height, color_rgb):
    """
    Creates a single layered arc with its complex shadow using lxml.
    """
    spTree = _get_shape_tree(slide)
    
    # Create the <p:sp> element
    sp = etree.Element(qn('p:sp'))
    
    # Non-visual properties
    nvSpPr = etree.SubElement(sp, qn('p:nvSpPr'))
    cnvPr = etree.SubElement(nvSpPr, qn('p:cNvPr'))
    cnvPr.set('id', str(slide.shapes.next_id))
    cnvPr.set('name', 'Layered Arc')
    etree.SubElement(nvSpPr, qn('p:cNvPrSpPr'))
    etree.SubElement(nvSpPr, qn('p:nvPr'))

    # Shape Properties (spPr)
    spPr = etree.SubElement(sp, qn('p:spPr'))

    # Transform
    xfrm = etree.SubElement(spPr, qn('a:xfrm'))
    xfrm.set('rot', '5400000') # 90 degrees rotation
    etree.SubElement(xfrm, qn('a:off')).set('x', str(x)).set('y', str(y))
    etree.SubElement(xfrm, qn('a:ext')).set('cx', str(width)).set('cy', str(height))

    # Geometry (Block Arc)
    prstGeom = etree.SubElement(spPr, qn('a:prstGeom'))
    prstGeom.set('prst', 'arc')
    avLst = etree.SubElement(prstGeom, qn('a:avLst'))
    etree.SubElement(avLst, qn('a:gd')).set('name', 'adj1').set('fmla', 'val 12500') # Start Angle
    etree.SubElement(avLst, qn('a:gd')).set('name', 'adj2').set('fmla', 'val 168750') # End Angle
    
    # Fill
    solidFill = etree.SubElement(spPr, qn('a:solidFill'))
    srgbClr = etree.SubElement(solidFill, qn('a:srgbClr'))
    srgbClr.set('val', '%02x%02x%02x' % color_rgb)

    # Outline
    ln = etree.SubElement(spPr, qn('a:ln'))
    etree.SubElement(ln, qn('a:noFill'))

    # Add the crucial outer shadow for layering
    _add_shadow_effect(
        spPr,
        blur_rad=Emu(Pt(11)),
        dist=Emu(Pt(4)),
        direction='2700000', # 45 degrees
        alpha=23
    )
    
    # Append the completed shape to the slide's shape tree
    spTree.append(sp)

def create_slide(
    output_pptx_path: str,
    title_text: str = "Layered Crescent Infographic",
    **kwargs,
) -> str:
    """
    Creates a PPTX file reproducing the Layered Crescent Infographic.

    Returns: path to the saved PPTX file.
    """
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_slide_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(blank_slide_layout)

    # === Layer 1: Background Plane ===
    # A custom polygon to create a subtle perspective effect
    freeform = slide.shapes.add_freeform_shape()
    with freeform.build_freeform() as builder:
        builder.add_line_segments([(0, 0), (Inches(13.333), Inches(1)), (Inches(13.333), Inches(6.5)), (0, Inches(7.5))], close=True)
    
    fill = freeform.fill
    fill.gradient()
    fill.gradient_angle = 135
    fill.gradient_stops[0].color.rgb = RGBColor(242, 242, 242)
    fill.gradient_stops[0].position = 0.0
    fill.gradient_stops[1].color.rgb = RGBColor(220, 220, 220)
    fill.gradient_stops[1].position = 1.0
    
    # Send background to back
    sp_id = freeform.element.sp_id
    sp = freeform.element
    sp.getparent().remove(sp)
    sp.getparent().insert(0, sp)
    
    # === Layer 2: Main Visual Elements (Crescents) ===
    # Define colors and positions
    colors = {
        'A': (218, 150, 148),
        'B': (89, 133, 169),
        'C': (146, 172, 134),
    }
    positions = {
        'C': (Inches(1.8), Inches(4.0)),
        'B': (Inches(1.8), Inches(2.25)),
        'A': (Inches(1.8), Inches(0.5)),
    }
    arc_size = Emu(Inches(3))

    # Create the underlying long shadow shape
    shadow_base = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(3.7), Inches(0.5), Inches(0.4), Inches(6.5))
    shadow_base.fill.background()
    shadow_base.line.fill.background()
    spPr_base = shadow_base.element.spPr
    _add_shadow_effect(
        spPr_base,
        blur_rad=Emu(Pt(14)),
        dist=Emu(Pt(6)),
        direction='0', # 0 degrees
        alpha=23
    )
    # Send shadow base to back (but in front of the background plane)
    sp_base_id = shadow_base.element.sp_id
    sp_base = shadow_base.element
    sp_base.getparent().remove(sp_base)
    sp_base.getparent().insert(1, sp_base)


    # Create arcs in reverse order for correct layering
    for key in ['C', 'B', 'A']:
        x, y = positions[key]
        _create_layered_arc_with_shadow(slide, Emu(x), Emu(y), arc_size, arc_size, colors[key])

    # === Layer 3: Text & Icons ===
    icon_urls = {
        'C': 'https://www.flaticon.com/download/icon/889169?format=png&size=256',
        'B': 'https://www.flaticon.com/download/icon/1256553?format=png&size=256',
        'A': 'https://www.flaticon.com/download/icon/2941561?format=png&size=256',
    }
    
    for i, key in enumerate(['C', 'B', 'A']):
        # Add Letters (A, B, C)
        left, top = positions[key]
        txBox = slide.shapes.add_textbox(left - Inches(1.5), top + Inches(0.3), Inches(1), Inches(1))
        p = txBox.text_frame.paragraphs[0]
        p.text = key
        p.font.name = 'Arial Black'
        p.font.size = Pt(40)
        p.font.color.rgb = RGBColor(89, 89, 89)

        # Add Icons
        try:
            with urllib.request.urlopen(icon_urls[key]) as url_response:
                icon_data = url_response.read()
                slide.shapes.add_picture(BytesIO(icon_data), left + Inches(0.8), top + Inches(1.0), height=Inches(0.8))
        except Exception:
            # Fallback to a circle if image download fails
            slide.shapes.add_shape(MSO_SHAPE.OVAL, left + Inches(0.8), top + Inches(1.0), Inches(0.8), Inches(0.8))

        # Add Text Content
        txBox_content = slide.shapes.add_textbox(Inches(7.5), top + Inches(0.8), Inches(4.5), Inches(2))
        tf = txBox_content.text_frame
        tf.clear()

        p_head1 = tf.paragraphs[0]
        run1 = p_head1.add_run()
        run1.text = "OPTION"
        run1.font.name = 'Calibri'
        run1.font.size = Pt(14)
        run1.font.bold = True
        run1.font.color.rgb = RGBColor(89, 89, 89)
        
        run2 = p_head1.add_run()
        run2.text = "  INFOGRAPHIC"
        run2.font.name = 'Calibri'
        run2.font.size = Pt(14)
        run2.font.bold = True
        run2.font.color.rgb = RGBColor(*colors[key])

        p_body = tf.add_paragraph()
        p_body.text = "Lorem ipsum comes from section Contrary to popular belief. Lorem Ipsum is not simply random text."
        p_body.font.name = 'Calibri'
        p_body.font.size = Pt(11)
        p_body.font.color.rgb = RGBColor(127, 127, 127)

    # Add decorative line chart element
    chart_ff = slide.shapes.add_freeform_shape()
    with chart_ff.build_freeform() as builder:
        # Line 1 (Green)
        builder.move_to(Inches(10.5), Inches(6.5))
        builder.add_line_segments([(Inches(10.8), Inches(6.2)), (Inches(11.1), Inches(6.4)), (Inches(11.4), Inches(6.1))])
        # Line 2 (Blue)
        builder.move_to(Inches(10.5), Inches(6.8))
        builder.add_line_segments([(Inches(10.9), Inches(6.6)), (Inches(11.2), Inches(6.9)), (Inches(11.5), Inches(6.5))])
        # Line 3 (Pink)
        builder.move_to(Inches(10.6), Inches(7.0))
        builder.add_line_segments([(Inches(11.0), Inches(6.8)), (Inches(11.3), Inches(7.1)), (Inches(11.6), Inches(6.7))])
    
    chart_ff.line.fill.solid()
    chart_ff.line.fill.fore_color.rgb = RGBColor(220, 220, 220)
    chart_ff.line.width = Pt(1.5)
    chart_ff.fill.background()

    tx_box_chart = slide.shapes.add_textbox(Inches(11.5), Inches(6.5), Inches(2), Inches(0.5))
    p_chart = tx_box_chart.text_frame.paragraphs[0]
    p_chart.text = "INFOGRAPHIC\nELEMENTS"
    p_chart.font.name = 'Calibri'
    p_chart.font.size = Pt(9)
    p_chart.font.color.rgb = RGBColor(89, 89, 89)


    prs.save(output_pptx_path)
    return output_pptx_path

# Example of how to run the function
if __name__ == '__main__':
    output_filename = "layered_crescent_infographic.pptx"
    create_slide(output_filename)
    # On Windows, you might want to open the file automatically
    if os.name == 'nt':
        os.startfile(output_filename)

