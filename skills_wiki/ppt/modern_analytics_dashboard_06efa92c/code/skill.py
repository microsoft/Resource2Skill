import io
import urllib.request
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.chart import XL_CHART_TYPE, XL_LEGEND_POSITION, XL_DATA_LABEL_POSITION
from pptx.chart.data import ChartData, CategoryChartData
from pptx.enum.dml import MSO_THEME_COLOR
from lxml import etree
from PIL import Image

def _ns(tag):
    """
    Returns the XML namespace string for a given tag.
    """
    return '{{{}}}{}'.format('http://schemas.openxmlformats.org/drawingml/2006/main', tag)

def apply_shadow(shape):
    """
    Applies a soft outer drop shadow to a shape.
    This requires manipulating the underlying XML.
    """
    try:
        # Get the shape's XML element
        shape_xml = shape.element
        
        # Create the spPr (Shape Properties) element if it doesn't exist
        spPr = shape_xml.get_or_add_spPr()

        # Create the effectLst (Effect List) element
        effectLst = etree.SubElement(spPr, _ns('effectLst'))

        # Create the outerShdw (Outer Shadow) element
        # Attributes set for a soft, bottom-right shadow
        outerShdw = etree.SubElement(effectLst, _ns('outerShdw'), {
            'blurRad': '76200', 'dist': '38100', 'dir': '2700000', 'algn': 'bl', 'rotWithShape': '0'
        })
        
        # Set shadow color (black with 65% transparency)
        srgbClr = etree.SubElement(outerShdw, _ns('srgbClr'), {'val': '000000'})
        etree.SubElement(srgbClr, _ns('alpha'), {'val': '35000'})
        
    except Exception as e:
        print(f"Error applying shadow: {e}")

