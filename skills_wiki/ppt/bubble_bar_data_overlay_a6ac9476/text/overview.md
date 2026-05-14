# Bubble Bar Data Overlay

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Bubble Bar Data Overlay

*   **Core Visual Mechanism**: This design overlays a series of size-encoded bubbles on a horizontal bar chart. The bar chart visualizes primary absolute metrics (e.g., total revenue and a component like profit), while the bubbles, aligned with each category bar, represent a third, often ratio-based, metric (e.g., profit margin). The bubble's size and its central label provide an intuitive, at-a-glance comparison layer.

*   **Why Use This Skill (Rationale)**: It is a highly efficient method for displaying three related data points per category in a single, compact visualization. The bar chart establishes a clear baseline for absolute values, while the bubble overlay adds a third dimension of data without the clutter of a second chart. This combination facilitates the quick identification of key insights, such as categories with high revenue but low margins.

*   **Overall Applicability**: Ideal for business performance dashboards, financial reports, and product analysis slides where viewers need to compare absolute values alongside a key performance ratio. Examples include:
    *   Product Sales Analysis (Revenue, Profit, Profit Margin)
    *   Regional Performance (Sales Target, Actual Sales, % Achieved)
    *   Marketing Campaigns (Budget, Spend, Return on Investment)

*   **Value Addition**: Compared to separate charts or a table, this style condenses three dimensions of data into a two-dimensional space, making complex relationships easier to grasp. It is visually engaging and effectively directs the viewer's attention to the interplay between absolute numbers and efficiency rates.

### 2. Visual Breakdown

*   **Step A: Core Visual Elements**
    *   **Bar Chart**: A horizontal bar chart styled to appear stacked.
        *   **Total Value Bar (e.g., Revenue)**: A base bar with a lighter color, representing the total. Color: Light Blue `(155, 194, 230, 255)`.
        *   **Component Value Bar (e.g., Profit)**: A shorter bar layered on top of the total bar, with a darker, more prominent color. Color: Dark Blue `(47, 117, 181, 255)`.
    *   **Bubbles**: Circular shapes aligned in a column to the right of the bars.
        *   The **size** of each bubble is proportional to the third metric (Profit Rate).
        *   The **color** is a distinct but harmonious accent. Color: Bright Cyan `(79, 178, 222, 255)`.
    *   **Labels**:
        *   Category labels (e.g., "Product F") on the vertical axis.
        *   Data labels for Profit are white and centered on the dark blue bars.
        *   Data labels for Revenue are dark gray and positioned at the end of the light blue bars.
        *   Data labels for Profit Rate are white, bold, and centered within each bubble.
    *   **Text Hierarchy**: Chart title is largest, followed by category labels, then data labels.

*   **Step B: Compositional Style**
    *   The layout is clean, structured, and analytical. The bar chart occupies about 60-70% of the horizontal space on the left.
    *   The bubbles are aligned in a neat vertical column on the right, creating a dedicated zone for the ratio metric.
    *   There are no visible axes lines or gridlines, reducing visual clutter.
    *   The vertical axis is reversed, so the first data item appears at the top of the chart.

*   **Step C: Dynamic Effects & Transitions**
    *   The original tutorial presents a static chart with no animations. This is fully reproducible in code.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| Overlapped Bar Chart | `python-pptx` native chart | The "stacked" effect is achieved by creating a `BAR_CLUSTERED` chart and setting the series overlap to 100%. This is a standard and reliable technique. |
| Bubbles (Sized & Labeled) | `python-pptx` native shapes | Since a direct bar-and-bubble combo chart isn't a standard type, we programmatically draw `MSO_SHAPE.OVAL` shapes. This gives full control over size, position, and color. The size is scaled based on the data, and the position is calculated to align with each bar. |
| Data Labels & Layout | `python-pptx` native | Chart data labels are a built-in feature. Overall layout and the chart title are handled with standard `python-pptx` objects. |

> **Feasibility Assessment**: 100%. This entire visual effect can be faithfully reproduced using the `python-pptx` library by combining a formatted chart object with programmatically generated shapes. No external libraries or XML manipulation are required.

#### 3b. Complete Reproduction Code

