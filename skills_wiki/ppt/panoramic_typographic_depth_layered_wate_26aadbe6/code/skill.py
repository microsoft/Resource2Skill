import os
import urllib.request
from pptx import Presentation
from pptx.util import Pt, Inches
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.oxml.xmlchemy import OxmlElement
from pptx.oxml import parse_xml
from PIL import Image, ImageDraw

def _create_fallback_gradient_image(filepath: str, width=1920, height=1080):
    """Generates a deep blue to sunrise orange gradient using PIL as a fallback background."""
    img = Image.new('RGB', (width, height))
    draw = ImageDraw.Draw(img)
    # Deep blue to sunrise
    color_top = (10, 25, 70)
    color_bottom = (230, 120, 80)
    
    for y in range(height):
        # Calculate interpolation factor
        factor = y / height
        r = int(color_top[0] + (color_bottom[0] - color_top[0]) * factor)
        g = int(color_top[1] + (color_bottom[1] - color_top[1]) * factor)
        b = int(color_top[2] + (color_bottom[2] - color_top[2]) * factor)
        draw.line([(0, y), (width, y)], fill=(r, g, b))
    
    img.save(filepath)
    return filepath

def _set_text_transparency(font, alpha_percentage: float):
    """Injects transparency (alpha) into a python-pptx font object via lxml."""
    # Ensure solidFill exists by setting a color first
    font.color.rgb = RGBColor(255, 255, 255)
    
    # Access the underlying XML of the color run
    color_element = font.color._xFill
    if color_element is not None:
        # PowerPoint alpha is 0 to 100000 (100% opaque is 100000, 15% opaque is 15000)
        alpha_val = int(alpha_percentage * 100000)
        
        # Find or create srgbClr
        srgbClr = color_element.find('.//a:srgbClr', namespaces=color_element.nsmap)
        if srgbClr is not None:
            # Create alpha element
            alpha_elem = OxmlElement('a:alpha')
            alpha_elem.set('val', str(alpha_val))
            srgbClr.append(alpha_elem)

def _add_custom_dropshadow(shape, color_rgb: tuple, blur_pt: int = 5, distance_pt: int = 4):
    """Injects a custom colored drop shadow to a shape via lxml."""
    # Convert pts to EMUs (1 pt = 12700 EMUs)
    blur_emu = blur_pt * 12700
    dist_emu = distance_pt * 12700
    r, g, b = color_rgb
    hex_color = f"{r:02X}{g:02X}{b:02X}"

    # Build drawingML effect list XML
    effectLst_xml = f"""
    <a:effectLst xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">
        <a:outerShdw blurRad="{blur_emu}" dist="{dist_emu}" dir="5400000" algn="b" rotWithShape="0">
            <a:srgbClr val="{hex_color}">
                <a:alpha val="60000"/>
            </a:srgbClr>
        </a:outerShdw>
    </a:effectLst>
    """
    effectLst = parse_xml(effectLst_xml)
    
    # Inject into the shape properties (spPr)
    shape.element.spPr.append(effectLst)


