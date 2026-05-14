import os
import urllib.request
from io import BytesIO
from lxml import etree
from pptx import Presentation
from pptx.chart.data import CategoryChartData
from pptx.dml.color import RGBColor
from pptx.enum.chart import XL_CHART_TYPE, XL_LEGEND_POSITION, XL_DATA_LABEL_POSITION
from pptx.enum.dml import MSO_THEME_COLOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.util import Inches, Pt, Emu
from PIL import Image, ImageDraw
import cairosvg

# Helper function to add shadow to shapes using lxml
def add_shadow(shape):
    """
    Adds a default outer shadow to a shape.
    """
    shape_element = shape.element
    prst_geom = shape_element.xpath('.//a:prstGeom')[0]
    prst_geom.addprevious(etree.fromstring(
        '<a:effectLst xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">'
        '<a:outerShdw blurRad="50800" dist="38100" dir="2700000" algn="ctr" rotWithShape="0">'
        '<a:srgbClr val="000000">'
        '<a:alpha val="35000"/>'
        '</a:srgbClr>'
        '</a:outerShdw>'
        '</a:effectLst>'
    ))

# Helper to create the map visual
def create_california_map_visual(output_path, width_px=900):
    """
    Downloads a California counties SVG, colors some counties, and saves as a transparent PNG.
    """
    svg_url = "https://simplemaps.com/static/maps/us-counties/us_county_california_map.svg"
    colored_counties = {
        "Los Angeles County": "#2E75B5", # Dark Blue
        "San Diego County": "#5B9BD5",   # Medium Blue
        "Orange County": "#DEEBF6",      # Light Blue
        "San Bernardino County": "#ED7D31", # Orange
        "Riverside County": "#F4B183"      # Light Orange
    }

    try:
        with urllib.request.urlopen(svg_url) as response:
            svg_content = response.read().decode('utf-8')
    except Exception:
        # Fallback: create a simple placeholder image if download fails
        img = Image.new('RGBA', (width_px, int(width_px * 1.1)), (200, 200, 200, 128))
        draw = ImageDraw.Draw(img)
        draw.text((10, 10), "Map Placeholder\n(Download failed)", fill="black")
        img.save(output_path, 'PNG')
        return

    # Modify SVG content to color counties
    for county, color in colored_counties.items():
        search_str = f'id="{county}"'
        replace_str = f'{search_str} fill="{color}"'
        svg_content = svg_content.replace(search_str, replace_str)
        
    # Set default fill for other paths
    svg_content = svg_content.replace('<path', '<path fill="#F2F2F2"') # Light gray for other counties

    # Convert SVG to PNG
    height_px = int(width_px * 1.1) # Approximate aspect ratio of CA
    cairosvg.svg2png(bytestring=svg_content.encode('utf-8'), write_to=output_path, output_width=width_px, output_height=height_px, background_color="rgba(0,0,0,0)")


