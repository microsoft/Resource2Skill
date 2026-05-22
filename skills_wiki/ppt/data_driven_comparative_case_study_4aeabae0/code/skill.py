import requests
import io
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.chart.data import ChartData
from pptx.enum.chart import XL_CHART_TYPE, XL_TICK_MARK
from pptx.enum.dml import MSO_THEME_COLOR
from lxml import etree
from PIL import Image, ImageDraw

# Helper function for lxml to handle namespaces
def _get_shape_xml(shape):
    return shape.element._sp

def _add_shadow_to_shape(shape, blur_radius=15, distance=5, direction=45, alpha=50):
    """Adds an outer shadow effect to a shape using lxml."""
    sp = _get_shape_xml(shape)
    
    # Namespace map
    nsmap = {
        'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
        'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'
    }

    # Find or create spPr element
    spPr = sp.find('a:spPr', namespaces=nsmap)
    if spPr is None:
        spPr = etree.SubElement(sp, f"{{{nsmap['a']}}}spPr")

    # Find or create effectLst element
    effectLst = spPr.find('a:effectLst', namespaces=nsmap)
    if effectLst is None:
        effectLst = etree.SubElement(spPr, f"{{{nsmap['a']}}}effectLst")
    
    # Create outerShdw element
    outerShdw = etree.SubElement(effectLst, f"{{{nsmap['a']}}}outerShdw",
                                 blurRad=str(blur_radius * 12700),
                                 dist=str(distance * 12700),
                                 dir=str(direction * 60000),
                                 algn="bl", rotWithShape="0")
    
    # Add shadow color
    srgbClr = etree.SubElement(outerShdw, f"{{{nsmap['a']}}}srgbClr", val="000000")
    etree.SubElement(srgbClr, f"{{{nsmap['a']}}}alpha", val=str(alpha * 1000))

def create_slide(
    output_pptx_path: str,
    title_text: str = "Visitor Experience: Before & After Analysis",
    bg_keyword: str = "australia twelve apostles",
    accent_color_1: tuple = (91, 155, 213),
    accent_color_2: tuple = (255, 192, 0),
    **kwargs,
) -> str:
    """
    Creates a PPTX slide reproducing the Data-Driven Comparative Case Study style.

    Returns: path to the saved PPTX file.
    """
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    # === Layer 1: Background Image ===
    try:
        # Using an API like Pexels or Unsplash is recommended, here we use a direct link for simplicity
        # A more robust solution would use an API key
        search_url = f"https://source.unsplash.com/1600x900/?{bg_keyword.replace(' ', '+')}"
        response = requests.get(search_url, timeout=10)
        response.raise_for_status()
        bg_image_stream = io.BytesIO(response.content)
        slide.shapes.add_picture(bg_image_stream, 0, 0, width=prs.slide_width, height=prs.slide_height)
    except (requests.exceptions.RequestException, IOError) as e:
        print(f"Warning: Could not download background image ({e}). Using a solid color fallback.")
        background = slide.background
        fill = background.fill
        fill.solid()
        fill.fore_color.rgb = RGBColor(13, 17, 28)

    # === Layer 2: Color Overlay ===
    overlay_img = Image.new('RGBA', (int(prs.slide_width), int(prs.slide_height)), (40, 85, 106, 200))
    overlay_stream = io.BytesIO()
    overlay_img.save(overlay_stream, format='PNG')
    overlay_stream.seek(0)
    slide.shapes.add_picture(overlay_stream, 0, 0, width=prs.slide_width, height=prs.slide_height)

    # === Layer 3: Content Panel with Shadow ===
    panel_width = Inches(5.5)
    panel = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.5), Inches(0.5), panel_width, Inches(6.5))
    fill = panel.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(255, 255, 255)
    line = panel.line
    line.fill.background()
    _add_shadow_to_shape(panel, blur_radius=20, distance=3, alpha=35)

    # === Layer 4: Chart ===
    chart_data = ChartData()
    chart_data.categories = ['Service Quality', 'Wait Times', 'Navigation', 'Value']
    chart_data.add_series('Before Redesign', (2.5, 4.1, 3.0, 2.2))
    chart_data.add_series('After Redesign (Projected)', (4.5, 2.0, 4.8, 4.0))

    x, y, cx, cy = Inches(1), Inches(2.2), Inches(4.5), Inches(4)
    chart = slide.shapes.add_chart(
        XL_CHART_TYPE.COLUMN_CLUSTERED, x, y, cx, cy, chart_data
    ).chart

    chart.has_legend = True
    chart.legend.include_in_layout = False # Hide but keep data for series
    chart.value_axis.has_major_gridlines = False
    chart.value_axis.tick_labels.font.size = Pt(10)
    chart.value_axis.tick_labels.font.color.rgb = RGBColor(80, 80, 80)
    chart.value_axis.major_tick_mark = XL_TICK_MARK.NONE
    chart.category_axis.tick_labels.font.size = Pt(11)
    chart.category_axis.tick_labels.font.color.rgb = RGBColor(50, 50, 50)
    
    # Style series
    chart.series[0].fill.solid()
    chart.series[0].fill.fore_color.rgb = RGBColor(*accent_color_1)
    chart.series[1].fill.solid()
    chart.series[1].fill.fore_color.rgb = RGBColor(*accent_color_2)
    
    chart.plot_area.format.fill.background()

    # === Layer 5: Text ===
    # Chart Title
    chart_title_box = slide.shapes.add_textbox(Inches(1), Inches(0.8), Inches(4.5), Inches(1))
    p = chart_title_box.text_frame.add_paragraph()
    p.text = "Key Experience Metrics Improvement"
    p.font.bold = True
    p.font.size = Pt(20)
    p.font.color.rgb = RGBColor(0, 0, 0)

    # Main Slide Title
    title_box = slide.shapes.add_textbox(Inches(6.5), Inches(1.5), Inches(6.5), Inches(2))
    p_title = title_box.text_frame.add_paragraph()
    p_title.text = title_text
    p_title.font.bold = True
    p_title.font.size = Pt(40)
    p_title.font.color.rgb = RGBColor(255, 255, 255)

    prs.save(output_pptx_path)
    return output_pptx_path

# Example Usage:
# create_slide("comparative_analysis_slide.pptx")