def create_slide(
    output_pptx_path: str,
    title_text: str = "Dashboard",
    **kwargs,
) -> str:
    """
    Create a PPTX file reproducing the Modern Analytics Dashboard visual effect.

    Returns: path to the saved PPTX file.
    """
    prs = Presentation()
    prs.slide_width = Inches(16)
    prs.slide_height = Inches(9)
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    # === Layer 1: Background ===
    try:
        url = "https://images.pexels.com/photos/911738/pexels-photo-911738.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2"
        with urllib.request.urlopen(url) as response:
            img_data = response.read()
        
        bg_image = Image.open(io.BytesIO(img_data)).convert("RGBA")
        
        # Create a semi-transparent black overlay
        overlay = Image.new('RGBA', bg_image.size, (50, 50, 50, 150))
        
        # Composite the image and the overlay
        composited_image = Image.alpha_composite(bg_image, overlay)
        
        # Save to a byte stream
        img_byte_arr = io.BytesIO()
        composited_image.save(img_byte_arr, format='PNG')
        img_byte_arr = img_byte_arr.getvalue()

        # Add as background
        slide.shapes.add_picture(io.BytesIO(img_byte_arr), 0, 0, width=prs.slide_width, height=prs.slide_height)

    except Exception as e:
        print(f"Could not download background image. Using fallback gradient. Error: {e}")
        # Fallback to a solid color if image download fails
        background = slide.background
        fill = background.fill
        fill.solid()
        fill.fore_color.rgb = RGBColor(220, 220, 220)

    # === Main Dashboard Panel ===
    main_panel = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.25), Inches(0.25), 
        Inches(15.5), Inches(8.5)
    )
    main_panel.fill.solid()
    main_panel.fill.fore_color.rgb = RGBColor(242, 242, 242)
    main_panel.line.fill.background() # No line
    
    # === Toolbar ===
    toolbar = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, Inches(0.25), Inches(0.25), 
        Inches(15.5), Inches(0.75)
    )
    toolbar.fill.solid()
    toolbar.fill.fore_color.rgb = RGBColor(34, 34, 34)
    toolbar.line.fill.background()
    
    # Title
    title_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.25), Inches(3), Inches(0.75))
    p = title_box.text_frame.paragraphs[0]
    p.text = title_text
    p.font.color.rgb = RGBColor(255, 255, 255)
    p.font.size = Pt(20)
    p.font.bold = True

    # Search bar
    search_bar = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE, Inches(12.5), Inches(0.4), 
        Inches(2), Inches(0.45)
    )
    search_bar.fill.solid()
    search_bar.fill.fore_color.rgb = RGBColor(255, 255, 255)
    search_bar.line.fill.background()
    
    # Hamburger
    for i in range(3):
        slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE, Inches(14.8), Inches(0.45 + i*0.15), 
            Inches(0.7), Inches(0.08)
        ).fill.solid()

    # === Data Card Containers ===
    card_top = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.5), Inches(1.2), Inches(15), Inches(1.7))
    card_top.fill.solid()
    card_top.fill.fore_color.rgb = RGBColor(255, 255, 255)
    card_top.line.fill.background()
    apply_shadow(card_top)

    card_left = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.5), Inches(3.1), Inches(4.8), Inches(5.4))
    card_left.fill.solid()
    card_left.fill.fore_color.rgb = RGBColor(255, 255, 255)
    card_left.line.fill.background()
    apply_shadow(card_left)

    card_mid = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(5.6), Inches(3.1), Inches(4.8), Inches(5.4))
    card_mid.fill.solid()
    card_mid.fill.fore_color.rgb = RGBColor(255, 255, 255)
    card_mid.line.fill.background()
    apply_shadow(card_mid)

    card_right = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(10.7), Inches(3.1), Inches(4.8), Inches(5.4))
    card_right.fill.solid()
    card_right.fill.fore_color.rgb = RGBColor(255, 255, 255)
    card_right.line.fill.background()
    apply_shadow(card_right)

    # === TOP CARD CONTENT ===
    # Total Sales
    sales_val = slide.shapes.add_textbox(Inches(0.7), Inches(1.4), Inches(3), Inches(0.8))
    p = sales_val.text_frame.paragraphs[0]
    p.text = "$2,500,000"
    p.font.size = Pt(36)
    p.font.bold = True
    sales_lbl = slide.shapes.add_textbox(Inches(0.7), Inches(2.2), Inches(2), Inches(0.4))
    sales_lbl.text_frame.paragraphs[0].text = "Total Sales"
    
    # Average Deal Size with slider
    deal_val = slide.shapes.add_textbox(Inches(4.5), Inches(1.4), Inches(2.5), Inches(0.8))
    p = deal_val.text_frame.paragraphs[0]
    p.text = "$33,500"
    p.font.size = Pt(36)
    p.font.bold = True
    deal_lbl = slide.shapes.add_textbox(Inches(4.5), Inches(2.2), Inches(2), Inches(0.4))
    deal_lbl.text_frame.paragraphs[0].text = "Avg. Deal Size"
    
    # Slider visual
    slide.shapes.add_shape(MSO_SHAPE.LINE_INV, Inches(6.5), Inches(1.8), Inches(2.5), 0)
    status_bar = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(7.3), Inches(1.65), Inches(0.1), Inches(0.3))
    status_bar.fill.solid()
    status_bar.fill.fore_color.rgb = RGBColor(218, 1, 122)
    status_bar.line.fill.background()
    goal_bar = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(8.3), Inches(1.7), Inches(0.2), Inches(0.2))
    goal_bar.fill.solid()
    goal_bar.fill.fore_color.rgb = RGBColor(118, 188, 33)
    goal_bar.line.fill.background()

    # YTD Sales Target Gauge Chart
    ytd_val = slide.shapes.add_textbox(Inches(9.5), Inches(1.4), Inches(2), Inches(0.8))
    p = ytd_val.text_frame.paragraphs[0]
    p.text = "70%"
    p.font.size = Pt(36)
    p.font.bold = True
    ytd_lbl = slide.shapes.add_textbox(Inches(9.5), Inches(2.2), Inches(2.5), Inches(0.4))
    ytd_lbl.text_frame.paragraphs[0].text = "YTD Sales Target Achv."

    chart_data = ChartData()
    chart_data.categories = ['Achieved', 'Remaining', 'Hidden']
    chart_data.add_series('Series 1', (70, 30, 100))

    x, y, cx, cy = Inches(11.5), Inches(1.3), Inches(2.5), Inches(1.5)
    graphic_frame = slide.shapes.add_chart(
        XL_CHART_TYPE.DOUGHNUT, x, y, cx, cy, chart_data
    )
    chart = graphic_frame.chart
    chart.has_legend = False
    chart.has_title = False

    plot = chart.plots[0]
    plot.has_data_labels = False
    
    # Color the slices
    plot.series[0].points[0].format.fill.solid()
    plot.series[0].points[0].format.fill.fore_color.rgb = RGBColor(218, 1, 122)
    plot.series[0].points[1].format.fill.solid()
    plot.series[0].points[1].format.fill.fore_color.rgb = RGBColor(200, 200, 200)

    # XML part to hide the bottom slice and rotate
    chart_xml = chart._chart.chart_part.chart_xml
    plotArea = chart_xml.find('.//c:plotArea', namespaces=chart_xml.nsmap)
    doughtnutChart = plotArea.find('.//c:doughnutChart', namespaces=chart_xml.nsmap)
    
    # Set rotation
    firstSliceAng = doughtnutChart.find('.//c:firstSliceAng', namespaces=chart_xml.nsmap)
    if firstSliceAng is None:
        firstSliceAng = etree.SubElement(doughtnutChart, '{http://schemas.openxmlformats.org/drawingml/2006/chart}firstSliceAng')
    firstSliceAng.set('val', '270')
    
    # Hide the third data point
    ser = doughtnutChart.find('.//c:ser', namespaces=chart_xml.nsmap)
    dPt = ser.findall('.//c:dPt', namespaces=chart_xml.nsmap)[2] # 3rd data point
    spPr = etree.SubElement(dPt, '{http://schemas.openxmlformats.org/drawingml/2006/chart}spPr')
    etree.SubElement(spPr, '{http://schemas.openxmlformats.org/drawingml/2006/main}noFill')

    # === LEFT CARD CONTENT: Sales by Account ===
    left_title_box = slide.shapes.add_textbox(Inches(0.7), Inches(3.3), Inches(4), Inches(0.5))
    p = left_title_box.text_frame.paragraphs[0]
    p.text = "Sales by Account"
    p.font.bold = True
    
    # Custom Horizontal Bars
    accounts = [("Account #1", 22), ("Account #2", 20), ("Account #3", 15), ("Account #4", 9), ("Account #5", 2)]
    bar_width = Inches(3.5)
    for i, (name, value) in enumerate(accounts):
        y_pos = Inches(4.0 + i * 0.8)
        # Label
        lbl_box = slide.shapes.add_textbox(Inches(0.7), y_pos - Inches(0.1), Inches(1.5), Inches(0.3))
        lbl_box.text_frame.paragraphs[0].text = name
        
        # Background Bar
        bg_bar = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(2.2), y_pos, bar_width, Inches(0.2))
        bg_bar.fill.solid()
        bg_bar.fill.fore_color.rgb = RGBColor(200, 200, 200)
        bg_bar.line.fill.background()
        
        # Value Bar
        val_bar = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(2.2), y_pos, bar_width * (value / 100), Inches(0.2))
        val_bar.fill.solid()
        val_bar.fill.fore_color.rgb = RGBColor(255, 204, 0)
        val_bar.line.fill.background()

    prs.save(output_pptx_path)
    return output_pptx_path
