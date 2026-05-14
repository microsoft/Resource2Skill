# Minimalist "Rule of Thirds" Data Storytelling Layout

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Minimalist "Rule of Thirds" Data Storytelling Layout

* **Core Visual Mechanism**: This pattern replaces cluttered text bullets with a clean, bifurcated layout governed by the "Rule of Thirds". The left third of the slide is anchored by an edge-to-edge striking visual (cropped precisely), while the right two-thirds act as a high-negative-space canvas housing a clean, modern horizontal bar chart.
* **Why Use This Skill (Rationale)**: Based on the tutorial's core principles, humans struggle to parse raw numbers in bulleted lists (clutter) and ignore unanchored text. By combining **Tip 1 (Visualize Data)**, **Tip 2 (Use White Space)**, and **Tip 5 (Rule of Thirds)**, the slide effortlessly guides the eye from the emotional anchor (the image on the left vertical third) to the logical anchor (the chart on the right vertical third).
* **Overall Applicability**: Perfect for survey results, customer satisfaction metrics, product feature comparisons, and executive summaries where qualitative impact must be paired with quantitative proof.
* **Value Addition**: Transforms a dense, "read-only" slide into a highly legible, scannable "billboard" that commands attention and makes data immediately comprehensible.

### 2. Visual Breakdown

* **Step A: Core Visual Elements**
  - **Color Logic**: Minimalist foundation with a single strong accent. 
    - Background: Pure White `(255, 255, 255)` or Off-White `(245, 247, 250)`
    - Primary Text: Charcoal `(51, 51, 51)`
    - Data/Accent: Teal/Mint `(56, 178, 172)` — used specifically to draw attention to the data visualization.
  - **Text Hierarchy**: 
    - Headline: Very large, bold, placed exactly on the upper horizontal third line.
    - Data Labels: Large, placed at the end of chart bars (no complex Y-axis scales).

* **Step B: Compositional Style**
  - **Left Third (0% to 33% width)**: A full-bleed photographic anchor. 
  - **Right Two-Thirds (33% to 100% width)**: Bountiful white space. The text and chart begin around the 50% width mark, ensuring the space between the image and the text acts as a breathing zone.
  - **Data Visualization**: Bullet points are stripped away. A native horizontal bar chart is used, completely stripped of its legend, gridlines, and borders to look like native graphical shapes rather than an Excel import.

* **Step C: Dynamic Effects & Transitions**
  - **Morph Transition (PowerPoint native)**: If the image remains constant while the chart on the right changes across slides, applying a Morph transition creates a seamless "dashboard" feel. (Must be set natively in PPT).

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| **Rule of Thirds Image Cropping** | `PIL/Pillow` | Native PowerPoint image insertion can distort aspect ratios. PIL mathematically crops the image to exactly `16:27` (one-third of a 16:9 slide) before insertion. |
| **Data Visualization** | `python-pptx` Chart API | The tutorial emphasizes converting text to charts. Building a native `BAR_CLUSTERED` chart allows it to be editable and styled programmatically (removing axes and gridlines). |
| **White Space & Layout** | `python-pptx` native | Precise geometric placement using Inches to enforce the 1/3 and 2/3 grid alignments. |

> **Feasibility Assessment**: 95%. The code fully replicates the translation of bullet points into a clean data chart, the rule of thirds image anchoring, and the minimalist white space layout.

#### 3b. Complete Reproduction Code

```python
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
```