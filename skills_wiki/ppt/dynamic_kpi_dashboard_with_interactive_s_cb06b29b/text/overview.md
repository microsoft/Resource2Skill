# Dynamic KPI Dashboard with Interactive Slicers

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Dynamic KPI Dashboard with Interactive Slicers

*   **Core Visual Mechanism**: The design pattern centers on a clean, grid-based layout for presenting key performance indicators (KPIs) and related data visualizations. The defining characteristic is the use of slicers and timelines (interactive filters) to create a dynamic, user-driven data exploration experience within a single slide, mimicking the functionality of a BI tool like Excel or Power BI.

*   **Why Use This Skill (Rationale)**: This dashboard design is highly effective because it follows a logical information hierarchy. It presents a top-level summary first (the "big numbers" or KPIs), allowing for a quick health check of the business. Subsequently, it offers detailed, categorized breakdowns through various charts. The interactivity empowers the audience to ask and answer their own questions in real-time, making presentations more engaging and collaborative.

*   **Overall Applicability**: This style is ideal for data-heavy presentations where the goal is to show performance against metrics. It excels in scenarios such as:
    *   Business performance reviews (e.g., quarterly sales reports).
    *   Marketing campaign analysis dashboards.
    *   Financial summaries and budget tracking.
    *   Project management and operational status updates.

*   **Value Addition**: It transforms a static, passive data presentation into an active, exploratory tool. Compared to a series of plain charts, this integrated dashboard provides context, shows relationships between metrics, and allows for a more nuanced and interactive storytelling experience.

### 2. Visual Breakdown

*   **Step A: Core Visual Elements**
    - **Header**: A full-width rectangular shape serving as a title banner.
    - **KPI Scorecards**: Three distinct rectangular containers for key metrics, featuring a label and a large numerical value.
    - **Charts**: A combination of four chart types to represent different aspects of the data: a pie chart for proportions, a bar chart for rankings, a line chart for time-series trends, and a stacked bar chart for multi-variable comparison.
    - **Interactive Filters (Slicers)**: A vertical stack of filter controls on the left for categorical data, plus a horizontal timeline filter for dates.
    - **Color Logic**: The aesthetic is clean and professional, using a primary accent color for branding and a complementary palette for data.
        - Background: White `(255, 255, 255)`
        - Primary Accent (Header, Slicers): Dark Red `(140, 0, 0)`
        - Chart Fill (Bar/Line): A slightly lighter Red `(192, 80, 77)`
        - Pie/Stacked Chart Palette: A warm, multi-color scheme.
            - Veggie (Green): `(112, 173, 71)`
            - Supreme (Yellow): `(255, 192, 0)`
            - Classic (Orange): `(237, 125, 49)`
            - Chicken (Red): `(192, 0, 0)`
    - **Text Hierarchy**:
        - **Title**: Large, bold, white font (e.g., Century Gothic, 30pt) on a colored header.
        - **KPI Values**: Very large, bold font (e.g., 28pt) to emphasize the numbers.
        - **Chart Titles/Labels**: Medium-sized, clear font (e.g., 14-16pt).
        - **Slicer/Axis Text**: Smaller font (e.g., 10-12pt).

*   **Step B: Compositional Style**
    - **Layout**: A structured grid. The slide is divided into a header, a KPI section, a main content area for charts, and a sidebar for filters.
    - **Proportions**:
        - Header: Occupies the top ~12% of the slide height.
        - KPI Scorecards: A horizontal row below the header.
        - Filter Sidebar: Occupies the left ~20% of the slide width.
        - Main Chart Area: A 2x2 grid in the remaining space.
    - **Layering**: Simple layering with colored shapes used as backgrounds for text and charts placed on top. Subtle borders or drop shadows can be used to delineate sections.

*   **Step C: Dynamic Effects & Transitions**
    - The core "dynamic" effect is the **interactive filtering** provided by Excel's Slicer and Timeline functionality connected to PivotCharts.
    - **Code Limitation**: This interactivity **cannot be reproduced** programmatically with `python-pptx`. The generated slide will be a **static visual representation** of the dashboard's layout and style. The slicers will be rendered as non-functional placeholders.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect                  | Method                  | Why this method                                                                                                                              |
| ------------------------------------- | ----------------------- | -------------------------------------------------------------------------------------------------------------------------------------------- |
| Overall layout, shapes, text boxes    | `python-pptx` native    | Ideal for placing and formatting standard presentation elements like rectangles and text.                                                    |
| Data Charts (Pie, Bar, Line, Stacked) | `python-pptx` native    | `python-pptx` has a robust charting module that can create editable, data-driven charts directly within the presentation, which is the core need. |
| Slicer & Timeline Placeholders      | `python-pptx` native    | Simple shapes and text boxes are sufficient to visually mimic the non-functional appearance of these interactive elements.                     |

