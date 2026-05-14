import io
import urllib.request
from lxml import etree
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE, XL_LEGEND_POSITION, XL_DATA_LABEL_POSITION

# Helper for lxml to handle XML namespaces
def qn(tag):
    """
    Stands for 'qualified name', a utility function to turn a namespace prefixed
    tag name into a Clark-notation qualified tag name for lxml. For example,
    'p:cSld' becomes '{http://schemas.openxmlformats.org/presentationml/2006/main}cSld'.
    """
    nsmap = {
        'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
        'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
        'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
    }
    prefix, tagroot = tag.split(':')
    uri = nsmap[prefix]
    return f'{{{uri}}}{tagroot}'

# Helper function to add a shadow to a shape
def add_shadow_effect(shape_element):
    """
    Applies a soft, outer drop shadow to the given shape element.
    This function directly manipulates the underlying OOXML.
    """
    spPr = shape_element.find(qn('p:spPr'))
    if spPr is None:
        spPr = etree.SubElement(shape_element, qn('p:spPr'))

    effect_lst = etree.SubElement(spPr, qn('a:effectLst'))
    
    # Outer shadow effect
    outer_shdw = etree.SubElement(effect_lst, qn('a:outerShdw'))
    outer_shdw.set('blurRad', str(Emu(Pt(5))))  # Blur radius
    outer_shdw.set('dist', str(Emu(Pt(4))))    # Distance
    outer_shdw.set('dir', '2700000')           # Direction (270 degrees)
    outer_shdw.set('algn', 'bl')               # Alignment (bottom-left)
    outer_shdw.set('rotWithShape', '0')
    
    # Shadow color
    srgb_clr = etree.SubElement(outer_shdw, qn('a:srgbClr'))
    srgb_clr.set('val', '000000')
    
    # Shadow transparency
    alpha = etree.SubElement(srgb_clr, qn('a:alpha'))
    alpha.set('val', '15000') # 15% opacity

def add_kpi_card(slide, left, top, width, height, title, value, change, icon_url):
    """
    Adds a complete KPI card widget to the slide.
    """
    # Create the card shape
    card = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height
    )
    card.shadow.inherit = False
    card.fill.solid()
    card.fill.fore_color.rgb = RGBColor(255, 255, 255)
    card.line.fill.background()

    # Apply shadow using lxml
    add_shadow_effect(card._element)
    
    # Add Icon
    try:
        with urllib.request.urlopen(icon_url) as url:
            image_stream = io.BytesIO(url.read())
            slide.shapes.add_picture(
                image_stream, 
                left + Inches(0.2), 
                top + Inches(0.2), 
                height=Inches(0.4)
            )
    except Exception as e:
        print(f"Warning: Could not fetch icon from {icon_url}. {e}")

    # Add Title
    title_box = slide.shapes.add_textbox(
        left + Inches(0.2), top + Inches(0.7), width - Inches(0.4), Inches(0.3)
    )
    title_p = title_box.text_frame.paragraphs[0]
    title_p.text = title
    title_p.font.size = Pt(12)
    title_p.font.color.rgb = RGBColor(102, 102, 102)

    # Add Value
    value_box = slide.shapes.add_textbox(
        left + Inches(0.2), top + Inches(0.95), width - Inches(0.4), Inches(0.6)
    )
    value_p = value_box.text_frame.paragraphs[0]
    value_p.text = value
    value_p.font.size = Pt(32)
    value_p.font.bold = True
    value_p.font.color.rgb = RGBColor(0, 0, 0)
    
    # Add Change
    change_box = slide.shapes.add_textbox(
        left + Inches(0.2), top + Inches(1.5), width - Inches(0.4), Inches(0.3)
    )
    change_p = change_box.text_frame.paragraphs[0]
    change_run = change_p.add_run()
    change_run.text = change
    change_run.font.size = Pt(11)
    is_positive = "+" in change
    change_run.font.color.rgb = RGBColor(20, 167, 83) if is_positive else RGBColor(214, 69, 55)

