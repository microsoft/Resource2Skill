# Color-Coded KPI Scorecard

## Analysis

### 1. High-level Design Pattern Extraction

> **Skill Name**: Color-Coded KPI Scorecard

*   **Core Visual Mechanism**: The design is a structured grid of "scorecard" blocks, each representing a single Key Performance Indicator (KPI). The block's background color (typically green for good, red for bad) instantly communicates the status of that KPI against its target. Each block features a large, bold metric number as the focal point, a descriptive title, and smaller text showing comparisons (e.g., vs. Target, vs. Prior Period).

*   **Why Use This Skill (Rationale)**: This technique leverages pre-attentive visual attributes, primarily color, to enable rapid assessment of business health. A viewer can identify problem areas (red blocks) in seconds without needing to read every number. The consistent, modular structure allows for high information density and easy comparability across different metrics.

*   **Overall Applicability**: This style is highly effective for:
    *   Monthly or quarterly business review dashboards.
    *   Executive summary slides.
    *   Project status reports.
    *   Financial performance snapshots.

*   **Value Addition**: It transforms a simple list or table of numbers into a compelling visual story of performance. By immediately highlighting positive and negative trends, it directs the audience's attention to the most critical information, facilitating faster decision-making.

### 2. Visual Breakdown

*   **Step A: Core Visual Elements**
    - **Category Headers**: Wide, solid-colored rectangular bars that group related KPIs. Text is typically white and bold.
    - **KPI Blocks**: Rounded rectangles containing all information for a single KPI.
    - **Color Logic**:
        - **Good/On-Target**: Light Green (e.g., `(226, 240, 217)`).
        - **Bad/Off-Target**: Light Red/Pink (e.g., `(255, 230, 230)`).
        - **Category Headers**: Strong, distinct colors to separate sections (e.g., Gray `(115, 115, 115)`, Blue `(68, 114, 196)`, Red `(192, 0, 0)`).
        - **Text**: Dark Gray/Black `(64, 64, 64)` for high readability.
    - **Text Hierarchy**:
        1.  **KPI Value**: Extra-large, bold font (e.g., Arial Black, 40pt). This is the hero element.
        2.  **Category Title**: Medium-large, bold font, white.
        3.  **KPI Title**: Small-medium font, regular weight, placed at the top of the block.
        4.  **Comparison Labels & Values**: Smallest font size, regular weight, located in the footer of the block.

*   **Step B: Compositional Style**
    - **Grid-Based Layout**: The KPI blocks are arranged in a clean, structured grid with consistent horizontal and vertical spacing (gutters). This creates a sense of order and professionalism.
    - **Flat Design**: The aesthetic is modern and flat, avoiding gradients, shadows, or 3D effects.
    - **Visual Separation**: Thin horizontal lines are used within each block to separate the main metric from the comparison data in the footer.

*   **Step C: Dynamic Effects & Transitions**
    - The primary "dynamic" effect is the data-driven conditional coloring of the KPI blocks.
    - The tutorial demonstrates changing the month via a dropdown, which updates all values. This functionality is reproduced by passing different data sets into the slide generation code. No animations or slide transitions are required.

### 3. Reproduction Code

#### 3a. Implementation Method Selection

| Aspect of the effect | Method | Why this method |
|---|---|---|
| Main layout, text boxes, and shapes | `python-pptx` | This is the most direct and efficient way to create basic geometric shapes, position text, and set font properties. |
| Rounded corners for KPI blocks | `python-pptx` | The `add_shape` method with `MSO_SHAPE.ROUNDED_RECTANGLE` and adjustment properties natively supports this. |
| Conditional background coloring | Python Logic | The color of each KPI block is determined by a simple `if/else` condition within the Python code before the shape is drawn. This is more robust than trying to manipulate a pre-existing slide. |

> **Feasibility Assessment**: 100%. This design is based on fundamental shapes, text, and color, all of which are fully controllable via the `python-pptx` library. The logic for conditional coloring is straightforward to implement in Python.

#### 3b. Complete Reproduction Code

