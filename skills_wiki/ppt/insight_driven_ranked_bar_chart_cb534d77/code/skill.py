import io
import urllib.request
from pptx import Presentation
from pptx.chart.data import ChartData
from pptx.enum.chart import XL_CHART_TYPE, XL_DATA_LABEL_POSITION, XL_LEGEND_POSITION
from pptx.enum.dml import MSO_LINE_DASH_STYLE
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from PIL import Image, ImageDraw

def create_slide(
    output_pptx_path: str,
    title_text: str = "China and India produce the most rice globally, with nearly 400 million tonnes of combined rice production in 2019",
    chart_data_dict: dict = None,
    **kwargs,
) -> str:
    """
    Creates a PowerPoint slide with an insight-driven ranked bar chart.

    This function reproduces the "corporate style" data visualization shown in the tutorial,
    transforming a ranked list into a clean, annotated horizontal bar chart.

    Args:
        output_pptx_path: The path to save the generated .pptx file.
        title_text: The main takeaway message to be used as the slide title.
        chart_data_dict: A dictionary of data for the chart, where keys are category names
                         and values are numeric. Includes 'code' for flag fetching.

    Returns:
        The path to the saved PPTX file.
    """
    if chart_data_dict is None:
        chart_data_dict = {
            "China": {"value": 211, "code": "cn"},
            "India": {"value": 178, "code": "in"},
            "Indonesia": {"value": 55, "code": "id"},
            "Bangladesh": {"value": 55, "code": "bd"},
            "Vietnam": {"value": 43, "code": "vn"},
            "Thailand": {"value": 28, "code": "th"},
            "Myanmar": {"value": 26, "code": "mm"},
            "Philippines": {"value": 19, "code": "ph"},
            "Pakistan": {"value": 11, "code": "pk"},
            "Brazil": {"value": 10, "code": "br"},
        }

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    # === Layer 1: Background (White) ===
    # Default is white, so no code needed.

    # === Layer 2: Text & Content ===
    # Title
    title_shape = slide.shapes.add_textbox(Inches(0.8), Inches(0.5), Inches(11.7), Inches(0.75))
    title_tf = title_shape.text_frame
    title_p = title_tf.paragraphs[0]
    title_p.text = title_text
    title_p.font.name = "Calibri"
    title_p.font.size = Pt(28)
    title_p.font.bold = True
    title_p.font.color.rgb = RGBColor(0, 0, 0)

    # Chart Subtitle
    subtitle_shape = slide.shapes.add_textbox(Inches(3.5), Inches(1.5), Inches(6), Inches(0.5))
    subtitle_p = subtitle_shape.text_frame.paragraphs[0]
    subtitle_p.text = "Biggest Rice Producers\nRice produced by country, in million tonnes (2019)"
    subtitle_p.font.name = "Calibri Light"
    subtitle_p.font.size = Pt(12)
    subtitle_p.font.color.rgb = RGBColor(89, 89, 89)

    # Source
    source_shape = slide.shapes.add_textbox(Inches(0.8), Inches(6.8), Inches(4), Inches(0.5))
    source_p = source_shape.text_frame.paragraphs[0]
    source_p.text = "Source: FAOSTAT, USDA"
    source_p.font.name = "Calibri"
    source_p.font.size = Pt(10)
    source_p.font.italic = True
    source_p.font.color.rgb = RGBColor(128, 128, 128)

    # Supporting Details Box
    details_shape = slide.shapes.add_textbox(Inches(9.2), Inches(1.5), Inches(3.5), Inches(4))
    details_tf = details_shape.text_frame
    details_tf.word_wrap = True
    
    p1 = details_tf.paragraphs[0]
    p1.text = "Key Facts"
    p1.font.name = "Calibri"
    p1.font.size = Pt(16)
    p1.font.bold = True
    p1.space_after = Pt(12)

    key_facts = [
        "Over half of the world’s population lives on rice as a staple food.",
        "756 million tonnes of rice was produced globally in 2019.",
        "Rice is the world’s third-most produced crop, behind sugarcane and corn (maize)."
    ]
    for fact in key_facts:
        p = details_tf.add_paragraph()
        p.text = fact
        p.font.name = "Calibri Light"
        p.font.size = Pt(14)
        p.level = 1
        p.space_after = Pt(8)

    # === Layer 3: Chart & Annotations ===
    chart_data = ChartData()
    chart_data.categories = list(chart_data_dict.keys())
    chart_data.add_series('Production', [d['value'] for d in chart_data_dict.values()])

    x, y, cx, cy = Inches(3.5), Inches(2.0), Inches(5.5), Inches(4.5)
    chart_graphic_frame = slide.shapes.add_chart(
        XL_CHART_TYPE.BAR_CLUSTERED, x, y, cx, cy, chart_data
    )
    chart = chart_graphic_frame.chart

    # Format Chart
    chart.has_legend = False
    chart.value_axis.has_major_gridlines = False
    chart.value_axis.visible = False
    chart.category_axis.visible = False # We create custom labels
    chart.chart_title.text_frame.text = ""

    plot = chart.plots[0]
    plot.has_data_labels = True
    plot.gap_width = 50
    
    series = plot.series[0]
    series.points[0].format.fill.solid()
    series.points[0].format.fill.fore_color.rgb = RGBColor(1, 113, 122)

    data_labels = series.data_labels
    data_labels.position = XL_DATA_LABEL_POSITION.OUTSIDE_END
    data_labels.font.size = Pt(10)
    data_labels.font.name = "Calibri"

    # Custom Category Labels with Flags
    num_categories = len(chart_data.categories)
    bar_area_height = cy / num_categories
    for i, category in enumerate(chart_data.categories):
        label_y = y + (i * bar_area_height) + bar_area_height * 0.1
        
        # Add country name
        label_box = slide.shapes.add_textbox(Inches(1.5), label_y, Inches(1.9), bar_area_height * 0.8)
        label_tf = label_box.text_frame
        label_tf.margin_bottom = 0
        label_tf.margin_top = 0
        p = label_tf.paragraphs[0]
        p.text = category
        p.font.size = Pt(11)
        p.font.name = "Calibri"

        # Add flag
        flag_code = chart_data_dict[category].get("code", "xx")
        flag_url = f"https://flagcdn.com/w40/{flag_code}.png"
        try:
            with urllib.request.urlopen(flag_url) as response:
                image_stream = io.BytesIO(response.read())
                slide.shapes.add_picture(image_stream, Inches(0.8), label_y + Inches(0.05), height=Inches(0.25))
        except Exception: # Fallback if flag cannot be downloaded
            img = Image.new('RGB', (40, 30), color = 'grey')
            img_stream = io.BytesIO()
            img.save(img_stream, 'PNG')
            img_stream.seek(0)
            slide.shapes.add_picture(img_stream, Inches(0.8), label_y + Inches(0.05), height=Inches(0.25))

    # Emphasis Callout
    # Dotted box
    box_shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.7), Inches(2.0), Inches(8.3), Inches(0.95))
    box_shape.fill.background() # No fill
    line = box_shape.line
    line.color.rgb = RGBColor(226, 172, 172)
    line.width = Pt(1.5)
    line.dash_style = MSO_LINE_DASH_STYLE.DASH

    # Annotation text
    callout_box = slide.shapes.add_textbox(Inches(5.0), Inches(2.9), Inches(2.5), Inches(0.5))
    callout_p = callout_box.text_frame.paragraphs[0]
    callout_p.text = "Accounts for 51% of\nglobal rice production"
    callout_p.font.name = "Calibri Light"
    callout_p.font.size = Pt(11)
    callout_p.font.color.rgb = RGBColor(190, 80, 80)
    
    prs.save(output_pptx_path)
    return output_pptx_path