def create_slide(
    output_pptx_path: str,
    title_text: str = "Sales Performance KPI Dashboard",
    **kwargs,
) -> str:
    """
    Creates a PPTX file reproducing the Sleek Sales Performance Dashboard visual effect.

    Returns: path to the saved PPTX file.
    """
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    # === Layer 1: Background ===
    background = slide.background
    background.fill.solid()
    background.fill.fore_color.rgb = RGBColor(248, 249, 251)

    # === Layer 2: Content & Widgets ===
    # Add a main title for the dashboard
    title_shape = slide.shapes.add_textbox(Inches(0.5), Inches(0.2), Inches(12), Inches(0.75))
    title_shape.text_frame.paragraphs[0].text = title_text
    title_shape.text_frame.paragraphs[0].font.size = Pt(28)
    title_shape.text_frame.paragraphs[0].font.bold = True
    title_shape.text_frame.paragraphs[0].font.color.rgb = RGBColor(68, 68, 68)

    # --- KPI Cards ---
    gutter = Inches(0.25)
    card_width = (prs.slide_width - Inches(1) - gutter * 3) / 4
    card_height = Inches(2.0)
    card_top = Inches(1.2)
    
    kpi_data = [
        {"title": "REVENUE", "value": "$1,061M", "change": "+14.16%", "icon": "https://api.iconify.design/ph:chart-line-up-bold.svg?color=%23888888&width=32&height=32"},
        {"title": "NEW CUSTOMERS", "value": "10,156", "change": "-11.16%", "icon": "https://api.iconify.design/ph:users-three-bold.svg?color=%23888888&width=32&height=32"},
        {"title": "GROSS PROFIT", "value": "$5,061M", "change": "+4.16%", "icon": "https://api.iconify.design/ph:money-bold.svg?color=%23888888&width=32&height=32"},
        {"title": "CUSTOMER SATISFACTION", "value": "93.15%", "change": "+14.29%", "icon": "https://api.iconify.design/ph:thumbs-up-bold.svg?color=%23888888&width=32&height=32"},
    ]
    
    for i, data in enumerate(kpi_data):
        card_left = Inches(0.5) + i * (card_width + gutter)
        add_kpi_card(slide, card_left, card_top, card_width, card_height, data["title"], data["value"], data["change"], data["icon"])

    # --- Chart Cards ---
    chart_card_top = card_top + card_height + gutter
    chart_card_height = prs.slide_height - chart_card_top - Inches(0.5)
    chart_card_width = (prs.slide_width - Inches(1) - gutter) / 2

    # --- Left Chart Card: Bar Chart ---
    left_chart_card_l = Inches(0.5)
    left_card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left_chart_card_l, chart_card_top, chart_card_width, chart_card_height)
    left_card.fill.solid()
    left_card.fill.fore_color.rgb = RGBColor(255, 255, 255)
    left_card.line.fill.background()
    add_shadow_effect(left_card._element)

    slide.shapes.add_textbox(left_chart_card_l + Inches(0.2), chart_card_top + Inches(0.2), Inches(5), Inches(0.3)).text_frame.paragraphs[0].text = "Sales by Month"

    chart_data = CategoryChartData()
    chart_data.categories = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
    chart_data.add_series('Last Year', (15.2, 18.3, 16.5, 22.1, 25.0, 21.8))
    chart_data.add_series('This Year', (17.8, 20.1, 19.5, 25.3, 28.2, 24.9))

    x, y, cx, cy = left_chart_card_l + Inches(0.2), chart_card_top + Inches(0.6), chart_card_width - Inches(0.4), chart_card_height - Inches(0.8)
    bar_chart = slide.shapes.add_chart(XL_CHART_TYPE.COLUMN_CLUSTERED, x, y, cx, cy, chart_data).chart
    bar_chart.has_legend = True
    bar_chart.legend.position = XL_LEGEND_POSITION.TOP
    bar_chart.value_axis.has_major_gridlines = False
    
    # --- Right Chart Card: Donut Chart ---
    right_chart_card_l = left_chart_card_l + chart_card_width + gutter
    right_card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, right_chart_card_l, chart_card_top, chart_card_width, chart_card_height)
    right_card.fill.solid()
    right_card.fill.fore_color.rgb = RGBColor(255, 255, 255)
    right_card.line.fill.background()
    add_shadow_effect(right_card._element)
    
    slide.shapes.add_textbox(right_chart_card_l + Inches(0.2), chart_card_top + Inches(0.2), Inches(5), Inches(0.3)).text_frame.paragraphs[0].text = "Sales by Product Category"

    chart_data = CategoryChartData()
    chart_data.categories = ['Furniture', 'Office Supplies', 'Technology', 'Apparel']
    chart_data.add_series('Sales (M)', (3.7, 2.5, 3.2, 1.2))

    x, y, cx, cy = right_chart_card_l + Inches(0.2), chart_card_top + Inches(0.6), chart_card_width - Inches(0.4), chart_card_height - Inches(0.8)
    donut_chart = slide.shapes.add_chart(XL_CHART_TYPE.DOUGHNUT, x, y, cx, cy, chart_data).chart
    donut_chart.has_legend = True
    donut_chart.legend.include_in_layout = False
    donut_chart.legend.position = XL_LEGEND_POSITION.RIGHT
    donut_chart.plots[0].has_data_labels = True
    donut_chart.plots[0].data_labels.position = XL_DATA_LABEL_POSITION.OUTSIDE_END
    donut_chart.plots[0].hole_size = 65

    prs.save(output_pptx_path)
    return output_pptx_path