def create_slide(
    output_pptx_path: str,
    main_title: str = "我的年终总结",
    subtitle: str = "MY YEAR-END SUMMARY",
    watermark_text: str = "2024",
    metadata_text: str = "演讲者：璞石   |   2024年12月31日",
    bg_image_url: str = "https://images.unsplash.com/photo-1477959858617-67f85cf4f1df?q=80&w=1920&h=1080&fit=crop",
) -> str:
    """
    Create a PPTX file reproducing the Panoramic Typographic Depth effect.
    """
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6]) # Blank layout

    bg_path = "temp_bg.jpg"
    try:
        urllib.request.urlretrieve(bg_image_url, bg_path)
    except Exception:
        # Fallback to generated PIL gradient if network fails
        _create_fallback_gradient_image(bg_path)

    # === Layer 0: Background Image ===
    slide.shapes.add_picture(bg_path, 0, 0, prs.slide_width, prs.slide_height)

    # === Layer 1: Massive Watermark Text (Semi-transparent) ===
    # Placed in the center/upper-center
    tx_watermark = slide.shapes.add_textbox(Inches(0), Inches(0.5), prs.slide_width, Inches(4))
    tf_watermark = tx_watermark.text_frame
    tf_watermark.clear()
    p_watermark = tf_watermark.paragraphs[0]
    p_watermark.text = watermark_text
    p_watermark.alignment = PP_ALIGN.CENTER
    
    run_wm = p_watermark.runs[0]
    run_wm.font.name = 'Arial Black'
    run_wm.font.size = Pt(220)
    run_wm.font.bold = True
    # Magic LXML to make it 15% transparent white
    _set_text_transparency(run_wm.font, alpha_percentage=0.15)


    # === Layer 2: Main Foreground Title ===
    tx_main = slide.shapes.add_textbox(Inches(0), Inches(2.2), prs.slide_width, Inches(2))
    tf_main = tx_main.text_frame
    tf_main.clear()
    p_main = tf_main.paragraphs[0]
    p_main.text = main_title
    p_main.alignment = PP_ALIGN.CENTER
    
    run_main = p_main.runs[0]
    run_main.font.name = 'Microsoft YaHei' # Calligraphy fallback
    run_main.font.size = Pt(80)
    run_main.font.bold = True
    run_main.font.color.rgb = RGBColor(255, 255, 255)
    
    # Inject tinted drop shadow (Deep Navy blue to blend with background)
    _add_custom_dropshadow(tx_main, color_rgb=(10, 20, 50), blur_pt=8, distance_pt=4)


    # === Layer 3: Subtitle (Spaced out) ===
    tx_sub = slide.shapes.add_textbox(Inches(0), Inches(3.6), prs.slide_width, Inches(1))
    tf_sub = tx_sub.text_frame
    tf_sub.clear()
    p_sub = tf_sub.paragraphs[0]
    # Simulate distributed spacing by injecting spaces between letters
    spaced_subtitle = "  ".join(list(subtitle))
    p_sub.text = spaced_subtitle
    p_sub.alignment = PP_ALIGN.CENTER
    
    run_sub = p_sub.runs[0]
    run_sub.font.name = 'Times New Roman' # Serif
    run_sub.font.size = Pt(20)
    run_sub.font.bold = True
    run_sub.font.color.rgb = RGBColor(255, 255, 255)


    # === Layer 4: Metadata and Lines ===
    tx_meta = slide.shapes.add_textbox(Inches(0), Inches(4.3), prs.slide_width, Inches(0.5))
    tf_meta = tx_meta.text_frame
    tf_meta.clear()
    p_meta = tf_meta.paragraphs[0]
    p_meta.text = metadata_text
    p_meta.alignment = PP_ALIGN.CENTER
    
    run_meta = p_meta.runs[0]
    run_meta.font.name = 'Microsoft YaHei'
    run_meta.font.size = Pt(14)
    run_meta.font.color.rgb = RGBColor(230, 230, 230)

    # Decorative Lines flanking metadata
    # Center is ~6.66 Inches.
    line_left = slide.shapes.add_connector(1, Inches(3.5), Inches(4.5), Inches(4.8), Inches(4.5))
    line_left.line.color.rgb = RGBColor(255, 255, 255)
    line_left.line.width = Pt(1)
    
    line_right = slide.shapes.add_connector(1, Inches(8.5), Inches(4.5), Inches(9.8), Inches(4.5))
    line_right.line.color.rgb = RGBColor(255, 255, 255)
    line_right.line.width = Pt(1)

    prs.save(output_pptx_path)
    
    # Cleanup temp image
    if os.path.exists(bg_path):
        os.remove(bg_path)
        
    return output_pptx_path

# Example execution:
# create_slide("panoramic_cover.pptx")
