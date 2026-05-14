def create_slide(
    output_pptx_path: str,
    title_text: str = "Quarterly Revenue Spotlight",
    accent_color: tuple = (0, 191, 255),  # Cyan bars
    spotlight_color: tuple = (255, 215, 0),  # Gold spotlight
    **kwargs,
) -> str:
    """
    Creates a two-slide presentation demonstrating the 'Data Spotlight Reveal via Morph' technique.
    Slide 1 establishes the chart context; Slide 2 smoothly morphs a spotlight over the key data point.
    """
    import os
    from pptx import Presentation
    from pptx.chart.data import CategoryChartData
    from pptx.enum.chart import XL_CHART_TYPE
    from pptx.enum.shapes import MSO_SHAPE
    from pptx.dml.color import RGBColor
    from pptx.util import Inches, Pt
    from lxml import etree
    from pptx.oxml import OxmlElement
    from pptx.oxml.ns import qn
    from PIL import Image, ImageDraw

    # --- Utility Functions for XML Injection ---
    
    def force_transparent_fill(shape):
        """Forces a shape to have absolutely no fill via OOXML injection."""
        spPr = shape.element.spPr
        for child in spPr.xpath('a:solidFill | a:gradFill | a:blipFill | a:pattFill | a:noFill'):
            spPr.remove(child)
        spPr.insert(0, OxmlElement('a:noFill'))

    def force_morph_name(shape, name="!!Spotlight"):
        """Prefixes shape name with '!!' to force PowerPoint's Morph engine to match them."""
        cNvPr = shape.element.nvSpPr.cNvPr
        cNvPr.set('name', name)

    def inject_morph_transition(slide):
        """Injects the Morph transition XML directly into the slide element."""
        transition = OxmlElement('p:transition')
        transition.set('spd', 'slow')
        
        # Create morph element with the correct namespace mapped locally
        morph = etree.Element("{http://schemas.microsoft.com/office/powerpoint/2010/main}morph", 
                              nsmap={'p14': 'http://schemas.microsoft.com/office/powerpoint/2010/main'})
        morph.set('option', 'byObject')
        transition.append(morph)
        
        # Safe insertion point in slide XML
        cSld = slide.element.find(qn('p:cSld'))
        if cSld is not None:
            cSld.addnext(transition)
        else:
            slide.element.insert(0, transition)

    # --- Step 1: Generate Premium Gradient Background ---
    bg_path = "temp_spotlight_bg.png"
    img = Image.new('RGB', (1920, 1080))
    draw = ImageDraw.Draw(img)
    color1, color2 = (13, 17, 28), (30, 45, 65)
    for y in range(1080):
        r = int(color1[0] + (color2[0] - color1[0]) * y / 1080)
        g = int(color1[1] + (color2[1] - color1[1]) * y / 1080)
        b = int(color1[2] + (color2[2] - color1[2]) * y / 1080)
        draw.line([(0, y), (1920, y)], fill=(r, g, b))
    img.save(bg_path)

    # --- Step 2: Setup Presentation & Data ---
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    chart_data = CategoryChartData()
    chart_data.categories = ['Q1', 'Q2', 'Q3', 'Q4']
    chart_data.add_series('Revenue', (4.3, 2.5, 3.5, 6.8))

    # --- Step 3: Create Slide 1 (The Macro Context) ---
    slide1 = prs.slides.add_slide(prs.slide_layouts[6])
    slide1.shapes.add_picture(bg_path, 0, 0, prs.slide_width, prs.slide_height)

    # Title
    txBox = slide1.shapes.add_textbox(Inches(1), Inches(0.5), Inches(11.33), Inches(1))
    p = txBox.text_frame.add_paragraph()
    p.text = title_text
    p.font.size = Pt(44)
    p.font.color.rgb = RGBColor(255, 255, 255)
    p.font.bold = True

    # Chart
    chart_x, chart_y, chart_cx, chart_cy = Inches(1), Inches(2), Inches(11.33), Inches(4.5)
    chart_obj = slide1.shapes.add_chart(XL_CHART_TYPE.COLUMN_CLUSTERED, chart_x, chart_y, chart_cx, chart_cy, chart_data).chart
    chart_obj.has_legend = False
    
    # Style Chart Series
    series = chart_obj.series[0]
    series.format.fill.solid()
    series.format.fill.fore_color.rgb = RGBColor(*accent_color)
    
    # Lighten Axes for dark background
    chart_obj.category_axis.tick_labels.font.color.rgb = RGBColor(200, 200, 200)
    chart_obj.value_axis.tick_labels.font.color.rgb = RGBColor(200, 200, 200)

    # Spotlight 1 (Small, resting on Q1)
    # Math: Center of 1st column is roughly 1/8th across the chart width
    s1_size = Inches(1.5)
    s1_left = chart_x + (chart_cx / 8) - (s1_size / 2)
    s1_top = Inches(3.5)
    
    spotlight1 = slide1.shapes.add_shape(MSO_SHAPE.OVAL, s1_left, s1_top, s1_size, s1_size)
    force_transparent_fill(spotlight1)
    spotlight1.line.color.rgb = RGBColor(*spotlight_color)
    spotlight1.line.width = Pt(4)
    force_morph_name(spotlight1, "!!Spotlight")


    # --- Step 4: Create Slide 2 (The Micro Focus) ---
    slide2 = prs.slides.add_slide(prs.slide_layouts[6])
    slide2.shapes.add_picture(bg_path, 0, 0, prs.slide_width, prs.slide_height)

    # Duplicate Title
    txBox2 = slide2.shapes.add_textbox(Inches(1), Inches(0.5), Inches(11.33), Inches(1))
    p2 = txBox2.text_frame.add_paragraph()
    p2.text = title_text
    p2.font.size = Pt(44)
    p2.font.color.rgb = RGBColor(255, 255, 255)
    p2.font.bold = True

    # Duplicate Chart
    chart_obj2 = slide2.shapes.add_chart(XL_CHART_TYPE.COLUMN_CLUSTERED, chart_x, chart_y, chart_cx, chart_cy, chart_data).chart
    chart_obj2.has_legend = False
    series2 = chart_obj2.series[0]
    series2.format.fill.solid()
    series2.format.fill.fore_color.rgb = RGBColor(*accent_color)
    chart_obj2.category_axis.tick_labels.font.color.rgb = RGBColor(200, 200, 200)
    chart_obj2.value_axis.tick_labels.font.color.rgb = RGBColor(200, 200, 200)

    # Spotlight 2 (Large, framed over Q4 outlier)
    # Math: Center of 4th column is roughly 7/8th across the chart width
    s2_size = Inches(3.5)
    s2_left = chart_x + (chart_cx * 7 / 8) - (s2_size / 2)
    s2_top = Inches(1.5)

    spotlight2 = slide2.shapes.add_shape(MSO_SHAPE.OVAL, s2_left, s2_top, s2_size, s2_size)
    force_transparent_fill(spotlight2)
    spotlight2.line.color.rgb = RGBColor(*spotlight_color)
    spotlight2.line.width = Pt(10)  # Thicker line implies scaling up
    force_morph_name(spotlight2, "!!Spotlight")

    # Apply Morph Transition to Slide 2
    inject_morph_transition(slide2)

    # --- Cleanup & Save ---
    prs.save(output_pptx_path)
    if os.path.exists(bg_path):
        os.remove(bg_path)
        
    return output_pptx_path
