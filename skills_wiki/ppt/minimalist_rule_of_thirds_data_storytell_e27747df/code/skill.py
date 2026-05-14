import os
import urllib.request
from io import BytesIO
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.chart import XL_CHART_TYPE, XL_TICK_MARK, XL_LABEL_POSITION
from pptx.enum.text import PP_ALIGN
from pptx.chart.data import CategoryChartData
from PIL import Image

def create_slide(
    output_pptx_path: str,
    title_text: str = "Customer Survey Results",
    subtitle_text: str = "Availability is the most critical factor for our users.",
    image_keyword: str = "business,portrait",
    accent_color: tuple = (56, 178, 172),  # Teal
    text_color: tuple = (51, 51, 51)       # Charcoal
) -> str:
    """
    Creates a minimalist PPTX slide using the Rule of Thirds, White Space, 
    and Data Visualization principles.
    """
    prs = Presentation()
    # Set to 16:9 Widescreen
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    # Use blank slide layout
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    # ---------------------------------------------------------
    # 1. RULE OF THIRDS: LEFT IMAGE ANCHOR (Using PIL for precise crop)
    # ---------------------------------------------------------
    # The slide is 13.333" wide. One third is ~4.444"
    third_width = 13.333 / 3
    slide_height = 7.5
    target_ratio = third_width / slide_height  # approx 0.5925

    try:
        # Fetch image
        url = f"https://source.unsplash.com/random/800x1200/?{image_keyword}"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            img = Image.open(BytesIO(response.read()))
            
        # Crop to exactly fit the left third without distortion
        img_w, img_h = img.size
        img_ratio = img_w / img_h
        
        if img_ratio > target_ratio:
            # Crop width
            new_w = int(img_h * target_ratio)
            left = (img_w - new_w) // 2
            img = img.crop((left, 0, left + new_w, img_h))
        else:
            # Crop height
            new_h = int(img_w / target_ratio)
            top = (img_h - new_h) // 2
            img = img.crop((0, top, img_w, top + new_h))
            
        img_stream = BytesIO()
        img.save(img_stream, format='PNG')
        img_stream.seek(0)
        
        slide.shapes.add_picture(img_stream, 0, 0, width=Inches(third_width), height=Inches(slide_height))
    except Exception as e:
        print(f"Image fetch failed, using fallback solid color: {e}")
        # Fallback: Create a solid gray rectangle using python-pptx
        shape = slide.shapes.add_shape(
            1, 0, 0, width=Inches(third_width), height=Inches(slide_height) # 1 = MSO_SHAPE.RECTANGLE
        )
        shape.fill.solid()
        shape.fill.fore_color.rgb = RGBColor(200, 200, 200)
        shape.line.fill.background()

    # ---------------------------------------------------------
    # 2. WHITE SPACE & TYPOGRAPHY: RIGHT TWO-THIRDS
    # ---------------------------------------------------------
    # Place text boxes giving ample breathing room (starting at X = 5.5")
    # Title placed near the upper horizontal "Rule of Thirds" line (~2.5")
    
    title_box = slide.shapes.add_textbox(Inches(5.5), Inches(1.0), Inches(7.0), Inches(1.0))
    tf = title_box.text_frame
    p = tf.paragraphs[0]
    p.text = title_text
    p.font.size = Pt(40)
    p.font.bold = True
    p.font.color.rgb = RGBColor(*text_color)
    p.font.name = "Arial"

    sub_box = slide.shapes.add_textbox(Inches(5.5), Inches(1.8), Inches(7.0), Inches(0.5))
    tf_sub = sub_box.text_frame
    p_sub = tf_sub.paragraphs[0]
    p_sub.text = subtitle_text
    p_sub.font.size = Pt(18)
    p_sub.font.color.rgb = RGBColor(120, 120, 120)  # Subtle gray
    p_sub.font.name = "Arial"

    # ---------------------------------------------------------
    # 3. VISUALIZE DATA: HORIZONTAL BAR CHART
    # ---------------------------------------------------------
    # Replacing bullet points with a clean horizontal bar chart
    chart_data = CategoryChartData()
    chart_data.categories = ['Availability', 'Price', 'Service', 'Online Shop', 'Tech Support']
    chart_data.add_series('Importance', (84, 70, 63, 33, 25))

    # Add chart in the remaining white space
    chart_shape = slide.shapes.add_chart(
        XL_CHART_TYPE.BAR_CLUSTERED, 
        Inches(5.5), Inches(2.8), 
        Inches(6.5), Inches(4.0), 
        chart_data
    )
    chart = chart_shape.chart

    # Strip away chart clutter (Applying tip: Less is more)
    chart.has_legend = False
    
    # Category Axis (Y-axis for horizontal charts) formatting
    cat_axis = chart.category_axis
    cat_axis.has_major_gridlines = False
    cat_axis.major_tick_mark = XL_TICK_MARK.NONE
    cat_axis.format.line.fill.background() # Hide axis line
    cat_axis.tick_labels.font.size = Pt(14)
    cat_axis.tick_labels.font.color.rgb = RGBColor(*text_color)

    # Value Axis (X-axis for horizontal charts) formatting
    val_axis = chart.value_axis
    val_axis.has_major_gridlines = False
    val_axis.visible = False # Completely hide the numbers at the bottom

    # Format the bars and add Data Labels to the ends
    plot = chart.plots[0]
    plot.has_data_labels = True
    data_labels = plot.data_labels
    data_labels.font.size = Pt(14)
    data_labels.font.bold = True
    data_labels.font.color.rgb = RGBColor(*accent_color)
    data_labels.position = XL_LABEL_POSITION.OUTSIDE_END

    series = plot.series[0]
    series.format.fill.solid()
    series.format.fill.fore_color.rgb = RGBColor(*accent_color)
    series.invert_if_negative = False
    
    # Adjust bar thickness (Gap Width)
    plot.gap_width = 80  # Lower number = thicker bars

    # Save presentation
    prs.save(output_pptx_path)
    return output_pptx_path

# Example execution:
# create_slide("rule_of_thirds_data_slide.pptx")