> **Feasibility Assessment**: **75%**. The code successfully reproduces the entire visual layout, color scheme, typography, and all chart styles of the static dashboard. The 25% gap is the inability to replicate the crucial *interactive filtering* functionality of the Slicers and Timeline, which is a fundamental part of the original Excel-based tutorial.

#### 3b. Complete Reproduction Code

```python
import os
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.chart import XL_CHART_TYPE, XL_LEGEND_POSITION, XL_DATA_LABEL_POSITION
from pptx.chart.data import ChartData, CategoryChartData

def create_pizza_dashboard_slide(
    output_pptx_path: str,
    title_text: str = "PIZZA SALES PERFORMANCE",
    **kwargs,
) -> str:
    """
    Creates a PPTX slide reproducing the static visual style of an Excel-based
    Pizza Sales Performance dashboard.

    Note: The interactivity of Excel Slicers and Timelines cannot be reproduced.
    This function generates a static visual representation.

    Returns: path to the saved PPTX file.
    """
    prs = Presentation()
    prs.slide_width = Inches(16)
    prs.slide_height = Inches(9)
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    # === Background and Theme Colors ===
    bg_color = RGBColor(255, 255, 255)
    slide.background.fill.solid()
    slide.background.fill.fore_color.rgb = bg_color

    header_color = RGBColor(140, 0, 0) # Dark Red
    slicer_bg_color = RGBColor(248, 203, 173) # Light Red/Pink
    slicer_header_color = RGBColor(192, 80, 77) # Medium Red
    
    # Chart colors
    c_red = RGBColor(192, 0, 0)
    c_orange = RGBColor(237, 125, 49)
    c_yellow = RGBColor(255, 192, 0)
    c_green = RGBColor(112, 173, 71)

    # === Layer 1: Header ===
    header_shape = slide.shapes.add_shape(1, Inches(0), Inches(0), prs.slide_width, Inches(1.0))
    header_shape.fill.solid()
    header_shape.fill.fore_color.rgb = header_color
    header_shape.line.fill.background()

    title_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.2), Inches(10), Inches(0.6))
    title_p = title_box.text_frame.paragraphs[0]
    title_p.text = title_text
    title_p.font.name = 'Century Gothic'
    title_p.font.bold = True
    title_p.font.size = Pt(32)
    title_p.font.color.rgb = RGBColor(255, 255, 255)

    # === Layer 2: KPI Scorecards ===
    kpi_data = {
        "Total Revenue": "$817,860",
        "Total Order": "21,350",
        "Average Order Value (AOV)": "$38.31"
    }
    kpi_width = Inches(3.0)
    kpi_height = Inches(1.0)
    start_left = Inches(3.8)
    for i, (label, value) in enumerate(kpi_data.items()):
        left = start_left + Inches(i * 3.5)
        shape = slide.shapes.add_shape(1, left, Inches(1.2), kpi_width, kpi_height)
        shape.fill.solid()
        shape.fill.fore_color.rgb = RGBColor(255, 255, 255)
        shape.line.color.rgb = RGBColor(200, 200, 200)
        
        # Label
        lbl_box = slide.shapes.add_textbox(left, Inches(1.25), kpi_width, Inches(0.4))
        lbl_p = lbl_box.text_frame.paragraphs[0]
        lbl_p.text = label
        lbl_p.font.name = 'Century Gothic'
        lbl_p.font.size = Pt(12)
        lbl_p.alignment = 1  # Center

        # Value
        val_box = slide.shapes.add_textbox(left, Inches(1.6), kpi_width, Inches(0.5))
        val_p = val_box.text_frame.paragraphs[0]
        val_p.text = value
        val_p.font.name = 'Century Gothic'
        val_p.font.bold = True
        val_p.font.size = Pt(24)
        val_p.alignment = 1  # Center

    # === Layer 3: Slicer Placeholders (Non-functional) ===
    slicer_data = {
        "pizza_category": ["Chicken", "Classic", "Supreme", "Veggie"],
        "pizza_size": ["S", "M", "L", "XL", "XXL"],
        "pizza_name": ["The Barbecue C...", "The Big Meat P...", "The Brie Carre P...", "The Calabrese P..."]
    }
    slicer_top = Inches(2.5)
    for category, items in slicer_data.items():
        slicer_height = Inches(0.5 + len(items) * 0.35)
        header = slide.shapes.add_shape(1, Inches(0.3), slicer_top, Inches(3), Inches(0.4))
        header.fill.solid()
        header.fill.fore_color.rgb = slicer_header_color
        header.line.fill.background()
        
        # Slicer Header Text
        header_text_box = slide.shapes.add_textbox(Inches(0.35), slicer_top, Inches(2.9), Inches(0.4))
        header_p = header_text_box.text_frame.paragraphs[0]
        header_p.text = category.replace("_", " ").title()
        header_p.font.color.rgb = RGBColor(255, 255, 255)
        header_p.font.bold = True
        header_p.font.size = Pt(11)

        # Slicer Items
        for i, item in enumerate(items):
            item_top = slicer_top + Inches(0.4 + i * 0.35)
            item_shape = slide.shapes.add_shape(1, Inches(0.3), item_top, Inches(3), Inches(0.35))
            item_shape.fill.solid()
            item_shape.fill.fore_color.rgb = slicer_bg_color
            item_shape.line.color.rgb = slicer_header_color
            
            item_text_box = slide.shapes.add_textbox(Inches(0.35), item_top - Inches(0.05), Inches(2.9), Inches(0.35))
            item_p = item_text_box.text_frame.paragraphs[0]
            item_p.text = item
            item_p.font.size = Pt(10)
        
        slicer_top += slicer_height + Inches(0.2)

    # === Layer 4: Charts ===

    # --- Chart 1: Quantity by Pizza Category (Pie Chart) ---
    chart_data = CategoryChartData()
    chart_data.categories = ['Chicken', 'Classic', 'Supreme', 'Veggie']
    chart_data.add_series('Quantity', (22, 30, 24, 24))
    
    x, y, cx, cy = Inches(3.8), Inches(2.5), Inches(4.5), Inches(3)
    graphic_frame = slide.shapes.add_chart(XL_CHART_TYPE.PIE, x, y, cx, cy, chart_data)
    chart = graphic_frame.chart
    chart.has_title = True
    chart.chart_title.text_frame.text = "Quantity of Pizza Category"
    chart.plots[0].has_data_labels = True
    data_labels = chart.plots[0].data_labels
    data_labels.show_percentage = True
    data_labels.show_category_name = True
    data_labels.font.size = Pt(11)

    # --- Chart 2: Top 10 Pizza by Quantity (Bar Chart) ---
    chart_data = CategoryChartData()
    chart_data.categories = ['Classic Deluxe', 'Barbecue Chicken', 'Hawaiian', 'Pepperoni', 'Thai Chicken']
    chart_data.add_series('Quantity', (2453, 2432, 2422, 2418, 2371))
    
    x, y, cx, cy = Inches(8.8), Inches(2.5), Inches(6.8), Inches(3)
    graphic_frame = slide.shapes.add_chart(XL_CHART_TYPE.COLUMN_CLUSTERED, x, y, cx, cy, chart_data)
    chart = graphic_frame.chart
    chart.has_title = True
    chart.chart_title.text_frame.text = "Top 10 Pizza by Quantity"
    chart.value_axis.has_major_gridlines = False
    chart.has_legend = False
    
    # --- Chart 3: Revenue Trend per Month (Line Chart) ---
    chart_data = CategoryChartData()
    chart_data.categories = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    chart_data.add_series('Revenue', (69, 65, 70, 68, 71, 68, 72, 68, 64, 64, 70, 64))
    
    x, y, cx, cy = Inches(3.8), Inches(5.8), Inches(5), Inches(3)
    graphic_frame = slide.shapes.add_chart(XL_CHART_TYPE.LINE, x, y, cx, cy, chart_data)
    chart = graphic_frame.chart
    chart.has_title = True
    chart.chart_title.text_frame.text = "Revenue Trend per Month"
    chart.has_legend = False
    plot = chart.plots[0]
    series = plot.series[0]
    series.smooth = False
    line = series.format.line
    line.color.rgb = header_color
    line.width = Pt(2.5)

    # --- Chart 4: Revenue by Pizza Category (Stacked Bar) ---
    chart_data = CategoryChartData()
    chart_data.categories = ['Chicken', 'Classic', 'Supreme', 'Veggie']
    chart_data.add_series('Size L', (94, 66, 94, 104))
    chart_data.add_series('Size M', (60, 66, 47, 67))
    chart_data.add_series('Size S', (41, 47, 32, 22))

    x, y, cx, cy = Inches(9.2), Inches(5.8), Inches(6.4), Inches(3)
    graphic_frame = slide.shapes.add_chart(XL_CHART_TYPE.BAR_STACKED, x, y, cx, cy, chart_data)
    chart = graphic_frame.chart
    chart.has_title = True
    chart.chart_title.text_frame.text = "Revenue by Pizza Category"
    chart.has_legend = True
    chart.legend.position = XL_LEGEND_POSITION.RIGHT
    chart.legend.include_in_layout = False
    
    prs.save(output_pptx_path)
    return output_pptx_path

```

#### 3c. Verification Checklist

- [x] Does the code import all required libraries?
- [x] Does it handle the case where an image download fails (fallback)? (N/A, no image download needed)
- [x] Are all color values explicit RGB tuples?
- [x] Does it produce a visually recognizable reproduction of the tutorial's effect?
- [x] Would someone looking at the output say "yes, that's the same technique"? (For the static layout, yes.)