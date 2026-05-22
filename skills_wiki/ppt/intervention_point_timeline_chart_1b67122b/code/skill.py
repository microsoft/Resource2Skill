import collections
from pptx import Presentation
from pptx.chart.data import ChartData
from pptx.enum.chart import XL_CHART_TYPE, XL_LEGEND_POSITION
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.dml import MSO_THEME_COLOR
from lxml import etree

def create_slide(
    output_pptx_path: str,
    chart_title: str = "Before-and-After Comparison Chart",
    y_axis_title: str = "Defect Rate %",
    raw_data: dict = None,
    intervention_date: str = "2/10/2019",
) -> str:
    """
    Creates a PPTX slide with a 'before-and-after' intervention point chart.

    Args:
        output_pptx_path: Path to save the generated .pptx file.
        chart_title: The main title for the chart.
        y_axis_title: The title for the vertical (value) axis.
        raw_data: A dictionary of {date_string: value}.
        intervention_date: The date string marking the intervention.

    Returns:
        Path to the saved PPTX file.
    """
    # --- Sample Data if none provided ---
    if raw_data is None:
        raw_data = collections.OrderedDict([
            ("2/2/2019", 20), ("2/3/2019", 18), ("2/4/2019", 21),
            ("2/5/2019", 19), ("2/6/2019", 20), ("2/7/2019", 16),
            ("2/8/2019", 19), ("2/9/2019", 15), ("2/10/2019", 10), # Value on intervention day is part of 'after'
            ("2/11/2019", 9.5), ("2/12/2019", 9), ("2/13/2019", 8.5),
            ("2/14/2019", 9), ("2/15/2019", 8), ("2/16/2019", 7),
            ("2/17/2019", 7.5), ("2/18/2019", 7)
        ])

    # --- 1. Data Preparation ---
    categories = list(raw_data.keys())
    max_value = max(v for v in raw_data.values() if v is not None) * 1.1

    try:
        intervention_idx = categories.index(intervention_date)
    except ValueError:
        raise ValueError(f"Intervention date '{intervention_date}' not found in data keys.")

    before_values = [raw_data[cat] if i < intervention_idx else None for i, cat in enumerate(categories)]
    after_values = [raw_data[cat] if i >= intervention_idx else None for i, cat in enumerate(categories)]
    intervention_values = [max_value if i == intervention_idx else None for i, cat in enumerate(categories)]

    chart_data = ChartData()
    chart_data.categories = categories
    chart_data.add_series('Before', before_values)
    chart_data.add_series('After', after_values)
    # Give the intervention series a "hidden" name so it doesn't show in legend easily
    chart_data.add_series('_Intervention', intervention_values)

    # --- 2. Create Presentation and Slide ---
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide_layout = prs.slide_layouts[6]  # Blank layout
    slide = prs.slides.add_slide(slide_layout)

    # --- Set Slide Background Color ---
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(47, 85, 151)

    # --- 3. Add a base LINE chart (will be modified to combo) ---
    x, y, cx, cy = Inches(0.5), Inches(0.5), Inches(12.333), Inches(6.5)
    graphic_frame = slide.shapes.add_chart(
        XL_CHART_TYPE.LINE, x, y, cx, cy, chart_data
    )
    chart = graphic_frame.chart
    chart.has_legend = True
    chart.legend.position = XL_LEGEND_POSITION.TOP
    chart.legend.include_in_layout = False
    chart.legend.font.color.rgb = RGBColor(255, 255, 255)

    # --- 4. Style Chart Elements using python-pptx ---
    chart.chart_title.text_frame.text = chart_title
    chart.chart_title.text_frame.paragraphs[0].font.color.rgb = RGBColor(255, 255, 255)
    chart.chart_title.text_frame.paragraphs[0].font.size = Pt(24)

    category_axis = chart.category_axis
    category_axis.tick_labels.font.color.rgb = RGBColor(255, 255, 255)
    category_axis.major_tick_mark = 0 # No tick marks
    
    value_axis = chart.value_axis
    value_axis.has_title = True
    value_axis.axis_title.text_frame.text = y_axis_title
    value_axis.axis_title.text_frame.paragraphs[0].font.color.rgb = RGBColor(255, 255, 255)
    value_axis.tick_labels.font.color.rgb = RGBColor(255, 255, 255)
    value_axis.maximum_scale = max_value
    
    # Style Gridlines and Plot Area
    value_axis.has_major_gridlines = True
    gridlines = value_axis.major_gridlines
    gridlines.format.line.color.rgb = RGBColor(255, 255, 255)
    gridlines.format.line.width = Pt(0.5)
    
    chart.plot_area.format.fill.solid()
    chart.plot_area.format.fill.fore_color.rgb = RGBColor(47, 85, 151)
    chart.plot_area.format.line.fill.background()

    # Style the line series
    chart.series[0].format.line.color.rgb = RGBColor(0, 0, 0) # Before
    chart.series[0].marker.style = 1
    chart.series[1].format.line.color.rgb = RGBColor(255, 0, 0) # After
    chart.series[1].marker.style = 1

    # --- 5. LXML Magic: Convert to Combo Chart ---
    # Helper to get namespaced tag
    def qn(tag):
        ns = {
            'c': 'http://schemas.openxmlformats.org/drawingml/2006/chart',
            'a': 'http://schemas.openxmlformats.org/drawingml/2006/main'
        }
        prefix, tagroot = tag.split(':')
        return '{{{}}}{}'.format(ns[prefix], tagroot)

    # Get the chart's XML element
    chart_xml = etree.fromstring(chart.part.blob)
    plot_area = chart_xml.find(qn('c:chart')).find(qn('c:plotArea'))
    
    # Create a new barChart element
    bar_chart = etree.SubElement(plot_area, qn('c:barChart'))
    etree.SubElement(bar_chart, qn('c:barDir'), val="col")
    etree.SubElement(bar_chart, qn('c:grouping'), val="stacked")
    etree.SubElement(bar_chart, qn('c:axId'), val=str(chart.value_axis.axis_id))
    etree.SubElement(bar_chart, qn('c:axId'), val=str(chart.category_axis.axis_id))

    # Move the third series (intervention) from lineChart to barChart
    line_chart = plot_area.find(qn('c:lineChart'))
    intervention_ser = line_chart.xpath('c:ser[c:idx[@val="2"]]')[0]
    line_chart.remove(intervention_ser)
    bar_chart.append(intervention_ser)
    
    # Style the intervention bar to be thin
    etree.SubElement(bar_chart, qn('c:gapWidth'), val="500")

    # Set color for the intervention bar series
    spPr = intervention_ser.find(qn('c:spPr'))
    if spPr is None:
        spPr = etree.SubElement(intervention_ser, qn('c:spPr'))
    
    solidFill = etree.SubElement(spPr, qn('a:solidFill'))
    srgbClr = etree.SubElement(solidFill, qn('a:srgbClr'), val="F4B084") # Orange color
    
    # Remove the border from the bar
    ln = etree.SubElement(spPr, qn('a:ln'))
    etree.SubElement(ln, qn('a:noFill'))
    
    # Remove the intervention series from the legend by finding its entry and deleting it
    legend = chart_xml.find(qn('c:chart')).find(qn('c:legend'))
    if legend is not None:
        legend_entry_to_remove = legend.xpath('c:legendEntry[c:idx[@val="2"]]')
        if legend_entry_to_remove:
            legend.remove(legend_entry_to_remove[0])

    # Replace the chart XML with our modified version
    chart.part.blob = etree.tostring(chart_xml, pretty_print=True)

    # --- 6. Save Presentation ---
    prs.save(output_pptx_path)
    return output_pptx_path

# Example usage:
# create_slide("before_after_chart.pptx")
