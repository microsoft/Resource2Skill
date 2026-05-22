# Sub-Zero Axis Annotation

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Sub-Zero Axis Annotation

*   **Core Visual Mechanism**: The defining characteristic of this style is the manipulation of a chart's vertical axis to create a "sub-zero" region. By setting the axis's minimum bound to a negative value (e.g., -20%), the zero-baseline is shifted upwards, creating a dedicated, clean space at the bottom of the chart. This newly created space is then used for placing supplementary information, most effectively icons or short labels, that align with the chart's categories.

*   **Why Use This Skill (Rationale)**: This technique integrates annotations directly into the chart's structure, creating a stronger visual connection between the data and its context. Unlike a separate legend, placing icons directly beneath their corresponding data columns reduces the cognitive load on the viewer, making the chart more intuitive and faster to read. It transforms a standard chart into a more compelling infographic.

*   **Overall Applicability**: This style is highly effective for:
    *   **Dashboard Summaries**: When presenting categorical data where each category has a well-known icon (e.g., social media platforms, product types, departments).
    *   **Infographics**: Adding visual flair and clarity to data-driven stories.
    *   **Marketing & Sales Reports**: Quickly communicating performance across different channels or products.

*   **Value Addition**: Compared to a standard chart, this style adds a layer of professional polish and significantly improves information density without creating clutter. It makes the data visualization feel custom-built and thoughtfully designed.

### 2. Visual Breakdown

*   **Step A: Core Visual Elements**
    - **Background**: A full-bleed background image, typically thematic to the data, with a dark, semi-transparent color overlay. This creates depth and ensures text/data readability.
    - **Chart**: A clustered column chart is the most suitable type, comparing two or more series across several categories.
    - **Icons**: Simple, monochromatic line-art icons are placed in the "sub-zero" space, each centered below a category label.
    - **Color Logic**: A dark, muted background with high-contrast text and vibrant, distinct colors for the data series.
        - Background Overlay: Dark Blue/Purple, e.g., `(48, 35, 174, 180)` (RGBA, with alpha for transparency).
        - Series 1 (Male): Deep Blue/Black, e.g., `(25, 25, 112, 255)`.
        - Series 2 (Female): Bright Red/Magenta, e.g., `(226, 61, 100, 255)`.
        - Text & Icons: White, `(255, 255, 255, 255)`.
    - **Text Hierarchy**:
        - **Title**: Large, bold, top-left.
        - **Axis Labels**: Clean, sans-serif, smaller font size.
        - **Legend**: Unobtrusive, placed at the bottom.

*   **Step B: Compositional Style**
    - **Layering**: The slide is built in layers: Image (bottom), Color Overlay, Chart, Hiding Rectangle, Icons, and Text (top).
    - **Spatial Logic**: The chart dominates the slide. The key compositional trick is the vertical axis manipulation, which allocates approximately 15-20% of the chart's plot area height to the sub-zero annotation space.
    - **Alignment**: Icons and category labels are precisely vertically aligned, reinforcing the connection between the data and the symbol.

*   **Step C: Dynamic Effects & Transitions**
    - The core technique is a static design principle. Any animations (like fade-ins for the icons) would be applied manually in PowerPoint after the slide is generated. The code focuses on producing the final static layout.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| Background image with color overlay | PIL/Pillow & `urllib` | `python-pptx` cannot apply a transparent color overlay to an image. PIL is required for this image composition. `urllib` handles the image download. |
| Clustered column chart | `python-pptx` native | The library has robust support for creating and formatting standard charts. |
| **Axis min/max manipulation** | `python-pptx` native | The core of the technique—setting `minimum_scale` and `maximum_scale`—is directly supported by the `python-pptx` API for chart axes. |
| Hiding negative axis labels | `python-pptx` native shapes | The simplest and most reliable way to replicate the tutorial's "hack" is to draw a rectangle shape over the unwanted labels, filled with the background color. |
| Icon placement | `python-pptx` native shapes | Placeholder shapes (ovals) are used to demonstrate the positioning logic for icons. This is easily achieved with basic shape creation. |

> **Feasibility Assessment**: **90%**. The provided code fully reproduces the core technique: creating a sub-zero axis space, populating it with placeholders, and hiding negative labels. The only deviation from the video is the visual style of the data points; the video uses a custom triangular shape, while the code uses standard rectangular columns, which is the standard representation for this chart type. The fundamental design pattern is perfectly replicated.

#### 3b. Complete Reproduction Code

