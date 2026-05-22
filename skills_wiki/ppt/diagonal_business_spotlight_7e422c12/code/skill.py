import collections.abc
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_VERTICAL_ANCHOR
from pptx.shapes.freeform import FreeformBuilder
from pptx.oxml.xmlchemy import OxmlElement
import urllib.request
import io
import os

def _set_gradient_fill(shape, angle, stops):
    """
    Apply a complex gradient fill to a shape using lxml.
    'shape': the python-pptx shape object.
    'angle': linear gradient angle in degrees.
    'stops': a list of tuples, each containing (RGB tuple, position_float, transparency_float).
    """
    sp = shape.element
    spPr = sp.spPr

    # Remove any existing fill
    if spPr.find('a:solidFill') is not None:
        spPr.remove(spPr.find('a:solidFill'))

    gradFill = OxmlElement('a:gradFill')
    lin = OxmlElement('a:lin')
    lin.set('ang', str(angle * 60000))
    lin.set('scaled', '1')

    gsLst = OxmlElement('a:gsLst')

    for color, pos, trans in stops:
        gs = OxmlElement('a:gs')
        gs.set('pos', str(int(pos * 100000)))
        srgbClr = OxmlElement('a:srgbClr')
        srgbClr.set('val', '%02x%02x%02x' % color)
        alpha = OxmlElement('a:alpha')
        alpha.set('val', str(int((1 - trans) * 100000)))
        srgbClr.append(alpha)
        gs.append(srgbClr)
        gsLst.append(gs)

    lin.append(gsLst)
    gradFill.append(lin)
    spPr.append(gradFill)

def set_char_spacing(run, spacing_pt):
    """Set character spacing for a run in points."""
    rPr = run._r.get_or_add_rPr()
    rPr.set('spc', str(int(spacing_pt * 100))) # Spacing is in 100ths of a point in some contexts, but EMU may be better. Let's use Pt directly, pptx handles conversion. Pt(1) = 100.
    # The video uses "Loose", which is ~3pt. Let's use Pt for consistency.
    rPr.set('spc', str(Pt(spacing_pt).twips * 20)) # A more reliable conversion path.
    # Actually, the direct EMU value is most reliable. 1pt = 12700 EMU.
    rPr.set('spc', str(int(spacing_pt * 12700)))