```python
import collections.abc
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.shapes import MSO_SHAPE
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.dml import MSO_THEME_COLOR

def create_kpi_dashboard_slide(
    output_pptx_path: str,
    kpi_data: dict,
    slide_title: str = "KPI Dashboard",
    month_str: str = "Feb-20"
) -> str:
    """
    Creates a PPTX file with a single, professionally styled KPI Dashboard slide.

    The slide features color-coded blocks that visually represent the status of each KPI
    (green for good, red for bad) based on its performance against a target.

    Args:
        output_pptx_path (str): The path to save the generated PPTX file.
        kpi_data (dict): A nested dictionary containing the KPI data. Each KPI should
                         include 'value', 'target', 'prior', and a boolean 'higher_is_better'.
        slide_title (str): The main title for the dashboard.
        month_str (str): The string representing the current period (e.g., "Feb-20").

    Returns:
        str: The path to the saved PPTX file.
    """
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_slide_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(blank_slide_layout)

    # --- Colors & Fonts ---
    COLOR_GOOD = RGBColor(226, 240, 217)
    COLOR_BAD = RGBColor(255, 230, 230)
    COLOR_HEADER_WC = RGBColor(115, 115, 115)
    COLOR_HEADER_SALES = RGBColor(68, 114, 196)
    COLOR_HEADER_COST = RGBColor(192, 0, 0)
    FONT_COLOR_DARK = RGBColor(64, 64, 64)
    FONT_COLOR_LIGHT = RGBColor(255, 255, 255)

    def _add_kpi_block(slide, left, top, width, height, title, value, target, prior, value_prefix="", value_suffix="", higher_is_better=True):
        kpi_block = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        kpi_block.adjustments[0] = 0.1

        is_good = (value >= target) if higher_is_better else (value <= target)
        block_fill = kpi_block.fill
        block_fill.solid()
        block_fill.fore_color.rgb = COLOR_GOOD if is_good else COLOR_BAD
        
        line = kpi_block.line
        line.fill.solid()
        line.fill.fore_color.rgb = RGBColor(200, 200, 200)
        line.width = Pt(0.75)

        title_box = slide.shapes.add_textbox(left, top + Inches(0.1), width, Inches(0.4))
        p_title = title_box.text_frame.paragraphs[0]
        p_title.text = title
        p_title.font.name = 'Arial'
        p_title.font.size = Pt(11)
        p_title.font.color.rgb = FONT_COLOR_DARK
        p_title.alignment = PP_ALIGN.CENTER

        value_box = slide.shapes.add_textbox(left, top + Inches(0.4), width, height - Inches(1.1))
        p_value = value_box.text_frame.paragraphs[0]
        formatted_value = f"{value:,.0f}" if value_prefix != '$' else f"${value:,.0f}"
        if '%' in value_suffix: formatted_value = f"{value:.0f}%"
        p_value.text = formatted_value
        p_value.font.name = 'Arial Black'
        p_value.font.size = Pt(40)
        p_value.font.color.rgb = FONT_COLOR_DARK
        p_value.alignment = PP_ALIGN.CENTER
        value_box.text_frame.vertical_anchor = 3

        line_top = top + height - Inches(0.55)
        line_shape = slide.shapes.add_shape(MSO_SHAPE.LINE_INVERSE, left + Inches(0.2), line_top, width - Inches(0.4), 0)
        line_shape.line.fill.solid()
        line_shape.line.fill.fore_color.rgb = RGBColor(180, 180, 180)
        line_shape.line.width = Pt(0.5)
        
        for i, (label, val) in enumerate([("Vs. Target", target), ("Vs. Prior Month", prior)]):
            col_left = left + (width / 2 * i)
            p_label = slide.shapes.add_textbox(col_left, line_top + Inches(0.05), width / 2, Inches(0.2)).text_frame.paragraphs[0]
            p_label.text = label
            p_label.font.size = Pt(9)
            p_label.font.color.rgb = FONT_COLOR_DARK
            p_label.alignment = PP_ALIGN.CENTER
            
            p_val = slide.shapes.add_textbox(col_left, line_top + Inches(0.25), width / 2, Inches(0.2)).text_frame.paragraphs[0]
            formatted_val = f"{val:,.0f}" if value_prefix != '$' else f"${val:,.0f}"
            if '%' in value_suffix: formatted_val = f"{val:.0f}%"
            p_val.text = formatted_val
            p_val.font.size = Pt(9)
            p_val.font.color.rgb = FONT_COLOR_DARK
            p_val.alignment = PP_ALIGN.CENTER

    # --- Layout ---
    BLOCK_WIDTH, BLOCK_HEIGHT = Inches(3.8), Inches(1.9)
    H_GUTTER, V_GUTTER = Inches(0.3), Inches(0.8)
    START_LEFT, current_top = Inches(0.8), Inches(1.3)

    categories = [
        ("Working Capital Efficiency", COLOR_HEADER_WC, ["DSO", "DPO", "Non-Current AR %"]),
        ("Sales KPIs", COLOR_HEADER_SALES, ["CAC", "Sales vs. Budget%", "Gross Margin"]),
        ("Cost KPIs", COLOR_HEADER_COST, ["OPEX Actual vs. Budget", "CPFTE"]),
    ]

    for title, color, kpis in categories:
        header = slide.shapes.add_textbox(START_LEFT, current_top, prs.slide_width - 2*START_LEFT, Inches(0.4))
        header.fill.solid()
        header.fill.fore_color.rgb = color
        p_h = header.text_frame.paragraphs[0]
        p_h.text = title
        p_h.font.bold = True
        p_h.font.color.rgb = FONT_COLOR_LIGHT
        p_h.alignment = PP_ALIGN.CENTER
        current_top += Inches(0.5)

        for i, kpi_name in enumerate(kpis):
            data = kpi_data[kpi_name]
            block_left = START_LEFT + i * (BLOCK_WIDTH + H_GUTTER)
            _add_kpi_block(slide, block_left, current_top, BLOCK_WIDTH, BLOCK_HEIGHT,
                           data['title'], data['value'], data['target'], data['prior'],
                           data.get('prefix', ''), data.get('suffix', ''), data['higher_is_better'])
        current_top += BLOCK_HEIGHT + V_GUTTER

    prs.save(output_pptx_path)
    return output_pptx_path

if __name__ == '__main__':
    # Example data mirroring the video for February 2020
    # The 'higher_is_better' flag is crucial for correct color-coding
    sample_data = {
        'DSO': {'title': "DSO (Days Sales Outstanding)", 'value': 54, 'target': 45, 'prior': 58, 'higher_is_better': False},
        'DPO': {'title': "DPO (Days Payables Outstanding)", 'value': 99, 'target': 90, 'prior': 107, 'higher_is_better': True},
        'Non-Current AR %': {'title': "Non-Current AR %", 'value': 5, 'target': 3, 'prior': 5, 'suffix': '%', 'higher_is_better': False},
        'CAC': {'title': "CAC (Customer Acquisition Cost)", 'value': 14444, 'target': 15000, 'prior': 13750, 'prefix': '$', 'higher_is_better': False},
        'Sales vs. Budget%': {'title': "Sales vs. Budget%", 'value': 92, 'target': 100, 'prior': 91, 'suffix': '%', 'higher_is_better': True},
        'Gross Margin': {'title': "Gross Margin", 'value': 40, 'target': 38, 'prior': 40, 'suffix': '%', 'higher_is_better': True},
        'OPEX Actual vs. Budget': {'title': "OPEX Actual vs. Budget", 'value': 106, 'target': 100, 'prior': 109, 'suffix': '%', 'higher_is_better': False},
        'CPFTE': {'title': "CPFTE (Cost Per Full Time Employee)", 'value': 13032, 'target': 12500, 'prior': 13344, 'prefix': '$', 'higher_is_better': False}
    }
    
    create_kpi_dashboard_slide("kpi_dashboard_reproduction.pptx", sample_data)
    print("KPI Dashboard slide created successfully at 'kpi_dashboard_reproduction.pptx'")
```

#### 3c. Verification Checklist

- [x] Does the code import all required libraries?
- [x] Does it handle the case where an image download fails (fallback)? (N/A)
- [x] Are all color values explicit RGBA tuples (not referencing undefined variables)?
- [x] Does it produce a visually recognizable reproduction of the tutorial's effect?
- [x] Would someone looking at the output say "yes, that's the same technique"?