```python
import pandas as pd
from pptx import Presentation
from pptx.chart.data import ChartData
from pptx.enum.chart import XL_CHART_TYPE, XL_LEGEND_POSITION, XL_DATA_LABEL_POSITION
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_VERTICAL_ANCHOR, PP_ALIGN

def create_slide(
    output_pptx_path: str,
    chart_data: dict,
    title_text: str = "Bubble Bar Chart",
    **kwargs,
) -> str:
    """
    Creates a PPTX file reproducing the Bubble Bar Data Overlay visual effect.

    The function generates a slide containing a horizontal bar chart where one series
    (e.g., Profit) is overlaid on another (e.g., Revenue). To the right of each bar,
    a bubble is placed, with its size and label corresponding to a third metric (e.g., Profit Rate).

    Args:
        output_pptx_path: Path to save the output .pptx file.
        chart_data: A dictionary containing the data for the chart.
                    Expected format: {'Category': [...], 'Revenue': [...], 'Profit': [...]}.
                    'ProfitRate' will be calculated from this data.
        title_text: The main title for the chart.

    Returns:
        Path to the saved PPTX file.
    """
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    slide_layout = prs.slide_layouts[6]  # Blank layout
    slide = prs.slides.add_slide(slide_layout)

    # === Layer 1: Data Preparation ===
    df = pd.DataFrame(chart_data)
    df['ProfitRate'] = df['Profit'] / df['Revenue']
    df = df.sort_values(by='Revenue', ascending=True) # Sort for visual order in chart
    categories = df['Category'].tolist()
    
    chart_data_obj = ChartData()
    chart_data_obj.categories = categories
    chart_data_obj.add_series('Revenue', df['Revenue'].tolist())
    chart_data_obj.add_series('Profit', df['Profit'].tolist())

    # === Layer 2: Bar Chart ===
    x, y, cx, cy = Inches(1.0), Inches(1.25), Inches(8), Inches(5.5)
    graphic_frame = slide.shapes.add_chart(
        XL_CHART_TYPE.BAR_CLUSTERED, x, y, cx, cy, chart_data_obj
    )
    chart = graphic_frame.chart

    # Format plot area
    chart.plot_area.format.fill.background()
    chart.plot_area.format.line.fill.background()
    
    # Format category axis (Y-axis)
    category_axis = chart.category_axis
    category_axis.tick_labels.font.size = Pt(12)
    category_axis.format.line.fill.background()
    category_axis.reverse_order = True

    # Format value axis (X-axis)
    value_axis = chart.value_axis
    value_axis.has_major_gridlines = False
    value_axis.visible = False

    # Format series
    series_revenue = chart.series[0]
    series_revenue.fill.solid()
    series_revenue.fill.fore_color.rgb = RGBColor(155, 194, 230)
    series_revenue.has_data_labels = True
    data_labels_revenue = series_revenue.data_labels
    data_labels_revenue.position = XL_DATA_LABEL_POSITION.INSIDE_END
    data_labels_revenue.font.size = Pt(11)
    data_labels_revenue.font.color.rgb = RGBColor(89, 89, 89)

    series_profit = chart.series[1]
    series_profit.fill.solid()
    series_profit.fill.fore_color.rgb = RGBColor(47, 117, 181)
    series_profit.has_data_labels = True
    data_labels_profit = series_profit.data_labels
    data_labels_profit.position = XL_DATA_LABEL_POSITION.CENTER
    data_labels_profit.font.size = Pt(11)
    data_labels_profit.font.color.rgb = RGBColor(255, 255, 255)
    data_labels_profit.font.bold = True

    # Overlap series and set gap width
    chart.plot_area.cat_groupings[0].overlap = 100
    chart.plot_area.cat_groupings[0].gap_width = 80

    # Format Legend and Title
    chart.has_legend = True
    chart.legend.position = XL_LEGEND_POSITION.TOP
    chart.legend.include_in_layout = False
    chart.legend.font.size = Pt(12)
    chart.chart_title.text_frame.text = title_text
    chart.chart_title.text_frame.paragraphs[0].font.size = Pt(18)
    
    # === Layer 3: Bubbles ===
    num_categories = len(categories)
    plot_height_estimate = cy - Inches(0.5) # Estimate plot area height
    plot_y_start_estimate = y + Inches(0.25) # Estimate plot area top
    
    bubble_x_pos = x + cx + Inches(0.3)
    
    min_rate, max_rate = df['ProfitRate'].min(), df['ProfitRate'].max()
    min_bubble_size, max_bubble_size = Inches(0.4), Inches(0.9)

    for i, row in df.reset_index().iterrows():
        # Calculate Y position for the bubble, aligning with the bar center
        category_band_height = plot_height_estimate / num_categories
        bar_center_y = plot_y_start_estimate + (i * category_band_height) + (category_band_height / 2)
        
        rate = row['ProfitRate']
        scale_factor = (rate - min_rate) / (max_rate - min_rate) if (max_rate - min_rate) > 0 else 0.5
        bubble_diameter = min_bubble_size + (scale_factor * (max_bubble_size - min_bubble_size))
        bubble_y_pos = bar_center_y - (bubble_diameter / 2)
        
        bubble = slide.shapes.add_shape(
            MSO_SHAPE.OVAL, bubble_x_pos, bubble_y_pos, bubble_diameter, bubble_diameter
        )
        bubble.fill.solid()
        bubble.fill.fore_color.rgb = RGBColor(79, 178, 222)
        bubble.line.fill.background()
        
        text_frame = bubble.text_frame
        text_frame.clear()
        p = text_frame.paragraphs[0]
        p.text = f"{rate:.1%}"
        p.font.size = Pt(10)
        p.font.color.rgb = RGBColor(255, 255, 255)
        p.font.bold = True
        p.alignment = PP_ALIGN.CENTER
        text_frame.vertical_anchor = MSO_VERTICAL_ANCHOR.MIDDLE

    prs.save(output_pptx_path)
    return output_pptx_path

if __name__ == '__main__':
    # Example data from the tutorial
    tutorial_data = {
        'Category': ['产品 F', '产品 G', '产品 C', '产品 E', '产品 D', '产品 A', '产品 B'],
        'Revenue': [1916, 1843, 1839, 1820, 1614, 1612, 1304],
        'Profit': [188, 123, 385, 177, 163, 369, 200],
    }
    create_slide(
        output_pptx_path="bubble_bar_chart_reproduction.pptx",
        chart_data=tutorial_data,
        title_text="泡泡组合条形图类型"
    )

```

#### 3c. Verification Checklist

- [x] Does the code import all required libraries?
- [x] Does it handle the case where an image download fails (fallback)? (N/A - no image download)
- [x] Are all color values explicit RGB tuples?
- [x] Does it produce a visually recognizable reproduction of the tutorial's effect?
- [x] Would someone looking at the output say "yes, that's the same technique"?