def create_slide(
    output_pptx_path: str,
    title_text: str = "BUSINESS PRESENTATIONS",
    bg_image_url: str = 'https://images.pexels.com/photos/313782/pexels-photo-313782.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2',
    accent_color_main: tuple = (226, 0, 122),
    **kwargs,
) -> str:
    """
    Creates a PPTX file reproducing the Diagonal Business Spotlight visual effect.

    Args:
        output_pptx_path: Path to save the generated .pptx file.
        title_text: The main title, use a separator like '|' (e.g., "BUSINESS|PRESENTATIONS").
        bg_image_url: URL for the background image.
        accent_color_main: The primary accent color as an RGB tuple.

    Returns:
        Path to the saved PPTX file.
    """
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    # === Layer 1: Background ===
    try:
        with urllib.request.urlopen(bg_image_url) as url:
            f = io.BytesIO(url.read())
        pic = slide.shapes.add_picture(f, 0, 0, width=prs.slide_width, height=prs.slide_height)
        # Send picture to back
        slide.shapes._spTree.remove(pic.element)
        slide.shapes._spTree.insert(2, pic.element)
    except Exception:
        background = slide.background
        fill = background.fill
        fill.solid()
        fill.fore_color.rgb = RGBColor(10, 10, 20)

    # === Layer 2: Overlays and Panels ===
    overlay = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
    overlay.line.fill.background()
    _set_gradient_fill(overlay, 90, [((24, 10, 18), 0.0, 0.25), ((8, 15, 12), 1.0, 0.15)])

    # Darker Left Panel
    ff_builder = slide.shapes.build_freeform(Emu(Inches(-1)), Emu(0))
    ff_builder.add_line_segments([(Emu(Inches(7)), Emu(0)), (Emu(Inches(5.5)), Emu(prs.slide_height)), (Emu(Inches(-2.5)), Emu(prs.slide_height))], close=True)
    dark_panel = ff_builder.convert_to_shape()
    dark_panel.line.fill.background()
    fill = dark_panel.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(9, 9, 15)
    fill.transparency = 0.22

    # Main Accent Panel
    ff_builder = slide.shapes.build_freeform(Emu(Inches(4.5)), Emu(0))
    ff_builder.add_line_segments([(Emu(prs.slide_width), Emu(0)), (Emu(Inches(8.833)), Emu(prs.slide_height)), (Emu(0), Emu(prs.slide_height))], close=True)
    accent_panel = ff_builder.convert_to_shape()
    accent_panel.line.fill.background()
    _set_gradient_fill(accent_panel, 90, [(accent_color_main, 0.0, 0.26), ((149, 32, 80), 1.0, 0.0)])
    
    # White Metrics Panel
    ff_builder = slide.shapes.build_freeform(Emu(Inches(6.8)), Emu(Inches(6.1)))
    ff_builder.add_line_segments([(Emu(prs.slide_width), Emu(Inches(6.1))), (Emu(prs.slide_width), Emu(prs.slide_height)), (Emu(Inches(9.1)), Emu(prs.slide_height))], close=True)
    metrics_panel = ff_builder.convert_to_shape()
    metrics_panel.line.fill.background()
    fill = metrics_panel.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(255, 255, 255)
    fill.transparency = 0.90
    
    # Decorative Top-Left Element
    ff_builder = slide.shapes.build_freeform(Emu(0), Emu(0))
    ff_builder.add_line_segments([(Emu(0), Emu(Inches(1.5))), (Emu(Inches(1.8)), Emu(0))], close=True)
    deco_shape = ff_builder.convert_to_shape()
    deco_shape.line.fill.background()
    fill = deco_shape.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor.from_string(accent_color_main.hex) if isinstance(accent_color_main, RGBColor) else RGBColor(*accent_color_main)
    fill.transparency = 0.94

    # === Layer 3: Text & Content ===
    title_parts = title_text.split('|')
    title1 = title_parts[0]
    title2 = title_parts[1] if len(title_parts) > 1 else "PRESENTATIONS"

    txBox = slide.shapes.add_textbox(Inches(0.5), Inches(2.0), Inches(4.5), Inches(2))
    tf = txBox.text_frame
    tf.clear()
    p1 = tf.paragraphs[0]
    run1 = p1.add_run()
    run1.text = title1.upper()
    font1 = run1.font
    font1.name = 'Agency FB'
    font1.size = Pt(120)
    font1.bold = True
    font1.color.rgb = RGBColor.from_string(accent_color_main.hex) if isinstance(accent_color_main, RGBColor) else RGBColor(*accent_color_main)

    txBox2 = slide.shapes.add_textbox(Inches(0.5), Inches(3.3), Inches(5.5), Inches(1))
    tf2 = txBox2.text_frame
    p2 = tf2.paragraphs[0]
    run2 = p2.add_run()
    run2.text = title2.upper()
    font2 = run2.font
    font2.name = 'Agency FB'
    font2.size = Pt(54)
    font2.bold = True
    font2.color.rgb = RGBColor(255, 255, 255)
    set_char_spacing(run2, 3)

    # Content points
    content_points = [
        ("HEADING A", "Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Maecenas porttitor congue massa. Fusce posuere, magna sed pulvinar ultricies."),
        ("HEADING B", "Purus lectus malesuada libero, sit amet commodo magna eros quis urna. Nunc viverra imperdiet enim. Fusce est. Vivamus a tellus."),
        ("HEADING C", "Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Proin pharetra nonummy pede. Mauris et orci."),
    ]
    y_start = Inches(1.2)
    for i, (heading, text) in enumerate(content_points):
        icon = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(7.0), y_start + Inches(i * 1.7), Inches(0.4), Inches(0.4))
        icon.fill.solid(); icon.fill.fore_color.rgb = RGBColor(255, 255, 255); icon.line.fill.background()

        txBox_h = slide.shapes.add_textbox(Inches(7.6), y_start - Inches(0.25) + Inches(i * 1.7), Inches(5), Inches(0.5))
        p_h = txBox_h.text_frame.paragraphs[0]
        run_h = p_h.add_run(); run_h.text = heading.upper(); font_h = run_h.font
        font_h.name = 'Agency FB'; font_h.size = Pt(16); font_h.bold = True; font_h.color.rgb = RGBColor(255, 255, 255)
        set_char_spacing(run_h, 3)
        
        txBox_b = slide.shapes.add_textbox(Inches(7.6), y_start + Inches(0.15) + Inches(i * 1.7), Inches(5.2), Inches(1.2))
        p_b = txBox_b.text_frame.paragraphs[0]; p_b.text = text; font_b = p_b.font
        font_b.name = 'Agency FB'; font_b.size = Pt(9); font_b.color.rgb = RGBColor(255, 255, 255)
        txBox_b.text_frame.word_wrap = True

    # Metrics
    metrics_data = [("500+", "Clients"), ("2000+", "Projects"), ("300+", "Employees")]
    x_start = Inches(7.2)
    for i, (number, label) in enumerate(metrics_data):
        txBox_m = slide.shapes.add_textbox(x_start + Inches(i * 2.1), Inches(6.3), Inches(2), Inches(1))
        tf_m = txBox_m.text_frame; tf_m.clear()
        p_num = tf_m.paragraphs[0]; p_num.alignment = PP_ALIGN.LEFT
        run_num = p_num.add_run(); run_num.text = number; font_num = run_num.font
        font_num.name = 'Agency FB'; font_num.size = Pt(36); font_num.bold = True; font_num.color.rgb = RGBColor.from_string(accent_color_main.hex) if isinstance(accent_color_main, RGBColor) else RGBColor(*accent_color_main)
        
        p_label = tf_m.add_paragraph(); p_label.alignment = PP_ALIGN.LEFT
        run_label = p_label.add_run(); run_label.text = label.upper(); font_label = run_label.font
        font_label.name = 'Agency FB'; font_label.size = Pt(18); font_label.color.rgb = RGBColor(255, 255, 255)
    
    prs.save(output_pptx_path)
    return output_pptx_path