```python
import io
import urllib.request
from pptx import Presentation
from pptx.chart.data import CategoryChartData
from pptx.dml.color import RGBColor
from pptx.enum.chart import XL_CHART_TYPE, XL_LEGEND_POSITION
from pptx.enum.shapes import MSO_SHAPE
from pptx.util import Inches, Pt
from PIL import Image, ImageDraw

def create_slide(
    output_pptx_path: str,
    title_text: str = "PPT 柱狀圖",
    subtitle_text: str = "座標軸選項 (範圍最大值最小值)",
    bg_keyword: str = "fitness",
) -> str:
    """
    Creates a PPTX slide demonstrating the Sub-Zero Axis Annotation technique.

    This involves setting a chart's vertical axis to a negative minimum value
    to create space for icons below the zero baseline.

    Returns: path to the saved PPTX file.
    """
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    # === Style & Color Definitions ===
    BG_COLOR = (48, 35, 174)
    SERIES_1_COLOR = (25, 25, 112)
    SERIES_2_COLOR = (226, 61, 100)
    TEXT_COLOR = RGBColor(255, 255, 255)

    # === Layer 1: Background ===
    try:
        url = f"https://source.unsplash.com/1920x1080/?{bg_keyword}"
        with urllib.request.urlopen(url) as response:
            image_data = response.read()
        
        bg_image = Image.open(io.BytesIO(image_data)).convert("RGBA")
        overlay = Image.new("RGBA", bg_image.size, BG_COLOR + (180,)) # 180 alpha for ~70% opacity
        composite_bg = Image.alpha_composite(bg_image, overlay)

        with io.BytesIO() as output:
            composite_bg.save(output, format="PNG")
            slide.shapes.add_picture(output, 0, 0, width=prs.slide_width, height=prs.slide_height)
    except Exception:
        # Fallback to solid color if image download fails
        fill = slide.background.fill
        fill.solid()
        fill.fore_color.rgb = RGBColor(*BG_COLOR)

    # === Layer 2: Chart ===
    chart_data = CategoryChartData()
    chart_data.categories = ['跑步', '單車', '跳舞', '瑜珈', '重訓', '球類', '伸展']
    chart_data.add_series('男%', (0.45, 0.62, 0.37, 0.28, 0.66, 0.78, 0.34))
    chart_data.add_series('女%', (0.55, 0.38, 0.63, 0.72, 0.34, 0.22, 0.66))

    x, y, cx, cy = Inches(1), Inches(1.5), Inches(11.33), Inches(5)
    chart = slide.shapes.add_chart(
        XL_CHART_TYPE.COLUMN_CLUSTERED, x, y, cx, cy, chart_data
    ).chart

    chart.has_legend = True
    chart.legend.position = XL_LEGEND_POSITION.BOTTOM
    chart.legend.include_in_layout = False
    chart.legend.font.size = Pt(12)
    chart.legend.font.color.rgb = TEXT_COLOR

    # --- Core Technique: Manipulate Value Axis ---
    value_axis = chart.value_axis
    value_axis.minimum_scale = -0.2  # Set minimum to a negative value
    value_axis.maximum_scale = 0.8   # Set maximum based on data
    value_axis.has_major_gridlines = True
    value_axis.major_gridlines.format.line.color.rgb = RGBColor(255, 255, 255)
    value_axis.major_gridlines.format.line.width = Pt(0.5)
    value_axis.major_gridlines.format.line.dash_style = 2 # Dash

    # Format axis labels and lines
    value_axis.format.line.fill.background()
    value_axis.tick_labels.font.color.rgb = TEXT_COLOR
    value_axis.tick_labels.font.size = Pt(12)

    category_axis = chart.category_axis
    category_axis.format.line.fill.background()
    category_axis.tick_labels.font.color.rgb = TEXT_COLOR
    category_axis.tick_labels.font.size = Pt(14)
    
    # Format data series
    plot = chart.plots[0]
    plot.gap_width = 150
    series_1 = plot.series[0]
    series_1.format.fill.solid()
    series_1.format.fill.fore_color.rgb = RGBColor(*SERIES_1_COLOR)
    series_2 = plot.series[1]
    series_2.format.fill.solid()
    series_2.format.fill.fore_color.rgb = RGBColor(*SERIES_2_COLOR)

    # === Layer 3: Hide Negative Labels & Add Placeholders ===
    
    # Add a rectangle to hide the negative axis labels (-10%, -20%)
    # This is a robust approximation of the area.
    hiding_rect_left = x
    # The total vertical range is 1.0 (0.8 - (-0.2)). Negative part is 0.2, or 20%.
    # So we cover the bottom 20% of the chart's height.
    hiding_rect_top = y + cy * 0.82 
    hiding_rect_width = Inches(0.75)
    hiding_rect_height = cy * 0.18
    
    hider = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, 
        hiding_rect_left, 
        hiding_rect_top, 
        hiding_rect_width, 
        hiding_rect_height
    )
    hider.fill.solid()
    hider.fill.fore_color.rgb = RGBColor(*BG_COLOR)
    hider.line.fill.background()

    # Add icon placeholders in the newly created space
    num_categories = len(chart_data.categories)
    category_width = cx / num_categories
    icon_size = Inches(0.4)
    icon_y_pos = y + cy - Inches(0.5)

    for i in range(num_categories):
        icon_center_x = x + (i + 0.5) * category_width
        slide.shapes.add_shape(
            MSO_SHAPE.OVAL,
            left=icon_center_x - (icon_size / 2),
            top=icon_y_pos,
            width=icon_size,
            height=icon_size,
        ).fill.solid()
        # You could add custom icons here instead of ovals

    # === Layer 4: Text ===
    title_shape = slide.shapes.add_textbox(Inches(0.5), Inches(0.5), Inches(8), Inches(0.75))
    p = title_shape.text_frame.paragraphs[0]
    p.text = title_text
    p.font.bold = True
    p.font.size = Pt(32)
    p.font.color.rgb = TEXT_COLOR
    
    subtitle_shape = slide.shapes.add_textbox(Inches(0.5), Inches(1.0), Inches(8), Inches(0.5))
    p = subtitle_shape.text_frame.paragraphs[0]
    p.text = subtitle_text
    p.font.size = Pt(16)
    p.font.color.rgb = TEXT_COLOR


    prs.save(output_pptx_path)
    return output_pptx_path

# Example usage:
# create_slide("sub_zero_axis_chart.pptx")

```

#### 3c. Verification Checklist

- [x] Does the code import all required libraries?
- [x] Does it handle the case where an image download fails (fallback)?
- [x] Are all color values explicit RGB tuples?
- [x] Does it produce a visually recognizable reproduction of the tutorial's effect?
- [x] Would someone looking at the output say "yes, that's the same technique"?