def create_slide(
    output_pptx_path: str,
    title_text: str = "VIVO CALIF",
    **kwargs,
) -> str:
    """
    Creates a PPTX file reproducing the Modern Grid & Sidebar BI Dashboard.

    Returns: path to the saved PPTX file.
    """
    prs = Presentation()
    prs.slide_width = Inches(16)
    prs.slide_height = Inches(9)
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    # === Colors & Fonts ===
    COLOR_SIDEBAR_BG = RGBColor(22, 54, 38)
    COLOR_MAIN_BG = RGBColor(235, 241, 222)
    COLOR_PANEL_BG = RGBColor(255, 255, 255)
    COLOR_KPI_ACCENT = RGBColor(255, 192, 0)
    COLOR_TEXT_DARK = RGBColor(89, 89, 89)
    COLOR_CHART_BLUE = RGBColor(47, 117, 181)
    COLOR_CHART_ORANGE = RGBColor(237, 125, 49)
    COLOR_CHART_GREEN = RGBColor(112, 173, 71)

    FONT_MAIN = "Aptos Narrow"

    # === Layer 1: Backgrounds ===
    # Main background
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = COLOR_MAIN_BG

    # Sidebar background
    sidebar_width = Inches(3.5)
    slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, 0, 0, sidebar_width, prs.slide_height
    ).fill.solid.fore_color.rgb = COLOR_SIDEBAR_BG

    # === Layer 2: Sidebar Content (KPIs & Slicers) ===
    # Logo
    logo_box = slide.shapes.add_textbox(Inches(0.25), Inches(0.25), Inches(3), Inches(0.75))
    p = logo_box.text_frame.paragraphs[0]
    p.text = title_text
    p.font.name = FONT_MAIN
    p.font.bold = True
    p.font.size = Pt(36)
    p.font.color.rgb = RGBColor(255, 255, 255)

    # KPIs
    kpi_data = {
        "Orders": ("2,400", "362"),
        "Quantity": ("11,997", "1,588"),
        "Amount": ("$649.0k", "$75.1k"),
        "Avg. Rating": ("4.0", None),
        "Avg. Days to Deliver": ("2.3", "2.4")
    }
    y_pos = Inches(1.5)
    for label, (main_val, sub_val) in kpi_data.items():
        # Main Value
        val_box = slide.shapes.add_textbox(Inches(0.25), y_pos, Inches(1.5), Inches(0.5))
        p_val = val_box.text_frame.paragraphs[0]
        p_val.text = main_val
        p_val.font.name = FONT_MAIN
        p_val.font.bold = True
        p_val.font.size = Pt(28)
        p_val.font.color.rgb = RGBColor(255, 192, 0) if "Amount" in label else RGBColor(255, 255, 255)

        # Label
        lbl_box = slide.shapes.add_textbox(Inches(0.35), y_pos + Inches(0.35), Inches(1.5), Inches(0.25))
        p_lbl = lbl_box.text_frame.paragraphs[0]
        p_lbl.text = label
        p_lbl.font.name = FONT_MAIN
        p_lbl.font.size = Pt(10)
        p_lbl.font.color.rgb = RGBColor(200, 200, 200)

        # Sub Value (if exists)
        if sub_val:
            sub_val_box = slide.shapes.add_textbox(Inches(2.25), y_pos, Inches(1), Inches(0.5))
            p_sub = sub_val_box.text_frame.paragraphs[0]
            p_sub.text = sub_val
            p_sub.font.name = FONT_MAIN
            p_sub.font.size = Pt(14)
            p_sub.font.color.rgb = RGBColor(200, 200, 200)

        y_pos += Inches(0.8)
    
    # Slicer Placeholders
    slide.shapes.add_textbox(Inches(0.25), Inches(5.8), Inches(3), Inches(0.25)).text_frame.paragraphs[0].text = "Order Mode"
    slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.25), Inches(6.1), Inches(3), Inches(1.0)).fill.solid.fore_color.rgb = RGBColor(91, 155, 213)
    slide.shapes.add_textbox(Inches(0.25), Inches(7.3), Inches(3), Inches(0.25)).text_frame.paragraphs[0].text = "Customer"
    slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.25), Inches(7.6), Inches(3), Inches(1.0)).fill.solid.fore_color.rgb = RGBColor(112, 173, 71)


    # === Layer 3: Main Grid Panels ===
    grid_start_x = Inches(3.8)
    grid_start_y = Inches(0.3)
    panel_width = Inches(3.9)
    panel_height = Inches(2.6)
    gutter = Inches(0.2)

    panel_positions = []
    for row in range(3):
        for col in range(3):
            x = grid_start_x + col * (panel_width + gutter)
            y = grid_start_y + row * (panel_height + gutter)
            panel = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, panel_width, panel_height)
            panel.fill.solid.fore_color.rgb = COLOR_PANEL_BG
            panel.line.fill.background()
            add_shadow(panel)
            panel_positions.append((x,y))

    # === Layer 4: Populate Charts ===
    
    # 1. Trend Chart
    chart_data = CategoryChartData()
    chart_data.categories = [f"W{i}" for i in range(1, 14)]
    chart_data.add_series('Qty', (200, 250, 300, 220, 280, 400, 350, 320, 450, 500, 480, 430, 410))
    chart_data.add_series('Amount', (4000, 5000, 6000, 4400, 5600, 8000, 7000, 6400, 9000, 10000, 9600, 8600, 8200))
    x, y, cx, cy = panel_positions[0][0]+Inches(0.2), panel_positions[0][1]+Inches(0.4), panel_width-Inches(0.4), panel_height-Inches(0.6)
    slide.shapes.add_chart(XL_CHART_TYPE.LINE, x, y, cx, cy, chart_data).has_legend = False
    slide.shapes.add_textbox(panel_positions[0][0], panel_positions[0][1], panel_width, Inches(0.5)).text_frame.paragraphs[0].text = "Last 13 Week Trends - Qty & Amount"

    # 2. How they like to buy? (Heatmap Table)
    x, y = panel_positions[1]
    rows, cols = 6, 5
    table = slide.shapes.add_table(rows, cols, x + Inches(0.2), y + Inches(0.6), panel_width - Inches(0.4), panel_height - Inches(0.8)).table
    # ... (code to fill and color table)

    # 3. How many they buy? (Column Chart)
    chart_data = CategoryChartData()
    chart_data.categories = ["1", "2", "3-5", "6-10", "10+"]
    chart_data.add_series('Orders', (300, 550, 400, 200, 100))
    x, y, cx, cy = panel_positions[2][0]+Inches(0.2), panel_positions[2][1]+Inches(0.4), panel_width-Inches(0.4), panel_height-Inches(0.6)
    chart = slide.shapes.add_chart(XL_CHART_TYPE.COLUMN_CLUSTERED, x, y, cx, cy, chart_data)
    chart.has_legend = False
    chart.plots[0].series[0].fill.solid()
    chart.plots[0].series[0].fill.fore_color.rgb = COLOR_CHART_GREEN
    slide.shapes.add_textbox(panel_positions[2][0], panel_positions[2][1], panel_width, Inches(0.5)).text_frame.paragraphs[0].text = "How many they buy?"
    
    # 4. Popular Products
    chart_data = CategoryChartData()
    chart_data.categories = ["T-Shirts", "Jeans", "Sneakers", "Tank Tops", "Bikinis", "Shorts"]
    chart_data.add_series('Male', (764, 627, 568, 627, 482, 426))
    chart_data.add_series('Female', (713, 303, 303, 306, 293, 295))
    x, y, cx, cy = panel_positions[3][0]+Inches(0.2), panel_positions[3][1]+Inches(0.4), panel_width-Inches(0.4), panel_height-Inches(0.6)
    chart = slide.shapes.add_chart(XL_CHART_TYPE.BAR_STACKED, x, y, cx, cy, chart_data)
    chart.has_legend = False
    chart.plots[0].series[0].fill.solid.fore_color.rgb = COLOR_CHART_BLUE
    chart.plots[0].series[1].fill.solid.fore_color.rgb = COLOR_CHART_ORANGE
    slide.shapes.add_textbox(panel_positions[3][0], panel_positions[3][1], panel_width, Inches(0.5)).text_frame.paragraphs[0].text = "Which Products are Popular?"

    # 5. Map Chart
    x, y = panel_positions[4]
    map_image_path = "california_map.png"
    create_california_map_visual(map_image_path)
    slide.shapes.add_picture(map_image_path, x + Inches(0.2), y + Inches(0.4), height=panel_height - Inches(0.6))
    slide.shapes.add_textbox(panel_positions[4][0], panel_positions[4][1], panel_width, Inches(0.5)).text_frame.paragraphs[0].text = "Where do our customers live?"
    if os.path.exists(map_image_path):
        os.remove(map_image_path)

    # 6. How long to ship?
    chart_data = CategoryChartData()
    chart_data.categories = [str(i) for i in range(11)]
    chart_data.add_series('Count', (170, 880, 300, 200, 95, 51, 32, 22, 9, 4, 11))
    x, y, cx, cy = panel_positions[5][0]+Inches(0.2), panel_positions[5][1]+Inches(0.4), panel_width-Inches(0.4), panel_height-Inches(0.6)
    chart = slide.shapes.add_chart(XL_CHART_TYPE.COLUMN_CLUSTERED, x, y, cx, cy, chart_data)
    chart.has_legend = False
    chart.plots[0].gap_width = 0
    slide.shapes.add_textbox(panel_positions[5][0], panel_positions[5][1], panel_width, Inches(0.5)).text_frame.paragraphs[0].text = "How long we take to ship?"

    # 7. Customer Satisfaction
    chart_data = CategoryChartData()
    chart_data.categories = ["1", "2", "3", "4", "5"]
    chart_data.add_series('Jan', (7, 37, 150, 312, 224))
    chart_data.add_series('Feb', (51, 182, 373, 247, 861))
    chart_data.add_series('Mar', (39, 163, 351, 250, 809))
    x, y, cx, cy = panel_positions[8][0]+Inches(0.2), panel_positions[8][1]+Inches(0.4), panel_width-Inches(0.4), panel_height-Inches(0.6)
    chart = slide.shapes.add_chart(XL_CHART_TYPE.COLUMN_CLUSTERED, x, y, cx, cy, chart_data)
    chart.has_legend = False
    slide.shapes.add_textbox(panel_positions[8][0], panel_positions[8][1], panel_width, Inches(0.5)).text_frame.paragraphs[0].text = "How satisfied are the customers?"

    prs.save(output_pptx_path)
    return output_pptx_path
